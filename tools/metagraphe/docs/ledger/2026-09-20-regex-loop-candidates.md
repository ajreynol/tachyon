# Bounded repetition and degenerate replace-all patterns

**2026-09-20 — rewriter probe, source audit of an unmerged branch, equivalence
checks, occurrence scan, and paired scratch measurements.** A second request in
the same session: the human proposed the identity

```text
(str.in_re s ((_ re.loop N N) R))
  ->
(and (str.in_re s (re.* R)) (= (str.len s) (* N m)))      ; m = the length of every word of L(R)
```

asked whether cvc5 already has it (there is a dedicated `reLoopImprove`
branch), asked for siblings, and asked for a study document naming benchmarks
worth attacking. This entry records what was checked. The study document is
[cvc5-vs-z3noodler.md](../cvc5-vs-z3noodler.md); it continues the
[benchmark comparison](2026-09-20-string-benchmark-comparison.md) and uses the
same binaries and corpus.

## Question and scope

Search area [S3](../directions.md). A rewriter probe and source audit, then
validity checks, an occurrence scan, and original-versus-rewritten measurements
on scratch inputs. Three candidates are filed: M-23, M-24 and M-25. Nothing
here proves a rule or measures cvc5 carrying one.

## Provenance

Binaries, corpus, limits and host are unchanged from the
[comparison entry](2026-09-20-string-benchmark-comparison.md): cvc5
`1.3.5.dev+master@40a4bb7e43` matching source
`40a4bb7e43adf97534c29a52ed079c4efd687644`, and Z3-Noodler `Z3 5.1.0` with
mata `d28368a6…`, both with no extra arguments, run sequentially under an 8 GiB
address-space cap.

**The branch.** `reLoopImprove` exists on the `ajreynol/CVC4` remote of a local
cvc5 checkout, at
[`f1fde0d583038f213c8534da4ae828fb8e9bc34a`](https://github.com/ajreynol/CVC4/commit/f1fde0d583038f213c8534da4ae828fb8e9bc34a)
(a merge of cvc5 `main` dated 2026-05-07), 18 commits ahead of its merge base
`56e2b54527` ("Prepare 1.3.4 release (#12656)"). It touches 13 files. Nothing
was fetched, pushed or modified; the branch was read only.

## Reproduction

```bash
# how cvc5 rewrites each re.loop and fixed-length shape
python3 scratch/metagraphe-compare/loop/probe.py

# equivalence checks for the whole family, on both solvers
python3 scratch/metagraphe-compare/loop/equiv.py

# where the shapes occur
python3 scratch/metagraphe-compare/loop/count_loops.py <dir>
python3 scratch/metagraphe-compare/loop/top_loop.py <dir>

# small cvc5-hard inputs (PARALLEL screen; finalists re-timed serially)
python3 scratch/metagraphe-compare/screen_small.py
python3 scratch/metagraphe-compare/time_shortlist.py

# original vs hand-rewritten scratch inputs, 3 repetitions, 60 s
python3 scratch/metagraphe-compare/run_focus2.py

# RARE drafts, pinned cvc5 tooling at 40a4bb7e43
python3 scratch/metagraphe-compare/rare/check_rare.py <drafts>.rare
```

## What the branch already does

`reLoopImprove` adds `Rewrite::RE_IN_LOOP_FIXED_LEN` in
`SequencesRewriter::rewriteMembership`, in the **bounded** form

```text
(str.in_re x ((_ re.loop l u) R))
  ->
(and (str.in_re x (re.* R)) (<= (* l k) (str.len x)) (<= (str.len x) (* u k)))
```

when `RegExpEntail::getFixedLengthForRegexp(R)` returns `k`. The proposed
`l = u = N` identity is its special case, with the two inequalities in place of
one equation. The branch also stops eliminating every loop: `rewriteLoopRegExp`
now expands only when `u <= 2` or (`u <= 32` and `l == u`), otherwise unfolding
one copy (`RE_LOOP_UNFOLD_ONE`) when `l == 1`. The rest of the diff is constant
evaluation for loops, regular-expression derivative work, two `neg-loop`
regressions and an Eunoia proof rule. **`rewriteStarRegExp` is untouched**, so
the star-of-loop family below is not covered by it.

## Rewriter probe at the recorded baseline

`--preprocess-only -o post-asserts`, one membership per input:

| input regular expression | cvc5's rewritten form | verdict |
| --- | --- | --- |
| `((_ re.loop 1 1) R)` | membership in `R` | handled |
| `((_ re.loop 0 0) R)` | `true` | handled |
| `((_ re.loop 40 40) re.allchar)` | `(= (str.len x) 40)` | handled, but only because the unrolled concatenation then matches `RE_CONCAT_PURE_ALLCHAR` |
| `((_ re.loop 40 40) (re.range "a" "z"))` | 40-fold concatenation | **not handled** |
| `((_ re.loop 500 500) (re.union …))` | 500-fold concatenation | **not handled** |
| `((_ re.loop 0 40) (re.union …))` | 41-way disjunction | **not handled** |
| `((_ re.^ 40) R)` | as `re.loop 40 40` | **not handled** |
| `((_ re.loop 0 40) (re.* R))` | `(re.* R)` | handled (`re-loop-star`) |
| `(re.* ((_ re.loop 1 3) R))` | `(re.* (re.union R RR RRR))` | **not handled** |
| `(re.+ ((_ re.loop 1 3) R))` | matching unsimplified form | **not handled** |
| `(re.* ((_ re.loop 2 3) R))` | left alone | correct: the identity needs `l <= 1` |
| `(str.replace_re_all x re.none t)` | `x` | handled |
| `(str.replace_re_all x (re.* re.allchar) "")` | unchanged | **not handled** |
| `(str.replace_re_all x re.allchar "")` | unchanged | **not handled** |
| `(str.replace_re_all x (str.to_re "") t)` | unchanged | **not handled** |

The `re.allchar` row against the `re.range` row is the sharpest statement of
the loop gap: two bodies of fixed length 1, one collapses to an arithmetic
constraint and the other becomes forty concatenation children.

## Equivalence checks

`(distinct lhs rhs)` on both solvers, 25 s each. Z3-Noodler decided every case;
cvc5 agreed wherever it did not time out.

| family | instantiations | result |
| --- | ---: | --- |
| M-23 exact, `N` in {0,1,3,7} over 7 bodies | 28 | all `unsat` |
| M-23 bounded, `(l,u)` in {(0,4),(2,5),(3,3)} over 4 bodies | 12 | all `unsat` |
| M-24 star of loop, `l <= 1 <= u` | 9 | all `unsat` |
| M-24 star of loop, `l = 2` | 6 | all `sat` — the side condition is necessary |
| M-24 plus of loop | 6 | all `unsat` |
| nested exact loops `(R{n}){k} = R{n*k}` | 9 | all `unsat` |
| M-25 delete-everything, four universal patterns | 4 | all `unsat` |
| M-25 with `R = (re.range "a" "z")` | 1 | `sat` — the side condition is necessary |
| M-25 empty-string pattern | 1 | `unknown` from Z3-Noodler, cvc5 timeout — open |

**A correction to the proposed side condition.** "Every word of `L(R)` has
length `m`" is vacuously true when `L(R)` is empty, and read that way the rule
is unsound: take `R = (re.inter (str.to_re "") re.none)`, `m = 0`, `N = 1`. The
left side is `"" in the empty language`, false; the right side is
`"" in {""}` and `0 = 1*0`, true. M-23 therefore states `L(R)` nonempty.
cvc5's syntactic `getFixedLengthForRegexp` returns nothing for `re.none`, so an
implementation built on it never meets this case — the premise is needed for
the written rule, not for the branch.

## Where the shapes occur

Structural scan of the whole QF_SLIA directory (84,411 inputs):

| shape | occurrences | files |
| --- | ---: | ---: |
| `re.loop` anywhere | 1,922 | 20230329-denghang only |
| … body of fixed length | 1,568 | 773 |
| … of those, exact `l == u` | 1,153 | — |
| membership whose **whole** regex is a loop | 36 | — |
| … with a fixed-length body — **M-23's actual footprint** | 12 | 12 |
| star or plus of a loop — **M-24's footprint** | 0 | 0 |

All 12 M-23 inputs are answered by cvc5 in about 0.1 s, so none of them is a
performance target. The remaining 1,556 fixed-length loops sit inside
concatenations, where neither the proposed rule nor the branch's version
applies.

## Original versus hand-rewritten scratch inputs

Three repetitions per solver, 60 s, 8 GiB, sequential; medians.

| case | rule | cvc5 original | cvc5 rewritten | Z3-Noodler original | Z3-Noodler rewritten |
| --- | --- | ---: | ---: | ---: | ---: |
| `lan_replace_all44` | M-25 | **timeout, 60.05 s** | **unsat, 0.004 s** | 0.022 s | 0.011 s |
| focused `loop{60,60}` | M-23 | sat, 0.020 s | sat, 0.496 s | 0.050 s | 0.011 s |
| focused `loop{200,200}` | M-23 | sat, 0.050 s | sat, 21.25 s | 0.481 s | 0.011 s |
| focused star of `loop{1,6}` | M-24 | sat, 0.073 s | sat, 0.113 s | 0.021 s | 0.021 s |

**M-25 is the one that pays.** Replacing a single `str.replace_re_all` over
`(re.* re.allchar)` with `""` turns a repeatable 60 s timeout into a 4 ms
`unsat`.

**M-23 measures backwards for cvc5.** On the focused pair the star-plus-length
form is 25x slower at `loop{60,60}` and 425x slower at `loop{200,200}`, while
Z3-Noodler moves the other way and becomes 44x faster at `loop{200,200}`. The
rewrite removes an operator and suits an automaton-based backend; on this cvc5
build the unrolled concatenation is the easier input. That is a statement about
two inputs, not about cvc5 carrying the rule, and it does not bear on the
branch's own motivation.

## Conclusion and limits

1. The proposed identity is valid under a nonemptiness premise and absent from
   the recorded baseline, but an implementation of its bounded generalisation
   already exists on the unmerged `reLoopImprove` branch. Filed as **M-23**.
2. Two siblings were found by probing rather than proposed: **M-24**, star or
   plus of a bounded repetition, the loop analogue of M-22; and **M-25**,
   degenerate patterns in `str.replace_re_all`. A third identity,
   `(R{n}){k} = R{n*k}`, checked out on nine instantiations but was **not**
   filed: cvc5 eliminates the inner loop first, so the shape never survives,
   and no occurrence was found.
3. Only M-25 has a positive measured effect. M-23 measures negative for cvc5
   and has a 12-file footprint; M-24 has none and no occurrence at all.
4. Limits: one corpus directory, one host, one build. The `re.loop` counts come
   from a syntactic scan that mirrors `getFixedLengthForRegexp` and was not
   cross-checked against cvc5's own computation. Raw output stays in ignored
   `scratch/metagraphe-compare/` on this host.
