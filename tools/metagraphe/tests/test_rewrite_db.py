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
        self.rows = self.document["rewrites"]
        self.by_id = {row["candidate"]: row for row in self.rows}
        self.scope_archive = json.loads((ROOT / "tools/metagraphe/docs/ledger/2026-09-19-rewrite-candidate-scope-before.json").read_text())
        self.historical = {row["candidate"]: row for row in self.scope_archive["records"]}
        self.historical.update(self.by_id)

    def test_retained_records_satisfy_owner_contract(self):
        contract.validate(self.document)

    def test_current_survey_and_drafts_agree(self):
        self.assertTrue({f"M-{n}" for n in range(1, 21)} <= set(self.historical))
        survey = (ROOT / "docs/github-issues-rewrites.md").read_text()
        drafts = []
        for block in re.findall(r"```lisp\n(.*?)```", survey, re.S):
            drafts.extend(part.strip() for part in re.split(r"\n\n(?=\(define-)", block.strip()))
        filed = [draft for n in range(1, 11)
                 if f"M-{n}" in self.by_id
                 for draft in self.by_id[f"M-{n}"]["proposal"]["rare_drafts"]]
        self.assertEqual(filed, drafts)
        issues = {int(n) for n in re.findall(r"/issues/(\d+)", survey)}
        filed_issues = {i["number"] for row in self.historical.values() for i in row["origin"]["issues"]}
        self.assertTrue(issues <= filed_issues)

    def test_scope_archive_preserves_triage_and_m12_reassessment(self):
        archived = {"M-8", "M-11", "M-15", "M-17", "M-19", "M-20"}
        self.assertEqual(set(self.scope_archive["archived_ids"]),
                         {"metagraphe:" + candidate for candidate in archived})
        self.assertFalse(archived & set(self.by_id))
        self.assertTrue(archived <= set(self.historical))
        before = next(row for row in self.scope_archive["records"] if row["candidate"] == "M-12")
        after = self.by_id["M-12"]
        self.assertEqual(after["classification"], "candidate")
        self.assertEqual(after["proposal"]["rewrites"], before["proposal"]["rewrites"])
        self.assertEqual(after["assessment"], before["assessment"])
        self.assertEqual(after["reassessments"][:-1], before["reassessments"])

    def test_issue_only_and_known_rule_filings_are_rejected(self):
        self.rejected(lambda r: r.update(classification="excluded", priority=None))
        self.rejected(lambda r: r.update(classification="existing-coverage", priority=None))
        self.rejected(lambda r: r["proposal"].update(rewrites=[]))
        row = copy.deepcopy(self.rows[0])
        row["assessment"].update(validity="unchecked", availability="unchecked")
        contract.validate([row], filing=True)
        row["assessment"]["availability"] = "existing-rule-needs-context"
        with self.assertRaisesRegex(ValueError, "known-rule context or reachability"):
            contract.validate([row], filing=True)
        # Later discovery of existing support is a reassessment, not a reason
        # to delete a previously filed candidate or prevent its closure.
        contract.validate({"rewrites": [row]})
        row.update(closed_verdict="withdrawn", closed_on="2026-09-19",
                   closed_why="Synthetic existing-support correction.",
                   closed_evidence=[row["origin"]["ledger"]])
        contract.validate([row], filing=True)

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
            contract.validate({"rewrites": [row]})

    def test_orientation_corrections_preserve_the_original_equalities(self):
        archive = json.loads((ROOT / "tools/metagraphe/docs/ledger/2026-09-19-rewrite-orientation-before.json").read_text())
        self.assertEqual({row["candidate"] for row in archive["records"]},
                         {"M-1", "M-5", "M-11", "M-12", "M-16"})
        for before in archive["records"]:
            after = self.historical[before["candidate"]]
            self.assertTrue(after["reassessments"])
            for original, corrected in zip(before["proposal"]["rewrites"], after["proposal"]["rewrites"]):
                sides = ("rhs", "lhs") if before["candidate"] == "M-12" else ("lhs", "rhs")
                self.assertEqual((original["lhs"], original["rhs"]),
                                 tuple(corrected[side] for side in sides))
                for field in ("variables", "condition", "notation"):
                    self.assertEqual(original[field], corrected[field])

    def test_growth_needs_a_declared_order_and_reverse_introduction_is_rejected(self):
        contract.validate({"rewrites": [copy.deepcopy(self.by_id["M-1"])]})
        self.rejected(lambda r: r["proposal"].pop("orientation"))
        self.rejected(lambda r: r["proposal"]["orientation"].update(reason=""))
        self.rejected(lambda r: r["proposal"]["orientation"].update(operators=["abs"]))
        def reverse(row):
            rule = row["proposal"]["rewrites"][0]
            rule["lhs"], rule["rhs"] = rule["rhs"], rule["lhs"]
        self.rejected(reverse)
        self.rejected(lambda r: r["proposal"].update(rare_drafts=[
            '(define-rule expansion ((x Int)) x (+ x 0))']))
        self.rejected(lambda r: r["proposal"]["rewrites"][0].update(lhs="true", rhs="true"))

    def test_lexicographic_precedence_and_size_tiebreak(self):
        order = {"kind": "lexicographic", "operators": ["expensive", "cheap"],
                 "reason": "Synthetic precedence example."}
        lhs = contract.expression_tree('(expensive x)')
        rhs = contract.expression_tree('(cheap (cheap x))')
        contract.check_orientation(lhs, rhs, order)
        with self.assertRaises(ValueError):
            contract.check_orientation(rhs, lhs, order)
        larger = contract.expression_tree('(expensive (+ x 0))')
        contract.check_orientation(larger, lhs, order)
        with self.assertRaises(ValueError):
            contract.check_orientation(lhs, larger, order)

    def test_operator_review_preserves_prior_directions_and_rejects_reversed_drafts(self):
        archive = json.loads((ROOT / "tools/metagraphe/docs/ledger/2026-09-19-rewrite-operator-order-before.json").read_text())
        for before in archive["records"]:
            after = self.historical[before["candidate"]]
            self.assertEqual(after["reassessments"][:-1], before["reassessments"])
            for old, new in zip(before["proposal"]["rewrites"], after["proposal"]["rewrites"]):
                self.assertEqual((old["lhs"], old["rhs"]), (new["rhs"], new["lhs"]))
                self.assertEqual(old["condition"], new["condition"])
                self.assertEqual(old["variables"], new["variables"])
        reversed_drafts = archive["records"][0]["proposal"]["rare_drafts"]
        self.rejected(lambda r: r["proposal"].update(rare_drafts=reversed_drafts))

    def test_structural_size_counts_terms_not_text_or_indices(self):
        self.assertEqual(contract.term_size('(= s "long (text) with ""quotes""")'), 3)
        self.assertEqual(contract.term_size('((_ extract 7 0) x)'), 2)
        self.assertEqual(contract.term_size('(_ bv0 32)'), 1)
        self.assertEqual(contract.term_size('(= x zero(w))'), 3)
        for malformed in ('(f x', 'x y', '"unterminated', ')'):
            with self.assertRaises(ValueError):
                contract.term_size(malformed)

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
            contract.validate({"rewrites": [self.rows[0], self.rows[0]]})

    def test_filing_can_omit_only_ingestion_dates(self):
        row = copy.deepcopy(self.rows[0])
        del row["first_seen"], row["last_seen"]
        contract.validate([row], filing=True)
        with self.assertRaises(ValueError):
            contract.validate({"rewrites": [row]})
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
            contract.validate({"rewrites": [row]})
        row["awaiting_landing"] = {"project": "cvc5", "branch": "example", "commit": "a" * 40}
        contract.validate({"rewrites": [row]})
        row["closed_verdict"] = "fixed and landed"
        with self.assertRaises(ValueError):
            contract.validate({"rewrites": [row]})
        del row["awaiting_landing"]
        contract.validate({"rewrites": [row]})
        row["closed_evidence"] = []
        with self.assertRaises(ValueError):
            contract.validate({"rewrites": [row]})

    def test_delivery_and_recoding_require_evidence(self):
        self.rejected(lambda r: r.update(carried=[{"to": "cvc5", "on": "2026-09-19"}]))
        self.rejected(lambda r: r.update(closed_verdict="re-coded", closed_on="2026-09-19",
                     closed_why="Synthetic recoding.", closed_evidence=[r["origin"]["ledger"]],
                     replacement_id="metagraphe:M-99999"))


if __name__ == "__main__":
    unittest.main()
