"""Small recorded-format cases for the arm reading; no solver or benchmark-host dependency."""
import importlib.machinery
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "reports/arms"
SPEC = importlib.util.spec_from_loader("arms", importlib.machinery.SourceFileLoader("arms", str(SCRIPT)))
arms = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(arms)

REFERENCE = "a.smt2\nunsat\n1.0 1\nb.smt2\nunsat\n2.0 1\nc.smt2\nsat\n0.5 1\nd.smt2\n30.0 1\n"
ARM = "a.smt2\nunsat\n1.5 1\nb.smt2\nnone\n0.1 1\nc.smt2\nunsat\n0.5 1\nd.smt2\nsat\n3.0 1\n"


class ArmsTests(unittest.TestCase):
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

    def test_gained_lost_crash_and_disagreement(self):
        ref = arms.load(self.data("ref.txt", REFERENCE), 30)
        arm = arms.load(self.data("arm.txt", ARM), 30)
        gained, lost, disagree = arms.compare(ref, arm)
        self.assertEqual(gained, {"d.smt2"})
        self.assertEqual(lost, {"b.smt2"})
        self.assertEqual(disagree, {"c.smt2"})
        solved, unknown, timeouts, crashes, par2 = arms.summary(arm, 30)
        self.assertEqual((solved, unknown, timeouts, crashes), (3, 0, 0, 1))
        self.assertAlmostEqual(par2, 1.5 + 60 + 0.5 + 3.0)

    def test_a_solve_at_the_timeout_counts_as_a_timeout(self):
        ref = arms.load(self.data("ref.txt", "a.smt2\nunsat\n30.0 1\n"), 30)
        self.assertEqual(ref["a.smt2"][0], "timeout")

    def test_the_command_prints_net_and_refuses_a_different_cohort(self):
        ref, arm = self.data("ref.txt", REFERENCE), self.data("arm.txt", ARM)
        done = self.command("--md", f"ref={ref}", f"arm={arm}")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("| arm | +1 | -1 | +0 | 3 | 0 | 0 | 1 | 1 | 65.0 |", done.stdout)
        short = self.data("short.txt", "a.smt2\nunsat\n1.0 1\n")
        refused = self.command(f"ref={ref}", f"arm={short}")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("not the same set", refused.stderr)


if __name__ == "__main__":
    unittest.main()
