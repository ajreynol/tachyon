"""Exercise launcher boundaries with local stand-ins; never contact a host."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.launcher = self.root / "job_launcher"
        shutil.copytree(ROOT / "job_launcher", self.launcher, ignore=shutil.ignore_patterns("site.conf"))
        self.run_dev = self.root / "run-dev"
        self.run_dev.mkdir()
        self.env = dict(os.environ, RUN_DEV=str(self.run_dev),
                        TACHYON_SITE=str(self.launcher / "site.conf"),
                        CAPTURE=str(self.root / "args.json"))
        (self.launcher / "site.conf").write_text("DEFAULT_HOST=example-host\n")
        self.script(self.run_dev / "submit", """#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
Path(os.environ['CAPTURE']).write_text(json.dumps(sys.argv[1:]))
""")
        self.script(self.run_dev / "status", "#!/bin/bash\nexit 0\n")
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.env["PATH"] = str(self.bin) + os.pathsep + os.environ["PATH"]
        self.script(self.bin / "ssh", "#!/bin/bash\nexit 99\n")
        self.script(self.bin / "scp", "#!/bin/bash\nexit 99\n")

    def script(self, path, text):
        path.write_text(text)
        path.chmod(0o755)

    def command(self, command, *args):
        return subprocess.run([str(self.launcher / command), *args], cwd=self.root,
                              env=self.env, capture_output=True, text=True)

    def submit(self, *args):
        result = self.command("submit", *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads((self.root / "args.json").read_text())

    def test_config_resolution_preserves_local_files_and_option_values(self):
        name = "quant-cvc5.conf"
        bundled = str(self.launcher / "configs" / name)
        self.assertEqual(self.submit("-n", name), ["-n", bundled])
        for flag in ["-b", "--build", "-H", "--host", "-s", "--session", "-k"]:
            self.assertEqual(self.submit(flag, name), [flag, name])
        self.assertEqual(self.submit("-k", name, "quant-z3.conf"), ["-k", name, "quant-z3.conf"])
        (self.root / name).write_text("# caller's config\n")
        self.assertEqual(self.submit(name), [name])

    def test_submit_keeps_log_and_failure_after_partial_launch(self):
        self.script(self.run_dev / "submit", "#!/bin/bash\nprintf 'launched\n' >> \"${RUN_DEV}/log.txt\"\nexit 7\n")
        (self.run_dev / "log.txt").write_text("prior launch\n")
        before = (self.launcher / "log.txt").read_text()
        result = self.command("submit", "quant-cvc5.conf")
        self.assertEqual(result.returncode, 7)
        self.assertEqual((self.launcher / "log.txt").read_text(), before + "launched\n")

    def test_fetch_usage_does_not_need_site_or_checkout(self):
        (self.launcher / "site.conf").unlink()
        self.assertEqual(self.command("fetch", "--help").returncode, 0)
        for args in [[], ["-d"], ["-H"], ["valid", "bad/name"]]:
            result = self.command("fetch", *args)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertNotIn("unbound variable", result.stderr)
        self.assertFalse((self.root / "scratch").exists())

    def test_fetch_distinguishes_listing_failure_from_no_results(self):
        result = self.command("fetch", "job")
        self.assertEqual(result.returncode, 1)
        self.assertIn("could not list results", result.stderr)
        self.script(self.bin / "ssh", "#!/bin/bash\nexit 0\n")
        result = self.command("fetch", "job")
        self.assertEqual(result.returncode, 1)
        self.assertIn("no results", result.stderr)

    def test_fetch_reads_files_and_directories_and_stops_on_copy_failure(self):
        self.script(self.bin / "ssh", "#!/bin/bash\nprintf '%s\n' analysis/data/results-cvc5-job.txt analysis/stats/job-dir\n")
        self.script(self.bin / "scp", """#!/bin/bash
dest=${@: -1}
source=${@: -2:1}
case "$source" in
  *job-dir) mkdir -p "$dest/job-dir" ;;
  *) printf 'one\ntwo\n' > "$dest/results-cvc5-job.txt" ;;
esac
""")
        result = self.command("fetch", "job")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("(2 lines)", result.stdout)
        self.assertIn("(directory)", result.stdout)
        self.assertTrue((self.root / "scratch/results/job-dir").is_dir())
        self.script(self.bin / "scp", "#!/bin/bash\nexit 8\n")
        result = self.command("fetch", "job")
        self.assertEqual(result.returncode, 8)
        self.assertNotIn("fetched", result.stdout)

    def test_checks_parse_fetch(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        self.script(self.launcher / "fetch", "#!/bin/bash\nif\n")
        result = self.command("checks")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("bash -n fails: job_launcher/fetch", result.stdout)

    def test_checks_accept_public_template_defaults(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        shutil.copyfile(self.launcher / "site.conf.example", self.launcher / "site.conf")
        (self.root / ".gitignore").write_text("job_launcher/site.conf\n")
        result = self.command("checks")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_checks_find_literal_identity_even_early_in_large_files(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / ".gitignore").write_text("job_launcher/site.conf\n")
        (self.launcher / "site.conf").write_text("DEFAULT_HOST=private.host\n")
        evidence = self.root / "public.txt"
        evidence.write_text("privateXhost\n")
        result = self.command("checks")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        evidence.write_text("private.host\n" + "ordinary text\n" * 100000)
        result = self.command("checks")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("personal pattern 'private.host' appears in: public.txt", result.stdout)


if __name__ == "__main__":
    unittest.main()
