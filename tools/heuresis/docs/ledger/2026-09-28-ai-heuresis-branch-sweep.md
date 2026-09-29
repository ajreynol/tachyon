# 2026-09-28 — the `ai-heuresis-*` branch sweep

**Goal 3, the ten branches added on 2026-09-28.** Every `ai-heuresis-*`
proposal row in the register, run as the reference plus its own option string,
against a reference measured at the branches' own base. **Complete**: 1
reference and 31 arms, one run each, no build, sha or smoke failure. The
sweep ran 2026-09-28T19:22:10Z–23:27:14Z.

## 1. What was asked

Give the 31 new branch rows a number. The branches sit on
[`03e5ee1ebf`](https://github.com/cvc5/cvc5/commit/03e5ee1ebfcaea0994b1f38ef53a1b4aa87a30bd),
14 commits past the register's reference revision `d7d5b948c1`, so the register
asked for the reference to be measured at that base first.

## 2. What was run

The same separate clone and build directory as the
[branch sweep](2026-09-24-branch-sweep.md) and the
[one-reference re-run](2026-09-25-option-sweep-one-reference.md), so the new
reference and the old one differ by revision and not by build directory. It is
a Production build with shared libraries and GCC 10, built with `make -j60`.
Per branch: check out the exact sha, build, verify the binary's
`--show-config` hash against it, and solve a trivial `unsat` input **with that
arm's own options**, then run the set. A failure skips the branch. Arms ran one
at a time on the idle host, 56 benchmarks in parallel, as before.

`03e5ee1ebf` is on upstream cvc5 `main` ("Start post-release for 1.4.1"). Every
branch tip is exactly one commit on it and zero behind it, and every tip matched
the sha inspected in the shared
[branch list](../../../../docs/active-dev-branches.md#carrying-the-pin-or-within-11-commits-of-it).
Builds took 24–66 s each.

```
-q --no-cbqi --user-pat=strict --sat-solver=cadical  <the arm's options>
-q --user-pat=strict --sat-solver=cadical            <the arm's options>   # R6 rows only
```

This sweep did not go through `submit`, so it has no `job_launcher/log.txt`
entry. It was driven by a script on the host, like wave 2. The per-arm command
was `solve_dir_rec_par_cvc5 -t 30 w3-cvc5 cvc5_solve.sh quant-092826-w3-<arm>
<options>`.

## 3. The set

`quant-07-25`, 6124 benchmarks, 30 s, one arm at a time on the idle host.

## 4. What came back

Results are `results-cvc5_solve.sh-quant-092826-w3-<arm>.txt` on the host,
read with the [`gap`](../../reports/gap) parser's `read` and its definitions of
solved, timeout and PAR2. Before use, the same reading reproduced the
2026-09-24 reference exactly: 5576 solved, PAR2 39304.4.

**The reference at `03e5ee1ebf`: 5572 solved**, 5 unknown, 547 timeout, PAR2
**39436.5**. Against the 5576 reference at `d7d5b948c1` in the same directory
it is **+2 / −6**, net −4, PAR2 +0.31%. That is inside the ±5 noise band, so
the 14 commits between the two revisions moved nothing measurable.

**No arm disagrees with the reference on sat versus unsat.** gained and lost
are against the new reference, as in the register.

| branch | direction | tip | options | gained | lost | net | unknown | PAR2 |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| *reference* | — | `03e5ee1ebf` | — | | | | 5 | 39436.5 |
| `ai-heuresis-r1-claude` | R1 | `9b3bf13d54` | `--inst-chain` | +38 | −101 | **−63** | 6 | 42779.2 |
| | | | `--inst-chain --inst-chain-depth=4` | +13 | −259 | **−246** | 8 | 53129.7 |
| | | | `--inst-chain --inst-chain-depth=8` | +12 | −377 | **−365** | 6 | 60087.5 |
| | | | `--inst-chain --inst-chain-depth=4 --inst-chain-limit=100` | +35 | −99 | **−64** | 13 | 43396.6 |
| | | | `--inst-chain --inst-chain-depth=4 --inst-chain-limit=1000` | +15 | −224 | **−209** | 8 | 51107.5 |
| `ai-heuresis-r2-codex` | R2 | `65b7b012f0` | `--term-db-reuse-eqc` | +7 | −1 | +6 | 5 | 39243.7 |
| `ai-heuresis-r6-claude` | R6 | `e60d0b4b76` | `--cbqi --cbqi-round-budget=-1 --no-cbqi-round-share` (control) | +1 | −11 | −10 | 5 | 40197.6 |
| | | | `--cbqi --cbqi-round-budget=0` | +7 | −5 | +2 | 5 | 39417.4 |
| | | | `--cbqi --cbqi-round-budget=2` | +7 | −5 | +2 | 5 | 39431.5 |
| | | | `--cbqi --cbqi-round-share` | +3 | −13 | −10 | 5 | 40177.5 |
| | | | `--cbqi --cbqi-round-budget=0 --cbqi-round-share` | +5 | −2 | +3 | 5 | 39391.8 |
| | | | `--cbqi --cbqi-round-budget=2 --cbqi-round-share` | +6 | −5 | +1 | 5 | 39444.8 |
| `ai-heuresis-r28-codex` | R28 | `7729490e73` | `--eager-inst-literal` | +5 | −7 | −2 | 5 | 39608.6 |
| | | | `--eager-inst-literal --eager-inst-literal-budget=1000` | +9 | −6 | +3 | 5 | 39355.8 |
| | | | `--eager-inst-literal --eager-inst-literal-budget=100000` | +7 | −10 | −3 | 5 | 39590.8 |
| | | | `--eager-inst-literal --eager-inst-literal-budget=0` (control) | +8 | −2 | +6 | 5 | 39284.0 |
| `ai-heuresis-r9-claude` | R9 | `7b2548f123` | `--no-incremental --inst-gc=none` (control) | +6 | −3 | +3 | 5 | 39388.0 |
| | | | `--no-incremental --inst-gc=assert` | +4 | −3 | +1 | 5 | 39448.3 |
| | | | `--no-incremental --inst-gc=body` | +4 | −12 | −8 | 10 | 39852.8 |
| `ai-heuresis-r10-codex` | R10 | `96e7ec1edd` | `--jh-inst-round-robin` | +16 | −26 | −10 | 4 | 39927.5 |
| | | | `--jh-inst-round-robin --jh-rlv-order` | +11 | −21 | −10 | 3 | 39917.6 |
| `ai-heuresis-r11-claude` | R11 | `079613fb8b` | `--rlv-quant=full` | +7 | −79 | **−72** | 6 | 47268.7 |
| | | | `--rlv-quant=strict` | +1 | −1280 | **−1279** | **1487** | 114908.6 |
| `ai-heuresis-r15-claude` | R15 | `5a936dbf58` | `--ee-share-uf-dt` | **+53** | −38 | +15 | **37** | 38407.9 |
| | | | `--ee-share-uf-dt --ieval=off` | **+59** | −32 | **+27** | **34** | **37003.6** |
| `ai-heuresis-r16-claude` | R16 | `8f890911af` | `--dt-split-order=base-first` | +5 | −2 | +3 | 5 | 39377.6 |
| | | | `--dt-split-order=base-last` | +14 | −10 | +4 | 5 | 39389.5 |
| | | | `--dt-split-prefer-phase` | +4 | −4 | 0 | 5 | 39454.0 |
| | | | `--dt-split-order=base-first --dt-split-prefer-phase` | +8 | −7 | +1 | 5 | 39414.4 |
| | | | `--dt-split-order=base-last --dt-split-prefer-phase` | +8 | −10 | −2 | 5 | 39562.9 |
| `ai-heuresis-r17-codex` | R17 | `05b63a7b09` | `--arith-int-repair` | +8 | −3 | +5 | 5 | 39290.7 |

**Against their own controls.** The register asks that the R6 policies be
compared with the QCF-enabled control on the same branch:

| R6 arm, against the control | gained | lost | net |
| --- | ---: | ---: | ---: |
| `--cbqi-round-budget=0` | +15 | −3 | +12 |
| `--cbqi-round-budget=2` | +14 | −2 | +12 |
| `--cbqi-round-share` | +6 | −6 | 0 |
| `--cbqi-round-budget=0 --cbqi-round-share` | +15 | −2 | +13 |
| `--cbqi-round-budget=2 --cbqi-round-share` | +13 | −2 | +11 |

The same comparison for R9 and R28, whose rows also name a control, finds
nothing. Against `--inst-gc=none`, `assert` is +3/−5 and `body` +2/−13.
Against `--eager-inst-literal-budget=0`, the three enabled R28 arms are
+2/−10, +5/−8 and +3/−12.

**`ai-heuresis-r15-claude` crashes.** Both of its arms segfault on the same 10
benchmarks, which the reference solves. They are 5 problems, each in the set
twice:

```
sundance/UFDTLIA/20241211-verus/{anvil/splinterdb-smt-betree__,splinterdb/betree__}PagedBetreeRefinement_v.{10,11,27,30,34}.smt2
```

The wrappers logged `cvc5 suffered a segfault.` for each. No other arm in this
sweep produced an error. The branch also answers `unknown` far more often: 37
and 34 against the reference's 5. **Its losses are mostly not slowdowns.** Of
the 32 benchmarks `--ee-share-uf-dt --ieval=off` loses, 10 are crashes, 13 are
`unknown` on benchmarks the reference proves `unsat`, and only 9 are timeouts.
For `--ee-share-uf-dt` alone, the 38 losses are 10 crashes, 15 unknowns and 13
timeouts.

## 5. What it settled

**R15's shared UF/datatypes engine is the one new mechanism that moves the
set.** Both arms rescue more than 50 benchmarks the reference cannot solve, and
with `--ieval=off` the arm nets +27 at the best PAR2 of the sweep, 37003.6
against 39436.5. It cannot be proposed as it stands. The branch crashes on 5
problems and gives up with `unknown` on 13–15 that the reference proves, so its
row must carry those failures beside its number. **R6's round budgets work as
designed but only break even.** Any budget recovers the 10 solves that turning
QCF on costs, +11 to +13 against the control, but none beats the QCF-off
reference. So the register's `--no-cbqi` choice stands, and sharing a round with
E-matching does nothing. **R1 chaining is red on every arm and gets worse with
depth.** Its default still rescues 38 benchmarks, like every earlier R1
mechanism. **R11 relevance filtering is red.** `strict` gives up on 1487
benchmarks, which is incompleteness by design and not slowness. R2, R9, R10,
R16, R17 and R28 are inside noise on every arm. R10's round-robin is the only
one of those to reach +16 gained, and it loses 26.

## 6. What it did not settle

**How much of R15's +27 is `--ieval=off`.** Evaluator-off alone measured
+20/−8, net +12, at the old reference
([entry](2026-09-25-option-sweep-one-reference.md)). The gap between the two R15
arms here is also +12, which suggests the effects add. But the option was not
re-run at `03e5ee1ebf`, so this is a hypothesis. **Whether the crash and the
unknowns are one defect.** All 10 crashes are `UFDTLIA` splinterdb problems,
the class the mechanism touches, but no backtrace was taken. **Whether any of
this survives a repeat.** It is one run per arm, as in the earlier sweeps. The
R15 figures are two to five noise bands out; everything else is within one.

**These cells are against a second reference.** The register's other cells are
against 5576 at `d7d5b948c1`. The two references are within noise of each other
(+2/−6), so a reader can compare across them in practice, but not exactly.
