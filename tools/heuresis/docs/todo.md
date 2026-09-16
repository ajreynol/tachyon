# heuresis — active top ten

**These priorities are the AI agent's current assessment, not a measured
ranking or a human-approved plan.** They are based on the initial internal
Google Doc of cvc5 performance notes, its structured
[`notes.md`](../notes.md) summary, and the subsequent source audit in
[`directions.md`](directions.md).

**Purpose of the queue.** Find cvc5 shortcomings and research questions worth
a human's attention. The next steps gather enough evidence to expose a useful
finding. Once one emerges, record it with its research direction and ledger
links, using the [charter's criteria](../README.md#what-makes-a-useful-finding).
A human may independently pursue it at their discretion. Continue discovery
without waiting for that decision; implementation suggestions serve as possible
experiments or starting points for later work.

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
heuresis. It is intentionally separate from the AI-agent assessment above:
AI agents should maintain an independent opinion and should not mirror this
ordering by default. The maintainer owns the ranks; AI agents may fill in and
evolve the possible first steps from the same repository state and evidence
used for the AI-agent table. Human rationale remains blank unless the
maintainer supplies it.

**Initial ranking recorded.** 2026-09-15.

| rank | research direction | effort | next possible step | human rationale |
| ---: | --- | --- | --- | --- |
| 1 | [R9 — Deleting instantiation lemmas](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 🔴 High Risk / 🟢 High Gain | Instrument persistent SAT-clause count and instantiation-clause conflict use on the ten worst benchmarks before designing deletion. |  |
| 2 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🔴 High Risk / 🟢 High Gain | Compare cvc5 full-effort round counts with z3 instance-generation depth on a fixed gap sample before selecting an eager branch. |  |
| 3 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🔴 High Risk / 🟢 High Gain | Measure E-matching's share of solve time; add a new-versus-rediscovered match counter only if that share is material. |  |
| 4 | [R15 — Equality-engine architecture](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 🔴 High Risk / 🟡 Medium Gain | Profile equality-engine time on the ten worst benchmarks, then run `--ee-mode=central` if it is material. |  |
| 5 | [R6 — Conflict-based instantiation](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | 🟢 Low Risk / 🟡 Medium Gain | Run `--no-cbqi` alone against the fixed baseline to isolate CBQI's effect from strict user patterns. |  |
| 6 | [R10 — Instance-lemma decision order](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟡 Medium Risk / 🟢 High Gain | Run `--inst-local` and `--jh-rlv-order` separately; compare decision counts before considering [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer). |  |
| 7 | [R7 — Entailment filtering](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 🟢 Low Risk / 🟡 Medium Gain | Capture the entailed-to-total-instantiation ratio, then compare `--ieval=off`, `--ieval=use-learn`, and `--no-inst-no-entail`. |  |
| 8 | [R17 — Linear integer arithmetic](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | 🔴 High Risk / 🟡 Medium Gain | Capture branch-and-bound and Diophantine lemma counts on the relevant gap slice before testing `--no-dio-solver` or building [`ajreynol:ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc). |  |
| 9 | [R16 — Datatypes](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 🟡 Medium Risk / 🟡 Medium Gain | Capture `DATATYPES_SPLIT` counts on the gap set, then test `--dt-binary-split` if splitting is material. |  |
| 10 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟢 Low Risk / 🟢 High Gain | Capture `--stats-internal` and `-o inst` for the first ten gap benchmarks and define the smallest normalized result schema. |  |

## Branch maintenance

**Current recommendation:** fast-forward `ajreynol:master`, then rebase
`ajreynol:ai-instDefer`. Do not rebase `qdebugStats` wholesale yet, and leave
the remaining branches alone until their prerequisite measurement is positive.

This is the AI agent's rebase assessment, not part of the human priority
ranking. It is intentionally evidence-sensitive: a stale experimental branch
does not need maintenance until its cheaper prerequisite experiment points to
it. Counts below are commits unique to current upstream `main` / unique to the
branch, audited 2026-09-15 against
[`cvc5:main@2900761`](https://github.com/cvc5/cvc5/commit/2900761a7c2e2c0e99e2cf669cffa3740ea9a138).

| recommendation | branch | directions | behind / ahead | reason or trigger |
| --- | --- | --- | ---: | --- |
| 🔵 Update base first | [`ajreynol:master`](https://github.com/ajreynol/cvc5/tree/master) | all | 29 / 0 | Fast-forward the fork's base before rebasing an experiment. |
| 🟢 Rebase now | [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) | R9, R10 | 127 / 2 | Both priority lists rank this area highly, and a disposable trial rebase onto current upstream `main` completed cleanly. |
| 🟠 Inspect, then port selectively | [`ajreynol:qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) | R26 | 394 / 29 | A trial rebase conflicts in `candidate_generator.{cpp,h}` and `term_database.cpp`. First inventory what current `main` still lacks after the statistics run; port only the needed counters. |
| ⚪ Wait for an equality-engine profile | [`ajreynol:dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3) | R15 | 175 / 31 | Rebase only if equality-engine time is material on the ten worst benchmarks. |
| ⚪ Wait for parser timing | [`ajreynol:ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt) | R27 | 313 / 2 | Rebase only if `--parse-only` shows a material front-end share. |
| ⚪ Wait for arithmetic counters | [`ajreynol:ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc) | R17 | 126 / 3 | Rebase only if Diophantine or branch-and-bound lemmas identify the relevant slice. |
| ⚪ Wait for datatype counters | [`ajreynol:dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant) | R16 | 135 / 2 | Rebase only if `DATATYPES_SPLIT` is material and the mainline binary-split experiment is promising. |
| ⚪ Wait for the mainline option | [`ajreynol:preregRlv`](https://github.com/ajreynol/cvc5/tree/preregRlv) | R22 | 217 / 155 | Its rebase surface is large; test `--preregister-mode=lazy` first. |
| ⚪ Wait for eager-instantiation attribution | [`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | R1 | 135 / 5 | Rebase only if full-effort-round and instance-depth measurements support an eager experiment. |
