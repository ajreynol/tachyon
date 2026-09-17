import importlib.util
import re
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("stats_plots", Path(__file__).parents[1] / "plots.py")
plots = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(plots)


def run(index, total, values):
    return {"id": index, "benchmark": f"{index}.smt2", "status": "unsat", "total": total,
            "values": values, "accounted": sum(values), "residual": total - sum(values),
            "gap": max(0, total - sum(values)), "excess": max(0, sum(values) - total),
            "coverage": sum(values) / total, "missing": [], "excluded": ""}


def report(rows, names):
    included = [r for r in rows if not r["excluded"]]
    total = sum(r["total"] for r in included)
    summary = {"runs": len(rows), "included": len(included), "excluded": len(rows) - len(included),
               "total_seconds": total, "accounted_seconds": sum(r["accounted"] for r in included)}
    config = {"total": "global::totalTime", "missing": "zero",
              "categories": [{"name": n, "terms": {n: 1}} for n in names], "warnings": []}
    return summary, config


class PlotTests(unittest.TestCase):
    def test_survival_is_the_complement_of_the_distribution(self):
        points = plots.survival([0.1, 0.2, 0.3, 0.4])
        self.assertEqual(points[0], (0.0, 100.0))
        self.assertEqual([round(x, 6) for x, _ in points[1:]], [10.0, 20.0, 30.0, 40.0])
        self.assertEqual([round(y, 6) for _, y in points[1:]], [100.0, 75.0, 50.0, 25.0])
        # Every threshold keeps the runs at or above it; the axes never leave [0, 100].
        self.assertTrue(all(0 <= y <= 100 for _, y in points))
        self.assertLessEqual(len(plots.survival([i / 5000 for i in range(5000)], samples=400)), 402)

    def test_percentile_interpolates_between_order_statistics(self):
        self.assertEqual(plots.percentile([0, 10], 0.5), 5)
        self.assertEqual(plots.percentile([0, 1, 2, 3], 0.9), 2.7)
        self.assertEqual(plots.percentile([4], 0.9), 4)
        self.assertIsNone(plots.percentile([], 0.5))

    def test_text_is_measured_and_escaped(self):
        self.assertAlmostEqual(plots.measure("00", 10), 11.12)
        canvas = plots.Canvas()
        canvas.text(0, 0, r"a(b)c\d")
        canvas.text(100, 0, "right", anchor="end")
        stream = "\n".join(canvas.ops)
        self.assertIn(r"(a\(b\)c\\d) Tj", stream)
        # An end-anchored label is placed by its measured width, never past its anchor.
        self.assertIn(f"{100 - plots.measure('right', 9):.2f} 0.00 Tm", stream)

    def test_pdf_structure_and_offsets(self):
        with tempfile.TemporaryDirectory() as directory:
            path = plots.write_pdf(Path(directory) / "x.pdf", [plots.Canvas(), plots.Canvas()])
            raw = path.read_bytes()
            self.assertTrue(raw.startswith(b"%PDF-1.4"))
            self.assertTrue(raw.rstrip().endswith(b"%%EOF"))
            self.assertIn(b"/Count 2", raw)
            offsets = [int(m) for m in re.findall(rb"^(\d{10}) 00000 n $", raw, re.M)]
            self.assertEqual(len(offsets), 8)  # catalog, pages, two fonts, two pages, two streams
            for number, offset in enumerate(offsets, 1):
                self.assertTrue(raw[offset:].startswith(f"{number} 0 obj".encode()))
            length = int(re.search(rb"/Length (\d+) >>\nstream\n", raw)[1])
            body = raw.split(b"stream\n", 1)[1]
            self.assertEqual(body[:length] + b"\nendstream", body[:length + 10])

    def test_write_plots_emits_a_file_per_category_plus_the_summaries(self):
        rows = [run(1, 10, [1, 2]), run(2, 90, [9, 9])]
        summary, config = report(rows, ["a::b", "c::d"])
        with tempfile.TemporaryDirectory() as directory:
            written = plots.write_plots(directory, rows, summary, config, "stats.txt")
            self.assertEqual([p.name for p in written],
                             ["cdf-1-a-b.pdf", "cdf-2-c-d.pdf", "cdf-all.pdf", "pie-total.pdf", "plots.pdf"])
            self.assertIn(b"/Count 4", (Path(directory) / "plots.pdf").read_bytes())
            pie = (Path(directory) / "pie-total.pdf").read_text(encoding="latin-1")
            # Misc is 100 - 21% of the 100 s total, and the table's rows carry every value.
            self.assertIn("(79.0%) Tj", pie)
            self.assertIn("(misc \\(global::totalTime not in a timer above\\)) Tj", pie)

    def test_over_counting_draws_no_negative_slice(self):
        rows = [run(1, 10, [8, 7])]
        summary, config = report(rows, ["a", "b"])
        with tempfile.TemporaryDirectory() as directory:
            plots.write_plots(directory, rows, summary, config, "stats.txt")
            pie = (Path(directory) / "pie-total.pdf").read_text(encoding="latin-1")
            self.assertIn("no misc slice", pie)
            self.assertIn("(-50.0%) Tj", pie)  # the excess stays visible in the table

    def test_shares_beyond_the_axis_are_clipped_and_counted(self):
        rows = [run(1, 10, [9.0]), run(2, 10, [1.0])]
        summary, config = report(rows, ["a"])
        with tempfile.TemporaryDirectory() as directory:
            plots.write_plots(directory, rows, summary, config, "stats.txt", x_max=50.0)
            page = (Path(directory) / "cdf-1-a.pdf").read_text(encoding="latin-1")
            self.assertIn("1 per-benchmark shares exceed the 50% axis and are clipped", page)
            self.assertIn(" re W n", page)

    def test_refusals(self):
        rows = [run(1, 10, [1] * 9)]
        summary, config = report(rows, [f"c{i}" for i in range(9)])
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "at most 8 categories"):
                plots.write_plots(directory, rows, summary, config, "stats.txt")
            excluded = dict(run(1, 10, [1]), excluded="missing total")
            summary, config = report([excluded], ["a"])
            with self.assertRaisesRegex(ValueError, "No included runs"):
                plots.write_plots(directory, [excluded], summary, config, "stats.txt")


if __name__ == "__main__":
    unittest.main()
