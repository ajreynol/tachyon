# heuresis — progress

**The measuring stick.** One table, kept over time, that says whether cvc5 is
getting better or worse on this set. Everything else in this project —
[`directions.md`](directions.md), [`todo.md`](todo.md), the
[ledger](ledger) — exists to move a number in this file. If a piece of
work does not eventually show up here, it did not count.

**What it is a history of:** cvc5 `main` revisions. A row is one revision of
upstream cvc5 measured in fixed configurations on a fixed set. The
configurations, the set, the timeout and the host protocol are held constant so
that the *only* thing varying between rows is cvc5 itself.

**The goal.** Produce pull requests to cvc5 `main` that move the tracked
configurations down this table. A branch that wins in a one-off A/B has not
achieved anything here; the number only moves when the change is in upstream
main and a later row measures it. That is the bar this project sets itself.

**It is also a monitor.** The same table catches the opposite case: work
elsewhere in cvc5, unrelated to this project, that makes these benchmarks
worse. A regression found here is worth reporting upstream whether or not this
project caused it, and whether or not anyone here intends to fix it. Check
semi-frequently — a new row costs two runs and about fifteen minutes.

**Every number here comes from a [ledger](ledger) entry**, named in the row.
A figure that is not in the ledger does not belong in this file. Nothing here
is a claim about cvc5 in general; it is a claim about this set, at this
timeout, on one host.

## The protocol

Held fixed across every row. Changing any of it starts a new table, it does
not add a row to this one.

| | |
| --- | --- |
| set | `quant-07-25`, **6124 benchmarks**, Verus-derived; see [`README.md`](../README.md), "The set" |
| timeout | 30 s wall |
| host | the execution host, run idle, one job at a time, never overlapping |
| reading | [`gap`](../reports/gap) with its defaults: factor 10, floor 1 s |
| PAR2 | time if solved, else 2 × timeout, summed over all 6124 |
| ratio | PAR2(cvc5) / PAR2(z3 reference) — **lower is better, 1.00 is parity** |
| gap set | benchmarks where cvc5 is unsolved and z3 solved, or both solved and cvc5 is ≥10× slower |

## The tracked configurations

| name | options | what it is |
| --- | --- | --- |
| **default** | `-q` | cvc5 out of the box. The floor. |
| **verus** | `-q --no-cbqi --user-pat=strict --sat-solver=cadical` | cvc5 asked to behave the way Verus asks z3 to behave — no conflict-based instantiation, strict user patterns — plus the SAT solver named explicitly. |
| **best** | verus + `--ee-mode=central --ieval=off` | the strongest measured configuration. **This is the number to beat.** |

`best` is a configuration, not a default: it is what cvc5 *can* do on this set
today, reachable only by passing options. Moving `best` down is progress;
moving its options into cvc5's own defaults is a separate question this table
does not address.

> ⚠️ **`best` segfaults.** `--ee-mode=central` and `--ieval=off` together crash
> cvc5 on at least 2 of the 6124 benchmarks, deterministically, on current main
> and on every earlier main tested
> ([2026-09-17](ledger/2026-09-17-central-ieval-segfault.md)). Either flag
> alone is fine. The PAR2 effect is nil — both benchmarks are unsolved in every
> arm regardless — so the history below is unaffected, but **this is not a
> configuration to recommend to anyone** until the crash is fixed. A 300 s sweep
> puts the count at exactly two among the 5845 benchmarks that reach a terminal
> answer — rare, but a floor rather than a total, since 279 still time out
> ([2026-09-17](ledger/2026-09-17-segfault-scope-and-failure-logging.md)).

## The targets — z3

These do not move with cvc5 and are not part of the history. They are what we
are measuring against.

| z3 | options | solved | unknown | timeout | PAR2 | ledger |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| **4.15.4** | **full current Verus set (nine options)** | 5785 | 310 | 29 | **23413.7** | [2026-09-15](ledger/2026-09-15-z3-full-verus-options.md) |
| 4.15.4 | five-option subset | 6014 | 31 | 79 | 10128.3 | [2026-09-14](ledger/2026-09-14-baseline.md) |
| 4.8.17 | five-option subset | 5966 | 28 | 130 | 13466 | [2026-09-14](ledger/2026-09-14-baseline.md) |

**The first row is the reference**, because it is what Verus actually runs. Note
that it is the *worse* of the two 4.15.4 rows by PAR2: the full option set makes
z3 answer `unknown` on 310 benchmarks it otherwise solves. Comparing against
the five-option row instead would flatter z3 and is not the honest comparison;
comparing against a z3 configuration nobody runs would flatter cvc5. Ratios in
the history below are all against **23413.7**.

## The history

One row per cvc5 `main` revision, per configuration. Newest last.

| date | cvc5 `main` | config | solved | timeout | PAR2 | ratio | gap | Δ PAR2 | ledger |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2026-09-14 | `5cc03f4b9` | default | 5418 | 702 | 53390 | 2.28 | 2266 | — | [baseline](ledger/2026-09-14-baseline.md) |
| 2026-09-15 | `5cc03f4b9` | default | 5414 | 706 | 53479 | 2.28 | — | +0.17% | [quantifier-controls](ledger/2026-09-15-quantifier-controls.md) |
| 2026-09-15 | `5cc03f4b9` | verus | 5550 | 569 | 41056.3 | 1.75 | 1073 | — | [sat-and-instance-order](ledger/2026-09-15-sat-and-instance-order.md) |
| 2026-09-16 | `5cc03f4b9` | verus | 5548 | 571 | 41135.4 | 1.76 | — | +0.19% | [combined](ledger/2026-09-16-combined-central-equality-and-evaluator-off.md) |
| 2026-09-16 | `5cc03f4b9` | **best** | 5625 | 473 | **35619.5** | **1.52** | 789 | — | [combined](ledger/2026-09-16-combined-central-equality-and-evaluator-off.md) |
| 2026-09-16 | `d7d03b082c` | verus | 5546 | 573 | 41207.7 | 1.76 | — | +0.37% | [rebased-branches](ledger/2026-09-16-rebased-equality-and-evaluator-branches.md) |
| 2026-09-16 | `d7d03b082c` | **best** | 5623 | 474 | **35600.5** | **1.52** | 796 | −0.05% | [rebased-branches](ledger/2026-09-16-rebased-equality-and-evaluator-branches.md) |
| 2026-09-16 | `95050cf8155d` | **best** | 5624 | 473 | **35557.3** | **1.52** | 789 | −0.12% | [bounded-eager](ledger/2026-09-16-bounded-eager-instantiation.md) † |
| 2026-09-17 | `67954d09dc` | verus | 5548 | 571 | 41142.2 | 1.76 | 1073 | −0.16% | [self-contained](ledger/2026-09-17-self-contained-launcher-and-current-main.md) |
| 2026-09-17 | `67954d09dc` | **best** | 5626 | 471 | **35532.7** | **1.52** | **784** | −0.07% | [self-contained](ledger/2026-09-17-self-contained-launcher-and-current-main.md) |
| 2026-09-17 | `a07d513075` ‡ | verus | 5545 | 574 | 41191.8 | 1.76 | 1079 | +0.12% | [1.4.0](ledger/2026-09-17-cvc5-1-4-0-release.md) |
| 2026-09-17 | `a07d513075` ‡ | **best** | 5624 | 473 | **35580.3** | **1.52** | 786 | +0.13% | [1.4.0](ledger/2026-09-17-cvc5-1-4-0-release.md) |

† measured on `claude-eagerInst@995b23bcfa` with its module off, which is 0
behind `95050cf8155d`. Compared against the `best` row at `d7d03b082c` it
differs by 2 solves, 0.12% PAR2, and **zero** benchmarks ≥2× faster or slower
in either direction — so the branch's non-module changes and the one commit
main advanced are, together, inside the noise band. It stood in for a main
build, and the direct `67954d09dc` measurement below has since confirmed it:
35532.7 against the proxy's 35557.3, a 0.07% difference. No further proxy rows
should be needed.

‡ **the cvc5 1.4.0 release.** `a07d513075` is "Start post-release for 1.4.0"
and reports `1.4.1.dev`; the `cvc5-1.4.0` tag is `b432cd77eb`, one commit
earlier, and the two differ only in `cmake/version-base.cmake` with no changes
under `src/`. The whole diff from the previous row, `67954d09dc`, is that one
`cmake` line — so these two rows were expected to reproduce the ones above
them, and do.

Δ PAR2 is against the previous row for that configuration; lower is better.

### What the history says so far

**cvc5 main has not moved this number, up to and including the 1.4.0
release.** Across five revisions from `5cc03f4b9` to `a07d513075`, five
`verus` measurements span 0.37% (41056.3–41207.7) and five `best` measurements
span 0.24% (35532.7–35619.5). Every one is inside the noise band below.
Nothing upstream in that window helped these benchmarks, and nothing hurt them
either — which is the monitor doing its job, reporting no change rather than
nothing.

This is weaker than it looks, and the weakness is worth stating: only five
revisions have been measured, not every commit between them. A regression that
appeared and was fixed inside one of those windows would be invisible here.
What the table supports is that the *endpoints* are flat, including across a
release.

**Every gain so far is configuration, not code.** default → verus is −23%,
verus → best is −13%, and both come from passing options that already exist.
This project has not yet changed a line of cvc5. **Zero PRs have been opened;
zero rows have been moved by our work.** That is the honest state, and it is
what the table exists to make unavoidable.

## Noise

The table contains two pairs of repeat measurements of an unchanged binary and
configuration: `default` at `5cc03f4b9` (+0.17%) and `verus` at `5cc03f4b9`
(+0.19%). Run-to-run variation on this host is therefore around **±0.2% PAR2**,
and the largest movement anywhere in the history is 0.37%.

So, as a working rule: **a PAR2 change under about 0.5% is noise.** A change
that matters here is a percent or more. Two solves either way is noise; the
gap-set count drifts ±7 between identical configurations.

The five-measurement spreads above — 0.37% for `verus`, 0.24% for `best`,
across revisions, a release, *and* a rewrite of the launcher — are consistent
with this and have not widened as points accumulated.

The rule is calibrated on repeats of unchanged configurations, not on a
controlled noise study, and it does not license reading a 0.6% change as real
without a repeat.

## Adding a row

1. Run the tracked configuration on the current set at 30 s, on an idle host.
   Configs for `verus` and `best` are in
   [`job_launcher/configs/`](../../../job_launcher/configs).
2. Read it with [`gap`](../reports/gap) against the z3 reference above.
3. Write the ledger entry first. The row here cites it; it is not the record.
4. Add the row, with the exact cvc5 `main` revision — not "current main".
5. If Δ PAR2 exceeds the noise band, say so in the entry and in the summary
   above, in whichever direction it went.

**When a row gets worse.** Bisect upstream to the commit, confirm it
reproduces, and report it to cvc5 with the benchmark and the two revisions.
Do this whether or not the cause is related to anything this project is
working on — that is what makes the table a monitor rather than a scoreboard.

## Pull requests to cvc5 main

The record of what this project has actually landed. A branch that passes
regressions and wins an A/B is not an entry here; a merged commit is. What
might become an entry is a [proposal](directions.md#proposals), held in the
table of the one research direction that owns it.

| PR | direction | what it changes | landed | effect on this table |
| --- | --- | --- | --- | --- |
| *(none yet)* | | | | |

**Ready to file now:** the `--ee-mode=central --ieval=off` segfault
([2026-09-17](ledger/2026-09-17-central-ieval-segfault.md)) — a
reproducible crash on current main with a backtrace and a two-flag bisection.
Not a performance change, so it will not move a row, but it is the first
upstream-reportable defect this project has produced.

**Standing candidates**, from the ledger, none yet proposed upstream. The
[proposals tables](directions.md#proposals) now name sixty-five branches
across twenty-five of the twenty-seven directions, but every candidate below is an **option**
proposal or a change no branch yet implements, so none of them is in a table
yet — and the eager pair budget would go under one of R1 or R28, not both:

- **A cumulative eager pair budget** (R1/R28, short-term goal S8). The strongest
  candidate: rescues and slowdowns separate cleanly on cumulative pairs
  processed, and no option expresses that axis
  ([evidence](ledger/2026-09-16-eager-counters-and-timeout-sensitivity.md)).
  Untested — the cap is fitted in-sample on twelve benchmarks.
- **`--ee-mode=central` as a default for this workload** (R15). It is 10.3% of
  PAR2 and is already in `best`, but a default change needs cross-corpus and
  correctness-policy evidence this project has not gathered.
- Two branches were tested and explicitly **did not** earn a PR:
  [`ai-eecNoShare`](https://github.com/ajreynol/cvc5/tree/ai-eecNoShare)
  (within noise) and
  [`ievalTravTrie`](https://github.com/ajreynol/cvc5/tree/ievalTravTrie)
  (neutral, and worse than evaluator-off)
  ([evidence](ledger/2026-09-16-rebased-equality-and-evaluator-branches.md)).
