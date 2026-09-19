# Complex operators before structural size

**2026-09-19 — human clarification.** The human permits growth when eliminating
costly operators and specified a lexicographic ordering, complex operators
first. This supersedes the size-only interpretation in the
[preceding review](2026-09-19-rewrite-orientation.md).

## Current directions

| family | primary cost | cost vector before -> after | decision |
| --- | --- | --- | --- |
| M-1 | `str.replace_all` count | `(1, 6) -> (0, 7)` | Restore replacement elimination into two containment tests; priority 1. |
| M-5 | `re.comp` count | `(1, 5) -> (0, 7)` | Restore the positive two-range character class; priority 2. |
| M-11 | `bvurem` count | `(1, 5) -> (0, 8)` | Restore the existing comparison-to-Boolean rule; the old compression guard size(x) < 4 no longer applies. |
| M-16 | `str.to_lower` count | `(1, 4) -> (0, 7)` | Restore fixed-target preimage expansion; exact conversion semantics remain unchecked. |
| M-12 | structural size | `(4) -> (3)` | Keep removing `abs`: reversing it would add an operator while leaving `mod` present. |

Each vector lists declared complex-operator counts in priority order, then
term size. The first differing component decides; size is a tie-breaker.
`proposal.orientation` makes that precedence and its rationale explicit for
each of the four growing schemas and their associated RARE drafts. Other
schemas retain decreasing structural size. A structural decrease alone is not
a reason to introduce costly operators; review operator precedence first.

The [previous working-tree records](2026-09-19-rewrite-operator-order-before.json)
retain the four compression directions and their assessments. The original
elimination records are retained in the
[first review's snapshot](2026-09-19-rewrite-orientation-before.json). Current
records append another reassessment without changing identities, semantic
conditions, observation dates, or ingestion dates. Original availability
assessments apply again where the original direction was restored; this is
not a fresh source audit. The JSON, survey, prompt, and generated view agree.

## Validation and limits

The current ten RARE drafts were parsed and passed through
`mkrewrites.validate_rule` at cvc5 source
`dbf176dfb71b272ffbfdee06888dace73fee5aa8`, using the
[recorded reproduction command](2026-09-19-rewrite-orientation.md#checks-and-reproduction).
The local validator compares the declared lexicographic costs for schemas and
ordinary drafts. Regression cases cover permitted growth, reversed costly
operator introductions, operator precedence before size, and size tie-breaks.

These are syntactic priorities backed by a written rationale, not runtime
measurements or validity proofs. Account for duplication of compound subterms
and interaction with other normalizers. M-16's semantics remain unchecked;
no solver experiment or measured speedup is claimed.
