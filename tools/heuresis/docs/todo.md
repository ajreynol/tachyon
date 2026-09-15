# heuresis — active top ten

The ten research directions to work on next, in priority order. The ranking
applies to research directions, not table rows: a direction may have several
independent **possible next first steps**, so its rank is repeated. Any one of
those rows is a reasonable place for an AI agent or human to begin; the rows
are alternatives, not a required sequence.

Each direction comes from [`directions.md`](directions.md). After completing a
step, record the evidence in [`../ledger/`](../ledger/), rerank the ten
directions, and replace or refine that direction's possible first steps.

**Updated.** 2026-09-15.

| rank | research direction | effort | possible next first step |
| ---: | --- | --- | --- |
| 1 | [R13 — The SAT backend](directions.md#r13--the-sat-backend-cadical-minisat-restarts-units) | 🟢 Low Risk / 🟡 Medium Gain | Confirm the effective backend on one baseline command with `-o options-auto` before launching another corpus run. |
| 1 | [R13 — The SAT backend](directions.md#r13--the-sat-backend-cadical-minisat-restarts-units) | 🟢 Low Risk / 🟡 Medium Gain | Rerun the fixed baseline with explicit `--sat-solver=cadical`, using the same set and timeout. |
| 1 | [R13 — The SAT backend](directions.md#r13--the-sat-backend-cadical-minisat-restarts-units) | 🟢 Low Risk / 🟡 Medium Gain | On a small fixed gap slice, compare explicit CaDiCaL with `--no-incremental` to detect effects beyond backend selection. |
| 2 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟢 Low Risk / 🟢 High Gain | Capture `--stats-internal` and `-o inst` for the first ten gap benchmarks and inventory the counters actually present. |
| 2 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟢 Low Risk / 🟢 High Gain | Specify the smallest normalized result schema using one cvc5 output and one z3 profile before writing a corpus extractor. |
| 2 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟢 Low Risk / 🟢 High Gain | Build [`ajreynol:qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) and identify which of its counters are still missing from main. |
| 3 | [R24 — A domain configuration](directions.md#r24--a-domain-configuration-run-cvc5-the-way-verus-runs-z3) | 🟢 Low Risk / 🟢 High Gain | Run `--no-cbqi` alone against the baseline to isolate its share of the existing two-flag win. |
| 3 | [R24 — A domain configuration](directions.md#r24--a-domain-configuration-run-cvc5-the-way-verus-runs-z3) | 🟢 Low Risk / 🟢 High Gain | Run `--user-pat=strict` alone against the baseline to isolate its share of the existing two-flag win. |
| 3 | [R24 — A domain configuration](directions.md#r24--a-domain-configuration-run-cvc5-the-way-verus-runs-z3) | 🟢 Low Risk / 🟢 High Gain | Choose one unmeasured mainline flag from R24 and run it alone on the fixed gap set before constructing a bundle. |
| 4 | [R27 — SMT-LIB parser throughput](directions.md#r27--smt-lib-parser-throughput-pay-less-before-solving) | 🟡 Medium Risk / 🟡 Medium Gain | Measure `--parse-only` wall time and input bytes across the corpus to bound parsing's possible contribution. |
| 4 | [R27 — SMT-LIB parser throughput](directions.md#r27--smt-lib-parser-throughput-pay-less-before-solving) | 🟡 Medium Risk / 🟡 Medium Gain | Profile parsing on one large solved-but-slow input to distinguish lexing, symbol lookup, term construction, and command execution. |
| 4 | [R27 — SMT-LIB parser throughput](directions.md#r27--smt-lib-parser-throughput-pay-less-before-solving) | 🟡 Medium Risk / 🟡 Medium Gain | Build [`ajreynol:ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt) and A/B it on a fixed sample of the largest generated inputs. |
| 5 | [R23 — Term-database relevance](directions.md#r23--term-database-relevance-which-ground-terms-e-matching-may-use) | 🟡 Medium Risk / 🟢 High Gain | Run `--term-db-mode=all` against `relevant-all-delay`, recording instances, time, and the last-call fallback. |
| 5 | [R23 — Term-database relevance](directions.md#r23--term-database-relevance-which-ground-terms-e-matching-may-use) | 🟡 Medium Risk / 🟢 High Gain | Run `--term-db-mode=relevant` against `relevant-all-delay`, recording unknowns as well as performance. |
| 5 | [R23 — Term-database relevance](directions.md#r23--term-database-relevance-which-ground-terms-e-matching-may-use) | 🟡 Medium Risk / 🟢 High Gain | Add or locate counters for term-database size and terms rejected by relevance, then measure a small gap slice. |
| 6 | [R10 — Instance-lemma decision order](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟡 Medium Risk / 🟢 High Gain | Run `--inst-local` alone, treating it as a scoped-cache and justification experiment rather than clause deletion. |
| 6 | [R10 — Instance-lemma decision order](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟡 Medium Risk / 🟢 High Gain | Run `--jh-rlv-order` alone and compare decision counts as well as wall time. |
| 6 | [R10 — Instance-lemma decision order](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟡 Medium Risk / 🟢 High Gain | Build [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) and test it on a fixed gap slice against both mainline alternatives. |
| 7 | [R9 — Deleting instantiation lemmas](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 🔴 High Risk / 🟢 High Gain | Add a time-series counter for persistent SAT clauses and run it on the ten worst benchmarks. |
| 7 | [R9 — Deleting instantiation lemmas](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 🔴 High Risk / 🟢 High Gain | Instrument the fraction of instantiation clauses that participate in a conflict before designing a deletion policy. |
| 7 | [R9 — Deleting instantiation lemmas](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 🔴 High Risk / 🟢 High Gain | Compile and regression-test the [`ajreynol:satNotify`](https://github.com/ajreynol/cvc5/tree/satNotify) notification plumbing without enabling deletion. |
| 8 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🔴 High Risk / 🟢 High Gain | Compare cvc5 full-effort round counts with z3 instance-generation depth on a fixed gap sample. |
| 8 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🔴 High Risk / 🟢 High Gain | Build [`ajreynol:eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) and reproduce its shipped Verus regressions before a corpus run. |
| 8 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🔴 High Risk / 🟢 High Gain | Run [`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) on a fixed gap slice with conservative explicit pacing limits. |
| 9 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🔴 High Risk / 🟢 High Gain | Measure `theory::QuantifiersEngine::time_ematching` as a fraction of solve time across the gap set. |
| 9 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🔴 High Risk / 🟢 High Gain | Add one counter separating newly found matches from matches rediscovered across instantiation rounds. |
| 9 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🔴 High Risk / 🟢 High Gain | Build [`ajreynol:ai-emFilter`](https://github.com/ajreynol/cvc5/tree/ai-emFilter) and count filtered triggers, saved matches, and filter time on a small slice. |
| 10 | [R4 — Instantiation budgeting](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | 🔴 High Risk / 🟢 High Gain | Compare the distributions of instances per round and total instances in cvc5 and z3 profiles for the same benchmarks. |
| 10 | [R4 — Instantiation budgeting](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | 🔴 High Risk / 🟢 High Gain | Sweep the explicit generation, pair, and per-round limits in [`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) on a fixed sample. |
| 10 | [R4 — Instantiation budgeting](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | 🔴 High Risk / 🟢 High Gain | Use `--inst-max-rounds` and `--inst-max-level` as diagnostic caps on a small sample, recording unknowns and regressions rather than treating them as a production policy. |
