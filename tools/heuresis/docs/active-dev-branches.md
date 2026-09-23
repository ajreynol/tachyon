# Active development branches

**What this is.** Every branch of [`ajreynol/cvc5`](https://github.com/ajreynol/cvc5)
that heuresis calls **active**: which cvc5 commit each one carries, how large it
is, and whether it compiles. It exists so a pass over them — by a person or an
agent — can start from one file instead of from the register. What still needs
updating is the second table; there is no separate work-order file.

**Seven branches were retired on 2026-09-22** and are listed at the bottom
rather than dropped in silence: the update pass could not bring them onto a
current commit, and why not is a finding about what upstream changed underneath
them.

**Active means: named by a proposal row** in a research direction's table in
[`directions.md`](directions.md#proposals). That register is authoritative; this
file is derived from it, from the fork, and from a build on the project's host.
It is **not** a place to add a branch: a branch earns a row here by first
earning a proposal row there.

**Every commit is named by sha.** Nothing here says *master* or *main* as a
state, because those are different commits on different days. The same rule
governs [`progress.md`](progress.md): *the exact cvc5 `main` revision, not
"current main"*.

**Elaphros keeps its own.** The 23 active branches of the sibling project are in
[its register](../../elaphros/docs/directions.md#proposals) and are not listed
here; the two projects do not write in each other's directories.

**Compiling is not a result.** A branch that builds has not been shown to help,
and two of the branches below compile *because* a merge emptied them. The
`± solved` column of the register stays empty until a branch is run on
`quant-07-25` against the reference.

## State

**Read 2026-09-22, after a third update pass.** The pin is cvc5
[`10bd5cb`](https://github.com/cvc5/cvc5/commit/10bd5cb3bb9ad9cb10277e0ae54e352e6d2ac345) (2026-09-22), which `ajreynol/cvc5` `master`
matched exactly when read — the fork was in sync with upstream, with nothing
between them.

| | |
| --- | --- |
| active branches | **65**, across 25 of the 27 research directions |
| within 6 commits of the pin | **52** — 50 with their changes intact, **2 emptied by a merge** |
| older | **13**, carrying commits 522 to 9377 back |
| compile-checked | **52 of 52** pass, 0 fail, 0 not yet run |

Three passes have now run: 37 branches on 2026-09-21, 33 more on 2026-09-22,
and 58 refreshed again the same day. **Every one was brought up by merging, not
by rebasing** — each current tip is a `Merge branch 'master' into …` commit.
That is enough to build and measure, and `± LOC` is a three-dot diff against
the pin, so it still reports only the branch's own changes. It is not the
linear series an upstream review will ask for.

### Two merges dropped the branch's changes, and still have

A merge in the second pass resolved in favour of upstream on four branches,
leaving them identical to the pin; the third pass merged again on top, which
carried the emptiness forward rather than repairing it. Two are heuresis's and
are listed here; the other two are elaphros's, recorded in
[its register](../../elaphros/docs/directions.md#proposals). Their proposal
rows describe nothing, and they compile for that reason.

| branch | direction | what was lost | tip that still holds it |
| --- | --- | --- | --- |
| [`fmfIeval`](https://github.com/ajreynol/cvc5/tree/fmfIeval) | [R7](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | 5 src files, +40/−22 | `61156a62b2` |
| [`bvToIntQuant-031126`](https://github.com/ajreynol/cvc5/tree/bvToIntQuant-031126) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | 1 src file, +60/−16 | `163e60360b` |

Recover the work from those tips, onto a named pin, and check the diff before
recording anything about them.

## The compile check

**Host and toolchain.** The project's benchmark host, 64 cores, building with
`/usr/bin/gcc10-c++` (GCC 10.5) — the compiler the host's existing cvc5 build
uses; the system default is GCC 7.3, which current cvc5 rejects. The build type
is `unrestricted`: **cvc5 has removed the `production` build type**, and
`configure.sh production` now fails, which is worth knowing before the next
time the host's own build is reconfigured.

Each branch is checked out at the exact tip in the table and built with
`make -j48` in one reused build directory, so after the first build each branch
compiles incrementally. A separate clone and build directory are used; the
host's own `~/cvc5-ajr` checkout and `~/builds-cvc5/ajr/prod` build are left
untouched, because the launcher measures from them.

**What a ✅ means:** the branch's source compiles and links against the pin,
and the figure beside it is that branch's incremental build time. It does not
mean the branch is correct, that its regressions pass, or that it helps. Only
the branches within 6 commits of the pin are built; an older branch would be
compiling a cvc5 from years ago, which answers nothing.

**All 52 pass, which is worth distrusting**, so the check was verified rather
than assumed: the binary built from
[`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst)
accepts `--eager-inst-limit=5`, and the binary built from the pin rejects it as
an unknown option. The branch's code is in the binary, and each branch is a real
rebuild — 4 to 75 seconds, median 41, against 107 for the pin from scratch.

## Within 6 commits of the pin — 52 branches

`± LOC` is the three-dot source diff against [`10bd5cb`](https://github.com/cvc5/cvc5/commit/10bd5cb3bb9ad9cb10277e0ae54e352e6d2ac345), `src/` only.

| branch | direction | carries | its commits | ± LOC | builds |
| --- | --- | --- | ---: | ---: | :-: |
| [`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 8 | +1455/−8 over 13 src files | ✅ 53s |
| [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 181 | +3771/−37 over 38 src files | ✅ 74s |
| [`ai-extEagerInst3-1`](https://github.com/ajreynol/cvc5/tree/ai-extEagerInst3-1) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 185 | +4057/−38 over 39 src files | ✅ 52s |
| [`instFullPreempt`](https://github.com/ajreynol/cvc5/tree/instFullPreempt) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 3 | +11/−1 over 2 src files | ✅ 44s |
| [`ai-emFilter`](https://github.com/ajreynol/cvc5/tree/ai-emFilter) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 13 | +758/−15 over 20 src files | ✅ 75s |
| [`imTrivial`](https://github.com/ajreynol/cvc5/tree/imTrivial) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 12 | +268/−21 over 14 src files | ✅ 37s |
| [`imSimpleInc2`](https://github.com/ajreynol/cvc5/tree/imSimpleInc2) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 10 | +122/−23 over 4 src files | ✅ 18s |
| [`ai-imgDirect`](https://github.com/ajreynol/cvc5/tree/ai-imgDirect) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 6 | +705/−4 over 5 src files | ✅ 55s |
| [`ai-quantOpt-1`](https://github.com/ajreynol/cvc5/tree/ai-quantOpt-1) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | +36/−4 over 2 src files | ✅ 5s |
| [`ai-prepared13`](https://github.com/ajreynol/cvc5/tree/ai-prepared13) | [R3](directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 13 | +291/−6 over 4 src files | ✅ 6s |
| [`termOrigin`](https://github.com/ajreynol/cvc5/tree/termOrigin) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 17 | +474/−11 over 19 src files | ✅ 50s |
| [`instLastCallDelay`](https://github.com/ajreynol/cvc5/tree/instLastCallDelay) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 3 | +2/−2 over 1 src files | ✅ 39s |
| [`dtInstMode`](https://github.com/ajreynol/cvc5/tree/dtInstMode) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | +14/−1 over 2 src files | ✅ 48s |
| [`multiTriggerSingleBase`](https://github.com/ajreynol/cvc5/tree/multiTriggerSingleBase) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 3 | +43/−0 over 3 src files | ✅ 43s |
| [`nestedTriggers`](https://github.com/ajreynol/cvc5/tree/nestedTriggers) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | +40/−22 over 4 src files | ✅ 16s |
| [`simpleTriggerMore`](https://github.com/ajreynol/cvc5/tree/simpleTriggerMore) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 5 | +48/−33 over 2 src files | ✅ 39s |
| [`gttOpt`](https://github.com/ajreynol/cvc5/tree/gttOpt) | [R5](directions.md#r5--trigger-selection-strict-user-patterns-multi-triggers-and-what-strictness-disables) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | +9/−1 over 2 src files | ✅ 45s |
| [`ai-cbqi-0423`](https://github.com/ajreynol/cvc5/tree/ai-cbqi-0423) | [R6](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 6 | +136/−87 over 1 src files | ✅ 8s |
| [`ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) | [R7](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 5 | +165/−43 over 8 src files | ✅ 42s |
| [`fmfIeval`](https://github.com/ajreynol/cvc5/tree/fmfIeval) | [R7](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | **empty — dropped +40/−22** | ✅ 54s |
| [`notifySatClause`](https://github.com/ajreynol/cvc5/tree/notifySatClause) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 6 | +49/−10 over 6 src files | ✅ 10s |
| [`ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) | [R10](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | +116/−32 over 11 src files | ✅ 52s |
| [`ai-jhRlvInst`](https://github.com/ajreynol/cvc5/tree/ai-jhRlvInst) | [R10](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 5 | +326/−18 over 9 src files | ✅ 17s |
| [`ai-jhConflictFirst`](https://github.com/ajreynol/cvc5/tree/ai-jhConflictFirst) | [R10](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | +93/−33 over 9 src files | ✅ 49s |
| [`claudeDev-dts-idef`](https://github.com/ajreynol/cvc5/tree/claudeDev-dts-idef) | [R10](directions.md#r10--where-instance-lemmas-sit-in-the-decision-order-local-deferred-gated) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 5 | +179/−37 over 13 src files | ✅ 51s |
| [`jhRandom`](https://github.com/ajreynol/cvc5/tree/jhRandom) | [R11](directions.md#r11--decision-heuristic-versus-relevancy-what-the-sat-solver-is-made-to-decide-on) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 5 | +262/−20 over 7 src files | ✅ 16s |
| [`subConflict`](https://github.com/ajreynol/cvc5/tree/subConflict) | [R12](directions.md#r12--lemma-inprocessing-and-conflict-minimisation) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 11 | +333/−1 over 12 src files | ✅ 49s |
| [`cadicalPortfolio`](https://github.com/ajreynol/cvc5/tree/cadicalPortfolio) | [R13](directions.md#r13--the-sat-backend-cadical-minisat-restarts-units) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | +50/−0 over 1 src files | ✅ 4s |
| [`mbtc25`](https://github.com/ajreynol/cvc5/tree/mbtc25) | [R14](directions.md#r14--theory-combination-care-graph-or-model-based) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 31 | +365/−82 over 15 src files | ✅ 42s |
| [`ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare) | [R15](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | +9/−3 over 1 src files | ✅ 19s |
| [`dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3) | [R15](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 33 | +378/−72 over 10 src files | ✅ 20s |
| [`cdno`](https://github.com/ajreynol/cvc5/tree/cdno) | [R15](directions.md#r15--equality-engine-architecture-central-distributed-and-who-gets-told-what) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 18 | +168/−12 over 5 src files | ✅ 46s |
| [`dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | +61/−8 over 2 src files | ✅ 20s |
| [`dtLazyInst3`](https://github.com/ajreynol/cvc5/tree/dtLazyInst3) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 21 | +80/−2 over 3 src files | ✅ 17s |
| [`oneConsInst`](https://github.com/ajreynol/cvc5/tree/oneConsInst) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 5 | +42/−11 over 2 src files | ✅ 10s |
| [`ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc) | [R17](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 5 | +95/−2 over 6 src files | ✅ 20s |
| [`deferBlock`](https://github.com/ajreynol/cvc5/tree/deferBlock) | [R17](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 21 | +330/−16 over 15 src files | ✅ 53s |
| [`bitblastLc`](https://github.com/ajreynol/cvc5/tree/bitblastLc) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 3 | +28/−1 over 2 src files | ✅ 15s |
| [`bvToIntQuant-031126`](https://github.com/ajreynol/cvc5/tree/bvToIntQuant-031126) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | **empty — dropped +60/−16** | ✅ 15s |
| [`ufConvRlv`](https://github.com/ajreynol/cvc5/tree/ufConvRlv) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | +12/−4 over 3 src files | ✅ 16s |
| [`ufEagerDistinct`](https://github.com/ajreynol/cvc5/tree/ufEagerDistinct) | [R20](directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 3 | +25/−0 over 3 src files | ✅ 17s |
| [`simplifyRecFun`](https://github.com/ajreynol/cvc5/tree/simplifyRecFun) | [R20](directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 60 | +101/−39 over 11 src files | ✅ 44s |
| [`quantRew-1006`](https://github.com/ajreynol/cvc5/tree/quantRew-1006) | [R21](directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | +27/−4 over 1 src files | ✅ 22s |
| [`preregRlv`](https://github.com/ajreynol/cvc5/tree/preregRlv) | [R22](directions.md#r22--preregistration-which-literals-the-theories-are-told-about) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 157 | +833/−13 over 9 src files | ✅ 42s |
| [`tdbOldIndex`](https://github.com/ajreynol/cvc5/tree/tdbOldIndex) | [R23](directions.md#r23--term-database-relevance-which-ground-terms-e-matching-may-use) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 7 | +61/−7 over 5 src files | ✅ 49s |
| [`lowLevelOptMore`](https://github.com/ajreynol/cvc5/tree/lowLevelOptMore) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 13 | +72/−8 over 2 src files | ✅ 16s |
| [`tdbLLOpts`](https://github.com/ajreynol/cvc5/tree/tdbLLOpts) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | +34/−34 over 2 src files | ✅ 48s |
| [`qdebugStats`](https://github.com/ajreynol/cvc5/tree/qdebugStats) | [R26](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 32 | +534/−15 over 19 src files | ✅ 23s |
| [`debugDumpLemmas`](https://github.com/ajreynol/cvc5/tree/debugDumpLemmas) | [R26](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 7 | +49/−0 over 5 src files | ✅ 51s |
| [`trackInferId`](https://github.com/ajreynol/cvc5/tree/trackInferId) | [R26](directions.md#r26--attribution-instrumentation-the-tools-goal-2-needs) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 3 | +22/−3 over 3 src files | ✅ 17s |
| [`ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt) | [R27](directions.md#r27--smt-lib-parser-throughput-pay-less-before-solving) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 4 | +228/−141 over 7 src files | ✅ 18s |
| [`eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi) | [R28](directions.md#r28--eager-conflict-based-instantiation-find-a-useful-instance-before-full-effort) | [`47f43bd`](https://github.com/cvc5/cvc5/commit/47f43bd012a227fb91743b8362170d4444dd270e) | 206 | +5248/−202 over 58 src files | ✅ 75s |

## Older than the pin — 13 branches

**This is the work order for the next pass.** Nearest first; the last column is
commits behind the pin. Nothing here can be built, measured or reviewed as it
stands, and none is compile-checked.

| branch | direction | newest cvc5 commit it carries | its commits | behind `10bd5cb` |
| --- | --- | --- | ---: | ---: |
| [`emExp`](https://github.com/ajreynol/cvc5/tree/emExp) | [R2](directions.md#r2--incremental-e-matching-match-what-changed-not-everything) | [`310f487`](https://github.com/cvc5/cvc5/commit/310f487e6a829fb1bdfbef2849536176b047606e) (2025-11-11) | 6 | **522** |
| [`dtElim`](https://github.com/ajreynol/cvc5/tree/dtElim) | [R16](directions.md#r16--datatypes-when-to-split-on-what-and-whether-to-have-them-at-all) | [`aeb5547`](https://github.com/cvc5/cvc5/commit/aeb554775be7eb9eb59f640fa76ee90879e19746) (2025-10-29) | 26 | **537** |
| [`eagerQM`](https://github.com/ajreynol/cvc5/tree/eagerQM) | [R1](directions.md#r1--eager-instantiation-instantiate-during-search-not-only-at-full-effort) | [`aca9908`](https://github.com/cvc5/cvc5/commit/aca99089d0de4fa9292227af36f25c5499024a3c) (2025-08-28) | 3 | **623** |
| [`eagerElimDefs`](https://github.com/ajreynol/cvc5/tree/eagerElimDefs) | [R20](directions.md#r20--preprocessing-distinct-non-clausal-simplification-ite) | [`9e7ee41`](https://github.com/cvc5/cvc5/commit/9e7ee41e7c50a972afd6f7210ecf94d798beb235) (2024-10-04) | 9 | **1292** |
| [`emStratify`](https://github.com/ajreynol/cvc5/tree/emStratify) | [R7](directions.md#r7--entailment-filtering-of-instances-what-ieval-buys-and-costs) | [`78e58a5`](https://github.com/cvc5/cvc5/commit/78e58a5ca5504d1794ba961179cae4c0f5405850) (2023-11-01) | 17 | **2211** |
| [`p657`](https://github.com/ajreynol/cvc5/tree/p657) | [R21](directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | [`43c1d0f`](https://github.com/cvc5/cvc5/commit/43c1d0f6815c58f30b6c0b405080da169f56fc04) (2023-08-23) | 4 | **2359** |
| [`isActiveLemma`](https://github.com/ajreynol/cvc5/tree/isActiveLemma) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`51aa806`](https://github.com/cvc5/cvc5/commit/51aa8060989af2d8a626adcc18efb088bcbd1438) (2023-08-18) | 50 | **2374** |
| [`smtLazyAssert`](https://github.com/ajreynol/cvc5/tree/smtLazyAssert) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`1c41fda`](https://github.com/cvc5/cvc5/commit/1c41fdaef2639ab81737bca2bda33d385157bda7) (2022-08-03) | 21 | **3045** |
| [`emFailMasks`](https://github.com/ajreynol/cvc5/tree/emFailMasks) | [R3](directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | [`2e555b3`](https://github.com/cvc5/cvc5/commit/2e555b3cac196cb141a3a4dbf934f282bfbdd723) (2022-04-20) | 27 | **3325** |
| [`cacheEntCheck`](https://github.com/ajreynol/cvc5/tree/cacheEntCheck) | [R3](directions.md#r3--worst-case-e-matching-failure-caching-and-early-pruning) | [`b446953`](https://github.com/cvc5/cvc5/commit/b4469530d2f6de599ddf7207a1914b88be49de5b) (2021-10-15) | 5 | **4439** |
| [`virtualClauseDel`](https://github.com/ajreynol/cvc5/tree/virtualClauseDel) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | [`55ce505`](https://github.com/cvc5/cvc5/commit/55ce505ca757dc241bf4c1e10023bc43ac531a23) (2021-10-13) | 15 | **4450** |
| [`carryInst`](https://github.com/ajreynol/cvc5/tree/carryInst) | [R4](directions.md#r4--instantiation-budgeting-how-many-instances-per-round-and-which) | [`54490c6`](https://github.com/cvc5/cvc5/commit/54490c6053d51910f5f7c2160451ad4d36fe6946) (2021-07-28) | 3 | **4811** |
| [`bvBbExtf`](https://github.com/ajreynol/cvc5/tree/bvBbExtf) | [R19](directions.md#r19--bit-vectors-inside-quantified-problems) | [`be7662b`](https://github.com/cvc5/cvc5/commit/be7662bdcd3881d349bfba4c959a0c2be4159ce9) (2016-12-08) | 5 | **9377** |

## Retired — 7 branches

Not work for the next pass: these were attempted or assessed and could not be
brought onto a current commit, so their proposal rows are gone from the
register. The verdict is the point — each says what upstream did to the ground
the branch stood on. From the maintainer's update-pass notes, 2026-09-22.

| branch | direction | verdict | why |
| --- | --- | --- | --- |
| [`refactorQcf`](https://github.com/ajreynol/cvc5/tree/refactorQcf) | [R6](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | **REWRITTEN UPSTREAM** | 79 substantive conflict hunks, all inside `quant_conflict_find.{cpp,h}`, which master has rewritten. A merge would be a rewrite of the branch against a different design. |
| [`qcfClean`](https://github.com/ajreynol/cvc5/tree/qcfClean) | [R6](directions.md#r6--conflict-based-instantiation-off-for-this-domain-and-why-that-is-right-or-wrong) | **REWRITTEN UPSTREAM** | 60 substantive conflict hunks in the same two rewritten files. Same verdict as `refactorQcf`. |
| [`virtualLemma`](https://github.com/ajreynol/cvc5/tree/virtualLemma) | [R9](directions.md#r9--deleting-instantiation-lemmas-garbage-collection-or-scoping-them-to-the-branch) | **TARGETS DELETED CODE** | 40 substantive hunks across 13 files, two of which master has deleted: `decision_engine_old.cpp` and `decision_engine_old.h`. The decision-engine surface the branch attaches to no longer exists. |
| [`linearSolverSub`](https://github.com/ajreynol/cvc5/tree/linearSolverSub) | [R17](directions.md#r17--linear-integer-arithmetic-branch-and-bound-cuts-and-the-diophantine-solver) | **NEEDS REIMPLEMENTATION** | Dropped by the author, and independently a signature migration rather than a merge: master changed `LinearSolver`'s interface — `propagate()` lost its `Effort` argument, `ppAssert` returns `bool`, `ppStaticLearn` takes `std::vector<TrustNode>` — while the branch adds a 376-line implementation of the old signatures. Porting means migrating the base, `LinearSolverLegacy`, `LinearSolverSub` and the call sites together. |
| [`ai-fixAlphaEq-2`](https://github.com/ajreynol/cvc5/tree/ai-fixAlphaEq-2) | [R21](directions.md#r21--quantifier-preprocessing-what-is-done-to-a-quantifier-before-it-is-ever-matched) | **AUTHOR-DROPPED** | Dropped on the author's instruction; not assessed further. The branch is left untouched on the fork. |
| [`optTdbTNode`](https://github.com/ajreynol/cvc5/tree/optTdbTNode) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | **SUPERSEDED** | Its entire content is `Node` → `TNode` on `TermDb::d_op_map` and `d_type_map` to avoid reference counting. Master replaced both with context-dependent `CDHashMap<Node, std::shared_ptr<DbList>>`, so all 25 hunks target structures that no longer exist, and master's own `DbList` rewrite supersedes the optimisation. |
| [`perfDataStructures`](https://github.com/ajreynol/cvc5/tree/perfDataStructures) | [R25](directions.md#r25--low-level-engineering-the-constant-factors) | **CANNOT BUILD** | A 2018 benchmarking scaffold. Merging silently resurrected two files master had deleted — `smt_engine.cpp` (6105 lines, renamed `solver_engine.cpp`) and the autotools `src/Makefile.am` — a clean-looking merge that was in fact broken. Its `--do-test` hook lands in `SmtEnginePrivate::processAssertions`, which no longer exists, and its sources use `cvc4_private.h`, `namespace CVC4` and `__CVC4__` guards, so they cannot compile against `cvc5::internal`. |

`perfDataStructures` is the one to remember: its merge looked clean while
silently resurrecting two files master had deleted. That is the same failure as
the two emptied branches above, caught from the other side.


**The far end is design evidence, not a queue.** The oldest commits carried here
predate current cvc5 by years; `bvBbExtf` holds one from 2016. The register
keeps those rows because the idea is a candidate, not because the patch is one,
and below roughly a thousand commits an update is more likely to drop the
mechanism than to preserve it — which is no longer hypothetical. A report that
such a branch should be reimplemented rather than updated is the useful outcome.
