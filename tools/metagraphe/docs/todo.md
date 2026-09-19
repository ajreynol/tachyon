# metagraphe — work queue

**Started 2026-09-16; updated 2026-09-19.** The human requested the initial
[GitHub issue survey](../../../docs/github-issues-rewrites.md), now completed
as a source audit and candidate writeup, and then requested the
[rewrite database](../rewrite_db/README.md). The initial JSON filing and
[experience log](experience.md) are in place. This ordering is the AI agent's
assessment within the human's string and bit-vector focus. The executable
baseline and experiments below remain open.

| priority | next step | concrete output |
| ---: | --- | --- |
| 1 | Build a clean binary matching the survey's pinned source (or record a newer baseline), options, and simplification entry point. Probe M-1/M-2/M-3 and the BV candidate M-4. | A baseline ledger entry with inputs, exact commands, and actual outcomes. |
| 2 | Extend the survey's targeted source audit to normalization paths, preprocessing, and regressions for those candidates. Check the existing #10520 rule as a control. | Distinguish missing rules from matching, context, or configuration gaps. |
| 3 | Reduce the strongest gap from each primary theory and check its conditions and equivalence, including the survey's counterexamples. | Small reproduction cases, validity queries or arguments, and recorded results. |
| 4 | Look for those patterns in a named benchmark sample or generated term set. | A recorded manifest or generation recipe and an account of where the patterns occur. |
| 5 | Assess the strongest candidate's usefulness and write up the finding. | Evidence of simplification or measured impact, with remaining uncertainty and possible next experiments. |

After an experiment, add its evidence to the [ledger](ledger/README.md),
file new observations through the database workflow, record reassessments
without overwriting the original claims, and revise this queue. Build a helper only when
the next experiment needs it. A human's independent decision to pursue a
finding is not a prerequisite for further discovery.
