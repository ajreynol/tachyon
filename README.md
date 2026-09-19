# tachyon

**Find the opportunities to improve cvc5's performance, and back each one with
evidence a reader can recompute.**

Tachyon investigates cvc5 shortcomings worth a human's attention: concrete
performance problems and research questions grounded in observed limitations.
Its research projects keep their own questions, hypotheses, priorities and
evidence. A human may independently pursue a finding; that follow-up is outside
this repository's discovery work.

**[Read the published analyses](https://ajreynol.github.io/tachyon/).**

## Research projects

| project | question |
| --- | --- |
| [elaphros](tools/elaphros/README.md) | What does producing a proof cost cvc5, and where does that cost go? |
| [heuresis](tools/heuresis/README.md) | What do quantified benchmarks where z3 is much faster reveal about cvc5? |
| [metagraphe](tools/metagraphe/README.md) | Which useful string and bit-vector rewrites is cvc5 missing? |

Metagraphe's first investigation is the
[cvc5 GitHub issue survey](docs/github-issues-rewrites.md): ranked rewrite
candidates, RARE drafts, existing coverage, and the checks needed before
implementation. Refresh it with
[`prompts/metagraphe_read_github`](prompts/metagraphe_read_github)
(`--show-prompt` previews the task; `--help` lists the launch options).

Each project owns its charter, priorities and evidence. Its README records the
current findings and links to its investigation; the shared tools supply the
measurements. Research lives under [`tools/`](tools), with a charter, a queue
and the evidence in each project's directory.

Two shared tools support the investigations, and each has a guide.
[`job_launcher/`](job_launcher) validates and launches remote experiments using
the host scripts in this repository and records every launch; the
[launcher guide](docs/job-launcher.md) covers configuration, host deployment
and retrieving results. [`stats_profiler/`](stats_profiler) reads local cvc5
statistics and produces offline HTML, CSV, JSON and optional vector PDF
reports; the [profiler guide](docs/stats-profiler.md) covers timer selection,
accounting, missing data and a worked experiment. **Setup and usage
instructions live in those guides**, not here.

**Raw job output is never committed.** Solver output, statistics dumps and
error sidecars stay on the execution host or in ignored working space; the
[retention policy](docs/maintenance.md#result-retention) defines the derived
evidence that may be kept, and a check refuses the rest.

## What the evidence supports

A measurement describes the recorded solver revisions, options, corpus and
timeout. It is not a general cvc5 performance claim or an independent replication.
Research ledgers distinguish observations from hypotheses and name the artifacts
needed to recompute their numbers. Raw results and benchmark inputs may need to
be retrieved from the execution host; this checkout alone cannot reproduce every
measurement.

Timer coverage is accounting against a selected total, not proof that timers
form a disjoint or complete partition. Missing output cannot be reconstructed.
The [regression tests](tests) and [profiler tests](stats_profiler/tests)
exercise the local tools with synthetic inputs; they establish neither solver
correctness nor the research conclusions.

## On the name

ταχύς — *swift*. A tachyon is a hypothetical particle that travels faster
than light. The name fits a search for speed whose promising claims still need
measurement.

## Common questions

- **Where are the documents?** The [documentation index](docs/README.md) is the route to the guides and maintenance workflow.
- **How is the published site built?** [site.md](docs/site.md) covers what may be published, what the builders refuse, and how a project adds a report.
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
