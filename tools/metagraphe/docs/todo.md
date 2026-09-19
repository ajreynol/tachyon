# metagraphe — initial work queue

**Started 2026-09-16.** This ordering is the AI agent's initial assessment.
The human has set the focus to strings and bit-vectors; no separate human
ranking has been supplied. All tasks below remain open.

| priority | next step | concrete output |
| ---: | --- | --- |
| 1 | Pin cvc5's commit, build, options, and the entry point for observing rewrites. Select one small string probe and one bit-vector probe. | A baseline ledger entry with inputs, exact commands, and actual outputs. |
| 2 | Read the existing rewrite implementations and regression cases for S1 and B1 in the [search map](directions.md). | A source audit with pinned paths and candidate identities, marking anything already handled. |
| 3 | Reduce the first plausible gap from each primary theory and check its conditions and equivalence. | Small reproduction cases, validity queries or arguments, and recorded results. |
| 4 | Look for those patterns in a named benchmark sample or generated term set. | A recorded manifest or generation recipe and an account of where the patterns occur. |
| 5 | Assess the strongest candidate's usefulness and write up the finding. | Evidence of simplification or measured impact, with remaining uncertainty and possible next experiments. |

After an experiment, add its evidence to the [ledger](ledger/README.md),
update the candidate register, and revise this queue. Build a helper only when
the next experiment needs it. A human's independent decision to pursue a
finding is not a prerequisite for further discovery.
