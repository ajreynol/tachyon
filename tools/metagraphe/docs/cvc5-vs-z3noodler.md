# Where cvc5 trails Z3-Noodler on QF_SLIA

**A study list, not a result.** These are ten small SMT-LIB inputs chosen to be
worth opening in an editor: each one isolates a mechanism where the two solvers
diverge sharply, and eight of the ten are under 1.5 kB. The point is to give a
person a short queue of concrete things to look at, with the current diagnosis
for each and what would plausibly help.

Evidence and provenance are in the two ledger entries this page draws on: the
[benchmark comparison](ledger/2026-09-20-string-benchmark-comparison.md) (200
paired inputs, coverage, reverse wins) and the
[bounded-repetition entry](ledger/2026-09-20-regex-loop-candidates.md) (the
`re.loop` family and `str.replace_re_all`). Filed candidate rewrites live in the
[rewrite database](../rewrite_db/rewrites.md). Diagnoses below are an agent's
reading of observed behaviour, not maintainer statements.

## Setup

cvc5 `1.3.5.dev+master@40a4bb7e43` matching source
`40a4bb7e43adf97534c29a52ed079c4efd687644`; Z3-Noodler `Z3 5.1.0` with mata
`d28368a6…`, whose `smt.string_solver` defaults to `noodler`. Both invoked with
no extra arguments, sequentially, under an 8 GiB address-space cap. Paths below
are relative to `<corpus>/non-incremental/QF_SLIA/`, where `<corpus>` is an
SMT-LIB 2026 checkout.

```bash
~/bin/ajr-cvc5  <corpus>/non-incremental/QF_SLIA/<path>
~/bin/z3noodler <corpus>/non-incremental/QF_SLIA/<path>
~/bin/ajr-cvc5 --preprocess-only -o post-asserts <input>    # see what cvc5 rewrote
```

## The shortlist

Medians of three sequential repetitions at a 30 s limit. `timeout` means all
three repetitions hit the limit.

| # | input | size | answer | cvc5 | Z3-Noodler | mechanism |
| ---: | --- | ---: | --- | ---: | ---: | --- |
| 1 | `2018-Kepler/quad-005-2-sat.smt2` | 656 B | sat | timeout | 0.008 s | quadratic word equation |
| 2 | `2018-Kepler/quad-024-3-unsat.smt2` | 749 B | unsat | timeout | 0.008 s | quadratic word equation, refutation |
| 3 | `20230403-webapp/lan-rep-all/lan_replace_all44.smt2` | 1.3 kB | unsat | timeout | 0.022 s | **degenerate `str.replace_re_all`** |
| 4 | `20230329-denghang/instance57871.smt2` | 1.1 kB | sat | timeout | 0.023 s | `re.loop` with a variable-length body |
| 5 | `20230329-denghang/instance51087.smt2` | 1.0 kB | sat | 10.06 s | 0.013 s | `re.loop 0 30`, sanitizer negation |
| 6 | `20230327-stringfuzz-lu/generated/regexlengths/regex-lengths-00426-14.smt2` | 1.4 kB | sat | timeout | 0.011 s | long regex concatenation + length bound |
| 7 | `20240411-redos_attack_detection/sat/3224_attack.smt2` | 1.3 kB | sat | 9.42 s | 0.008 s | `re.loop 5000 5000` |
| 8 | `20230403-webapp/str-rep/str_replace231.smt2` | 5.2 kB | sat | timeout | 0.013 s | regex containment via concatenation |
| 9 | `20230331-transducer-plus/Duality/htmlUnescape-addslashes.smt2` | 3.5 kB | sat | 0.416 s | timeout | **cvc5 wins**: nested `str.replace_all` |
| 10 | `20230329-woorpje-lu/track05/05_track_80.smt2` | 1.2 kB | sat | 0.013 s | timeout | **cvc5 wins**: word equation system |

Rows 9 and 10 are there on purpose. On the 200-input sample cvc5 solved 167 and
Z3-Noodler 189, but Z3-Noodler solved only 4 of 14 sampled
`20230331-transducer-plus` inputs against cvc5's 9. The gap is concentrated in
four families, not general.

## 1-2. Quadratic word equations — `2018-Kepler`

`quad-005-2-sat.smt2` is the whole problem in one line, with two variables:

```text
(= (str.++ x3 "abbc" x4) (str.++ x4 "cbba" x3))
```

`quad-024-3-unsat.smt2` is the same shape with three variables and no solution.
Both are 700-byte files that cvc5 cannot settle in 30 s and Z3-Noodler settles
in 8 ms. The family is crafted for a decision procedure for quadratic word
equations (Le and He, APLAS 2018); Z3-Noodler runs a Nielsen-transformation
search with a cycle check, cvc5 does not.

**What would help:** a decision procedure, not a rewrite. These two inputs are
the cheapest possible regression cases for one — no regular expressions, no
length constraints in `quad-005`, nothing to reduce. If a Nielsen-style loop
lands in cvc5, `quad-005-2-sat.smt2` is the first thing to run.

## 3. Degenerate `str.replace_re_all` — `20230403-webapp/lan-rep-all`

The only line that matters:

```text
(= x_4 (str.replace_re_all sigmaStar_048 (re.* re.allchar) ""))
```

Every single character is matched by `(re.* re.allchar)`, so by the SMT-LIB
"shortest non-empty match" rule this deletes the whole string: `x_4` is `""`.
The file then forces `".php"` to contain `"/evil"`, which is false. Z3-Noodler
sees this in 22 ms. cvc5 leaves the term untouched — asked on its own whether
`(str.replace_re_all x (re.* re.allchar) "")` equals `""`, it times out at 30 s
— and then reduces an extended function it did not need to.

**What would help: a rewrite, and it is measured.** Substituting `""` for that
one subterm, changing nothing else, takes cvc5 from a timeout that repeats three
times out of three at both a 30 s and a 60 s limit to **4 ms `unsat`**, also
three times out of three. Filed as [M-25](../rewrite_db/rewrites.md#m-25) with two
schemas and three parser-checked RARE drafts. This is the best
effort-to-payoff ratio on the list. The pattern comes from a taint-analysis
generator, so the rest of `20230403-webapp/lan-rep-all` is worth re-measuring
once it lands.

## 4-5, 7. `re.loop` expansion — `20230329-denghang`, `20240411-redos_attack_detection`

Three inputs, one mechanism. `instance57871.smt2` encodes the phone-number
regex `\+?(?:\d[ .-]?){7,20}`:

```text
((_ re.loop 7 20) (re.++ (re.range "0" "9") (re.opt (re.union " " "." "-"))))
```

`instance51087.smt2` has `((_ re.loop 0 30) …)`, and `3224_attack.smt2` has
`((_ re.loop 5000 5000) …)` over an `re.inter` of three `re.+` terms.

At this baseline `rewriteLoopRegExp` always expands: `--preprocess-only` turns
the 0-to-30 loop into a **31-way disjunction** over concatenations of the body,
and the 7-to-20 loop into a 14-way one. Z3-Noodler builds an automaton and
never enumerates. Note that the bodies here are **not** fixed-length — `re.opt`
makes the first one 1 or 2 characters long — so the fixed-length shortcut below
does not apply to any of the three.

**What would help: the loop strategy, not a rewrite.** The `reLoopImprove`
branch on `ajreynol/CVC4` already stops expanding when `u > 2` unless
`l == u <= 32`, unfolding one copy at a time instead; that is the change these
three inputs are asking for. `instance57871.smt2` is the sharpest regression
case because `l != u` and the body is variable-length, so it exercises the
unfolding path rather than any shortcut.

A related **rewrite** does exist for fixed-length bodies —
[M-23](../rewrite_db/rewrites.md#m-23), the identity the branch implements as
`RE_IN_LOOP_FIXED_LEN` — but it is worth being clear about its reach: across
all 84,411 QF_SLIA inputs the shape it matches occurs in **12 files**, and cvc5
already answers all 12 in about 0.1 s. On a focused probe it measured
*backwards* for cvc5, 0.05 s to 21 s at `loop{200,200}`, while making
Z3-Noodler 44x faster. Treat it as a simplification for automaton-based
backends and check it on cvc5 before assuming it pays there.

**A smaller sharp case to keep beside these:** cvc5 turns
`((_ re.loop 40 40) re.allchar)` into `(= (str.len x) 40)` but expands
`((_ re.loop 40 40) (re.range "a" "z"))` into forty concatenation children.
Same fixed length, opposite treatment; the first is handled only because the
expansion happens to match `RE_CONCAT_PURE_ALLCHAR`.

## 6. Long regex concatenation with a length bound — `20230327-stringfuzz-lu`

`regex-lengths-00426-14.smt2` is one membership in a ten-way concatenation of
starred and plussed alternations, plus `(<= 426 (str.len var0))`. cvc5 times
out at 60 s; Z3-Noodler answers in 11 ms, because a length lower bound against
an automaton is a Parikh-image question, not a search.

**What would help: length reasoning over regular expressions.** A rewrite is
not the lever here — hand-applying
[M-22](../rewrite_db/rewrites.md#m-22) (the nesting cleanup this file contains
twice) left the timeout exactly where it was. The nearby
`generated/variants/2f407694.smt2` is the same shape and *is* solvable, in
31 s, so it makes a better instrumented case: the two bracket what changes
between 31 s and a timeout.

## 8. Regex containment written as a concatenation — `20230403-webapp/str-rep`

The generator emits

```text
(assert (str.in_re atkPtn <attack-pattern>))
(assert (= atk_sink (str.++ atk_sigmaStar_1 atkPtn atk_sigmaStar_2)))
(assert (= sink atk_sink))
```

where `atk_sigmaStar_1` and `atk_sigmaStar_2` occur nowhere else. That is
"`sink` contains a word of the attack language" written with three variables
instead of one membership, and cvc5 spends its time splitting the
concatenation. Z3-Noodler answers in 13 ms.

**What would help: a preprocessing pass, not a rewrite.** Recognising this
needs to know that two variables are otherwise unconstrained, which a local
term rewrite cannot see. The clean statement is: an equality
`t = (str.++ a p b)` with `a`, `b` fresh and `p` constrained only by a
membership becomes `(str.in_re t (re.++ (re.* re.allchar) R (re.* re.allchar)))`
— and *that* form cvc5 already turns into `str.contains` when `R` is a single
constant ([M-21](../rewrite_db/rewrites.md#m-21) covers the union case).

## 9-10. Where cvc5 already wins

`htmlUnescape-addslashes.smt2` composes two transducers as 50-odd nested
`str.replace_all` terms; cvc5 answers in 0.4 s and Z3-Noodler times out.
`05_track_80.smt2` is a woorpje word-equation system cvc5 settles in 13 ms and
Z3-Noodler cannot. Any change aimed at rows 1-8 should be checked against these
two, and against the nine `20230331-transducer-plus` inputs cvc5 solved in the
sample where Z3-Noodler solved four.

## What has been tried, and what it did

| candidate | valid? | missing at `40a4bb7e43`? | measured effect on cvc5 |
| --- | --- | --- | --- |
| [M-21](../rewrite_db/rewrites.md#m-21) containment from a character-union membership | argued, instantiation-checked | yes | none: 10.1 s to 11.1 s on its own benchmark, unchanged in a focused probe |
| [M-22](../rewrite_db/rewrites.md#m-22) `(re.* (re.+ r)) -> (re.* r)` | argued, instantiation-checked | yes | none on its benchmarks; 60 s timeout to 0.41 s in a focused probe |
| [M-23](../rewrite_db/rewrites.md#m-23) fixed-length loop to star plus length | argued, instantiation-checked | yes, but implemented on `reLoopImprove` | negative: 0.05 s to 21 s in a focused probe |
| [M-24](../rewrite_db/rewrites.md#m-24) star or plus of a bounded repetition | argued, instantiation-checked | yes | none; the shape does not occur in this corpus |
| [M-25](../rewrite_db/rewrites.md#m-25) degenerate `str.replace_re_all` | argued, instantiation-checked | yes | **30 s timeout to 4 ms** on row 3 |

The pattern is worth stating plainly: four of the five rewrites are valid and
genuinely absent, and four of the five change nothing that matters. Missing
rewrites were not the reason cvc5 lost these benchmarks — with one exception,
which was worth the search.

## Next tests

1. Implement M-25 and re-measure all of `20230403-webapp/lan-rep-all`, not just
   row 3.
2. Run rows 4, 5 and 7 against a build of `reLoopImprove` and record whether
   the lazy loop policy alone closes them.
3. Bracket row 6 against `generated/variants/2f407694.smt2`, which is the same
   shape and solvable, to find what makes the difference.
4. Ask whether the concatenation pattern in row 8 is worth a preprocessing
   pass, and how often the generator that produced it emits the shape.
5. Re-run the comparison over `QF_S` and `QF_SNIA`, which the sampled directory
   did not contain.
