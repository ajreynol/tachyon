# String benchmarks where cvc5 trails Z3-Noodler

**2026-09-20 — paired benchmark comparison, reduction, source audit, and
equivalence checks.** The human launched
[`prompts/metagraphe_compare_solvers`](../../../../prompts/metagraphe_compare_solvers)
with a QF_SLIA corpus, a pinned cvc5 build, and Z3-Noodler as the external
solver, asking which string benchmarks cvc5 loses and whether a missing rewrite
could explain any of them. This entry records the screening, the confirmed
gaps, two concrete candidate rewrites (filed as M-21 and M-22), and the leads
that are **not** rewrite gaps.

## Question and scope

Search areas [S3](../directions.md) (strings at theory boundaries, regular
expressions) and [S2](../directions.md). This is a performance comparison
followed by reduction, an equivalence check, and a targeted source audit. It is
not a proof of either candidate and not a measurement of cvc5 with either rule
implemented.

## Provenance

| item | value |
| --- | --- |
| cvc5 binary | `~/bin/ajr-cvc5`, self-reported `cvc5 1.3.5.dev+master@40a4bb7e43`, GCC 15.2.0, built 2026-08-25 |
| cvc5 source | `40a4bb7e43adf97534c29a52ed079c4efd687644` ("Add proveEqualityWithRewriteSteps utility (#12655)", 2026-08-25), read from a local checkout containing that commit |
| cvc5 SHA-256 | `c7a6225edc89a5c9b8592fd3f61959918345e15f0aaee4715584495997ac94fc` |
| external binary | `~/bin/z3noodler`, self-reported `Z3 version 5.1.0 - 64 bit - build hashcode ccf9f8e330e880b293e1f67df46d093f1550ae1e - mata hashcode d28368a6957a1606162aea3fbe77345f6e1e13d5` |
| external SHA-256 | `486635590617c63a433a2c32c08e8d025af4b043e49c6d927f27d1661f840090` |
| external string backend | `smt.string_solver` defaults to `noodler` in this build; a plain invocation reports the `noodler-final_checks` statistic, and `smt.string_solver=seq` instead reports `seq-*` statistics. Both solvers were run with **no extra arguments**, as configured |
| corpus | `~/benchmarks/smt-lib-2026/non-incremental/QF_SLIA`, 84,411 inputs in 14 families, left unmodified |
| semantics | SMT-LIB [Unicode Strings](https://smt-lib.org/theories-UnicodeStrings.shtml), consulted 2026-09-16 (unchanged for this entry) |
| host | 24 logical cores, Linux; solvers run **sequentially**, never concurrently |

**Logic coverage is narrower than the configuration names.** The configured
`benchmarks_dir` is the `QF_SLIA` directory, so the configured `QF_S` and
`QF_SNIA` logics contributed nothing: every sampled input declares
`(set-logic QF_SLIA)`, and no input under that directory declares another
logic. The sibling `QF_S/` and `QF_SNIA/` directories exist one level up and
were **not** sampled. Re-running with `--benchmarks-dir` set to
`non-incremental/` would cover all three.

## Reproduction

Sampling, running, analysis and pattern counting scripts are in ignored
`scratch/metagraphe-compare/`, which also holds the raw solver output; that
scratch copy is disposable and is not an archive.

```bash
# deterministic stratified sample: sha256("metagraphe-2026-09-20|<relpath>")
# orders each family; 200 inputs allocated evenly, remainder to the largest
python3 scratch/metagraphe-compare/sample.py                  # -> sample.json

# screening: both solvers, same input, 10 s wall clock, RLIMIT_AS 8 GiB, sequential
python3 scratch/metagraphe-compare/run_pairs.py --timeout 10  # -> screen.json
python3 scratch/metagraphe-compare/analyze.py

# confirmation: 10 diverse leads, 3 repetitions each, 60 s wall clock
python3 scratch/metagraphe-compare/run_pairs.py --timeout 60 --repeats 3 \
  --only scratch/metagraphe-compare/shortlist.txt --out .../confirm.json

# candidate-pattern occurrence counts over the sample and the whole corpus
python3 scratch/metagraphe-compare/count_patterns.py <paths>

# original vs hand-rewritten scratch inputs, 3 repetitions, 60 s
python3 scratch/metagraphe-compare/run_value.py               # -> value.json
python3 scratch/metagraphe-compare/run_focus.py               # -> focus.json

# candidate equivalence checks on both solvers
python3 scratch/metagraphe-compare/reduce/check_equiv.py

# rewriter probe used throughout (prints cvc5's preprocessed assertions)
~/bin/ajr-cvc5 --preprocess-only -o post-asserts <input>.smt2

# RARE drafts, parsed with the pinned cvc5 tooling at 40a4bb7e43
python3 scratch/metagraphe-compare/rare/check_rare.py <drafts>.rare
```

## Observed results: screening

200 paired inputs, 10 s and 8 GiB for both solvers, run sequentially.
**No answer disagreement was observed**, so nothing was quarantined; no input
was reported unsupported and no solver error occurred.

| outcome | count |
| --- | ---: |
| both `unsat` | 89 |
| both `sat` | 71 |
| cvc5 timeout, Z3-Noodler solved | 29 |
| cvc5 solved, Z3-Noodler timeout | 7 |
| both timeout | 4 |
| **cvc5 solved** | **167 / 200** |
| **Z3-Noodler solved** | **189 / 200** |

Per-family coverage (solved out of sampled):

| family | sampled | cvc5 | Z3-Noodler |
| --- | ---: | ---: | ---: |
| 2015-Norn | 14 | 14 | 14 |
| 2018-Kepler | 14 | 8 | 14 |
| 20180523-Reynolds | 15 | 15 | 15 |
| 2019-Jiang | 14 | 14 | 14 |
| 2019-Leetcode | 14 | 14 | 14 |
| 2019-full_str_int | 15 | 15 | 15 |
| 20190311-str-small-rw-Noetzli | 14 | 14 | 14 |
| 20230327-stringfuzz-lu | 15 | 12 | 15 |
| 20230329-denghang | 14 | 13 | 14 |
| 20230329-woorpje-lu | 14 | 14 | 13 |
| 20230331-transducer-plus | 14 | 9 | 4 |
| 20230403-webapp | 14 | 9 | 14 |
| 20240411-redos_attack_detection | 15 | 2 | 15 |
| 20250410-matching | 14 | 14 | 14 |

**Reverse wins are real and concentrated.** Z3-Noodler solved only 4 of the 14
sampled `20230331-transducer-plus` inputs against cvc5's 9, and lost one
`20230329-woorpje-lu` input. Seven inputs are cvc5-only solves. Three
both-solved inputs show Z3-Noodler at least 3x slower, the largest being
`20230329-woorpje-lu/track05/05_track_87.smt2` at 0.436 s against cvc5's
0.010 s. Any claim that cvc5 "loses on strings" is false at this granularity:
it loses badly on four families and wins on one.

## Observed results: confirmation

Ten diverse leads, 3 repetitions each, 60 s and 8 GiB, sequential. Statuses
were identical across repetitions for every input; the table gives each
solver's median.

| input | cvc5 | median | Z3-Noodler | median |
| --- | --- | ---: | --- | ---: |
| `2018-Kepler/quad-105-4-2-sat.smt2` | timeout | 60.04 s | sat | 0.011 s |
| `20240411-redos_attack_detection/sat/73_attack.smt2` | timeout | 60.13 s | sat | 0.008 s |
| `20240411-redos_attack_detection/unsat/825_attack.smt2` | timeout | 60.16 s | unsat | 0.009 s |
| `20230403-webapp/str-rep/str_replace231.smt2` | timeout | 60.07 s | sat | 0.013 s |
| `20230327-stringfuzz-lu/generated/regexlengths/regex-lengths-00426-14.smt2` | timeout | 60.09 s | sat | 0.011 s |
| `20230331-transducer-plus/Commutativity/toLower-toUpper.smt2` | timeout | 60.05 s | sat | 1.538 s |
| `20230327-stringfuzz-lu/generated/variants/2f407694.smt2` | sat | 31.12 s | sat | 0.011 s |
| `20230403-webapp/lan-rep-all/lan_replace_all63.smt2` | sat | 20.88 s | sat | 0.017 s |
| `20230329-denghang/instance51087.smt2` | sat | 10.14 s | sat | 0.013 s |
| `2019-full_str_int/py-conbyte_z3seq/leetcode_int-restoreIpAddresses/1479.smt2` | sat | 2.16 s | sat | 0.073 s |

Six of the ten remain cvc5 timeouts at the six-fold limit. The other four are
solved by cvc5 at 29x to roughly 2800x Z3-Noodler's time, so the 10 s screening
threshold understates rather than invents these gaps.

## Ranked assessment of the confirmed gaps

Ranked by how much of the gap a *rewrite* could plausibly explain, which is not
the same as ranking by the size of the gap. This is the agent's assessment.

| rank | lead | what the gap is | rewrite candidate? |
| ---: | --- | --- | --- |
| 1 | stringfuzz `regexlengths` / `variants` | Nested `re.*`/`re.+` in a long concatenation with a length lower bound | **Yes — M-22.** cvc5 leaves `(re.* (re.++ r (re.* r)))` unsimplified |
| 2 | denghang `instance51087` and siblings | Sanitizer constraint `not (X in Sigma* (c1&#124;...&#124;cn) Sigma*)` beside a bounded `re.loop` | **Yes — M-21**, but the measured cost here is the `re.loop`, not the membership |
| 3 | webapp `str-rep` / `lan-rep-all` | `sink = a ++ atkPtn ++ b` with `atkPtn` in a regular language and `a`, `b` otherwise unconstrained | No. Recognising this needs variable-occurrence analysis, not a local rewrite |
| 4 | 2018-Kepler `quad-*` | Quadratic word equations with `str.len x1 > 16000` | No. A decision-procedure/strategy gap (Nielsen transformation), not a rewrite |
| 5 | redos `*_attack` | `((_ re.loop 5000 5000) r)` over a nontrivial `r` | No. A preprocessing/strategy gap: cvc5 eliminates `re.loop` by unrolling |
| 6 | transducer `toLower-toUpper` | 52 nested `str.replace_all` forming two case maps | No exact rule proposed. Composing case maps is a separate, much larger proposal |

Items 3 to 6 are recorded here and deliberately **not** filed in
[`rewrites.json`](../../rewrite_db/rewrites.json): they are strategy,
preprocessing, or occurrence-analysis observations without an exact
`lhs -> rhs`, which the [reporting policy](../../rewrite_db/reporting-policy.md)
keeps in the ledger.

`re.loop` elimination was observed directly: on the 0-to-30 loop in
`instance51087`, `--preprocess-only -o post-asserts` returns a 31-way
disjunction over concatenations of the loop body. The same mechanism applied to
`re.loop 5000 5000` explains the redos family.

## Candidate M-21 — containment disjunction from a character-union membership

**Reduction.** `20230329-denghang/instance51087.smt2` asserts a sanitizer
condition of the shape

```text
(not (str.in_re X (re.++ re.all (re.union (str.to_re "<") (str.to_re ">")
                                          (str.to_re "'") (str.to_re "\u{22}")
                                          (str.to_re "&")) re.all)))
```

`re.all` is eliminated to `(re.* re.allchar)` by the existing `re-all-elim`
rule, so the middle argument is the only non-`Sigma*` child.

**Availability.** cvc5 already rewrites the single-string case. On a two-line
probe, `x in (re.++ Sigma* (str.to_re "<") Sigma*)` becomes
`(str.contains x "<")` (`Rewrite::RE_CONCAT_TO_CONTAINS`, in
`SequencesRewriter::rewriteMembership`). With the constant replaced by a union
of `str.to_re` arguments, the term is returned **unchanged**, under the default
configuration and under both `--re-elim=on` and `--re-elim=agg`. The source
reason is visible in `rewriteMembership`: the `REGEXP_CONCAT` branch accepts at
most one `STRING_TO_REGEXP` child and sets `allSigma = false` for anything
else, so a `REGEXP_UNION` child aborts the match. `Rewrite::RE_IN_ANDOR`
distributes a union that is the *whole* regular expression, not one nested
inside a concatenation, and `re-union-const-elim` only removes a redundant arm.

**Validity.** Concatenation distributes over union, so
`L(Sigma* (s1|...|sn) Sigma*) = union_i Sigma* {si} Sigma*`, and
`x in Sigma* {si} Sigma*` is exactly `str.contains(x, si)` by the SMT-LIB
definition. No side condition is needed; `si = ""` makes both sides true, and
the argument is alphabet-independent, so it holds for sequences as well as
strings. Solver checks of `(distinct lhs rhs)`: Z3-Noodler returned `unsat` for
all nine constant instantiations tried — seven two-arm cases (including `""`,
a repeated arm, a prefix pair `"ab"`/`"abc"` and an overlapping pair
`"aa"`/`"a"`) and two three-arm cases, one of them `"<"`, `">"`, `"&"` from the
sanitizer set; cvc5 agreed on six and timed out on three at 20 s. With **symbolic** needles the question stayed open: cvc5
timed out and Z3-Noodler returned `unknown`.

**RARE draft.** The binary instance parses and validates with the pinned
`src/rewriter/rw_parser.py` and `mkrewrites.validate_rule` at `40a4bb7e43`. The
n-ary rule is the one the benchmarks need, and ordinary RARE cannot map
`str.to_re` over a `:list` parameter, so it would have to be a C++ rule beside
`RE_CONCAT_TO_CONTAINS`. A fixed-point peeling variant also parses, but each
step re-introduces a `str.in_re`, so it is the wrong orientation under the
project's operator-first ordering and is not filed.

## Candidate M-22 — idempotent nesting of regular-expression star and plus

**Reduction.** `20230327-stringfuzz-lu/generated/regexlengths/regex-lengths-00426-14.smt2`
contains `(re.* (re.+ (str.to_re "ccc")))` and `(re.+ (re.+ (str.to_re "ddd")))`
inside one long concatenation under a `(<= 426 (str.len var0))` bound;
`.../generated/variants/2f407694.smt2` contains `(re.* (re.+ (str.to_re "8")))`.

**Availability.** Probing the four nestings with
`--preprocess-only -o post-asserts` at the pinned build:

| input regex | cvc5's rewritten form | handled? |
| --- | --- | --- |
| `(re.* (re.* r))` | `(re.* r)` | yes (`re-star-star`, `RE_STAR_NESTED_STAR`) |
| `(re.+ (re.* r))` | `(re.* r)` | yes |
| `(re.* (re.+ r))` | `(re.* (re.++ r (re.* r)))` | **no** |
| `(re.+ (re.+ r))` | `(re.++ r (re.* r) (re.* (re.++ r (re.* r))))` | **no** |

`re-plus-elim` rewrites `re.+` first, so the missing rule has to be stated on
the eliminated form. `SequencesRewriter::rewriteStarRegExp` handles a nested
star, an empty or `re.none` body, and unions containing `re.allchar` or
epsilon, but not a body of the form `(re.++ r (re.* r))`. Adding
`(re.* (re.++ r (re.* r))) -> (re.* r)` closes **both** rows: in the second
row the inner star collapses first, leaving `(re.++ r (re.* r) (re.* r))`,
which the existing `re-concat-star-repeat` rule reduces to `(re.++ r (re.* r))`.

**Validity.** `L((R R*)*) = (L(R) L(R)*)* = (L(R)+)* = L(R)*`: one inclusion
because `L(R)+ subset L(R)*`, the other because every nonempty member of
`L(R)*` is a concatenation of at least one `R`-word. Solver checks of
`(distinct lhs rhs)` for ten concrete `r` — including `re.none`,
`(str.to_re "")`, `re.allchar`, a range, a union, a nullable union, a starred
body and a concatenation — returned `unsat` from Z3-Noodler in every case, and
from cvc5 in the four it did not time out on. The general identity rests on the
written argument: cvc5 rejects regular-expression variables, so no
solver-checked schematic version is available here.

**RARE draft.** The core rule and both surface identities parse and validate
with the pinned tooling at `40a4bb7e43`.

## Where the two patterns occur

`count_patterns.py` parses each input's s-expressions and counts the two shapes
structurally (not by text search). `P1` is a `str.in_re` whose regular
expression is a concatenation of `(re.* re.allchar)` arguments and exactly one
`re.union` all of whose arguments are `str.to_re`, with at least two arms. `P2`
is `(re.* (re.+ r))`, `(re.+ (re.+ r))` or the eliminated
`(re.* (re.++ r (re.* r)))`.

| scope | files | P1 occurrences / files | P2 occurrences / files |
| --- | ---: | ---: | ---: |
| the 200-input sample | 200 | 14 / 14 | 43 / 5 |
| all of QF_SLIA | 84,411 | 998 / 998 | 88,572 / 4,192 |

P1 is confined to `20230329-denghang` — 998 of that family's 999 inputs. P2 is
concentrated in `20230327-stringfuzz-lu` (88,504 occurrences in 4,164 of its
11,618 inputs), with 59 more in 25 `20240411-redos_attack_detection` inputs and
9 in 3 `20230329-denghang` inputs. Both patterns are therefore frequent but
family-specific, and `20230327-stringfuzz-lu` is fuzzer-generated, so P2's
count says more about the generator than about hand-written inputs.

## Observed results: does applying the rewrite by hand help?

Each candidate was applied by hand to a copy of its motivating input, changing
nothing else, and the pair was run 3 times per solver at 60 s and 8 GiB. Medians:

| case | rule applied | cvc5 original | cvc5 rewritten | Z3-Noodler |
| --- | --- | ---: | ---: | ---: |
| `20230329-denghang/instance51087.smt2` | M-21 | sat, 10.12 s | sat, 11.09 s | sat, 0.012 s |
| stringfuzz `regex-lengths-00426-14` | M-22 | timeout, 60.07 s | timeout, 60.09 s | sat, 0.010 s |
| stringfuzz `variants/2f407694` | M-22 | sat, 30.99 s | sat, 31.20 s | sat, 0.011 s |

**On the benchmarks that motivated them, neither rewrite helps.** M-21 is
slightly slower on `instance51087`, whose cost is the 31-way `re.loop`
expansion rather than the sanitizer membership. M-22 leaves both stringfuzz
inputs where they were, because the surrounding concatenation and the length
bound dominate.

Focused probes then isolate each pattern in a synthetic input containing
nothing else, again 3 repetitions at 60 s. Medians for cvc5:

| rule | `str.len` bound | original | rewritten |
| --- | ---: | --- | --- |
| M-21 | 200 | sat, 0.006 s | sat, 0.006 s |
| M-21 | 1000 | sat, 0.006 s | sat, 0.006 s |
| M-21 | 4000 | sat, 0.007 s | sat, 0.006 s |
| M-22 | 100 | **timeout, 60.06 s** | **sat, 0.409 s** |
| M-22 | 400 | **timeout, 60.06 s** | **sat, 22.17 s** |
| M-22 | 1000 | timeout, 60.08 s | timeout, 60.07 s |

Z3-Noodler answered every focused probe in 0.008 s to 0.014 s.

M-21 changes nothing even when it is the only structure present: cvc5 already
handles `Sigma* (u1|...|un) Sigma*` memberships cheaply, so its case rests on
term simplification, not on runtime. M-22 turns a 60 s timeout into 0.41 s at a
length-100 bound and into 22 s at 400, and still times out at 1000. That is a
real effect of the rewrite on a scratch input; it is **not** evidence that
implementing the rule inside cvc5 would produce the same result, since matching
cost and interaction with the concat-star normalisation are untested.

## Conclusion and limits

1. On this sample cvc5 solves 167 of 200 and Z3-Noodler 189 of 200, with no
   disagreement. The losses are concentrated in four families, and cvc5 wins
   clearly on `20230331-transducer-plus`.
2. Two concrete rewrites are missing from this cvc5 build and are filed as
   [M-21](../../rewrite_db/rewrites.md#m-21) and
   [M-22](../../rewrite_db/rewrites.md#m-22). Their validity is argued and
   checked on concrete instantiations, not proved; the schematic versions were
   not decided by either solver.
3. **Neither rewrite explains the benchmark gap that led to it.** M-22 has a
   measured effect in isolation; M-21 has none anywhere tested. Treat both as
   simplification candidates, not as explanations of the performance gap.
4. Four of the six confirmed gaps are not rewrite problems at all. The largest
   ones — quadratic word equations and `re.loop` unrolling — are decision
   procedure and preprocessing questions.
5. Coverage limits: one logic directory, one host, one repetition set, 200 of
   84,411 inputs, and no bit-vector corpus. Raw output lives in ignored
   `scratch/metagraphe-compare/` on this host only and is not archived.
