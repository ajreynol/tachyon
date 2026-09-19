# Metagraphe rewrites

Generated from [rewrites.json](rewrites.json). **Do not edit this view by hand.**
See the [database guide](README.md) for filing and the
[reporting policy](reporting-policy.md) for reassessment and closure.

Regenerate from tachyon's root with `python3 tools/metagraphe/scripts/render_rewrite_db.py`; add `--check` to check freshness.

**20 records:** 16 candidates, 2 existing-coverage controls, 2 exclusions.
**0 explicit closure verdicts; 0 fixes awaiting landing.**

A record is a candidate family, not a count of new rules or solved issues.
`argued` denotes a written validity argument, not a checked proof. RARE parser
acceptance does not establish correctness or solver performance. Classifications
and priorities are metagraphe's assessments; closure requires a separate verdict.
Issue states below are snapshots at review, not live GitHub status.

## Overview

| Record | Priority | Classification | Validity | RARE drafts | Closure | Issues |
| --- | --- | --- | --- | --- | --- | --- |
| [M-1: Singleton replacement](#m-1) | 1 | candidate | argued | 2 | no closure recorded | [\#12936](https://github.com/cvc5/cvc5/issues/12936), [\#9875](https://github.com/cvc5/cvc5/issues/9875) |
| [M-2: Prefix before first match](#m-2) | 1 | candidate | argued | 1 | no closure recorded | [\#11362](https://github.com/cvc5/cvc5/issues/11362) |
| [M-3: Lexicographic prefix cancellation](#m-3) | 1 | candidate | argued | 2 | no closure recorded | [\#11151](https://github.com/cvc5/cvc5/issues/11151), [\#9875](https://github.com/cvc5/cvc5/issues/9875) |
| [M-4: Signed comparison disjunction](#m-4) | 1 | candidate | argued | 1 | no closure recorded | [\#11357](https://github.com/cvc5/cvc5/issues/11357) |
| [M-5: Complement of a character](#m-5) | 2 | candidate | argued | 1 | no closure recorded | [\#12815](https://github.com/cvc5/cvc5/issues/12815) |
| [M-6: Guarded zero division](#m-6) | 2 | candidate | argued | 1 | no closure recorded | [\#11201](https://github.com/cvc5/cvc5/issues/11201) |
| [M-7: Modular arithmetic](#m-7) | 2 | candidate | argued | 2 | no closure recorded | [\#11535](https://github.com/cvc5/cvc5/issues/11535), [\#11872](https://github.com/cvc5/cvc5/issues/11872) |
| [M-8: Learned lengths and encoded reversal](#m-8) | 3 | candidate | argued | 0 | no closure recorded | [\#10522](https://github.com/cvc5/cvc5/issues/10522), [\#11010](https://github.com/cvc5/cvc5/issues/11010) |
| [M-9: String order totality](#m-9) | 3 | candidate | argued | 0 | no closure recorded | [\#12042](https://github.com/cvc5/cvc5/issues/12042) |
| [M-10: Character\-language intersections](#m-10) | 3 | candidate | argued | 0 | no closure recorded | [\#11206](https://github.com/cvc5/cvc5/issues/11206) |
| [M-11: BV remainder comparison already represented](#m-11) | — | existing\-coverage | argued | 0 | no closure recorded | [\#10520](https://github.com/cvc5/cvc5/issues/10520) |
| [M-12: Modulus sign has conditional support](#m-12) | — | existing\-coverage | argued | 0 | no closure recorded | [\#9420](https://github.com/cvc5/cvc5/issues/9420) |
| [M-13: Nested replacement emptiness](#m-13) | 3 | candidate | argued | 0 | no closure recorded | [\#10508](https://github.com/cvc5/cvc5/issues/10508) |
| [M-14: Sequence prefix forces index zero](#m-14) | 3 | candidate | argued | 0 | no closure recorded | [\#11156](https://github.com/cvc5/cvc5/issues/11156) |
| [M-15: Absence propagates to an included slice](#m-15) | 3 | candidate | unchecked | 0 | no closure recorded | [\#11460](https://github.com/cvc5/cvc5/issues/11460) |
| [M-16: Inverse case conversion](#m-16) | 3 | candidate | unchecked | 0 | no closure recorded | [\#11970](https://github.com/cvc5/cvc5/issues/11970) |
| [M-17: Nested ITE and extract synthesis](#m-17) | 3 | candidate | unchecked | 0 | no closure recorded | [\#10850](https://github.com/cvc5/cvc5/issues/10850) |
| [M-18: BV quotient with no\-overflow conditions](#m-18) | 3 | candidate | argued | 0 | no closure recorded | [\#9417](https://github.com/cvc5/cvc5/issues/9417) |
| [M-19: RARE name in Alethe is a consistency issue](#m-19) | — | excluded | not\-applicable | 0 | no closure recorded | [\#12801](https://github.com/cvc5/cvc5/issues/12801) |
| [M-20: Boolean operand order is a search\-order lead](#m-20) | — | excluded | not\-applicable | 0 | no closure recorded | [\#12353](https://github.com/cvc5/cvc5/issues/12353) |

## M-1

**Singleton replacement**

Classification: candidate. Priority: 1. Theories: sequences, strings.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: s: String or Seq\(T\); u: same sort as s; r: same sort as s.

```text
(str.contains (str.replace_all s u r) u)
  ->
(and (str.contains s u) (str.contains r u))

when: (= (str.len u) 1)
```

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

Issues: [\#12936](https://github.com/cvc5/cvc5/issues/12936) (open at review), [\#9875](https://github.com/cvc5/cvc5/issues/9875) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#m-1-singleton-replacement) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

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

Classification: candidate. Priority: 1. Theories: strings, sequences.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: s: String or Seq\(T\); t: same sort as s.

```text
(str.contains (str.substr s 0 (str.indexof s t 0)) t)
  ->
(= (str.len t) 0)

when: true
```

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

Issues: [\#11362](https://github.com/cvc5/cvc5/issues/11362) (open at review).

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

Classification: candidate. Priority: 1. Theories: strings.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: s: String; t: String.

```text
(str.< (str.++ s t) s)
  ->
false

when: true
```

### Rewrite 2

Notation: SMT\-LIB term schema.

Variables: s: String; t: String.

```text
(str.<= (str.++ s t) s)
  ->
(= t "")

when: true
```

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

Issues: [\#11151](https://github.com/cvc5/cvc5/issues/11151) (open at review), [\#9875](https://github.com/cvc5/cvc5/issues/9875) (open at review).

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

Classification: candidate. Priority: 1. Theories: bit\-vectors, booleans.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: x: BitVec\(w\); y: BitVec\(w\).

```text
(or (= x y) (bvslt x y))
  ->
(bvsle x y)

when: w is a positive integer
```

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

Issues: [\#11357](https://github.com/cvc5/cvc5/issues/11357) (open at review).

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

Classification: candidate. Priority: 2. Theories: strings, regular\-expressions.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: none.

```text
(re.inter re.allchar (re.comp (str.to_re "/")))
  ->
(re.union (re.range "\u{0}" ".") (re.range "0" "\u{2ffff}"))

when: SMT-LIB Unicode Strings alphabet: code points 0 through 0x2ffff
```

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

Issues: [\#12815](https://github.com/cvc5/cvc5/issues/12815) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#m-5-complement-of-a-character) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

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

Classification: candidate. Priority: 2. Theories: integers, strings.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: v: Int.

```text
(ite (= v 0) 0 (div 0 v))
  ->
0

when: true
```

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

Issues: [\#11201](https://github.com/cvc5/cvc5/issues/11201) (open at review).

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

Classification: candidate. Priority: 2. Theories: integers.

**Closure:** no closure recorded.

**Application context:** Internal totalized arithmetic; surface\-to\-internal conversion may require contextual nonzero facts\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: a: Int; b: Int; c: Int.

```text
(mod_total (* a c b) c)
  ->
0

when: true
```

### Rewrite 2

Notation: SMT\-LIB term schema.

Variables: n: Int.

```text
(mod_total (* n (+ n 1)) 2)
  ->
0

when: true
```

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

Issues: [\#11535](https://github.com/cvc5/cvc5/issues/11535) (open at review), [\#11872](https://github.com/cvc5/cvc5/issues/11872) (open at review).

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

## M-8

**Learned lengths and encoded reversal**

Classification: candidate. Priority: 3. Theories: strings, bit\-vector\-conversions.

**Closure:** no closure recorded.

**Application context:** Requires learned length bounds and composition of existing substring rules\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: s: String; i: Int; n: Int.

```text
(str.len (str.substr s i n))
  ->
n

when: (and (<= 0 i) (<= 0 n) (<= (+ i n) (str.len s)))
```

No RARE draft is filed.

### Assessment and next step

- **Validity: argued.** An in\-range substring of requested nonnegative length has that length\. This local rule already exists; encoded reversal needs composition with length reasoning\.
- **Availability: existing\-rule\-needs\-context.** str\-len\-substr\-in\-range and native seq\-rev\-rev already exist\. The issue uses substring\-encoded reversal and globally learned length facts\.
- **Value: unmeasured.** Could expose simplification of encoded reversals; no new native double\-reversal rule is needed\.

**RARE syntax:** not\-run.

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- \#10522 constrains length modulo 2^64 to four, not exactly four; nonnegativity implies only the needed lower bound\.
- \#11010 does assert exact length four, but uses concatenated substrings rather than str\.rev\.
- int2bv\(8,str\.to\_code\(\.\.\.\)\) is modulo 256 and does not preserve arbitrary Unicode codes\.
- PR \#10717 is prior relevant work, not evidence the issue is resolved\.

**Next step:** Compare native reversal and the encoded form, with exact and modular length constraints separately\.

### Evidence and follow-up

Issues: [\#10522](https://github.com/cvc5/cvc5/issues/10522) (open at review), [\#11010](https://github.com/cvc5/cvc5/issues/11010) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#m-8-learned-lengths-and-encoded-reversal) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/10522](https://github.com/cvc5/cvc5/issues/10522)
- [https://github\.com/cvc5/cvc5/files/14657704/str20\.smt2\.txt](https://github.com/cvc5/cvc5/files/14657704/str20.smt2.txt)
- [https://github\.com/cvc5/cvc5/issues/10522\#issuecomment\-2090831450](https://github.com/cvc5/cvc5/issues/10522#issuecomment-2090831450)
- [https://github\.com/cvc5/cvc5/issues/10522\#issuecomment\-2015208979](https://github.com/cvc5/cvc5/issues/10522#issuecomment-2015208979)
- [https://github\.com/cvc5/cvc5/pull/10717](https://github.com/cvc5/cvc5/pull/10717)
- [https://github\.com/cvc5/cvc5/issues/11010](https://github.com/cvc5/cvc5/issues/11010)
- [https://github\.com/user\-attachments/files/16110870/symcc\-structs\-assertions\-modified\.smt2\.txt](https://github.com/user-attachments/files/16110870/symcc-structs-assertions-modified.smt2.txt)

**Source references:**

- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/rewrites](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/rewrites)

No delivery recorded.

[Back to overview](#overview)

## M-9

**String order totality**

Classification: candidate. Priority: 3. Theories: strings, booleans.

**Closure:** no closure recorded.

**Application context:** May require preprocessing across assertions or a theory lemma\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: x: String; y: String.

```text
(and (not (str.< x y)) (not (str.< y x)))
  ->
(= x y)

when: true
```

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

Issues: [\#12042](https://github.com/cvc5/cvc5/issues/12042) (open at review).

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

Classification: candidate. Priority: 3. Theories: strings, regular\-expressions.

**Closure:** no closure recorded.

**Application context:** Requires a character\-language entailment check before applying the schema\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: A: RegLan; B: RegLan.

```text
(re.inter (re.* A) (re.* B))
  ->
(re.* (re.inter A B))

when: A and B accept only strings of length one
```

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

Issues: [\#11206](https://github.com/cvc5/cvc5/issues/11206) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#m-10-character-language-intersections) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/11206](https://github.com/cvc5/cvc5/issues/11206)

**Source references:**

- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/sequences\_rewriter\.cpp](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/sequences_rewriter.cpp)

No delivery recorded.

[Back to overview](#overview)

## M-11

**BV remainder comparison already represented**

Classification: existing\-coverage. Priority: not ranked. Theories: bit\-vectors.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: x: BitVec\(w\); C: BitVec\(w\).

```text
(bvult x (bvurem C x))
  ->
(and (= x zero(w)) (not (= C zero(w))))

when: w is positive; zero(w) is the width-w zero
```

No RARE draft is filed.

### Assessment and next step

- **Validity: argued.** For nonzero x unsigned remainder is less than x; for zero x it equals C\.
- **Availability: existing\-rule\-reachability\-unchecked.** bv\-ugt\-urem and UgtUrem already express the symmetric greater\-than form\.
- **Value: unmeasured.** Use as an existing\-rule control; the nonzero constant in the issue leaves x=0\.

**RARE syntax:** not\-run.

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- Source presence does not show the original less\-than orientation reaches the rule\.

**Next step:** Probe the original orientation and its symmetric form before claiming either a new rule or an issue resolution\.

### Evidence and follow-up

Issues: [\#10520](https://github.com/cvc5/cvc5/issues/10520) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/10520](https://github.com/cvc5/cvc5/issues/10520)

**Source references:**

- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/bv/rewrites\-simplification](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/bv/rewrites-simplification)
- [https://github\.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/bv/theory\_bv\_rewrite\_rules\_simplification\.h](https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/bv/theory_bv_rewrite_rules_simplification.h)

No delivery recorded.

[Back to overview](#overview)

## M-12

**Modulus sign has conditional support**

Classification: existing\-coverage. Priority: not ranked. Theories: integers.

**Closure:** no closure recorded.

**Application context:** Conditional reasoning with a known nonzero divisor\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: x: Int; y: Int.

```text
(mod x y)
  ->
(mod x (abs y))

when: (not (= y 0))
```

No RARE draft is filed.

### Assessment and next step

- **Validity: argued.** Euclidean remainder depends on the absolute magnitude of a nonzero divisor\.
- **Availability: existing\-conditional\-support.** The issue discussion already points to \-\-learned\-rewrite and records mixed suite results\.
- **Value: unmeasured.** An option/context investigation rather than an established missing identity\.

**RARE syntax:** not\-run.

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- The nonzero condition is required for surface mod\.
- Historical option support does not establish the behavior of the pinned default solver\.

**Next step:** Compare current default and learned\-rewrite behavior and trace availability of the nonzero condition\.

### Evidence and follow-up

Issues: [\#9420](https://github.com/cvc5/cvc5/issues/9420) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/9420](https://github.com/cvc5/cvc5/issues/9420)
- [https://github\.com/cvc5/cvc5/issues/9420\#issuecomment\-1404268724](https://github.com/cvc5/cvc5/issues/9420#issuecomment-1404268724)

No delivery recorded.

[Back to overview](#overview)

## M-13

**Nested replacement emptiness**

Classification: candidate. Priority: 3. Theories: strings.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: a: String; b: String; c: String.

```text
(= (str.replace_all (str.replace_all a b a) c a) "")
  ->
(= a "")

when: true
```

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

Issues: [\#10508](https://github.com/cvc5/cvc5/issues/10508) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/10508](https://github.com/cvc5/cvc5/issues/10508)

No delivery recorded.

[Back to overview](#overview)

## M-14

**Sequence prefix forces index zero**

Classification: candidate. Priority: 3. Theories: sequences.

**Closure:** no closure recorded.

**Application context:** Requires the prefix fact as a premise or in a combined Boolean term\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: s: Seq\(T\); t: Seq\(T\).

```text
(seq.indexof s t 0)
  ->
0

when: (seq.prefixof t s)
```

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

Issues: [\#11156](https://github.com/cvc5/cvc5/issues/11156) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/11156](https://github.com/cvc5/cvc5/issues/11156)

No delivery recorded.

[Back to overview](#overview)

## M-15

**Absence propagates to an included slice**

Classification: candidate. Priority: 3. Theories: strings, integers.

**Closure:** no closure recorded.

**Application context:** Arithmetic context must establish that the one\-character slice is inside the larger substring\.

No exact rewrite is filed.

No RARE draft is filed.

### Assessment and next step

- **Validity: unchecked.** The proposed direction needs exact substring inclusion, nonempty character and in\-range index conditions from the unreduced attachment\.
- **Availability: unchecked.** The attachment was not reduced and no concrete rule has been audited\.
- **Value: unmeasured.** May expose the contradiction caused by the final character constraint\.

**RARE syntax:** not\-run.

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- No exact rewrite is filed until slice inclusion and bounds are stated\.

**Next step:** Reduce the attachment and state the exact indices and side conditions before proposing a rule\.

### Evidence and follow-up

Issues: [\#11460](https://github.com/cvc5/cvc5/issues/11460) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/11460](https://github.com/cvc5/cvc5/issues/11460)

No delivery recorded.

[Back to overview](#overview)

## M-16

**Inverse case conversion**

Classification: candidate. Priority: 3. Theories: strings, regular\-expressions.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: s: String.

```text
(= (str.to_lower s) "a")
  ->
(or (= s "a") (= s "A"))

when: Subject to verification against cvc5 case-conversion semantics
```

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

Issues: [\#11970](https://github.com/cvc5/cvc5/issues/11970) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/11970](https://github.com/cvc5/cvc5/issues/11970)
- [https://github\.com/cvc5/cvc5/issues/11970\#issuecomment\-2956111004](https://github.com/cvc5/cvc5/issues/11970#issuecomment-2956111004)

No delivery recorded.

[Back to overview](#overview)

## M-17

**Nested ITE and extract synthesis**

Classification: candidate. Priority: 3. Theories: bit\-vectors, synthesis.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

No exact rewrite is filed.

No RARE draft is filed.

### Assessment and next step

- **Validity: unchecked.** No exact identity has been extracted from the attachment\.
- **Availability: unchecked.** Grammar feasibility, quantifiers and signedness need attachment\-level analysis\.
- **Value: unmeasured.** Comparison decomposition is an investigation lead, not an established rewrite\.

**RARE syntax:** not\-run.

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- A synthesis grammar restriction is not evidence of a missing solver rewrite\.

**Next step:** Inspect and reduce the attachment, distinguishing synthesis feasibility from SMT equivalence\.

### Evidence and follow-up

Issues: [\#10850](https://github.com/cvc5/cvc5/issues/10850) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/10850](https://github.com/cvc5/cvc5/issues/10850)

No delivery recorded.

[Back to overview](#overview)

## M-18

**BV quotient with no\-overflow conditions**

Classification: candidate. Priority: 3. Theories: bit\-vectors.

**Closure:** no closure recorded.

**Application context:** Requires divisor, remainder and no\-overflow facts from the assertion context\.

### Rewrite 1

Notation: SMT\-LIB term schema.

Variables: q: BitVec\(w\); y: BitVec\(w\); r: BitVec\(w\).

```text
(bvudiv (bvadd (bvmul q y) r) y)
  ->
q

when: w>0; y!=0; unsigned r<y; unsigned q*y and q*y+r do not overflow
```

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

Issues: [\#9417](https://github.com/cvc5/cvc5/issues/9417) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/9417](https://github.com/cvc5/cvc5/issues/9417)

No delivery recorded.

[Back to overview](#overview)

## M-19

**RARE name in Alethe is a consistency issue**

Classification: excluded. Priority: not ranked. Theories: proof\-export.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

No exact rewrite is filed.

No RARE draft is filed.

### Assessment and next step

- **Validity: not\-applicable.** No simplifying identity is proposed\.
- **Availability: not\-applicable.** The issue concerns proof export/database naming consistency\.
- **Value: not\-applicable.** Retain as an exclusion so a future survey does not misclassify it as a missing rewrite\.

**RARE syntax:** not\-run.

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- An occurrence of RARE in an issue title is not evidence of a missing simplification\.

**Next step:** Track through proof\-export consistency work if separately authorized\.

### Evidence and follow-up

Issues: [\#12801](https://github.com/cvc5/cvc5/issues/12801) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/12801](https://github.com/cvc5/cvc5/issues/12801)

No delivery recorded.

[Back to overview](#overview)

## M-20

**Boolean operand order is a search\-order lead**

Classification: excluded. Priority: not ranked. Theories: booleans.

**Closure:** no closure recorded.

**Application context:** Local term rewriting; normalized matching remains to be tested\.

No exact rewrite is filed.

No RARE draft is filed.

### Assessment and next step

- **Validity: not\-applicable.** Commutativity by itself does not identify a beneficial missing rewrite\.
- **Availability: not\-applicable.** The report is about search\-order performance\.
- **Value: not\-applicable.** Retain the exclusion from the rewrite queue\.

**RARE syntax:** not\-run.

**Solver check:** not\-run.

**Performance check:** not\-run.

**Cautions:**

- Do not file Boolean commutativity as a new performance rewrite without a concrete mechanism\.

**Next step:** Reconsider only if reduction identifies a specific missing transformation\.

### Evidence and follow-up

Issues: [\#12353](https://github.com/cvc5/cvc5/issues/12353) (open at review).

Observed: 2026-09-19 at cvc5 source [dbf176dfb71b272ffbfdee06888dace73fee5aa8](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).

Koine ingestion: first 2026-09-19; last 2026-09-19.

[Survey](../../../docs/github-issues-rewrites.md#existing-coverage-and-leads-needing-more-work) (tachyon revision `d2ef784441e59059e44d23c6a594d216a2eb75ad`); [investigation ledger](../../../tools/metagraphe/docs/ledger/2026-09-19-github-issues.md).

**Supporting references:**

- [https://github\.com/cvc5/cvc5/issues/12353](https://github.com/cvc5/cvc5/issues/12353)

No delivery recorded.

[Back to overview](#overview)
