#!/usr/bin/env python3
"""Run local CI checks, as defined in docs/maintenance.md; no remote jobs."""
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main():
    suites = ["tests", "stats_profiler/tests"]
    guide = (ROOT / "docs/maintenance.md").read_text()
    if (any(name not in guide for name in ("job_launcher/checks", "scripts/check_data_retention.py"))
            or any(f"`{suite}/`" not in guide for suite in suites)):
        sys.exit("check: maintenance.md must describe retention, launcher lint and shared test suites")
    result = subprocess.run([sys.executable, str(ROOT / "scripts/check_data_retention.py")], cwd=ROOT)
    if result.returncode:
        return result.returncode
    result = subprocess.run([str(ROOT / "job_launcher/checks")], cwd=ROOT)
    if result.returncode:
        return result.returncode
    # A child with a tests directory and nothing in it is not a failure, and
    # `unittest discover` finding no test exits 5 from Python 3.12 on.
    suites += [str(path.relative_to(ROOT)) for path in sorted((ROOT / "tools").glob("*/tests"))
               if path.is_dir() and any(path.glob("test_*.py"))]
    for path in suites:
        print(f"check: {path}", flush=True)
        # Separate discovery processes let isolated children use their own module names.
        result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", path, "-v"], cwd=ROOT)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
