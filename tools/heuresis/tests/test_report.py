"""Report-builder cases on small synthetic trees; no solver, host or network."""
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPO = "https://example.invalid/repo"
SCRIPT = ROOT / "reports/build"
SPEC = importlib.util.spec_from_loader("report", importlib.machinery.SourceFileLoader("report", str(SCRIPT)))
report = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(report)

PROGRESS = """# progress

## The protocol

| | |
| --- | --- |
| set | `demo-set`, **12 benchmarks**, derived; see [`README.md`](../README.md) |
| timeout | 30 s wall |
| reading | [`gap`](../gap) with its defaults: factor 10, floor 1 s |

## The history

| date | config | PAR2 | ledger |
| --- | --- | ---: | --- |
| 2026-01-01 | **best** | 100.5 | [example](../ledger/2026-01-01-example.md) † |

† a note about `the proxy`, with **emphasis**.

### What the history says so far

Nothing has moved yet.

## Noise

Not part of the history.
"""

ENTRY = """# 2026-01-01 — an example experiment

## 2. What was run

```
solve_dir_rec_par_cvc5 -t 30 cvc5 cvc5_solve.sh demo-010126-arm -q --no-cbqi
# cvc5: git abc1234 on branch main
```

The gap list is [`data/gapset-arm-vs-ref-010126.txt`](data/gapset-arm-vs-ref-010126.txt).
"""

GAPSET = "./a/one.smt2 0.10 2.50\n./a/two.smt2 0.20 timeout\n./b/three.smt2 1.00 30.00\n"


class ReadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def gapset(self, text):
        path = self.root / "gapset-arm-vs-ref.txt"
        path.write_text(text)
        return path

    def test_rows_lose_the_leading_dot_and_keep_the_unsolved_status(self):
        rows = report.read_gapset(self.gapset(GAPSET))
        self.assertEqual(rows, [("a/one.smt2", 0.10, 2.50), ("a/two.smt2", 0.20, None), ("b/three.smt2", 1.00, 30.0)])

    def test_malformed_lists_are_refused(self):
        for text in ["", "./a.smt2 0.1\n", "./a.smt2 0.1 2.0 3.0\n", "./a.smt2 fast 2.0\n",
                     "./a.smt2 -1 2.0\n", "./a.smt2 0.1 2.0\n./a.smt2 0.2 3.0\n"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                report.read_gapset(self.gapset(text))

    def test_summary_counts_and_median_come_from_the_rows(self):
        summary = report.summarize(report.read_gapset(self.gapset(GAPSET)))
        self.assertEqual((summary["gap"], summary["unsolved"], summary["slower"]), (3, 1, 2))
        self.assertEqual(summary["median"], 25.0)
        self.assertEqual(summary["widest"], 30.0)


class DocumentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.progress = self.root / "progress.md"
        self.progress.write_text(PROGRESS)

    def read(self):
        return report.progress(self.progress, "https://example.invalid/repo", "docs/progress.md")

    def test_the_protocol_and_history_are_read_from_the_document(self):
        protocol, history = self.read()
        self.assertEqual(protocol, {"name": "demo-set", "size": 12, "timeout": 30.0, "factor": 10.0, "floor": 1.0})
        self.assertEqual(history["columns"], ["date", "config", "PAR2", "ledger"])
        self.assertEqual(history["rows"][0][:3], ["2026-01-01", "best", "100.5"])
        self.assertEqual(history["rows"][0][3],
                         [{"text": "example", "href": "https://example.invalid/repo/blob/main/ledger/2026-01-01-example.md"},
                          " †"])

    def test_the_notes_under_the_table_are_kept_and_the_next_section_is_not(self):
        _, history = self.read()
        self.assertEqual(history["notes"][1], {"heading": "What the history says so far"})
        self.assertIn("<strong>emphasis</strong>", history["notes"][0]["paragraph"])
        self.assertIn("<code>the proxy</code>", history["notes"][0]["paragraph"])
        self.assertNotIn("Not part of the history", json.dumps(history))

    def test_a_document_that_stops_stating_the_protocol_is_refused(self):
        self.progress.write_text(PROGRESS.replace("**12 benchmarks**", "some benchmarks"))
        with self.assertRaises(ValueError):
            self.read()

    def test_a_document_with_no_history_table_is_refused(self):
        self.progress.write_text(re.sub(r"^\|.*$", "", PROGRESS, flags=re.MULTILINE))
        with self.assertRaises(ValueError):
            self.read()

    def test_markup_escapes_before_it_adds_tags(self):
        rendered = report.markup("a <script> and [a link](../x.md)", "https://example.invalid/repo", "docs/progress.md")
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn('<a href="https://example.invalid/repo/blob/main/x.md">a link</a>', rendered)


TODO = """# demo queue

## Short-term goals

| # | short-term goal | blocked on | closed when |
| --- | --- | --- | --- |
| ✅ S1 | a finished thing | — | **Closed.** |
| S2 | an unfinished thing | nothing | it is measured |

## AI-agent priorities

The agent's own ordering.

| rank | research direction | effort | next possible step |
| ---: | --- | --- | --- |
| 1 | [R1 — a direction](directions.md#r1--a-direction) | 🟩 Low Risk | count something |

## Human-maintainer priorities

The maintainer's, kept separate.

| rank | research direction | effort | next possible step | human rationale |
| ---: | --- | --- | --- | --- |
| 1 | [R1 — a direction](directions.md#r1--a-direction) | 🟩 Low Risk | count something | |

## Branch maintenance

| recommendation | branch | directions | behind / ahead | reason or trigger |
| --- | --- | --- | ---: | --- |
| ✅ No base action | `demo` | R1 | 0 / 0 | nothing to do |
"""

DIRECTIONS = """# demo directions

## R1 — A direction: with a subtitle

**Effort.** 🟩 Low Risk / 🟩 High Gain — because it is small.

## R2 — Another direction

**Effort.** 🟥 High Risk / 🟨 Medium Gain — because it is not.
"""

PULL_REQUESTS = """
## Pull requests to cvc5 main

| PR | direction | what it changes | landed | effect on this table |
| --- | --- | --- | --- | --- |
| *(none yet)* | | | | |
"""


class BuildTests(unittest.TestCase):
    """A whole report, built from a synthetic project tree and from this one."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "reports/data").mkdir(parents=True)
        (self.root / "docs/ledger").mkdir(parents=True)
        (self.root / "docs/ledger/2026-01-01-example.md").write_text(ENTRY)
        (self.root / "reports/data/gapset-arm-vs-ref-010126.txt").write_text(GAPSET)
        (self.root / "docs/progress.md").write_text(PROGRESS + PULL_REQUESTS)
        (self.root / "docs/todo.md").write_text(TODO)
        (self.root / "docs/directions.md").write_text(DIRECTIONS)
        self.real, report.ROOT = report.ROOT, self.root
        self.real_here, report.HERE = report.HERE, self.root / "reports"
        self.addCleanup(setattr, report, "HERE", self.real_here)
        self.addCleanup(setattr, report, "ROOT", self.real)

    def build(self, **kwargs):
        options = {"out": self.root / "out", "base_url": "https://example.invalid/site/heuresis",
                   "repo_url": "https://example.invalid/repo"}
        options.update(kwargs)
        return report.build(**options)

    def data(self, out):
        page = (out / "index.html").read_text()
        island = re.search(r'<script id="data" type="application/json">(.*?)</script>', page, re.DOTALL)
        return json.loads(island.group(1).replace("<\\/", "</")), page

    def test_a_report_describes_itself_and_writes_what_it_names(self):
        out = self.root / "out"
        summary = self.build()
        self.assertEqual(summary["name"], "heuresis")
        self.assertEqual(summary["updated"], "2026-01-01")
        self.assertEqual([(tile["label"], tile["value"]) for tile in summary["headline"]],
                         [("gap set", "3"), ("cvc5 unsolved, z3 solved", "1"),
                          ("both solved, cvc5 slower", "2"),
                          # the pair both research projects put on the index card
                          ("research directions", "2"), ("ranked in the queue", "1")])
        self.assertTrue((out / summary["href"]).is_file())
        data, page = self.data(out)
        comparison = data["comparisons"][0]
        self.assertEqual(comparison["id"], "arm-vs-ref-010126")
        self.assertEqual(comparison["arm"], {"job": "arm", "options": "-q --no-cbqi", "revision": "abc1234"})
        self.assertEqual(comparison["ledger"]["text"], "2026-01-01-example.md")
        self.assertTrue((out / comparison["csv"]).is_file())
        self.assertNotIn("__REPORT_DATA__", page)
        # A JSON island ends at the first "</": the payload must not contain one.
        self.assertNotIn("</", page.split('type="application/json">')[1].split("</script>")[0])

    def test_the_csv_carries_every_row_with_its_status(self):
        out = self.root / "out"
        self.build()
        lines = (out / "data/arm-vs-ref-010126.csv").read_text().splitlines()
        self.assertEqual(lines[0], "benchmark,reference_seconds,cvc5_seconds,cvc5_status,slowdown")
        self.assertEqual(lines[1], "a/one.smt2,0.10,2.50,solved,25.00")
        self.assertEqual(lines[2], "a/two.smt2,0.20,,unsolved,")
        self.assertEqual(len(lines), 4)

    def test_a_list_that_stopped_publishing_does_not_linger(self):
        out = self.root / "out"
        (out / "data").mkdir(parents=True)
        (out / "data/old-list.csv").write_text("stale")
        self.build()
        self.assertFalse((out / "data/old-list.csv").exists())
        self.assertTrue((out / "data/arm-vs-ref-010126.csv").is_file())

    def test_a_gap_list_no_ledger_entry_cites_is_refused(self):
        (self.root / "reports/data/gapset-orphan-vs-ref-010126.txt").write_text(GAPSET)
        with self.assertRaises(ValueError) as refusal:
            self.build()
        self.assertIn("no ledger entry cites", str(refusal.exception))

    def test_a_list_that_is_not_named_as_a_comparison_is_refused(self):
        (self.root / "reports/data/gapset-nothing.txt").write_text(GAPSET)
        with self.assertRaises(ValueError):
            self.build()

    def test_writing_into_the_retained_lists_is_refused(self):
        """The builder writes CSVs; it must not be pointed at the lists it reads."""
        with self.assertRaises(ValueError):
            self.build(out=self.root / "reports/data/site")
        with self.assertRaises(ValueError):
            self.build(out=self.root / "reports/data")

    def test_the_lists_this_project_retains_all_publish(self):
        report.ROOT, report.HERE = self.real, self.real_here
        out = self.root / "real"
        summary = report.build(out, "https://example.invalid/site/heuresis", "https://example.invalid/repo")
        retained = sorted((self.real_here / "data").glob("gapset-*.txt"))
        self.assertEqual(summary["comparisons"], len(retained))
        data, _ = self.data(out)
        for comparison in data["comparisons"]:
            with self.subTest(comparison=comparison["id"]):
                self.assertTrue((out / comparison["csv"]).is_file())
                self.assertEqual(len(comparison["rows"]), comparison["summary"]["gap"])
                self.assertTrue(comparison["ledger"]["href"].endswith(comparison["ledger"]["text"]))



class QueueTests(unittest.TestCase):
    """The queue page: the project's plan, published from the document that holds it."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name) / "site"

    def build(self):
        return report.build(self.out, "https://example.invalid/site/heuresis", REPO)

    def todo(self):
        return (ROOT / "docs/todo.md").read_text()

    def test_the_queue_page_is_written_and_reachable_from_the_report(self):
        summary = self.build()
        page = (self.out / "queue.html").read_text()
        self.assertEqual(re.findall(r"__[A-Z_]+__", page), [], "an unreplaced template placeholder")
        self.assertIn("queue.html", summary["pages"])
        self.assertIn('href="queue.html"', (self.out / "index.html").read_text())
        self.assertIn('href="index.html"', page)

    def test_it_publishes_every_section_of_the_document(self):
        self.build()
        page = (self.out / "queue.html").read_text()
        for heading in re.findall(r"^## (.+)$", self.todo(), re.MULTILINE):
            with self.subTest(heading=heading):
                self.assertIn(f"<h2>{heading}</h2>", page)

    def test_the_two_rankings_stay_separately_labelled(self):
        """The maintainer's ranking is theirs; a page that merged them would misreport it."""
        self.build()
        page = (self.out / "queue.html").read_text()
        self.assertIn("<h2>AI-agent priorities</h2>", page)
        self.assertIn("<h2>Human-maintainer priorities</h2>", page)
        self.assertLess(page.index("AI-agent priorities"), page.index("Human-maintainer priorities"))

    def test_the_counts_come_from_the_documents(self):
        self.build()
        page = (self.out / "queue.html").read_text()
        sections = report.sections(self.todo(), REPO, "tools/heuresis/docs/todo.md")
        goals = [s for s in sections if s["heading"] == "Short-term goals"][0]["rows"]
        closed = sum(1 for row in goals if "\u2705" in report.render_cell(row[0]))
        self.assertIn(f"<strong>{len(goals) - closed} of {len(goals)}</strong>", page)
        for heading in ("AI-agent priorities", "Branch maintenance"):
            rows = [s for s in sections if s["heading"] == heading][0]["rows"]
            self.assertIn(f"<strong>{len(rows)}</strong>", page)

    def test_the_landed_pull_requests_are_read_and_not_asserted(self):
        self.assertEqual(report.landed(ROOT / "docs/progress.md"), 0)
        tree = Path(self.temp.name) / "docs"
        tree.mkdir()
        record = tree / "progress.md"
        record.write_text("## Pull requests to cvc5 main\n\n| PR | what |\n| --- | --- |\n"
                          "| #1 | a thing |\n| #2 | another |\n")
        self.assertEqual(report.landed(record), 2)
        record.write_text("# nothing here\n")
        with self.assertRaises(ValueError):
            report.landed(record)

    def test_the_gap_report_says_what_is_being_done_about_the_gap(self):
        """A measurement with no stated next step leaves the reader nowhere to go."""
        self.build()
        page = (self.out / "index.html").read_text()
        self.assertIn("What we are doing about it", page)
        self.assertIn('href="queue.html"', page)
        self.assertIn("docs/directions.md", page)
        sections = report.sections(self.todo(), REPO, "tools/heuresis/docs/todo.md")
        ranked = report.named(sections, "AI-agent priorities")
        table, total, shown = report.next_steps(sections, REPO)
        self.assertEqual(total, len(ranked))
        self.assertEqual(shown, min(5, len(ranked)))
        self.assertEqual(table.count("<tr>"), shown + 1, "the header row plus one per direction")
        for row in ranked[:shown]:
            self.assertIn(report.render_cell(row[1]), page)

    def test_the_register_publishes_every_direction_with_a_resolving_anchor(self):
        """The rankings carry ten each; the register must show the rest too."""
        self.build()
        page = (self.out / "queue.html").read_text()
        source = (ROOT / "docs/directions.md").read_text()
        headings = re.findall(r"^##\s+(.+?)\s*$", source, re.MULTILINE)
        slugs = {report.slug(h) for h in headings}
        used = set(re.findall(r"directions\.md#([a-z0-9-]+)", page))
        self.assertEqual(len(used), len(re.findall(r"^## R\d+\b", source, re.MULTILINE)))
        self.assertEqual(used - slugs, set(), "an anchor the register does not define")
        self.assertEqual(used & set(re.findall(r"directions\.md#([a-z0-9-]+)", self.todo())),
                         set(re.findall(r"directions\.md#([a-z0-9-]+)", self.todo())),
                         "the generated anchors disagree with the ones the queue writes by hand")

    def test_an_em_dash_heading_keeps_both_hyphens_in_its_anchor(self):
        """Collapsing the spaces would produce a link resolving nowhere."""
        self.assertEqual(report.slug("R9 — Deleting instantiation lemmas: garbage collection"),
                         "r9--deleting-instantiation-lemmas-garbage-collection")
        self.assertEqual(report.slug("E1 Unrewriting"), "e1-unrewriting")

    def test_the_two_ranks_stay_in_their_own_columns(self):
        self.build()
        page = (self.out / "queue.html").read_text()
        self.assertIn("<th class=\"rank\">Agent rank</th>", page)
        self.assertIn("<th class=\"rank\">Maintainer rank</th>", page)
        sections = report.sections(self.todo(), REPO, "tools/heuresis/docs/todo.md")
        agent = report.ranking(sections, "AI-agent priorities")
        maintainer = report.ranking(sections, "Human-maintainer priorities")
        self.assertNotEqual(agent, maintainer, "the fixture no longer distinguishes them")
        self.assertIn(f"<strong>{len(agent)}</strong>", page, "the ranked tile")

    def test_the_counts_mirror_the_register_and_the_ranking(self):
        self.build()
        page = (self.out / "queue.html").read_text()
        source = (ROOT / "docs/directions.md").read_text()
        total = len(re.findall(r"^## R\d+\b", source, re.MULTILINE))
        self.assertIn(f"<strong>{total}</strong>", page)
        self.assertIn(f"of {total}, by the agent", page)

    def test_a_direction_that_states_no_effort_is_refused(self):
        source = (ROOT / "docs/directions.md").read_text()
        start = source.index("## R1 ")
        end = source.index("**The hypothesis.**", start)
        with self.assertRaises(ValueError) as refusal:
            report.register(source[:start] + source[start:end].split("**Effort.**")[0] + source[end:],
                            "docs/directions.md", REPO, {}, {})
        self.assertIn("R1", str(refusal.exception))

    def test_a_section_that_loses_its_table_is_refused(self):
        original = report.ROOT
        tree = Path(self.temp.name) / "heuresis"
        shutil.copytree(ROOT, tree, ignore=shutil.ignore_patterns("tests", "__pycache__"))
        todo = tree / "docs/todo.md"
        body = todo.read_text()
        start = body.index("## Branch maintenance")
        todo.write_text(body[:start] + "## Branch maintenance\n\nNo table any more.\n")
        report.ROOT = tree
        report.TEMPLATE = tree / "reports/report.html"
        report.QUEUE_TEMPLATE = tree / "reports/queue.html"
        self.addCleanup(setattr, report, "QUEUE_TEMPLATE", original / "reports/queue.html")
        self.addCleanup(setattr, report, "TEMPLATE", original / "reports/report.html")
        self.addCleanup(setattr, report, "ROOT", original)
        with self.assertRaises(ValueError) as refusal:
            self.build()
        self.assertIn("Branch maintenance", str(refusal.exception))

    def test_markup_in_the_document_cannot_smuggle_tags_onto_the_page(self):
        self.build()
        page = (self.out / "queue.html").read_text()
        self.assertNotIn("<script>", page[page.index("<main>"):])


if __name__ == "__main__":
    unittest.main()
