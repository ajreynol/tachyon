# Metagraphe rewrites

Generated from [rewrites.json](rewrites.json). **Do not edit this view by hand.**
See the [database guide](README.md) for filing and the
[reporting policy](reporting-policy.md) for reassessment and closure.

Regenerate from tachyon's root with `python3 tools/metagraphe/scripts/render_rewrite_db.py`; add `--check` to check freshness.

**16 candidate families; 21 proposed rewrites; 14 RARE drafts.**
**0 explicit closure verdicts; 0 fixes awaiting landing.**

A record is a candidate family, not a count of new rules or solved issues.
`argued` denotes a written validity argument, not a checked proof. RARE parser
acceptance does not establish correctness or solver performance. Priorities
are metagraphe's assessments; closure concerns the proposed rewrite.
Issues supply motivation and evidence; their states are snapshots at review.
Existing-rule investigations and other issue triage are retained in the
[scope archive](../docs/ledger/2026-09-19-rewrite-candidate-scope.md).

**Orientation: LHS -> RHS, complex -> simpler.** Compare lexicographically:
counts of the declared complex operators first, then structural term size.
Eliminating a costly operator can therefore justify a larger RHS. Records name
the precedence and rationale; these are candidate orderings, not measured runtimes.

## Overview

| Candidate | Priority | Validity | RARE drafts | Closure | Source issues |
| --- | --- | --- | --- | --- | --- |
| [M-1: Singleton replacement](#m-1) | 1 | argued | 2 | no closure recorded | [\#12936](https://github.com/cvc5/cvc5/issues/12936), [\#9875](https://github.com/cvc5/cvc5/issues/9875) |
| [M-2: Prefix before first match](#m-2) | 1 | argued | 1 | no closure recorded | [\#11362](https://github.com/cvc5/cvc5/issues/11362) |
| [M-3: Lexicographic prefix cancellation](#m-3) | 1 | argued | 2 | no closure recorded | [\#11151](https://github.com/cvc5/cvc5/issues/11151), [\#9875](https://github.com/cvc5/cvc5/issues/9875) |
| [M-4: Signed comparison disjunction](#m-4) | 1 | argued | 1 | no closure recorded | [\#11357](https://github.com/cvc5/cvc5/issues/11357) |
| [M-5: Complement of a character](#m-5) | 2 | argued | 1 | no closure recorded | [\#12815](https://github.com/cvc5/cvc5/issues/12815) |
| [M-6: Guarded zero division](#m-6) | 2 | argued | 1 | no closure recorded | [\#11201](https://github.com/cvc5/cvc5/issues/11201) |
| [M-7: Modular arithmetic](#m-7) | 2 | argued | 2 | no closure recorded | [\#11535](https://github.com/cvc5/cvc5/issues/11535), [\#11872](https://github.com/cvc5/cvc5/issues/11872) |
| [M-9: String order totality](#m-9) | 3 | argued | 0 | no closure recorded | [\#12042](https://github.com/cvc5/cvc5/issues/12042) |
| [M-10: Character\-language intersections](#m-10) | 3 | argued | 0 | no closure recorded | [\#11206](https://github.com/cvc5/cvc5/issues/11206) |
| [M-12: Remove absolute value from a modulus divisor](#m-12) | 3 | argued | 0 | no closure recorded | [\#9420](https://github.com/cvc5/cvc5/issues/9420) |
| [M-13: Nested replacement emptiness](#m-13) | 3 | argued | 0 | no closure recorded | [\#10508](https://github.com/cvc5/cvc5/issues/10508) |
| [M-14: Sequence prefix forces index zero](#m-14) | 3 | argued | 0 | no closure recorded | [\#11156](https://github.com/cvc5/cvc5/issues/11156) |
| [M-16: Inverse case conversion](#m-16) | 3 | unchecked | 0 | no closure recorded | [\#11970](https://github.com/cvc5/cvc5/issues/11970) |
| [M-18: BV quotient with no\-overflow conditions](#m-18) | 3 | argued | 0 | no closure recorded | [\#9417](https://github.com/cvc5/cvc5/issues/9417) |
| [M-21: Containment disjunction from a character\-union membership](#m-21) | 1 | argued | 1 | no closure recorded | — |
| [M-22: Idempotent nesting of regular\-expression star and plus](#m-22) | 1 | argued | 3 | no closure recorded | — |

## M-1

**Singleton replacement**

Priority: 1. Theories: sequences, strings.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

**Orientation order:** str\.replace\_all count > term size. Eliminate replace\_all before minimizing syntax size: containment of a replaced singleton becomes two plain containment tests\. The 6 \-&gt; 7 node growth and duplicated needle are explicit; matching cost and solver benefit remain unmeasured\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: s: String or Seq\(T\); u: same sort as s; r: same sort as s.

```text
(str.contains (str.replace_all s u r) u)
  ->
(and (str.contains s u) (str.contains r u))

when: (= (str.len u) 1)
```

Structural size: **6 -> 7** term nodes.

Lexicographic cost: **(1, 6) -> (0, 7)**.

### RARE drafts

```lisp
(define-rule metagraphe-contains-replace-all-unit
  ((s ?Seq) (r ?Seq) (x ?))
  (str.contains (str.replace_all s (seq.unit x) r) (seq.unit x))
  (and (str.contains s (seq.unit x))
       (str.contains r (seq.unit x))))
```

```lisp
(define-cond-rule metagraphe-contains-replace-all-char
  ((s ?Seq) (u ?Seq) (r ?Seq))
  (= (str.len u) 1)
  (str.contains (str.replace_all s u r) u)
  (and (str.contains s u) (str.contains r u)))
```

### Assessment and next step

- **Validity: argued.** Every original singleton occurrence is replaced\. An output occurrence must be inserted by a replacement, which requires both a source match and an occurrence in the replacement\.
- **Availability: source\-gap\-candidate.** The audited RARE and rewriteContains/rewriteReplaceAll paths lack this composition; related single\-replacement rules exist\.
- **Value: unmeasured.** Empty replacement makes the containment assertion false; prefix variants need additional reasoning\.

**RARE syntax:** passed at [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- The issue proposal omits source containment: s=\[\], u=\[0\], r=\[0\] makes its LHS false and RHS true\.
- Do not generalize to longer needles: deleting ab from aabb creates ab across a boundary\.
- The nonempty\-replacement RHS adds containment work\.

**Next step:** Probe both singleton sequences and one\-character strings, including no\-match and empty\-replacement cases; measure matching and proof support\.

### Evidence and follow-up

Source issues: [\#12936](https://github.com/cvc5/cvc5/issues/12936) (open at review), [\#9875](https://github.com/cvc5/cvc5/issues/9875) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#m-1-singleton-replacement) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Dated reassessments:**

- 2026-09-19: Reoriented the same equality from complex \-&gt; simpler by structural term size; reviewed direction\-dependent availability and value\. [review](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-orientation.md); [previous record](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-orientation-before.json).
- 2026-09-19: The human clarified lexicographic precedence: complex operators first, structural term size last\. Restored operator elimination, allowing the stated syntax growth\. [review](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-operator-order.md); [previous record](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-operator-order-before.json).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/12936](https://github.com/cvc5/cvc5/issues/12936)
- [https://github\.com/cvc5/cvc5/issues/9875\#issuecomment\-1625411673](https://github.com/cvc5/cvc5/issues/9875#issuecomment-1625411673)

**Source references:**

- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/rewrites](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/rewrites)
- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/sequences\_rewriter\.cpp](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/sequences_rewriter.cpp)

No delivery recorded.

[Back to overview](#overview)

## M-2

**Prefix before first match**

Priority: 1. Theories: strings, sequences.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

**Orientation rationale:** decrease structural term size.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: s: String or Seq\(T\); t: same sort as s.

```text
(str.contains (str.substr s 0 (str.indexof s t 0)) t)
  ->
(= (str.len t) 0)

when: true
```

Structural size: **9 -> 4** term nodes.

### RARE drafts

```lisp
(define-rule metagraphe-contains-before-indexof
  ((s ?Seq) (t ?Seq))
  (str.contains (str.substr s 0 (str.indexof s t 0)) t)
  (= (str.len t) 0))
```

### Assessment and next step

- **Validity: argued.** A nonempty needle cannot occur before its first occurrence\. An absent needle gives index \-1 and an empty substring\. An empty needle occurs in the resulting empty prefix\.
- **Availability: source\-gap\-candidate.** No corresponding composition was found in the inspected RARE or contains/indexof implementation\.
- **Value: unmeasured.** Discharges the added tautological fact; speeding up the original input may require generating a lemma\.

**RARE syntax:** passed at [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- The RHS is true for the empty needle; unconditional false is invalid\.
- The useful fact is not present in the original base benchmark\.

**Next step:** Probe empty, missing, overlapping, and multi\-character needles, then compare the complete original query with and without lemma generation\.

### Evidence and follow-up

Source issues: [\#11362](https://github.com/cvc5/cvc5/issues/11362) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#m-2-prefix-before-first-match) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/11362](https://github.com/cvc5/cvc5/issues/11362)
- [https://github\.com/cvc5/cvc5/issues/11362\#issuecomment\-2474655250](https://github.com/cvc5/cvc5/issues/11362#issuecomment-2474655250)

**Source references:**

- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/rewrites](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/rewrites)
- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/sequences\_rewriter\.cpp](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/sequences_rewriter.cpp)
- [https://smt\-lib\.org/theories\-UnicodeStrings\.shtml](https://smt-lib.org/theories-UnicodeStrings.shtml)

No delivery recorded.

[Back to overview](#overview)

## M-3

**Lexicographic prefix cancellation**

Priority: 1. Theories: strings.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

**Orientation rationale:** decrease structural term size.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: s: String; t: String.

```text
(str.< (str.++ s t) s)
  ->
false

when: true
```

Structural size: **5 -> 1** term nodes.

### Rewrite 2

Notation: SMT\-LIB term schema.

Variables: s: String; t: String.

```text
(str.<= (str.++ s t) s)
  ->
(= t "")

when: true
```

Structural size: **5 -> 3** term nodes.

### RARE drafts

```lisp
(define-rule metagraphe-str-lt-own-prefix
  ((s String) (ts String :list))
  (str.< (str.++ s ts) s)
  false)
```

```lisp
(define-rule metagraphe-str-leq-own-prefix
  ((s String) (ts String :list))
  (str.<= (str.++ s ts) s)
  (= (str.++ ts) ""))
```

### Assessment and next step

- **Validity: argued.** A string never precedes its own prefix; the non\-strict relation holds only when the added suffix is empty\.
- **Availability: source\-gap\-candidate.** The inspected string\-order implementation handles constants, equality, empty operands and differing constant prefixes, without cancelling a shared symbolic prefix\.
- **Value: unmeasured.** Directly refutes the strict example and the non\-strict example with a nonempty suffix\.

**RARE syntax:** passed at [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- Strict comparison already normalizes to disequality and non\-strict comparison\.
- Flattened n\-ary concatenation needs list matching; the RARE drafts include it\.

**Next step:** Probe both original and normalized comparison forms, including empty suffixes and flattened concatenation\.

### Evidence and follow-up

Source issues: [\#11151](https://github.com/cvc5/cvc5/issues/11151) (open at review), [\#9875](https://github.com/cvc5/cvc5/issues/9875) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#m-3-lexicographic-prefix-cancellation) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/11151](https://github.com/cvc5/cvc5/issues/11151)
- [https://github\.com/cvc5/cvc5/issues/9875](https://github.com/cvc5/cvc5/issues/9875)

**Source references:**

- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/rewrites](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/rewrites)
- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/strings\_rewriter\.cpp](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/strings_rewriter.cpp)

No delivery recorded.

[Back to overview](#overview)

## M-4

**Signed comparison disjunction**

Priority: 1. Theories: bit\-vectors, booleans.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

**Orientation rationale:** decrease structural term size.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: x: BitVec\(w\); y: BitVec\(w\).

```text
(or (= x y) (bvslt x y))
  ->
(bvsle x y)

when: w is a positive integer
```

Structural size: **7 -> 3** term nodes.

### RARE drafts

```lisp
(define-rule metagraphe-bv-eq-or-slt
  ((x ?BitVec) (y ?BitVec))
  (or (= x y) (bvslt x y))
  (bvsle x y))
```

### Assessment and next step

- **Validity: argued.** Non\-strict signed order is the reflexive closure of strict signed order, at every common positive width\.
- **Availability: source\-gap\-candidate.** No direct disjunction rule was found in the inspected BV RARE file\. Maintainer reports a solution under BV logic or \-\-cegqi\-full\.
- **Value: unmeasured.** The reporter identifies this equivalent form as sufficient for the quantified example under the reported configuration\.

**RARE syntax:** passed at [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- Do not mix signed and unsigned comparisons\.
- Inspect equality/Boolean operand ordering and subsequent bvsle elimination\.
- An option\-sensitive quantifier issue is not general BV incompleteness\.

**Next step:** Compare simplification and solving under ALL, BV, and \-\-cegqi\-full at a matching clean baseline\.

### Evidence and follow-up

Source issues: [\#11357](https://github.com/cvc5/cvc5/issues/11357) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#m-4-signed-comparison-disjunction) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/11357](https://github.com/cvc5/cvc5/issues/11357)
- [https://github\.com/cvc5/cvc5/issues/11357\#issuecomment\-2476882359](https://github.com/cvc5/cvc5/issues/11357#issuecomment-2476882359)

**Source references:**

- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/bv/rewrites\-simplification](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/bv/rewrites-simplification)

No delivery recorded.

[Back to overview](#overview)

## M-5

**Complement of a character**

Priority: 2. Theories: strings, regular\-expressions.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

**Orientation order:** re\.comp count > term size. Eliminate general regex complement inside this one\-character class before minimizing syntax size\. Two full\-alphabet ranges expose a positive character\-class representation at 5 \-&gt; 7 nodes; actual regex\-engine benefit remains unmeasured\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: none.

```text
(re.inter re.allchar (re.comp (str.to_re "/")))
  ->
(re.union (re.range "\u{0}" ".") (re.range "0" "\u{2ffff}"))

when: SMT-LIB Unicode Strings alphabet: code points 0 through 0x2ffff
```

Structural size: **5 -> 7** term nodes.

Lexicographic cost: **(1, 5) -> (0, 7)**.

### RARE drafts

```lisp
(define-rule metagraphe-re-allchar-except-slash ()
  (re.inter re.allchar (re.comp (str.to_re "/")))
  (re.union (re.range "\u{0}" ".")
            (re.range "0" "\u{2ffff}")))
```

### Assessment and next step

- **Validity: argued.** The two ranges contain exactly the permitted single characters other than slash, whose code point is 47\.
- **Availability: source\-gap\-candidate.** No literal complement\-to\-ranges RARE rule was found; regex inclusion and normalization need further investigation\.
- **Value: unmeasured.** Simplifies the path\-segment character class; impact on concatenated language inclusion remains unmeasured\.

**RARE syntax:** passed at [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- The printable\-ASCII replacement in a comment restricts the language and is not equivalent\.
- Complement alone also admits strings whose length is not one\.
- A general character\-class normalizer should handle endpoint exclusions\.

**Next step:** Compare the exact full\-alphabet encoding on the original inclusion query, then investigate a general constant character\-class rule\.

### Evidence and follow-up

Source issues: [\#12815](https://github.com/cvc5/cvc5/issues/12815) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#m-5-complement-of-a-character) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Dated reassessments:**

- 2026-09-19: Reoriented the same equality from complex \-&gt; simpler by structural term size; reviewed direction\-dependent availability and value\. [review](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-orientation.md); [previous record](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-orientation-before.json).
- 2026-09-19: The human clarified lexicographic precedence: complex operators first, structural term size last\. Restored operator elimination, allowing the stated syntax growth\. [review](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-operator-order.md); [previous record](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-operator-order-before.json).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/12815](https://github.com/cvc5/cvc5/issues/12815)
- [https://github\.com/cvc5/cvc5/issues/12815\#issuecomment\-5257520827](https://github.com/cvc5/cvc5/issues/12815#issuecomment-5257520827)

**Source references:**

- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/rewrites](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/rewrites)
- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/sequences\_rewriter\.cpp](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/sequences_rewriter.cpp)
- [https://smt\-lib\.org/theories\-UnicodeStrings\.shtml](https://smt-lib.org/theories-UnicodeStrings.shtml)

No delivery recorded.

[Back to overview](#overview)

## M-6

**Guarded zero division**

Priority: 2. Theories: integers, strings.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

**Orientation rationale:** decrease structural term size.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: v: Int.

```text
(ite (= v 0) 0 (div 0 v))
  ->
0

when: true
```

Structural size: **8 -> 1** term nodes.

### RARE drafts

```lisp
(define-rule metagraphe-int-zero-div-guard ((v Int))
  (ite (= v 0) 0 (div 0 v))
  0)
```

### Assessment and next step

- **Validity: argued.** The selected branch is zero when v=0; for nonzero v, Euclidean division of zero is zero\.
- **Availability: source\-gap\-candidate.** No surface guarded\-division rule was found in the inspected arithmetic RARE file; ITE contextual simplification and division elimination remain to be checked\.
- **Value: unmeasured.** Collapses the term inside the reported string\-length/modulus expression to expose constant evaluation\.

**RARE syntax:** passed at [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- Surface div\(0,v\) cannot be rewritten to zero without the guard: division by zero is underspecified\.

**Next step:** Inspect ITE and division normalization and probe the complete reported arithmetic/string composition\.

### Evidence and follow-up

Source issues: [\#11201](https://github.com/cvc5/cvc5/issues/11201) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#m-6-guarded-zero-division) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/11201](https://github.com/cvc5/cvc5/issues/11201)
- [https://smt\-lib\.org/theories\-Ints\.shtml](https://smt-lib.org/theories-Ints.shtml)

**Source references:**

- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/arith/rewrites](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/arith/rewrites)

No delivery recorded.

[Back to overview](#overview)

## M-7

**Modular arithmetic**

Priority: 2. Theories: integers.

**Closure:** no closure recorded.

**Application context:** Internal totalized arithmetic; surface\-to\-internal conversion may require contextual nonzero facts\.

**Orientation rationale:** decrease structural term size.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: a: Int; b: Int; c: Int.

```text
(mod_total (* a c b) c)
  ->
0

when: true
```

Structural size: **6 -> 1** term nodes.

### Rewrite 2

Notation: SMT\-LIB term schema.

Variables: n: Int.

```text
(mod_total (* n (+ n 1)) 2)
  ->
0

when: true
```

Structural size: **7 -> 1** term nodes.

### RARE drafts

```lisp
(define-rule metagraphe-mod-total-factor
  ((xs Int :list) (c Int) (ys Int :list))
  (mod_total (* xs c ys) c)
  0)
```

```lisp
(define-rule metagraphe-mod-total-consecutive ((n Int))
  (mod_total (* n (+ n 1)) 2)
  0)
```

### Assessment and next step

- **Validity: argued.** A product containing a nonzero divisor is divisible by it\. At c=0 the product is zero and internal mod\_total\(0,0\)=0\. One of two consecutive integers is even, including for negative n\.
- **Availability: source\-gap\-candidate.** The inspected arithmetic rules cover nested moduli but not these patterns\. Existing nonlinear extended simplification and normalization need comparison\.
- **Value: unmeasured.** Removes the nonlinear remainder in each example if the rule is reached\.

**RARE syntax:** passed at [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- The unconditional factor rule is for internal mod\_total, not surface mod\.
- For surface mod, c\!=0 must be established and transported to the application stage\.
- Polynomial expansion may replace n\*\(n\+1\) with n\*n\+n before matching\.

**Next step:** Probe internal and surface forms with recorded nonzero context and factored/expanded polynomial forms\.

### Evidence and follow-up

Source issues: [\#11535](https://github.com/cvc5/cvc5/issues/11535) (open at review), [\#11872](https://github.com/cvc5/cvc5/issues/11872) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#m-7-modular-arithmetic) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/11535](https://github.com/cvc5/cvc5/issues/11535)
- [https://github\.com/cvc5/cvc5/issues/11535\#issuecomment\-2605819222](https://github.com/cvc5/cvc5/issues/11535#issuecomment-2605819222)
- [https://github\.com/cvc5/cvc5/issues/11872](https://github.com/cvc5/cvc5/issues/11872)

**Source references:**

- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/arith/rewrites](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/arith/rewrites)
- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/arith/arith\_rewriter\.cpp](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/arith/arith_rewriter.cpp)

No delivery recorded.

[Back to overview](#overview)

## M-9

**String order totality**

Priority: 3. Theories: strings, booleans.

**Closure:** no closure recorded.

**Application context:** May require preprocessing across assertions or a theory lemma\.

**Orientation rationale:** decrease structural term size.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: x: String; y: String.

```text
(and (not (str.< x y)) (not (str.< y x)))
  ->
(= x y)

when: true
```

Structural size: **9 -> 3** term nodes.

No RARE draft is filed.

### Assessment and next step

- **Validity: argued.** Totality of lexicographic order makes incomparable strings equal\.
- **Availability: unchecked.** The source transforms strict order, and the original constraints are separate assertions; no runtime or full preprocessing audit established a matching gap\.
- **Value: unmeasured.** Combined with the asserted disequality, exposes a contradiction\.

**RARE syntax:** not\-run.

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- A Boolean conjunction rule does not automatically combine separately asserted constraints\.

**Next step:** Compare the combined term and original assertion set, inspecting strict\-order elimination and lemma generation\.

### Evidence and follow-up

Source issues: [\#12042](https://github.com/cvc5/cvc5/issues/12042) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#m-9-string-order-totality) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/12042](https://github.com/cvc5/cvc5/issues/12042)

**Source references:**

- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/strings\_rewriter\.cpp](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/strings_rewriter.cpp)

No delivery recorded.

[Back to overview](#overview)

## M-10

**Character\-language intersections**

Priority: 3. Theories: strings, regular\-expressions.

**Closure:** no closure recorded.

**Application context:** Requires a character\-language entailment check before applying the schema\.

**Orientation rationale:** decrease structural term size.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: A: RegLan; B: RegLan.

```text
(re.inter (re.* A) (re.* B))
  ->
(re.* (re.inter A B))

when: A and B accept only strings of length one
```

Structural size: **5 -> 4** term nodes.

No RARE draft is filed.

### Assessment and next step

- **Validity: argued.** For languages of single characters, either star constrains every position independently; intersection restricts each character to both alphabets\.
- **Availability: unchecked.** Existing regex inclusion and membership normalization need a focused audit and runtime probe\.
- **Value: unmeasured.** Reduces \(a&#124;b\)\* intersect \(b&#124;c\)\* to b\*, leaving commutation/periodicity reasoning in the complete issue\.

**RARE syntax:** not\-run.

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- Invalid for arbitrary languages: A=\{ab\}, B=\{a,b\} admits ab on the left but not on the proposed right\.
- This normalization alone does not settle the original query\.

**Next step:** Audit regex normalization, discharge the character\-language condition, and compare the full normalized query\.

### Evidence and follow-up

Source issues: [\#11206](https://github.com/cvc5/cvc5/issues/11206) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#m-10-character-language-intersections) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/11206](https://github.com/cvc5/cvc5/issues/11206)

**Source references:**

- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/sequences\_rewriter\.cpp](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/sequences_rewriter.cpp)

No delivery recorded.

[Back to overview](#overview)

## M-12

**Remove absolute value from a modulus divisor**

Priority: 3. Theories: integers.

**Closure:** no closure recorded.

**Application context:** Remove abs from a modulus divisor under the explicit nonzero condition\. Availability of this direction is unchecked; historical learned\-rewrite discussion is source context, not the proposed finding\.

**Orientation rationale:** decrease structural term size.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: x: Int; y: Int.

```text
(mod x (abs y))
  ->
(mod x y)

when: (not (= y 0))
```

Structural size: **4 -> 3** term nodes.

No RARE draft is filed.

### Assessment and next step

- **Validity: argued.** Euclidean remainder depends on the absolute magnitude of a nonzero divisor\.
- **Availability: unchecked.** The issue discussion concerns sign normalization and \-\-learned\-rewrite; it does not establish the pinned solver's behavior for removing abs\.
- **Value: unmeasured.** Reduces structural term size from 4 to 3 nodes by removing abs\. Runtime usefulness and interaction with sign normalization remain unmeasured\.

**RARE syntax:** not\-run.

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- The nonzero condition is required for surface mod\.
- Historical option support does not establish the behavior of the pinned default solver\.

**Next step:** Probe mod\(x,abs\(y\)\) with a known nonzero y under default and learned\-rewrite settings; check whether the smaller divisor is expanded again\.

### Evidence and follow-up

Source issues: [\#9420](https://github.com/cvc5/cvc5/issues/9420) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Dated reassessments:**

- 2026-09-19: Reoriented the same equality from complex \-&gt; simpler by structural term size; reviewed direction\-dependent availability and value\. [review](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-orientation.md); [previous record](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-orientation-before.json).
- 2026-09-19: The candidate\-only scope review retains the explicit abs\-elimination proposal and corrects its historical existing\-coverage classification\. No new availability or runtime claim is made\. [review](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-candidate-scope.md); [previous record](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-candidate-scope-before.json).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/9420](https://github.com/cvc5/cvc5/issues/9420)
- [https://github\.com/cvc5/cvc5/issues/9420\#issuecomment\-1404268724](https://github.com/cvc5/cvc5/issues/9420#issuecomment-1404268724)

No delivery recorded.

[Back to overview](#overview)

## M-13

**Nested replacement emptiness**

Priority: 3. Theories: strings.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

**Orientation rationale:** decrease structural term size.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: a: String; b: String; c: String.

```text
(= (str.replace_all (str.replace_all a b a) c a) "")
  ->
(= a "")

when: true
```

Structural size: **9 -> 3** term nodes.

No RARE draft is filed.

### Assessment and next step

- **Validity: argued.** If a is empty both stages stay empty; otherwise each stage keeps a nonempty source or inserts the nonempty replacement a\.
- **Availability: unchecked.** No focused availability audit was performed for this additional lead\.
- **Value: unmeasured.** Contradicts the reported simultaneous lower lexicographic bound A&lt;=a\.

**RARE syntax:** not\-run.

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- Prefer reusable nonemptiness rules over a hard\-coded two\-level replacement match\.

**Next step:** Reduce to reusable emptiness/nonemptiness rules and audit existing replacement reasoning\.

### Evidence and follow-up

Source issues: [\#10508](https://github.com/cvc5/cvc5/issues/10508) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/10508](https://github.com/cvc5/cvc5/issues/10508)

No delivery recorded.

[Back to overview](#overview)

## M-14

**Sequence prefix forces index zero**

Priority: 3. Theories: sequences.

**Closure:** no closure recorded.

**Application context:** Requires the prefix fact as a premise or in a combined Boolean term\.

**Orientation rationale:** decrease structural term size.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: s: Seq\(T\); t: Seq\(T\).

```text
(seq.indexof s t 0)
  ->
0

when: (seq.prefixof t s)
```

Structural size: **4 -> 1** term nodes.

No RARE draft is filed.

### Assessment and next step

- **Validity: argued.** A prefix has an occurrence at index zero, including the empty prefix\.
- **Availability: unchecked.** No focused context or matching audit was performed\.
- **Value: unmeasured.** Contradicts the index bound in the reported input\.

**RARE syntax:** not\-run.

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- Prefix and index assertions are separate; prefix elimination can change the match\.

**Next step:** Test a conditional lemma or conjunction rewrite on both a combined term and the original assertions\.

### Evidence and follow-up

Source issues: [\#11156](https://github.com/cvc5/cvc5/issues/11156) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/11156](https://github.com/cvc5/cvc5/issues/11156)

No delivery recorded.

[Back to overview](#overview)

## M-16

**Inverse case conversion**

Priority: 3. Theories: strings, regular\-expressions.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

**Orientation order:** str\.to\_lower count > term size. Eliminate case conversion against the fixed ASCII target before minimizing syntax size\. Two constant equality tests grow from 4 \-&gt; 7 nodes and duplicate s; exact extension semantics and runtime benefit remain unchecked\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: s: String.

```text
(= (str.to_lower s) "a")
  ->
(or (= s "a") (= s "A"))

when: Subject to verification against cvc5 case-conversion semantics
```

Structural size: **4 -> 7** term nodes.

Lexicographic cost: **(1, 4) -> (0, 7)**.

No RARE draft is filed.

### Assessment and next step

- **Validity: unchecked.** An ASCII preimage suggests this identity, but the survey did not audit the exact extension semantics\.
- **Availability: unchecked.** The maintainer describes a broader solver technique; no existing implementation audit was completed\.
- **Value: unmeasured.** Could replace inverse conversion against a fixed target by character choices or regex membership\.

**RARE syntax:** not\-run.

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- Long targets require length control and growth analysis; do not claim the ASCII example establishes a Unicode\-wide conversion rule\.

**Next step:** Verify the exact conversion semantics, then measure preimage encodings and term growth\.

### Evidence and follow-up

Source issues: [\#11970](https://github.com/cvc5/cvc5/issues/11970) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Dated reassessments:**

- 2026-09-19: Reoriented the same equality from complex \-&gt; simpler by structural term size; reviewed direction\-dependent availability and value\. [review](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-orientation.md); [previous record](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-orientation-before.json).
- 2026-09-19: The human clarified lexicographic precedence: complex operators first, structural term size last\. Restored operator elimination, allowing the stated syntax growth\. [review](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-operator-order.md); [previous record](../../../tools/metagraphe/docs/ledger/2026-09-19-rewrite-operator-order-before.json).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/11970](https://github.com/cvc5/cvc5/issues/11970)
- [https://github\.com/cvc5/cvc5/issues/11970\#issuecomment\-2956111004](https://github.com/cvc5/cvc5/issues/11970#issuecomment-2956111004)

No delivery recorded.

[Back to overview](#overview)

## M-18

**BV quotient with no\-overflow conditions**

Priority: 3. Theories: bit\-vectors.

**Closure:** no closure recorded.

**Application context:** Requires divisor, remainder and no\-overflow facts from the assertion context\.

**Orientation rationale:** decrease structural term size.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: q: BitVec\(w\); y: BitVec\(w\); r: BitVec\(w\).

```text
(bvudiv (bvadd (bvmul q y) r) y)
  ->
q

when: w>0; y!=0; unsigned r<y; unsigned q*y and q*y+r do not overflow
```

Structural size: **7 -> 1** term nodes.

No RARE draft is filed.

### Assessment and next step

- **Validity: argued.** Under the divisor, remainder and no\-overflow premises this is the ordinary quotient/remainder decomposition within the width\-w range\.
- **Availability: unchecked.** The survey identified a contextual lemma direction, not a missing local rewrite\.
- **Value: unmeasured.** Could establish the quotient assertion in the issue once all premises are available\.

**RARE syntax:** not\-run.

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- Both multiplication and addition no\-overflow conditions are necessary\.
- These premises do not justify unrestricted modular cancellation\.

**Next step:** Encode and validate all width\-dependent premises, then determine how the solver could expose them to a lemma\.

### Evidence and follow-up

Source issues: [\#9417](https://github.com/cvc5/cvc5/issues/9417) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/9417](https://github.com/cvc5/cvc5/issues/9417)

No delivery recorded.

[Back to overview](#overview)

## M-21

**Containment disjunction from a character\-union membership**

Priority: 1. Theories: strings, regular\-expressions, sequences.

**Closure:** no closure recorded.

**Application context:** Local term rewriting on STRING\_IN\_REGEXP, beside Rewrite::RE\_CONCAT\_TO\_CONTAINS in SequencesRewriter::rewriteMembership\. cvc5's REGEXP\_UNION is n\-ary and flattened, and the motivating benchmarks use five arms, so the rule that actually fires has to be n\-ary\. Ordinary RARE cannot map str\.to\_re over a :list parameter, so the n\-ary form would be a C\+\+ rule; the filed draft is the two\-arm instance\.

**Orientation order:** str\.in\_re count > re\.\* count > re\.\+\+ count > re\.union count > str\.to\_re count > term size. Eliminate the regular\-expression membership first: str\.in\_re drives unfolding and automaton work, while str\.contains is handled by the string rewriter and the extended\-function reductions\. All five regular expression operators disappear\. Size falls for up to seven union arms and grows beyond that, because the right\-hand side repeats x once per arm; that growth is accepted under the operator\-first ordering\.

### Rewrite 1

Notation: SMT\-LIB term schema; two\-arm instance of the n\-ary union.

Variables: x: String or \(Seq T\); s1: same sort as x; s2: same sort as x.

```text
(str.in_re x (re.++ (re.* re.allchar) (re.union (str.to_re s1) (str.to_re s2)) (re.* re.allchar)))
  ->
(or (str.contains x s1) (str.contains x s2))

when: none; every union argument must be (str.to_re t) and every other concatenation argument must be (re.* re.allchar)
```

Structural size: **12 -> 7** term nodes.

Lexicographic cost: **(1, 2, 1, 1, 2, 12) -> (0, 0, 0, 0, 0, 7)**.

### Rewrite 2

Notation: SMT\-LIB term schema; three\-arm instance showing the n\-ary shape.

Variables: x: String or \(Seq T\); s1: same sort as x; s2: same sort as x; s3: same sort as x.

```text
(str.in_re x (re.++ (re.* re.allchar) (re.union (str.to_re s1) (str.to_re s2) (str.to_re s3)) (re.* re.allchar)))
  ->
(or (str.contains x s1) (str.contains x s2) (str.contains x s3))

when: none; same restriction on the union and concatenation arguments
```

Structural size: **14 -> 10** term nodes.

Lexicographic cost: **(1, 2, 1, 1, 3, 14) -> (0, 0, 0, 0, 0, 10)**.

### RARE drafts

```lisp
(define-rule metagraphe-re-ctn-union-two
  ((x ?Seq) (s ?Seq) (t ?Seq))
  (str.in_re x (re.++ (re.* re.allchar) (re.union (str.to_re s) (str.to_re t)) (re.* re.allchar)))
  (or (str.contains x s) (str.contains x t)))
```

### Assessment and next step

- **Validity: argued.** Concatenation distributes over union, so the left\-hand language is the union of Sigma\* \{si\} Sigma\*, and membership in Sigma\* \{si\} Sigma\* is the SMT\-LIB definition of str\.contains\(x, si\)\. No side condition is needed: an empty si makes both sides true, and the argument is alphabet\-independent, so it covers sequences\. Z3\-Noodler returned unsat for \(distinct lhs rhs\) on all nine constant instantiations tried and cvc5 agreed on six, timing out on three; with symbolic needles both solvers left the question open\.
- **Availability: source\-gap\-candidate.** At 40a4bb7e43adf97534c29a52ed079c4efd687644, \-\-preprocess\-only \-o post\-asserts rewrites x in \(re\.\+\+ Sigma\* \(str\.to\_re "&lt;"\) Sigma\*\) to \(str\.contains x "&lt;"\) but returns the union form unchanged, under the default configuration and under \-\-re\-elim=on and \-\-re\-elim=agg\. rewriteMembership's REGEXP\_CONCAT branch accepts at most one STRING\_TO\_REGEXP child and rejects any other child, so a REGEXP\_UNION aborts the match; RE\_IN\_ANDOR only distributes a union that is the whole regular expression\.
- **Value: measured.** No speedup was measured\. Applying the rewrite by hand to 20230329\-denghang/instance51087\.smt2 moved cvc5 from a 10\.12 s median to 11\.09 s over three repetitions at a 60 s limit, and a focused probe containing nothing but this pattern ran in about 0\.006 s with and without the rewrite at length bounds 200, 1000 and 4000\. cvc5 already handles these memberships cheaply; the cost on the motivating input is the 31\-way re\.loop expansion beside them\. The case for the rule is the elimination of a regular\-expression membership and five regular\-expression operators, and the pattern's occurrence in 998 of the 84,411 QF\_SLIA inputs, not a runtime gain\. Whether an in\-solver implementation pays for its matching cost is untested\.

**RARE syntax:** passed at [40a4bb7e43adf97534c29a52ed079c4efd687644](https://github.com/cvc5/cvc5/commit/40a4bb7e43adf97534c29a52ed079c4efd687644).

**Solver check:** recorded; [evidence](../../../tools/metagraphe/docs/ledger/2026-09-20-string-benchmark-comparison.md).

**Performance check:** recorded; [evidence](../../../tools/metagraphe/docs/ledger/2026-09-20-string-benchmark-comparison.md).

**Cautions:**

- The filed RARE draft is the two\-arm instance; the five\-arm unions in the motivating benchmarks need an n\-ary rule that ordinary RARE cannot express\.
- Sound only when every union argument is \(str\.to\_re t\) and every remaining concatenation argument is \(re\.\* re\.allchar\); one other arm leaves a str\.in\_re on the right and loses the elimination\.
- From eight union arms on, the right\-hand side has more term nodes than the left, because x is repeated once per arm\.
- The schematic equivalence with symbolic needles was not decided: cvc5 timed out and Z3\-Noodler answered unknown\.
- A fixed\-point peeling variant parses but re\-introduces str\.in\_re at each step, so it is the wrong orientation and is not filed\.

**Next step:** Implement the n\-ary form beside RE\_CONCAT\_TO\_CONTAINS and measure it on the 14 sampled 20230329\-denghang inputs, separating its effect from the re\.loop elimination that dominates instance51087; then look for the pattern in QF\_S and QF\_SNIA, which this sample did not cover\.

### Evidence and follow-up

No source issue: this candidate comes from a benchmark comparison over SMT\-LIB 2026 non\-incremental QF\_SLIA \(84,411 inputs, 14 families\); 200\-input stratified sample, seed metagraphe\-2026\-09\-20.

Observed: 2026-09-20 at cvc5 source [40a4bb7e43adf97534c29a52ed079c4efd687644](https://github.com/cvc5/cvc5/commit/40a4bb7e43adf97534c29a52ed079c4efd687644).

Koine ingestion: first 2026-09-20; last 2026-09-20.

Corpus: SMT\-LIB 2026 non\-incremental QF\_SLIA \(84,411 inputs, 14 families\); 200\-input stratified sample, seed metagraphe\-2026\-09\-20; [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-20-string-benchmark-comparison.md).

**Source references:**

- [https://github\.com/cvc5/cvc5/blob/40a4bb7e43adf97534c29a52ed079c4efd687644/src/theory/strings/sequences\_rewriter\.cpp](https://github.com/cvc5/cvc5/blob/40a4bb7e43adf97534c29a52ed079c4efd687644/src/theory/strings/sequences_rewriter.cpp)
- [https://github\.com/cvc5/cvc5/blob/40a4bb7e43adf97534c29a52ed079c4efd687644/src/theory/strings/rewrites](https://github.com/cvc5/cvc5/blob/40a4bb7e43adf97534c29a52ed079c4efd687644/src/theory/strings/rewrites)

No delivery recorded.

[Back to overview](#overview)

## M-22

**Idempotent nesting of regular\-expression star and plus**

Priority: 1. Theories: strings, regular\-expressions.

**Closure:** no closure recorded.

**Application context:** Local term rewriting on REGEXP\_STAR, beside Rewrite::RE\_STAR\_NESTED\_STAR in SequencesRewriter::rewriteStarRegExp and the re\-star\-star RARE rule\. re\-plus\-elim runs first, so the core rule has to match \(re\.\* \(re\.\+\+ r \(re\.\* r\)\)\)\. The \(r\+\)\+ case then closes through the existing re\-concat\-star\-repeat rule, which collapses the resulting \(re\.\+\+ r \(re\.\* r\) \(re\.\* r\)\)\.

**Orientation order:** re\.\* count > re\.\+\+ count > term size. Remove a star before removing a concatenation: each surviving re\.\* is a separate unfolding obligation for the regular\-expression solver, and the nested body duplicates the whole of r\. Both counts and the term size fall, so no growth has to be accepted here\.

### Rewrite 1

Notation: SMT\-LIB term schema, stated on the form cvc5 produces after re\-plus\-elim.

Variables: r: RegLan.

```text
(re.* (re.++ r (re.* r)))
  ->
(re.* r)

when: none
```

Structural size: **5 -> 2** term nodes.

Lexicographic cost: **(2, 1, 5) -> (1, 0, 2)**.

### Rewrite 2

Notation: SMT\-LIB term schema, surface form before re\-plus\-elim.

Variables: r: RegLan.

```text
(re.* (re.+ r))
  ->
(re.* r)

when: none
```

Structural size: **3 -> 2** term nodes.

Lexicographic cost: **(1, 0, 3) -> (1, 0, 2)**.

### Rewrite 3

Notation: SMT\-LIB term schema, surface form before re\-plus\-elim.

Variables: r: RegLan.

```text
(re.+ (re.+ r))
  ->
(re.+ r)

when: none
```

Structural size: **3 -> 2** term nodes.

Lexicographic cost: **(0, 0, 3) -> (0, 0, 2)**.

### RARE drafts

```lisp
(define-rule metagraphe-re-star-plus-elim
  ((r RegLan))
  (re.* (re.++ r (re.* r)))
  (re.* r))
```

```lisp
(define-rule metagraphe-re-star-plus
  ((r RegLan))
  (re.* (re.+ r))
  (re.* r))
```

```lisp
(define-rule metagraphe-re-plus-plus
  ((r RegLan))
  (re.+ (re.+ r))
  (re.+ r))
```

### Assessment and next step

- **Validity: argued.** L\(\(R R\*\)\*\) = \(L\(R\) L\(R\)\*\)\* = \(L\(R\)\+\)\* = L\(R\)\*\. One inclusion holds because L\(R\)\+ is contained in L\(R\)\*; the other because every nonempty member of L\(R\)\* is a concatenation of at least one R\-word\. No side condition, and the empty, re\.none, nullable and starred bodies are all covered\. Z3\-Noodler returned unsat for \(distinct lhs rhs\) on all ten concrete r tried, and cvc5 agreed on the four it did not time out on\. cvc5 rejects regular\-expression variables, so no schematic solver check was possible\.
- **Availability: source\-gap\-candidate.** At 40a4bb7e43adf97534c29a52ed079c4efd687644, \-\-preprocess\-only \-o post\-asserts reduces \(re\.\* \(re\.\* r\)\) and \(re\.\+ \(re\.\* r\)\) to \(re\.\* r\) but leaves \(re\.\* \(re\.\+ r\)\) as \(re\.\* \(re\.\+\+ r \(re\.\* r\)\)\) and \(re\.\+ \(re\.\+ r\)\) as \(re\.\+\+ r \(re\.\* r\) \(re\.\* \(re\.\+\+ r \(re\.\* r\)\)\)\)\. rewriteStarRegExp handles a nested star, an empty or re\.none body and unions containing re\.allchar or epsilon, but no body of the form \(re\.\+\+ r \(re\.\* r\)\)\.
- **Value: measured.** Mixed, and negative where it matters most\. On the two stringfuzz inputs that motivated it, applying the rewrite by hand changed nothing: regex\-lengths\-00426\-14 stayed a 60 s timeout and variants/2f407694 moved from a 30\.99 s median to 31\.20 s\. In a focused probe containing only the nesting, cvc5 went from a 60 s timeout to a 0\.409 s median at a length\-100 bound and to 22\.17 s at 400, and still timed out at 1000; all medians are over three repetitions\. The pattern occurs 88,572 times in 4,192 of the 84,411 QF\_SLIA inputs, almost all fuzzer\-generated\. The scratch\-input effect is not evidence that an in\-solver rule would behave the same: matching cost and interaction with re\-concat\-star\-swap and re\-concat\-star\-repeat are untested\.

**RARE syntax:** passed at [40a4bb7e43adf97534c29a52ed079c4efd687644](https://github.com/cvc5/cvc5/commit/40a4bb7e43adf97534c29a52ed079c4efd687644).

**Solver check:** recorded; [evidence](../../../tools/metagraphe/docs/ledger/2026-09-20-string-benchmark-comparison.md).

**Performance check:** recorded; [evidence](../../../tools/metagraphe/docs/ledger/2026-09-20-string-benchmark-comparison.md).

**Cautions:**

- cvc5 eliminates re\.\+ before this could match, so only the first schema is the rule that has to fire; the two surface identities describe the same equality before that elimination\.
- The \(r\+\)\+ case is not closed by this rule alone: it leaves \(re\.\+\+ r \(re\.\* r\) \(re\.\* r\)\) and depends on the existing re\-concat\-star\-repeat rule\.
- Checked for ten concrete r only; the general identity rests on the written language argument, because cvc5 rejects RegLan variables\.
- Nested star and plus are a fuzzer\-generated shape here; occurrence outside 20230327\-stringfuzz\-lu was not established\.

**Next step:** Implement \(re\.\* \(re\.\+\+ r \(re\.\* r\)\)\) \-&gt; \(re\.\* r\) in rewriteStarRegExp, check that it does not re\-enter the concat\-star normalisation loop with re\-concat\-star\-swap and re\-concat\-star\-repeat, and measure it on the 20230327\-stringfuzz\-lu inputs that carry the pattern\.

### Evidence and follow-up

No source issue: this candidate comes from a benchmark comparison over SMT\-LIB 2026 non\-incremental QF\_SLIA \(84,411 inputs, 14 families\); 200\-input stratified sample, seed metagraphe\-2026\-09\-20.

Observed: 2026-09-20 at cvc5 source [40a4bb7e43adf97534c29a52ed079c4efd687644](https://github.com/cvc5/cvc5/commit/40a4bb7e43adf97534c29a52ed079c4efd687644).

Koine ingestion: first 2026-09-20; last 2026-09-20.

Corpus: SMT\-LIB 2026 non\-incremental QF\_SLIA \(84,411 inputs, 14 families\); 200\-input stratified sample, seed metagraphe\-2026\-09\-20; [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-20-string-benchmark-comparison.md).

**Source references:**

- [https://github\.com/cvc5/cvc5/blob/40a4bb7e43adf97534c29a52ed079c4efd687644/src/theory/strings/sequences\_rewriter\.cpp](https://github.com/cvc5/cvc5/blob/40a4bb7e43adf97534c29a52ed079c4efd687644/src/theory/strings/sequences_rewriter.cpp)
- [https://github\.com/cvc5/cvc5/blob/40a4bb7e43adf97534c29a52ed079c4efd687644/src/theory/strings/rewrites](https://github.com/cvc5/cvc5/blob/40a4bb7e43adf97534c29a52ed079c4efd687644/src/theory/strings/rewrites)

No delivery recorded.

[Back to overview](#overview)
