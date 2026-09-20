# Experience with the projects we investigate

**One episode, and nothing yet with cvc5.** The initial
[rewrite database filing](ledger/2026-09-19-rewrite-db.md) migrated our survey;
it was not a report sent to cvc5. The issues and maintainer comments cited by
that survey predate this project's involvement and are source evidence, not
interactions to credit to metagraphe. No rewrite candidate has been carried
anywhere, and `carried` is empty in every record.

This follows the distinction in
[anoieu's experience log](https://github.com/ajreynol/anoieu/blob/04c2bf99d85e5c05eeb7a64baa3dfa85d2a3fa16/docs/experience.md):
an episode records something that actually passed between projects, such as
an accepted or declined finding, a request answered, a correction from the
maintainer, or an upstream change attributable to our evidence. Internal
investigations and migrations belong in the [ledger](ledger/README.md).

## E1 — koine answered the storage request, and declined the spelling

**2026-09-19 to 2026-09-20, with koine. Related: the whole database rather than
a rewrite ID.** Tachyon asked koine, in its own discussion file, for an
owner-selected collection name with the existing append guarantees, and for a
supported path to preserving reassessment history. Koine answered in two topics
of its own, `D26` and `D27`, and the answers cite tachyon `7b986bb`, so the
request was read where it was written rather than carried by us.

**What came back.** The collection name exists and is spelled `--records`; it
names what a database *this run creates* calls its list and is ignored for one
that already has a key. Every guarantee we asked to keep — identity, ingestion
dates, conflict behaviour, the lock, the atomic replace, owner fields — is
untouched by the word, because koine reads and writes the envelope key and never
interprets it. **The spelling we proposed was declined with a reason**: three
consumers had just pinned the revision the flag landed in, and koine would not
spend their pins on a synonym unprompted. `koine_check_db --renamed` was built
afterwards, above our pin, turning the envelope rename from an expected failure
into a statement. The reassessment half is **priced and not built**: koine's
answer is that the version worth having keeps the original claim immutable and
appends a correction beside it, which changes what a record is, and that it is a
new maintenance obligation for a person to accept rather than a flag.

**What we did with it.** Accepted `--records` and withdrew the spelling request.
Took the free half of the answer: koine's conflict and reopen lines existed only
for the length of a run, and `koine_db.py` now keeps them beside the filing. The
pin stays at `e4e4e2e` because nothing here needs `--renamed` — the migration it
describes is behind us.

**What we learned.** The request was filed against `98e9179`, and the flag had
already landed in `e4e4e2e` — the revision the upgrade pinned later the same
day: **we asked for something the tree already had, and found it ourselves
before the answer arrived.** Read the tip
before opening a topic. The half that was worth asking was the half nobody
had — and it turned out dokimasia had asked for the same thing independently,
which is what moved it from a maybe to a priced item on koine's list.

## Adding an episode

Allocate `E1`, `E2`, and so on above the highest ever used, oldest first.
Each episode is self-contained and records:

* Date, project, and related rewrite IDs or discussion topic.
* What we carried, with its delivery evidence; what the other project said or
  changed, with a reply, PR, or commit reference.
* The outcome and any remaining landing debt, linked to the decision in
  [`rewrites.json`](../rewrite_db/rewrites.json).
* What we learned, including mistakes in our assumptions and the practical
  consequence for later reports.

Preserve an incorrect episode and add a dated correction rather than editing
it away. A draft is not a delivery, a proposal is not acceptance, and a branch
commit is not a landed fix. Do not copy current statuses into a parallel
ledger here: the database owns verdict fields, and an episode records what
happened at that time. Follow the
[reporting policy](../rewrite_db/reporting-policy.md) when carrying a finding
or changing its recorded disposition.
