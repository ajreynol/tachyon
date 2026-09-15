# heuresis — active top ten

The ten research directions to work on next, in priority order. Each row is
exactly one direction from [`docs/directions.md`](docs/directions.md). When a
next step is completed, record the evidence in [`ledger/`](ledger/), rerank the
table, and replace the next step with the new smallest action that would settle
that direction.

**Updated.** 2026-09-15.

| rank | research direction | effort | next step |
| ---: | --- | --- | --- |
| 1 | [R13 — The SAT backend](docs/directions.md#r13--the-sat-backend-cadical-minisat-restarts-units) | 🟢 Low Risk / 🟡 Medium Gain | Rerun the fixed baseline with `--sat-solver=cadical`, on the same set and timeout, and record the corrected gap and PAR2 ratio. |
| 2 | [R26 — Attribution instrumentation](docs/directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟢 Low Risk / 🟢 High Gain | Run `--stats-internal` and `-o inst` on the first ten gap benchmarks, then specify the smallest extractor that captures the counters actually present. |
| 3 | [R24 — A domain configuration](docs/directions.md#r24--a-domain-configuration-run-cvc5-the-way-verus-runs-z3) | 🟢 Low Risk / 🟢 High Gain | Run each mainline flag listed under “What to run first” independently against the corrected baseline; build the bundle only from measured wins. |
| 4 | [R27 — SMT-LIB parser throughput](docs/directions.md#r27--smt-lib-parser-throughput-pay-less-before-solving) | 🟡 Medium Risk / 🟡 Medium Gain | Measure `--parse-only` time and input bytes across the set, then A/B [`ajreynol:ai-parserOpt`](https://github.com/ajreynol/CVC4/tree/ai-parserOpt) on the solved-but-slow slice. |
| 5 | [R23 — Term-database relevance](docs/directions.md#r23--term-database-relevance-which-ground-terms-e-matching-may-use) | 🟡 Medium Risk / 🟢 High Gain | Run `--term-db-mode=all` and `--term-db-mode=relevant` against `relevant-all-delay`, recording term-database size, instances, and the last-call fallback. |
| 6 | [R10 — Instance-lemma decision order](docs/directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟡 Medium Risk / 🟢 High Gain | Run `--inst-local` and `--jh-rlv-order` separately; if either wins, build and test [`ajreynol:ai-instDefer`](https://github.com/ajreynol/CVC4/tree/ai-instDefer). |
| 7 | [R9 — Deleting instantiation lemmas](docs/directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 🔴 High Risk / 🟢 High Gain | Add or locate clause-database and instance-conflict-use counters, then measure both over time on the ten worst benchmarks before designing deletion. |
| 8 | [R1 — Eager instantiation](docs/directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🔴 High Risk / 🟢 High Gain | Compare cvc5 full-effort round counts with z3 instance-generation depth on the gap set; test an eager branch only if the two track each other. |
| 9 | [R2 — Incremental E-matching](docs/directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🔴 High Risk / 🟢 High Gain | Measure E-matching's share of solve time and add one counter separating new matches from matches rediscovered across rounds. |
| 10 | [R4 — Instantiation budgeting](docs/directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | 🔴 High Risk / 🟢 High Gain | Compare instances per round and total instances with z3 profiles on the same gap benchmarks before selecting a budget policy. |
