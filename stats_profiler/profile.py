#!/usr/bin/env python3
"""Profile cvc5 --stats-internal benchmark blocks; Python standard library only."""
import argparse
import csv
import fnmatch
import json
import math
import re
import sys
from pathlib import Path


DURATION = re.compile(r"([+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*(ns|us|µs|μs|ms|s|min|h)")
UNITS = {"ns": 1e-9, "us": 1e-6, "µs": 1e-6, "μs": 1e-6,
         "ms": 1e-3, "s": 1, "min": 60, "h": 3600}


def seconds(value):
    """Only unit-bearing durations are timers, never bare numeric counters."""
    match = DURATION.fullmatch(value.strip())
    if not match:
        return None
    result = float(match[1]) * UNITS[match[2]]
    return result if math.isfinite(result) else None


def read_stats(path):
    records, warnings = [], []
    current = None
    with Path(path).open(encoding="utf-8", errors="replace") as stream:
        for number, line in enumerate(stream, 1):
            line = line.strip()
            if not line:
                continue
            # Check assignments first: driver::filename also ends in .smt2.
            if " = " in line:
                key, value = line.split(" = ", 1)
                if current is None:
                    continue
                duration = seconds(value)
                if duration is not None:
                    if key in current["timers"]:
                        warnings.append(f"Line {number}: repeated timer {key} in {current['benchmark']}; last snapshot used.")
                    current["timers"][key] = duration
                continue
            if line.endswith(".smt2") or line.endswith(".smt2.gz"):
                current = {"benchmark": line, "status": "unreported", "timers": {}}
                records.append(current)
            elif current is not None:
                if line in {"sat", "unsat", "unknown"}:
                    current["status"] = line
                elif re.search(r"interrupted|terminated|timed out|exit status 124|non-zero status 124", line, re.I):
                    current["status"] = "timeout"
    if not records:
        raise ValueError("No benchmark blocks found; use the raw stats file, not the -processed summary.")
    names = [r["benchmark"] for r in records]
    if len(set(names)) != len(names):
        warnings.append("Repeated benchmark paths are retained as separate runs (rows are not merged).")
    return records, warnings


def compile_config(config, keys):
    if not isinstance(config, dict):
        raise ValueError("Config must be a JSON object.")
    total = config.get("total", "global::totalTime")
    missing = config.get("missing", "zero")
    if not isinstance(total, str) or not total:
        raise ValueError("total must be a nonempty timer name.")
    if not isinstance(missing, str) or missing not in {"zero", "exclude"}:
        raise ValueError("missing must be zero or exclude.")
    categories = config.get("categories")
    if not isinstance(categories, list) or not categories:
        raise ValueError("categories must be a nonempty list.")
    compiled, warnings, names = [], [], set()
    for category in categories:
        if not isinstance(category, dict):
            raise ValueError("Each category must be an object.")
        name = category.get("name")
        if not isinstance(name, str) or not name or name in names:
            raise ValueError("Category names must be nonempty and unique.")
        names.add(name)
        terms = {}
        for field, sign in (("add", 1), ("subtract", -1)):
            patterns = category.get(field, [])
            if not isinstance(patterns, list) or any(not isinstance(p, str) or not p for p in patterns):
                raise ValueError(f"{name}: {field} must be a list of timer names or globs.")
            matched = set()
            for pattern in patterns:
                found = {k for k in keys if fnmatch.fnmatchcase(k, pattern)}
                if not found:
                    warnings.append(f"{name}: pattern {pattern!r} matched no observed timer.")
                    # Keep absent literal keys so missing-data handling still applies.
                    if not any(c in pattern for c in "*?["):
                        found.add(pattern)
                matched.update(found)
            for key in matched:
                terms[key] = terms.get(key, 0) + sign
        terms = {k: v for k, v in sorted(terms.items()) if v}
        if total in terms:
            raise ValueError(f"{name}: the total timer cannot also be a category term.")
        if not terms:
            warnings.append(f"{name}: no effective timer terms; category contributes zero.")
        compiled.append({"name": name, "terms": terms})
    return {"total": total, "missing": missing, "categories": compiled}, warnings


def analyze(records, config):
    rows = []
    categories = config["categories"]
    for index, record in enumerate(records):
        timers = record["timers"]
        total = timers.get(config["total"])
        missing = sorted({k for c in categories for k in c["terms"] if k not in timers})
        reason = "missing total" if total is None else "zero total" if total == 0 else ""
        if not reason and missing and config["missing"] == "exclude":
            reason = "missing category timers"
        values = [sum(timers.get(k, 0) * v for k, v in c["terms"].items()) for c in categories]
        accounted = sum(values)
        residual = total - accounted if total is not None else None
        rows.append({"id": index + 1, "benchmark": record["benchmark"], "status": record["status"],
                     "total": total, "values": values, "accounted": accounted,
                     "residual": residual, "gap": max(0, residual) if residual is not None else None,
                     "excess": max(0, -residual) if residual is not None else None,
                     "coverage": accounted / total if total else None,
                     "missing": missing, "excluded": reason})
    included = [r for r in rows if not r["excluded"]]
    total = sum(r["total"] for r in included)
    accounted = sum(r["accounted"] for r in included)
    summary = {"runs": len(rows), "included": len(included), "excluded": len(rows) - len(included),
               "total_seconds": total, "accounted_seconds": accounted,
               "coverage": accounted / total if total else None,
               "residual_seconds": total - accounted,
               "gap_seconds": sum(r["gap"] for r in included),
               "excess_seconds": sum(r["excess"] for r in included),
               "negative_category_runs": sum(any(v < 0 for v in r["values"]) for r in included),
               "missing_timer_runs": sum(bool(r["missing"]) for r in rows)}
    return rows, summary


def write_report(output, records, config, warnings, source):
    rows, summary = analyze(records, config)
    output.mkdir(parents=True, exist_ok=True)
    payload = {"source": source, "records": records, "config": config, "warnings": warnings}
    # Raw input strings must never terminate the JSON script element.
    encoded = json.dumps(payload, ensure_ascii=True, allow_nan=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    template = Path(__file__).with_name("report.html").read_text(encoding="utf-8")
    (output / "index.html").write_text(template.replace("__PROFILE_DATA__", encoded), encoding="utf-8")
    (output / "summary.json").write_text(json.dumps({"source": source, "config": config,
        "warnings": warnings, "summary": summary, "benchmarks": rows}, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    with (output / "benchmarks.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["run", "benchmark", "status", "excluded", "total_seconds", "accounted_seconds",
                         "coverage", "residual_seconds", "gap_seconds", "excess_seconds", "missing_timers"]
                        + [c["name"] + " (s)" for c in config["categories"]])
        for row in rows:
            writer.writerow([row[k] for k in ("id", "benchmark", "status", "excluded", "total", "accounted",
                "coverage", "residual", "gap", "excess")] + [";".join(row["missing"])] + row["values"])
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="raw stats-*.txt emitted by a stats job")
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("default.json"))
    parser.add_argument("--output", type=Path, default=Path("stats_profiler/output"))
    parser.add_argument("--list-timers", action="store_true", help="list observed timers and exit")
    parser.add_argument("--benchmarks", type=Path, help="restrict to exact benchmark paths, one per line")
    args = parser.parse_args(argv)
    try:
        records, warnings = read_stats(args.input)
        if args.benchmarks:
            selected = {s.strip() for s in args.benchmarks.read_text().splitlines() if s.strip()}
            absent = selected - {r["benchmark"] for r in records}
            if absent:
                warnings.append(f"{len(absent)} requested benchmark paths were absent from input.")
            records = [r for r in records if r["benchmark"] in selected]
            if not records:
                raise ValueError("Benchmark selection matched no runs.")
        keys = sorted({key for record in records for key in record["timers"]})
        if args.list_timers:
            print("timer\tpresent runs\ttotal seconds")
            for key in keys:
                print(f"{key}\t{sum(key in r['timers'] for r in records)}\t{sum(r['timers'].get(key, 0) for r in records):.9g}")
            return 0
        config, notices = compile_config(json.loads(args.config.read_text()), keys)
        warnings.extend(notices)
        if not any(config["total"] in r["timers"] for r in records):
            raise ValueError(f"Total timer {config['total']!r} was not found in any benchmark.")
        summary = write_report(args.output, records, config, warnings, args.input.name)
        print(f"Report: {args.output / 'index.html'}")
        print(json.dumps(summary, indent=2))
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
        return 0
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    sys.exit(main())
