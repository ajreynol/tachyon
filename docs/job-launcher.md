# Running experiments

[run-dev](https://github.com/ajreynol/run-dev) launches benchmark jobs on a
remote host and records them. `job_launcher/` is *this repository's use of it*: the
configs, the site file, and the log that run-dev keeps private and git-ignored,
because in run-dev they carry one person's hosts and history. Here they are the
experimental record cited by the individual research ledgers, so here they
are tracked, and made portable so that they can be.

Nothing of run-dev is copied. Its scripts, drivers, wrappers and docs are used
from a checkout, found as described below, with a tested commit recorded in
[`run-dev.lock`](../job_launcher/run-dev.lock).
This guide describes the interface targeted by that lock as of 2026-09-17;
local wrapper tests use stand-ins and do not certify a run-dev installation.

## Setup

```bash
git clone https://github.com/ajreynol/run-dev ../run-dev   # or anywhere: set RUN_DEV
git -C ../run-dev checkout "$(sed -n 's/^commit=//p' job_launcher/run-dev.lock)"
cp job_launcher/site.conf.example job_launcher/site.conf                     # then edit: host, paths, binaries
job_launcher/checks
```

The host side is run-dev's, unchanged: the deployed scripts in `~/bin/run-dev/`
and the one host file `run-dev.conf`, set up as run-dev's
[`docs/QUICKSTART.md`](https://github.com/ajreynol/run-dev/blob/main/docs/QUICKSTART.md)
says. This directory adds nothing on the host.

## What is where

Paths below are relative to `job_launcher/`.

| file | tracked | holds |
| --- | --- | --- |
| `site.conf.example` | yes | the template: every machine- and user-specific name, and the naming tables |
| `site.conf` | **no** | your personal setup; launch records may separately identify the host and build |
| `configs/*.conf` | yes | one job each, written against names the site file resolves |
| `log.txt` | yes | every launch, in run-dev's format, appended by `job_launcher/submit` |
| `run-dev.lock` | yes | the run-dev commit this was tested against |
| `submit`, `status` | yes | run-dev's commands, pointed at this site file and these configs |
| `fetch` | yes | copy result files and stats directories from the host |
| `common.sh` | yes | finds the checkout and the site file; sourced by the three scripts |
| `checks` | yes | the lint |

## How a config stays site-independent

A run-dev config is a shell-variable file that `submit` sources *after* the
site file. So a config here never names a path, a host or a binary; it names a
variable that `site.conf` defines:

```bash
DIR=$QUANT_DIR                 # not ~/benchmarks/...
BINARY=$CVC5_BIN               # not cvc5-mybuild
DRIVER=solve_dir_rec_par_cvc5
OPTS="-q --user-pat=strict --no-cbqi --sat-solver=cadical"
```

`HOST` is left unset, so `DEFAULT_HOST` from the site file applies. The naming
table `set_prefix` keys on `"$QUANT_DIR"` for the same reason. `job_launcher/checks`
checks unquoted `DIR=/...` and `DIR=~/...` assignments. Its identity scan uses
the current username, home-directory basename, Git email local part, and the
site's host, repository basename and build binary. Public URLs, the launch log,
research ledgers, and values shipped in the site template are exempt. Patterns
are matched literally, without treating dots as regular-expression wildcards.
This is a targeted lint, not a guarantee that
every possible personal path or name is detected; review records before sharing.

To add a benchmark set: one variable in `site.conf.example` (with a generic
placeholder value), one line in `set_prefix`, and configs that use the name.

## The wrappers

`job_launcher/submit` is run-dev's `submit` with four things added and nothing changed:

1. the site file is `job_launcher/site.conf` (or `$TACHYON_SITE`), passed as `SUBMIT_SITE`;
2. an existing config path is passed through; a missing bare name resolves
   against `job_launcher/configs/`. Branch, host and session option values and
   names following `-k` are passed through;
3. the log entries run-dev's `submit` appends to *its* `log.txt` during the
   call are copied to `job_launcher/log.txt`;
4. a warning when the checkout is not at the pinned commit.

Everything else — flags, refusals, queueing, `--baseline`, `-b`/`-r`/`-x`,
`-k` — is run-dev's, and `job_launcher/submit -h` prints both help texts. run-dev keeps
writing its own files (`configs/.gen/` for derived configs, its own log) in
its own checkout; that is by design, and the copy in `job_launcher/log.txt` is the
record this repository cites.
Avoid simultaneous submissions through the same run-dev checkout: the wrapper
copies the appended span of its shared log and cannot attribute concurrent writes.

`job_launcher/status` is run-dev's `status` against this site file. Read-only.

**Finished windows stay open** (run-dev leaves them for post-mortem), and the
next launch can fail with tmux's `create window failed: index in use` before
anything is logged. Close the finished window first:

```bash
job_launcher/submit -k quant-091426      # the NAME of the finished job
```

**Where the checkout is found**, in order: `$RUN_DEV` in the environment,
`RUN_DEV=` in `job_launcher/site.conf`, `../run-dev` beside this repository.
The example site file sets `RUN_DEV=~/run-dev`; edit it to match the checkout
you actually installed. `$TACHYON_SITE` selects a different site file for the
wrappers; `checks` always validates against the tracked template and scans the
default `job_launcher/site.conf` when present.

## Retrieve results

```bash
job_launcher/fetch -d scratch/results quant-091526-u-ss-stats
```

`fetch [-H HOST] [-d DIR] NAME...` copies matching result files from
`~/analysis/data/` and matching files or directories from `~/analysis/stats/`.
It defaults to `DEFAULT_HOST` and ignored `scratch/results/`, needs the site
file and a run-dev checkout, and never changes the host. A listing or copy
failure returns nonzero; no matching files is reported separately. Its help
and argument checks work before site setup. Repeated copies replace local files.

## The pin

[`run-dev.lock`](../job_launcher/run-dev.lock) records the run-dev commit these wrappers were
tested against. The wrappers depend on three things about `submit` — that it
honours `SUBMIT_SITE`, sources configs after the site file, and appends to
`log.txt` next to itself. A different checkout produces a warning, not a
refusal; the wrappers do not fetch run-dev or check out the lock automatically.
After running against a newer run-dev and
finding the wrappers still correct, update the commit in the lock.

## What this does not do

- **Copy run-dev.** A fork would drift; the pin is the honest alternative.
- **Analyse results.** Results land on the host in `~/analysis/data/` as
  run-dev's drivers write them, in benchmark blocks. What is read from
  them, and how, is the research project's business and is recorded in its
  ledger. run-dev's analysis notebooks are self-contained and a good starting
  point, and the first one that is needed twice is the one to extract.
- **Run anything locally.** Every job runs on the host through run-dev.
