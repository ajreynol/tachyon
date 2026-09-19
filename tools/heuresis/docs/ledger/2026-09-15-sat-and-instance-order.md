# 2026-09-15 — CaDiCaL and two instance-order controls

**Goal 3, R13 and R10.** Three one-option changes from the fresh
`--no-cbqi --user-pat=strict` control.

## 1. What was asked

Correct the SAT-backend omission in the original baseline by selecting
CaDiCaL explicitly, and test the two available mainline approximations to
changing where instance lemmas sit in the search: `--inst-local` and
`--jh-rlv-order`.

## 2. What was run

The control is the `quant-091526-u-ss` arm in
[`2026-09-15-quantifier-controls.md`](2026-09-15-quantifier-controls.md).
The three new launch records are:

```
# 2026-09-15 16:10 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-cadical.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091526-u-ssc -q --no-cbqi --user-pat=strict --sat-solver=cadical
# cvc5: git 5cc03f4b9 on branch main

# 2026-09-15 16:10 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-inst-local.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091526-u-ss-inst-local -q --no-cbqi --user-pat=strict --inst-local
# cvc5: git 5cc03f4b9 on branch main

# 2026-09-15 16:10 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-jh-rlv-order.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091526-u-ss-jh-rlv-order -q --no-cbqi --user-pat=strict --jh-rlv-order
# cvc5: git 5cc03f4b9 on branch main
```

All four arms used cvc5 `main@5cc03f4b9`. Driver wall times were 468 s for
the control, then 448 s, 481 s, and 490 s in table order.

## 3. The set

`quant-07-25`, **6124 benchmarks**, 30 s each. Every arm read all 6124.

## 4. What came back

Raw files in [`data/`](../../reports/data), read by [`gap`](../../reports/gap):

| arm | solved | unknown | timeout | time on solved (s) | PAR2 | change from control |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| control | 5495 | 10 | 619 | 6187.4 | 43927.4 | — |
| explicit CaDiCaL | **5550** | **5** | **569** | 6616.4 | **41056.3** | **−6.54%** |
| `--inst-local` | 5504 | 17 | 603 | 7249.0 | 44449.0 | +1.19% |
| `--jh-rlv-order` | 5429 | 5 | 690 | **5398.1** | 47098.1 | +7.22% |

Paired with the control:

| arm | uniquely solves | control uniquely solves | at least 2× faster, both solved | at least 2× slower, both solved |
| --- | ---: | ---: | ---: | ---: |
| explicit CaDiCaL | 55 | 0 | 152 | 116 |
| `--inst-local` | 84 | 75 | 171 | 480 |
| `--jh-rlv-order` | 10 | 76 | 113 | 156 |

Against the corrected z3 baseline, the control's PAR2 ratio / gap is 1.88 /
1122. Explicit CaDiCaL improves that to **1.75 / 1073** (534 cvc5-unsolved,
539 solved-but-at-least-10×-slower). `--inst-local` is 1.90 / 1332 and
`--jh-rlv-order` is 2.01 / 1135. No arm produced a `sat` answer or a
sat/unsat disagreement. The CaDiCaL gap list is
[`data/gapset-u-ssc-vs-z3-full-091526.txt`](../../reports/data/gapset-u-ssc-vs-z3-full-091526.txt).

## 5. What it settled

R13 has a real, corpus-wide win: explicit CaDiCaL recovers 55 additional
benchmarks, loses none of the control's solves, removes 50 timeouts, and cuts
PAR2 by 6.5%. The explicit option remains necessary even though CaDiCaL is
the declared default on current cvc5 `main`, because incremental solving is
on by default and the default-setting code otherwise switches the backend to
MiniSat.

The two global R10 controls are negative. `--inst-local` trades many rescues
for many losses and makes 480 common solves at least 2× slower; its slightly
better timeout count is overwhelmed by slower solves and a much larger
solved-but-slow gap. `--jh-rlv-order` reduces time on the benchmarks it still
solves but loses 66 net solves and raises PAR2 7.2%. Their mixed paired
results justify looking for a subpopulation, not enabling either globally.

## 6. What it did not settle

This did not run [`ajreynol:ai-instDefer`](https://github.com/ajreynol/cvc5/tree/ai-instDefer),
test real clause deletion, or explain the cases helped by the ordering
changes. Those cases should be classified before paying the branch-rebase
cost. The CaDiCaL result also does not identify which SAT policy caused the
gain.
