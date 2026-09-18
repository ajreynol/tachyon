"""Report-builder cases on small synthetic trees; no solver, host or network."""
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "report"
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


class BuildTests(unittest.TestCase):
    """A whole report, built from a synthetic project tree and from this one."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "ledger/data").mkdir(parents=True)
        (self.root / "docs").mkdir()
        (self.root / "ledger/2026-01-01-example.md").write_text(ENTRY)
        (self.root / "ledger/data/gapset-arm-vs-ref-010126.txt").write_text(GAPSET)
        (self.root / "docs/progress.md").write_text(PROGRESS)
        self.real, report.ROOT = report.ROOT, self.root
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
        self.assertEqual([tile["value"] for tile in summary["headline"]], ["3", "1", "2"])
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
        (self.root / "ledger/data/gapset-orphan-vs-ref-010126.txt").write_text(GAPSET)
        with self.assertRaises(ValueError) as refusal:
            self.build()
        self.assertIn("no ledger entry cites", str(refusal.exception))

    def test_a_list_that_is_not_named_as_a_comparison_is_refused(self):
        (self.root / "ledger/data/gapset-nothing.txt").write_text(GAPSET)
        with self.assertRaises(ValueError):
            self.build()

    def test_writing_into_the_recorded_evidence_is_refused(self):
        with self.assertRaises(ValueError):
            self.build(out=self.root / "ledger/data/site")

    def test_the_lists_this_project_retains_all_publish(self):
        report.ROOT = self.real
        out = self.root / "real"
        summary = report.build(out, "https://example.invalid/site/heuresis", "https://example.invalid/repo")
        retained = sorted((self.real / "ledger/data").glob("gapset-*.txt"))
        self.assertEqual(summary["comparisons"], len(retained))
        data, _ = self.data(out)
        for comparison in data["comparisons"]:
            with self.subTest(comparison=comparison["id"]):
                self.assertTrue((out / comparison["csv"]).is_file())
                self.assertEqual(len(comparison["rows"]), comparison["summary"]["gap"])
                self.assertTrue(comparison["ledger"]["href"].endswith(comparison["ledger"]["text"]))


if __name__ == "__main__":
    unittest.main()
