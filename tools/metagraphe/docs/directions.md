# Search areas and candidate rewrites

**Initial search map, 2026-09-16.** These are places to investigate, not claims
that cvc5 lacks particular rules. None has been audited for this project yet.
The scope and evidence criteria are in the [charter](../README.md).

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

No concrete candidates have been recorded yet. Give each new candidate a stable
`M-N` identifier and a section here. Each record carries:

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
