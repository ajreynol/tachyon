# 2026-09-15 — first whole-set attribution statistics

**Goal 2, R26.** Internal cvc5 statistics on the whole set, analysed over the
corrected 1122-benchmark gap of the `--no-cbqi --user-pat=strict` control.

## 1. What was asked

Measure where cvc5 spends time and collect the existing counters needed to
rerank the research directions before building or rebasing instrumentation.

## 2. What was run

```
# 2026-09-15 16:34 [dev1:~/benchmarks/quant-07-25] (quant-cvc5-stats.conf)
stats_dir_rec_par_cvc5 -t 30 cvc5 quant-091526-u-ss-stats -q --no-cbqi --user-pat=strict
# cvc5: git 5cc03f4b9 on branch main
```

The stats job ran after the z3 job in the same queue and finished in 470 s.
It deliberately used the `u-ss` control, not the newly measured explicit
CaDiCaL variant, so it can be paired directly with that control's result
file.

## 3. The set

`quant-07-25`, **6124 benchmarks**, 30 s each. The analysis gap is the 1122
benchmarks in
[`data/gapset-u-ss-vs-z3-full-091526.txt`](data/gapset-u-ss-vs-z3-full-091526.txt),
defined against the corrected nine-option z3 run.

## 4. What came back

The local-only raw artifact
`data/stats-cvc5-quant-091526-u-ss-stats.txt` contains 6124 benchmark blocks
and 186 distinct keys (see the [data-retention policy](data/README.md)). The
driver also emitted a `-processed` file containing only five empty
proof-summary headings; it is tracked for provenance but was not used.

For this entry, every `key = value` statistic was associated with the
preceding benchmark path, timer units were normalized to seconds, absent
counters were treated as zero, and map-valued inference counters were read
by inference ID. Percentages use the sum of `global::totalTime`; cvc5 timers
can be nested, so rows must not be added together.

| timer | all 6124 (s) | share | 1122 gap (s) | gap share |
| --- | ---: | ---: | ---: | ---: |
| total | 25125.8 | 100% | 21615.7 | 100% |
| quantifiers engine | 7719.4 | 30.7% | 6743.9 | 31.2% |
| E-matching | 6797.4 | 27.1% | 6014.9 | **27.8%** |
| arithmetic checks | 2937.2 | 11.7% | 2519.0 | 11.7% |
| UF checks | 2405.7 | 9.6% | 2190.5 | 10.1% |
| datatype checks | 1523.1 | 6.1% | 1400.8 | 6.5% |
| theory combination | 639.5 | 2.5% | 578.0 | 2.7% |
| process assertions | 557.5 | 2.2% | 205.2 | 0.9% |

The 1122 gap benchmarks are 18.3% of the corpus but consume **86.0%** of
measured cvc5 time. Other gap-set counters:

| counter | total | nonzero benchmarks | median | p90 | maximum |
| --- | ---: | ---: | ---: | ---: | ---: |
| instantiations | 3,064,026 | 1121 | 2247 | 5512 | 9217 |
| full instantiation rounds | 31,334 | 1121 | 22 | 54 | 95 |
| SAT clause literals | 29,881,003 | 1122 | 23,567.5 | 49,925 | 193,323 |
| SAT decisions | 69,909,503 | 1122 | 55,280.5 | 135,272 | 240,730 |
| entailed duplicate instances | 247,662 | 985 | 117.5 | 558 | 2438 |
| `DATATYPES_SPLIT` lemmas | 27,484 | 920 | 7 | 79 | 194 |
| DIO conflict calls | 2807 | 283 | 0 | 5 | 82 |
| DIO cut calls | 1962 | 242 | 0 | 3 | 56 |
| external branch-and-bound | 619 | 278 | 0 | 1 | 16 |

Entailed duplicates are 8.1% of total gap-set instantiations. The datatype
row uses the actual `theory::datatypes::inferencesLemma` map; the much larger
`resource::steps::inference-id` value is resource accounting attributed to
that inference ID, not a lemma count.

## 5. What it settled

- **R2 moves up:** E-matching is material, taking 27.8% of gap-set time, so
  adding a new-versus-rediscovered match counter is justified.
- **R1 remains live:** 1121 gap cases instantiate, with median 22 and p90 54
  full rounds. The missing half is a comparable z3 generation-depth measure.
- **R7 is ready for A/B:** 985 gap cases record entailed duplicates, equal to
  8.1% of instances in aggregate.
- **R16 is ready for the cheap mainline test:** 920 gap cases emit 27,484
  datatype-split lemmas, so `--dt-binary-split` precedes any branch rebase.
- **R17 narrows:** DIO and external branch-and-bound counters are nonzero on
  only about one quarter of the gap. Test that slice before rebasing.
- **R9 is plausible but not attributed:** clause-literal and decision counts
  are large, but current stats do not expose persistent clause count or
  whether an instance clause participates in a conflict.
- **R27 is not measured:** `processAssertionsTime` is only 0.9% of gap time,
  but it is not a parse-only timer and cannot answer the parser question.

## 6. What it did not settle

This is aggregate evidence, not the one-row-per-benchmark attribution table,
so the project's attributed fraction remains zero. Current `main` still
lacks the decisive R2 and R9 counters (new versus rediscovered E-matches,
persistent clauses, and conflict use by instance clauses), a comparable z3
depth statistic for R1, and an equality-engine-specific timer for R15. Those
gaps argue for a selective port from `qdebugStats`, not a wholesale rebase.
