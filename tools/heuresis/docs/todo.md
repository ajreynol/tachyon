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

The ranking now incorporates the first whole-set attribution statistics and
option A/Bs ([evidence](../ledger/2026-09-15-attribution-stats.md)); it should
continue to move when evidence changes.

**Updated.** 2026-09-15 after the first evidence sweep.

| rank | research direction | effort | next possible step |
| ---: | --- | --- | --- |
| 1 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🔴 High Risk / 🟢 High Gain | Add a new-versus-rediscovered E-match counter now that E-matching is measured at 27.8% of gap-set time. |
| 2 | [R9 — Deleting instantiation lemmas](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 🔴 High Risk / 🟢 High Gain | Add persistent-clause count and instance-clause conflict-use counters before designing deletion. |
| 3 | [R16 — Datatypes](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 🟡 Medium Risk / 🟡 Medium Gain | Run `--dt-binary-split`; 920 gap cases emitted 27,484 datatype-split lemmas. |
| 4 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟢 Low Risk / 🟢 High Gain | Turn the captured whole-set statistics into the first normalized per-benchmark attribution table. |
| 5 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🔴 High Risk / 🟢 High Gain | Compare the measured cvc5 full-effort rounds with z3 instance-generation depth on a fixed gap sample. |
| 6 | [R7 — Entailment filtering](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 🟢 Low Risk / 🟡 Medium Gain | Compare `--ieval=off`, `--ieval=use-learn`, and `--no-inst-no-entail`; entailed duplicates are 8.1% of gap-set instances. |
| 7 | [R13 — The SAT backend](directions.md#r13--the-sat-backend-cadical-minisat-restarts-units) | 🟢 Low Risk / 🟡 Medium Gain | Make explicit CaDiCaL the control and classify its 55 rescued benchmarks and 116 at-least-2× regressions. |
| 8 | [R15 — Equality-engine architecture](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 🔴 High Risk / 🟡 Medium Gain | Run the existing `--ee-mode=central` control; UF time is material but is not an equality-engine timer. |
| 9 | [R10 — Instance-lemma decision order](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟡 Medium Risk / 🟢 High Gain | Classify the disjoint wins and losses from the two negative global controls before building or rebasing `ai-instDefer`. |
| 10 | [R17 — Linear integer arithmetic](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | 🔴 High Risk / 🟡 Medium Gain | Isolate the roughly one-quarter of gap cases with DIO or branch-and-bound activity before testing a policy change. |

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
| 1 | [R9 — Deleting instantiation lemmas](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 🔴 High Risk / 🟢 High Gain | Add persistent-clause count and instance-clause conflict-use counters before designing deletion. |  |
| 2 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🔴 High Risk / 🟢 High Gain | Compare the measured cvc5 full-effort rounds with z3 instance-generation depth on a fixed gap sample. |  |
| 3 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🔴 High Risk / 🟢 High Gain | Add a new-versus-rediscovered E-match counter now that E-matching is measured at 27.8% of gap-set time. |  |
| 4 | [R15 — Equality-engine architecture](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 🔴 High Risk / 🟡 Medium Gain | Run `--ee-mode=central`; the existing UF timer does not isolate equality-engine cost. |  |
| 5 | [R6 — Conflict-based instantiation](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | 🟢 Low Risk / 🟡 Medium Gain | Inspect the 9 `--no-cbqi`-only and 3 strict-only rescues and measure user-pattern coverage before another global run. |  |
| 6 | [R10 — Instance-lemma decision order](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟡 Medium Risk / 🟢 High Gain | Classify the rescues and losses from `--inst-local` and `--jh-rlv-order` before considering [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer). |  |
| 7 | [R7 — Entailment filtering](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 🟢 Low Risk / 🟡 Medium Gain | Compare `--ieval=off`, `--ieval=use-learn`, and `--no-inst-no-entail`; the entailed-instance ratio is now measured. |  |
| 8 | [R17 — Linear integer arithmetic](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | 🔴 High Risk / 🟡 Medium Gain | Isolate the 283 DIO-conflict and 278 branch-and-bound gap cases before testing `--no-dio-solver` or building [`ajreynol:ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc). |  |
| 9 | [R16 — Datatypes](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 🟡 Medium Risk / 🟡 Medium Gain | Run `--dt-binary-split`; datatype splitting is now measured as material on 920 gap cases. |  |
| 10 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟢 Low Risk / 🟢 High Gain | Turn the captured whole-set statistics into the first normalized per-benchmark attribution table. |  |

## Branch maintenance

**Current recommendation:** fast-forward `ajreynol:master`, but do not urgently
rebase an experimental branch. Port only the missing counters from
`qdebugStats`; run the cheap mainline datatype and equality-engine controls
before reconsidering their branches.

This is the AI agent's rebase assessment, not part of the human priority
ranking. It is intentionally evidence-sensitive: a stale experimental branch
does not need maintenance until its cheaper prerequisite experiment points to
it. Counts below are commits unique to current upstream `main` / unique to the
branch, audited 2026-09-15 against
[`cvc5:main@2900761`](https://github.com/cvc5/cvc5/commit/2900761a7c2e2c0e99e2cf669cffa3740ea9a138).

| recommendation | branch | directions | behind / ahead | reason or trigger |
| --- | --- | --- | ---: | --- |
| 🔵 Update base first | [`ajreynol:master`](https://github.com/ajreynol/cvc5/tree/master) | all | 29 / 0 | Fast-forward the fork's base before rebasing an experiment. |
| 🟡 Defer despite clean trial rebase | [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) | R9, R10 | 127 / 2 | A disposable trial rebase was clean, but both mainline global ordering controls regressed; classify the helped subset before maintaining this branch. |
| 🟠 Port selectively; do not rebase wholesale | [`ajreynol:qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) | R26 | 394 / 29 | A trial rebase conflicts in `candidate_generator.{cpp,h}` and `term_database.cpp`; current main still needs new-versus-rediscovered E-match and clause-use counters, not all 29 commits. |
| ⚪ Wait for an equality-engine profile | [`ajreynol:dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3) | R15 | 175 / 31 | Rebase only if equality-engine time is material on the ten worst benchmarks. |
| ⚪ Wait for parser timing | [`ajreynol:ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt) | R27 | 313 / 2 | Rebase only if `--parse-only` shows a material front-end share. |
| ⚪ Wait for slice analysis | [`ajreynol:ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc) | R17 | 126 / 3 | DIO and branch-and-bound activity appears on only about one quarter of the gap; classify that slice before maintaining the branch. |
| 🟡 Run the mainline control first | [`ajreynol:dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant) | R16 | 135 / 2 | `DATATYPES_SPLIT` is material on 920 gap cases; run `--dt-binary-split`, then rebase this two-commit branch only if that signal is positive. |
| ⚪ Wait for the mainline option | [`ajreynol:preregRlv`](https://github.com/ajreynol/cvc5/tree/preregRlv) | R22 | 217 / 155 | Its rebase surface is large; test `--preregister-mode=lazy` first. |
| ⚪ Wait for eager-instantiation attribution | [`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | R1 | 135 / 5 | Rebase only if full-effort-round and instance-depth measurements support an eager experiment. |
