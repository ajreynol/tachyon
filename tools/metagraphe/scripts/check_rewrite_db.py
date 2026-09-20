#!/usr/bin/env python3
"""Validate metagraphe's curated records; never rewrite the database."""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[3]
DATABASE = ROOT / "tools/metagraphe/rewrite_db/rewrites.json"
VERDICTS = {"accepted and fixed", "fixed and landed", "declined", "intentional",
            "not audited", "withdrawn", "re-coded"}
AVAILABILITY = {"source-gap-candidate", "existing-rule-needs-context", "unchecked",
                "existing-rule-reachability-unchecked", "existing-conditional-support",
                "not-applicable"}
# How a candidate was found. An issue survey cites the survey and its issues; a
# benchmark comparison cites the corpus it sampled and has no source issue.
ORIGIN_KINDS = {"github-issue-survey", "benchmark-comparison"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value, empty=False):
    return isinstance(value, list) and (empty or bool(value)) and all(map(nonempty, value))


def revision(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None


def day(value):
    require(isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value),
            "date must be YYYY-MM-DD")
    return date.fromisoformat(value)


def reference(value, root):
    require(nonempty(value), "empty evidence reference")
    parsed = urlsplit(value)
    if parsed.scheme:
        require(parsed.scheme == "https" and bool(parsed.netloc), "expected an HTTPS reference")
    else:
        path = (root / parsed.path).resolve()
        require(root in path.parents and path.is_file(), "missing or non-repository evidence: " + value)


def object_at(row, name):
    value = row.get(name)
    require(isinstance(value, dict), name + " must be an object")
    return value


def expression_tree(expression):
    """Read a term schema for size checking, not SMT-LIB type/validity checking.

    Strings use SMT-LIB doubled quotes. zero(w) is the database's existing
    shorthand for a width-parameterized zero literal, counted as one atom.
    """
    token = re.compile(r'\s*("(?:[^"]|"")*"|\|[^|]*\||zero\(w\)|[()]|[^\s()"|]+)')
    stack, roots = [], []
    pos = 0
    while expression[pos:].strip():
        match = token.match(expression, pos)
        require(match is not None, "unrecognized term syntax")
        value, pos = match.group(1), match.end()
        if value == "(":
            node = []
            (stack[-1] if stack else roots).append(node)
            stack.append(node)
        elif value == ")":
            require(bool(stack), "unmatched closing parenthesis")
            stack.pop()
        else:
            (stack[-1] if stack else roots).append(value)
    require(not stack and len(roots) == 1, "expected one complete term")
    return roots[0]


def tree_size(tree):
    if isinstance(tree, str):
        return 1
    require(bool(tree), "empty application")
    # Indexed literals and qualified constants denote a single term node;
    # an indexed operator in function position is also one application node.
    if tree[0] in ("_", "as"):
        return 1
    return 1 + sum(tree_size(child) for child in tree[1:])


def term_size(expression):
    return tree_size(expression_tree(expression))


def operator_count(tree, operator):
    if isinstance(tree, str):
        return 0
    require(bool(tree), "empty application")
    head = tree[0]
    if isinstance(head, list) and len(head) > 1 and head[0] == "_":
        head = head[1]
    return int(head == operator) + sum(operator_count(child, operator) for child in tree[1:])


def orientation_cost(tree, orientation):
    """Lexicographic operator counts, highest priority first, then term size."""
    if orientation is None:
        return (tree_size(tree),)
    require(isinstance(orientation, dict) and orientation.get("kind") == "lexicographic",
            "invalid orientation rationale")
    require(strings(orientation.get("operators")) and nonempty(orientation.get("reason")),
            "lexicographic orientation requires ordered operators and a reason")
    require(len(set(orientation["operators"])) == len(orientation["operators"]),
            "operator precedence must not contain duplicates")
    return tuple(operator_count(tree, op) for op in orientation["operators"]) + (tree_size(tree),)


def check_orientation(lhs, rhs, orientation):
    """Check the declared ordering, not actual runtime cost."""
    require(orientation_cost(lhs, orientation) > orientation_cost(rhs, orientation),
            "rewrite must decrease the lexicographic cost: complex operators first, size last")


def validate(document, root=ROOT, filing=False):
    """Return validated records, or raise ValueError with the affected identity."""
    if filing and isinstance(document, list):
        rows = document
    else:
        require(isinstance(document, dict) and set(document) == {"rewrites"},
                "expected an object with only a rewrites collection")
        rows = document["rewrites"]
    require(isinstance(rows, list), "collection must be a list")
    seen = set()
    for row in rows:
        require(isinstance(row, dict), "record must be an object")
        identity = row.get("id")
        try:
            require(nonempty(identity) and re.fullmatch(r"metagraphe:M-[1-9][0-9]*", identity),
                    "invalid stable id")
            require(identity not in seen, "duplicate id")
            seen.add(identity)
            require(row.get("candidate") == identity.split(":", 1)[1], "candidate/id mismatch")
            require(type(row.get("schema_version")) is int and row["schema_version"] == 1,
                    "unsupported schema_version")
            require(row.get("tool") == "metagraphe" and row.get("owner") == "cvc5",
                    "unexpected producer or subject owner")
            for field in ("description", "next_step"):
                require(nonempty(row.get(field)), "missing " + field)
            require(strings(row.get("theories")), "theories must be a nonempty string list")
            require(strings(row.get("cautions"), empty=True), "cautions must be a string list")
            require(row.get("classification") == "candidate",
                    "rewrite_db accepts only candidate rewrites; keep issue triage in the ledger")
            priority = row.get("priority")
            require(type(priority) is int and 1 <= priority <= 3, "invalid candidate priority")
            require(revision(row.get("found_at")), "found_at must be a full source commit")
            observed = day(row.get("observed_on"))
            if not filing or "first_seen" in row or "last_seen" in row:
                require(observed <= day(row.get("first_seen")) <= day(row.get("last_seen")),
                        "observation and ingestion dates are out of order")

            origin = object_at(row, "origin")
            kind = origin.get("kind")
            require(kind in ORIGIN_KINDS, "unsupported origin kind")
            reference(origin.get("ledger"), root)
            if kind == "github-issue-survey":
                require(revision(origin.get("survey_revision")), "missing survey revision")
                reference(origin.get("survey"), root)
            else:
                require("survey" not in origin and "survey_revision" not in origin,
                        "a benchmark comparison cites its corpus and ledger, not an issue survey")
                require(nonempty(origin.get("corpus")), "benchmark origin must name its corpus")
            for field in ("references", "source_references"):
                require(strings(origin.get(field), empty=True), "invalid origin " + field)
                for item in origin[field]:
                    reference(item, root)
            issues = origin.get("issues")
            require(isinstance(issues, list), "origin issues must be a list")
            require(bool(issues) or kind == "benchmark-comparison", "missing origin issues")
            numbers = set()
            for issue in issues:
                require(isinstance(issue, dict), "issue must be an object")
                number = issue.get("number")
                require(type(number) is int and number > 0 and number not in numbers,
                        "invalid or duplicate issue number")
                numbers.add(number)
                require(issue.get("url") == f"https://github.com/cvc5/cvc5/issues/{number}",
                        "issue URL does not match number")
                require(issue.get("state_at_review") in {"open", "closed"}, "invalid issue state")

            proposal = object_at(row, "proposal")
            require(nonempty(proposal.get("application_context")), "missing application context")
            rewrites = proposal.get("rewrites")
            require(isinstance(rewrites, list) and bool(rewrites),
                    "candidate requires at least one explicit lhs -> rhs rewrite")
            for rewrite in rewrites:
                require(isinstance(rewrite, dict), "rewrite must be an object")
                for field in ("lhs", "rhs", "condition", "notation"):
                    require(nonempty(rewrite.get(field)), "missing rewrite " + field)
                variables = object_at(rewrite, "variables")
                require(all(nonempty(k) and nonempty(v) for k, v in variables.items()),
                        "variables must name their sorts")
                check_orientation(expression_tree(rewrite["lhs"]), expression_tree(rewrite["rhs"]),
                                  proposal.get("orientation"))
            drafts = proposal.get("rare_drafts")
            require(strings(drafts, empty=True), "rare_drafts must be a string list")
            require(all(re.match(r"\(define-(?:cond-)?rule\*?\s", d) for d in drafts),
                    "RARE draft must be a declaration")
            for draft in drafts:
                tree = expression_tree(draft)
                if tree[0] in {"define-rule", "define-cond-rule"}:
                    check_orientation(tree[-2], tree[-1], proposal.get("orientation"))
            assessment = object_at(row, "assessment")
            require(assessment.get("validity") in {"argued", "unchecked", "refuted", "not-applicable"},
                    "invalid validity status; parser acceptance is not a proof")
            require(assessment.get("availability") in AVAILABILITY, "invalid availability status")
            require(assessment.get("value") in {"unmeasured", "measured", "not-applicable"},
                    "invalid value status")
            for field in ("validity_reason", "availability_reason", "value_reason"):
                require(nonempty(assessment.get(field)), "missing " + field)
            if filing and "closed_verdict" not in row:
                require(assessment["availability"] in {"source-gap-candidate", "unchecked"},
                        "file a proposed rewrite, not a known-rule context or reachability issue")
            checks = object_at(row, "checks")
            require(checks.get("rare_syntax") in {"passed", "not-run"}, "invalid RARE check")
            if checks["rare_syntax"] == "passed":
                require(bool(drafts) and revision(checks.get("rare_parser_revision")),
                        "RARE parser pass requires drafts and a revision")
            else:
                require(checks.get("rare_parser_revision") is None, "unrun parser check has a revision")
            for field in ("solver", "performance"):
                require(checks.get(field) in {"not-run", "recorded"}, "invalid " + field + " check")
                if checks[field] == "recorded":
                    reference(checks.get(field + "_evidence"), root)
            if assessment["value"] == "measured":
                require(checks["performance"] == "recorded", "measured value needs run evidence")

            carried = row.get("carried", [])
            require(isinstance(carried, list), "carried must be an event list")
            for delivery in carried:
                require(isinstance(delivery, dict) and nonempty(delivery.get("to")),
                        "delivery requires a recipient")
                day(delivery.get("on"))
                reference(delivery.get("evidence"), root)
            reassessments = row.get("reassessments", [])
            require(isinstance(reassessments, list), "reassessments must be an event list")
            for event in reassessments:
                require(isinstance(event, dict) and nonempty(event.get("reason")),
                        "reassessment requires a reason")
                require(day(event.get("on")) >= observed, "reassessment precedes observation")
                reference(event.get("evidence"), root)
                reference(event.get("previous_record"), root)
            closed = any(k.startswith("closed_") for k in row)
            verdict = row.get("closed_verdict")
            if closed:
                require(verdict in VERDICTS and nonempty(row.get("closed_why")), "invalid closure")
                require(day(row.get("closed_on")) >= observed, "closure precedes observation")
                require(strings(row.get("closed_evidence")), "closure needs evidence")
                for item in row["closed_evidence"]:
                    reference(item, root)
                if verdict in {"accepted and fixed", "fixed and landed"}:
                    require(revision(row.get("closed_commit")) and revision(row.get("closed_checked_at")),
                            "fix verdict needs implementation and rechecked source commits")
                if verdict == "re-coded":
                    require(row.get("replacement_id") != identity and nonempty(row.get("replacement_id")),
                            "re-coded requires a different replacement identity")
            if verdict == "accepted and fixed":
                debt = object_at(row, "awaiting_landing")
                require(debt.get("project") == row["owner"] and nonempty(debt.get("branch"))
                        and revision(debt.get("commit")), "invalid landing debt")
                require(debt["commit"] == row["closed_commit"], "landing debt names a different fix")
            else:
                require("awaiting_landing" not in row, "landing debt requires accepted and fixed")
        except (ValueError, TypeError) as exc:
            raise ValueError(f"{identity!r}: {exc}") from exc
    if not filing:
        for row in rows:
            if row.get("closed_verdict") == "re-coded":
                require(row["replacement_id"] in seen, "replacement record is not retained")
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path, default=DATABASE)
    parser.add_argument("--filing", action="store_true", help="accept a producer list without ingestion dates")
    args = parser.parse_args()
    try:
        rows = validate(json.loads(args.file.read_text()), filing=args.filing)
    except (OSError, ValueError) as exc:
        print(f"rewrite database: {exc}", file=sys.stderr)
        return 1
    print(f"rewrite database: {len(rows)} records satisfy the local metadata contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
