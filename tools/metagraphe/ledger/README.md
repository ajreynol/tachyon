# The ledger

**No experiments or source audits recorded yet.** Each entry records work
actually performed. Search proposals belong in the
[candidate register](../docs/directions.md).

## An entry

Use `YYYY-MM-DD-<subject>.md` and record:

1. **Question and scope.** The candidate or search-area ID; whether this is a
   source audit, equivalence check, rewrite probe, or performance experiment.
2. **Provenance.** cvc5 commit, build and options, semantic specification
   revision, any other solver versions, and the exact input or corpus manifest.
   For generated terms, include the generator revision, bounds, and seed.
3. **Reproduction.** Exact commands or API calls, limits, and the paths to
   saved inputs and raw outputs. For source audits, use commit-pinned file and
   symbol references. For remote runs, cite the shared launcher's config and
   launch entry. Keep machine-specific setup out of reusable commands.
4. **Observed results.** Actual rewritten terms, counterexamples, proof or
   solver results, and any measured structural or runtime changes. Name the
   script or calculation behind each aggregate.
5. **Conclusion and limits.** What this establishes about validity,
   availability, or usefulness, and what remains open. An inconclusive result
   is recorded as such.

Store the minimal cases and raw results inside this project and link them from
the entry. Keep evidence sufficient to recompute claimed numbers. A correction
is a new entry naming the old one; preserve the original experimental record.
