import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("stats_top", Path(__file__).parents[1] / "top.py")
top = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(top)


def quietly(call, *argv):
    """argparse writes usage to stderr and main prints the path; neither is the test."""
    with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
        return call(list(argv))


def row(name, total, values, status="unsat", excluded=""):
    return {"benchmark": name, "status": status, "total": total, "values": values, "excluded": excluded}


class TopTests(unittest.TestCase):
    def results(self, text, timeout=30.0):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "results.txt"
            path.write_text(text)
            return top.read_results(path, timeout)

    def test_results_format_and_timeout_rule(self):
        parsed, ignored = self.results("""./a.smt2
unsat
1.50 21792
./b.smt2
2.00 900
./c.smt2
sat
31.00 100
./d.smt2
cvc5 interrupted by SIGTERM.
30.00 100
rm: cannot remove 'x'
""")
        # No token means the wrapper was killed; a solved run at the limit is a timeout too.
        self.assertEqual(parsed, {"./a.smt2": ("unsat", 1.5), "./b.smt2": ("timeout", 2.0),
                                  "./c.smt2": ("timeout", 31.0), "./d.smt2": ("timeout", 30.0)})
        self.assertEqual(ignored, 1)

    def test_loss_set_follows_the_gap_rule(self):
        reference = {"unsolved": ("unsat", 0.10), "slow": ("unsat", 0.10), "noise": ("unsat", 0.001),
                     "fast": ("unsat", 0.10), "ref-lost": ("timeout", 30.0)}
        run = {"unsolved": ("timeout", 30.0), "slow": ("unsat", 5.0), "noise": ("unsat", 0.5),
               "fast": ("unsat", 0.2), "ref-lost": ("unsat", 29.0)}
        found = top.losses(reference, run, factor=10.0, floor=1.0, timeout=30.0)
        # noise is 500x slower but under the floor; fast is over the floor but only 2x.
        self.assertEqual(sorted(found), ["slow", "unsolved"])
        self.assertEqual(found["unsolved"], (0.10, None))
        self.assertEqual(found["slow"], (0.10, 5.0))

    def test_rank_is_by_timer_seconds_and_honours_the_filter(self):
        rows = [row("big-share-tiny-run", 0.5, [0.45]), row("long-run-tiny-share", 30.0, [0.30]),
                row("both", 20.0, [12.0]), row("dropped", 40.0, [39.0], excluded="missing total")]
        # share x total is the timer's own seconds, so only "both" is long *and* dominated.
        self.assertEqual([r["benchmark"] for r in top.rank(rows, 0, None, 10)],
                         ["both", "big-share-tiny-run", "long-run-tiny-share"])
        self.assertEqual([r["benchmark"] for r in top.rank(rows, 0, {"long-run-tiny-share": (1, 2)}, 10)],
                         ["long-run-tiny-share"])
        self.assertEqual(len(top.rank(rows, 0, None, 1)), 1)

    def test_render_states_the_measure_and_whether_c_applied(self):
        rows = [row("./a.smt2", 10.0, [4.0])]
        without = top.render(["t::x"], rows, None, 10, "s.txt", "", "", "rule", [])
        self.assertIn("seconds_t(b) = share_t(b) x totalTime(b)", without)
        self.assertIn("Criterion (C) is **not applied**", without)
        self.assertIn("| 1 | `./a.smt2` | 4.00 | 40.0% | 10.00 | unsat |", without)
        with_c = top.render(["t::x"], rows, {"./a.smt2": (0.5, None)}, 10, "s.txt", "z3", "cvc5", "rule", ["n"])
        self.assertIn("filter, not a third factor", with_c)
        self.assertIn("| 0.50 | unsolved |", with_c)
        solved = top.render(["t::x"], rows, {"./a.smt2": (0.5, 20.0)}, 10, "s.txt", "z3", "cvc5", "rule", [])
        self.assertIn("| 0.50 | 40x |", solved)

    def test_refusals(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            summary = work / "summary.json"
            summary.write_text(json.dumps({"source": "s.txt", "summary": {},
                "config": {"categories": [{"name": "t::x", "terms": {}}]},
                "benchmarks": [row("./a.smt2", 10.0, [4.0])]}))
            with self.assertRaises(SystemExit):  # one half of the comparison is not a comparison
                quietly(top.main, str(summary), "--baseline", str(work / "z3.txt"))
            with self.assertRaises(SystemExit):
                quietly(top.main, str(summary), "--count", "0")
            (work / "z3.txt").write_text("./other.smt2\nunsat\n1.0 10\n")
            (work / "cvc5.txt").write_text("./other.smt2\nunsat\n20.0 10\n")
            with self.assertRaises(SystemExit):  # no shared path: not the same set
                quietly(top.main, str(summary), "--baseline", str(work / "z3.txt"),
                        "--results", str(work / "cvc5.txt"))

    def test_end_to_end_writes_the_log(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            summary = work / "summary.json"
            summary.write_text(json.dumps({"source": "s.txt", "summary": {},
                "config": {"categories": [{"name": "t::x", "terms": {}}]},
                "benchmarks": [row("./a.smt2", 10.0, [8.0]), row("./b.smt2", 20.0, [19.0])]}))
            (work / "z3.txt").write_text("./a.smt2\nunsat\n0.10 10\n./b.smt2\nunsat\n19.00 10\n")
            (work / "cvc5.txt").write_text("./a.smt2\nunsat\n10.00 10\n./b.smt2\nunsat\n20.00 10\n")
            quietly(top.main, str(summary), "--baseline", str(work / "z3.txt"),
                    "--results", str(work / "cvc5.txt"))
            log = (work / "top-benchmarks.md").read_text()
            # b spends more timer seconds but only loses 1.05x, so the filter drops it.
            self.assertIn("./a.smt2", log)
            self.assertNotIn("./b.smt2", log)
            self.assertIn("1 benchmarks qualify", log)
            self.assertIn("2 of 2 statistics benchmarks matched", log)
            self.assertIn("separate executions of the same configuration", log)


if __name__ == "__main__":
    unittest.main()
