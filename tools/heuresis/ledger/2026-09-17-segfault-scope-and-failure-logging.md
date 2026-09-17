# 2026-09-17 — how far the segfault reaches, and a 300 s look at the rescues

**S11, S12.** Make a failed benchmark say why it failed, then use that to size
the [segfault](2026-09-17-central-ieval-segfault.md).

## 1. What was asked

The segfault entry could not say how many benchmarks are affected: two were
found incidentally in a 120 s run, every 30 s run reports zero, and the fault
needs roughly 20 s of CPU to reach, so nothing had looked properly. Two things
were missing — a way to see *why* a benchmark failed without an ssh
investigation, and a run long enough for the question to mean anything.

## 2. What was run

**S11, first.** The wrappers in
[`job_launcher/host/`](../../../job_launcher/host/) now append the first line
of unexpected output to `~/analysis/data/errors-<script>-<name>.txt`. The
result token is deliberately unchanged: [`gap`](../gap) has a fixed column list
(`solved`, `sat`, `unsat`, `unknown`, `timeout`, `error`), so a token such as
`error-segfault` would be counted in no column at all and the benchmark would
quietly leave the accounting. The token stays `error`; the reason goes beside
it. `job_launcher/fetch` copies the file when it is non-empty.

**S12.** The best-known configuration — which is the crashing one — at a
**300 s** timeout, ten times the standard budget:

```
# quant-091726-u-ssc-best-t300
-q --no-cbqi --user-pat=strict --sat-solver=cadical --ee-mode=central --ieval=off
```

on `master@67954d09dc`. Before either, the rewritten launcher was sanity-tested
by rerunning the z3 reference and a statistics job; the z3 rerun reproduced
[`2026-09-15`](2026-09-15-z3-full-verus-options.md) exactly — 5785 solved, 310
unknown, 29 timeout, zero benchmarks differing in either direction, PAR2 within
0.08% — which is recorded here because every ratio in
[`progress.md`](../docs/progress.md) divides by that number.

## 3. The set

`quant-07-25`, **6124 benchmarks**, 300 s each, all read.

## 4. What came back

| | count |
| --- | ---: |
| solved | 5815 |
| unknown | 28 |
| **error (segfault)** | **2** |
| timeout | 279 |

The failure log contains exactly two lines, and says what the previous entry
needed an ssh session to discover:

```
…verusatmosphere/allocator__page_allocator_spec_impl.18.smt2	cvc5 suffered a segfault.
…v_ironfleet/unsolvable/single_delivery_model_v.5.smt2	cvc5 suffered a segfault.
```

They are the same two benchmarks found at 120 s.

**The 12 surviving eager rescues, re-examined at 300 s** (from
[`counters-and-timeout`](2026-09-16-eager-counters-and-timeout-sensitivity.md)):

| | count |
| --- | ---: |
| now solved by the control at 300 s (at 116 s and 198 s) | 2 |
| still not solved | **10** |
| — of which the control answers `unknown` | **7** |
| — of which the control still times out | 3 |

## 5. What it settled

**The segfault is narrow.** Two crashes among the **5845** benchmarks that
reached a terminal answer, at ten times the standard timeout, and the same two
as before. It is a real defect but not a widespread one, and the upstream
report can now say so instead of leaving the scope open.

**Failure is visible now.** The previous entry needed an ad-hoc ssh session to
learn the word "segfault", because the wrapper mapped any unexpected output to
a bare token and discarded the message. A crash now arrives with its reason
attached, which is what the monitor role in
[`progress.md`](../docs/progress.md) requires in order to mean anything.

**The eager rescue count is 10, not 12, and its character is now clear.**
Successive timeouts have eroded it — 29 at 30 s, 12 at 120 s, 10 at 300 s —
but the erosion has only ever removed benchmarks the control eventually
*solves*. The **7** on which the control returns `unknown` have not moved at
any timeout, and cannot: the control terminates and declines to answer, while
`--eager-inst` proves `unsat`. No longer budget fixes that. Those 7 are a
difference in what cvc5 can prove, not in how fast, and they are the durable
part of the finding.

## 6. What it did not settle

**The crash count is a floor, not a total.** 279 benchmarks still hit the
timeout at 300 s and never reached a terminal answer, so the honest statement
is 2 among the 5845 that finished. A longer run could find more, and the set
has only ever been examined in this one configuration.

The three remaining timeout-based rescues may erode further at a longer budget,
on the same argument that removed 17 and then 2. Only the 7 `unknown` cases are
safe from it.

Nothing here explains *why* the control answers `unknown` on those 7 — whether
one incompleteness is responsible or several — which is what S9 asks.
