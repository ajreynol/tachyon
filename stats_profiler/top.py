#!/usr/bin/env python3
"""Rank the benchmarks worth looking at, per timer; Python standard library only."""
import argparse
import json
import re
import sys
from pathlib import Path


SOLVED = {"sat", "unsat"}
# The two line shapes a results file has besides the benchmark path, spelled as
# the gap reading spells them so the two tools cannot drift apart.
TIME = re.compile(r"([0-9]+(?:\.[0-9]+)?)(?: ([0-9]+))?")
TOKEN = re.compile(r"[a-z][a-z0-9-]*")


def read_results(path, timeout):
    """-> benchmark -> (result, user seconds), from a run-dev results file.

    The format is the drivers': a path line ending in .smt2, the wrapper's
    result token (absent when it was killed), then "<user-seconds> <max-rss>".
    Re-implemented rather than imported: a research project's scripts are its
    own island, and this tool must keep working if one of them is deleted.
    """
    out, benchmark, result, ignored = {}, None, None, 0
    for line in Path(path).read_text(errors="replace").splitlines():
        line = line.strip()
        if line.endswith(".smt2") or line.endswith(".smt2.gz"):
            benchmark, result = line, None
            continue
        if benchmark is None:
            ignored += 1
            continue
        if TIME.fullmatch(line):
            seconds = float(TIME.fullmatch(line)[1])
            # A solved run at or past the limit is a timeout, as the gap reading has it.
            out[benchmark] = ("timeout" if not result or seconds >= timeout else result, seconds)
            benchmark = None
        elif TOKEN.fullmatch(line):
            result = line
        elif "interrupted" in line or "terminated" in line:
            result = "timeout"
        else:
            ignored += 1
    return out, ignored


def losses(reference, run, factor, floor, timeout):
    """Benchmarks where the run loses to the reference, by this project's gap-set rule:
    unsolved where the reference solved, or both solved and at least `factor` times
    slower with at least `floor` seconds spent."""
    out = {}
    for benchmark in set(reference) & set(run):
        reference_result, reference_seconds = reference[benchmark]
        result, seconds = run[benchmark]
        if reference_result not in SOLVED:
            continue
        if result not in SOLVED:
            out[benchmark] = (reference_seconds, None)
        elif seconds >= floor and seconds >= factor * max(reference_seconds, 1e-3):
            out[benchmark] = (reference_seconds, seconds)
    return out


def rank(rows, index, keep, count):
    """The `count` runs with the most seconds in timer `index`, among `keep`."""
    usable = [row for row in rows if not row["excluded"] and (keep is None or row["benchmark"] in keep)]
    usable.sort(key=lambda row: row["values"][index], reverse=True)
    return usable[:count]


def render(names, rows, keep, count, source, reference_label, run_label, rule, notes):
    blocks = ["# Benchmarks to look at, per timer",
              f"Source: `{source}`. Top {count} per timer.",
              "## The measure",
              "For a benchmark `b` and timer `t`, the rank key is",
              "```\nseconds_t(b) = share_t(b) x totalTime(b)\n```",
              "which is criterion (A) times criterion (B): `share_t(b)` is the fraction of "
              "that run's `global::totalTime` spent in `t`, and `totalTime(b)` is how long "
              "cvc5 took overall. Their product is just the timer's own seconds, so a large "
              "share of a trivial benchmark and a long benchmark that barely touches the "
              "timer both rank low. Only a benchmark that is *both* long and dominated by "
              "the timer ranks high."]
    if keep is None:
        blocks.append("Criterion (C) is **not applied**: no baseline results file was given, so "
                      "the tables rank every included run and say nothing about z3.")
    else:
        blocks.append(f"Criterion (C) is a **filter, not a third factor**: a benchmark is listed "
                      f"only if it is in the loss set of `{run_label}` against `{reference_label}` "
                      f"({rule}), which is this project's standard gap-set rule. The z3 ratio is "
                      f"unbounded -- z3 at 0.01 s against a cvc5 timeout is 3000x -- so multiplying "
                      f"by it would swamp (A) and (B) and fill the list with benchmarks that are "
                      f"quick for cvc5 and quicker still for z3, which is the opposite of what was "
                      f"asked. As a filter every row is a benchmark cvc5 loses on, and the ordering "
                      f"within them stays the attributable time. {len(keep):,} benchmarks qualify.")
    blocks.append("(A) and (B) come from cvc5's internal `global::totalTime` in the statistics run; "
                  "(C) compares the wrapper's user seconds in the paired solve runs. The two are "
                  "never mixed inside one ratio. Ranking by seconds means a run's timers are "
                  "compared only with its own total.")
    if notes:
        blocks.append("\n".join(f"- {note}" for note in notes))
    for index, name in enumerate(names):
        top = rank(rows, index, keep, count)
        blocks.append(f"## {index + 1}. `{name}`")
        if not top:
            blocks.append("No qualifying benchmark.")
            continue
        head = ["#", "benchmark", f"{name} (s)", "share of total", "cvc5 total (s)", "result"]
        if keep is not None:
            head += [f"{reference_label} (s)", "ratio"]
        table = ["| " + " | ".join(head) + " |", "|" + "|".join(["---"] * len(head)) + "|"]
        for place, row in enumerate(top, 1):
            cells = [str(place), f"`{row['benchmark']}`", f"{row['values'][index]:.2f}",
                     f"{row['values'][index] / row['total'] * 100:.1f}%", f"{row['total']:.2f}", row["status"]]
            if keep is not None:
                reference_seconds, seconds = keep[row["benchmark"]]
                cells += [f"{reference_seconds:.2f}",
                          "unsolved" if seconds is None else f"{seconds / max(reference_seconds, 1e-3):.0f}x"]
            table.append("| " + " | ".join(cells) + " |")
        blocks.append("\n".join(table))
    return "\n\n".join(blocks) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary", type=Path, help="summary.json written by profile.py")
    parser.add_argument("--results", type=Path, help="the cvc5 run's results file, for criterion (C)")
    parser.add_argument("--baseline", type=Path, help="the reference (z3) results file, for criterion (C)")
    parser.add_argument("--output", type=Path, help="where to write the log (default: top-benchmarks.md "
                                                    "beside the summary)")
    parser.add_argument("--count", type=int, default=10, help="rows per timer (default: 10)")
    parser.add_argument("--factor", type=float, default=10.0, help="slowdown that counts as a loss (default: 10)")
    parser.add_argument("--floor", type=float, default=1.0, help="seconds below which a slowdown is noise (default: 1)")
    parser.add_argument("--timeout", type=float, default=30.0, help="the job's per-benchmark limit (default: 30)")
    args = parser.parse_args(argv)
    try:
        if args.count < 1:
            raise ValueError("--count must be at least 1.")
        if bool(args.results) != bool(args.baseline):
            raise ValueError("--results and --baseline go together: criterion (C) needs both runs.")
        report = json.loads(args.summary.read_text())
        names = [category["name"] for category in report["config"]["categories"]]
        rows = report["benchmarks"]
        keep, notes = None, []
        reference_label = run_label = ""
        if args.baseline:
            reference, ignored = read_results(args.baseline, args.timeout)
            run, run_ignored = read_results(args.results, args.timeout)
            reference_label, run_label = args.baseline.stem, args.results.stem
            keep = losses(reference, run, args.factor, args.floor, args.timeout)
            overlap = {row["benchmark"] for row in rows} & set(run)
            if not overlap:
                raise ValueError("No benchmark path in the results files matches the statistics file; "
                                 "these are not the same set, or the paths are written differently.")
            notes.append(f"Paths: {len(overlap):,} of {len(rows):,} statistics benchmarks matched the "
                         f"results files ({len(reference):,} in the baseline, {len(run):,} in the run).")
            if ignored or run_ignored:
                notes.append(f"Unparsed results lines ignored: {ignored:,} baseline, {run_ignored:,} run.")
            notes.append("The statistics run and the solve runs are separate executions of the same "
                         "configuration, so loss-set membership is measured on a different execution "
                         "than the timer values it filters.")
        rule = f"unsolved where the baseline solved, or >= {args.factor:g}x slower with >= {args.floor:g} s spent"
        path = args.output or args.summary.parent / "top-benchmarks.md"
        path.write_text(render(names, rows, keep, args.count, report["source"],
                               reference_label, run_label, rule, notes))
        print(path)
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    sys.exit(main())
