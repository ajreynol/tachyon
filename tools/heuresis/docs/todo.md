# heuresis — short-term goals and the active top ten

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

## Short-term goals

**The actionable layer.** The two ranked tables below order *research
directions*, which are long-lived and move slowly. This table is the small set
of concrete things in flight or next, each with the condition that closes it.
A goal here is closed by a ledger entry or a pushed counter, not by a judgement.
It is the AI agent's own queue; it does not override either ranking.

**Updated.** 2026-09-16, after S1 closed. Bounded eager instantiation is a
net loss on this set but rescues 29 gap cases nothing else reaches
([evidence](../ledger/2026-09-16-bounded-eager-instantiation.md)); S2 and the
new S6/S7 follow from that split result, and S5 is promoted because the run
turned R9's premise into measurement.

| # | short-term goal | blocked on | closed when |
| ---: | --- | --- | --- |
| ✅ S1 | Read out the three eager-instantiation arms against the combined control | — | **Closed 2026-09-16.** [`2026-09-16-bounded-eager-instantiation.md`](../ledger/2026-09-16-bounded-eager-instantiation.md): module-off is main to within 2 solves and 0 benchmarks ≥2× either way; `--eager-inst` costs 19.46% PAR2, `--eager-inst-rlv` 10.88%; together they rescue 29 of the 461 control-unsolved gap cases, only 5 shared. |
| S2 | Capture the eager module's counters (`d_statPairs`, `d_statMatches`, `d_statInst`, `d_statRematch`, `d_procTime`, `d_addInstTime`) on **both** eager arms, not just a winner | nothing — the branch is built and the arms are known | the counters are read for the 29 rescues and for the 125 benchmarks `--eager-inst` makes ≥2× slower, so the loss and the rescues have a mechanism rather than a total |
| S5 | Count persistent instance clauses and how often one is used in a conflict | nothing; a counter patch | both counters are measured on the gap set. **Promoted:** S1 measured the drowning — 13.7% less time on solved, 109 more timeouts — so R9's premise is now evidence, not folklore |
| S6 | Find whether a cheap static predicate separates the 29 rescued benchmarks from the 125 that `--eager-inst` makes ≥2× slower | S2 | either a predicate is identified and stated, or it is recorded that the obvious syntactic ones do not separate the two sets |
| S7 | Confirm the 29 rescues are not boundary artefacts | nothing | the two eager arms are rerun at a longer timeout and the rescued set is reported as reproduced, shrunk or gone |
| S3 | Make the mainline new-versus-rediscovered instantiation count a registered statistic | the updated [`ajreynol:qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) being pushed; the public ref is still `9f3e4ae6a1`, 398 behind / 29 ahead | `--stats` reports unique versus total instantiations on current main, so R2's question can be asked outside the eager module |
| S4 | Count the shared-equality propagations that central mode and `ai-eecNoShare` skip, and the callback time they cost | nothing; a fresh counter patch, no branch to rebase | the skipped-propagation count and callback time are measured on the gap set, so R15's 10.3% PAR2 signal has a mechanism attached to it |

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

**Updated.** 2026-09-16, after the eager-instantiation runs
([evidence](../ledger/2026-09-16-bounded-eager-instantiation.md)). The
provisional rank R1 and R28 held in the preceding revision is now settled by
measurement, and it did not survive intact: eager instantiation as implemented
is a net loss, so R1 falls from a rank it held on promise. It does not fall
far, because the same run produced this project's first candidate finding — 29
gap cases reachable only through an eager mode. R9 rises to 1 on the strength
of a measured mechanism rather than a recalled one, which also converges with
the maintainer's ranking; that convergence is evidence-driven and not
deference. This remains the AI agent's independent ordering.

| rank | research direction | effort | next possible step |
| ---: | --- | --- | --- |
| 1 | [R9 — Deleting instantiation lemmas](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 🔴 High Risk / 🟢 High Gain | S1 measured the drowning directly: 13.7% less time on solved, 109 more timeouts, 19 more unknowns. Add persistent-clause and conflict-use counters (S5), then design deletion. |
| 2 | [R15 — Equality-engine architecture](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 🔴 High Risk / 🟢 High Gain | Still the largest measured signal: central mode cuts current-main PAR2 10.3%. Count skipped shared-equality propagations and callback time (S4); [`ajreynol:ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare) itself is neutral. |
| 3 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🔴 High Risk / 🟢 High Gain | Not a default: −19.46% PAR2 at branch budgets, −10.88% with `--eager-inst-rlv`. But 29 gap cases are reachable only this way. Take the module's counters (S2), then ask what separates the rescues from the slowdowns (S6). |
| 4 | [R28 — Eager conflict-based instantiation](directions.md#r28--eager-conflict-based-instantiation-find-a-useful-instance-before-full-effort) | 🔴 High Risk / 🟢 High Gain | The bounded matcher exists and is measured; the untested half is acceptance. Add conflict/unit acceptance so an eager instance is kept only when it conflicts or propagates, which is the obvious answer to a 19% unpaced loss. |
| 5 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🔴 High Risk / 🟢 High Gain | E-matching is 27.8% of gap-set time. `d_statRematch` answers this inside the eager module (S2); `qdebugStats` has the mainline count as a `Trace`, needing the port in S3. |
| 6 | [R7 — Entailment filtering](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 🟢 Low Risk / 🟡 Medium Gain | Add evaluator pushes, early-rejection, time, and memory counters before designing a narrower replacement; [`ajreynol:ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) is neutral and evaluator-off remains better. |
| 7 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟢 Low Risk / 🟢 High Gain | Produce the first normalized per-benchmark attribution table for the current gap; the eager run showed how little a bare PAR2 total says without one. |
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
| 2 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🔴 High Risk / 🟢 High Gain | Push the rebased bounded eager branch, then test it on a fixed slice of the current gap with full-round and time-to-first-useful-instance counters. |  |
| 3 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🔴 High Risk / 🟢 High Gain | Add a new-versus-rediscovered E-match counter now that E-matching is measured at 27.8% of gap-set time. |  |
| 4 | [R15 — Equality-engine architecture](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 🔴 High Risk / 🟢 High Gain | Count the work skipped by [`ajreynol:ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare), which passes regressions but is timing-neutral; test central mode on a second corpus. |  |
| 5 | [R6 — Conflict-based instantiation](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | 🟢 Low Risk / 🟡 Medium Gain | Classify the 49 benchmarks that emit any QCF conflict lemma before doing further work on structural QCF. |  |
| 6 | [R10 — Instance-lemma decision order](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟡 Medium Risk / 🟢 High Gain | Classify the rescues and losses from `--inst-local` and `--jh-rlv-order` before considering [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer). |  |
| 7 | [R7 — Entailment filtering](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 🟢 Low Risk / 🟡 Medium Gain | Add evaluator-work counters before a fresh focused design; [`ajreynol:ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) passes regressions but is neutral and loses to evaluator-off. |  |
| 8 | [R17 — Linear integer arithmetic](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | 🔴 High Risk / 🟡 Medium Gain | Intersect the 283 DIO-conflict and 278 branch-and-bound cases with the new gap before testing `--no-dio-solver` or [`ajreynol:ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc). |  |
| 9 | [R16 — Datatypes](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 🟡 Medium Risk / 🟡 Medium Gain | Add eligible-versus-suppressed split counters before testing relevance gating; global binary splitting was negative. |  |
| 10 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟢 Low Risk / 🟢 High Gain | Produce the first normalized per-benchmark attribution table for the current 796-case gap. |  |

## Branch maintenance

**Concrete request to the maintainer:** please push the updated
[`ajreynol:qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats).
The public ref is still `9f3e4ae6a1`, unchanged from the previous audit, so
the update is not yet visible to dev1 and short-term goal S3 stays blocked.
The previous request is closed: the rebased
[`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst)
tip was pushed, and it has since built and passed `make regress`. The fork's
`master` already matches upstream, so no base fast-forward is needed.

This is the AI agent's rebase assessment, not part of the human priority
ranking. It is intentionally evidence-sensitive: a stale experimental branch
does not need maintenance until its cheaper prerequisite experiment points to
it. Every row below was live-audited 2026-09-16 against
[`cvc5:main@95050cf815`](https://github.com/cvc5/cvc5/commit/95050cf8155d),
which advanced one commit from the `d7d03b082c` of the preceding audit.
Behind / ahead is `git rev-list --left-right --count main...branch`, the
symmetric difference that `submit`'s BEHIND check tests; where that disagrees
with a figure carried in an earlier row, the row says so rather than
overwriting it silently.
“Clean trial” means a disposable local rebase, never a mutation of the fork.

| recommendation | branch | directions | behind / ahead | reason or trigger |
| --- | --- | --- | ---: | --- |
| ✅ No base action | [`ajreynol:master`](https://github.com/ajreynol/cvc5/tree/master) | all | 0 / 0 | The fork base already equals current upstream main, and tracked it across the one commit main advanced. |
| 🟡 Keep; do not upstream as a default | [`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | R1, R28 | 0 / 6 | **Tested 2026-09-16.** Built, regression-clean at `995b23bcfa`, and with the module off it is main to within 2 solves and 0 benchmarks ≥2× either way — an unusually clean control. `--eager-inst` costs 19.46% PAR2, so no default follows; but it rescues 29 otherwise-unsolved gap cases, so keep the branch as the substrate for S2, S6, S7 and the R28 acceptance layer. |
| 🔵 Please push updated tip | [`ajreynol:qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) | R26, R2 | 398 / 29 | The maintainer reports an update, but the public ref is unchanged at `9f3e4ae6a1`. Blocks S3. When it lands, port only the missing counters — in particular the `#inst unique/total` figure, which today is a `Trace("ajr-temp-stats")` line and not a registered statistic. |
| 🟡 Instrument before upstreaming | [`ajreynol:ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare) | R15 | 1 / 2 | Behind only because main advanced; the 2026-09-16 result stands. Regression-clean; the effective one-file patch adds two net solves and changes PAR2 −0.20%, within observed noise. Count skipped propagation work first (S4). |
| ⚪ Do not upstream from this result | [`ajreynol:ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) | R7 | 1 / 3 | Behind only because main advanced; the result stands — one net solve and 0.09% PAR2 worse than evaluator-on, 3.91% worse than evaluator-off. Any retry should be a focused port with counters. *(The preceding audit recorded “0 / 320 history commits” for this branch; today's symmetric difference is 3 ahead, 2 of them non-merge. The discrepancy is in the counting, not in the branch, and is left visible.)* |
| 🟠 Mine; do not rebase wholesale | [`ajreynol:eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi) | R28 | 1267 / 204 | Its first replayed commit conflicts in equality and quantifier-engine files; retain its conflict/unit modes as design evidence for the acceptance layer now going on top of `claude-eagerInst`. |
| 🟡 Do not rebase yet | [`ajreynol:ai-cbqi-0423`](https://github.com/ajreynol/cvc5/tree/ai-cbqi-0423) | R6 | 219 / 4 | Clean trial, but current QCF emits only 54 conflict lemmas after 272,280 rounds and costs 0.24% directly; this branch optimizes the wrong first target for this corpus. |
| 🟡 Instrument first | [`ajreynol:dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant) | R16 | 139 / 2 | Clean trial, but global binary splitting was negative; count eligible and suppressed relevance-gated splits before maintaining the branch. |
| 🟠 Port selectively; do not rebase wholesale | [`ajreynol:dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3) | R15 | 179 / 31 | Its first replayed commit conflicts in `inference_manager.cpp`; start with the clean one-commit equality branch instead. |
| 🟡 Defer despite clean trial rebase | [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) | R9, R10 | 131 / 2 | Both mainline global ordering controls regressed; classify their helped subsets first. |
| ⚪ Wait for parser timing | [`ajreynol:ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt) | R27 | 317 / 2 | Rebase only if `--parse-only` shows a material front-end share. |
| ⚪ Wait for slice analysis | [`ajreynol:ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc) | R17 | 130 / 3 | Intersect DIO and branch-and-bound activity with the current 796-case gap before maintaining the branch. |
