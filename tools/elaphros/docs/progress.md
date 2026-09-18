# Investigation progress

**Updated 2026-09-18. Planning only; no experiments.**

| question | current evidence |
| --- | --- |
| What is the public development inventory? | 809 branch heads from `ajreynol/cvc5`, with full SHA snapshot. |
| Was the scan limited to proof-like names? | No. All heads were screened by their merge-base source paths; 203 touch proof/rewrite paths under the recorded heuristic. |
| How much was investigated further? | 49 selected branches have source-delta/history summaries; the survey explains the most relevant mechanisms. This is not a correctness review of all 49. |
| What is the comparison source? | `cvc5/cvc5` main at `3dcc1ef5421ab62cc1ee9af52d70042ce6861af0`. |
| What ideas did the maintainer highlight? | `ajreynol:unrewrite` and `ajreynol:pfrConvert`, plus a request to look beyond names for substantial postprocessor changes. No numerical ranking supplied. |
| What are the research candidates? | Twelve directions with source evidence and prospective discriminating observations. |
| Which corpus, format, checker and success threshold are fixed? | None. CPC is proposed as an initial format in the queue, not adopted as a benchmark contract. |
| How much overhead is measured? | Unknown; no ordinary/proof baseline pairs. |
| What fraction is attributed? | Unknown; no profiles or phase measurements. |
| Which branches build and produce validated proofs? | Not established here. |
| Which optimizations improve time or memory? | None established. |

All inventory counts come from the [source survey](../ledger/2026-09-18-branch-survey.md).
The [priority queue](todo.md) ranks information to acquire, not measured wins.
Readiness to measure requires a fixed comparison and a genuine proof output and
validation path; Tachyon's solve wrapper alone does not provide that path.

Future progress should report completed validated pairs, added seconds and
time ratios, peak memory, output size, checker time and all non-success
outcomes. Keep a session-level view for incremental workloads. Do not fill
these fields with estimates derived from line counts or branch age.
