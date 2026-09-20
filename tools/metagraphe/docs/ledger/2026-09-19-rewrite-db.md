# Initial rewrite database filing

**2026-09-19 — migration and update-mechanics check.** The human requested a
rewrite database analogous to anoieu's bug database, plus an experience log.
The path uses the existing project spelling, `tools/metagraphe/rewrite_db/`;
no separate `tools/metagraph/` project was created.

## Source of the filing

The initial [JSON database](../../rewrite_db/rewrites.json) was curated from
[`docs/github-issues-rewrites.md`](../../../../docs/github-issues-rewrites.md)
at tachyon commit `d2ef784441e59059e44d23c6a594d216a2eb75ad`, backed by the
[source-audit ledger](2026-09-19-github-issues.md). Its cvc5 source baseline
remains `dbf176dfb71b272ffbfdee06888dace73fee5aa8`. This filing did not refresh
GitHub issue state, rerun a solver, or remeasure performance.

M-1 through M-10 preserve the original family identities. The ten additional
triage rows were assigned M-11 through M-20 in survey order:

| IDs | disposition at filing |
| --- | --- |
| M-1–M-10 | Original ranked candidate families. |
| M-11, M-12 | Existing coverage for #10520 and #9420; reachability/default behavior still requires checking. |
| M-13–M-18 | Additional leads from #10508, #11156, #11460, #11970, #10850, and #9417. |
| M-19, M-20 | Excluded rewrite directions from #12801 and #12353. |

These are inventory counts for the migration, not claims about useful rules,
solver coverage, or resolved issues. The records carry original source pins,
observation dates, issue links, proposed schemas and conditions, cautions,
separate assessments, and next steps. All ten RARE declarations were retained
verbatim with their original parser-check evidence. No record carries a
delivery or closure. Existing coverage and exclusion are local classifications,
not upstream acceptance or rejection.

## Policy and writer provenance

Read anoieu's `bug_db/README.md`, `bug_db/reporting-policy.md`, and
`docs/experience.md` at `04c2bf99d85e5c05eeb7a64baa3dfa85d2a3fa16`.
Metagraphe's [local policy](../../rewrite_db/reporting-policy.md) adopts the
distinction between filing, reassessment, delivery, and closure, and states
where our enforcement is weaker. The experience log has no episodes: the
survey read other people's conversations but delivered nothing to cvc5.

Used koine's committed `bug_db_manager/koine_append_db` at
`98e917993425eb2fec0047da4fa9ac0a3730627d`, now recorded in
[`koine.lock`](../../rewrite_db/koine.lock). Its tests and policy jobs were
successful for that exact commit, as linked in the
[database guide](../../rewrite_db/README.md). The local koine checkout had
uncommitted database-manager changes; the writer was extracted with `git show`
at the pin rather than run from that working tree. The committed writer has
locking and atomic replacement but predates the local reopen-report feature.

## Operations and observed results

The disposable producer filing is `scratch/metagraphe-filing/github-issues.json`;
the extracted writer is `scratch/metagraphe-filing/koine_append_db.py`.
The scratch preparer assembled curated metadata and extracted the original
RARE fences; it is not a reusable producer or a retained artifact. The
committed JSON, survey pin, and migration checks preserve the result.

```bash
python3 tools/metagraphe/scripts/check_rewrite_db.py --filing \
  scratch/metagraphe-filing/github-issues.json
python3 scratch/metagraphe-filing/koine_append_db.py \
  scratch/metagraphe-filing/github-issues.json \
  tools/metagraphe/rewrite_db/rewrites.json --date 2026-09-19 --dry-run
python3 scratch/metagraphe-filing/koine_append_db.py \
  scratch/metagraphe-filing/github-issues.json \
  tools/metagraphe/rewrite_db/rewrites.json --date 2026-09-19
python3 tools/metagraphe/scripts/check_rewrite_db.py
python3 -m unittest discover -s tools/metagraphe/tests -v
```

The preview identified twenty new records without conflicts; the append filed
them with `first_seen` and `last_seen` equal to the ingestion date. Repeating
the exact filing at the same date preserved the database byte-for-byte.
On a temporary copy, submitting an existing ID with a synthetic changed
description reported a conflict and preserved the original. A dump repeating
the same ID twice was refused without mutating that copy. These are writer
mechanics checks, not cvc5 experiments.

The child test suite validates the retained metadata, checks that the original
issue references and RARE drafts survived migration, and rejects misleading
parser/proof statuses, missing evidence, duplicate identities, and invalid
closure/debt combinations. It does not enforce historical immutability under
manual edits, prove an identity, or establish that a fix landed.

A local request for koine, opened in tachyon's discussion file on this date,
asks for named collections and a history-preserving reassessment interface.
The current `bugs` envelope is a documented compatibility choice. Nothing was
sent to another repository; no upstream issue or change was opened.

**Follow-up, 2026-09-20.** Koine answered both halves, and the topic is closed
and removed. The collection name is `--records`, taken by the migration in the
[koine upgrade](2026-09-19-koine-upgrade.md), so this entry's envelope sentence
describes the state on 2026-09-19 and not the file today; the reassessment
writer is priced and not built. What that settles is in the
[database guide](../../rewrite_db/README.md#format-and-identity) and the
[reporting policy](../../rewrite_db/reporting-policy.md#closure), and the
exchange itself is [episode E1](../experience.md).
