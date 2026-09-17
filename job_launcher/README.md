# job_launcher/ — this repository's experiments, self-contained

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
[`host/heuresis.conf.example`](host/heuresis.conf.example) the first time and
never overwrites it afterwards — it is host-local in the same way `site.conf`
is machine-local. Set `JOBS` in it at least. Re-run `deploy` after changing
anything in [`host/`](host/).

The host also needs GNU `parallel`, `timeout` and `strip` on its `PATH`, and
the directories `~/analysis/data`, `~/analysis/stats` and `~/analysis/binaries`.

## What is where

| file | tracked | holds |
| --- | --- | --- |
| `site.conf.example` | yes | the template: every machine- and user-specific name, and the naming tables |
| `site.conf` | **no** | your copy of it. The only file with anything personal in it |
| `submit` | yes | validates configs, runs the remote checks, launches and logs jobs |
| `status` | yes | read-only view of what the host is doing |
| `deploy` | yes | installs `host/` to `HOST:~/bin/heuresis` |
| `fetch` | yes | copies results back from the host |
| `checks` | yes | the lint |
| `common.sh` | yes | finds the site file; sourced by `deploy` and `checks` |
| `host/` | yes | **the scripts that run on the host**: the drivers, the wrappers, `benchmark_binary`, and the host conf template |
| `configs/*.conf` | yes | one job each, written against names the site file resolves |
| `log.txt` | yes | every launch, appended by `submit` |

## The two sides

**Local.** `submit` reads a config, derives the job name, runs read-only
sanity checks over ssh, and opens one tmux window per launch. `-b BRANCH`
and `-r` are blocking instead, streaming progress and ending in an explicit
verdict. Everything it does is recorded in `log.txt`.

**Host.** [`host/`](host/) is installed to `~/bin/heuresis`, and every job runs
with `PATH=$HOME/bin/heuresis:$HOME/bin:$PATH`, so the drivers and wrappers a
job uses are the ones in this repository at the revision that launched it. A
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
`job_launcher/checks` refuses a config with a literal path in `DIR`, and
refuses any public file containing your username, home directory, git
identity, or anything `site.conf` names.

To add a benchmark set: one variable in `site.conf.example` (with a generic
placeholder value), one line in `set_prefix`, and configs that use the name.

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

- **Analyse results.** Results land on the host, one line per benchmark. What
  is read from them, and how, is the research project's business and is
  recorded in its ledger.
- **Run anything locally.** Every job runs on the host.
- **Own the host.** `deploy` writes only inside `~/bin/heuresis`. Anything else
  already on the host is left alone.
