# 2026-09-24 — the branch sweep

**Goal 3, the branch half of the register.** Every branch proposal run as the
reference plus its own option string. **Complete**: all **70 arms** ran, one
run each, and every branch row in the register now carries a number. The sweep
finished 2026-09-25T00:41:12Z.

## 1. What was asked

Give the branch rows a number. Each arm is one branch's binary run with the
fixed reference prefix and the arm's own options, so the difference from the
reference is that branch's doing.

## 2. What was run

A separate clone and build directory, used only for these arms, so that a branch
build cannot disturb the launcher's. Per arm: check out the branch tip, build,
**verify the binary's own `--show-config` hash against that tip**, solve a
trivial input as a smoke test, then run the set. A build or smoke failure skips
the branch rather than measuring the wrong solver.

```
-q --no-cbqi --user-pat=strict --sat-solver=cadical  <the arm's options>
```

**The reference for these arms is the one built in the same directory**: 5576
solved, PAR2 39304.4, at cvc5 `d7d5b948c11d2d83be0212d4a954ef49740ecdab`. It is
**not** the 5550 reference the option sweep used; the two builds differ by 26
solves ([entry](2026-09-24-build-directory-difference.md)), so an arm here must
not be compared with an option row.

**Every branch tip is exactly 1 commit behind the fork's `master`**, recorded
per row below, while the reference is at upstream `d7d5b948c1`. An arm
therefore differs from the reference by its own changes *and* by that drift.
This was accepted deliberately to get first data; `submit` would have refused
these arms as BEHIND.

## 3. The set

`quant-07-25`, 6124 benchmarks, 30 s, one arm at a time on the idle host.

## 4. What came back

Reference: **5576** solved, 5 unknown, 543 timeout, PAR2 **39304.4**.
**gained** is benchmarks the arm solves that the reference does not; **lost** is
the reverse.

| branch | direction | tip | behind | run as | gained | lost | net | unknown | PAR2 |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| [`ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) | R10 | `fed62ecb77` | 1 | `--inst-defer` | **+47** | **−33** | **+14** | 6 | 38233.4 |
| [`claudeDev-dts-idef`](https://github.com/ajreynol/cvc5/tree/claudeDev-dts-idef) | R10 | `e6866442b2` | 1 | `--inst-defer --dt-split-relevant` | **+44** | **−31** | **+13** | 5 | 38398.1 |
| [`ai-jhRlvInst`](https://github.com/ajreynol/cvc5/tree/ai-jhRlvInst) | R10 | `936b1636ad` | 1 | `--jh-rlv-inst` | **+27** | **−17** | **+10** | 7 | 38660.6 |
| [`simpleTriggerMore`](https://github.com/ajreynol/cvc5/tree/simpleTriggerMore) | R5 | `77c5a5a771` | 1 | *none* | **+15** | **−7** | **+8** | 5 | 38909.1 |
| [`ai-quantOpt-1`](https://github.com/ajreynol/cvc5/tree/ai-quantOpt-1) | R2 | `1c57427e95` | 1 | *none* | **+11** | **−7** | **+4** | 5 | 39145.5 |
| [`eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi) | R28 | `23646a0db8` | 1 | `--eager-inst --eager-inst-mode=prop` | **+7** | **−3** | **+4** | 5 | 39205.5 |
| [`eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi) | R28 | `23646a0db8` | 1 | `--eager-inst --eager-inst-trigger=narrow` | **+7** | **−3** | **+4** | 5 | 39228.8 |
| [`eagerElimDefs`](https://github.com/ajreynol/cvc5/tree/eagerElimDefs) | R20 | `b1406de017` | 1 | `--eager-elim-defs` | **+5** | **−1** | **+4** | 5 | 39190.0 |
| [`emExp`](https://github.com/ajreynol/cvc5/tree/emExp) | R2 | `b8602289be` | 1 | *none* | **+10** | **−6** | **+4** | 6 | 39070.6 |
| [`ai-cbqi-0423`](https://github.com/ajreynol/cvc5/tree/ai-cbqi-0423) | R6 | `01fa9c6bb0` | 1 | *none* | **+6** | **−3** | **+3** | 5 | 39215.1 |
| [`eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi) | R28 | `23646a0db8` | 1 | `--eager-inst` | **+9** | **−6** | **+3** | 5 | 39254.0 |
| [`virtualClauseDel`](https://github.com/ajreynol/cvc5/tree/virtualClauseDel) | R9 | `56a2af3c66` | 1 | *none* | **+7** | **−4** | **+3** | 5 | 39242.1 |
| [`dtSplitRelevant`](https://github.com/ajreynol/cvc5/tree/dtSplitRelevant) | R16 | `25c1f909a2` | 1 | `--dt-split-relevant` | **+9** | **−7** | **+2** | 5 | 39308.5 |
| [`ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie) | R7 | `6f2ccdc3d8` | 1 | *none* | **+6** | **−4** | **+2** | 5 | 39266.0 |
| [`tdbLLOpts`](https://github.com/ajreynol/cvc5/tree/tdbLLOpts) | R25 | `0bfa3bdcfb` | 1 | *none* | **+5** | **−3** | **+2** | 5 | 39256.2 |
| [`ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare) | R15 | `02d502285b` | 1 | *none* | **+8** | **−7** | **+1** | 5 | 39316.8 |
| [`cdno`](https://github.com/ajreynol/cvc5/tree/cdno) | R15 | `028e2fc6d1` | 1 | *none* | **+5** | **−4** | **+1** | 5 | 39299.1 |
| [`lowLevelOptMore`](https://github.com/ajreynol/cvc5/tree/lowLevelOptMore) | R25 | `99a6b776f7` | 1 | *none* | **+6** | **−5** | **+1** | 5 | 39259.0 |
| [`quantRew-1006`](https://github.com/ajreynol/cvc5/tree/quantRew-1006) | R21 | `498d64205b` | 1 | *none* | **+6** | **−5** | **+1** | 5 | 39302.5 |
| [`ufConvRlv`](https://github.com/ajreynol/cvc5/tree/ufConvRlv) | R19 | `68333f2aa6` | 1 | *none* | **+5** | **−4** | **+1** | 5 | 39284.8 |
| [`ai-parserOpt`](https://github.com/ajreynol/cvc5/tree/ai-parserOpt) | R27 | `0abe040be0` | 1 | *none* | **+6** | **−6** | **+0** | 5 | 39324.9 |
| [`deferBlock`](https://github.com/ajreynol/cvc5/tree/deferBlock) | R17 | `17c1b55999` | 1 | `--defer-block` | **+5** | **−5** | **+0** | 5 | 39364.4 |
| [`deferBlock`](https://github.com/ajreynol/cvc5/tree/deferBlock) | R17 | `17c1b55999` | 1 | `--defer-block --defer-block-mode=delay` | **+5** | **−5** | **+0** | 5 | 39351.0 |
| [`multiTriggerSingleBase`](https://github.com/ajreynol/cvc5/tree/multiTriggerSingleBase) | R5 | `45658ba812` | 1 | *none* | **+5** | **−5** | **+0** | 5 | 39355.6 |
| [`notifySatClause`](https://github.com/ajreynol/cvc5/tree/notifySatClause) | R9 | `f724885a58` | 1 | *none* | **+3** | **−3** | **+0** | 5 | 39345.8 |
| [`gttOpt`](https://github.com/ajreynol/cvc5/tree/gttOpt) | R5 | `4ecf86b531` | 1 | `--gt-trigger-reg` | **+3** | **−4** | **−1** | 6 | 39349.8 |
| [`nestedTriggers`](https://github.com/ajreynol/cvc5/tree/nestedTriggers) | R5 | `4bbf5bcb61` | 1 | *none* | **+3** | **−4** | **−1** | 5 | 39347.5 |
| [`simplifyRecFun`](https://github.com/ajreynol/cvc5/tree/simplifyRecFun) | R20 | `4d12cdbb83` | 1 | `--simplify-rec-fun` | **+4** | **−5** | **−1** | 5 | 39358.4 |
| [`subConflict`](https://github.com/ajreynol/cvc5/tree/subConflict) | R12 | `b9a239091d` | 1 | `--sub-conflict-find` | **+7** | **−8** | **−1** | 5 | 39412.8 |
| [`termOrigin`](https://github.com/ajreynol/cvc5/tree/termOrigin) | R4 | `12384f8076` | 1 | `--inst-nested-max-level=1` | **+5** | **−6** | **−1** | 5 | 39362.6 |
| [`termOrigin`](https://github.com/ajreynol/cvc5/tree/termOrigin) | R4 | `12384f8076` | 1 | `--inst-nested-max-level=3` | **+4** | **−5** | **−1** | 5 | 39341.4 |
| [`emStratify`](https://github.com/ajreynol/cvc5/tree/emStratify) | R7 | `e9d7d833aa` | 1 | `--term-db-cd` | **+4** | **−6** | **−2** | 5 | 39433.5 |
| [`mbtc25`](https://github.com/ajreynol/cvc5/tree/mbtc25) | R14 | `6ee576dcf0` | 1 | `--tc-mode=model-based` | **+16** | **−18** | **−2** | 4 | 39327.4 |
| [`cadicalPortfolio`](https://github.com/ajreynol/cvc5/tree/cadicalPortfolio) | R13 | `028940df2c` | 1 | *none* | **+4** | **−7** | **−3** | 5 | 39416.7 |
| [`smtLazyAssert`](https://github.com/ajreynol/cvc5/tree/smtLazyAssert) | R9 | `b4e2128df8` | 1 | `--smt-lazy-assert` | **+2** | **−5** | **−3** | 0 | 39376.1 |
| [`tdbOldIndex`](https://github.com/ajreynol/cvc5/tree/tdbOldIndex) | R23 | `f116b96df5` | 1 | `--tdb-old-index` | **+12** | **−15** | **−3** | 9 | 39304.3 |
| [`eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi) | R28 | `23646a0db8` | 1 | `--eager-inst --eager-inst-mode=conflict` | **+4** | **−8** | **−4** | 5 | 39475.7 |
| [`imTrivial`](https://github.com/ajreynol/cvc5/tree/imTrivial) | R2 | `608f2bfbd5` | 1 | *none* | **+14** | **−20** | **−6** | 7 | 39383.7 |
| [`imSimpleInc2`](https://github.com/ajreynol/cvc5/tree/imSimpleInc2) | R2 | `40af836430` | 1 | *none* | **+10** | **−17** | **−7** | 6 | 39664.7 |
| [`instLastCallDelay`](https://github.com/ajreynol/cvc5/tree/instLastCallDelay) | R4 | `2f65f0ae53` | 1 | *none* | **+6** | **−13** | **−7** | 5 | 39564.8 |
| [`eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi) | R28 | `23646a0db8` | 1 | `--eager-inst --eager-inst-when=asserted` | **+2** | **−15** | **−13** | 5 | 39877.1 |
| [`ufEagerDistinct`](https://github.com/ajreynol/cvc5/tree/ufEagerDistinct) | R20 | `e8b83b71bf` | 1 | `--uf-eager-distinct` | **+4** | **−17** | **−13** | 5 | 42167.2 |
| [`ai-emFilter`](https://github.com/ajreynol/cvc5/tree/ai-emFilter) | R2 | `dfe6d9aa16` | 1 | `--filter-e-matching` | **+11** | **−27** | **−16** | 5 | 40627.0 |
| [`dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3) | R15 | `7c2c6a1e58` | 1 | *none* | **+3** | **−19** | **−16** | 5 | 39998.6 |
| [`oneConsInst`](https://github.com/ajreynol/cvc5/tree/oneConsInst) | R16 | `8293e0830f` | 1 | *none* | **+15** | **−31** | **−16** | 5 | 40049.6 |
| [`ai-jhConflictFirst`](https://github.com/ajreynol/cvc5/tree/ai-jhConflictFirst) | R10 | `9c036e7c2d` | 1 | `--jh-conflict-first` | **+19** | **−37** | **−18** | 5 | 40165.1 |
| [`ai-imgDirect`](https://github.com/ajreynol/cvc5/tree/ai-imgDirect) | R2 | `9b06b84edc` | 1 | *none* | **+7** | **−27** | **−20** | 5 | 40510.4 |
| [`bitblastLc`](https://github.com/ajreynol/cvc5/tree/bitblastLc) | R19 | `4dc8781a0f` | 1 | `--bitblast-lc` | **+5** | **−26** | **−21** | 26 | 40591.1 |
| [`preregRlv`](https://github.com/ajreynol/cvc5/tree/preregRlv) | R22 | `b909d21426` | 1 | `--preregister-mode=rlv` | **+26** | **−54** | **−28** | 51 | 41030.8 |
| [`ai-prepared13`](https://github.com/ajreynol/cvc5/tree/ai-prepared13) | R3 | `ed9960de8f` | 1 | *none* | **+1** | **−31** | **−30** | 5 | 41104.1 |
| [`dtLazyInst3`](https://github.com/ajreynol/cvc5/tree/dtLazyInst3) | R16 | `9dac983f1f` | 1 | `--dt-lazy-inst` | **+27** | **−75** | **−48** | 34 | 41659.7 |
| [`ai-dioLc`](https://github.com/ajreynol/cvc5/tree/ai-dioLc) | R17 | `55949c052a` | 1 | `--dio-solver-last-call` | **+5** | **−93** | **−88** | 5 | 44097.9 |
| [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | R1 | `6b04950de9` | 1 | `--eager-inst --eager-inst-macro-only` | **+22** | **−116** | **−94** | 4 | 44685.7 |
| [`emStratify`](https://github.com/ajreynol/cvc5/tree/emStratify) | R7 | `e9d7d833aa` | 1 | `--e-matching-stratify-ieval` | **+6** | **−109** | **−103** | 7 | 46792.7 |
| [`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | R1 | `a5666dcf14` | 1 | `--eager-inst --eager-inst-gen-limit=2` | **+18** | **−131** | **−113** | 22 | 44219.7 |
| [`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | R1 | `a5666dcf14` | 1 | `--eager-inst --eager-inst-rlv` | **+13** | **−130** | **−117** | 31 | 45760.8 |
| [`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | R1 | `a5666dcf14` | 1 | `--eager-inst` | **+28** | **−147** | **−119** | 38 | 45052.1 |
| [`jhRandom`](https://github.com/ajreynol/cvc5/tree/jhRandom) | R11 | `7cf2323029` | 1 | `--jh-rand` | **+25** | **−150** | **−125** | 3 | 45771.5 |
| [`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | R1 | `a5666dcf14` | 1 | `--eager-inst --eager-inst-pair-limit=500` | **+17** | **−149** | **−132** | 37 | 45764.8 |
| [`dtInstMode`](https://github.com/ajreynol/cvc5/tree/dtInstMode) | R4 | `4c50eb3383` | 1 | `--no-dt-inst-internal` | **+23** | **−253** | **−230** | 265 | 52190.2 |
| [`instFullPreempt`](https://github.com/ajreynol/cvc5/tree/instFullPreempt) | R1 | `47fc2e5c45` | 1 | `--inst-when=full-preempt` | **+12** | **−388** | **−376** | 3 | 61416.3 |
| [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | R1 | `6b04950de9` | 1 | `--eager-inst --eager-inst-term=assert` | **+18** | **−564** | **−546** | 71 | 69255.0 |
| [`ai-extEagerInst3-1`](https://github.com/ajreynol/cvc5/tree/ai-extEagerInst3-1) | R1 | `b071a271d6` | 1 | `--eager-inst --eager-inst-term=assert` | **+16** | **−564** | **−548** | 66 | 69512.1 |
| [`ai-extEagerInst3-1`](https://github.com/ajreynol/cvc5/tree/ai-extEagerInst3-1) | R1 | `b071a271d6` | 1 | `--eager-inst` | **+18** | **−897** | **−879** | 72 | 88818.4 |
| [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | R1 | `6b04950de9` | 1 | `--eager-inst` | **+18** | **−913** | **−895** | 77 | 89719.4 |
| [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | R1 | `6b04950de9` | 1 | `--eager-inst --eager-inst-term=eqc-merge` | **+15** | **−926** | **−911** | 173 | 90957.9 |
| [`dtElim`](https://github.com/ajreynol/cvc5/tree/dtElim) | R16 | `ff1ff9d4e8` | 1 | `--dt-elim` | **+9** | **−954** | **−945** | 917 | 93373.8 |
| [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | R1 | `6b04950de9` | 1 | `--eager-inst --eager-inst-quant=preregister` | **+27** | **−1069** | **−1042** | 65 | 98177.5 |
| [`subConflict`](https://github.com/ajreynol/cvc5/tree/subConflict) | R12 | `b9a239091d` | 1 | `--sub-conflict-find --no-sub-conflict-last-call` | **+2** | **−1423** | **−1421** | 1 | 144328.0 |
| [`eagerQM`](https://github.com/ajreynol/cvc5/tree/eagerQM) | R1 | `f3a2f4ce3d` | 1 | `--eager-q-matching` | **+0** | **−2539** | **−2539** | 1671 | 187740.2 |

## 5. What it settled

**No branch arm reaches green.** Green here is a net of +20 solves, and the best
arm is +14. Of 70 arms, **20 have a positive net** and three reach +10. That is
the headline: the fork's branch inventory, measured one arm at a time against a
reference built beside it, contains no single change that decides 20 more
benchmarks on this set.

**R10 holds all three of the best arms, and they are the same idea.**

| branch | run as | gained | lost | net | PAR2 |
| --- | --- | ---: | ---: | ---: | ---: |
| [`ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer) | `--inst-defer` | **+47** | −33 | **+14** | **38233.4** |
| [`claudeDev-dts-idef`](https://github.com/ajreynol/cvc5/tree/claudeDev-dts-idef) | `--inst-defer --dt-split-relevant` | **+44** | −31 | **+13** | **38398.1** |
| [`ai-jhRlvInst`](https://github.com/ajreynol/cvc5/tree/ai-jhRlvInst) | `--jh-rlv-inst` | **+27** | −17 | **+10** | **38660.6** |

All three are R10 — where instance lemmas sit in the decision order — and all
three **beat the reference's PAR2 of 39304.4** by roughly 1000 — as do 19 arms
in all. That is the
stronger signal. A net of +14 is under three noise bands; a PAR2 drop of 1000
with 47 rescued benchmarks is a change doing real work on the set rather than
drifting inside it. `--inst-defer` rescues more than any other arm measured.

**The question these three pose is concrete.** Are the 33 benchmarks
`--inst-defer` loses the same ones the other two R10 arms lose? If they are, one
mechanism is mispaced and can be gated; if they are not, the three compose and
the direction is worth more than any of its arms. That intersection is one
command on the saved gap sets and is the obvious next step.

**Five arms rescue 25 or more while netting negative**, and they are not the
same mechanism as each other: `claude-eagerInst --eager-inst` +28/−147,
`dtLazyInst3 --dt-lazy-inst` +27/−75, `eagerInst3
--eager-inst-quant=preregister` +27/−1069, `preregRlv --preregister-mode=rlv`
+26/−54, `jhRandom --jh-rand` +25/−150. Each finds two dozen benchmarks the
reference cannot, then loses more elsewhere. These are the rows the gained/lost
split exists for; a net-only table would have discarded all of them, and
`preregRlv` and `dtLazyInst3` in particular lose little enough to be worth
gating rather than dropping.

**`simpleTriggerMore` (R5) is real but small.** +15/−7, net +8, fourth overall.
A `reset(Node eqc)` override on `InstMatchGeneratorSimple` caching the term-arg
trie so a simple trigger can be driven by a candidate equivalence class.

**Pacing is visible within R1.** `claude-eagerInst` loses about 120 on every
variant while the older `eagerInst3` and `ai-extEagerInst3-1` lose 500–900. The
budgets that branch added do what they were written to do, even though the
result is still a net loss.

**Four arms lose more than 900, and two of them indict the option rather than
the branch.** `eagerQM --eager-q-matching` loses **2539** with 1671 unknown,
meaning incompleteness rather than slowness; `subConflict --sub-conflict-find
--no-sub-conflict-last-call` loses **1423** where the same branch with the
last-call check left on loses 8; `eagerInst3
--eager-inst-quant=preregister` loses **1069** while its `--eager-inst-macro-only`
variant loses 116; `dtElim --dt-elim` loses **954**. In the two middle cases the
branch is not the problem, the option string is.

**`eagerCbqi` is now measured.** Its five arms were the largest block of skipped
work in the first attempt and are small: +4 to −13, nothing outside noise except
`--eager-inst-when=asserted` at −13.

## 6. What this does not settle

**One run per arm, no repetition.** The three R10 leaders sit 2–3 noise bands
above zero on a single run each. They are candidates, not results, and repeating
those three is worth more than any new arm.

**These arms are not comparable with the option rows.** Wave 1 measured options
against a 5550-solve build; these arms are against a 5576-solve build of the
same commit, and the two differ by 26 solves
([entry](2026-09-24-build-directory-difference.md)). A reader must not rank
`--ee-mode=central` (+86, Wave 1) against `ai-instDefer` (+47, here).

**Each arm carries one commit of drift** as well as its own changes.

**Two builds of GMP broke mid-sweep** and the smoke test caught both. The first
attempt lost 38 arms to it before the cause was found: this GMP is a fat
(CPU-dispatching) build, a partial rebuild relinks stale non-fat objects against
fat-mode ones, and `libgmp.so` ends up with five undefined `__gmpn_*` symbols.
No measured arm is affected — every failure was a refusal to run, not a bad
number.
