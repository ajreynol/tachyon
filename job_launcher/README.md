# job_launcher/ — this repository's experiments, on run-dev

[run-dev](https://github.com/ajreynol/run-dev) launches benchmark jobs on a
remote host and records them. This directory is *one project's use of it*: the
configs, the site file, and the log that run-dev keeps private and git-ignored,
because in run-dev they carry one person's hosts and history. Here they are the
experimental record — the thing `tools/heuresis/ledger/` cites — so here they
are tracked, and made portable so that they can be.

Nothing of run-dev is copied. Its scripts, drivers, wrappers and docs are used
from a checkout, found as described below, and pinned by commit in
[`run-dev.lock`](run-dev.lock).

## Setup

```bash
git clone https://github.com/ajreynol/run-dev ../run-dev   # or anywhere: set RUN_DEV
cp job_launcher/site.conf.example job_launcher/site.conf                     # then edit: host, paths, binaries
job_launcher/checks
```

The host side is run-dev's, unchanged: the deployed scripts in `~/bin/run-dev/`
and the one host file `run-dev.conf`, set up as run-dev's
[`docs/QUICKSTART.md`](https://github.com/ajreynol/run-dev/blob/main/docs/QUICKSTART.md)
says. This directory adds nothing on the host.

## What is where

| file | tracked | holds |
| --- | --- | --- |
| `site.conf.example` | yes | the template: every machine- and user-specific name, and the naming tables |
| `site.conf` | **no** | your copy of it. The only file with anything personal in it |
| `configs/*.conf` | yes | one job each, written against names the site file resolves |
| `log.txt` | yes | every launch, in run-dev's format, appended by `job_launcher/submit` |
| `run-dev.lock` | yes | the run-dev commit this was tested against |
| `submit`, `status` | yes | run-dev's commands, pointed at this site file and these configs |
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
refuses a config with a literal path in `DIR`, and refuses any public file
containing your username, home directory, git identity, or anything
`site.conf` names.

To add a benchmark set: one variable in `site.conf.example` (with a generic
placeholder value), one line in `set_prefix`, and configs that use the name.

## The wrappers

`job_launcher/submit` is run-dev's `submit` with four things added and nothing changed:

1. the site file is `job_launcher/site.conf`, passed as `SUBMIT_SITE`;
2. a bare config name resolves against `job_launcher/configs/` first (an existing path
   is passed through; the argument after `-b` is a branch, never a config);
3. the log entries run-dev's `submit` appends to *its* `log.txt` during the
   call are copied to `job_launcher/log.txt`;
4. a warning when the checkout is not at the pinned commit.

Everything else — flags, refusals, queueing, `--baseline`, `-b`/`-r`/`-x`,
`-k` — is run-dev's, and `job_launcher/submit -h` prints both help texts. run-dev keeps
writing its own files (`configs/.gen/` for derived configs, its own log) in
its own checkout; that is by design, and the copy in `job_launcher/log.txt` is the
record this repository cites.

`job_launcher/status` is run-dev's `status` against this site file. Read-only.

**Where the checkout is found**, in order: `$RUN_DEV` in the environment,
`RUN_DEV=` in `job_launcher/site.conf`, `../run-dev` beside this repository.

## The pin

[`run-dev.lock`](run-dev.lock) records the run-dev commit these wrappers were
tested against. The wrappers depend on three things about `submit` — that it
honours `SUBMIT_SITE`, sources configs after the site file, and appends to
`log.txt` next to itself — all of which have been stable, so a newer checkout
is a warning rather than a refusal. After running against a newer run-dev and
finding the wrappers still correct, update the commit in the lock.

## What this does not do

- **Copy run-dev.** A fork would drift; the pin is the honest alternative.
- **Analyse results.** Results land on the host in `~/analysis/data/` as
  run-dev's drivers write them, one line per benchmark. What is read from
  them, and how, is the research project's business and is recorded in its
  ledger. run-dev's analysis notebooks are self-contained and a good starting
  point, and the first one that is needed twice is the one to extract.
- **Run anything locally.** Every job runs on the host through run-dev.
