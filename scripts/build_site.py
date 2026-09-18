#!/usr/bin/env python3
"""Build the published report site from what the research projects have recorded.

    python3 scripts/build_site.py [--out site] [--base-url URL] [--repo-url URL]

The site index is tachyon's own: the front page's research projects, the limits
of the evidence, and a card for every project that publishes a report. It knows
nothing about any project's measurements. A project publishes by providing an
executable `tools/<project>/report` that writes a report into `--out` and prints
one JSON object describing it (see docs/site.md). Projects without one are
listed and not published, and deleting a project directory removes its report
from the site and nothing else.

Refusals, rather than a site that quietly says less than it appears to: a report
that does not honour the contract, a published report the front page does not
advertise, and a front page whose research-project table cannot be read.

Writes `index.html` and `.nojekyll` under --out, rewritten whole. Python
standard library only; no network access.
"""
import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = Path(__file__).resolve().parent / "site.html"
DEFAULT_REPO = "https://github.com/ajreynol/tachyon"
DEFAULT_URL = "https://ajreynol.github.io/tachyon"
CONTRACT = ("name", "title", "question", "summary", "href", "updated", "headline")
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def projects(readme, repo_url):
    """The research projects the front page advertises: name, link and question."""
    section = re.search(r"^## Research projects\s*$(.*?)^## ", readme.read_text(), re.MULTILINE | re.DOTALL)
    if not section:
        raise ValueError(f"{readme.name}: no '## Research projects' section to read the project list from")
    found = []
    for line in section.group(1).splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 2 or set(cells[0]) <= set("- ") or cells[0] == "project":
            continue
        link = LINK.fullmatch(cells[0])
        if not link:
            raise ValueError(f"{readme.name}: research project '{cells[0]}' is not a link to its directory")
        found.append({"name": link.group(1), "href": f"{repo_url}/blob/main/{link.group(2)}",
                      "question": LINK.sub(r"\1", cells[1])})
    if not found:
        raise ValueError(f"{readme.name}: the research projects table has no rows")
    return found


def run_report(builder, out, base_url, repo_url):
    """Run one project's report builder and check what it says it published."""
    name = builder.parent.name
    destination = out / name
    result = subprocess.run(
        [sys.executable, str(builder), "--out", str(destination), "--base-url", f"{base_url}/{name}",
         "--repo-url", repo_url, "--site-href", "../index.html"],
        cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        raise ValueError(f"{name}: its report builder failed:\n{result.stderr.strip() or result.stdout.strip()}")
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError:
        raise ValueError(f"{name}: its report builder did not print a JSON description on stdout") from None
    missing = [key for key in CONTRACT if key not in report]
    if missing:
        raise ValueError(f"{name}: its report description is missing {', '.join(missing)}")
    if report["name"] != name:
        raise ValueError(f"{name}: its report calls itself {report['name']!r}")
    if not (destination / report["href"]).is_file():
        raise ValueError(f"{name}: its report names {report['href']}, which it did not write")
    report["path"] = f"{name}/{report['href']}"
    return report


def card(report):
    esc = html.escape
    tiles = "".join(
        f'<div class="tile"><span>{esc(tile["label"])}</span><strong>{esc(str(tile["value"]))}</strong>'
        f'<span>{esc(tile.get("note", ""))}</span></div>'
        for tile in report["headline"])
    return (f'<section>\n<p class="eyebrow">{esc(report["title"])} · measured {esc(report["updated"])}</p>\n'
            f'<h2>{esc(report["question"])}</h2>\n<p>{esc(report["summary"])}</p>\n'
            f'<div class="tiles">{tiles}</div>\n'
            f'<p><a class="button" href="{esc(report["path"])}">Explore the report →</a></p>\n</section>')


def rows(project_list, published):
    esc = html.escape
    cells = []
    for project in project_list:
        report = published.get(project["name"])
        state = (f'<a href="{esc(report["path"])}">the report</a>, measured {esc(report["updated"])}'
                 if report else "charter and search register only")
        cells.append(f'<tr><td><a href="{esc(project["href"])}">{esc(project["name"])}</a></td>'
                     f'<td>{esc(project["question"])}</td><td>{state}</td></tr>')
    return "\n".join(cells)


def build(out, base_url, repo_url):
    out = out.resolve()
    if out == ROOT or out in ROOT.parents:
        raise ValueError("the site output must be its own directory")
    base_url = base_url.rstrip("/")
    project_list = projects(ROOT / "README.md", repo_url)
    known = {project["name"] for project in project_list}

    out.mkdir(parents=True, exist_ok=True)
    published = {}
    for builder in sorted(ROOT.glob("tools/*/report")):
        if not builder.is_file():
            continue
        report = run_report(builder, out, base_url, repo_url)
        if report["name"] not in known:
            raise ValueError(f"{report['name']}: publishes a report but the front page does not list it; "
                             "advertise it in README.md or do not publish it")
        published[report["name"]] = report

    footer = " ".join(
        f'<a href="{html.escape(href)}">{html.escape(text)}</a>' for text, href in (
            ("Repository", repo_url),
            ("Documentation", f"{repo_url}/blob/main/docs/README.md"),
            ("How this site is built", f"{repo_url}/blob/main/docs/site.md"),
            ("Maintenance", f"{repo_url}/blob/main/docs/maintenance.md"),
            ("Ecosystem policy", "https://github.com/ajreynol/kanon/blob/main/docs/policy.md")))

    body = TEMPLATE.read_text()
    replacements = {
        "__TITLE__": html.escape("Tachyon reports — measured cvc5 performance evidence"),
        "__DESCRIPTION__": html.escape(
            "Published measurements from tachyon's cvc5 performance research: the benchmarks where cvc5 "
            "loses time, each list tied to the recorded experiment that produced it."),
        "__CANONICAL__": html.escape(f"{base_url}/"),
        "__REPO_URL__": html.escape(repo_url),
        "__DOCS_URL__": html.escape(f"{repo_url}/blob/main/docs/README.md"),
        "__REPORT_CARDS__": "\n".join(card(published[name]) for name in sorted(published)),
        "__PROJECT_ROWS__": rows(project_list, published),
        "__FOOTER__": footer,
    }
    for token, value in replacements.items():
        if token not in body:
            raise ValueError(f"{TEMPLATE.name}: the template no longer has {token}")
        body = body.replace(token, value)

    # GitHub Pages serves the files as they are built here; Jekyll must not run.
    (out / ".nojekyll").write_text("")
    (out / "index.html").write_text(body, encoding="utf-8")
    return published


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=ROOT / "site")
    parser.add_argument("--base-url", default=DEFAULT_URL, help="where the site will be published")
    parser.add_argument("--repo-url", default=DEFAULT_REPO, help="repository the evidence links point at")
    args = parser.parse_args()
    try:
        published = build(args.out, args.base_url, args.repo_url)
    except (OSError, ValueError) as error:
        parser.exit(1, f"build_site: {error}\n")
    names = ", ".join(sorted(published)) or "no project reports"
    print(f"build_site: {names} -> {args.out.resolve() / 'index.html'}")
    print(f"after deployment: {args.base_url.rstrip('/')}/")


if __name__ == "__main__":
    main()
