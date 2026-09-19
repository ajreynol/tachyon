# tachyon

**Find the opportunities to improve cvc5's performance, and back each one with
evidence a reader can recompute.**

Tachyon investigates cvc5 shortcomings worth a human's attention: concrete
performance problems and research questions grounded in observed limitations.
Its research projects keep their own questions, hypotheses, priorities and
evidence. A human may independently pursue a finding; that follow-up is outside
this repository's discovery work.

Two shared tools support the investigations. [`job_launcher/`](job_launcher/)
validates and launches remote experiments using the host scripts in this
repository, and records launches.
[`stats_profiler/`](stats_profiler/) reads local cvc5 statistics and produces
offline HTML, CSV, JSON and optional vector PDF reports. Research lives under
[`tools/`](tools/), with a charter and evidence in each project's directory.

What those projects have measured is published at
**<https://ajreynol.github.io/tachyon/>**, built from the recorded evidence in
this repository; the [site guide](docs/site.md) describes what may go there.

## Research projects

| project | question |
| --- | --- |
| [heuresis](tools/heuresis/README.md) | What do quantified benchmarks where z3 is much faster reveal about cvc5? |
| [metagraphe](tools/metagraphe/README.md) | Which useful string and bit-vector rewrites is cvc5 missing? |

Each project owns its charter, priorities and evidence. Its README records the
current findings and links to its investigation; the shared tools supply the
measurements.

## Run it

The timing profiler requires Python 3.9+ and no third-party packages:

```bash
python3 stats_profiler/profile.py /path/to/raw-stats.txt --output scratch/profile
```

Open `scratch/profile/index.html` in a browser. Use raw benchmark blocks from a
stats job, not a `-processed` proof summary. The
[profiler guide](docs/stats-profiler.md) covers timer selection, accounting,
missing data, exports and a worked experiment.

Remote jobs require Bash, SSH and a configured execution host; the launcher
and host scripts are included here:

```bash
cp job_launcher/site.conf.example job_launcher/site.conf
# Edit site.conf: host, benchmark paths and solver binaries.
job_launcher/deploy
# Configure ~/bin/heuresis/heuresis.conf on the host (JOBS at least).
job_launcher/checks
job_launcher/submit -n quant-cvc5.conf quant-z3.conf
job_launcher/submit    quant-cvc5.conf quant-z3.conf
job_launcher/status
```

The [launcher guide](docs/job-launcher.md) explains installation, configuration,
host deployment and result retrieval. Configs and the
[launch log](job_launcher/log.txt) are tracked; personal settings and fetched
raw results stay local. **Raw job output must not be committed**, including
processed text dumps and error logs; the [retention policy](docs/maintenance.md#result-retention)
defines the derived evidence that may be kept.

## What the evidence supports

A measurement describes the recorded solver revisions, options, corpus and
timeout. It is not a general cvc5 performance claim or an independent replication.
Research ledgers distinguish observations from hypotheses and name the artifacts
needed to recompute their numbers. Raw results and benchmark inputs may need to
be retrieved from the execution host; this checkout alone cannot reproduce every
measurement.

Timer coverage is accounting against a selected total, not proof that timers
form a disjoint or complete partition. Missing output cannot be reconstructed.
The [regression tests](tests/) and [profiler tests](stats_profiler/tests/)
exercise the local tools with synthetic inputs; they establish neither solver
correctness nor the research conclusions.

## On the name

ταχύς — *swift*. A tachyon is a hypothetical particle that travels faster
than light. The name fits a search for speed whose promising claims still need
measurement.

## Common questions

- **Where are the documents?** The [documentation index](docs/README.md) is the route to the guides and maintenance workflow.
- **Where can I see the measurements?** The [report site](https://ajreynol.github.io/tachyon/) publishes each project's recorded evidence; [site.md](docs/site.md) covers building and deploying it.
- **How do I maintain this tree or run CI locally?** Start at [maintenance](docs/maintenance.md).
- **Where does a solver finding go?** Record its evidence in the research ledger; [maintenance](docs/maintenance.md#findings-and-discussion) describes human review and the reporting route.
- **Who defines the shared repository rules?** Kanon keeps the [policy](https://github.com/ajreynol/kanon/blob/main/docs/policy.md); anoieu publishes its checker.

## How this repository is maintained

This repository is part of the **Eunoia ecosystem** and follows its shared
repository policy, kept by [kanon](https://github.com/ajreynol/kanon) in
[`docs/policy.md`](https://github.com/ajreynol/kanon/blob/main/docs/policy.md).

**Written by AI agents, under light human supervision.** A human directs the
work, reads what is published and decides what is filed; nobody vets the
internal design, and nothing reaches another project's issue tracker without
review. The [maintenance guide](docs/maintenance.md) describes that supervision
and its limits.
