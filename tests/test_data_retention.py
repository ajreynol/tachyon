"""Check retention against real temporary Git indexes, with synthetic output."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("retention", ROOT / "scripts/check_data_retention.py")
retention = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(retention)


class RetentionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        shutil.copyfile(ROOT / ".gitignore", self.root / ".gitignore")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True)

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def test_dumps_are_ignored_anywhere_but_force_added_ones_fail(self):
        names = ["results-demo.txt", "stats-demo-processed.txt", "errors-demo.txt",
                 "stats-demo.txt.gz", "run.log", "build.stdout", "build.stderr", "stdout", "stderr"]
        for name in names:
            name = "tools/demo/ledger/data/" + name
            with self.subTest(name=name):
                path = self.write(name, "synthetic output\n")
                self.git("check-ignore", "-q", name)
                self.assertEqual(retention.violations(self.root), [])
                self.git("add", "-f", name)
                self.assertEqual(retention.violations(self.root), [(name, "reserved raw-output filename")])
                # A tracked deletion can pass before the deletion is staged.
                path.unlink()
                self.assertEqual(retention.violations(self.root), [])

    def test_renamed_and_pasted_output_is_detected(self):
        for content in ["./a.smt2\nunsat\n0.12 5000\n",
                        "./a.smt2\nglobal::totalTime = 1s\n",
                        "#0  EqualityEngine::getExplanation(unsigned)\n"]:
            with self.subTest(content=content):
                self.write("notes.md", "# Notes\n\n```\n" + content + "```\n")
                self.assertEqual([name for name, _ in retention.violations(self.root)], ["notes.md"])

    def test_derived_records_and_synthetic_source_inputs_are_allowed(self):
        self.write("tools/demo/ledger/data/gapset-demo.txt", "./a.smt2 0.10 timeout\n")
        self.write("job_launcher/log.txt", "# demo\nsolve_dir_rec_par_cvc5 -t 30 demo\n# result: SUCCESS\n")
        self.write("tests/test_parser.py", 'SAMPLE = """\n./a.smt2\nunsat\n0.12 5000\n"""\n')
        self.write("scratch/capture.txt", "./a.smt2\nunsat\n0.12 5000\n")
        self.assertEqual(retention.violations(self.root), [])
        # Ignored directories have no exemption once their data is force-added.
        self.git("add", "-f", "scratch/capture.txt")
        self.assertEqual([name for name, _ in retention.violations(self.root)], ["scratch/capture.txt"])

    def test_missing_pattern_register_is_an_error(self):
        (self.root / ".gitignore").write_text("scratch/\n")
        with self.assertRaises(ValueError):
            retention.violations(self.root)


if __name__ == "__main__":
    unittest.main()
