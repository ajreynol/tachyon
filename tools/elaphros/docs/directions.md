# Research directions for proof-production overhead

**Source assessment, 2026-09-18.** These twelve directions start from the
[hypothesis register](../notes.md) and the
[public-branch survey](../ledger/2026-09-18-branch-survey.md). No performance
effect is measured. Risk estimates concern implementation, validation and
regression exposure; potential value is conditional on the mechanism being
important on the eventual corpus. The [queue](todo.md) separates these priors
from maintainer guidance.

Source comparisons use upstream [main at `3dcc1ef542`][main]. Branch names below
link to living branches for navigation; their **audited tips, merge bases and
source deltas are pinned in the survey**. A feature found on main is not
evidence that the old fork tip was merged verbatim. Buildability and proof
validity have not been tested.

## The map

| part of the problem | directions | distinguishing question |
| --- | --- | --- |
| Avoid unnecessary proof work | E1–E4 | Can we avoid a justification, reduce its dependencies, or represent it compactly? |
| Process the necessary proof efficiently | E5–E8 | Can sharing, provenance, caching or better rule algorithms reduce the work? |
| Retain and emit proofs efficiently | E9–E11 | Which representation, lifetime and session costs can be avoided? |
| Make the comparison interpretable | E12 | Did proof mode change the solving problem or available algorithms? |

The first four directions are related but distinct. **Unrewriting** changes
which atom representation the refutation uses. **Macro decomposition** reduces
a large obligation to small local ones. **Compact conversion** changes how a
necessary equality derivation is represented. **Dependency minimization** avoids
justifying child rewrites irrelevant to the final result. A combined branch
cannot tell us which mechanism matters.

## E1 Unrewriting

**Question.** Can a refutation keep an atom in its original form and omit its
rewrite proof when the Boolean reasoning does not depend on the rewritten
form? This is a maintainer-highlighted research direction.

**Code.** [`unrewrite`][unrewrite] adds `--proof-unrewrite`, connects preprocessing
proofs, and classifies atoms occurring in input-derived versus theory lemmas.
Its converter callback has an empty body; the tip is a sketch, not an
established implementation. [`unrewrite2`][unrewrite2] descends from it and adds
candidate preimages, exclusive removable-node accounting, replay of renamed
proof steps, fallback when replay fails, and an input-only variant
(`--proof-unrewrite-input-only`). It checks that a replacement introduces no
new free assumptions before installing it. Those checks express intent;
their sufficiency is not established here.

**Critical timing distinction.** The second branch analyzes before and after
`ProofPostprocess::process`, but attempts its actual replacement **after**
elaboration. It may reduce printed/checker work while already having paid to
construct the discarded material. The stronger research question is whether
the safe decisions can be made before elaboration. Count exclusively removed
nodes: a subproof still reachable elsewhere was not saved.

**Controls and next evidence.** Neither option is on pinned main. First specify
the allowed atom renamings, theory boundaries, fixed input assumptions and
fallback policy. Later compare unchanged, analysis-only, post-elaboration
conversion, and a separately justified early-conversion design. Record replay
failures, analysis/replay time, exclusive nodes avoided, emission and checking.
The existing trace summary is an instrumentation lead, not a result.

**Risk / value.** High / high potential. The proposal removes a class of
justifications, but atom collisions, theory-sensitive rules, scopes and
repeated replay can erase the benefit or invalidate the proof.

## E2 Smaller macro obligations

**Question.** Must a macro that transforms one large formula into another
reconstruct rewriting throughout both formulas, when only a few parts change?

**Code.** [`reduceTransform`][reduceTransform] intercepts
`MACRO_SR_PRED_INTRO` and `MACRO_SR_PRED_TRANSFORM`. It decomposes conjunctions,
uses conversion conditions to isolate changed subterms, reuses matching
premises, and uses transitivity when two equalities share a side. A conceptual
case is transforming `(and G H1)` into `(and G H2)` by retaining `G` and proving
the local change. This is an explanation of the mechanism, not a run result.
The implementation is confined to two postprocessor source files, but adds
recursive obligations and internal rule checks. Related code in
[`cpcDevChainMRes`][cpcDevChainMRes] also tries polynomial-normalization rules.
The specific reduction helpers are absent from pinned main.

**Controls and next evidence.** There is no dedicated mainline switch for this
decomposition. Existing granularity controls change which macros are expanded;
using a coarser output is not an equivalent optimization. First enumerate each
decomposition and its fallback, distinguish code shared with the larger CPC
branch, and identify the current equivalent insertion points. Later count
macro sizes, changed versus unchanged subterms, successful reductions, failed
checks, and expansion work saved under identical output requirements.

**Risk / value.** Medium / high potential. A relatively contained way to test
whether oversized obligations, rather than primitive checker operations, are
the main cost. Repeated speculative checking and lost DAG sharing are risks.

## E3 Compact term conversion

**Question.** Can a checked conversion step replace long congruence and
transitivity derivations? This is the other maintainer-highlighted direction.

**Code.** [`pfrConvert`][pfrConvert] adds `--proof-use-convert`, a `CONVERT` rule,
and context-sensitive changes inside `TConvProofGenerator`.
[`pfrConvert2`][pfrConvert2] is a distinct design, **not a descendant of the
first audited tip**: it adds `--proof-use-rule-convert`, `CONVERT` and
`CONVERT_FIXED_POINT`, and a checker that applies pre/post rewrite maps while
recording used premises. These switches and the proposed conversion rules are
absent from pinned main. The old ALF printer changes do not establish current
CPC/checker support.

**Critical timing distinction.** In `pfrConvert2`, the ordinary internal
conversion path runs first to obtain a reference result; the compact attempt
then recomputes conversion and falls back if needed. A compact final proof can
therefore still pay for much of the original construction. Separate the
representation experiment from a future direct compact-production design.

**Controls and next evidence.** First compare the two rule contracts, context
handling, traversal/fixed-point semantics, premise collection and validation
path. Investigate them as proof-production designs within cvc5's pipeline;
Elaphros does not adopt a new calculus or change the proof contract silently.
Later measure congruence/transitivity nodes, term visits, conversion attempts,
fallbacks and total production plus external checking. A missing checker rule
is unsupported output, not a speedup.

**Risk / value.** High / high potential. The representation could affect many
theories, but correctness and checker compatibility are broader than a small
postprocessor patch.

## E4 Rewrite dependencies

**Question.** Can a parent rewrite be proved without reproducing rewrites of
children that do not affect its result?

**Code.** [`rewriteDep`][rewriteDep] adds `convertMinimizedRewrite` before the
ordinary proof-producing rewrite path. It probes replacing a child by a
purification symbol, retains the replacement if the final rewrite result is
unchanged, builds the smaller proof, and substitutes the original terms back
through its steps. It also adds a shared substitution-cache interface. That
minimization helper is absent from pinned main.

**Controls and next evidence.** No dedicated mainline option. First specify
which dependencies the probing algorithm can remove and how the translated
proof preserves binding and assumptions. Later compare saved reconstruction
against extra rewriting probes and proof translation. Useful counters include
probes, invariant-child successes, original/minimized term sizes and
reconstruction calls avoided. Input-level unrewriting (E1) is not a substitute
for this experiment: E4 acts inside individual rewrite obligations.

**Risk / value.** Medium to high / high potential. It attacks wasted work
directly, but discovering irrelevance may itself be expensive.

## E5 Proof DAG simplification and sharing

**Question.** What should be simplified or merged before expanding a proof
node, and how much does recognizing that opportunity cost?

**Code.** Main already has `--proof-pp-merge` (declared default true),
`--proof-pre-simp-lookahead=N` (2), result caching and scope-aware handling.
Its presimplifier handles `AND_ELIM` over `AND_INTRO`, double symmetry and a
bounded search for a descendant with the same conclusion.
[`pfTrustId`][pfTrustId] contains that history **and extra TRANS simplification**;
[`cpcDevChainMRes`][cpcDevChainMRes] also removes round trips in transitivity
chains and combines consecutive congruence steps. The latter TRANS case is
absent from pinned main's presimplifier. Thus neither bundle is accurately
classified as wholly new or wholly landed.

[`freeAsumpMerge`][freeAsumpMerge] is relevant scope/assumption-cache history;
main already has related machinery. [`pfpUpdate-0417`][pfpUpdate] has its main
changes present upstream: the macro-expansion histogram, `addExpandStep`, and
the final trusted-step scan. Its helper explicitly still calls expansion
recursively; the comment about a more aggressively merged alternative is not
an implementation of that alternative.

**Controls and next evidence.** Start with a mechanism-by-mechanism delta,
especially the additional TRANS/CONG simplification. Later compare lookahead
and merge policies with scope-safe simplification held constant; count visits,
cache hits, discarded expansions, duplicate results, and exclusive live nodes.
Final DAG size alone misses temporary allocations and traversals. Do not
attribute all of the large `pfTrustId` history to this optimization.

**Risk / value.** Medium to high / high potential. Shared mutable proof nodes,
open assumptions and cycles make a superficially local change sensitive.

## E6 Recorded rewrite provenance

**Question.** How much reconstruction search can be replaced by remembering
the rule that the solver already applied?

**Code.** [`rdbExec`][rdbExec] compiles selected `:exec` RARE rules into rewrite
code and records a rule ID. Its DSL postprocessor attempts that rule directly,
reconstructs its conditions and otherwise falls back to search. It moves DSL
reconstruction before subtype elimination so recorded terms still match.
This executable-rule/provenance path is absent from pinned main.

**Controls and next evidence.** Separate three ideas: generated rewriting,
recording its explanation, and direct reconstruction from the record. A
whole-branch comparison changes the solver's rewriter as well as proof work.
First map the marked rules, the information retained for them, condition
reconstruction, fallback and subtype handling. Later isolate recording cost,
direct reconstruction success, search avoided and changes in ordinary solving.
Remaining trusted conditions must still be discharged under the same contract.

**Risk / value.** High / high potential. This could avoid rediscovering
reasoning, but the branch is an architecture prototype spanning 29 source
files. Reusing selected existing rules for proof attribution is within this
project; discovering new rewrite rules remains Metagraphe's question.

## E7 Reconstruction cache and search policy

**Question.** Are repeated evaluation and unsuccessful reconstruction attempts
more expensive than the proof steps eventually emitted?

**Code.** [`rareOptEval`][rareOptEval] has a one-file effective delta: it stops
clearing `d_evalCache` at each `RewriteDbProofCons::prove` call. Main still
clears it. [`rpcAlwaysPre`][rpcAlwaysPre] promotes `POST_DSL` theory rewrites
to `PRE_DSL`, but **inherits `proofDisable`'s diagnostic switches**.
[`smtPpBasicRewriteOnly`][smtPpBasicRewriteOnly] limits one trusted-step recovery
attempt to ordinary rewriting instead of extended rewriting.
[`rareNoEvalPremise`][rareNoEvalPremise] changes the reconstruction of evaluation
premises and several theory rewrites; it is not merely a cache option.

**Controls and next evidence.** Main declares
`--proof-rewrite-rcons-rec-limit=5` and
`--proof-rewrite-rcons-step-limit=1000`, plus `dsl-rewrite` and
`dsl-rewrite-strict` granularity choices. These are reconstruction-policy
controls, not licenses to leave holes. First isolate each effective patch and
audit the cache's keys, lifetime and memory bound. Later record evaluations,
reuse, cache size, attempts, successes, resource-limit failures and residual
trust. Reject a faster result obtained by failing to reconstruct required work.

**Risk / value.** Cache change: medium / uncertain but cheaply testable later.
Ordering changes: medium / potentially broad. One removed cache clear can
retain substantial memory, so source size is not a risk estimate.

## E8 Resolution construction and internal checking

**Question.** Does checking a resolution chain repeatedly rebuild or scan an
intermediate clause that could be processed more directly?

**Code.** [`chainMResOpt`][chainMResOpt] replaces repeated intermediate-vector
elimination with pending-pivot counts and a surviving-literal set in
`CHAIN_M_RESOLUTION` checking. Main still contains the older vector loop.
This is distinct from [`cpcDevChainMRes`][cpcDevChainMRes]'s broader
postprocessing work. [`pfrDev`][pfrDev] is another mixed rule-implementation
prototype, useful background rather than an isolated experiment.

**Controls and next evidence.** Main declares `--proof-chain-m-res=true`,
`--opt-res-reconstruction-size=true` and `--proof-check=none`. The last does
**not** imply that the checker is never called: `ProofNodeManager` may need it
to compute an unspecified conclusion, and reconstruction calls `checkDebug`
directly. First map the calls reaching this rule under the intended production
configuration. Later separate ordinary construction from optional eager/lazy
validation, record chain lengths and literal visits, and validate repeated
pivots, singleton/OR ambiguity and duplicate-literal cases.

**Risk / value.** Medium / uncertain. A small, recent patch makes a good narrow
candidate, but only exercised checker calls can save production time. External
checker optimization is outside Elaphros's scope.

## E9 Definitions and proof output

**Question.** Can definitions and term sharing survive through the proof
pipeline without expensive expansion and re-encoding?

**Code.** [`pf-defineFun`][defineFun] adds `--proof-define-fun-macros`, tracks
original assertions and handles definitions in output and assumption
connections. [`pf-defineFun-printerOnly`][defineFunPrinter] descends from it but
moves the effective approach toward a `MacroDefConverter` in proof output.
These are alternatives, not two independent effects. The option is absent
from pinned main. Main already provides `--proof-dag-global` (true),
`--proof-prune-input` (false), and format-specific printing/conversion paths.

**Controls and next evidence.** First specify how each variant connects the
same original assertions and definitions to the checked refutation. Select
definition-heavy inputs only as a proposed stratum until the corpus is fixed.
Later separate proof construction, term conversion/letification, output bytes,
I/O and checker time. Pin the output destination and its handling. Smaller
files do not establish faster production or identical proof obligations.

**Risk / value.** Medium to high / workload dependent. Public tips are recent,
but scope, defined functions and external checker interpretation matter.

## E10 Lazy bookkeeping and theory reconstruction

**Question.** Which proof objects must survive search, and which explanations
can be built once, only when needed?

**Code.** [`theoryEngineLazyProofs`][theoryEngineLazyProofs] replaces several uses
of a common lazy proof with separately allocated `LazyCDProof` objects in a
`CDProofSet`. It is from 2021; it does not introduce laziness to a solver that
lacks it. Main already has lazy proof generators and fresh proofs in some
explanation paths. The meaningful comparison concerns ownership, retention and
reconstruction, not an eager-versus-lazy slogan.

The theory-specific leads include
[`stratifiedStrIpc`][stratifiedStrIpc]'s two-stage substitution construction,
[`stringsIpcRefactor`][stringsIpcRefactor]'s contextual substitutions and
`stringsIpcAgg`/`stringsIpcAgg2` reconstruction alternatives. These require a
strings stratum; they cannot be inferred from Heuresis's quantified corpus.

**Controls and next evidence.** First map generator ownership and context
lifetimes, then identify which strings variants are still distinct from main.
Later measure generator calls, retained proof nodes, allocation/peak memory,
substitution passes and reconstruction coverage. Per-conflict objects may
increase allocation cost even if they simplify dependencies.

**Risk / value.** High / unknown until attribution. Old interfaces and
backtracking-sensitive ownership make a broad rebase an unattractive first
step; preserve the idea and isolate the needed mechanism.

## E11 Incremental output and reuse

**Question.** Can related queries share proof declarations and state without
paying repeated setup/printing costs or retaining dead scopes?

**Code.** [`ai-pfIncremental`][aiPfIncremental] extends the CPC logger and printer
with scoped incremental output, push/pop notifications, and handling of
incremental `dump-proofs`. Main has proof logging, including the older
`pfLogInferface` lineage, but its defaults still reject `proof-log` combined
with incremental solving. This restriction is about that logging mode; it is
not a claim that all incremental proof retrieval is unsupported.

**Controls and next evidence.** This rises in priority only if real query
sessions are in scope. First specify the session output/checker contract and
the behavior of push/pop, reset, assumptions and mixed SAT/UNSAT/unknown
queries. Later compare whole sessions, peak retained state, repeated
declarations and every required refutation. Splitting sessions into independent
files removes precisely the reuse being studied.

**Risk / value.** High / potentially high for incremental clients, unmotivated
for a corpus of unrelated single queries.

## E12 Proof-induced search changes

**Question.** How much of the overhead comes from changes in solving rather
than from constructing the proof of the same search?

**Code.** Pinned [defaults][defaults] make full proof production select internal
bit-blasting unless explicitly overridden, affect nonlinear covering settings,
and reject some combinations such as lemma inprocessing and deep restarts.
Strict proof mode adds further restrictions. An unspecified granularity is
promoted to `dsl-rewrite` when full proofs are requested, despite the option
declaration's `macro` default. Effective configuration is part of the baseline.
[`ai-macroPf`][aiMacroPf] is an adjacent proof-support proposal; availability
of a proof-capable feature is not evidence that using it improves this corpus.

**Comparison design, for later.** Specify ordinary solving, an ordinary run
with matched proof-compatible solving choices, proof-enabled solving without
extracting a final proof, and full proof extraction/output. Keep internal
checking policy explicit; external checking is a separate measured stage.
The matched arm distinguishes configuration penalties where matching is
possible. It does not guarantee identical search or a disjoint decomposition
by subtraction. Compare effective SAT/BV backends instead of assuming proof
mode always forces a particular SAT solver.

**Risk / value.** Low source-audit risk / high information value. This is a
baseline prerequisite, not a proposed optimization or a return to general
solver tuning.

## Attribution before an experiment queue

Useful counters already present in source include
`ProofPostprocessCallback::macroExpandCount`,
`RewriteDbProofCons::totalInputs`, `totalAttempts`, `totalInputSuccess`,
`ProofCheckerStatistics::totalRuleChecks`, and final-proof rule/trust
histograms. Their source definitions are starting points, not observed data.
An attempt count does not measure time, and final nodes do not count all
temporary proof construction. Dedicated, non-overlapping timings for every
phase above have not been established by this audit.

[`proofDisable`][proofDisable] replaces selected parts with trusted/opaque
steps; `rpcAlwaysPre` inherits those switches. Such ablations may inform later
attribution but do not produce equivalent validated outputs. They do not
necessarily remove the production cost either: the SAT replacement happens
after fetching the SAT proof. Record exactly which work is bypassed, rather
than interpreting the switch name as a timer boundary.

## Reading that frames the questions

- [Flexible Proof Production in an Industrial-Strength SMT Solver
  (IJCAR 2022)](https://u.cs.biu.ac.il/~zoharyo1/ijcar22-proofs.pdf): the
  architecture of eager/lazy production and reconstruction; useful context
  for E2, E3, E5 and E10, not a measurement of today's branches.
- [Reconstructing Fine-Grained Proofs of Rewrites Using a Domain-Specific
  Language (FMCAD 2022)](https://cs.stanford.edu/~niemetz/publications/2022/NoetzliBNPRBT-FMCAD22.pdf):
  reconstruction from a rule database, the starting contrast for recording
  applied-rule provenance in E6 and changing search in E7.
- [IsaRare: Automatic Verification of SMT Rewrites in Isabelle/HOL
  (TACAS 2024)](https://theory.stanford.edu/~barrett/pubs/LFA%2B24-abstract.html):
  distinguishes checking an application from validating the rewrite rules
  themselves. It informs the proof contract; Elaphros does not take over that
  verification project.
- [cvc5 proof-production documentation](https://cvc5.github.io/docs-ci/docs-main/proofs/proofs.html):
  format and API entry point, read on 2026-09-18. Pin the implementation,
  specification and checker before any measurement.

[main]: https://github.com/cvc5/cvc5/tree/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0
[defaults]: https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/smt/set_defaults.cpp
[unrewrite]: https://github.com/ajreynol/cvc5/tree/unrewrite
[unrewrite2]: https://github.com/ajreynol/cvc5/tree/unrewrite2
[reduceTransform]: https://github.com/ajreynol/cvc5/tree/reduceTransform
[pfrConvert]: https://github.com/ajreynol/cvc5/tree/pfrConvert
[pfrConvert2]: https://github.com/ajreynol/cvc5/tree/pfrConvert2
[rewriteDep]: https://github.com/ajreynol/cvc5/tree/rewriteDep
[cpcDevChainMRes]: https://github.com/ajreynol/cvc5/tree/cpcDevChainMRes
[pfTrustId]: https://github.com/ajreynol/cvc5/tree/pfTrustId
[freeAsumpMerge]: https://github.com/ajreynol/cvc5/tree/freeAsumpMerge
[pfpUpdate]: https://github.com/ajreynol/cvc5/tree/pfpUpdate-0417
[rdbExec]: https://github.com/ajreynol/cvc5/tree/rdbExec
[rareOptEval]: https://github.com/ajreynol/cvc5/tree/rareOptEval
[rpcAlwaysPre]: https://github.com/ajreynol/cvc5/tree/rpcAlwaysPre
[smtPpBasicRewriteOnly]: https://github.com/ajreynol/cvc5/tree/smtPpBasicRewriteOnly
[rareNoEvalPremise]: https://github.com/ajreynol/cvc5/tree/rareNoEvalPremise
[chainMResOpt]: https://github.com/ajreynol/cvc5/tree/chainMResOpt
[pfrDev]: https://github.com/ajreynol/cvc5/tree/pfrDev
[defineFun]: https://github.com/ajreynol/cvc5/tree/pf-defineFun
[defineFunPrinter]: https://github.com/ajreynol/cvc5/tree/pf-defineFun-printerOnly
[theoryEngineLazyProofs]: https://github.com/ajreynol/cvc5/tree/theoryEngineLazyProofs
[stratifiedStrIpc]: https://github.com/ajreynol/cvc5/tree/stratifiedStrIpc
[stringsIpcRefactor]: https://github.com/ajreynol/cvc5/tree/stringsIpcRefactor
[aiPfIncremental]: https://github.com/ajreynol/cvc5/tree/ai-pfIncremental
[aiMacroPf]: https://github.com/ajreynol/cvc5/tree/ai-macroPf
[proofDisable]: https://github.com/ajreynol/cvc5/tree/proofDisable
