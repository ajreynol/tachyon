# 2026-09-29 — the two R12 option rows

**Goal 3, the last empty cells.** R12's two option-default proposals,
`--lemma-inprocess=light` and `--conflict-process=min`, were added to the
register on 2026-09-16 and never picked up by an option sweep. **Complete**: a
reference and both arms, one run each, on one binary.

## 1. What was asked

Fill the register's two remaining empty `± solved` cells. The direction's own
"What would settle it" asks for exactly these two runs.

## 2. What was run

cvc5 `d7d5b948c11d2d83be0212d4a954ef49740ecdab`, the revision every other option
row is measured at. It was rebuilt in the branch-sweep build directory, the one
the [one-reference re-run](2026-09-25-option-sweep-one-reference.md) and the
[`ai-heuresis-*` sweep](2026-09-28-ai-heuresis-branch-sweep.md) used. The
binary's `--show-config` hash was verified against the commit, and each arm's
options were smoke-tested on a trivial `unsat` input. That one build ran the
reference and both arms, back to back, on the idle host. The run was driven by a
script on the host, as waves 2 and 3 were, so there is no `job_launcher/log.txt`
entry. Each arm ran `solve_dir_rec_par_cvc5 -t 30 w1c-cvc5 cvc5_solve.sh
quant-092926-w1c-<arm> <options>`.

```
-q --no-cbqi --user-pat=strict --sat-solver=cadical  <one option added>
```

## 3. The set

`quant-07-25`, 6124 benchmarks, 30 s, one arm at a time on the idle host.

## 4. What came back

Results are `results-cvc5_solve.sh-quant-092926-w1c-<arm>.txt` on the host,
read with [`arms`](../../reports/arms), which uses the `gap` parser, as in the 2026-09-28 entry.

**The rebuilt reference solves 5574**, 5 unknown, 545 timeout, PAR2 39400.1.
Against the 2026-09-24 run of the same revision in the same directory (5576,
PAR2 39304.4) it is **+3 / −5**, net −2, PAR2 +0.24%. That is the third
measurement of this build and configuration, and all three are within the ±5
noise band. The arms are read against this run, their own batch's reference.

| option | gained | lost | net | unknown | timeout | PAR2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| *reference* | | | | 5 | 545 | 39400.1 |
| `--lemma-inprocess=light` | +11 | −12 | −1 | 8 | 543 | 39561.8 |
| `--conflict-process=min` | +4 | −14 | −10 | 5 | 555 | 39884.6 |

Against the 5576 run instead, the arms are +10 / −13 and +4 / −16, with the
same markers. Neither arm disagrees with the reference on sat versus unsat, and
neither logged an error. `--lemma-inprocess=light` answers `unknown` on 3
benchmarks the reference does not, two of which are one splinterdb problem that
appears twice in the set.

## 5. What it settled

**Neither option-default change is a proposal on this set.** Light lemma
inprocessing is inside noise: it decides 23 benchmarks differently and nets −1,
and its PAR2 is 0.4% worse. Conflict minimisation loses 14 benchmarks for 4 and
is 1.2% worse by PAR2. Both cells are ⚪, so R12's options join R13's and R29's
as measured and flat. The direction's other rows, the `subConflict` branch
arms, were already measured, so R12 has no empty cell left.

## 6. What it did not settle

**The mechanism.** The direction also asked for average lemma size before and
after. This run measured only speed, so whether inprocessing shrinks the
instance lemmas at all, and the cost of doing it, is still open. `full`
inprocessing and `min-ext` minimisation were not run. They are not proposal
rows.
