# Active development branches

**What this is.** Every branch of [`ajreynol/cvc5`](https://github.com/ajreynol/cvc5)
that heuresis calls **active**, and where it sits relative to the fork's
`master`. It exists so a rebase pass — by a person or an agent — can start from
one file instead of from the register.

**Active means: named by a proposal row** in a research direction's table in
[`directions.md`](directions.md#proposals). That register is authoritative; this
file is derived from it and from the fork, and is **not** a place to add a
branch. A branch earns a row here by first earning a proposal row there.

**Elaphros keeps its own.** The 23 active branches of the sibling project are in
[its register](../../elaphros/docs/directions.md#proposals) and are not listed
here; the two projects do not write in each other's directories.

**A branch being current is not a result.** Nothing here says a branch helps.
The `± solved` column of the register stays empty until the branch is built and
run on `quant-07-25` against the reference.

## State

**Derived 2026-09-22.** The target is the fork's `master` at
[`c2cc3caf`](https://github.com/ajreynol/cvc5/commit/c2cc3caf78414931b0feaed26a05c4426ed96098),
itself **3 commits behind cvc5 `main`** (`ab20a7cc`) when this was read: a branch
on `master` is current with the fork, not necessarily with upstream.

| | |
| --- | --- |
| active branches | **72**, across 25 of the 27 research directions |
| current with `master` | **25**, all by merge rather than rebase |
| still behind | **47**, from 126 to 9371 commits |

**How the current ones got there.** Every one is a `Merge branch 'master' into
…` tip, adding one merge commit to the branch. That is enough to build and
measure, and the `± LOC` below is a three-dot diff against `master`, so it
still reports only the branch's own changes. It is not a linear patch series,
which is what an upstream review will ask for; linearising is work deferred,
not work avoided.

**The fork moves under this file.** Thirty-six branches changed between the
2026-09-21 reading and this one. Treat every figure here as a reading, not a
fact about today, and re-derive before acting:

```bash
git clone --filter=tree:0 --bare https://github.com/ajreynol/cvc5 fork.git
git --git-dir=fork.git merge-base master BRANCH          # the base it sits on
git --git-dir=fork.git rev-list --count BRANCH..master   # 0 means it is current
git --git-dir=fork.git rev-list --count master..BRANCH   # its own commits
git --git-dir=fork.git rev-list --parents -n1 BRANCH     # two parents: a merge
```

## Bringing a branch up to date

1. **Prefer a rebase onto `master`**, keeping the branch's own commits. Merging
   `master` in is acceptable and is what the first pass did — it makes the
   branch current, which is what a measurement needs — but record which was
   done, because only one of them leaves a reviewable series.
2. **One branch at a time**, and no unrelated work squashed in.
3. **Do not force a resolution.** A rebase that will not come out cleanly is a
   result: report the conflicts. How large and how conflicted it is is part of
   what the proposal costs, and a branch better reimplemented than rebased can
   retire its proposal row — which is progress, not failure.
4. **Check the diff against the register.** If the source diff has collapsed to
   nothing, or lost the mechanism the direction names, the update dropped
   content. Say so rather than recording a small diff.
5. **Report, per branch:** new tip, merge base, diffstat, and whether it builds
   and passes `make regress`.
6. **Then update two places:** the `rebased to` and `± LOC` cells of the
   proposal row in [`directions.md`](directions.md#proposals), and the row here.

## Current with `master` — 25 branches

Ready to build and measure. `± LOC` is the three-dot source diff against
`master`, `src/` only.

| branch | direction | how | its commits | ± LOC |
| --- | --- | --- | ---: | ---: |
| [`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | merge | 7 | +1455/−8 over 13 src files |
| [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | merge | 180 | +3771/−37 over 38 src files |
| [`ai-prepared13`](https://github.com/ajreynol/cvc5/tree/ai-prepared13) | [R3](directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | merge | 12 | +291/−6 over 4 src files |
| [`termOrigin`](https://github.com/ajreynol/cvc5/tree/termOrigin) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | merge | 16 | +474/−11 over 19 src files |
| [`multiTriggerSingleBase`](https://github.com/ajreynol/cvc5/tree/multiTriggerSingleBase) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | merge | 2 | +43/−0 over 3 src files |
| [`ai-cbqi-0423`](https://github.com/ajreynol/cvc5/tree/ai-cbqi-0423) | [R6](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | merge | 5 | +136/−87 over 1 src files |
| [`ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) | [R7](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | merge | 4 | +165/−43 over 8 src files |
| [`notifySatClause`](https://github.com/ajreynol/cvc5/tree/notifySatClause) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | merge | 5 | +49/−10 over 6 src files |
| [`ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) | [R10](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | merge | 3 | +116/−32 over 11 src files |
| [`ai-jhConflictFirst`](https://github.com/ajreynol/cvc5/tree/ai-jhConflictFirst) | [R10](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | merge | 3 | +93/−33 over 9 src files |
| [`subConflict`](https://github.com/ajreynol/cvc5/tree/subConflict) | [R12](directions.md#r12--lemma-inprocessing-and-conflict-minimisation) | merge | 9 | +332/−1 over 12 src files |
| [`cadicalPortfolio`](https://github.com/ajreynol/cvc5/tree/cadicalPortfolio) | [R13](directions.md#r13--the-sat-backend-cadical-minisat-restarts-units) | merge | 3 | +50/−0 over 1 src files |
| [`mbtc25`](https://github.com/ajreynol/cvc5/tree/mbtc25) | [R14](directions.md#r14--theory-combination-care-graph-or-model-based) | merge | 30 | +365/−82 over 15 src files |
| [`ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare) | [R15](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | merge | 3 | +9/−3 over 1 src files |
| [`dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | merge | 3 | +61/−8 over 2 src files |
| [`ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc) | [R17](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | merge | 4 | +95/−2 over 6 src files |
| [`bitblastLc`](https://github.com/ajreynol/cvc5/tree/bitblastLc) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | merge | 2 | +28/−1 over 2 src files |
| [`ufEagerDistinct`](https://github.com/ajreynol/cvc5/tree/ufEagerDistinct) | [R20](directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | merge | 2 | +25/−0 over 3 src files |
| [`quantRew-1006`](https://github.com/ajreynol/cvc5/tree/quantRew-1006) | [R21](directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | merge | 3 | +27/−4 over 1 src files |
| [`preregRlv`](https://github.com/ajreynol/cvc5/tree/preregRlv) | [R22](directions.md#r22--preregistration-which-literals-the-theories-are-told-about) | merge | 156 | +833/−13 over 9 src files |
| [`tdbOldIndex`](https://github.com/ajreynol/cvc5/tree/tdbOldIndex) | [R23](directions.md#r23--term-database-relevance-which-ground-terms-e-matching-may-use) | merge | 6 | +61/−7 over 5 src files |
| [`lowLevelOptMore`](https://github.com/ajreynol/cvc5/tree/lowLevelOptMore) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | merge | 12 | +72/−8 over 2 src files |
| [`qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) | [R26](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | merge | 31 | +534/−15 over 19 src files |
| [`ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt) | [R27](directions.md#r27--smt-lib-parser-throughput-pay-less-before-solving) | merge | 3 | +228/−141 over 7 src files |
| [`eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi) | [R28](directions.md#r28--eager-conflict-based-instantiation-find-a-useful-instance-before-full-effort) | merge | 205 | +5248/−202 over 58 src files |

## Behind `master` — 47 branches

Nearest first. Nothing here can be built, measured or reviewed as it stands;
the work order derived from this section is `rebase-to-master-round2.txt`.

| branch | direction | sits on | its commits | distance |
| --- | --- | --- | ---: | ---: |
| [`jhRandom`](https://github.com/ajreynol/cvc5/tree/jhRandom) | [R11](directions.md#r11--decision-heuristic-versus-relevancy-what-the-sat-solver-is-made-to-decide-on) | `f888519` (2026-06-29) | 3 | **126 behind** |
| [`ai-jhRlvInst`](https://github.com/ajreynol/cvc5/tree/ai-jhRlvInst) | [R10](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | `09668f2` (2026-06-17) | 3 | **140 behind** |
| [`claudeDev-dts-idef`](https://github.com/ajreynol/cvc5/tree/claudeDev-dts-idef) | [R10](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | `8c86597` (2026-06-09) | 3 | **153 behind** |
| [`dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3) | [R15](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | `f4f9779` (2026-05-14) | 31 | **193 behind** |
| [`ai-emFilter`](https://github.com/ajreynol/cvc5/tree/ai-emFilter) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | `5509c56` (2026-04-23) | 11 | **230 behind** |
| [`ai-fixAlphaEq-2`](https://github.com/ajreynol/cvc5/tree/ai-fixAlphaEq-2) | [R21](directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | `f172d88` (2026-04-17) | 27 | **243 behind** |
| [`ai-extEagerInst3-1`](https://github.com/ajreynol/cvc5/tree/ai-extEagerInst3-1) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | `01be634` (2026-04-14) | 183 | **250 behind** |
| [`instLastCallDelay`](https://github.com/ajreynol/cvc5/tree/instLastCallDelay) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | `5c6b53b` (2026-03-29) | 1 | **282 behind** |
| [`ai-imgDirect`](https://github.com/ajreynol/cvc5/tree/ai-imgDirect) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | `c2c4dd4` (2026-03-12) | 3 | **327 behind** |
| [`ai-quantOpt-1`](https://github.com/ajreynol/cvc5/tree/ai-quantOpt-1) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | `57561fa` (2026-03-12) | 1 | **329 behind** |
| [`bvToIntQuant-031126`](https://github.com/ajreynol/cvc5/tree/bvToIntQuant-031126) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | `6fa07bf` (2026-03-11) | 2 | **333 behind** |
| [`simplifyRecFun`](https://github.com/ajreynol/cvc5/tree/simplifyRecFun) | [R20](directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | `398316d` (2026-02-20) | 58 | **374 behind** |
| [`emExp`](https://github.com/ajreynol/cvc5/tree/emExp) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | `310f487` (2025-11-11) | 6 | **516 behind** |
| [`oneConsInst`](https://github.com/ajreynol/cvc5/tree/oneConsInst) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | `1120e3d` (2025-11-05) | 3 | **524 behind** |
| [`imTrivial`](https://github.com/ajreynol/cvc5/tree/imTrivial) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | `aeb5547` (2025-10-29) | 9 | **531 behind** |
| [`imSimpleInc2`](https://github.com/ajreynol/cvc5/tree/imSimpleInc2) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | `aeb5547` (2025-10-29) | 7 | **531 behind** |
| [`dtElim`](https://github.com/ajreynol/cvc5/tree/dtElim) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | `aeb5547` (2025-10-29) | 26 | **531 behind** |
| [`cdno`](https://github.com/ajreynol/cvc5/tree/cdno) | [R15](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | `d509acd` (2025-09-09) | 16 | **602 behind** |
| [`debugDumpLemmas`](https://github.com/ajreynol/cvc5/tree/debugDumpLemmas) | [R26](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | `f7db8fa` (2025-09-03) | 5 | **612 behind** |
| [`eagerQM`](https://github.com/ajreynol/cvc5/tree/eagerQM) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | `aca9908` (2025-08-28) | 3 | **617 behind** |
| [`deferBlock`](https://github.com/ajreynol/cvc5/tree/deferBlock) | [R17](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | `2ae4ede` (2025-08-25) | 19 | **619 behind** |
| [`eagerElimDefs`](https://github.com/ajreynol/cvc5/tree/eagerElimDefs) | [R20](directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | `9e7ee41` (2024-10-04) | 9 | **1286 behind** |
| [`tdbLLOpts`](https://github.com/ajreynol/cvc5/tree/tdbLLOpts) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | `8b0a628` (2024-09-10) | 2 | **1345 behind** |
| [`linearSolverSub`](https://github.com/ajreynol/cvc5/tree/linearSolverSub) | [R17](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | `9a741c0` (2024-08-24) | 10 | **1356 behind** |
| [`instFullPreempt`](https://github.com/ajreynol/cvc5/tree/instFullPreempt) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | `0a48958` (2024-08-12) | 1 | **1377 behind** |
| [`trackInferId`](https://github.com/ajreynol/cvc5/tree/trackInferId) | [R26](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | `58a68cf` (2024-04-17) | 1 | **1823 behind** |
| [`nestedTriggers`](https://github.com/ajreynol/cvc5/tree/nestedTriggers) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | `5ef7a7f` (2023-11-11) | 2 | **2193 behind** |
| [`simpleTriggerMore`](https://github.com/ajreynol/cvc5/tree/simpleTriggerMore) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | `4c2037d` (2023-11-02) | 2 | **2202 behind** |
| [`emStratify`](https://github.com/ajreynol/cvc5/tree/emStratify) | [R7](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | `78e58a5` (2023-11-01) | 17 | **2205 behind** |
| [`p657`](https://github.com/ajreynol/cvc5/tree/p657) | [R21](directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | `43c1d0f` (2023-08-23) | 4 | **2353 behind** |
| [`isActiveLemma`](https://github.com/ajreynol/cvc5/tree/isActiveLemma) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | `51aa806` (2023-08-18) | 50 | **2368 behind** |
| [`ufConvRlv`](https://github.com/ajreynol/cvc5/tree/ufConvRlv) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | `2f859d8` (2023-01-23) | 2 | **2719 behind** |
| [`fmfIeval`](https://github.com/ajreynol/cvc5/tree/fmfIeval) | [R7](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | `6df8e7a` (2022-08-28) | 2 | **3002 behind** |
| [`smtLazyAssert`](https://github.com/ajreynol/cvc5/tree/smtLazyAssert) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | `1c41fda` (2022-08-03) | 21 | **3039 behind** |
| [`dtLazyInst3`](https://github.com/ajreynol/cvc5/tree/dtLazyInst3) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | `9fe8509` (2022-05-16) | 18 | **3207 behind** |
| [`emFailMasks`](https://github.com/ajreynol/cvc5/tree/emFailMasks) | [R3](directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | `2e555b3` (2022-04-20) | 27 | **3319 behind** |
| [`refactorQcf`](https://github.com/ajreynol/cvc5/tree/refactorQcf) | [R6](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | `51d731e` (2022-01-26) | 18 | **3875 behind** |
| [`virtualLemma`](https://github.com/ajreynol/cvc5/tree/virtualLemma) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | `8fe459b` (2021-10-19) | 10 | **4424 behind** |
| [`cacheEntCheck`](https://github.com/ajreynol/cvc5/tree/cacheEntCheck) | [R3](directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | `b446953` (2021-10-15) | 5 | **4433 behind** |
| [`virtualClauseDel`](https://github.com/ajreynol/cvc5/tree/virtualClauseDel) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | `55ce505` (2021-10-13) | 15 | **4444 behind** |
| [`carryInst`](https://github.com/ajreynol/cvc5/tree/carryInst) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | `54490c6` (2021-07-28) | 3 | **4805 behind** |
| [`qcfClean`](https://github.com/ajreynol/cvc5/tree/qcfClean) | [R6](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | `b3c6975` (2021-03-25) | 8 | **5405 behind** |
| [`gttOpt`](https://github.com/ajreynol/cvc5/tree/gttOpt) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | `2c4025e` (2021-01-27) | 1 | **5720 behind** |
| [`dtInstMode`](https://github.com/ajreynol/cvc5/tree/dtInstMode) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | `9e481fa` (2020-10-10) | 2 | **6100 behind** |
| [`optTdbTNode`](https://github.com/ajreynol/cvc5/tree/optTdbTNode) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | `a6bd02c` (2019-03-26) | 1 | **7581 behind** |
| [`perfDataStructures`](https://github.com/ajreynol/cvc5/tree/perfDataStructures) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | `047e75b` (2018-08-07) | 31 | **8174 behind** |
| [`bvBbExtf`](https://github.com/ajreynol/cvc5/tree/bvBbExtf) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | `be7662b` (2016-12-08) | 5 | **9371 behind** |

**The far end is design evidence, not a queue.** The oldest bases here predate
current cvc5 by years; `bvBbExtf` sits on a 2016 commit. The register keeps
those rows because the idea is a candidate, not because the patch is one, and
below roughly a thousand commits a clean-looking update is more likely to have
dropped the mechanism than preserved it. A report that such a branch should be
reimplemented rather than rebased is the useful outcome.
