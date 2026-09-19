# 2026-09-17 — current main, on the self-contained launcher

**Measuring stick.** Two tracked configurations at current cvc5 `main`, run as
the first jobs through a launcher that no longer depends on anything outside
this repository.

## 1. What was asked

[`progress.md`](../progress.md) had no row measured on a real `main`
build: its `95050cf8155d` row stood in for one, using the eager branch with its
module off. Replace it with a direct measurement at current main, and in doing
so exercise every path of the rewritten launcher.

## 2. What was run

`job_launcher/` was made self-contained: `submit` and `status` are now part of
this repository rather than a separate checkout, and the scripts that run on
the host — the drivers, the wrappers and `benchmark_binary` — are
[`job_launcher/host/`](../../../../job_launcher/host), installed by
`job_launcher/deploy` to `~/bin/heuresis`. Jobs run with
`PATH=$HOME/bin/heuresis:$HOME/bin:$PATH`, so the driver a job uses is the one
in this repository at the revision that launched it.

These were the first jobs through it:

```
# quant-091726-u-ssc-current
-q --no-cbqi --user-pat=strict --sat-solver=cadical
# quant-091726-u-ssc-current-ee-central-ieval-off
-q --no-cbqi --user-pat=strict --sat-solver=cadical --ee-mode=central --ieval=off
```

The binary was `master@67954d09dc`, equal to current upstream `main`, built
through the rewritten blocking build path — which fast-forwarded `master` from
`cvcm/main`, confirming the host-side conf is read. The commands are in
[`job_launcher/log.txt`](../../../../job_launcher/log.txt); the configs are
`quant-cvc5-current.conf` and `quant-cvc5-current-ee-central-ieval-off.conf`.

Three things changed on the host side and are recorded here because they could
in principle affect a result:

- `getproofstats`, which is not part of this repository, is now optional. When
  absent the raw statistics file is the whole output. It only ever produced the
  222-byte, contentless `-processed.txt` files.
- The wrapper's proof arguments (`-s`, `-e`, `-l`) are passed only when the
  host conf sets them. Both wrappers parse and ignore them, so the solver
  command line is unchanged.
- Nothing else differs. `~/bin/run-dev` was left untouched.

## 3. The set

`quant-07-25`, **6124 benchmarks**, 30 s each, both arms reading all 6124. The
reference is the full-Verus-option z3 4.15.4 run of
[`2026-09-15`](2026-09-15-z3-full-verus-options.md), PAR2 23413.7.

## 4. What came back

| arm | solved | unknown | timeout | time on solved (s) | PAR2 | ratio | gap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `verus` | 5548 | 5 | 571 | 6582.2 | 41142.2 | 1.76 | 1073 |
| `best` | **5626** | 27 | **471** | 5652.7 | **35532.7** | **1.52** | **784** |

Against the previous row for each configuration: `verus` **−0.16%**
(41207.7 at `d7d03b082c`), `best` **−0.07%** (35557.3 at `95050cf8155d`). No
`sat` answers, no disagreements.

## 5. What it settled

**The launcher migration is sound.** Every path was exercised — validation,
remote checks, tmux launch, logging, the blocking build with its upstream
fast-forward, window cleanup and fetch — and both arms reproduce their
configuration's previous value to within a fifth of a percent. Had the rewrite
changed what a job actually runs, these two numbers are where it would show.

**`progress.md` now has a real row at current main.** The `95050cf8155d` proxy
row can be read as confirmed rather than assumed: `best` measured directly on
`67954d09dc` is 35532.7 against the proxy's 35557.3, a 0.07% difference.

**cvc5 `main` still has not moved this number.** Four `verus` measurements
across four revisions span 0.37%, and four `best` measurements span 0.24% —
both within the noise band, and the band itself is unchanged by these runs.

## 6. What it did not settle

These runs say nothing about cvc5 itself beyond confirming the plateau. The
`best` arm is the configuration that
[segfaults](2026-09-17-central-ieval-segfault.md) on at least two benchmarks;
both were unsolved here, as in every previous arm, so the crash does not
disturb the PAR2 comparison, but the number is still measured in a
configuration with a known defect.

The three host-side behaviour changes above were reasoned about rather than
tested in isolation: no arm was run both with and without them. The agreement
of both arms with their predecessors is the evidence, and it is indirect.
