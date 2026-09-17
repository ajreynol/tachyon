# Maintaining tachyon

Start with the [front page](../README.md), kanon's
[policy](https://github.com/ajreynol/kanon/blob/main/docs/policy.md) and
[vision](https://github.com/ajreynol/kanon/blob/main/docs/vision.md), then the
charter and active queue of the research project you are working on. The
[documentation index](README.md) leads to the shared tool guides.

Tachyon owns its launcher, host scripts, timing profiler, and research records.
Solver implementations are maintained elsewhere. Keep experiments
inside their research directory, personal settings in ignored `site.conf`,
and transient output under ignored `scratch/`. A person sets research scope
and owns the priorities recorded in their name; an agent's ranking is separate.
Do not revise an experimental record to match a new result: add a correction
entry and update the claims that cite it.

## Checks

From the repository root, with Bash and Python 3.9+:

```bash
python3 scripts/check.py
```

This is the local definition of the `checks / tooling` CI job:

1. Run `job_launcher/checks` to parse launcher scripts and configs, resolve
   configs against the template, check host-script syntax and executability,
   and scan public files for local identity.
   The launch log and research ledgers are exempt from that identity scan.
2. Run unittest discovery in `tests/` and `stats_profiler/tests/`, and in each
   existing `tools/*/tests/` directory. Launcher tests use local stand-ins;
   nothing contacts a host or starts a benchmark job.

[`scripts/check.py`](../scripts/check.py) is the executable copy of this
sequence; it also checks that the two shared suite paths remain named here.
Green means these local regressions and lint pass. It does not validate the
remote installation, solver behavior, research conclusions or chart legibility.
Inspect rendered plots before citing them.

The separate [`anoieu / policy`](../.github/workflows/anoieu.yml) job runs the
checker at the `ANOIEU_REV` in that workflow. To reproduce it with a checkout
at that revision, set `ANOIEU_CHECKOUT` to its path and run:

```bash
python3 "$ANOIEU_CHECKOUT/scripts/policy_check.py" --root .
```

For a current local anoieu checkout, also run the same command with
`--policy-version 1`. As read on 2026-09-17, anoieu offers that stable interface
while kanon's adoption instructions still require a checker pin. Retain this
workflow's pin until the shared workflow is published and the adoption guidance
supports migration. A pin change requires green anoieu CI for the selected
commit. The [live discussion](discussion.md) records tachyon's answer to the
announcement. These conventions are reviewed against kanon's working tree on
2026-09-17, based on `dc6f56942fbc567abea76c562565557e5e7c6e19` with local
policy edits present; the checker pin identifies a separate artifact.
The pinned checker reports an advisory asking for a discussion `Status` field;
the current policy explicitly omits that field. Keep the current four-field
format. Contract 1 accepts it, and the pinned advisory does not fail CI.

## Findings and discussion

Keep a candidate's inputs, revisions, options, actual output, proposed
explanation and remaining uncertainty together. Numbers must cite recorded
evidence; a single host run is not independent replication. Raw artifacts may
be available only on the execution host. Say what is needed to recompute a
claim and do not claim a measurement has been rerun when only prose was read.

A human reviews what is published and decides what is carried to another
project. That review does not cover every line of code, validate the internal
design, or turn an agent's interpretation into a proved result. Findings about
another project's code use anoieu's
[reporting policy](https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-policy.md).
Questions and requests across tool boundaries use [discussion.md](discussion.md).
Read other trees freely; answer only topics whose `To:` names tachyon and which
the human instruction authorizes. Draft replies here; a person carries them.
When a discussion settles, preserve the decision in its governing document and
remove the whole topic. Allocate IDs above the highest ever used, including
removed topics in Git history.

Fix failures before completing maintenance. If a gate cannot be satisfied,
state the evidence and the exact blockage; the shared policy allows a human
override, recorded with its reason and the condition that would remove the
need for it.
