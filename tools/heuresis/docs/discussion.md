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
**Evidence:** [ledger 2026-09-17](../ledger/2026-09-17-central-ieval-segfault.md),
scope in [2026-09-17 segfault-scope](../ledger/2026-09-17-segfault-scope-and-failure-logging.md).

### Summary

cvc5 segfaults when `--ee-mode=central` and `--ieval=off` are passed together.
Either option alone solves the same benchmark normally. The crash is
deterministic, is reached after roughly 20–30 s of CPU, and is not new: it
reproduces on builds several months apart.

### Reproducing

```
cvc5 -q --no-cbqi --user-pat=strict --ee-mode=central --ieval=off BENCHMARK
```

The run terminates with a segmentation fault; the reported offending address
was `0x119db0e40`.

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
  on the same combination; the call chain summarized below came from a
  CaDiCaL run.
- `-q --ee-mode=central --ieval=off` *without* the quantifier options did not
  crash within a 150 s CPU limit, so the quantifier configuration appears to
  be part of reaching the faulty state — though that may only be a matter of
  how quickly the search gets there.

### Backtrace

Both benchmarks fault in `EqualityEngine::getExplanation`. CaDiCaL conflict
analysis reaches the fault while explaining external propagations, through
`explain_reason`, `learn_external_reason_clause` and `add_external_clause`.
The reason-clause callback enters `TheoryProxy::explainPropagation` and
`TheoryEngine::getExplanation`, then shared-solver and shared-terms explanation,
then the equality engine's `mkExplainLit`, `explainLit` and `explainEquality`.

This summarizes the diagnostic under the
[retention correction](../ledger/2026-09-19-output-retention.md); raw debugger
output belongs in the external diagnostic artifact, not this document.

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
- **The scope, now measured.** A 300 s sweep of the whole set in the crashing
  configuration finds **exactly two** crashes — the same two — among the
  **5845** benchmarks that reach a terminal answer
  ([ledger](../ledger/2026-09-17-segfault-scope-and-failure-logging.md)). This
  is a floor rather than a total: 279 benchmarks still hit the 300 s timeout
  and never got the chance to crash. So: rare, reproducible, and not
  widespread.
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
