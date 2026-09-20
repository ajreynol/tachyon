# metagraphe — work queue

**Started 2026-09-16; updated 2026-09-20.** The human requested the initial
[GitHub issue survey](../../../docs/github-issues-rewrites.md), then the
[rewrite database](../rewrite_db/README.md), and then a
[string benchmark comparison](ledger/2026-09-20-string-benchmark-comparison.md)
against an external solver. That comparison supplied the project's first
executable baseline: a cvc5 build matching a named source commit, a 200-input
QF_SLIA sample, confirmed gaps, and two new candidates, M-21 and M-22. This
ordering is the AI agent's assessment within the human's string and bit-vector
focus.

File concrete candidate rewrites only, following the
[scope correction](ledger/2026-09-19-rewrite-candidate-scope.md). Existing-rule
controls support experiments in the ledger; they are not new rewrite findings.

| priority | next step | concrete output |
| ---: | --- | --- |
| 1 | Implement M-22 in `rewriteStarRegExp` and check it against the existing concat-star normalisation for termination, then measure it on the 4,192 QF_SLIA inputs that carry the pattern. | A rewrite probe and a measured before/after on a named subset, not only on the scratch pair. |
| 2 | Implement M-21's n-ary form beside `RE_CONCAT_TO_CONTAINS` and measure it on the 998 `20230329-denghang` inputs that carry the pattern, separating it from the `re.loop` elimination that dominates their runtime. | Evidence on whether the elimination pays off anywhere, given the null result on `instance51087`. |
| 3 | Probe M-1/M-2/M-3 and the BV candidate M-4 on this same pinned build, which the earlier survey could not do. | A baseline ledger entry with inputs, exact commands, and actual outcomes for the issue-derived candidates. |
| 4 | Re-run the comparison with `--benchmarks-dir` at `non-incremental/` so QF_S and QF_SNIA are actually sampled, and with a bit-vector corpus for the B-series areas. | Coverage of the configured logics and the second focus theory. |
| 5 | Decide what to do with the four non-rewrite gaps: quadratic word equations, `re.loop` unrolling, concatenation-encoded regular-expression containment, and nested case maps. | Either an exact rule that brings one of them into scope, or a recorded decision to leave it in the ledger. |

After an experiment, add its evidence to the [ledger](ledger/README.md),
file new observations through the database workflow, record reassessments
without overwriting the original claims, and revise this queue. Build a helper only when
the next experiment needs it. A human's independent decision to pursue a
finding is not a prerequisite for further discovery.
