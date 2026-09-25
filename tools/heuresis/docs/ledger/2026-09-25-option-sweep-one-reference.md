# 2026-09-25 — the option sweep re-run on one reference

**Goal 3, a correction.** The register had **two** references: options were
measured in the launcher's build directory (5550 solved) and branches in a
separate one (5576), and two Production builds of the same commit differ by 26
solves, so an option row could not be compared with a branch row. This re-runs
every option arm in the branch directory, against the reference built there, and
the register now has one reference. **Complete**: all 22 arms ran, plus the
reference, on one binary.

## 1. What was asked

Put the option rows and the branch rows on the same reference. Additionally,
price `--cbqi`: it is in the reference as `--no-cbqi`, and the register had
declared it unmeasurable for that reason.

## 2. What was run

**One build for the whole sweep.** cvc5 `d7d5b948c11d2d83be0212d4a954ef49740ecdab`
checked out in the branch-sweep build directory, built once, its own
`--show-config` hash verified against that commit, smoke-tested, then used
unchanged for every arm. No arm triggered a rebuild, so no arm can differ from
another by anything but its options — the failure mode that cost the branch
sweep 38 arms cannot arise here.

```
-q --no-cbqi --user-pat=strict --sat-solver=cadical   <one option added>
```

**One arm subtracts instead of adding.** `--cbqi` removes `--no-cbqi` from the
prefix, because that option is the reference's own choice and the only way to
price a choice the prefix already makes is to take it away. `cbqi` is default-on
in cvc5, so the reference disables a default.

A **re-run of the reference itself** was included, to check that this directory
reproduces 5576 rather than assuming it.

## 3. The set

`quant-07-25`, **6124 benchmarks**, 30 s, one arm at a time on the idle host.

## 4. The reference reproduced, and the noise band is now measured

The rebuilt reference solves **5576**, with the same 5 unknown and 543 timeout as
the branch sweep's reference, PAR2 **39313.7** against 39304.4 — 0.02% apart.

**Two builds of the same commit in the same directory disagree on 8 benchmarks:
4 each way, net 0.** That is the first direct measurement of this project's
run-to-run churn, and it is what the ±5 noise band had been assuming without
evidence. The band stands.

It also settles what the 5550/5576 gap was: a genuine difference between two
build directories, not randomness. A rebuild here lands on 5576 every time.

## 5. What came back

Reference: **5576** solved, 5 unknown, 543 timeout, PAR2 **39313.7**.
**gained** is benchmarks the arm solves that the reference does not; **lost** is
the reverse.

| arm | gained | lost | net | unknown | PAR2 | Δ PAR2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `--ee-mode=central` | **+73** | **−19** | **+54** | 28 | 35646.7 | -9.33% |
| `--ieval=off` | **+20** | **−8** | **+12** | 5 | 38201.2 | -2.83% |
| `--enum-inst` | **+7** | **−3** | **+4** | 5 | 39196.8 | -0.30% |
| `--deep-restart=input --deep-restart-factor=1.5` | **+19** | **−17** | **+2** | 8 | 39572.7 | +0.66% |
| `--deep-restart=input` | **+19** | **−18** | **+1** | 7 | 39613.1 | +0.76% |
| `--no-inst-no-entail` | **+8** | **−9** | **−1** | 5 | 39484.1 | +0.43% |
| `--miniscope-quant=off` | **+5** | **−8** | **−3** | 5 | 39406.8 | +0.24% |
| `--dt-binary-split` | **+12** | **−23** | **−11** | 18 | 39896.7 | +1.48% |
| `--jh-rlv-order` | **+11** | **−23** | **−12** | 3 | 39647.5 | +0.85% |
| `--cbqi` (prefix minus `--no-cbqi`) | **+2** | **−16** | **−14** | 5 | 40186.6 | +2.22% |
| `--theoryof-mode=type` | **+10** | **−29** | **−19** | 4 | 40248.6 | +2.38% |
| `--preregister-mode=lazy` | **+26** | **−72** | **−46** | 45 | 41814.2 | +6.36% |
| `--deep-restart=all` | **+15** | **−95** | **−80** | 23 | 43919.3 | +11.72% |
| `--term-db-mode=all` | **+29** | **−129** | **−100** | 5 | 44093.9 | +12.16% |
| `--inst-when=full` | **+38** | **−170** | **−132** | 2 | 45619.0 | +16.04% |
| `--inst-max-rounds=50` | **+3** | **−248** | **−245** | 450 | 51559.9 | +31.15% |
| `--nl-ext=light` | **+8** | **−281** | **−273** | 268 | 55326.6 | +40.73% |
| `--decision=internal` | **+25** | **−502** | **−477** | 3 | 68078.6 | +73.17% |
| `--decision=stoponly` | **+23** | **−525** | **−502** | 2 | 69322.5 | +76.33% |
| `--macros-quant --macros-quant-mode=all` | **+43** | **−595** | **−552** | 521 | 70043.9 | +78.17% |
| `--inst-local` | **+23** | **−629** | **−606** | 3 | 74691.9 | +89.99% |
| `--sub-cbqi` | **+2** | **−1484** | **−1482** | 4 | 147867.2 | +276.12% |

## 6. What the correction changed

Every arm moved, and mostly in the same direction: against a reference that
solves 26 more benchmarks, an option has less room to gain and more to lose.

| arm | on 5550 | on 5576 |
| --- | ---: | ---: |
| `--ee-mode=central` | +67 | **+54** |
| `--inst-when=full` | −117 | **−132** |
| `--macros-quant --macros-quant-mode=all` | −538 | **−552** |
| `--inst-max-rounds=50` | −231 | **−245** |
| `--jh-rlv-order` | −4 | **−12** |
| `--inst-local` | −598 | **−606** |

**No conclusion is overturned.** `--ee-mode=central` is still the only option
above +20 and still the largest single effect in the register; the heavy losses
are still heavy. The largest shift is `--ee-mode=central` losing 13 of its 67,
which is a correction to a number, not to a finding.

**Four arms changed sign, all inside the noise band**: `--enum-inst` −2 → +4,
`--deep-restart=input --deep-restart-factor=1.5` −2 → +2, `--no-inst-no-entail`
−5 → −1, `--deep-restart=input` +3 → +1. This is what a ±4 churn predicts, and
it is the reason a cell inside the band is marked ⚪ rather than reported as a
small gain or a small loss.

## 7. What this does not settle

**One run per arm**, apart from the reference, which now has two.

**`--user-pat=strict` is still unpriced.** It is the reference's other embedded
choice, and the same subtraction that priced `--cbqi` would price it. It was not
run here because it was not asked for.

## 8. What `--cbqi` settled

The reference's own `--no-cbqi` is **worth about +14 solves**, and that is much
less than the register had been claiming for it.

Run with cbqi turned back on, the solver gains 2 benchmarks and loses 16 — net
**−14** for the arm, so **+14** for the reference's choice. PAR2 rises from
39313.7 to 40186.6.

The register had cited **+83** for this option, taken in 2026-09-15 against
`default` at `5cc03f4b9`. That figure is not wrong for what it measured; it is
simply about a different solver and a different baseline, one where quantifier
handling had not yet had `--user-pat=strict` and CaDiCaL applied to it. On the
current reference the effect is a sixth of that. **A default-change proposal
keeps its number only as long as the baseline it was taken against**, and this is
the clearest instance of it in the register.

The sign of this row reads backwards from every other option row, because the
arm is the proposal's opposite. Its cell in
[`directions.md`](../directions.md) says so.

`--sub-cbqi`, the related option, remains the worst arm in the sweep: **+2 /
−1484**, PAR2 147867.2, 4094 solved against the reference's 5576.
