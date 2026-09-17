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
        self.env = dict(os.environ, TACHYON_SITE=str(self.launcher / "site.conf"),
                        CAPTURE=str(self.root / "ssh.jsonl"), TMPDIR=str(self.root))
        self.env.pop("SUBMIT_SITE", None)
        (self.launcher / "site.conf").write_text(
            (self.launcher / "site.conf.example").read_text() + "\nDEFAULT_HOST=example-host\n")
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

    def mock_submit_host(self):
        self.script(self.bin / "ssh", """#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
with Path(os.environ['CAPTURE']).open('a') as stream:
    stream.write(json.dumps(sys.argv[1:]) + '\\n')
if 'WCMD=' in sys.argv[-1]:
    print('SCM: git abcdef on branch test')
    sys.exit(0)
print(os.environ.get('SSH_OUTPUT', ''))
sys.exit(int(os.environ.get('SSH_EXIT', '0')))
""")

    def ssh_calls(self):
        return [json.loads(line) for line in (self.root / "ssh.jsonl").read_text().splitlines()]

    def test_config_resolution_preserves_local_files_and_option_values(self):
        self.mock_submit_host()
        name = "quant-cvc5.conf"
        result = self.command("submit", "-n", name)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("solve_dir_rec_par_cvc5", result.stdout)
        for flag in ["-b", "--build"]:
            result = self.command("submit", "-n", flag, name)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f"cmd: [blocking] build {name}", result.stdout)
        result = self.command("submit", "-k", name, "quant-z3.conf")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.ssh_calls()[-1][-2:], [name, "quant-z3.conf"])
        (self.root / name).write_text("COMMENT='local config'\nNAME=local-job\nDIR=$QUANT_DIR\nCMD='printf local-marker'\n")
        result = self.command("submit", "-n", name)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("cmd: printf local-marker", result.stdout)
        self.assertNotIn("cmd: solve_dir_rec_par_cvc5", result.stdout)

    def test_submit_logs_successful_launch_and_not_failed_launch(self):
        self.mock_submit_host()
        before = (self.launcher / "log.txt").read_text()
        result = self.command("submit", "-n", "quant-cvc5.conf")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.launcher / "log.txt").read_text(), before)
        self.env["SSH_EXIT"] = "7"
        result = self.command("submit", "quant-cvc5.conf")
        self.assertEqual(result.returncode, 7)
        self.assertEqual((self.launcher / "log.txt").read_text(), before)
        self.env["SSH_EXIT"] = "0"
        result = self.command("submit", "quant-cvc5.conf")
        self.assertEqual(result.returncode, 0, result.stderr)
        log = (self.launcher / "log.txt").read_text()
        self.assertTrue(log.startswith(before))
        self.assertIn("SCM", self.ssh_calls()[0][-1])
        self.assertIn("# cvc5: git abcdef on branch test", log[len(before):])
        self.assertIn("(quant-cvc5.conf)", log[len(before):])

    def test_blocking_failure_records_the_remote_exit_status(self):
        self.mock_submit_host()
        self.env.update(SSH_EXIT="7", SSH_OUTPUT="[submit] build failed")
        before = (self.launcher / "log.txt").read_text()
        result = self.command("submit", "-b", "test-branch")
        self.assertEqual(result.returncode, 1, result.stderr)
        log = (self.launcher / "log.txt").read_text()
        self.assertTrue(log.startswith(before))
        self.assertIn("# result: FAILED (exit 7,", log[len(before):])

    def test_custom_site_is_shared_by_submit_status_deploy_and_fetch(self):
        self.mock_submit_host()
        custom = self.root / "custom-site.conf"
        (self.launcher / "site.conf").rename(custom)
        self.env["TACHYON_SITE"] = str(custom)
        self.assertEqual(self.command("submit", "-n", "quant-cvc5.conf").returncode, 0)
        self.assertEqual(self.command("status", "-H", "alternate-host", "-s", "2").returncode, 0)
        self.assertEqual(self.ssh_calls()[-1], ["-q", "alternate-host", "bash", "-s", "2"])
        result = self.command("deploy", "-n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("example-host:", result.stdout)
        result = self.command("fetch", "job")
        self.assertIn("no results", result.stderr)
        self.assertEqual(self.ssh_calls()[-1][1], "example-host")

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
