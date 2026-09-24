# 2026-09-24 — the branch sweep (in progress)

**Goal 3, the branch half of the register.** Every branch proposal run as the
reference plus its own option string. **This entry is partial**: the sweep is
still running, and the table below carries only the arms finished at the time of
writing. It will be extended, not rewritten, as the rest land.

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

**Each branch carries a commit 1 or 11 behind the fork's `master`**, recorded
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
| [`ai-quantOpt-1`](https://github.com/ajreynol/cvc5/tree/ai-quantOpt-1) | R2 | `1c57427e95` | 1 | *none* | **+11** | **−7** | **+4** | 5 | 39145.5 |
| [`emExp`](https://github.com/ajreynol/cvc5/tree/emExp) | R2 | `b8602289be` | 1 | *none* | **+10** | **−6** | **+4** | 6 | 39070.6 |
| [`imTrivial`](https://github.com/ajreynol/cvc5/tree/imTrivial) | R2 | `608f2bfbd5` | 1 | *none* | **+14** | **−20** | **-6** | 7 | 39383.7 |
| [`imSimpleInc2`](https://github.com/ajreynol/cvc5/tree/imSimpleInc2) | R2 | `40af836430` | 1 | *none* | **+10** | **−17** | **-7** | 6 | 39664.7 |
| [`ai-emFilter`](https://github.com/ajreynol/cvc5/tree/ai-emFilter) | R2 | `dfe6d9aa16` | 1 | `--filter-e-matching` | **+11** | **−27** | **-16** | 5 | 40627.0 |
| [`ai-imgDirect`](https://github.com/ajreynol/cvc5/tree/ai-imgDirect) | R2 | `9b06b84edc` | 1 | *none* | **+7** | **−27** | **-20** | 5 | 40510.4 |
| [`ai-prepared13`](https://github.com/ajreynol/cvc5/tree/ai-prepared13) | R3 | `ed9960de8f` | 1 | *none* | **+1** | **−31** | **-30** | 5 | 41104.1 |
| [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | R1 | `6b04950de9` | 1 | `--eager-inst --eager-inst-macro-only` | **+22** | **−116** | **-94** | 4 | 44685.7 |
| [`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | R1 | `a5666dcf14` | 1 | `--eager-inst --eager-inst-gen-limit=2` | **+18** | **−131** | **-113** | 22 | 44219.7 |
| [`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | R1 | `a5666dcf14` | 1 | `--eager-inst --eager-inst-rlv` | **+13** | **−130** | **-117** | 31 | 45760.8 |
| [`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | R1 | `a5666dcf14` | 1 | `--eager-inst` | **+28** | **−147** | **-119** | 38 | 45052.1 |
| [`claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst) | R1 | `a5666dcf14` | 1 | `--eager-inst --eager-inst-pair-limit=500` | **+17** | **−149** | **-132** | 37 | 45764.8 |
| [`dtInstMode`](https://github.com/ajreynol/cvc5/tree/dtInstMode) | R4 | `4c50eb3383` | 1 | `--no-dt-inst-internal` | **+23** | **−253** | **-230** | 265 | 52190.2 |
| [`instFullPreempt`](https://github.com/ajreynol/cvc5/tree/instFullPreempt) | R1 | `47fc2e5c45` | 1 | `--inst-when=full-preempt` | **+12** | **−388** | **-376** | 3 | 61416.3 |
| [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | R1 | `6b04950de9` | 1 | `--eager-inst --eager-inst-term=eqc-merge` | **+14** | **−525** | **-511** | 59 | 52146.1 |
| [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | R1 | `6b04950de9` | 1 | `--eager-inst --eager-inst-term=assert` | **+18** | **−564** | **-546** | 71 | 69255.0 |
| [`ai-extEagerInst3-1`](https://github.com/ajreynol/cvc5/tree/ai-extEagerInst3-1) | R1 | `b071a271d6` | 1 | `--eager-inst --eager-inst-term=assert` | **+16** | **−564** | **-548** | 66 | 69512.1 |
| [`ai-extEagerInst3-1`](https://github.com/ajreynol/cvc5/tree/ai-extEagerInst3-1) | R1 | `b071a271d6` | 1 | `--eager-inst` | **+18** | **−897** | **-879** | 72 | 88818.4 |
| [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | R1 | `6b04950de9` | 1 | `--eager-inst` | **+18** | **−913** | **-895** | 77 | 89719.4 |
| [`eagerInst3`](https://github.com/ajreynol/cvc5/tree/eagerInst3) | R1 | `6b04950de9` | 1 | `--eager-inst --eager-inst-quant=preregister` | **+27** | **−1069** | **-1042** | 65 | 98177.5 |
| [`eagerQM`](https://github.com/ajreynol/cvc5/tree/eagerQM) | R1 | `f3a2f4ce3d` | 1 | `--eager-q-matching` | **+0** | **−2539** | **-2539** | 1671 | 187740.2 |

## 5. What it settled so far

**Nothing yet helps on net.** The best arms are inside the noise band this
project uses: `ai-quantOpt-1` and `emExp` at +4 each, where ±5 is noise.

**Every arm rescues something.** Even the heaviest losses solve benchmarks the
reference cannot: the eager-instantiation line rescues 13–28 apiece while losing
between 116 and 913. That is the orthogonality the gained/lost split exists to
show, and those rescued sets are the thing worth intersecting before any of
these branches is dismissed.

**Pacing is visible.** Within R1, `claude-eagerInst` loses about 120 on every
variant while the older `eagerInst3` and `ai-extEagerInst3-1` lose 500–900.
The budgets that branch added are doing what they were written to do, even
though the result is still a net loss.

**Scope.** One run per arm, no repetition. Partial: 21 of 70 arms.
