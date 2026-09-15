# tachyon

*What would make cvc5 fast?*

Two things live here, and they are kept apart on purpose:

| | | |
| --- | --- | --- |
| [`job_launcher/`](job_launcher/) | **run experiments** — the job configs, site file and log for this repository's benchmark runs, driving a pinned checkout of [run-dev](https://github.com/ajreynol/run-dev) | tooling |
| [`tools/heuresis/`](tools/heuresis/) | **what would make cvc5 fast on quantified benchmarks** — the question, the register of hypotheses with the evidence for each, the plan, and the ledger | research project |

The first exists so that the second can produce numbers, and so that anybody
with a benchmark host can reproduce them without editing a script. The second
is the reason the repository exists.

**On the name.** ταχύς — *swift*. A tachyon is the hypothetical particle that
travels faster than light, and nothing has ever observed one. That is the right
amount of ambition for a repository about speed, and the right amount of
humility: the goal is stated as something that may not exist, and every claim
made here has to be measured before it is believed.

## `job_launcher/` — experiments, independent of any one machine

[run-dev](https://github.com/ajreynol/run-dev) is a launcher for remote
benchmark jobs: it validates a config, opens a tmux window on a benchmark host,
runs one driver there, and logs the launch with the solver's branch and commit.
Its tracked half is site-independent already — everything about a person's
machines lives in two git-ignored files, `site.conf` on the control side and
`run-dev.conf` on the host, and its own `checks` refuses personal data in
anything tracked.

What run-dev deliberately does **not** track is the other half: the job configs
and the log, because there they carry one person's hosts and history. Here they
are the experimental record, so here they are tracked. `job_launcher/` is that half for
this repository:

- [`job_launcher/configs/`](job_launcher/configs/) — the jobs, one file each, written against
  names (`$QUANT_DIR`, `$CVC5_BIN`, `$Z3_BIN`) that `job_launcher/site.conf` resolves,
  never against a path;
- [`job_launcher/site.conf.example`](job_launcher/site.conf.example) — the one file with anything
  personal in it, copied to `job_launcher/site.conf` (git-ignored) and edited once;
- [`job_launcher/log.txt`](job_launcher/log.txt) — every launch, appended by `job_launcher/submit`;
- [`job_launcher/submit`](job_launcher/submit), [`job_launcher/status`](job_launcher/status) — run-dev's commands,
  pointed at this site file and these configs;
- [`job_launcher/run-dev.lock`](job_launcher/run-dev.lock) — the run-dev commit this was written
  against; the wrappers warn when the checkout differs;
- [`job_launcher/checks`](job_launcher/checks) — the lint: scripts parse, configs resolve, and no
  personal data is in anything that could be committed.

```bash
cp job_launcher/site.conf.example job_launcher/site.conf      # once: host, paths, binaries
job_launcher/checks                                  # nothing personal, everything parses
job_launcher/submit -n quant-cvc5.conf               # dry run against the host
job_launcher/submit    quant-cvc5.conf quant-z3.conf # launch, queued, logged
job_launcher/status
```

The details — where run-dev is found, what the wrappers add and do not add,
how a config stays portable — are in [`job_launcher/README.md`](job_launcher/README.md).

## `tools/heuresis/` — the question

There is a set of quantified benchmarks, from verification tooling, on which z3
is much faster than cvc5 — by enough that the reason must be structural. The
project asks **which structural differences account for the gap, in what
proportion, and what is the cheapest change to cvc5 that closes most of it**,
and it insists on the attribution before any building. The charter, the goals
in order, and the two numbers that say whether it is working are in
[`tools/heuresis/README.md`](tools/heuresis/README.md); the register of
hypotheses it starts from — a summary of a set of performance notes, one row per
candidate cause with its state and what would settle it — is
[`tools/heuresis/notes.md`](tools/heuresis/notes.md).

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

## Status

Set up on 2026-09-14. The current ranked work is maintained in
[`tools/heuresis/docs/todo.md`](tools/heuresis/docs/todo.md); its entries refer to the
research registry in
[`tools/heuresis/docs/directions.md`](tools/heuresis/docs/directions.md).
