# Retained source evidence

These are **generated, dated source snapshots**, produced with Git queries and
a local Python inventory pass on 2026-09-18. They contain no benchmark results.
Snapshots are retained whole; a later audit writes new dated files rather than
rewriting these to match moved branches. Research interpretation belongs in
the [survey](../2026-09-18-branch-survey.md).

| artifact | contents |
| --- | --- |
| [ajreynol heads](2026-09-18-ajreynol-cvc5-heads.tsv) | Raw `git ls-remote --heads https://github.com/ajreynol/cvc5.git` output: SHA and full ref, 809 rows. |
| [branch tips](2026-09-18-branch-tips.tsv) | All 809 names, full SHAs, tip commit dates and subjects. |
| [source path screen](2026-09-18-source-path-screen.tsv) | All 809 names/SHAs, merge bases with pinned upstream, total changed source-file counts and matching proof/rewrite paths. Empty matches are retained. |
| [selected branches](2026-09-18-selected-branches.json) | Pinned upstream and 49 branch summaries: tips, dates, merge bases, ahead/behind counts, `src/` numstat and branch-only non-merge source commit subjects. |

The upstream SHA is `3dcc1ef5421ab62cc1ee9af52d70042ce6861af0`.
The selection heuristic tests each changed `src/` path against
`proof|/rewriter/|/infer_proof|/options/proof_`; 203 branches have a match.
The 49 selected records include some adjacent candidates without such a match.
Commit subjects are author-supplied labels, not assertions of performance or
correctness endorsed by this project.

## Recomputing the source comparisons

Use a full Git object database containing the pinned upstream and relevant
fork tips. For each recorded tip, the inventory operations are:

```bash
# Set these to the object database and exact SHAs recorded in the snapshot.
git -C "$audit_repo" show -s --format='%cs%x09%s' "$branch_sha"
git -C "$audit_repo" merge-base "$upstream_sha" "$branch_sha"
git -C "$audit_repo" rev-list --left-right --count "$upstream_sha...$branch_sha"
git -C "$audit_repo" diff --name-only "$merge_base_sha" "$branch_sha" -- src/
git -C "$audit_repo" diff --numstat "$merge_base_sha" "$branch_sha" -- src/
git -C "$audit_repo" log --no-merges --format='%h %cs %s' \
  "$upstream_sha..$branch_sha" -- src/
git -C "$audit_repo" diff "$merge_base_sha" "$branch_sha" -- src/
```

The count command returns **behind then ahead**; the human table deliberately
displays **ahead / behind**. Source diff counts exclude tests, signatures and
public headers. Inspect those too before evaluating build readiness or the
proof contract. A source-only screen cannot establish either.

This checkout retains metadata, not vendored solver history. Recomputing the
diffs requires obtaining the pinned Git objects; branch names alone may have
moved or disappeared. All named objects were available during this audit.
The scratch object database may reuse another local database and is disposable,
not a portable retained artifact. No binaries, inputs, proofs, timing output
or experiment harness have been produced.
