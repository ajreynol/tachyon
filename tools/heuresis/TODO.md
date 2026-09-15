# heuresis — the plan

Nothing has been run. This is the order the work goes in, so that a reader can
tell what is intended from what exists. The goals it serves are numbered in
[`README.md`](README.md); the rows it refers to are in [`notes.md`](notes.md).

## First — goal 0, the set and the baselines

- [x] **Name the set.** `quant-07-25` on the host, named 2026-09-14; see
      `README.md`, "The set". Count still to be recorded from the first run.
- [x] **Fix the rest of goal 0**: 30 s timeout, two cvc5 configurations, the
      gap factor 10× with a 1 s floor, PAR2 ratio. The z3 version and the cvc5
      commit are recorded per ledger entry.
- [ ] **Check `--term-db=relevant`** is or is not in the default
      configuration, and write the answer into `notes.md`, "The configuration
      under study". The notes list it among things that helped without saying
      whether it is on.
- [ ] `cp job_launcher/site.conf.example job_launcher/site.conf`, `job_launcher/checks`, and a dry run of
      `quant-cvc5.conf` and `quant-z3.conf`.

## Then — goal 1, the gap

- [x] Run `quant-z3.conf`, `quant-cvc5-default.conf` and `quant-cvc5.conf`,
      queued, same host, same timeout. [Ledger, 2026-09-14](ledger/2026-09-14-baseline.md):
      PAR2 ratio 4.34, gap set 1049.
- [ ] One run of cvc5 with the options Verus itself passes to cvc5, if they
      differ from the best known configuration; the ledger entry says why.
- [ ] One run of the 545 cvc5 timeouts at a long timeout (20 min), to split
      "slow" from "stuck" before attributing.
- [x] The first analysis script: [`gap`](gap) reads run-dev results files and
      prints the counts, the PAR2 ratio and the gap set. Nothing more general
      until a second experiment needs it.

## Then — goal 2, the attribution

- [ ] `quant-cvc5-stats.conf` on the set; per gap benchmark, the counters that
      distinguish the register's classes (instantiation rounds and counts,
      lemmas sent, decisions, branch-and-bound lemmas, datatype splits,
      preprocessing time). Which counters, exactly, is decided by looking at
      the first ten gap benchmarks by hand.
- [ ] Profiles of the ten worst, through run-dev's `get_profile`.
- [ ] The attribution table: one row per gap benchmark, one column per class
      of `notes.md`, and the fraction each column explains. This is the
      project's first result and the second number in `README.md`.
- [ ] Rewrite or delete `notes.md`, "A reading of the register", according to
      what the table says.

## Then — goal 3

- [ ] Pick the top row. If it has a branch, `BRANCH=` in a copy of
      `quant-cvc5.conf`; if it is an option, add it to `OPTS`. A/B against the
      baseline, one ledger entry, whether or not it helped.
- [ ] Repeat down the ranking while a row explains a share worth the run.

## Not yet

- **Any code on the register's branches.** Until the attribution says which
  row is worth it, working a branch is building before finding out.
- **An analysis library.** run-dev's notebooks are self-contained on purpose;
  the first helper needed twice is the one to extract, and not before.
- **Widening the set.** A second set is a second project.
- **Anything upstream.** No pull request, no issue comment, no push from
  here. A person carries a result, if there is one.
