# Running experiments

Opens benchmark jobs on a remote host and records them. Everything needed to
do that lives here: the launcher scripts, the scripts that run on the host,
the configs, the site file, and the log. **No external checkout is required**,
on this machine or on the host.

The log is the experimental record cited by the research ledgers, so it is
tracked here, and the configs are written so that they can be.

## Setup

```bash
cp job_launcher/site.conf.example job_launcher/site.conf   # then edit: host, paths, binaries
job_launcher/deploy                                        # install host/ to HOST:~/bin/heuresis
job_launcher/checks
```

`deploy` creates `~/bin/heuresis/heuresis.conf` on the host from
[`host/heuresis.conf.example`](../job_launcher/host/heuresis.conf.example) the first time and
never overwrites it afterwards — it is host-local in the same way `site.conf`
is machine-local. Set `JOBS` in it at least. Re-run `deploy` after changing
anything in [`host/`](../job_launcher/host).

The host also needs GNU `parallel`, `timeout` and `strip` on its `PATH`, and
the directories `~/analysis/data`, `~/analysis/stats` and `~/analysis/binaries`.

## What is where

Paths below are relative to `job_launcher/`.

| file | tracked | holds |
| --- | --- | --- |
| `site.conf.example` | yes | the template: every machine- and user-specific name, and the naming tables |
| `site.conf` | **no** | your personal setup; launch records separately identify the host and build |
| `submit` | yes | validates configs, runs the remote checks, launches and logs jobs |
| `status` | yes | read-only view of what the host is doing |
| `deploy` | yes | installs `host/` to `HOST:~/bin/heuresis` |
| `fetch` | yes | copies results back from the host |
| `checks` | yes | the lint |
| `common.sh` | yes | finds the site file; sourced by `deploy` and `fetch` |
| `host/` | yes | **the scripts that run on the host**: the drivers, the wrappers, `benchmark_binary`, and the host conf template |
| `configs/*.conf` | yes | one job each, written against names the site file resolves |
| `log.txt` | yes | every launch, appended by `submit` |

## The two sides

**Local.** `submit` reads a config, derives the job name, runs read-only
sanity checks over ssh, and opens one tmux window per launch. `-b BRANCH`
and `-r` are blocking instead, streaming progress and ending in an explicit
verdict. `log.txt` records launch metadata and final verdicts. Full blocking-job
output is written to a local temporary file, whose path the launcher prints.

**Host.** [`host/`](../job_launcher/host) is installed to `~/bin/heuresis`, and every job runs
with `PATH=$HOME/bin/heuresis:$HOME/bin:$PATH`, so the drivers and wrappers a
job uses are the ones from the latest deployment. Redeploy after host-script
changes and record that revision when recording an experiment. A
driver benchmarks its working directory (`find -name '*.smt2'`), runs
`parallel -j$JOBS`, and writes one results file to `~/analysis/`.

The wrappers take everything as explicit arguments, so a run is fully
described by its command line and nothing is read from the host's environment.

## How a config stays site-independent

A config is a shell-variable file that `submit` sources *after* the site file.
So a config here never names a path, a host or a binary; it names a variable
that `site.conf` defines:

```bash
DIR=$QUANT_DIR                 # not ~/benchmarks/...
BINARY=$CVC5_BIN               # not cvc5-mybuild
DRIVER=solve_dir_rec_par_cvc5
OPTS="-q --user-pat=strict --no-cbqi --sat-solver=cadical"
```

`HOST` is left unset, so `DEFAULT_HOST` from the site file applies. The naming
table `set_prefix` keys on `"$QUANT_DIR"` for the same reason.
`job_launcher/checks` checks unquoted `DIR=/...` and `DIR=~/...` assignments. Its identity scan uses
literal matches for the current username, home-directory basename, Git email
local part, and the site's host, repository basename and build binary. Public
URLs, launch records, research ledgers and values shipped in the site template
are exempt. This is targeted lint, not a guarantee that every possible personal
path or name is detected; review records before sharing.

To add a benchmark set: one variable in `site.conf.example` (with a generic
placeholder value), one line in `set_prefix`, and configs that use the name.

## Config and site selection

An existing config path is used as supplied. A missing bare name is looked up
under `job_launcher/configs/`. Branch names after `-b` and window names after
`-k` are not config paths. `-x CONFIG` selects the config for a combined build
and run. Derived configurations are written to ignored `configs/.gen/`.

All launcher commands accept `$TACHYON_SITE` to select a site file, with
`$SUBMIT_SITE` as a fallback and `job_launcher/site.conf` as the default.
`checks` always validates against the tracked template and scans the default
site file when present. `-h` or `--help` as the first argument prints the
command's own header comment and needs no site file: the reader asking what a
command does is the one who has not configured it yet.

## Retrieve results

```bash
job_launcher/fetch -d scratch/results quant-091526-u-ss-stats
```

`fetch [-H HOST] [-d DIR] NAME...` copies matching result files from
`~/analysis/data/` and files or directories from `~/analysis/stats/`. It defaults
to `DEFAULT_HOST` and ignored `scratch/results/`, needs only the site file,
and never changes the host. Listing and copy failures return nonzero; no
matching files is reported separately. Its argument checks, like every
command's help, run before site setup. Repeated copies replace local files.

Fetched results, statistics (including `-processed.txt`) and error sidecars are
raw job artifacts. Keep them under ignored `scratch/` or outside the checkout;
do not commit them or paste their contents into a ledger. Record summaries and
artifact locations according to the [retention policy](maintenance.md#result-retention).

## Things that will bite

**One job per tmux window.** `submit` accepts several configs and queues them
into one window, but tmux refuses a command line beyond a few hundred
characters with `create window failed`, which in practice means two full
configs. Submit them one at a time and wait; `submit` refuses to start a
second job while one is running, which is the backstop.

**Finished windows stay open** on purpose, so a post-mortem is possible, and
the next launch into that index then fails. Close it first:

```bash
job_launcher/submit -k quant-091426      # the NAME of the finished job
```

## What this does not do

- **Analyse results.** Results land on the host in benchmark blocks. What
  is read from them, and how, is the research project's business and is
  recorded in its ledger.
- **Run anything locally.** Every job runs on the host.
- **Own the host.** `deploy` writes only inside `~/bin/heuresis`. Anything else
  already on the host is left alone.
