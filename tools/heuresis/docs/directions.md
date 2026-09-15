# Research directions: what would make cvc5 catch up to z3 on Verus-style quantified benchmarks

**Twenty-six directions, R1 to R26, each with the same four inventories:
the cvc5 flags that test it today, what has been tried, what z3 and others
do, and the papers.** Written 2026-09-15 from the performance notes
summarised in [`../notes.md`](../notes.md) (the `h-N` rows referenced below),
from cvc5 `main` at `f294265` and z3 `master` at `2d2fb04` read on that day,
from the 801 branches of the `ajreynol/CVC4` fork as fetched on 2026-08-26,
and from the literature. Directions are not mutually exclusive; several
are the same mechanism seen from different sides, and the grouping says
which.

*What this document is not.* It is not an attribution. No direction below
has been measured against the set; the only number the project owns is the
baseline ([ledger, 2026-09-14](../ledger/2026-09-14-baseline.md)): PAR2 ratio
4.34, gap set 1049 of 6124, 545 of them cvc5 timeouts on benchmarks z3 solves.
The inventories say what *could* be tested and how; goal 2 of the charter
decides what *is*. Where a claim about z3 or cvc5 rests on code read today it
says `(code)`; where on a paper, it cites; where on the notes, it names the
`h-` row; where on reasoning alone, it says so.

**Conventions.** A cvc5 flag is given as `--name` with its default in
brackets; `none` means the feature does not exist in cvc5. Fork branches are
named as on GitHub (`ajreynol/CVC4`, branch `NAME`); a branch marked *merged*
has no commits beyond `main`. "Best known" means the configuration under study,
`--no-cbqi --user-pat=strict`.

## The map

| group | directions | what they have in common |
| --- | --- | --- |
| A — when and how much to instantiate | R1–R8 | the instantiation policy: z3 instantiates *during* search and cheaply; cvc5 instantiates at full effort and completely |
| B — what happens to lemmas afterwards | R9–R13 | the lemma lifecycle and the SAT search around it: deletion, ordering, relevance, the SAT core |
| C — the ground engine | R14–R19 | theory combination, congruence closure, datatypes, arithmetic, bit-vectors |
| D — before the search | R20–R23 | preprocessing and what the search is made to look at |
| E — cross-cutting | R24–R26 | configuration, low-level engineering, and the instruments to attribute with |

The baseline says half the gap set is timeouts and half is solved-but-slow.
The reading in `notes.md` (*A reading of the register*) predicts that groups A
and B carry most of it. That is a prediction, and goal 2 exists to test it.

---

# Group A — when and how much to instantiate

The structural difference the notes name first (`h-16`, `h-18`), and the one
the z3 code confirms most sharply `(code)`: z3 turns an E-matching match into
a clause *during propagation* when its cost is below `smt.qi.eager_threshold`,
E-matches only terms that relevancy has marked, finds new matches
incrementally from a candidate queue fed by merges, and deletes the instance
clauses again on backtracking. cvc5 does none of these four things: it
instantiates only at `EFFORT_FULL`/`LAST_CALL` (and skips one round in three
by default, `--inst-when-phase=2`), rebuilds every trigger index from scratch
each round, enumerates every match a trigger has with no budget, and keeps
every instance forever (group B). R1–R4 are the four halves of that
difference; R5–R8 are the policies around it.

## R1 — Eager instantiation: instantiate during search, not only at full effort

*Rows `h-16`. Coupled to R2 (incrementality), R4 (budget), R9 (deletion).*

**The hypothesis.** A Verus proof obligation is a chain of trigger-driven
instantiations, each of which creates the ground terms that fire the next. z3
walks that chain inside unit propagation, with no SAT decision in between;
cvc5 must first let the SAT solver complete a propositional model, then runs
one E-matching round, then returns to the SAT solver. On a chain of depth *d*
that is *d* full checks against a growing clause set. The notes call this the
lack of eager instantiation and record three attempts.

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

**Tried.** Three generations of design in the fork, none on `main`.
Generation 1, `eagerCbqi` (2024-10, 204 commits): an "eager term database"
built on the instantiation evaluator that adds only conflicting,
unit-propagating or non-entailed instances eagerly (`--eager-inst-when=eqc|
eqc-delay|asserted|std-check`, `--eager-inst-mode=conflict|prop|unit-prop|…`,
`--eager-inst-trigger=narrow|all`, `--track-inst-level`,
`--inst-level-buffer=N`). Generation 2, `macrosEagerInst` →
`macroEagerInstMt` → `eagerInst3` (2024-09 to 2026-04, 1713 lines of
`eager_inst.cpp`): E-matching over a ground trie fed by master-engine
notifications, with `--eager-inst-term=eqc|eqc-merge|assert`,
`--eager-inst-quant=preregister|assert`, `--eager-inst-watch`,
`--eager-inst-simple` ("do not search modulo equality to match operators"),
`--eager-inst-macro-only`, `--eager-inst-gcong`, and `--defer-block`; it
ships `verus-16s.smt2` and `verus-mim-40s.smt2` as regressions;
`ai-extEagerInst3-1` adds auto-triggers on top. Generation 3, restarted
in 2026-04: `ai-eagerInst1` (a skeleton), `ai-eagerInst2` ("a small
incremental term database that is populated only from notification events
… a lightweight eager matcher for user-provided patterns"), and
`claude-eagerInst` (2026-06, 939 lines): per-operator context-dependent term
lists with a cursor per trigger, merge-driven re-matching through a parent
index, and — alone among the three generations — pacing:
`--eager-inst-limit=N` (instances per round), `--eager-inst-gen-limit=N`
("do not eagerly match terms whose generation … is N or more", default 1),
`--eager-inst-pair-limit=N` ("this paces eager instantiation so that the
SAT solver makes progress between rounds", default 2000), and
`--eager-inst-rlv` ("defer eager matching of terms in singleton equivalence
classes until they participate in a merge; this approximates relevancy").
Also `eagerQM` (2025, a preprocessing-time matching pass) and
`instFullPreempt` (2024, `--inst-when=full-preempt`). The notes' verdict on
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

**Papers.** de Moura and Bjørner, *Efficient E-Matching for SMT Solvers*,
CADE 2007 — the eager/lazy split, the promotion of useful quantifiers to eager
instantiation, and "Deleting clauses". Detlefs, Nelson and Saxe, *Simplify: a
theorem prover for program checking*, J. ACM 52(3), 2005. Hoenicke and
Schindler, *Incremental Search for Conflict and Unit Instances of Quantified
Formulas with E-Matching*, VMCAI 2021. Ge, Barrett and Tinelli, *Solving
Quantified Verification Conditions Using Satisfiability Modulo Theories*,
CADE 2007. Bjørner, *Z3 Internals*, §7.1.5–7.1.6.

**What would settle it.** The attribution first: on the gap set, the number of
full-effort rounds per benchmark (`QuantifiersEngine::Rounds_Instantiation_Full`)
against z3's instance generation depth; if cvc5's rounds track z3's depth,
the cost is rounds, and R1 is the direction. Then the cheapest existing
branch against the set, with R9 in place, because without deletion eager
instantiation drowns.

## R2 — Incremental E-matching: match what changed, not everything

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

**Tried.** `ai-emFilter` (2026-04, `--filter-e-matching` "conservatively
filter quantified formulas from E-matching": an `EMatchingFilter` that
snapshots master-engine events and marks triggers dirty by match operator,
with a last-call backstop; the author's note reads "Probably too
aggressive"); `imTrivial` (2025-10, `InstMatchGeneratorTrivial` for
triggers `f(x1..xn)` with distinct variables that "only subsequently
considers terms that have not yet been considered … avoids repeated calls to
matching, and in particular entailment checking"); `imSimpleInc`,
`imSimpleInc2` (the same for `InstMatchGeneratorSimple`); `quantCgInc` (an
incremental candidate generator, last commit "Try, broken"); `ai-imgDirect`
(2026-03, a direct matcher for nested single triggers such as `f(g(x))`
that can exclude failed root candidates for the round); `ai-quantOpt-1`
(candidate caching per pattern arity); `emExp` (2025, records the context
level at which each term entered the database); `emStratify` (2023,
`--e-matching-stratify-ieval`); `emFailMasks` (2022,
`--inst-track-fail-masks`); `fixEm` (merged). None on `main`.

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

**Papers.** de Moura and Bjørner CADE 2007 (code trees, inverted path index,
"the practical overhead ... is searching and maintaining sets of patterns
that can efficiently retrieve new matches as soon as E-graph operations
introduce them"). Simplify J. ACM 2005, §5 (mod-time, pattern-element).
Moskal, Łopuszański and Kiniry, *E-matching for Fun and Profit*, SMT 2007 /
ENTCS 198(2), 2008. Barbosa, *New techniques for instantiation and proof
production in SMT solving*, PhD thesis 2017. Bjørner, *Z3 Internals*
§7.1.2–7.1.3.

**What would settle it.** `theory::QuantifiersEngine::time_ematching` as a
fraction of solve time on the gap set, and the ratio of matches found to
matches re-found (a counter to add). If E-matching time is small, R2 is not
where the gap is, whatever z3 does.

## R3 — Worst-case E-matching: failure caching and early pruning

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
is already entailed (counter `Instantiate::Duplicate_Inst_Ent`). The
evaluator is reset each round (`resetAll`). `--multi-trigger-linear` [`true`]
bounds multi-trigger instances linearly in the number of ground terms.

**Tried.** `ai-prepared13` (2026-06, unmerged): `getNextMatch` returns a
distinguished failure "for reasons that are invariant modulo the current
equality engine", keyed by the representative being matched, the
representatives of the continuation generators and the partial match, and
caches it for the round; its regressions are Verus worst cases
(`prepared_13`, `ironkv … delegation_map`, `verismo … range_set`).
`instEval` (2022, merged as `--ieval`); `cacheEntCheck` (2021);
`ai-imgDirect` (R2).

**Elsewhere `(code)`.** z3 bounds the same problem differently: fingerprints
(`smt/fingerprints.h`) reject a (quantifier, root bindings) tuple already seen
in the current scope; `smt_checker::is_sat` discards an instance whose body
is already true before it becomes a clause; label filters reject most
candidates in constant time; and the eager/lazy cost split (R1) is itself the
budget. veriT's CCFV frames E-matching as E-ground (dis)unification with its
own pruning.

**Papers.** Barbosa, Fontaine and Reynolds, *Congruence Closure with Free
Variables*, TACAS 2017. Bansal, Reynolds, King, Barrett and Wies, *Deciding
Local Theory Extensions via E-matching*, CAV 2015. No paper on cvc5's
instantiation evaluator exists; PR #9092 is the reference.

**What would settle it.** The distribution of E-matching time per round on the
gap set: a heavy tail on few benchmarks is R3, a uniform cost is R2.

## R4 — Instantiation budgeting: how many instances per round, and which

*Rows `h-19`. z3's cost function is the mechanism; cvc5 has none.*

**The hypothesis.** cvc5 sends every match of every trigger every round. z3
sends the cheap ones now, the expensive ones at final check, and the very
expensive ones never. A budget — per round, per trigger, per ground term, or
by generation — would keep the clause set small (R9) and the SAT search short,
at the price of completeness that the Verus workload does not need (all unsat,
all trigger-driven).

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

**Tried.** `termOrigin` (2025-04, unmerged): `--inst-nested-max-level=N`
"maximum nested instantiation level of terms used to instantiate quantified
formulas" and `--track-term-origins`, a lemma-origin DAG over terms — the
closest cvc5 has come to z3's generation. `eagerCbqi`'s
`--inst-level-buffer=N` ("maximum inst level of terms in proportion to the
number of full effort checks") and `claude-eagerInst`'s three limits (R1)
are budgets inside eager instantiation. `instLastCallDelay` (2026-03: skip
the last-call check while the valuation still needs one),
`instFullPreempt` (2024), `dtInstMode` (2020), `carryInst` (2021). Nothing
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

**Papers.** CADE 2007 (priority queues, promotion/demotion). Bjørner, *Z3
Internals* §7.1.6. Jakubův, Janota, Piepenbrock and Urban, *Machine Learning
for Quantifier Selection in cvc5*, ECAI 2024 (learned selection, a budget of
a different kind).

**What would settle it.** Instances per round and total instances on the gap
set versus z3's `smt.qi.profile` counts on the same benchmarks. If cvc5 makes
an order of magnitude more instances to reach the same refutation, R4 (with
R9) is the direction; if the counts are similar, the cost is elsewhere.

## R5 — Trigger selection: strict user patterns, multi-triggers, and what strictness disables

*Rows in the notes: `--user-pat=strict` under "things that helped".*

**The hypothesis.** Verus supplies a trigger for every quantifier and designs
them for z3's semantics: user patterns only, no inferred ones, matching loops
avoided by construction. cvc5's default `trust` already uses only user
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

**Tried.** `multiTriggerSingleBase` (2024, "using single trigger as a base
for multi triggers"); `nestedTriggers2` (2022, `--nested-triggers` "generate
triggers based on terms in nested quantifiers"), `nestedTriggers` (2023,
"another attempt"); `simpleTriggerMore` (2023); `gttOpt` (2021,
`--gt-trigger-reg` register ground subterms of triggers); `userTriggerOut2`
(merged: user triggers distinguished in `-o trigger`); `eagerCbqi`'s
`--eager-inst-trigger=narrow` ("use the most constrained trigger") and
`--eager-inst-merge-triggers` ("combine triggers that are equivalent modulo
ground subterms"). All stale except the merged output change.

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

**Papers.** Leino and Pit-Claudel, *Trigger Selection Strategies to Stabilize
Program Verifiers*, CAV 2016. Moskal, *Programming with Triggers*, SMT 2009.
Dross, Conchon, Kanig and Paskevich, *Adding Decision Procedures to SMT
Solvers Using Axioms with Triggers*, JAR 56(4), 2016. Bugariu,
Ter-Gabrielyan and Müller, *Identifying Overly Restrictive Matching Patterns
in SMT-based Program Verifiers*, FM 2021. Ge, Garcia and Summers, *A Formal
Model to Prove Instantiation Termination for E-matching-Based
Axiomatisations*, CAV 2024.

**What would settle it.** `-o trigger` on the gap set: how many quantifiers
have no user pattern (and so get auto-triggers), how many multi-triggers
there are, and an A/B of `trust` vs `strict` alone (the baseline measured
`strict` and `--no-cbqi` together).

## R6 — Conflict-based instantiation: off for this domain, and why that is right or wrong

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

**Tried.** `ai-cbqi-0423` (2026-04, unmerged): a rework of
`quant_conflict_find.cpp` for the case where "large flattened UF encodings,
e.g. graph-preservation constraints, tend to force QCF into an exhaustive
search over auxiliary function applications while other quantifier modules
return quickly" — the `mu_test.smt2` case of the notes. `safeOpts-0305`
(merged: `--cbqi` promoted to a common option); `refactorQcf` (2022),
`qcfClean` (2021); `cbqiDev`, `cbqiImp-v2` (2018, a different "cbqi":
counterexample-guided for bit-vectors).

**Elsewhere `(code)`.** z3 has no conflict-based instantiation module; its
analogues are `qi.promote_unsat` (an instance that `smt_checker::is_unsat`
shows falsified jumps the eager queue) and `smt.qi.quick_checker` (off by
default; mode 2 is warned against in code as "too expensive"). SMTInterpol's
E-matching theory finds conflict and unit instances directly.

**Papers.** Reynolds, Tinelli and de Moura, *Finding Conflicting Instances of
Quantified Formulas in SMT*, FMCAD 2014. Hoenicke and Schindler VMCAI 2021.

**What would settle it.** The baseline already has `--no-cbqi` bundled with
`--user-pat=strict`; an A/B of each alone says what cbqi costs here.

## R7 — Entailment filtering of instances: what ieval buys and costs

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
`Duplicate_Inst_Eq`, `Duplicate_Inst_Ent`.

**Tried.** `instEval` (2022, merged as `--ieval`); `eagerCbqi` extends the
evaluator for eager use (R1); `fmfIeval` (2022), `ievalTravTrie` (2023),
`emStratify` (2023), `cacheEntCheck` (2021); all stale.

**Elsewhere `(code)`.** z3's `smt_checker::is_sat` before internalising an
instance is the same test at the same point; fingerprints are the duplicate
filter.

**Papers.** None on ieval (PR #9092). Hoenicke and Schindler VMCAI 2021 is the
closest published analogue.

**What would settle it.** `Duplicate_Inst_Ent` over `Instantiations_Total` on
the gap set, and an A/B of `--ieval=off`, `--ieval=use-learn`,
`--no-inst-no-entail`.

## R8 — The fallbacks: enumerative instantiation, MBQI, finite model finding

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

**Tried.** `enumInstOpts` (2022, merged: the `--enum-inst*` family);
`mbqiEnumChoice`, `mbqiEnumChoice2` (2025, mostly merged: choice grammars
for fast enumeration in MBQI), `mbqiHoDev` (2024); `fmfCollectModelValue`
(2025); `quantVirtualModel` (2019, `--quant-vmodel`). Nothing about turning
cegqi off for this domain.

**Elsewhere `(code)`.** z3 with `smt.mbqi=false` answers unknown when the
SAT branch is satisfied and quantifiers remain (`m_last_search_failure =
QUANTIFIERS`), which is exactly right for benchmarks known unsat. Dafny, F*
and Boogie set the same. `auto_config=true` would force `mbqi=true`.

**Papers.** Reynolds, Barbosa and Fontaine, *Revisiting Enumerative
Instantiation*, TACAS 2018. Janota, Barbosa, Fontaine and Reynolds, *Fair and
Adventurous Enumeration of Quantifier Instantiations*, FMCAD 2021. Ge and de
Moura, *Complete Instantiation for Quantified Formulas in Satisfiabiliby
[sic] Modulo Theories*, CAV 2009. Reynolds, Tinelli, Goel and Krstić,
*Finite Model Finding in SMT*, CAV 2013. Dančo, Hozzová and Janota, *From
MBQI to Enumerative Instantiation and Back*, SMT 2025.

**What would settle it.** `-o inst-strategy` on the gap set to see whether
cegqi ever fires; an A/B of `--no-cegqi` and of `--enum-inst` on the 545
timeouts.

---

# Group B — what happens to lemmas afterwards

Downstream of group A. A solver that instantiates eagerly must forget; one
that keeps everything must at least decide on it in a sensible order and keep
the SAT core from drowning. The code says cvc5 keeps everything `(code)`:
`LemmaProperty::REMOVABLE` is declared and never set by any theory, MiniSat's
`reduceDB` touches only `clauses_removable`, and the CaDiCaL propagator hands
every theory lemma over as irredundant. z3 deletes every instance clause on
backtracking and only keeps what conflicts taught it.

## R9 — Deleting instantiation lemmas: garbage collection, or scoping them to the branch

*Rows `h-1`. The mirror of R1.*

**The hypothesis.** After a few hundred rounds the clause database is
dominated by instances that mattered on some abandoned branch. Every unit
propagation, every justification pass and every decision pays for them. z3
throws them away and pays to re-derive; cvc5 keeps them and pays to carry
them. On this workload, where z3 wins, forgetting is the better trade.

**In cvc5 today `(code)`.** `--inst-local` [`false`] (PR #12121, from the fork's
`instVolatile`): instantiation lemmas are local to the SAT context, dropped on
backtrack, and re-derived if needed — `LemmaProperty::LOCAL`. Otherwise
`Instantiate::addInstantiation` sends `LemmaProperty::INPROCESS`, never
`REMOVABLE`. MiniSat: `clauses_persistent` are exempt from `reduceDB`;
CaDiCaL: `add_clause(clause, forgettable=false)`; the only forgettable
clauses in the whole propagator are two tautology "pacifiers". The catch that
makes a one-line `REMOVABLE` experiment unsound: cvc5 caches sent instances
in `inst_match_trie` for the whole user context, so a clause the SAT solver
forgot would never be re-sent. z3 scopes its fingerprint set for exactly this
reason. Deletion therefore needs a deletion *notification* back to the
quantifiers module, which is what the fork's `satNotify` / `notifySatClause`
branches built.

**Tried.** `virtualLemma` (2021, `--virtual-inst` "mark instantiations as
virtual clauses") and `virtualClauseDel` (2021) — the first design;
`instVolatile` (2025, merged as `--inst-local`); `ai-instDefer` (2026,
`--inst-defer`: "instantiations are recorded globally (never re-derived) but
are treated like local assertions in the justification heuristic; a variant
of inst-local that avoids re-deriving instantiations after backtracking");
`isActiveLemma` (2023, `--track-relevant-literals`); `deferBlock` (2025,
`--defer-block` with `--defer-block-mode=subsolve|delay`, a theory-engine
module that holds lemmas back, with arithmetic branch-and-bound hooks);
`smtLazyAssert` (2022); `satNotify`, `notifySatClause` (the deletion
callback). None but `--inst-local` is on `main`; `--inst-local` has not been
measured on the set.

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

**Papers.** de Moura and Bjørner CADE 2007. Audemard and Simon, *Predicting
Learnt Clauses Quality in Modern SAT Solvers*, IJCAI 2009 (LBD). Fazekas,
Biere and Scholl, *Incremental Inprocessing in SAT Solving*, SAT 2019.

**What would settle it.** Clause-database size against time on the ten worst
(MiniSat's `clauses_persistent` count is one added statistic away), and the
fraction of instance clauses that are ever used in a conflict. Then
`--inst-local` on the set, then `--inst-defer`. A true GC needs the
notification plumbing first.

## R10 — Where instance lemmas sit in the decision order: local, deferred, gated

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
skolem-definition machinery that `ai-jhRlvInst` generalises to instances;
`--decision` [`justification`] for any quantified logic (R11).

**Tried.** `ai-instDefer` (`--inst-defer`, above) and `claudeDev-dts-idef`
(`--inst-defer` with `--dt-split-relevant`, "taking both ideas");
`ai-jhRlvInst` (`--jh-rlv-inst`: "dynamically activate instantiation lemmas
based on whether their associated quantified formula is asserted, analogous
to skolem definitions"; the notes expect low impact since it only matters for
quantifiers that are not top-level); `ai-jhConflictFirst` (`--jh-conflict-first`:
"prioritize conflict clauses over theory lemmas in the decision justification
heuristic"); `instLastCallDelay` (skip the last-call check while the
valuation still needs a check); `termOrigin` (`--inst-nested-max-level=N`,
`--track-term-origins`: a lemma-origin DAG over terms, i.e. z3's generation);
`instFullPreempt` (2024, `--inst-when=full-preempt`: instantiate before
theory combination and before other theories have checked). All active or
unmerged; none measured on the set.

**Elsewhere `(code)`.** z3 `smt.case_split` [1] = `CS_ACTIVITY_DELAY_NEW`:
`dact_case_split_queue` keeps Boolean variables created while searching in a
second heap consulted only when the main one is exhausted, so "the atoms
introduced by instance clauses do not immediately hijack the decision order".
Verus sets `case_split=3`, relevancy-driven structural splitting (Dafny's
discussion #3362 calls this avoiding "time travelling triggers"). Instances
also carry a generation, and the cost function reads it (R4).

**Papers.** de Moura and Bjørner, *Relevancy Propagation*, MSR-TR-2007-140.
Barrett, Dill and Stump, *Checking Satisfiability of First-Order Formulas by
Incremental Translation to SAT*, CAV 2002 (the justification idea).

**What would settle it.** `--inst-local` and `--inst-defer` on the set are two
runs; `--jh-rlv-order` is a third. The decision count per benchmark
(`prop::decisions`) before and after says whether the heuristic was the cost.

## R11 — Decision heuristic versus relevancy: what the SAT solver is made to decide on

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

**Tried.** `preregRlv` (2024–2026, 155 commits, PR #9503:
`--preregister-mode=rlv` "Preregister literals when they become relevant";
`RelevantPreregistrar`: "we want to preregister only the literals that, if
they were to be T-propagated, could contribute towards a SAT conflict in the
current context"; polarity-aware relevance over inputs and lemmas);
`satRlv` (2022, 294 commits, `--sat-rlv=none|asserts|all` "use relevancy to
filter all calls, including asserts and preregisters" — the notes call it
broken); `satRlvTppSolver`; `jh-new` (2021, merged: the current
justification heuristic); `jhRandom` (2026, `--jh-rand`: randomised
assertion and branch order); `decEngineReqPhase`, `propOrderInput`.

**Elsewhere `(code)`.** z3 `smt.relevancy` [2]: `context::assign_core` queues
an atom for theory propagation only if `is_relevant_core(l)`;
`context::relevant_eh` is where quantifiers are asserted, where theories get
`relevant_eh` for lazy axioms (datatype accessors, `bv2int`), and where the
matcher gets its candidates; relevancy is structure-aware (`or`: one true
child; `ite`: the taken branch) and fully backtrackable. `smt.case_split`
modes 3–5 are relevancy-based and refused when `auto_config` is on.
`smt.phase_selection` [3, caching conservative]. Simplify's relevancy is the
ancestor; F* sets `smt.relevancy=2` explicitly.

**Papers.** MSR-TR-2007-140. Barrett, Dill and Stump CAV 2002. Goel, Krstić
and Fuchs, *Deciding array formulas with frugal axiom instantiation*, SMT
2008.

**What would settle it.** `--preregister-mode=lazy` and `--decision=internal`
on the set are two cheap runs; `preregRlv` is a build. The measurement that
matters is how many theory facts and matched terms the run touches, not the
decision count.

## R12 — Lemma inprocessing and conflict minimisation

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
inprocessing produces untrusted proof nodes and is incompatible with
`--deep-restart`. Implementation `prop/lemma_inprocess.cpp`,
`prop/zero_level_learner.cpp`.

**Tried.** Developed upstream; no fork branch. Adjacent: `subConflict` (2024,
`--sub-conflict-find` with a subsolver, `--sub-conflict-last-call`,
`--sub-conflict-tlem`), unmerged.

**Elsewhere `(code)`.** z3 has no lemma inprocessing as such, but
`qi_queue::instantiate` runs the instance through `m_context.get_rewriter()`
before internalising it, which is the light form; learned-clause
minimisation is the SAT-level standard.

**Papers.** Sörensson and Biere, *Minimizing Learned Clauses*, SAT 2009.
Fleury and Biere, *Efficient All-UIP Learned Clause Minimization*, SAT 2021.
Fazekas, Biere and Scholl SAT 2019. No paper on cvc5's inprocessing.

**What would settle it.** Two runs: `--lemma-inprocess=light` and
`--conflict-process=min`, with the average lemma size before and after.

## R13 — The SAT backend: CaDiCaL, MiniSat, restarts, units

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

**Tried.** `cadicalDefault` (2026-08, merged: CaDiCaL the common default,
MiniSat kept for incremental); `cadicalPortfolio` (2026, unmerged);
`alfCadical` (SAT proofs). Nothing on restart or phase policy under
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
*IPASIR-UP: User Propagators for CDCL*, SAT 2023. Biere, Faller, Fazekas,
Fleury, Froleyks and Pollitt, *CaDiCaL 2.0*, CAV 2024. Bjørner, Eisenhofer
and Kovács, *Satisfiability Modulo Custom Theories in Z3*, VMCAI 2023.
Pipatsrisawat and Darwiche, *A Lightweight Component Caching Scheme for
Satisfiability Solvers*, SAT 2007 (phase saving).

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

**Tried.** `mbtc25` (2026-01, 29 commits, PR #12095: `--tc-mode=model-based`
"Use model-based theory combination": build a model, find congruent but
unmerged applications, split on their unequal arguments; status "30 failures
only"); `mbtc2` (2019); `noHoApplyCg` (partly merged); `sharedSolverCentral`
(2021); `arraysStdCg` (2022). The notes: model-based is much simpler, usually
comparable, worse on some logics such as QF_ABV.

**Elsewhere `(code)`.** z3: `theory::assume_eqs` hashes theory variables by
model value and calls `context::assume_eq` for collisions; the new equality
atom gets `set_true_first_flag`, so the SAT solver tries it true first —
that phase bias is the "model-based" part. `theory_lra` runs `random_update`
before `assume_eqs` to break value ties. Ground subterms of triggers are
treated as shared terms (`mam_impl::m_shared_enodes`).

**Papers.** de Moura and Bjørner, *Model-based Theory Combination*, SMT 2007 /
ENTCS 198(2), 2008. Krstić and Goel, *Architecting Solvers for SAT Modulo
Theories: Nelson–Oppen with DPLL*, FroCoS 2007. Jovanović and Barrett,
*Sharing Is Caring: Combination of Theories*, FroCoS 2011 (care graphs).
Barrett, Nieuwenhuis, Oliveras and Tinelli, *Splitting on Demand in SAT
Modulo Theories*, LPAR 2006. Bruttomesso, Cimatti, Franzén, Griggio and
Sebastiani, *Delayed Theory Combination vs. Nelson–Oppen for SMT*, LPAR 2006.

**What would settle it.** The number of care-graph splits per benchmark
(`theory::CombinationCareGraph` statistics) on the gap set; then the PR's
branch as a build.

## R15 — Equality engine architecture: central, distributed, and who gets told what

*Rows `h-20`, `h-22`.*

**The hypothesis.** cvc5's distributed mode gives each theory its own
congruence closure, and shared equalities are propagated between them; every
merge costs a notification per interested party. z3 has one egraph and a list
of theory variables per class. The notes' `dtMergeNotify` line — merging UF
and datatypes into one engine, at the price of making datatypes a
second-class theory — is a step toward z3's arrangement.

**In cvc5 today `(code)`.** `--ee-mode` [`distributed`] (`central`: all
applicable theories use the central engine; auto-enables
`--arith-eq-solver`). Notifications: `eqNotifyTriggerPredicate`,
`eqNotifyTriggerTermEquality`, `eqNotifyConstantTermMerge`,
`eqNotifyNewClass`, `eqNotifyMerge`, `eqNotifyDisequal`; the quantifiers
engine hooks the master engine (`MasterNotifyClass`) and marks relevance on
merge (R23). PR #9724 (notifications only when the caller has been used) is
the notes' low-level optimisation; whether it landed is not stated.

**Tried.** `centralEe`, `centralEeDev` (2021, merged: `--ee-mode=central`);
`dtMergeNotify`, `-v2`, `-v3` (2026-05, active: datatypes under the central
engine without `notifyFact`, pending inferences valid in the SAT context,
`Theory::getFactTheory`, regressions named `central-ee-verus-prereg` and
`central-ee-splinterdb-*`); `dtEecNotDone` (merged); `ai-eecFixes-0430`,
`ai-eecNoShare` (skip `propagateSharedEquality` for theories fully explained
by the central engine); `cdno` (2025, context-dynamic notify objects);
`minorOpt-0516`; `noEeLinear` (2023); `perfDataStructures` (2018),
`lowLevelOptMore` (2019).

**Elsewhere `(code)`.** z3: `context::add_eq` merges once, calls
`m_qmanager->add_eq_eh` (the matcher's label union and parent-index walk,
typically the dominant cost) and then `merge_theory_vars`, whose fast path
is "r2 and r1 have at most one theory var"; theories may opt out of
disequality notifications (`use_diseqs`). One merge, one notification per
theory variable on the roots.

**Papers.** Nieuwenhuis and Oliveras, *Fast congruence closure and
extensions*, Inf. Comput. 205(4), 2007. de Moura and Bjørner, *Z3: An
Efficient SMT Solver*, TACAS 2008. Nelson and Oppen, *Fast Decision
Procedures Based on Congruence Closure*, J. ACM 27(2), 1980. Barbosa et al.,
*cvc5: A Versatile and Industrial-Strength SMT Solver*, TACAS 2022.

**What would settle it.** `--ee-mode=central` on the set is one run and
exists today; the `dtMergeNotify-v3` branch is a build. A profile of the ten
worst says what fraction of time is in the equality engines at all.

## R16 — Datatypes: when to split, on what, and whether to have them at all

*Rows `h-23`, `h-24`.*

**The hypothesis.** Verus encodes Rust types as datatypes (`Poly` boxing,
`Option`, records), so every benchmark has datatype terms in the thousands,
nearly all of which never need a constructor decision. cvc5 considers every
datatype equivalence class for splitting; z3 splits infinite datatypes only
at final check, and only after relevancy has had its say, with the phase
biased to the non-recursive constructor. Two of the fork's most recent
branches, and one merged change from `verusDev`, are about exactly this.

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

**Tried.** `dtSplitRelevant` (2026-06, `--dt-split-relevant` "only add
splitting lemmas for datatype terms that occur in asserted literals");
`dtRlvSplit` (2025-11, partly merged, reworked into `verusDev`'s "No split
infinite"); `dtElim` (2025-10, 26 commits, `--dt-elim` "eliminate datatypes
at preprocessing", policies by constructor and field count, "Switch to
1-cons"); `oneConsInst` (single-constructor terms instantiated directly);
`dtLazyInst`, `-2`, `-3` (2020–22, `--dt-lazy-inst` "apply the datatypes
instantiate rule lazily"); `oneConsSkipTester` (2023); `dtMergeNotify-v3`
(R15). The notes credit an assistant's review with the relevant-split idea
independently, and record Kartik's suggestion of a more liberal variant.

**Elsewhere `(code)`.** z3 `smt.dt_lazy_splits` [1]: finite datatypes split
eagerly at `mk_var`, infinite ones only in `final_check_eh`; `mk_split`
first marks an existing recognizer relevant rather than deciding, prefers
the non-recursive constructor and sets `true_first`; accessor axioms are
asserted straight into the egraph when the constructor is known; the occurs
check runs at final check as a DFS. Vampire's approach to datatypes is
axiomatic (Kovács, Robillard and Voronkov).

**Papers.** Barrett, Shikanian and Tinelli, *An Abstract Decision Procedure
for a Theory of Inductive Data Types*, JSAT 3, 2007. Reynolds and Blanchette,
*A Decision Procedure for (Co)datatypes in SMT Solvers*, JAR 58(3), 2017.
Reynolds, Viswanathan, Barbosa, Tinelli and Barrett, *Datatypes with Shared
Selectors*, IJCAR 2018. Kovács, Robillard and Voronkov, *Coming to Terms with
Quantified Reasoning*, POPL 2017. Hojjat and Rümmer, *Deciding and
Interpolating Algebraic Data Types by Reduction*, 2018.

**What would settle it.** `DATATYPES_SPLIT` lemma counts on the gap set (from
`--stats-internal`), then `--dt-binary-split` as a run and `dtSplitRelevant`
as a build.

## R17 — Linear integer arithmetic: branch and bound, cuts, and the Diophantine solver

*Rows `h-9`, `h-10`, `h-11`, `h-12`.*

**The hypothesis.** Verus arithmetic is mostly bounds and clipping
(`nClip`, `uClip`) over integers that are otherwise uninterpreted; cvc5's
integer solver runs its Diophantine solver and branch-and-bound at every full
check and can branch forever, while z3 does all integer reasoning at final
check, delegates a branch to the SAT solver as an atom, and periodises the
expensive handlers with randomised gates.

**In cvc5 today `(code)`.** `--arith-brab` [`true`], `--dio-solver` [`true`;
off only for quantifier-free nonlinear logics], `--dio-turns` [`10`],
`--rr-turns` [`3`], `--dio-decomps` [`false`], `--cut-all-bounded`
[`false`], `--maxCutsInContext` [`65535`], `--arith-eq-solver` [`false`],
`--use-approx` [`false`; GLPK], `--miplib-trick` [`false`],
`--arith-static-learning` [`true`], `--unate-lemmas` [`all`], `--arith-prop`
[`both`], `--new-prop` [`true`], `--replay-*`; pivot heuristics are tuned only
for pure quantifier-free arithmetic; `--arith-rewrite-equalities` off for
these logics.

**Tried.** `deferBlock` (2025, `--defer-block`, branch-and-bound deferral
hooks "BB only"; the notes: block or delay the lemmas); `ai-dioLc` (2026-06,
`--dio-solver-last-call` "defer Diophantine equation solver conflict
detection to last call effort, instead of running it at every full effort
check"); cvc5 PR #12178 (Daniel Larraz: DIO handles nonlinear monomials;
disabled it for quantifier-free nonlinear logics); `liaSplitDelay` (2023);
`linearSolverSub` (2024, `--arith-sub-solver`); `limitArith` (2024);
`elimArith`, `elimArithU`, `noArith` (2024, the notes' inconclusive
elimination experiment); `learnBranchIte`; `eqstatusLinear`.

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

**Papers.** Dutertre and de Moura, *A Fast Linear-Arithmetic Solver for
DPLL(T)*, CAV 2006. Jovanović and de Moura, *Cutting to the Chase: Solving
Linear Integer Arithmetic*, CADE 2011 / JAR 51(1), 2013. Griggio, *A
Practical Approach to Satisfiability Modulo Linear Integer Arithmetic*, JSAT
8, 2012. Dillig, Dillig and Aiken, *Cuts from Proofs*, CAV 2009. King,
*Effective Algorithms for the Satisfiability of Quantifier-Free Formulas Over
Linear Real and Integer Arithmetic*, PhD thesis, NYU 2014. King, Barrett and
Tinelli, *Leveraging Linear and Mixed Integer Programming for SMT*, FMCAD
2014. Bromberger and Weidenbach, *New techniques for linear arithmetic:
cubes and equalities*, FMSD 51(3), 2017.

**What would settle it.** Branch-and-bound and DIO lemma counts per benchmark
on the gap set; `ai-dioLc` as a build; `--no-dio-solver` as a run.

## R18 — Nonlinear arithmetic: off, light, or lazy

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

**Tried.** `arithFlattenCollect2` (2025, merged: the AC flattening of the
notes' `h-13`, "very incomplete"); `nlEnums` (merged); `nlAlwaysCheck`
(2022); `simpleNonzeroFactor` (2023); `nlExtTplaneLimit`, `nlExtTplanesDef`
(2018). No branch named `arithFlattenEq` exists in the fork; the notes' link
is stale.

**Elsewhere `(code)`.** z3: `smt.arith.nl=false` is read only by the legacy
solver (`theory_arith_nl.h`), which is the one Verus selects, so for Verus's
default queries nonlinear reasoning is off entirely; with the lra solver the
`nla` core runs only when a *relevant* monomial exists
(`core::has_relevant_monomial`), gated by `arith.nl.delay` [10] final checks,
and monomials stay as egraph terms and tableau columns regardless. Verus
switches to `smt.arith.solver=6` for `by(nonlinear_arith)` queries.

**Papers.** Cimatti, Griggio, Irfan, Roveri and Sebastiani, *Incremental
Linearization for Satisfiability and Verification Modulo Nonlinear Arithmetic
and Transcendental Functions*, TOCL 19(3), 2018. Reynolds, Tinelli, Jovanović
and Barrett, *Designing Theory Solvers with Extensions*, FroCoS 2017.
Jovanović and de Moura, *Solving Non-linear Arithmetic*, IJCAR 2012. Kremer,
Reynolds, Barrett and Tinelli, *Cooperating Techniques for Solving Nonlinear
Real Arithmetic in the cvc5 SMT Solver*, IJCAR 2022.

**What would settle it.** The gap set split by logic (the results files carry
the path, and the path carries the logic); then `--nl-ext=none` and
`--nl-ext=light` on the NIA subset. If cvc5 answers unsat as often with
nonlinear off, the extension was pure cost here.

## R19 — Bit-vectors inside quantified problems

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

**Tried.** `bitblastLc` (2025, `--bitblast-lc` "delay to last call for
bitblasting"); `bvToIntQuant-031126` (2026, int-blasting under quantified
`bv2nat`); `bvVElim`, `bbOpt`, `bvLimitRec`, `disableFlattenAssoc` (2025);
`ufConvRlv` (2023, reduce only relevant terms in the UF conversion solver);
`bvBbExtf` (2017, lazy blasting of expensive operators).

**Elsewhere `(code)`.** z3 `smt/theory_bv.cpp`: every bit-vector term is
blasted at internalisation (`init_bits`, one Boolean per bit); no lazy mode
in the smt kernel (`bv.delay` is read only by the new euf solver);
`bv.reflect` [true] keeps bit-vector terms as egraph nodes with visible
arguments so triggers over them fire; relevancy stays at level 2 for
quantified bit-vector problems; `bv2int`/`int2bv` bridging axioms are
asserted lazily from `relevant_eh`. Verus sends `by(bit_vector)` obligations
as separate prelude-free queries with solver defaults ("TODO: tune Z3/CVC5
options for bit-vector queries").

**Papers.** Niemetz, Preiner, Reynolds, Zohar, Barrett and Tinelli, *Towards
Bit-Width-Independent Proofs in SMT Solvers*, CADE 2019 (JAR 2021). Zohar,
Irfan, Mann, Niemetz, Nötzli, Preiner, Reynolds, Barrett and Tinelli,
*Bit-Precise Reasoning via Int-Blasting*, VMCAI 2022. Hadarean, Bansal,
Jovanović, Barrett and Tinelli, *A Tale of Two Solvers: Eager and Lazy
Approaches to Bit-Vectors*, CAV 2014. Niemetz, Preiner and Zohar, *Scalable
Bit-Blasting with Abstractions*, CAV 2024.

**What would settle it.** The gap set by logic first: if the UFBVDTNIA share
of the gap is proportional to its share of the set, bit-vectors are not a
direction. Then `--theoryof-mode=term` on that subset.

---

# Group D — before the search

What the search is given, and what it is made to look at. R20 holds the one
measured win so far; R22 and R23 have one-flag experiments.

## R20 — Preprocessing: `distinct`, non-clausal simplification, ITE

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
otherwise `theory/uf/distinct_extension.cpp` handles it lazily (PR #12136,
from the fork's `distinctExt`). `--simplification` [`batch`] (`none`),
`--static-learning` [`true`], `--arith-static-learning` [`true`],
`--learned-rewrite` [`false`], `--ite-simp` [`false`; implies
`--early-ite-removal`], `--on-repeat-ite-simp` [`false`], `--simp-ite-compress`
[`false`], `--repeat-simp`, `--unconstrained-simp`, `--simp-with-care` [all
require a quantifier-free logic], `--ext-rew-prep` [`off`], `--sort-inference`
[`false`], `--deep-restart` [`none`]. Pass order in
`smt/process_assertions.cpp`; `non-clausal-simp` runs inside
`simplifyAssertions` under `batch`.

**Tried.** `lazyDistinct` → `distinctExt` (2025, merged), `distinctElim`
(2026, merged, the threshold option), `ufEagerDistinct` (2026,
`--uf-eager-distinct`, unmerged), `lazyDistinctSlv-pf` (proofs);
`simplifyRecFun` (2026, `--simplify-rec-fun`); `eagerElimDefs` (2024,
`--eager-elim-defs`); `rlvTermSimplify` (2024); `ncSimpMore` (2023),
`ncSimplifyInc` (2019); `iteApply`, `learnBranchIte`, `theoryRewriteEqIte`;
`noSimpleLearnedLitPp`, `noConjoinLit` (2023).

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

**Papers.** Kim, Somenzi and Jin, *Efficient Term-ITE Conversion for
Satisfiability Modulo Theories*, SAT 2009 (cited by cvc5's `--ite-simp`).
Barbosa et al., cvc5, TACAS 2022 (the pass pipeline). Bjørner, de Moura,
Nachmanson and Wintersteiger, *Programming Z3*, 2019.

**What would settle it.** Preprocessing time as a share of solve time on the
gap set (`--stats`); then `--simplification=none`, `--no-static-learning`,
`--ite-simp` as runs.

## R21 — Quantifier preprocessing: what is done to a quantifier before it is ever matched

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

**Tried.** `macrosEagerInst`, `macroEagerInstMt` (2024, macros as the first
eager-instantiation target), `ai-macroPf`, `macrosHo` (merged),
`quantMacrosPf`; `prenexLift` (2017); `p657` (do not prenex into non-standard
quantifiers); `quantRew-1006` (constructor equalities in bodies);
`quantTheoryRewrites`; `alphaEqVarShadow`, `ai-fixAlphaEq*` (alpha-equivalence
and proofs). No miniscoping branch.

**Elsewhere `(code)`.** z3: pattern inference returns early on an annotated
quantifier and Verus sets `pi.enabled=false` anyway; `smt.pull_nested_quantifiers`
[false], `smt.q.lift_ite` [0], `smt.macro_finder` [false] with the code
comment that it "destroys the existing patterns" on Boogie-style benchmarks;
NNF is forced. Dafny, F* and Verus all tune the *encoding* side (trigger
selection, `sort_disjunctions`, `der`) rather than the solver's rewriting.

**Papers.** Fontaine and Schurr, *Quantifier Simplification by Unification in
SMT*, FroCoS 2021. El Ghazi, Ulbrich, Taghdiri and Herda, *Reducing the
Complexity of Quantified Formulas via Variable Elimination*, SMT 2013.
Leino and Pit-Claudel CAV 2016 (why verifiers own trigger selection).

**What would settle it.** `--user-pat=trust` with `--miniscope-quant=off
--prenex-quant=none --ite-lift-quant=none --cond-var-split-quant=off` against
`strict`: if they match, the rewriting was the effect of `strict`.

## R22 — Preregistration: which literals the theories are told about

*Rows `h-28`.*

**The hypothesis.** cvc5 preregisters a literal with its theory when the
literal is registered with the SAT solver, so every instance lemma delivers
all its atoms to the theories at once, whether or not the search will ever
assign them. z3 hands an atom to its theory only when it is assigned *and*
relevant. `lazy` preregistration exists on `main`; `relevant` exists as a
long-lived branch.

**In cvc5 today `(code)`.** `--preregister-mode` [`eager`] (`lazy`: when
asserted); `--relevance-filter` [`false`]; `prop/theory_preregistrar.cpp`.

**Tried.** `preregRlv` (R11: `--preregister-mode=rlv`, 552 lines, PR #9503,
branch since 2024-04, still active 2026-04); `satRlv` (2022, the notes' old
broken branch); `sdm-assertTerms`, `skolemLemma` (2022).

**Elsewhere `(code)`.** z3 `smt.relevancy` [2] — see R11; theory axioms for
datatype accessors and `bv2int` are created from `relevant_eh`.

**Papers.** MSR-TR-2007-140.

**What would settle it.** `--preregister-mode=lazy` on the set, today. Then the
branch.

## R23 — Term-database relevance: which ground terms E-matching may use

*The "things that helped" row `--term-db=relevant`; now the default.*

**The hypothesis.** The set of ground terms available to triggers decides how
many instances a round produces. `relevant-all-delay` — only terms connected
to current assertions, then everything as a last resort — is the fork's
`verusDev` work and is now cvc5's default. Its relevance is a monotone
over-approximation (a merge marks both sides and their subterms relevant
forever), so on long runs it converges to `all`.

**In cvc5 today `(code)`.** `--term-db-mode` [`relevant-all-delay`] (`all` /
`relevant`); `TermDb::eqNotifyMerge` marks on merge; `shouldRecheck` widens
once before answering unknown, "only if at least one new term was added to
the term database"; `--register-quant-body-terms` [`false`].

**Tried.** `verusDev`, `lastCallRecheck` (2026-02, merged); `tdbRelevant`
(2024, enable `relevant` by default; superseded); `cdRlvTerms` (2024,
context-dependent relevance via the master engine → `trackSkip`, likely
merged); `rlvTermSimplify`, `tdbLLOpts` (2024); `tdbDev1107`, `tdbOpt1108`
(2021); `tdbOldIndex` (2020, `--tdb-old-index` prefer old terms in indices);
`optTdbTNode` (2019).

**Elsewhere `(code)`.** z3 matches only enodes marked relevant: `relevant_eh`
feeds the matcher's candidate queue, `execute_core` asserts relevance, and
relevancy is backtracked with the search rather than accumulated.

**Papers.** MSR-TR-2007-140; Simplify J. ACM 2005 (the relevance of terms to
matching).

**What would settle it.** `--term-db-mode=all` and `=relevant` against the
default on the set (three runs), with `QuantifiersEngine::Num_Quantifiers`,
term-database size and instance counts.

---

# Group E — cross-cutting

## R24 — A domain configuration: run cvc5 the way Verus runs z3

*The notes' "things that helped", made into one object.*

**The hypothesis.** Verus hands z3 nine options and hands cvc5 one
(`incremental=true`, plus `(set-logic ALL)`). Every z3 option in that list
corresponds to a cvc5 decision that is currently made by a default tuned for
SMT-LIB: no MBQI, no auto-configuration, strict patterns, delayed units,
nonlinear off, relevancy-based case splits. A cvc5 configuration assembled
from the directions above — and a mode that sets it — is the cheapest thing
this project can deliver, and the baseline shows its first two flags are
worth a factor of 1.2 on PAR2.

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

**Tried.** `verusDev` (2025-11 to 2026-02, merged in pieces: the
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
change phase and restart policy. Dafny: the same list with
`smt.qi.eager_threshold=44`, `smt.case_split=3` restored after it was dropped
("time travelling triggers", dafny discussion #3362). F*: `smt.mbqi=false`,
`auto_config=false`, `smt.case_split=3`, `smt.relevancy=2`,
`rewriter.enable_der=false`, `rewriter.sort_disjunctions=false`,
`pi.decompose_patterns=false`. Boogie issue #73 records that the defaults
date from about 2007 and were "geared towards particular kinds of benchmarks
(quantifier-heavy, etc.)" with no per-option rationale; Leino on z3 issue
#7363: "the requirement for :auto_config and :smt.mbqi to be set to false
enables trigger-based quantifiers".

**Papers.** Leino and Pit-Claudel CAV 2016. Bai, Hawblitzel and Lattuada,
*Tunable Automation in Automated Program Verification*, 2025 (Verus's
tunable instantiation levels). Lattuada et al., *Verus: A Practical
Foundation for Systems Verification*, SOSP 2024.

**What would settle it.** This is goal 3 in its cheapest form: the twelve
single-flag runs above, each against the baseline, then the bundle. The
result is a table with one row per flag, which is also the first draft of
the attribution.

## R25 — Low-level engineering: the constant factors

*Rows `h-22`. Not a research direction on its own; the tail that remains
when the algorithmic directions are done, and sometimes the head.*

**The hypothesis.** Some of the 10–20× cases in the gap set (306 of the 504
solved-but-slow) are not a different algorithm but the same algorithm with
larger constants: node hashing, the trie indices of the term database,
equality-engine notification overhead, memory. A profile finds these in an
afternoon, and the fork has three old branches of exactly this kind.

**In cvc5 today `(code)`.** Nothing to configure; `job_launcher`'s host
scripts include `get_profile` (callgrind) and `get_backtrace`. PR #9724 (fire
equality-engine notifications only when the caller has been used) is the
notes' example.

**Tried.** `perfDataStructures` (2018, 31 commits), `lowLevelOptMore` (2019),
`optTdbTNode` (2019), `tdbLLOpts` (2024), `minorOpt-0516` (2025, partly
merged), `cdno` (2025), `optTheoryOf`, `optGetType`, `optArithRw`,
`getValueOpt` (2022–23), `rewriteDep` (2025, "fix performance").

**Elsewhere `(code)`.** z3's matcher and egraph are built around cheap
approximations: 64-bit label sets as Bloom filters on every root, region
allocators, fingerprints as the duplicate check, candidate lists compressed
by expr id above a threshold.

**Papers.** None; engineering.

**What would settle it.** callgrind on the ten worst solved-but-slow
benchmarks, at row 1 of the latency table. If one function dominates, this is
the direction for those ten.

## R26 — Attribution instrumentation: the tools goal 2 needs

*Rows `h-14` (instability); the profiling the notes never had.*

**The hypothesis.** Every direction above ends with "what would settle it",
and most of those measurements need counters cvc5 does not print by default,
per-quantifier instance counts against z3's, or a view of the instantiation
graph. The verifier community built these for z3 (Axiom Profiler, SMTScope,
Verus's `--profile`, Mariposa, Cazamariposas, SHAKE) and none of them reads
cvc5's output. Building the cvc5 side is the project's own instrument, and
it is also what makes a Verus user able to debug a cvc5 slowdown at all.

**In cvc5 today `(code)`.** `-o inst` (instantiations as they happen, and
`(num-instantiations <qid> <n>)` per round), `-o inst-strategy` (which module
ran), `-o trigger` (selected triggers; `userTriggerOut2` distinguishes user
ones), `-o lemmas`, `-o incomplete` (why unknown), `-o options-auto`,
`-o learned-lits`; `--dump-instantiations`, `--print-inst` [`list`] (`num`),
`--print-inst-full`; `--stats-internal` with `Instantiate::Instantiations_Total`,
`Duplicate_Inst`, `Duplicate_Inst_Eq`, `Duplicate_Inst_Ent`,
`QuantifiersEngine::time_ematching`, `time_conflict_based_inst`,
`Rounds_Instantiation_Full`, `Rounds_Instantiation_Last_Call`, `Triggers`,
`Triggers_Multi`, and the CaDiCaL propagator counters. No matching-loop
detection, no instantiation graph, no per-quantifier cost on `main`.

**Tried.** `qdebugStats` (2026-01, 29 commits, "debug stats for
e-matching", an `AnalyzeEE` module, unmerged); `debugDumpLemmas` (2025,
`--re-check-lemmas`); `termOrigin` (2025, `--track-term-origins`: the
lemma-origin DAG, i.e. an instantiation graph); `trackInferId` (2024,
`--track-lemma-inference-ids`); `uclHistogram`, `oclTimestamp` (2024);
`miscStats` (2023); `dfcPp` (2021, difficulty). Outside the fork, in
September 2026: BasisResearch/cvc5 pull requests adding `(get-info
:matching-loops)`, `--inst-graph` and `(get-info :inst-pressure)`, with
matching Verus-side `-V matching-loops` support — not upstream, and not
evaluated here.

**Elsewhere.** z3 `smt.qi.profile` (per-quantifier instances and cost),
`trace=true` with the Axiom Profiler and now SMTScope (z3-only, "~10x
faster"); Verus `--profile` / `--profile-all` reads the z3 log and ranks
quantifiers by cost times instances; F*'s `qprofdiff`. Mariposa measures
instability under semantics-preserving mutation; Cazamariposas localises it;
SHAKE prunes context for stability (29 % / 41 % on z3 and cvc5).

**Papers.** Becker, Müller and Summers, *The Axiom Profiler: Understanding and
Debugging SMT Quantifier Instantiations*, TACAS 2019. Fiala and Müller,
*SMTScope: Automated and Efficient Analysis of SMT Traces*, TACAS 2026.
Zhou, Bosamiya, Takashima, Li, Heule and Parno, *Mariposa: Measuring SMT
Instability in Automated Program Verification*, FMCAD 2023. Zhou, Shah, Lin,
Heule and Parno, *Cazamariposas: Automated Instability Debugging in SMT-Based
Program Verification*, CADE 2025. Zhou, Bosamiya, Li, Heule and Parno,
*Context Pruning for More Robust SMT-based Program Verification*, FMCAD 2024.
Amrollahi, Preiner, Niemetz, Reynolds, Charikar, Tinelli and Barrett,
*Towards SMT Solver Stability via Input Normalization*, FMCAD 2024. Lattuada
et al., Verus, OOPSLA 2023.

**What would settle it.** Nothing; this direction is the instrument. Its
deliverable is the attribution table of goal 2, and the first version of it
needs only `--stats-internal` and `-o inst` on the gap set.

---

# What to run first, as a prediction

The directions are not ranked by expected share of the gap — that is goal
2's job — but by what one run costs today. Everything in the first list is a
config change in [`job_launcher/configs/`](../../../job_launcher/configs/)
against the baseline; everything in the second is a `BRANCH=` build of a
fork branch; the third needs design work and is where the notes and the z3
code agree the structural difference lives.

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

**Fork branches, one build each.** `ai-instDefer` (R9/R10), `ai-jhRlvInst`
(R10), `dtSplitRelevant` (R16), `ai-dioLc` (R17), `ai-prepared13` (R3),
`preregRlv` (R22), `mbtc25` (R14), `dtMergeNotify-v3` (R15), `deferBlock`
(R9/R17), `bitblastLc` (R19), and `claude-eagerInst` with its pacing limits
(R1) — the only eager-instantiation branch designed with a budget.

**Design work.** R1 with R2 and R9 together: eager, incremental,
forgetting. The notes' three attempts at R1 each ran into the absence of R9
("clauses are not deleted, can encounter infinite branch and bound, matching
loops"), and the z3 code says the three are one mechanism. It is the
expensive direction, and the attribution has to earn it.

---

# Sources

- The performance notes of 2026-09-14, as summarised in
  [`../notes.md`](../notes.md).
- cvc5 `main` at `f294265` (2026-09-14): `src/options/*.toml`,
  `src/smt/set_defaults.cpp`, `src/theory/quantifiers/`, `src/prop/`,
  `src/theory/datatypes/`, `src/theory/arith/`, read 2026-09-15.
- z3 `master` at `2d2fb04` (2026-09-14): `src/smt/qi_queue.cpp`,
  `smt_quantifier.cpp`, `mam.cpp`, `smt_context.cpp`, `smt_relevancy.cpp`,
  `smt_case_split_queue.cpp`, `theory_datatype.cpp`, `theory_lra.cpp`,
  `theory_bv.cpp`, `smt_setup.cpp`, `src/params/*.pyg`,
  `src/math/lp/int_solver.cpp`, `dioph_eq.cpp`, `src/ast/pattern/`,
  `src/solver/assertions/asserted_formulas.cpp`, read 2026-09-15.
- The `ajreynol/CVC4` fork, 801 branches as fetched into the local checkout
  on 2026-08-26 plus 52 newer ones; commit subjects, diffstats and option
  help text read 2026-09-15. Merged/unmerged status was checked by looking
  for each branch's added lines in `main`, since upstream squash-merges.
- Verus `source/air/src/context.rs` and `source/rust_verify/src/verifier.rs`;
  Dafny `Source/DafnyCore/DafnyOptions.cs`; Boogie
  `Source/Provers/SMTLib/Z3.cs`; F* `src/smtencoding/FStarC.SMTEncoding.Z3.fst`;
  z3 issues #1151, #7363; Dafny discussion #3362; Boogie issue #73.
- Papers as cited, verified against publisher or dblp pages on 2026-09-15;
  where a citation could not be verified the text says so.
