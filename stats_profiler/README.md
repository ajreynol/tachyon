# cvc5 timing profiler

Explore how much of a job's measured solver time is covered by a configurable
set of `--stats-internal` timers. Produces a standalone interactive HTML report,
plus `benchmarks.csv` and `summary.json`. Requires Python 3.9+; no dependencies,
server, or network access. Open the HTML directly in a browser.

```bash
python3 stats_profiler/profile.py /path/to/stats-job.txt --output scratch/profile
python3 stats_profiler/profile.py /path/to/stats-job.txt --list-timers
python3 stats_profiler/profile.py /path/to/stats-job.txt \
  --config my-timers.json --benchmarks /path/to/benchmark-list.txt \
  --output scratch/profile-subset
```

Use the **raw** `stats-*.txt` produced by the launcher's
`stats_dir_rec_par_cvc5` driver, not its `-processed` proof summary. Each block
starts with a benchmark path ending in `.smt2` (or `.smt2.gz`), followed by
solver output and `key = value` statistics. A single benchmark's output can
be used by prepending its path. The input must have grouped, non-interleaved
benchmark blocks, as the driver emits. No remote job is launched or fetched.

The report includes:

- Time-weighted aggregate category shares, uncovered gaps, and over-counting.
- A coverage histogram and per-category empirical cumulative distributions,
  with seconds / per-run percentage switching and median, p90, and p99 values.
- Path and result filters, category toggles, additional observed timers,
  configurable total timer, and missing-data policy.
- Sortable, paginated benchmark details, including incomplete runs.
- A configuration download to reproduce the selected categories with the CLI.

## Choosing a partition

[`default.json`](default.json) is a starting hypothesis: process assertions,
theory checks, and theory combination. It is **not a certified disjoint or
complete partition**. The report makes its uncovered portion explicit. Timer
names and scopes vary with the solver revision. Use `--list-timers` to inspect
the keys, presence counts, and aggregate seconds actually observed in your job.

Each category adds the union of names/globs in `add` and subtracts the union
in `subtract`. Globs use case-sensitive shell-style matching, with `*` matching
across `::`. Matching a key twice in one list counts it once. For example, to
split a measured quantifier timer into E-matching and the remaining time:

```json
{
  "total": "global::totalTime",
  "missing": "zero",
  "categories": [
    {
      "name": "E-matching",
      "add": ["theory::QuantifiersEngine::time_ematching"]
    },
    {
      "name": "Other quantifier work",
      "add": ["theory::QuantifiersEngine::time"],
      "subtract": ["theory::QuantifiersEngine::time_ematching"]
    },
    {
      "name": "Arithmetic checks",
      "add": ["theory::arith::checkTime"]
    }
  ]
}
```

Use subtraction only after verifying the child is contained in the parent in
the solver version under study. Adding both inclusive parents and children
double-counts work. A 100% sum alone cannot establish that the chosen timers
form a partition. The tool cannot infer nesting from names. Negative category
values remain visible and are flagged rather than clipped; this helps expose
invalid subtraction, missing parents, and timer rounding.

Unmatched patterns are reported. An absent literal remains a required term
for missing-data checks; an unmatched wildcard has no discoverable required
keys. Glob expansion is against all selected input runs, before browser filters.
Saved browser configurations use expanded exact names for reproducibility.
Browser changes do not rewrite the original CSV or JSON; rerun with the saved
configuration to regenerate them. Output files in the chosen directory are
replaced on each run.

## Accounting and missing data

All timing values must carry units (`ns`, `us`, `µs`, `μs`, `ms`, `s`, `min`,
or `h`); numeric counters and histograms are ignored. Units are converted to
seconds. The default denominator is cvc5's `global::totalTime`, **not** the
wrapper's user CPU seconds or the wall time of the parallel job. No fallback
mixes these different measurements.

For each included benchmark, with total `T` and sum of categories `A`:

| Measure | Definition |
| --- | --- |
| Coverage | `A / T` |
| Net residual | `T - A` (signed) |
| Uncovered gap | `max(T - A, 0)` |
| Over-counted excess | `max(A - T, 0)` |

Aggregate coverage is `sum(A) / sum(T)`, not the average of per-run percentages.
Aggregate gaps and excesses sum the corresponding per-run amounts separately,
so a gap on one benchmark cannot disappear behind overlap on another.
Distributions weight benchmarks equally; percentiles use linear interpolation.
Chart drawing samples at most roughly 400 ranks per curve; calculations use
every included run.

Missing or zero totals are excluded from all aggregates and distributions and
retained in benchmark details and exports. By default missing category timers
contribute zero, with missing counts shown: omitted zero statistics are common,
but truncated output can look the same. Set `"missing": "exclude"` to exclude
any run lacking any category term. Neither policy can reconstruct missing data.
An unreported result remains `unreported`; only explicit interruption/timeout
text marks a timeout. Result status does not otherwise determine inclusion.

Repeated benchmark paths are retained as separate runs and reported. Repeated
timer keys within a block use the last printed snapshot and emit diagnostics;
they are not summed. This is suitable for cumulative snapshots, not a sum of
independent solver sessions without benchmark delimiters. Precision is limited
by the printed timer units; small excesses can reflect rounding.

Reports embed benchmark names and timings. They are local artifacts; inspect
them before sharing. Default output is ignored at `stats_profiler/output/`.

## Checks

```bash
python3 -m unittest discover -s stats_profiler/tests -v
job_launcher/checks
```
