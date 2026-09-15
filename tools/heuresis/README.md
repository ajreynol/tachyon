# heuresis

*What would make cvc5 fast on the quantified benchmarks where z3 is much
faster?*

**A research project, in the shape of
[dokimasia](https://github.com/ajreynol/dokimasia)'s.** It has a question, goals
in a fixed order, a register of hypotheses with the evidence for each, a ledger
of what was run, and two numbers that say whether it is working. It makes no
claim about cvc5 that a row in the ledger does not back: a hypothesis is a
hypothesis until it has been run against the set, however good the branch
looks.

**An island in this repository.** heuresis reads its own notes and ledger, and
it launches experiments through [`job_launcher/`](../../job_launcher/). Nothing else here depends
on it. Delete this directory and `job_launcher/` is exactly as functional — which is the
property that lets the launcher be reused for the next question.

## On the name

**εὕρεσις** — *finding out*; the noun of εὑρίσκω, whose perfect tense is
Archimedes' εὕρηκα. In the rhetorical tradition it is the first of the five
canons — *inventio* in Latin — the stage in which the arguments are found,
before any of them are arranged or delivered. That is exactly the stage this
project is at, and the discipline it most needs. The notes it starts from hold
some thirty candidate causes for the gap, several with a branch already
written, and the temptation is to start building. *Heuresis* is the work of
finding out which of them are the cause, and it comes first.

*The tempting alternative was* **τάχος**, *speed. It is the wrong word twice
over: the repository already carries that hope in its own name, and a project
named after its outcome has to explain on its first page why it has not
produced one. The name should say what the work is, and the work is finding
out.*

## The charter

**The question.** There is a set of quantified SMT benchmarks — from Verus and
related verification tooling — on which z3 is much faster than cvc5. Not
marginally: by enough that the reason must be structural rather than a matter
of tuning. **Which structural differences account for the gap, in what
proportion, and what is the cheapest change to cvc5 that closes most of it?**

**Why this and not "make cvc5 faster".** Because the register already exists,
and it is long. The performance notes this project starts from
([`notes.md`](notes.md)) list around thirty candidate causes, and the one that
has been measured — handling large `distinct` lazily — gave an average speedup
of 1.75 on the set at a 60-second timeout, from a single preprocessing change
([`h-25`](notes.md#f--preprocessing)). That is the argument for attribution
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
- **Attribution before construction.** No hypothesis is worked on until the
  attribution table says how much of the gap it could explain. A branch that
  exists but has never been run against the set is not evidence for anything,
  and the notes contain several.
- **Only measured claims.** Every number here comes from a row in
  [`ledger/`](ledger/) with a config in [`job_launcher/configs/`](../../job_launcher/configs/)
  and an entry in [`job_launcher/log.txt`](../../job_launcher/log.txt) beside it. A claim
  without one lives in [`notes.md`](notes.md) as a hypothesis, marked as one.

**The goals, in order.**

0. **Fix the set and the two baselines.** Name the benchmarks; the cvc5
   configuration under study (today, from the notes: `--user-pat=strict
   --no-cbqi --sat-solver=cadical`); the z3 version; the timeout. Numbered
   zero because it produces nothing on its own and everything else is
   meaningless without it. A gap between two solvers on an unnamed set is an
   anecdote.
1. **Measure the gap.** cvc5 and z3 on the set, same host, same timeout. The
   *gap set* is every benchmark where cvc5 is slower than z3 by more than a
   fixed factor, or times out where z3 does not. Two numbers come out: the
   size of the gap set, and one aggregate ratio.
2. **Attribute the gap.** For every benchmark in the gap set: where does
   cvc5's time go, and which row of the register explains it? One row per
   benchmark, one column per hypothesis class, filled from `--stats-internal`
   and profiles rather than from reading the benchmark. Most of the register
   will explain almost nothing. The result is the two or three rows that
   explain most of it, with the fraction beside each.
3. **Test the top row.** An A/B on the set through `job_launcher/`: the same
   configuration with one change — a branch, or an option — and a ledger
   entry saying what happened, whether or not it helped. Then the next row.
4. **Close the gap, or say what it would take.** Either the changes land on
   `main` and the number moves, or the attribution says the remainder is a
   design difference — eager instantiation, say — with an estimated cost.
   Either is the report.

**The wishue** — the outcome if this went unusually well, and not a
commitment. cvc5 within a small constant factor of z3 on the set, with the
changes on `main`, and the attribution table as the central figure of a paper:
for each structural difference between the two solvers, how much of the gap it
explained, measured.

**Out of scope**, explicitly, because a research project with no boundary
becomes a general performance effort:

- **Benchmarks outside the set.** SMT-LIB at large, sledgehammer problems,
  strings. Some rows of the register — conflict-based instantiation most
  visibly — are large wins there and losses here, and the notes say so. A
  change that helps here and hurts elsewhere is reported as exactly that.
  Deciding a default is cvc5's.
- **Correctness.** A wrong answer or a crash found along the way is a bug and
  goes to cvc5's tracker as one. It is not a row here.
- **Reimplementing z3.** The oracle is consulted, not copied.
- **Sending anything upstream.** A branch and a measurement are in scope.
  Opening a pull request is a person's act, and nothing here does it.
- **Building instruments before the attribution asks for them.** A statistics
  pipeline, a profiler harness, an analysis library: each is built when a
  goal needs it and not before.

**Is there a paper in it?** Possibly, and only from goal 2. An attribution —
*on this set, this fraction of the gap between two mature solvers is explained
by these three differences, and here is the measurement* — is a result whether
or not the gap then closes. A list of thirty ideas is not one, and neither is a
speedup with no account of why.

## The set

**`quant-07-25`**, the quantifier benchmark tree on the benchmark host, named
by a person on 2026-09-14: **6124 benchmarks** — 5207 in `sundance/`, 779 in
`verus-no-option/`, 138 in `slow/` — all Verus-generated, all `unsat` where
solved, none carrying options of their own. In `job_launcher/site.conf` it is
`QUANT_DIR`. Counted by the baseline run ([ledger, 2026-09-14](ledger/2026-09-14-baseline.md)).

Fixed with it, for goal 0:

| | |
| --- | --- |
| timeout | 30 s per benchmark per solver, user time, on the host |
| cvc5 configurations | default (`-q`), and the best known: `-q --no-cbqi --user-pat=strict` |
| z3 | a current z3 (4.15.4), **with the options Verus passes it**: `auto_config=false smt.mbqi=false smt.qi.eager_threshold=100.0 smt.delay_units=true smt.arith.nl=false`. Without them z3 times out on benchmarks it solves in a quarter of a second with them; the benchmarks carry no options of their own |
| gap set | unsolved by cvc5 and solved by z3, or both solved and cvc5 at least 10× slower with cvc5 taking at least 1 s |
| aggregate | PAR2 ratio, cvc5 over z3, over the benchmarks both runs report |

These are the defaults of [`gap`](gap), the one script that reads results in
this project; a ledger entry that uses different ones says so.

## How we would know it is working

Two numbers, and neither is "cvc5 got faster":

> **the gap** — on the set, at the fixed timeout: the size of the gap set, and
> the aggregate ratio between the two solvers.
>
> **the attributed fraction** — of the gap set, what fraction is assigned to a
> row of the register with a ledger entry behind the assignment.

The second is the project's own number and moves first. The first is the one
that matters and moves later, if the attribution was right.

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

Goal 2 lives on rows 1 and 2. Goal 3 starts on row 3 and ends on row 4. Row 5
is done once, for the baseline, and otherwise only when a row-4 result depends
on it.

## What it inherits, and where

| inherited | where it was established |
| --- | --- |
| the launcher: configs, site file, results format, host conventions | [`job_launcher/`](../../job_launcher/), and [run-dev](https://github.com/ajreynol/run-dev) |
| the register of hypotheses, with each one's branch or pull request | [`notes.md`](notes.md), a summary of performance notes dated 2026-09-14 |
| the research directions, with risk/gain estimates, flags, branches, z3's mechanisms and papers | [`docs/directions.md`](docs/directions.md), written 2026-09-15 from cvc5 and z3 source, the fork's 847 remote branch refs, and the literature |
| the configuration under study | [`notes.md`](notes.md#the-configuration-under-study) |
| the one measured number, and the only one | [`h-25`](notes.md#f--preprocessing): 1.75× average, lazy `distinct`, 60 s |
| what the notes say z3 has that cvc5 does not | [`notes.md`](notes.md#what-z3-has-according-to-the-notes) |
| the shape — charter, goals in order, wishue, ledger, three endings | dokimasia's [`tools/`](https://github.com/ajreynol/dokimasia/tree/main/tools) |

## Using it

[`docs/todo.md`](docs/todo.md) is the active top-ten queue;
[`docs/directions.md`](docs/directions.md) is the registry it refers to.

```bash
cp job_launcher/site.conf.example job_launcher/site.conf       # once; QUANT_DIR is the set
job_launcher/checks
job_launcher/submit -n quant-cvc5.conf quant-z3.conf  # dry run: the commands, the output files
job_launcher/submit    quant-cvc5.conf quant-z3.conf  # the baseline, queued in one window
job_launcher/status
```

Results land on the host; a ledger entry ([`ledger/README.md`](ledger/README.md))
records what was read from them and what it settled.

## Status

**Started 2026-09-14**, by an explicit human instruction, which is the only way
one of these begins. The same day, goal 0 and goal 1 were done: the set is
named and the baseline is in the ledger
([2026-09-14](ledger/2026-09-14-baseline.md)). As of it, the two numbers are:

> **the gap** — PAR2 ratio **4.34** (cvc5 `--no-cbqi --user-pat=strict` over
> z3 4.15.4 with Verus options, 30 s); gap set **1049** of 6124, of which
> 545 are cvc5 timeouts on benchmarks z3 solves.
>
> **the attributed fraction** — **0**. Nothing has been attributed yet.

The one number inherited from the notes (`h-25`) is still marked as
inherited. On 2026-09-15 the register was expanded into
[`docs/directions.md`](docs/directions.md): twenty-six active research directions,
each with the cvc5 flags that test it, what the fork has tried, what z3 does
in its code, the papers, and an argued risk/gain estimate. The active
recommendation is the ranked list in [`docs/todo.md`](docs/todo.md). Two caveats on the
baseline were found while writing it
([ledger, 2026-09-15](ledger/2026-09-15-baseline-caveats.md)).

There are three endings and a person picks: it graduates into its own
repository, it is folded into cvc5's own performance work, or it is retired in
place with a note saying what the attribution found. Going quiet is not one of
them.
