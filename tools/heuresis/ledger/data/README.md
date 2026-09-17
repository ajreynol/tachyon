# Experiment data retention

This directory tracks small processed summaries and the six gap lists linked
by the recorded experiments. Full `results-*.txt` and unprocessed `stats-*.txt`
remain local or on the execution host. New `gapset-*.txt` lists are ignored
by default; the ignore rule does not untrack retained evidence. Recomputing a
list requires the recorded raw results or access to the solver builds and
benchmark corpus, not just this checkout.

Ledger entries still name each raw artifact exactly. Use
`job_launcher/fetch` to restore an artifact from its execution host under that
name when recomputing a comparison. The ignore rules preserve such a local
copy without offering it to Git.

If a generated list is needed as input to a follow-up experiment, recreate or
fetch it locally under its recorded name. Record aggregate conclusions and
the generation command in the ledger. Retain a list deliberately when it is
needed as evidence for a recorded experiment; do not remove existing evidence
as part of routine housekeeping.
