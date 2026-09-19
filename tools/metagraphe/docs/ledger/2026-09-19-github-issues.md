# GitHub issues as rewrite candidates

**2026-09-19 — source audit and draft syntax check.** The human requested an
initial survey of cvc5 issues, a writeup at tachyon's root documentation level,
and a reusable prompt script. The resulting
[survey](../../../../docs/github-issues-rewrites.md) is the evidence record for
candidates M-1 through M-10; it contains the issue/comment/attachment links,
exact identities, semantic arguments, source references, and next checks.

## Work performed

Screened the 144 open issue titles returned by three GitHub REST pages
(`state=open&per_page=100&page=N`, excluding pull requests), then read the
concrete rewrite/performance reports identified in the survey. Also screened
100 of 274 `repo:cvc5/cvc5 is:issue rewrite` search results and all 61
`repo:cvc5/cvc5 is:issue rewrite in:title` results. Comments were fetched for
#12936, #11357, #11362, #10522, #11535, #9420, #11206, #9875, #11970,
#12815, #11151, #10520, and #11201. Empty comment lists were not treated as
missing evidence. The small attachments for #10522 and #11010 were inspected;
the survey names other inputs still requiring attachment-level analysis.

Read upstream source at
[`dbf176dfb71b272ffbfdee06888dace73fee5aa8`](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8),
retrieved from GitHub's commit endpoint and
[source archive](https://codeload.github.com/cvc5/cvc5/tar.gz/dbf176dfb71b272ffbfdee06888dace73fee5aa8).
Audited the relevant string/sequence, BV, and arithmetic RARE declarations
and C++ entry points linked in the survey. An available local executable
identified itself as modified and did not match this source baseline, so it
was not used to establish current solver behavior.

Parsed all **10 draft rules** extracted from the survey's `lisp` fences with
the pinned `rw_parser.Parser.parse_rules`, then called
`mkrewrites.validate_rule` on each. All passed. The exact reproduction command
is in the survey's validation section. No full rule-database C++ build,
machine-checked validity proof, or solver/performance experiment was run.

Fetched issue JSON, comments, attachments, and the unpacked source were kept
in disposable `/tmp/metagraphe-*` locations. They are not retained evidence
or an archive guarantee; the public links and source pin identify what to
retrieve again. GitHub issue status/comments may change after this date.

## Conclusions

Prioritize M-1 through M-4 for solver probes. The proposed singleton replacement
identity in #12936 needs a source-containment conjunct; #11362 needs correct
empty-needle handling. #10522's first assertion constrains length modulo
`2^64`, whereas #11010's attachment uses exact length and encodes reversal with
substrings. #10520 already has related RARE and C++ rules. These distinctions
are useful findings from the audit, without establishing any new default-solver
rewrite gap or performance improvement.

The [queue](../todo.md) now starts with matching executable baselines and
focused probes. The parent-level
[prompt launcher](../../../../prompts/metagraphe_read_github) can repeat the
survey; this audit did not launch another assistant or send anything upstream.
