"""Check pin enforcement and the boundary between local policy and shared tools."""
from contextlib import redirect_stderr
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
SPEC = importlib.util.spec_from_file_location("koine_db_adapter", SCRIPTS / "koine_db.py")
adapter = importlib.util.module_from_spec(SPEC)
with patch.object(sys, "path", [str(SCRIPTS), *sys.path]):
    SPEC.loader.exec_module(adapter)


class KoineAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.db = self.root / "rewrites.json"
        self.db.write_bytes(adapter.DATABASE.read_bytes())
        self.filing = self.root / "new.json"
        self.filing.write_text(json.dumps([json.loads(self.db.read_text())["rewrites"][0]]))
        self.view = self.root / "rewrites.md"
        self.view.write_text("old view\n")
        for name, value in (("DATABASE", self.db), ("OUTPUT", self.view)):
            patcher = patch.object(adapter, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_pin_wins_over_head_and_dirty_worktree(self):
        repo = self.root / "koine"
        repo.mkdir()
        def git(*args):
            return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()
        git("init", "--quiet")
        script = repo / "bug_db_manager/koine_check_db"
        script.parent.mkdir()
        def source(label):
            return f"import sys\nfrom pathlib import Path\nPath(sys.argv[1]).write_text({label!r})\n"
        script.write_text(source("pinned"))
        git("add", ".")
        git("-c", "user.name=Fixture", "-c", "user.email=test@example.invalid",
            "commit", "--quiet", "-m", "pinned fixture")
        pin = git("rev-parse", "HEAD")
        script.write_text(source("newer HEAD"))
        git("add", ".")
        git("-c", "user.name=Fixture", "-c", "user.email=test@example.invalid",
            "commit", "--quiet", "-m", "newer fixture")
        script.write_text(source("dirty"))
        lock = self.root / "koine.lock"
        lock.write_text(pin + "\n")
        output = self.root / "result"
        with patch.object(adapter, "LOCK", lock):
            self.assertEqual(adapter.run_pinned(repo, "koine_check_db", [str(output)]), 0)
            self.assertEqual(output.read_text(), "pinned")
            lock.write_text("0" * 40)
            with self.assertRaises(ValueError):
                adapter.run_pinned(repo, "koine_check_db", [str(output)])
            self.assertEqual(output.read_text(), "pinned")

    def test_dry_run_and_upstream_failure_do_not_refresh_the_view(self):
        before = self.db.read_bytes()
        with patch.object(adapter, "run_pinned", return_value=0) as run:
            self.assertEqual(adapter.main(["append", str(self.filing), "--dry-run"]), 0)
            self.assertEqual(run.call_args.args[1], "koine_append_db")
            self.assertEqual(run.call_args.args[2],
                             [str(self.filing), str(self.db), "--records", "rewrites", "--dry-run"])
        self.assertEqual(self.view.read_text(), "old view\n")
        self.assertEqual(self.db.read_bytes(), before)
        with patch.object(adapter, "run_pinned", return_value=3):
            self.assertEqual(adapter.main(["append", str(self.filing)]), 3)
        self.assertEqual(self.view.read_text(), "old view\n")

    def test_successful_append_refreshes_from_the_validated_database(self):
        with patch.object(adapter, "run_pinned", return_value=0):
            self.assertEqual(adapter.main(["append", str(self.filing)]), 0)
        self.assertEqual(self.view.read_text(), adapter.render(json.loads(self.db.read_text())))

    def test_invalid_filing_and_duplicate_database_never_reach_koine(self):
        self.filing.write_text('[{"id": "metagraphe:M-99"}]')
        with patch.object(adapter, "run_pinned") as run, redirect_stderr(io.StringIO()):
            self.assertEqual(adapter.main(["append", str(self.filing)]), 1)
            run.assert_not_called()
            document = json.loads(self.db.read_text())
            document["rewrites"].append(document["rewrites"][0])
            self.db.write_text(json.dumps(document))
            self.assertEqual(adapter.main(["check-closure"]), 1)
            run.assert_not_called()

    def test_closure_flags_are_scoped_and_amendment_is_explicit(self):
        before = self.db.read_bytes()
        with patch.object(adapter, "run_pinned", return_value=0) as run:
            self.assertEqual(adapter.main(["check-closure"]), 0)
            self.assertEqual(run.call_args.args[1:], ("koine_check_db", [str(self.db),
                             "--against", "HEAD", "--also", "awaiting_landing",
                             "--also", "replacement_id"]))
            self.assertEqual(adapter.main(["check-closure", "--against", "HEAD~1", "--amended"]), 0)
            self.assertIn("HEAD~1", run.call_args.args[2])
            self.assertEqual(run.call_args.args[2][-1], "--amended")
        self.assertEqual(self.db.read_bytes(), before)
        self.assertEqual(self.view.read_text(), "old view\n")

    @unittest.skipUnless(os.environ.get("KOINE"), "set KOINE to exercise the real pinned shared tools")
    def test_pinned_tools_append_and_check_real_owner_records(self):
        def git(*args):
            return subprocess.check_output(["git", "-C", str(self.root), *args], text=True).strip()
        def commit(message):
            git("add", "rewrites.json")
            git("-c", "user.name=Fixture", "-c", "user.email=test@example.invalid",
                "commit", "--quiet", "-m", message)
        git("init", "--quiet")
        commit("pre-filing fixture")
        original = self.db.read_bytes()
        with redirect_stderr(io.StringIO()):
            self.assertEqual(adapter.main(["append", str(self.filing), "--dry-run"]), 0)
        self.assertEqual(self.db.read_bytes(), original)
        new = json.loads(self.filing.read_text())[0]
        new.update(id="metagraphe:M-99999", candidate="M-99999", description="Synthetic integration fixture")
        for field in ("first_seen", "last_seen"):
            del new[field]
        self.filing.write_text(json.dumps([new]))
        self.assertEqual(adapter.main(["append", str(self.filing)]), 0)
        filed = json.loads(self.db.read_text())
        self.assertEqual(list(filed), ["rewrites"])
        self.assertEqual(filed["rewrites"][:-1], json.loads(original)["rewrites"])
        self.assertEqual(self.view.read_text(), adapter.render(filed))
        commit("filed fixture")
        row = filed["rewrites"][0]
        row.update(closed_verdict="accepted and fixed", closed_on="2026-09-19",
                   closed_why="Synthetic closure fixture.", closed_evidence=[row["origin"]["ledger"]],
                   closed_commit="a" * 40, closed_checked_at="b" * 40,
                   awaiting_landing={"project": "cvc5", "branch": "fixture", "commit": "a" * 40})
        self.db.write_text(json.dumps(filed))
        self.assertEqual(adapter.main(["check-closure"]), 0)
        description = row["description"]
        row["description"] = "Unauthorized claim change"
        self.db.write_text(json.dumps(filed))
        self.assertEqual(adapter.main(["check-closure"]), 1)
        row["description"] = description
        self.db.write_text(json.dumps(filed))
        commit("closed fixture")
        row["closed_verdict"] = "fixed and landed"
        del row["awaiting_landing"]
        self.db.write_text(json.dumps(filed))
        self.assertEqual(adapter.main(["check-closure"]), 1)
        self.assertEqual(adapter.main(["check-closure", "--amended"]), 0)


if __name__ == "__main__":
    unittest.main()
