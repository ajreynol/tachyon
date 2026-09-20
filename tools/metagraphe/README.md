# metagraphe

*Which useful rewrites is cvc5 missing, especially for strings and bit-vectors?*

A child research project for proposing useful cvc5 rewrites. Its result is a
concrete `lhs -> rhs` candidate, a small motivating example, its conditions, and the
evidence. A human may be inspired to pursue it independently, at their
discretion. Discovery continues without waiting for that follow-up.

## The charter

**The question.** Which equivalent forms could cvc5 use to simplify string and
bit-vector expressions, and where does its current rewriting miss a useful
opportunity? A candidate may be a new identity or an existing pattern with
weaker sufficient conditions, stated as an explicit rule. Reports concern
candidate rewrites; issues in the rewriter belong in separate investigation notes.

**The focus.** Strings and fixed-size bit-vectors are the primary search areas.
String length arithmetic, regular expressions, Boolean structure, and
conversions are included where they bear directly on those rewrites. Other
theories are secondary and considered only when a concrete candidate leads
there. This is a search for candidate simplifications, with other solvers and the
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
4. **Write the finding.** Preserve the proposed rewrite, its conditions,
   minimal input, actual and proposed outputs, validity evidence, and remaining
   questions. Keep leads without a concrete rule in the investigation ledger.

**The wishue.** A small set of findings inspires useful new cvc5 rewrites or a
research contribution about how to discover or apply them. That subsequent
work is a human's independent choice.

**Out of scope.** Shipping a general rewrite synthesizer, completing cvc5
patches, tuning the whole solver, and surveying every theory. Add instruments
only as concrete experiments require them. Incorrect solver answers encountered
along the way are recorded separately for a human to consider reporting.
Rewriter defects, proof-export problems, search-order issues, and work solely
on applying an already-known rule are outside the rewrite database's scope.
Publishing findings, filing issues, and opening upstream pull requests are
outside this project's discovery workflow.

**Publishing stance.** No paper is planned. Findings may motivate
independent human research; the project does not commit to developing it.

## What counts as a finding

Every filing proposes at least one exact rewrite with sorts and side conditions.
Validity and availability may still be unchecked. GitHub issues are sources
of motivation and evidence; a report or closure addresses the rewrite proposal,
independently of whether that issue is resolved.

**Standing rule: write every rewrite as `LHS -> RHS`, complex -> simpler.**
The human clarified the **lexicographic ordering: complex operators first,
structural term size last**. Eliminating costly operators may justify a larger
RHS. Record their precedence and explain the benefit and growth tradeoff;
size breaks ties in those operator counts. Check the JSON, RARE
declaration, and prose directions together, retaining sorts and side conditions.
Check duplication after substituting actual matched subterms and interactions
with other rules. Operator elimination and smaller syntax are rationales to
investigate, not measured speedups or proofs of termination.

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

The standing rewrite convention is the one above, under
[what counts as a finding](#what-counts-as-a-finding): every candidate is
written `LHS -> RHS`, complex to simpler, and a change to an existing direction
preserves the previous record in the ledger, reassesses the claims that depend
on the direction, regenerates the view and runs the repository checks.
The [rewrite database](rewrite_db/README.md) owns filed candidate records and
verdicts; [rewrites.md](rewrite_db/rewrites.md) provides a generated view.
Its [reporting policy](rewrite_db/reporting-policy.md) follows
anoieu's distinction between a candidate, a carried finding, and an explicit
closure. The [experience log](docs/experience.md) records actual exchanges with
other projects. The [documentation index](docs/README.md) leads to the search
map and work queue; the [ledger](docs/ledger/README.md) records source audits and
experiments. Keep project code, cases, and results inside this directory as
they become necessary. Nothing outside it imports or runs it, and deleting
`tools/metagraphe/` would leave the rest of the repository as functional as it
was.

**Named exceptions.** This project is **not an island** in the following
respects: tachyon's front page names and advertises it.
The human-requested issue survey lives at
[`docs/github-issues-rewrites.md`](../../docs/github-issues-rewrites.md), and its
launcher lives at
[`prompts/metagraphe_read_github`](../../prompts/metagraphe_read_github).
The human-requested benchmark assessment launcher is
[`prompts/metagraphe_compare_solvers`](../../prompts/metagraphe_compare_solvers);
its [guide](docs/benchmark-prompt.md) describes configurable corpus and solver
paths. It invokes an agent; `--help` lists agent selection options and
`--show-prompt` previews without launching.
These parent-level entry points are deliberate exceptions to keeping project
material inside this directory. The human also requested `rewrite_db/` as a
named exception to tachyon's usual child layout; `scripts/` holds its record
validator, Markdown renderer, and thin pinned-koine adapter; `tests/` checks
the filing, view, and shared-tool boundary.
The survey supplies source-audited
candidates;
it does not establish a solver performance finding. The promotion decision
remains the human maintainer's.

The project inherits tachyon's [discovery purpose](../../README.md) and the
measurement conventions of its shared [launcher](../../docs/job-launcher.md).
It inherits no rewrite findings or benchmark results. Remote benchmark jobs
can use the shared launcher once a corpus and experiment are defined; local
rewrite probes record their exact commands directly in the ledger.

## Status

**Authorized by the human maintainer**, with strings and bit-vectors as the
main focus. The first investigation is the
[GitHub issue survey](../../docs/github-issues-rewrites.md), requested on
2026-09-19. It screened 144 open issues and initially ranked ten families,
with ten parser-checked RARE drafts, existing coverage, and semantic
corrections to tempting rules. The [source audit](docs/ledger/2026-09-19-github-issues.md)
pins upstream cvc5. The [initial database filing](docs/ledger/2026-09-19-rewrite-db.md)
preserved the main candidates and additional triage rows as JSON. The later
[scope correction](docs/ledger/2026-09-19-rewrite-candidate-scope.md) keeps 14
concrete candidate families in the database and retains six triage records in
the historical ledger. The
[string benchmark comparison](docs/ledger/2026-09-20-string-benchmark-comparison.md)
of 2026-09-20 then supplied the first **matching executable baseline**: a cvc5
build identifying the source commit it was built from, a 200-input QF_SLIA
sample paired against Z3-Noodler, ten confirmed gaps, and two new candidates,
M-21 and M-22, whose absence was reproduced on that build. Their validity is
argued and instantiation-checked; **neither showed a runtime improvement on the
benchmark that motivated it**, and only M-22 showed one in a focused probe. Four
further confirmed gaps are recorded there as strategy or preprocessing
observations rather than rewrite candidates. A follow-up request then checked
the maintainer's own `re.loop` identity against an unmerged `reLoopImprove`
branch and probed for siblings, filing M-23 to M-25 and the
[study list](docs/cvc5-vs-z3noodler.md) of ten inputs worth attacking. **M-25,
a degenerate `str.replace_re_all` pattern, is the first candidate here with a
positive measured effect**: turning a repeatable 30 s timeout into 4 ms on a
1.3 kB input. The next task is to implement and measure it across its family.

The human maintainer decides whether the project eventually graduates into its
own repository, folds into the parent's work, or retires in place with an
account of what was learned. That decision is open, and it is theirs.
