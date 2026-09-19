# Metagraphe's rewrite database

[`rewrites.json`](rewrites.json) is the persistent record of rewrite candidates,
existing coverage, and rejected search directions. **These are proposals and
source observations, not established solver fixes.** Validity, availability,
and usefulness are separate assessments. Metagraphe owns those assessments;
koine supplies the append mechanics.

Browse [rewrites.md](rewrites.md) for a generated overview and each record's
terms, side conditions, RARE drafts, assessments, and evidence. It includes
existing coverage, exclusions, and any closed records as well as candidates.

The initial filing lifts the [GitHub survey](../../../docs/github-issues-rewrites.md)
into structured records. M-1 through M-10 retain their survey identities.
M-11 through M-20 record the survey's additional triage rows, including two
existing-coverage controls and two exclusions. A record groups a candidate
family; its individual identities live in `proposal.rewrites`. A family is
not a count of new rules or solved issues.

The JSON is the authority for filed claims and subsequent verdicts. The survey
remains the dated narrative behind the initial filing, the
[ledger](../docs/ledger/README.md) records investigations, and
[experience.md](../docs/experience.md) records actual exchanges with other
projects. Neither prose file maintains a second current status table.

## Format and identity

The top-level key is **`bugs`**, solely for compatibility with koine's current
writer. Its console also calls entries bugs; that wording does not classify
rewrite proposals as defects. No fake `bug` field is needed: explicit IDs are
supported. Tachyon's [request to koine](../../../docs/discussion.md#d4--support-named-collections-for-metagraphes-rewrite-database)
asks for a configurable collection name without changing the append guarantees.

| field | contract |
| --- | --- |
| `id`, `candidate` | Global `metagraphe:M-N` identity and local `M-N` label. Allocate above the highest ever used, including Git history; never reuse or derive IDs from mutable wording. |
| `schema_version`, `tool`, `owner` | Record format version (`1`), producer (`metagraphe`), and subject owner (`cvc5`). |
| `description`, `classification`, `priority`, `theories` | Original claim/title; `candidate`, `existing-coverage`, or `excluded`; agent-assigned priority 1–3, or null for controls/exclusions; affected theories. |
| `found_at`, `observed_on` | Full cvc5 **source** commit and observation date. They do not identify a matching executable or imply a solver run. |
| `origin` | Issue URLs and state at review, local survey/ledger references, the tachyon commit containing that survey, and supporting external/source links. File references are relative to tachyon's root. |
| `proposal.rewrites` | Term schemas with variables/sorts, `lhs`, `rhs`, conditions, and notation. An empty array explicitly means the lead has no exact rule yet. |
| `proposal.rare_drafts`, `application_context` | Literal RARE declarations, if available, and the facts/stage needed to apply the proposal. |
| `proposal.orientation` (optional) | `{kind: "lexicographic", operators: [...], reason: "..."}` declares complex operators in descending priority, followed by structural term size. Applies to all schemas and ordinary RARE drafts in that family. |
| `assessment` | Separate validity, availability, and value statuses, each with its reasoning. `argued` means a written argument, not a checked proof. |
| `checks` | Parser outcome and revision, plus solver/performance check status. A parser pass does not promote validity or establish default-solver reachability. |
| `cautions`, `next_step` | Counterexamples, applicability limits, and the next discriminating investigation. |
| `first_seen`, `last_seen` | Koine ingestion dates. Re-ingesting an old survey is not a fresh reproduction. |
| `carried` (optional) | Append-only list of `{to, on, evidence}` for actual deliveries; absence means none recorded. Existing issue links do not count as delivery by us. |
| `reassessments` (optional) | Dated `{on, reason, evidence, previous_record}` events linking the review and the retained original record. |
| `closed_*`, `awaiting_landing` (optional) | An explicit verdict under the [reporting policy](reporting-policy.md#closure). Absence means no closure recorded. Initial exclusions and existing coverage do not imply a maintainer verdict. |

Keep related issues in one record when they motivate the same identity. A new
issue is additional evidence, not automatically a new rewrite. A genuinely
different identity or corrected condition can receive a new ID that names the
old one in its evidence; preserve the original and record the decision in the
ledger. Current files and Git history are both part of the identity register.

## Orientation

Always write **`LHS -> RHS`, complex -> simpler**. The human clarified a
**lexicographic ordering: complex operators first, structural term size last**.
Reducing the count of a higher-priority operator may grow lower-priority
structure. Only when those operator counts tie does term size decide.

For example, M-1 declares `operators: ["str.replace_all"]`. Its cost is
`(replace_all count, term nodes)`: `(1, 6) -> (0, 7)` decreases lexicographically
despite adding a syntax node. Name each family's operator precedence and explain
the expected simplification and growth tradeoff in `reason`. These priorities
are proposals for review, not universal operation-cost measurements.

The validator checks this order for schemas and ordinary RARE drafts. Without
an explicit precedence, it checks structural size alone; this fallback is not
permission to introduce a costly operator merely to shorten the expression.
Size counts one node per operator application and variable/constant occurrence;
indexed literals and `zero(w)` each count as one constant. Conditions remain
premises. The generated view shows both sizes and the declared cost vectors.

This checks the written schema, not validity or runtime. Check duplication
after substitution and interactions with existing rules. Fixed-point RARE
rules require a separate review of their context and decrease.

The [operator-order clarification](../docs/ledger/2026-09-19-rewrite-operator-order.md)
supersedes the earlier size-only review, restoring four elimination directions
while retaining M-12's removal of `abs`. Both reviews retain previous records.
Direction-only corrections preserve the same equality and stable ID; update
direction-dependent assessments and syntax checks under the reporting policy.

## File new records

Prepare a curated JSON list in `scratch/metagraphe-filing/new.json` using the
fields above. Do not copy raw API responses or invent observation dates. Omit
ingestion dates for new records and let koine set them. For an exact repeat,
re-submit the original fields rather than replacing `found_at` with a newer
commit: changed content on a known ID is a conflict, not an update.

Use an available koine Git checkout containing the revision in
[`koine.lock`](koine.lock). The commands extract that **committed** writer,
so local changes in the koine working tree cannot silently alter the tool.
There is no automatic download or checkout mutation.

```bash
# Run from tachyon's root. Set this to an existing koine checkout.
KOINE=/path/to/koine
KOINE_REV=$(cat tools/metagraphe/rewrite_db/koine.lock)
mkdir -p scratch/metagraphe-filing
git -C "$KOINE" show "$KOINE_REV:bug_db_manager/koine_append_db" \
  > scratch/metagraphe-filing/koine_append_db.py

python3 tools/metagraphe/scripts/check_rewrite_db.py --filing \
  scratch/metagraphe-filing/new.json
python3 tools/metagraphe/scripts/check_rewrite_db.py
python3 scratch/metagraphe-filing/koine_append_db.py \
  scratch/metagraphe-filing/new.json tools/metagraphe/rewrite_db/rewrites.json \
  --dry-run
# Inspect the preview, then apply the same filing:
python3 scratch/metagraphe-filing/koine_append_db.py \
  scratch/metagraphe-filing/new.json tools/metagraphe/rewrite_db/rewrites.json
python3 tools/metagraphe/scripts/check_rewrite_db.py
python3 tools/metagraphe/scripts/render_rewrite_db.py
python3 scripts/check.py
```

The writer locks and atomically replaces the database. Its `.lock` and
temporary replacement files are ignored. Do not bypass locking. A malformed
dump is refused as a whole. Koine leaves original entries intact, adds new
ones, and only changes `last_seen` on a repeat. It reports conflicting existing
fields without overwriting them; **a zero exit code does not mean there were no
conflicts**. Additional fields on a repeat are not merged either.

This pin passed upstream [tests](https://github.com/ajreynol/koine/actions/runs/35450241649)
and [policy](https://github.com/ajreynol/koine/actions/runs/35450242015), checked
2026-09-19. Updating the pin is a deliberate reviewed change. The pinned
writer does not yet report closed entries seen again; inspect such repeats
manually. Newer local koine work was read as design context, not used as the
writer. The [filing ledger](../docs/ledger/2026-09-19-rewrite-db.md) records the
actual initial append and checks.

## Reassessment is a separate operation

An append does not revise an assessment, record a delivery, close a record,
or reopen it. For those operations, retain the original observation and add
dated evidence to the ledger; review the proposed metadata diff under the
[reporting policy](reporting-policy.md). Koine currently has no shared
evidence/closure writer. Do not work around its conflict protection by changing
IDs, replacing the database wholesale, or treating an absent entry in a later
scan as a fix.

`check_rewrite_db.py` validates local field/status requirements and evidence
references. CI runs it through the child test suite. It does not prove a
rewrite, audit whether a commit has landed, or prevent a human from editing an
old claim; preservation of historical content currently relies on reviewing
the diff.

## Refresh the readable view

After a filing or an evidence-backed metadata update, regenerate
[rewrites.md](rewrites.md) from the JSON; do not edit it directly:

```bash
python3 tools/metagraphe/scripts/render_rewrite_db.py
python3 tools/metagraphe/scripts/render_rewrite_db.py --check
```

Rendering validates the database first and only writes the Markdown view.
`--check` fails for missing or stale output without changing files. The child
test suite also checks freshness, so `python3 scripts/check.py` catches a view
that was not regenerated. Rendering preserves the source observation dates;
it does not refresh GitHub status or constitute a new investigation.
