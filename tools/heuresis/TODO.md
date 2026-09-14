# heuresis — the plan

Nothing has been run. This is the order the work goes in, so that a reader can
tell what is intended from what exists. The goals it serves are numbered in
[`README.md`](README.md); the rows it refers to are in [`notes.md`](notes.md).

## First — goal 0, the set and the baselines

- [ ] **Name the set.** A person's decision. Candidates the notes and the
      launcher know of: "the verus+sundance set" on which `h-25` was measured;
      the quantifier benchmark tree and the cvc5-is-slow list that run-dev's
      naming tables mention. Record in `README.md`, "The set": location on the
      host, count, how it was selected, date. Then set `QUANT_DIR` in
      `job_launcher/site.conf` to it.
- [ ] **Fix the rest of goal 0** in the same section: the cvc5 commit or
      branch, the z3 version (a binary name in `Z3_BIN` and a version string
      in the ledger), the timeout (60 s, unless there is a reason), and the
      factor that defines the gap set (10×, unless there is a reason).
- [ ] **Check `--term-db=relevant`** is or is not in the default
      configuration, and write the answer into `notes.md`, "The configuration
      under study". The notes list it among things that helped without saying
      whether it is on.
- [ ] `cp job_launcher/site.conf.example job_launcher/site.conf`, `job_launcher/checks`, and a dry run of
      `quant-cvc5.conf` and `quant-z3.conf`.

## Then — goal 1, the gap

- [ ] Run `quant-cvc5.conf` and `quant-z3.conf`, queued, same host, same
      timeout. One ledger entry with both result files, the gap set (as a
      list, tracked in the ledger entry), its size, and the aggregate ratio.
- [ ] Run `quant-cvc5-default.conf` once, so that what the configuration under
      study buys is a number and not a memory.
- [ ] The first analysis script, only now: read two run-dev results files,
      print the gap set and the ratio. Small, in this directory, cited by the
      ledger entry. Nothing more general until a second experiment needs it.

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
