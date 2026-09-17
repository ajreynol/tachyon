# cvc5 timing profiler

Explore how much of a job's measured solver time is covered by a configurable
set of `--stats-internal` timers. Produces a standalone interactive HTML report,
plus `benchmarks.csv`, `summary.json`, and — with `--pdf` — vector PDF plots.
Requires Python 3.9+; no dependencies, server, or network access. Open the HTML
directly in a browser. **Start with [the worked example](#the-worked-example)**.

```bash
python3 stats_profiler/profile.py /path/to/stats-job.txt --output scratch/profile
python3 stats_profiler/profile.py /path/to/stats-job.txt --list-timers
python3 stats_profiler/profile.py /path/to/stats-job.txt \
  --config my-timers.json --benchmarks /path/to/benchmark-list.txt \
  --output scratch/profile-subset
python3 stats_profiler/profile.py /path/to/stats-job.txt \
  --config stats_profiler/quant-07-25.json --output scratch/profile --pdf
```

Use the **raw** `stats-*.txt` produced by the launcher's
`stats_dir_rec_par_cvc5` driver, not its `-processed` proof summary. Each block
starts with a benchmark path ending in `.smt2` (or `.smt2.gz`), followed by
solver output and `key = value` statistics. A single benchmark's output can
be used by prepending its path. The input must have grouped, non-interleaved
benchmark blocks, as the driver emits. `profile.py` only ever reads a local
file; launching a job and copying its output back is the launcher's half of
[the worked example](#the-worked-example).

The report includes:

- Time-weighted aggregate category shares, uncovered gaps, and over-counting.
- A coverage histogram and per-category empirical cumulative distributions,
  with seconds / per-run percentage switching and median, p90, and p99 values.
- Path and result filters, category toggles, additional observed timers,
  configurable total timer, and missing-data policy.
- Sortable, paginated benchmark details, including incomplete runs.
- A configuration download to reproduce the selected categories with the CLI.

## The worked example

[`quant-07-25.json`](../stats_profiler/quant-07-25.json) is the example configuration: eight named
cvc5 timers against `global::totalTime`, with everything else left over as misc.
It is a **list of timers, not a claim about them**; read
[Choosing a partition](#choosing-a-partition) before treating the slices as a
decomposition.

| | |
| --- | --- |
| set | `$QUANT_DIR` (`quant-07-25`), on the host `DEFAULT_HOST` names in `job_launcher/site.conf` |
| job | [`quant-cvc5-stats.conf`](../job_launcher/configs/quant-cvc5-stats.conf), driver `stats_dir_rec_par_cvc5`, 30 s per benchmark |
| timers | `TheoryEngine::combineTheoriesTime`, `theory::uf::checkTime`, `theory::datatypes::checkTime`, `prop::CnfStream::cnfConversionTime`, `theory::QuantifiersEngine::time_ematching`, `theory::arith::checkTime`, `smt::SolverEngine::processAssertionsTime`, `JustifyStrategy::getNextTime` |
| total | `global::totalTime`; misc is whatever none of the eight account for |

Everything machine-specific — which host, where the set is — stays in
`job_launcher/site.conf`, so the commands below are the same for anyone who has
copied [`site.conf.example`](../job_launcher/site.conf.example) and edited it once.

```bash
# 1. run the stats job on the host.  It queues in a tmux window there and
#    writes ~/analysis/stats/stats-cvc5-quant-<MMDDYY>-u-ssc-stats.txt.
job_launcher/submit -n quant-cvc5-stats.conf        # dry run first: prints the name
job_launcher/submit    quant-cvc5-stats.conf
job_launcher/status                             # finished windows remain open; close with submit -k NAME

# 2. copy the raw stats file back (read-only on the host).  An earlier stats
#    job can be fetched by name without launching anything.
job_launcher/fetch -d scratch/stats 'quant-<MMDDYY>-u-ssc-stats'

# 3. profile it and write the PDFs.
python3 stats_profiler/profile.py \
  'scratch/stats/stats-cvc5-quant-<MMDDYY>-u-ssc-stats.txt' \
  --config stats_profiler/quant-07-25.json \
  --output scratch/profile-quant-07-25 --pdf
```

Replace `<MMDDYY>` with the name printed by the dry run. Step 3 prints the
HTML and PDF paths and the aggregate summary. CSV and JSON are also written.
Drop `--pdf` for HTML, CSV and JSON alone. To replot without
reparsing 30 MB of stats — a different axis, say — run the plotter on its own:

```bash
python3 stats_profiler/plots.py scratch/profile-quant-07-25/summary.json --max-share 60
```

The recorded example uses `quant-091526-u-ss-stats`
([log](../job_launcher/log.txt),
[ledger](../tools/heuresis/ledger/2026-09-15-attribution-stats.md)), without
explicit CaDiCaL. The tracked config selects CaDiCaL and a fresh submit measures
`u-ssc`; the two runs are not interchangeable.

## The plots

`--pdf` writes vector PDFs beside the HTML, each page 720x450 pt, drawn with
base-14 fonts and no embedded resources:

| file | what it shows |
| --- | --- |
| `cdf-<n>-<timer>.pdf` | one timer's distribution over benchmarks |
| `cdf-all.pdf` | all selected categories on one axis |
| `pie-total.pdf` | cumulative seconds per timer, plus misc, with the table beside it |
| `plots.pdf` | every page above, in order |

A CDF page is an **empirical survival curve**, not a cumulative one: a point
`(x, y)` reads *for y% of the benchmarks this timer was at least x% of
the selected total timer*. The default is `global::totalTime`; labels follow
the configuration. The x-axis is the same 0-100% on every page,
`--max-share` narrows it to a value in `(0, 100]`, and shares outside the axis,
including negative values, are clipped and counted in the footer. Median and p90 are marked on
the curve. The thin vertical rule is that timer's **cumulative** share — its
slice of the pie — which is a different quantity: the pie weights a benchmark by
its seconds, the curve weights every benchmark equally. A timer can be a small
slice and still dominate most runs, or the reverse; that divergence is the point
of having both.

The pie is part-to-whole over included runs only, and its misc slice is the
signed residual `total - sum(timers)` in aggregate. If the timers
over-count the total there is no misc slice, the chart says so, and the negative
share stays visible in the table rather than being clipped away.
If a category's aggregate is negative, no pie is drawn: the signed table
remains, since negative slices cannot represent parts of a whole.

Each category keeps one colour across every PDF page, in the fixed order of a
palette; misc is grey because it is a
residual and not a category. That ordering is why the plotter refuses more than
eight categories instead of inventing a ninth colour — combine categories, or
plot a subset.

## Choosing a partition

[`default.json`](../stats_profiler/default.json) is a starting hypothesis: process assertions,
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
python3 scripts/check.py
```

The PDF writer is checked structurally — object offsets, the cross-reference
table, stream lengths, escaping, and the refusals — but no test can tell you a
chart is legible. Render a page and look at it before citing one.

## Generated artifacts

`profile.py` writes `index.html` from the maintained
[`report.html`](../stats_profiler/report.html) template, plus `summary.json`
and `benchmarks.csv`. `plots.py` writes the PDFs listed above. All are rewritten
whole: edit the configuration and regenerate, not the generated files. An output
directory can still contain older PDFs if a later run omits `--pdf` or changes
category names; use a fresh directory for each report you intend to share.

The committed [example PDF](../stats_profiler/example-plots-quant-07-25.pdf) is
a generated measurement artifact of the recorded example run, not a regenerated
CI baseline. Its raw input is not committed; fetch the named stats job to
recompute it. CI checks synthetic cases and PDF structure, not agreement with
that measurement or the visual accessibility of the palette.
