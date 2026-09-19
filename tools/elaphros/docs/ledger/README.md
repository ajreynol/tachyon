# Evidence ledger

Source audits establish what code exists at pinned revisions. Experiment
records establish observed behavior under recorded conditions. These are
different evidence types; the ledger currently contains only source audits.

| date | record | type |
| --- | --- | --- |
| 2026-09-18 | [Public branches and initial research map](2026-09-18-branch-survey.md) | Source inspection; no solver execution. |
| 2026-09-19 | [Proof pipeline audit of pinned main](2026-09-19-pinned-main-pipeline-audit.md) | Source inspection of upstream main; no solver execution. |

For source audits, retain the queried repository, dated refs, upstream SHA,
selection method, merge bases and inspection limitations. Correct a dated
record with a new entry rather than silently replacing its evidence.

For future experiments, record the inputs, exact revisions/builds, requested
and effective options, proof contract, commands, host/resource limits,
repetitions, timing boundaries and validation results. Include timeouts,
missing or incomplete proofs, checker failures and regressions. Link the
relevant direction and distinguish observations from their explanation.

**Raw output is named here, not kept here.** Emitted proofs, solver stdout,
statistics dumps and checker transcripts are exactly what the repository
[retention policy](../../../../docs/maintenance.md#result-retention) keeps on the
execution host or under ignored `scratch/`, and a proof-production experiment
produces them by the gigabyte. An entry records the artifact's location, exact
name, derivation command and, where available, its checksum; the derived
measurements it supports may be retained when the entry identifies their source,
schema and use. Elaphros's own records stay in this project.

The [data index](../../reports/data/README.md) describes the retained source snapshots.
