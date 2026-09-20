# The ledger

Each entry records work actually performed. Search proposals belong in the
[candidate register](../directions.md).

| date | work | scope |
| --- | --- | --- |
| 2026-09-19 | [GitHub issue survey](2026-09-19-github-issues.md) | Open-issue screening, targeted source audit, and RARE syntax validation; no solver experiment. |
| 2026-09-19 | [Initial rewrite database filing](2026-09-19-rewrite-db.md) | Migration of the survey to JSON through koine, local metadata checks, and reporting policy. |
| 2026-09-19 | [Rewrite orientation correction](2026-09-19-rewrite-orientation.md) | Five equalities reoriented from complex to simpler, original records retained, and current RARE drafts re-parsed. |
| 2026-09-19 | [Complex operator precedence](2026-09-19-rewrite-operator-order.md) | Human clarification: lexicographic operator complexity before size; four elimination directions restored. |
| 2026-09-19 | [Koine tooling upgrade](2026-09-19-koine-upgrade.md) | Native rewrites collection, pinned append/closure adapter, preserved records, and shared-tool checks. |
| 2026-09-19 | [Candidate-only reporting scope](2026-09-19-rewrite-candidate-scope.md) | Six triage records archived, M-12 retained as an explicit proposal, and candidate-only filing requirements. |
| 2026-09-20 | [String benchmark comparison](2026-09-20-string-benchmark-comparison.md) | 200 paired QF_SLIA inputs against Z3-Noodler on a matching cvc5 build, ten confirmed gaps, two filed candidate rewrites (M-21, M-22), and four leads that are not rewrite gaps. |
| 2026-09-20 | [Bounded repetition and replace-all](2026-09-20-regex-loop-candidates.md) | The human's re.loop identity checked against an unmerged branch, two siblings found by probing, occurrence counts, and paired measurements; M-23, M-24 and M-25 filed. |

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

Store the minimal cases — the terms, the queries, the generation recipe — inside
this project and link them from the entry. **Raw solver output does not come with
them.** The repository
[retention policy](../../../../docs/maintenance.md#result-retention) keeps stdout,
result blocks, statistics dumps and backtraces on the execution host or under
ignored `scratch/`, and `scripts/check_data_retention.py` rejects recognizable
blocks in tracked text whichever project wrote them. Record the command, the
rewritten term or status it produced, and where the raw artifact can be
retrieved; that is what keeps a claimed number recomputable. A correction is a
new entry naming the old one; preserve the original experimental record.
