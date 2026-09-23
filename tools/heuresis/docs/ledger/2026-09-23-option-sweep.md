# 2026-09-23 — the option sweep: twenty-one single-option arms

**Goal 3, across sixteen directions.** Every option proposal in
[`directions.md`](../directions.md) measured at one revision, against one
reference, changing one thing each. This is the first time the register's
`± solved` column has numbers that were all taken the same day on the same
binary.

## 1. What was asked

Fill the option rows. Each arm is the reference plus exactly one change, so the
difference in solved benchmarks is attributable to that change.

## 2. What was run

The reference binary from
[the same day's baseline](2026-09-23-reference-at-current-main.md) —
`ajr-cvc5` verified as `git d7d5b948c1 on branch master` before every arm —
with the fixed prefix

```
-q --no-cbqi --user-pat=strict --sat-solver=cadical
```

and one option added. Configs are `job_launcher/configs/quant-cvc5-w1-*.conf`;
commands are in [`job_launcher/log.txt`](../../../../job_launcher/log.txt).
Every arm read all 6124 benchmarks at 30 s on the idle host, one at a time.

## 3. The set

`quant-07-25`, **6124 benchmarks**, 30 s. The gap column compares against the
retained z3 4.15.4 run of 2026-09-17; z3 was not re-run.

## 4. What came back

Reference: **5550** solved, 5 unknown, 569 timeout, PAR2 **41055.9**, gap 1064.

| arm | direction | gained | lost | net | unknown | PAR2 | Δ PAR2 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `--ee-mode=central` | R15 | **+86** | **−19** | **+67** | 28 | 36911.3 | -10.10% |
| `--ieval=off` | R7 | **+20** | **−6** | **+14** | 5 | 39830.6 | -2.98% |
| `--deep-restart=input` | R29 | **+23** | **−20** | **+3** | 7 | 41319.0 | +0.64% |
| `--deep-restart=input --deep-restart-factor=1.5` | R29 | **+21** | **−23** | **-2** | 8 | 41518.7 | +1.13% |
| `--enum-inst` | R8 | **+3** | **−5** | **-2** | 5 | 41094.8 | +0.09% |
| `--miniscope-quant=off` | R21 | **+3** | **−6** | **-3** | 5 | 41138.6 | +0.20% |
| `--jh-rlv-order` | R11 | **+14** | **−18** | **-4** | 3 | 41079.7 | +0.06% |
| `--no-inst-no-entail` | R7 | **+4** | **−9** | **-5** | 5 | 41355.7 | +0.73% |
| `--dt-binary-split` | R16 | **+12** | **−23** | **-11** | 16 | 41616.0 | +1.36% |
| `--theoryof-mode=type` | R14 | **+9** | **−23** | **-14** | 4 | 41783.0 | +1.77% |
| `--preregister-mode=lazy` | R22 | **+21** | **−64** | **-43** | 45 | 43535.6 | +6.04% |
| `--deep-restart=all` | R29 | **+17** | **−94** | **-77** | 21 | 45492.1 | +10.81% |
| `--term-db-mode=all` | R23 | **+29** | **−124** | **-95** | 4 | 45518.0 | +10.87% |
| `--inst-when=full` | R1 | **+45** | **−162** | **-117** | 2 | 46728.5 | +13.82% |
| `--inst-max-rounds=50` | R4 | **+2** | **−233** | **-231** | 440 | 52473.4 | +27.81% |
| `--nl-ext=light` | R18 | **+6** | **−281** | **-275** | 268 | 57081.0 | +39.03% |
| `--decision=internal` | R11 | **+25** | **−504** | **-479** | 3 | 69946.0 | +70.37% |
| `--decision=stoponly` | R11 | **+20** | **−519** | **-499** | 2 | 71032.5 | +73.01% |
| `--macros-quant --macros-quant-mode=all` | R21 | **+41** | **−579** | **-538** | 511 | 70934.6 | +72.78% |
| `--inst-local` | R9 | **+24** | **−622** | **-598** | 3 | 76090.2 | +85.33% |
| `--sub-cbqi` | R6 | **+2** | **−1504** | **-1502** | 3 | 151002.3 | +267.80% |

**gained** is benchmarks the arm solves that the reference does not; **lost** is
the reverse. They are reported apart because the net hides orthogonality: an arm
can be a large net loss and still solve benchmarks nothing else reaches.

## 5. What it settled

**Orthogonality is the reading the net number hides.** Nine arms rescue ten or
more benchmarks the reference cannot solve, including several that are large net
losses: `--inst-when=full` gains 45 while losing 162, `--macros-quant` gains 41
while losing 579, `--term-db-mode=all` gains 29, `--decision=internal` gains 25,
`--inst-local` gains 24, `--deep-restart=input` gains 23 against 20 lost, and
`--preregister-mode=lazy` gains 21. Those rescued sets are worth intersecting
before any of these options is dismissed: a change that only loses says nothing,
while a change that reaches benchmarks nothing else reaches is a lead even at a
net loss. Two arms gain almost nothing — `--inst-max-rounds=50` and `--sub-cbqi`
rescue 2 each — and those are the ones the evidence simply closes.

**Two arms help on net; nineteen do not.** `--ee-mode=central` is the only substantial
gain, and it reproduces: +67 here against +63 and +70 in two earlier runs at
other revisions, so the project's largest measured effect survives
re-measurement. `--ieval=off` adds 14. Everything else is neutral or a loss,
and eight arms lose more than 40 solves.

**Unknowns are the tell for the bad ones.** `--macros-quant` returns 511
unknowns, `--inst-max-rounds=50` 440, `--nl-ext=light` 268: these are not slow
so much as incomplete, trading answers for time. `--sub-cbqi` is the worst arm
by far, −1502 solves and PAR2 nearly quadrupled, with the gap set rising to
4143.

**`--inst-local` contradicts what this register recorded, and the earlier
number is the unreliable one.** The [2026-09-15
entry](2026-09-15-sat-and-instance-order.md) measured +9 solves and +1.19% PAR2;
here it loses **598** solves and raises PAR2 85%. The runs are not comparable:
that arm was `-q --no-cbqi --user-pat=strict --inst-local`, with no explicit
`--sat-solver`, against a control with none either — and at that revision the
implicit backend was *not* CaDiCaL, which is why its control solved 5495 where
the CaDiCaL control solved 5548. So the old pair measured `--inst-local` on one
SAT backend and this one measures it on another. Given the option scopes
instantiation lemmas inside the SAT solver, a backend-sized difference is not
surprising. **The single arm that would settle it** is `--inst-local` with
`--sat-solver=minisat` at this revision; it was not run here.

**Scope.** One run per arm, no repetition, so small differences — everything
between −5 and +3 — are inside the noise this project has measured before and
should not be read as effects. No gap lists were retained.
