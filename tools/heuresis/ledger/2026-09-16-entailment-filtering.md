# 2026-09-16 — instantiation-evaluator and entailment controls

**Goal 3, R7.** Separate the incremental partial evaluator from generalized
learning and the completed-instance entailment check.

## 1. What was asked

Concretize the 2026-09-15 observation that entailed duplicates are 8.1% of
gap-set instantiations. Test whether the default evaluator earns its cost, and
whether any effect belongs to partial evaluation or to the final entailment
filter.

## 2. What was run

The fresh control is the first arm in
[`2026-09-16-datatype-and-equality-controls.md`](2026-09-16-datatype-and-equality-controls.md).
The three new [`job_launcher/log.txt`](../../../job_launcher/log.txt) records
are:

```
# 2026-09-16 10:39 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-ieval-off.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091626-u-ssc-ieval-off -q --no-cbqi --user-pat=strict --sat-solver=cadical --ieval=off
# cvc5: git 5cc03f4b9 on branch main

# 2026-09-16 10:39 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-ieval-use-learn.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091626-u-ssc-ieval-use-learn -q --no-cbqi --user-pat=strict --sat-solver=cadical --ieval=use-learn
# cvc5: git 5cc03f4b9 on branch main

# 2026-09-16 10:39 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-no-inst-no-entail.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091626-u-ssc-no-inst-no-entail -q --no-cbqi --user-pat=strict --sat-solver=cadical --no-inst-no-entail
# cvc5: git 5cc03f4b9 on branch main
```

The jobs ran sequentially. Driver wall times were 430 s, 450 s, and 451 s in
table order.

## 3. The set

`quant-07-25`, **6124 benchmarks**, 30 s each. Every arm read all 6124.

## 4. What came back

Raw files in [`data/`](data/), read by [`gap`](../gap):

| arm | solved | unknown | timeout | time on solved (s) | PAR2 | change from control |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fresh control (`--ieval=use`) | 5548 | 5 | 571 | 6575.4 | 41135.4 | — |
| `--ieval=off` | **5564** | 5 | **555** | **6243.2** | **39843.2** | **−3.14%** |
| `--ieval=use-learn` | 5548 | 5 | 571 | 6635.6 | 41195.6 | +0.15% |
| `--no-inst-no-entail` | 5549 | 5 | 570 | 6776.3 | 41276.3 | +0.34% |

Paired with the fresh control:

| arm | uniquely solves | control uniquely solves | at least 2× faster, both solved | at least 2× slower, both solved |
| --- | ---: | ---: | ---: | ---: |
| `--ieval=off` | **23** | 7 | **13** | 3 |
| `--ieval=use-learn` | 3 | 3 | 0 | 0 |
| `--no-inst-no-entail` | 4 | 3 | 2 | 2 |

Against the corrected z3 baseline, the control's PAR2 ratio / gap size is
1.76 / 1071. Evaluator-off improves this to **1.70 / 954**; generalized
learning is 1.76 / 1087 and no completed-instance entailment check is 1.76 /
1075. No arm produced `sat` or a sat/unsat disagreement.

## 5. What it settled

R7 has a real but mechanism-specific signal. Disabling the incremental
instantiation evaluator yields 16 net solves and lowers PAR2 3.1%.
Generalized learning changes no aggregate status count and is slightly
slower. Disabling only `--inst-no-entail` is also slightly slower and changes
only one net solve, within repeat noise.

The source distinction matters: `--ieval=off` removes partial evaluation as
E-matching fills a match, but leaves the default completed-instance
`EntailmentCheck` enabled. `--no-inst-no-entail` does the converse. Thus these
runs support reducing the cost or selectivity of partial evaluation; they do
not support dropping entailment filtering wholesale.

## 6. What it did not settle

The run did not count evaluator pushes, early rejections, or time in the
evaluator, so it cannot say whether the win comes from bookkeeping overhead or
from avoiding a harmful pruning/search-order effect. It also used installed
`main@5cc03f4b9`, 79 commits behind current upstream. Rebuild current main,
repeat evaluator-off, and test the two-commit
[`ajreynol:ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie)
branch with those counters. The branch makes partial evaluation traverse term
tries as assignments arrive and rebased cleanly in a disposable trial, but its
tip is from 2023 and the whole design must be revalidated.
