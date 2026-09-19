"""Small recorded-format cases; no solver or benchmark-host dependency."""
import importlib.machinery
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "reports/gap"
SPEC = importlib.util.spec_from_loader("gap", importlib.machinery.SourceFileLoader("gap", str(SCRIPT)))
gap = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gap)


class GapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def data(self, name, text):
        path = self.root / name
        path.write_text(text)
        return path

    def command(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], text=True, capture_output=True)

    def test_compressed_names_and_wrapper_timeout(self):
        path = self.data("run.txt", "a.smt2.gz\nunsat\n0.25 1024\nb.smt2\nCommand exited with non-zero status 124\n30.0 2048\n")
        records, ignored = gap.read(path)
        self.assertEqual(records, {"a.smt2.gz": ("unsat", .25, 1024), "b.smt2": ("timeout", 30, 2048)})
        self.assertEqual(ignored, 1)

    def test_incomplete_duplicate_and_empty_data_are_rejected(self):
        for text in ["", "a.smt2\nunsat\n", "a.smt2\nb.smt2\nunsat\n1 1\n",
                     "a.smt2\nunsat\n1 1\na.smt2\nunsat\n2 2\n"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                gap.read(self.data("run.txt", text))

    def test_cli_does_not_silently_drop_an_incomplete_run(self):
        path = self.data("run.txt", "a.smt2\nunsat\n1 1\nb.smt2\nunsat\n")
        result = self.command(f"run={path}")
        self.assertEqual(result.returncode, 2)
        self.assertIn("incomplete benchmark block: b.smt2", result.stderr)
        self.assertNotIn("PAR2", result.stdout)

    def test_gap_keeps_unsolved_status_and_excludes_wrong_answers(self):
        ref = self.data("ref.txt", "a.smt2\nunsat\n0.1 1\nb.smt2\nunsat\n0.1 1\nc.smt2\nunsat\n0.1 1\n")
        run = self.data("run.txt", "a.smt2\nunknown\n1 1\nb.smt2\nsat\n2 1\nc.smt2\nunsat\n3 1\n")
        output = self.root / "gap.txt"
        result = self.command(f"ref={ref}", f"run={run}", "--gapset", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("gap set 2", result.stdout)
        self.assertIn("sat/unsat disagreements 1", result.stdout)
        self.assertEqual(output.read_text(), "a.smt2 0.10 unknown\nc.smt2 0.10 3.00\n")

    def test_invalid_thresholds_and_empty_intersection(self):
        first = self.data("one.txt", "a.smt2\nunsat\n1 1\n")
        second = self.data("two.txt", "b.smt2\nunsat\n1 1\n")
        result = self.command(f"a={first}", f"b={second}")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no benchmarks in common", result.stderr)
        for flag, value in [("--timeout", "0"), ("--factor", "nan"), ("--floor", "-1")]:
            self.assertEqual(self.command(f"a={first}", flag, value).returncode, 2)


if __name__ == "__main__":
    unittest.main()
