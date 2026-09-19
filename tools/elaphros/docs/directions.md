# Research directions for proof-production overhead

**Source assessment, 2026-09-18; extended 2026-09-19.** These sixteen
directions start from the [hypothesis register](../notes.md) and the
[public-branch survey](../ledger/2026-09-18-branch-survey.md). No performance
effect is measured. The [queue](todo.md) separates the agent's priorities from
maintainer guidance.

**Two provenances.** E1–E12 are branch-derived: each starts from code someone
already wrote on `ajreynol/cvc5`, so together they map what has been *tried*,
not where the cost is. E13–E16 come instead from the 2026-09-19 [pipeline
audit][audit] of pinned main and have **no branch behind them**; they are
mechanisms visible in the current source that no surveyed branch addresses.
Neither provenance is evidence of a performance effect, but they fail
differently: a branch-derived direction inherits an author's judgment that the
idea was worth prototyping, while an audit-derived one has not had even that
filter applied to it.

Source comparisons use upstream [main at `3dcc1ef542`][main]. Fork branches use
`ajreynol:NAME` and link to living branches for navigation; their **audited tips,
merge bases and source deltas are pinned in the survey**. A feature found on main is not
evidence that the old fork tip was merged verbatim. Buildability and proof
validity have not been tested.

**Effort levels.** As in Heuresis, each direction has two color-coded axes:
*Risk* runs 🟢 Low → 🟡 Medium → 🔴 High and combines implementation size,
architectural reach, correctness exposure and regression risk. *Gain* runs
🔴 Low → 🟡 Medium → 🟢 High and estimates project value if the hypothesis is
right: time or memory saved, or an important uncertainty resolved. The
argument after each rating matters more than the badge. These are qualitative
priors, not measured gains or estimates of their probability; the corpus and
attribution can change them.

**Managing the risk.** Each direction names a bounded first investigation and
the evidence that would justify expanding it or reducing its priority. Keep
changes with distinct mechanisms separate, retain the same proof contract and
count the proposed optimization's own cost. High potential gain does not
justify a broad rebase before the relevant cost is established. All proposed
measurements below remain future work; the current phase is planning only.

## The map

| part of the problem | directions | distinguishing question |
| --- | --- | --- |
| Avoid unnecessary proof work | E1–E4 | Can we avoid a justification, reduce its dependencies, or represent it compactly? |
| Process the necessary proof efficiently | E5–E8, E16 | Can sharing, provenance, caching or better rule algorithms reduce the work? |
| Retain and emit proofs efficiently | E9–E11, E14–E15 | Which representation, lifetime and session costs can be avoided? |
| Make the comparison interpretable | E12–E13 | Did proof mode change the solving problem or available algorithms, and where does the cost fall? |

The first four directions are related but distinct. **Unrewriting** changes
which atom representation the refutation uses. **Macro decomposition** reduces
a large obligation to small local ones. **Compact conversion** changes how a
necessary equality derivation is represented. **Dependency minimization** avoids
justifying child rewrites irrelevant to the final result. A combined branch
cannot tell us which mechanism matters.

## E1 Unrewriting

**Effort.** 🔴 High Risk / 🟢 High Gain — eliminating entire rewrite
justifications could save substantial work, but atom collisions,
theory-sensitive rules and scopes put correctness at risk.

**Question.** Can a refutation keep an atom in its original form and omit its
rewrite proof when the Boolean reasoning does not depend on the rewritten
form? This is a maintainer-highlighted research direction.

**Code.** [`ajreynol:unrewrite`][unrewrite] adds `--proof-unrewrite`, connects preprocessing
proofs, and classifies atoms occurring in input-derived versus theory lemmas.
Its converter callback has an empty body; the tip is a sketch, not an
established implementation. [`ajreynol:unrewrite2`][unrewrite2] descends from it and adds
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

**Manage the risk.** Begin with a precisely specified input-only transformation
and a fallback to the original proof. Expand to theory atoms or earlier
placement only after their proof obligations are understood. Later compare
exclusive work saved with analysis/replay cost; if only output or checker cost
falls, retain that narrower result and lower the production-time expectation.

## E2 Smaller macro obligations

**Effort.** 🟡 Medium Risk / 🟢 High Gain — local decomposition could avoid
full-formula elaboration without redesigning the pipeline. Recursive
obligations, speculative checks and lost DAG sharing can still cause regressions.

**Question.** Must a macro that transforms one large formula into another
reconstruct rewriting throughout both formulas, when only a few parts change?

**Code.** [`ajreynol:reduceTransform`][reduceTransform] intercepts
`MACRO_SR_PRED_INTRO` and `MACRO_SR_PRED_TRANSFORM`. It decomposes conjunctions,
uses conversion conditions to isolate changed subterms, reuses matching
premises, and uses transitivity when two equalities share a side. A conceptual
case is transforming `(and G H1)` into `(and G H2)` by retaining `G` and proving
the local change. This is an explanation of the mechanism, not a run result.
The implementation is confined to two postprocessor source files, but adds
recursive obligations and internal rule checks. Related code in
[`ajreynol:cpcDevChainMRes`][cpcDevChainMRes] also tries polynomial-normalization rules.
The specific reduction helpers are absent from pinned main.

**Controls and next evidence.** There is no dedicated mainline switch for this
decomposition. Existing granularity controls change which macros are expanded;
using a coarser output is not an equivalent optimization. First enumerate each
decomposition and its fallback, distinguish code shared with the larger CPC
branch, and identify the current equivalent insertion points. Later count
macro sizes, changed versus unchanged subterms, successful reductions, failed
checks, and expansion work saved under identical output requirements.

**Manage the risk.** Separate conjunction, equality and congruence reductions
and preserve the ordinary expansion fallback for each. Promote the cases whose
avoided expansion outweighs failed decomposition and extra checking; reduce
priority if large macros mostly change throughout or already share their work.

## E3 Compact term conversion

**Effort.** 🔴 High Risk / 🟢 High Gain — compact conversion could reduce
proof scaffolding across many theories. Rule semantics, context handling and
external checker compatibility make this broader than a postprocessor patch.

**Question.** Can a checked conversion step replace long congruence and
transitivity derivations? This is the other maintainer-highlighted direction.

**Code.** [`ajreynol:pfrConvert`][pfrConvert] adds `--proof-use-convert`, a `CONVERT` rule,
and context-sensitive changes inside `TConvProofGenerator`.
[`ajreynol:pfrConvert2`][pfrConvert2] is a distinct design, **not a descendant of the
first audited tip**: it adds `--proof-use-rule-convert`, `CONVERT` and
`CONVERT_FIXED_POINT`, and a checker that applies pre/post rewrite maps while
recording used premises. These switches and the proposed conversion rules are
absent from pinned main. The old ALF printer changes do not establish current
CPC/checker support.

**Critical timing distinction.** In `ajreynol:pfrConvert2`, the ordinary internal
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

**Manage the risk.** Specify the rule and validation path before choosing a
branch design. Keep compact representation and direct compact construction as
separate proposals, with an expanded-proof fallback. Lower the production-time
expectation if the ordinary conversion still dominates; record any size or
checking benefit separately.

## E4 Rewrite dependencies

**Effort.** 🔴 High Risk / 🟢 High Gain — avoiding irrelevant child proofs
could remove substantial reconstruction, but discovering dependencies adds
rewriting and translating proofs must preserve binding and assumptions.

**Question.** Can a parent rewrite be proved without reproducing rewrites of
children that do not affect its result?

**Code.** [`ajreynol:rewriteDep`][rewriteDep] adds `convertMinimizedRewrite` before the
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

**Manage the risk.** Start with one rewrite shape and bound its probing work,
falling back when minimization is inconclusive. Expand only if avoided
reconstruction exceeds probing and translation costs; few removable
dependencies or expensive unsuccessful probes would lower this priority.

## E5 Proof DAG simplification and sharing

**Effort.** 🔴 High Risk / 🟢 High Gain — simplifying before expansion can
avoid work throughout the proof DAG. Shared mutable nodes, open assumptions
and cycles make even small transformations sensitive.

**Question.** What should be simplified or merged before expanding a proof
node, and how much does recognizing that opportunity cost?

**Code.** Main already has `--proof-pp-merge` (declared default true),
`--proof-pre-simp-lookahead=N` (2), result caching and scope-aware handling.
Its presimplifier handles `AND_ELIM` over `AND_INTRO`, double symmetry and a
bounded search for a descendant with the same conclusion.
[`ajreynol:pfTrustId`][pfTrustId] contains that history **and extra TRANS simplification**;
[`ajreynol:cpcDevChainMRes`][cpcDevChainMRes] also removes round trips in transitivity
chains and combines consecutive congruence steps. The latter TRANS case is
absent from pinned main's presimplifier. Thus neither bundle is accurately
classified as wholly new or wholly landed.

[`ajreynol:freeAsumpMerge`][freeAsumpMerge] is relevant scope/assumption-cache history;
main already has related machinery. [`ajreynol:pfpUpdate-0417`][pfpUpdate] has its main
changes present upstream: the macro-expansion histogram, `addExpandStep`, and
the final trusted-step scan. Its helper explicitly still calls expansion
recursively; the comment about a more aggressively merged alternative is not
an implementation of that alternative.

**Controls and next evidence.** Start with a mechanism-by-mechanism delta,
especially the additional TRANS/CONG simplification. Later compare lookahead
and merge policies with scope-safe simplification held constant; count visits,
cache hits, discarded expansions, duplicate results, and exclusive live nodes.
Final DAG size alone misses temporary allocations and traversals. Do not
attribute all of the large `ajreynol:pfTrustId` history to this optimization.

**Manage the risk.** Isolate a single additional TRANS/CONG transformation
from the mixed branches and document the scopes in which sharing is valid.
Broaden only when exclusive expansions avoided exceed traversal/allocation
costs. A smaller final DAG with unchanged temporary work weakens the expected
production gain.

## E6 Recorded rewrite provenance

**Effort.** 🔴 High Risk / 🟢 High Gain — recorded rule identities could
replace expensive reconstruction search, but generated rewriting, retained
provenance and subtype-pass ordering change several parts of the pipeline.

**Question.** How much reconstruction search can be replaced by remembering
the rule that the solver already applied?

**Code.** [`ajreynol:rdbExec`][rdbExec] compiles selected `:exec` RARE rules into rewrite
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

**Manage the risk.** Restrict the initial design to a small set of existing
rules and separate execution, recording and reconstruction changes in the
29-file prototype. Expand only when direct reconstruction saves more than
recording costs and leaves no new proof holes. Frequent fallback or benefits
explained by ordinary solver changes reduce this direction's priority.
Discovering new rewrite rules remains Metagraphe's question.

## E7 Reconstruction cache and search policy

**Effort.** 🟡 Medium Risk / 🟡 Medium Gain — cache reuse and better attempt
ordering offer contained candidates, but their benefit depends on repetition
and failed search. Memory retention and reconstruction coverage are the risks.

**Question.** Are repeated evaluation and unsuccessful reconstruction attempts
more expensive than the proof steps eventually emitted?

**Code.** [`ajreynol:rareOptEval`][rareOptEval] has a one-file effective delta: it stops
clearing `d_evalCache` at each `RewriteDbProofCons::prove` call. Main still
clears it. [`ajreynol:rpcAlwaysPre`][rpcAlwaysPre] promotes `POST_DSL` theory rewrites
to `PRE_DSL`, but **inherits `ajreynol:proofDisable`'s diagnostic switches**.
[`ajreynol:smtPpBasicRewriteOnly`][smtPpBasicRewriteOnly] limits one trusted-step recovery
attempt to ordinary rewriting instead of extended rewriting.
[`ajreynol:rareNoEvalPremise`][rareNoEvalPremise] changes the reconstruction of evaluation
premises and several theory rewrites; it is not merely a cache option.

**Controls and next evidence.** Main declares
`--proof-rewrite-rcons-rec-limit=5` and
`--proof-rewrite-rcons-step-limit=1000`, plus `dsl-rewrite` and
`dsl-rewrite-strict` granularity choices. These are reconstruction-policy
controls, not licenses to leave holes. First isolate each effective patch and
audit the cache's keys, lifetime and memory bound. Later record evaluations,
reuse, cache size, attempts, successes, resource-limit failures and residual
trust. Reject a faster result obtained by failing to reconstruct required work.

**Manage the risk.** Treat cache lifetime and search ordering independently;
specify a memory bound and exclude inherited diagnostic ablations. Raise the
gain estimate if repeated evaluation or failed attempts dominate. Low reuse,
memory growth or additional unresolved proof obligations would lower it,
regardless of the patch's small size.

## E8 Resolution construction and internal checking

**Effort.** 🟡 Medium Risk / 🟡 Medium Gain — a recent one-file change could
reduce repeated clause scans, but only exercised checker calls can save
production time. Pivot and literal-representation corner cases need care.

**Question.** Does checking a resolution chain repeatedly rebuild or scan an
intermediate clause that could be processed more directly?

**Code.** [`ajreynol:chainMResOpt`][chainMResOpt] replaces repeated intermediate-vector
elimination with pending-pivot counts and a surviving-literal set in
`CHAIN_M_RESOLUTION` checking. Main still contains the older vector loop.
This is distinct from [`ajreynol:cpcDevChainMRes`][cpcDevChainMRes]'s broader
postprocessing work. [`ajreynol:pfrDev`][pfrDev] is another mixed rule-implementation
prototype, useful background rather than an isolated experiment.

**Controls and next evidence.** Main declares `--proof-chain-m-res=true`,
`--opt-res-reconstruction-size=true` and `--proof-check=none`. The last does
**not** imply that the checker is never called: `ProofNodeManager` may need it
to compute an unspecified conclusion, and reconstruction calls `checkDebug`
directly. First map the calls reaching this rule under the intended production
configuration. Later separate ordinary construction from optional eager/lazy
validation, record chain lengths and literal visits, and validate repeated
pivots, singleton/OR ambiguity and duplicate-literal cases.

**Manage the risk.** Establish the production call path before prioritizing
the algorithm change, and separate internal construction from optional
validation costs. Long, frequently checked chains would raise the gain
estimate; short or rarely exercised chains would lower it. External checker
optimization remains outside Elaphros's scope.

## E9 Definitions and proof output

**Effort.** 🔴 High Risk / 🟡 Medium Gain — preserving definitions could
reduce conversion and output costs on generated inputs. Assumption connections,
definition scope and checker interpretation raise the risk; gain depends on
the corpus's use of definitions.

**Question.** Can definitions and term sharing survive through the proof
pipeline without expensive expansion and re-encoding?

**Code.** [`ajreynol:pf-defineFun`][defineFun] adds `--proof-define-fun-macros`, tracks
original assertions and handles definitions in output and assumption
connections. [`ajreynol:pf-defineFun-printerOnly`][defineFunPrinter] descends from it but
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

**Manage the risk.** Compare the assertion-tracking and printer variants as
alternatives under one input/definition contract. Promote the direction if
definition expansion or serialization dominates. If the benefit is only fewer
bytes, report it as such and avoid predicting lower construction time.

## E10 Lazy bookkeeping and theory reconstruction

**Effort.** 🔴 High Risk / 🟡 Medium Gain — retention and repeated theory
reconstruction may cost substantial memory or time, but relevance is not yet
attributed. Old interfaces and backtracking-sensitive ownership increase risk.

**Question.** Which proof objects must survive search, and which explanations
can be built once, only when needed?

**Code.** [`ajreynol:theoryEngineLazyProofs`][theoryEngineLazyProofs] replaces several uses
of a common lazy proof with separately allocated `LazyCDProof` objects in a
`CDProofSet`. It is from 2021; it does not introduce laziness to a solver that
lacks it. Main already has lazy proof generators and fresh proofs in some
explanation paths. The meaningful comparison concerns ownership, retention and
reconstruction, not an eager-versus-lazy slogan.

The theory-specific leads include
[`ajreynol:stratifiedStrIpc`][stratifiedStrIpc]'s two-stage substitution construction,
[`ajreynol:stringsIpcRefactor`][stringsIpcRefactor]'s contextual substitutions and
[`ajreynol:stringsIpcAgg`][stringsIpcAgg] and
[`ajreynol:stringsIpcAgg2`][stringsIpcAgg2] reconstruction alternatives. These
require a strings stratum; they cannot be inferred from Heuresis's quantified
corpus.

**Controls and next evidence.** First map generator ownership and context
lifetimes, then identify which strings variants are still distinct from main.
Later measure generator calls, retained proof nodes, allocation/peak memory,
substitution passes and reconstruction coverage. Per-conflict objects may
increase allocation cost even if they simplify dependencies.

**Manage the risk.** Map ownership and lifetimes first, then isolate one
generator path or theory-specific reconstruction case. Promote only where
retention or repeated construction is material; deprioritize a broad rebase if
main already provides the needed behavior or fresh objects merely increase
allocations. Strings variants need an actual strings workload.

## E11 Incremental output and reuse

**Effort.** 🔴 High Risk / 🟢 High Gain — real incremental clients could
avoid repeated setup and output across many queries. Correct scoping, state
lifetime and checker support make this a substantial change; the high gain
estimate is conditional on selecting such sessions.

**Question.** Can related queries share proof declarations and state without
paying repeated setup/printing costs or retaining dead scopes?

**Code.** [`ajreynol:ai-pfIncremental`][aiPfIncremental] extends the CPC logger and printer
with scoped incremental output, push/pop notifications, and handling of
incremental `dump-proofs`. Main has proof logging, including the older
[`ajreynol:pfLogInferface`][pfLogInferface] lineage, but its defaults still reject
`proof-log` combined with incremental solving. This restriction is about that logging mode; it is
not a claim that all incremental proof retrieval is unsupported.

**Controls and next evidence.** This rises in priority only if real query
sessions are in scope. First specify the session output/checker contract and
the behavior of push/pop, reset, assumptions and mixed SAT/UNSAT/unknown
queries. Later compare whole sessions, peak retained state, repeated
declarations and every required refutation. Splitting sessions into independent
files removes precisely the reuse being studied.

**Manage the risk.** Define one complete session contract before extending
reuse across queries, including push/pop, resets and every required refutation.
Promote if shared declarations and repeated setup dominate session cost.
Keep this deferred for unrelated single-query workloads, and count retained
state against any time saved.

## E12 Proof-induced search changes

**Effort.** 🟢 Low Risk / 🟢 High Gain — a source/configuration comparison
can prevent misattributing changed solving behavior to proof construction.
The gain is information needed by every other direction, not a promised
solver speedup.

**Question.** How much of the overhead comes from changes in solving rather
than from constructing the proof of the same search?

**Code.** Pinned [defaults][defaults] make full proof production select internal
bit-blasting unless explicitly overridden, affect nonlinear covering settings,
and reject some combinations such as lemma inprocessing and deep restarts.
Strict proof mode adds further restrictions. An unspecified granularity is
promoted to `dsl-rewrite` when full proofs are requested, despite the option
declaration's `macro` default. Effective configuration is part of the baseline.
[`ajreynol:ai-macroPf`][aiMacroPf] is an adjacent proof-support proposal; availability
of a proof-capable feature is not evidence that using it improves this corpus.

**Comparison design, for later.** Specify ordinary solving, an ordinary run
with matched proof-compatible solving choices, proof-enabled solving without
extracting a final proof, and full proof extraction/output. Keep internal
checking policy explicit; external checking is a separate measured stage.
The matched arm distinguishes configuration penalties where matching is
possible. It does not guarantee identical search or a disjoint decomposition
by subtraction. Compare effective SAT/BV backends instead of assuming proof
mode always forces a particular SAT solver.

**Manage the risk.** Record requested and effective settings separately and
state where matching is impossible. Close this prerequisite with an explicit
comparison design, then revisit it when revisions or proof settings change.
It does not expand into general solver tuning.

## E13 Proof-work accounting

**Effort.** 🟢 Low Risk / 🟢 High Gain — instrumentation changes no proof
obligation, and it supplies the partition on which every other direction's
priority depends. The gain is information needed to rank E1–E16, not a solver
speedup.

**Question.** Which phases of proof production consume the time and memory,
and how much constructed proof material never reaches the final proof?

**Code.** The counters named below under
[attribution](#attribution-before-an-experiment-queue) are attempt and outcome
counts, not phase timers. The [pipeline audit][audit] adds two findings about
the final-proof statistics. `ProofFinalCallback::finalize` is reached only
through `PfManager::checkFinalProof`, whose sole call site is guarded by
`options().smt.checkProofs`; the final rule and trust histograms are therefore
unavailable in a run that does not also enable proof checking. That same
guarded block calls `connectProofToAssertions`, which the proof-retrieval path
calls again, against the method's own stated assumption that it runs once per
unsat response. No counter found distinguishes proof nodes reaching the final
proof from nodes constructed and discarded, and no non-overlapping per-phase
timer partition exists.

**Critical measurement distinction.** Instrumentation that is reachable only
under `--check-proofs` measures a different configuration from the one whose
overhead is in question, and may add postprocessing work rather than only
observing it. Whether that work is in fact performed twice is a code reading
in the audit, not an observation; the first instrumented run should settle it
before any timing comparison relies on those numbers.

**Controls and next evidence.** Establish timer scopes before adding or
subtracting them, following the [profiler
guide](../../../docs/stats-profiler.md#choosing-a-partition). Separate
search-time proof bookkeeping, postprocessing/elaboration, rewrite
reconstruction, conversion, scoping and output, and state which costs the
instrument cannot separate. Add a discarded-work measure — nodes constructed
versus nodes reachable from the final proof — and a peak-memory attribution;
count the instrument's own overhead. Prefer observations available without
enabling checking, and report any that are not.

**Manage the risk.** Build the smallest partition that can distinguish the
three competing explanations: expensive necessary proof, large discarded
proof, and lost solving capability (E12). Do not let the instrument grow into
general profiling infrastructure before an experiment needs it, and do not
report a phase attribution whose scopes overlap.

## E14 Proof node representation and allocation

**Effort.** 🔴 High Risk / 🟡 Medium Gain — mutability is load-bearing in the
postprocessor, so an immutable or shared representation reaches much of the
pipeline. It is the only direction aimed at allocation and memory, which the
charter names as half the subject; the gain estimate is conditional on E13.

**Question.** Terms are hash-consed; proof nodes are not. What do per-call
allocation and the absence of structural sharing cost in memory and time?

**Code.** `ProofNodeManager::mkNode` allocates a fresh
`std::make_shared<ProofNode>` per call, with no uniqueness table found on that
path. The class comment states the reason and names the unbuilt alternative
directly: proof nodes are mutable, "hence this class does not cache the
results of mkNode", and a caching layer over immutable proof nodes "could be
built as an extension or layer on top of this class". The mutability is used:
`ProofPostprocess::process` splices its subtype-converted proof back with
`updateNode`. Main's `--proof-pp-merge` and `--proof-dag-global` govern
merging and printing, which is a different mechanism from construction-time
uniquing. Line anchors are in the [pipeline audit][audit]. No surveyed branch
proposes this; `ajreynol:proofTerm` is a broader proof-as-term prototype, not
an allocation change.

**Controls and next evidence.** Keep three separable changes apart: allocation
strategy for `ProofNode`, construction-time uniquing of immutable nodes, and
the existing merge and DAG options. Measure first — live and total nodes,
duplicate structure, peak RSS, allocator time — since E13's discarded-work
measure bounds what either change can recover. An immutable layer must state
its behavior at every existing `updateNode` site rather than assume there are
few.

**Manage the risk.** Begin with an allocation change that preserves the
current object model and mutation points, and treat uniquing as a separate
later proposal. Promote if allocation or duplicate structure is material.
Reduce priority if merging already captures the available sharing, or if the
mutation sites make an immutable layer equivalent to rewriting the
postprocessor.

## E15 Streaming proof emission

**Effort.** 🔴 High Risk / 🟡 Medium Gain — peak memory could fall if the
final proof need not coexist with its output, but scoping, letification and
the checker's input contract constrain what may be emitted early. The gain is
conditional on peak memory being a binding cost on the corpus.

**Question.** Must the whole final proof be materialized before any part of it
is emitted?

**Code.** The pipeline materializes: the prop-engine proof is connected and
postprocessed by `PfManager::connectProofToAssertions`, scoped, then printed.
`--proof-log` streams at the SAT layer through `ProofLogger`, which calls
`connectProofToAssertions` per logged component; the `ajreynol:pfLogInferface`
lineage is that feature's history and E11 covers its incremental use. Whole-
pipeline streaming is absent from main and from the surveyed branches. The
[audit][audit] identifies the first obstacle in the Eo/CPC path: `EoPrinter`
runs the proof twice by construction, passing it through `EoPrintChannelPre`
to compute letification and the variable set before printing.

**Controls and next evidence.** Specify the output contract first: whether the
pinned checker accepts a proof whose let bindings and declarations arrive
incrementally, and what a partially emitted proof means if the run is then
interrupted. Main already rejects `--proof-log` with incremental solving,
which is a fact about that logging mode and not about streaming in general.
Later separate peak memory from total allocation and from output bytes, which
is E9's subject. Reordering output without reducing live nodes is not this
direction.

**Manage the risk.** Treat the two-pass letification requirement as the
gating question and answer it before designing an emission schedule. Keep
this distinct from E14: cheaper nodes and fewer simultaneously live nodes are
different mechanisms and should not be bundled into one measurement. Reduce
priority if the postprocessed proof must be complete for the chosen format
anyway.

## E16 Traversal fusion

**Effort.** 🟡 Medium Risk / 🟡 Medium Gain — the passes are identifiable and
fusing them changes no proof obligation, but each exists for a reason, and
their per-node work may be small beside elaboration.

**Question.** How many times is the proof walked between the prop-engine proof
and the emitted output, and how much of that is separable bookkeeping?

**Code.** Verified at the pin by the [audit][audit]. Inside
`ProofPostprocess::process`: the updater pass always runs; under
`--proof-elim-subtypes` a `ProofNodeConverter` builds a converted proof and
splices it back with `updateNode`; when trusted-rule elimination is
configured, `expr::getSubproofRules` scans for the remaining trusted steps
before reconstruction. The Eo/CPC printer then walks the proof twice. Other
traversals are gated rather than default: `pfgEnsureClosed*` returns
immediately unless eager checking or its trace is on, the final-callback
traversal runs only under `--check-proofs`, and `proof_letify` belongs to the
LFSC path. Fusion candidates must therefore be identified in the configuration
actually measured.

**Controls and next evidence.** Count traversals and per-node visits in a
production build under the intended configuration, not in a debug build with
traces on; traversal count is not traversal cost. Separate passes that could
ride along with an existing walk, such as a scan for remaining trusted steps,
from passes that rebuild the proof, such as the subtype converter. Record what
each fused pass observed and whether the order of effects is preserved. Fusing
two cheap walks while elaboration dominates is a measurable non-result worth
recording.

**Manage the risk.** Establish visit counts before changing any pass, then
fuse a single pair whose combination demonstrably preserves the current order
of effects, keeping the separate passes available for comparison. Deprioritize
if visits are few or per-node work is dominated by the updater's own
elaboration.

## Attribution before an experiment queue

Useful counters already present in source include
`ProofPostprocessCallback::macroExpandCount`,
`RewriteDbProofCons::totalInputs`, `totalAttempts`, `totalInputSuccess`,
`ProofCheckerStatistics::totalRuleChecks`, and final-proof rule/trust
histograms. Their source definitions are starting points, not observed data.
An attempt count does not measure time, and final nodes do not count all
temporary proof construction. Dedicated, non-overlapping timings for every
phase above have not been established by this audit.

The final-proof histograms carry a further condition established by the
[pipeline audit][audit]: they are produced by `ProofFinalCallback::finalize`,
which is reached only through a call site guarded by
`options().smt.checkProofs`. They are not free observations of an
unchecked proof-producing run, and requesting them changes the configuration
being measured. [E13](#e13-proof-work-accounting) treats that coupling, and
the absence of any discarded-work measure, as the instrumentation gap to close
before the queue below can be ordered by cost rather than by readiness.

[`ajreynol:proofDisable`][proofDisable] replaces selected parts with trusted/opaque
steps; `ajreynol:rpcAlwaysPre` inherits those switches. Such ablations may inform later
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

[audit]: ../ledger/2026-09-19-pinned-main-pipeline-audit.md
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
[stringsIpcAgg]: https://github.com/ajreynol/cvc5/tree/stringsIpcAgg
[stringsIpcAgg2]: https://github.com/ajreynol/cvc5/tree/stringsIpcAgg2
[pfLogInferface]: https://github.com/ajreynol/cvc5/tree/pfLogInferface
[aiPfIncremental]: https://github.com/ajreynol/cvc5/tree/ai-pfIncremental
[aiMacroPf]: https://github.com/ajreynol/cvc5/tree/ai-macroPf
[proofDisable]: https://github.com/ajreynol/cvc5/tree/proofDisable
