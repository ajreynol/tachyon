"""Keep the readable view faithful to the JSON, including unlanded fixes."""
import copy
from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
SPEC = importlib.util.spec_from_file_location("rewrite_view", SCRIPTS / "render_rewrite_db.py")
view = importlib.util.module_from_spec(SPEC)
with patch.object(sys, "path", [str(SCRIPTS), *sys.path]):
    SPEC.loader.exec_module(view)


class RewriteViewTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads(view.DATABASE.read_text())

    def test_checked_in_view_is_current(self):
        self.assertEqual(view.OUTPUT.read_text(), view.render(self.document),
                         "Regenerate with: " + view.COMMAND)

    def test_view_explains_permitted_growth_with_the_operator_order(self):
        result = view.render({"rewrites": [self.document["rewrites"][0]]})
        self.assertIn("**6 -> 7** term nodes", result)
        self.assertIn("**(1, 6) -> (0, 7)**", result)
        self.assertIn("**Orientation order:**", result)
        self.assertIn("term size.", result)

    def test_all_records_terms_conditions_and_drafts_are_visible(self):
        original = copy.deepcopy(self.document)
        result = view.render(self.document)
        self.assertEqual(self.document, original)
        for row in self.document["rewrites"]:
            with self.subTest(candidate=row["candidate"]):
                self.assertIn(f"## {row['candidate']}\n", result)
                self.assertIn(f"](#{row['candidate'].lower()})", result)
                for rewrite in row["proposal"]["rewrites"]:
                    self.assertIn(rewrite["lhs"], result)
                    self.assertIn(rewrite["rhs"], result)
                    self.assertIn("when: " + rewrite["condition"], result)
                    self.assertIn(f"**{view.term_size(rewrite['lhs'])} -> {view.term_size(rewrite['rhs'])}** term nodes", result)
                for draft in row["proposal"]["rare_drafts"]:
                    self.assertIn(draft, result)
                for issue in row["origin"]["issues"]:
                    self.assertIn(f"]({issue['url']})", result)
                for event in row.get("reassessments", []):
                    self.assertIn("](../../../" + event["previous_record"] + ")", result)
        self.assertIn("](" + "../../../docs/github-issues-rewrites.md#m-1-singleton-replacement)", result)
        self.assertIn("No exact rewrite is filed.", result)
        self.assertIn("**Closure:** no closure recorded.", result)

    def test_closure_landing_debt_and_delivery_remain_visible(self):
        row = self.document["rewrites"][0]
        evidence = row["origin"]["ledger"]
        row.update(closed_verdict="accepted and fixed", closed_on="2026-09-19",
                   closed_why="Synthetic closure.", closed_evidence=[evidence],
                   closed_commit="a" * 40, closed_checked_at="b" * 40,
                   awaiting_landing={"project": "cvc5", "branch": "test-fix", "commit": "a" * 40},
                   carried=[{"to": "cvc5", "on": "2026-09-19", "evidence": evidence}])
        row["checks"].update(solver="recorded", solver_evidence=evidence,
                             performance="recorded", performance_evidence=evidence)
        result = view.render({"rewrites": [row]})
        self.assertIn("1 explicit closure verdicts; 1 fixes awaiting landing", result)
        self.assertIn("accepted and fixed; awaiting landing", result)
        self.assertIn("**Awaiting landing:**", result)
        self.assertIn("/commit/" + "a" * 40, result)
        self.assertIn("/commit/" + "b" * 40, result)
        self.assertIn("**Recorded deliveries:**", result)
        self.assertIn("**Solver check:** recorded; [evidence]", result)
        self.assertIn("**Performance check:** recorded; [evidence]", result)

    def test_markdown_text_links_and_code_do_not_break_the_view(self):
        row = self.document["rewrites"][0]
        row["description"] = "Literal | [title]\n<script>"
        result = view.render({"rewrites": [row]})
        self.assertIn(r"Literal &#124; \[title\]<br>&lt;script&gt;", result)
        self.assertIn("````text\n```\n# still code", view.block("```\n# still code"))
        self.assertEqual(view.link("probe", "https://example.org/a(b).smt2#part"),
                         "[probe](https://example.org/a%28b%29.smt2#part)")

    def test_check_mode_never_repairs_missing_or_stale_output(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "rewrites.json"
            database.write_bytes(view.DATABASE.read_bytes())
            original = database.read_bytes()
            output = Path(directory) / "rewrites.md"
            with patch.object(view, "DATABASE", database), patch.object(view, "OUTPUT", output), \
                    redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(view.main(["--check"]), 1)
                self.assertFalse(output.exists())
                output.write_text("stale\n")
                self.assertEqual(view.main(["--check"]), 1)
                self.assertEqual(output.read_text(), "stale\n")
                self.assertEqual(view.main([]), 0)
                self.assertEqual(view.main(["--check"]), 0)
                self.assertEqual(database.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
