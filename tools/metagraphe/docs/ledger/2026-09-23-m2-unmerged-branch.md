# M-2 on an unmerged cvc5 branch

**2026-09-23: source audit of an unmerged branch; no build, no solver run.**
The human pointed at `strContainsBeforeIdof` and asked that its rewrite be
recorded in metagraphe, without tracking the branch as a delivery. This entry
does that. It adds no `carried`, `awaiting_landing` or closure metadata to M-2,
and it does not change M-2's filed claim or assessment.

## Question and scope

Candidate [M-2](../../rewrite_db/rewrites.md#m-2), prefix before first match,
from [#11362](https://github.com/cvc5/cvc5/issues/11362). Does the branch
implement M-2, and does its form differ from the filed record?

## Provenance

- Branch `strContainsBeforeIdof` on `ajreynol/cvc5`, tip
  [`8be0ced6f49dfe8a06da66bd8e2bf3a1ed22aa7a`](https://github.com/ajreynol/cvc5/commit/8be0ced6f49dfe8a06da66bd8e2bf3a1ed22aa7a)
  (2024-11-14). It has six commits over merge base
  [`e81f508eae373d87bfa659be15b4c077b060e320`](https://github.com/cvc5/cvc5/commit/e81f508eae373d87bfa659be15b4c077b060e320)
  (2024-11-11, #11340) and is 1238 commits behind cvc5 `main`. Elaphros's
  [branch-tip inventory](../../../elaphros/reports/data/2026-09-18-branch-tips.tsv)
  already lists the same tip.
- cvc5 `main` was checked at
  [`d7d5b948c11d2d83be0212d4a954ef49740ecdab`](https://github.com/cvc5/cvc5/commit/d7d5b948c11d2d83be0212d4a954ef49740ecdab)
  (2026-09-23). #11362 was still open.

## Reproduction

```bash
curl -s https://api.github.com/repos/cvc5/cvc5/compare/main...ajreynol:cvc5:strContainsBeforeIdof
curl -s https://raw.githubusercontent.com/cvc5/cvc5/main/src/theory/strings/rewrites \
  | grep -n 'before-indexof'
curl -s https://raw.githubusercontent.com/cvc5/cvc5/main/src/theory/strings/sequences_rewriter.cpp \
  | grep -n 'SUBSTR_INDEXOF\|checkIsPrefix'
```

I only read the branch. Nothing was fetched into a local checkout, built or run.

## What the branch contains

**RARE rule** in `src/theory/strings/rewrites`, and a matching
`ProofRewriteRule::STR_CONTAINS_SUBSTR_BEFORE_INDEXOF`:

```text
(define-cond-rule str-contains-substr-before-indexof ((x ?Seq) (y ?Seq))
  (> (str.len y) 0)
  (str.contains (str.substr x 0 (str.indexof x y 0)) y)
  false)
```

This is M-2 restricted to a nonempty needle. It agrees with M-2's caution that
an unconditional `false` is invalid. M-2 files the unconditional equality with
right-hand side `(= (str.len t) 0)`. That equality implies the branch's rule.

**C++ rewrite** `Rewrite::CTN_SUBSTR_INDEXOF` in
`SequencesRewriter::rewriteContains`. It generalizes the rule: the string that
`indexof` searches may be any `x'` that `StringsEntail::checkIsPrefix(x', x)`
shows is a prefix of `x`.

```text
(str.contains (str.substr x 0 (str.indexof x' y 0)) y) -> false
    if checkIsPrefix(x', x) and checkNonEmpty(y)
```

The generalization is valid by M-2's argument. If `y` is absent from `x'`, the
index is -1 and the substring is empty. Otherwise `x` and `x'` agree before the
first occurrence. The new `checkIsPrefix` recognizes syntactic equality,
`(str.substr t 0 n)`, two substrings of the same base with the same start whose
lengths are ordered by arithmetic entailment, and a concatenation whose first
component is `s`. A constant-prefix case is left as `TODO`. The existing
`CTN_SUBSTR` becomes `CTN_SUBSTR_EQ_LEN`, and a zero constant is hoisted into
`d_zero`.

**Test.** The regression `regress0/strings/str-rewrite-issue11362.smt2`
expects `unsat` for the issue's tautology with the needle `"y"`.

**Unrelated to the rewrite.** In `TermRegistry::eagerReduce`, the branch adds a
length lemma for `str.substr`. A second copy, which would register that lemma,
is commented out. This bears on M-2's note that the original query may need a
lemma, but this audit does not assess it.

## Conclusion and limits

- M-2 is the record for this rewrite. The branch adds no new identity, so there
  is no new ID.
- The branch's rule is the nonempty-needle instance of M-2, and its C++ form
  generalizes the indexed string to a provable prefix. Filing that
  generalization as a separate schema would need its own record and review.
- M-2's availability, `source-gap-candidate`, still holds for cvc5 `main` at
  the commit above: neither the rule name nor the rewrite enum appears there. A
  prototype does exist off the default branch. A later assessment of M-2's
  availability should cite this entry.
- Nothing here establishes that the branch builds, that the rewrite fires on
  the issue's input, or any performance effect. M-2's `solver` and
  `performance` checks stay `not-run`.
