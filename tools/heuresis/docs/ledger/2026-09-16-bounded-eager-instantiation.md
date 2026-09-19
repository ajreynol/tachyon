# 2026-09-16 — bounded eager instantiation on the pushed branch

**Goal 3, R1/R28.** Test the rebased eager-instantiation branch, now that its
tip is on current main, against the strongest measured configuration.

## 1. What was asked

The maintainer pushed the rebased
[`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst)
tip, which closed the one blocker recorded in
[`2026-09-16-rebased-equality-and-evaluator-branches.md`](2026-09-16-rebased-equality-and-evaluator-branches.md).
Establish whether bounded eager instantiation — E-matching on new terms at
standard effort, paced by the branch's own budgets — helps this set, and
whether the branch perturbs anything with its module switched off.

## 2. What was run

The branch tip was `claude-eagerInst@995b23bcfa`, **0 behind / 6 ahead** of
`cvc5:main@95050cf8155d`; the fork's `master` equalled that main. It built and
passed `make regress -j64` in 1m49s before any job was queued.

All three arms extend the combined arm of the preceding entry,
`-q --no-cbqi --user-pat=strict --sat-solver=cadical --ee-mode=central --ieval=off`:

```
# quant-091626-u-ssc-eager-off       (no further options — the module is default-off)
# quant-091626-u-ssc-eager-inst      --eager-inst
# quant-091626-u-ssc-eager-inst-rlv  --eager-inst --eager-inst-rlv
```

`--eager-inst` runs at the branch's default budgets:
`--eager-inst-gen-limit=1`, `--eager-inst-pair-limit=2000`,
`--eager-inst-multi=true`, `--eager-inst-merge=false`. The first arm is a
sanity control: the module is off, so it isolates whatever the branch's
non-module changes (20 lines in `instantiate.cpp`, plus the quantifiers-engine
registration) cost on their own.

The exact commands and revisions are in
[`job_launcher/log.txt`](../../../../job_launcher/log.txt); the three configs are
`quant-cvc5-eager-off.conf`, `quant-cvc5-eager-inst.conf` and
`quant-cvc5-eager-inst-rlv.conf` in
[`job_launcher/configs/`](../../../../job_launcher/configs). tmux refused a
multi-job queue as `command too long`, so the three ran one window each,
back-to-back with a wait between, rather than concurrently.

## 3. The set

`quant-07-25`, **6124 benchmarks**, 30 s each. Every arm read all 6124. The
reference is the full-Verus-option z3 4.15.4 run of
[`2026-09-15-z3-full-verus-options.md`](2026-09-15-z3-full-verus-options.md).

## 4. What came back

The local-only raw artifacts are
`data/results-cvc5_solve.sh-quant-091626-u-ssc-eager-{off,inst,inst-rlv}.txt`;
see the [data-retention policy](../../reports/data/README.md). [`gap`](../../reports/gap) produced:

| arm | solved | unknown | timeout | time on solved (s) | PAR2 | ratio vs z3 | gap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| combined control (main) | 5623 | 27 | 474 | 5540.5 | 35600.5 | 1.52 | 796 |
| branch, module off | **5624** | 27 | **473** | 5557.3 | **35557.3** | 1.52 | **789** |
| `--eager-inst` | 5496 | 46 | 582 | **4797.9** | 42477.9 | 1.81 | 916 |
| `--eager-inst --eager-inst-rlv` | 5561 | **25** | 538 | 5646.9 | 39426.9 | 1.68 | 891 |

Paired against the branch with the module off:

| comparison | arm-only solves | off-only solves | arm ≥2× faster | arm ≥2× slower | PAR2 change |
| --- | ---: | ---: | ---: | ---: | ---: |
| module off vs control (main) | 2 | 1 | **0** | **0** | −0.12% |
| `--eager-inst` vs module off | 26 | 154 | 46 | 125 | **+19.46%** |
| `--eager-inst-rlv` vs module off | 12 | 75 | 8 | 70 | **+10.88%** |
| `--eager-inst-rlv` vs `--eager-inst` | 103 | 38 | 85 | 84 | −7.18% |

Restricted to the control's own 796-case gap set, `--eager-inst` is +14.20%
PAR2 and `--eager-inst-rlv` +8.25%.

Of the **461** gap-set benchmarks the control cannot solve at all:

| rescued by | count |
| --- | ---: |
| `--eager-inst` | 23 |
| `--eager-inst-rlv` | 11 |
| both | 5 |
| **either arm** | **29** |

z3 solves all 29. They fall in `sundance/UFDTNIA` (15),
`verus-no-option/mariposa_queries` (7), `sundance/UFDTLIA` (6) and
`verus-no-option/mimalloc` (1). No arm returned `sat`, and there were no
sat/unsat disagreements anywhere.

## 5. What it settled

**The sanity control is clean, which makes the rest attributable.** With the
module off the branch is main: two net solves, PAR2 −0.12%, and *zero*
benchmarks at least 2× faster or slower in either direction. Every difference
below is the eager module and not the branch it rides on.

**Bounded eager instantiation, as this branch implements it, is a clear
net loss on this set.** `--eager-inst` costs 19.46% PAR2 and 128 net solves;
it is not a candidate for a default, and no upstream recommendation follows
from this result. `--eager-inst-rlv` halves the damage but remains 10.88%
worse than leaving the module off.

**The loss has exactly the recorded shape.** `--eager-inst` spends *less* time
on what it solves than the control does — 4797.9 s against 5557.3 s, 13.7%
less — while timing out 109 more often and returning 19 more unknowns. It is
faster when it works and drowns when it does not. That is the failure mode the
notes attribute to every prior eager attempt, and this is the first time it has
been measured on the set rather than recalled. It bears directly on **R9**:
the premise that eager instantiation needs lemma deletion to be viable is now
evidence, not folklore.

**The negative aggregate hides a positive signal worth keeping.** Twenty-nine
of the 461 gap cases the best configuration cannot solve at all are solved by
one of the two eager arms, and only five by both — the arms are largely
complementary, so this is not one easy cluster being picked up twice. cvc5's
portfolio currently has no access to those 29 cases in any measured
configuration. Under the [charter's
criteria](../../README.md#what-makes-a-useful-finding) that is the first candidate
finding this project has produced: not "turn eager instantiation on", but "a
bounded eager mode reaches benchmarks nothing else here reaches, and the open
question is how to pay for it only where it pays".

## 6. What it did not settle

No counters were collected. The branch registers `d_statPairs`,
`d_statMatches`, `d_statInst`, `d_statRematch`, `d_procTime` and
`d_addInstTime`, and none of them were read in these runs, so the *mechanism*
of both the loss and the 29 rescues is unmeasured. Nothing here distinguishes
a pacing problem (wrong budgets) from a lifetime problem (no deletion); the
`gen-limit`, `pair-limit` and `eager-inst-limit` budgets were left at their
defaults and never swept, and `--eager-inst-merge` was never enabled.

Whether the 29 rescues survive a rerun, a different timeout, or a different
corpus is untested, and 29 of 6124 is within the range where boundary effects
matter. The runs also do not say whether a cheap static predicate separates
the rescued benchmarks from the 125 that `--eager-inst` makes at least 2×
slower, which is what a gating policy would need.
