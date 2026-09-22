# elaphros

**A child research project of [tachyon](../../README.md)**, investigating what
cvc5 pays to produce a proof. It reads whatever it likes and writes only inside
this directory, and it is not part of what tachyon ships. Its charter is below;
what governs the subject rather than this account is under
[authority and working boundary](#authority-and-working-boundary).

**Planning status, 2026-09-19.** The [branch survey](docs/ledger/2026-09-18-branch-survey.md)
screens all 809 public heads of `ajreynol/cvc5` and characterizes 49 selected
branches against pinned upstream source, and the
[pipeline audit](docs/ledger/2026-09-19-pinned-main-pipeline-audit.md) reads
allocation, traversals and instrumentation directly in pinned main. Together
they support sixteen [research directions](docs/directions.md) and a
provisional [priority queue](docs/todo.md), with `ajreynol:unrewrite` and
`ajreynol:pfrConvert` explicitly highlighted by the maintainer. The last four
directions have no branch behind them. These are source observations and
hypotheses; no experiments, performance results or validated optimizations are
delivered.

The queue is published at
**<https://ajreynol.github.io/tachyon/elaphros/>**, built by [`reports/build`](reports/build)
from the documents below and refusing to state a figure they do not.
Start at the [documentation index](docs/README.md) for the register and evidence.

## The charter

**The question.** How can cvc5's performance in proof production mode be
optimized so that producing proofs adds little overhead to solving the same
problems without proofs?

The subject is the extra time and memory required to produce a usable proof:
work during search, restrictions that proof mode places on solving, and work
to construct, process and emit the proof. The project investigates concrete
optimizations and records the evidence for their effect.

**The goals, in order.**

1. **Define the comparison.** Fix a benchmark corpus with the human maintainer
   and record its inputs, the cvc5 revision and build, options, host, resource
   limits, proof format and granularity. State what counts as a complete proof
   and how it will be checked. Choose a measurable meaning of "little overhead"
   before judging success; no numerical target is set by this charter.
2. **Measure the cost of proof production.** Compare ordinary solving with
   proof mode enabled and with a complete proof requested and emitted. Record
   the effective solver settings in each arm, including changes required by
   proof mode. Measure time, peak memory, proof size and result status, keeping
   proof checking time separate. Preserve the commands and outputs so the
   comparison can be recomputed.
3. **Attribute the overhead.** Use profiles, counters and focused experiments
   to distinguish search changes, proof bookkeeping, construction,
   post-processing and serialization. Treat these as candidate causes until
   measured. Establish timer scopes before adding or subtracting them, and
   record costs the available instruments cannot separate.
4. **Test optimizations.** Start with the smallest experiment that can test a
   proposed explanation. Keep experimental patches, probes and results in this
   directory. Compare each candidate against the pinned proof-producing
   baseline and the ordinary-solving reference, retaining the same proof
   requirements. Check emitted proofs and repeat promising measurements before
   expanding the comparison to the agreed corpus. Record regressions and
   failures alongside improvements.
5. **Make the result usable.** Record the bottleneck, candidate optimization,
   reproduction procedure, measured savings, proof-validation evidence and
   remaining uncertainty. A useful result may also explain why an apparent
   optimization fails. A human decides whether to pursue a finding in cvc5;
   discovery here can continue independently of that decision.

**The wishue.** Proof production becomes inexpensive enough on the studied
workloads that users can routinely request proofs without a material
performance penalty. This is an aspiration, not a promise of zero overhead or
of a change to cvc5's defaults.

**Out of scope.**

- General solver tuning with no demonstrated connection to proof-production
  overhead, or taking over heuresis's quantifier search or metagraphe's rewrite
  search.
- Designing a new solver, proof calculus or proof format, or maintaining a
  production fork of cvc5. Focused optimization prototypes serve experiments.
- Optimizing proof checkers or developing their soundness proofs. Running a
  checker to validate a candidate's output is part of the evidence here.
- Claiming a speedup by omitting required proof work, weakening the agreed
  proof requirements, or silently adding trusted steps. Unsupported cases,
  incomplete proofs and validation failures remain visible in the results.
- Turning incidental correctness bugs into a separate bug-hunting effort.
  Record them for human review; a failed proof is never a successful
  performance result.
- Writing outside this directory, integrating with tachyon's imports, tests or
  CI, and building general infrastructure before a concrete experiment needs
  it.
- Publishing findings, filing issues, opening pull requests, or independently
  contacting other projects. Candidate feedback stays here until a person
  carries it through tachyon's reporting process.

## What an overhead claim means

For comparable completed runs, report both added seconds and the ratio of
proof-producing time to ordinary-solving time. Name the measured interval:
time to a solver answer and time through completion of proof output answer
different questions. Use the same timing measure in both arms; internal
timers, user CPU time and wall time are not interchangeable. Record output
handling and separate the overhead of profiling from the timing comparison.

Report the whole corpus's outcomes as well as ratios on the completed pairs.
Timeouts, memory exhaustion, unsupported configurations, missing proofs and
checker failures must not disappear through intersection filtering. SAT and
unresolved cases can reveal the cost of enabling proof mode, but do not supply
a completed refutation. Proof size and checker time help explain tradeoffs;
neither alone establishes lower production overhead. A configuration forced
by proof support is part of the observed cost, and any attempt to isolate its
effect needs a separately identified control.

Each finding needs a ledger entry with the exact inputs, revisions, commands,
raw artifacts, validation result, repetitions and analysis procedure. State
what cannot be reproduced from this checkout alone. A single run is not an
independent replication, and no measurement here establishes a claim about
all cvc5 workloads.

## Proposals

**A proposal is a change to cvc5 that a person could carry upstream.** Exactly
two things qualify: a **default-option change** — a cvc5 option whose *default*
this project proposes to change — or a **development branch** of cvc5 proposed
for merge into `main`. A probe, a counter, an experimental patch written to
answer a question: each can produce a proposal and none is one. Neither is a
change that buys its saving by weakening the proof requirement, for the reason
[out of scope](#the-charter) gives.

**Each proposal belongs to exactly one research direction**, listed in that
direction's table at the end of its entry in
[`docs/directions.md`](docs/directions.md) and nowhere else, so the union of
those tables is the register and no global copy exists to drift out of date.
Four columns, the same four heuresis uses: the branch or the option; the
upstream revision the branch is rebased to; ± LOC for a branch; and
± benchmarks solved on the corpus. The
[register's own section](docs/directions.md#proposals) defines them and what to
do with a change that touches two directions.

**Twelve of the sixteen tables name branches — twenty-three in all — and not
one carries a number.** A direction may own several, because competing designs
for one mechanism compete in the same table. Eighteen carry cvc5 `main@c2cc3caf`; the other five are 548 to
4379 commits behind it, read on 2026-09-22, and the last column names a corpus this
project does not have: goal 1 fixes it, and until then there is no
baseline to subtract. Goal 1 also settles what those three columns
are missing here — added seconds, the time ratio, proof size, checker time and
the validation outcome, which [an overhead
claim](#what-an-overhead-claim-means) requires and a solved count does not
carry. Recording a proposal stays separate from filing one, which is a person's
act through tachyon's reporting process.

## On the name

**Elaphros** transliterates Greek **ἐλαφρός**, "light in weight"
([LSJ](https://atlas.perseus.tufts.edu/dictionaries/entry/urn:cite2:scaife-viewer:dictionaries.v1:lsj-n33486/)):
the work seeks to make the burden of producing a proof light relative to
solving the problem, measured in time and memory.

## What this builds on

Tachyon's evidence supplies the experimental discipline and concrete cautions:

- Heuresis's [baseline caveats](../heuresis/docs/ledger/2026-09-15-baseline-caveats.md)
  show how an implicit SAT-backend choice and an incomplete option list can
  change a comparison. Elaphros records effective settings as well as requested
  ones, especially when enabling proofs changes what the solver can use.
- Its [attribution experiment](../heuresis/docs/ledger/2026-09-15-attribution-stats.md)
  demonstrates profiles guiding a focused search, while explicitly identifying
  missing attribution. The same entry records empty processed proof-summary
  headings. Such a summary is not evidence that a proof was produced.
- Tachyon's [solve wrapper](../../job_launcher/host/cvc5_solve.sh) accepts but
  ignores its signature and checker arguments. Its
  [recorded launcher run](../heuresis/docs/ledger/2026-09-17-self-contained-launcher-and-current-main.md)
  documents that limitation. Those arguments do not establish proof generation
  or validation, and the recorded solving results are not an elaphros baseline.
- The [profiler guide](../../docs/stats-profiler.md#choosing-a-partition)
  explains timer overlap, missing data and the limits of inferred accounting.
  These conventions guide attribution; timer names alone do not identify the
  proof overhead.

The existing quantified corpus is a possible source of inputs, not a selected
corpus for this project. No proof-production overhead measurement or
optimization result is inherited from these records.

## Authority and working boundary

As recorded in kanon's [name register](https://github.com/ajreynol/kanon/blob/main/docs/glossary.md),
read on 2026-09-18, **cvc5 owns CPC**, and **ethos's Eunoia manual remains the
authoritative language account**. cvc5's maintainers govern its implementation,
proof support and defaults. The chosen proof format's specification and
checker's documented contract govern validation. Pin those references in each
experiment. Elaphros's descriptions and hypotheses are an additional research
account; disagreements with an existing account are findings to investigate.

The project follows tachyon's [evidence limits](../../README.md#what-the-evidence-supports)
and [reporting discipline](../../docs/maintenance.md#findings-and-discussion).
It reads existing tools and records but imports no parent code. All project
code, patches, inputs and outputs stay under `tools/elaphros/`; experiments do
not write the parent's launcher configs or launch log. Nothing outside this
directory imports it, and removing the directory removes this project's page
from the site and leaves everything else in tachyon as it was.

**Two named exceptions.** In two respects this project is **not an island**,
both the parent's choice and both written down here so they are named exceptions
rather than drift. Tachyon's front page names and advertises it, which is a link
inward that a reader meets before this page. And the parent's site builder runs
[`reports/build`](reports/build) when that file exists, as it runs the tests in
[`tests/`](tests), to publish this project's queue at
<https://ajreynol.github.io/tachyon/elaphros/>; it reads nothing here itself,
and a project without a builder is listed and not published
([site.md](../../docs/site.md)).

What has been delivered so far is the charter, a source survey, a pipeline audit
and a planning queue — no corpus, no baseline and no measurement — so the
promotion decision is open and it is the human maintainer's.

**Status.** The human maintainer authorizes the proof-production performance
question and a source survey to set priorities. The current instruction is
planning only: do not run experiments. No corpus, numerical overhead target or
baseline is fixed. The [progress record](docs/progress.md) distinguishes the
completed source survey from the measurements still absent.
The human maintainer owns changes to scope and priorities and decides the
ending: graduation into its own repository, folding into the parent, or
retirement in place with the lesson recorded. That decision remains open.
