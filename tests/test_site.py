"""Site-builder cases: the project list, the report contract, and the built links."""
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_site", ROOT / "scripts/build_site.py")
site = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(site)

README = """# demo

## Research projects

| project | question |
| --- | --- |
| [alpha](tools/alpha/README.md) | What does alpha ask? |
| [beta](tools/beta/README.md) | What does beta ask? |

## Run it
"""

BUILDER = '''#!/usr/bin/env python3
import argparse, json
from pathlib import Path
parser = argparse.ArgumentParser()
parser.add_argument("--out", type=Path, required=True)
parser.add_argument("--base-url")
parser.add_argument("--repo-url")
parser.add_argument("--site-href")
args = parser.parse_args()
args.out.mkdir(parents=True, exist_ok=True)
%s
print(json.dumps(%s))
'''
DESCRIPTION = {"name": "alpha", "title": "alpha", "question": "What does alpha ask?",
               "summary": "A summary.", "href": "index.html", "updated": "2026-01-01",
               "headline": [{"label": "gap set", "value": "3", "note": "of 12"}]}


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.readme = Path(self.temp.name) / "README.md"
        self.readme.write_text(README)

    def test_the_front_page_table_is_the_project_list(self):
        found = site.projects(self.readme, "https://example.invalid/repo")
        self.assertEqual([project["name"] for project in found], ["alpha", "beta"])
        self.assertEqual(found[0]["href"], "https://example.invalid/repo/blob/main/tools/alpha/README.md")
        self.assertEqual(found[1]["question"], "What does beta ask?")

    def test_a_front_page_without_the_table_is_refused(self):
        for text in [README.replace("## Research projects", "## Projects"),
                     README.replace("| [alpha](tools/alpha/README.md) | What does alpha ask? |\n", "")
                           .replace("| [beta](tools/beta/README.md) | What does beta ask? |\n", ""),
                     README.replace("[alpha](tools/alpha/README.md)", "alpha")]:
            with self.subTest(text=text[:60]), self.assertRaises(ValueError):
                self.readme.write_text(text)
                site.projects(self.readme, "https://example.invalid/repo")

    def test_this_repository_lists_its_own_projects(self):
        found = site.projects(ROOT / "README.md", "https://example.invalid/repo")
        self.assertIn("heuresis", [project["name"] for project in found])
        for project in found:
            with self.subTest(project=project["name"]):
                self.assertTrue((ROOT / "tools" / project["name"]).is_dir())
                self.assertTrue(project["question"])


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.out = self.root / "site"

    def builder(self, writes, prints):
        path = self.root / "tools/alpha/reports/build"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(BUILDER % (writes, prints))
        return path

    def run_report(self, writes='(args.out / "index.html").write_text("page")', prints=repr(DESCRIPTION),
                   out=None):
        return site.run_report(self.builder(writes, prints), out or self.out, "https://example.invalid/site",
                               "https://example.invalid/repo")

    def test_a_report_that_honours_the_contract_is_published(self):
        report = self.run_report()
        self.assertEqual(report["path"], "alpha/index.html")
        self.assertTrue((self.out / "alpha/index.html").is_file())

    def test_a_report_that_does_not_is_refused(self):
        cases = {
            "not JSON": ('pass', '"' + "not JSON" + '"'),
            "missing keys": ('pass', repr({"name": "alpha"})),
            "another name": ('(args.out / "index.html").write_text("page")',
                             repr({**DESCRIPTION, "name": "gamma"})),
            "an unwritten page": ('pass', repr(DESCRIPTION)),
        }
        for reason, (writes, prints) in cases.items():
            # A fresh output directory: an earlier case's page must not stand in.
            with self.subTest(reason=reason), self.assertRaises(ValueError):
                self.run_report(writes, prints, out=self.root / f"site-{reason.replace(' ', '-')}")

    def test_a_builder_that_fails_is_refused_with_what_it_said(self):
        with self.assertRaises(ValueError) as refusal:
            self.run_report('raise SystemExit("report: the evidence moved")')
        self.assertIn("the evidence moved", str(refusal.exception))


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name) / "site"

    def build(self):
        return site.build(self.out, "https://example.invalid/site", "https://example.invalid/repo")

    def test_the_site_publishes_this_tree(self):
        published = self.build()
        page = (self.out / "index.html").read_text()
        self.assertTrue((self.out / ".nojekyll").is_file())
        self.assertIn("heuresis", published)
        self.assertIn('href="heuresis/index.html"', page)
        self.assertIn(published["heuresis"]["headline"][0]["value"], page)
        self.assertEqual(re.findall(r"__[A-Z_]+__", page), [], "an unreplaced template placeholder")

    def test_every_project_is_listed_whether_or_not_it_publishes(self):
        self.build()
        page = (self.out / "index.html").read_text()
        for project in site.projects(ROOT / "README.md", "https://example.invalid/repo"):
            with self.subTest(project=project["name"]):
                self.assertIn(f">{project['name']}</a>", page)
        self.assertIn("no report here; its records are in the repository", page)

    def test_the_links_the_site_writes_resolve(self):
        self.build()
        for page in self.out.rglob("*.html"):
            for href in re.findall(r'(?:href|src)="([^"]+)"', page.read_text()):
                if href.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                with self.subTest(page=page.name, href=href):
                    self.assertTrue((page.parent / href).exists(), f"{href} is missing")

    def test_a_published_report_the_front_page_does_not_advertise_is_refused(self):
        original = site.ROOT
        stand_in = Path(self.temp.name) / "tree"
        (stand_in / "tools/gamma/reports").mkdir(parents=True)
        (stand_in / "README.md").write_text(README)
        (stand_in / "tools/gamma/reports/build").write_text(
            BUILDER % ('(args.out / "index.html").write_text("page")', repr({**DESCRIPTION, "name": "gamma"})))
        site.ROOT = stand_in
        self.addCleanup(setattr, site, "ROOT", original)
        with self.assertRaises(ValueError) as refusal:
            self.build()
        self.assertIn("the front page does not list it", str(refusal.exception))


    def test_a_report_says_what_its_date_is_the_date_of(self):
        """The index must not call something a measurement on a project's behalf."""
        published = self.build()
        page = (self.out / "index.html").read_text()
        self.assertEqual(published["heuresis"]["dated"], "measured")
        self.assertIn(f'measured {published["heuresis"]["updated"]}', page)
        for name, report in published.items():
            with self.subTest(project=name):
                self.assertIn(f'{report["dated"]} {report["updated"]}', page)
                if report["dated"] != "measured":
                    self.assertNotIn(f'measured {report["updated"]}', page)

    def test_every_published_project_carries_the_shared_figures_on_its_card(self):
        """The index is read across projects, so the comparable pair must be on it.

        Both publishing projects keep a register of directions and a queue that
        ranks part of it. Those two figures are the ones a reader compares
        between cards, so each published report puts them in its `headline`
        rather than only on its own page -- which is where they were, and why
        the index did not show them for heuresis.
        """
        published = self.build()
        page = (self.out / "index.html").read_text()
        shared = {"research directions", "ranked in the queue"}
        for name, report in sorted(published.items()):
            labels = {tile["label"] for tile in report["headline"]}
            with self.subTest(project=name):
                self.assertEqual(shared - labels, set(),
                                 f"{name}'s card omits a figure the other card shows")
                for tile in report["headline"]:
                    self.assertIn(f"<strong>{tile['value']}</strong>", page)

    def test_a_missing_or_malformed_date_label_is_refused_or_defaulted(self):
        original = site.ROOT
        stand_in = Path(self.temp.name) / "labelled"
        (stand_in / "tools/alpha/reports").mkdir(parents=True)
        (stand_in / "README.md").write_text(README)
        site.ROOT = stand_in
        self.addCleanup(setattr, site, "ROOT", original)
        builder = stand_in / "tools/alpha/reports/build"

        builder.write_text(BUILDER % ('(args.out / "index.html").write_text("page")',
                                      repr({**DESCRIPTION, "name": "alpha"})))
        self.assertEqual(self.build()["alpha"]["dated"], "updated")

        builder.write_text(BUILDER % ('(args.out / "index.html").write_text("page")',
                                      repr({**DESCRIPTION, "name": "alpha", "dated": "two words"})))
        with self.assertRaises(ValueError) as refusal:
            self.build()
        self.assertIn("one word", str(refusal.exception))

if __name__ == "__main__":
    unittest.main()
