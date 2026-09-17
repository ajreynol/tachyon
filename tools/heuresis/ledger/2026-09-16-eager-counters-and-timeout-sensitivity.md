# 2026-09-16 — eager-instantiation counters, and the rescues at a longer timeout

**Goal 3, R1/R28/R2 (S2, S6, S7).** Give the preceding entry's loss and its 29
rescues a mechanism, and test whether the rescues are an artifact of the 30 s
cutoff.

## 1. What was asked

[`2026-09-16-bounded-eager-instantiation.md`](2026-09-16-bounded-eager-instantiation.md)
left two questions open in its section 6: no counters were collected, so
neither the 19.46% PAR2 loss nor the 29 rescues had a mechanism; and 29 of 6124
is close enough to the timeout boundary to be an artifact. This entry answers
both, and asks whether anything cheap separates the rescues from the
slowdowns.

## 2. What was run

Five jobs, all on `claude-eagerInst@995b23bcfa`, the branch already built and
regression-checked in the preceding entry. All extend
`-q --no-cbqi --user-pat=strict --sat-solver=cadical --ee-mode=central --ieval=off`:

```
# S2, stats_dir_rec_par_cvc5, 30 s
quant-091626-u-ssc-eager-inst-stats       --eager-inst
quant-091626-u-ssc-eager-inst-rlv-stats   --eager-inst --eager-inst-rlv
# S7, solve_dir_rec_par_cvc5, 120 s
quant-091626-u-ssc-eager-off-t120         (module off -- the control)
quant-091626-u-ssc-eager-inst-t120        --eager-inst
quant-091626-u-ssc-eager-inst-rlv-t120    --eager-inst --eager-inst-rlv
```

The control is included at 120 s on purpose: the question is not only whether
the rescues survive, but whether the control reaches those benchmarks given
four times the budget. Commands and revisions are in
[`job_launcher/log.txt`](../../../job_launcher/log.txt); the five configs are in
[`job_launcher/configs/`](../../../job_launcher/configs/). The drivers glob a
directory tree and take no benchmark list, so S7 could not be restricted to
the gap slice and was run on the whole set.

## 3. The set

`quant-07-25`, **6124 benchmarks**. S2 at 30 s, S7 at 120 s. Every arm read all
6124. The 30 s reference remains the full-Verus-option z3 4.15.4 run of
[`2026-09-15-z3-full-verus-options.md`](2026-09-15-z3-full-verus-options.md).

## 4. What came back

### S7 — the 120 s arms

| arm | solved | unknown | timeout | error | time on solved (s) | PAR2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| module off (control) | **5756** | 28 | **338** | 2 | 13603.8 | **101923.8** |
| `--eager-inst` | 5605 | 58 | 461 | 0 | 11242.8 | 135802.8 |
| `--eager-inst-rlv` | 5681 | 39 | 404 | 0 | 13295.4 | 119615.4 |

The ordering at 30 s is unchanged at 120 s: eager instantiation is still a
clear net loss, and relevancy deferral still recovers about half of it.

**Of the 29 rescues measured at 30 s:**

| | count |
| --- | ---: |
| also solved by the control at 120 s — i.e. merely slow, not unreachable | **17** |
| still unsolved by the control at 120 s | **12** |

The control's times on the 17 run from 30.6 s to 80.5 s, median 37.0 s: they sat
just past the old cutoff. **The headline number was inflated by the boundary,
and 59% of it does not survive.**

The 12 that remain are not marginal. `--eager-inst` solves **all 12** at 120 s,
against a control given four times the budget. Seven of the 12 are
`page_organization__PageOrg` benchmarks; the rest are `linked_list` (2),
`process_manager__container_tree_spec_impl` (2) and
`pagetable__pagetable_spec_impl` (1). On seven of the 12 the control answers
`unknown` rather than timing out, while `--eager-inst` answers `unsat` — a
difference in what is proved, not only in how fast.

Independently of the original 29, at 120 s the control cannot solve 331 gap-set
benchmarks, and an eager arm rescues **26** of them.

### S2 — the counters

Whole-set totals over the benchmarks with any eager activity:

| arm | active | (term, trigger) pairs | matches | match rate | eager instantiations | processTime |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `--eager-inst` | 4803 | 5,706,412,466 | 43,963,612 | **0.77%** | 3,983,309 | 4811.3 s |
| `--eager-inst-rlv` | 4788 | 3,980,139,880 | 40,854,197 | **1.03%** | 1,820,211 | 4737.7 s |

**Fewer than one pair in a hundred yields a match.** That is the mechanism of
the loss: the module processes 5.7 billion pairs to produce 4.0 million
instantiations. Relevancy deferral cuts pairs 30% and lifts the match rate by a
third, which is consistent with it halving the PAR2 damage.

Where eager instantiation is active it dominates instantiation: 64.3% of all
instantiations are eager. `numTermsRematched` never appears, because
`--eager-inst-merge` defaults to false and no term is ever re-matched on a
merge — so **these runs carry no new-versus-rediscovered signal for R2**.

### S6 — what separates the rescues from the slowdowns

Pairs processed, by population, in the `--eager-inst` arm:

| population | min | p50 | p90 | max |
| --- | ---: | ---: | ---: | ---: |
| the 12 hard rescues | 9,999 | 85,552 | 359,797 | **376,456** |
| the 17 boundary rescues | 178 | 1,179,159 | 4,928,060 | 15,368,807 |
| the 91 benchmarks ≥2× slower | 502 | 407,321 | 6,976,649 | 21,971,021 |

**The benchmarks eager instantiation rescues are the ones where it does least
work.** No hard rescue exceeds 376,456 pairs; 52% of the slowdowns do. The
concentration is extreme: **590 of the 4803 active benchmarks — 12% — account
for 4581 s of the 4811 s of eager processing time, 95% of it**, and no rescue
is among them.

A cumulative pair budget, evaluated in-sample:

| cap | hard rescues kept | slowdowns still run | losses cut |
| ---: | ---: | ---: | ---: |
| 250,000 | 10 / 12 | 41 / 91 | 55% |
| **500,000** | **12 / 12** | 50 / 91 | **45%** |
| 1,000,000 | 12 / 12 | 59 / 91 | 35% |
| 5,000,000 | 12 / 12 | 80 / 91 | 12% |

## 5. What it settled

**The rescue count is 12, not 29, and the preceding entry over-claimed.** Most
of that number was the 30 s cutoff. This entry corrects it. What survives is
smaller and stronger: 12 benchmarks that a control with four times the budget
cannot solve and `--eager-inst` solves outright, plus 26 further rescues at the
120 s boundary. On seven of the 12 the control returns `unknown`, so eager
instantiation is changing what cvc5 can prove there, not merely when.

**The loss has a measured mechanism.** A 0.77% match rate over 5.7 billion
pairs is the cost, and it is not spread evenly: an eighth of the active
benchmarks carry 95% of the eager time. The module is not badly paced on
average; it is catastrophically paced on a small minority.

**Rescues and slowdowns separate on work done, and the branch cannot express
the separation.** `--eager-inst-pair-limit` is a *per-round* limit, default
2000; nothing in the branch caps cumulative pairs per benchmark, which is the
axis the two populations differ on. That is a concrete, implementable proposal
for R1/R28: a cumulative eager budget, after which the module stands down and
lazy instantiation proceeds. It is also the first thing in this project that
looks like a design recommendation rather than an observation.

**R2 gained nothing here.** The rematch counter is structurally zero under the
default `--eager-inst-merge=false`, so S2 does not close the
new-versus-rediscovered question, and S3 remains the path to it.

## 6. What it did not settle

**The 500,000 cap is fitted on the twelve points it is evaluated against.** It
is an in-sample threshold on a 12-benchmark population, not a validated policy,
and the table above is a hypothesis generator, not a result. No cumulative-cap
option exists to test, so nothing here has been run; the per-round
`--eager-inst-pair-limit` is a different quantity and lowering it would not
test this.

The counters are whole-benchmark totals. They do not say *when* in a run the
wasted pairs are processed, whether the 95% concentration is a few pathological
quantifiers or a general blow-up, or what the 12 rescued benchmarks have in
common structurally beyond sharing a source family. The 120 s control also
returned two `error` results —
`allocator__page_allocator_spec_impl.18.smt2` at 47.05 s and
`single_delivery_model_v.5.smt2` at 32.63 s — which were not diagnosed and are
excluded from no count deliberately; they appear as neither solved nor timeout.

Whether the 12 survive a third timeout, a rerun, or another corpus is still
untested, and the same boundary argument that removed 17 of the original 29
applies again at 120 s.
