# 2026-09-29 — what the winning arms have in common

**An analysis entry; nothing was run.** It intersects the gained and lost sets
of the register's positive arms, using results already on the host. The
question is whether the positive arms are one effect or several. That decides
whether combining them can beat any one of them.

## 1. What was asked

Two questions from [`todo.md`](../todo.md). R10's next step since 2026-09-25 has
been to ask whether its three positive arms lose the same benchmarks. The
[`ai-heuresis-*` sweep](2026-09-28-ai-heuresis-branch-sweep.md) then found a
second R15 effect, the shared UF/datatypes engine, and it was not known whether
this is the same effect as `--ee-mode=central` or a new one.

## 2. What was run

Nothing. The inputs are these results files on the host:
`quant-092426-w2-{reference,ai-instdefer,claudedev-dts-idef,ai-jhrlvinst}`,
`quant-092526-w1b-{reference,ee-mode-central,ieval-off}` and
`quant-092826-w3-{reference,r15-share-1,r15-share-2}`. They were read with the
[`gap`](../../reports/gap) parser, through [`arms`](../../reports/arms)'s `load` and `compare`. **gained** and **lost** are taken against
each arm's own reference, as in the register. Comparing sets across the
`d7d5b948c1` and `03e5ee1ebf` references is exact about which benchmarks are
involved and approximate about why. Those two references differ by +2 / −6.

## 3. The set

`quant-07-25`, 6124 benchmarks, 30 s.

## 4. What came back

**R10: two of the three arms are one arm.**

| pair | gained in common | lost in common |
| --- | ---: | ---: |
| `--inst-defer` (+47 / −33) and `--inst-defer --dt-split-relevant` (+44 / −31) | 42 | 30 |
| `--inst-defer` and `--jh-rlv-inst` (+27 / −17) | 12 | 10 |
| all three | 10 | 9 |

The union of the three arms' gains is 63 benchmarks, and of their losses 41.

**R15: the shared UF/datatypes engine rescues mostly what central mode
rescues.**

| arm | gained | of which `--ee-mode=central` (+73 / −19) also gains |
| --- | ---: | ---: |
| `ai-heuresis-r15-claude --ee-share-uf-dt` | 53 | **48** |
| `ai-heuresis-r15-claude --ee-share-uf-dt --ieval=off` | 59 | 49; with `--ieval=off`'s own 20 gains, 54 |

The two arms share 8 of their losses with central mode's 19.

**Across directions: R10 and R15 rescue different benchmarks.** Of the 47
benchmarks `--inst-defer` gains, 23 are also gained by `--ee-mode=central`, 8 by
`--ieval=off` and 19 by `--ee-share-uf-dt --ieval=off`. The two arms share 5 of
their losses.

## 5. What it settled

**Central mode's gain is largely UF–datatype equality sharing.** A branch that
changes only that sharing, within the distributed engine, reproduces 48 of
central mode's 73 rescues. That gives R15's one 🟢 option a candidate mechanism
where it previously had only a size. **`--dt-split-relevant` adds nothing to
`--inst-defer`.** The combined branch decides almost exactly the same
benchmarks. **`--jh-rlv-inst` is a different effect from `--inst-defer`.** It
overlaps them on a third of its gains and about half its losses. **R10 and R15
are close to independent.** About half of `--inst-defer`'s rescues are
benchmarks central mode does not reach. So `--inst-defer --ee-mode=central` is
the first combination in the register with a measured reason to beat both of
its parts.

## 6. What it did not settle

Whether any of these combinations actually add up. That needs a run, and none
has been made. Overlapping gained sets are a necessary condition for a shared
mechanism, not a proof of one. The UF–datatype attribution also needs the
counter S4 asks for.
