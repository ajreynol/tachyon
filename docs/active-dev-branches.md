# Active development branches

**What this is.** Every branch of [`ajreynol/cvc5`](https://github.com/ajreynol/cvc5)
that a tachyon research project calls **active**: which cvc5 commit it carries,
how large it is, and whether it compiles. It is shared ground, so a pass over
the fork — by a person or an agent — can start from one file instead of from
each project's register in turn.

**Active means: named by a proposal row** in some project's research-direction
table. Those registers are authoritative and this file is derived from them,
from the fork, and from a build on the benchmark host. It is **not** a place to
add a branch: a branch earns a row here by first earning a proposal row there.

| project | register | branch proposals | in this file |
| --- | --- | ---: | --- |
| heuresis | [`directions.md`](../tools/heuresis/docs/directions.md#proposals) | 57 | quantifier-performance branches |
| elaphros | [`directions.md`](../tools/elaphros/docs/directions.md#proposals) | 20 | proof-production branches |

**Branches only.** A proposal can also be a change to the default of an option
that already exists on `main`; heuresis records 23 of those. They have no
branch to update and nothing to build, so they live in their register and not
here.

A project that starts keeping proposals adds its rows here; nothing in this file
governs a project, and removing a project's rows changes no claim it makes.
Each row's `direction` links back to the register entry that owns it.

**Every commit is named by sha.** Nothing here says *master* or *main* as a
state, because those are different commits on different days. The same rule
governs heuresis's [`progress.md`](../tools/heuresis/docs/progress.md): *the
exact cvc5 `main` revision, not "current main"*.

**Compiling is not a result.** A branch that builds has not been shown to help,
and two of the branches below compile *because* a merge emptied them. No number
in either project's `± solved` column comes from this file.

## State

**Read 2026-09-22, after a third update pass.** The pin is cvc5
[`1c0b206`](https://github.com/cvc5/cvc5/commit/1c0b2066ce8d6c947f25212af74be705f1c0cbe5) (2026-09-22), which `ajreynol/cvc5` `master`
matched exactly when read — the fork was in sync with upstream, with nothing
between them.

| | |
| --- | --- |
| active branches | **77** — 57 heuresis, 20 elaphros |
| within 11 commits of the pin | **77** (57 heuresis + 20 elaphros) |
| older | **none** — every active branch is within that distance |
| compile-checked | **77 of 77** pass |

Three passes have run: 37 branches on 2026-09-21, 33 more on 2026-09-22, and 58
refreshed again the same day. **Every one was brought up by merging, not by
rebasing** — each current tip is a `Merge branch 'master' into …` commit. That
is enough to build and measure, and `± LOC` is a three-dot diff against the pin,
so it still reports only the branch's own changes. It is not the linear series
an upstream review will ask for.

### Five branches whose own diff is empty, and why

Five branches carry **no changes of their own** against the pin: their
`diff --stat $PIN...BRANCH -- src/` is nothing. They compile perfectly in that
state, which is why the check below reports the diff rather than trusting a
clean build.

**The first reading of this was wrong, and the correction matters.** The obvious
explanation — a merge resolving in favour of upstream and destroying the work —
is not what happened. On four of the five the branch's mechanism is **already in
the pin**: the contribution landed upstream, and an empty own-diff is exactly
what that looks like. The fifth, `bvToIntQuant-031126`, was **superseded** rather
than taken: the pin collects range constraints per uninterpreted-function symbol
through `IntBlaster::addQuantifiedRangeConstraint`, which subsumes the branch's
coarser constraint, and its remaining novelty — extending the quantified path to
`EXISTS` — is unreachable while `int_blaster.cpp` asserts the node is a `FORALL`.
Restoring it as it stands would regress generality.

All five are retired in their registers. **Nothing was lost**, and their
pre-update tips are recorded beside the fork should anyone want to look again.

## The compile check

**Host and toolchain.** The benchmark host, 64 cores, building with
`/usr/bin/gcc10-c++` (GCC 10.5) — the compiler the host's existing cvc5 build
uses; the system default is GCC 7.3, which current cvc5 rejects. The build type
is `unrestricted`: **cvc5 has removed the `production` build type**, and
`configure.sh production` now fails, which is worth knowing before the host's
own build is next reconfigured.

Each branch is checked out at the exact tip recorded here and built with
`make -j48` in one reused build directory, so after the first build each branch
compiles incrementally. A separate clone and build directory are used, so
the host's own checkout and production build — `REPO` and `BUILDDIR` in
[`site.conf`](../job_launcher/site.conf.example) — are left untouched, because
the launcher measures from them.

**What a ✅ means:** the branch's source compiles and links against the pin, in
the time beside it. It does not mean the branch is correct, that its regressions
pass, or that it helps. Only branches within 6 commits of the pin are built; an
older branch would be compiling a cvc5 from years ago, which answers nothing.

**All 77 pass, which is worth distrusting**, so the check was verified rather
than assumed: the binary built from [`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst)
accepts `--eager-inst-limit=5`, and the binary built from the pin rejects it as
an unknown option. The branch's code is in the binary, and each branch is a real
rebuild — 4 to 75 seconds, median 41, against 107 for the pin from scratch.

**The fork moves under this file.** Thirty-three branches changed between the
first pass and this reading, and the pin has moved twice since it was chosen.
Re-derive before acting, naming the commit you derived against:

```bash
git clone --filter=tree:0 --bare https://github.com/ajreynol/cvc5 fork.git
PIN=$(git --git-dir=fork.git rev-parse master)           # name it, then use the sha
git --git-dir=fork.git merge-base $PIN BRANCH            # the commit it carries
git --git-dir=fork.git rev-list --count BRANCH..$PIN     # 0 means it carries the pin
git --git-dir=fork.git rev-list --count $PIN..BRANCH     # its own commits
git --git-dir=fork.git rev-list --parents -n1 BRANCH     # two parents: a merge
git --git-dir=fork.git diff --stat $PIN...BRANCH -- src/ # empty means content was lost
```

## Bringing a branch up to date

1. **Prefer a rebase onto the pin you chose**, keeping the branch's own
   commits. Merging is acceptable and is what all three passes did — it makes
   the branch current, which is what a measurement needs — but record which was
   done and onto which sha, because only one of them leaves a reviewable series.
2. **One branch at a time**, and no unrelated work squashed in.
3. **Check the source diff after every update.** If it has collapsed to
   nothing, or lost the mechanism the direction names, the update dropped
   content — as four merges did. Report it and keep the pre-update tip; do not
   record a small diff as if it were the branch.
4. **Do not force a resolution.** An update that will not come out cleanly is a
   result: report the conflicts. How large and how conflicted it is is part of
   what the proposal costs, and a branch better reimplemented than updated can
   retire its proposal row — which is progress, not failure.
5. **Report, per branch:** new tip, the sha it now carries, diffstat, and
   whether it builds and passes `make regress`.
6. **Then update two places:** the proposal row in the owning project's
   register, and the row here.

## Carrying the pin, or within 11 commits of it — 77 branches

`± LOC` is the three-dot source diff against [`1c0b206`](https://github.com/cvc5/cvc5/commit/1c0b2066ce8d6c947f25212af74be705f1c0cbe5), `src/` only.

| branch | what it does | project | direction | its commits | ± LOC | builds |
| --- | --- | --- | --- | ---: | ---: | :-: |
| <a id="unrewrite2"></a>[`unrewrite2`](https://github.com/ajreynol/cvc5/tree/unrewrite2) | Candidate preimages, replay of renamed proof steps, fallback when replay fails | elaphros | [E1](../tools/elaphros/docs/directions.md#e1-unrewriting) | 14 | +1082/−0 over 10 src files | ✅ 69s |
| <a id="reduceTransform"></a>[`reduceTransform`](https://github.com/ajreynol/cvc5/tree/reduceTransform) | Decomposes a macro obligation to the subterms that actually changed | elaphros | [E2](../tools/elaphros/docs/directions.md#e2-smaller-macro-obligations) | 18 | +324/−1 over 2 src files | ✅ 51s |
| <a id="pfrConvert2"></a>[`pfrConvert2`](https://github.com/ajreynol/cvc5/tree/pfrConvert2) | `--proof-use-rule-convert`, `CONVERT`/`CONVERT_FIXED_POINT` and a checker | elaphros | [E3](../tools/elaphros/docs/directions.md#e3-compact-term-conversion) | 19 | +272/−20 over 7 src files | ✅ 64s |
| <a id="rewriteDep"></a>[`rewriteDep`](https://github.com/ajreynol/cvc5/tree/rewriteDep) | Probes replacing a rewrite's child by a purification symbol to drop dependencies | elaphros | [E4](../tools/elaphros/docs/directions.md#e4-rewrite-dependencies) | 16 | +225/−32 over 6 src files | ✅ 67s |
| <a id="cpcDevChainMRes"></a>[`cpcDevChainMRes`](https://github.com/ajreynol/cvc5/tree/cpcDevChainMRes) | Removes transitivity round trips and combines consecutive congruence steps | elaphros | [E5](../tools/elaphros/docs/directions.md#e5-proof-dag-simplification-and-sharing) | 179 | +522/−1 over 3 src files | ✅ 26s |
| <a id="pfTrustId"></a>[`pfTrustId`](https://github.com/ajreynol/cvc5/tree/pfTrustId) | Extra TRANS simplification over main's presimplifier history | elaphros | [E5](../tools/elaphros/docs/directions.md#e5-proof-dag-simplification-and-sharing) | 1220 | +597/−232 over 24 src files | ✅ 77s |
| <a id="rdbExec"></a>[`rdbExec`](https://github.com/ajreynol/cvc5/tree/rdbExec) | Compiles selected `:exec` RARE rules into rewrite code and records a rule ID | elaphros | [E6](../tools/elaphros/docs/directions.md#e6-recorded-rewrite-provenance) | 19 | +2561/−49 over 29 src files | ✅ 67s |
| <a id="rareOptEval"></a>[`rareOptEval`](https://github.com/ajreynol/cvc5/tree/rareOptEval) | Stops clearing `d_evalCache` at every `RewriteDbProofCons::prove` | elaphros | [E7](../tools/elaphros/docs/directions.md#e7-reconstruction-cache-and-search-policy) | 7 | +1/−2 over 1 src files | ✅ 67s |
| <a id="rpcAlwaysPre"></a>[`rpcAlwaysPre`](https://github.com/ajreynol/cvc5/tree/rpcAlwaysPre) | Promotes `POST_DSL` theory rewrites to `PRE_DSL` | elaphros | [E7](../tools/elaphros/docs/directions.md#e7-reconstruction-cache-and-search-policy) | 12 | +60/−1 over 6 src files | ✅ 65s |
| <a id="rareNoEvalPremise"></a>[`rareNoEvalPremise`](https://github.com/ajreynol/cvc5/tree/rareNoEvalPremise) | Changes reconstruction of evaluation premises and several theory rewrites | elaphros | [E7](../tools/elaphros/docs/directions.md#e7-reconstruction-cache-and-search-policy) | 15 | +3/−3 over 2 src files | ✅ 71s |
| <a id="rareEncodeSubcall"></a>[`rareEncodeSubcall`](https://github.com/ajreynol/cvc5/tree/rareEncodeSubcall) | One stratified search with an on-demand `ENCODE` step, not two full searches | elaphros | [E7](../tools/elaphros/docs/directions.md#e7-reconstruction-cache-and-search-policy) | 6 | +46/−41 over 4 src files | ✅ 67s |
| <a id="chainMResOpt"></a>[`chainMResOpt`](https://github.com/ajreynol/cvc5/tree/chainMResOpt) | Pending-pivot counts and a surviving-literal set in `CHAIN_M_RESOLUTION` checking | elaphros | [E8](../tools/elaphros/docs/directions.md#e8-resolution-construction-and-internal-checking) | 3 | +62/−55 over 1 src files | ✅ 5s |
| <a id="pf-defineFun"></a>[`pf-defineFun`](https://github.com/ajreynol/cvc5/tree/pf-defineFun) | `--proof-define-fun-macros`: tracks definitions through output and assumptions | elaphros | [E9](../tools/elaphros/docs/directions.md#e9-definitions-and-proof-output) | 10 | +698/−60 over 15 src files | ✅ 73s |
| <a id="pf-defineFun-printerOnly"></a>[`pf-defineFun-printerOnly`](https://github.com/ajreynol/cvc5/tree/pf-defineFun-printerOnly) | The same idea moved to a `MacroDefConverter` in proof output | elaphros | [E9](../tools/elaphros/docs/directions.md#e9-definitions-and-proof-output) | 8 | +876/−25 over 11 src files | ✅ 41s |
| <a id="stratifiedStrIpc"></a>[`stratifiedStrIpc`](https://github.com/ajreynol/cvc5/tree/stratifiedStrIpc) | Two-stage substitution construction for strings proof reconstruction | elaphros | [E10](../tools/elaphros/docs/directions.md#e10-lazy-bookkeeping-and-theory-reconstruction) | 2 | +58/−7 over 1 src files | ✅ 42s |
| <a id="stringsIpcRefactor"></a>[`stringsIpcRefactor`](https://github.com/ajreynol/cvc5/tree/stringsIpcRefactor) | Contextual substitutions in strings proof reconstruction | elaphros | [E10](../tools/elaphros/docs/directions.md#e10-lazy-bookkeeping-and-theory-reconstruction) | 17 | +4/−0 over 2 src files | ✅ 40s |
| <a id="stringsIpcAgg"></a>[`stringsIpcAgg`](https://github.com/ajreynol/cvc5/tree/stringsIpcAgg) | A strings reconstruction alternative | elaphros | [E10](../tools/elaphros/docs/directions.md#e10-lazy-bookkeeping-and-theory-reconstruction) | 8 | +72/−4 over 3 src files | ✅ 18s |
| <a id="theoryEngineLazyProofs"></a>[`theoryEngineLazyProofs`](https://github.com/ajreynol/cvc5/tree/theoryEngineLazyProofs) | Separately allocated `LazyCDProof` objects in a `CDProofSet` | elaphros | [E10](../tools/elaphros/docs/directions.md#e10-lazy-bookkeeping-and-theory-reconstruction) | 6 | +32/−29 over 2 src files | ✅ 17s |
| <a id="ai-pfIncremental"></a>[`ai-pfIncremental`](https://github.com/ajreynol/cvc5/tree/ai-pfIncremental) | Scoped incremental CPC output with push/pop notifications | elaphros | [E11](../tools/elaphros/docs/directions.md#e11-incremental-output-and-reuse) | 8 | +365/−23 over 7 src files | ✅ 11s |
| <a id="ai-macroPf"></a>[`ai-macroPf`](https://github.com/ajreynol/cvc5/tree/ai-macroPf) | Proof support for the quantifier-macro preprocessing pass | elaphros | [E12](../tools/elaphros/docs/directions.md#e12-proof-induced-search-changes) | 3 | +118/−45 over 5 src files | ✅ 65s |
| <a id="claude-eagerInst"></a>[`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | Notification-driven eager matcher with generation, pair and per-round budgets | heuresis | [R1](../tools/heuresis/docs/directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 10 | +1449/−8 over 13 src files | ✅ 52s |
| <a id="eagerInst3"></a>[`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | E-matching over a persistent ground trie fed by equality-engine notifications | heuresis | [R1](../tools/heuresis/docs/directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 183 | +3777/−41 over 38 src files | ✅ 55s |
| <a id="ai-extEagerInst3-1"></a>[`ai-extEagerInst3-1`](https://github.com/ajreynol/cvc5/tree/ai-extEagerInst3-1) | `eagerInst3` plus auto-triggers | heuresis | [R1](../tools/heuresis/docs/directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 187 | +4060/−42 over 39 src files | ✅ 11s |
| <a id="eagerQM"></a>[`eagerQM`](https://github.com/ajreynol/cvc5/tree/eagerQM) | A preprocessing-time matching pass | heuresis | [R1](../tools/heuresis/docs/directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 5 | +219/−0 over 8 src files | ✅ 55s |
| <a id="instFullPreempt"></a>[`instFullPreempt`](https://github.com/ajreynol/cvc5/tree/instFullPreempt) | `--inst-when=full-preempt`: instantiate before theory combination runs | heuresis | [R1](../tools/heuresis/docs/directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 5 | +10/−0 over 2 src files | ✅ 54s |
| <a id="ai-emFilter"></a>[`ai-emFilter`](https://github.com/ajreynol/cvc5/tree/ai-emFilter) | `--filter-e-matching`: filters quantified formulas out of E-matching by event | heuresis | [R2](../tools/heuresis/docs/directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 15 | +764/−16 over 20 src files | ✅ 47s |
| <a id="imTrivial"></a>[`imTrivial`](https://github.com/ajreynol/cvc5/tree/imTrivial) | Trivial-trigger matcher that considers only terms not yet seen | heuresis | [R2](../tools/heuresis/docs/directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 14 | +268/−21 over 14 src files | ✅ 51s |
| <a id="imSimpleInc2"></a>[`imSimpleInc2`](https://github.com/ajreynol/cvc5/tree/imSimpleInc2) | The same incremental treatment for `InstMatchGeneratorSimple` | heuresis | [R2](../tools/heuresis/docs/directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 12 | +122/−23 over 4 src files | ✅ 36s |
| <a id="ai-imgDirect"></a>[`ai-imgDirect`](https://github.com/ajreynol/cvc5/tree/ai-imgDirect) | Direct matcher for nested single triggers, excluding failed roots for the round | heuresis | [R2](../tools/heuresis/docs/directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 8 | +707/−4 over 5 src files | ✅ 7s |
| <a id="ai-quantOpt-1"></a>[`ai-quantOpt-1`](https://github.com/ajreynol/cvc5/tree/ai-quantOpt-1) | Candidate caching per pattern arity | heuresis | [R2](../tools/heuresis/docs/directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 6 | +36/−4 over 2 src files | ✅ 6s |
| <a id="emExp"></a>[`emExp`](https://github.com/ajreynol/cvc5/tree/emExp) | Records the context level at which each term entered the database | heuresis | [R2](../tools/heuresis/docs/directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 11 | +124/−2 over 13 src files | ✅ 37s |
| <a id="ai-prepared13"></a>[`ai-prepared13`](https://github.com/ajreynol/cvc5/tree/ai-prepared13) | Caches match failures that are invariant modulo the equality engine | heuresis | [R3](../tools/heuresis/docs/directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | 15 | +290/−6 over 4 src files | ✅ 37s |
| <a id="termOrigin"></a>[`termOrigin`](https://github.com/ajreynol/cvc5/tree/termOrigin) | `--inst-nested-max-level` and a lemma-origin DAG — cvc5's nearest thing to z3's generation | heuresis | [R4](../tools/heuresis/docs/directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | 19 | +478/−11 over 19 src files | ✅ 53s |
| <a id="instLastCallDelay"></a>[`instLastCallDelay`](https://github.com/ajreynol/cvc5/tree/instLastCallDelay) | Skips the last-call check while the valuation still needs one | heuresis | [R4](../tools/heuresis/docs/directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | 5 | +5/−4 over 1 src files | ✅ 49s |
| <a id="dtInstMode"></a>[`dtInstMode`](https://github.com/ajreynol/cvc5/tree/dtInstMode) | `--dt-inst-internal`: send datatype instantiate inferences as lemmas, bypassing `dtPoliteOptimize` | heuresis | [R4](../tools/heuresis/docs/directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | 6 | +14/−1 over 2 src files | ✅ 15s |
| <a id="multiTriggerSingleBase"></a>[`multiTriggerSingleBase`](https://github.com/ajreynol/cvc5/tree/multiTriggerSingleBase) | Uses a single trigger as the base for multi-triggers | heuresis | [R5](../tools/heuresis/docs/directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | 5 | +44/−0 over 3 src files | ✅ 22s |
| <a id="nestedTriggers"></a>[`nestedTriggers`](https://github.com/ajreynol/cvc5/tree/nestedTriggers) | `--nested-triggers`: triggers from terms in nested quantifiers | heuresis | [R5](../tools/heuresis/docs/directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | 6 | +39/−22 over 4 src files | ✅ 15s |
| <a id="simpleTriggerMore"></a>[`simpleTriggerMore`](https://github.com/ajreynol/cvc5/tree/simpleTriggerMore) | Caches the term-arg trie so a simple trigger can be reset onto a candidate equivalence class | heuresis | [R5](../tools/heuresis/docs/directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | 7 | +48/−33 over 2 src files | ✅ 5s |
| <a id="gttOpt"></a>[`gttOpt`](https://github.com/ajreynol/cvc5/tree/gttOpt) | `--gt-trigger-reg`: registers ground subterms of triggers | heuresis | [R5](../tools/heuresis/docs/directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | 6 | +9/−1 over 2 src files | ✅ 43s |
| <a id="ai-cbqi-0423"></a>[`ai-cbqi-0423`](https://github.com/ajreynol/cvc5/tree/ai-cbqi-0423) | Reworks QCF where flattened UF encodings force an exhaustive search | heuresis | [R6](../tools/heuresis/docs/directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | 8 | +136/−87 over 1 src files | ✅ 45s |
| <a id="ievalTravTrie"></a>[`ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) | Evaluator walks term tries as assignments arrive, rejecting infeasible matches earlier | heuresis | [R7](../tools/heuresis/docs/directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 7 | +166/−43 over 8 src files | ✅ 16s |
| <a id="emStratify"></a>[`emStratify`](https://github.com/ajreynol/cvc5/tree/emStratify) | `--e-matching-stratify-ieval` | heuresis | [R7](../tools/heuresis/docs/directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 19 | +180/−27 over 16 src files | ✅ 45s |
| <a id="notifySatClause"></a>[`notifySatClause`](https://github.com/ajreynol/cvc5/tree/notifySatClause) | The SAT deletion callback a real instantiation-lemma GC would need | heuresis | [R9](../tools/heuresis/docs/directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 8 | +49/−10 over 6 src files | ✅ 45s |
| <a id="virtualClauseDel"></a>[`virtualClauseDel`](https://github.com/ajreynol/cvc5/tree/virtualClauseDel) | The first deletion design: instantiation lemmas as virtual clauses | heuresis | [R9](../tools/heuresis/docs/directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 18 | +25/−5 over 9 src files | ✅ 46s |
| <a id="smtLazyAssert"></a>[`smtLazyAssert`](https://github.com/ajreynol/cvc5/tree/smtLazyAssert) | `--smt-lazy-assert`: assert the input incrementally under model guidance, with an and-elim pass | heuresis | [R9](../tools/heuresis/docs/directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 23 | +377/−16 over 15 src files | ✅ 91s |
| <a id="ai-instDefer"></a>[`ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) | `--inst-defer`: records instantiations globally, treats them as local in the heuristic | heuresis | [R10](../tools/heuresis/docs/directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 6 | +116/−32 over 11 src files | ✅ 82s |
| <a id="ai-jhRlvInst"></a>[`ai-jhRlvInst`](https://github.com/ajreynol/cvc5/tree/ai-jhRlvInst) | `--jh-rlv-inst`: activates an instantiation lemma when its quantifier is asserted | heuresis | [R10](../tools/heuresis/docs/directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 7 | +327/−18 over 9 src files | ✅ 49s |
| <a id="ai-jhConflictFirst"></a>[`ai-jhConflictFirst`](https://github.com/ajreynol/cvc5/tree/ai-jhConflictFirst) | `--jh-conflict-first`: prioritises conflict clauses over theory lemmas | heuresis | [R10](../tools/heuresis/docs/directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 6 | +90/−36 over 9 src files | ✅ 17s |
| <a id="claudeDev-dts-idef"></a>[`claudeDev-dts-idef`](https://github.com/ajreynol/cvc5/tree/claudeDev-dts-idef) | `--inst-defer` and `--dt-split-relevant` together | heuresis | [R10](../tools/heuresis/docs/directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 7 | +177/−40 over 13 src files | ✅ 48s |
| <a id="jhRandom"></a>[`jhRandom`](https://github.com/ajreynol/cvc5/tree/jhRandom) | `--jh-rand`: randomised assertion and branch order | heuresis | [R11](../tools/heuresis/docs/directions.md#r11--decision-heuristic-versus-relevancy-what-the-sat-solver-is-made-to-decide-on) | 7 | +262/−20 over 7 src files | ✅ 50s |
| <a id="subConflict"></a>[`subConflict`](https://github.com/ajreynol/cvc5/tree/subConflict) | `--sub-conflict-find`: a subsolver that looks for conflicts | heuresis | [R12](../tools/heuresis/docs/directions.md#r12--lemma-inprocessing-and-conflict-minimisation) | 13 | +328/−1 over 12 src files | ✅ 48s |
| <a id="cadicalPortfolio"></a>[`cadicalPortfolio`](https://github.com/ajreynol/cvc5/tree/cadicalPortfolio) | Makes CaDiCaL the `--sat-solver` default for non-quantified, non-string logics | heuresis | [R13](../tools/heuresis/docs/directions.md#r13--the-sat-backend-cadical-minisat-restarts-units) | 6 | +50/−0 over 1 src files | ✅ 48s |
| <a id="mbtc25"></a>[`mbtc25`](https://github.com/ajreynol/cvc5/tree/mbtc25) | `--tc-mode=model-based`: model-based theory combination; upstream PR #12095 open | heuresis | [R14](../tools/heuresis/docs/directions.md#r14--theory-combination-care-graph-or-model-based) | 35 | +367/−82 over 15 src files | ✅ 44s |
| <a id="ai-eecNoShare"></a>[`ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare) | Skips `propagateSharedEquality` for theories the central engine already explains | heuresis | [R15](../tools/heuresis/docs/directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 6 | +9/−3 over 1 src files | ✅ 43s |
| <a id="dtMergeNotify-v3"></a>[`dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3) | Datatypes under the central equality engine without `notifyFact` | heuresis | [R15](../tools/heuresis/docs/directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 35 | +377/−73 over 10 src files | ✅ 12s |
| <a id="cdno"></a>[`cdno`](https://github.com/ajreynol/cvc5/tree/cdno) | Context-dynamic notify objects | heuresis | [R15](../tools/heuresis/docs/directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 20 | +168/−12 over 5 src files | ✅ 42s |
| <a id="dtSplitRelevant"></a>[`dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant) | `--dt-split-relevant`: splits only on datatype terms in asserted literals | heuresis | [R16](../tools/heuresis/docs/directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 6 | +61/−8 over 2 src files | ✅ 48s |
| <a id="dtElim"></a>[`dtElim`](https://github.com/ajreynol/cvc5/tree/dtElim) | `--dt-elim`: eliminates datatypes at preprocessing, by constructor and field count | heuresis | [R16](../tools/heuresis/docs/directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 28 | +1086/−2 over 13 src files | ✅ 73s |
| <a id="dtLazyInst3"></a>[`dtLazyInst3`](https://github.com/ajreynol/cvc5/tree/dtLazyInst3) | `--dt-lazy-inst`: applies the datatypes instantiate rule lazily | heuresis | [R16](../tools/heuresis/docs/directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 23 | +80/−2 over 3 src files | ✅ 73s |
| <a id="oneConsInst"></a>[`oneConsInst`](https://github.com/ajreynol/cvc5/tree/oneConsInst) | Instantiates single-constructor terms directly | heuresis | [R16](../tools/heuresis/docs/directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 7 | +42/−11 over 2 src files | ✅ 16s |
| <a id="ai-dioLc"></a>[`ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc) | `--dio-solver-last-call`: defers Diophantine conflict detection to last call | heuresis | [R17](../tools/heuresis/docs/directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | 7 | +95/−2 over 6 src files | ✅ 20s |
| <a id="deferBlock"></a>[`deferBlock`](https://github.com/ajreynol/cvc5/tree/deferBlock) | `--defer-block`: holds lemmas back, with arithmetic branch-and-bound hooks | heuresis | [R17](../tools/heuresis/docs/directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | 23 | +336/−17 over 15 src files | ✅ 49s |
| <a id="bitblastLc"></a>[`bitblastLc`](https://github.com/ajreynol/cvc5/tree/bitblastLc) | `--bitblast-lc`: delays bit-blasting to last call | heuresis | [R19](../tools/heuresis/docs/directions.md#r19--bit-vectors-inside-quantified-problems) | 5 | +27/−0 over 2 src files | ✅ 49s |
| <a id="ufConvRlv"></a>[`ufConvRlv`](https://github.com/ajreynol/cvc5/tree/ufConvRlv) | Reduces only relevant terms in the UF conversion solver | heuresis | [R19](../tools/heuresis/docs/directions.md#r19--bit-vectors-inside-quantified-problems) | 6 | +13/−4 over 3 src files | ✅ 15s |
| <a id="ufEagerDistinct"></a>[`ufEagerDistinct`](https://github.com/ajreynol/cvc5/tree/ufEagerDistinct) | `--uf-eager-distinct` | heuresis | [R20](../tools/heuresis/docs/directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | 5 | +25/−0 over 3 src files | ✅ 16s |
| <a id="simplifyRecFun"></a>[`simplifyRecFun`](https://github.com/ajreynol/cvc5/tree/simplifyRecFun) | `--simplify-rec-fun` | heuresis | [R20](../tools/heuresis/docs/directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | 62 | +101/−39 over 11 src files | ✅ 45s |
| <a id="eagerElimDefs"></a>[`eagerElimDefs`](https://github.com/ajreynol/cvc5/tree/eagerElimDefs) | `--eager-elim-defs` | heuresis | [R20](../tools/heuresis/docs/directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | 11 | +70/−15 over 8 src files | ✅ 46s |
| <a id="quantRew-1006"></a>[`quantRew-1006`](https://github.com/ajreynol/cvc5/tree/quantRew-1006) | Constructor equalities in quantifier bodies | heuresis | [R21](../tools/heuresis/docs/directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | 6 | +27/−4 over 1 src files | ✅ 43s |
| <a id="preregRlv"></a>[`preregRlv`](https://github.com/ajreynol/cvc5/tree/preregRlv) | `--preregister-mode=rlv`: preregisters only literals relevance can use; PR #9503 open | heuresis | [R22](../tools/heuresis/docs/directions.md#r22--preregistration-which-literals-the-theories-are-told-about) | 159 | +833/−13 over 9 src files | ✅ 11s |
| <a id="tdbOldIndex"></a>[`tdbOldIndex`](https://github.com/ajreynol/cvc5/tree/tdbOldIndex) | `--tdb-old-index`: prefers old terms in term-database indices | heuresis | [R23](../tools/heuresis/docs/directions.md#r23--term-database-relevance-which-ground-terms-e-matching-may-use) | 9 | +61/−7 over 5 src files | ✅ 50s |
| <a id="lowLevelOptMore"></a>[`lowLevelOptMore`](https://github.com/ajreynol/cvc5/tree/lowLevelOptMore) | Compact constant-factor work from 2019 | heuresis | [R25](../tools/heuresis/docs/directions.md#r25--low-level-engineering-the-constant-factors) | 15 | +72/−8 over 2 src files | ✅ 48s |
| <a id="tdbLLOpts"></a>[`tdbLLOpts`](https://github.com/ajreynol/cvc5/tree/tdbLLOpts) | Signature refactor only: passes the quantifier by const reference through the duplicate tries | heuresis | [R25](../tools/heuresis/docs/directions.md#r25--low-level-engineering-the-constant-factors) | 6 | +38/−34 over 2 src files | ✅ 10s |
| <a id="qdebugStats"></a>[`qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) | E-matching debug statistics and an `AnalyzeEE` module | heuresis | [R26](../tools/heuresis/docs/directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 34 | +536/−15 over 19 src files | ✅ 24s |
| <a id="debugDumpLemmas"></a>[`debugDumpLemmas`](https://github.com/ajreynol/cvc5/tree/debugDumpLemmas) | `--re-check-lemmas` | heuresis | [R26](../tools/heuresis/docs/directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 9 | +50/−0 over 5 src files | ✅ 48s |
| <a id="trackInferId"></a>[`trackInferId`](https://github.com/ajreynol/cvc5/tree/trackInferId) | `--track-lemma-inference-ids` | heuresis | [R26](../tools/heuresis/docs/directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 5 | +22/−3 over 3 src files | ✅ 44s |
| <a id="ai-parserOpt"></a>[`ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt) | Reserved parser stacks, `from_chars`, static token tables, less vector movement | heuresis | [R27](../tools/heuresis/docs/directions.md#r27--smt-lib-parser-throughput-pay-less-before-solving) | 6 | +228/−141 over 7 src files | ✅ 16s |
| <a id="eagerCbqi"></a>[`eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi) | Evaluator-backed eager term database with conflict and propagation modes | heuresis | [R28](../tools/heuresis/docs/directions.md#r28--eager-conflict-based-instantiation-find-a-useful-instance-before-full-effort) | 208 | +5250/−206 over 58 src files | ✅ 74s |

**The columns.** **branch** links to the tip in the fork. **what it does** is one
line, condensed from the account in the owning project's register; *(not
characterised)* marks a branch the register dates but never describes, which is
a gap in the reading rather than a judgement about the branch. **project** and
**direction** say which register owns the proposal, and the direction links to
the entry that carries the argument for it. **its commits** counts what the
branch has that the pin does not, which includes the merge commit that brought
it up to date, so a branch of its own single change reads as 2. **± LOC** is the
three-dot source diff against the pin, `src/` only, so it shows the branch's own
work and not the merge. **builds** is the compile check described above, with
that branch's incremental build time.


## Older than the pin — none

**Every active branch is within reach of the pin**, for the first time since
this list was started. There is no update backlog left; what remains is
measurement.

