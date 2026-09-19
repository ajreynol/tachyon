# Rewrite orientation correction

**Historical review, superseded in part.** The human subsequently clarified
that the ordering is lexicographic, complex operators first. See the
[operator-order review](2026-09-19-rewrite-operator-order.md) for current
directions; the size-only policy and M-11 size guard below are historical.

**2026-09-19 — human-requested direction review.** The standing convention is
`LHS -> RHS`, complex -> simpler. This review uses structural term size:
one node per operator application and per variable/constant occurrence,
counting repeated occurrences separately. Sort annotations and operator
indices are not term nodes. Conditions remain premises. This is an orientation
review of existing equalities, not a new issue scan or solver experiment.

## Corrections

Five of the 18 filed schemas expanded structural size. Their equalities,
sorts, and semantic side conditions were retained and their sides exchanged.
The [complete original records](2026-09-19-rewrite-orientation-before.json)
preserve the proposals, drafts, checks, assessments, and ingestion provenance
from tachyon revision `bf65e85`. Current records keep their IDs and link this
review through `reassessments`. Observation dates and cvc5 source pins were
not advanced.

| family | original size | current size | consequence |
| --- | --- | --- | --- |
| M-1 | 6 -> 7 | 7 -> 6 | Conjunction compression introduces `replace_all`. It does not simplify the original replacement-shaped input; investigate deletion-to-false separately. |
| M-5 | 5 -> 7 | 7 -> 5 | Compress the two full-alphabet ranges into a one-character exclusion. The issue already uses the new RHS. |
| M-11 | 5 -> 8 | 8 -> 5 | General conjunction compression introduces remainder. The historical existing-rule observation supports the opposite direction, whose nonzero-constant specialization remains a useful control. |
| M-12 | 3 -> 4 | 4 -> 3 | Remove `abs` from the nonzero modulus divisor. The historical option discussion does not establish current availability of this direction. |
| M-16 | 4 -> 7 | 7 -> 4 | Compress the two ASCII alternatives into the conversion test. Exact extension semantics remain unchecked. |

M-11 duplicates `x` on the RHS. For substituted terms, the size decrease is
`4 - size(x)`, so only apply that orientation when `size(x) < 4`. This is an
application-size guard, not a new semantic premise. More generally, a smaller
schema alone does not guarantee a smaller term after substitution.

The other 13 schemas were already decreasing. All 18 now decrease as written.
The two M-1 RARE drafts and the M-5 draft were reversed and renamed to describe
the new directions. The other seven drafts were unchanged. Direction-dependent
availability for all five corrections is now unchecked; M-11/M-12 retain their
existing-coverage classification as historical controls, with that distinction
explicit in their application context. M-1 and M-5 move to priority 3 because
their new directions do not establish a remedy for the motivating inputs.

The current JSON, survey, generated view, prompt, and standing project guidance
agree on the direction. Historical source-audit and initial-filing ledger
entries remain dated accounts. Neither those accounts nor the original record
snapshot is a queue of currently recommended orientations.

## Checks and reproduction

All ten current drafts passed `rw_parser.Parser.parse_rules` followed by
`mkrewrites.validate_rule` from the previously retrieved cvc5 source at
[`dbf176dfb71b272ffbfdee06888dace73fee5aa8`](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).
Reproduce using an unpacked copy of that source:

```bash
python3 - /path/to/pinned-cvc5 tools/metagraphe/rewrite_db/rewrites.json <<'PY'
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(sys.argv[1]) / "src/rewriter"))
from rw_parser import Parser
from mkrewrites import validate_rule

rows = json.loads(Path(sys.argv[2]).read_text())["bugs"]
rules = Parser().parse_rules("\n".join(
    draft for row in rows for draft in row["proposal"]["rare_drafts"]))
for rule in rules:
    validate_rule(rule)
print(f"Validated {len(rules)} current draft rules")
PY
python3 tools/metagraphe/scripts/check_rewrite_db.py
python3 tools/metagraphe/scripts/render_rewrite_db.py
python3 scripts/check.py
```

Local regression checks reject growing/equal-size schemas and ordinary RARE
drafts, preserve the reversed equality's conditions and sorts, retain the
original records, and verify the Markdown view. The size checker is a schema
check, not an SMT type checker or a proof of a globally terminating rewrite
system. No solver run, performance improvement, new availability audit, or
upstream action is claimed. Any implementation must check interactions with
existing normalizers rather than enabling both directions.
