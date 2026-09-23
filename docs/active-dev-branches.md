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
| heuresis | [`directions.md`](../tools/heuresis/docs/directions.md#proposals) | 65 | quantifier-performance branches |
| elaphros | [`directions.md`](../tools/elaphros/docs/directions.md#proposals) | 23 | proof-production branches |

**Branches only.** A proposal can also be a change to the default of an option
that already exists on `main`; heuresis records 22 of those. They have no
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
[`10bd5cb`](https://github.com/cvc5/cvc5/commit/10bd5cb3bb9ad9cb10277e0ae54e352e6d2ac345) (2026-09-22), which `ajreynol/cvc5` `master`
matched exactly when read — the fork was in sync with upstream, with nothing
between them.

| | |
| --- | --- |
| active branches | **88** — 65 heuresis, 23 elaphros |
| within 6 commits of the pin | **70** (52 + 18) — 66 with their changes intact, **4 emptied by a merge** |
| older | **18**, carrying commits 522 to 9377 back |
| compile-checked | **70 of 70** pass |
| retired | **8**, listed at the bottom |

Three passes have run: 37 branches on 2026-09-21, 33 more on 2026-09-22, and 58
refreshed again the same day. **Every one was brought up by merging, not by
rebasing** — each current tip is a `Merge branch 'master' into …` commit. That
is enough to build and measure, and `± LOC` is a three-dot diff against the pin,
so it still reports only the branch's own changes. It is not the linear series
an upstream review will ask for.

### Two merges dropped the branch's changes, and still have

A merge in the second pass resolved in favour of upstream on four branches,
leaving them identical to the pin; the third pass merged again on top, which
carried the emptiness forward rather than repairing it. Their proposal rows
describe nothing, and they compile for that reason.

| branch | project | direction | what was lost | tip that still holds it |
| --- | --- | --- | --- | --- |
| [`smtPpBasicRewriteOnly`](https://github.com/ajreynol/cvc5/tree/smtPpBasicRewriteOnly) | elaphros | [E7](../tools/elaphros/docs/directions.md#e7-reconstruction-cache-and-search-policy) | 1 src file, +3/−12 | `cfddc7a96c` |
| [`stringsIpcAgg2`](https://github.com/ajreynol/cvc5/tree/stringsIpcAgg2) | elaphros | [E10](../tools/elaphros/docs/directions.md#e10-lazy-bookkeeping-and-theory-reconstruction) | 1 src file, +17/−0 | `892d178f2b` |
| [`fmfIeval`](https://github.com/ajreynol/cvc5/tree/fmfIeval) | heuresis | [R7](../tools/heuresis/docs/directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 5 src files, +40/−22 | `61156a62b2` |
| [`bvToIntQuant-031126`](https://github.com/ajreynol/cvc5/tree/bvToIntQuant-031126) | heuresis | [R19](../tools/heuresis/docs/directions.md#r19--bit-vectors-inside-quantified-problems) | 1 src file, +60/−16 | `163e60360b` |

Recover the work from those tips, onto a named pin, and check the diff before
recording anything about them.

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

**All 70 pass, which is worth distrusting**, so the check was verified rather
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

## Within 6 commits of the pin — 70 branches

`± LOC` is the three-dot source diff against [`10bd5cb`](https://github.com/cvc5/cvc5/commit/10bd5cb3bb9ad9cb10277e0ae54e352e6d2ac345), `src/` only.

| branch | what it does | project | direction | its commits | ± LOC | builds |
| --- | --- | --- | --- | ---: | ---: | :-: |
| [`unrewrite2`](https://github.com/ajreynol/cvc5/tree/unrewrite2) | Candidate preimages, replay of renamed proof steps, fallback when replay fails | elaphros | [E1](../tools/elaphros/docs/directions.md#e1-unrewriting) | 14 | +1082/−0 over 10 src files | ✅ 52s |
| [`reduceTransform`](https://github.com/ajreynol/cvc5/tree/reduceTransform) | Decomposes a macro obligation to the subterms that actually changed | elaphros | [E2](../tools/elaphros/docs/directions.md#e2-smaller-macro-obligations) | 18 | +324/−1 over 2 src files | ✅ 67s |
| [`pfrConvert2`](https://github.com/ajreynol/cvc5/tree/pfrConvert2) | `--proof-use-rule-convert`, `CONVERT`/`CONVERT_FIXED_POINT` and a checker | elaphros | [E3](../tools/elaphros/docs/directions.md#e3-compact-term-conversion) | 19 | +272/−20 over 7 src files | ✅ 67s |
| [`rewriteDep`](https://github.com/ajreynol/cvc5/tree/rewriteDep) | Probes replacing a rewrite's child by a purification symbol to drop dependencies | elaphros | [E4](../tools/elaphros/docs/directions.md#e4-rewrite-dependencies) | 16 | +225/−32 over 6 src files | ✅ 26s |
| [`cpcDevChainMRes`](https://github.com/ajreynol/cvc5/tree/cpcDevChainMRes) | Removes transitivity round trips and combines consecutive congruence steps | elaphros | [E5](../tools/elaphros/docs/directions.md#e5-proof-dag-simplification-and-sharing) | 179 | +522/−1 over 3 src files | ✅ 7s |
| [`rdbExec`](https://github.com/ajreynol/cvc5/tree/rdbExec) | Compiles selected `:exec` RARE rules into rewrite code and records a rule ID | elaphros | [E6](../tools/elaphros/docs/directions.md#e6-recorded-rewrite-provenance) | 19 | +2561/−49 over 29 src files | ✅ 67s |
| [`rareOptEval`](https://github.com/ajreynol/cvc5/tree/rareOptEval) | Stops clearing `d_evalCache` at every `RewriteDbProofCons::prove` | elaphros | [E7](../tools/elaphros/docs/directions.md#e7-reconstruction-cache-and-search-policy) | 7 | +1/−2 over 1 src files | ✅ 64s |
| [`rpcAlwaysPre`](https://github.com/ajreynol/cvc5/tree/rpcAlwaysPre) | Promotes `POST_DSL` theory rewrites to `PRE_DSL` | elaphros | [E7](../tools/elaphros/docs/directions.md#e7-reconstruction-cache-and-search-policy) | 10 | +60/−1 over 6 src files | ✅ 38s |
| [`smtPpBasicRewriteOnly`](https://github.com/ajreynol/cvc5/tree/smtPpBasicRewriteOnly) | Limits one trusted-step recovery to ordinary, not extended, rewriting | elaphros | [E7](../tools/elaphros/docs/directions.md#e7-reconstruction-cache-and-search-policy) | 3 | **empty — dropped +3/−12** | ✅ 46s |
| [`chainMResOpt`](https://github.com/ajreynol/cvc5/tree/chainMResOpt) | Pending-pivot counts and a surviving-literal set in `CHAIN_M_RESOLUTION` checking | elaphros | [E8](../tools/elaphros/docs/directions.md#e8-resolution-construction-and-internal-checking) | 3 | +62/−55 over 1 src files | ✅ 12s |
| [`pf-defineFun`](https://github.com/ajreynol/cvc5/tree/pf-defineFun) | `--proof-define-fun-macros`: tracks definitions through output and assumptions | elaphros | [E9](../tools/elaphros/docs/directions.md#e9-definitions-and-proof-output) | 8 | +698/−60 over 15 src files | ✅ 41s |
| [`pf-defineFun-printerOnly`](https://github.com/ajreynol/cvc5/tree/pf-defineFun-printerOnly) | The same idea moved to a `MacroDefConverter` in proof output | elaphros | [E9](../tools/elaphros/docs/directions.md#e9-definitions-and-proof-output) | 8 | +876/−25 over 11 src files | ✅ 41s |
| [`stratifiedStrIpc`](https://github.com/ajreynol/cvc5/tree/stratifiedStrIpc) | Two-stage substitution construction for strings proof reconstruction | elaphros | [E10](../tools/elaphros/docs/directions.md#e10-lazy-bookkeeping-and-theory-reconstruction) | 2 | +58/−7 over 1 src files | ✅ 27s |
| [`stringsIpcAgg2`](https://github.com/ajreynol/cvc5/tree/stringsIpcAgg2) | A second strings reconstruction alternative | elaphros | [E10](../tools/elaphros/docs/directions.md#e10-lazy-bookkeeping-and-theory-reconstruction) | 5 | **empty — dropped +17/−0** | ✅ 18s |
| [`stringsIpcAgg`](https://github.com/ajreynol/cvc5/tree/stringsIpcAgg) | A strings reconstruction alternative | elaphros | [E10](../tools/elaphros/docs/directions.md#e10-lazy-bookkeeping-and-theory-reconstruction) | 6 | +72/−4 over 3 src files | ✅ 17s |
| [`theoryEngineLazyProofs`](https://github.com/ajreynol/cvc5/tree/theoryEngineLazyProofs) | Separately allocated `LazyCDProof` objects in a `CDProofSet` | elaphros | [E10](../tools/elaphros/docs/directions.md#e10-lazy-bookkeeping-and-theory-reconstruction) | 4 | +32/−28 over 2 src files | ✅ 51s |
| [`ai-pfIncremental`](https://github.com/ajreynol/cvc5/tree/ai-pfIncremental) | Scoped incremental CPC output with push/pop notifications | elaphros | [E11](../tools/elaphros/docs/directions.md#e11-incremental-output-and-reuse) | 8 | +365/−23 over 7 src files | ✅ 65s |
| [`ai-macroPf`](https://github.com/ajreynol/cvc5/tree/ai-macroPf) | Proof support for the quantifier-macro preprocessing pass | elaphros | [E12](../tools/elaphros/docs/directions.md#e12-proof-induced-search-changes) | 3 | +118/−45 over 5 src files | ✅ 66s |
| [`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | Notification-driven eager matcher with generation, pair and per-round budgets | heuresis | [R1](../tools/heuresis/docs/directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 8 | +1455/−8 over 13 src files | ✅ 53s |
| [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | E-matching over a persistent ground trie fed by equality-engine notifications | heuresis | [R1](../tools/heuresis/docs/directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 181 | +3771/−37 over 38 src files | ✅ 74s |
| [`ai-extEagerInst3-1`](https://github.com/ajreynol/cvc5/tree/ai-extEagerInst3-1) | `eagerInst3` plus auto-triggers | heuresis | [R1](../tools/heuresis/docs/directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 185 | +4057/−38 over 39 src files | ✅ 52s |
| [`instFullPreempt`](https://github.com/ajreynol/cvc5/tree/instFullPreempt) | `--inst-when=full-preempt`: instantiate before theory combination runs | heuresis | [R1](../tools/heuresis/docs/directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | 3 | +11/−1 over 2 src files | ✅ 44s |
| [`ai-emFilter`](https://github.com/ajreynol/cvc5/tree/ai-emFilter) | `--filter-e-matching`: filters quantified formulas out of E-matching by event | heuresis | [R2](../tools/heuresis/docs/directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 13 | +758/−15 over 20 src files | ✅ 75s |
| [`imTrivial`](https://github.com/ajreynol/cvc5/tree/imTrivial) | Trivial-trigger matcher that considers only terms not yet seen | heuresis | [R2](../tools/heuresis/docs/directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 12 | +268/−21 over 14 src files | ✅ 37s |
| [`imSimpleInc2`](https://github.com/ajreynol/cvc5/tree/imSimpleInc2) | The same incremental treatment for `InstMatchGeneratorSimple` | heuresis | [R2](../tools/heuresis/docs/directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 10 | +122/−23 over 4 src files | ✅ 18s |
| [`ai-imgDirect`](https://github.com/ajreynol/cvc5/tree/ai-imgDirect) | Direct matcher for nested single triggers, excluding failed roots for the round | heuresis | [R2](../tools/heuresis/docs/directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 6 | +705/−4 over 5 src files | ✅ 55s |
| [`ai-quantOpt-1`](https://github.com/ajreynol/cvc5/tree/ai-quantOpt-1) | Candidate caching per pattern arity | heuresis | [R2](../tools/heuresis/docs/directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | 4 | +36/−4 over 2 src files | ✅ 5s |
| [`ai-prepared13`](https://github.com/ajreynol/cvc5/tree/ai-prepared13) | Caches match failures that are invariant modulo the equality engine | heuresis | [R3](../tools/heuresis/docs/directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | 13 | +291/−6 over 4 src files | ✅ 6s |
| [`termOrigin`](https://github.com/ajreynol/cvc5/tree/termOrigin) | `--inst-nested-max-level` and a lemma-origin DAG — cvc5's nearest thing to z3's generation | heuresis | [R4](../tools/heuresis/docs/directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | 17 | +474/−11 over 19 src files | ✅ 50s |
| [`instLastCallDelay`](https://github.com/ajreynol/cvc5/tree/instLastCallDelay) | Skips the last-call check while the valuation still needs one | heuresis | [R4](../tools/heuresis/docs/directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | 3 | +2/−2 over 1 src files | ✅ 39s |
| [`dtInstMode`](https://github.com/ajreynol/cvc5/tree/dtInstMode) | *(not characterised)* | heuresis | [R4](../tools/heuresis/docs/directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | 4 | +14/−1 over 2 src files | ✅ 48s |
| [`multiTriggerSingleBase`](https://github.com/ajreynol/cvc5/tree/multiTriggerSingleBase) | Uses a single trigger as the base for multi-triggers | heuresis | [R5](../tools/heuresis/docs/directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | 3 | +43/−0 over 3 src files | ✅ 43s |
| [`nestedTriggers`](https://github.com/ajreynol/cvc5/tree/nestedTriggers) | `--nested-triggers`: triggers from terms in nested quantifiers | heuresis | [R5](../tools/heuresis/docs/directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | 4 | +40/−22 over 4 src files | ✅ 16s |
| [`simpleTriggerMore`](https://github.com/ajreynol/cvc5/tree/simpleTriggerMore) | *(not characterised)* | heuresis | [R5](../tools/heuresis/docs/directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | 5 | +48/−33 over 2 src files | ✅ 39s |
| [`gttOpt`](https://github.com/ajreynol/cvc5/tree/gttOpt) | `--gt-trigger-reg`: registers ground subterms of triggers | heuresis | [R5](../tools/heuresis/docs/directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | 4 | +9/−1 over 2 src files | ✅ 45s |
| [`ai-cbqi-0423`](https://github.com/ajreynol/cvc5/tree/ai-cbqi-0423) | Reworks QCF where flattened UF encodings force an exhaustive search | heuresis | [R6](../tools/heuresis/docs/directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | 6 | +136/−87 over 1 src files | ✅ 8s |
| [`ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) | Evaluator walks term tries as assignments arrive, rejecting infeasible matches earlier | heuresis | [R7](../tools/heuresis/docs/directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 5 | +165/−43 over 8 src files | ✅ 42s |
| [`fmfIeval`](https://github.com/ajreynol/cvc5/tree/fmfIeval) | *(not characterised)* | heuresis | [R7](../tools/heuresis/docs/directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 4 | **empty — dropped +40/−22** | ✅ 54s |
| [`notifySatClause`](https://github.com/ajreynol/cvc5/tree/notifySatClause) | The SAT deletion callback a real instantiation-lemma GC would need | heuresis | [R9](../tools/heuresis/docs/directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | 6 | +49/−10 over 6 src files | ✅ 10s |
| [`ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) | `--inst-defer`: records instantiations globally, treats them as local in the heuristic | heuresis | [R10](../tools/heuresis/docs/directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 4 | +116/−32 over 11 src files | ✅ 52s |
| [`ai-jhRlvInst`](https://github.com/ajreynol/cvc5/tree/ai-jhRlvInst) | `--jh-rlv-inst`: activates an instantiation lemma when its quantifier is asserted | heuresis | [R10](../tools/heuresis/docs/directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 5 | +326/−18 over 9 src files | ✅ 17s |
| [`ai-jhConflictFirst`](https://github.com/ajreynol/cvc5/tree/ai-jhConflictFirst) | `--jh-conflict-first`: prioritises conflict clauses over theory lemmas | heuresis | [R10](../tools/heuresis/docs/directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 4 | +93/−33 over 9 src files | ✅ 49s |
| [`claudeDev-dts-idef`](https://github.com/ajreynol/cvc5/tree/claudeDev-dts-idef) | `--inst-defer` and `--dt-split-relevant` together | heuresis | [R10](../tools/heuresis/docs/directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | 5 | +179/−37 over 13 src files | ✅ 51s |
| [`jhRandom`](https://github.com/ajreynol/cvc5/tree/jhRandom) | `--jh-rand`: randomised assertion and branch order | heuresis | [R11](../tools/heuresis/docs/directions.md#r11--decision-heuristic-versus-relevancy-what-the-sat-solver-is-made-to-decide-on) | 5 | +262/−20 over 7 src files | ✅ 16s |
| [`subConflict`](https://github.com/ajreynol/cvc5/tree/subConflict) | `--sub-conflict-find`: a subsolver that looks for conflicts | heuresis | [R12](../tools/heuresis/docs/directions.md#r12--lemma-inprocessing-and-conflict-minimisation) | 11 | +333/−1 over 12 src files | ✅ 49s |
| [`cadicalPortfolio`](https://github.com/ajreynol/cvc5/tree/cadicalPortfolio) | *(not characterised)* | heuresis | [R13](../tools/heuresis/docs/directions.md#r13--the-sat-backend-cadical-minisat-restarts-units) | 4 | +50/−0 over 1 src files | ✅ 4s |
| [`mbtc25`](https://github.com/ajreynol/cvc5/tree/mbtc25) | `--tc-mode=model-based`: model-based theory combination; upstream PR #12095 open | heuresis | [R14](../tools/heuresis/docs/directions.md#r14--theory-combination-care-graph-or-model-based) | 31 | +365/−82 over 15 src files | ✅ 42s |
| [`ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare) | Skips `propagateSharedEquality` for theories the central engine already explains | heuresis | [R15](../tools/heuresis/docs/directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 4 | +9/−3 over 1 src files | ✅ 19s |
| [`dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3) | Datatypes under the central equality engine without `notifyFact` | heuresis | [R15](../tools/heuresis/docs/directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 33 | +378/−72 over 10 src files | ✅ 20s |
| [`cdno`](https://github.com/ajreynol/cvc5/tree/cdno) | Context-dynamic notify objects | heuresis | [R15](../tools/heuresis/docs/directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | 18 | +168/−12 over 5 src files | ✅ 46s |
| [`dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant) | `--dt-split-relevant`: splits only on datatype terms in asserted literals | heuresis | [R16](../tools/heuresis/docs/directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 4 | +61/−8 over 2 src files | ✅ 20s |
| [`dtLazyInst3`](https://github.com/ajreynol/cvc5/tree/dtLazyInst3) | `--dt-lazy-inst`: applies the datatypes instantiate rule lazily | heuresis | [R16](../tools/heuresis/docs/directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 21 | +80/−2 over 3 src files | ✅ 17s |
| [`oneConsInst`](https://github.com/ajreynol/cvc5/tree/oneConsInst) | Instantiates single-constructor terms directly | heuresis | [R16](../tools/heuresis/docs/directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | 5 | +42/−11 over 2 src files | ✅ 10s |
| [`ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc) | `--dio-solver-last-call`: defers Diophantine conflict detection to last call | heuresis | [R17](../tools/heuresis/docs/directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | 5 | +95/−2 over 6 src files | ✅ 20s |
| [`deferBlock`](https://github.com/ajreynol/cvc5/tree/deferBlock) | `--defer-block`: holds lemmas back, with arithmetic branch-and-bound hooks | heuresis | [R17](../tools/heuresis/docs/directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | 21 | +330/−16 over 15 src files | ✅ 53s |
| [`bitblastLc`](https://github.com/ajreynol/cvc5/tree/bitblastLc) | `--bitblast-lc`: delays bit-blasting to last call | heuresis | [R19](../tools/heuresis/docs/directions.md#r19--bit-vectors-inside-quantified-problems) | 3 | +28/−1 over 2 src files | ✅ 15s |
| [`bvToIntQuant-031126`](https://github.com/ajreynol/cvc5/tree/bvToIntQuant-031126) | Int-blasting under quantified `bv2nat` | heuresis | [R19](../tools/heuresis/docs/directions.md#r19--bit-vectors-inside-quantified-problems) | 4 | **empty — dropped +60/−16** | ✅ 15s |
| [`ufConvRlv`](https://github.com/ajreynol/cvc5/tree/ufConvRlv) | Reduces only relevant terms in the UF conversion solver | heuresis | [R19](../tools/heuresis/docs/directions.md#r19--bit-vectors-inside-quantified-problems) | 4 | +12/−4 over 3 src files | ✅ 16s |
| [`ufEagerDistinct`](https://github.com/ajreynol/cvc5/tree/ufEagerDistinct) | `--uf-eager-distinct` | heuresis | [R20](../tools/heuresis/docs/directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | 3 | +25/−0 over 3 src files | ✅ 17s |
| [`simplifyRecFun`](https://github.com/ajreynol/cvc5/tree/simplifyRecFun) | `--simplify-rec-fun` | heuresis | [R20](../tools/heuresis/docs/directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | 60 | +101/−39 over 11 src files | ✅ 44s |
| [`quantRew-1006`](https://github.com/ajreynol/cvc5/tree/quantRew-1006) | Constructor equalities in quantifier bodies | heuresis | [R21](../tools/heuresis/docs/directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | 4 | +27/−4 over 1 src files | ✅ 22s |
| [`preregRlv`](https://github.com/ajreynol/cvc5/tree/preregRlv) | `--preregister-mode=rlv`: preregisters only literals relevance can use; PR #9503 open | heuresis | [R22](../tools/heuresis/docs/directions.md#r22--preregistration-which-literals-the-theories-are-told-about) | 157 | +833/−13 over 9 src files | ✅ 42s |
| [`tdbOldIndex`](https://github.com/ajreynol/cvc5/tree/tdbOldIndex) | `--tdb-old-index`: prefers old terms in term-database indices | heuresis | [R23](../tools/heuresis/docs/directions.md#r23--term-database-relevance-which-ground-terms-e-matching-may-use) | 7 | +61/−7 over 5 src files | ✅ 49s |
| [`lowLevelOptMore`](https://github.com/ajreynol/cvc5/tree/lowLevelOptMore) | Compact constant-factor work from 2019 | heuresis | [R25](../tools/heuresis/docs/directions.md#r25--low-level-engineering-the-constant-factors) | 13 | +72/−8 over 2 src files | ✅ 16s |
| [`tdbLLOpts`](https://github.com/ajreynol/cvc5/tree/tdbLLOpts) | *(not characterised)* | heuresis | [R25](../tools/heuresis/docs/directions.md#r25--low-level-engineering-the-constant-factors) | 4 | +34/−34 over 2 src files | ✅ 48s |
| [`qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) | E-matching debug statistics and an `AnalyzeEE` module | heuresis | [R26](../tools/heuresis/docs/directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 32 | +534/−15 over 19 src files | ✅ 23s |
| [`debugDumpLemmas`](https://github.com/ajreynol/cvc5/tree/debugDumpLemmas) | `--re-check-lemmas` | heuresis | [R26](../tools/heuresis/docs/directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 7 | +49/−0 over 5 src files | ✅ 51s |
| [`trackInferId`](https://github.com/ajreynol/cvc5/tree/trackInferId) | `--track-lemma-inference-ids` | heuresis | [R26](../tools/heuresis/docs/directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | 3 | +22/−3 over 3 src files | ✅ 17s |
| [`ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt) | Reserved parser stacks, `from_chars`, static token tables, less vector movement | heuresis | [R27](../tools/heuresis/docs/directions.md#r27--smt-lib-parser-throughput-pay-less-before-solving) | 4 | +228/−141 over 7 src files | ✅ 18s |
| [`eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi) | Evaluator-backed eager term database with conflict and propagation modes | heuresis | [R28](../tools/heuresis/docs/directions.md#r28--eager-conflict-based-instantiation-find-a-useful-instance-before-full-effort) | 206 | +5248/−202 over 58 src files | ✅ 75s |

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


## Older than the pin — 18 branches

**This is the work order for the next pass.** Nearest first; the last column is
commits behind the pin. Nothing here can be built, measured or reviewed as it
stands, and none is compile-checked.

| branch | project | direction | newest cvc5 commit it carries | its commits | behind `10bd5cb` |
| --- | --- | --- | --- | ---: | ---: |
| [`emExp`](https://github.com/ajreynol/cvc5/tree/emExp) | heuresis | [R2](../tools/heuresis/docs/directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | [`310f487`](https://github.com/cvc5/cvc5/commit/310f487e6a829fb1bdfbef2849536176b047606e) (2025-11-11) | 6 | **522** |
| [`dtElim`](https://github.com/ajreynol/cvc5/tree/dtElim) | heuresis | [R16](../tools/heuresis/docs/directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | [`aeb5547`](https://github.com/cvc5/cvc5/commit/aeb554775be7eb9eb59f640fa76ee90879e19746) (2025-10-29) | 26 | **537** |
| [`rareNoEvalPremise`](https://github.com/ajreynol/cvc5/tree/rareNoEvalPremise) | elaphros | [E7](../tools/elaphros/docs/directions.md#e7-reconstruction-cache-and-search-policy) | [`cbcaf6e`](https://github.com/cvc5/cvc5/commit/cbcaf6e7836e3c62698caa7ee22d37e9d344485c) (2025-10-16) | 13 | **554** |
| [`eagerQM`](https://github.com/ajreynol/cvc5/tree/eagerQM) | heuresis | [R1](../tools/heuresis/docs/directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | [`aca9908`](https://github.com/cvc5/cvc5/commit/aca99089d0de4fa9292227af36f25c5499024a3c) (2025-08-28) | 3 | **623** |
| [`pfTrustId`](https://github.com/ajreynol/cvc5/tree/pfTrustId) | elaphros | [E5](../tools/elaphros/docs/directions.md#e5-proof-dag-simplification-and-sharing) | [`91201c4`](https://github.com/cvc5/cvc5/commit/91201c459edd6f999de22bee6665a1f0b1fccffd) (2025-06-17) | 1217 | **706** |
| [`rareEncodeSubcall`](https://github.com/ajreynol/cvc5/tree/rareEncodeSubcall) | elaphros | [E7](../tools/elaphros/docs/directions.md#e7-reconstruction-cache-and-search-policy) | [`85fa780`](https://github.com/cvc5/cvc5/commit/85fa7800ce49e88be19d92389b3a4d89316f0524) (2025-05-20) | 3 | **759** |
| [`stringsIpcRefactor`](https://github.com/ajreynol/cvc5/tree/stringsIpcRefactor) | elaphros | [E10](../tools/elaphros/docs/directions.md#e10-lazy-bookkeeping-and-theory-reconstruction) | [`8cfac8f`](https://github.com/cvc5/cvc5/commit/8cfac8f956c4ef1543f52eb2d862d81367b3d3ed) (2024-12-13) | 15 | **1155** |
| [`eagerElimDefs`](https://github.com/ajreynol/cvc5/tree/eagerElimDefs) | heuresis | [R20](../tools/heuresis/docs/directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | [`9e7ee41`](https://github.com/cvc5/cvc5/commit/9e7ee41e7c50a972afd6f7210ecf94d798beb235) (2024-10-04) | 9 | **1292** |
| [`emStratify`](https://github.com/ajreynol/cvc5/tree/emStratify) | heuresis | [R7](../tools/heuresis/docs/directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | [`78e58a5`](https://github.com/cvc5/cvc5/commit/78e58a5ca5504d1794ba961179cae4c0f5405850) (2023-11-01) | 17 | **2211** |
| [`pfrConvert`](https://github.com/ajreynol/cvc5/tree/pfrConvert) | elaphros | [E3](../tools/elaphros/docs/directions.md#e3-compact-term-conversion) | [`f53fc5f`](https://github.com/cvc5/cvc5/commit/f53fc5f26eee6c51e43526825ea15856b80f06a6) (2023-10-24) | 19 | **2219** |
| [`p657`](https://github.com/ajreynol/cvc5/tree/p657) | heuresis | [R21](../tools/heuresis/docs/directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | [`43c1d0f`](https://github.com/cvc5/cvc5/commit/43c1d0f6815c58f30b6c0b405080da169f56fc04) (2023-08-23) | 4 | **2359** |
| [`isActiveLemma`](https://github.com/ajreynol/cvc5/tree/isActiveLemma) | heuresis | [R9](../tools/heuresis/docs/directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`51aa806`](https://github.com/cvc5/cvc5/commit/51aa8060989af2d8a626adcc18efb088bcbd1438) (2023-08-18) | 50 | **2374** |
| [`smtLazyAssert`](https://github.com/ajreynol/cvc5/tree/smtLazyAssert) | heuresis | [R9](../tools/heuresis/docs/directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`1c41fda`](https://github.com/cvc5/cvc5/commit/1c41fdaef2639ab81737bca2bda33d385157bda7) (2022-08-03) | 21 | **3045** |
| [`emFailMasks`](https://github.com/ajreynol/cvc5/tree/emFailMasks) | heuresis | [R3](../tools/heuresis/docs/directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | [`2e555b3`](https://github.com/cvc5/cvc5/commit/2e555b3cac196cb141a3a4dbf934f282bfbdd723) (2022-04-20) | 27 | **3325** |
| [`cacheEntCheck`](https://github.com/ajreynol/cvc5/tree/cacheEntCheck) | heuresis | [R3](../tools/heuresis/docs/directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | [`b446953`](https://github.com/cvc5/cvc5/commit/b4469530d2f6de599ddf7207a1914b88be49de5b) (2021-10-15) | 5 | **4439** |
| [`virtualClauseDel`](https://github.com/ajreynol/cvc5/tree/virtualClauseDel) | heuresis | [R9](../tools/heuresis/docs/directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`55ce505`](https://github.com/cvc5/cvc5/commit/55ce505ca757dc241bf4c1e10023bc43ac531a23) (2021-10-13) | 15 | **4450** |
| [`carryInst`](https://github.com/ajreynol/cvc5/tree/carryInst) | heuresis | [R4](../tools/heuresis/docs/directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | [`54490c6`](https://github.com/cvc5/cvc5/commit/54490c6053d51910f5f7c2160451ad4d36fe6946) (2021-07-28) | 3 | **4811** |
| [`bvBbExtf`](https://github.com/ajreynol/cvc5/tree/bvBbExtf) | heuresis | [R19](../tools/heuresis/docs/directions.md#r19--bit-vectors-inside-quantified-problems) | [`be7662b`](https://github.com/cvc5/cvc5/commit/be7662bdcd3881d349bfba4c959a0c2be4159ce9) (2016-12-08) | 5 | **9377** |

**The far end is design evidence, not a queue.** The oldest commits carried here
predate current cvc5 by years; `bvBbExtf` holds one from 2016. The registers
keep those rows because the idea is a candidate, not because the patch is one,
and below roughly a thousand commits an update is more likely to drop the
mechanism than to preserve it — which is no longer hypothetical. A report that
such a branch should be reimplemented rather than updated is the useful outcome.

## Retired — 8 branches

Not work for the next pass: these were attempted or assessed and could not be
brought onto a current commit, so their proposal rows are gone from the
registers. The verdict is the point — each says what upstream did to the ground
the branch stood on. From the maintainer's update-pass notes, 2026-09-22.

| branch | project | direction | verdict | why |
| --- | --- | --- | --- | --- |
| [`pfrDev`](https://github.com/ajreynol/cvc5/tree/pfrDev) | elaphros | [E8](../tools/elaphros/docs/directions.md#e8-resolution-construction-and-internal-checking) | **SUPERSEDED** | Its mechanism is a `proofMacroRes` option plus a `MACRO_RESOLUTION` proof checker. Master has removed `ProofRule::MACRO_RESOLUTION` entirely and replaced it with `CHAIN_M_RESOLUTION` and its own `proofChainMRes` option — the route `cpcDevChainMRes` (E5) took — and rewrote the checker algorithm. There is nothing left to merge onto. |
| [`refactorQcf`](https://github.com/ajreynol/cvc5/tree/refactorQcf) | heuresis | [R6](../tools/heuresis/docs/directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | **REWRITTEN UPSTREAM** | 79 substantive conflict hunks, all inside `quant_conflict_find.{cpp,h}`, which master has rewritten. A merge would be a rewrite of the branch against a different design. |
| [`qcfClean`](https://github.com/ajreynol/cvc5/tree/qcfClean) | heuresis | [R6](../tools/heuresis/docs/directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | **REWRITTEN UPSTREAM** | 60 substantive conflict hunks in the same two rewritten files. Same verdict as `refactorQcf`. |
| [`virtualLemma`](https://github.com/ajreynol/cvc5/tree/virtualLemma) | heuresis | [R9](../tools/heuresis/docs/directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | **TARGETS DELETED CODE** | 40 substantive hunks across 13 files, two of which master has deleted: `decision_engine_old.cpp` and `decision_engine_old.h`. The decision-engine surface the branch attaches to no longer exists. |
| [`linearSolverSub`](https://github.com/ajreynol/cvc5/tree/linearSolverSub) | heuresis | [R17](../tools/heuresis/docs/directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | **NEEDS REIMPLEMENTATION** | Dropped by the author, and independently a signature migration rather than a merge: master changed `LinearSolver`'s interface — `propagate()` lost its `Effort` argument, `ppAssert` returns `bool`, `ppStaticLearn` takes `std::vector<TrustNode>` — while the branch adds a 376-line implementation of the old signatures. Porting means migrating the base, `LinearSolverLegacy`, `LinearSolverSub` and the call sites together. |
| [`ai-fixAlphaEq-2`](https://github.com/ajreynol/cvc5/tree/ai-fixAlphaEq-2) | heuresis | [R21](../tools/heuresis/docs/directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | **AUTHOR-DROPPED** | Dropped on the author's instruction; not assessed further. The branch is left untouched on the fork. |
| [`optTdbTNode`](https://github.com/ajreynol/cvc5/tree/optTdbTNode) | heuresis | [R25](../tools/heuresis/docs/directions.md#r25--low-level-engineering-the-constant-factors) | **SUPERSEDED** | Its entire content is `Node` → `TNode` on `TermDb::d_op_map` and `d_type_map` to avoid reference counting. Master replaced both with context-dependent `CDHashMap<Node, std::shared_ptr<DbList>>`, so all 25 hunks target structures that no longer exist, and master's own `DbList` rewrite supersedes the optimisation. |
| [`perfDataStructures`](https://github.com/ajreynol/cvc5/tree/perfDataStructures) | heuresis | [R25](../tools/heuresis/docs/directions.md#r25--low-level-engineering-the-constant-factors) | **CANNOT BUILD** | A 2018 benchmarking scaffold. Merging silently resurrected two files master had deleted — `smt_engine.cpp` (6105 lines, renamed `solver_engine.cpp`) and the autotools `src/Makefile.am` — a clean-looking merge that was in fact broken. Its `--do-test` hook lands in `SmtEnginePrivate::processAssertions`, which no longer exists, and its sources use `cvc4_private.h`, `namespace CVC4` and `__CVC4__` guards, so they cannot compile against `cvc5::internal`. |

`perfDataStructures` is the one to remember: its merge looked clean while
silently resurrecting two files master had deleted. That is the same failure as
the two emptied branches above, caught from the other side.
