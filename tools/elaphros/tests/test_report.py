"""Exercise elaphros's report builder against this project's own documents.

The builder publishes counts taken from the documents beside it, so the tests
that matter are the refusals: a document that has lost the section or the table
the page is built from must stop the build rather than publish a page that has
quietly drifted from it.
"""
import importlib.util
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPO = "https://example.invalid/repo"


def load(path):
    spec = importlib.util.spec_from_loader("elaphros_report",
                                           importlib.machinery.SourceFileLoader("elaphros_report", str(path)))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name) / "site"
        self.report = load(ROOT / "reports/build")

    def build(self):
        return self.report.build(self.out, "https://example.invalid/site/elaphros", REPO)

    def stand_in(self):
        """A copy of the project, so a document can be damaged without touching it."""
        tree = Path(tempfile.mkdtemp(dir=self.temp.name)) / "elaphros"
        shutil.copytree(ROOT, tree, ignore=shutil.ignore_patterns("tests", "__pycache__"))
        self.report.ROOT = tree
        self.report.HERE = tree / "reports"
        self.report.TEMPLATE = tree / "reports/report.html"
        self.addCleanup(setattr, self.report, "ROOT", ROOT)
        self.addCleanup(setattr, self.report, "HERE", ROOT / "reports")
        self.addCleanup(setattr, self.report, "TEMPLATE", ROOT / "reports/report.html")
        return tree

    def test_the_report_describes_itself_and_writes_what_it_names(self):
        summary = self.build()
        for key in ("name", "title", "question", "summary", "href", "updated", "headline"):
            self.assertIn(key, summary, "the site contract in docs/site.md")
        self.assertEqual(summary["name"], "elaphros")
        self.assertTrue((self.out / summary["href"]).is_file())
        self.assertRegex(summary["updated"], r"^\d{4}-\d{2}-\d{2}$")
        page = (self.out / "index.html").read_text()
        self.assertEqual(re.findall(r"__[A-Z_]+__", page), [], "an unreplaced template placeholder")

    def test_every_count_on_the_page_comes_from_a_document(self):
        summary = self.build()
        register = (ROOT / "docs/directions.md").read_text()
        self.assertEqual(summary["directions"], len(re.findall(r"^## E\d+\b", register, re.MULTILINE)))
        queue = re.search(r"^## Agent research priorities\s*$(.*?)(?=^## )",
                          (ROOT / "docs/todo.md").read_text(), re.MULTILINE | re.DOTALL).group(1)
        rows = [line for line in queue.splitlines() if line.strip().startswith("|")]
        self.assertEqual(summary["ranked"], len(rows) - 2)
        page = (self.out / "index.html").read_text()
        for tile in summary["headline"]:
            self.assertIn(f"<strong>{tile['value']}</strong>", page)

    def test_the_page_states_that_nothing_has_been_measured(self):
        summary = self.build()
        self.assertEqual([t for t in summary["headline"] if t["label"] == "measurements"][0]["value"], "0")
        page = (self.out / "index.html").read_text().lower()
        self.assertIn("no experiment has been run", page)
        self.assertIn("nothing here is a measurement", page)

    def test_a_ranked_direction_the_register_does_not_define_is_refused(self):
        tree = self.stand_in()
        todo = tree / "docs/todo.md"
        todo.write_text(todo.read_text().replace("directions.md#e2-smaller-macro-obligations",
                                                 "directions.md#e99-invented", 1)
                                        .replace("[E2: smaller macro obligations]", "[E99: invented]", 1))
        with self.assertRaises(ValueError) as refusal:
            self.build()
        self.assertIn("E99", str(refusal.exception))

    def test_a_planning_status_in_an_unknown_state_is_refused(self):
        tree = self.stand_in()
        todo = tree / "docs/todo.md"
        todo.write_text(todo.read_text().replace(
            "| Specify E13's instrument | Open:", "| Specify E13's instrument | Probably:", 1))
        with self.assertRaises(ValueError) as refusal:
            self.build()
        self.assertIn("starts with none of", str(refusal.exception))

    def test_a_document_that_loses_its_section_or_table_is_refused(self):
        for name, damage in (("docs/todo.md", ("## Agent research priorities", "## Something else")),
                             ("docs/todo.md", ("## Planning work", "## Gone")),
                             ("docs/todo.md", ("## Maintainer guidance", "## Gone")),
                             ("docs/directions.md", ("## The map", "## Not the map")),
                             ("docs/progress.md", ("| question | current evidence |", "| a | b |"))):
            with self.subTest(document=name, damage=damage[0]):
                tree = self.stand_in()
                path = tree / name
                path.write_text(path.read_text().replace(*damage, 1))
                with self.assertRaises(ValueError):
                    self.build()

    def test_a_progress_record_with_no_date_is_refused(self):
        tree = self.stand_in()
        record = tree / "docs/progress.md"
        record.write_text(record.read_text().replace("**Updated 2026-09-19.", "**Recently.", 1))
        with self.assertRaises(ValueError) as refusal:
            self.build()
        self.assertIn("Updated", str(refusal.exception))

    def test_the_register_publishes_every_direction_with_a_resolving_anchor(self):
        """The queue shows thirteen; the register must show what was left out too."""
        summary = self.build()
        page = (self.out / "index.html").read_text()
        register = (ROOT / "docs/directions.md").read_text()
        headings = re.findall(r"^##\s+(.+?)\s*$", register, re.MULTILINE)
        slugs = {"-".join(re.sub(r"[^\w\s-]", "", h.lower()).split()) for h in headings}
        used = set(re.findall(r"directions\.md#([a-z0-9-]+)", page))
        self.assertEqual(len(used), summary["directions"])
        self.assertEqual(used - slugs, set(), "an anchor the register does not define")
        self.assertIn("unranked", page)

    def test_a_direction_that_states_no_effort_is_refused(self):
        tree = self.stand_in()
        register = tree / "docs/directions.md"
        body = register.read_text()
        start = body.index("## E1 Unrewriting")
        end = body.index("**Question.**", start)
        register.write_text(body[:start] + "## E1 Unrewriting\n\n" + body[end:])
        with self.assertRaises(ValueError) as refusal:
            self.build()
        self.assertIn("E1", str(refusal.exception))

    def test_the_retained_snapshots_are_counted_and_checked_against_their_register(self):
        summary = self.build()
        page = (self.out / "index.html").read_text()
        data = ROOT / "reports/data"
        files = [p for p in data.iterdir() if p.is_file() and p.name != "README.md"
                 and not p.name.startswith(".")]
        for path in files:
            with self.subTest(artifact=path.name):
                lines = sum(1 for _ in path.open(encoding="utf-8", errors="replace"))
                self.assertIn(f"<td class=\"rank\">{lines:,}</td>", page)
        self.assertIn(f"<strong>{len(files)}</strong>", page)

    def test_a_register_and_a_directory_that_disagree_are_refused(self):
        for damage in ("extra file", "missing file"):
            with self.subTest(damage=damage):
                tree = self.stand_in()
                if damage == "extra file":
                    (tree / "reports/data/2026-09-18-unlisted.tsv").write_text("a\tb\n")
                else:
                    next(p for p in (tree / "reports/data").iterdir()
                         if p.suffix == ".json").unlink()
                with self.assertRaises(ValueError) as refusal:
                    self.build()
                self.assertRegex(str(refusal.exception), "not retained here|named by no register row")

    def test_writing_into_the_project_itself_is_refused(self):
        for destination in (ROOT, ROOT / "docs"):
            with self.subTest(destination=destination.name):
                with self.assertRaises(ValueError):
                    self.report.build(destination, "https://example.invalid/site", REPO)

    def test_markup_escapes_before_it_adds_tags(self):
        rendered = self.report.markup("**bold** <script>alert(1)</script> [x](y.md)",
                                      REPO, "tools/elaphros/docs/todo.md")
        self.assertIn("<strong>bold</strong>", rendered)
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn(f'href="{REPO}/blob/main/tools/elaphros/docs/y.md"', rendered)

    def test_links_resolve_against_the_document_that_carried_them(self):
        resolve = self.report.resolve
        source = "tools/elaphros/docs/todo.md"
        self.assertEqual(resolve(REPO, source, "directions.md#e1-unrewriting"),
                         f"{REPO}/blob/main/tools/elaphros/docs/directions.md#e1-unrewriting")
        self.assertEqual(resolve(REPO, source, "ledger/README.md"),
                         f"{REPO}/blob/main/tools/elaphros/docs/ledger/README.md")
        self.assertEqual(resolve(REPO, source, "https://example.com/x"), "https://example.com/x")

    def test_the_json_description_is_one_object_on_stdout(self):
        summary = self.build()
        self.assertEqual(json.loads(json.dumps(summary))["href"], "index.html")


if __name__ == "__main__":
    unittest.main()
