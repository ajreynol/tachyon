# job_launcher/ — this repository's experiments, independent of any one machine

The launcher opens benchmark jobs on a remote host and records them. This
directory is *this repository's use of it*: the configs, the site file, and the
log, which the launcher itself keeps private and git-ignored because there they
carry one person's hosts and history. Here they are the experimental record
cited by the individual research ledgers, so here they are tracked, and made
portable so that they can be.

Nothing of the launcher is copied. Its scripts, drivers, wrappers and docs are
used from a checkout, found as described below, and pinned by commit in
[`launcher.lock`](launcher.lock).

## Setup

```bash
cp job_launcher/site.conf.example job_launcher/site.conf   # then edit: LAUNCHER_DIR, host, paths, binaries
job_launcher/checks
```

`LAUNCHER_DIR` in the site file (or in the environment) is the path to the launcher
checkout; there is no default. The host side is the launcher's own, unchanged:
its deployed scripts and its one host config file, set up as its own quickstart
says. This directory adds nothing on the host.

## What is where

| file | tracked | holds |
| --- | --- | --- |
| `site.conf.example` | yes | the template: every machine- and user-specific name, and the naming tables |
| `site.conf` | **no** | your copy of it. The only file with anything personal in it |
| `configs/*.conf` | yes | one job each, written against names the site file resolves |
| `log.txt` | yes | every launch, in the launcher's format, appended by `job_launcher/submit` |
| `launcher.lock` | yes | the launcher commit this was tested against |
| `submit`, `status` | yes | the launcher's commands, pointed at this site file and these configs |
| `common.sh` | yes | finds the checkout and the site file; sourced by the three scripts |
| `checks` | yes | the lint |

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
table `set_prefix` keys on `"$QUANT_DIR"` for the same reason. `job_launcher/checks`
refuses a config with a literal path in `DIR`, and refuses any public file
containing your username, home directory, git identity, or anything
`site.conf` names.

To add a benchmark set: one variable in `site.conf.example` (with a generic
placeholder value), one line in `set_prefix`, and configs that use the name.

## The wrappers

`job_launcher/submit` is the launcher's `submit` with four things added and nothing changed:

1. the site file is `job_launcher/site.conf`, passed as `SUBMIT_SITE`;
2. a bare config name resolves against `job_launcher/configs/` first (an existing path
   is passed through; the argument after `-b` is a branch, never a config);
3. the log entries the launcher's `submit` appends to *its* `log.txt` during the
   call are copied to `job_launcher/log.txt`;
4. a warning when the checkout is not at the pinned commit.

Everything else — flags, refusals, queueing, `--baseline`, `-b`/`-r`/`-x`,
`-k` — is the launcher's, and `job_launcher/submit -h` prints both help texts. The
launcher keeps writing its own files (`configs/.gen/` for derived configs, its
own log) in its own checkout; that is by design, and the copy in `job_launcher/log.txt`
is the record this repository cites.

`job_launcher/status` is the launcher's `status` against this site file. Read-only.

**Finished windows stay open** (the launcher leaves them for post-mortem), and the
next launch can fail with tmux's `create window failed: index in use` before
anything is logged. Close the finished window first:

```bash
job_launcher/submit -k quant-091426      # the NAME of the finished job
```

**Where the checkout is found**, in order: `$LAUNCHER_DIR` in the environment, then
`LAUNCHER_DIR=` in `job_launcher/site.conf`. Neither set is an error.

## The pin

[`launcher.lock`](launcher.lock) records the launcher commit these wrappers were
tested against. The wrappers depend on three things about `submit` — that it
honours `SUBMIT_SITE`, sources configs after the site file, and appends to
`log.txt` next to itself — all of which have been stable, so a newer checkout
is a warning rather than a refusal. After running against a newer checkout and
finding the wrappers still correct, update the commit in the lock.

## What this does not do

- **Fork the launcher.** A fork would drift; the pin is the honest alternative.
- **Analyse results.** Results land on the host, where the drivers write
  them, one line per benchmark. What is read from them, and how, is the
  research project's business and is recorded in its ledger.
- **Run anything locally.** Every job runs on the host through the launcher.
