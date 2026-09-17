import importlib.util
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("stats_profile", Path(__file__).parents[1] / "profile.py")
profile = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(profile)


class ProfilerTests(unittest.TestCase):
    def test_pdf_cli_rejects_bad_axis_before_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "stats.txt"
            path.write_text("a.smt2\nglobal::totalTime = 1s\n")
            output = Path(directory) / "report"
            for limit in ["0", "-1", "101", "nan", "inf"]:
                stderr = io.StringIO()
                with self.subTest(limit=limit), contextlib.redirect_stderr(stderr):
                    with self.assertRaises(SystemExit) as error:
                        profile.main([str(path), "--pdf", "--max-share", limit, "--output", str(output)])
                    self.assertEqual(error.exception.code, 2)
                    self.assertIn("--max-share must be", stderr.getvalue())
            self.assertFalse(output.exists())

    def parse(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "stats.txt"
            path.write_text(text)
            return profile.read_stats(path)

    def config(self, categories, missing="zero"):
        return profile.compile_config({"total": "total", "missing": missing,
            "categories": categories}, ["total", "parent", "child"])[0]

    def test_units_and_counters(self):
        for value, expected in [("2ns", 2e-9), ("2us", 2e-6), ("2µs", 2e-6),
                                ("2ms", .002), ("2 s", 2), ("2min", 120), ("2h", 7200), ("1e2ms", .1)]:
            self.assertAlmostEqual(profile.seconds(value), expected)
        for value in ["12", "{ a: 1 }", "nanms", "infms", "-1ms", "1e999s"]:
            self.assertIsNone(profile.seconds(value))

    def test_job_blocks_filename_status_and_truncated_output(self):
        rows, warnings = self.parse("""job preamble
./a.smt2
unsat
driver::filename = ./a.smt2
total = 100ms
counter = 8
histogram = { TIMER: 2 }
0.12 5000
./b.smt2
cvc5 interrupted by SIGTERM.
total = 2s
./c.smt2
""")
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["timers"], {"total": .1})
        self.assertEqual([r["status"] for r in rows], ["unsat", "timeout", "unreported"])
        self.assertEqual(warnings, [])

    def test_duplicate_snapshots_and_benchmarks(self):
        rows, warnings = self.parse("a.smt2\ntotal = 1s\ntotal = 2s\na.smt2\ntotal = 3s\n")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["timers"]["total"], 2)
        self.assertEqual(len(warnings), 2)

    def test_processed_summary_rejected(self):
        with self.assertRaisesRegex(ValueError, "No benchmark blocks"):
            self.parse("=== Final proof size: ===\n")

    def test_glob_union_and_subtraction(self):
        config = self.config([{"name": "exclusive", "add": ["p*", "parent"], "subtract": ["child"]}])
        self.assertEqual(config["categories"][0]["terms"], {"parent": 1, "child": -1})

    def test_unknown_literal_is_missing(self):
        config, warnings = profile.compile_config({"categories": [{"name": "x", "add": ["absent", "nothing*"]}]}, [])
        self.assertEqual(config["categories"][0]["terms"], {"absent": 1})
        self.assertEqual(len(warnings), 2)

    def test_bad_configs(self):
        for config in [[], {}, {"categories": [None]}, {"categories": [{"name": "x", "add": "parent"}]},
                       {"categories": [{"name": "x", "add": ["global::totalTime"]}]},
                       {"categories": [{"name": "x"}, {"name": "x"}]},
                       {"missing": "guess", "categories": [{"name": "x"}]}]:
            with self.subTest(config=config), self.assertRaises(ValueError):
                profile.compile_config(config, ["global::totalTime"])

    def test_gap_excess_do_not_cancel_and_weighted_coverage(self):
        records = [{"benchmark": "a", "status": "sat", "timers": {"total": 10, "parent": 5}},
                   {"benchmark": "b", "status": "sat", "timers": {"total": 2, "parent": 4}}]
        _, summary = profile.analyze(records, self.config([{"name": "p", "add": ["parent"]}]))
        self.assertEqual(summary["gap_seconds"], 5)
        self.assertEqual(summary["excess_seconds"], 2)
        self.assertEqual(summary["residual_seconds"], 3)
        self.assertEqual(summary["coverage"], .75)

    def test_missing_and_zero_totals_are_excluded(self):
        records = [{"benchmark": "a", "status": "unknown", "timers": {"parent": 3}},
                   {"benchmark": "b", "status": "unknown", "timers": {"total": 0, "parent": 2}}]
        rows, summary = profile.analyze(records, self.config([{"name": "p", "add": ["parent"]}]))
        self.assertEqual([r["excluded"] for r in rows], ["missing total", "zero total"])
        self.assertEqual(summary["included"], 0)
        self.assertIsNone(summary["coverage"])

    def test_missing_policies_and_negative_exclusive_time(self):
        records = [{"benchmark": "a", "status": "unknown", "timers": {"total": 10, "child": 2}}]
        categories = [{"name": "p", "add": ["parent"], "subtract": ["child"]}]
        rows, summary = profile.analyze(records, self.config(categories))
        self.assertEqual(rows[0]["values"], [-2])
        self.assertEqual(rows[0]["gap"], 12)
        self.assertEqual(summary["negative_category_runs"], 1)
        self.assertEqual(summary["missing_timer_runs"], 1)
        _, strict = profile.analyze(records, self.config(categories, "exclude"))
        self.assertEqual(strict["included"], 0)

    def test_export_and_safe_html_embedding(self):
        name = '</script><script>alert("x")</script>.smt2'
        records = [{"benchmark": name, "status": "sat", "timers": {"total": 2, "parent": 1}}]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            profile.write_report(output, records, self.config([{"name": "p", "add": ["parent"]}]), [], "stats.txt")
            html = (output / "index.html").read_text()
            self.assertNotIn(name, html)
            self.assertNotIn("__PROFILE_DATA__", html)
            report = json.loads((output / "summary.json").read_text())
            self.assertEqual(report["benchmarks"][0]["benchmark"], name)
            self.assertEqual(report["summary"]["coverage"], .5)
            self.assertIn("p (s)", (output / "benchmarks.csv").read_text())


if __name__ == "__main__":
    unittest.main()
