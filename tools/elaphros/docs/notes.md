# Hypothesis register

**2026-09-18: source evidence only; extended 2026-09-19.** Unlike Heuresis's
inherited performance notes, this register starts from a fresh public-branch
survey and maintainer guidance. Every proposed performance effect below is
unmeasured. The [survey](ledger/2026-09-18-branch-survey.md) pins the code;
the [directions](directions.md) explain mechanisms and limitations.

Hypotheses e-1 through e-12 are branch-derived: each rests on code someone
wrote on `ajreynol/cvc5`. Hypotheses e-13 through e-16 rest instead on the
[pipeline audit](ledger/2026-09-19-pinned-main-pipeline-audit.md) of pinned
main and have no branch behind them. The distinction is about the kind of
prior support each has, not about their likelihood.

Identifiers are stable. A source observation is not evidence of time saved,
proof completeness or a branch's correctness. Related branches need not be
independent implementations, and an old branch can contain behavior now on
main. No branch has been built or tested here.

| id | hypothesis | source status | direction / what would distinguish it |
| --- | --- | --- | --- |
| e-1 | Some atom rewrites need not appear in the final refutation if the Boolean proof can consistently use their original forms. | Maintainer-highlighted `ajreynol:unrewrite` family; original sketch, transformation attempt in `ajreynol:unrewrite2`. | [E1](directions.md#e1-unrewriting): exclusive removable nodes, replay success and when their construction could be avoided. |
| e-2 | Large substitution/rewrite macros expand substantially more syntax than their conclusions require. | `ajreynol:reduceTransform` and overlapping code in `ajreynol:cpcDevChainMRes`. | [E2](directions.md#e2-smaller-macro-obligations): local obligations versus full macro expansion, including failed decomposition cost. |
| e-3 | Explicit congruence/transitivity scaffolding dominates term-conversion proofs. | Maintainer-highlighted `ajreynol:pfrConvert`; a distinct `ajreynol:pfrConvert2` design. | [E3](directions.md#e3-compact-term-conversion): checked compact conversion versus expanded proof, including work done before compaction. |
| e-4 | Reconstruction justifies child rewrites that do not affect a parent's result. | `ajreynol:rewriteDep` minimizes dependencies before proof-producing rewriting. | [E4](directions.md#e4-rewrite-dependencies): probing cost versus avoided reconstruction. |
| e-5 | Simplifying and sharing the proof DAG before expansion can avoid repeated or ultimately discarded work. | Main has merging and bounded presimplification; fork bundles contain additional transformations. | [E5](directions.md#e5-proof-dag-simplification-and-sharing): exclusive avoided work, scope-safe sharing and traversal cost. |
| e-6 | Remembering which rewrite fired can replace expensive proof search with direct reconstruction. | `ajreynol:rdbExec` compiles selected RARE rules and records rule identities. | [E6](directions.md#e6-recorded-rewrite-provenance): reconstruction saved versus tracing and changed rewriting costs. |
| e-7 | Repeated evaluation and a poor ordering of reconstruction attempts waste postprocessing time. | `ajreynol:rareOptEval`, `ajreynol:rpcAlwaysPre`, `ajreynol:smtPpBasicRewriteOnly`, `ajreynol:rareNoEvalPremise`. | [E7](directions.md#e7-reconstruction-cache-and-search-policy): reuse, peak memory, successful reconstruction and residual trust. |
| e-8 | Internal resolution-rule checking repeatedly scans large intermediate clauses. | `ajreynol:chainMResOpt` changes one checker file; baseline still has the old loop. | [E8](directions.md#e8-resolution-construction-and-internal-checking): calls and clause volume under the intended checking policy. |
| e-9 | Losing definitions and term sharing causes unnecessary proof representation and output work. | `ajreynol:pf-defineFun`, its printer variant, and mainline DAG controls. | [E9](directions.md#e9-definitions-and-proof-output): generation, conversion, output bytes and external checking separately. |
| e-10 | Proof bookkeeping and theory reconstruction retain or rebuild more material than the final proof needs. | `ajreynol:theoryEngineLazyProofs`; strings substitution/reconstruction variants. | [E10](directions.md#e10-lazy-bookkeeping-and-theory-reconstruction): retained objects, generator calls, reconstruction failures and scope lifetime. |
| e-11 | Related incremental queries repay proof setup and printing costs repeatedly. | `ajreynol:ai-pfIncremental` adds scoped CPC output; older logging branches supply context. | [E11](directions.md#e11-incremental-output-and-reuse): whole-session cost, query coverage and validation across push/pop. |
| e-12 | Some proof overhead is lost solving capability or changed configuration rather than proof construction. | Main's effective-setting changes; `ajreynol:ai-macroPf` is an adjacent support candidate. | [E12](directions.md#e12-proof-induced-search-changes): ordinary, matched-settings and proof-enabled controls. |
| e-13 | The cost of proof production cannot presently be attributed, because no phase partition exists and no counter separates proof material that reaches the final proof from material constructed and discarded. | Audited: existing counters are attempts and outcomes; the final-proof histograms are reachable only under `--check-proofs`. | [E13](directions.md#e13-proof-work-accounting): a non-overlapping phase partition, a discarded-work measure and the instrument's own overhead. |
| e-14 | Allocating every proof node individually, with no structural sharing, costs memory and time that a different representation would not. | Audited: `mkNode` allocates per call; the header records that mutability is why results are not cached and names the unbuilt immutable layer. | [E14](directions.md#e14-proof-node-representation-and-allocation): live/total nodes, duplicate structure, peak memory and allocator time, against the cost at each `updateNode` site. |
| e-15 | Materializing the whole proof before emitting any of it sets peak memory higher than the output requires. | Audited: the pipeline postprocesses, scopes and then prints; `--proof-log` streams the SAT layer only; the Eo/CPC printer is two-pass by construction. | [E15](directions.md#e15-streaming-proof-emission): peak memory versus total allocation and output bytes, under a stated incremental-output contract. |
| e-16 | The proof is walked more times than the work requires, and some passes could ride along with an existing traversal. | Audited: updater, optional subtype conversion, trusted-step scan and a two-pass printer; other traversals are gated by checking options. | [E16](directions.md#e16-traversal-fusion): traversal and per-node visit counts in the measured configuration, and whether fusion preserves the order of effects. |

The central research question joins e-1 through e-6: **how much of the proof
work is logically necessary, and how early can unnecessary work be recognized?**
That is a proposed organizing question, not an attribution result. e-7 and e-8
offer smaller implementation candidates; their convenience does not establish
that they address the largest costs.

e-13 stands before the others rather than beside them: while it is open, the
ordering of every remaining hypothesis rests on how much source each one has
behind it. e-14 and e-15 are the register's only entries about memory, which
the charter names as half the subject.
