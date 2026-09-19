# Experience with the projects we investigate

**No external episodes recorded as of 2026-09-19.** The initial
[rewrite database filing](ledger/2026-09-19-rewrite-db.md) migrated our survey;
it was not a report sent to cvc5. The issues and maintainer comments cited by
that survey predate this project's involvement and are source evidence, not
interactions to credit to metagraphe. The request for koine in tachyon's
[discussion file](../../../docs/discussion.md#d4--support-named-collections-for-metagraphes-rewrite-database)
is a local draft until a person carries it.

This follows the distinction in
[anoieu's experience log](https://github.com/ajreynol/anoieu/blob/04c2bf99d85e5c05eeb7a64baa3dfa85d2a3fa16/docs/experience.md):
an episode records something that actually passed between projects, such as
an accepted or declined finding, a request answered, a correction from the
maintainer, or an upstream change attributable to our evidence. Internal
investigations and migrations belong in the [ledger](ledger/README.md).

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
