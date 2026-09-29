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
| **1c** | R12's two option rows, the register's last empty cells, plus a reference rebuild at `d7d5b948c1` | **done** — the reference solves 5574, within noise of 5576. `--lemma-inprocess=light` ⚪ +11/−12 and `--conflict-process=min` ⚪ +4/−14. The register has no empty cell left ([ledger](ledger/2026-09-29-lemma-inprocessing-options.md)) |
| **4** | the new R16 branch `dtElim-0929`, with and without `--no-cbqi`, each against a reference at its base `4692619e6a` | **done** — the reference solves 5577, inside noise. 🔴 **−2090** and, with QCF on, −1888 against its own control. It gains nothing, segfaults on over 400 benchmarks and hangs on problems the reference solves instantly ([ledger](ledger/2026-09-29-dt-elim-0929.md)) |

## Short-term goals

**The actionable layer.** The two ranked tables below order *research
directions*, which are long-lived and move slowly. This table is the small set
of concrete things in flight or next, each with the condition that closes it.
A goal here is closed by a ledger entry or a pushed counter, not by a judgement.
It is the AI agent's own queue; it does not override either ranking.

**Updated.** 2026-09-29, from a global view: the register is complete, with every
proposal row measured, and two overlap readings were taken from results already
on disk ([ledger](ledger/2026-09-29-overlap-of-winning-arms.md)). The queue now
turns on three facts. **Central mode's gain is mostly UF–datatype equality
sharing.** A branch that changes only that sharing reproduces 48 of its 73
rescues. **The two positive R10 arms that matter are different effects, and
`--inst-defer` is close to independent of central mode.** And **the register's
positive results are spread over three crash-prone configurations**: `best`,
the R15 branch, and `dtElim-0929`. So the first new goal is a combination run,
the second is a crash, and the third is making crashes impossible to miss.

| # | short-term goal | blocked on | closed when |
| ---: | --- | --- | --- |
| ✅ S1, S2, S6, S7 | the bounded-eager line: read out the arms, take the module's counters, find what separates rescues from slowdowns, test the timeout boundary | — | **Closed 2026-09-16.** [`bounded-eager`](ledger/2026-09-16-bounded-eager-instantiation.md) and [`counters-and-timeout`](ledger/2026-09-16-eager-counters-and-timeout-sensitivity.md). Eager costs 19.46% PAR2 at a 0.77% match rate; 12 gap cases are reachable only through it; rescues and slowdowns separate on cumulative pairs processed |
| ✅ S11 | Record *why* a run failed, without changing the result token | — | **Closed 2026-09-17**, and found incomplete on 2026-09-29: see S18 |
| ✅ S12 | Find how many benchmarks the segfault actually affects | — | **Closed 2026-09-17.** [`segfault-scope`](ledger/2026-09-17-segfault-scope-and-failure-logging.md): **2 crashes among the 5845 benchmarks that reach a terminal answer** at 300 s — the same two. A floor, not a total: 279 still time out |
| ✅ S15 | Intersect the gained and lost sets of R10's three positive arms, and of the R15 arms against central mode | — | **Closed 2026-09-29.** [`overlap`](ledger/2026-09-29-overlap-of-winning-arms.md): `--inst-defer` and `--inst-defer --dt-split-relevant` share 42 of 47 gains and 30 of 33 losses; `--jh-rlv-inst` is a different effect; `--ee-share-uf-dt` rescues 48 of central mode's 73; `--inst-defer` shares only 23 of its 47 rescues with central mode |
| **S16** | **Run the first combination with a measured reason to win.** `ai-instDefer` with `--inst-defer --ee-mode=central`, and `ai-jhRlvInst` with `--jh-rlv-inst --ee-mode=central`, each beside `--ee-mode=central` alone on the same binary as its control | nothing — both branches built and ran in wave 2; three runs, about 25 minutes | a ledger entry reads both. **Success criterion:** a combination beats its own central-only control by more than the noise band. The overlap reading predicts up to about 24 extra rescues for `--inst-defer`. Adding `--ieval=off` waits on S10's crash, since it is the `best` pairing |
| **S17** | **Find why `ai-heuresis-r15-claude` crashes.** It segfaults on 5 splinterdb `PagedBetreeRefinement` problems (10 benchmarks) and answers `unknown` on 13–15 that the reference proves | nothing — a debug build of `5a936dbf58` and a backtrace | the ledger has a backtrace, and says whether the unknowns and the crash have one cause. It is the register's second 🟢 and the cleanest handle on central mode's gain, so it is worth a fixed branch rather than a caveat |
| **S4** | Count the shared-equality propagations between UF and datatypes, and their callback time, in distributed mode, central mode and `--ee-share-uf-dt` | nothing; a counter patch | the counts are measured. **Sharpened 2026-09-29**: the overlap reading names UF–datatype sharing as the likely mechanism, so this counter now tests a specific hypothesis rather than looking for one |
| **S18** | Make every crash visible. `cvc5_solve.sh` prints `none` and logs nothing when cvc5's output is empty, so `dtElim-0929`'s 480 segfaults left the error log empty. Separately, the binaries saved under the results directory link to the shared build directory, so they stop reproducing their run as soon as it is rebuilt | nothing — the wrappers are this repository's | the wrapper logs the exit status for empty output, a test covers that path, and a saved binary still runs as measured after a rebuild, either by carrying its libraries or by a static build |
| S20 | Put the branch-sweep driver in this repository. Waves 2, 1b, 3, 1c, 4 and 4b each ran from a script kept only on the host. Each script checks out a sha, builds in the sweep directory, verifies `--show-config`, smoke-tests the arm's options, then runs the set. None of those launches is in `job_launcher/log.txt` | nothing — the host scripts are this repository's to own | a tracked driver, run through the launcher or logging like it, reproduces a wave from a list of `name, sha, options` rows. The gained/lost reading it feeds is already tracked as [`arms`](../reports/arms), added 2026-09-29 |
| **S10** | File the `best` segfault upstream | the maintainer checking whether the two benchmarks may be shared publicly | the report in [`upstream-questions.md`](upstream-questions.md) is filed, still unfiled on 2026-09-29. The two newer crash sources, the R15 branch and `dtElim-0929`, are in unmerged branches, so they are for the maintainer and not for upstream |
| S13 | Measure `--ee-mode=central` on a second corpus | nothing — the launcher is self-contained, and the host carries other benchmark sets | central mode's 10.3% PAR2 win is confirmed or refuted off this one set. It is still the stated blocker on an R15 default-change proposal, and more valuable now that its mechanism has a name |
| S19 | Decide how anchors are compared. The register now has four anchor runs at three revisions, all within ±5 of each other, and a cell is read against its own | the maintainer: a rule change | either anchors within the noise band are declared comparable, or the 92 rows at `d7d5b948c1` are re-run at one newer revision, about 12 hours |
| **S14** | Publish three branches written on 2026-09-23 that answer R-4 and the R-2 format gap: `cacheEntCheck2` (R3, `9fc61815c7`), `emFailMasks2` (R3, `56ad448402`, `--inst-track-fail-masks`), and a whitespace fix for `rareEncodeSubcall` (E7, `f5dc8c80e1`) | nothing — they exist locally and build; `regress0` passes for all three. **Still unpublished on 2026-09-29:** the first two are not on the fork | they are pushed, so the register can carry them as proposals. **`emFailMasks2` has had no performance evaluation** and on the one regression where anything moved it *increased* E-matching lemmas 1871 → 1943; do not record it as a win |
| S3 | Make the mainline new-versus-rediscovered instantiation count a registered statistic | nothing — [`ajreynol:qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) is published at `ea71e3e7` | `--stats` reports unique versus total instantiations. Still **the only path to R2** |
| S5 | Count persistent instance clauses and how often one is used in a conflict | nothing; a counter patch | both are measured on the gap set. Seven R9 arms are now flat, so this is what R9 needs before another design |
| S9 | Explain why the control answers `unknown` on 7 benchmarks that `--eager-inst` proves | nothing | it is known whether one incompleteness is responsible or several. These 7 have survived 30 s, 120 s and 300 s unchanged |
| S8 | Add a cumulative eager pair budget, after which the module stands down | nothing — a bounded patch to `eager_inst.cpp` | the option is run and beats `best` (35532.7 PAR2), not merely unbudgeted eager. **Demoted 2026-09-29:** R1 is now red on all 19 arms, including five of instance chaining, so another eager mode is the weakest bet in this table |

## AI-agent priorities

**Updated.** 2026-09-29, on 128 measured proposal rows
([`ai-heuresis-*`](ledger/2026-09-28-ai-heuresis-branch-sweep.md),
[R12](ledger/2026-09-29-lemma-inprocessing-options.md),
[`dtElim-0929`](ledger/2026-09-29-dt-elim-0929.md)) and the
[overlap reading](ledger/2026-09-29-overlap-of-winning-arms.md). The previous
rank was 2026-09-25, on 92.

**The new rows confirm the ranking's top and thin out its bottom.** The one new
🟢 is in R15, the direction already first, and the overlap reading ties it to
central mode's gain. Every other new branch is flat or red. That leaves R1,
R16, R17 and R28 with more measured failures and no new lead, and it lets R26
rise, because four of the five goals above are counters or attribution rather
than runs.

**The expensive combined design R1 + R2 + R9 stays out.** Its three parts now
have 33 arms between them, none netting above +6.

The table contains ten research directions in priority order. Normally a
direction has one row. Where genuinely independent starting choices are
useful, a continuation row leaves the first three columns blank.

Each direction comes from [`directions.md`](directions.md). After completing a
step, record the evidence in [`ledger/`](ledger), rerank the ten
directions, and replace or refine that direction's possible first steps.

| rank | research direction | effort | its rows in the register | next possible step |
| ---: | --- | --- | --- | --- |
| 1 | [R15 — Equality-engine architecture](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 🟥 High Risk / 🟩 High Gain | 6 arms; `--ee-mode=central` **+73/−19, net +54**; `ai-heuresis-r15-claude --ee-share-uf-dt --ieval=off` **+59/−32, net +27**, with 10 segfaults | **The lead now has a mechanism.** 48 of the branch's 53 rescues are central mode's, so the gain is most likely UF–datatype sharing. Fix the branch's crash (S17), count the sharing (S4), and test central mode off this set (S13). A narrow UF–datatype sharing patch is also easier to upstream than a mode switch. |
| 2 | [R10 — Instance-lemma decision order](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 🟨 Medium Risk / 🟩 High Gain | 6 arms; `--inst-defer` **+47/−33, net +14**; `--jh-rlv-inst` +27/−17; new round-robin arms −10 | **Combine it with R15 (S16).** `--inst-defer` rescues 24 benchmarks central mode does not, so it is the first addition with a measured reason to help. `--dt-split-relevant` adds nothing to it and can be dropped from further runs. |
| 3 | [R7 — Entailment filtering](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 🟩 Low Risk / 🟨 Medium Gain | 5 arms; `--ieval=off` **+20/−8, net +12** | Unchanged and still the cheapest real effect. It adds about 6 rescues on top of R15's branch. The evaluator counters remain the next step, but they wait behind S10: `--ieval=off` is half of the crashing `best` pairing. |
| 4 | [R26 — Attribution instrumentation](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 🟩 Low Risk / 🟩 High Gain | 3 rows, all *n/a* | **Rises from 7.** The three leads above now need counters more than runs: UF–datatype sharing (S4), evaluator refusals (R7), and the per-benchmark attribution table. S18's crash visibility belongs here too. |
| 5 | [R9 — Deleting instantiation lemmas](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 🟥 High Risk / 🟩 High Gain | 7 arms; best +3 to +7 gained; `--inst-local` **−606** | Falls from 4. Three new GC arms are flat against their control. The drowning S1 measured is still real, but seven designs have not touched it. Take S5's counters before an eighth. |
| 6 | [R2 — Incremental E-matching](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 🟥 High Risk / 🟩 High Gain | 7 arms; `--term-db-reuse-eqc` +7/−1 | Holds. The new arm is the cleanest in R2, gaining 7 and losing only 1, but it is inside noise. E-matching is still 27.8% of gap-set time, so the case for S3's counter is unchanged. |
| 7 | [R6 — Conflict-based instantiation](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | 🟩 Low Risk / 🟨 Medium Gain | 9 arms; round budgets **+11 to +13 against their QCF control**, level with the reference | **Enters the ten.** Budgeting QCF rounds is the only new mechanism that measurably fixes what it targets: it removes QCF's whole cost. Whether QCF with a budget adds anything on top of R15 is a single run once S16's control exists. |
| 8 | [R16 — Datatypes](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 🟨 Medium Risk / 🟨 Medium Gain | 12 arms; `dtLazyInst3` +27/−75; two `--dt-elim` implementations **−945** and **−2090** | Holds. Split-order arms are flat and wholesale elimination is dead twice over. What is left is `dtLazyInst3`'s 27 rescues, a gating question. R15's UF–datatype finding may also belong partly here. |
| 9 | [R1 — Eager instantiation](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 🟥 High Risk / 🟩 High Gain | **19 arms, all red** | Falls from 6. Instance chaining is red on all five arms and worse with depth. It keeps a place only because its default arm still rescues 38, like every earlier eager mode. S9 is the only step worth taking. |
| 10 | [R28 — Eager conflict-based instantiation](directions.md#r28--eager-conflict-based-instantiation-find-a-useful-instance-before-full-effort) | 🟥 High Risk / 🟩 High Gain | 9 arms, all inside noise | Falls from 9. The literal-driven arms are flat against their own fallback control. Nothing further until R6's budgeted QCF shows whether conflict instances pay at all. |

**Out of the ten:** R17, whose integer-repair arm is flat (+8/−3); R11, whose
relevance filter is red on both arms; and R12, both of whose options are now
measured flat.


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
