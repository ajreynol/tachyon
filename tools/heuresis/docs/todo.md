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
exists, the queue points at it and the register owns the wording. Seventy-nine
proposals across twenty-seven directions currently sit there, ninety-five rows
in all once the option strings are counted separately.

## Runs in flight

One row per wave of the option-and-branch sweep the register specifies. A wave
is finished when its `± solved` cells are filled and a ledger entry carries the
numbers.

| wave | what it measures | state |
| --- | --- | --- |
| **0** | the reference itself, on current `main` [`d7d5b948c1`](https://github.com/cvc5/cvc5/commit/d7d5b948c11d2d83be0212d4a954ef49740ecdab) | **done** — 5550 of 6124 solved, PAR2 41055.9, ratio 1.75, gap 1064 ([ledger](ledger/2026-09-23-reference-at-current-main.md)); now the last row of [`progress.md`](progress.md) |
| **1** | the 20 option rows, each the reference plus one change, same binary | **done** — 21 arms against the 5550 reference; every option row carries a number, and the seven figures taken against `d7d03b082c` are replaced ([ledger](ledger/2026-09-23-option-sweep.md)) |
| **2** | the 70 branch runs | **running, 42 filled** — in its own clone and build directory, against a reference rebuilt there (5576, not Wave 1's 5550, so the two are not comparable [why](ledger/2026-09-24-build-directory-difference.md)). Each branch is 1 or 11 behind the fork's `master`, recorded per row; `submit` would refuse them as BEHIND and this was accepted to get first data ([ledger](ledger/2026-09-24-branch-sweep.md)) |

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

**The expensive combined design remains R1 + R2 + R9** — eager, incremental,
forgetting — and the attribution still has to earn it. Each of the three is
ranked on its own below; none of them is proposed as a bundle until the
measurements say the combination is what the gap needs.

The table contains ten research directions in priority order. Normally a
direction has one row. Where genuinely independent starting choices are
useful, a continuation row leaves the first three columns blank.

Each direction comes from [`directions.md`](directions.md). After completing a
step, record the evidence in [`ledger/`](ledger), rerank the ten
directions, and replace or refine that direction's possible first steps.

The ranking now incorporates the first whole-set attribution statistics and
option A/Bs ([evidence](ledger/2026-09-15-attribution-stats.md)); it should
continue to move when evidence changes.

**Updated.** 2026-09-16, after the eager-instantiation runs
([evidence](ledger/2026-09-16-bounded-eager-instantiation.md)). The
provisional rank R1 and R28 held in the preceding revision is now settled by
measurement, and it did not survive intact: eager instantiation as implemented
is a net loss, so R1 falls from a rank it held on promise. It does not fall
far, because the same run produced this project's first candidate finding — 29
gap cases reachable only through an eager mode. R9 rises to 1 on the strength
of a measured mechanism rather than a recalled one, which also converges with
the maintainer's ranking; that convergence is evidence-driven and not
deference. This remains the AI agent's independent ordering.

| rank | research direction | effort | its rows in the register | next possible step |
| ---: | --- | --- | --- | --- |
| 1 | [R9 — Deleting instantiation lemmas](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 🔴 High Risk / 🟢 High Gain | 3 branch runs + `--inst-local` | S1 measured the drowning directly: 13.7% less time on solved, 109 more timeouts, 19 more unknowns. Add persistent-clause and conflict-use counters (S5), then design deletion. |
| 2 | [R15 — Equality-engine architecture](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 🔴 High Risk / 🟢 High Gain | 3 branch runs + `--ee-mode=central` | Still the largest measured signal: central mode cuts current-main PAR2 10.3%. Count skipped shared-equality propagations and callback time (S4); [`ajreynol:ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare) itself is neutral. |
| 3 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🔴 High Risk / 🟢 High Gain | **13 branch runs** + `--inst-when=full` | Not a default: −19.46% PAR2 at branch budgets, −10.88% with `--eager-inst-rlv`. But 29 gap cases are reachable only this way. Take the module's counters (S2), then ask what separates the rescues from the slowdowns (S6). |
| 4 | [R28 — Eager conflict-based instantiation](directions.md#r28--eager-conflict-based-instantiation-find-a-useful-instance-before-full-effort) | 🔴 High Risk / 🟢 High Gain | 5 branch runs (`eagerCbqi` modes) | The bounded matcher exists and is measured; the untested half is acceptance. Add conflict/unit acceptance so an eager instance is kept only when it conflicts or propagates, which is the obvious answer to a 19% unpaced loss. |
| 5 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🔴 High Risk / 🟢 High Gain | 6 branch runs, no option | E-matching is 27.8% of gap-set time. `d_statRematch` answers this inside the eager module (S2); `qdebugStats` has the mainline count as a `Trace`, needing the port in S3. |
| 6 | [R7 — Entailment filtering](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 🟢 Low Risk / 🟡 Medium Gain | 3 branch runs + `--ieval=off`, `--no-inst-no-entail` | Add evaluator pushes, early-rejection, time, and memory counters before designing a narrower replacement; [`ajreynol:ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) is neutral and evaluator-off remains better. |
| 7 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟢 Low Risk / 🟢 High Gain | 3 runs, all *n/a* — counters, not speed | Produce the first normalized per-benchmark attribution table for the current gap; the eager run showed how little a bare PAR2 total says without one. |
| 8 | [R10 — Instance-lemma decision order](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟡 Medium Risk / 🟢 High Gain | 4 branch runs, no option | Classify the disjoint wins and losses from the two negative global controls before building or rebasing `ai-instDefer`. |
| 9 | [R17 — Linear integer arithmetic](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | 🔴 High Risk / 🟡 Medium Gain | 3 branch runs, no option | Isolate the roughly one-quarter of the old gap with DIO or branch-and-bound activity, intersect it with the new gap, then test a policy change. |
| 10 | [R16 — Datatypes](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 🟡 Medium Risk / 🟡 Medium Gain | 4 branch runs + `--dt-binary-split` | Add eligible-versus-suppressed split counters before pursuing relevance gating; global binary splitting worsened PAR2 1.15%. |

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

**Moved, and mostly gone.** The table that used to sit here was a hand-kept copy
of branch state audited on 2026-09-16; it went stale within a day of every
update pass. Every active branch is now within eleven commits of the pin and
compiles, so there is no maintenance backlog left to rank.

| what | where it lives now |
| --- | --- |
| which commit a branch carries, its distance from the pin, its size, whether it compiles | the shared [`active-dev-branches.md`](../../../docs/active-dev-branches.md), regenerated from the fork rather than maintained by hand |
| why a branch could not be carried forward | beside the fork, in the maintainer's abandoned list; the register retires the row and keeps the question |
| whether to spend an update pass now | this queue — it is what Wave 2 above is waiting on |
