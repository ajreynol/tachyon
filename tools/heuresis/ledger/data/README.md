# Experiment data retention

This directory tracks only small processed summaries. Full `results-*.txt`,
unprocessed `stats-*.txt`, and generated `gapset-*.txt` benchmark lists are
intentionally local-only. They are reproducible from the recorded
configuration, command, solver revision, benchmark set, and comparison
definition.

Ledger entries still name each raw artifact exactly. Use
`job_launcher/fetch` to restore an artifact from its execution host under that
name when recomputing a comparison. The ignore rules preserve such a local
copy without offering it to Git.

If a generated list is needed as input to a follow-up experiment, recreate or
fetch it locally under its recorded name. Record aggregate conclusions and
the generation command in the ledger rather than committing the full list.
