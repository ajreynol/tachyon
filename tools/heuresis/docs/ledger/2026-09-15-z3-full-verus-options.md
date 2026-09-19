# 2026-09-15 — z3 with the full current Verus option set

**Goal 1 correction.** This resolves the second caveat in
[`2026-09-15-baseline-caveats.md`](2026-09-15-baseline-caveats.md).

## 1. What was asked

Rerun z3 4.15.4 with all nine options passed by current Verus, rather than
the five-option list used by the original baseline, before quoting the gap.

## 2. What was run

```
# 2026-09-15 16:34 [dev1:~/benchmarks/quant-07-25] (quant-z3.conf)
solve_dir_rec_par_z3 -t 30 z3-4.15.4 z3_solve.sh quant-091526-z3-4.15.4 auto_config=false smt.mbqi=false smt.case_split=3 smt.qi.eager_threshold=100.0 smt.delay_units=true smt.arith.solver=2 smt.arith.nl=false pi.enabled=false rewriter.sort_disjunctions=false
```

The binary reports `Z3 version 4.15.4 - 64 bit`. Driver wall time was 95 s.

## 3. The set

`quant-07-25`, **6124 benchmarks**, 30 s each. Both z3 runs read all 6124.

## 4. What came back

The local-only raw artifact is
`data/results-z3_solve.sh-quant-091526-z3-4.15.4.txt` (see the
[data-retention policy](../../reports/data/README.md)). The comparison below uses
[`gap`](../../reports/gap); the old row is the five-option run from the 2026-09-14
baseline.

| z3 4.15.4 options | solved | unknown | timeout | time on solved (s) | PAR2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| five-option baseline | **6014** | 31 | 79 | 3528.3 | **10128.3** |
| full current Verus set | 5785 | **310** | **29** | **3073.7** | 23413.7 |

The full configuration newly solves 80 benchmarks (64 old timeouts and 16
old unknowns), but loses 309 old solves (293 become unknown and 16 time out).
Among benchmarks both solve, the new run is at least 2× faster on 479 and at
least 2× slower on 351. There are no `sat` answers or disagreements.

With the fresh cvc5 `--no-cbqi --user-pat=strict` run, the corrected gap is
PAR2 ratio **1.88**, gap set **1122**: 587 cvc5-unsolved where z3 solves and
535 both-solved cases at least 10× slower in cvc5. With explicit CaDiCaL,
the best measured cvc5 configuration is ratio **1.75**, gap **1073**: 534
unsolved and 539 solved-but-slow.

## 5. What it settled

The project now measures z3 as current Verus configures it. The four omitted
options were not a harmless transcription detail: together they cut z3
timeouts by 50 but add 279 unknowns and more than double PAR2. Consequently
the corrected cvc5/z3 PAR2 ratio is much smaller than the original 4.34 even
though cvc5 itself did not close that much of the gap. Future headline
numbers use this full option list and state the unknown count.

## 6. What it did not settle

The run changes four options at once, so it does not identify which causes
the 293 solved-to-unknown transitions. It also shows that “z3 as Verus runs
it” is not the strongest z3 oracle on this corpus; it is the fixed comparison
chosen by the charter.
