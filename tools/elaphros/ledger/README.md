# Evidence ledger

Source audits establish what code exists at pinned revisions. Experiment
records establish observed behavior under recorded conditions. These are
different evidence types; the ledger currently contains only a source audit.

| date | record | type |
| --- | --- | --- |
| 2026-09-18 | [Public branches and initial research map](2026-09-18-branch-survey.md) | Source inspection; no solver execution. |

For source audits, retain the queried repository, dated refs, upstream SHA,
selection method, merge bases and inspection limitations. Correct a dated
record with a new entry rather than silently replacing its evidence.

For future experiments, record the inputs, exact revisions/builds, requested
and effective options, proof contract, commands, host/resource limits,
repetitions, raw outputs, timing boundaries and validation results. Include
timeouts, missing or incomplete proofs, checker failures and regressions. Link
the relevant direction and distinguish observations from their explanation.
All Elaphros records and future experiment artifacts stay in this project.

The [data index](data/README.md) describes the retained source snapshots.
