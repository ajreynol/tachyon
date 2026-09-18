# Hypothesis register

**2026-09-18: source evidence only.** Unlike Heuresis's inherited performance
notes, this register starts from a fresh public-branch survey and maintainer
guidance. Every proposed performance effect below is unmeasured. The
[survey](ledger/2026-09-18-branch-survey.md) pins the code; the
[directions](docs/directions.md) explain mechanisms and limitations.

Identifiers are stable. A source observation is not evidence of time saved,
proof completeness or a branch's correctness. Related branches need not be
independent implementations, and an old branch can contain behavior now on
main. No branch has been built or tested here.

| id | hypothesis | source status | direction / what would distinguish it |
| --- | --- | --- | --- |
| e-1 | Some atom rewrites need not appear in the final refutation if the Boolean proof can consistently use their original forms. | Maintainer-highlighted `unrewrite` family; original sketch, transformation attempt in `unrewrite2`. | [E1](docs/directions.md#e1-unrewriting): exclusive removable nodes, replay success and when their construction could be avoided. |
| e-2 | Large substitution/rewrite macros expand substantially more syntax than their conclusions require. | `reduceTransform` and overlapping code in `cpcDevChainMRes`. | [E2](docs/directions.md#e2-smaller-macro-obligations): local obligations versus full macro expansion, including failed decomposition cost. |
| e-3 | Explicit congruence/transitivity scaffolding dominates term-conversion proofs. | Maintainer-highlighted `pfrConvert`; a distinct `pfrConvert2` design. | [E3](docs/directions.md#e3-compact-term-conversion): checked compact conversion versus expanded proof, including work done before compaction. |
| e-4 | Reconstruction justifies child rewrites that do not affect a parent's result. | `rewriteDep` minimizes dependencies before proof-producing rewriting. | [E4](docs/directions.md#e4-rewrite-dependencies): probing cost versus avoided reconstruction. |
| e-5 | Simplifying and sharing the proof DAG before expansion can avoid repeated or ultimately discarded work. | Main has merging and bounded presimplification; fork bundles contain additional transformations. | [E5](docs/directions.md#e5-proof-dag-simplification-and-sharing): exclusive avoided work, scope-safe sharing and traversal cost. |
| e-6 | Remembering which rewrite fired can replace expensive proof search with direct reconstruction. | `rdbExec` compiles selected RARE rules and records rule identities. | [E6](docs/directions.md#e6-recorded-rewrite-provenance): reconstruction saved versus tracing and changed rewriting costs. |
| e-7 | Repeated evaluation and a poor ordering of reconstruction attempts waste postprocessing time. | `rareOptEval`, `rpcAlwaysPre`, `smtPpBasicRewriteOnly`, `rareNoEvalPremise`. | [E7](docs/directions.md#e7-reconstruction-cache-and-search-policy): reuse, peak memory, successful reconstruction and residual trust. |
| e-8 | Internal resolution-rule checking repeatedly scans large intermediate clauses. | `chainMResOpt` changes one checker file; baseline still has the old loop. | [E8](docs/directions.md#e8-resolution-construction-and-internal-checking): calls and clause volume under the intended checking policy. |
| e-9 | Losing definitions and term sharing causes unnecessary proof representation and output work. | `pf-defineFun`, its printer variant, and mainline DAG controls. | [E9](docs/directions.md#e9-definitions-and-proof-output): generation, conversion, output bytes and external checking separately. |
| e-10 | Proof bookkeeping and theory reconstruction retain or rebuild more material than the final proof needs. | `theoryEngineLazyProofs`; strings substitution/reconstruction variants. | [E10](docs/directions.md#e10-lazy-bookkeeping-and-theory-reconstruction): retained objects, generator calls, reconstruction failures and scope lifetime. |
| e-11 | Related incremental queries repay proof setup and printing costs repeatedly. | `ai-pfIncremental` adds scoped CPC output; older logging branches supply context. | [E11](docs/directions.md#e11-incremental-output-and-reuse): whole-session cost, query coverage and validation across push/pop. |
| e-12 | Some proof overhead is lost solving capability or changed configuration rather than proof construction. | Main's effective-setting changes; `ai-macroPf` is an adjacent support candidate. | [E12](docs/directions.md#e12-proof-induced-search-changes): ordinary, matched-settings and proof-enabled controls. |

The central research question joins e-1 through e-6: **how much of the proof
work is logically necessary, and how early can unnecessary work be recognized?**
That is a proposed organizing question, not an attribution result. e-7 and e-8
offer smaller implementation candidates; their convenience does not establish
that they address the largest costs.
