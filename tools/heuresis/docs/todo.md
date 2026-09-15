# heuresis — active top ten

**These priorities are the AI agent's current assessment, not a measured
ranking or a human-approved plan.** They are based on the initial internal
Google Doc of cvc5 performance notes, its structured
[`notes.md`](../notes.md) summary, and the subsequent source audit in
[`directions.md`](directions.md).

## AI-agent priorities

The table contains ten research directions in priority order. Normally a
direction has one row. Where genuinely independent starting choices are
useful, a continuation row leaves the first three columns blank.

Each direction comes from [`directions.md`](directions.md). After completing a
step, record the evidence in [`../ledger/`](../ledger/), rerank the ten
directions, and replace or refine that direction's possible first steps.

**Updated.** 2026-09-15.

| rank | research direction | effort | next possible step |
| ---: | --- | --- | --- |
| 1 | [R13 — The SAT backend](directions.md#r13--the-sat-backend-cadical-minisat-restarts-units) | 🟢 Low Risk / 🟡 Medium Gain | Confirm the effective backend on one baseline command with `-o options-auto`, then rerun the fixed baseline with explicit `--sat-solver=cadical`. |
| 2 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟢 Low Risk / 🟢 High Gain | Capture `--stats-internal` and `-o inst` for the first ten gap benchmarks and define the smallest normalized result schema. |
|  |  |  | Build [`ajreynol:qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) and identify which of its counters are still missing from main. |
| 3 | [R27 — SMT-LIB parser throughput](directions.md#r27--smt-lib-parser-throughput-pay-less-before-solving) | 🟡 Medium Risk / 🟡 Medium Gain | Measure `--parse-only` wall time and input bytes across the corpus; build [`ajreynol:ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt) only if parsing is material. |
| 4 | [R23 — Term-database relevance](directions.md#r23--term-database-relevance-which-ground-terms-e-matching-may-use) | 🟡 Medium Risk / 🟢 High Gain | Compare `--term-db-mode=all`, `relevant`, and `relevant-all-delay`, recording instances, unknowns, time, and the last-call fallback. |
| 5 | [R10 — Instance-lemma decision order](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟡 Medium Risk / 🟢 High Gain | Run `--inst-local` and `--jh-rlv-order` separately; compare decision counts before considering [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer). |
| 6 | [R9 — Deleting instantiation lemmas](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 🔴 High Risk / 🟢 High Gain | Instrument persistent SAT-clause count and instantiation-clause conflict use on the ten worst benchmarks before designing deletion. |
| 7 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🔴 High Risk / 🟢 High Gain | Compare cvc5 full-effort round counts with z3 instance-generation depth on a fixed gap sample before selecting an eager branch. |
| 8 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🔴 High Risk / 🟢 High Gain | Measure E-matching's share of solve time; add a new-versus-rediscovered match counter only if that share is material. |
| 9 | [R4 — Instantiation budgeting](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | 🔴 High Risk / 🟢 High Gain | Compare instances per round and total instances in cvc5 and z3 profiles before selecting a budget policy. |
| 10 | [R22 — Preregistration](directions.md#r22--preregistration-which-literals-the-theories-are-told-about) | 🟡 Medium Risk / 🟡 Medium Gain | Run `--preregister-mode=lazy` on the gap set; build [`ajreynol:preregRlv`](https://github.com/ajreynol/cvc5/tree/preregRlv) only if the mainline experiment moves the target counters. |

## Human-maintainer priorities

This is the current priority list as judged by the human maintainer of
heuresis. It is intentionally separate from the AI-agent assessment and may
rank the same directions differently. It remains blank until the maintainer
fills it in.

| rank | research direction | effort | next possible step | human rationale |
| ---: | --- | --- | --- | --- |
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |
| 6 |  |  |  |  |
| 7 |  |  |  |  |
| 8 |  |  |  |  |
| 9 |  |  |  |  |
| 10 |  |  |  |  |
