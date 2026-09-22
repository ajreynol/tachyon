# Active development branches

**What this is.** Every branch of [`ajreynol/cvc5`](https://github.com/ajreynol/cvc5)
that heuresis calls **active**, and which cvc5 commit each one contains. It
exists so a pass to bring them up to date — by a person or an agent — can start
from one file instead of from the register.

**Active means: named by a proposal row** in a research direction's table in
[`directions.md`](directions.md#proposals). That register is authoritative; this
file is derived from it and from the fork, and is **not** a place to add a
branch. A branch earns a row here by first earning a proposal row there.

**Every commit is named by sha.** Nothing here says *master* or *main* as a
state, because those are different commits on different days: a file that said
"up to date with master" would be quietly wrong a week later, and so would a
distance measured against it. The same rule governs [`progress.md`](progress.md):
*the exact cvc5 `main` revision, not "current main"*.

**Elaphros keeps its own.** The 23 active branches of the sibling project are in
[its register](../../elaphros/docs/directions.md#proposals) and are not listed
here; the two projects do not write in each other's directories.

**A branch being current is not a result.** Nothing here says a branch helps.
The `± solved` column of the register stays empty until the branch is built and
run on `quant-07-25` against the reference.

## State

**Read 2026-09-22.** The pin this file measures against is cvc5
[`c2cc3caf`](https://github.com/cvc5/cvc5/commit/c2cc3caf78414931b0feaed26a05c4426ed96098) (2026-09-21), which is what
`ajreynol/cvc5` `master` pointed at when it was read. cvc5 `main` had already
moved on to [`ab20a7cc`](https://github.com/cvc5/cvc5/commit/ab20a7cc3d6ff62cc4721a8a57aa4502f6ef2328), 3 commits further, so a branch
carrying the pin is current with the fork's copy, not with upstream.

| | |
| --- | --- |
| active branches | **72**, across 25 of the 27 research directions |
| contain `c2cc3caf` | **25**, every one by merge rather than rebase |
| older | **47**, sitting 126 to 9371 commits back |

**How the current ones got there.** Every one is a `Merge branch 'master' into
…` tip, adding one merge commit to the branch. That is enough to build and
measure, and the `± LOC` below is a three-dot diff against `c2cc3caf`, so it
still reports only the branch's own changes. It is not a linear patch series,
which is what an upstream review will ask for; linearising is work deferred,
not work avoided.

**The fork moves under this file.** Thirty-six branches changed between the
2026-09-21 reading and this one, and the pin itself changed twice that day.
Re-derive before acting, naming the commit you derived against:

```bash
git clone --filter=tree:0 --bare https://github.com/ajreynol/cvc5 fork.git
PIN=$(git --git-dir=fork.git rev-parse master)           # name it, then use the sha
git --git-dir=fork.git merge-base $PIN BRANCH            # the commit it contains
git --git-dir=fork.git rev-list --count BRANCH..$PIN     # 0 means it carries the pin
git --git-dir=fork.git rev-list --count $PIN..BRANCH     # its own commits
git --git-dir=fork.git rev-list --parents -n1 BRANCH     # two parents: a merge
```

## Bringing a branch up to date

1. **Prefer a rebase onto the pin you chose**, keeping the branch's own
   commits. Merging is acceptable and is what the first pass did — it makes the
   branch current, which is what a measurement needs — but record which was
   done and onto which sha, because only one of them leaves a reviewable series.
2. **One branch at a time**, and no unrelated work squashed in.
3. **Do not force a resolution.** A rebase that will not come out cleanly is a
   result: report the conflicts. How large and how conflicted it is is part of
   what the proposal costs, and a branch better reimplemented than updated can
   retire its proposal row — which is progress, not failure.
4. **Check the diff against the register.** If the source diff has collapsed to
   nothing, or lost the mechanism the direction names, the update dropped
   content. Say so rather than recording a small diff.
5. **Report, per branch:** new tip, the sha it now contains, diffstat, and
   whether it builds and passes `make regress`.
6. **Then update two places:** the `rebased to` and `± LOC` cells of the
   proposal row in [`directions.md`](directions.md#proposals), and the row here.

## Carrying `c2cc3caf` — 25 branches

Ready to build and measure. `± LOC` is the three-dot source diff against
[`c2cc3caf`](https://github.com/cvc5/cvc5/commit/c2cc3caf78414931b0feaed26a05c4426ed96098), `src/` only.

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

## Older than `c2cc3caf` — 47 branches

Nearest first; the last column is commits behind the pin. Nothing here can be
built, measured or reviewed as it stands. The work order derived from this
section is `rebase-to-master-round2.txt`.

| branch | direction | newest cvc5 commit it contains | its commits | behind `c2cc3caf` |
| --- | --- | --- | ---: | ---: |
| [`jhRandom`](https://github.com/ajreynol/cvc5/tree/jhRandom) | [R11](directions.md#r11--decision-heuristic-versus-relevancy-what-the-sat-solver-is-made-to-decide-on) | [`f888519`](https://github.com/cvc5/cvc5/commit/f88851967fbfde8c1815f0bc641af5d48b8a8a87) (2026-06-29) | 3 | **126** |
| [`ai-jhRlvInst`](https://github.com/ajreynol/cvc5/tree/ai-jhRlvInst) | [R10](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | [`09668f2`](https://github.com/cvc5/cvc5/commit/09668f2e865a2c21335a7da238406066b2b1f938) (2026-06-17) | 3 | **140** |
| [`claudeDev-dts-idef`](https://github.com/ajreynol/cvc5/tree/claudeDev-dts-idef) | [R10](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | [`8c86597`](https://github.com/cvc5/cvc5/commit/8c8659731a1e1286efb5f3895aac540c1faa307c) (2026-06-09) | 3 | **153** |
| [`dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3) | [R15](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | [`f4f9779`](https://github.com/cvc5/cvc5/commit/f4f977983984497e9797038e5906b668063e535a) (2026-05-14) | 31 | **193** |
| [`ai-emFilter`](https://github.com/ajreynol/cvc5/tree/ai-emFilter) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | [`5509c56`](https://github.com/cvc5/cvc5/commit/5509c567cde03ce2369cf63ab61ef0c77f353027) (2026-04-23) | 11 | **230** |
| [`ai-fixAlphaEq-2`](https://github.com/ajreynol/cvc5/tree/ai-fixAlphaEq-2) | [R21](directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | [`f172d88`](https://github.com/cvc5/cvc5/commit/f172d88a2e02f979605bc4572fa710c2749deba7) (2026-04-17) | 27 | **243** |
| [`ai-extEagerInst3-1`](https://github.com/ajreynol/cvc5/tree/ai-extEagerInst3-1) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | [`01be634`](https://github.com/cvc5/cvc5/commit/01be63481269d7bd859c0301aa290e4dd949e77b) (2026-04-14) | 183 | **250** |
| [`instLastCallDelay`](https://github.com/ajreynol/cvc5/tree/instLastCallDelay) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | [`5c6b53b`](https://github.com/cvc5/cvc5/commit/5c6b53b365c187a91cc6f2715474d9dc8e405597) (2026-03-29) | 1 | **282** |
| [`ai-imgDirect`](https://github.com/ajreynol/cvc5/tree/ai-imgDirect) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | [`c2c4dd4`](https://github.com/cvc5/cvc5/commit/c2c4dd49ccf9473ab74f5ee738a56da6b204dbe8) (2026-03-12) | 3 | **327** |
| [`ai-quantOpt-1`](https://github.com/ajreynol/cvc5/tree/ai-quantOpt-1) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | [`57561fa`](https://github.com/cvc5/cvc5/commit/57561fa37a431da4a07791ca70d7f27040223f93) (2026-03-12) | 1 | **329** |
| [`bvToIntQuant-031126`](https://github.com/ajreynol/cvc5/tree/bvToIntQuant-031126) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | [`6fa07bf`](https://github.com/cvc5/cvc5/commit/6fa07bf4dfce147a73d9142d62a3c534cfcfec10) (2026-03-11) | 2 | **333** |
| [`simplifyRecFun`](https://github.com/ajreynol/cvc5/tree/simplifyRecFun) | [R20](directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | [`398316d`](https://github.com/cvc5/cvc5/commit/398316d6ed350f4bf86602231184dc9f12f08aaa) (2026-02-20) | 58 | **374** |
| [`emExp`](https://github.com/ajreynol/cvc5/tree/emExp) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | [`310f487`](https://github.com/cvc5/cvc5/commit/310f487e6a829fb1bdfbef2849536176b047606e) (2025-11-11) | 6 | **516** |
| [`oneConsInst`](https://github.com/ajreynol/cvc5/tree/oneConsInst) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | [`1120e3d`](https://github.com/cvc5/cvc5/commit/1120e3df17caa4154cc2974136dd993ee12489b2) (2025-11-05) | 3 | **524** |
| [`imTrivial`](https://github.com/ajreynol/cvc5/tree/imTrivial) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | [`aeb5547`](https://github.com/cvc5/cvc5/commit/aeb554775be7eb9eb59f640fa76ee90879e19746) (2025-10-29) | 9 | **531** |
| [`imSimpleInc2`](https://github.com/ajreynol/cvc5/tree/imSimpleInc2) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | [`aeb5547`](https://github.com/cvc5/cvc5/commit/aeb554775be7eb9eb59f640fa76ee90879e19746) (2025-10-29) | 7 | **531** |
| [`dtElim`](https://github.com/ajreynol/cvc5/tree/dtElim) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | [`aeb5547`](https://github.com/cvc5/cvc5/commit/aeb554775be7eb9eb59f640fa76ee90879e19746) (2025-10-29) | 26 | **531** |
| [`cdno`](https://github.com/ajreynol/cvc5/tree/cdno) | [R15](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | [`d509acd`](https://github.com/cvc5/cvc5/commit/d509acd588d64ed54e569f5117df355cc02a2d79) (2025-09-09) | 16 | **602** |
| [`debugDumpLemmas`](https://github.com/ajreynol/cvc5/tree/debugDumpLemmas) | [R26](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | [`f7db8fa`](https://github.com/cvc5/cvc5/commit/f7db8faac6639980ed61a1920042ded79cd15e21) (2025-09-03) | 5 | **612** |
| [`eagerQM`](https://github.com/ajreynol/cvc5/tree/eagerQM) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | [`aca9908`](https://github.com/cvc5/cvc5/commit/aca99089d0de4fa9292227af36f25c5499024a3c) (2025-08-28) | 3 | **617** |
| [`deferBlock`](https://github.com/ajreynol/cvc5/tree/deferBlock) | [R17](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | [`2ae4ede`](https://github.com/cvc5/cvc5/commit/2ae4ede42a9b876e5715620dbeee63fcfe89ce11) (2025-08-25) | 19 | **619** |
| [`eagerElimDefs`](https://github.com/ajreynol/cvc5/tree/eagerElimDefs) | [R20](directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | [`9e7ee41`](https://github.com/cvc5/cvc5/commit/9e7ee41e7c50a972afd6f7210ecf94d798beb235) (2024-10-04) | 9 | **1286** |
| [`tdbLLOpts`](https://github.com/ajreynol/cvc5/tree/tdbLLOpts) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | [`8b0a628`](https://github.com/cvc5/cvc5/commit/8b0a6283a374109a9c73c63699f1cc519b36dcc5) (2024-09-10) | 2 | **1345** |
| [`linearSolverSub`](https://github.com/ajreynol/cvc5/tree/linearSolverSub) | [R17](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | [`9a741c0`](https://github.com/cvc5/cvc5/commit/9a741c0a99f7451273b0bbce8cb7e2eec20148b8) (2024-08-24) | 10 | **1356** |
| [`instFullPreempt`](https://github.com/ajreynol/cvc5/tree/instFullPreempt) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | [`0a48958`](https://github.com/cvc5/cvc5/commit/0a4895827815bed1a43c4c2121a619c7c7293bdf) (2024-08-12) | 1 | **1377** |
| [`trackInferId`](https://github.com/ajreynol/cvc5/tree/trackInferId) | [R26](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | [`58a68cf`](https://github.com/cvc5/cvc5/commit/58a68cfb9e47635b7252fd999d0f4af9dae6e821) (2024-04-17) | 1 | **1823** |
| [`nestedTriggers`](https://github.com/ajreynol/cvc5/tree/nestedTriggers) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | [`5ef7a7f`](https://github.com/cvc5/cvc5/commit/5ef7a7fedeee39ed77f8717bc434894a2e294e0d) (2023-11-11) | 2 | **2193** |
| [`simpleTriggerMore`](https://github.com/ajreynol/cvc5/tree/simpleTriggerMore) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | [`4c2037d`](https://github.com/cvc5/cvc5/commit/4c2037dad676f5e67a274a60ee1be17a837bab87) (2023-11-02) | 2 | **2202** |
| [`emStratify`](https://github.com/ajreynol/cvc5/tree/emStratify) | [R7](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | [`78e58a5`](https://github.com/cvc5/cvc5/commit/78e58a5ca5504d1794ba961179cae4c0f5405850) (2023-11-01) | 17 | **2205** |
| [`p657`](https://github.com/ajreynol/cvc5/tree/p657) | [R21](directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | [`43c1d0f`](https://github.com/cvc5/cvc5/commit/43c1d0f6815c58f30b6c0b405080da169f56fc04) (2023-08-23) | 4 | **2353** |
| [`isActiveLemma`](https://github.com/ajreynol/cvc5/tree/isActiveLemma) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`51aa806`](https://github.com/cvc5/cvc5/commit/51aa8060989af2d8a626adcc18efb088bcbd1438) (2023-08-18) | 50 | **2368** |
| [`ufConvRlv`](https://github.com/ajreynol/cvc5/tree/ufConvRlv) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | [`2f859d8`](https://github.com/cvc5/cvc5/commit/2f859d837dd3c6d055c021bc5cb55f537644bcf1) (2023-01-23) | 2 | **2719** |
| [`fmfIeval`](https://github.com/ajreynol/cvc5/tree/fmfIeval) | [R7](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | [`6df8e7a`](https://github.com/cvc5/cvc5/commit/6df8e7ab6d3497844cbbd428de47dc9c7a0a65a9) (2022-08-28) | 2 | **3002** |
| [`smtLazyAssert`](https://github.com/ajreynol/cvc5/tree/smtLazyAssert) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`1c41fda`](https://github.com/cvc5/cvc5/commit/1c41fdaef2639ab81737bca2bda33d385157bda7) (2022-08-03) | 21 | **3039** |
| [`dtLazyInst3`](https://github.com/ajreynol/cvc5/tree/dtLazyInst3) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | [`9fe8509`](https://github.com/cvc5/cvc5/commit/9fe8509ed935c094469a7a108d59b854aaa71b35) (2022-05-16) | 18 | **3207** |
| [`emFailMasks`](https://github.com/ajreynol/cvc5/tree/emFailMasks) | [R3](directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | [`2e555b3`](https://github.com/cvc5/cvc5/commit/2e555b3cac196cb141a3a4dbf934f282bfbdd723) (2022-04-20) | 27 | **3319** |
| [`refactorQcf`](https://github.com/ajreynol/cvc5/tree/refactorQcf) | [R6](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | [`51d731e`](https://github.com/cvc5/cvc5/commit/51d731ec403becd8a46e02933112ff2fc6b310e9) (2022-01-26) | 18 | **3875** |
| [`virtualLemma`](https://github.com/ajreynol/cvc5/tree/virtualLemma) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`8fe459b`](https://github.com/cvc5/cvc5/commit/8fe459b1fb3843ebdbda86f24a414c46b986aa90) (2021-10-19) | 10 | **4424** |
| [`cacheEntCheck`](https://github.com/ajreynol/cvc5/tree/cacheEntCheck) | [R3](directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | [`b446953`](https://github.com/cvc5/cvc5/commit/b4469530d2f6de599ddf7207a1914b88be49de5b) (2021-10-15) | 5 | **4433** |
| [`virtualClauseDel`](https://github.com/ajreynol/cvc5/tree/virtualClauseDel) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`55ce505`](https://github.com/cvc5/cvc5/commit/55ce505ca757dc241bf4c1e10023bc43ac531a23) (2021-10-13) | 15 | **4444** |
| [`carryInst`](https://github.com/ajreynol/cvc5/tree/carryInst) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | [`54490c6`](https://github.com/cvc5/cvc5/commit/54490c6053d51910f5f7c2160451ad4d36fe6946) (2021-07-28) | 3 | **4805** |
| [`qcfClean`](https://github.com/ajreynol/cvc5/tree/qcfClean) | [R6](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | [`b3c6975`](https://github.com/cvc5/cvc5/commit/b3c6975af6354eb027aa52d6a23386b5dd0ef1cd) (2021-03-25) | 8 | **5405** |
| [`gttOpt`](https://github.com/ajreynol/cvc5/tree/gttOpt) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | [`2c4025e`](https://github.com/cvc5/cvc5/commit/2c4025e44771707ba548b6d8aa5a8a13ec3cd8f1) (2021-01-27) | 1 | **5720** |
| [`dtInstMode`](https://github.com/ajreynol/cvc5/tree/dtInstMode) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | [`9e481fa`](https://github.com/cvc5/cvc5/commit/9e481faf7dfce8f992ae6730ad49f6db335b6432) (2020-10-10) | 2 | **6100** |
| [`optTdbTNode`](https://github.com/ajreynol/cvc5/tree/optTdbTNode) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | [`a6bd02c`](https://github.com/cvc5/cvc5/commit/a6bd02c5c442b806b5e01fed40ab9d1017e42bc3) (2019-03-26) | 1 | **7581** |
| [`perfDataStructures`](https://github.com/ajreynol/cvc5/tree/perfDataStructures) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | [`047e75b`](https://github.com/cvc5/cvc5/commit/047e75b485ad16a729083c210ba4064943d2e7c5) (2018-08-07) | 31 | **8174** |
| [`bvBbExtf`](https://github.com/ajreynol/cvc5/tree/bvBbExtf) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | [`be7662b`](https://github.com/cvc5/cvc5/commit/be7662bdcd3881d349bfba4c959a0c2be4159ce9) (2016-12-08) | 5 | **9371** |

**The far end is design evidence, not a queue.** The oldest commits carried here
predate current cvc5 by years; `bvBbExtf` holds one from 2016. The register
keeps those rows because the idea is a candidate, not because the patch is one,
and below roughly a thousand commits a clean-looking update is more likely to
have dropped the mechanism than preserved it. A report that such a branch should
be reimplemented rather than updated is the useful outcome.
