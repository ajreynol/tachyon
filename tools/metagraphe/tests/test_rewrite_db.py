"""Protect curated rewrite evidence and reject misleading status combinations."""
import copy
import importlib.util
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "rewrite_contract", ROOT / "tools/metagraphe/scripts/check_rewrite_db.py")
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)


class RewriteDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads(contract.DATABASE.read_text())
        self.rows = self.document["bugs"]
        self.by_id = {row["candidate"]: row for row in self.rows}

    def test_retained_records_satisfy_owner_contract(self):
        contract.validate(self.document)

    def test_initial_survey_and_drafts_were_not_lost(self):
        self.assertTrue({f"M-{n}" for n in range(1, 21)} <= set(self.by_id))
        survey = (ROOT / "docs/github-issues-rewrites.md").read_text()
        drafts = []
        for block in re.findall(r"```lisp\n(.*?)```", survey, re.S):
            drafts.extend(part.strip() for part in re.split(r"\n\n(?=\(define-)", block.strip()))
        filed = [draft for n in range(1, 11)
                 for draft in self.by_id[f"M-{n}"]["proposal"]["rare_drafts"]]
        self.assertEqual(filed, drafts)
        issues = {int(n) for n in re.findall(r"/issues/(\d+)", survey)}
        filed_issues = {i["number"] for row in self.rows for i in row["origin"]["issues"]}
        self.assertTrue(issues <= filed_issues)
        self.assertEqual(self.by_id["M-11"]["classification"], "existing-coverage")
        self.assertEqual(self.by_id["M-12"]["classification"], "existing-coverage")
        self.assertEqual(self.by_id["M-19"]["classification"], "excluded")
        self.assertEqual(self.by_id["M-20"]["classification"], "excluded")

    def test_known_semantic_conditions_survive_filing(self):
        first = self.by_id["M-1"]["proposal"]["rewrites"][0]
        self.assertIn("(str.contains s u)", first["rhs"])
        self.assertEqual(first["condition"], "(= (str.len u) 1)")
        prefix = self.by_id["M-2"]["proposal"]["rewrites"][0]
        self.assertEqual(prefix["rhs"], "(= (str.len t) 0)")
        self.assertIn("length one", self.by_id["M-10"]["proposal"]["rewrites"][0]["condition"])
        self.assertIn("0x2ffff", self.by_id["M-5"]["proposal"]["rewrites"][0]["condition"])

    def rejected(self, change):
        row = copy.deepcopy(self.by_id["M-1"])
        change(row)
        with self.assertRaises(ValueError):
            contract.validate({"bugs": [row]})

    def test_parser_acceptance_cannot_be_mislabeled_as_proof(self):
        self.rejected(lambda r: r["assessment"].update(validity="proved"))
        self.rejected(lambda r: r["checks"].update(rare_parser_revision=None))
        self.rejected(lambda r: r["assessment"].update(value="measured"))

    def test_bad_identity_dates_and_evidence_are_rejected(self):
        self.rejected(lambda r: r.update(candidate="M-2"))
        self.rejected(lambda r: r.update(found_at="main"))
        self.rejected(lambda r: r.update(last_seen="2000-01-01"))
        self.rejected(lambda r: r["origin"].update(ledger="/tmp/not-retained.md"))
        with self.assertRaises(ValueError):
            contract.validate({"bugs": [self.rows[0], self.rows[0]]})

    def test_filing_can_omit_only_ingestion_dates(self):
        row = copy.deepcopy(self.rows[0])
        del row["first_seen"], row["last_seen"]
        contract.validate([row], filing=True)
        with self.assertRaises(ValueError):
            contract.validate({"bugs": [row]})
        del row["observed_on"]
        with self.assertRaises(ValueError):
            contract.validate([row], filing=True)

    def test_fix_closure_requires_evidence_and_landing_debt(self):
        row = copy.deepcopy(self.rows[0])
        row.update(closed_verdict="accepted and fixed", closed_on="2026-09-19",
                   closed_why="Synthetic closure for schema testing.",
                   closed_evidence=[row["origin"]["ledger"]], closed_commit="a" * 40,
                   closed_checked_at="a" * 40)
        with self.assertRaises(ValueError):
            contract.validate({"bugs": [row]})
        row["awaiting_landing"] = {"project": "cvc5", "branch": "example", "commit": "a" * 40}
        contract.validate({"bugs": [row]})
        row["closed_verdict"] = "fixed and landed"
        with self.assertRaises(ValueError):
            contract.validate({"bugs": [row]})
        del row["awaiting_landing"]
        contract.validate({"bugs": [row]})
        row["closed_evidence"] = []
        with self.assertRaises(ValueError):
            contract.validate({"bugs": [row]})

    def test_delivery_and_recoding_require_evidence(self):
        self.rejected(lambda r: r.update(carried=[{"to": "cvc5", "on": "2026-09-19"}]))
        self.rejected(lambda r: r.update(closed_verdict="re-coded", closed_on="2026-09-19",
                     closed_why="Synthetic recoding.", closed_evidence=[r["origin"]["ledger"]],
                     replacement_id="metagraphe:M-99999"))


if __name__ == "__main__":
    unittest.main()
