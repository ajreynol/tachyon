# heuresis — short-term goals and the active top ten

**These priorities are the AI agent's current assessment, not a measured
ranking or a human-approved plan.** They are based on the initial internal
Google Doc of cvc5 performance notes, its structured
[`notes.md`](notes.md) summary, and the subsequent source audit in
[`directions.md`](directions.md).

**The measuring stick is [`progress.md`](progress.md).** Every goal and rank
below is justified by whether it eventually moves a number there. A direction
that cannot be traced to that table is not a priority, however interesting.

**Purpose of the queue.** Find cvc5 shortcomings and research questions worth
a human's attention. The next steps gather enough evidence to expose a useful
finding. Once one emerges, record it with its research direction and ledger
links, using the [charter's criteria](../README.md#what-makes-a-useful-finding).
A human may independently pursue it at their discretion. Continue discovery
without waiting for that decision; implementation suggestions serve as possible
experiments or starting points for later work.

**Work at the level of a proposal row.** The register's tables are no longer a
list of candidates: each row is **a run someone can launch** — a branch or an
option-default change, the exact option string to add to the
reference stated at the top of [`directions.md`](directions.md), and the
`± solved` it produced. That
is the level of detail to strive for here too. A queue item should name the
rows that would answer it, and a step that cannot be expressed as one or more
runs should say what it is instead: a counter to add, a branch to read, a
source question. "Investigate R*n*" is no longer a step.

**What that changes.** This queue still ranks *directions*, because the ranking
is a judgement about where the gap is and rows cannot carry that. What it stops
doing is restating experiments the register already specifies: where a row
exists, the queue points at it and the register owns the wording.

## Runs in flight

One row per wave of the option-and-branch sweep the register specifies. A wave
is finished when its `± solved` cells are filled and a ledger entry carries the
numbers.

| wave | what it measures | state |
| --- | --- | --- |
| **0** | the reference itself, on current `main` [`d7d5b948c1`](https://github.com/cvc5/cvc5/commit/d7d5b948c11d2d83be0212d4a954ef49740ecdab) | **done** — 5550 of 6124 solved, PAR2 41055.9, ratio 1.75, gap 1064 ([ledger](ledger/2026-09-23-reference-at-current-main.md)). Superseded as the register's anchor by the 5576 build measured in wave 1b; it stays in [`progress.md`](progress.md) as history |
| **1** | the 23 option rows, each the reference plus one change, same binary | **done, then re-run** — the first pass measured against the 5550 build; every arm was re-run in the branch build directory so the whole register shares one reference, and `--cbqi` was added by *removing* `--no-cbqi` ([ledger](ledger/2026-09-25-option-sweep-one-reference.md)) |
| **2** | the 70 branch runs | **done** — all 70 arms, every branch row filled; no arm reaches +20, and the best three are R10 (`--inst-defer` +47/−33, `--inst-defer --dt-split-relevant` +44/−31, `--jh-rlv-inst` +27/−17), each beating the reference on PAR2 ([ledger](ledger/2026-09-24-branch-sweep.md)) |
| **1b** | the option sweep re-run on the branch reference, plus a reference re-run | **done** — 22 arms and the reference on one binary. The reference reproduced 5576 exactly, fixing this project's run-to-run churn at 4 solves each way and putting the ±5 noise band on measured ground ([ledger](ledger/2026-09-25-option-sweep-one-reference.md)) |
| **3** | the 31 `ai-heuresis-*` branch rows, plus the reference at their base `03e5ee1ebf` | **done** — the reference solves 5572, within noise of 5576. One 🟢, R15's `--ee-share-uf-dt --ieval=off` at +59/−32, and it **segfaults on 10 benchmarks** and answers `unknown` on 34. R6's round budgets net +11 to +13 against their QCF control but only break even with the reference. R1 chaining and R11 relevance filtering are red. Everything else is inside noise ([ledger](ledger/2026-09-28-ai-heuresis-branch-sweep.md)) |

## Short-term goals

**The actionable layer.** The two ranked tables below order *research
directions*, which are long-lived and move slowly. This table is the small set
of concrete things in flight or next, each with the condition that closes it.
A goal here is closed by a ledger entry or a pushed counter, not by a judgement.
It is the AI agent's own queue; it does not override either ranking.

**Updated.** 2026-09-17. The eager line (S1, S2, S6, S7) is closed and its
results are in the ledger. Three new goals come from what the 120 s run turned
up — a cvc5 segfault — and from the launcher becoming self-contained, which
means the host scripts are now ours to change.

| # | short-term goal | blocked on | closed when |
| ---: | --- | --- | --- |
| ✅ S1, S2, S6, S7 | the bounded-eager line: read out the arms, take the module's counters, find what separates rescues from slowdowns, test the timeout boundary | — | **Closed 2026-09-16.** [`bounded-eager`](ledger/2026-09-16-bounded-eager-instantiation.md) and [`counters-and-timeout`](ledger/2026-09-16-eager-counters-and-timeout-sensitivity.md). Eager costs 19.46% PAR2 at a 0.77% match rate; 12 gap cases are reachable only through it; rescues and slowdowns separate on cumulative pairs processed |
| ✅ S11 | Record *why* a run failed, without changing the result token | — | **Closed 2026-09-17.** The wrappers append the reason to `errors-<script>-<name>.txt`; the token stays `error`, so no existing number moved. Proven in production: the S12 sweep's log reads `cvc5 suffered a segfault.` for both failures |
| ✅ S12 | Find how many benchmarks the segfault actually affects | — | **Closed 2026-09-17.** [`segfault-scope`](ledger/2026-09-17-segfault-scope-and-failure-logging.md): **2 crashes among the 5845 benchmarks that reach a terminal answer** at 300 s — the same two. A floor, not a total: 279 still time out |
| **S14** | Publish three branches written on 2026-09-23 that answer R-4 and the R-2 format gap: `cacheEntCheck2` (R3, `9fc61815c7`), `emFailMasks2` (R3, `56ad448402`, `--inst-track-fail-masks`), and a whitespace fix for `rareEncodeSubcall` (E7, `f5dc8c80e1`) | nothing — they exist locally and build; `regress0` passes for all three | they are pushed, so the register can carry them as proposals and the shared list can read their state. Until then they are not proposals: an unpublished branch is not something a person can carry upstream. **`emFailMasks2` has had no performance evaluation** and on the one regression where anything moved it *increased* E-matching lemmas 1871 → 1943; do not record it as a win |
| **S10** | File the segfault upstream | the maintainer checking whether the two benchmarks may be shared publicly | the report in [`upstream-questions.md`](upstream-questions.md) is filed. It now carries a measured scope as well as a backtrace and an option bisection. Still the only thing this project has that can go upstream today, and [`progress.md`](progress.md)'s PR table is empty |
| S13 | Measure `--ee-mode=central` on a second corpus | nothing — the launcher is self-contained, and the host carries other benchmark sets | central mode's 10.3% PAR2 win is confirmed or refuted off this one set, which is the stated blocker on an R15 default-change proposal, and the only path that turns an already-measured win into a PR |
| S8 | Add a cumulative eager pair budget, after which the module stands down and lazy instantiation proceeds | nothing — a bounded patch to `eager_inst.cpp` | the option is run on the set. **Success criterion:** eager-plus-budget must beat `best` (35532.7 PAR2), not merely beat unbudgeted eager — halving a 19% loss would be a real result that still moves nothing in `progress.md` |
| S5 | Count persistent instance clauses and how often one is used in a conflict | nothing; a counter patch | both are measured on the gap set. S1 measured the drowning, so R9's premise is evidence |
| S4 | Count the shared-equality propagations that central mode and `ai-eecNoShare` skip, and the callback time they cost | nothing; a counter patch | the count and callback time are measured, so R15's signal has a mechanism as well as a size |
| S3 | Make the mainline new-versus-rediscovered instantiation count a registered statistic | nothing — **unblocked 2026-09-22**: [`ajreynol:qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) is published at `ea71e3e7`, carrying `c2cc3caf` with 31 commits of its own | `--stats` reports unique versus total instantiations on `main@c2cc3caf`. Still **the only path to R2** |
| **S9** | Explain why the control answers `unknown` on 7 benchmarks that `--eager-inst` proves | nothing — no longer waits on S8 | it is known whether one incompleteness is responsible or several. **Promoted:** these 7 have survived 30 s, 120 s and 300 s unchanged, so unlike the rest of the rescue set they are not a timeout artefact and no longer can be |

## AI-agent priorities

**The expensive combined design R1 + R2 + R9 is now the weaker hypothesis.**
Eager, incremental, forgetting was ranked on promise. All three have since been
measured across 24 arms and none of them produces a proposal above the noise
band: R1 is red on every one of its 14 arms, R2's best is +4, R9's best is +3
and its option `--inst-local` is −606. The combination is not refuted — a bundle
can beat its parts — but it can no longer outrank a direction whose parts
already win.

**R10 is that direction.** It owns the three best branch arms in the register
and is the only direction whose branches are positive at all.

The table contains ten research directions in priority order. Normally a
direction has one row. Where genuinely independent starting choices are
useful, a continuation row leaves the first three columns blank.

Each direction comes from [`directions.md`](directions.md). After completing a
step, record the evidence in [`ledger/`](ledger), rerank the ten
directions, and replace or refine that direction's possible first steps.

**Updated.** 2026-09-25, on the first complete register: all 70 branch arms
([ledger](ledger/2026-09-24-branch-sweep.md)) and all 22 option arms re-run so
that every cell shares one reference
([ledger](ledger/2026-09-25-option-sweep-one-reference.md)). This is the first
rerank with nothing pending, and it moved more than any before it, because for
the first time the ranking can be read off measurements rather than priors.

**Two directions clear the noise band and eight do not.** R15 at **+54** and R10
at **+14** are the whole of the register's positive evidence; every other
direction's best arm sits between +12 and −273. The ordering below is therefore
those two first, then the directions whose *mechanism* is measured as
significant even though no proposal exploits it yet, then the directions whose
proposals have now been measured and found flat.

**Three directions fall on their own evidence.** R9 gives up rank 1: the
drowning it identified is real and measured, but four arms later nothing in the
direction exceeds +3, so it is a diagnosis without a remedy rather than a lead.
R1 falls from 3 to 6 — it has 14 arms, all red, the most failed arms of any
direction, and keeps a place only because its rescues are large and unique. R28
falls furthest, 4 to 9: it was ranked on the argument that the bounded matcher's
acceptance half was untested, and its five arms are now tested and flat (+4 to
−13).

**R10's next step is cheap and decisive**, which is the other reason it ranks
second rather than fifth: the question is whether its three arms lose the *same*
benchmarks, and that is an intersection of gap sets already on disk, not a new
run.

| rank | research direction | effort | its rows in the register | next possible step |
| ---: | --- | --- | --- | --- |
| 1 | [R15 — Equality-engine architecture](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 🟥 High Risk / 🟩 High Gain | 4 arms; `--ee-mode=central` **+73/−19, net +54** — the register's only 🟢 | The largest measured effect in the project, and it is an option rather than a branch: its three branch arms are flat or negative (`ai-eecNoShare` +8/−7, `cdno` +5/−4, `dtMergeNotify-v3` +3/−19). So the gain lives in central mode itself, not in anything the fork has written. Count skipped shared-equality propagations and callback time (S4), then ask what the 73 rescued benchmarks share. |
| 2 | [R10 — Instance-lemma decision order](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟨 Medium Risk / 🟩 High Gain | 4 arms, **zero red**; `--inst-defer` **+47/−33, net +14**, `--inst-defer --dt-split-relevant` +44/−31, `--jh-rlv-inst` +27/−17 | The only direction whose branches win. All three beat the reference on PAR2 (38233, 38398, 38661 against the reference's 39304) and `--inst-defer` rescues more benchmarks than any other arm measured. **Intersect the three arms' lost sets** — if they lose the same 33, one mechanism is mispaced and can be gated; if not, the three compose. The gap sets are on disk, so this costs no run. |
| 3 | [R7 — Entailment filtering](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 🟩 Low Risk / 🟨 Medium Gain | 5 arms; `--ieval=off` **+20/−8, net +12**, `--no-inst-no-entail` +8/−9 | Third-best measured result in the register and the cheapest to act on — 🟩 low risk, an existing option, no branch to land. Rises from 6 on that combination. `--ieval=off` rescuing 20 while losing 8 says the evaluator is refusing instances that were worth keeping; add evaluator push/pop and refusal counters and read which. |
| 4 | [R9 — Deleting instantiation lemmas](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 🟥 High Risk / 🟩 High Gain | 4 arms; best `virtualClauseDel` +7/−4; `--inst-local` **−606** | S1 measured the drowning directly — 13.7% less time on solved, 109 more timeouts, 19 more unknowns — and that stands. What has not appeared is a proposal: four arms, best +3, and the one option is catastrophic. Falls from 1 because a measured problem is not a measured lead. Design deletion against the S1 counters rather than trying another scope switch. |
| 5 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🟥 High Risk / 🟩 High Gain | 6 arms; best `ai-quantOpt-1` +11/−7 | Holds rank on mechanism, not on proposals: E-matching is 27.8% of gap-set time, the largest single consumer, while the direction's best arm is +4. That gap between cost and achieved gain is the argument for instrumenting rather than patching. `d_statRematch` answers this inside the eager module (S2); `qdebugStats` needs the port in S3. |
| 6 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🟥 High Risk / 🟩 High Gain | **14 arms, all red**; best `--eager-inst-macro-only` +22/−116; worst `eagerQM` −2539 | The most heavily measured and most thoroughly negative direction in the register. Not a default at any budget. Its claim is now narrow and specific: thirteen of the fourteen arms rescue between 12 and 38 benchmarks the reference cannot solve, `eagerQM` alone rescuing none, and `claude-eagerInst`'s budgets cut the loss from 900 to 120, so pacing works and is simply not paced enough. Ask what separates rescues from slowdowns (S6) before writing another mode. |
| 7 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟩 Low Risk / 🟩 High Gain | 3 rows, all *n/a* — counters, not speed | Unchanged in kind and rising in importance: five of the nine directions above and below it now need a counter rather than an arm, and this is the direction that builds them. Produce the first normalized per-benchmark attribution table. |
| 8 | [R16 — Datatypes](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 🟨 Medium Risk / 🟨 Medium Gain | 5 arms; `dtLazyInst3` +27/−75; `dtSplitRelevant` +9/−7; `--dt-elim` **−945** | Rises from 10 on one number: `dtLazyInst3` rescues 27 benchmarks, among the largest rescues in the register, while losing 75 — a gating problem rather than a dead end. The other end is now bounded too: `--dt-elim` at −945 rules out eliminating datatypes wholesale. Add eligible-versus-suppressed split counters. |
| 9 | [R28 — Eager conflict-based instantiation](directions.md#r28--eager-conflict-based-instantiation-find-a-useful-instance-before-full-effort) | 🟥 High Risk / 🟩 High Gain | 5 arms, all inside noise: +4, +4, +3, −4, −13 | Falls from 4, the largest drop in this rerank. It was ranked on the argument that the bounded matcher existed and only its acceptance half was untested; all five `eagerCbqi` modes are now measured and none moves the set. Either acceptance is the whole of the idea and must be built before the direction is ranked again, or the mechanism does not pay here. |
| 10 | [R17 — Linear integer arithmetic](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | 🟥 High Risk / 🟨 Medium Gain | 3 arms; best `deferBlock` +5/−5; `--dio-solver-last-call` −88 | Holds last place with the register's flattest evidence: its best arm is net 0 and its branches barely move the set. The roughly one-quarter of gap benchmarks with integer reasoning is still worth isolating, but that is a measurement, not a proposal, and `linearSolverSub` was abandoned as a reimplementation. |


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
| 1 | [R9 — Deleting instantiation lemmas](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 🟥 High Risk / 🟩 High Gain | Add persistent-clause count and instance-clause conflict-use counters before designing deletion. |  |
| 2 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🟥 High Risk / 🟩 High Gain | Push the rebased bounded eager branch, then test it on a fixed slice of the current gap with full-round and time-to-first-useful-instance counters. |  |
| 3 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🟥 High Risk / 🟩 High Gain | Add a new-versus-rediscovered E-match counter now that E-matching is measured at 27.8% of gap-set time. |  |
| 4 | [R15 — Equality-engine architecture](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 🟥 High Risk / 🟩 High Gain | Count the work skipped by [`ajreynol:ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare), which passes regressions but is timing-neutral; test central mode on a second corpus. |  |
| 5 | [R6 — Conflict-based instantiation](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | 🟩 Low Risk / 🟨 Medium Gain | Classify the 49 benchmarks that emit any QCF conflict lemma before doing further work on structural QCF. |  |
| 6 | [R10 — Instance-lemma decision order](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟨 Medium Risk / 🟩 High Gain | Classify the rescues and losses from `--inst-local` and `--jh-rlv-order` before considering [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer). |  |
| 7 | [R7 — Entailment filtering](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 🟩 Low Risk / 🟨 Medium Gain | Add evaluator-work counters before a fresh focused design; [`ajreynol:ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) passes regressions but is neutral and loses to evaluator-off. |  |
| 8 | [R17 — Linear integer arithmetic](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | 🟥 High Risk / 🟨 Medium Gain | Intersect the 283 DIO-conflict and 278 branch-and-bound cases with the new gap before testing `--no-dio-solver` or [`ajreynol:ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc). |  |
| 9 | [R16 — Datatypes](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 🟨 Medium Risk / 🟨 Medium Gain | Add eligible-versus-suppressed split counters before testing relevance gating; global binary splitting was negative. |  |
| 10 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟩 Low Risk / 🟩 High Gain | Produce the first normalized per-benchmark attribution table for the current 796-case gap. |  |

## Branch maintenance

**Moved, and mostly gone.** The table that used to sit here was a hand-kept copy
of branch state audited on 2026-09-16; it went stale within a day of every
update pass. Every active branch is now within eleven commits of the pin and
compiles, so there is no maintenance backlog left to rank.

| what | where it lives now |
| --- | --- |
| which commit a branch carries, its distance from the pin, its size, whether it compiles | the shared [`active-dev-branches.md`](../../../docs/active-dev-branches.md), regenerated from the fork rather than maintained by hand |
| why a branch could not be carried forward | beside the fork, in the maintainer's abandoned list; the register retires the row and keeps the question |
| whether to spend an update pass now | this queue — it is what Wave 2 above is waiting on |
