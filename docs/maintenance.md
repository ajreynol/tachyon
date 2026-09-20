# Maintaining tachyon

Start with the [front page](../README.md), kanon's
[policy](https://github.com/ajreynol/kanon/blob/main/docs/policy.md) and
[vision](https://github.com/ajreynol/kanon/blob/main/docs/vision.md), then the
charter and active queue of the research project you are working on. The
[documentation index](README.md) leads to the shared tool guides.

Tachyon owns its launcher, host scripts, timing profiler, and research records.
Solver implementations are maintained elsewhere. Keep experiments
inside their research directory, personal settings in ignored `site.conf`,
and transient output under ignored `scratch/`.

**A research project normally keeps three directories**: `docs/` for
everything written, including its dated ledger; `reports/` for what it
publishes, including the programs that build it and the data they read; and
`tests/`. Anything else is a directory the shared layout has no purpose for,
and the ecosystem's tooling audit reports it as unregistered until somebody
records what it is.
The human-requested exception for metagraphe is `rewrite_db/` for its curated
rewrite records, generated Markdown view, and reporting/update policy, with
`scripts/` for validation, rendering, and the adapter to pinned koine tools.
Its [database guide](../tools/metagraphe/rewrite_db/README.md) records
the purpose and shared koine writer; its child test suite checks the retained
records and catches a stale view. Kanon's register carries it as a `database`
owned by metagraphe, beside the `webpage` rows for the two projects that
publish, so the exception is described rather than merely tolerated. It does
not change the other projects' layout.
A person sets research scope
and owns the priorities recorded in their name; an agent's ranking is separate.
Do not revise an experimental record to match a new result: add a correction
entry and update the claims that cite it.

## Result retention

**Do not commit raw text from job runs.** Keep solver stdout/stderr, benchmark
result blocks, statistics dumps, error sidecars, backtraces and build or
regression transcripts on the execution host or under ignored `scratch/`.
This applies throughout the repository, including text pasted into Markdown.
Small size, a `-processed` suffix, compression or a different extension does
not make a transcript retained evidence.

Commit launch metadata (commands, configs, revisions and final verdicts),
written conclusions and aggregate tables. Derived data may be retained when a
ledger entry identifies its source artifacts, derivation command, schema and
use in a recorded finding or report. Keep only the fields needed for that use:
benchmark identifiers, numeric measurements and normalized statuses are
appropriate; copied diagnostic messages and free-form output are not. The
heuresis gap lists and elaphros source inventories meet this distinction, and
both live in their project's `reports/data/` beside the builder that publishes
them, each named by a register the build compares against the directory.
Synthetic parser inputs in test code are allowed; do not use real run dumps as
test fixtures. Summarize a failure's category and affected benchmarks in the
ledger, and cite where its raw diagnostic can be retrieved.

Record the host location and exact artifact name, job/config, solver revision,
analysis command and, when available, checksum. A local scratch copy is
disposable; do not claim it makes an experiment reproducible. Raw data that
must remain recoverable needs an execution-host or external archive location.
Fetch into `scratch/results/`, then commit only the required derived evidence.

The root `.gitignore` reserves common dump filenames. The retention check in
`scripts/check_data_retention.py` rejects those names even when force-added,
and recognizable benchmark blocks or backtraces in public text files. It scans
tracked and unignored files and skips `.py` and `.sh` source when looking for
those blocks, because parser examples and synthetic fixtures live there; an
extensionless program is read like any other public text, so keep a sample
transcript out of one. It does not inspect Git history or decode archives, and
review still has to catch other transcript formats. Removing files from the current tree does not purge
old commits; rewriting published history is a separate maintenance operation.

## Checks

From the repository root, with Bash and Python 3.9+:

```bash
python3 scripts/check.py
```

This is the local definition of the `checks / tooling` CI job:

1. Run `scripts/check_data_retention.py` to check result retention as described
   above.
2. Run `job_launcher/checks` to parse launcher scripts and configs, resolve
   configs against the template, check host-script syntax and executability,
   and scan public files for local identity.
   The launch log, the research ledgers and the retained report data are
   exempt from that identity scan.
3. Run unittest discovery in `tests/` and `stats_profiler/tests/`, and in each
   `tools/*/tests/` directory that holds any. Launcher tests use local
   stand-ins; nothing contacts a host or starts a benchmark job.

**One of those cases is about the interpreter rather than this code.** Every
program here must parse on Python 3.9, which is what CI pins and what the tool
guides promise, while a developer's interpreter is usually far newer — so syntax
introduced after 3.9 passes locally and fails in CI. `tests/test_python_floor.py`
reads the source for the cases `ast` alone will not catch, a backslash or the
enclosing quote reused inside an f-string expression among them.

[`scripts/check.py`](../scripts/check.py) is the executable copy of this
sequence; it also checks that the two shared suite paths remain named here.
Green means these local regressions and lint pass. It does not validate the
remote installation, solver behavior, research conclusions or chart legibility.
Inspect rendered plots before citing them.

The [`reports / build`](../.github/workflows/reports.yml) job runs the index
suite and the builder suite of each project that has one, then builds the
published site from the recorded evidence on every push and pull request; pushes
to `main` also deploy it. Reproduce it with:

```bash
python3 scripts/build_site.py
```

It writes the ignored `site/` and contacts nothing. [site.md](site.md) describes
what may be published and what the builders refuse; a pull request builds the
site without deploying it.

The separate [`anoieu / policy`](../.github/workflows/anoieu.yml) job calls
anoieu's shared workflow at `main` and names **policy contract 1**. **This
repository is on the contract form, not a checker pin**: the contract fixes the
obligations and their severity, the implementation behind it moves on anoieu's
schedule, and there is no `ANOIEU_REV` here to bump. The cost of that choice is
that the job can turn red with nothing committed here, which within a contract
means a violation already in the tree has started being reported. Reproduce it
against a local anoieu checkout with:

```bash
python3 /path/to/anoieu/scripts/policy_check.py --policy-version 1 --root .
```

Name the version explicitly; omitting it selects 1 today and would keep doing
so after later contracts exist. Moving to a different contract is a deliberate
change to that workflow, never a way to turn a build green.

These conventions are reviewed against kanon `2e78d13`, a clean checkout read
on 2026-09-20, whose adoption instructions accept the shared workflow and a
checker pin alike and ask a repository to say which form it took. Contract 1
accepts this repository's four-field discussion format, which the shared policy
defines and which omits a `Status` field. Two things in that revision postdate
the arrangement this guide described: the policy now asks a member's maintenance note to link the
[ecosystem's human-maintainer list](https://github.com/ajreynol/kanon/blob/main/docs/policy.md#human-maintainers)
rather than name anybody, which the [front page](../README.md#how-this-repository-is-maintained)
does; and it says in as many words that a child project uses its parent's
discussion channel and keeps its own candidate feedback in a ledger under a name
of its own, which is where heuresis's
[upstream questions](../tools/heuresis/docs/upstream-questions.md) already sit.

## Findings and discussion

Keep a candidate's input references, revisions, options, result summary,
raw-artifact locations, proposed explanation and remaining uncertainty together.
Numbers must cite recorded evidence; a single host run is not independent
replication. Raw artifacts may
be available only on the execution host. Say what is needed to recompute a
claim and do not claim a measurement has been rerun when only prose was read.

A human reviews what is published and decides what is carried to another
project. That review does not cover every line of code, validate the internal
design, or turn an agent's interpretation into a proved result. Findings about
another project's code use anoieu's
[reporting policy](https://github.com/ajreynol/anoieu/blob/main/bug_db/reporting-policy.md).
Metagraphe's [local application](../tools/metagraphe/rewrite_db/reporting-policy.md)
separates rewrite validity, availability, and value, and identifies which parts
of its append and closure policy are mechanically checked.
Questions and requests across tool boundaries use [discussion.md](discussion.md).
Read other trees freely; answer only topics whose `To:` names tachyon and which
the human instruction authorizes. Draft replies here; a person carries them.
When a discussion settles, preserve the decision in its governing document and
remove the whole topic. Allocate IDs above the highest ever used, including
removed topics in Git history.
**A child project opens no topic and answers none**: what one of them needs from
another project is asked for there, in tachyon's voice, and what it would tell
the project it investigates waits in a ledger of its own — heuresis's
[upstream questions](../tools/heuresis/docs/upstream-questions.md) is the one in
use — until a person carries it.

Fix failures before completing maintenance. If a gate cannot be satisfied,
state the evidence and the exact blockage; the shared policy allows a human
override, recorded with its reason and the condition that would remove the
need for it.
