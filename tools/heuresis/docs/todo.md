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

**Updated.** 2026-09-16 after the equality, evaluator, datatype, QCF, and
composition runs. This remains the AI agent's independent ordering even where
it differs from the human-maintainer list.

| rank | research direction | effort | next possible step |
| ---: | --- | --- | --- |
| 1 | [R15 — Equality-engine architecture](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 🔴 High Risk / 🟢 High Gain | Rebuild current main, repeat control / central / evaluator-off / combined, then test rebased [`ajreynol:ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare) against the combined comparator. |
| 2 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🔴 High Risk / 🟢 High Gain | Add a new-versus-rediscovered E-match counter now that E-matching is measured at 27.8% of gap-set time. |
| 3 | [R9 — Deleting instantiation lemmas](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 🔴 High Risk / 🟢 High Gain | Add persistent-clause count and instance-clause conflict-use counters before designing deletion. |
| 4 | [R7 — Entailment filtering](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 🟢 Low Risk / 🟡 Medium Gain | Test rebased [`ajreynol:ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) with evaluator pushes, early rejections, completed matches, and evaluator time recorded. |
| 5 | [R28 — Eager conflict-based instantiation](directions.md#r28--eager-conflict-based-instantiation-find-a-useful-instance-before-full-effort) | 🔴 High Risk / 🟢 High Gain | Use rebased [`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) as the bounded eager matcher, then add conflict/unit acceptance instead of invoking structural QCF earlier. |
| 6 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🔴 High Risk / 🟢 High Gain | On the rebased bounded eager branch, compare time-to-first useful instance and full-effort rounds on a fixed slice of the 789-case gap. |
| 7 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟢 Low Risk / 🟢 High Gain | Produce the first normalized per-benchmark attribution table for the new 789-case gap. |
| 8 | [R10 — Instance-lemma decision order](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟡 Medium Risk / 🟢 High Gain | Classify the disjoint wins and losses from the two negative global controls before building or rebasing `ai-instDefer`. |
| 9 | [R17 — Linear integer arithmetic](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | 🔴 High Risk / 🟡 Medium Gain | Isolate the roughly one-quarter of the old gap with DIO or branch-and-bound activity, intersect it with the new gap, then test a policy change. |
| 10 | [R16 — Datatypes](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 🟡 Medium Risk / 🟡 Medium Gain | Add eligible-versus-suppressed split counters before pursuing relevance gating; global binary splitting worsened PAR2 1.15%. |

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
| 2 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🔴 High Risk / 🟢 High Gain | Test the rebased bounded eager branch on a fixed slice of the new gap with full-round and time-to-first-useful-instance counters. |  |
| 3 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🔴 High Risk / 🟢 High Gain | Add a new-versus-rediscovered E-match counter now that E-matching is measured at 27.8% of gap-set time. |  |
| 4 | [R15 — Equality-engine architecture](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 🔴 High Risk / 🟢 High Gain | Repeat the four-arm experiment on current main, then test rebased [`ajreynol:ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare). |  |
| 5 | [R6 — Conflict-based instantiation](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | 🟢 Low Risk / 🟡 Medium Gain | Classify the 49 benchmarks that emit any QCF conflict lemma before doing further work on structural QCF. |  |
| 6 | [R10 — Instance-lemma decision order](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟡 Medium Risk / 🟢 High Gain | Classify the rescues and losses from `--inst-local` and `--jh-rlv-order` before considering [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer). |  |
| 7 | [R7 — Entailment filtering](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 🟢 Low Risk / 🟡 Medium Gain | Test rebased [`ajreynol:ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) with evaluator-work counters against evaluator-off. |  |
| 8 | [R17 — Linear integer arithmetic](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | 🔴 High Risk / 🟡 Medium Gain | Intersect the 283 DIO-conflict and 278 branch-and-bound cases with the new gap before testing `--no-dio-solver` or [`ajreynol:ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc). |  |
| 9 | [R16 — Datatypes](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 🟡 Medium Risk / 🟡 Medium Gain | Add eligible-versus-suppressed split counters before testing relevance gating; global binary splitting was negative. |  |
| 10 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟢 Low Risk / 🟢 High Gain | Produce the first normalized per-benchmark attribution table for the new 789-case gap. |  |

## Branch maintenance

**Concrete request to the maintainer:** please rebase
[`ajreynol:ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare),
[`ajreynol:ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie),
and [`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst)
onto current cvc5 `main`. If doing one first, use `ai-eecNoShare`; it is one
commit and follows the strongest measured control. The fork's `master`
already matches upstream, so no base fast-forward is needed.

This is the AI agent's rebase assessment, not part of the human priority
ranking. It is intentionally evidence-sensitive: a stale experimental branch
does not need maintenance until its cheaper prerequisite experiment points to
it. Counts below are commits unique to current upstream `main` / unique to the
branch, live-audited 2026-09-16 against
[`cvc5:main@835ccd95e`](https://github.com/cvc5/cvc5/commit/835ccd95ed1071828ddaba1de736e925b694ed28).
“Clean trial” means a disposable local rebase, never a mutation of the fork.

| recommendation | branch | directions | behind / ahead | reason or trigger |
| --- | --- | --- | ---: | --- |
| ✅ No base action | [`ajreynol:master`](https://github.com/ajreynol/cvc5/tree/master) | all | 0 / 0 | The fork base already equals current upstream main. |
| 🔵 Please rebase now | [`ajreynol:ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare) | R15 | 201 / 1 | Clean trial; central equality cuts PAR2 9.6%, and this one-file patch removes redundant shared-equality propagation under that mode. |
| 🔵 Please rebase now | [`ajreynol:ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) | R7 | 2186 / 2 | Clean trial; evaluator-off cuts PAR2 3.1%, and this compact branch changes the implicated partial-evaluation traversal. |
| 🔵 Please rebase now | [`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | R1, R28 | 137 / 5 | Clean trial; its budgets make it the practical current substrate for an eager conflict/unit experiment. |
| 🟠 Mine; do not rebase wholesale | [`ajreynol:eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi) | R28 | 1265 / 204 | Its first replayed commit conflicts in equality and quantifier-engine files; retain its conflict/unit modes as design evidence. |
| 🟡 Do not rebase yet | [`ajreynol:ai-cbqi-0423`](https://github.com/ajreynol/cvc5/tree/ai-cbqi-0423) | R6 | 217 / 4 | Clean trial, but current QCF emits only 54 conflict lemmas after 272,280 rounds and costs 0.24% directly; this branch optimizes the wrong first target for this corpus. |
| 🟡 Instrument first | [`ajreynol:dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant) | R16 | 137 / 2 | Clean trial, but global binary splitting was negative; count eligible and suppressed relevance-gated splits before maintaining the branch. |
| 🟠 Port selectively; do not rebase wholesale | [`ajreynol:dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3) | R15 | 177 / 31 | Its first replayed commit conflicts in `inference_manager.cpp`; start with the clean one-commit equality branch instead. |
| 🟠 Port selectively; do not rebase wholesale | [`ajreynol:qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) | R26 | 396 / 29 | Port only the missing new-versus-rediscovered E-match and clause-use counters. |
| 🟡 Defer despite clean trial rebase | [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) | R9, R10 | 129 / 2 | Both mainline global ordering controls regressed; classify their helped subsets first. |
| ⚪ Wait for parser timing | [`ajreynol:ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt) | R27 | 315 / 2 | Rebase only if `--parse-only` shows a material front-end share. |
| ⚪ Wait for slice analysis | [`ajreynol:ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc) | R17 | 128 / 3 | Intersect DIO and branch-and-bound activity with the new 789-case gap before maintaining the branch. |
