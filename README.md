# tachyon

**Find the opportunities to improve cvc5's performance, and back each one with
evidence a reader can recompute.**

cvc5 is slower than it should be on problems people actually run, and the
reasons are rarely obvious from the outside. This repository is where those
reasons get found. Each project here takes an observed limitation, investigates
the candidate explanations, measures them against a set of benchmarks fixed in
advance, and writes up what survives: the shortcoming, the evidence for it, how
to reproduce it, and what remains unknown.

What comes out is a *finding*, not a patch — a concrete performance shortcoming,
or a research question grounded in a real limitation, stated clearly enough that
a person can judge it and decide for themselves whether to pursue it. That
follow-up happens outside this repository, at their discretion. **Finding the
diamond in the rough is the work here**; cutting it is somebody else's, and a
diamond found is a useful result whether or not anyone pursues it.

Two habits are what make that worth reading. Nothing is claimed that has not
been measured: every number comes from a row in a project's ledger with the job
config and the launch line beside it. And every measurement goes through the
shared launcher, so a reader who was not here can run it again.

## What is here

| | |
| --- | --- |
| [`tools/heuresis/`](tools/heuresis/) | **research** — what the quantified benchmarks where z3 is much faster reveal about cvc5 |
| [`tools/metagraphe/`](tools/metagraphe/) | **research** — which useful string and bit-vector rewrites cvc5 is missing |
| [`job_launcher/`](job_launcher/) | **tool** — reproducible benchmark jobs on a remote host, configs and log tracked |
| [`stats_profiler/`](stats_profiler/) | **tool** — where a job's solver time actually went |

A research project owns a question and the evidence for it. The tooling supplies
the measurements and is shared by all of them.

## The research projects

### [`heuresis/`](tools/heuresis/) — the quantifier gap against z3

*Find the cvc5 shortcomings worth pursuing in the quantified benchmarks where z3
is much faster.*

There is a set of quantified SMT benchmarks from Verus and related verification
tooling — 6124 of them, named by a person and then fixed — on which z3 is much
faster than cvc5. Heuresis asks what that gap reveals. It starts from a register
of some thirty candidate causes, several with a branch already written, and its
discipline is attribution before construction: a branch that looks promising is
a hypothesis until it has been run against the set. z3 is the oracle and not the
target — what z3 does is evidence about what a benchmark needs, never a thing to
copy.

The gap is measured, twenty-seven research directions are written up from cvc5
and z3 source and the literature, and decomposing the gap benchmark by benchmark
is the work in progress. The charter, the fixed set and baselines, and the
current numbers are in [its README](tools/heuresis/README.md#status); the
register is [`docs/directions.md`](tools/heuresis/docs/directions.md), the queue
is [`docs/todo.md`](tools/heuresis/docs/todo.md), and every run behind a number
is in [`ledger/`](tools/heuresis/ledger/).

### [`metagraphe/`](tools/metagraphe/) — the rewrites cvc5 is missing

*Which equivalent forms could cvc5 use to simplify string and bit-vector
expressions, and where does its current rewriting miss a useful opportunity?*

A candidate is a missing rule, a rule whose conditions are more restrictive than
they need to be, or an interaction that keeps existing rules from firing. Each
one is held to three separate questions — is the rewrite valid, is cvc5 really
missing it, and why does it matter — because a smaller expression is not by
itself a solver speedup, and a rule that already exists under another option is
not a gap.

Started 2026-09-16. The charter, the search areas, and the evidence format are
in place; pinning a baseline and running the first probes from each theory is
the next work. See [its README](tools/metagraphe/README.md) and its
[documentation index](tools/metagraphe/docs/README.md).

## The tooling

### [`job_launcher/`](job_launcher/) — experiments, independent of any one machine

The launcher runs remote benchmark jobs: it validates a config, opens a tmux
window on a benchmark host, runs one driver there, and logs the launch with the
solver's branch and commit. What a launcher deliberately does *not* track is
the job configs and the log, because there they carry one person's hosts and
history. Here they are the
experimental record, so here they are tracked — and everything about a person's
machines stays in one git-ignored `site.conf`.

- [`configs/`](job_launcher/configs/) — the jobs, one file each, written against
  names (`$QUANT_DIR`, `$CVC5_BIN`, `$Z3_BIN`) that `job_launcher/site.conf`
  resolves, never against a path;
- [`log.txt`](job_launcher/log.txt) — every launch, appended by `submit`;
- [`site.conf.example`](job_launcher/site.conf.example) — the one file with
  anything personal in it, copied once and edited once;
- [`checks`](job_launcher/checks) — the lint: scripts parse, configs resolve, and
  no personal data is in anything that could be committed.

```bash
cp job_launcher/site.conf.example job_launcher/site.conf      # once: host, paths, binaries
job_launcher/checks                                  # nothing personal, everything parses
job_launcher/submit -n quant-cvc5.conf               # dry run against the host
job_launcher/submit    quant-cvc5.conf quant-z3.conf # launch, queued, logged
job_launcher/status
```

The details — where the launcher is found, which commit the wrappers were
written against, what they add and do not add, how a config stays portable — are in
[`job_launcher/README.md`](job_launcher/README.md).

### [`stats_profiler/`](stats_profiler/) — timing coverage of a stats job

[`stats_profiler/`](stats_profiler/) turns raw cvc5 `--stats-internal` job output
into an interactive offline report: configurable timing categories, benchmark
distributions, totals, and uncovered or over-counted time. It also exports CSV
and JSON for further analysis, and vector PDF plots — a distribution per timer
and a cumulative-time pie — for citing in a ledger entry. Requires only
Python 3.9+.

```bash
python3 stats_profiler/profile.py /path/to/stats-job.txt --output scratch/profile
```

Its [worked example](stats_profiler/README.md#the-worked-example) runs the
launcher's [`quant-cvc5-stats.conf`](job_launcher/configs/quant-cvc5-stats.conf)
over `$QUANT_DIR` (`quant-07-25`) and profiles the result against the eight
timers in [`quant-07-25.json`](stats_profiler/quant-07-25.json).

## On the name

ταχύς — *swift*. A tachyon is the hypothetical particle that travels faster
than light, and nothing has ever observed one. That is the right amount of
ambition for a repository about speed, and the right amount of humility: the
goal is stated as something that may not exist, and every claim made here has
to be measured before it is believed.

## Conventions

Borrowed from [dokimasia](https://github.com/ajreynol/dokimasia), which this
repository is modelled on:

- **Nothing personal in tracked files.** Hosts, home directories, usernames,
  binary names: all of it lives in `job_launcher/site.conf`, and `job_launcher/checks` refuses a
  commit that contains any of it.
- **Only measured claims.** A number in a document comes from a row in a ledger
  with a config and a log entry beside it. A claim that cannot be measured yet
  is a hypothesis, and is filed as one.
- **A research project is an island.** It reads the launcher and its own
  files. Deleting `tools/<name>/` leaves everything else as functional as it
  was, which is what lets the launcher be reused for the next question.
- **Written for a reader who was not here.** Every document says what was
  checked and what was reasoned, and which is which.

## How this repository is maintained

This repository is part of the **Eunoia ecosystem** and follows its shared
repository policy, kept by [kanon](https://github.com/ajreynol/kanon) in
[`docs/policy.md`](https://github.com/ajreynol/kanon/blob/main/docs/policy.md).

**Written by AI agents, under a human maintainer who owns the questions.** A
person starts each research project, sets its scope, and owns any priorities
recorded in their name. The agents write
the documents, the register of directions, the job configs and the ledger
entries, and keep a ranking of their own beside the maintainer's rather than
mirroring it. Their analysis is intended to inspire independent human work on
the shortcomings it uncovers. Choosing and pursuing that work is the person's
discretion; discovery here does not wait for a finding to be taken up.

**What that supervision leaves out.** Nobody reads every line before it is
committed. Every number here comes from a single run on one benchmark host,
recorded in the ledger with its config and its launch line so that a reader can
recompute it from this checkout — which is reproducibility from the results, and
not an independent measurement by a second party. The reasoning around a number,
and the ranking of what to do next, are an agent's argument until the maintainer
has said otherwise. Nothing leaves this repository by machine: a finding is
carried to cvc5, or anywhere else, only by a person deciding to carry it.
