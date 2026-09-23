# 2026-09-23 — the reference re-measured on current main

**Goal 1, and the anchor for every proposal row.** Every `± solved` cell in
[`directions.md`](../directions.md) is a difference against this configuration.
It had last been measured on 2026-09-17, six days and roughly two hundred
upstream commits earlier, so no proposal could be given a number that meant
anything until it was run again.

## 1. What was asked

Run the reference configuration on the set at current cvc5 `main`, so that the
option arms of the next batch have something to be subtracted from, and so the
[progress table](../progress.md) has a current row.

## 2. What was run

`job_launcher/submit --baseline quant-cvc5.conf`, which fast-forwards the
host's `master` from upstream, builds it, installs it, and **verifies the
installed binary's own `--show-config` git hash against the checkout** before
running anything. The verified revision was

```
d7d5b948c11d2d83be0212d4a954ef49740ecdab
  sep: Never construct an empty set of heap locations (#12922), 2026-09-23
```

The arm is the generated `quant-cvc5-baseline.conf`:

```
-q --no-cbqi --user-pat=strict --sat-solver=cadical
```

`--sat-solver=cadical` is redundant on this revision — CaDiCaL has been the
declared default since 2026-08 — and is kept only because every earlier row of
the history table carries it. The exact commands are in
[`job_launcher/log.txt`](../../../../job_launcher/log.txt); the job took 519 s
including the build.

## 3. The set

`quant-07-25`, **6124 benchmarks**, 30 s each, on the idle host. All 6124 were
read. The comparison point is the retained z3 4.15.4 run of 2026-09-17 with
the nine Verus options; z3 was not re-run.

## 4. What came back

| run | solved | unknown | timeout | time on solved (s) | PAR2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| z3 4.15.4 (2026-09-17) | 5785 | 310 | 29 | 3092.5 | 23432.5 |
| **reference @ `d7d5b948c1`** | **5550** | 5 | 569 | 6615.9 | **41055.9** |

Ratio **1.75**; gap set **1064** — 534 unsolved where z3 solves, 530 solved at
least 10× slower. No sat/unsat disagreements, no errors.

Against the same configuration at `a07d513075` on 2026-09-17 (5545 solved,
41191.8 PAR2): **+5 solves and −0.33% PAR2**, which is inside the noise band
this project uses. Two hundred commits of upstream work moved this workload by
nothing measurable, which is itself the useful reading.

## 5. What it settled

The reference exists at a named revision, so an arm run against this binary can
be given a `± solved` number. It settles nothing about any proposal: no arm was
run here.

**Scope.** One run, no repetition, so the ±5 solves against 2026-09-17 is not
evidence of a real change. No gap list was retained from this run.
