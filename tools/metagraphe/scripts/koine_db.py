#!/usr/bin/env python3
"""Run pinned koine append/closure checks with metagraphe's local validation."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from check_rewrite_db import DATABASE, ROOT, validate
from render_rewrite_db import OUTPUT, render


LOCK = DATABASE.parent / "koine.lock"


def run_pinned(checkout, program, arguments):
    if not checkout:
        raise ValueError("set KOINE or --koine to a Git checkout containing the pinned revision")
    revision = LOCK.read_text().strip()
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("koine.lock must contain a full commit hash")
    result = subprocess.run(["git", "-C", str(checkout), "show",
                             f"{revision}:bug_db_manager/{program}"],
                            capture_output=True, text=True)
    if result.returncode:
        raise ValueError(f"cannot read pinned {program}: {result.stderr.strip()}")
    # These two upstream programs are standalone. Never execute an installed
    # command or a modified source file from the supplied checkout.
    with tempfile.TemporaryDirectory(prefix="metagraphe-koine-") as directory:
        script = Path(directory) / program
        script.write_text(result.stdout, encoding="utf-8")
        run = subprocess.run([sys.executable, str(script), *arguments], cwd=ROOT,
                             stderr=subprocess.PIPE, text=True)
        # Koine reports a disagreement with an existing record on stderr and
        # never writes it down, so a launcher that drops the stream loses the
        # only copy. Echo it where it was going, and hand it back to be kept.
        sys.stderr.write(run.stderr)
        sys.stderr.flush()
        return run.returncode, run.stderr


def retain(diagnostics, destination):
    """Keep koine's per-record conflict and reopen lines beside the filing."""
    kept = [line for line in diagnostics.splitlines()
            if line.startswith(("-- conflict:", "-- reopen candidate:"))]
    if not kept:
        return None
    destination.write_text("\n".join(kept) + "\n", encoding="utf-8")
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--koine", type=Path, default=os.environ.get("KOINE"),
                        help="existing koine Git checkout (default: KOINE environment variable)")
    commands = parser.add_subparsers(dest="command", required=True)
    append = commands.add_parser("append", help="validate, use koine's locked append, and regenerate the view")
    append.add_argument("input", type=Path)
    append.add_argument("--dry-run", action="store_true")
    append.add_argument("--conflicts", type=Path,
                        help="where to keep koine's conflict and reopen lines "
                             "(default: beside the filing, as <input>.conflicts.txt)")
    check = commands.add_parser("check-closure", help="validate metadata and check only closure fields changed")
    check.add_argument("--against", default="HEAD", help="committed pre-closure revision")
    check.add_argument("--amended", action="store_true", help="explicitly allow amending a prior closure")
    args = parser.parse_args(argv)
    try:
        validate(json.loads(DATABASE.read_text(encoding="utf-8")))
        if args.command == "append":
            validate(json.loads(args.input.read_text(encoding="utf-8")), filing=True)
            command = [str(args.input.resolve()), str(DATABASE), "--records", "rewrites"]
            if args.dry_run:
                command.append("--dry-run")
            result, diagnostics = run_pinned(args.koine, "koine_append_db", command)
            if result or args.dry_run:
                return result
            # Both of these follow a database koine has already written, so
            # neither is a reason to report the filing as failed.
            try:
                kept = retain(diagnostics, args.conflicts
                              or args.input.with_name(args.input.name + ".conflicts.txt"))
                if kept:
                    print(f"-- koine's conflict and reopen lines are kept in {kept}")
            except OSError as exc:
                print(f"rewrite database: appended, but the conflict lines were not kept: {exc}",
                      file=sys.stderr)
            try:
                OUTPUT.write_text(render(json.loads(DATABASE.read_text(encoding="utf-8"))), encoding="utf-8")
            except (OSError, ValueError) as exc:
                # A stale view to regenerate rather than a filing to retry.
                print(f"rewrite database: appended, but the view is stale: {exc}", file=sys.stderr)
                return 1
            return 0
        command = [str(DATABASE), "--against", args.against,
                   "--also", "awaiting_landing", "--also", "replacement_id"]
        if args.amended:
            command.append("--amended")
        return run_pinned(args.koine, "koine_check_db", command)[0]
    except (OSError, ValueError) as exc:
        print(f"rewrite database: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
