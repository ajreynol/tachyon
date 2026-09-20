# Metagraphe's rewrite database

[`rewrites.json`](rewrites.json) is the persistent record of **candidate rewrites**,
including their later dispositions. **These are proposals and
source observations, not established solver fixes.** Validity, availability,
and usefulness are separate assessments. Metagraphe owns those assessments;
koine supplies append mechanics and checks the scope of closure edits.

Browse [rewrites.md](rewrites.md) for a generated overview and each record's
terms, side conditions, RARE drafts, assessments, and evidence. Every entry
proposes an explicit `lhs -> rhs` with sorts and conditions. GitHub issues
provide motivation; rewriter bugs, known-rule context/reachability work, and
leads without a concrete rule belong in the survey or ledger.

The initial filing lifts the [GitHub survey](../../../docs/github-issues-rewrites.md)
into structured records. Later records may instead come from a benchmark
comparison; those cite their corpus and ledger entry and carry no source issue. The [scope correction](../docs/ledger/2026-09-19-rewrite-candidate-scope.md)
retains 14 candidate families and archives six triage rows with their original
IDs and evidence. M-12 is retained for its concrete `abs`-elimination proposal;
its availability remains unchecked. A record groups a candidate
family; its individual identities live in `proposal.rewrites`. A family is
not a count of new rules or solved issues.

The JSON is the authority for filed claims and subsequent verdicts. The survey
remains the dated narrative behind the initial filing, the
[ledger](../docs/ledger/README.md) records investigations, and
[experience.md](../docs/experience.md) records actual exchanges with other
projects. Neither prose file maintains a second current status table.

## Format and identity

The top-level key is **`rewrites`**. Koine reads and preserves that name and
reports entries as rewrites. Explicit `metagraphe:M-N` IDs identify records;
no `bug` field or compatibility envelope is needed. The
[upgrade ledger](../docs/ledger/2026-09-19-koine-upgrade.md) records the migration
from `bugs`, preserving every record, ID, date, assessment, and history event.

| field | contract |
| --- | --- |
| `id`, `candidate` | Global `metagraphe:M-N` identity and local `M-N` label. Allocate above the highest ever used, including Git history; never reuse or derive IDs from mutable wording. |
| `schema_version`, `tool`, `owner` | Record format version (`1`), producer (`metagraphe`), and subject owner (`cvc5`). |
| `description`, `classification`, `priority`, `theories` | Proposed rewrite/title; classification must be `candidate`; agent-assigned priority 1–3; affected theories. |
| `found_at`, `observed_on` | Full cvc5 **source** commit and observation date. They do not identify a matching executable or imply a solver run. |
| `origin` | How the candidate was found. `kind` is `github-issue-survey` (issue URLs and state at review, the local survey and the tachyon commit containing it) or `benchmark-comparison` (a `corpus` string naming the sampled benchmark set, an empty `issues` list, and no survey). Both cite a `ledger` entry and may add supporting external/source links. File references are relative to tachyon's root. |
| `proposal.rewrites` | At least one term schema with variables/sorts, `lhs`, `rhs`, conditions, and notation. An issue or lead without an exact rule cannot be filed. |
| `proposal.rare_drafts`, `application_context` | Literal RARE declarations, if available, and the facts/stage needed to apply the proposal. |
| `proposal.orientation` (optional) | `{kind: "lexicographic", operators: [...], reason: "..."}` declares complex operators in descending priority, followed by structural term size. Applies to all schemas and ordinary RARE drafts in that family. |
| `assessment` | Separate validity, availability, and value statuses, each with its reasoning. `argued` means a written argument, not a checked proof. |
| `checks` | Parser outcome and revision, plus solver/performance check status. A parser pass does not promote validity or establish default-solver reachability. |
| `cautions`, `next_step` | Counterexamples, applicability limits, and the next discriminating investigation. |
| `first_seen`, `last_seen` | Koine ingestion dates. Re-ingesting an old survey is not a fresh reproduction. |
| `carried` (optional) | Append-only list of `{to, on, evidence}` for actual deliveries; absence means none recorded. Existing issue links do not count as delivery by us. |
| `reassessments` (optional) | Dated `{on, reason, evidence, previous_record}` events linking the review and the retained original record. |
| `closed_*`, `awaiting_landing` (optional) | An explicit verdict on the proposed rewrite under the [reporting policy](reporting-policy.md#closure). Absence means no closure recorded. The source issue's status is not this verdict. |

Keep related issues in one record when they motivate the same identity. A new
issue is additional evidence, not automatically a new rewrite. A genuinely
different identity or corrected condition can receive a new ID that names the
old one in its evidence; preserve the original and record the decision in the
ledger. Current files, ledger archives, and Git history are all part of the
identity register. Never reuse archived IDs; M-1 through M-20 remain reserved.

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
records about implementation defects or known-rule reachability alone; a
concrete candidate may still have unchecked validity or availability. Omit
ingestion dates for new records and let koine set them. For an exact repeat,
re-submit the original fields rather than replacing `found_at` with a newer
commit: changed content on a known ID is a conflict, not an update.

Set `KOINE` to a Git checkout containing the revision in [`koine.lock`](koine.lock).
The thin [adapter](../scripts/koine_db.py) reads the **committed** program at
that pin into a temporary directory. It never uses the installed command or
modified working-tree source, and does not fetch or change the koine checkout.
`--koine /path/to/koine` before the subcommand also selects a checkout.

```bash
export KOINE=/path/to/koine
python3 tools/metagraphe/scripts/koine_db.py append scratch/metagraphe-filing/new.json --dry-run
# Inspect the preview, then apply the same filing:
python3 tools/metagraphe/scripts/koine_db.py append scratch/metagraphe-filing/new.json
python3 scripts/check.py
```

The adapter validates both inputs before invoking koine and regenerates
`rewrites.md` after a successful append. A preview leaves both files unchanged.
It supplies metagraphe's paths and policy; locking, merging, identity handling,
and conflict/repeat reporting remain entirely koine's.

The writer locks and atomically replaces the database. Its `.lock` and
temporary replacement files are ignored. Do not bypass locking. A malformed
dump is refused as a whole. Koine leaves original entries intact, adds new
ones, and only changes `last_seen` on a repeat. It reports conflicting existing
fields without overwriting them; **a zero exit code does not mean there were no
conflicts**. Additional fields on a repeat are not merged either. Repeat
sightings of entries carrying `closed_*` are reported as reopen candidates;
koine preserves the verdict and does not reopen them.

The pin is [`e4e4e2e`](https://github.com/ajreynol/koine/commit/e4e4e2e760197429ff182826ed9b7a90fea11633).
Its append and closure-check suites and metagraphe's integration cases were
run locally; see the upgrade ledger. The
[initial filing ledger](../docs/ledger/2026-09-19-rewrite-db.md) remains the
record of the earlier pin and original append.

## Check a closure

After a closure-only edit, run:

```bash
python3 tools/metagraphe/scripts/koine_db.py check-closure
python3 tools/metagraphe/scripts/render_rewrite_db.py
python3 scripts/check.py
```

This validates metagraphe's metadata, then delegates the diff check to pinned
`koine_check_db`. By default it compares against `HEAD`; `--against REV` selects
another committed pre-closure baseline. It permits adding `closed_*` and the
owner's `awaiting_landing`/`replacement_id` fields, while rejecting changes to
claims, assessments, evidence, IDs, order, or membership. Use `--amended` only
for an intentional amendment of an existing closure after preserving its old
decision in the ledger. The local validator still enforces verdict/evidence
requirements; koine does not know that vocabulary.

The baseline must contain the same collection envelope. Scope migrations such
as the candidate-only correction change membership and are not closures. The `bugs` ->
`rewrites` migration is a separate reviewed change and correctly fails a
closure-only comparison to a pre-migration commit. Ordinary filings and
reassessments also have their own workflow; this is not a general CI diff gate.

## Reassessment is a separate operation

An append does not revise an assessment, record a delivery, close a record,
or reopen it. For those operations, retain the original observation and add
dated evidence to the ledger; review the proposed metadata diff under the
[reporting policy](reporting-policy.md). Koine supplies a closure diff checker,
but still has no history-preserving reassessment or closure writer. Do not
work around its conflict protection by changing
IDs, replacing the database wholesale, or treating an absent entry in a later
scan as a fix.

`check_rewrite_db.py` validates local field/status requirements and evidence
references. CI runs it through the child test suite. It does not prove a
rewrite or audit whether a commit has landed. General reassessments still
require retained previous records and a reviewed diff. Koine's checker
protects the narrower closure-only workflow; do not whitelist `proposal`,
`assessment`, or `reassessments` as closure fields to bypass its protection.

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
