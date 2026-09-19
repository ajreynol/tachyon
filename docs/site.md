# The published reports

The measurements recorded in this repository are published as a small static
site: **<https://ajreynol.github.io/tachyon/>**. The site index introduces
tachyon and lists the research projects; each project that publishes gets a
report page of its own, built from what it tracks — its measurements where it
has them, and its reasoning where it does not.

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
| `heuresis/queue.html` | every section of [`todo.md`](../tools/heuresis/docs/todo.md), and the pull-request record in `progress.md` |
| [`elaphros/`](../tools/elaphros/report) | the ranked queue and planning work in [`todo.md`](../tools/elaphros/docs/todo.md), the register in [`directions.md`](../tools/elaphros/docs/directions.md), the record in [`progress.md`](../tools/elaphros/docs/progress.md), and the evidence index in [`ledger/README.md`](../tools/elaphros/ledger/README.md) |

**A project with nothing measured still has something to publish.** What a
research project produces before its first measurement is its *reasoning*:
which mechanisms it thinks are worth investigating, in what order, on what
source evidence, and what it refuses to claim. Elaphros publishes exactly that
and no figure beyond it — its headline tile reads **0 measurements**, because
that is what the documents say. A planning page that implied otherwise would be
the one failure this site is built to prevent.

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
  document that has stopped stating its own protocol;
- a document that has lost the section or the table a page is built from, and
  a queue that ranks a direction its own register does not define.

**That last one is the rule the planning pages rest on.** They restate a
document, so the failure they are exposed to is the document moving underneath
them — a section renamed, a table dropped, a status written in a word the
builder cannot read. Each of those stops the build. A page that is a copy of a
document nobody compares it to is drift that has not surfaced yet.

## How a project publishes

`scripts/build_site.py` knows nothing about any project's measurements. A
project publishes by providing an executable `tools/<project>/report` that

1. accepts `--out DIR` (where to write), `--base-url URL` (where that directory
   will be served), `--repo-url URL` (what links to the evidence should point
   at) and `--site-href PATH` (a relative link back to the site index);
2. writes its pages under `--out`, rewritten whole; and
3. prints one JSON object on stdout with `name` (the directory name), `title`,
   `question`, `summary`, `href` (the page it wrote, relative to `--out`),
   `updated` (the date of the newest thing the page rests on — a measurement
   where there is one, otherwise the newest record in the project's ledger),
   `headline` (a short list of `{label, value, note}` figures for the index
   card), and optionally `dated`: **one word saying what `updated` is the date
   of**, which the index prints beside it.

`dated` defaults to *updated*, and a project that has measured something says
`measured`. It exists because the index used to print *measured* for every
project, which was a claim the index was making on a project's behalf and which
stopped being true the first time a project published before measuring
anything. Elaphros says `recorded`, because what its date names is a source
audit.

Anything else it prints goes to stderr. A project without such a file is listed
on the index and not published; deleting a project directory removes its report
and leaves the rest of the site as it was.

**A project may write more pages than the one it names.** `href` is the page
the index card links to; anything else it writes under `--out` is its own, and
must be reachable from that page. Heuresis writes two — the gap report and the
queue beside it.

The page templates — [`scripts/site.html`](../scripts/site.html) for the index,
[`tools/heuresis/report.html`](../tools/heuresis/report.html) and
[`queue.html`](../tools/heuresis/queue.html) for heuresis, and
[`tools/elaphros/report.html`](../tools/elaphros/report.html) for elaphros — are
maintained by hand, with the builders substituting the marked placeholders. The
gap report is one HTML file with its data embedded: it works offline,
`#<comparison>` links to a particular recorded comparison, and the CSV beside it
is the same rows the page draws. The queue and planning pages carry no script at
all; their tables are rendered when the site is built.

## Deployment

[`.github/workflows/reports.yml`](../.github/workflows/reports.yml) builds the
site on every push and pull request and deploys it from `main`. The build job
runs the index suite and every project's builder suite first, so a broken
builder fails before anything is published; it discovers those suites the way
`scripts/check.py` does and names no project, so adding one changes nothing in
the workflow. No branch holds the built site.

Pages itself was enabled once, by a person, with Actions as its source:

```bash
gh api -X POST repos/ajreynol/tachyon/pages -f build_type=workflow
```

The workflow does ask `actions/configure-pages` to create the site
(`enablement: true`), but its token is not allowed to — `Resource not accessible
by integration` — so the first deployments failed until that setting was made on
2026-09-18. A fork wanting its own copy of the site needs the same one-time
setting, from that command or from the repository's Pages settings.

A pull request builds the site and stops there — the artifact it uploads is not
deployed. To see a change before it lands, build locally and open `site/`.

## What the site does not do

It publishes what a project has measured and what it has decided to do next.
It does not republish the documents themselves: charters, ledger entries,
research directions and guides stay in Git and are linked from the pages rather
than rendered into them.

It is not a claim of correctness for any measurement, and its pages carry the
same evidence limits as the records behind them: single runs, one host,
recorded revisions and options, raw artifacts that live on the execution host.
**A published plan claims even less than a published measurement** — a ranked
direction is an argument about what to do, not evidence that doing it would
help, and where a ranking is the maintainer's rather than an agent's the page
says so and keeps the two apart. Inspect a rendered page before citing it.
