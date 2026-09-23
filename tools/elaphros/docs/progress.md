# Investigation progress

**Updated 2026-09-19. Planning only; no experiments.**

| question | current evidence |
| --- | --- |
| What is the public development inventory? | 809 branch heads from `ajreynol/cvc5`, with full SHA snapshot. |
| Was the scan limited to proof-like names? | No. All heads were screened by their merge-base source paths; 203 touch proof/rewrite paths under the recorded heuristic. |
| How much was investigated further? | 49 selected branches have source-delta/history summaries; the survey explains the most relevant mechanisms. This is not a correctness review of all 49. |
| What is the comparison source? | `cvc5/cvc5` main at `3dcc1ef5421ab62cc1ee9af52d70042ce6861af0`. |
| What ideas did the maintainer highlight? | `ajreynol:unrewrite` and `ajreynol:pfrConvert`, plus a request to look beyond names for substantial postprocessor changes. No numerical ranking supplied. |
| What are the research candidates? | Sixteen directions with source evidence and prospective discriminating observations. |
| Where do the candidates come from? | E1–E12 from the branch survey, so they map what has been prototyped rather than where cost falls. E13–E16 from a 2026-09-19 audit of pinned main, with no branch behind them. |
| Was the pipeline of main itself read? | Partly. Allocation, traversals, instrumentation and the Eo/CPC output path were read at the pin. Theory-level proof generators, prop-engine proof construction and other formats were not. |
| Can proof-production cost be attributed with what exists? | No. Existing counters are attempts and outcomes; no phase partition and no discarded-work measure exist, and the final-proof histograms are reachable only under `--check-proofs`. |
| Which corpus, format, checker and success threshold are fixed? | None. CPC is proposed as an initial format in the queue, not adopted as a benchmark contract. |
| How much overhead is measured? | Unknown; no ordinary/proof baseline pairs. |
| What fraction is attributed? | Unknown; no profiles or phase measurements. |
| Which branches build and produce validated proofs? | Not established here. |
| Which optimizations improve time or memory? | None established. |
| What changes to cvc5 are proposed? | Twenty branches across E1–E12, each named as a merge candidate the survey characterized; E13–E16 have none. No proposal is measured: each branch is behind upstream main, and a number needs the corpus, baseline and validated measurement goal 1 fixes. See the [proposals tables](../README.md#proposals). |

All inventory counts come from the [source survey](ledger/2026-09-18-branch-survey.md),
and the pipeline observations from the
[pipeline audit](ledger/2026-09-19-pinned-main-pipeline-audit.md).
The [priority queue](todo.md) ranks information to acquire, not measured wins.
Readiness to measure requires a fixed comparison and a genuine proof output and
validation path; Tachyon's solve wrapper alone does not provide that path.

Future progress should report completed validated pairs, added seconds and
time ratios, peak memory, output size, checker time and all non-success
outcomes. Keep a session-level view for incremental workloads. Do not fill
these fields with estimates derived from line counts or branch age.
