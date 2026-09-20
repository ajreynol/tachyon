# String benchmark assessment prompt

[`prompts/metagraphe_compare_solvers`](../../../prompts/metagraphe_compare_solvers)
generates a prompt for finding string benchmarks where cvc5 trails an external
solver, then investigating concrete rewrite opportunities. It only writes
Markdown to standard output: it never launches an agent or runs a solver.
This is prompt setup; no benchmark assessment has been performed by generating it.
It requires Python 3.9+ and uses only the standard library.

From the repository root, preview the prompt with the requested defaults:

```bash
prompts/metagraphe_compare_solvers
```

The defaults are `~/benchmarks/smt-lib-2026/`, `~/bin/ajr-cvc5` and
`~/bin/z3noodler`. Override all three, or select a smaller corpus:

```bash
prompts/metagraphe_compare_solvers \
  --benchmarks-dir /path/to/smt-lib/non-incremental/QF_SLIA \
  --cvc5-binary /path/to/cvc5 \
  --external-binary /path/to/external-solver \
  --max-benchmarks 100 \
  --timeout-seconds 10
```

Use `--cvc5-source /path/to/source` when a matching checkout is available.
`--cvc5-arg=--some-option` and `--external-arg=some.setting=value` each add one
literal solver argument and can be repeated; use `=` for values beginning with
a dash. These are syntax examples, not recommended solver options. The later
investigation must verify the exact external solver's backend and invocation.
`--logic` can be repeated to replace the default QF_S/QF_SLIA/QF_SNIA selection.
Run `--help` for every option.

Paths are expanded and made absolute relative to the caller's working directory.
Generation does not require them to exist or inspect the executables. Review the
rendered configuration before using the prompt on another machine. To keep a
local copy for a later agent session in this checkout:

```bash
mkdir -p scratch/metagraphe-prompts
prompts/metagraphe_compare_solvers > scratch/metagraphe-prompts/string-comparison.md
```

The generated task specifies a deterministic sample of at most 200 benchmarks,
paired sequential runs with 10-second limits, and up to ten diverse gaps confirmed
three times with 60-second limits. All these bounds are configurable. Those
defaults permit up to about 127 minutes of solver wall time for screening and
confirmation alone if every run exhausts its limit; source analysis and rewrite
probes take additional time. Choose smaller bounds for a shorter first pass.

The prompt separates timeouts, unknown answers, unsupported inputs, errors and
answer disagreements; requires matching-source checks and semantic evidence for
proposed `lhs -> rhs` rules; and asks for controlled original/transformed-input
comparisons where justified. It directs findings into the project's ledger and
concrete candidates through its existing rewrite database workflow, with raw
output in ignored scratch space. A performance gap alone is not a rewrite finding.

This generator records instructions and configuration. A later agent must carry
out the experiment and report actual limits, coverage and evidence; the generator
does not implement or enforce a benchmark harness.
