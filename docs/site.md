# The published reports

The measurements recorded in this repository are published as a small static
site: **<https://ajreynol.github.io/tachyon/>**. The site index introduces
tachyon and lists the research projects; each project that has recorded
measurements gets a report page of its own, built from the evidence it tracks.

```bash
python3 scripts/build_site.py                    # writes site/, which Git ignores
python3 -m http.server -d site 8000              # then open http://localhost:8000/
```

The build takes a second, needs Python 3.9+ and no dependencies, and reads only
this checkout — no host, no solver, no network. `site/` is rewritten whole every
time; nothing there is edited by hand. Add `--out DIR` to build elsewhere, and
`--base-url URL` when the site will be served from somewhere other than its
usual address.

## What it publishes

| page | built from |
| --- | --- |
| the index | the [front page](../README.md)'s research-project table, and each project's report description |
| [`heuresis/`](../tools/heuresis/report) | the gap lists retained under `tools/heuresis/ledger/data/`, the ledger entries that cite them, and the protocol and history tables of [`progress.md`](../tools/heuresis/docs/progress.md) |

**No figure on the site is typed into it.** Each number is either read from a
tracked document — the set, the timeout, the thresholds, the history rows — or
computed from a retained gap list while the page is built. That is what keeps
the site inside the rule that the ledger is the only place a number enters a
research project: changing the site cannot change a measurement, and a
measurement that changes the documents changes the site at the next build.

The builders refuse rather than publish something weaker than it looks:

- a gap list no ledger entry cites, or one with a malformed or duplicated row;
- a project whose report does not honour the contract below, or which names a
  page it did not write;
- a published report the front page does not advertise;
- a front page whose research-project table cannot be read, or a project
  document that has stopped stating its own protocol.

## How a project publishes

`scripts/build_site.py` knows nothing about any project's measurements. A
project publishes by providing an executable `tools/<project>/report` that

1. accepts `--out DIR` (where to write), `--base-url URL` (where that directory
   will be served), `--repo-url URL` (what links to the evidence should point
   at) and `--site-href PATH` (a relative link back to the site index);
2. writes its pages under `--out`, rewritten whole; and
3. prints one JSON object on stdout with `name` (the directory name), `title`,
   `question`, `summary`, `href` (the page it wrote, relative to `--out`),
   `updated` (the date of the newest measurement) and `headline` (a short list
   of `{label, value, note}` figures for the index card).

Anything else it prints goes to stderr. A project without such a file is listed
on the index and not published; deleting a project directory removes its report
and leaves the rest of the site as it was.

The two page templates — [`scripts/site.html`](../scripts/site.html) for the
index and [`tools/heuresis/report.html`](../tools/heuresis/report.html) for the
gap report — are maintained by hand, with the builders substituting the marked
placeholders. The report page is one HTML file with its data embedded: it works
offline, `#<comparison>` links to a particular recorded comparison, and the CSV
beside it is the same rows the page draws.

## Deployment

[`.github/workflows/reports.yml`](../.github/workflows/reports.yml) builds the
site on every push and pull request and deploys it from `main`. The build job
runs the two builder test suites first, so a broken builder fails before
anything is published. `actions/configure-pages` enables GitHub Pages with
Actions as the source on the first successful deployment from `main`; no branch
holds the built site.

A pull request builds the site and stops there — the artifact it uploads is not
deployed. To see a change before it lands, build locally and open `site/`.

## What the site does not do

It publishes measurements, not documents: charters, ledger entries, research
directions and guides stay in Git and are linked from the pages rather than
rendered into them. It is not a claim of correctness for any measurement, and
its pages carry the same evidence limits as the records behind them: single
runs, one host, recorded revisions and options, raw artifacts that live on the
execution host. Inspect a rendered page before citing it.
