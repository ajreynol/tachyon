#!/usr/bin/env python3
"""Vector PDF plots for a profile run; Python standard library only."""
import argparse
import json
import math
import re
import sys
from pathlib import Path


# Slots 1-8 of a categorical palette validated for colour-vision deficiency in
# this fixed order.  A category keeps its slot in every plot, so colour follows
# the timer and not its rank, and a ninth slot is never invented.  Uncovered
# time is not a category and wears muted ink rather than a series colour.
SERIES = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100",
          "#e87ba4", "#008300", "#4a3aa7", "#e34948")
MISC = "#898781"
SURFACE, INK, SECOND, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"

# Helvetica advance widths (1/1000 em, ASCII 32-126): a PDF base-14 font ships
# no metrics, and a label has to be measured before it can be placed.  Bold text
# is measured with these too, so only set it where the text is left-aligned.
WIDTHS = (278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278,
          556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556,
          1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
          667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556,
          333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
          556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584)
WIDE, TALL = 720, 450
LEFT, RIGHT, TOP, FOOT = 62, 24, 74, 64


def measure(text, size):
    return sum(WIDTHS[ord(c) - 32] for c in text if 32 <= ord(c) < 127) * size / 1000


def arc(x, y, radius, start, end):
    """Cubic segments approximating an arc, at most a quarter turn each."""
    count = max(1, math.ceil(abs(end - start) / (math.pi / 2)))
    step = (end - start) / count
    reach = 4 / 3 * math.tan(step / 4) * radius
    segments = []
    for index in range(count):
        a, b = start + index * step, start + (index + 1) * step
        ax, ay = x + radius * math.cos(a), y + radius * math.sin(a)
        bx, by = x + radius * math.cos(b), y + radius * math.sin(b)
        segments.append(f"{ax - reach * math.sin(a):.2f} {ay + reach * math.cos(a):.2f} "
                        f"{bx + reach * math.sin(b):.2f} {by - reach * math.cos(b):.2f} "
                        f"{bx:.2f} {by:.2f} c")
    return segments


class Canvas:
    """One PDF content stream, in points, with the origin at the bottom left."""

    def __init__(self):
        self.ops = []

    def emit(self, *ops):
        self.ops.extend(ops)

    def paint(self, color, stroke=False):
        red, green, blue = (int(color[index:index + 2], 16) / 255 for index in (1, 3, 5))
        self.emit(f"{red:.3f} {green:.3f} {blue:.3f} {'RG' if stroke else 'rg'}")

    def clip(self, x, y, width, height):
        """Open a state in which drawing is confined to this box; close with restore()."""
        self.emit("q", f"{x:.2f} {y:.2f} {width:.2f} {height:.2f} re W n")

    def restore(self):
        self.emit("Q")

    def rect(self, x, y, width, height, fill):
        self.paint(fill)
        self.emit(f"{x:.2f} {y:.2f} {width:.2f} {height:.2f} re f")

    def line(self, points, color, width=1):
        if len(points) < 2:
            return
        self.paint(color, True)
        self.emit(f"{width:g} w 1 J 1 j", f"{points[0][0]:.2f} {points[0][1]:.2f} m")
        self.emit(*(f"{x:.2f} {y:.2f} l" for x, y in points[1:]), "S")

    def dot(self, x, y, radius, fill):
        # A 2pt surface ring keeps a marker legible where it crosses its own line.
        for size, color in ((radius + 2, SURFACE), (radius, fill)):
            self.paint(color)
            self.emit(f"{x + size:.2f} {y:.2f} m", *arc(x, y, size, 0, 2 * math.pi), "f")

    def wedge(self, x, y, radius, start, end, fill):
        self.paint(fill)
        self.paint(SURFACE, True)
        # The 2pt stroke is the surface itself: a gap between slices, not a border.
        self.emit(f"{x:.2f} {y:.2f} m", f"{x + radius * math.cos(start):.2f} {y + radius * math.sin(start):.2f} l",
                  *arc(x, y, radius, start, end), "h 2 w B")

    def text(self, x, y, text, size=9, color=INK, bold=False, anchor="start", turned=False):
        text = "".join(c if 32 <= ord(c) < 127 else "?" for c in text)
        offset = 0 if anchor == "start" else measure(text, size) / (2 if anchor == "middle" else 1)
        x, y = (x, y - offset) if turned else (x - offset, y)
        self.paint(color)
        body = text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
        matrix = f"0 1 -1 0 {x:.2f} {y:.2f}" if turned else f"1 0 0 1 {x:.2f} {y:.2f}"
        self.emit(f"BT /{'F2' if bold else 'F1'} {size:g} Tf {matrix} Tm ({body}) Tj ET")


def write_pdf(path, pages):
    """Assemble content streams into a PDF; base-14 fonts only, nothing embedded."""
    objects = ["<< /Type /Catalog /Pages 2 0 R >>", None,
               "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
               "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"]
    kids = []
    for canvas in pages:
        content = "\n".join(canvas.ops)
        number = len(objects) + 1
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {WIDE} {TALL}] "
                       f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {number + 1} 0 R >>")
        objects.append(f"<< /Length {len(content.encode('latin-1'))} >>\nstream\n{content}\nendstream")
        kids.append(f"{number} 0 R")
    objects[1] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(pages)} >>"
    out, offsets = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"), []
    for number, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n{body}\nendobj\n".encode("latin-1")
    start = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("latin-1")
    out += b"".join(f"{offset:010d} 00000 n \n".encode("latin-1") for offset in offsets)
    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n".encode("latin-1")
    Path(path).write_bytes(out)
    return Path(path)


def percentile(ordered, fraction):
    """Linear interpolation between order statistics, as the HTML report uses."""
    if not ordered:
        return None
    position = (len(ordered) - 1) * fraction
    below, above = math.floor(position), math.ceil(position)
    return ordered[below] + (ordered[above] - ordered[below]) * (position - below)


def survival(shares, samples=400):
    """Points (threshold, share of benchmarks at or above it), both in percent."""
    ordered = sorted(shares, reverse=True)
    count = len(ordered)
    points = [(0.0, 100.0)] + [(ordered[k] * 100, (k + 1) * 100 / count) for k in reversed(range(count))]
    if len(points) <= samples:
        return points
    stride = math.ceil(len(points) / samples)
    return points[::stride] + [points[-1]]


def frame(title, subtitle, note):
    canvas = Canvas()
    canvas.rect(0, 0, WIDE, TALL, SURFACE)
    canvas.text(24, TALL - 32, title, 13, INK, bold=True)
    canvas.text(24, TALL - 48, subtitle, 8.5, SECOND)
    canvas.text(24, 16, note, 7.5, MUTED)
    return canvas


def axes(canvas, right, x_max, x_label, y_label):
    """A percent-by-percent plot box with hairline gridlines; returns its corners."""
    x0, x1, y0, y1 = LEFT, right, FOOT, TALL - TOP
    for step in range(0, 6):
        y = y0 + (y1 - y0) * step / 5
        canvas.line([(x0, y), (x1, y)], GRID if step else AXIS)
        canvas.text(x0 - 6, y - 3, f"{step * 20}%", 8, MUTED, anchor="end")
    for step in range(0, 6):
        value = x_max * step / 5
        x = x0 + (x1 - x0) * step / 5
        if step:
            canvas.line([(x, y0), (x, y1)], GRID)
        canvas.text(x, y0 - 14, f"{value:g}%", 8, MUTED, anchor="middle")
    canvas.line([(x0, y0), (x0, y1)], AXIS)
    canvas.text((x0 + x1) / 2, y0 - 30, x_label, 8.5, SECOND, anchor="middle")
    canvas.text(20, (y0 + y1) / 2, y_label, 8.5, SECOND, anchor="middle", turned=True)
    return x0, x1, y0, y1


def place(box, x_max, x, y):
    x0, x1, y0, y1 = box
    return x0 + (x1 - x0) * x / x_max, y0 + (y1 - y0) * y / 100


def cdf_page(name, color, shares, x_max, aggregate, note, marks=True):
    """One timer's survival curve: the share of runs at or above a share of total time."""
    ordered = sorted(shares)
    canvas = frame(name, "Share of global::totalTime per benchmark. A point (x, y) reads: "
                   f"for y% of the {len(shares):,} benchmarks, this timer was at least x% of total time.", note)
    box = axes(canvas, WIDE - RIGHT, x_max, "This timer as a share of global::totalTime (%)",
               "Benchmarks at or above (%)")
    if aggregate is not None and aggregate * 100 <= x_max:
        x, _ = place(box, x_max, aggregate * 100, 0)
        canvas.line([(x, box[2]), (x, box[3])], AXIS)
        canvas.text(x + 4, box[3] - 9, f"cumulative {aggregate * 100:.1f}%", 7.5, MUTED)
    canvas.clip(box[0], box[2], box[1] - box[0], box[3] - box[2])
    canvas.line([place(box, x_max, x, y) for x, y in survival(shares)], color, 2)
    canvas.restore()
    for fraction, label in ((0.5, "median"), (0.9, "p90")) if marks else ():
        value = percentile(ordered, fraction) * 100
        if value > x_max:
            continue
        x, y = place(box, x_max, value, 100 - fraction * 100)
        canvas.dot(x, y, 4, color)
        canvas.text(min(x + 11, box[1] - 74), y - 3, f"{label} {value:.2f}%", 8, SECOND)
    return canvas


def overlay_page(names, shares, x_max, note):
    """Every timer on one axis, so the distributions can be compared directly."""
    legend = WIDE - RIGHT - max(measure(name, 8) for name in names) - 16
    canvas = frame("All timers", "Share of global::totalTime per benchmark. A point (x, y) reads: "
                   f"for y% of the {len(shares[0]):,} benchmarks, that timer was at least x% of total time.", note)
    box = axes(canvas, legend - 20, x_max, "The timer as a share of global::totalTime (%)",
               "Benchmarks at or above (%)")
    canvas.clip(box[0], box[2], box[1] - box[0], box[3] - box[2])
    for index, column in enumerate(shares):
        canvas.line([place(box, x_max, x, y) for x, y in survival(column)], SERIES[index], 2)
    canvas.restore()
    top = box[3] - 4
    for index, name in enumerate(names):
        y = top - index * 16
        canvas.line([(legend, y), (legend + 10, y)], SERIES[index], 2)
        canvas.text(legend + 15, y - 3, name, 8, SECOND)
    return canvas


def pie_page(names, seconds, misc, total, note):
    """Cumulative time over every included run, with uncovered time as its own slice."""
    slices = [(name, value, SERIES[index]) for index, (name, value) in enumerate(zip(names, seconds))]
    slices.append(("misc (global::totalTime not in a timer above)", misc, MISC))
    over = misc < 0
    whole = sum(value for _, value, _ in slices) if not over else sum(seconds)
    canvas = frame("Cumulative time by timer",
                   f"Total global::totalTime over all included runs, {total:,.0f} s. "
                   + ("Timers over-count the total, so there is no misc slice; the excess is noted below."
                      if over else f"Misc is the {misc / total * 100:.1f}% of total time no timer above accounts for."),
                   note)
    x, y, radius = 190, 200, 128
    angle = math.pi / 2
    for name, value, color in slices:
        if value <= 0 or whole <= 0:
            continue
        end = angle - 2 * math.pi * value / whole
        canvas.wedge(x, y, radius, angle, end, color)
        if value / whole >= 0.04:  # Label only slices with room for the text inside.
            middle = (angle + end) / 2
            light = sum(int(color[i:i + 2], 16) for i in (1, 3, 5)) / 765 > 0.6
            canvas.text(x + 0.64 * radius * math.cos(middle), y + 0.64 * radius * math.sin(middle) - 3,
                        f"{value / whole * 100:.1f}%", 9, INK if light else SURFACE, anchor="middle")
        angle = end
    table = 392
    for label, column, anchor in (("timer", table + 14, "start"), ("seconds", WIDE - RIGHT - 62, "end"),
                                  ("share", WIDE - RIGHT, "end")):
        canvas.text(column, TALL - TOP - 6, label, 7.5, MUTED, anchor=anchor)
    canvas.line([(table, TALL - TOP - 12), (WIDE - RIGHT, TALL - TOP - 12)], AXIS)
    for index, (name, value, color) in enumerate(slices):
        y = TALL - TOP - 28 - index * 19
        canvas.rect(table, y - 1, 9, 9, color)
        canvas.text(table + 14, y, name, 8.5, INK if index < len(names) else SECOND)
        canvas.text(WIDE - RIGHT - 62, y, f"{value:,.1f}", 8.5, SECOND, anchor="end")
        canvas.text(WIDE - RIGHT, y, f"{value / total * 100:.1f}%", 8.5, SECOND, anchor="end")
    y = TALL - TOP - 28 - len(slices) * 19
    canvas.line([(table, y + 13), (WIDE - RIGHT, y + 13)], AXIS)
    canvas.text(table + 14, y, "global::totalTime", 8.5, INK, bold=True)
    canvas.text(WIDE - RIGHT - 62, y, f"{total:,.1f}", 8.5, INK, anchor="end")
    canvas.text(WIDE - RIGHT, y, "100.0%", 8.5, INK, anchor="end")
    return canvas


def write_plots(output, rows, summary, config, source, x_max=100.0):
    """One CDF page per category, a combined CDF, the pie, and all of them in one file."""
    names = [category["name"] for category in config["categories"]]
    if len(names) > len(SERIES):
        raise ValueError(f"plots support at most {len(SERIES)} categories, the palette's slots; "
                         "combine categories rather than repeating a colour.")
    included = [row for row in rows if not row["excluded"]]
    if not included:
        raise ValueError("No included runs to plot; every run had a missing or zero total.")
    total = summary["total_seconds"]
    shares = [[row["values"][index] / row["total"] for row in included] for index in range(len(names))]
    seconds = [sum(row["values"][index] for row in included) for index in range(len(names))]
    beyond = sum(value * 100 > x_max for column in shares for value in column)
    note = (f"{source} | {summary['included']:,} of {summary['runs']:,} runs included; "
            f"{summary['excluded']:,} excluded for a missing or zero total"
            + (f" | {beyond:,} per-benchmark shares exceed the {x_max:g}% axis and are clipped" if beyond else "")
            + (f" | {len(config['warnings']):,} warnings" if config.get("warnings") else ""))
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    pages, written = [], []
    for index, name in enumerate(names):
        page = cdf_page(name, SERIES[index], shares[index], x_max, seconds[index] / total if total else None, note)
        slug = re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-")
        written.append(write_pdf(output / f"cdf-{index + 1}-{slug}.pdf", [page]))
        pages.append(page)
    pages.append(overlay_page(names, shares, x_max, note))
    written.append(write_pdf(output / "cdf-all.pdf", [pages[-1]]))
    pages.append(pie_page(names, seconds, total - sum(seconds), total, note))
    written.append(write_pdf(output / "pie-total.pdf", [pages[-1]]))
    written.append(write_pdf(output / "plots.pdf", pages))
    return written


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary", type=Path, help="summary.json written by profile.py")
    parser.add_argument("--output", type=Path, help="directory for the PDFs (default: the summary's own)")
    parser.add_argument("--max-share", type=float, default=100.0,
                        help="upper bound of the shared share-of-total axis, in percent (default: 100)")
    args = parser.parse_args(argv)
    try:
        if not 0 < args.max_share <= 100:
            raise ValueError("--max-share must be in (0, 100].")
        report = json.loads(args.summary.read_text())
        config = dict(report["config"], warnings=report.get("warnings", []))
        written = write_plots(args.output or args.summary.parent, report["benchmarks"],
                              report["summary"], config, report["source"], args.max_share)
        for path in written:
            print(path)
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    sys.exit(main())
