# 2026-09-17 — cvc5 segfaults under `--ee-mode=central --ieval=off`

**Monitor finding.** A defect in cvc5 `main`, found by following up the two
`error` results left undiagnosed by the preceding entry. It is in the
configuration [`progress.md`](../docs/progress.md) tracks as `best`.

## 1. What was asked

[`2026-09-16-eager-counters-and-timeout-sensitivity.md`](2026-09-16-eager-counters-and-timeout-sensitivity.md)
recorded two benchmarks that returned `error` in the 120 s control and were not
diagnosed. The wrapper `cvc5_solve.sh` maps any output that is not a clean
result token to `error` and discards the message, so the cause was unknown.
Find out what it was.

## 2. What was run

**This entry is a diagnosis, not a benchmark run.** Nothing went through a
run-dev config; the commands were issued directly on the execution host
against two named files. The only launcher record is the `master` build that
produced the binary
([`job_launcher/log.txt`](../../../job_launcher/log.txt)). The ledger's usual
"config plus log line" form does not apply, and the commands are quoted in
full below instead.

```
cvc5 -q --no-cbqi --user-pat=strict --sat-solver=cadical \
     --ee-mode=central --ieval=off BENCHMARK
```

Binaries: `master@67954d09dc` (current upstream `main`, built for this entry),
and the host's older `main@5cc03f4b9` build for the regression check.

## 3. The set

Two benchmarks of `quant-07-25`:

- `sundance/UFDTNIA/20241211-verus/20241211-verusatmosphere/allocator__page_allocator_spec_impl.18.smt2`
- `verus-no-option/mariposa_queries/v_ironfleet/unsolvable/single_delivery_model_v.5.smt2`

## 4. What came back

**Both benchmarks segfault.** Not a timeout, not an error message: a
`SIGSEGV`, deterministic, reproducing on every attempt, after roughly 27 s and
18 s of CPU respectively at ~105 MB RSS.

Option bisection on `single_delivery_model_v.5`:

| options | result |
| --- | --- |
| `-q` | (CPU limit) |
| `-q --no-cbqi --user-pat=strict --sat-solver=cadical` | (CPU limit) |
| … `--ee-mode=central` | **unsat** |
| … `--ieval=off` | **unsat** |
| … `--ee-mode=central --ieval=off` | **SEGFAULT** |

**Both flags are required.** Either alone solves the benchmark. Only the
combination crashes.

`--sat-solver=cadical` is **not** required — the default SAT solver segfaults
on the same combination. `-q --ee-mode=central --ieval=off` alone, without the
quantifier options, did not crash within a 150 s CPU limit, so the quantifier
configuration is part of reaching the faulty state.

Both benchmarks crash at the identical frame:

```
#0  EqualityEngine::getExplanation(unsigned, unsigned, vector<Node>&, map<...>&, EqProof*) const
#1  EqualityEngine::explainEquality(Node, Node, bool, vector<Node>&, EqProof*) const
#2  EqualityEngine::explainLit(Node, vector<Node>&) const
#3  EqualityEngine::mkExplainLit(Node) const
#4  SharedTermsDatabase::explain(Node) const
#5  SharedSolverDistributed::explain(Node, TheoryId)
#6  TheoryEngine::getExplanation(vector<NodeTheoryPair>&)
#8  prop::TheoryProxy::explainPropagation(SatLiteral, vector<SatLiteral>&)
#9  prop::cadical::CadicalPropagator::cb_add_reason_clause_lit(int)
#13 CaDiCaL::Internal::explain_external_propagations()
#14 CaDiCaL::Internal::analyze()
```

**It is not a stack overflow.** The crashing frame sits at `0x7fffffffc810`,
within a few kilobytes of the stack top, and the backtrace shows no recursion
— 25 frames from `main` to the fault. The host's stack limit is 10240 kB soft
and hard, so raising it could not be tested, but the shallow stack rules out
exhaustion as the explanation.

**It is not a regression.** The same combination segfaults on the older
`main@5cc03f4b9` build, so the defect predates the window
[`progress.md`](../docs/progress.md) covers.

## 5. What it settled

**cvc5 `main` has a reproducible segmentation fault**, on current main
`67954d09dc`, requiring `--ee-mode=central` and `--ieval=off` together, in
equality-engine explanation reached through shared-term explanation. It is
long-standing rather than new. This is a defect report that can go upstream on
the evidence in this entry, and it is the first thing this project has produced
that is worth sending to cvc5 regardless of any performance question.

**It qualifies the `best` configuration.** `best` is exactly the crashing
combination. The number
[`progress.md`](../docs/progress.md) holds up as the one to beat is measured in
a configuration that crashes on at least 2 of 6124 benchmarks. The PAR2 effect
is nil — both benchmarks are unsolved in every arm and score as unsolved either
way — but a configuration that segfaults is not one to recommend to a user, and
the table now says so.

**Only a long timeout could have found it.** Under the 30 s runs both
benchmarks were killed before reaching the fault: at 56-way parallelism, 18–27 s
of solo CPU exceeds 30 s of wall clock. They surfaced only in the 120 s arm of
S7, which was run for an unrelated reason.

## 6. What it did not settle

The cause inside `getExplanation` is unknown. No debug build was made, the
frame has no symbols beyond the signature, and no argument values were
recovered, so whether this is a null dereference, a dangling `EqProof*`, or an
out-of-bounds index is not established here.

Nothing establishes how many of the 6124 benchmarks are affected. Two were
found because they happened to run long enough in one arm; the crash requires
roughly 20 s of CPU to reach, so the set has not been swept for others, and the
true count is unknown and plausibly larger.

Whether the two benchmarks may be shared publicly in an upstream issue was not
checked. The `mariposa_queries/v_ironfleet` file comes from a public benchmark
suite; the `sundance/` file's provenance was not established.
