# cvc5 GitHub issues that suggest rewrites

**Metagraphe issue survey, 2026-09-19.** The best first implementation targets
are M-1 through M-4: singleton replacement, the prefix before an `indexof`
match, lexicographic prefix cancellation, and signed bit-vector comparison.
They have small identities and direct issue motivation. This ranking is the
agent's assessment, not a maintainer commitment.

These are **candidates, not verified fixes**. The review checked issue bodies,
selected comments and attachments, and pinned upstream source. It did not
build that revision, reproduce the reported runtimes, or establish that a new
rule reaches the relevant term during solving. The RARE drafts below have
semantic arguments; the validation section records the separate syntax check.

**Filed on 2026-09-19.** The [rewrite database](../tools/metagraphe/rewrite_db/README.md)
now holds the structured claims and owns subsequent assessments and verdicts.
M-1 through M-10 retain their identities; the additional triage rows were
filed as M-11 through M-20 in their table order. This document remains the
dated source narrative, not a parallel current-status database. See the
[filing ledger](../tools/metagraphe/docs/ledger/2026-09-19-rewrite-db.md) and
[experience log](../tools/metagraphe/docs/experience.md).

## Coverage and how to repeat the survey

The [open issue list](https://github.com/cvc5/cvc5/issues) was retrieved through
the public GitHub REST API on 2026-09-19. Three pages of
`repos/cvc5/cvc5/issues?state=open&per_page=100&page=N` contained **144 issues**
after excluding pull requests. Every issue title was screened; the concrete
string, sequence, bit-vector, and arithmetic reports cited below received
closer reading. This is not a claim that every attachment or crash trace was
audited. In particular, the large inputs in #11460 and #10850 were not reduced.

Additional searches were `repo:cvc5/cvc5 is:issue rewrite` (274 results; only
the first 100 screened) and `repo:cvc5/cvc5 is:issue rewrite in:title` (all 61
results screened). These include closed history but do not constitute an
exhaustive survey of closed issues. All issue numbers in the candidate and
triage tables below were **open** at the review date. Open status alone does
not establish that a problem persists.

Source references are pinned to upstream main at
[`dbf176dfb71b272ffbfdee06888dace73fee5aa8`](https://github.com/cvc5/cvc5/commit/dbf176dfb71b272ffbfdee06888dace73fee5aa8).
The principal files inspected were [string/sequence RARE rules][str-rules],
[sequence rewriting][seq-cpp], [string ordering][str-cpp],
[bit-vector RARE rules][bv-rules], and [arithmetic RARE rules][arith-rules].
This is a source baseline; a matching executable baseline remains to be built.

Run the reusable workflow from any working directory:

```bash
/path/to/tachyon/prompts/metagraphe_read_github --show-prompt
/path/to/tachyon/prompts/metagraphe_read_github --codex
# Omit --codex to use the default agent; --print runs non-interactively.
```

The [prompt script](../prompts/metagraphe_read_github) launches the survey in
tachyon and asks the agent to record dated survey updates and file new JSON
records through the database workflow. It preserves
the distinction between a source audit, a solver observation, and a proposed
rule. It does not itself fetch GitHub data. To repeat the retrieval manually:

```bash
mkdir -p scratch/metagraphe-github
curl -L --fail --get https://api.github.com/repos/cvc5/cvc5/issues \
  --data-urlencode state=open --data-urlencode per_page=100 \
  --data-urlencode page=1 --dump-header scratch/metagraphe-github/open-1.headers \
  -o scratch/metagraphe-github/open-1.json
# Follow the response Link header through every page; remove entries with
# a pull_request field. Read /issues/NUMBER/comments for shortlisted issues.
```

Keep fetched JSON, attachments, and solver transcripts in ignored scratch
space. The durable evidence here is the linked source, exact identities,
counterexamples, and commands, rather than a copy of mutable GitHub output.

## Ranked candidates

| priority | candidate | issues | assessment |
| --- | --- | --- | --- |
| 1 | [M-1: singleton replacement](#m-1-singleton-replacement) | [#12936](https://github.com/cvc5/cvc5/issues/12936), [#9875](https://github.com/cvc5/cvc5/issues/9875) | Direct rewrite request; correct the proposed identity before implementation. |
| 1 | [M-2: prefix before first match](#m-2-prefix-before-first-match) | [#11362](https://github.com/cvc5/cvc5/issues/11362) | Maintainer explicitly identifies a rewrite opportunity; handle the empty needle. |
| 1 | [M-3: lexicographic prefix cancellation](#m-3-lexicographic-prefix-cancellation) | [#11151](https://github.com/cvc5/cvc5/issues/11151), [#9875](https://github.com/cvc5/cvc5/issues/9875) | Small, unconditional rules directly refute the examples. |
| 1 | [M-4: signed comparison disjunction](#m-4-signed-comparison-disjunction) | [#11357](https://github.com/cvc5/cvc5/issues/11357) | Reporter supplies the successful equivalent form; also a quantifier configuration issue. |
| 2 | [M-5: complement of a character](#m-5-complement-of-a-character) | [#12815](https://github.com/cvc5/cvc5/issues/12815) | Exact regex normalization; benchmark impact still uncertain. |
| 2 | [M-6: guarded zero division](#m-6-guarded-zero-division) | [#11201](https://github.com/cvc5/cvc5/issues/11201) | Explicit small simplification; preserve division-by-zero semantics. |
| 2 | [M-7: modular arithmetic](#m-7-modular-arithmetic) | [#11535](https://github.com/cvc5/cvc5/issues/11535), [#11872](https://github.com/cvc5/cvc5/issues/11872) | Secondary theory; short algebraic rules, with normalization and context work. |
| 3 | [M-8: learned lengths and encoded reversal](#m-8-learned-lengths-and-encoded-reversal) | [#10522](https://github.com/cvc5/cvc5/issues/10522), [#11010](https://github.com/cvc5/cvc5/issues/11010) | Existing local identities; the main gap is exposing or transporting conditions. |
| 3 | [M-9: string order totality](#m-9-string-order-totality) | [#12042](https://github.com/cvc5/cvc5/issues/12042) | Valid Boolean identity, but three assertions must meet at the right stage. |
| 3 | [M-10: character-language intersections](#m-10-character-language-intersections) | [#11206](https://github.com/cvc5/cvc5/issues/11206) | Useful normalization, insufficient on its own to solve the full report. |

### Reading the RARE drafts

The [pinned RARE grammar][rare-grammar] uses `define-rule` and
`define-cond-rule`. The existing string file uses `?Seq` and `str.*` operators
for both strings and sequences; this is why the sequence draft below is not
written with SMT-LIB's surface `seq.contains` spelling. A conditional rule's
condition must be dischargeable at the point of application. An asserted
arithmetic fact is not automatically available to a context-free rewriter.

RARE describes proof reconstruction rules. Adding a declaration alone does
not demonstrate a new default simplification: the implementation must perform
the transformation at an appropriate stage and reconstruct its proof. Check
both the theory rewriter and the RARE database; the maintainer makes the same
distinction in [#11535's discussion](https://github.com/cvc5/cvc5/issues/11535#issuecomment-2629040753).

### M-1: singleton replacement

**Origin.** [#12936](https://github.com/cvc5/cvc5/issues/12936) asks for a rewrite
of containment after replacing every occurrence of a singleton sequence.
The deletion case also appears for strings in
[#9875's fourth example](https://github.com/cvc5/cvc5/issues/9875#issuecomment-1625411673).

**Correction.** For a singleton `u`, the correct identity is

```text
contains(replace_all(s, u, r), u)
  -> contains(s, u) AND contains(r, u)
```

The issue's proposed RHS omits `contains(s,u)`. Counterexample: `s = []`,
`u = [0]`, `r = [0]`. No replacement happens; the LHS is false while the
proposed RHS is true. The corrected rule follows because every original
occurrence of the element is replaced, and an occurrence in the result can
only come from an inserted replacement. This argument works for arbitrary
sequence element sorts and for one-character strings.

```lisp
(define-rule metagraphe-contains-replace-all-unit
  ((s ?Seq) (r ?Seq) (x ?))
  (str.contains (str.replace_all s (seq.unit x) r) (seq.unit x))
  (and (str.contains s (seq.unit x))
       (str.contains r (seq.unit x))))

(define-cond-rule metagraphe-contains-replace-all-char
  ((s ?Seq) (u ?Seq) (r ?Seq))
  (= (str.len u) 1)
  (str.contains (str.replace_all s u r) u)
  (and (str.contains s u) (str.contains r u)))
```

For empty `r`, the result is immediately false, resolving the core assertions
in both cited deletion examples. The prefix assertions in #9875 additionally
need prefix/containment reasoning. Do not generalize to longer needles:
deleting `"ab"` from `"aabb"` produces `"ab"`, creating a new match across the
deletion boundary. Empty needles have different replacement semantics too.

**Availability and next check.** The pinned [replacement RARE rules][str-rules]
and `SequencesRewriter::rewriteContains` / `rewriteReplaceAll` in
[sequences_rewriter.cpp][seq-cpp] do not contain this `contains`/`replace_all`
pattern. They do contain related rules for single replacement. Check the
singleton sequence and string forms through simplification and solving,
including proofs and the no-match counterexample. The RHS can duplicate
containment work for nonempty replacements; measure that cost separately.

### M-2: prefix before first match

**Origin.** [#11362](https://github.com/cvc5/cvc5/issues/11362) adds a fact saying
that the prefix before the first `"x"` contains no `"x"`. A
[maintainer comment](https://github.com/cvc5/cvc5/issues/11362#issuecomment-2474655250)
explicitly supports adding a rewrite. The reported runtime difference is
historical evidence, not a measurement repeated here.

The following stronger identity also handles an empty needle:

```lisp
(define-rule metagraphe-contains-before-indexof
  ((s ?Seq) (t ?Seq))
  (str.contains (str.substr s 0 (str.indexof s t 0)) t)
  (= (str.len t) 0))
```

For a nonempty `t`, a found occurrence cannot start earlier than the first
match. If no occurrence exists, `indexof` is `-1` and the substring is empty.
For empty `t`, the index is zero and the empty substring contains `t`, so the
answer is true. Consequently, rewriting unconditionally to false would be
wrong. These cases follow the [SMT-LIB string definitions][string-semantics].

**Availability and next check.** No corresponding pattern was found in the
pinned [RARE rules][str-rules] or `rewriteContains` / `rewriteIndexof` in
[sequence rewriting][seq-cpp]. Test empty, absent, overlapping, and
multi-character needles. A successful rewrite discharges the *added* fact;
the fact is absent from the original faster/slower comparison's base input.
Solving that original input may additionally require generating a useful
lemma, so this declaration alone is not a demonstrated performance fix.

### M-3: lexicographic prefix cancellation

**Origin.** [#11151](https://github.com/cvc5/cvc5/issues/11151) asserts
`str.<(str.++(s,t,u),s)`. [#9875](https://github.com/cvc5/cvc5/issues/9875)
asserts `str.<=(str.++(s,t,"a"),s)`. A string cannot precede its own prefix;
equality is possible only when the suffix is empty.

```lisp
(define-rule metagraphe-str-lt-own-prefix
  ((s String) (ts String :list))
  (str.< (str.++ s ts) s)
  false)

(define-rule metagraphe-str-leq-own-prefix
  ((s String) (ts String :list))
  (str.<= (str.++ s ts) s)
  (= (str.++ ts) ""))
```

These rules include empty strings and arbitrary Unicode characters. The
non-strict case in #9875 becomes false because its suffix contains a nonempty
constant. A wider family cancels an identical prefix from both operands of
`str.<` or `str.<=`; choose one decreasing orientation to avoid cycles.

**Availability and next check.** The pinned
[`StringsRewriter::rewriteStringLeq`][str-cpp] handles identical operands,
constants, empty strings, and differing constant prefixes, but does not cancel
a shared symbolic prefix. Existing [RARE ordering rules][str-rules] also leave
this specific case open. `str.<` already expands to disequality plus `str.<=`,
so test the non-strict rule after that normalization as well as the original
syntax. The list variable accommodates flattened concatenations.

### M-4: signed comparison disjunction

**Origin.** [#11357](https://github.com/cvc5/cvc5/issues/11357) reports that a
quantified disjunction fails while the equivalent `bvsle` formula succeeds.
After normalizing `not(bvsge(x,0))` to `bvslt(x,0)`, the identity is:

```lisp
(define-rule metagraphe-bv-eq-or-slt
  ((x ?BitVec) (y ?BitVec))
  (or (= x y) (bvslt x y))
  (bvsle x y))
```

This is reflexive closure of signed strict order, valid at every common
positive width, including width one. It does not mix signed and unsigned
orders and involves no arithmetic overflow. Include reversed Boolean/equality
operand orders when integrating it, and inspect how `bvsle` is subsequently
eliminated. An unsigned counterpart is independently valid.

**Availability and next check.** No direct disjunction rule was found in the
pinned [BV RARE simplifications][bv-rules]. The
[maintainer reports](https://github.com/cvc5/cvc5/issues/11357#issuecomment-2476882359)
that `--cegqi-full` or logic `BV` solves the example. Thus this is also a
configuration-sensitive quantifier problem, not evidence that BV reasoning is
generally incomplete. Compare default `ALL`, `BV`, and `--cegqi-full`, checking
both the simplified body and the complete quantified query. A RARE proof
identity and an effective default simplification are separate deliverables.

### M-5: complement of a character

**Origin.** [#12815](https://github.com/cvc5/cvc5/issues/12815) uses
`re.inter(re.allchar,re.comp(str.to_re("/")))` inside path-segment stars.
The proposed normalization replaces this character class with two ranges:

```lisp
(define-rule metagraphe-re-allchar-except-slash ()
  (re.inter re.allchar (re.comp (str.to_re "/")))
  (re.union (re.range "\u{0}" ".")
            (re.range "0" "\u{2ffff}")))
```

The endpoints cover precisely the [SMT-LIB alphabet][string-semantics] except
code point 47. The printable-ASCII alternative in an
[issue comment](https://github.com/cvc5/cvc5/issues/12815#issuecomment-5257520827)
restricts the language; it is not an equivalent rewrite for arbitrary strings.
The intersection with `re.allchar` is essential: complement alone also contains
strings of other lengths. A general implementation should evaluate arbitrary
constant character exclusions and handle endpoint characters with one range.

**Availability and next check.** No literal character-complement-to-ranges
rule was found in [the RARE file][str-rules]; the regex inclusion machinery in
[sequence rewriting][seq-cpp] requires further investigation. Compare this
encoding on the complete inclusion query. Smaller character classes do not
guarantee that concatenation and negative membership become easy. Prefer a
general character-class normalizer if it can justify this transformation
without adding a collection of punctuation-specific rules.

### M-6: guarded zero division

**Origin.** [#11201](https://github.com/cvc5/cvc5/issues/11201) identifies
`ite(v=0,0,div(0,v))` as the obstacle inside a string-length/modulus expression.

```lisp
(define-rule metagraphe-int-zero-div-guard ((v Int))
  (ite (= v 0) 0 (div 0 v))
  0)
```

If `v=0`, the selected branch is zero; otherwise Euclidean division of zero
is zero. The guard is indispensable for surface SMT-LIB `div`: do not propose
`div(0,v) -> 0` without it. The zero-divisor value is underspecified in the
[integer theory](https://smt-lib.org/theories-Ints.shtml).

**Availability and next check.** The pinned [arithmetic rules][arith-rules]
distinguish `div` from internal `div_total`; no rule with this surface guarded
pattern was found there. Inspect ITE contextual simplification and division
elimination before adding a special case. The rule collapses the reported
inner term, after which its outer constant operations can be evaluated.

### M-7: modular arithmetic

Two secondary-theory reports have compact mathematical remedies:

* [#11535](https://github.com/cvc5/cvc5/issues/11535): under `c>0`,
  `mod(a*c*b,c) -> 0`. A [maintainer](https://github.com/cvc5/cvc5/issues/11535#issuecomment-2605819222)
  attributes the regression to nonlinear extended simplification. For surface
  `mod`, require `c != 0` and explain how that fact becomes available.
* [#11872](https://github.com/cvc5/cvc5/issues/11872):
  `mod(n*(n+1),2) -> 0` for every integer, including negative integers, because
  one of two consecutive integers is even. Account for polynomial expansion
  to `n*n+n` before matching.

The internal totalized operators offer these RARE drafts:

```lisp
(define-rule metagraphe-mod-total-factor
  ((xs Int :list) (c Int) (ys Int :list))
  (mod_total (* xs c ys) c)
  0)

(define-rule metagraphe-mod-total-consecutive ((n Int))
  (mod_total (* n (+ n 1)) 2)
  0)
```

The first is also valid for `c=0`: the product is zero and cvc5's
`mod_total(t,0)` is `t`, so the result is zero. This internal convention is
explicit in the [pinned arithmetic rules][arith-rules] and
[`rewriteIntsDivModTotal`][arith-cpp]. It does **not** justify the same
unconditional rule for surface `mod`.

**Availability and next check.** The inspected rules handle nested moduli but
do not declare these two patterns. Factor normalization, known nonzero
conditions, and existing nonlinear extended simplification need runtime
comparison. The parity rule is a narrow seed for modular polynomial reasoning,
not a solution to arbitrary nonlinear arithmetic.

### M-8: learned lengths and encoded reversal

**Origin and correction.** [#10522](https://github.com/cvc5/cvc5/issues/10522)
asks to reduce lengths of one-character substrings using a known input length.
The [attachment](https://github.com/cvc5/cvc5/files/14657704/str20.smt2.txt)
actually asserts `((_ int2bv 64) (str.len s)) = (_ bv4 64)`.
As the [maintainer explains](https://github.com/cvc5/cvc5/issues/10522#issuecomment-2090831450),
that means length congruent to four modulo `2^64`, not exactly four. Since
length is nonnegative, it does imply length at least four mathematically;
extracting and using that bound is a separate solver task.

The useful identity is `len(substr(s,i,n)) -> n` under
`0 <= i`, `0 <= n`, and `i+n <= len(s)`. **It already exists** as
`str-len-substr-in-range` in [the RARE file][str-rules]. The
[discussion](https://github.com/cvc5/cvc5/issues/10522#issuecomment-2015208979)
distinguishes local rewriting from learning lengths globally and links
[PR #10717](https://github.com/cvc5/cvc5/pull/10717) as relevant prior work.
Do not submit the existing rule as a new finding or assume that PR resolves
the still-open issue.

[#11010](https://github.com/cvc5/cvc5/issues/11010) is related but different:
its [inspected attachment](https://github.com/user-attachments/files/16110870/symcc-structs-assertions-modified.smt2.txt)
does assert length exactly four. It encodes reversal through concatenated
substrings, followed by character-code and BV conversions. There is no
`str.rev` node to match. The existing `seq-rev-rev` rule already eliminates
native double reversal. The opportunity is instead to use length facts to
normalize the encoded reversals, or recognize that encoding first. Do not
cancel `int2bv(8, str.to_code(...))` as if it preserved arbitrary Unicode
codes; the conversion is modulo 256.

**Next check.** Compare native reversal, the actual four-substring encoding,
exact length, and the modular length constraint separately. This is a context
and rule-composition project; the issue evidence does not support a claim that
one missing double-reversal declaration is the fix.

### M-9: string order totality

[#12042](https://github.com/cvc5/cvc5/issues/12042) asserts `x != y`,
`not(str.<(x,y))`, and `not(str.<(y,x))`. String order is total, giving

```text
and(not(str.<(x,y)), not(str.<(y,x))) -> (x = y)
```

This is a valid local Boolean identity when that conjunction occurs. The
original has separate assertions, and [strict-order elimination][str-cpp]
also changes the shape. A preprocessing combination or theory lemma may be
needed. Prototype on both the combined term and the original assertion set;
track proof reconstruction and term growth. This is a plausible rewrite
family, with lower implementation confidence than M-3.

### M-10: character-language intersections

[#11206](https://github.com/cvc5/cvc5/issues/11206) constrains a string to both
`(a|b)*` and `(b|c)*`. Their intersection is `b*`. More generally:

```text
re.inter(re.*(A), re.*(B)) -> re.*(re.inter(A,B))
  provided both A and B accept only strings of length one
```

Proof: membership in either star is a position-by-position restriction on
characters. The restriction is essential: for arbitrary languages, take
`A={"ab"}`, `B={"a","b"}`. The left side contains `"ab"` but the proposed
right side does not. Do not turn this into a general star/intersection rule.

The full report also has `s*t=t*s`, a lower bound on `len(s)`, and exclusion of
`b*` for `t`. Reducing the intersection leaves commutation/periodicity reasoning
to establish the contradiction. Audit [regex rewriting][seq-cpp] and existing
membership rules before claiming a missing normalization, then compare the
normalized full query. A syntax rule alone may need a character-language
entailment check to discharge its condition.

## Existing coverage and leads needing more work

| issue | disposition |
| --- | --- |
| [#10520](https://github.com/cvc5/cvc5/issues/10520), small BV remainder query | **Already represented in RARE and C++.** `bvult(x,bvurem(C,x))` is equivalent to `x=0 AND C!=0`. With the issue's nonzero constant it becomes `x=0`; BV remainder by zero is the dividend. `bv-ugt-urem` in [RARE][bv-rules] and `UgtUrem` in [C++][bv-cpp] express the symmetric greater-than form. Investigate orientation/reachability and rerun before declaring either a missing rule or a fixed issue. |
| [#9420](https://github.com/cvc5/cvc5/issues/9420), modulus sign | `mod(x,y)=mod(x,abs(y))` for nonzero `y` is valid, but [the comments](https://github.com/cvc5/cvc5/issues/9420#issuecomment-1404268724) already point to `--learned-rewrite`; the reporter found mixed suite results. This is existing conditional support and a default-policy question. |
| [#10508](https://github.com/cvc5/cvc5/issues/10508), nested replacement emptiness | A further string candidate: `replace_all(replace_all(a,b,a),c,a) = ""` iff `a = ""`. If `a` is nonempty, both stages preserve nonemptiness. Together with `str.<= "A" a`, this contradicts the report. Reduce to reusable emptiness rules rather than hard-coding two nested replacements; availability remains unchecked. |
| [#11156](https://github.com/cvc5/cvc5/issues/11156), sequence prefix/index | `prefixof(t,s)` implies `indexof(s,t,0)=0`, including empty `t`. This contradicts the issue's index bound already. A conditional lemma or conjunction rewrite is plausible, but the assertions are separate and prefix elimination may change the match. |
| [#11460](https://github.com/cvc5/cvc5/issues/11460), substring containment | Propagate absence of a character from a substring to a contained one-character slice. Requires proving index inclusion and nonempty/in-range slices from arithmetic context. The attachment was not reduced here. |
| [#11970](https://github.com/cvc5/cvc5/issues/11970), inverse case conversion | A fixed ASCII target can suggest regex preimages, e.g. `to_lower(s)="a"` iff `s` is `"a"` or `"A"`. Longer targets need length control and per-character choices. Check cvc5's exact conversion semantics and growth; the [maintainer](https://github.com/cvc5/cvc5/issues/11970#issuecomment-2956111004) describes a broader solver technique. |
| [#10850](https://github.com/cvc5/cvc5/issues/10850), nested ITE/extract synthesis | Comparison decomposition may supply rules, but grammar feasibility, quantifiers, and signedness need attachment-level analysis. No specific missing rule established. |
| [#9417](https://github.com/cvc5/cvc5/issues/9417), BV quotient/remainder | The identity requires a nonzero divisor, remainder bound, and **both** multiplication and addition no-overflow conditions. These are contextual facts, not permission for modular cancellation. Keep as a lemma candidate. |
| [#12801](https://github.com/cvc5/cvc5/issues/12801), RARE name in Alethe | Proof export/database consistency, not evidence of a missing simplifying identity. Track separately from this queue. |
| [#12353](https://github.com/cvc5/cvc5/issues/12353), Boolean operand order | A search-order performance report; commutativity alone does not identify a beneficial missing rewrite. |

Crash reports and incorrect-answer reports were not converted into rewrite
requests merely because they mention rewriting. Likewise, a closed issue title
in the historical search is not evidence for a new rule.

## Validation and implementation handoff

**Semantics.** The arguments above use SMT-LIB 2.7
[Unicode Strings][string-semantics] (updated 2025-12-03),
[FixedSizeBitVectors](https://smt-lib.org/theories-FixedSizeBitVectors.shtml), and
[Ints](https://smt-lib.org/theories-Ints.shtml) (updated 2026-01-16), consulted
2026-09-19. Sequence polymorphism and internal totalized arithmetic follow the
pinned cvc5 sources. The candidate validity arguments are mathematical case
analyses, not machine-checked proofs.

**Draft syntax.** The ten draft rules in the `lisp` blocks were parsed and passed through
`mkrewrites.validate_rule` using the pinned upstream parser. This checks the
draft language accepted by that parser, not proof validity, full generated C++
compilation, or operational matching. Reproduce with an unpacked checkout at
the source revision above, Python, and cvc5's `pyparsing` dependency:

```bash
python3 - /path/to/pinned-cvc5 docs/github-issues-rewrites.md <<'PY'
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(sys.argv[1]) / "src/rewriter"))
from rw_parser import Parser
from mkrewrites import validate_rule

document = Path(sys.argv[2]).read_text()
drafts = "\n".join(re.findall(r"```lisp\n(.*?)```", document, re.S))
rules = Parser().parse_rules(drafts)
for rule in rules:
    validate_rule(rule)
print(f"Validated {len(rules)} draft rules")
PY
```

**Next implementation prompt.** Start with M-1 through M-4. For each:

1. Pin a clean cvc5 source **and matching binary**, build options, and the exact
   simplification entry point. Preserve the issue's original logic/options;
   compare alternative settings separately.
2. Check what is already implemented in the theory rewriter, extended
   rewriting, preprocessing, RARE, and regressions. Record actual current
   behavior before claiming a gap. Adapt matches to normalized equality,
   Boolean, and concatenation forms.
3. Prove the identity for its stated sorts and conditions. Query
   `P AND lhs != rhs`; record `unsat`, `sat`, `unknown`, or timeout accurately.
   Check condition satisfiability. Keep the counterexamples in M-1, M-2, M-5,
   and M-10 as guards against overgeneralization.
4. Implement the effective simplification and its RARE proof support together
   where necessary. Run focused correctness/proof regressions, then compare
   the original report and a small surrounding family. Assess growth, cycles,
   and replacement work, not just expression size.
5. Report whether the change fixes the exact issue, simplifies only a subterm,
   or needs contextual lemmas. Preserve unsuccessful and already-handled
   candidates. No speedup or upstream resolution is established by this survey.

[str-rules]: https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/rewrites
[seq-cpp]: https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/sequences_rewriter.cpp
[str-cpp]: https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/strings/strings_rewriter.cpp
[bv-rules]: https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/bv/rewrites-simplification
[bv-cpp]: https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/bv/theory_bv_rewrite_rules_simplification.h
[arith-rules]: https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/arith/rewrites
[arith-cpp]: https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/theory/arith/arith_rewriter.cpp
[rare-grammar]: https://github.com/cvc5/cvc5/blob/dbf176dfb71b272ffbfdee06888dace73fee5aa8/src/rewriter/README.md
[string-semantics]: https://smt-lib.org/theories-UnicodeStrings.shtml
