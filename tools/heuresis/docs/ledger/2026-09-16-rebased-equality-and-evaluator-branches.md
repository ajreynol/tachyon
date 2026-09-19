# 2026-09-16 — current main and rebased equality/evaluator branches

**Goal 3, R7/R15.** Recheck the strongest option result on current main, then
test the two compact branches that it motivated.

## 1. What was asked

After the maintainer updated the requested fork branches, run more jobs and
decide whether any branch has enough safety, performance, and patch-shape
evidence to move toward cvc5 main.

## 2. What was run

Current cvc5 `main` and the fork's `master` were both
`d7d03b082c56ad8e7226e0b5385973d82b16d626`. The current-main control used
`--no-cbqi --user-pat=strict --sat-solver=cadical`; the two option arms added
`--ee-mode=central`, then `--ieval=off`.

The branch arms were:

```
# ai-eecNoShare@c2f448675e
-q --no-cbqi --user-pat=strict --sat-solver=cadical --ee-mode=central --ieval=off

# ievalTravTrie@78e6fd0889
-q --no-cbqi --user-pat=strict --sat-solver=cadical --ee-mode=central
```

Both branches first built successfully and passed `make regress -j64`.
Driver wall times were 448 s for the control, 401 s for central, 379 s for
central plus evaluator-off, 380 s for `ai-eecNoShare`, and 402 s for
`ievalTravTrie`. The exact commands and revisions are in
[`job_launcher/log.txt`](../../../../job_launcher/log.txt); the five configs are
in [`job_launcher/configs/`](../../../../job_launcher/configs).

## 3. The set

`quant-07-25`, **6124 benchmarks**, 30 s each. Every arm read all 6124.

## 4. What came back

The local-only raw artifacts have names beginning
`results-cvc5_solve.sh-quant-091626-u-ssc-current`, plus
`results-cvc5_solve.sh-quant-091626-u-ssc-eec-no-share.txt` and
`results-cvc5_solve.sh-quant-091626-u-ssc-ieval-trav-trie.txt`; see the
[data-retention policy](../../reports/data/README.md). [`gap`](../../reports/gap) produced:

| arm | solved | unknown | timeout | time on solved (s) | PAR2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| current-main control | 5546 | 5 | 573 | 6527.7 | 41207.7 |
| current-main central | 5616 | 28 | 480 | 6481.3 | 36961.3 |
| current-main central + evaluator-off | **5623** | 27 | 474 | **5540.5** | **35600.5** |
| `ai-eecNoShare`, central + evaluator-off | **5625** | 27 | **472** | 5588.6 | **35528.6** |
| `ievalTravTrie`, central | 5615 | 28 | 481 | 6452.9 | 36992.9 |

Current-main central lowers PAR2 10.30% versus the control and adds 70 net
solves. The combined arm lowers PAR2 13.61% and adds 77 net solves. Against
corrected z3, the combined arm has ratio **1.52** and a **796-case gap**. The
local-only list is
`data/gapset-u-ssc-current-ee-central-ieval-off-vs-z3-full-091626.txt`.

Paired branch results:

| branch comparison | branch-only solves | main-only solves | branch at least 2× faster | branch at least 2× slower | PAR2 change |
| --- | ---: | ---: | ---: | ---: | ---: |
| `ai-eecNoShare` vs combined | 5 | 3 | 114 | 106 | −0.20% |
| `ievalTravTrie` vs central | 4 | 5 | 120 | 103 | +0.09% |
| `ievalTravTrie` vs evaluator-off comparator | 7 | 15 | 108 | 167 | +3.91% |

No arm returned `sat`, and there were no sat/unsat disagreements.

## 5. What it settled

The option result is real on current main: central equality remains a strong
R15 signal, and evaluator-off still composes with it. That is the promising
implementation direction, but this one workload does not justify changing a
global default without cross-corpus and correctness-policy evaluation.

Neither tested branch earned a performance-based upstream recommendation.
`ai-eecNoShare` is regression-clean and reviewable—one effective source
commit, one file, +9/−3—but its two net solves and 0.20% PAR2 change are within
the observed boundary/run noise, with nearly balanced large speedups and
slowdowns. Instrument the number and cost of skipped shared-equality
propagations before proposing it as an optimization.

`ievalTravTrie` is also regression-clean, but is neutral against the enabled
evaluator and clearly loses to evaluator-off. Its effective source delta is
eight files, +165/−43, while its merged history is 320 commits ahead of main;
any future experiment should be a fresh focused port with evaluator-work
counters, not an upstream request for the branch as it stands.

## 6. What it did not settle

The runs cover only the fixed Verus-derived set and do not measure callback
counts, evaluator pushes, early trie rejections, or memory. The small branch
movements need not reproduce under another run or timeout.

The third requested branch was not testable: the published
[`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst)
tip remained `d9a13309dc1`, **138 commits behind / 5 ahead** current main when
rechecked after the other jobs. A rebased tip may exist locally, but it must be
pushed before dev1 can build it.
