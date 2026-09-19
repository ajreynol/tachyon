# Documentation index

The [front page](../README.md) introduces tachyon. These guides describe the
shared tools and how to maintain them. Each research project under
[`tools/`](../tools) has its own charter, documentation index and evidence.

| document | purpose |
| --- | --- |
| [github-issues-rewrites.md](github-issues-rewrites.md) | Metagraphe's cvc5 issue survey, ranked rewrite candidates, RARE drafts, and implementation handoff. |
| [Metagraphe rewrite database](../tools/metagraphe/rewrite_db/README.md) | Structured filings, update and reporting policy, and the experience log. |
| [job-launcher.md](job-launcher.md) | Configure experiments, deploy host scripts, launch jobs and retrieve results. |
| [stats-profiler.md](stats-profiler.md) | Interpret statistics, configure timers and export offline reports and PDFs. |
| [site.md](site.md) | Build and deploy the published report site, and add a project report to it. |
| [maintenance.md](maintenance.md) | Maintain this tree, apply result-retention rules, run CI checks and review findings and correspondence. |
| [discussion.md](discussion.md) | Live correspondence drafted here for a person to carry. |

These Markdown pages are maintained by hand. The profiler's HTML, CSV, JSON
and PDFs are generated and rewritten whole; they are described in the
[profiler guide](stats-profiler.md#generated-artifacts).
