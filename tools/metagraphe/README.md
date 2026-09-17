# metagraphe

*Which useful rewrites is cvc5 missing, especially for strings and bit-vectors?*

A child research project for finding concrete gaps in cvc5's rewriting and
simplification. Its result is a small, reproducible example of a missing
opportunity, with the rule or research question, its conditions, and the
evidence. A human may be inspired to pursue it independently, at their
discretion. Discovery continues without waiting for that follow-up.

## The charter

**The question.** Which equivalent forms could cvc5 use to simplify string and
bit-vector expressions, and where does its current rewriting miss a useful
opportunity? A candidate may be a missing rule, a rule whose conditions are
unnecessarily restrictive, or an interaction that prevents existing rules
from exposing a simplification.

**The focus.** Strings and fixed-size bit-vectors are the primary search areas.
String length arithmetic, regular expressions, Boolean structure, and
conversions are included where they bear directly on those rewrites. Other
theories are secondary and considered only when a concrete candidate leads
there. This is a search for cvc5 shortcomings, with other solvers and the
literature serving as sources of candidates.

**The goals, in order.**

0. **Pin the baseline.** Record the cvc5 commit, build, options, and exact
   rewriting or simplification entry point. Start with a small, recorded set
   of string terms and a separate set of bit-vector terms; preserve their
   origin or generation recipe.
1. **Find candidates.** Inspect existing rules and regression cases, mine
   benchmark terms, and explore small expressions in the
   [search areas](docs/directions.md). Record a proposed equivalent form and
   why it might help. Check what cvc5 already does before calling it missing.
2. **Check meaning and availability.** State all side conditions, sorts, and
   widths; seek counterexamples and a validity argument. Reproduce the
   baseline's output and inspect the relevant source. Distinguish a missing
   rule from one available under another option or later preprocessing pass.
3. **Establish why it matters.** Measure the simplification, its occurrence in
   inputs, or its effect in a focused experiment. Record the cost of applying
   it and possible growth or rewrite cycles. A smaller expression alone does
   not establish a solver speedup.
4. **Write the finding.** Preserve the minimal input, actual and proposed
   outputs, validity evidence, observed limitation, and remaining questions.
   A well-supported research question is useful even before a remedy exists.

**The wishue.** A small set of findings inspires useful new cvc5 rewrites or a
research contribution about how to discover or apply them. That subsequent
work is a human's independent choice.

**Out of scope.** Shipping a general rewrite synthesizer, completing cvc5
patches, tuning the whole solver, and surveying every theory. Add instruments
only as concrete experiments require them. Incorrect solver answers encountered
along the way are recorded separately for a human to consider reporting.
Publishing findings, filing issues, and opening upstream pull requests are
outside this project's discovery workflow.

**Publishing stance.** No paper is planned. Findings may motivate
independent human research; the project does not commit to developing it.

## What counts as a finding

Keep three questions separate in each candidate's record:

| question | evidence to record |
| --- | --- |
| Is the proposed rewrite valid? | Exact `lhs -> rhs`, side condition `P`, sorts and widths, proof argument or recorded solver checks, and their limits. |
| Is cvc5 missing the opportunity? | A pinned command or API call, the actual output, and relevant source locations; distinguish rewriting from later preprocessing and solving. |
| Why is it useful? | A concrete simplification, benchmark occurrences, measured cost or runtime effect, or a precise open question motivated by the observed behavior. |

For an equivalence check, test whether `P` and `lhs != rhs` can hold together.
An `unsat` result is evidence for the exact formula checked; preserve the query
and result and identify the solver used. A timeout or `unknown` leaves the
question open. Testing a few bit widths does not prove a rule for every width,
and testing bounded string lengths does not establish an identity for all
strings. Check that side conditions are satisfiable and available at the point
where the rewrite would apply. A condition known only during search needs to
be identified as such.

The semantic references are SMT-LIB's
[Unicode Strings](https://smt-lib.org/theories-UnicodeStrings.shtml) and
[FixedSizeBitVectors](https://smt-lib.org/theories-FixedSizeBitVectors.shtml)
theories, consulted on 2026-09-16. Record the specification revision used by
each experiment. Pay attention to empty strings, index bounds, conversion
error values, bit widths, signedness, overflow, shifts, and division by zero.
The specifications govern meaning; the pinned cvc5 implementation establishes
its observed behavior. This project's analysis remains a research account.

## On the name

**μεταγραφή** — transcription, writing in another form; the Greek dictionary
also traces it to an older sense of changing a text
([Dictionary of Standard Modern Greek](https://www.greek-language.gr/greekLang/modern_greek/tools/lexica/triantafyllides/search.html?dq=&lq=%CE%BC%CE%B5%CF%84%CE%B1%CE%B3%CF%81%CE%B1%CF%86%CE%AE)).
Here the desired change is in an expression's form while preserving its
meaning. **Metagraphe** is the working name.

## Working here

The [documentation index](docs/README.md) leads to the search register and
initial work queue. The [ledger](ledger/README.md) records source audits and
experiments. Keep project code, cases, and results inside this directory as
they become necessary. Nothing outside it imports or runs it, and deleting
`tools/metagraphe/` would leave the rest of the repository as functional as it
was.

**One named exception.** In one respect this project is **not an island**:
tachyon's front page names and advertises it, which is a link inward that a
reader meets before this page. That is the parent's choice, recorded here so it
is a named exception rather than drift. What has been delivered so far is the
charter, the search areas, and the evidence format — no baseline and no
findings. The promotion decision is therefore open, and it is the human
maintainer's.

The project inherits tachyon's [discovery purpose](../../README.md) and the
measurement conventions of its shared [launcher](../../docs/job-launcher.md).
It inherits no rewrite findings or benchmark results. Remote benchmark jobs
can use the shared launcher once a corpus and experiment are defined; local
rewrite probes record their exact commands directly in the ledger.

## Status

**Authorized by the human maintainer**, with strings and
bit-vectors as the main focus. The charter,
search areas, initial queue, and evidence format are in place. No cvc5 baseline
has been pinned for this project, no experiments have run, and no missing
rewrite has been established. The first task is the baseline and a small probe
from each primary theory.

The human maintainer decides whether the project eventually graduates into its
own repository, folds into the parent's work, or retires in place with an
account of what was learned. That decision is open, and it is theirs.
