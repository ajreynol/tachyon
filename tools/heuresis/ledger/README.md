# The ledger

**One file per experiment, written after the run, from the results.** The
ledger is the only place a number is allowed to enter this project: a figure
in `README.md` or `notes.md` that does not point at an entry here is a
hypothesis and must say so.

Entries:

- [`2026-09-14-baseline.md`](2026-09-14-baseline.md)
- [`2026-09-15-baseline-caveats.md`](2026-09-15-baseline-caveats.md)
  (a correction entry, nothing run)
- [`2026-09-15-quantifier-controls.md`](2026-09-15-quantifier-controls.md)
- [`2026-09-15-sat-and-instance-order.md`](2026-09-15-sat-and-instance-order.md)
- [`2026-09-15-z3-full-verus-options.md`](2026-09-15-z3-full-verus-options.md)
- [`2026-09-15-attribution-stats.md`](2026-09-15-attribution-stats.md)
- [`2026-09-16-datatype-and-equality-controls.md`](2026-09-16-datatype-and-equality-controls.md)
- [`2026-09-16-entailment-filtering.md`](2026-09-16-entailment-filtering.md)
- [`2026-09-16-combined-central-equality-and-evaluator-off.md`](2026-09-16-combined-central-equality-and-evaluator-off.md)
- [`2026-09-16-conflict-instantiation.md`](2026-09-16-conflict-instantiation.md)
- [`2026-09-16-rebased-equality-and-evaluator-branches.md`](2026-09-16-rebased-equality-and-evaluator-branches.md)

Full results and statistics files remain on the execution host and may be
copied into [`data/`](data/) with `job_launcher/fetch` for local analysis, but
they are ignored by Git. Each entry records the exact raw artifact name,
command, solver revision, and aggregate result. Generated benchmark lists,
including gap sets written by `gap --gapset`, also remain local; only small
processed summaries are tracked. See the [data-retention
policy](data/README.md).

## An entry

`ledger/YYYY-MM-DD-<name>.md`, where `<name>` is the run-dev job NAME (or
the two NAMEs of an A/B, joined by `-vs-`). Each entry carries, in this order:

1. **What was asked.** The goal or the row of `notes.md` this run serves.
2. **What was run.** The config file(s) in `job_launcher/configs/` as they were at the
   time, and the `job_launcher/log.txt` entry, quoted — it has the host, the command,
   and the binary's `branch@commit`. For z3, the version string.
3. **The set.** Its name from `README.md`, "The set", and the count actually
   run.
4. **What came back.** The results file names on the host, and the numbers
   read from them, with the script that read them named. For a baseline: the
   gap set as a list, its size, the aggregate ratio. For an A/B: the same
   numbers for both arms, and the benchmarks that changed status.
5. **What it settled.** One paragraph. Which row(s) of the register it bears
   on, in which direction, and how strongly. *Nothing* is an acceptable
   answer and is written down as one.
6. **What it did not settle**, if the run's design left an obvious question
   open — a timeout that was hiding the answer, a confound.

An entry is never edited after the fact; a correction is a new entry that
names the old one.
