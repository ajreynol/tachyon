# Active development branches

**What this is.** Every branch of [`ajreynol/cvc5`](https://github.com/ajreynol/cvc5)
that heuresis calls **active**, and which cvc5 commit each one carries. It
exists so a pass to bring them up to date — by a person or an agent — can start
from one file instead of from the register. The list of what still needs doing
is the second table; there is no separate work-order file.

**Active means: named by a proposal row** in a research direction's table in
[`directions.md`](directions.md#proposals). That register is authoritative; this
file is derived from it and from the fork, and is **not** a place to add a
branch. A branch earns a row here by first earning a proposal row there.

**Every commit is named by sha.** Nothing here says *master* or *main* as a
state, because those are different commits on different days: a file that said
"up to date with master" would be quietly wrong a week later, and so would a
distance measured against it. The same rule governs [`progress.md`](progress.md):
*the exact cvc5 `main` revision, not "current main"*.

**Elaphros keeps its own.** The 24 active branches of the sibling project are in
[its register](../../elaphros/docs/directions.md#proposals) and are not listed
here; the two projects do not write in each other's directories.

**A branch carrying the pin is not a result.** Nothing here says a branch helps.
The `± solved` column of the register stays empty until the branch is built and
run on `quant-07-25` against the reference. None of these has been built.

## State

**Read 2026-09-22, after the second update pass.** The pin both passes targeted
is cvc5 [`c2cc3caf`](https://github.com/cvc5/cvc5/commit/c2cc3caf78414931b0feaed26a05c4426ed96098) (2026-09-21). Since then the
fork's `master` has advanced to [`ab20a7cc`](https://github.com/cvc5/cvc5/commit/ab20a7cc3d6ff62cc4721a8a57aa4502f6ef2328)
and cvc5 `main` to [`64640792`](https://github.com/cvc5/cvc5/commit/64640792e6430a607cffe34f4acc361b412dc66d),
so a branch carrying the pin is three or four commits off the newest upstream —
current enough to build and measure, and **not** work to redo. A third pass
should name its own fresh pin and re-read this file against it.

| | |
| --- | --- |
| active branches | **72**, across 25 of the 27 research directions |
| carry `c2cc3caf` | **52** — 50 with their changes intact, **2 emptied by the merge** |
| older | **20**, carrying commits 243 to 9371 commits back |

**How they got there: merges, not rebases, in both passes.** Every current tip
is a `Merge branch 'master' into …` commit. That is enough to build and
measure, and `± LOC` below is a three-dot diff against the pin, so it still
reports only the branch's own changes. It is not a linear patch series, which
is what an upstream review will ask for; linearising is deferred, not avoided.

### Two merges dropped the branch's changes

The second pass resolved four merges in favour of upstream, leaving the branch
identical to the pin; two of the four are heuresis's and are listed here, the
other two are elaphros's and are recorded in
[its register](../../elaphros/docs/directions.md#proposals). Their proposal
rows now describe nothing. This is the
failure the procedure below warns about, and it is why the diff is checked
rather than assumed:

| branch | direction | what was lost | tip that still holds it |
| --- | --- | --- | --- |
| [`fmfIeval`](https://github.com/ajreynol/cvc5/tree/fmfIeval) | [R7](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 5 src files, +40/−22 | `61156a62b2` |
| [`bvToIntQuant-031126`](https://github.com/ajreynol/cvc5/tree/bvToIntQuant-031126) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | 1 src file, +60/−16 | `163e60360b` |

The pre-merge tips above were read from this project's own 2026-09-22 snapshot,
not from a rollback file, and each is the commit to recover the work from. Redo
these four onto a named pin and check the resulting diff before recording
anything about them.

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
   commits. Merging is acceptable and is what both passes did — it makes the
   branch current, which is what a measurement needs — but record which was
   done and onto which sha, because only one of them leaves a reviewable series.
2. **One branch at a time**, and no unrelated work squashed in.
3. **Check the source diff after every update.** If it has collapsed to
   nothing, or lost the mechanism the direction names, the update dropped
   content — as four merges did in the second pass. Report it and keep the
   pre-update tip; do not record a small diff as if it were the branch.
4. **Do not force a resolution.** A rebase that will not come out cleanly is a
   result: report the conflicts. How large and how conflicted it is is part of
   what the proposal costs, and a branch better reimplemented than updated can
   retire its proposal row — which is progress, not failure.
5. **Report, per branch:** new tip, the sha it now carries, diffstat, and
   whether it builds and passes `make regress`.
6. **Then update two places:** the `rebased to` and `± LOC` cells of the
   proposal row in [`directions.md`](directions.md#proposals), and the row here.

## Carrying `c2cc3caf` — 52 branches

`± LOC` is the three-dot source diff against [`c2cc3caf`](https://github.com/cvc5/cvc5/commit/c2cc3caf78414931b0feaed26a05c4426ed96098), `src/` only.

| branch | direction | how | its commits | ± LOC |
| --- | --- | --- | ---: | ---: |
| [`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | merge | 7 | +1455/−8 over 13 src files |
| [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | merge | 180 | +3771/−37 over 38 src files |
| [`ai-extEagerInst3-1`](https://github.com/ajreynol/cvc5/tree/ai-extEagerInst3-1) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | merge | 184 | +4057/−38 over 39 src files |
| [`instFullPreempt`](https://github.com/ajreynol/cvc5/tree/instFullPreempt) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | merge | 2 | +11/−1 over 2 src files |
| [`ai-emFilter`](https://github.com/ajreynol/cvc5/tree/ai-emFilter) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | merge | 12 | +758/−15 over 20 src files |
| [`imTrivial`](https://github.com/ajreynol/cvc5/tree/imTrivial) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | merge | 10 | +264/−21 over 14 src files |
| [`imSimpleInc2`](https://github.com/ajreynol/cvc5/tree/imSimpleInc2) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | merge | 8 | +124/−23 over 4 src files |
| [`ai-imgDirect`](https://github.com/ajreynol/cvc5/tree/ai-imgDirect) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | merge | 4 | +704/−4 over 5 src files |
| [`ai-quantOpt-1`](https://github.com/ajreynol/cvc5/tree/ai-quantOpt-1) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | merge | 2 | +47/−4 over 2 src files |
| [`ai-prepared13`](https://github.com/ajreynol/cvc5/tree/ai-prepared13) | [R3](directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | merge | 12 | +291/−6 over 4 src files |
| [`termOrigin`](https://github.com/ajreynol/cvc5/tree/termOrigin) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | merge | 16 | +474/−11 over 19 src files |
| [`instLastCallDelay`](https://github.com/ajreynol/cvc5/tree/instLastCallDelay) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | merge | 2 | +2/−2 over 1 src files |
| [`dtInstMode`](https://github.com/ajreynol/cvc5/tree/dtInstMode) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | merge | 3 | +14/−1 over 2 src files |
| [`multiTriggerSingleBase`](https://github.com/ajreynol/cvc5/tree/multiTriggerSingleBase) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | merge | 2 | +43/−0 over 3 src files |
| [`nestedTriggers`](https://github.com/ajreynol/cvc5/tree/nestedTriggers) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | merge | 3 | +40/−22 over 4 src files |
| [`simpleTriggerMore`](https://github.com/ajreynol/cvc5/tree/simpleTriggerMore) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | merge | 3 | +52/−33 over 3 src files |
| [`gttOpt`](https://github.com/ajreynol/cvc5/tree/gttOpt) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | merge | 2 | +9/−1 over 2 src files |
| [`ai-cbqi-0423`](https://github.com/ajreynol/cvc5/tree/ai-cbqi-0423) | [R6](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | merge | 5 | +136/−87 over 1 src files |
| [`ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) | [R7](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | merge | 4 | +165/−43 over 8 src files |
| [`fmfIeval`](https://github.com/ajreynol/cvc5/tree/fmfIeval) | [R7](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | merge | 3 | **empty — dropped +40/−22** |
| [`notifySatClause`](https://github.com/ajreynol/cvc5/tree/notifySatClause) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | merge | 5 | +49/−10 over 6 src files |
| [`ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) | [R10](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | merge | 3 | +116/−32 over 11 src files |
| [`ai-jhRlvInst`](https://github.com/ajreynol/cvc5/tree/ai-jhRlvInst) | [R10](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | merge | 4 | +326/−18 over 9 src files |
| [`ai-jhConflictFirst`](https://github.com/ajreynol/cvc5/tree/ai-jhConflictFirst) | [R10](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | merge | 3 | +93/−33 over 9 src files |
| [`claudeDev-dts-idef`](https://github.com/ajreynol/cvc5/tree/claudeDev-dts-idef) | [R10](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | merge | 4 | +179/−37 over 13 src files |
| [`jhRandom`](https://github.com/ajreynol/cvc5/tree/jhRandom) | [R11](directions.md#r11--decision-heuristic-versus-relevancy-what-the-sat-solver-is-made-to-decide-on) | merge | 4 | +262/−20 over 7 src files |
| [`subConflict`](https://github.com/ajreynol/cvc5/tree/subConflict) | [R12](directions.md#r12--lemma-inprocessing-and-conflict-minimisation) | merge | 9 | +332/−1 over 12 src files |
| [`cadicalPortfolio`](https://github.com/ajreynol/cvc5/tree/cadicalPortfolio) | [R13](directions.md#r13--the-sat-backend-cadical-minisat-restarts-units) | merge | 3 | +50/−0 over 1 src files |
| [`mbtc25`](https://github.com/ajreynol/cvc5/tree/mbtc25) | [R14](directions.md#r14--theory-combination-care-graph-or-model-based) | merge | 30 | +365/−82 over 15 src files |
| [`ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare) | [R15](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | merge | 3 | +9/−3 over 1 src files |
| [`dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3) | [R15](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | merge | 32 | +378/−72 over 10 src files |
| [`cdno`](https://github.com/ajreynol/cvc5/tree/cdno) | [R15](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | merge | 17 | +168/−12 over 5 src files |
| [`dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | merge | 3 | +61/−8 over 2 src files |
| [`dtLazyInst3`](https://github.com/ajreynol/cvc5/tree/dtLazyInst3) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | merge | 19 | +82/−4 over 3 src files |
| [`oneConsInst`](https://github.com/ajreynol/cvc5/tree/oneConsInst) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | merge | 4 | +42/−11 over 2 src files |
| [`ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc) | [R17](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | merge | 4 | +95/−2 over 6 src files |
| [`deferBlock`](https://github.com/ajreynol/cvc5/tree/deferBlock) | [R17](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | merge | 20 | +330/−16 over 15 src files |
| [`bitblastLc`](https://github.com/ajreynol/cvc5/tree/bitblastLc) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | merge | 2 | +28/−1 over 2 src files |
| [`bvToIntQuant-031126`](https://github.com/ajreynol/cvc5/tree/bvToIntQuant-031126) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | merge | 3 | **empty — dropped +60/−16** |
| [`ufConvRlv`](https://github.com/ajreynol/cvc5/tree/ufConvRlv) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | merge | 3 | +12/−4 over 3 src files |
| [`ufEagerDistinct`](https://github.com/ajreynol/cvc5/tree/ufEagerDistinct) | [R20](directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | merge | 2 | +25/−0 over 3 src files |
| [`simplifyRecFun`](https://github.com/ajreynol/cvc5/tree/simplifyRecFun) | [R20](directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | merge | 59 | +101/−39 over 11 src files |
| [`quantRew-1006`](https://github.com/ajreynol/cvc5/tree/quantRew-1006) | [R21](directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | merge | 3 | +27/−4 over 1 src files |
| [`preregRlv`](https://github.com/ajreynol/cvc5/tree/preregRlv) | [R22](directions.md#r22--preregistration-which-literals-the-theories-are-told-about) | merge | 156 | +833/−13 over 9 src files |
| [`tdbOldIndex`](https://github.com/ajreynol/cvc5/tree/tdbOldIndex) | [R23](directions.md#r23--term-database-relevance-which-ground-terms-e-matching-may-use) | merge | 6 | +61/−7 over 5 src files |
| [`lowLevelOptMore`](https://github.com/ajreynol/cvc5/tree/lowLevelOptMore) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | merge | 12 | +72/−8 over 2 src files |
| [`tdbLLOpts`](https://github.com/ajreynol/cvc5/tree/tdbLLOpts) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | merge | 3 | +34/−34 over 2 src files |
| [`qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) | [R26](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | merge | 31 | +534/−15 over 19 src files |
| [`debugDumpLemmas`](https://github.com/ajreynol/cvc5/tree/debugDumpLemmas) | [R26](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | merge | 6 | +49/−0 over 5 src files |
| [`trackInferId`](https://github.com/ajreynol/cvc5/tree/trackInferId) | [R26](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | merge | 2 | +22/−3 over 3 src files |
| [`ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt) | [R27](directions.md#r27--smt-lib-parser-throughput-pay-less-before-solving) | merge | 3 | +228/−141 over 7 src files |
| [`eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi) | [R28](directions.md#r28--eager-conflict-based-instantiation-find-a-useful-instance-before-full-effort) | merge | 205 | +5248/−202 over 58 src files |

## Older than `c2cc3caf` — 20 branches

**This is the work order for the next pass.** Nearest first; the last column is
commits behind the pin. Nothing here can be built, measured or reviewed as it
stands.

| branch | direction | newest cvc5 commit it carries | its commits | behind `c2cc3caf` |
| --- | --- | --- | ---: | ---: |
| [`ai-fixAlphaEq-2`](https://github.com/ajreynol/cvc5/tree/ai-fixAlphaEq-2) | [R21](directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | [`f172d88`](https://github.com/cvc5/cvc5/commit/f172d88a2e02f979605bc4572fa710c2749deba7) (2026-04-17) | 27 | **243** |
| [`emExp`](https://github.com/ajreynol/cvc5/tree/emExp) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | [`310f487`](https://github.com/cvc5/cvc5/commit/310f487e6a829fb1bdfbef2849536176b047606e) (2025-11-11) | 6 | **516** |
| [`dtElim`](https://github.com/ajreynol/cvc5/tree/dtElim) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | [`aeb5547`](https://github.com/cvc5/cvc5/commit/aeb554775be7eb9eb59f640fa76ee90879e19746) (2025-10-29) | 26 | **531** |
| [`eagerQM`](https://github.com/ajreynol/cvc5/tree/eagerQM) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | [`aca9908`](https://github.com/cvc5/cvc5/commit/aca99089d0de4fa9292227af36f25c5499024a3c) (2025-08-28) | 3 | **617** |
| [`eagerElimDefs`](https://github.com/ajreynol/cvc5/tree/eagerElimDefs) | [R20](directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | [`9e7ee41`](https://github.com/cvc5/cvc5/commit/9e7ee41e7c50a972afd6f7210ecf94d798beb235) (2024-10-04) | 9 | **1286** |
| [`linearSolverSub`](https://github.com/ajreynol/cvc5/tree/linearSolverSub) | [R17](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | [`9a741c0`](https://github.com/cvc5/cvc5/commit/9a741c0a99f7451273b0bbce8cb7e2eec20148b8) (2024-08-24) | 10 | **1356** |
| [`emStratify`](https://github.com/ajreynol/cvc5/tree/emStratify) | [R7](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | [`78e58a5`](https://github.com/cvc5/cvc5/commit/78e58a5ca5504d1794ba961179cae4c0f5405850) (2023-11-01) | 17 | **2205** |
| [`p657`](https://github.com/ajreynol/cvc5/tree/p657) | [R21](directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | [`43c1d0f`](https://github.com/cvc5/cvc5/commit/43c1d0f6815c58f30b6c0b405080da169f56fc04) (2023-08-23) | 4 | **2353** |
| [`isActiveLemma`](https://github.com/ajreynol/cvc5/tree/isActiveLemma) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`51aa806`](https://github.com/cvc5/cvc5/commit/51aa8060989af2d8a626adcc18efb088bcbd1438) (2023-08-18) | 50 | **2368** |
| [`smtLazyAssert`](https://github.com/ajreynol/cvc5/tree/smtLazyAssert) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`1c41fda`](https://github.com/cvc5/cvc5/commit/1c41fdaef2639ab81737bca2bda33d385157bda7) (2022-08-03) | 21 | **3039** |
| [`emFailMasks`](https://github.com/ajreynol/cvc5/tree/emFailMasks) | [R3](directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | [`2e555b3`](https://github.com/cvc5/cvc5/commit/2e555b3cac196cb141a3a4dbf934f282bfbdd723) (2022-04-20) | 27 | **3319** |
| [`refactorQcf`](https://github.com/ajreynol/cvc5/tree/refactorQcf) | [R6](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | [`51d731e`](https://github.com/cvc5/cvc5/commit/51d731ec403becd8a46e02933112ff2fc6b310e9) (2022-01-26) | 18 | **3875** |
| [`virtualLemma`](https://github.com/ajreynol/cvc5/tree/virtualLemma) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`8fe459b`](https://github.com/cvc5/cvc5/commit/8fe459b1fb3843ebdbda86f24a414c46b986aa90) (2021-10-19) | 10 | **4424** |
| [`cacheEntCheck`](https://github.com/ajreynol/cvc5/tree/cacheEntCheck) | [R3](directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | [`b446953`](https://github.com/cvc5/cvc5/commit/b4469530d2f6de599ddf7207a1914b88be49de5b) (2021-10-15) | 5 | **4433** |
| [`virtualClauseDel`](https://github.com/ajreynol/cvc5/tree/virtualClauseDel) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`55ce505`](https://github.com/cvc5/cvc5/commit/55ce505ca757dc241bf4c1e10023bc43ac531a23) (2021-10-13) | 15 | **4444** |
| [`carryInst`](https://github.com/ajreynol/cvc5/tree/carryInst) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | [`54490c6`](https://github.com/cvc5/cvc5/commit/54490c6053d51910f5f7c2160451ad4d36fe6946) (2021-07-28) | 3 | **4805** |
| [`qcfClean`](https://github.com/ajreynol/cvc5/tree/qcfClean) | [R6](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | [`b3c6975`](https://github.com/cvc5/cvc5/commit/b3c6975af6354eb027aa52d6a23386b5dd0ef1cd) (2021-03-25) | 8 | **5405** |
| [`optTdbTNode`](https://github.com/ajreynol/cvc5/tree/optTdbTNode) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | [`a6bd02c`](https://github.com/cvc5/cvc5/commit/a6bd02c5c442b806b5e01fed40ab9d1017e42bc3) (2019-03-26) | 1 | **7581** |
| [`perfDataStructures`](https://github.com/ajreynol/cvc5/tree/perfDataStructures) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | [`047e75b`](https://github.com/cvc5/cvc5/commit/047e75b485ad16a729083c210ba4064943d2e7c5) (2018-08-07) | 31 | **8174** |
| [`bvBbExtf`](https://github.com/ajreynol/cvc5/tree/bvBbExtf) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | [`be7662b`](https://github.com/cvc5/cvc5/commit/be7662bdcd3881d349bfba4c959a0c2be4159ce9) (2016-12-08) | 5 | **9371** |

**The far end is design evidence, not a queue.** The oldest commits carried here
predate current cvc5 by years; `bvBbExtf` holds one from 2016. The register
keeps those rows because the idea is a candidate, not because the patch is one,
and below roughly a thousand commits an update is more likely to drop the
mechanism than to preserve it — which is no longer hypothetical. A report that
such a branch should be reimplemented rather than updated is the useful outcome.
