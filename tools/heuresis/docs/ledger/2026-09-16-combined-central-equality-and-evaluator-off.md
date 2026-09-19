# 2026-09-16 — central equality plus evaluator-off

**Goal 3, R7/R15.** Check whether the two positive mainline controls compose.

## 1. What was asked

After central equality and evaluator-off each improved the whole-set result,
run them together before choosing the baseline and fork branches for the next
implementation experiments.

## 2. What was run

```
# 2026-09-16 11:10 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-ee-central-ieval-off.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091626-u-ssc-ee-central-ieval-off -q --no-cbqi --user-pat=strict --sat-solver=cadical --ee-mode=central --ieval=off
# cvc5: git 5cc03f4b9 on branch main
```

The driver wall time was 382 s.

## 3. The set

`quant-07-25`, **6124 benchmarks**, 30 s each. The arm read all 6124.

## 4. What came back

The local-only raw artifact is
`data/results-cvc5_solve.sh-quant-091626-u-ssc-ee-central-ieval-off.txt` (see
the [data-retention policy](../../reports/data/README.md)), read by [`gap`](../../reports/gap):

| arm | solved | unknown | timeout | time on solved (s) | PAR2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| fresh control | 5548 | 5 | 571 | 6575.4 | 41135.4 |
| `--ee-mode=central` | 5611 | 27 | 486 | 6388.4 | 37168.4 |
| `--ieval=off` | 5564 | 5 | 555 | 6243.2 | 39843.2 |
| combined | **5625** | 26 | **473** | **5679.5** | **35619.5** |

Paired results for the combined arm:

| reference | combined uniquely solves | reference uniquely solves | at least 2× faster, both solved | at least 2× slower, both solved |
| --- | ---: | ---: | ---: | ---: |
| fresh control | **101** | 24 | **180** | 2 |
| central only | 21 | 7 | 11 | 2 |
| evaluator-off only | 88 | 27 | 112 | 1 |

Combined PAR2 is 13.41% below the fresh control, 4.17% below central only,
and 10.60% below evaluator-off only. Against corrected z3 it has a **1.52
PAR2 ratio and gap set of 789**: 460 cvc5-unsolved where z3 solves and 329
both-solved cases at least 10× slower. The gap list is
[`data/gapset-u-ssc-ee-central-ieval-off-vs-z3-full-091626.txt`](../../reports/data/gapset-u-ssc-ee-central-ieval-off-vs-z3-full-091626.txt).
There were no `sat` answers or sat/unsat disagreements.

## 5. What it settled

The two controls compose positively at whole-set scale. Their combination is
the best measured configuration on this installed binary: 77 net solves and
13.4% lower PAR2 than the fresh control. The incremental benefit over central
alone—14 net solves and 4.2% lower PAR2—also shows that evaluator-off is not
merely recovering the same cases as central equality.

This raises R15 to the top implementation lead and keeps R7 high: use the
combined mode as a comparator when testing equality-engine or evaluator
branches, not just each option's original control.

## 6. What it did not settle

The combined arm still loses 24 control solves and changes 5 `unknown`
results into timeouts net, so it is not a risk-free default. More importantly,
it used installed `main@5cc03f4b9`, now 79 commits behind current upstream.
Current main must be rebuilt and the four-arm control / central /
evaluator-off / combined experiment repeated before attributing the gains to
current code or evaluating rebased branches.
