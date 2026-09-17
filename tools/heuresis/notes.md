# The register

**Every candidate cause of the gap, one row each, with its state and what
would settle it.** A summary of a set of cvc5 performance notes dated
2026-09-14, rewritten as a register: the source is a working document and is
not tracked here; this file is what the project cites.

*What a row is and is not.* A row is a hypothesis about where cvc5 loses time
on the set. The `state` column is the state of the *code* as the notes
describe it as of 2026-09-14, not a fresh source audit. The project's later
source checks and measurements are in [directions.md](docs/directions.md).
This inherited state says nothing about the *effect* on the set. Exactly one row
carries a measured effect (`h-25`), and it is marked. Every other row is a
candidate until the attribution ([`README.md`](README.md), goal 2) assigns it a
share of the gap and a ledger entry backs the assignment.

**States.** `main` — landed, possibly behind an option; `pr` — an open pull
request; `branch` — a working branch exists, unmerged; `sketch` — a partial
branch; `idea` — no code; `inconclusive` — tried, no conclusion drawn;
`unlikely` — the notes themselves discount it.

**Ids** are this file's (`h-N`) and stable: a row is never renumbered, only
marked settled.

---

## A — Lemma lifecycle

*cvc5 keeps every lemma it ever learns, and every instantiation, and decides
on them in an order that was not designed for tens of thousands of them.*

| id | hypothesis | state | where | what would settle it |
| --- | --- | --- | --- | --- |
| h-1 | **No clause deletion.** Instantiation lemmas are never removed once sent to the SAT solver; the clause database only grows. Candidate mechanism: cadical's removable clauses. | idea | — | count of active clauses over time on a gap benchmark vs. the same in z3; then an implementation |
| h-2 | **"Local" lemmas in the decision heuristic**: treat instantiation lemmas as local to the context that produced them. | main | `--inst-local`, [cvc5#12121](https://github.com/cvc5/cvc5/pull/12121) | A/B on the set with the option on and off |
| h-3 | Justification heuristic is slightly slow because the lemma list is never cleaned; would need aggressive traversal. | unlikely | — | the notes discount it; a profile of a gap benchmark confirms or reopens |
| h-4 | **Justify conflicts before lemmas**, so the heuristic does not spend its time satisfying a large number of instantiations. Variant: defer only instantiation lemmas. | branch | [`ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) | A/B on the set |
| h-5 | **Relevance ordering**: move clauses to the front where a conflict was found while satisfying them. | main | `--jh-rlv-order` | A/B on the set |
| h-6 | **Relevance for instantiations**: ignore an instantiation lemma in the justification strategy until its quantified formula is asserted. Expected impact low — it only matters for quantified formulas that are not top-level. | branch | [`ai-jhRlvInst`](https://github.com/ajreynol/cvc5/tree/ai-jhRlvInst) | count of non-top-level quantified formulas on the set; if small, close |
| h-7 | **Lemma inprocessing**: when instantiations are added, replace their literals with known SAT literals via a globally maintained set of learned substitutions. Experimental. | main | `--lemma-inprocess=X` | A/B on the set |
| h-8 | **Conflict minimization**: when a theory lemma is added, re-prove it by substitution and rewriting and drop redundant literals; the notes say up to 50 % of lemmas come out smaller. Experimental. | main | `--conflict-process=X` | A/B on the set; the 50 % is a lemma-size figure, not a time figure |

## B — Arithmetic

*The set is quantified arithmetic with datatypes, and the arithmetic solvers
were tuned elsewhere.*

| id | hypothesis | state | where | what would settle it |
| --- | --- | --- | --- | --- |
| h-9 | **Infinite branch and bound** in linear arithmetic. Candidate: block branch-and-bound lemmas, or delay them. | branch | [`deferBlock`](https://github.com/ajreynol/cvc5/tree/deferBlock) | count of branch-and-bound lemmas per gap benchmark; A/B |
| h-10 | **The DIO solver is slow.** It was fixed to handle non-linear monomials ([cvc5#12178](https://github.com/cvc5/cvc5/pull/12178), which also disabled it for quantifier-free non-linear logics); candidate: move it, at least partly, to last-call effort. | branch | [`ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc) | share of time in the DIO solver on gap benchmarks, from a profile; A/B |
| h-11 | **Eliminate arithmetic at preprocessing** (a debugging experiment, not a proposal). Involved: datatype fields carry arithmetic, and it disturbs trigger selection. Too many things changed at once to conclude anything. | inconclusive | — | not worth repeating as an experiment; superseded by attribution |
| h-12 | **Incremental performance** is related to the quantifier-instantiation problems. A question in the notes, not a claim. | idea | — | whether the set is incremental at all; if not, close |
| h-13 | **AC reasoning over multiplication**: infer terms equal by associativity and commutativity of `*`. Very incomplete. | main (default) | the notes link a branch `arithFlattenEq` that does not exist in the fork; the merged work is `arithFlattenCollect2` (2025-04) | count of non-linear terms on the set; A/B with it disabled |
| h-14 | **Instability** in non-linear arithmetic: consider sending some lemmas eagerly. | idea | — | variance across seeds or orderings on gap benchmarks |

## C — Instantiation

*The largest cluster, and the one where the notes name what z3 has and cvc5
does not.*

| id | hypothesis | state | where | what would settle it |
| --- | --- | --- | --- | --- |
| h-15 | **Conflict-based instantiation has exponential behaviour**, seen in rare cases (`mu_test.smt2`, from Marco Roveri). On this set it is disabled outright (see [the configuration](#the-configuration-under-study)). | branch | [`ai-cbqi-0423`](https://github.com/ajreynol/cvc5/tree/ai-cbqi-0423) | settled for this set: enabled modes regress and 272,280 QCF rounds emit only 54 conflict lemmas ([ledger](ledger/2026-09-16-conflict-instantiation.md)); the branch matters elsewhere |
| h-16 | **No eager instantiation**, in the sense of [de Moura and Bjørner's *Efficient E-matching*](https://leodemoura.github.io/files/ematching.pdf): cvc5 instantiates only at full effort. An implementation exists and has three problems: performance (clauses are not deleted, infinite branch and bound, matching loops; no lazy-vs-eager dynamic policy), generality (user patterns only, no auto-generated ones), and E-matching is not incremental. Two assistant-written attempts followed, one from scratch and one extending it. | branch ×3 | [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3), [`ai-eagerInst2`](https://github.com/ajreynol/cvc5/tree/ai-eagerInst2), [`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | push the rebased compact bounded branch; A/B time-to-first-useful-instance and full rounds on a fixed gap slice |
| h-17 | **E-matching has exponential behaviour** (best example: `prepared_13.smt2`, from Kartik). Candidate: cache the state at which matching failed, for a better worst case. `--ieval=use` is another route via entailment, with more advanced settings (`--ieval=use-learn`). | branch | [`ai-prepared13`](https://github.com/ajreynol/cvc5/tree/ai-prepared13) | time in E-matching per gap benchmark, from a profile; A/B |
| h-18 | **No mod-time optimization**: compute only the triggers worth recomputing, from a diff of the E-graph. A key component of the z3 and Simplify papers, and by itself a poor fit for cvc5 because cvc5 lacks eager instantiation (h-16). | sketch | [`ai-emFilter`](https://github.com/ajreynol/cvc5/tree/ai-emFilter) | coupled to h-16; measure the fraction of trigger evaluations that find nothing new |
| h-19 | **Trigger policies** that limit instantiations per round — for instance, not considering multiple matches for the same ground term in one round. | idea | — | distribution of instantiations per round on gap benchmarks |

## D — Theory combination and equality engines

| id | hypothesis | state | where | what would settle it |
| --- | --- | --- | --- | --- |
| h-20 | **Distributed equality engines** cost something the central mode does not. `--ee-mode=central` exists on `main`; a branch merges specifically UF and datatypes, at the price of making datatypes a second-class theory (no theory combination, no assertion stack of its own). The notes float merging engines in the default distributed mode. | main (option) + branch | `--ee-mode=central`, [`ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare), [`dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3) | current-main central mode cuts PAR2 10.3%; `ai-eecNoShare` passes regressions but changes PAR2 only −0.20%, so count skipped propagation work before upstreaming ([ledger](ledger/2026-09-16-rebased-equality-and-evaluator-branches.md)) |
| h-21 | **Care graph vs. model-based theory combination.** Model-based is much simpler and typically comparable, worse in some logics (QF_ABV). | pr | [cvc5#12095](https://github.com/cvc5/cvc5/pull/12095) | A/B on the set |
| h-22 | **Equality-engine notifications**: fire them only when the caller has been used; a low-level optimization. | pr | [cvc5#9724](https://github.com/cvc5/cvc5/pull/9724) | a profile: share of time in notification callbacks |

## E — Datatypes

| id | hypothesis | state | where | what would settle it |
| --- | --- | --- | --- | --- |
| h-23 | **No elimination of datatypes** at preprocessing. | sketch | [`dtElim`](https://github.com/ajreynol/cvc5/tree/dtElim) | how much of the set is datatype-heavy; the sketch's completeness |
| h-24 | **Datatype splitting is too liberal.** Conservative variant: split only on relevant datatype terms, those in currently asserted terms. A more liberal variant was suggested by Kartik (the notes break off mid-sentence describing it). | branch | [`dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant) | split count is measured and global binary splitting regresses; add eligible/suppressed relevance counters before the branch ([ledger](ledger/2026-09-16-datatype-and-equality-controls.md)) |

## F — Preprocessing

| id | hypothesis | state | where | what would settle it |
| --- | --- | --- | --- | --- |
| h-25 | **Large `distinct` terms** caused a pause of about four seconds at preprocessing. **Measured: average speedup 1.75× on the verus+sundance set at a 60-second timeout.** Now lazy by default. | main | [cvc5#12136](https://github.com/cvc5/cvc5/pull/12136) | settled for what it is; the baseline (goal 1) will show what remains |
| h-26 | **Non-clausal simplification is somewhat slow**; may need revisiting. | idea | — | share of preprocessing time in the pass, from a profile |
| h-27 | **ITE simplification** that is off by default should be on: `(= (ite C x 1) 0)` to `C ∧ x = 0` when `(ite C 0 1)` has a single parent. | idea | — | count of such patterns on the set; A/B |

## G — Preregistration and relevance

*What the SAT solver is made to decide on, and what the theories are made to
see.*

| id | hypothesis | state | where | what would settle it |
| --- | --- | --- | --- | --- |
| h-28 | **Eager preregistration** hands the theories terms the search may never need. Lazy mode is on `main`; a *relevant* mode maintains a boundary of watched literals that are actively relevant to satisfying the current Boolean skeleton. | main (option) + pr | `--preregister-mode=lazy`, [cvc5#9503](https://github.com/cvc5/cvc5/pull/9503) | A/B with lazy; then the pull request |
| h-29 | **Justification heuristic vs. relevance.** z3 uses relevancy filtering ([de Moura and Bjørner, MSR-TR-2007-140](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2007-140.pdf)); the candidate is `--decision=internal` with relevance filtering. An old branch is broken. | sketch (broken) | [`satRlv`](https://github.com/ajreynol/cvc5/tree/satRlv) | the attribution first: how much time is spent on decisions that relevancy would have skipped |

---

## The configuration under study

The notes list what has helped on this set. The best measured configuration —
the one future A/Bs use unless a ledger entry says otherwise — is:

```
--no-cbqi --user-pat=strict --sat-solver=cadical --ee-mode=central --ieval=off
```

The first five rows are its measured components; the remaining helpers are
candidates to test one at a time.

| option | why | caveat in the notes |
| --- | --- | --- |
| `--user-pat=strict` | preserve user-provided triggers exactly | odd semantics: `(forall x. false :pattern (P x))` should be a conflict but needs a `P` term |
| `--no-cbqi` | conflict-based instantiation is a loss here (h-15) | an order-of-magnitude win on sledgehammer problems; the notes say it should be off by default on Verus benchmarks |
| `--sat-solver=cadical` | faster SAT core; explicit selection cut PAR2 6.5% and rescued 55 benchmarks | the declared default since 2026-08, **but** `--incremental` defaults to true and forces MiniSat unless the SAT solver is set explicitly ([ledger](ledger/2026-09-15-sat-and-instance-order.md)) |
| `--ee-mode=central` | 70 net additional solves and 10.3% lower PAR2 on current main | broad correctness surface; test a second corpus before treating this as a default ([ledger](ledger/2026-09-16-rebased-equality-and-evaluator-branches.md)) |
| `--ieval=off` | composes with central equality for 77 net solves and 13.6% lower PAR2 than the current-main control | points specifically at partial-evaluator cost or pruning; `ievalTravTrie` is neutral, so instrument before redesigning ([ledger](ledger/2026-09-16-rebased-equality-and-evaluator-branches.md)) |
| `--term-db=relevant` | filter congruent terms; ignore ground terms preregistered but not asserted; recently made incremental | whether it is default is not stated; check before assuming it is in the baseline |
| `--enum-inst` | solves more | and times out more; not enabled by default |

## What helps elsewhere, and not here

Recorded so that a later reader does not rediscover them as candidates.

- **Conflict-based instantiation** (`--cbqi`, default on): order-of-magnitude
  improvement on sledgehammer; off for this set.
- **Entailment filtering** (`--inst-no-entail`, default on): a quick
  entailment test on each instantiation, discarding those already entailed.
- **Incremental entailment filtering** (`--ieval=use`, default): the same
  test as instantiations are built, so an entailed instantiation can be
  discarded after a partial assignment to its variables.

## What z3 has, according to the notes

The rows above that the notes describe as things z3 (or Simplify) does and
cvc5 does not. This is the list the attribution is most likely to end up
ranking, and it is written down here so that it is a hypothesis with an id and
not a background assumption:

| difference | rows |
| --- | --- |
| eager instantiation, with lazy-vs-eager policies | h-16 |
| mod-time optimization of trigger evaluation | h-18 |
| relevancy filtering in the SAT search | h-29 |
| learned-clause deletion for instantiation lemmas | h-1 |

Three rows — h-16, h-20 and h-24 — are marked in the notes as having also
been arrived at independently by an assistant's review of cvc5 (its
"directions" 1, 3 and 4). That is agreement between two readings, not
evidence; it changes nothing about their state.

## A reading of the register

*This section is reasoning, not measurement, and is here to be tested by the
attribution and deleted if wrong.*

Twenty-nine rows collapse into four structural differences and two tails:

1. **When instantiation happens** (h-16, h-18, h-19; h-17 as its worst case).
   The solvers differ in kind, not degree: z3 instantiates during search and
   throws the results away on backtrack; cvc5 instantiates at full effort and
   keeps everything.
2. **What happens to lemmas afterwards** (h-1, h-2, h-4, h-5, h-6, h-7, h-8).
   Downstream of 1: a solver that instantiates eagerly must delete, and one
   that keeps everything must at least decide on it in a sensible order.
3. **What the SAT solver is made to look at** (h-28, h-29). Relevancy.
4. **How theories talk to each other** (h-20, h-21, h-22).
5. **Arithmetic** (h-9, h-10, h-13, h-14) and **datatypes** (h-23, h-24) —
   the tails, unless the set turns out to be dominated by one of them, which
   the attribution will show.
6. **Preprocessing** (h-25, h-26, h-27) — one already paid out at 1.75×, which
   is a reason to look at the rest of the pass rather than to dismiss it.

If the reading is right, the attribution table will have three heavy columns
and many light ones, and the cheapest change that closes most of the gap is
somewhere in 2 or 3 rather than 1, because 1 is the expensive one and the
notes already record three attempts at it. If the reading is wrong, the table
will say so, and this section goes.

## Sources

- The performance notes, a working document of 2026-09-14, not tracked
  (`.gitignore`: `*.docx`). Its triage spreadsheet:
  <https://docs.google.com/spreadsheets/d/1KPtfIMxzFAoI3dwpa3ZvGsClcBEZ3Ozd4z25xLwpkGw/edit?gid=63079960#gid=63079960>.
- The two z3 papers the notes cite: *Efficient E-matching for SMT Solvers*
  (de Moura, Bjørner, CADE 2007) and *Relevancy Propagation*
  (de Moura, Bjørner, MSR-TR-2007-140).
