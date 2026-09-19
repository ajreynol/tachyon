# Candidate rewrites are the reporting unit

**2026-09-19 — scope correction requested by the human.** Report candidate
rewrites, not issues in the rewriter. This is a local review of the existing
survey and JSON; no new GitHub scan, cvc5 source audit, or solver run was made.
The pre-change database is at tachyon
`258102dcfd0a7d21bc2963825acef58bea119214`.

## Retained proposals and archived triage

The database now contains 14 candidate families, 16 explicit `lhs -> rhs`
schemas, and the same ten RARE drafts. A conditional schema can be a candidate
even if its conditions need contextual reasoning. Uncertain validity or
availability remains labeled; a candidate is not an established missing rule
or a solved issue. Existing complex-operator-first directions are unchanged.

Six records move out of the database and its generated view into this ledger:

| former ID | reason for archiving |
| --- | --- |
| M-8 | The filed substring-length identity already exists. The remaining work concerns learned bounds and applying/composing existing rules to an encoded reversal. No new identity was proposed. |
| M-11 | The remainder-comparison identity is already represented in RARE and C++; this was a reachability control. |
| M-15 | A substring-containment lead with no exact LHS, RHS, and bounds extracted from the attachment. |
| M-17 | A synthesis/ITE/extract lead with no exact identity extracted from the attachment. |
| M-19 | A proof-export/RARE naming consistency issue, with no simplifying identity. |
| M-20 | Search-order performance, with no proposed simplifying identity. |

Their complete records, including dates, source references, assessments, and
prior reassessments, are retained verbatim as JSON objects in the
[snapshot](2026-09-19-rewrite-candidate-scope-before.json). Its `archived_ids`
identifies the six records removed from the current database. These are
historical triage, not closure verdicts, fixed issues, or upstream deliveries.
Their IDs remain reserved. A future concrete proposal from one of these leads
gets a new ID and links to the archived origin.

M-12 remains: `(mod x (abs y)) -> (mod x y)` under `y != 0` is an explicit
candidate in the requested direction. Its previous `existing-coverage`
classification referred to historical learned-rewrite context, while its
assessment already said availability of this direction was unchecked. Corrected
the classification to `candidate`, assigned priority 3, and focused its title
and context on the rule. Its previous complete record is also in the snapshot;
the retained record links this dated reassessment. The identity, side condition,
validity/availability/value assessments, and original dates are unchanged.

The other 13 retained records are unchanged. Genuine filed candidates remain
in the database if later rejected or found implemented, with a supported
verdict or reassessment. This requested scope correction is not a general
deletion workflow or a closure-only edit.

## Workflow changes and validation

The owner validator now requires `classification: candidate`, priority 1–3,
and a nonempty list of explicit term schemas. Producer filings reject new open
known-rule/context controls. Semantic scope remains a review obligation;
supplying an arbitrary equality cannot turn a rewriter defect into a candidate.
The reporting policy, standing agent guidance, and survey launcher record this
scope. The readable view reports candidate families and source issues, and
links here for historical triage. The experience log remains unchanged because
this work was internal.

Reproduce the checks from the repository root:

```bash
python3 tools/metagraphe/scripts/check_rewrite_db.py
python3 tools/metagraphe/scripts/render_rewrite_db.py --check
KOINE=/path/to/koine python3 scripts/check.py
python3 /path/to/anoieu/scripts/policy_check.py --policy-version 1 --root .
bash -n prompts/metagraphe_read_github
./prompts/metagraphe_read_github --show-prompt
```

The repository check passed all 135 tests, including 27 metagraphe tests and
the real pinned-koine integration, plus retention and launcher checks. The
shared policy check reported zero failures and six inapplicable checks skipped.
The prompt parsed and rendered successfully; the generated view is current.
These checks validate the tooling and retained data, not rewrite semantics.

Compared the JSON objects against the pre-change revision: the six archives
and M-12 snapshot match, retained order is preserved, the other 13 records
are unchanged, and all retained terms/RARE drafts are unchanged.
The migration held the database lock and atomically replaced
the current JSON after saving the snapshot. Koine's closure checker is
deliberately unsuitable for this membership change; subsequent closure work
needs a committed baseline after the migration.
