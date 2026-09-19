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

## Candidate register

The [GitHub issue survey](../../../docs/github-issues-rewrites.md) holds the
initial candidates M-1 through M-10, their identities, conditions, validity
arguments, source availability checks, and next experiments. The
[dated audit](ledger/2026-09-19-github-issues.md) records what was actually checked.

| IDs | search areas | investigation |
| --- | --- | --- |
| M-1, M-2 | S2 | Singleton replacement and containment before an index match. |
| M-3, M-9 | S1, S3 | String prefix ordering and order totality. |
| M-4 | B3 | Signed comparison disjunction. |
| M-5, M-10 | S3 | Character complements and intersections of character-language stars. |
| M-6, M-7 | Secondary arithmetic | Guarded division and modular identities motivated by issues. |
| M-8 | S1, S2, S3 | Learned lengths and substring-encoded reversal; existing rules need context. |

These remain candidates: usefulness is structurally motivated but unmeasured,
and runtime availability is unchecked. The survey separately records
already-covered and lower-confidence leads. Give subsequent candidates new
`M-N` identifiers, preserving these IDs. Each record carries:

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

Preserve rejected and already-handled candidates with the reason, so the next
search does not rediscover them. A finding can motivate further research while
its performance value remains unmeasured; state that limitation plainly.
