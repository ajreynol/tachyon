#!/usr/bin/env python3
"""Render rewrites.md from the validated JSON; --check detects a stale view."""
import argparse
import html
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote, urlsplit

from check_rewrite_db import DATABASE, expression_tree, orientation_cost, term_size, validate


OUTPUT = DATABASE.with_suffix(".md")
COMMAND = "python3 tools/metagraphe/scripts/render_rewrite_db.py"


def prose(value):
    """Keep database text literal in Markdown, including inside table cells."""
    value = html.escape(str(value), quote=False)
    value = re.sub(r"([\\`*_{}\[\]()#+.!>~-])", r"\\\1", value)
    return value.replace("|", "&#124;").replace("\n", "<br>")


def block(value, language="text"):
    fence = "`" * max(3, 1 + max((len(m) for m in re.findall(r"`+", value)), default=0))
    return f"{fence}{language}\n{value}\n{fence}"


def link(label, reference):
    # All local evidence paths in JSON start at the repository root. The view
    # lives three levels below it; preserve query strings and fragment anchors.
    target = reference if urlsplit(reference).scheme else "../../../" + reference
    return f"[{prose(label)}]({quote(target, safe='/:#?=&%+@;,$')})"


def source_revision(revision):
    return link(revision, "https://github.com/cvc5/cvc5/commit/" + revision)


def disposition(row):
    verdict = row.get("closed_verdict", "no closure recorded")
    if "awaiting_landing" in row:
        verdict += "; awaiting landing"
    return verdict


def render(document):
    rows = sorted(validate(document), key=lambda row: int(row["candidate"].split("-")[1]))
    rewrites = sum(len(row["proposal"]["rewrites"]) for row in rows)
    drafts = sum(len(row["proposal"].get("rare_drafts", [])) for row in rows)
    closed = sum("closed_verdict" in row for row in rows)
    pending = sum("awaiting_landing" in row for row in rows)
    lines = [
        "# Metagraphe rewrites", "",
        "Generated from [rewrites.json](rewrites.json) by",
        "[`render_rewrite_db.py`](../scripts/render_rewrite_db.py), and **rewritten whole** on",
        "every run: anything typed in here is lost at the next one, so edit the JSON instead.",
        "See the [database guide](README.md) for filing and the",
        "[reporting policy](reporting-policy.md) for reassessment and closure.", "",
        f"Regenerate from tachyon's root with `{COMMAND}`; add `--check` to check freshness.", "",
        f"**{len(rows)} candidate families; {rewrites} proposed rewrites; {drafts} RARE drafts.**",
        f"**{closed} explicit closure verdicts; {pending} fixes awaiting landing.**", "",
        "A record is a candidate family, not a count of new rules or solved issues.",
        "`argued` denotes a written validity argument, not a checked proof. RARE parser",
        "acceptance does not establish correctness or solver performance. Priorities",
        "are metagraphe's assessments; closure concerns the proposed rewrite.",
        "Issues supply motivation and evidence; their states are snapshots at review.",
        "Existing-rule investigations and other issue triage are retained in the",
        "[scope archive](../docs/ledger/2026-09-19-rewrite-candidate-scope.md).", "",
        "**Orientation: LHS -> RHS, complex -> simpler.** Compare lexicographically:",
        "counts of the declared complex operators first, then structural term size.",
        "Eliminating a costly operator can therefore justify a larger RHS. Records name",
        "the precedence and rationale; these are candidate orderings, not measured runtimes.", "",
        "## Overview", "",
        "| Candidate | Priority | Validity | RARE drafts | Closure | Source issues |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        candidate = row["candidate"]
        issues = ", ".join(link(f"#{issue['number']}", issue["url"])
                           for issue in row["origin"]["issues"]) or "—"
        cells = [f"[{candidate}: {prose(row['description'])}](#{candidate.lower()})",
                 str(row["priority"]) if row["priority"] else "—",
                 prose(row["assessment"]["validity"]),
                 str(len(row["proposal"].get("rare_drafts", []))), prose(disposition(row)), issues]
        lines.append("| " + " | ".join(cells) + " |")

    for row in rows:
        proposal, checks, origin = row["proposal"], row["checks"], row["origin"]
        lines += ["", f"## {row['candidate']}", "", f"**{prose(row['description'])}**", "",
                  f"Priority: {row['priority'] or 'not ranked'}. "
                  f"Theories: {', '.join(prose(t) for t in row['theories'])}.", "",
                  f"**Closure:** {prose(disposition(row))}.", ""]
        if "closed_verdict" in row:
            lines += [f"On {row['closed_on']}: {prose(row['closed_why'])}", "",
                      "Evidence: " + ", ".join(link(f"closure {i}", ref) for i, ref
                                               in enumerate(row["closed_evidence"], 1)) + ".", ""]
            for field, label in (("closed_commit", "Fix commit"),
                                 ("closed_checked_at", "Rechecked source")):
                if field in row:
                    lines += [f"{label}: {source_revision(row[field])}.", ""]
            if "replacement_id" in row:
                replacement = row["replacement_id"].split(":", 1)[1]
                lines += [f"Replacement: [{replacement}](#{replacement.lower()}).", ""]
            if "awaiting_landing" in row:
                debt = row["awaiting_landing"]
                lines += [f"**Awaiting landing:** {prose(debt['project'])}, "
                          f"branch {prose(debt['branch'])}, {source_revision(debt['commit'])}.", ""]
        lines += [f"**Application context:** {prose(proposal['application_context'])}", ""]
        if proposal.get("orientation"):
            orientation = proposal["orientation"]
            lines += ["**Orientation order:** "
                      + " > ".join(prose(op) + " count" for op in orientation["operators"])
                      + " > term size. "
                      + prose(orientation["reason"]), ""]
        else:
            lines += ["**Orientation rationale:** decrease structural term size.", ""]
        for i, rewrite in enumerate(proposal["rewrites"], 1):
            variables = "; ".join(f"{prose(name)}: {prose(sort)}"
                                  for name, sort in rewrite["variables"].items())
            lines += [f"### Rewrite {i}", "", f"Notation: {prose(rewrite['notation'])}.", "",
                      f"Variables: {variables or 'none'}.", "",
                      block(f"{rewrite['lhs']}\n  ->\n{rewrite['rhs']}\n\nwhen: {rewrite['condition']}"), "",
                      f"Structural size: **{term_size(rewrite['lhs'])} -> {term_size(rewrite['rhs'])}** term nodes.", ""]
            if proposal.get("orientation"):
                costs = [orientation_cost(expression_tree(rewrite[side]), proposal["orientation"])
                         for side in ("lhs", "rhs")]
                lines += [f"Lexicographic cost: **{costs[0]} -> {costs[1]}**.", ""]
        if proposal.get("rare_drafts"):
            lines += ["### RARE drafts", ""]
            for draft in proposal["rare_drafts"]:
                lines += [block(draft, "lisp"), ""]
        else:
            lines += ["No RARE draft is filed.", ""]
        lines += ["### Assessment and next step", ""]
        for field in ("validity", "availability", "value"):
            assessment = row["assessment"]
            lines += [f"- **{field.title()}: {prose(assessment[field])}.** "
                      + prose(assessment[field + "_reason"])]
        parser_revision = checks.get("rare_parser_revision")
        lines += ["", f"**RARE syntax:** {prose(checks['rare_syntax'])}"
                  + (" at " + source_revision(parser_revision) if parser_revision else "") + ".", ""]
        for field in ("solver", "performance"):
            evidence = checks.get(field + "_evidence")
            lines += [f"**{field.title()} check:** {prose(checks[field])}"
                      + ("; " + link("evidence", evidence) if evidence else "") + ".", ""]
        if row.get("cautions"):
            lines += ["**Cautions:**", ""] + ["- " + prose(c) for c in row["cautions"]] + [""]
        if origin["issues"]:
            found = "Source issues: " + ", ".join(link(f"#{i['number']}", i["url"])
                                                  + f" ({i['state_at_review']} at review)"
                                                  for i in origin["issues"]) + "."
        else:
            found = ("No source issue: this candidate comes from a benchmark comparison "
                     f"over {prose(origin['corpus'])}.")
        if origin.get("survey"):
            provenance = (link("Survey", origin["survey"])
                          + f" (tachyon revision `{origin['survey_revision']}`); "
                          + link("investigation ledger", origin["ledger"]) + ".")
        else:
            provenance = ("Corpus: " + prose(origin["corpus"]) + "; "
                          + link("investigation ledger", origin["ledger"]) + ".")
        lines += [f"**Next step:** {prose(row['next_step'])}", "",
                  "### Evidence and follow-up", "", found, "",
                  f"Observed: {row['observed_on']} at cvc5 source {source_revision(row['found_at'])}.", "",
                  f"Koine ingestion: first {row['first_seen']}; last {row['last_seen']}.", "",
                  provenance, ""]
        if row.get("reassessments"):
            lines += ["**Dated reassessments:**", ""]
            lines += [f"- {event['on']}: {prose(event['reason'])} "
                      + link("review", event["evidence"]) + "; "
                      + link("previous record", event["previous_record"]) + "."
                      for event in row["reassessments"]] + [""]
        for field, label in (("references", "Supporting references"),
                             ("source_references", "Source references")):
            if origin.get(field):
                lines += [f"**{label}:**", ""]
                lines += ["- " + link(ref, ref) for ref in origin[field]] + [""]
        if row.get("carried"):
            lines += ["**Recorded deliveries:**", ""]
            lines += [f"- {event['on']} to {prose(event['to'])}: " + link("evidence", event["evidence"])
                      for event in row["carried"]] + [""]
        else:
            lines += ["No delivery recorded.", ""]
        lines += ["[Back to overview](#overview)"]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the view is missing or stale; never write")
    args = parser.parse_args(argv)
    try:
        expected = render(json.loads(DATABASE.read_text(encoding="utf-8")))
        if args.check:
            if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
                print(f"rewrite view is missing or stale; run: {COMMAND}", file=sys.stderr)
                return 1
            print("rewrite view is current")
        else:
            OUTPUT.write_text(expected, encoding="utf-8")
            print(f"wrote {OUTPUT}")
    except (OSError, ValueError) as exc:
        print(f"rewrite view: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
