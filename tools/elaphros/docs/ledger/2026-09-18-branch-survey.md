# 2026-09-18 — Public branches and initial research map

**Evidence type: source inspection. No experiments, builds, rebases or proof
checker runs.** This record supports a hypothesis register and priorities,
not a claim of improved proof performance.

## Scope and pinned source

- Fork: [ajreynol/cvc5](https://github.com/ajreynol/cvc5), queried with
  `git ls-remote --heads`. The retained snapshot has **809 public heads**.
- Upstream: [cvc5/cvc5 main at
  `3dcc1ef5421ab62cc1ee9af52d70042ce6861af0`](https://github.com/cvc5/cvc5/commit/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0),
  resolved live on the audit date. This is the comparison revision, not an
  experimental baseline.
- All 809 head objects were available for the completed screen. Existing Git
  objects were reused in a project-local scratch repository; missing objects
  were fetched from the named public repositories. Existing solver working
  trees were not changed.
- Each branch was compared to **its merge base with pinned upstream**, over
  `src/`, rather than comparing two diverged trees and mistaking upstream
  additions for branch changes.
- A path screen selected names containing `proof`, `/rewriter/`,
  `/infer_proof` or `/options/proof_`. **203 heads** matched. This is a broad
  proof/rewrite candidate count, not a count of proof-performance ideas.
- Names, tip subjects and source paths guided selection. The deeper review
  followed the postprocessor, updater, conversion and reconstruction paths,
  including the maintainer's `ajreynol:unrewrite` and `ajreynol:pfrConvert` leads. **49 branches**
  have retained source-delta/history summaries. Inspection depth varies: the
  tables below explain the principal mechanisms; peripheral branches are not
  all reviewed line by line.

The [data index](../../reports/data/README.md) names the exact artifacts and reproduction
method. Full source deltas and ancestry are recoverable from the pinned Git
objects; downloaded source and temporary diff files remain in ignored scratch.

## The principal branches

`Ahead/behind` counts commits in `main...tip`, including merge/history commits.
`Source delta` is files and added/deleted lines in `src/` from merge base to
tip, excluding tests, public headers and proof signatures. These quantities
describe archaeology, **not total patch size, effort or performance**. Dates
are tip commit dates; a recent merge can refresh an old design.

| branch / pinned tip | tip date | ahead / behind | source delta | source assessment |
| --- | --- | ---: | --- | --- |
| [`ajreynol:unrewrite`](https://github.com/ajreynol/cvc5/tree/2023c6c83e2f42981bdc6a5943690d90fdf324cf) | 2026-08-19 | 12 / 63 | 10 files, +387/−0 | E1: preprocessing links and atom analysis; converter callback is an empty sketch. |
| [`ajreynol:unrewrite2`](https://github.com/ajreynol/cvc5/tree/69064b385d5d699a890a7dc87b90914c053715c9) | 2026-08-19 | 13 / 63 | 10 files, +1082/−0 | E1: adds an actual replacement attempt after elaboration, step replay and fallback; not validated here. |
| [`ajreynol:reduceTransform`](https://github.com/ajreynol/cvc5/tree/6af2d9093f462039ebd42ba24ca76e3d187d5c0e) | 2025-06-23 | 17 / 676 | 2 files, +324/−2 | E2: smaller predicate-introduction/transform obligations using local congruence, conjunctions and transitivity. |
| [`ajreynol:pfrConvert`](https://github.com/ajreynol/cvc5/tree/0ab530cb4592248f7fcd7504d2809d7f0f600e15) | 2023-10-30 | 19 / 2203 | 7 files, +374/−29 | E3: context-sensitive CONVERT production inside term conversion. |
| [`ajreynol:pfrConvert2`](https://github.com/ajreynol/cvc5/tree/6c74757436a92f22156d5d139cd9e9b6c4422cad) | 2026-01-30 | 18 / 402 | 7 files, +272/−20 | E3: distinct CONVERT/fixed-point design; obtains the ordinary result before trying compaction. |
| [`ajreynol:rewriteDep`](https://github.com/ajreynol/cvc5/tree/307640b2c80de8cff289a67b34000bf187c0e46d) | 2025-04-15 | 15 / 816 | 6 files, +225/−33 | E4: probes irrelevant children and translates a minimized rewrite proof back. |
| [`ajreynol:cpcDevChainMRes`](https://github.com/ajreynol/cvc5/tree/6e08c402be9d7aa78721ec43d64d0f73a412af57) | 2025-08-20 | 178 / 624 | 6 files, +532/−3 | E2/E5/E8: macro reductions, polynomial cases and TRANS/CONG simplification alongside resolution representation. Mixed bundle. |
| [`ajreynol:pfTrustId`](https://github.com/ajreynol/cvc5/tree/9eab5fece6851b70d968c847fdbf22365e4202cd) | 2025-06-18 | 1217 / 690 | 25 files, +748/−249 | E5: mainline presimplification history plus extra TRANS/CONG work; extensive unrelated history. |
| [`ajreynol:freeAsumpMerge`](https://github.com/ajreynol/cvc5/tree/7decef4c91793f38722c4f235902008d74c81668) | 2022-09-22 | 19 / 2927 | 7 files, +146/−80 | E5: scope/free-assumption-aware caching and merging; related behavior exists on main. |
| [`ajreynol:pfpUpdate-0417`](https://github.com/ajreynol/cvc5/tree/ea02fee56165b5f13487244f3a351988dbeffe09) | 2025-05-06 | 5 / 782 | 2 files, +55/−71 | E5: main changes already present; a comment proposing different expansion scheduling is not implemented there. |
| [`ajreynol:rdbExec`](https://github.com/ajreynol/cvc5/tree/458596700493247219a02c06b5f79f4b25c32803) | 2026-08-14 | 18 / 85 | 29 files, +2561/−49 | E6: executable RARE rules, recorded IDs, direct reconstruction and changed subtype-pass ordering. |
| [`ajreynol:rareOptEval`](https://github.com/ajreynol/cvc5/tree/07579cea12d2bac9f7734bfb3a1d349cb19b9165) | 2025-08-27 | 6 / 609 | 1 file, +1/−2 | E7: retain the reconstruction evaluation cache across calls. |
| [`ajreynol:rpcAlwaysPre`](https://github.com/ajreynol/cvc5/tree/adab37c00d6ec5a0f70d383276311b6c3b4ac19c) | 2025-08-27 | 8 / 609 | 6 files, +60/−1 | E7: promote POST_DSL rules to PRE_DSL; inherits the proofDisable bundle. |
| [`ajreynol:chainMResOpt`](https://github.com/ajreynol/cvc5/tree/cdebf282fc3ac22cddee66db548887fffbffe16f) | 2026-07-07 | 2 / 110 | 1 file, +62/−55 | E8: pending pivots/surviving literals replace repeated intermediate-clause scans in the internal checker. |
| [`ajreynol:pf-defineFun`](https://github.com/ajreynol/cvc5/tree/5edf06a936816ecd74b96162ae327fd46be591c8) | 2026-08-19 | 6 / 67 | 15 files, +698/−60 | E9: preserve macro definitions and connect original assertions. |
| [`ajreynol:pf-defineFun-printerOnly`](https://github.com/ajreynol/cvc5/tree/255eca8f34b93b7b106c2a074d3aaf55fb4be3f5) | 2026-08-19 | 7 / 67 | 11 files, +876/−25 | E9: descendant with a different effective design centered on proof-output conversion. |
| [`ajreynol:theoryEngineLazyProofs`](https://github.com/ajreynol/cvc5/tree/3b36cfc3bf2901ab00e08dd26e7825338f9e0c52) | 2021-10-22 | 2 / 4369 | 2 files, +22/−23 | E10: separate lazy-proof objects in selected theory-engine paths; old ownership experiment. |
| [`ajreynol:ai-pfIncremental`](https://github.com/ajreynol/cvc5/tree/3528e45cba629156c2964d92f680f956597e2515) | 2026-03-28 | 7 / 273 | 7 files, +365/−23 | E11: scoped CPC output across incremental queries. |
| [`ajreynol:proofDisable`](https://github.com/ajreynol/cvc5/tree/cd61fa165f7b85dcbfb2e9d3e8b93222511ba9ae) | 2025-08-25 | 7 / 609 | 5 files, +56/−1 | Diagnostic ablations that replace proof obligations; not an equivalent-proof optimization. |

Full SHAs, dates, merge bases and file-level statistics for these and the
other characterized branches are in
[`2026-09-18-selected-branches.json`](../../reports/data/2026-09-18-selected-branches.json).

## Additional postprocessor leads and limits

The path screen catches substantial code under names that do not advertise
postprocessing. Besides `ajreynol:reduceTransform` and `ajreynol:rewriteDep`, these merit explicit
classification:

| branch or group | interpretation after source inspection |
| --- | --- |
| `ajreynol:smtPpBasicRewriteOnly` | Uses ordinary rather than extended rewriting for a trusted-step recovery attempt. A policy candidate with a proof-coverage tradeoff to establish. |
| `ajreynol:rareNoEvalPremise`, `ajreynol:rareNoMix`, `ajreynol:cpcSimpEval` | Reconstruction/evaluation and theory-rewrite alternatives. Their effective changes differ; they are not interchangeable ways to disable evaluation. |
| `ajreynol:stratifiedStrIpc`, `ajreynol:stringsIpcRefactor`, `ajreynol:stringsIpcAgg`, `ajreynol:stringsIpcAgg2` | Different string inference reconstruction/substitution designs. Relevant if a strings stratum is selected; not four independent general postprocessor wins. |
| `ajreynol:pfnConvert`, `ajreynol:applyEmbedding`, `ajreynol:pfTrustId-no-enc` | Subtype/encoding and reconstruction history or mixed bundles. Selected summaries retained; further mechanism-level comparison is needed before promotion. |
| `ajreynol:elimTrustSubs`, `ajreynol:trustSubsRcons`, `ajreynol:subsElabFixpoint` | Substitution elaboration/correctness history. The last is a path-screen lead, not one of the 49 characterized summaries. Do not treat a correctness repair as a measured optimization. |
| `ajreynol:fixDupBrc`, `ajreynol:macroQuantOnce` | Small reconstruction fixes useful for understanding duplicate steps and conversion policy; not presently assigned independent research directions. |
| `ajreynol:ai-annotatePf` | Adds origin annotations and changes merging around them. An attribution lead, not established low-overhead instrumentation. |
| `ajreynol:pfLogInferface`, `ajreynol:dumpProofEagerPre` | Proof logging/staging history; full emitted-proof semantics must be distinguished from preprocessing or lemma output. |
| `ajreynol:proofTerm` | Older proof-as-term/compression prototype. Deferred as a broad representation change, not part of the initial shortlist. |
| `ajreynol:dtIpcNoRew`, `ajreynol:ai-macroPf`, `ajreynol:doki-1` | Theory/proof-support changes that can inform coverage or attribution. No general production-time improvement inferred. |
| Older `ajreynol:alf*`, format support/fix, regression-only and documentation branches | Visible in the inventory/path screen. Format availability and bug fixes are not counted as independent performance proposals. |

This is not an exhaustive semantic audit of all 203 hits. The heuristic also
misses changes restricted to nonmatching files, tests or signatures. All refs
and source-file counts remain available so selection can be revisited.

## Relationships checked in Git

At the pinned tips:

- `ajreynol:unrewrite` is an ancestor of `ajreynol:unrewrite2`.
- `ajreynol:pf-defineFun` is an ancestor of `ajreynol:pf-defineFun-printerOnly`.
- `ajreynol:proofDisable` is an ancestor of `ajreynol:rpcAlwaysPre`.
- `ajreynol:pfrConvert` is **not** an ancestor of `ajreynol:pfrConvert2`.
- `ajreynol:reduceTransform` is **not** an ancestor of `ajreynol:cpcDevChainMRes`; their
  overlapping mechanisms were identified from source, not presumed ancestry.

These checks do not establish independence, feature equivalence or upstream PR
status. No open/merged PR status is claimed; squash merges make fork ancestry
insufficient for that purpose.

## Pinned mainline evidence

The following links locate the current behaviors used in the research map.

| source | observations used here |
| --- | --- |
| [proof options](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/options/proof_options.toml) | Mainline merge, lookahead, resolution, checking, DAG and reconstruction controls; branch-only switches distinguished by absence. |
| [effective defaults](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/smt/set_defaults.cpp) | Proof-compatible solving changes, granularity promotion and logging/incremental restriction. |
| [proof postprocessor](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/smt/proof_post_processor.cpp) | Macro expansion, `addExpandStep`, subtype conversion and subsequent DSL reconstruction. |
| [proof-node updater](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/proof/proof_node_updater.cpp) | Existing presimplification, scope handling and sharing; no additional TRANS case from the identified fork bundles. |
| [conversion generator](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/proof/conv_proof_generator.cpp) | Ordinary term-conversion path contrasted with the two compact-conversion proposals. |
| [rewrite reconstruction](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/rewriter/rewrite_db_proof_cons.cpp) | Evaluation-cache clear per `prove` call and registered attempts/input/success counters. |
| [Boolean proof checker](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/theory/booleans/proof_checker.cpp) | Current CHAIN_M_RESOLUTION intermediate-vector algorithm. |
| [proof-node manager](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/proof/proof_node_manager.cpp) | Internal checker can compute conclusions even when optional checking is disabled. |
| [proof final callback](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/smt/proof_final_callback.cpp) | Final proof rule/trust statistics; these are not phase timers. |

## What follows from the audit

There are several distinct proof-performance design families, not merely
proof support branches. The strongest source-grounded organizing question is
how to avoid unnecessary elaboration. Whether it is the largest *measured*
cost is unknown. The [directions](../directions.md) and
[priority queue](../todo.md) are the proposed research interpretation.

This survey does not establish a cross-project count comparison with Heuresis:
the inventories use different dates and selection criteria. Nor does it
establish buildability, branch correctness, emitted-proof completeness,
checker compatibility, benchmark relevance or performance. No solver result
from another project is inherited as an Elaphros baseline.
