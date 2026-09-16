# Experiment data retention

This directory tracks compact evidence needed for ongoing work: gap-set lists
and small processed summaries. Full `results-*.txt` and unprocessed
`stats-*.txt` job outputs are intentionally local-only because they are large
and reproducible from the recorded configuration, command, solver revision,
and benchmark set.

Ledger entries still name each raw artifact exactly. Use
`job_launcher/fetch` to restore an artifact from its execution host under that
name when recomputing a comparison. The ignore rules preserve such a local
copy without offering it to Git.

Do not ignore a derived artifact merely because it came from a job. If an
artifact is compact and necessary to continue the research—such as a gap set
used as the input to a follow-up experiment—track it.
