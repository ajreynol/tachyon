# String benchmark assessment launcher

[`prompts/metagraphe_compare_solvers`](../../../prompts/metagraphe_compare_solvers)
launches Claude or Codex in this checkout to find string benchmarks where cvc5
trails an external solver and investigate useful rewrites.

```bash
prompts/metagraphe_compare_solvers                 # Claude (default)
prompts/metagraphe_compare_solvers --codex         # Codex
prompts/metagraphe_compare_solvers --codex --print # non-interactive
prompts/metagraphe_compare_solvers --show-prompt   # preview; launches nothing
```

The defaults are `~/benchmarks/smt-lib-2026/`, `~/bin/ajr-cvc5` and
`~/bin/z3noodler`. To change them:

```bash
prompts/metagraphe_compare_solvers --claude \
  --benchmarks-dir /path/to/smt-lib \
  --cvc5-binary /path/to/cvc5 \
  --external-binary /path/to/external-solver
```

Paths resolve relative to the caller's directory, with `~` expanded.
`--cvc5-source` names optional matching source. Repeat `--cvc5-arg=ARG` or
`--external-arg=ARG` for individual literal solver arguments; use `=` when an
argument starts with a dash. Repeat `--logic` to replace QF_S/QF_SLIA/QF_SNIA.

The prompt defaults to 200 paired inputs with 10-second screening limits and
up to ten gaps confirmed three times with 60-second limits. Use `--help` to
adjust these bounds. The launched agent performs the experiments and records
findings under Metagraphe's existing evidence and rewrite database policies.

Requires Python 3.9+ and the selected agent on PATH. `--show-prompt` requires
neither an agent nor existing corpus/solver paths and overrides launch options.
`--print` uses `claude -p` or `codex exec`; it runs the assessment, whereas
`--show-prompt` only displays its instructions.
