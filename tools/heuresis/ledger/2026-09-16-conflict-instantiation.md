# 2026-09-16 — conflict-instantiation modes and statistics

**Goal 3, R6/R28.** Measure current conflict-based quantifier instantiation
before defining the distinct eager conflict/unit design.

## 1. What was asked

Add eager conflict-based instantiation as a research direction and run the
closest mainline controls. Compare conflict-only and propagation/equality QCF
with the fixed no-QCF control, then measure how much work and how many useful
instances the conflict-only engine actually produces.

## 2. What was run

The fresh no-QCF control is the first arm in
[`2026-09-16-datatype-and-equality-controls.md`](2026-09-16-datatype-and-equality-controls.md).
The new launch records are:

```
# 2026-09-16 10:08 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-cbqi-conflict.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091626-u-sc-cbqi-conflict -q --user-pat=strict --sat-solver=cadical --cbqi-mode=conflict
# cvc5: git 5cc03f4b9 on branch main

# 2026-09-16 10:39 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-cbqi-prop-eq.conf)
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh quant-091626-u-sc-cbqi-prop-eq -q --user-pat=strict --sat-solver=cadical --cbqi-mode=prop-eq
# cvc5: git 5cc03f4b9 on branch main

# 2026-09-16 11:10 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-cbqi-conflict-stats.conf)
stats_dir_rec_par_cvc5 -t 30 cvc5 quant-091626-u-sc-cbqi-conflict-stats-stats -q --user-pat=strict --sat-solver=cadical --cbqi-mode=conflict
# cvc5: git 5cc03f4b9 on branch main
```

Driver wall times were 455 s, 457 s, and 456 s respectively. Jobs within each
queue ran sequentially.

## 3. The set

`quant-07-25`, **6124 benchmarks**, 30 s each. Every arm and the statistics
run read all 6124. The statistics subsection also uses the 1115-benchmark
conflict-only gap in
[`data/gapset-u-sc-cbqi-conflict-vs-z3-full-091626.txt`](data/gapset-u-sc-cbqi-conflict-vs-z3-full-091626.txt).

## 4. What came back

Solve-result files in [`data/`](data/), read by [`gap`](../gap):

| arm | solved | unknown | timeout | time on solved (s) | PAR2 | change from control |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| no-QCF control | **5548** | 5 | **571** | **6575.4** | **41135.4** | — |
| `--cbqi-mode=conflict` | 5545 | 5 | 574 | 6845.7 | 41585.6 | +1.09% |
| `--cbqi-mode=prop-eq` | 5543 | 5 | 576 | 6832.2 | 41692.2 | +1.35% |

Paired with the control:

| arm | uniquely solves | control uniquely solves | at least 2× faster, both solved | at least 2× slower, both solved |
| --- | ---: | ---: | ---: | ---: |
| conflict | 2 | 5 | 0 | 0 |
| propagation/equality | 1 | 6 | 0 | 0 |

Against corrected z3, conflict mode has PAR2 ratio / gap size 1.78 / 1115;
propagation/equality is 1.78 / 1122, compared with 1.76 / 1071 for no QCF.
No arm produced `sat` or a sat/unsat disagreement.

The raw statistics file is
[`data/stats-cvc5-quant-091626-u-sc-cbqi-conflict-stats-stats.txt`](data/stats-cvc5-quant-091626-u-sc-cbqi-conflict-stats-stats.txt).
It contains 6124 benchmark blocks. Timer units were normalized to seconds,
absent counters were zero, and `QUANTIFIERS_INST_CBQI_CONFLICT` was read from
the map-valued `theory::quantifiers::inferencesLemma` statistic.

| scope | total cvc5 time (s) | QCF time (s) | share of total | QCF rounds | cases with rounds | QCF conflict lemmas | cases with lemmas |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all 6124 | 24285.8 | 58.9 | **0.243%** | 272280 | 4595 | **54** | **49** |
| 1115 QCF gap | 20678.8 | 49.3 | **0.238%** | 197801 | 1114 | **9** | **7** |

Across all cases, QCF time is 0.634% of the quantifiers-engine timer. The
round count has median 7, p90 134, and maximum 1827 over all 6124; on the QCF
gap it has median 128, p90 353, and maximum 869. No benchmark emits more than
three QCF conflict lemmas. The raw driver's five-line processed proof-summary
file is tracked for provenance but contains no additional data.

## 5. What it settled

R6's global policy is settled more strongly for this corpus: both available
QCF modes lose solves and worsen PAR2, while current conflict-only QCF spends
little directly and almost never finds an instance. It emits roughly one
conflict lemma per 5,042 rounds overall, and only one per 21,978 rounds on its
z3 gap. This does not justify rebasing
[`ajreynol:ai-cbqi-0423`](https://github.com/ajreynol/cvc5/tree/ai-cbqi-0423)
merely to optimize current structural QCF.

For R28, the negative control narrows rather than rejects the hypothesis. A
useful eager design should not invoke today's structural conflict finder more
often. It should reuse an incremental E-matching candidate stream, test each
candidate against the current assignment, and promote only conflict or unit
instances. That is the material distinction between R28 and R6.

## 6. What it did not settle

No arm implemented eager candidate discovery or unit promotion, and the QCF
timer excludes downstream search-path effects of the few emitted lemmas. The
direct historical prototype
[`ajreynol:eagerCbqi`](https://github.com/ajreynol/cvc5/tree/eagerCbqi) is 204
commits ahead / 1265 behind current main and conflicts on its first replayed
commit, so it should be mined rather than rebased wholesale. A practical next
test is the cleanly rebasing, five-commit
[`ajreynol:claude-eagerInst`](https://github.com/ajreynol/cvc5/tree/claude-eagerInst)
as a bounded eager-matching substrate, with conflict/unit acceptance and the
counters above added narrowly. Current main must be the comparator.
