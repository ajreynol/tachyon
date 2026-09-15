# Research directions: what would make cvc5 catch up to z3 on Verus-style quantified benchmarks

**Twenty-seven directions, R1 to R27, each with an argued risk/gain estimate
and the same four inventories: the cvc5 flags that test it today,
what has been tried, what z3 and others do, and the papers.** Written
2026-09-15 from the performance notes
summarised in [`../notes.md`](../notes.md) (the `h-N` rows referenced below),
from cvc5 `main` at
[`f294265`](https://github.com/cvc5/cvc5/commit/f294265c2b939a8e6cee8551f5a08afe5fb01efa)
and z3 `master` at
[`2d2fb04`](https://github.com/Z3Prover/z3/commit/2d2fb04fe3f1ab2111b550645f7c49198a3165f6)
read on that day,
from the 847 remote branch refs of the `ajreynol/cvc5` fork (excluding its
symbolic remote `HEAD`) as fetched on 2026-08-26,
and from the literature. Directions are not mutually exclusive; several
are the same mechanism seen from different sides, and the grouping says
which.

*What this document is not.* It is not an attribution of the remaining gap.
The project baseline ([ledger,
2026-09-14](../ledger/2026-09-14-baseline.md)) measures a PAR2 ratio of 4.34,
a gap set of 1049 of 6124, and 545 cvc5 timeouts on benchmarks z3 solves. It
also measures `--no-cbqi --user-pat=strict` only as a bundle: relative to
cvc5's default, cvc5 PAR2 improves from 53390 to 43942, but the two flags'
individual shares are unknown. Separately, the notes inherit one measured
direction, lazy large-`distinct` handling (R20), at 1.75× average speedup on
the Verus+Sundance set with a 60-second timeout. Everything else remains a
hypothesis or an unmeasured branch. The inventories say what *could* be
tested and how; goal 2 of the charter decides what *is*. Where a claim about
z3 or cvc5 rests on code read today it says `(code)`; where on a paper, it
cites; where on the notes, it names the `h-` row; where on reasoning alone,
it says so.

**Conventions.** A cvc5 flag is given as `--name` with its default in
brackets; `none` means the feature does not exist in cvc5. Fork branches are
displayed as `ajreynol:NAME` and linked to that branch in `ajreynol/cvc5`; a
parenthesized "commits" count means
`git rev-list --count origin/master..origin/NAME` at that fetched snapshot.
It is an archaeology aid, not an estimate of patch size: long-lived branches
can contain merge and update commits. A feature marked *merged* means its
intended behavior or option was found in the pinned cvc5 source; it does not
mean the fork commit is an ancestor of `main`, because upstream often
squash-merges. "Open" and "unmerged" are statuses as checked on 2026-09-15.
"Best known" means the configuration under study,
`--no-cbqi --user-pat=strict`.

**Effort levels.** Each direction is classified on two color-coded axes:
*Risk* runs 🟢 Low → 🟡 Medium → 🔴 High and combines implementation size,
architectural reach, correctness exposure, and the chance of regressions;
*Gain* runs 🔴 Low → 🟡 Medium → 🟢 High and estimates project value if the
hypothesis is right, either in performance gap closed or important uncertainty
removed. The argument after each classification matters more than the badge.
These are priors, not measured claims; attribution should change them.

## The map

| group | directions | what they have in common |
| --- | --- | --- |
| A — when and how much to instantiate | R1–R8 | the instantiation policy: z3 instantiates *during* search and cheaply; cvc5 instantiates at full effort and completely |
| B — what happens to lemmas afterwards | R9–R13 | the lemma lifecycle and the SAT search around it: deletion, ordering, relevance, the SAT core |
| C — the ground engine | R14–R19 | theory combination, congruence closure, datatypes, arithmetic, bit-vectors |
| D — before the search | R20–R23 | preprocessing and what the search is made to look at |
| E — cross-cutting | R24–R27 | configuration, low-level engineering, instrumentation, and input parsing |

The baseline says half the gap set is timeouts and half is solved-but-slow.
The reading in `notes.md` (*A reading of the register*) predicts that groups A
and B carry most of it. That is a prediction, and goal 2 exists to test it.

## Fork archaeology: the highest-signal branches

The fork is a design notebook, not a benchmark result. The table below records
what is actually present at the fetched tips and the next discriminating step.
"Ahead" uses the convention above; the source delta is the three-dot diff from
the merge base to the branch over `src/` and the regression CMake list. Neither
number proves that a branch is good, current, or reviewable as one patch.

| direction | branch evidence at the fetched tip | concrete mechanism | next branch step |
| --- | --- | --- | --- |
| R1 | [`ajreynol:eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi): 204 ahead, 2024-10-09; 62 files, +5285/−235 | evaluator-backed eager term database with conflict/propagation modes and instantiation levels | Rebase only after a small run separates evaluator cost from the benefit of earlier instances. |
| R1/R2 | [`ajreynol:eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3): 179 ahead, 2026-04-16; 39 files, +3780/−37; 1713-line `eager_inst.cpp` | persistent ground trie fed by equality-engine notifications; verified ancestry `macrosEagerInst` → `macroEagerInstMt` → `eagerInst3` | Run its shipped Verus cases, then a fixed 50-case gap slice with instance, round, and memory counters. |
| R1/R4 | [`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst): 5 ahead, 2026-06-12; 14 files, +1464/−8, excluding two large SMT2 inputs | smaller notification-driven matcher with generation, pair, and per-round budgets | Sweep the three limits on the same slice before comparing it with the two older eager designs. |
| R2/R7 | [`ajreynol:ai-emFilter`](https://github.com/ajreynol/cvc5/tree/ai-emFilter): 11 ahead, 2026-04-27; 20 files, +758/−15 | `--filter-e-matching` and supporting equality/entailment filters | Count candidate matches rejected, time spent filtering, and net instances saved. |
| R3 | [`ajreynol:ai-prepared13`](https://github.com/ajreynol/cvc5/tree/ai-prepared13): 11 ahead, 2026-06-10; 4 files, +291/−6 | prepared-term indexing work concentrated in four source files | Profile lookup time and index size before treating the small file count as low risk. |
| R9/R10 | [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer): 2 ahead, 2026-06-15; 11 files, +116/−32; [`ajreynol:ai-jhRlvInst`](https://github.com/ajreynol/cvc5/tree/ai-jhRlvInst): 3 ahead, 2026-06-18; 10 files, +327/−18 | global duplicate recording with local-style justification, and quantifier-relevance activation in the justification heuristic | Compare each alone with `--inst-local`; neither branch implements SAT clause deletion. |
| R11/R22 | [`ajreynol:preregRlv`](https://github.com/ajreynol/cvc5/tree/preregRlv): 155 ahead, 2026-04-23; 10 files, +836/−13 | relevance-aware preregistration; related upstream [PR #9503](https://github.com/cvc5/cvc5/pull/9503) remains open | First compare `--preregister-mode=lazy`; build the branch only if the cheap flag moves the target counters. |
| R14 | [`ajreynol:mbtc25`](https://github.com/ajreynol/cvc5/tree/mbtc25): 29 ahead, 2026-01-13; 16 files, +371/−84 | model-based theory combination; related upstream [PR #12095](https://github.com/cvc5/cvc5/pull/12095) remains open | Add an explicit care-pair/split counter, then compare against care-graph combination. |
| R15 | [`ajreynol:dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3): 31 ahead, 2026-05-22; 13 files, +405/−73; verified ancestry `dtMergeNotify` → `v2` → `v3` | datatype merge-notification experiments, distinct from upstream context-notification PR #9724 | Isolate notification count and callback time before attributing a solver-level win. |
| R16 | [`ajreynol:dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant): 2 ahead, 2026-06-10; 3 files, +62/−8 | `--dt-split-relevant`, a small relevance gate around datatype splitting | Measure eligible versus suppressed splits and check that incompleteness is not introduced. |
| R17 | [`ajreynol:ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc): 3 ahead, 2026-06-16; 6 files, +95/−2; [`ajreynol:deferBlock`](https://github.com/ajreynol/cvc5/tree/deferBlock): 19 ahead, 2025-08-26; 15 files, +330/−21 | last-call Diophantine timing and deferred arithmetic blocking | Restrict to NIA/LIA cases and record branch lemmas, full/last-call checks, and conflicts. |
| R19 | [`ajreynol:bitblastLc`](https://github.com/ajreynol/cvc5/tree/bitblastLc): 1 ahead, 2025-06-12; 2 files, +28/−1 | last-call bit-blasting | Run only the bit-vector slice and inspect unknown/completeness behavior as well as time. |
| R24 | [`ajreynol:verusDev`](https://github.com/ajreynol/cvc5/tree/verusDev): 23 ahead, 2026-02-04; 10 files, +141/−33 | a mixed Verus-oriented line: relevance delay, recheck, function assignment, datatype splitting | Decompose it into the corresponding main flags/features; do not benchmark the aggregate as attribution. |
| R25 | [`ajreynol:lowLevelOptMore`](https://github.com/ajreynol/cvc5/tree/lowLevelOptMore): 11 ahead, 2019-12-16; 3 files, +105/−33 | old, compact constant-factor work | Treat it as profiling history; reproduce the hotspot on current main before porting code. |
| R26 | [`ajreynol:qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats): 29 ahead, 2026-01-29; 19 files, +532/−15 | E-matching debug statistics plus an `AnalyzeEE` module | Inventory which counters remain absent on main and port only those required by the attribution table. |
| R27 | [`ajreynol:ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt): 2 ahead, 2026-03-12; 7 files, +228/−144 | stack reservation, `from_chars`, static `string_view` token tables, and less argument-vector movement | Measure parse-only wall time, allocations, and bytes/s before and after on large generated inputs. |

---

# Group A — when and how much to instantiate

The structural difference the notes name first (`h-16`, `h-18`), and the one
the z3 code confirms most sharply `(code)`: z3 can turn an E-matching match
into a clause *during propagation* when its cost is below
`smt.qi.eager_threshold`, E-matches only terms that relevancy has marked,
finds new matches incrementally from a candidate queue fed by merges, and
deletes the instance clauses again on backtracking. cvc5 does not combine
these four mechanisms: it instantiates only at `EFFORT_FULL`/`LAST_CALL` (and
skips one round in three by default, `--inst-when-phase=2`), rebuilds every
trigger index from scratch each round, enumerates every match a trigger has
with no budget, and by default keeps every instance for the current user
context (group B).
R1–R4 are the four halves of that difference; R5–R8 are the policies around
it.

## R1 — Eager instantiation: instantiate during search, not only at full effort

**Effort.** 🔴 High Risk / 🟢 High Gain — this changes when quantifiers run and
touches SAT propagation, pacing, and backtracking; z3's eager chain is the
largest structural difference identified for this workload.

*Rows `h-16`. Coupled to R2 (incrementality), R4 (budget), R9 (deletion).*

**The hypothesis.** A Verus proof obligation can contain a chain of
trigger-driven instantiations, each of which creates the ground terms that
fire the next. z3 can walk such a chain inside propagation without requiring
a SAT decision between every link; cvc5 first lets the SAT solver reach a
full-effort theory check, runs an E-matching round, and returns to the SAT
solver. In the worst case, a chain of depth *d* therefore requires *d* full
checks against a growing clause set. The notes call this the lack of eager
instantiation and record three attempts.

**In cvc5 today `(code)`.**
- `--inst-when` [`full-last-call`]: modes `full`, `full-delay`,
  `full-last-call`, `full-delay-last-call`, `last-call`. Nothing runs at
  `EFFORT_STANDARD`; the quantifiers engine is not called there at all.
- `--inst-when-phase` [`2`]: the divisor is `1 + max(1, N)` = 3, so at full
  effort instantiation is skipped one round in three to let theory
  combination run first ("allow theory combination to go first").
- `--inst-max-rounds` [`-1`], `--inst-max-level` [`-1`] (setting the latter
  disables cegqi).
- Within a round, `InstantiationEngine::doInstantiationRound` walks internal
  efforts 0..2 (0..10 at last call) and stops at the first level that queues
  a lemma; `QuantifiersEngine::checkInternal` breaks out of the module loop
  as soon as any lemma is sent.
- `none` for eager instantiation itself: no option instantiates below full
  effort.

**Tried.** Three design lines in the fork, none on `main`; the labels below
do not imply ancestry. Line A,
[`ajreynol:eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi)
(2024-10, 204 commits): an "eager term database"
built on the instantiation evaluator that adds only conflicting,
unit-propagating or non-entailed instances eagerly (`--eager-inst-when=eqc|
eqc-delay|asserted|std-check`, `--eager-inst-mode=conflict|prop|unit-prop|…`,
`--eager-inst-trigger=narrow|all`, `--track-inst-level`,
`--inst-level-buffer=N`). Line B has verified ancestry
[`ajreynol:macrosEagerInst`](https://github.com/ajreynol/cvc5/tree/macrosEagerInst) →
[`ajreynol:macroEagerInstMt`](https://github.com/ajreynol/cvc5/tree/macroEagerInstMt) → [`ajreynol:eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) (2024-09 to 2026-04, 1713 lines of
`eager_inst.cpp`): E-matching over a ground trie fed by master-engine
notifications, with `--eager-inst-term=eqc|eqc-merge|assert`,
`--eager-inst-quant=preregister|assert`, `--eager-inst-watch`,
`--eager-inst-simple` ("do not search modulo equality to match operators"),
`--eager-inst-macro-only`, `--eager-inst-gcong`, and `--defer-block`; it
ships `verus-16s.smt2` and `verus-mim-40s.smt2` as regressions;
[`ajreynol:ai-extEagerInst3-1`](https://github.com/ajreynol/cvc5/tree/ai-extEagerInst3-1) adds auto-triggers on top. Line C, started
in 2026-04: [`ajreynol:ai-eagerInst1`](https://github.com/ajreynol/cvc5/tree/ai-eagerInst1) (a skeleton), [`ajreynol:ai-eagerInst2`](https://github.com/ajreynol/cvc5/tree/ai-eagerInst2) ("a small
incremental term database that is populated only from notification events
… a lightweight eager matcher for user-provided patterns"), and
[`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) (2026-06, 939 lines): per-operator context-dependent term
lists with a cursor per trigger, merge-driven re-matching through a parent
index, and — alone among the three generations — pacing:
`--eager-inst-limit=N` (instances per round), `--eager-inst-gen-limit=N`
("do not eagerly match terms whose generation … is N or more", default 1),
`--eager-inst-pair-limit=N` ("this paces eager instantiation so that the
SAT solver makes progress between rounds", default 2000), and
`--eager-inst-rlv` ("defer eager matching of terms in singleton equivalence
classes until they participate in a merge; this approximates relevancy").
Also [`ajreynol:eagerQM`](https://github.com/ajreynol/cvc5/tree/eagerQM) (2025, a preprocessing-time matching pass) and
[`ajreynol:instFullPreempt`](https://github.com/ajreynol/cvc5/tree/instFullPreempt) (2024, `--inst-when=full-preempt`). The notes' verdict on
the three problems of the hand-written line — no deletion, infinite branch
and bound, matching loops — is R9, R17 and R4 respectively. None was run
against the set.

**Elsewhere `(code)`.** z3: `mam::on_match` → `context::add_instance` →
`qi_queue::insert`; `qi_queue::instantiate()` runs from
`context::propagate`, and an entry is asserted immediately iff its cost
(`smt.qi.cost` = `(+ weight generation)`) is at most
`smt.qi.eager_threshold` [10.0; Verus sets 100], or if `qi.promote_unsat`
finds it already falsified. Everything else waits in `m_delayed_entries` for
`final_check_eh`, where entries with cost at most `smt.qi.lazy_threshold`
[20.0] are asserted, lowest cost first. Under Verus's settings the eager
threshold exceeds the lazy one, so an instance with generation above 100 is
never made: a depth cap on matching chains, not a delay. The instance body is
first evaluated by `smt_checker` against the current assignment and
discarded if already true. Simplify did the same eagerly, with its own
mod-time machinery (R2). SMTInterpol integrates E-matching as a theory that
finds conflict and unit instances incrementally (Hoenicke and Schindler
2021).

**Papers.** de Moura and Bjørner, [*Efficient E-Matching for SMT Solvers*](https://leodemoura.github.io/files/ematching.pdf),
CADE 2007 — the eager/lazy split, the promotion of useful quantifiers to eager
instantiation, and "Deleting clauses". Detlefs, Nelson and Saxe, [*Simplify: a
theorem prover for program checking*](https://doi.org/10.1145/1066100.1066102),
J. ACM 52(3), 2005. Hoenicke and Schindler, [*Incremental Search for Conflict
and Unit Instances of Quantified Formulas with
E-Matching*](https://doi.org/10.1007/978-3-030-67067-2_24), VMCAI 2021. Ge,
Barrett and Tinelli, [*Solving Quantified Verification Conditions Using
Satisfiability Modulo
Theories*](https://theory.stanford.edu/~barrett/pubs/GBT09-abstract.html), CADE
2007. Bjørner et al., [*Z3
Internals*](https://z3prover.github.io/papers/z3internals.html), §7.1.5–7.1.6.

**What would settle it.** The attribution first: on the gap set, the number of
full-effort rounds per benchmark (`QuantifiersEngine::Rounds_Instantiation_Full`)
against z3's instance generation depth; if cvc5's rounds track z3's depth,
the cost is rounds, and R1 is the direction. Then the cheapest existing
branch against the set with clause-lifetime and memory counters. The notes
report that eager attempts drowned without deletion, but `--inst-local` is
not deletion (R9); a genuine lifetime experiment must follow if the eager
signal is positive.

## R2 — Incremental E-matching: match what changed, not everything

**Effort.** 🔴 High Risk / 🟢 High Gain — persistent indices and merge notifications
cut across the term database and equality engine, but eliminating full rescans
could remove a multiplicative cost from every instantiation round.

*Rows `h-18`. Coupled to R1; independent of it in the notes' judgement ("does
not fit our setting well by itself").*

**The hypothesis.** cvc5 spends E-matching time re-deriving matches it found
last round. Simplify's mod-time optimisation and z3's candidate queue both
restrict matching to terms and classes that changed since the last pass; with
thousands of instantiation rounds on a large E-graph, the rebuilt-from-scratch
cost is a multiplicative factor on everything in group A.

**In cvc5 today `(code)`.** No incremental mechanism. `TermDb::reset` clears
`d_func_map_trie`, `d_func_map_eqc_trie`, `d_arg_reps` and the relevance map
every round, and `InstStrategyAutoGenTriggers::processResetInstantiationRound`
resets every trigger; candidate generators are re-`reset(eqc)` on each use.
`--term-db-mode` [`relevant-all-delay`] (`all` / `relevant` /
`relevant-all-delay`) limits which ground terms are indexed at all: relevance
is a monotone over-approximation marked on merge (`TermDb::eqNotifyMerge`)
and widened to everything as a last resort before answering unknown
(`QuantifiersEngine::shouldRecheck`). `--increment-triggers` [`true`]
regenerates trigger sets every third pass. `--register-quant-body-terms`
[`false`].

**Tried.** [`ajreynol:ai-emFilter`](https://github.com/ajreynol/cvc5/tree/ai-emFilter) (2026-04, `--filter-e-matching` "conservatively
filter quantified formulas from E-matching": an `EMatchingFilter` that
snapshots master-engine events and marks triggers dirty by match operator,
with a last-call backstop; the author's note reads "Probably too
aggressive"); [`ajreynol:imTrivial`](https://github.com/ajreynol/cvc5/tree/imTrivial) (2025-10, `InstMatchGeneratorTrivial` for
triggers `f(x1..xn)` with distinct variables that "only subsequently
considers terms that have not yet been considered … avoids repeated calls to
matching, and in particular entailment checking"); [`ajreynol:imSimpleInc`](https://github.com/ajreynol/cvc5/tree/imSimpleInc),
[`ajreynol:imSimpleInc2`](https://github.com/ajreynol/cvc5/tree/imSimpleInc2) (the same for `InstMatchGeneratorSimple`); [`ajreynol:quantCgInc`](https://github.com/ajreynol/cvc5/tree/quantCgInc) (an
incremental candidate generator, last commit "Try, broken"); [`ajreynol:ai-imgDirect`](https://github.com/ajreynol/cvc5/tree/ai-imgDirect)
(2026-03, a direct matcher for nested single triggers such as `f(g(x))`
that can exclude failed root candidates for the round); [`ajreynol:ai-quantOpt-1`](https://github.com/ajreynol/cvc5/tree/ai-quantOpt-1)
(candidate caching per pattern arity); [`ajreynol:emExp`](https://github.com/ajreynol/cvc5/tree/emExp) (2025, records the context
level at which each term entered the database); [`ajreynol:emStratify`](https://github.com/ajreynol/cvc5/tree/emStratify) (2023,
`--e-matching-stratify-ieval`); [`ajreynol:emFailMasks`](https://github.com/ajreynol/cvc5/tree/emFailMasks) (2022,
`--inst-track-fail-masks`); [`ajreynol:fixEm`](https://github.com/ajreynol/cvc5/tree/fixEm) (merged). None of the branch-only incremental
matchers above was found on pinned `main`; the `fixEm` repair was.

**Elsewhere `(code)`.** z3 `smt/mam.cpp`: triggers compile into code trees
shared per top symbol; each enode root carries two 64-bit approximate label
sets (`get_lbls`, `get_plbls`) used as Bloom filters; `relevant_eh` pushes a
newly relevant term as a candidate of its symbol's tree; `add_eq_eh` walks
an *inverted path index* (`m_pc`, `m_pp` path trees) from the merged roots to
find only the parents that could newly match; `match()` runs the trees over
the candidate lists and clears them. `rematch()` (the full re-scan) is used
only by the lazy multi-pattern matcher at final check. There is no mod-time
field in current z3; the incrementality is candidates plus path trees.
Simplify's mod-time and pattern-element optimisations are the ancestors.
veriT's CCFV is the other family (Barbosa's thesis).

**Papers.** [de Moura and Bjørner CADE
2007](https://leodemoura.github.io/files/ematching.pdf) (code trees, inverted path index,
"the practical overhead ... is searching and maintaining sets of patterns
that can efficiently retrieve new matches as soon as E-graph operations
introduce them"). [*Simplify* J. ACM
2005](https://doi.org/10.1145/1066100.1066102), §5 (mod-time,
pattern-element). Moskal, Łopuszański and Kiniry, [*E-matching for Fun and
Profit*](https://doi.org/10.1016/j.entcs.2008.04.078), SMT 2007 / ENTCS 198(2),
2008. Barbosa, [*New techniques for instantiation and proof production in SMT
solving*](https://hanielbarbosa.com/papers/phd-official.pdf), PhD thesis 2017.
Bjørner et al., [*Z3
Internals*](https://z3prover.github.io/papers/z3internals.html), §7.1.2–7.1.3.

**What would settle it.** `theory::QuantifiersEngine::time_ematching` as a
fraction of solve time on the gap set, and the ratio of matches found to
matches re-found (a counter to add). If E-matching time is small, R2 is not
where the gap is, whatever z3 does.

## R3 — Worst-case E-matching: failure caching and early pruning

**Effort.** 🟡 Medium Risk / 🟡 Medium Gain — the change is localized to matcher
state but cache validity is subtle; it targets a severe tail on a small,
not-yet-measured subset rather than the whole gap.

*Rows `h-17`. The exponential tail of R2.*

**The hypothesis.** A few benchmarks (`prepared_13.smt2` in the notes) make
cvc5's matcher enumerate an exponential number of partial matches that all
fail. Caching the failed state, or checking entailment of a partial match
before extending it, bounds the worst case.

**In cvc5 today `(code)`.** `--ieval` [`use`] (`off` / `use` / `use-learn`):
the instantiation evaluator (`theory/quantifiers/ieval/`, PR #9092, 2022)
pushes one variable at a time and tests `isFeasible()` — "infeasible if all
extensions of the current variable assignment lead to instantiations that are
entailed by the ground context"; `use-learn` generalises a failed substitution
and caches it. `--inst-no-entail` [`true`] rejects a completed instance that
is already entailed (counter `Instantiate::Duplicate_Inst_Entailed`). The
evaluator is reset each round (`resetAll`). `--multi-trigger-linear` [`true`]
bounds multi-trigger instances linearly in the number of ground terms.

**Tried.** [`ajreynol:ai-prepared13`](https://github.com/ajreynol/cvc5/tree/ai-prepared13) (2026-06, unmerged): `getNextMatch` returns a
distinguished failure "for reasons that are invariant modulo the current
equality engine", keyed by the representative being matched, the
representatives of the continuation generators and the partial match, and
caches it for the round; its regressions are Verus worst cases
(`prepared_13`, `ironkv … delegation_map`, `verismo … range_set`).
[`ajreynol:instEval`](https://github.com/ajreynol/cvc5/tree/instEval) (2022, merged as `--ieval`); [`ajreynol:cacheEntCheck`](https://github.com/ajreynol/cvc5/tree/cacheEntCheck) (2021);
[`ajreynol:ai-imgDirect`](https://github.com/ajreynol/cvc5/tree/ai-imgDirect) (R2).

**Elsewhere `(code)`.** z3 bounds the same problem differently: fingerprints
(`smt/fingerprints.h`) reject a (quantifier, root bindings) tuple already seen
in the current scope; `smt_checker::is_sat` discards an instance whose body
is already true before it becomes a clause; label filters reject most
candidates in constant time; and the eager/lazy cost split (R1) is itself the
budget. veriT's CCFV frames E-matching as E-ground (dis)unification with its
own pruning.

**Papers.** Barbosa, Fontaine and Reynolds, [*Congruence Closure with Free
Variables*](https://doi.org/10.1007/978-3-662-54580-5_13), TACAS 2017. Bansal,
Reynolds, King, Barrett and Wies, [*Deciding Local Theory Extensions via
E-matching*](https://theory.stanford.edu/~barrett/pubs/BRK%2B15-abstract.html),
CAV 2015. No paper on cvc5's instantiation evaluator exists; [PR
#9092](https://github.com/cvc5/cvc5/pull/9092) is the reference.

**What would settle it.** The distribution of E-matching time per round on the
gap set: a heavy tail on few benchmarks is R3, a uniform cost is R2.

## R4 — Instantiation budgeting: how many instances per round, and which

**Effort.** 🔴 High Risk / 🟢 High Gain — budgets create fairness and completeness
obligations and interact with R1 and R9, while a successful policy could stop
the instance and clause explosions predicted to dominate the gap.

*Rows `h-19`. z3's cost function is the mechanism; cvc5 has none.*

**The hypothesis.** cvc5 sends every match of every trigger every round. z3
sends the cheap ones now, the expensive ones at final check, and the very
expensive ones never. A budget — per round, per trigger, per ground term, or
by generation — would keep the clause set small (R9) and the SAT search short,
at the price of completeness this benchmark set may not need (its obligations
are unsat and its source encoding is designed around triggers).

**In cvc5 today `(code)`.** No per-round or per-trigger cap:
`InstMatchGenerator::addInstantiations` loops `while (getNextMatch(m) > 0)`
with conflict as the only early exit. What exists: `--inst-max-rounds`
[`-1`], `--inst-max-level` [`-1`] (max instantiation *level* of terms used —
the closest thing to z3's generation), `--multi-trigger-priority` [`false`]
(multi-triggers only when single ones yield nothing),
`--multi-trigger-when-single` [`false`], `--multi-trigger-cache` [`false`],
`--multi-trigger-linear` [`true`], `--trigger-sel` [`min`] (`min` / `max` /
`min-s-max` / `min-s-all` / `all`), `--trigger-active-sel` [`all`],
`--quant-rep-mode` [`first`], `--literal-matching` [`use`],
`--enum-inst-limit` (enumerative only).

**Tried.** [`ajreynol:termOrigin`](https://github.com/ajreynol/cvc5/tree/termOrigin) (2025-04, unmerged): `--inst-nested-max-level=N`
"maximum nested instantiation level of terms used to instantiate quantified
formulas" and `--track-term-origins`, a lemma-origin DAG over terms — the
closest cvc5 has come to z3's generation. [`ajreynol:eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi)'s
`--inst-level-buffer=N` ("maximum inst level of terms in proportion to the
number of full effort checks") and [`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst)'s three limits (R1)
are budgets inside eager instantiation. [`ajreynol:instLastCallDelay`](https://github.com/ajreynol/cvc5/tree/instLastCallDelay) (2026-03: skip
the last-call check while the valuation still needs one),
[`ajreynol:instFullPreempt`](https://github.com/ajreynol/cvc5/tree/instFullPreempt) (2024), [`ajreynol:dtInstMode`](https://github.com/ajreynol/cvc5/tree/dtInstMode) (2020), [`ajreynol:carryInst`](https://github.com/ajreynol/cvc5/tree/carryInst) (2021). Nothing
budgets a full-effort E-matching round on `main`.

**Elsewhere `(code)`.** z3 `smt.qi.cost` = `(+ weight generation)` over
fifteen variables (`weight`, `generation`, `instances`, `size`, `depth`,
`vars`, `pattern_width`, `total_instances`, `scope`, `nested_quantifiers`,
`cs_factor`, ...); `smt.qi.eager_threshold` [10; Verus 100],
`smt.qi.lazy_threshold` [20], `smt.qi.max_instances` [unbounded],
`smt.qi.max_multi_patterns` [0: one eager multi-pattern only when there is no
unary one, the rest lazy], `smt.qi.quick_checker` [0]. The
`params/qi_params.h` comment records the "weight 0" pitfall kept "because
this feature was requested by the Boogie team ... their patterns are
carefully constructed, and there are no matching loops". The `:weight`
annotation and generation stamping are the user-facing half.

**Papers.** [de Moura and Bjørner, CADE
2007](https://leodemoura.github.io/files/ematching.pdf) (priority queues,
promotion/demotion). Bjørner et al., [*Z3
Internals*](https://z3prover.github.io/papers/z3internals.html), §7.1.6.
Jakubův, Janota, Piepenbrock and Urban, [*Machine Learning for Quantifier
Selection in cvc5*](https://arxiv.org/abs/2408.14338), ECAI 2024 (learned
selection, a budget of a different kind).

**What would settle it.** Instances per round and total instances on the gap
set versus z3's `smt.qi.profile` counts on the same benchmarks. If cvc5 makes
an order of magnitude more instances to reach the same refutation, R4 (with
R9) is the direction; if the counts are similar, the cost is elsewhere.

## R5 — Trigger selection: strict user patterns, multi-triggers, and what strictness disables

**Effort.** 🟡 Medium Risk / 🟡 Medium Gain — trigger changes are contained but can
silently alter completeness and matching loops; strict patterns already help
in a bundle, though their isolated share is unknown.

*Rows in the notes: `--user-pat=strict` under "things that helped".*

**The hypothesis.** Verus's VIR-to-AIR lowering requires at least one manual
or automatically selected trigger for the ordinary quantifiers it lowers
(`build_triggers(..., allow_empty=false)`) and designs them for z3's
semantics: user patterns only, no solver-inferred ones, with loop avoidance as
an encoding goal. Generated SMT should still be measured rather than assuming
that every quantifier from every encoding path is patterned. cvc5's default
`trust` already uses only user
patterns when present, but leaves the quantifier open to the other modules;
`strict` closes it, and is in the best-known configuration. What else
`strict` changes, and whether the multi-trigger and selection policies are
tuned for this workload, is untested.

**In cvc5 today `(code)`.** `--user-pat` [`trust`] (`use` / `trust` /
`strict` / `resort` / `ignore` / `interleave`). Under `strict`: (1) the
instantiation engine takes *exclusive ownership* of every patterned
quantifier, so cbqi, cegqi, enum-inst, pool-inst and MBQI never touch it;
(2) the rewriter classifies it as non-standard, skipping miniscoping, variable
elimination, ITE lifting and conditional splitting for it (R21); (3)
auto-generated triggers are skipped (also true under `trust`). Also
`--relevant-triggers` [`false`] (SInE-style), `--relational-triggers`
[`false`], `--purify-triggers` [`false`], `--partial-triggers` [`false`],
`--cons-exp-triggers` [`false`], `--pre-skolem-quant` [`off`],
`--miniscope-quant-user` [`false`], `--prenex-quant-user` [`false`]. Trigger
ground subterms not in the equality engine get `QUANTIFIERS_GT_PURIFY`
lemmas.

**Tried.** [`ajreynol:multiTriggerSingleBase`](https://github.com/ajreynol/cvc5/tree/multiTriggerSingleBase) (2024, "using single trigger as a base
for multi triggers"); [`ajreynol:nestedTriggers2`](https://github.com/ajreynol/cvc5/tree/nestedTriggers2) (2022, `--nested-triggers` "generate
triggers based on terms in nested quantifiers"), [`ajreynol:nestedTriggers`](https://github.com/ajreynol/cvc5/tree/nestedTriggers) (2023,
"another attempt"); [`ajreynol:simpleTriggerMore`](https://github.com/ajreynol/cvc5/tree/simpleTriggerMore) (2023); [`ajreynol:gttOpt`](https://github.com/ajreynol/cvc5/tree/gttOpt) (2021,
`--gt-trigger-reg` register ground subterms of triggers); [`ajreynol:userTriggerOut2`](https://github.com/ajreynol/cvc5/tree/userTriggerOut2)
(merged: user triggers distinguished in `-o trigger`); [`ajreynol:eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi)'s
`--eager-inst-trigger=narrow` ("use the most constrained trigger") and
`--eager-inst-merge-triggers` ("combine triggers that are equivalent modulo
ground subterms"). None was measured on the set; only the `userTriggerOut2`
output distinction was found on pinned `main`.

**Elsewhere `(code)`.** z3 `pattern_inference_cfg::reduce_quantifier` returns
immediately when a quantifier has any pattern: nothing is added, the weight is
untouched. Verus additionally sets `pi.enabled=false`. Ground subterms of
triggers are registered as *shared terms* for theory combination
(`mam_impl::m_shared_enodes`). Multi-patterns are inserted once per component
as entry point; with `smt.qi.max_multi_patterns=0` only one multi-pattern is
eager when no unary pattern exists, the rest are matched lazily at most twice
per branch. z3's `setup_AUFLIA` comment on why macro-finder stays off:
"MACRO_FINDER is a horrible for AUFLIA and UFNIA benchmarks (boogie
benchmarks in general). It destroys the existing patterns."

**Papers.** Leino and Pit-Claudel, [*Trigger Selection Strategies to Stabilize
Program
Verifiers*](https://www.microsoft.com/en-us/research/publication/trigger-selection-strategies-stabilize-program-verifiers/),
CAV 2016. Moskal, [*Programming with
Triggers*](https://doi.org/10.1145/1670412.1670416), SMT 2009. Dross, Conchon,
Kanig and Paskevich, [*Adding Decision Procedures to SMT Solvers Using Axioms
with Triggers*](https://doi.org/10.1007/s10817-015-9352-2), JAR 56(4), 2016.
Bugariu, Ter-Gabrielyan and Müller, [*Identifying Overly Restrictive Matching
Patterns in SMT-based Program
Verifiers*](https://doi.org/10.1007/978-3-030-90870-6_15), FM 2021. Ge, Garcia
and Summers, [*A Formal Model to Prove Instantiation Termination for
E-matching-Based
Axiomatisations*](https://doi.org/10.1007/978-3-031-63498-7_25), CAV 2024.

**What would settle it.** `-o trigger` on the gap set: how many quantifiers
have no user pattern (and so get auto-triggers), how many multi-triggers
there are, and an A/B of `trust` vs `strict` alone (the baseline measured
`strict` and `--no-cbqi` together).

## R6 — Conflict-based instantiation: off for this domain, and why that is right or wrong

**Effort.** 🟢 Low Risk / 🟡 Medium Gain — the engine and off switch already exist,
so the first work is an isolated run; the current baseline suggests disabling
it helps, but that effect is still bundled with strict patterns.

*Rows `h-15`.*

**The hypothesis.** cbqi is an order-of-magnitude win on sledgehammer
problems and a loss here (the notes), with rare exponential behaviour. The
best-known configuration turns it off. The question left is whether its
*cost* on this set is the conflict search itself or the round it consumes
before E-matching runs, and whether a cheap conflict check in the style of
z3's `qi.promote_unsat` would be a win.

**In cvc5 today `(code)`.** `--cbqi` [`true`], `--cbqi-mode` [`prop-eq`]
(`conflict` / `prop-eq`), `--cbqi-all-conflict` [`false`],
`--cbqi-tconstraint` [`false`], `--cbqi-vo-exp`, `--cbqi-skip-rd`,
`--sub-cbqi` [`false`] (a subsolver strategy). With `--no-cbqi` the module is
not constructed; nothing runs at `QEFFORT_CONFLICT`. Passing `--cbqi-mode`
re-enables `--cbqi` unconditionally.

**Tried.** [`ajreynol:ai-cbqi-0423`](https://github.com/ajreynol/cvc5/tree/ai-cbqi-0423) (2026-04, unmerged): a rework of
`quant_conflict_find.cpp` for the case where "large flattened UF encodings,
e.g. graph-preservation constraints, tend to force QCF into an exhaustive
search over auxiliary function applications while other quantifier modules
return quickly" — the `mu_test.smt2` case of the notes. [`ajreynol:safeOpts-0305`](https://github.com/ajreynol/cvc5/tree/safeOpts-0305)
(merged: `--cbqi` promoted to a common option); [`ajreynol:refactorQcf`](https://github.com/ajreynol/cvc5/tree/refactorQcf) (2022),
[`ajreynol:qcfClean`](https://github.com/ajreynol/cvc5/tree/qcfClean) (2021); [`ajreynol:cbqiDev`](https://github.com/ajreynol/cvc5/tree/cbqiDev), [`ajreynol:cbqiImp-v2`](https://github.com/ajreynol/cvc5/tree/cbqiImp-v2) (2018, a different "cbqi":
counterexample-guided for bit-vectors).

**Elsewhere `(code)`.** z3 has no conflict-based instantiation module; its
analogues are `qi.promote_unsat` (an instance that `smt_checker::is_unsat`
shows falsified jumps the eager queue) and `smt.qi.quick_checker` (off by
default; mode 2 is warned against in code as "too expensive"). SMTInterpol's
E-matching theory finds conflict and unit instances directly.

**Papers.** Reynolds, Tinelli and de Moura, [*Finding Conflicting Instances of
Quantified Formulas in
SMT*](https://homepage.cs.uiowa.edu/~tinelli/papers/ReyTD-FMCAD-14.pdf), FMCAD
2014. [Hoenicke and Schindler VMCAI
2021](https://doi.org/10.1007/978-3-030-67067-2_24).

**What would settle it.** The baseline already has `--no-cbqi` bundled with
`--user-pat=strict`; an A/B of each alone says what cbqi costs here.

## R7 — Entailment filtering of instances: what ieval buys and costs

**Effort.** 🟢 Low Risk / 🟡 Medium Gain — existing modes bracket the experiment and
the evaluator is localized; avoiding expensive or duplicate instances could
matter broadly if its current checks dominate matching time.

*The "helps elsewhere" rows of the notes, measured here.*

**The hypothesis.** Entailment filtering (`--inst-no-entail`, `--ieval`) is on
by default and the notes list it among things that help elsewhere. On a
workload that is all unsat and trigger-driven, entailed instances may be
rare, and the evaluator's per-round reset may cost more than it saves — or it
may be the only thing standing between cvc5 and an instance explosion. Nobody
has measured it on this set.

**In cvc5 today `(code)`.** `--ieval` [`use`], `--inst-no-entail` [`true`];
trigger matching runs the evaluator in `NO_ENTAIL` mode; QCF in
`CONFLICT`/`PROP` mode. Counters `Instantiate::Duplicate_Inst`,
`Duplicate_Inst_Eq`, `Duplicate_Inst_Entailed`.

**Tried.** [`ajreynol:instEval`](https://github.com/ajreynol/cvc5/tree/instEval) (2022, merged as `--ieval`); [`ajreynol:eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi) extends the
evaluator for eager use (R1); [`ajreynol:fmfIeval`](https://github.com/ajreynol/cvc5/tree/fmfIeval) (2022), [`ajreynol:ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) (2023),
[`ajreynol:emStratify`](https://github.com/ajreynol/cvc5/tree/emStratify) (2023), [`ajreynol:cacheEntCheck`](https://github.com/ajreynol/cvc5/tree/cacheEntCheck) (2021). Apart from merged `instEval`, these tips date
from 2021–23; none was measured on the set.

**Elsewhere `(code)`.** z3's `smt_checker::is_sat` before internalising an
instance is the same test at the same point; fingerprints are the duplicate
filter.

**Papers.** None on ieval ([PR
#9092](https://github.com/cvc5/cvc5/pull/9092)). [Hoenicke and Schindler VMCAI
2021](https://doi.org/10.1007/978-3-030-67067-2_24) is the closest published
analogue.

**What would settle it.** `Duplicate_Inst_Entailed` over
`Instantiations_Total` on
the gap set, and an A/B of `--ieval=off`, `--ieval=use-learn`,
`--no-inst-no-entail`.

## R8 — The fallbacks: enumerative instantiation, MBQI, finite model finding

**Effort.** 🟡 Medium Risk / 🔴 Low Gain — coordinating fallback engines has
completeness consequences, while Verus deliberately disables MBQI and supplies
patterns, making these engines unlikely to explain much of this set.

*Rows: `--enum-inst` under "things that helped" (more solved, more
timeouts).*

**The hypothesis.** Verus runs z3 with `smt.mbqi=false`: E-matching or
nothing. cvc5's defaults for these logics already construct no MBQI or FMF
module, but `--cegqi` is auto-enabled (quantified logic with arithmetic or
datatypes) and `--enum-inst` is off. Whether cegqi costs anything on
patterned quantifiers under `strict` (it cannot own them) or on the unpatterned
ones, and whether enumerative instantiation as a last resort converts
timeouts into solves at the price of wasted rounds, are two separate
questions.

**In cvc5 today `(code)`.** `--cegqi` auto-`true` for these logics (set in
`set_defaults.cpp`); `--mbqi` [`false`], `--finite-model-find` [`false`],
`--fmf-bound` [`false`], `--fmf-fun` [`false`]; `--enum-inst` [`false`]
(`--full-saturate-quant` implies it), `--enum-inst-interleave` [`false`],
`--enum-inst-stratify`, `--enum-inst-sum`, `--enum-inst-rd` [`true`],
`--enum-inst-limit` [`-1`]; `--pool-inst` [`true`], inert without pools.
Enumerative runs at `QEFFORT_LAST_CALL` only when everything else is
saturated.

**Tried.** [`ajreynol:enumInstOpts`](https://github.com/ajreynol/cvc5/tree/enumInstOpts) (2022, merged: the `--enum-inst*` family);
[`ajreynol:mbqiEnumChoice`](https://github.com/ajreynol/cvc5/tree/mbqiEnumChoice), [`ajreynol:mbqiEnumChoice2`](https://github.com/ajreynol/cvc5/tree/mbqiEnumChoice2) (2025, mostly merged: choice grammars
for fast enumeration in MBQI), [`ajreynol:mbqiHoDev`](https://github.com/ajreynol/cvc5/tree/mbqiHoDev) (2024); [`ajreynol:fmfCollectModelValue`](https://github.com/ajreynol/cvc5/tree/fmfCollectModelValue)
(2025); [`ajreynol:quantVirtualModel`](https://github.com/ajreynol/cvc5/tree/quantVirtualModel) (2019, `--quant-vmodel`). Nothing about turning
cegqi off for this domain.

**Elsewhere `(code)`.** z3 with `smt.mbqi=false` answers unknown when the
SAT branch is satisfied and quantifiers remain (`m_last_search_failure =
QUANTIFIERS`), which is exactly right for benchmarks known unsat. Dafny, F*
and Boogie set the same. `auto_config=true` would force `mbqi=true`.

**Papers.** Reynolds, Barbosa and Fontaine, [*Revisiting Enumerative
Instantiation*](https://doi.org/10.1007/978-3-319-89963-3_7), TACAS 2018.
Janota, Barbosa, Fontaine and Reynolds, [*Fair and Adventurous Enumeration of
Quantifier Instantiations*](https://arxiv.org/abs/2105.13700), FMCAD 2021. Ge
and de Moura, [*Complete Instantiation for Quantified Formulas in
Satisfiabiliby [sic] Modulo
Theories*](https://doi.org/10.1007/978-3-642-02658-4_25), CAV 2009. Reynolds,
Tinelli, Goel and Krstić, [*Finite Model Finding in
SMT*](https://doi.org/10.1007/978-3-642-39799-8_42), CAV 2013. Dančo, Hozzová
and Janota, [*From MBQI to Enumerative Instantiation and
Back*](https://ceur-ws.org/Vol-4008/SMT_paper10.pdf), SMT 2025.

**What would settle it.** `-o inst-strategy` on the gap set to see whether
cegqi ever fires; an A/B of `--no-cegqi` and of `--enum-inst` on the 545
timeouts.

---

# Group B — what happens to lemmas afterwards

Downstream of group A. A solver that instantiates eagerly must forget; one
that keeps everything must at least decide on it in a sensible order and keep
the SAT core from drowning. The code says cvc5 keeps everything for the
current user context `(code)`:
`LemmaProperty::REMOVABLE` is declared and never set by any theory, MiniSat's
`reduceDB` touches only `clauses_removable`, and the CaDiCaL propagator hands
every theory lemma over as irredundant. z3 deletes every instance clause on
backtracking and only keeps what conflicts taught it.

## R9 — Deleting instantiation lemmas: garbage collection, or scoping them to the branch

**Effort.** 🔴 High Risk / 🟢 High Gain — sound deletion requires SAT callbacks and
scoped duplicate fingerprints across two backends; if stale instances dominate
the clause database, it removes a cost paid throughout the search.

*Rows `h-1`. The mirror of R1.*

**The hypothesis.** After a few hundred rounds the clause database is
dominated by instances that mattered on some abandoned branch. Every unit
propagation, every justification pass and every decision pays for them. z3
throws them away and pays to re-derive; cvc5 keeps them and pays to carry
them. On this workload, where z3 wins, forgetting is the better trade.

**In cvc5 today `(code)`.** `--inst-local` [`false`] ([PR
#12121](https://github.com/cvc5/cvc5/pull/12121), from the fork's
[`ajreynol:instVolatile`](https://github.com/ajreynol/cvc5/tree/instVolatile))
makes selected E-matching and conflict-based-instantiation duplicate caches
SAT-context-dependent, marks their lemmas `LemmaProperty::LOCAL`, and lets the
prop layer guard local lemmas and ignore out-of-scope ones during
justification. It does **not** tell the SAT
solver to delete the clause on pop; the PR explicitly leaves that part
unimplemented. Otherwise `Instantiate::addInstantiation` sends
`LemmaProperty::INPROCESS`, never `REMOVABLE`. MiniSat:
`clauses_persistent` are exempt from `reduceDB`; CaDiCaL:
`add_clause(clause, forgettable=false)`; the only forgettable clauses in the
whole propagator are two tautology "pacifiers". The catch that makes a
one-line `REMOVABLE` experiment unsound: cvc5 caches sent instances in
`inst_match_trie` for the whole user context, so a clause the SAT solver
forgot would never be re-sent. z3 scopes its fingerprint set for exactly this
reason. Deletion therefore needs a deletion *notification* back to the
quantifiers module, which is what the fork's [`ajreynol:satNotify`](https://github.com/ajreynol/cvc5/tree/satNotify) / [`ajreynol:notifySatClause`](https://github.com/ajreynol/cvc5/tree/notifySatClause)
branches built.

**Tried.** [`ajreynol:virtualLemma`](https://github.com/ajreynol/cvc5/tree/virtualLemma) (2021, `--virtual-inst` "mark instantiations as
virtual clauses") and [`ajreynol:virtualClauseDel`](https://github.com/ajreynol/cvc5/tree/virtualClauseDel) (2021) — the first design;
[`ajreynol:instVolatile`](https://github.com/ajreynol/cvc5/tree/instVolatile) (2025, merged as `--inst-local`); [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) (2026,
`--inst-defer`: "instantiations are recorded globally (never re-derived) but
are treated like local assertions in the justification heuristic; a variant
of inst-local that avoids re-deriving instantiations after backtracking");
[`ajreynol:isActiveLemma`](https://github.com/ajreynol/cvc5/tree/isActiveLemma) (2023, `--track-relevant-literals`); [`ajreynol:deferBlock`](https://github.com/ajreynol/cvc5/tree/deferBlock) (2025,
`--defer-block` with `--defer-block-mode=subsolve|delay`, a theory-engine
module that holds lemmas back, with arithmetic branch-and-bound hooks);
[`ajreynol:smtLazyAssert`](https://github.com/ajreynol/cvc5/tree/smtLazyAssert) (2022); [`ajreynol:satNotify`](https://github.com/ajreynol/cvc5/tree/satNotify), [`ajreynol:notifySatClause`](https://github.com/ajreynol/cvc5/tree/notifySatClause) (the deletion
callback). None but `--inst-local` is on `main`; `--inst-local` has not been
measured on the set. Its upstream PR also reports significantly worse overall
performance despite improvements on some cases, so merge status is not
positive performance evidence.

**Elsewhere `(code)`.** z3: instance clauses are `CLS_AUX`, stored in
`m_aux_clauses`, and `context::pop_scope_core` runs `del_clauses(m_aux_clauses,
...)`; `qi_queue::pop_scope` shrinks the instance and delayed-entry stacks;
`fingerprint_set::pop_scope` forgets the instance so it can be rediscovered.
Only `CLS_LEARNED`/`CLS_TH_LEMMA` survive, and those are subject to
activity-based GC (`smt.lemma_gc_strategy` [0: fixed], `lemma_gc_initial`
5000, factor 1.1; `del_inactive_lemmas2` by activity and unassigned-literal
count). `smt.delay_units` [false; Verus true] exists because deleting
instances makes a restart-to-base on every learned unit ruinous (R13). CADE
2007, "Deleting clauses": "we use a single SAT solver, but delete clauses
generated from quantifier instantiation when backtracking. Conflict clauses
and their literals are on the other hand not deleted." Wintersteiger on z3
issue #1151: "lots of 'independent' lemmas also clog up the memory, so you
don't necessarily want to collect and keep all irrelevant lemmas (or
quantifier instances) forever."

**Papers.** [de Moura and Bjørner CADE
2007](https://leodemoura.github.io/files/ematching.pdf). Audemard and Simon,
[*Predicting Learnt Clauses Quality in Modern SAT
Solvers*](https://www.ijcai.org/Proceedings/09/Papers/074.pdf), IJCAI 2009
(LBD). Fazekas, Biere and Scholl, [*Incremental Inprocessing in SAT
Solving*](https://fmv.jku.at/incrinpr/), SAT 2019.

**What would settle it.** Clause-database size against time on the ten worst
(MiniSat's `clauses_persistent` count is one added statistic away), and the
fraction of instance clauses that are ever used in a conflict. Run
`--inst-local` to test its scoped-cache/justification approximation and then
`--inst-defer`; neither run tests clause deletion. A true GC needs the
notification plumbing first.

## R10 — Where instance lemmas sit in the decision order: local, deferred, gated

**Effort.** 🟡 Medium Risk / 🟢 High Gain — existing flags and branches keep the
change narrower than deletion, and deprioritizing thousands of instance
lemmas could recover much of its benefit without changing clause lifetime.

*Rows `h-2`, `h-4`, `h-6`. R9's cheaper cousin: keep the lemmas but stop
deciding on them.*

**The hypothesis.** cvc5's justification heuristic treats an instance lemma
as an assertion to satisfy. With tens of thousands of them, the heuristic
spends its decisions satisfying instances of quantifiers that are not even
asserted on the current branch, and conflicts are found late. z3's default
case-split queue delays every Boolean variable created *during* search behind
the ones from the input, which is the same idea from the other side.

**In cvc5 today `(code)`.** `--inst-local` [`false`] (see R9);
`--jh-rlv-order` [`false`] (activity ordering in the justification
heuristic); `--jh-skolem` [`first`], `--jh-skolem-rlv` [`assert`] — the
skolem-definition machinery that [`ajreynol:ai-jhRlvInst`](https://github.com/ajreynol/cvc5/tree/ai-jhRlvInst) generalises to instances;
`--decision` [`justification`] for any quantified logic (R11).

**Tried.** [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) (`--inst-defer`, above) and [`ajreynol:claudeDev-dts-idef`](https://github.com/ajreynol/cvc5/tree/claudeDev-dts-idef)
(`--inst-defer` with `--dt-split-relevant`, "taking both ideas");
[`ajreynol:ai-jhRlvInst`](https://github.com/ajreynol/cvc5/tree/ai-jhRlvInst) (`--jh-rlv-inst`: "dynamically activate instantiation lemmas
based on whether their associated quantified formula is asserted, analogous
to skolem definitions"; the notes expect low impact since it only matters for
quantifiers that are not top-level); [`ajreynol:ai-jhConflictFirst`](https://github.com/ajreynol/cvc5/tree/ai-jhConflictFirst) (`--jh-conflict-first`:
"prioritize conflict clauses over theory lemmas in the decision justification
heuristic"); [`ajreynol:instLastCallDelay`](https://github.com/ajreynol/cvc5/tree/instLastCallDelay) (skip the last-call check while the
valuation still needs a check); [`ajreynol:termOrigin`](https://github.com/ajreynol/cvc5/tree/termOrigin) (`--inst-nested-max-level=N`,
`--track-term-origins`: a lemma-origin DAG over terms, i.e. z3's generation);
[`ajreynol:instFullPreempt`](https://github.com/ajreynol/cvc5/tree/instFullPreempt) (2024, `--inst-when=full-preempt`: instantiate before
theory combination and before other theories have checked). None of these
branch-only options was found on pinned `main`; none was measured on the set.

**Elsewhere `(code)`.** z3 `smt.case_split` [1] = `CS_ACTIVITY_DELAY_NEW`:
`dact_case_split_queue` keeps Boolean variables created while searching in a
second heap consulted only when the main one is exhausted, so "the atoms
introduced by instance clauses do not immediately hijack the decision order".
Verus sets `case_split=3`, relevancy-driven structural splitting (Dafny's
discussion #3362 calls this avoiding "time travelling triggers"). Instances
also carry a generation, and the cost function reads it (R4).

**Papers.** de Moura and Bjørner, [*Relevancy
Propagation*](https://www.microsoft.com/en-us/research/publication/relevancy-propagation/),
MSR-TR-2007-140. Barrett, Dill and Stump, [*Checking Satisfiability of
First-Order Formulas by Incremental Translation to
SAT*](https://doi.org/10.1007/3-540-45657-0_18), CAV 2002 (the justification
idea).

**What would settle it.** `--inst-local` and `--inst-defer` on the set are two
runs; `--jh-rlv-order` is a third. The decision count per benchmark
(`prop::decisions`) before and after says whether the heuristic was the cost.

## R11 — Decision heuristic versus relevancy: what the SAT solver is made to decide on

**Effort.** 🔴 High Risk / 🟢 High Gain — relevancy crosses assertions, theory
registration, propagation, and decisions; z3 uses it to suppress work at each
of those boundaries, so its possible reach is equally broad.

*Rows `h-29`, `h-28`. The oldest idea in the notes and the least tested.*

**The hypothesis.** z3's relevancy (level 2) does two things cvc5's
justification heuristic does not: it withholds an assigned atom from its
theory until the atom is relevant, and it withholds a term from E-matching
until it is relevant. cvc5 decides only on literals needed to justify the
assertions — the same intent — but every preregistered literal reaches the
theories, and the term database's relevance is a coarse over-approximation
(R23). The gap between the two may be the instances that fire on terms z3
would never have looked at.

**In cvc5 today `(code)`.** `--decision` [`justification` for quantified
logics; `internal` = VSIDS; `stoponly`]; `--jh-skolem`, `--jh-skolem-rlv`,
`--jh-rlv-order`; `--preregister-mode` [`eager`] (`lazy` = preregister when
asserted; `relevant` does not exist on `main`); `--relevance-filter`
[`false`] constructs the `RelevanceManager` (only difficulty and
`NEEDS_JUSTIFY` bookkeeping today); `--random-freq` [`0.0`]; no phase-saving
options are exposed for MiniSat.

**Tried.** [`ajreynol:preregRlv`](https://github.com/ajreynol/cvc5/tree/preregRlv) (2024–2026, 155 commits, [PR
#9503](https://github.com/cvc5/cvc5/pull/9503):
`--preregister-mode=rlv` "Preregister literals when they become relevant";
`RelevantPreregistrar`: "we want to preregister only the literals that, if
they were to be T-propagated, could contribute towards a SAT conflict in the
current context"; polarity-aware relevance over inputs and lemmas);
[`ajreynol:satRlv`](https://github.com/ajreynol/cvc5/tree/satRlv) (2022, 294 commits, `--sat-rlv=none|asserts|all` "use relevancy to
filter all calls, including asserts and preregisters" — the notes call it
broken); [`ajreynol:satRlvTppSolver`](https://github.com/ajreynol/cvc5/tree/satRlvTppSolver); [`ajreynol:jh-new`](https://github.com/ajreynol/cvc5/tree/jh-new) (2021, merged: the current
justification heuristic); [`ajreynol:jhRandom`](https://github.com/ajreynol/cvc5/tree/jhRandom) (2026, `--jh-rand`: randomised
assertion and branch order); [`ajreynol:decEngineReqPhase`](https://github.com/ajreynol/cvc5/tree/decEngineReqPhase), [`ajreynol:propOrderInput`](https://github.com/ajreynol/cvc5/tree/propOrderInput).

**Elsewhere `(code)`.** z3 `smt.relevancy` [2]: `context::assign_core` queues
an atom for theory propagation only if `is_relevant_core(l)`;
`context::relevant_eh` is where quantifiers are asserted, where theories get
`relevant_eh` for lazy axioms (datatype accessors, `bv2int`), and where the
matcher gets its candidates; relevancy is structure-aware (`or`: one true
child; `ite`: the taken branch) and fully backtrackable. `smt.case_split`
modes 3–5 are relevancy-based and refused when `auto_config` is on.
`smt.phase_selection` [3, caching conservative]. Simplify's relevancy is the
ancestor; F* sets `smt.relevancy=2` explicitly.

**Papers.** [*Relevancy
Propagation*](https://www.microsoft.com/en-us/research/publication/relevancy-propagation/),
MSR-TR-2007-140. [Barrett, Dill and Stump CAV
2002](https://doi.org/10.1007/3-540-45657-0_18). Goel, Krstić and Fuchs,
[*Deciding array formulas with frugal axiom
instantiation*](https://doi.org/10.1145/1512464.1512468), SMT 2008.

**What would settle it.** `--preregister-mode=lazy` and `--decision=internal`
on the set are two cheap runs; [`ajreynol:preregRlv`](https://github.com/ajreynol/cvc5/tree/preregRlv) is a build. The measurement that
matters is how many theory facts and matched terms the run touches, not the
decision count.

## R12 — Lemma inprocessing and conflict minimisation

**Effort.** 🟢 Low Risk / 🟡 Medium Gain — mainline switches already expose the
experiment and transformations are checked locally; they may shrink every
instance lemma, but cannot fix a bad instantiation policy.

*Rows `h-7`, `h-8`. Experimental on `main`; never measured here.*

**The hypothesis.** An instance lemma is sent verbatim, with literals the
solver already knows to be true or false at level zero. Rewriting it against
learned units before it reaches the SAT solver (inprocessing) shrinks the
clause set; re-proving a theory lemma by substitution and rewriting drops
redundant literals (the notes: up to half of lemmas come out smaller). Both
apply to instantiation lemmas because those carry `LemmaProperty::INPROCESS`.

**In cvc5 today `(code)`.** `--lemma-inprocess` [`none`] (`light` / `full`),
`--lemma-inprocess-subs` [`simple`] (`all`), `--lemma-inprocess-infer-eq-lit`
[`false`], `--conflict-process` [`none`] (`min` / `min-ext`). All expert;
inprocessing returns trusted nodes without a proof generator and therefore
does not support proof production. `--deep-restart` independently does not
support proofs; the source does not declare the two experimental features
incompatible with each other. Implementation `prop/lemma_inprocess.cpp`,
`prop/zero_level_learner.cpp`.

**Tried.** Developed upstream; no fork branch. Adjacent: [`ajreynol:subConflict`](https://github.com/ajreynol/cvc5/tree/subConflict) (2024,
`--sub-conflict-find` with a subsolver, `--sub-conflict-last-call`,
`--sub-conflict-tlem`), unmerged.

**Elsewhere `(code)`.** z3 has no lemma inprocessing as such, but
`qi_queue::instantiate` runs the instance through `m_context.get_rewriter()`
before internalising it, which is the light form; learned-clause
minimisation is the SAT-level standard.

**Papers.** Sörensson and Biere, [*Minimizing Learned
Clauses*](https://doi.org/10.1007/978-3-642-02777-2_23), SAT 2009. Fleury and
Biere, [*Efficient All-UIP Learned Clause
Minimization*](https://doi.org/10.1007/978-3-030-80223-3_12), SAT 2021.
[Fazekas, Biere and Scholl SAT 2019](https://fmv.jku.at/incrinpr/). No paper
on cvc5's inprocessing.

**What would settle it.** Two runs: `--lemma-inprocess=light` and
`--conflict-process=min`, with the average lemma size before and after.

## R13 — The SAT backend: CaDiCaL, MiniSat, restarts, units

**Effort.** 🟢 Low Risk / 🟡 Medium Gain — both SAT backends and their switch already
exist, making the baseline correction cheap; backend behavior can improve the
whole search but is unlikely to explain quantifier-specific pathologies alone.

*Rows: `--sat-solver=cadical` under "things that helped".*

**The hypothesis.** The SAT core sees a clause set that grows by thousands of
instance clauses per round, and its restart, phase and clause-management
policies were tuned for nothing like that. z3's core has specific
accommodations (delayed units, delayed new variables, geometric restarts
under auto-config); cvc5's MiniSat has restart intervals from 2008 and no
exposed phase policy, and its CaDiCaL runs with `walk`, `lucky` and `ilb`
disabled because of the propagator.

**In cvc5 today `(code)`.** `--sat-solver` [`cadical`] — **but
`--incremental` defaults to `true`, and `set_defaults.cpp` forces MiniSat for
incremental solving unless the SAT solver was set by the user.** The baseline
runs of 2026-09-14 therefore used MiniSat; to get CaDiCaL pass
`--sat-solver=cadical` or `--no-incremental`. `--minisat-simplification`
[`all`, forced to `clause-elim` for any quantified logic];
`--restart-int-base` [`25`], `--restart-int-inc` [`3.0`] (MiniSat only);
`--random-freq` [`0.0`]; `--sat-random-seed`; `--deep-restart` [`none`]
(SMT-level restarts with learned literals). CaDiCaL via IPASIR-UP
(`prop/cadical/cdclt_propagator.cpp`): theory checks run inside
`cb_check_found_model` in a `do…while(recheck)` loop; a theory decision that
introduces new variables forces a model-rejection round trip through
tautology clauses; per-user-level activation literals instead of deletion on
pop; no `--cadical-*` tuning options exist; `kissat` is only a bit-blasting
backend.

**Tried.** [`ajreynol:cadicalDefault`](https://github.com/ajreynol/cvc5/tree/cadicalDefault) (2026-08, merged: CaDiCaL the common default,
MiniSat kept for incremental); [`ajreynol:cadicalPortfolio`](https://github.com/ajreynol/cvc5/tree/cadicalPortfolio) (2026, unmerged);
[`ajreynol:alfCadical`](https://github.com/ajreynol/cvc5/tree/alfCadical) (SAT proofs). Nothing on restart or phase policy under
instantiation.

**Elsewhere `(code)`.** z3's own core: `smt.delay_units` [false; Verus true]
— on a learned unit z3 normally backjumps to base level, and the code comment
says "if the problem has quantifiers, it may be too expensive to do that,
since all instances will need to be recreated"; with `delay_units` it
backjumps one level and re-asserts up to `delay_units_threshold` [32] units
from `m_units_to_reassert`. `smt.restart_strategy` [1, inner-outer
geometric], `restart_factor` [1.1], adaptive restarts by agility;
`smt.phase_selection` [3]; `smt.case_split` [1, delay new variables];
`smt.lemma_gc_strategy`. Under `auto_config=true` the AUFLIA preset would
change these (geometric 1.5, phase always-false), which is one reason Verus
turns it off.

**Papers.** Fazekas, Niemetz, Preiner, Kirchweger, Szeider and Biere,
[*IPASIR-UP: User Propagators for
CDCL*](https://doi.org/10.4230/LIPIcs.SAT.2023.8), SAT 2023. Biere, Faller,
Fazekas, Fleury, Froleyks and Pollitt, [*CaDiCaL
2.0*](https://doi.org/10.1007/978-3-031-65627-9_7), CAV 2024. Bjørner,
Eisenhofer and Kovács, [*Satisfiability Modulo Custom Theories in
Z3*](https://doi.org/10.1007/978-3-031-24950-1_5), VMCAI 2023. Pipatsrisawat
and Darwiche, [*A Lightweight Component Caching Scheme for Satisfiability
Solvers*](https://doi.org/10.1007/978-3-540-72788-0_28), SAT 2007 (phase
saving).

**What would settle it.** The baseline rerun with `--sat-solver=cadical` is
the first experiment of goal 3, because the notes' best-known configuration
included it and the ledger's did not. Then restart intervals on MiniSat, and
a CaDiCaL `delay_units` analogue if the propagator statistics show restarts
after units.

---

# Group C — the ground engine

The theories under the instantiation loop. Each row here is a tail in the
reading of `notes.md`, unless the attribution says otherwise; two of them
(R15, R18) have a one-flag experiment available today.

## R14 — Theory combination: care graph or model-based

**Effort.** 🔴 High Risk / 🟡 Medium Gain — a second combination architecture changes
contracts across every theory and has known logic-specific losses; it may avoid
many care splits, but their share of this gap has not been measured.

*Rows `h-21`.*

**The hypothesis.** cvc5 combines theories by care graphs: each theory
enumerates pairs of shared terms it cares about and the engine splits on their
equality. On UF+datatypes+arithmetic with many shared terms this is a
quadratic source of splits, and the notes' `--inst-when-phase` pacing exists
to give it rounds. z3 has no such loop; a theory proposes only the equalities
its model already makes true.

**In cvc5 today `(code)`.** `--tc-mode` [`care-graph`] is the only mode on
`main`; `--theoryof-mode` [auto: `term` for UFDTLIA/UFDTNIA, `type` when
bit-vectors are present]; `--ee-mode` (R15); `--inst-when-phase` [`2`]
(R1). No `--shared-terms` option.

**Tried.** [`ajreynol:mbtc25`](https://github.com/ajreynol/cvc5/tree/mbtc25) (2026-01, 29 commits, [PR
#12095](https://github.com/cvc5/cvc5/pull/12095): `--tc-mode=model-based`
"Use model-based theory combination": build a model, find congruent but
unmerged applications, split on their unequal arguments; status "30 failures
only"); [`ajreynol:mbtc2`](https://github.com/ajreynol/cvc5/tree/mbtc2) (2019); [`ajreynol:noHoApplyCg`](https://github.com/ajreynol/cvc5/tree/noHoApplyCg) (partly merged); [`ajreynol:sharedSolverCentral`](https://github.com/ajreynol/cvc5/tree/sharedSolverCentral)
(2021); [`ajreynol:arraysStdCg`](https://github.com/ajreynol/cvc5/tree/arraysStdCg) (2022). The notes: model-based is much simpler, usually
comparable, worse on some logics such as QF_ABV.

**Elsewhere `(code)`.** z3: `theory::assume_eqs` hashes theory variables by
model value and calls `context::assume_eq` for collisions; the new equality
atom gets `set_true_first_flag`, so the SAT solver tries it true first —
that phase bias is the "model-based" part. `theory_lra` runs `random_update`
before `assume_eqs` to break value ties. Ground subterms of triggers are
treated as shared terms (`mam_impl::m_shared_enodes`).

**Papers.** de Moura and Bjørner, [*Model-based Theory
Combination*](https://doi.org/10.1016/j.entcs.2008.04.079), SMT 2007 / ENTCS
198(2), 2008. Krstić and Goel, [*Architecting Solvers for SAT Modulo Theories:
Nelson–Oppen with DPLL*](https://doi.org/10.1007/978-3-540-74621-8_1), FroCoS
2007. Jovanović and Barrett, [*Sharing Is Caring: Combination of
Theories*](https://doi.org/10.1007/978-3-642-24364-6_14), FroCoS 2011 (care
graphs). Barrett, Nieuwenhuis, Oliveras and Tinelli, [*Splitting on Demand in
SAT Modulo
Theories*](https://theory.stanford.edu/~barrett/pubs/BNO%2B06-abstract.html),
LPAR 2006. Bruttomesso, Cimatti, Franzén, Griggio and Sebastiani, [*Delayed
Theory Combination vs. Nelson–Oppen for
SMT*](https://disi.unitn.it/rseba/papers/lpar06_dtc.pdf), LPAR 2006.

**What would settle it.** Add a counter for care pairs/splits and record it on
the gap set; current main exposes per-theory `computeCareGraphTime` timers but
not that count. Then build the PR branch.

## R15 — Equality engine architecture: central, distributed, and who gets told what

**Effort.** 🔴 High Risk / 🟡 Medium Gain — shared equality ownership and notification
semantics reach every theory; a mainline central mode lowers experiment risk,
but the expected gain remains workload-dependent.

*Rows `h-20`, `h-22`.*

**The hypothesis.** cvc5's distributed mode gives each theory its own
congruence closure, and shared equalities are propagated between them; every
merge costs a notification per interested party. z3 has one egraph and a list
of theory variables per class. The notes' [`ajreynol:dtMergeNotify`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify) line — merging UF
and datatypes into one engine, at the price of making datatypes a
second-class theory — is a step toward z3's arrangement.

**In cvc5 today `(code)`.** `--ee-mode` [`distributed`] (`central`: all
applicable theories use the central engine; auto-enables
`--arith-eq-solver`). Notifications: `eqNotifyTriggerPredicate`,
`eqNotifyTriggerTermEquality`, `eqNotifyConstantTermMerge`,
`eqNotifyNewClass`, `eqNotifyMerge`, `eqNotifyDisequal`; the quantifiers
engine hooks the master engine (`MasterNotifyClass`) and marks relevance on
merge (R23). Open [PR #9724](https://github.com/cvc5/cvc5/pull/9724) is a
different, lower-level optimisation: replace an always-notified
`ContextNotifyObject` with a dynamic object that requests a pop notification
only after `markNeedsRestore()`. Its reported incremental `Kind2` improvement
is evidence about context-restoration traffic, not equality-merge callbacks;
it was still unmerged on 2026-09-15.

**Tried.** [`ajreynol:centralEe`](https://github.com/ajreynol/cvc5/tree/centralEe), [`ajreynol:centralEeDev`](https://github.com/ajreynol/cvc5/tree/centralEeDev) (2021, merged: `--ee-mode=central`);
[`ajreynol:dtMergeNotify`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify),
[`ajreynol:dtMergeNotify-v2`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v2),
[`ajreynol:dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3)
(tip 2026-05-22: datatypes under the central
engine without `notifyFact`, pending inferences valid in the SAT context,
`Theory::getFactTheory`, regressions named `central-ee-verus-prereg` and
`central-ee-splinterdb-*`); [`ajreynol:dtEecNotDone`](https://github.com/ajreynol/cvc5/tree/dtEecNotDone) (merged); [`ajreynol:ai-eecFixes-0430`](https://github.com/ajreynol/cvc5/tree/ai-eecFixes-0430),
[`ajreynol:ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare) (skip `propagateSharedEquality` for theories fully explained
by the central engine); [`ajreynol:cdno`](https://github.com/ajreynol/cvc5/tree/cdno) (2025, context-dynamic notify objects);
[`ajreynol:minorOpt-0516`](https://github.com/ajreynol/cvc5/tree/minorOpt-0516); [`ajreynol:noEeLinear`](https://github.com/ajreynol/cvc5/tree/noEeLinear) (2023); [`ajreynol:perfDataStructures`](https://github.com/ajreynol/cvc5/tree/perfDataStructures) (2018),
[`ajreynol:lowLevelOptMore`](https://github.com/ajreynol/cvc5/tree/lowLevelOptMore) (2019).

**Elsewhere `(code)`.** z3: `context::add_eq` merges once, calls
`m_qmanager->add_eq_eh` (the matcher's label union and parent-index walk,
typically the dominant cost) and then `merge_theory_vars`, whose fast path
is "r2 and r1 have at most one theory var"; theories may opt out of
disequality notifications (`use_diseqs`). One merge, one notification per
theory variable on the roots.

**Papers.** Nieuwenhuis and Oliveras, [*Fast congruence closure and
extensions*](https://doi.org/10.1016/j.ic.2006.08.009), Inf. Comput. 205(4),
2007. de Moura and Bjørner, [*Z3: An Efficient SMT
Solver*](https://doi.org/10.1007/978-3-540-78800-3_24), TACAS 2008. Nelson and
Oppen, [*Fast Decision Procedures Based on Congruence
Closure*](https://doi.org/10.1145/322186.322198), J. ACM 27(2), 1980. Barbosa
et al., [*cvc5: A Versatile and Industrial-Strength SMT
Solver*](https://doi.org/10.1007/978-3-030-99524-9_24), TACAS 2022.

**What would settle it.** `--ee-mode=central` on the set is one run and
exists today; the [`ajreynol:dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3) branch is a build. A profile of the ten
worst says what fraction of time is in the equality engines at all.

## R16 — Datatypes: when to split, on what, and whether to have them at all

**Effort.** 🟡 Medium Risk / 🟡 Medium Gain — the work is confined mostly to datatype
split gating, but missed splits threaten progress; Verus uses datatypes heavily,
so avoiding irrelevant splits may affect a meaningful subset.

*Rows `h-23`, `h-24`.*

**The hypothesis.** Verus encodes Rust types with datatypes (`Poly` boxing,
`Option`, records), so datatype terms may be numerous even when most never
need a constructor decision. Their prevalence and scale on this corpus must
be measured; the source alone does not justify "every benchmark" or
"thousands". cvc5 considers every datatype equivalence class for splitting;
z3 splits infinite datatypes only at final check, and only after relevancy has
had its say, with the phase
biased to the non-recursive constructor. Two fork branch lines, and one
merged change from [`ajreynol:verusDev`](https://github.com/ajreynol/cvc5/tree/verusDev), are about exactly this.

**In cvc5 today `(code)`.** `TheoryDatatypes::checkSplit` iterates every
datatype equivalence class; skips a class that already has a constructor
label, and — the one relevance guard — a class with an infinite constructor
and no selectors applied; one split lemma per check unless
`--dt-blast-splits` [`false`]; `--dt-binary-split` [`false`] (a `(is-C ∨
¬is-C)` split with a phase preference, instead of the n-way split);
`--dt-share-sel` [`false`; auto-on only for SyGuS, with the comment "not good
to combine with … E-matching"]; `--dt-infer-as-lemmas` [`false`];
`--dt-polite-optimize` [`true`]; `--dt-cyclic` [`true`]; quantifier side
`--quant-dsplit` [`default`, idle without FMF], `--dt-var-exp-quant`
[`true`], `--cons-exp-triggers` [`false`].

**Tried.** [`ajreynol:dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant) (2026-06, `--dt-split-relevant` "only add
splitting lemmas for datatype terms that occur in asserted literals");
[`ajreynol:dtRlvSplit`](https://github.com/ajreynol/cvc5/tree/dtRlvSplit) (2025-11, partly merged, reworked into [`ajreynol:verusDev`](https://github.com/ajreynol/cvc5/tree/verusDev)'s "No split
infinite"); [`ajreynol:dtElim`](https://github.com/ajreynol/cvc5/tree/dtElim) (2025-10, 26 commits, `--dt-elim` "eliminate datatypes
at preprocessing", policies by constructor and field count, "Switch to
1-cons"); [`ajreynol:oneConsInst`](https://github.com/ajreynol/cvc5/tree/oneConsInst) (single-constructor terms instantiated directly);
[`ajreynol:dtLazyInst`](https://github.com/ajreynol/cvc5/tree/dtLazyInst),
[`ajreynol:dtLazyInst2`](https://github.com/ajreynol/cvc5/tree/dtLazyInst2),
[`ajreynol:dtLazyInst3`](https://github.com/ajreynol/cvc5/tree/dtLazyInst3)
(2020–22, `--dt-lazy-inst` "apply the datatypes
instantiate rule lazily"); [`ajreynol:oneConsSkipTester`](https://github.com/ajreynol/cvc5/tree/oneConsSkipTester) (2023); [`ajreynol:dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3)
(R15). The notes credit an assistant's review with the relevant-split idea
independently, and record Kartik's suggestion of a more liberal variant.

**Elsewhere `(code)`.** z3 `smt.dt_lazy_splits` [1]: finite datatypes split
eagerly at `mk_var`, infinite ones only in `final_check_eh`; `mk_split`
first marks an existing recognizer relevant rather than deciding, prefers
the non-recursive constructor and sets `true_first`; accessor axioms are
asserted straight into the egraph when the constructor is known; the occurs
check runs at final check as a DFS. Vampire's approach to datatypes is
axiomatic (Kovács, Robillard and Voronkov).

**Papers.** Barrett, Shikanian and Tinelli, [*An Abstract Decision Procedure
for a Theory of Inductive Data
Types*](https://theory.stanford.edu/~barrett/pubs/BST07-JSAT-abstract.html),
JSAT 3, 2007. Reynolds and Blanchette, [*A Decision Procedure for (Co)datatypes
in SMT Solvers*](https://doi.org/10.1007/s10817-016-9372-6), JAR 58(3), 2017.
Reynolds, Viswanathan, Barbosa, Tinelli and Barrett, [*Datatypes with Shared
Selectors*](https://theory.stanford.edu/~barrett/pubs/RVB%2B18.pdf), IJCAR
2018. Kovács, Robillard and Voronkov, [*Coming to Terms with Quantified
Reasoning*](https://arxiv.org/abs/1611.02908), POPL 2017. Hojjat and Rümmer,
[*Deciding and Interpolating Algebraic Data Types by
Reduction*](https://arxiv.org/abs/1801.02367), 2018.

**What would settle it.** `DATATYPES_SPLIT` lemma counts on the gap set (from
`--stats-internal`), then `--dt-binary-split` as a run and [`ajreynol:dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant)
as a build.

## R17 — Linear integer arithmetic: branch and bound, cuts, and the Diophantine solver

**Effort.** 🔴 High Risk / 🟡 Medium Gain — integer reasoning is correctness-critical
and scheduling changes can trade progress for delay; arithmetic is common here,
but only profiling can separate it from quantifier-driven cost.

*Rows `h-9`, `h-10`, `h-11`, `h-12`.*

**The hypothesis.** Verus arithmetic is mostly bounds and clipping
(`nClip`, `uClip`) over integers that are otherwise uninterpreted; cvc5's
integer solver runs its Diophantine solver and branch-and-bound at every full
check and can branch forever, while z3's solver 6 propagates rational bounds
during search but defers integrality checks, cuts, and integer branching to
final check, delegates a branch to the SAT solver as an atom, and periodises
the expensive handlers with randomised gates.

**In cvc5 today `(code)`.** `--arith-brab` [`true`], `--dio-solver` [`true`;
off only for quantifier-free nonlinear logics], `--dio-turns` [`10`],
`--rr-turns` [`3`], `--dio-decomps` [`false`], `--cut-all-bounded`
[`false`], `--maxCutsInContext` [`65535`], `--arith-eq-solver` [`false`],
`--use-approx` [`false`; GLPK], `--miplib-trick` [`false`],
`--arith-static-learning` [`true`], `--unate-lemmas` [`all`], `--arith-prop`
[`both`], `--new-prop` [`true`], `--replay-*`; pivot heuristics are tuned only
for pure quantifier-free arithmetic; `--arith-rewrite-equalities` off for
these logics.

**Tried.** [`ajreynol:deferBlock`](https://github.com/ajreynol/cvc5/tree/deferBlock) (2025, `--defer-block`, branch-and-bound deferral
hooks "BB only"; the notes: block or delay the lemmas); [`ajreynol:ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc) (2026-06,
`--dio-solver-last-call` "defer Diophantine equation solver conflict
detection to last call effort, instead of running it at every full effort
check"); cvc5 [PR #12178](https://github.com/cvc5/cvc5/pull/12178)
(Daniel Larraz: DIO handles nonlinear monomials;
disabled it for quantifier-free nonlinear logics); [`ajreynol:liaSplitDelay`](https://github.com/ajreynol/cvc5/tree/liaSplitDelay) (2023);
[`ajreynol:linearSolverSub`](https://github.com/ajreynol/cvc5/tree/linearSolverSub) (2024, `--arith-sub-solver`); [`ajreynol:limitArith`](https://github.com/ajreynol/cvc5/tree/limitArith) (2024);
[`ajreynol:elimArith`](https://github.com/ajreynol/cvc5/tree/elimArith), [`ajreynol:elimArithU`](https://github.com/ajreynol/cvc5/tree/elimArithU), [`ajreynol:noArith`](https://github.com/ajreynol/cvc5/tree/noArith) (2024, the notes' inconclusive
elimination experiment); [`ajreynol:learnBranchIte`](https://github.com/ajreynol/cvc5/tree/learnBranchIte); [`ajreynol:eqstatusLinear`](https://github.com/ajreynol/cvc5/tree/eqstatusLinear).

**Elsewhere `(code)`.** z3 with `smt.arith.solver=6`: bound propagation
during search; `check_lia` at final check runs, in order, the gcd test,
`patch_basic_columns`, cubes, HNF cuts, the Diophantine handler (Griggio's
method, `math/lp/dioph_eq.cpp`, on by default, period doubled on failure,
Gomory re-enabled after 16 idle calls), Gomory cuts, and only then
`int_branch`, which returns a fresh bound atom to the SAT solver. Handlers
fire on periods with `lp.random_hammers` because "a deterministic period can
phase-lock with the search". Note that Verus sets `smt.arith.solver=2`, the
legacy simplex, for its default queries, so the z3 the baseline measures is
not the lra solver.

**Papers.** Dutertre and de Moura, [*A Fast Linear-Arithmetic Solver for
DPLL(T)*](https://doi.org/10.1007/11817963_11), CAV 2006. Jovanović and de
Moura, [*Cutting to the Chase: Solving Linear Integer
Arithmetic*](https://doi.org/10.1007/978-3-642-22438-6_26), CADE 2011 / JAR
51(1), 2013. Griggio, [*A Practical Approach to Satisfiability Modulo Linear
Integer Arithmetic*](https://doi.org/10.3233/SAT190086), JSAT 8, 2012. Dillig,
Dillig and Aiken, [*Cuts from
Proofs*](https://theory.stanford.edu/~aiken/publications/papers/cav09.pdf), CAV
2009. King, [*Effective Algorithms for the Satisfiability of Quantifier-Free
Formulas Over Linear Real and Integer
Arithmetic*](https://cs.nyu.edu/media/publications/king_tim.pdf), PhD thesis,
NYU 2014. King, Barrett and Tinelli, [*Leveraging Linear and Mixed Integer
Programming for SMT*](https://theory.stanford.edu/~barrett/pubs/KBT14.pdf),
FMCAD 2014. Bromberger and Weidenbach, [*New techniques for linear arithmetic:
cubes and equalities*](https://doi.org/10.1007/s10703-017-0278-7), FMSD 51(3),
2017.

**What would settle it.** Branch-and-bound and DIO lemma counts per benchmark
on the gap set; [`ajreynol:ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc) as a build; `--no-dio-solver` as a run.

## R18 — Nonlinear arithmetic: off, light, or lazy

**Effort.** 🟢 Low Risk / 🔴 Low Gain — an existing flag matches Verus's policy and
makes the experiment cheap; it applies only to the NIA subset and does not
address the dominant trigger-driven mechanism.

*Rows `h-13`, `h-14`.*

**The hypothesis.** Part of the set is UFDTNIA, and cvc5 enables the full
nonlinear extension (incremental linearisation, tangent planes, factoring,
monomial bounds) whenever the logic says NIA. Verus runs z3 with nonlinear
reasoning off for default queries, and its nonlinear obligations go to
separate `by(nonlinear_arith)` queries. cvc5 may be paying for lemma schemes
that never contribute to the refutation.

**In cvc5 today `(code)`.** `--nl-ext` [`full`] (`none` / `light` / `full`),
`--nl-cov` [off for quantified integer logics: "logic without reals, or
involving integers or quantifiers"], `--nl-ext-tplanes` [`true`],
`--nl-ext-factor` [`true`], `--nl-ext-rewrite` [`true`],
`--nl-ext-flatten-mon` [`true`], `--nl-ext-initial-sign-lemmas` [off with
quantifiers], `--nl-rlv` [`none`; any other value is a fatal error in a
quantified logic], `--nl-icp` [`false`]. To disable nonlinear reasoning:
`--nl-ext=none --no-nl-cov`. Nonlinear arithmetic forces UF into the logic.

**Tried.** [`ajreynol:arithFlattenCollect2`](https://github.com/ajreynol/cvc5/tree/arithFlattenCollect2) (2025, merged: the AC flattening of the
notes' `h-13`, "very incomplete"); [`ajreynol:nlEnums`](https://github.com/ajreynol/cvc5/tree/nlEnums) (merged); [`ajreynol:nlAlwaysCheck`](https://github.com/ajreynol/cvc5/tree/nlAlwaysCheck)
(2022); [`ajreynol:simpleNonzeroFactor`](https://github.com/ajreynol/cvc5/tree/simpleNonzeroFactor) (2023); [`ajreynol:nlExtTplaneLimit`](https://github.com/ajreynol/cvc5/tree/nlExtTplaneLimit), [`ajreynol:nlExtTplanesDef`](https://github.com/ajreynol/cvc5/tree/nlExtTplanesDef)
(2018). No branch named `arithFlattenEq` exists in the fork; the notes' link
is stale.

**Elsewhere `(code)`.** z3: `smt.arith.nl=false` is read only by the legacy
solver (`theory_arith_nl.h`), which is the one Verus selects, so for Verus's
default queries nonlinear reasoning is off entirely; with the lra solver the
`nla` core runs only when a *relevant* monomial exists
(`core::has_relevant_monomial`), gated by `arith.nl.delay` [10] final checks,
and monomials stay as egraph terms and tableau columns regardless. Verus
switches to `smt.arith.solver=6` for `by(nonlinear_arith)` queries.

**Papers.** Cimatti, Griggio, Irfan, Roveri and Sebastiani, [*Incremental
Linearization for Satisfiability and Verification Modulo Nonlinear Arithmetic
and Transcendental Functions*](https://doi.org/10.1145/3230639), TOCL 19(3),
2018. Reynolds, Tinelli, Jovanović and Barrett, [*Designing Theory Solvers with
Extensions*](https://theory.stanford.edu/~barrett/pubs/RTJ%2B17%2C-abstract.html),
FroCoS 2017. Jovanović and de Moura, [*Solving Non-linear
Arithmetic*](https://dddejan.github.io/papers/jovanovic-ijcar2012.pdf), IJCAR
2012. Kremer, Reynolds, Barrett and Tinelli, [*Cooperating Techniques for
Solving Nonlinear Real Arithmetic in the cvc5 SMT
Solver*](https://doi.org/10.1007/978-3-031-10769-6_7), IJCAR 2022.

**What would settle it.** The gap set split by logic (the results files carry
the path, and the path carries the logic); then `--nl-ext=none` and
`--nl-ext=light` on the NIA subset. If cvc5 answers unsat as often with
nonlinear off, the extension was pure cost here.

## R19 — Bit-vectors inside quantified problems

**Effort.** 🔴 High Risk / 🔴 Low Gain — delaying bit-blasting must preserve progress
across generated terms and theory combination, while only the bit-vector subset
can benefit.

*Not in the notes. The UFBVDTNIA subset of the set.*

**The hypothesis.** The bit-vector benchmarks are the same Verus proofs with
`by(bit_vector)` or bit-width reasoning mixed in. cvc5 handles them with lazy
bit-blasting through the `bitblast` solver, switches `--theoryof-mode` to
`type` because bit-vectors are present (a change that affects theory
combination for the whole benchmark, not just its bit-vector part), and
cannot use eager bit-blasting in a non-pure logic. z3 bit-blasts eagerly
inside its kernel at internalisation, rebuilds the circuit for each instance,
and keeps bit-vector terms visible to E-matching.

**In cvc5 today `(code)`.** `--bv-solver` [`bitblast`] (`bitblast-internal`),
`--bitblast` [`lazy`; `eager` is a fatal error outside pure BV / QF_UFBV],
`--bv-sat-solver` [`cadical`] (`cryptominisat`, `kissat`), `--bv-propagate`
[forced off for `bitblast`], `--solve-bv-as-int` [`off`; other modes widen
the logic to nonlinear integers], `--bv-to-bool` [`false`], `--bool-to-bv`
[forced off with `--cegqi-bv` in quantified logics], `--bv-eager-eval`
[`false`], `--cegqi-bv` [`true`], `--theoryof-mode` [`type` when BV is in
the logic]. Arithmetic with bit-vectors forces UF into the logic.

**Tried.** [`ajreynol:bitblastLc`](https://github.com/ajreynol/cvc5/tree/bitblastLc) (2025, `--bitblast-lc` "delay to last call for
bitblasting"); [`ajreynol:bvToIntQuant-031126`](https://github.com/ajreynol/cvc5/tree/bvToIntQuant-031126) (2026, int-blasting under quantified
`bv2nat`); [`ajreynol:bvVElim`](https://github.com/ajreynol/cvc5/tree/bvVElim), [`ajreynol:bbOpt`](https://github.com/ajreynol/cvc5/tree/bbOpt), [`ajreynol:bvLimitRec`](https://github.com/ajreynol/cvc5/tree/bvLimitRec), [`ajreynol:disableFlattenAssoc`](https://github.com/ajreynol/cvc5/tree/disableFlattenAssoc) (2025);
[`ajreynol:ufConvRlv`](https://github.com/ajreynol/cvc5/tree/ufConvRlv) (2023, reduce only relevant terms in the UF conversion solver);
[`ajreynol:bvBbExtf`](https://github.com/ajreynol/cvc5/tree/bvBbExtf) (2017, lazy blasting of expensive operators).

**Elsewhere `(code)`.** z3 `smt/theory_bv.cpp`: every bit-vector term is
blasted at internalisation (`init_bits`, one Boolean per bit); no lazy mode
in the smt kernel (`bv.delay` is read only by the new euf solver);
`bv.reflect` [true] keeps bit-vector terms as egraph nodes with visible
arguments so triggers over them fire; relevancy stays at level 2 for
quantified bit-vector problems; `bv2int`/`int2bv` bridging axioms are
asserted lazily from `relevant_eh`. Verus sends `by(bit_vector)` obligations
as separate prelude-free queries with solver defaults ("TODO: tune Z3/CVC5
options for bit-vector queries").

**Papers.** Niemetz, Preiner, Reynolds, Zohar, Barrett and Tinelli, [*Towards
Bit-Width-Independent Proofs in SMT
Solvers*](https://theory.stanford.edu/~barrett/pubs/NPR%2B19.pdf), CADE 2019
(JAR 2021). Zohar, Irfan, Mann, Niemetz, Nötzli, Preiner, Reynolds, Barrett and
Tinelli, [*Bit-Precise Reasoning via
Int-Blasting*](https://doi.org/10.1007/978-3-030-94583-1_24), VMCAI 2022.
Hadarean, Bansal, Jovanović, Barrett and Tinelli, [*A Tale of Two Solvers:
Eager and Lazy Approaches to
Bit-Vectors*](https://doi.org/10.1007/978-3-319-08867-9_45), CAV 2014.
Niemetz, Preiner and Zohar, [*Scalable Bit-Blasting with
Abstractions*](https://doi.org/10.1007/978-3-031-65627-9_9), CAV 2024.

**What would settle it.** The gap set by logic first: if the UFBVDTNIA share
of the gap is proportional to its share of the set, bit-vectors are not a
direction. Then `--theoryof-mode=term` on that subset.

---

# Group D — before the search

What the search is given, and what it is made to look at. R20 holds the one
measured win so far; R22 and R23 have one-flag experiments.

## R20 — Preprocessing: `distinct`, non-clausal simplification, ITE

**Effort.** 🟢 Low Risk / 🟡 Medium Gain — preprocessing rewrites are localized and
lazy `distinct` already produced the register's one measured speedup; further
wins are plausible but cannot explain search-heavy timeouts by themselves.

*Rows `h-25`, `h-26`, `h-27`.*

**The hypothesis.** The one measured number in the notes came from here: lazy
handling of large `distinct` terms, an average 1.75× on this set at 60 s, from
one preprocessing change. The rest of the pipeline was never examined with
the same eye: non-clausal simplification is "somewhat slow", an ITE
simplification is off by default, and `set_defaults.cpp` carries the comment
"simplification=none works better for SMT LIB benchmarks with quantifiers"
while setting `batch` anyway.

**In cvc5 today `(code)`.** `distinct`: the rewriter blasts up to 10 children;
`--distinct-elim-threshold` [`0`; runs only when set] blasts up to N;
otherwise `theory/uf/distinct_extension.cpp` handles it lazily ([PR
#12136](https://github.com/cvc5/cvc5/pull/12136),
from the fork's [`ajreynol:distinctExt`](https://github.com/ajreynol/cvc5/tree/distinctExt)). `--simplification` [`batch`] (`none`),
`--static-learning` [`true`], `--arith-static-learning` [`true`],
`--learned-rewrite` [`false`], `--ite-simp` [`false`; implies
`--early-ite-removal`], `--on-repeat-ite-simp` [`false`], `--simp-ite-compress`
[`false`], `--repeat-simp`, `--unconstrained-simp`, `--simp-with-care` [all
require a quantifier-free logic], `--ext-rew-prep` [`off`], `--sort-inference`
[`false`], `--deep-restart` [`none`]. Pass order in
`smt/process_assertions.cpp`; `non-clausal-simp` runs inside
`simplifyAssertions` under `batch`.

**Tried.** [`ajreynol:lazyDistinct`](https://github.com/ajreynol/cvc5/tree/lazyDistinct) → [`ajreynol:distinctExt`](https://github.com/ajreynol/cvc5/tree/distinctExt) (2025, merged), [`ajreynol:distinctElim`](https://github.com/ajreynol/cvc5/tree/distinctElim)
(2026, merged, the threshold option), [`ajreynol:ufEagerDistinct`](https://github.com/ajreynol/cvc5/tree/ufEagerDistinct) (2026,
`--uf-eager-distinct`, unmerged), [`ajreynol:lazyDistinctSlv-pf`](https://github.com/ajreynol/cvc5/tree/lazyDistinctSlv-pf) (proofs);
[`ajreynol:simplifyRecFun`](https://github.com/ajreynol/cvc5/tree/simplifyRecFun) (2026, `--simplify-rec-fun`); [`ajreynol:eagerElimDefs`](https://github.com/ajreynol/cvc5/tree/eagerElimDefs) (2024,
`--eager-elim-defs`); [`ajreynol:rlvTermSimplify`](https://github.com/ajreynol/cvc5/tree/rlvTermSimplify) (2024); [`ajreynol:ncSimpMore`](https://github.com/ajreynol/cvc5/tree/ncSimpMore) (2023),
[`ajreynol:ncSimplifyInc`](https://github.com/ajreynol/cvc5/tree/ncSimplifyInc) (2019); [`ajreynol:iteApply`](https://github.com/ajreynol/cvc5/tree/iteApply), [`ajreynol:learnBranchIte`](https://github.com/ajreynol/cvc5/tree/learnBranchIte), [`ajreynol:theoryRewriteEqIte`](https://github.com/ajreynol/cvc5/tree/theoryRewriteEqIte);
[`ajreynol:noSimpleLearnedLitPp`](https://github.com/ajreynol/cvc5/tree/noSimpleLearnedLitPp), [`ajreynol:noConjoinLit`](https://github.com/ajreynol/cvc5/tree/noConjoinLit) (2023).

**Elsewhere `(code)`.** z3's smt path uses `asserted_formulas::reduce`, not the
new simplifier pipeline (`smt.solve_eqs`, `smt.elim_unconstrained` have no
effect on a plain `z3 file.smt2`): value propagation, NNF/CNF (forced on when
quantifiers are present), the rewriter, injectivity-axiom refinement,
clause flattening; macro finding, quantifier elimination and Gaussian
elimination are off by default. `distinct` with at most 32 arguments is
asserted as is; above that, `context::assert_distinct` uses the fresh-sort
trick (a fresh function into a fresh sort with one interpreted constant per
argument), linear rather than quadratic. The rewriter's `blast_distinct` is
off. Verus and F* set `rewriter.sort_disjunctions=false`, keeping disjunct
order as written; cvc5's rewriter normalises the order of children of
commutative operators, which may reorder what the decision heuristic sees
(reasoning, not measured).

**Papers.** Kim, Somenzi and Jin, [*Efficient Term-ITE Conversion for
Satisfiability Modulo
Theories*](https://doi.org/10.1007/978-3-642-02777-2_20), SAT 2009 (cited by
cvc5's `--ite-simp`). [Barbosa et al., cvc5, TACAS
2022](https://doi.org/10.1007/978-3-030-99524-9_24) (the pass pipeline).
Bjørner, de Moura, Nachmanson and Wintersteiger, [*Programming
Z3*](https://z3prover.github.io/papers/programmingz3.html), 2019.

**What would settle it.** Preprocessing time as a share of solve time on the
gap set (`--stats`); then `--simplification=none`, `--no-static-learning`,
`--ite-simp` as runs.

## R21 — Quantifier preprocessing: what is done to a quantifier before it is ever matched

**Effort.** 🔴 High Risk / 🟡 Medium Gain — rewrites must preserve binders, annotations,
and trigger intent, so semantic risk is high; avoiding harmful preprocessing
could help all patterned quantifiers if the profiles implicate it.

*Not a row in the notes; the flip side of R5.*

**The hypothesis.** cvc5 miniscopes, prenexes, eliminates variables, lifts
ITEs and splits conditionals in quantifier bodies by default. Verus wrote its
quantifiers and triggers for z3, which leaves an annotated quantifier alone.
Under `--user-pat=strict` cvc5 also leaves it alone, because the rewriter
classifies it as non-standard; under the default `trust` it does not. Part of
what `strict` bought in the baseline may be this, not ownership.

**In cvc5 today `(code)`.** `--miniscope-quant` [`conj-and-fv`] (`off` /
`conj` / `fv` / `agg`), `--miniscope-quant-user` [`false`], `--prenex-quant`
[`simple`] (`none` / `norm`), `--prenex-quant-user` [`false`],
`--pre-skolem-quant` [`off`], `--var-elim-quant` [`true`],
`--var-ent-eq-elim-quant` [`true`], `--var-ineq-elim-quant` [`true`],
`--dt-var-exp-quant` [`true`], `--ite-lift-quant` [`simple`],
`--cond-var-split-quant` [`on`], `--elim-taut-quant` [`true`],
`--quant-alpha-equiv` [`true`], `--macros-quant` [`false`]
(`--macros-quant-mode` [`ground-uf`]), `--global-negate` [`false`],
`--ext-rewrite-quant` [`false`]. With `strict`, a patterned quantifier skips
nearly all of these.

**Tried.** [`ajreynol:macrosEagerInst`](https://github.com/ajreynol/cvc5/tree/macrosEagerInst), [`ajreynol:macroEagerInstMt`](https://github.com/ajreynol/cvc5/tree/macroEagerInstMt) (2024, macros as the first
eager-instantiation target), [`ajreynol:ai-macroPf`](https://github.com/ajreynol/cvc5/tree/ai-macroPf), [`ajreynol:macrosHo`](https://github.com/ajreynol/cvc5/tree/macrosHo) (merged),
[`ajreynol:quantMacrosPf`](https://github.com/ajreynol/cvc5/tree/quantMacrosPf); [`ajreynol:prenexLift`](https://github.com/ajreynol/cvc5/tree/prenexLift) (2017); [`ajreynol:p657`](https://github.com/ajreynol/cvc5/tree/p657) (do not prenex into non-standard
quantifiers); [`ajreynol:quantRew-1006`](https://github.com/ajreynol/cvc5/tree/quantRew-1006) (constructor equalities in bodies);
[`ajreynol:quantTheoryRewrites`](https://github.com/ajreynol/cvc5/tree/quantTheoryRewrites);
[`ajreynol:alphaEqVarShadow`](https://github.com/ajreynol/cvc5/tree/alphaEqVarShadow),
[`ajreynol:ai-fixAlphaEq`](https://github.com/ajreynol/cvc5/tree/ai-fixAlphaEq),
[`ajreynol:ai-fixAlphaEq-2`](https://github.com/ajreynol/cvc5/tree/ai-fixAlphaEq-2),
and [`ajreynol:ai-fixAlphaEq-v3`](https://github.com/ajreynol/cvc5/tree/ai-fixAlphaEq-v3)
(alpha-equivalence and proofs). No miniscoping branch.

**Elsewhere `(code)`.** z3: pattern inference returns early on an annotated
quantifier and Verus sets `pi.enabled=false` anyway; `smt.pull_nested_quantifiers`
[false], `smt.q.lift_ite` [0], `smt.macro_finder` [false] with the code
comment that it "destroys the existing patterns" on Boogie-style benchmarks;
NNF is forced. Dafny, F* and Verus all tune the *encoding* side (trigger
selection, `sort_disjunctions`, `der`) rather than the solver's rewriting.

**Papers.** Fontaine and Schurr, [*Quantifier Simplification by Unification in
SMT*](https://doi.org/10.1007/978-3-030-86205-3_13), FroCoS 2021. El Ghazi,
Ulbrich, Taghdiri and Herda, [*Reducing the Complexity of Quantified Formulas
via Variable Elimination*](https://arxiv.org/abs/1408.0700), SMT 2013. [Leino
and Pit-Claudel CAV
2016](https://www.microsoft.com/en-us/research/publication/trigger-selection-strategies-stabilize-program-verifiers/)
(why verifiers own trigger selection).

**What would settle it.** `--user-pat=trust` with `--miniscope-quant=off
--prenex-quant=none --ite-lift-quant=none --cond-var-split-quant=off` against
`strict`: if they match, the rewriting was the effect of `strict`.

## R22 — Preregistration: which literals the theories are told about

**Effort.** 🟡 Medium Risk / 🟡 Medium Gain — the long-lived branch demonstrates bounded
plumbing but relevance mistakes can hide needed theory facts; the gain depends
on how much eager preregistration pollutes this set.

*Rows `h-28`.*

**The hypothesis.** cvc5 preregisters a literal with its theory when the
literal is registered with the SAT solver, so every instance lemma delivers
all its atoms to the theories at once, whether or not the search will ever
assign them. z3 hands an atom to its theory only when it is assigned *and*
relevant. `lazy` preregistration exists on `main`; `relevant` exists as a
long-lived branch.

**In cvc5 today `(code)`.** `--preregister-mode` [`eager`] (`lazy`: when
asserted); `--relevance-filter` [`false`]; `prop/theory_preregistrar.cpp`.

**Tried.** [`ajreynol:preregRlv`](https://github.com/ajreynol/cvc5/tree/preregRlv) (R11: `--preregister-mode=rlv`, 552 lines, [PR
#9503](https://github.com/cvc5/cvc5/pull/9503),
branch since 2024-04, tip dated 2026-04-23); [`ajreynol:satRlv`](https://github.com/ajreynol/cvc5/tree/satRlv) (2022, the notes' old
broken branch); [`ajreynol:sdm-assertTerms`](https://github.com/ajreynol/cvc5/tree/sdm-assertTerms), [`ajreynol:skolemLemma`](https://github.com/ajreynol/cvc5/tree/skolemLemma) (2022).

**Elsewhere `(code)`.** z3 `smt.relevancy` [2] — see R11; theory axioms for
datatype accessors and `bv2int` are created from `relevant_eh`.

**Papers.** [de Moura and Bjørner, *Relevancy
Propagation*](https://www.microsoft.com/en-us/research/publication/relevancy-propagation/),
MSR-TR-2007-140.

**What would settle it.** `--preregister-mode=lazy` on the set, today. Then the
branch.

## R23 — Term-database relevance: which ground terms E-matching may use

**Effort.** 🟡 Medium Risk / 🟢 High Gain — eligibility and last-resort fallback are
subtle, but z3's matcher is relevance-driven and reducing the candidate term
set would compound across every E-matching round.

*The "things that helped" row `--term-db=relevant`; now the default.*

**The hypothesis.** The set of ground terms available to triggers decides how
many instances a round produces. `relevant-all-delay` — only terms connected
to current assertions, then everything as a last resort — is the fork's
[`ajreynol:verusDev`](https://github.com/ajreynol/cvc5/tree/verusDev) work and is now cvc5's default. Its relevance is a monotone
over-approximation (a merge marks both sides and their subterms relevant
forever), so on long runs it converges to `all`.

**In cvc5 today `(code)`.** `--term-db-mode` [`relevant-all-delay`] (`all` /
`relevant`); `TermDb::eqNotifyMerge` marks on merge; `shouldRecheck` widens
once before answering unknown, "only if at least one new term was added to
the term database"; `--register-quant-body-terms` [`false`].

**Tried.** [`ajreynol:verusDev`](https://github.com/ajreynol/cvc5/tree/verusDev), [`ajreynol:lastCallRecheck`](https://github.com/ajreynol/cvc5/tree/lastCallRecheck) (2026-02, merged); [`ajreynol:tdbRelevant`](https://github.com/ajreynol/cvc5/tree/tdbRelevant)
(2024, enable `relevant` by default; superseded); [`ajreynol:cdRlvTerms`](https://github.com/ajreynol/cvc5/tree/cdRlvTerms) (2024,
context-dependent relevance via the master engine → [`ajreynol:trackSkip`](https://github.com/ajreynol/cvc5/tree/trackSkip), likely
merged); [`ajreynol:rlvTermSimplify`](https://github.com/ajreynol/cvc5/tree/rlvTermSimplify), [`ajreynol:tdbLLOpts`](https://github.com/ajreynol/cvc5/tree/tdbLLOpts) (2024); [`ajreynol:tdbDev1107`](https://github.com/ajreynol/cvc5/tree/tdbDev1107), [`ajreynol:tdbOpt1108`](https://github.com/ajreynol/cvc5/tree/tdbOpt1108)
(2021); [`ajreynol:tdbOldIndex`](https://github.com/ajreynol/cvc5/tree/tdbOldIndex) (2020, `--tdb-old-index` prefer old terms in indices);
[`ajreynol:optTdbTNode`](https://github.com/ajreynol/cvc5/tree/optTdbTNode) (2019).

**Elsewhere `(code)`.** z3 matches only enodes marked relevant: `relevant_eh`
feeds the matcher's candidate queue, `execute_core` asserts relevance, and
relevancy is backtracked with the search rather than accumulated.

**Papers.** [de Moura and Bjørner, *Relevancy
Propagation*](https://www.microsoft.com/en-us/research/publication/relevancy-propagation/),
MSR-TR-2007-140; [*Simplify* J. ACM
2005](https://doi.org/10.1145/1066100.1066102) (the relevance of terms to
matching).

**What would settle it.** `--term-db-mode=all` and `=relevant` against the
default on the set (three runs), with `QuantifiersEngine::Num_Quantifiers`,
term-database size and instance counts.

---

# Group E — cross-cutting

## R24 — A domain configuration: run cvc5 the way Verus runs z3

**Effort.** 🟢 Low Risk / 🟢 High Gain — it composes existing options and is easy to
revert, while the existing two-flag baseline bundle already improves PAR2 and
a measured larger bundle is the cheapest plausible path to a substantial
result.

*The notes' "things that helped", made into one object.*

**The hypothesis.** Verus hands z3 nine options and hands cvc5 one
(`incremental=true`, plus `(set-logic ALL)`). Most of the z3 choices suggest
an analogous cvc5 policy worth isolating—quantifier modules and patterns,
incrementality/backend, nonlinear reasoning, and relevance—even though the
option sets are not one-to-one. A cvc5 configuration assembled from the
directions above — and a mode that sets it — is the cheapest thing this
project can deliver. The baseline shows that the existing
`--no-cbqi --user-pat=strict` bundle improves cvc5's PAR2 by a factor of 1.2;
its flags have not been isolated.

**In cvc5 today `(code)`.** No Verus- or Dafny-specific option, comment or
regression exists. `-q` is `--quiet` and changes nothing about solving.
`--safe-mode=safe|stable` forbids expert options and allows one regular
option, so it is unusable for tuning. `-o options-auto` prints every option
`set_defaults.cpp` flipped. The candidate bundle from this document, each
flag existing on `main`: `--no-incremental` (or `--sat-solver=cadical`),
`--user-pat=strict`, `--no-cbqi`, `--no-cegqi`, `--preregister-mode=lazy`,
`--inst-local` or `--jh-rlv-order`, `--nl-ext=none` for NIA,
`--lemma-inprocess=light`, `--dt-binary-split`, `--ee-mode=central`,
`--simplification=none`. Each is one run; the bundle is one more.

**Tried.** [`ajreynol:verusDev`](https://github.com/ajreynol/cvc5/tree/verusDev) (2025-11 to 2026-02, merged in pieces: the
`relevant-all-delay` default, the last-resort recheck, delayed function
assignment, datatype splitting over equivalence classes). The notes'
"u-ssc" configuration (`--user-pat=strict --no-cbqi --sat-solver=cadical`)
is the closest thing to a bundle so far.

**Elsewhere `(code)`.** Verus (`source/air/src/context.rs`): `auto_config=false`,
`smt.mbqi=false`, `smt.case_split=3`, `smt.qi.eager_threshold=100`,
`smt.delay_units=true`, `smt.arith.solver=2`, `smt.arith.nl=false`,
`pi.enabled=false`, `rewriter.sort_disjunctions=false`; `smt.arith.solver=6`
for `by(nonlinear_arith)`; bit-vector queries with defaults; rlimit scaled at
3,000,000 per second. With `auto_config=true` z3 would apply its AUFLIA
preset and silently replace the eager threshold with 7, turn MBQI on, and
change phase and restart policy. Dafny, through Boogie, also gets
`smt.mbqi=false`; Dafny itself sets `auto_config=false`, `type_check=true`,
`smt.qi.eager_threshold=44`, `smt.delay_units=true`, model-completion options,
and `smt.case_split=3` ("time travelling triggers", Dafny discussion #3362).
It sets `smt.arith.nl=false` only for arithmetic mode 3 or higher; this is not
the same nine-option preset as Verus. F*: `smt.mbqi=false`,
`auto_config=false`, `smt.case_split=3`, `smt.relevancy=2`, and, for z3
4.12.3 or newer, `rewriter.enable_der=false`,
`rewriter.sort_disjunctions=false`, `pi.decompose_patterns=false`, and
`smt.arith.solver=6`. Boogie issue #73 records that the defaults
date from about 2007 and were "geared towards particular kinds of benchmarks
(quantifier-heavy, etc.)" with no per-option rationale; Leino on z3 issue
#7363: "the requirement for :auto_config and :smt.mbqi to be set to false
enables trigger-based quantifiers".

**Papers.** [Leino and Pit-Claudel CAV
2016](https://www.microsoft.com/en-us/research/publication/trigger-selection-strategies-stabilize-program-verifiers/).
Bai, Hawblitzel and Lattuada, [*Tunable Automation in Automated Program
Verification*](https://arxiv.org/abs/2512.03926), 2025 (Verus's tunable
instantiation levels). Lattuada et al., [*Verus: A Practical Foundation for
Systems Verification*](https://doi.org/10.1145/3694715.3695952), SOSP 2024.

**What would settle it.** This is goal 3 in its cheapest form: the twelve
single-flag runs above, each against the baseline, then the bundle. The
result is a table with one row per flag, which is also the first draft of
the attribution.

## R25 — Low-level engineering: the constant factors

**Effort.** 🟢 Low Risk / 🟡 Medium Gain — profile-led constant-factor fixes are
usually isolated and individually safe; several may accumulate, but no single
one is expected to explain the structural timeout gap.

*Rows `h-22`. Not a research direction on its own; the tail that remains
when the algorithmic directions are done, and sometimes the head.*

**The hypothesis.** Some of the 10–20× cases in the gap set (306 of the 504
solved-but-slow) are not a different algorithm but the same algorithm with
larger constants: node hashing, the trie indices of the term database,
equality-engine notification overhead, memory. A targeted profile can expose
these, and the fork has several old branches of exactly this kind.

**In cvc5 today `(code)`.** Nothing to configure; `job_launcher`'s host
scripts include `get_profile` (callgrind) and `get_backtrace`. Open [PR
#9724](https://github.com/cvc5/cvc5/pull/9724), described precisely in R15,
is the notes' context-notification example.

**Tried.** [`ajreynol:perfDataStructures`](https://github.com/ajreynol/cvc5/tree/perfDataStructures) (2018, 31 commits), [`ajreynol:lowLevelOptMore`](https://github.com/ajreynol/cvc5/tree/lowLevelOptMore) (2019),
[`ajreynol:optTdbTNode`](https://github.com/ajreynol/cvc5/tree/optTdbTNode) (2019), [`ajreynol:tdbLLOpts`](https://github.com/ajreynol/cvc5/tree/tdbLLOpts) (2024), [`ajreynol:minorOpt-0516`](https://github.com/ajreynol/cvc5/tree/minorOpt-0516) (2025, partly
merged), [`ajreynol:cdno`](https://github.com/ajreynol/cvc5/tree/cdno) (2025), [`ajreynol:optTheoryOf`](https://github.com/ajreynol/cvc5/tree/optTheoryOf), [`ajreynol:optGetType`](https://github.com/ajreynol/cvc5/tree/optGetType), [`ajreynol:optArithRw`](https://github.com/ajreynol/cvc5/tree/optArithRw),
[`ajreynol:getValueOpt`](https://github.com/ajreynol/cvc5/tree/getValueOpt) (2022–23), [`ajreynol:rewriteDep`](https://github.com/ajreynol/cvc5/tree/rewriteDep) (2025, "fix performance").

**Elsewhere `(code)`.** z3's matcher and egraph are built around cheap
approximations: 64-bit label sets as Bloom filters on every root, region
allocators, fingerprints as the duplicate check, candidate lists compressed
by expr id above a threshold.

**Papers.** None; engineering.

**What would settle it.** callgrind on the ten worst solved-but-slow
benchmarks, at row 1 of the latency table. If one function dominates, this is
the direction for those ten.

## R26 — Attribution instrumentation: the tools goal 2 needs

**Effort.** 🟢 Low Risk / 🟢 High Gain — instrumentation is largely outside solving
semantics, and trustworthy attribution removes the central uncertainty that
currently blocks every high-risk implementation.

*Rows `h-14` (instability); the profiling the notes never had.*

**The hypothesis.** Every direction above ends with "what would settle it",
and most of those measurements need counters cvc5 does not print by default,
per-quantifier instance counts against z3's, or a view of the instantiation
graph. The verifier community built these for z3 (Axiom Profiler, SMTScope,
Verus's `--profile`, Mariposa, Cazamariposas, SHAKE) and none of them reads
cvc5's output. Building the cvc5 side is the project's own instrument, and
it is also what makes a Verus user able to debug a cvc5 slowdown at all.

**In cvc5 today `(code)`.** `-o inst` (`(num-instantiations <qid> <n>)` for
named quantifiers at the end of each instantiation round; unnamed formulas
require `--print-inst-full`), `-o inst-strategy` (which module ran),
`-o trigger` (selected triggers; [`ajreynol:userTriggerOut2`](https://github.com/ajreynol/cvc5/tree/userTriggerOut2) distinguishes user
ones), `-o lemmas`, `-o incomplete` (why unknown), `-o options-auto`,
`-o learned-lits`; `--dump-instantiations`, `--print-inst` [`list`] (`num`),
`--print-inst-full`; `--stats-internal` with
`Instantiate::Instantiations_Total`, `Instantiate::Duplicate_Inst`,
`Instantiate::Duplicate_Inst_Eq`,
`Instantiate::Duplicate_Inst_Entailed`,
`theory::QuantifiersEngine::time_ematching`,
`theory::QuantifiersEngine::time_conflict_based_inst`,
`QuantifiersEngine::Rounds_Instantiation_Full`,
`QuantifiersEngine::Rounds_Instantiation_Last_Call`,
`QuantifiersEngine::Triggers`, `QuantifiersEngine::Triggers_Multi`, and the
CaDiCaL propagator counters. No matching-loop
detection, no instantiation graph, no per-quantifier cost on `main`.

**Tried.** [`ajreynol:qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) (2026-01, 29 commits, "debug stats for
e-matching", an `AnalyzeEE` module, unmerged); [`ajreynol:debugDumpLemmas`](https://github.com/ajreynol/cvc5/tree/debugDumpLemmas) (2025,
`--re-check-lemmas`); [`ajreynol:termOrigin`](https://github.com/ajreynol/cvc5/tree/termOrigin) (2025, `--track-term-origins`: the
lemma-origin DAG, i.e. an instantiation graph); [`ajreynol:trackInferId`](https://github.com/ajreynol/cvc5/tree/trackInferId) (2024,
`--track-lemma-inference-ids`); [`ajreynol:uclHistogram`](https://github.com/ajreynol/cvc5/tree/uclHistogram), [`ajreynol:oclTimestamp`](https://github.com/ajreynol/cvc5/tree/oclTimestamp) (2024);
[`ajreynol:miscStats`](https://github.com/ajreynol/cvc5/tree/miscStats) (2023); [`ajreynol:dfcPp`](https://github.com/ajreynol/cvc5/tree/dfcPp) (2021, difficulty). Outside the fork, in
September 2026: BasisResearch/cvc5 fork PRs
[#3](https://github.com/BasisResearch/cvc5/pull/3),
[#4](https://github.com/BasisResearch/cvc5/pull/4), and
[#6](https://github.com/BasisResearch/cvc5/pull/6) add `(get-info
:matching-loops)`, `--inst-graph`, and `(get-info :inst-pressure)`;
BasisResearch/Verus fork PRs
[#20](https://github.com/BasisResearch/verus/pull/20),
[#21](https://github.com/BasisResearch/verus/pull/21), and
[#22](https://github.com/BasisResearch/verus/pull/22) add the corresponding
instantiation graph, `-V matching-loops`, and `-V inst-pressure` plumbing.
Those PRs are closed in the forks, not upstream cvc5/Verus, and were not
evaluated here.

**Elsewhere.** z3 `smt.qi.profile` (per-quantifier instances and cost),
`trace=true` with the Axiom Profiler and now SMTScope (z3-only, "~10x
faster"); Verus `--profile` / `--profile-all` reads the z3 log and ranks
quantifiers by cost times instances; F*'s `qprofdiff`. Mariposa measures
instability under semantics-preserving mutation; Cazamariposas localises it;
SHAKE prunes context for stability (29 % / 41 % on z3 and cvc5).

**Papers.** Becker, Müller and Summers, [*The Axiom Profiler: Understanding and
Debugging SMT Quantifier
Instantiations*](https://doi.org/10.1007/978-3-030-17462-0_6), TACAS 2019.
Fiala and Müller, [*SMTScope: Automated and Efficient Analysis of SMT
Traces*](https://doi.org/10.1007/978-3-032-22752-2_12), TACAS 2026. Zhou,
Bosamiya, Takashima, Li, Heule and Parno, [*Mariposa: Measuring SMT
Instability in Automated Program
Verification*](https://doi.org/10.34727/2023/isbn.978-3-85448-060-0_26), FMCAD
2023. Zhou, Shah, Lin, Heule and Parno, [*Cazamariposas: Automated Instability
Debugging in SMT-Based Program
Verification*](https://doi.org/10.1007/978-3-031-99984-0_5), CADE 2025. Zhou,
Bosamiya, Li, Heule and Parno, [*Context Pruning for More Robust SMT-based
Program Verification*](https://doi.org/10.34727/2024/isbn.978-3-85448-065-5_12),
FMCAD 2024. Amrollahi, Preiner, Niemetz, Reynolds, Charikar, Tinelli and
Barrett, [*Towards SMT Solver Stability via Input
Normalization*](https://doi.org/10.34727/2025/isbn.978-3-85448-084-6_14),
FMCAD 2025. Lattuada et al., [*Verus: Verifying Rust Programs using Linear
Ghost Types*](https://doi.org/10.1145/3586037), OOPSLA 2023.

**What would settle it.** Nothing; this direction is the instrument. Its
deliverable is the attribution table of goal 2, and the first version of it
needs only `--stats-internal` and `-o inst` on the gap set.

## R27 — SMT-LIB parser throughput: pay less before solving

**Effort.** 🟡 Medium Risk / 🟡 Medium Gain — lexer and term-construction changes are
contained in the front end, but its compliance and ownership surface is broad;
large generated inputs may benefit substantially, while parsing cannot explain
search-heavy timeouts unless measurement shows it consumes their budget.

*No row in the original notes. Added from the fork's parser-optimization branch.*

**The hypothesis.** Verus emits large, repetitive SMT-LIB files. Before cvc5
can make one SAT decision it must scan every byte, allocate token strings,
resolve every symbol, construct every API term, and execute declarations. That
fixed cost can be a material fraction of the 504 solved-but-slow cases and can
distort comparisons on fast solves. It is a different hypothesis from R20:
R27 is turning bytes into commands and terms; R20 begins after assertions exist.

**In cvc5 today `(code)`.** `FileInput` wraps a `std::ifstream`; the hand-written
`Lexer` reads non-interactive input through a 32 KiB buffer; `Smt2Lexer` appends
each token byte to a `std::vector<char>` and then adds a null terminator. The
command parser constructs a `std::map<std::string, Token>` and allocates a
`std::string` for command lookup. The iterative term parser grows parallel
context, term, and let-binder vectors and constructs API `Term`s as it reduces
the input. `--parse-only` skips solver commands other than definitions and is
the existing isolation tool. There is no parser-specific timer in
`--stats-internal`; parsing is visible only indirectly in total process time.

**Tried.** Upstream [PR #9723](https://github.com/cvc5/cvc5/pull/9723) removed
fields from `ParseOp` and redundant symbol-table lookups, reporting roughly a
10% parsing-time improvement in its initial tests. The subsequent hand-written
lexer ([PR #9720](https://github.com/cvc5/cvc5/pull/9720), enabled by
[PR #9759](https://github.com/cvc5/cvc5/pull/9759)) replaced the generated
front end. [`ajreynol:ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt)
(2026-03, two commits, unmerged) reserves parser stacks, uses `from_chars` for
indices, avoids front insertion into argument vectors, resolves most indexed
operators earlier, and changes command lookup to static tables over
`string_view`. It has not been measured on the set.

**Elsewhere `(code)`.** z3 also uses a hand-written
[SMT-LIB scanner and parser](https://github.com/Z3Prover/z3/tree/master/src/parsers/smt2),
so generated-parser overhead is not the differentiator it once was. cvc5's
lexer says it is partly based on
[Bitwuzla's SMT-LIB parser](https://github.com/bitwuzla/bitwuzla/tree/main/src/parser/smt2).
The useful comparison is therefore profiles, allocations, and bytes per second
on identical inputs, not parser architecture by name.

**Papers.** None specific to SMT-LIB parser throughput; the cvc5 pull requests
and the two solver front ends above are the relevant primary sources.

**What would settle it.** Time `--parse-only` on every benchmark and record file
bytes, token and term counts, peak memory, and parse-only time as a fraction of
end-to-end cvc5 time. Compare the same inputs with z3's front end, then A/B
[`ajreynol:ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt)
on the solved-but-slow slice. If parsing is not a
material share there, R27 leaves the top ten; if it is, a profile decides
whether lexing, symbol lookup, API term construction, or command execution is
the actual target.

---

# What to run first, as a prediction

The directions are not ranked by expected share of the gap — that is goal
2's job — but by what one run costs today. Everything in the first list is a
config change in [`job_launcher/configs/`](../../../job_launcher/configs/)
against the baseline; everything in the second is a `BRANCH=` build of a
fork branch; the third needs design work and is where the notes and the z3
code agree the structural difference lives.

**Parser measurement.** `--parse-only` on the set, then
[`ajreynol:ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt)
on the solved-but-slow slice (R27). This is cheap enough to reject before any
front-end design work.

**Flags on `main`, one run each.**

| run | direction | why first |
| --- | --- | --- |
| `--sat-solver=cadical` | R13 | the baseline ran MiniSat by accident of `--incremental`; the notes' best-known configuration had CaDiCaL |
| `--ee-mode=central` | R15 | one flag; the notes' direction 3 |
| `--preregister-mode=lazy` | R22 | one flag; the notes' `h-28` |
| `--inst-local`, then `--jh-rlv-order` | R10 | the merged half of the lemma-lifecycle work |
| `--term-db-mode=all` / `relevant` | R23 | brackets the current default |
| `--no-cegqi` | R8 | cegqi is auto-enabled and may cost rounds on unpatterned quantifiers |
| `--nl-ext=none` on the NIA subset | R18 | Verus runs z3 with nonlinear off |
| `--lemma-inprocess=light`, `--conflict-process=min` | R12 | the notes' experimental rows |
| `--dt-binary-split` | R16 | one flag |
| `--simplification=none`, `--no-static-learning` | R20 | the comment in `set_defaults.cpp` |
| `--ieval=off`, `--ieval=use-learn` | R7 | what entailment filtering costs here |
| `--user-pat=trust` alone; `--no-cbqi` alone | R5, R6 | the baseline measured them together |

**Fork branches, one build each.** [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) (R9/R10), [`ajreynol:ai-jhRlvInst`](https://github.com/ajreynol/cvc5/tree/ai-jhRlvInst)
(R10), [`ajreynol:dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant) (R16), [`ajreynol:ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc) (R17), [`ajreynol:ai-prepared13`](https://github.com/ajreynol/cvc5/tree/ai-prepared13) (R3),
[`ajreynol:preregRlv`](https://github.com/ajreynol/cvc5/tree/preregRlv) (R22), [`ajreynol:mbtc25`](https://github.com/ajreynol/cvc5/tree/mbtc25) (R14), [`ajreynol:dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3) (R15), [`ajreynol:deferBlock`](https://github.com/ajreynol/cvc5/tree/deferBlock)
(R9/R17), [`ajreynol:bitblastLc`](https://github.com/ajreynol/cvc5/tree/bitblastLc) (R19), and [`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) with its pacing limits
(R1) — the eager branch here with explicit per-round, pair, and generation
budgets — plus
[`ajreynol:ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt) (R27).

**Design work.** R1 with R2 and R9 together: eager, incremental,
forgetting. The notes' three attempts at R1 each ran into the absence of R9
("clauses are not deleted, can encounter infinite branch and bound, matching
loops"), and the z3 code says the three are one mechanism. It is the
expensive direction, and the attribution has to earn it.

---

# Sources

- The performance notes of 2026-09-14, as summarised in
  [`../notes.md`](../notes.md).
- cvc5 `main` at
  [`f294265`](https://github.com/cvc5/cvc5/commit/f294265c2b939a8e6cee8551f5a08afe5fb01efa)
  (2026-09-14): `src/options/*.toml`,
  `src/smt/set_defaults.cpp`, `src/theory/quantifiers/`, `src/prop/`,
  `src/theory/datatypes/`, `src/theory/arith/`, read 2026-09-15.
- z3 `master` at
  [`2d2fb04`](https://github.com/Z3Prover/z3/commit/2d2fb04fe3f1ab2111b550645f7c49198a3165f6)
  (2026-09-14): `src/smt/qi_queue.cpp`,
  `smt_quantifier.cpp`, `mam.cpp`, `smt_context.cpp`, `smt_relevancy.cpp`,
  `smt_case_split_queue.cpp`, `theory_datatype.cpp`, `theory_lra.cpp`,
  `theory_bv.cpp`, `smt_setup.cpp`, `src/params/*.pyg`,
  `src/math/lp/int_solver.cpp`, `dioph_eq.cpp`, `src/ast/pattern/`,
  `src/solver/assertions/asserted_formulas.cpp`, read 2026-09-15.
- The [`ajreynol/cvc5`](https://github.com/ajreynol/cvc5) fork, 847 remote
  branch refs excluding the symbolic
  remote `HEAD`, as fetched into the local checkout on 2026-08-26; commit
  subjects, tip dates, merge-base diffstats and option help text read
  2026-09-15. All 170 distinct branch URLs used here resolved to those refs,
  and their displayed names matched the URL targets. Feature status was
  checked semantically against pinned cvc5 source and upstream PR state, not
  inferred from Git ancestry.
- Verus at `a29e888` (2026-09-15),
  `source/air/src/context.rs` and `source/rust_verify/src/verifier.rs`; Dafny
  at `98ac8c0` (2026-08-31), `Source/DafnyCore/DafnyOptions.cs`; Boogie at
  `bb44ad3` (2026-08-20), `Source/Provers/SMTLib/Z3.cs`; F* at `c08d36a`
  (2026-09-14), `src/smtencoding/FStarC.SMTEncoding.Z3.fst`;
  z3 issues #1151, #7363; Dafny discussion #3362; Boogie issue #73.
- Papers as cited, verified against publisher or dblp pages on 2026-09-15;
  where a citation could not be verified the text says so.
