"""
Fear Less Maths — Enriched Tips Page (prototype)
Adds three visual blocks beneath the tips box on sheet-3 concept pages:
  1. A worked example box (step-by-step solved problem)
  2. A visual formula card (labelled diagram drawn in vector B&W)
  3. A quick-reference table (formula / values grid)

Drawn directly with ReportLab for crisp B&W output matching the worksheet style.
This module is intentionally self-contained so the experiment can be reviewed
on a single worksheet before rolling out.
"""
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
import math

BLACK = colors.black
WHITE = colors.white
BLUE = colors.HexColor("#1565C0")
LBLUE = colors.HexColor("#E8F4FD")
MGRAY = colors.HexColor("#555555")
LGRAY = colors.HexColor("#AAAAAA")
GREEN = colors.HexColor("#1f6f5c")
LGREEN = colors.HexColor("#E4EFE9")
GOLD = colors.HexColor("#B5862B")
LGOLD = colors.HexColor("#FBF3E2")


def _wrap(text, font, size, maxw):
    words = text.split(); lines = []; line = ""
    for w in words:
        test = (line + " " + w).strip()
        if stringWidth(test, font, size) <= maxw or not line:
            line = test
        else:
            lines.append(line); line = w
    if line: lines.append(line)
    return lines or [""]


# ═══════════════════════════════════════════════════════════════════════════════
# Block 1 — Worked Example box
# ═══════════════════════════════════════════════════════════════════════════════
def worked_example(c, x, y, w, title, steps):
    """Draw a worked-example box. Returns the new y (below the box)."""
    pad = 2.5 * mm
    line_h = 5 * mm
    # measure
    inner_w = w - 2 * pad
    wrapped = []
    for s in steps:
        for ln in _wrap(s, "Helvetica", 10, inner_w - 4 * mm):
            wrapped.append(ln)
    box_h = 7 * mm + len(wrapped) * line_h + pad
    # box
    c.setFillColor(LGREEN); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - box_h, w, box_h, 2 * mm, fill=1, stroke=1)
    # title
    c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 11)
    c.drawString(x + pad, y - 5.5 * mm, f"\u270e  {title}")
    # steps
    yy = y - 11 * mm
    c.setFont("Helvetica", 10); c.setFillColor(BLACK)
    for ln in wrapped:
        c.drawString(x + pad + 2 * mm, yy, ln)
        yy -= line_h
    return y - box_h - 3 * mm


# ═══════════════════════════════════════════════════════════════════════════════
# Block 2 — Visual Formula Cards (vector, B&W) keyed by topic
# ═══════════════════════════════════════════════════════════════════════════════
def formula_card_right_triangle(c, x, y, w):
    """Labelled right triangle for SOH-CAH-TOA. Returns new y."""
    card_h = 52 * mm
    c.setFillColor(WHITE); c.setStrokeColor(BLUE); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    c.setFillColor(BLUE); c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 2.5 * mm, y - 5.5 * mm, "\u25b3  Right Triangle — SOH CAH TOA")

    # triangle geometry (right angle bottom-left)
    bx = x + 6 * mm           # base-left x
    by = y - card_h + 8 * mm  # base y
    base = 34 * mm
    height = 26 * mm
    P_rt = (bx, by)                    # right angle
    P_br = (bx + base, by)             # bottom right (angle theta here)
    P_top = (bx, by + height)          # top
    c.setStrokeColor(BLACK); c.setLineWidth(1.4)
    c.line(*P_rt, *P_br)               # adjacent (bottom)
    c.line(*P_rt, *P_top)              # opposite (vertical)
    c.line(*P_br, *P_top)              # hypotenuse
    # right-angle square
    c.setLineWidth(0.8)
    c.rect(bx, by, 2.5 * mm, 2.5 * mm, fill=0, stroke=1)
    # theta arc at bottom-right
    c.setStrokeColor(GOLD); c.setLineWidth(1.2)
    c.arc(P_br[0] - 7 * mm, P_br[1] - 1 * mm, P_br[0] + 1 * mm, P_br[1] + 7 * mm, 110, 50)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 10)
    c.drawString(P_br[0] - 9 * mm, P_br[1] + 2 * mm, "\u03b8")
    # side labels
    c.setFillColor(BLACK); c.setFont("Helvetica-Oblique", 8.5)
    c.drawString(bx - 4 * mm, by + height / 2, "opp")
    c.drawCentredString(bx + base / 2, by - 4 * mm, "adj")
    c.saveState()
    c.translate(bx + base / 2 + 3 * mm, by + height / 2 + 1 * mm)
    c.rotate(37)
    c.drawCentredString(0, 0, "hyp")
    c.restoreState()
    # formula lines on the right
    fx = x + w - 33 * mm
    c.setFont("Helvetica-Bold", 9.5); c.setFillColor(BLACK)
    c.drawString(fx, by + height - 2 * mm, "sin \u03b8 = opp / hyp")
    c.drawString(fx, by + height - 8 * mm, "cos \u03b8 = adj / hyp")
    c.drawString(fx, by + height - 14 * mm, "tan \u03b8 = opp / adj")
    return y - card_h - 3 * mm


def formula_card_circle(c, x, y, w):
    """Labelled circle: radius, diameter, chord. Returns new y."""
    card_h = 52 * mm
    c.setFillColor(WHITE); c.setStrokeColor(BLUE); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    c.setFillColor(BLUE); c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 2.5 * mm, y - 5.5 * mm, "\u25cb  Circle — Parts & Formulas")
    cx = x + 22 * mm; cy = y - card_h + 24 * mm; r = 17 * mm
    c.setStrokeColor(BLACK); c.setLineWidth(1.4)
    c.circle(cx, cy, r, fill=0, stroke=1)
    # centre dot
    c.setFillColor(BLACK); c.circle(cx, cy, 0.7 * mm, fill=1, stroke=0)
    # radius
    c.setStrokeColor(GOLD); c.setLineWidth(1.3)
    c.line(cx, cy, cx + r, cy)
    c.setFillColor(GOLD); c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(cx + r / 2, cy + 1.2 * mm, "r")
    # diameter (vertical)
    c.setStrokeColor(GREEN); c.line(cx, cy - r, cx, cy + r)
    c.setFillColor(GREEN); c.drawString(cx + 1 * mm, cy + r - 4 * mm, "d")
    # chord
    c.setStrokeColor(MGRAY); c.setLineWidth(1.1)
    ang = math.radians(35)
    c.line(cx - r * math.cos(ang), cy - r * math.sin(ang),
           cx + r * math.cos(ang), cy - r * math.sin(ang))
    c.setFillColor(MGRAY); c.drawCentredString(cx, cy - r * math.sin(ang) - 4 * mm, "chord")
    # formulas
    fx = x + w - 36 * mm
    c.setFont("Helvetica-Bold", 9.5); c.setFillColor(BLACK)
    c.drawString(fx, cy + 10 * mm, "d = 2r")
    c.drawString(fx, cy + 4 * mm, "C = 2\u03c0r")
    c.drawString(fx, cy - 2 * mm, "A = \u03c0r\u00b2")
    c.setFont("Helvetica-Oblique", 8); c.setFillColor(MGRAY)
    c.drawString(fx, cy - 9 * mm, "(\u03c0 = 22/7)")
    return y - card_h - 3 * mm


# ═══════════════════════════════════════════════════════════════════════════════
# Block 3 — Quick reference table
# ═══════════════════════════════════════════════════════════════════════════════
def reference_table(c, x, y, w, title, headers, rows):
    """Draw a simple grid table. Returns new y."""
    n_cols = len(headers)
    col_w = w / n_cols
    row_h = 6 * mm
    n_rows = len(rows) + 1  # +header
    table_h = 7 * mm + n_rows * row_h
    # title
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y - 4.5 * mm, f"\u25a4  {title}")
    top = y - 7 * mm
    # header row
    c.setFillColor(LGOLD); c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.rect(x, top - row_h, w, row_h, fill=1, stroke=1)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 9)
    for i, h in enumerate(headers):
        c.drawCentredString(x + col_w * (i + 0.5), top - row_h + 1.8 * mm, str(h))
    # body
    yy = top - row_h
    c.setFont("Helvetica", 9)
    for r_i, row in enumerate(rows):
        yy -= row_h
        c.setFillColor(WHITE); c.setStrokeColor(LGRAY); c.setLineWidth(0.5)
        c.rect(x, yy, w, row_h, fill=1, stroke=1)
        c.setFillColor(BLACK)
        for i, cell in enumerate(row):
            c.drawCentredString(x + col_w * (i + 0.5), yy + 1.8 * mm, str(cell))
    # vertical separators
    c.setStrokeColor(LGRAY); c.setLineWidth(0.5)
    for i in range(1, n_cols):
        c.line(x + col_w * i, yy, x + col_w * i, top - row_h)
    return yy - 3 * mm


# ═══════════════════════════════════════════════════════════════════════════════
# Enrichment registry — which extras to draw for which worksheet
# Keyed by sublevel_code. Each returns a list of draw-callables.
# ═══════════════════════════════════════════════════════════════════════════════
def get_enrichment(sublevel_code, level_num, topic):
    """Return enrichment blocks for a given worksheet, or [] if none defined.
    Each block is a function(c, x, y, w) -> new_y."""
    if sublevel_code == "19A":   # PROTOTYPE: Trig ratios
        return [
            lambda c, x, y, w: formula_card_right_triangle(c, x, y, w),
            lambda c, x, y, w: worked_example(
                c, x, y, w, "Worked Example",
                ["Triangle: opp = 3, adj = 4, hyp = 5.",
                 "sin \u03b8 = opp/hyp = 3/5",
                 "cos \u03b8 = adj/hyp = 4/5",
                 "tan \u03b8 = opp/adj = 3/4"]),
            lambda c, x, y, w: reference_table(
                c, x, y, w, "Standard Values",
                ["\u03b8", "sin", "cos", "tan"],
                [["0\u00b0", "0", "1", "0"],
                 ["30\u00b0", "1/2", "\u221a3/2", "1/\u221a3"],
                 ["45\u00b0", "1/\u221a2", "1/\u221a2", "1"],
                 ["60\u00b0", "\u221a3/2", "1/2", "\u221a3"],
                 ["90\u00b0", "1", "0", "\u2014"]]),
        ]
    return []
