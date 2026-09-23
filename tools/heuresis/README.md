# heuresis

*Find the cvc5 shortcomings worth pursuing in the quantified benchmarks where
z3 is much faster.*

**Find the diamond in the rough.** A diamond is a concrete cvc5 performance
shortcoming or a research topic grounded in a cvc5 limitation. This project
investigates candidates and records enough evidence to make the promising ones
understandable and worth a human's attention. A human may then tackle one
independently, inspired by the analysis and at their own discretion. That is
an optional consequence of discovery, with no required handoff, acceptance,
or follow-up step in this project's workflow.

**A research project, in the shape of
[dokimasia](https://github.com/ajreynol/dokimasia)'s.** It has a question, goals
in a fixed order, a register of hypotheses with the evidence for each, a ledger
of what was run, and findings a human can assess independently. It makes no
claim about cvc5 that a row in the ledger does not back: a hypothesis is a
hypothesis until it has been run against the set, however good the branch
looks.

**An independent child project, with three named exceptions.** Heuresis keeps its
own notes and ledger in [`docs/`](docs), everything it publishes in
[`reports/`](reports), and uses the shared
[`job_launcher/`](../../job_launcher) for experiments. No code outside this directory imports it, and deleting
`tools/heuresis/` would leave the launcher and the profiler exactly as they are.
In three respects it is **not an island**, each the parent's choice and each
written down here so that they are named exceptions rather than drift. Tachyon's
front page names and advertises it, which is a link inward that a reader meets
before this page — it is advertised in Eunoia listings. The parent's site
builder runs [`reports/build`](reports/build) when that file exists, as it runs
the tests in [`tests/`](tests), to publish this project's evidence at
<https://ajreynol.github.io/tachyon/heuresis/>; it reads nothing here itself,
and a project without one is listed and not published
([site.md](../../docs/site.md)). And the parent's own index suite,
[`tests/test_site.py`](../../tests/test_site.py), names this project: it is the
one whose report the index must call a **measurement**, so deleting this
directory fails that suite rather than quietly changing what the index claims.

**What it has delivered, and who decides what comes next.** The set is named and
fixed, the gap is measured ([2026-09-14](docs/ledger/2026-09-14-baseline.md)), and the
register of directions is backed by whole-set statistics and option experiments.
The [bounded eager-instantiation experiment](docs/ledger/2026-09-16-bounded-eager-instantiation.md)
identifies 29 otherwise-unsolved gap cases as a candidate finding; a complete
per-benchmark attribution table is still absent. The human maintainer steers
this search. Any independent work inspired by a finding is their choice, and
discovery here can continue regardless.

## On the name

**εὕρεσις** — *finding out*; the noun of εὑρίσκω, whose perfect tense is
Archimedes' εὕρηκα. In the rhetorical tradition it is the first of the five
canons — *inventio* in Latin — the stage in which the arguments are found,
before any of them are arranged or delivered. That is exactly the stage this
project is at, and the discipline it most needs. The notes it starts from hold
some thirty candidate causes for the gap, several with a branch already
written, and the temptation is to start building. *Heuresis* is the work of
finding out which of them are the cause, and it comes first.

## The charter

**The question.** There is a set of quantified SMT benchmarks — from Verus and
related verification tooling — on which z3 is much faster than cvc5.
**Which cvc5 performance shortcomings or research questions does this gap
reveal, and what evidence makes them worth a human's further investigation?**

**Why this and not "make cvc5 faster".** Because the register already exists,
and it is long. The performance notes this project starts from
([`notes.md`](docs/notes.md)) list around thirty candidate causes, and the one that
has been measured — handling large `distinct` lazily — gave an average speedup
of 1.75 on the set at a 60-second timeout, from a single preprocessing change
([`h-25`](docs/notes.md#f--preprocessing)). That is the argument for attribution
before construction. The gap is probably a few large terms and a long tail, and
the branches already written may or may not be aimed at the large terms. Nobody
knows, because the gap has never been decomposed.

**The stance.**

- **One set, chosen by a person, then fixed.** The set is the whole subject.
  It is named once — a list, a location, a count — and every number in this
  directory is a number on that set at a stated timeout. Widening it is a new
  project, not a new row.
- **z3 is the oracle, not the target.** What z3 does on a benchmark is
  evidence about what the benchmark needs. The question is never *do what z3
  does*; it is *what does this benchmark need, and which solver supplies it*.
  Where the answer is a design z3 has and cvc5 lacks, the report says so and
  estimates the cost; it does not pretend that an option would do.
- **Evidence before construction.** Use profiles, counters, and focused
  experiments to establish a shortcoming and its significance. An option or
  experimental branch can help test an explanation; its existence alone is
  not evidence. A useful finding can emerge before the whole gap is attributed
  or a remedy is implemented.
- **Discovery has its own endpoint.** Record a finding when the evidence
  supports a specific shortcoming or a well-motivated research question.
  Further solver development and research may follow independently at a
  human's discretion. Continue the search without waiting for that choice.
- **Only measured claims.** Every number here comes from a row in
  [`ledger/`](docs/ledger) with a config in [`job_launcher/configs/`](../../job_launcher/configs)
  and an entry in [`job_launcher/log.txt`](../../job_launcher/log.txt) beside it. A claim
  without one lives in [`notes.md`](docs/notes.md) as a hypothesis, marked as one.

**The goals, in order.**

0. **Fix the set and the two baselines.** Name the benchmarks; the cvc5
   configuration under study (from the 2026-09-14 notes: `--user-pat=strict
   --no-cbqi --sat-solver=cadical`); the z3 version; the timeout. Numbered
   zero because it produces nothing on its own and everything else is
   meaningless without it. A gap between two solvers on an unnamed set is an
   anecdote.
1. **Measure the gap.** cvc5 and z3 on the set, same host, same timeout. The
   *gap set* is every benchmark where cvc5 is slower than z3 by more than a
   fixed factor, or times out where z3 does not. Two numbers come out: the
   size of the gap set, and one aggregate ratio.
2. **Attribute the gap.** On promising benchmarks in the gap set, determine
   where cvc5's time goes and which hypotheses the evidence supports. Build
   the attribution table from `--stats-internal`, profiles, and experiments;
   record the affected benchmarks and the scope actually measured. Use it to
   identify specific shortcomings and research questions. Full coverage of
   the gap set is not a prerequisite for a finding.
3. **Test promising candidates.** Use a focused experiment to distinguish
   explanations or establish significance. An A/B through `job_launcher/`
   may change one option or use an experimental branch; record what happened
   in the ledger, whether or not it helped. Expand to the full set when the
   claim needs it. A finished fix is not required to establish a shortcoming.
4. **Make the finding clear.** Write down the cvc5 shortcoming or research
   question, why it matters, the evidence and how to reproduce it, and what
   remains uncertain. Link it from the relevant research direction. A human
   should be able to understand it and decide independently whether to pursue
   it. Return to discovery without waiting for human follow-up.

**The wishue** — the outcome if this went unusually well, and not a
commitment. A finding here inspires a human to make a substantial cvc5
improvement or develop a research contribution. This project's contribution
is the discovery and its evidence; the subsequent work proceeds independently.

**Out of scope**, explicitly, because a research project with no boundary
becomes a general performance effort:

- **Benchmarks outside the set.** SMT-LIB at large, sledgehammer problems,
  strings. Some rows of the register — conflict-based instantiation most
  visibly — are large wins there and losses here, and the notes say so. A
  change that helps here and hurts elsewhere is reported as exactly that.
  Deciding a default is cvc5's.
- **Correctness.** A wrong answer or a crash found along the way is a bug and
  is recorded for a person to report to cvc5's tracker. It is not a row here.
- **Reimplementing z3.** The oracle is consulted, not copied.
- **Developing a finding into a finished solution.** Focused prototypes and
  measurements serve discovery. Owning the eventual fix, solver redesign, or
  publication is beyond this project's scope.
- **Sending anything upstream.** A branch and a measurement are in scope.
  Opening a pull request is a person's act, and nothing here does it.
- **Building instruments before the attribution asks for them.** A statistics
  pipeline, a profiler harness, an analysis library: each is built when a
  goal needs it and not before.

**Is there a paper in it?** A finding might motivate one: an attribution result,
a recurring performance failure, or an open question about a cvc5 design
limitation. Developing that into a research contribution is a human's
independent decision. The finding must make clear what the evidence establishes
and what remains a hypothesis.

## What makes a useful finding

A finding should stand on its own: name the specific cvc5 shortcoming or open
research question, explain why it matters on the observed benchmarks, and link
the relevant ledger entries, inputs, configurations, and reproduction commands.
Separate measured behavior from the proposed explanation, and state the
uncertainties, confounds, and limits of the evidence. An unresolved mechanism
can itself be the research question; say what observation motivates it and what
further experiment could distinguish the explanations.

Record the analysis with the relevant entry in [`docs/directions.md`](docs/directions.md)
and its supporting ledger entries. A fix, a complete decomposition of the gap,
and a human commitment to pursue the result are unnecessary. The purpose is to
give a human a solid starting point whenever they choose to use it.

## Proposals

**A proposal is a change to cvc5 that a person could carry upstream.** Exactly
two things qualify: a **default-option change** — a cvc5 option whose
*default* this project proposes to change — or a **development branch** of
cvc5 proposed for merge into `main`. An option passed on a command line is a
configuration, not a proposal; so is a counter patch, an instrument, or a
one-off A/B. Those produce proposals; they are not proposals.

**Each proposal belongs to exactly one research direction**, and is listed in
that direction's table at the end of its entry in
[`docs/directions.md`](docs/directions.md) and nowhere else. A direction may own
many: competing designs for one mechanism are separate proposals and compete in
the same table. Eager instantiation has three generations of branch behind it,
and they are three rows. The union of those
tables is the register; there is no second, global list to drift out of date.
Four columns: the branch or the option; the upstream revision the branch is
rebased to, which is what says whether the other two can be filled at all;
± LOC for a branch; and ± benchmarks solved on `quant-07-25`. The
[register's own section](docs/directions.md#proposals) defines them, the
baselines they are measured against, and what to do with a change that touches
two directions.

**Recording a proposal does not send it anywhere.** Filing and opening pull
requests stay a person's act, as out of scope above says. A proposal is this
project saying what it would file and attaching the evidence; when one lands,
it becomes a row in
[`progress.md`](docs/progress.md#pull-requests-to-cvc5-main). Proposals are
also not the point: a finding is the primary result, and a direction that
produces a good question and an empty table has done its job. As of 2026-09-22
the tables name **seventy-nine proposals**: twenty-two changes to the default
of an option that already exists on `main`, seven of them already measured, and
fifty-seven branches, every one of them within a commit of cvc5
`main@1c0b2066` and ready to measure
([the shared running list](../../docs/active-dev-branches.md)).

## The set

**`quant-07-25`**, the quantifier benchmark tree on the benchmark host, named
by a person on 2026-09-14: **6124 benchmarks** — 5207 in `sundance/`, 779 in
`verus-no-option/`, 138 in `slow/` — all Verus-generated, all `unsat` where
solved, none carrying options of their own. In `job_launcher/site.conf` it is
`QUANT_DIR`. Counted by the baseline run ([ledger, 2026-09-14](docs/ledger/2026-09-14-baseline.md)).

Fixed with it, for goal 0:

| | |
| --- | --- |
| timeout | 30 s per benchmark per solver, user time, on the host |
| cvc5 configurations | default (`-q`), the quantifier control (`-q --no-cbqi --user-pat=strict`), and the best measured configuration on `main@d7d03b082c` as of 2026-09-16: that control plus explicit `--sat-solver=cadical --ee-mode=central --ieval=off` |
| z3 | z3 4.15.4, **with the nine Verus options checked on 2026-09-15**: `auto_config=false smt.mbqi=false smt.case_split=3 smt.qi.eager_threshold=100.0 smt.delay_units=true smt.arith.solver=2 smt.arith.nl=false pi.enabled=false rewriter.sort_disjunctions=false`. The benchmarks carry no options of their own |
| gap set | unsolved by cvc5 and solved by z3, or both solved and cvc5 at least 10× slower with cvc5 taking at least 1 s |
| aggregate | PAR2 ratio, cvc5 over z3, over the benchmarks both runs report |

The gap factor, time floor and timeout are the defaults of [`gap`](reports/gap), the
script that reads results in this project. It compares the intersection of all
supplied runs; solver options and versions come from the inputs, not the script.
A ledger entry that uses different thresholds says so.

## How we would know it is working

The primary result is a useful finding: a specific cvc5 shortcoming or research
question supported well enough for a human to assess and pursue independently.
Its value does not depend on whether a human takes it up, a patch lands, or the
overall gap closes.

Two diagnostics guide the search:

> **the gap** — on the set, at the fixed timeout: the size of the gap set, and
> the aggregate ratio between the two solvers.
>
> **the attributed fraction** — of the gap set, what fraction is assigned to a
> row of the register with a ledger entry behind the assignment.

These numbers show the scale of the problem and how much has been explained.
They help prioritize discovery; a finding on a small part of the set can still
be the diamond.

### The operating constraint: feedback latency

A run of the whole set is the oracle and the slowest instrument. Ranked by how
fast each returns an answer:

| | instrument | latency | tells you |
| --- | --- | --- | --- |
| **1** | one benchmark, one profile | minutes | where the time goes on *this* input |
| **2** | one benchmark, `--stats-internal` | minutes | which subsystem's counters are large |
| **3** | the gap set under one option change | tens of minutes | whether a row is worth a full run |
| **4** | the set, A/B, at the fixed timeout | an hour or more | the number |
| **5** | the set at a long timeout | hours | what the timeouts were hiding |

Goal 2 starts on rows 1 and 2. Goal 3 uses the smallest experiment that can
resolve the question, expanding to rows 3 and 4 when needed to establish the
scope of a finding. Row 5 is used when timeouts obscure the answer. Goal 4
records the finding as soon as the evidence supports it.

## What it inherits, and where

| inherited | where it was established |
| --- | --- |
| the launcher: configs, site file, results format, host conventions | [`job_launcher/`](../../job_launcher) |
| the register of hypotheses, with each one's branch or pull request | [`notes.md`](docs/notes.md), a summary of performance notes dated 2026-09-14 |
| the research directions, with risk/gain estimates, flags, branches, z3's mechanisms and papers | [`docs/directions.md`](docs/directions.md), written 2026-09-15 from cvc5 and z3 source, the fork's 847 remote branch refs, and the literature |
| the configuration under study | [`notes.md`](docs/notes.md#the-configuration-under-study) |
| the measured number inherited from the notes | [`h-25`](docs/notes.md#f--preprocessing): 1.75× average, lazy `distinct`, 60 s |
| what the notes say z3 has that cvc5 does not | [`notes.md`](docs/notes.md#what-z3-has-according-to-the-notes) |
| the shape — charter, goals in order, wishue, ledger, three endings | dokimasia's [`tools/`](https://github.com/ajreynol/dokimasia/tree/main/tools) |

## Using it

[`docs/progress.md`](docs/progress.md) is the measuring stick: a history of
cvc5 `main` revisions on this set, the z3 targets they are measured against,
and the record of what this project has actually landed upstream. Read it
first — it is what everything else is trying to move, and it doubles as a
monitor for upstream changes that make these benchmarks worse.
[`docs/todo.md`](docs/todo.md) is the active short-term queue and top ten;
[`docs/directions.md`](docs/directions.md) is the registry it refers to.
The [documentation index](docs/README.md) covers the notes, guides and evidence.

```bash
cp job_launcher/site.conf.example job_launcher/site.conf       # once; QUANT_DIR is the set
job_launcher/checks
job_launcher/submit -n quant-cvc5.conf quant-z3.conf  # dry run: the commands, the output files
job_launcher/submit    quant-cvc5.conf quant-z3.conf  # the baseline, queued in one window
job_launcher/status
```

Results land on the host; a ledger entry ([`ledger/README.md`](docs/ledger/README.md))
records what was read from them and what it settled.

[`reports/build`](reports/build) builds the public pages from what this project
retained — the gap lists in [`reports/data/`](reports/data), the entries that cite them, and
the tables of [`docs/progress.md`](docs/progress.md) — and refuses a list no
entry cites. It computes its figures from those files rather than restating
them, so the page cannot say a number this project has not recorded. It writes
two: the [gap report](https://ajreynol.github.io/tachyon/heuresis/), and beside
it a [queue page](https://ajreynol.github.io/tachyon/heuresis/queue.html) that
publishes [`docs/todo.md`](docs/todo.md) — what is in flight, this project's own
ranking of the research directions, the separate ranking the maintainer owns,
and which branches of the fork are worth maintaining. The second keeps the two
rankings apart, because a page that merged them would misreport whose judgement
each one is:

```bash
tools/heuresis/reports/build --out scratch/heuresis-report   # then open index.html
```

For local comparisons, run `tools/heuresis/reports/gap z3=REFERENCE cvc5=RESULTS` on
complete result files. The parser accepts `.smt2` and `.smt2.gz` benchmark
headers and refuses incomplete blocks, duplicate paths, and an empty shared
cohort. It reports the intersection of all supplied runs. Positive factor and
timeout values and a nonnegative floor must be finite; reference times below
1 ms use 1 ms for the slowdown comparison. `--gapset FILE` rewrites that file
with benchmark, reference seconds, and comparison seconds or unsolved status.
Wrong-answer disagreements are flagged separately and excluded from the gap
list. [Local tests](tests) cover these boundaries without running a solver.

## Status

**Authorized by the human maintainer.** The fixed set is recorded in the
[baseline ledger](docs/ledger/2026-09-14-baseline.md). Comparisons use the
[nine-option Verus z3 baseline](docs/ledger/2026-09-15-z3-full-verus-options.md)
and [explicit CaDiCaL](docs/ledger/2026-09-15-sat-and-instance-order.md).
The latest recorded measurements are dated 2026-09-17, on `main@a07d513075`
— the cvc5 1.4.0 release ([ledger](docs/ledger/2026-09-17-cvc5-1-4-0-release.md)):

> **the gap** — PAR2 ratio **1.52** (cvc5 `--no-cbqi
> --user-pat=strict --sat-solver=cadical --ee-mode=central --ieval=off` over
> z3 4.15.4 with the nine recorded Verus options, 30 s); gap set **786** of
> 6124. The same configuration measured 35532.7 and a gap of 784 one revision
> earlier ([ledger](docs/ledger/2026-09-17-self-contained-launcher-and-current-main.md)),
> so the release moved this number by a tenth of a percent — inside the noise
> band. It lowers PAR2 13.6% versus the fixed control at the same revision
> (41191.8, in the same entry).
> The z3 baseline itself has 310 unknowns, so the ratio is not all cvc5
> progress, and **no gain so far is code**: every one comes from passing
> options that already exist ([progress.md](docs/progress.md)).
>
> **the attributed fraction** — **0**. Whole-set statistics now identify
> promising mechanisms, but the per-benchmark attribution table does not yet
> exist.

The published [report](https://ajreynol.github.io/tachyon/heuresis/) is built
from the retained gap lists rather than from this table. The newest lists are
from 2026-09-16, including the `best` list — 789 benchmarks, 460 cvc5-unsolved and 329 both
solved with cvc5 at least 10× slower
([ledger](docs/ledger/2026-09-16-combined-central-equality-and-evaluator-off.md)).
The report also includes that day's repeated current-main combined control
and eager-module-off control; their [retention notes](reports/data/README.md)
record the move into the report's data directory.
The 2026-09-17 runs retained no gap list, so the report does not move with the
rows above.

The fresh explicit-CaDiCaL control is ratio 1.76 with a gap of 1071
([ledger](docs/ledger/2026-09-16-entailment-filtering.md)). Central
equality alone cuts PAR2 9.6%, evaluator-off alone cuts it 3.1%, and together
they cut it 13.4% ([ledger](docs/ledger/2026-09-16-combined-central-equality-and-evaluator-off.md)).
The first whole-set statistics run also shows that the earlier 1122-case gap,
18.3% of the corpus, consumes 86.0% of cvc5 time and that E-matching consumes
27.8% within it ([ledger](docs/ledger/2026-09-15-attribution-stats.md)). This is
evidence for the next attribution work, not yet an attributed fraction.

The one number inherited from the notes (`h-25`) remains marked as inherited.
The register is [`docs/directions.md`](docs/directions.md): twenty-seven active
research directions, each with testing flags, fork work, the corresponding z3
mechanism, papers, and an argued risk/gain estimate. The evidence-sensitive AI
ranking and the separate human-maintainer ranking are in
[`docs/todo.md`](docs/todo.md).

There are three endings and the human maintainer picks: it graduates into its
own repository, it is folded into cvc5's own performance work, or it is retired
in place with a note saying what the attribution found. That decision is open,
and it is theirs. Going quiet is not one of them.
