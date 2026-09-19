# Koine tooling upgrade

**2026-09-19 — shared-tool integration.** The human requested a review of
koine's new tooling to simplify metagraphe's rewrite database workflow. Read
the clean local koine checkout at
[`e4e4e2e760197429ff182826ed9b7a90fea11633`](https://github.com/ajreynol/koine/commit/e4e4e2e760197429ff182826ed9b7a90fea11633)
and its committed database manager guide, append tool, closure checker, and
tests. Updated metagraphe's pin from `98e9179` to that revision. No upstream
CI result is claimed; the checks below ran locally.

## What moved to shared tooling

- The database now uses `{"rewrites": [...]}`. Koine preserves the existing
  envelope key and uses it in its summary diagnostics. Its `--records rewrites`
  selects the name for a new database; it does not rename an existing one.
- The [thin adapter](../../scripts/koine_db.py) replaces manual `git show`
  extraction and repeated validation/render commands. `append FILE --dry-run`
  validates both inputs and previews with the pinned koine writer; `append FILE`
  applies it and regenerates the view. Merge, conflict, locking, atomic write,
  and closed-record repeat handling remain upstream.
- `check-closure` uses pinned `koine_check_db` for preservation of the original
  claims, order, and record membership. It supplies our non-prefix closure
  fields `awaiting_landing` and `replacement_id`, after local metadata
  validation. Intentional prior-closure amendments require `--amended`.

The adapter extracts only the selected committed standalone program into a
temporary directory. It makes no network request and does not modify the koine
checkout. Missing pins or invalid checkouts fail rather than falling back to
HEAD, a dirty source file, or an installed command.

## What remains local

Koine deliberately does not know rewrite validity, side conditions, operator
precedence, priorities, evidence requirements, or closure vocabulary. The local
validator retains those checks. Koine also provides no Markdown renderer, so
our readable rule/RARE/evidence view remains local and unchanged by this migration.
There was no duplicate local append or closure-diff engine to remove; the
simplification is the owner workflow and delegation boundary, not a claim that
the total local source line count shrank.

`koine_close_db` can assemble and launch a closure investigation from owner
configuration and evidence instructions. We have no existing closure launcher
to replace and this request did not call for starting a new investigation.
The shared diff checker is useful independently, so no launcher/configuration
layer was added. General reassessment/history writing is still unimplemented
upstream; the existing snapshots and dated reassessments remain necessary.

The previous local discussion request is historical correspondence. No message,
closure decision about a candidate, or experience episode was manufactured by
adopting these tools.

## Migration and checks

Compared the database against tachyon
`82cf453ab92d89c3c4b9fa9f74f92cdf8ce92403`, its pre-migration revision:
the only text change was the first envelope key, `bugs` -> `rewrites`.
All 20 records, their order, IDs, dates, claims, RARE drafts, and reassessment
events compare equal. The generated Markdown also remained byte-for-byte equal.
Historical snapshots keep their original format. The older RARE reproduction
recipe now accepts either envelope without changing its rule checks.

Extracted `bug_db_manager/koine_append_db`, `bug_db_manager/koine_check_db`,
`tests/test_append_db.py`, and `tests/test_check_db.py` at the new pin under
ignored `scratch/metagraphe-koine-review/`. Both upstream suites passed,
including append locking/concurrency, repeat/conflict handling, collection
names, closure preservation, and amendments. Reproduce by extracting those
four paths with `git show REV:PATH`, preserving their relative layout, then:

```bash
python3 scratch/metagraphe-koine-review/tests/test_append_db.py
python3 scratch/metagraphe-koine-review/tests/test_check_db.py
KOINE=/path/to/koine python3 -m unittest discover -s tools/metagraphe/tests -v
```

The local suite passed all 25 tests with `KOINE` supplied. Its adapter cases
verify pin enforcement despite a newer HEAD and dirty working tree, preflight
refusal before koine sees invalid metadata, non-mutating previews, refresh only
after success, and explicit amendment flags. The optional real-tool case uses
a disposable owner Git repository: a new filing preserves all existing rows,
a valid closure with landing debt passes, a changed description fails, and
landing a prior fix requires `--amended`. Without `KOINE`, only that integration
case is skipped; normal repository checks require no neighboring checkout.

Running `check-closure` against this checkout's pre-migration `HEAD` refused
exactly the envelope rename: zero record changes and one file-shape change.
That is expected. A migration is not a closure; subsequent closure runs use a
committed baseline with the new envelope. General filings and reassessments
also must not be forced through this narrower check.
