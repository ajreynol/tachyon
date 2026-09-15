# 2026-09-15 — two caveats on the baseline of 2026-09-14, from reading code

**A correction entry.** Nothing was run. Both facts below were found while
reading cvc5 `main` (`f294265`) and Verus's source for
[`docs/directions.md`](../docs/directions.md), and both change how the
[baseline](2026-09-14-baseline.md) should be read. The baseline entry is not
edited; this one names it.

**1. The cvc5 runs used MiniSat, not CaDiCaL.** cvc5's `--sat-solver`
defaults to `cadical`, but `--incremental` defaults to `true`, and
`set_defaults.cpp` forces MiniSat for incremental solving unless the SAT
solver was set explicitly. Neither baseline config set it. The notes' "best
known" configuration (`--user-pat=strict --no-cbqi --sat-solver=cadical`,
the `u-ssc` tag in older runs) therefore differs from the ledger's `u-ss`
run by the SAT backend as well as by the two quantifier flags. The first run
of goal 3 is the baseline with `--sat-solver=cadical`; see R13 in
`docs/directions.md`.

**2. The z3 runs used five of Verus's nine options.** The list taken from the
host's `run_jobs` script (`auto_config=false smt.mbqi=false
smt.qi.eager_threshold=100 smt.delay_units=true smt.arith.nl=false`) is what
Verus passed at some point; Verus today (`source/air/src/context.rs`) also
passes `smt.case_split=3`, `smt.arith.solver=2`, `pi.enabled=false` and
`rewriter.sort_disjunctions=false`. Two of these are material: `case_split=3`
is relevancy-based case splitting, and `arith.solver=2` selects the legacy
simplex, which is the only solver for which `smt.arith.nl=false` does
anything. The z3 baseline is therefore "z3 with most of Verus's options",
not "z3 as Verus runs it". A rerun with the full list is cheap (about three
minutes) and should be done before the z3 numbers are quoted outside this
repository. The `quant-z3.conf` OPTS line is updated with this entry so the
next run is the full list; the ledger records which list each run used.

Neither caveat changes the shape of the result — a factor of four and a gap
set of a thousand are not artefacts of a SAT backend or a case-split mode —
but both change the numbers, and the numbers are the point.
