# 2026-09-15 — separating `--no-cbqi` from strict user patterns

**Goal 3, R5/R6.** A four-arm full-set experiment separating the two
quantifier options in the best-known configuration.

## 1. What was asked

The 2026-09-14 baseline bundled `--no-cbqi` and `--user-pat=strict`, so it
could not say which option caused the improvement. Run default, each option
alone, and both together on the same binary and set.

## 2. What was run

The configs in [`job_launcher/configs/`](../../../job_launcher/configs/) at
launch; the exact historical commands are preserved below because the live
baseline config advances when an option wins. The relevant
[`job_launcher/log.txt`](../../../job_launcher/log.txt) entries are:

```
# 2026-09-15 15:35 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-default.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091526-default -q
# cvc5: git 5cc03f4b9 on branch main

# 2026-09-15 15:35 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-no-cbqi.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091526-no-cbqi -q --no-cbqi
# cvc5: git 5cc03f4b9 on branch main

# 2026-09-15 15:35 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-user-pat-strict.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091526-user-pat-strict -q --user-pat=strict
# cvc5: git 5cc03f4b9 on branch main

# 2026-09-15 15:35 [dev1:~/benchmarks/quant-07-25] (quant-cvc5.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091526-u-ss -q --no-cbqi --user-pat=strict
# cvc5: git 5cc03f4b9 on branch main
```

The jobs ran sequentially in one queue. Driver wall times were 594 s, 471 s,
476 s, and 468 s in table order below.

## 3. The set

`quant-07-25`, **6124 benchmarks**, 30 s each. Every arm read all 6124.

## 4. What came back

Raw files in [`data/`](data/), read by [`gap`](../gap):

| arm | solved | unknown | timeout | time on solved (s) | PAR2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| default | 5414 | 4 | 706 | 10879.0 | 53479.0 |
| `--no-cbqi` | **5497** | 10 | **617** | 6397.6 | 44017.6 |
| `--user-pat=strict` | 5492 | 9 | 623 | 6512.4 | 44432.4 |
| both | 5495 | 10 | 619 | **6187.4** | **43927.4** |

Against default, `--no-cbqi` rescues 96 benchmarks and loses 13; strict
patterns rescue 90 and lose 12; both rescue 93 and lose 12. The two
single-option rescue sets overlap on 87 benchmarks: only 9 are unique to
`--no-cbqi`, only 3 to strict patterns, and the combined arm rescues only 2
outside their union. Against `--no-cbqi` alone, the combined arm uniquely
solves 6 and loses 8. Against strict patterns alone, it uniquely solves 5 and
loses 2.

Using the corrected nine-option z3 4.15.4 run recorded separately, the PAR2
ratios / gap-set sizes are default 2.28 / 2241, `--no-cbqi` 1.88 / 1125,
strict 1.90 / 1164, and both 1.88 / 1122. There were no `sat` answers or
sat/unsat disagreements.

## 5. What it settled

R6's requested factorial experiment is done. Either option alone recovers
nearly all of the aggregate improvement previously credited to their bundle;
the effects are highly overlapping and mildly non-monotone. `--no-cbqi`
alone wins on solved count and timeouts, while the combination has the best
time-on-solved and PAR2 by a small margin. This is consistent with strict
user-pattern ownership already excluding other instantiation techniques for
most relevant patterned quantifiers, but the run does not itself prove that
mechanism.

## 6. What it did not settle

The run did not measure user-pattern coverage or say why the small disjoint
rescue/loss sets differ. Inspect those cases and the ownership trace before
changing the fixed configuration. It also did not test the SAT backend;
that is the separate R13 entry.
