# The ledger

**One file per experiment, written after the run, from the results.** The
ledger is the only place a number is allowed to enter this project: a figure
in `README.md` or `notes.md` that does not point at an entry here is a
hypothesis and must say so.

There are no entries yet.

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
