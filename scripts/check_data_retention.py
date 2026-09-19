#!/usr/bin/env python3
"""Check public files against docs/maintenance.md's result-retention policy.

Read-only: reads Git's file inventory and working-tree files, writes nothing.
The marked block in .gitignore is the source of truth for reserved basenames.
Content checks catch common raw benchmark blocks and debugger backtraces;
they do not establish that every possible transcript format has been removed.
"""
from fnmatch import fnmatchcase
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
BEGIN = "# BEGIN raw job output"
END = "# END raw job output"
BENCHMARK_BLOCK = re.compile(
    r"^[ \t]*(?:\./)?[^\s`]+\.smt2(?:\.gz)?[ \t]*\r?\n"
    r"(?:[ \t]*\r?\n)*[ \t]*(?:"
    r"(?:sat|unsat|unknown|timeout|error|success|none)\s*$|"
    r"[\w:]+::[\w:]+\s*=|"
    r"\d+(?:\.\d+)?[ \t]+\d+[ \t]*$|"
    r"Command (?:exited|terminated)|(?:cvc5|z3) (?:interrupted|suffered))",
    re.MULTILINE,
)
BACKTRACE = re.compile(r"^#\d+[ \t]+(?:0x[0-9a-fA-F]+\b|[\w:]+\()", re.MULTILINE)


def raw_patterns(root):
    lines = (root / ".gitignore").read_text().splitlines()
    patterns = lines[lines.index(BEGIN) + 1:lines.index(END)]
    if not patterns or any(not p or p.startswith(("#", "!")) or "/" in p for p in patterns):
        raise ValueError("raw-output ignore block must contain only basename patterns")
    return patterns


def violations(root):
    patterns = raw_patterns(root)
    names = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=root
    ).decode().split("\0")
    found = []
    for name in sorted(set(names) - {""}):
        path = root / name
        if not path.is_file():  # Deletions in the working tree need not be staged yet.
            continue
        if any(fnmatchcase(path.name, pattern) for pattern in patterns):
            found.append((name, "reserved raw-output filename"))
            continue
        # Source contains parser examples and synthetic test inputs. Filenames
        # are still checked, and a data file in tests/ has no blanket exemption.
        if path.suffix in {".py", ".sh"}:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if BENCHMARK_BLOCK.search(content) or BACKTRACE.search(content):
            found.append((name, "raw benchmark output or debugger backtrace"))
    return found


def main():
    try:
        found = violations(ROOT)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"retention: could not check public files: {error}", file=sys.stderr)
        return 1
    for name, reason in found:
        print(f"retention: {name}: {reason}", file=sys.stderr)
    if found:
        print("Keep raw job output on the host or in ignored scratch/; "
              "see docs/maintenance.md#result-retention.", file=sys.stderr)
        return 1
    print("retention: no reserved dump names or recognized raw blocks in public files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
