# 2026-09-16 — datatype splitting and the central equality engine

**Goal 3, R15/R16.** Two cheap mainline controls selected by the first
whole-set statistics run, with a fresh repeat of the fixed control.

## 1. What was asked

Turn the measured datatype-split activity and equality-engine hypothesis into
whole-set evidence. Compare `--dt-binary-split` and `--ee-mode=central` with
the best measured cvc5 configuration on the same binary and set.

## 2. What was run

The configs are in [`job_launcher/configs/`](../../../../job_launcher/configs).
The relevant [`job_launcher/log.txt`](../../../../job_launcher/log.txt) records
are:

```
# 2026-09-16 10:08 [dev1:~/benchmarks/quant-07-25] (quant-cvc5.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091626-u-ssc -q --no-cbqi --user-pat=strict --sat-solver=cadical
# cvc5: git 5cc03f4b9 on branch main

# 2026-09-16 10:08 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-dt-binary-split.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091626-u-ssc-dt-binary -q --no-cbqi --user-pat=strict --sat-solver=cadical --dt-binary-split
# cvc5: git 5cc03f4b9 on branch main

# 2026-09-16 10:08 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-ee-central.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091626-u-ssc-ee-central -q --no-cbqi --user-pat=strict --sat-solver=cadical --ee-mode=central
# cvc5: git 5cc03f4b9 on branch main
```

The jobs ran sequentially. Driver wall times were 449 s, 445 s, and 402 s in
table order.

## 3. The set

`quant-07-25`, **6124 benchmarks**, 30 s each. Every arm read all 6124.

## 4. What came back

Raw files in [`data/`](../../reports/data), read by [`gap`](../../reports/gap):

| arm | solved | unknown | timeout | time on solved (s) | PAR2 | change from control |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fresh control | 5548 | 5 | 571 | 6575.4 | 41135.4 | — |
| `--dt-binary-split` | 5540 | 16 | 568 | 6568.5 | 41608.5 | +1.15% |
| `--ee-mode=central` | **5611** | 27 | **486** | **6388.4** | **37168.4** | **−9.64%** |

Paired with the fresh control:

| arm | uniquely solves | control uniquely solves | at least 2× faster, both solved | at least 2× slower, both solved |
| --- | ---: | ---: | ---: | ---: |
| `--dt-binary-split` | 10 | 18 | 0 | 0 |
| `--ee-mode=central` | **84** | 21 | **75** | 0 |

The preceding day's nominally identical control solved 5550 versus 5548 in
the fresh repeat. The two repeats have four old-only and two new-only solves,
which is the observed run-to-run boundary noise for interpreting small status
changes here.

Against the corrected z3 baseline, the fresh control's PAR2 ratio / gap size
is 1.76 / 1071. Binary datatype splitting is 1.78 / 1081. Central equality is
**1.59 / 918**, comprising 474 cvc5-unsolved cases where z3 solves and 444
both-solved cases where cvc5 is at least 10× slower. Its gap list is
[`data/gapset-u-ssc-ee-central-vs-z3-full-091626.txt`](../../reports/data/gapset-u-ssc-ee-central-vs-z3-full-091626.txt).
No arm produced `sat` or a sat/unsat disagreement.

## 5. What it settled

R15 moves from a profiling hypothesis to a high-priority implementation lead.
Central equality has 63 net additional solves, removes 85 timeouts, yields 75
at-least-2× speedups with no corresponding slowdowns under that threshold,
and cuts PAR2 by 9.6%. The rescues are not one isolated family: 59 are in the
Sundance UFDTLIA slice and 14 in its UFDTNIA slice, with the remainder spread
through the other Verus-derived groups.

R16's binary-split control is negative or neutral at whole-set scale. Its
eight net lost solves are near but larger than the repeat noise, and PAR2 gets
1.15% worse. This does not support changing that global policy or, by itself,
paying to maintain a relevance-gating branch.

## 6. What it did not settle

The central run does not attribute the gain to shared-equality propagation,
notification traffic, arithmetic's equality solver, or a changed search path.
It also used installed `main@5cc03f4b9`, now 79 commits behind current upstream
`main@835ccd95e`. CaDiCaL is the declared default on current main; these runs
select it explicitly both for comparability and to prevent default incremental
mode from selecting MiniSat. Rebuild current main, repeat the control and
central mode, then test the one-commit
[`ajreynol:ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare)
branch. Its exact effect is narrower than
[`ajreynol:dtMergeNotify-v3`](https://github.com/ajreynol/cvc5/tree/dtMergeNotify-v3),
which is both larger and conflicts in a disposable rebase trial.
