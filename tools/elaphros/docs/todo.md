# Priorities and planning queue

**2026-09-18. No experiments are queued.** The current request authorizes
branch analysis and priority setting. The ranking below is the agent's
assessment from source, not a measured ordering or maintainer approval of it.
The [progress record](progress.md) names what is still unknown.

## Maintainer guidance

- Investigate proof-production performance in a style similar to Heuresis.
- Use the public development branches at
  [ajreynol/cvc5](https://github.com/ajreynol/cvc5).
- Give `ajreynol:unrewrite` and `ajreynol:pfrConvert` explicit attention as major ideas.
- Look beyond names for substantial proof-postprocessor changes.
- Set the table for priorities; do not run experiments yet.

No ordered human ranking, fixed corpus or target overhead has been supplied.
This section records the guidance without converting it into invented ranks.

## Agent research priorities

The main recommendation is to lead with **avoiding unnecessary elaboration**.
Smaller cache and checker patches stay visible, but should not define the
research agenda merely because they are easier to port. E12's comparison
design is a prerequisite across the table and is not ranked as an optimization.

| rank | direction | why it is here | next planning step |
| ---: | --- | --- | --- |
| 1 | [E2: smaller macro obligations](directions.md#e2-smaller-macro-obligations) | A contained way to probe whether full-formula elaboration creates avoidable work; present branch has concrete decompositions. | Extract the logical cases in `ajreynol:reduceTransform` and distinguish them from the larger CPC bundle. |
| 2 | [E1: unrewriting](directions.md#e1-unrewriting) | Major opportunity to remove entire rewrite justifications; maintainer-highlighted, but current transformation runs late. | State admissible atom substitutions and distinguish postprocessing compression from early avoidance. |
| 3 | [E3: compact conversion](directions.md#e3-compact-term-conversion) | Major representation question across term conversions; maintainer-highlighted. | Compare both rule contracts, construction paths and external checker requirements. |
| 4 | [E4: rewrite dependencies](directions.md#e4-rewrite-dependencies) | Directly targets proofs of irrelevant child rewrites; closely complements E1/E2. | Specify probe/translation costs and candidate shapes where dependency minimization can help. |
| 5 | [E5: DAG simplification/sharing](directions.md#e5-proof-dag-simplification-and-sharing) | Can discard work before expansion and exposes meaningful deltas inside misleadingly named bundles. | Separate existing mainline behavior from additional TRANS/CONG simplification. |
| 6 | [E6: rewrite provenance](directions.md#e6-recorded-rewrite-provenance) | High potential to replace reconstruction search, but broad changes to rewriting complicate attribution. | Split the `ajreynol:rdbExec` design into execution, recording and reconstruction effects. |
| 7 | [E7: reconstruction cache/policy](directions.md#e7-reconstruction-cache-and-search-policy) | Narrow comparison candidates, including the surviving cache-clear delta. | Audit cache validity/lifetime and remove inherited ablation changes from the conceptual comparison. |
| 8 | [E8: internal resolution checking](directions.md#e8-resolution-construction-and-internal-checking) | Recent one-file candidate; relevance depends on checker calls in the actual production path. | Map construction/checking call sites before predicting an end-to-end benefit. |
| 9 | [E9: definitions/output](directions.md#e9-definitions-and-proof-output) | Potentially important on large generated inputs, but can improve size without reducing production time. | Compare definition handling and agree on output/validation semantics. |
| 10 | [E10: lazy/theory bookkeeping](directions.md#e10-lazy-bookkeeping-and-theory-reconstruction) | Memory and reconstruction may matter greatly; old branch interfaces and corpus dependence reduce readiness. | Inventory retained generators and identify the applicable theory strata. |

[E11: incremental output](directions.md#e11-incremental-output-and-reuse) is
conditional: promote it into the leading group if real incremental sessions
are selected. Do not flatten sessions into independent queries and claim to
have answered its question. A rank here is research value, not an instruction
to build the branches in that order.

## Planning work

| item | status / completion condition |
| --- | --- |
| Snapshot and screen the public fork | Complete: 809 refs, all source-path deltas screened, 49 selected branch summaries retained. |
| Identify the nontrivial postprocessor families | Initial pass complete: E1–E7, including `ajreynol:reduceTransform`, `ajreynol:rewriteDep` and additional simplifications in CPC/trust bundles. |
| Distinguish mainline, sketch and alternative designs | Initial pass complete in the survey; correctness/build readiness remains untested. |
| Deepen the top four designs | Next: short design comparisons specifying preserved proof obligations, fallback paths, phase placement and interactions. No solver execution needed. |
| Select the benchmark subject | Open: choose a fixed corpus and intended use with the maintainer. Candidate strata are rewriting/preprocessing-heavy UNSAT, theory reconstruction, definition-heavy inputs and genuine incremental sessions. Heuresis's corpus is an option, not the default subject. |
| Fix the proof contract | Open: propose CPC with a pinned compatible checker first; decide granularity, allowed trust, input references/definitions and what constitutes a complete proof. Other formats are separate comparisons. |
| Specify the baseline and observables | Open: ordinary / matched settings / proof enabled / emitted proof arms; explicit checking policy, timing boundaries, memory, failures and repetitions. Use existing counters first. |
| Choose what “little overhead” means | Open: agree absolute and relative time/memory criteria before judging success. No threshold inferred from the charter. |

Only after experiments are requested should the prospective measurements in
the directions become runnable configurations. No builds, rebases, benchmark
jobs, checker runs or new harnesses are part of this planning pass.
