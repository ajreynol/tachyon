# heuresis — discussion

Items this project wants to raise with cvc5 developers: defects, questions
about intended behaviour, and design points that are not performance results.
Each is written to be read by someone who works on cvc5 and has not read
anything else in this repository, so each restates its own context.

Performance work lives in [`progress.md`](progress.md) and the
[ledger](../ledger/); this file is for things worth a conversation upstream.

---

## 1. Segfault with `--ee-mode=central --ieval=off`

**Status:** reproducible on current `main`, not yet filed upstream.
**Evidence:** [ledger 2026-09-17](../ledger/2026-09-17-central-ieval-segfault.md).

### Summary

cvc5 segfaults when `--ee-mode=central` and `--ieval=off` are passed together.
Either option alone solves the same benchmark normally. The crash is
deterministic, is reached after roughly 20–30 s of CPU, and is not new: it
reproduces on builds several months apart.

### Reproducing

```
cvc5 -q --no-cbqi --user-pat=strict --ee-mode=central --ieval=off BENCHMARK
```

```
cvc5 suffered a segfault.
Offending address is 0x119db0e40
```

Confirmed on `main@67954d09dc`, and on `main@5cc03f4b9` (a build roughly one
month older), on Linux x86-64. Two benchmarks trigger it, both
Verus-generated, `UFDTNIA` and `UFDTLIA`, crashing after about 27 s and 18 s of
CPU at roughly 105 MB RSS.

### Which options matter

Bisected on one benchmark, each run to a 100 s CPU limit:

| options | result |
| --- | --- |
| `-q` | no answer within the limit |
| `-q --no-cbqi --user-pat=strict --sat-solver=cadical` | no answer within the limit |
| … plus `--ee-mode=central` | `unsat` |
| … plus `--ieval=off` | `unsat` |
| … plus **both** | **segfault** |

- **Both flags are required.** Neither alone crashes, and each alone is enough
  to solve the benchmark that the combination crashes on.
- **`--sat-solver=cadical` is not required.** The default SAT solver segfaults
  on the same combination; the first backtrace below simply came from a
  CaDiCaL run.
- `-q --ee-mode=central --ieval=off` *without* the quantifier options did not
  crash within a 150 s CPU limit, so the quantifier configuration appears to
  be part of reaching the faulty state — though that may only be a matter of
  how quickly the search gets there.

### Backtrace

Both benchmarks fault at an identical frame:

```
#0  EqualityEngine::getExplanation(unsigned, unsigned, vector<Node>&, map<...>&, EqProof*) const
#1  EqualityEngine::explainEquality(Node, Node, bool, vector<Node>&, EqProof*) const
#2  EqualityEngine::explainLit(Node, vector<Node>&) const
#3  EqualityEngine::mkExplainLit(Node) const
#4  SharedTermsDatabase::explain(Node) const
#5  SharedSolverDistributed::explain(Node, TheoryId)
#6  TheoryEngine::getExplanation(vector<NodeTheoryPair>&)
#7  TheoryEngine::getExplanation(Node)
#8  prop::TheoryProxy::explainPropagation(SatLiteral, vector<SatLiteral>&)
#9  prop::cadical::CadicalPropagator::cb_add_reason_clause_lit(int)
#10 CaDiCaL::Internal::add_external_clause(int, bool)
#11 CaDiCaL::Internal::learn_external_reason_clause(int, int, bool)
#12 CaDiCaL::Internal::explain_reason(int, CaDiCaL::Clause*, int&)
#13 CaDiCaL::Internal::explain_external_propagations()
#14 CaDiCaL::Internal::analyze()
```

So: explaining a propagated literal, during conflict analysis, through the
shared-terms database into equality-engine explanation.

### What it is not

- **Not a stack overflow.** The crashing frame is at `0x7fffffffc810`, within a
  few kilobytes of the stack top, and the backtrace shows no recursion — 25
  frames in total. (The host's stack limit is 10240 kB soft *and* hard, so
  raising it to confirm from the other direction was not possible.)
- **Not a recent regression.** It reproduces on a build roughly a month older.
- **Not memory exhaustion.** Peak RSS is about 105 MB.

### What we have not established

- **The cause.** No debug build was made. Whether this is a null dereference, a
  dangling `EqProof*`, or an out-of-bounds index is not known, and no argument
  values were recovered.
- **The scope.** Two benchmarks out of 6124 are known to crash, but they were
  found incidentally: the fault needs ~20 s of CPU to reach, and shorter runs
  kill the process first. The set has not been swept, so the true count is
  unknown and could be larger.
- **A minimal reproducer.** Both triggers are large Verus-generated files; no
  reduction was attempted.

### Questions for cvc5 developers

1. Is `--ee-mode=central` with `--ieval=off` a combination that is expected to
   work? If it is not supported, cvc5 rejecting it at option-parsing time would
   be better than crashing after 20 s.
2. Does the frame at `SharedSolverDistributed::explain` under
   `--ee-mode=central` look right, or is the distributed shared solver itself
   a sign that the configuration is inconsistent?
3. Would a reduced benchmark help enough to be worth producing, or is the
   backtrace and the option pair sufficient to locate this?
