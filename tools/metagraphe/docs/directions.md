# Search areas and candidate rewrites

**Search map started 2026-09-16; issue survey added 2026-09-19.** These are
places to investigate, not claims that cvc5 lacks particular rules. The scope
and evidence criteria are in the [charter](../README.md).

## Search areas

| id | area | first question |
| --- | --- | --- |
| S1 | String concatenation and length | Which combinations expose constant fragments or length information that could simplify another operation? |
| S2 | Substrings, containment, and replacement | Which nested operations admit simpler forms, with the exact index, emptiness, or containment conditions? |
| S3 | Strings at theory boundaries | Do regular-expression membership, integer conversions, or Boolean context expose useful simplifications? |
| B1 | Extraction, concatenation, and extension | Which compositions admit narrower or simpler expressions, and which already normalize in cvc5? |
| B2 | Masks, shifts, and bitwise operations | Which nested operations expose constant or unused bits, including boundary shift amounts? |
| B3 | Modular arithmetic and comparisons | Which arithmetic or comparison patterns simplify under explicit width and signedness conditions? |

Keep both strings and bit-vectors represented in the initial probes. Rank
concrete candidates by evidence, likely usefulness, and the cost of resolving
uncertainty. Source inspection, existing regression cases, benchmark terms,
small-term enumeration, and other solvers can all suggest candidates.

## Filed candidates

The [rewrite database](../rewrite_db/README.md) owns filed candidate identities,
conditions, evidence, assessments, and later verdicts. The
[GitHub issue survey](../../../docs/github-issues-rewrites.md) is the dated
narrative behind the initial M-1 through M-10 families and the triage rows
subsequently filed as M-11 through M-20. The
[scope correction](ledger/2026-09-19-rewrite-candidate-scope.md) moves six triage
rows to the ledger, leaving only concrete candidate rewrites in the database. The
[source audit](ledger/2026-09-19-github-issues.md) and
[filing record](ledger/2026-09-19-rewrite-db.md) distinguish the original
investigation from its migration to JSON. M-21 and M-22 instead come from the
[string benchmark comparison](ledger/2026-09-20-string-benchmark-comparison.md),
which also records four confirmed gaps that are **not** rewrite candidates:
quadratic word equations, `re.loop` unrolling, regular-expression containment
expressed through concatenation with otherwise-unconstrained variables, and
nested case maps.

| IDs | search areas | investigation |
| --- | --- | --- |
| M-1, M-2 | S2 | Singleton replacement and containment before an index match. |
| M-3, M-9 | S1, S3 | String prefix ordering and order totality. |
| M-4 | B3 | Signed comparison disjunction. |
| M-5, M-10 | S3 | Character complements and intersections of character-language stars. |
| M-6, M-7 | Secondary arithmetic | Guarded division and modular identities motivated by issues. |
| M-12 | Secondary arithmetic | Remove absolute value from a nonzero modulus divisor. |
| M-13, M-14 | S2 | Nested replacement emptiness and prefix/index identities. |
| M-16 | S3 | Inverse case conversion. |
| M-18 | B3 | Quotient simplification under explicit no-overflow premises. |
| M-21, M-22 | S3 | Regular-expression shapes from the [string benchmark comparison](ledger/2026-09-20-string-benchmark-comparison.md). |
| M-23, M-24 | S3 | Bounded repetition: fixed-length `re.loop` membership, and star or plus of a loop. |
| M-25 | S2, S3 | Degenerate patterns in `str.replace_re_all`. |

This table is a search-area map, not a parallel status register. Use the
database for candidate proposals and the ledger for existing coverage and
excluded directions. Allocate subsequent IDs under its identity policy and
preserve these IDs. Each filed record carries:

- The search-area ID, origin, and proposed `lhs -> rhs`, including conditions,
  sorts, and width parameters.
- **Validity:** unchecked, supported for the stated scope, or refuted, with
  the proof argument, queries, or counterexample linked.
- **Availability:** unchecked, already handled, or missing at the recorded
  cvc5 stage and configuration, with actual output and source evidence linked.
- **Value:** unmeasured, a structural simplification, or a measured effect,
  with an explicit cost model and the limits of any performance claim.
- The open question or next discriminating experiment, and links to the
  [ledger](ledger/README.md) and any saved cases.

Preserve rejected and already-handled search leads in the ledger with the
reason, so the next search does not rediscover them. Genuine filed proposals
remain in the database with their later verdicts. A finding can motivate further research while
its performance value remains unmeasured; state that limitation plainly.
