# Reporting and updating rewrite candidates

Metagraphe follows anoieu's
[reporting policy](https://github.com/ajreynol/anoieu/blob/04c2bf99d85e5c05eeb7a64baa3dfa85d2a3fa16/bug_db/reporting-policy.md)
and takes its append/closure model from the
[bug database guide](https://github.com/ajreynol/anoieu/blob/04c2bf99d85e5c05eeb7a64baa3dfa85d2a3fa16/bug_db/README.md),
read on 2026-09-19. This page records how those positions apply to rewrites;
the [database guide](README.md) describes the actual commands and format.

## What a record claims

A filed candidate may have only a source observation and an argument. Label
it accordingly. A valid identity is not necessarily absent from cvc5, an absent
declaration is not proof that a simplification is unreachable, and a smaller
term is not a measured speedup. Keep these assessments separate. Source pins,
parser checks, executable runs, and proof checks describe different evidence.
Silence from a search or checker establishes none of those claims.

Record the exact identity, conditions and sorts before calling something a
rewrite. A lead with no such identity remains explicitly unchecked. Preserve
counterexamples to rejected generalizations and already-covered cases. Rank
opportunities as an agent's assessment unless a person supplies the ranking.
Do not present database size or parser pass counts as solver quality, usefulness,
or success at reporting. The initial survey's screening counts remain dated
retrieval provenance, not a measure of the subject.

Every rewrite is oriented **`LHS -> RHS`, complex -> simpler**, following the
[standing rule](../README.md#what-counts-as-a-finding). Eliminating costly
operators may justify growth; use a lexicographic ordering of complex operator
counts, then structural term size. Record the precedence, rationale, and
growth tradeoff. Reversing a
valid equality preserves meaning but requires reassessing
matching, availability, usefulness, and interactions with existing rules.

## Preserve the observation

Routine filings are additive through the pinned koine writer. IDs survive
wording changes, new issue links, later source revisions, and closure. Only
ingestion time changes on a repeat; neither omission from a new scan nor an
issue becoming closed settles our record. A changed claim or new evidence
requires a separate dated reassessment linked to the original, never a silent
replacement of the first observation. When correcting the identity itself,
preserve the original, allocate a new ID, and explain the relationship. A
direction-only correction of the same equality, sorts, and conditions keeps
its family ID: retain the complete previous record in the ledger, link a dated
`reassessments` event, update direction-dependent claims, and recheck changed
RARE drafts. This is a reviewed correction, not a routine koine append.

Raw API responses, solver output and traces stay in ignored scratch space.
Curated claims, exact candidate terms, normalized verdicts and reproducible
source references are retained. Do not change `observed_on` or `found_at`
merely because the same material was ingested again.

## Carrying a finding

An issue authored by somebody else is an origin, not a delivery by metagraphe.
Before a candidate is carried to cvc5 as a finding, reduce and reproduce the
claimed gap on an identified build, check the semantic authority and available
evidence, and state the question that remains. A person decides what is sent.
Nothing here posts issues/comments, opens upstream PRs, or forwards a filing.

Record an actual delivery as a `carried` item with recipient, date, and an
evidence reference. A draft in tachyon's discussion file is still a draft.
An actual exchange or upstream action on our evidence also gets an episode in
[experience.md](../docs/experience.md). Old issue discussions consulted during
the survey do not become experiences of this project.

## Closure

Closure is an explicit verdict on the recorded claim, not a fresh search that
happened to find nothing. Keep the entry and its original evidence. Add
`closed_verdict`, `closed_on`, `closed_why`, and `closed_evidence` (nonempty list
of source, ledger, or reply references). Use anoieu's closed vocabulary:

| verdict | requirement for a rewrite record |
| --- | --- |
| `accepted and fixed` | A named implementation commit and evidence the claimed gap is addressed on that branch; `awaiting_landing` must name project, branch, and commit. |
| `fixed and landed` | A named commit on the default branch and a re-check establishing that the original gap is addressed there; no `awaiting_landing`. |
| `declined` | A maintainer's explicit decision, with its evidence. An open issue or lack of response is not a decline. |
| `intentional` | Evidence that the behavior is deliberate and the claim is ours to withdraw. |
| `not audited` | The claimed authority or ownership is elsewhere; identify where. |
| `withdrawn` | Our identity, validity argument, or missing-rule claim was wrong; retain the counterexample/correction. |
| `re-coded` | The finding survives under another ID; `replacement_id` names the retained replacement record. |

Both fix verdicts require a full `closed_commit`, the rechecked source revision
in `closed_checked_at`, and evidence of the actual rewrite/solver behavior.
RARE declaration presence or parser acceptance alone is insufficient.
`accepted and fixed` is outstanding landing work: periodically inspect the
named branch/commit, then record the landed change and remove the debt only
when it reaches the default branch. The local validator checks metadata shape,
not ancestry or runtime behavior.

Corrections and negative verdicts require evidence, not a fabricated fix commit.
Review closure metadata changes separately from the immutable original claim.
Before changing a prior verdict or reopening, preserve the old decision and
its evidence in a dated ledger entry and state why it changed. A later repeat
of a closed record requires review; it never automatically reopens it.
The [shared tooling request](../../../docs/discussion.md#d4--support-named-collections-for-metagraphes-rewrite-database)
asks koine for history-preserving reassessment mechanics. Until then, these
decisions are manually reviewed metadata changes, not append operations.

## What is enforced here

| position | current tier |
| --- | --- |
| Add once, preserve previous content, lock and replace atomically | Enforced by the pinned koine append tool. |
| Required record fields, separate assessment vocabularies, explicit closure vocabulary and landing debt | Enforced by the local validator and tests for retained JSON. |
| Validity, runtime reachability, performance, and actual landing | Evidence obligations; not established by the validator. |
| Original content preserved during manual reassessment | Review obligation; the append guarantee does not cover hand edits. |
| No automatic cross-project delivery | Structural: this workflow has no sender. |

These tiers describe metagraphe's mechanisms. They do not inherit anoieu's
stronger reproduction or landing checks merely by citing its policy.
