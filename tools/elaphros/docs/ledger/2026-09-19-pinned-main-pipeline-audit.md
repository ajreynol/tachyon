# 2026-09-19 — Proof pipeline audit of pinned main

**Evidence type: source inspection. No experiments, builds, rebases or proof
checker runs.** This record reads the proof pipeline of pinned upstream main
directly, rather than characterizing fork branches. It supports four
directions that no surveyed branch proposes; it establishes no performance
effect.

## Scope and pinned source

- Upstream: [cvc5/cvc5 main at
  `3dcc1ef5421ab62cc1ee9af52d70042ce6861af0`](https://github.com/cvc5/cvc5/commit/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0),
  the same revision pinned by the [branch survey](2026-09-18-branch-survey.md).
  Objects were read from the project-local scratch repository retained by that
  audit; no working tree was changed and no branch was fetched for this pass.
- Method: reading named source files and their call sites at the pinned
  revision. Line numbers below are at that revision and are not stable across
  upstream commits.
- **This is a reading of source, not of behavior.** Which call sites execute in
  a given run depends on options and on the query; nothing here was observed
  in a running solver. Statements about what a configuration does are
  predictions from the code, and are labeled as such.
- The audit was directed at four questions: how proof nodes are allocated,
  how many times the proof is traversed, which instrumentation exists, and
  what the output path requires. It is **not** a complete reading of the
  pipeline, and absence of a mechanism below means it was not found along the
  paths read, not that it does not exist.

## Proof node allocation and sharing

| source | observation |
| --- | --- |
| [`proof_node_manager.h:52-55`](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/proof/proof_node_manager.h#L52-L55) | The class comment states the design and names the unbuilt alternative: "Notice that ProofNode objects are mutable, and hence this class does not cache the results of mkNode. A version of this class that caches immutable version of ProofNode objects could be built as an extension or layer on top of this class." |
| [`proof_node_manager.cpp:56`](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/proof/proof_node_manager.cpp#L56) | `mkNode` allocates with `std::make_shared<ProofNode>(id, children, args)` per call. No uniqueness table, free list or pool was found on this path. |
| [`proof_post_processor.cpp:1127`](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/smt/proof_post_processor.cpp#L1127) | Mutability is load-bearing: the subtype-converted proof is spliced back into the existing node with `ProofNodeManager::updateNode`. An immutable layer must account for such sites. |

Terms are hash-consed by `NodeManager`; proof nodes are not. Main's
`--proof-pp-merge` and `--proof-dag-global` concern merging during
postprocessing and printing, which is a different mechanism from
construction-time uniquing or allocation strategy. No branch in the
[survey](2026-09-18-branch-survey.md) proposes changing proof node allocation
or representation, except `ajreynol:proofTerm`, which the survey records as a
broader proof-as-term prototype.

## Traversals between the prop-engine proof and output

`PfManager::connectProofToAssertions` obtains the proof body and calls
[`d_pfpp->process`](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/smt/proof_manager.cpp#L238),
then builds the scope. Within
[`ProofPostprocess::process`](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/smt/proof_post_processor.cpp#L1110-L1137):

| pass | condition | note |
| --- | --- | --- |
| `d_updater.process(pf)` | always | The elaboration pass; includes main's presimplification and merging. |
| `ProofNodeConverter subtypeConvert.process(pf)` then `updateNode` | `--proof-elim-subtypes` | Builds a converted proof and splices it in; this constructs rather than annotates. |
| `expr::getSubproofRules(pf, {TRUST, TRUST_THEORY_REWRITE}, tproofs)` then `d_ppdsl->reconstruct` | trusted-rule elimination configured | A scan for remaining trusted steps, separate from the updater pass that may have created them. |

Beyond the postprocessor, on the paths read:

- **Output, Eo/CPC.** `EoPrinter` runs the proof twice by construction: the
  loop at
  [`eo_printer.cpp:903-915`](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/proof/eo/eo_printer.cpp#L903-L915)
  passes `i == 0` through `EoPrintChannelPre` before printing at `i == 1`. Its
  class comment states the purpose: "Run on the proof before it is printed,
  and does two preparation steps: Computes the letification of nodes that
  appear in the proof. Computes the set of variables that appear in the
  proof." A single-pass emission would have to replace this pre-pass.
- **`proof_letify`** is included only by the LFSC printer and its utilities at
  this revision. It is not part of the Eo/CPC output path.
- **`pfgEnsureClosed*` is not a default-configuration traversal.**
  [`proof_ensure_closed.cpp:38-48`](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/proof/proof_ensure_closed.cpp#L38-L48)
  returns immediately unless proofs are produced and either
  `--proof-check=eager` or the corresponding trace is on.
- **The final-callback traversal is checking-gated**; see below.

Traversal *count* is not traversal *cost*: these passes visit nodes with very
different per-node work, and none of it is measured here.

## Instrumentation, and its coupling to checking

The counters named in the [directions](../directions.md) exist, but the
final-proof statistics are reached only through checking.
`PfManager::checkFinalProof` runs the finalizer traversal that invokes
`ProofFinalCallback::finalize`
([`proof_manager.cpp:293-297`](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/smt/proof_manager.cpp#L293-L297)),
and its only call site is inside a `options().smt.checkProofs` guard
([`solver_engine.cpp:1666-1673`](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/smt/solver_engine.cpp#L1666-L1673)).

Two consequences for measurement design, both predicted from the code:

1. The final rule and trust histograms are **not available in a run that does
   not also enable proof checking**. An experiment cannot treat them as free
   observations of the configuration whose cost it is measuring.
2. That same guarded block calls `connectProofToAssertions` on the SAT proof,
   and the proof-retrieval path calls it again when connecting to
   preprocessing
   ([`solver_engine.cpp:1955`](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/smt/solver_engine.cpp#L1955)).
   The method's own comment states the assumption it is making:
   "Note this assumes that connectProofToAssertions is only called once per
   unsat response. This method would need to cache its result otherwise."
   ([`proof_manager.cpp:190-191`](https://github.com/cvc5/cvc5/blob/3dcc1ef5421ab62cc1ee9af52d70042ce6861af0/src/smt/proof_manager.cpp#L190-L191))
   A run that both checks proofs and requests the proof may therefore perform
   postprocessing work more than once. **This is a code reading, not an
   observed double execution**, and confirming or refuting it is a task for
   the first instrumented run, not a claim of this record.

No counter found on these paths distinguishes proof nodes that reach the final
proof from proof nodes constructed and discarded, and no non-overlapping
per-phase timer partition for proof production was found.

## Limits of this record

Buildability, runtime behavior, proof validity and performance are not
established. The audit reads four paths and does not review the theory-level
proof generators, the prop-engine proof construction or any format other than
Eo/CPC and, incidentally, LFSC. Line anchors are valid only at the pinned
revision. Nothing here identifies which cost dominates; that requires the
instrument that [E13](../directions.md#e13-proof-work-accounting)
describes and that does not exist yet.

## What follows from the audit

Four mechanisms are visible in main that no surveyed fork branch addresses:
per-call proof node allocation without structural sharing
([E14](../directions.md#e14-proof-node-representation-and-allocation)),
full materialization before output
([E15](../directions.md#e15-streaming-proof-emission)), repeated whole-DAG
passes ([E16](../directions.md#e16-traversal-fusion)), and the absence of
a phase partition or a discarded-work counter
([E13](../directions.md#e13-proof-work-accounting)). Their priority
relative to the branch-derived directions is unknown and remains so until
E13's instrument exists.
