# heuresis — active top ten

This is the evolving answer to one question: **what should an AI agent or a
human work on next?** It assumes the hypotheses, evidence, flags, branches,
papers, and effort arguments in [`docs/directions.md`](docs/directions.md) and
refers to them by `R1`–`R27`. That document is the registry; this one is the
queue.

**Updated.** 2026-09-15.

## How to maintain this list

- Keep exactly ten entries, in priority order. Rank is the recommendation.
- Move an entry when evidence changes its expected value, not merely because
  somebody has started it. Record completed experiments in [`ledger/`](ledger/)
  and replace them here with the next concrete action.
- `ready` means work can begin now, `waiting` names work whose prerequisites
  are earlier in the list, and `conditional` means attribution must justify it.
- `Who` names the best lead, not an exclusive owner. An agent can prepare code,
  configs, analysis, and ledger drafts; a human chooses the fixed set, grants
  access to the benchmark host, and decides whether work goes upstream.
- Every effort is an argued `Low`, `Medium`, or `High` implementation *Risk*
  paired with expected project *Gain*. Queue entries judge the immediate task;
  RX entries judge the eventual solver change. These are priors and must move
  when measurements arrive.

## 1 — Correct and freeze the two baselines

**Status.** `ready`

**Who.** `agent + human`

**Directions.** R13, R24

**Effort.** Low Risk / High Gain — these are config and ledger changes, and
every later comparison is misleading until the baselines match the intended
CaDiCaL and Verus configurations.

**Work.** Rerun cvc5 with CaDiCaL despite incremental mode, and rerun z3 with
all Verus options. Keep the same 6,124 inputs, 30-second timeout, host, and gap
definition.

**Done when.** Both corrected runs have configs, launcher log entries, result
files, and ledger rows, and the README names them as the comparison baselines.

## 2 — Settle the remaining configuration facts

**Status.** `ready`

**Who.** `agent`

**Directions.** R23, R24

**Effort.** Low Risk / Medium Gain — this is source inspection and
documentation, but it prevents a default from being tested or credited twice.

**Work.** Establish whether `--term-db-mode=relevant` is already selected by
the effective defaults, and record the exact options Verus passes to cvc5.

**Done when.** `notes.md` and the baseline ledger distinguish explicit flags,
effective defaults, and options supplied by Verus, with source locations.

## 3 — Split the 545 timeouts into slow and stuck

**Status.** `ready`

**Who.** `agent + human`

**Directions.** R26

**Effort.** Low Risk / High Gain — one longer run has little technical risk and
separates finite slowdowns from non-progress, which changes both profiling and
the likely remedy.

**Work.** Run the corrected cvc5 baseline on the timeout subset at 20 minutes.
Use the result to distinguish finite slowdowns from matching loops or other
non-progress behavior before choosing profiles.

**Done when.** Every current timeout is classified as solved at long timeout or
still stuck, and both counts are recorded in the ledger.

## 4 — Build the attribution extractor

**Status.** `ready`

**Who.** `agent`

**Directions.** R26

**Effort.** Medium Risk / High Gain — counter formats and partial runs make a
trustworthy extractor nontrivial, while its output is the evidence needed to
choose among all high-risk solver changes.

**Work.** Read cvc5 `--stats-internal` and diagnostic output per benchmark and
emit the counters named by R1–R27: instantiation rounds and totals, E-matching
time, duplicate reasons, lemma counts, decisions, datatype splits, arithmetic
lemmas, preprocessing time, and parser measurements.

**Done when.** One command produces a stable row per benchmark, rejects missing
or malformed input, and has fixture tests for solved, timeout, and partial runs.

## 5 — Measure SMT-LIB parser cost and test the existing branch

**Status.** `ready`

**Who.** `agent + human`

**Directions.** R27

**Effort.** Low Risk / Medium Gain — `--parse-only` and an existing branch make
the hypothesis cheap to reject; any win is limited to the fraction of runtime
spent before solving.

**Work.** Record file size and cvc5 `--parse-only` time across the set, compare
with z3 on identical inputs, and A/B
[`ajreynol:ai-parserOpt`](https://github.com/ajreynol/CVC4/tree/ai-parserOpt)
on the solved-but-slow slice.

**Done when.** The ledger reports parser share and throughput distributions,
the branch's delta, and whether R27 stays in or leaves this top ten.

## 6 — Profile ten representative gap benchmarks

**Status.** `waiting`

**Who.** `agent + human`

**Directions.** R25, R26, R27

**Effort.** Low Risk / High Gain — profiles do not change solver semantics and
can eliminate whole classes of speculation before implementation begins.

**Work.** After items 1 and 3, choose both solved-but-slow and still-stuck
examples. Collect stats, instantiation traces, parse profiles, and callgrind
profiles, then map each dominant cost to one or more RX entries without
claiming attribution yet.

**Done when.** Ten ledger-backed case summaries identify dominant functions,
counter signatures, and plausible RX mappings.

## 7 — Run the cheap single-flag screen

**Status.** `waiting`

**Who.** `agent + human`

**Directions.** R5, R6, R7, R8, R10, R12, R13, R15, R16, R18, R20, R22, R23

**Effort.** Low Risk / High Gain — all flags already exist and are reversible;
the matrix can find a useful bundle or falsify many directions at once.

**Work.** Run the mainline flag matrix under “What to run first” in
`directions.md`, first on the gap set and then on the full set for changes that
survive. Change one choice per run.

**Done when.** Each flag has a comparable ledger row reporting gap-set size,
PAR2 ratio, wins, losses, and timeouts against the corrected baseline.

## 8 — Publish the first attribution table and rerank this file

**Status.** `waiting`

**Who.** `agent + human`

**Directions.** R26

**Effort.** Medium Risk / High Gain — combining noisy signals risks false
precision, but a reviewed table converts the register into the project's first
result and determines where implementation effort belongs.

**Work.** Combine the extractor, profiles, long-timeout classification,
parser measurements, and single-flag deltas into one row per gap benchmark and
one column per hypothesis class. Preserve ambiguity instead of forcing a winner.

**Done when.** The README's attributed fraction is nonzero and ledger-backed,
the top two or three directions have measured shares, and this top ten is
reranked from those shares.

## 9 — Test existing branches for the leading measured rows

**Status.** `waiting`

**Who.** `agent + human`

**Directions.** R3, R9, R10, R16, R17, R19, R22, R27

**Effort.** Medium Risk / High Gain — stale branches may need compatibility
repairs, but restricting work to measured leaders makes each A/B capable of
removing a known share of the gap.

**Work.** Select only branches whose RX rows rank highly in item 8. Start with
the smallest plausible implementation, run an A/B on the gap set, and promote
only clear wins to the full set.

**Done when.** Every tested branch has a ledger row and the leading measured
direction has either a reproducible improvement or a documented falsification.

## 10 — Implement the highest-leverage structural change

**Status.** `conditional`

**Who.** `agent + human`

**Directions.** R1, R2, R4, R9

**Effort.** High Risk / High Gain — eager, incremental, budgeted,
backtrack-aware instantiation spans several correctness-critical subsystems,
but it targets the central structural difference from z3.

**Work.** Proceed only if attribution shows that full-effort rounds and matcher
rework dominate the gap. Treat eager instantiation, incremental matching,
budgets, and instance lifetime as one design with staged milestones.

**Done when.** A reviewed design preserves completeness boundaries, targeted
regressions pass, and an A/B ledger row shows how much of the attributed share
the implementation actually removes.
