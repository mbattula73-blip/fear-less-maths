"""
Fear Less Maths — Rich Concept Page (prototype)
A full dedicated reference page added to SHEET 1 of each sublevel.
Designed to print on the back of the worksheet — a content-rich, visual,
interactive study sheet with:
  - A clear concept intro
  - A real-life example with a vector diagram
  - Two solved examples (step by step)
  - A visual concept card (drawn in vector)
  - A tips strip

All visuals drawn directly with ReportLab for crisp B&W + accent output.
Self-contained so it can be reviewed on one worksheet before rollout.
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
PINK = colors.HexColor("#C2185B")
LPINK = colors.HexColor("#FCE4EC")


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


def fraction_circle_vec(c, cx, cy, r, total, shaded, accent=GREEN):
    """Vector pie showing 'shaded' of 'total' slices filled."""
    import math as _m
    start = 90
    step = 360.0 / total
    for i in range(total):
        a0 = start - i * step
        a1 = a0 - step
        c.setStrokeColor(BLACK); c.setLineWidth(1.1)
        if i < shaded:
            c.setFillColor(accent)
        else:
            c.setFillColor(WHITE)
        # wedge via path
        p = c.beginPath()
        p.moveTo(cx, cy)
        a = a0
        p.lineTo(cx + r * _m.cos(_m.radians(a)), cy + r * _m.sin(_m.radians(a)))
        steps = max(2, int(step / 6))
        for s in range(1, steps + 1):
            aa = a0 - (step * s / steps)
            p.lineTo(cx + r * _m.cos(_m.radians(aa)), cy + r * _m.sin(_m.radians(aa)))
        p.close()
        c.drawPath(p, fill=1, stroke=1)


def fraction_bar_vec(c, x, y, w, h, total, shaded, accent=GREEN):
    """Vector bar split into 'total' cells, 'shaded' filled."""
    cell = w / total
    for i in range(total):
        c.setStrokeColor(BLACK); c.setLineWidth(1)
        c.setFillColor(accent if i < shaded else WHITE)
        c.rect(x + i * cell, y, cell, h, fill=1, stroke=1)


def two_bars_vec(c, x, y, w, h, t1, s1, t2, s2, lab1="", lab2="", accent=GOLD):
    """Two stacked comparison bars with labels. Returns total height used."""
    gap = 9 * mm
    fraction_bar_vec(c, x, y - h, w, h, t1, s1, accent=accent)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 9.5)
    if lab1: c.drawString(x, y - h - 5 * mm, lab1)
    y2 = y - h - gap - 6 * mm
    fraction_bar_vec(c, x, y2 - h, w, h, t2, s2, accent=accent)
    if lab2: c.drawString(x, y2 - h - 5 * mm, lab2)
    return h * 2 + gap + 12 * mm


def number_line_vec(c, x, y, w, ticks, marks=None, accent=GOLD):
    """Horizontal number line from 0..1 with 'ticks' divisions. marks: list of
    (index, label) to highlight. Returns height used."""
    c.setStrokeColor(BLACK); c.setLineWidth(1.3)
    c.line(x, y, x + w, y)
    # arrowheads
    c.line(x + w, y, x + w - 2 * mm, y + 1.4 * mm)
    c.line(x + w, y, x + w - 2 * mm, y - 1.4 * mm)
    step = w / ticks
    c.setFont("Helvetica", 8)
    for i in range(ticks + 1):
        tx = x + i * step
        c.setStrokeColor(BLACK); c.setLineWidth(1)
        c.line(tx, y - 1.6 * mm, tx, y + 1.6 * mm)
        c.setFillColor(MGRAY)
        if i == 0: c.drawCentredString(tx, y - 6 * mm, "0")
        elif i == ticks: c.drawCentredString(tx, y - 6 * mm, "1")
        else: c.drawCentredString(tx, y - 6 * mm, f"{i}/{ticks}")
    if marks:
        for idx, label in marks:
            mx = x + idx * step
            c.setFillColor(accent)
            c.circle(mx, y, 1.7 * mm, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(mx, y + 3 * mm, label)
    return 10 * mm


def tenths_grid_vec(c, x, y, w, h, shaded, accent=GOLD):
    """A bar split into 10 equal strips, 'shaded' filled (for tenths)."""
    cell = w / 10
    for i in range(10):
        c.setStrokeColor(BLACK); c.setLineWidth(0.9)
        c.setFillColor(accent if i < shaded else WHITE)
        c.rect(x + i * cell, y, cell, h, fill=1, stroke=1)


def hundredths_grid_vec(c, x, y, side, shaded, accent=GOLD):
    """A 10x10 grid, 'shaded' cells filled row by row (for hundredths)."""
    cell = side / 10
    k = 0
    for r in range(10):
        for col in range(10):
            c.setStrokeColor(LGRAY); c.setLineWidth(0.5)
            c.setFillColor(accent if k < shaded else WHITE)
            c.rect(x + col * cell, y + (9 - r) * cell, cell, cell, fill=1, stroke=1)
            k += 1
    # outer border
    c.setStrokeColor(BLACK); c.setLineWidth(1.1)
    c.rect(x, y, side, side, fill=0, stroke=1)


def int_line_vec(c, x, y, w, lo, hi, marks=None, jump=None):
    """Integer number line from lo..hi. marks: list of (value,label).
    jump: optional (start, delta, label) draws an arrow showing movement."""
    n = hi - lo
    step = w / n
    c.setStrokeColor(BLACK); c.setLineWidth(1.3)
    c.line(x, y, x + w, y)
    c.line(x, y, x + 2 * mm, y + 1.4 * mm); c.line(x, y, x + 2 * mm, y - 1.4 * mm)
    c.line(x + w, y, x + w - 2 * mm, y + 1.4 * mm); c.line(x + w, y, x + w - 2 * mm, y - 1.4 * mm)
    c.setFont("Helvetica", 7.5)
    for i in range(n + 1):
        v = lo + i
        tx = x + i * step
        c.setStrokeColor(BLACK); c.setLineWidth(1.6 if v == 0 else 1)
        c.line(tx, y - 1.8 * mm, tx, y + 1.8 * mm)
        c.setFillColor(BLACK if v == 0 else MGRAY)
        c.drawCentredString(tx, y - 6 * mm, str(v))
    if jump:
        s, d, lab = jump
        sx = x + (s - lo) * step
        ex = x + (s + d - lo) * step
        ay = y + 8 * mm
        c.setStrokeColor(GOLD); c.setLineWidth(1.4)
        c.line(sx, ay, ex, ay)
        dr = 1 if d > 0 else -1
        c.line(ex, ay, ex - dr * 2 * mm, ay + 1.4 * mm)
        c.line(ex, ay, ex - dr * 2 * mm, ay - 1.4 * mm)
        c.setLineWidth(0.5); c.setStrokeColor(LGRAY)
        c.line(sx, y, sx, ay); c.line(ex, y, ex, ay)
        c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString((sx + ex) / 2, ay + 1.5 * mm, lab)
    if marks:
        for v, label in marks:
            mx = x + (v - lo) * step
            c.setFillColor(GOLD)
            c.circle(mx, y, 1.7 * mm, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(mx, y + 3 * mm, label)
    return 12 * mm


def sign_rule_vec(c, x, y, w, pairs):
    """Grid of sign rules: list of (rule_text, result). Returns height used."""
    rh = 7 * mm
    cw = w / 2
    c.setFont("Helvetica-Bold", 10)
    for i, (rule, res) in enumerate(pairs):
        col = i % 2; row = i // 2
        bx = x + col * cw; by = y - (row + 1) * rh
        pos = res.strip().startswith("+")
        c.setFillColor(LGREEN if pos else LPINK)
        c.setStrokeColor(GREEN if pos else PINK)
        c.setLineWidth(0.8)
        c.rect(bx, by, cw - 2 * mm, rh - 1.5 * mm, fill=1, stroke=1)
        c.setFillColor(BLACK)
        c.drawString(bx + 2.5 * mm, by + 1.8 * mm, f"{rule} = {res}")
    rows = (len(pairs) + 1) // 2
    return rows * rh + 2 * mm


def place_value_vec(c, x, y, w, headers, digits):
    """Place-value chart with a decimal point column. headers/digits lists."""
    n = len(headers)
    cw = w / n
    rh = 7 * mm
    # header row
    c.setFillColor(LBLUE); c.setStrokeColor(BLUE); c.setLineWidth(0.8)
    c.rect(x, y - rh, w, rh, fill=1, stroke=1)
    c.setFillColor(BLUE); c.setFont("Helvetica-Bold", 8)
    for i, hd in enumerate(headers):
        c.drawCentredString(x + cw * (i + 0.5), y - rh + 1.8 * mm, hd)
    # digit row
    c.setFillColor(WHITE); c.setStrokeColor(BLUE)
    c.rect(x, y - 2 * rh, w, rh, fill=1, stroke=1)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    for i, dg in enumerate(digits):
        c.drawCentredString(x + cw * (i + 0.5), y - 2 * rh + 1.6 * mm, dg)
    # column separators
    c.setStrokeColor(LGRAY); c.setLineWidth(0.4)
    for i in range(1, n):
        c.line(x + cw * i, y - 2 * rh, x + cw * i, y)
    return 2 * rh + 2 * mm


# ───────────────────────────────────────────────────────────────────────────────
# The page renderer (uses host engine's frame helpers passed in)
# ───────────────────────────────────────────────────────────────────────────────
def render_rich_concept_page(c, spec, frame):
    """
    Draw a full rich concept page (~60% diagrams, 40% short bullet content).
    spec keys: title, intro (list[str] short), real_life (list of up to 3 dicts),
          card (callable or None), solved (list[dict]), tips (list[str]).
    """
    LXc = frame["LX"]; RXc = frame["RX"]; CW = frame["CW"]
    TOP = frame["P_TOP"]; BOT = frame["P_BOT"]; BW = frame["BW"]

    # faint vertical divider between columns
    midx = (LXc + CW + RXc) / 2
    c.setStrokeColor(LGRAY); c.setLineWidth(0.4)
    c.line(midx, TOP, midx, BOT)

    # ════════════ LEFT COLUMN ════════════
    ly = TOP - 1 * mm
    # Concept intro — short bullets
    ly = _section_band(c, LXc, ly, CW, "\u25c9  What is it?", BLUE, LBLUE)
    ly = _bullets(c, LXc, ly - 1 * mm, CW, spec["intro"], size=11)
    ly -= 2 * mm

    # Picture-it concept card (big visual)
    if spec.get("card"):
        ly = _section_band(c, LXc, ly, CW, "\u25a3  Picture It", GREEN, LGREEN)
        ly = spec["card"](c, LXc, ly - 1 * mm, CW)
        ly -= 2 * mm

    # Quick tips — short bullets
    if spec.get("tips"):
        ly = _section_band(c, LXc, ly, CW, "\u2605  Quick Tips", BLUE, LBLUE)
        ly = _bullets(c, LXc, ly - 1 * mm, CW, spec["tips"], size=10.5)

    # ════════════ RIGHT COLUMN ════════════
    ry = TOP - 1 * mm
    # Three real-life examples, each with its own diagram
    ry = _section_band(c, RXc, ry, CW, "\u25c8  Real-life Examples", GOLD, LGOLD)
    ry -= 1 * mm
    for rl in spec.get("real_life", [])[:3]:
        # short caption line(s)
        c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 9)
        for ln in _wrap(rl["text"], "Helvetica-Bold", 9, CW):
            c.drawString(RXc, ry, ln); ry -= 4.2 * mm
        ry -= 1 * mm
        # diagram, drawn centered
        dh = _draw_example_diagram(c, RXc, ry, CW, rl)
        ry -= dh + 3 * mm

    # Solved examples (compact) below the real-life ones if room
    if spec.get("solved") and ry > BOT + 36 * mm:
        ry = _section_band(c, RXc, ry, CW, "\u270e  Solved Examples", PINK, LPINK)
        ry -= 1 * mm
        for ex in spec["solved"]:
            if ry < BOT + 14 * mm: break
            c.setFillColor(PINK); c.setFont("Helvetica-Bold", 8.5)
            for ln in _wrap(ex["q"], "Helvetica-Bold", 8.5, CW):
                c.drawString(RXc, ry, ln); ry -= 4.0 * mm
            c.setFillColor(BLACK); c.setFont("Helvetica", 8.5)
            for step in ex["steps"]:
                for ln in _wrap(step, "Helvetica", 8.5, CW - 3 * mm):
                    c.drawString(RXc + 3 * mm, ry, ln); ry -= 4.0 * mm
            ry -= 1.2 * mm

    # ════════════ TRY IT YOURSELF — fills bottom, spans both columns ════════════
    ty = min(ly, ry)
    if spec.get("try_it") and ty > BOT + 22 * mm:
        full_w = (RXc + CW) - LXc
        box_h = ty - BOT - 2 * mm
        box_h = min(box_h, 34 * mm)
        by = ty - box_h
        c.setFillColor(colors.HexColor("#FFFDF5")); c.setStrokeColor(GOLD); c.setLineWidth(1.2)
        c.roundRect(LXc, by, full_w, box_h, 2 * mm, fill=1, stroke=1)
        c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 11)
        c.drawString(LXc + 3 * mm, ty - 5.5 * mm, "\u270e  Try it Yourself")
        c.setFillColor(BLACK); c.setFont("Helvetica", 10)
        yy = ty - 11 * mm
        for t in spec["try_it"]["questions"]:
            for ln in _wrap(t, "Helvetica", 10, full_w - 6 * mm):
                c.drawString(LXc + 4 * mm, yy, ln); yy -= 5 * mm
        # tiny answers line at the very bottom
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 8)
        c.drawString(LXc + 4 * mm, by + 2.5 * mm, "Answers: " + spec["try_it"]["answers"])


def _bullets(c, x, y, w, items, size=10):
    """Short bullet points. Returns new y."""
    c.setFillColor(BLACK); c.setFont("Helvetica", size)
    yy = y
    lh = (size + 2.4) * 0.353 * mm * 4  # comfortable leading
    lh = (size * 1.45) * 0.3528 * mm
    for t in items:
        wrapped = _wrap("\u2022 " + t, "Helvetica", size, w - 1 * mm)
        for j, ln in enumerate(wrapped):
            c.drawString(x + (0 if j == 0 else 2.5 * mm), yy, ln)
            yy -= (size * 1.5) * 0.3528 * mm
        yy -= 0.8 * mm
    return yy


def _draw_example_diagram(c, x, y, w, rl):
    """Draw the diagram for one real-life example. Returns the height used."""
    cxm = x + w / 2
    kind = rl.get("diagram")
    if kind == "fraction_circle":
        fraction_circle_vec(c, cxm, y - 22 * mm, 20 * mm,
                            rl["total"], rl["shaded"], accent=GOLD)
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - 47 * mm, rl.get("caption", ""))
        return 52 * mm
    if kind == "fraction_bar":
        bw = w - 8 * mm
        fraction_bar_vec(c, x + 4 * mm, y - 16 * mm, bw, 14 * mm,
                        rl["total"], rl["shaded"], accent=GOLD)
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - 25 * mm, rl.get("caption", ""))
        return 30 * mm
    if kind == "fraction_grid":
        total = rl["total"]; shaded = rl["shaded"]
        cols = rl.get("cols", total); rows = max(1, total // cols)
        gw = w - 8 * mm; gh = 28 * mm
        cw = gw / cols; ch = gh / rows
        gx = x + 4 * mm; gy = y - 2 * mm - gh
        k = 0
        for rr in range(rows):
            for cc in range(cols):
                c.setStrokeColor(BLACK); c.setLineWidth(1)
                c.setFillColor(GOLD if k < shaded else WHITE)
                c.rect(gx + cc * cw, gy + (rows - 1 - rr) * ch, cw, ch, fill=1, stroke=1)
                k += 1
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, gy - 7 * mm, rl.get("caption", ""))
        return gh + 13 * mm
    if kind == "two_bars":
        used = two_bars_vec(c, x + 4 * mm, y, w - 8 * mm, 11 * mm,
                            rl["t1"], rl["s1"], rl["t2"], rl["s2"],
                            rl.get("lab1", ""), rl.get("lab2", ""), accent=GOLD)
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - used - 1 * mm, rl.get("caption", ""))
        return used + 6 * mm
    if kind == "number_line":
        used = number_line_vec(c, x + 6 * mm, y - 8 * mm, w - 12 * mm,
                               rl["ticks"], rl.get("marks"), accent=GOLD)
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - 20 * mm, rl.get("caption", ""))
        return 24 * mm
    if kind == "tenths_grid":
        tenths_grid_vec(c, x + 4 * mm, y - 13 * mm, w - 8 * mm, 12 * mm,
                       rl["shaded"], accent=GOLD)
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - 20 * mm, rl.get("caption", ""))
        return 24 * mm
    if kind == "hundredths_grid":
        side = 30 * mm
        hundredths_grid_vec(c, cxm - side / 2, y - 2 * mm - side, side,
                           rl["shaded"], accent=GOLD)
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - side - 7 * mm, rl.get("caption", ""))
        return side + 11 * mm
    if kind == "place_value":
        used = place_value_vec(c, x + 4 * mm, y, w - 8 * mm,
                              rl["headers"], rl["digits"])
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - used - 2 * mm, rl.get("caption", ""))
        return used + 7 * mm
    if kind == "integer_line":
        used = int_line_vec(c, x + 5 * mm, y - 10 * mm, w - 10 * mm,
                           rl["lo"], rl["hi"], rl.get("marks"), rl.get("jump"))
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - 24 * mm, rl.get("caption", ""))
        return 28 * mm
    if kind == "sign_rule":
        used = sign_rule_vec(c, x + 4 * mm, y - 2 * mm, w - 8 * mm, rl["pairs"])
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - used - 4 * mm, rl.get("caption", ""))
        return used + 8 * mm
    return 0


def _section_band(c, x, y, w, text, accent, light):
    h = 7 * mm
    c.setFillColor(light); c.setStrokeColor(accent); c.setLineWidth(1)
    c.roundRect(x, y - h, w, h, 1.5 * mm, fill=1, stroke=1)
    c.setFillColor(accent); c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 2.5 * mm, y - 5 * mm, text)
    return y - h - 2 * mm


# ───────────────────────────────────────────────────────────────────────────────
# Concept card drawings (vector), keyed by topic
# ───────────────────────────────────────────────────────────────────────────────
def card_fraction(c, x, y, w):
    """Show a fraction visually: bar + circle + the parts labelled."""
    card_h = 78 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    # 3/4 bar (large)
    bx = x + 5 * mm; bw = w - 10 * mm
    fraction_bar_vec(c, bx, y - 20 * mm, bw, 15 * mm, 4, 3, accent=GREEN)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 12)
    c.drawString(bx, y - 29 * mm, "3 shaded of 4 parts  =  3/4")
    # numerator / denominator labels
    c.setFont("Helvetica-Oblique", 10); c.setFillColor(MGRAY)
    c.drawString(bx, y - 38 * mm, "top number (numerator) = parts taken")
    c.drawString(bx, y - 45 * mm, "bottom (denominator) = equal parts")
    # mini circle 1/2 (bigger)
    fraction_circle_vec(c, x + w - 18 * mm, y - 64 * mm, 11 * mm, 2, 1, accent=GREEN)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, y - 62 * mm, "Half a circle")
    c.drawString(bx, y - 69 * mm, "= 1/2")
    return y - card_h - 2 * mm


def card_proper_improper(c, x, y, w):
    """Bars showing proper (<1) vs improper (>1)."""
    card_h = 70 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    # proper 2/5
    fraction_bar_vec(c, bx, y - 16 * mm, bw, 12 * mm, 5, 2, accent=GREEN)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, y - 23 * mm, "Proper: 2/5  (top < bottom, less than 1)")
    # improper 7/5 -> one full bar + 2/5
    fraction_bar_vec(c, bx, y - 40 * mm, bw, 12 * mm, 5, 5, accent=GREEN)
    fraction_bar_vec(c, bx, y - 55 * mm, bw, 12 * mm, 5, 2, accent=GREEN)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, y - 62 * mm, "Improper: 7/5 = 1 whole + 2/5")
    return y - card_h - 2 * mm


def card_equivalent(c, x, y, w):
    """Two bars of equal shaded area showing 1/2 = 2/4."""
    card_h = 64 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    fraction_bar_vec(c, bx, y - 16 * mm, bw, 12 * mm, 2, 1, accent=GREEN)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, y - 23 * mm, "1/2")
    fraction_bar_vec(c, bx, y - 40 * mm, bw, 12 * mm, 4, 2, accent=GREEN)
    c.drawString(bx, y - 47 * mm, "2/4  (same shaded area!)")
    c.setFont("Helvetica-Bold", 12); c.setFillColor(GREEN)
    c.drawCentredString(x + w / 2, y - 57 * mm, "1/2 = 2/4 = 3/6   (equivalent)")
    return y - card_h - 2 * mm


def card_add_sub(c, x, y, w):
    """Show 1/5 + 2/5 = 3/5 visually with bars."""
    card_h = 64 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    fraction_bar_vec(c, bx, y - 15 * mm, bw, 10 * mm, 5, 1, accent=GREEN)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, y - 21 * mm, "1/5")
    fraction_bar_vec(c, bx, y - 34 * mm, bw, 10 * mm, 5, 2, accent=GREEN)
    c.drawString(bx, y - 40 * mm, "+ 2/5")
    fraction_bar_vec(c, bx, y - 53 * mm, bw, 10 * mm, 5, 3, accent=GOLD)
    c.setFont("Helvetica-Bold", 12); c.setFillColor(GREEN)
    c.drawString(bx, y - 59 * mm, "= 3/5  (same bottom, add tops)")
    return y - card_h - 2 * mm


def card_mixed(c, x, y, w):
    """Mixed number: 1 whole + 3/4 = 1 3/4."""
    card_h = 60 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    fraction_bar_vec(c, bx, y - 16 * mm, bw, 12 * mm, 4, 4, accent=GREEN)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, y - 23 * mm, "1 whole (4/4)")
    fraction_bar_vec(c, bx, y - 40 * mm, bw, 12 * mm, 4, 3, accent=GOLD)
    c.drawString(bx, y - 47 * mm, "+ 3/4")
    c.setFont("Helvetica-Bold", 13); c.setFillColor(GREEN)
    c.drawCentredString(x + w / 2, y - 55 * mm, "= 1\u00be  (mixed number)")
    return y - card_h - 2 * mm


def card_decimal_place(c, x, y, w):
    """Place-value card: tens . tenths hundredths, with 3.45 example."""
    card_h = 66 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 4 * mm; bw = w - 8 * mm
    # place value chart for 3.45
    place_value_vec(c, bx, y - 4 * mm, bw,
                    ["Ones", ".", "Tenths", "Hund"], ["3", ".", "4", "5"])
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 12)
    c.drawString(bx, y - 26 * mm, "3.45")
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawString(bx, y - 33 * mm, "3 ones, 4 tenths, 5 hundredths")
    c.drawString(bx, y - 39 * mm, "The dot is the DECIMAL POINT.")
    # tenths bar showing 0.4
    tenths_grid_vec(c, bx, y - 52 * mm, bw, 9 * mm, 4, accent=GREEN)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 10)
    c.drawString(bx, y - 60 * mm, "0.4 = 4 of 10 strips = 4 tenths")
    return y - card_h - 2 * mm


def card_decimal_grid(c, x, y, w):
    """Hundredths grid showing 0.30 = 30/100 and tenths equivalence."""
    card_h = 64 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    side = 38 * mm
    gx = x + 6 * mm; gy = y - 8 * mm - side
    hundredths_grid_vec(c, gx, gy, side, 30, accent=GREEN)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    tx = gx + side + 6 * mm
    c.drawString(tx, y - 16 * mm, "0.30")
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawString(tx, y - 24 * mm, "30 of 100")
    c.drawString(tx, y - 30 * mm, "small squares")
    c.setFont("Helvetica-Bold", 11); c.setFillColor(GREEN)
    c.drawString(tx, y - 40 * mm, "0.30 = 0.3")
    c.drawString(tx, y - 47 * mm, "= 3/10")
    return y - card_h - 2 * mm


def card_frac_to_dec(c, x, y, w):
    """Fraction-to-decimal: 1/2 = 0.5 with a half-shaded bar."""
    card_h = 60 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    fraction_bar_vec(c, bx, y - 16 * mm, bw, 11 * mm, 2, 1, accent=GREEN)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, y - 23 * mm, "1/2 = 5/10 = 0.5")
    fraction_bar_vec(c, bx, y - 38 * mm, bw, 11 * mm, 4, 1, accent=GOLD)
    c.drawString(bx, y - 45 * mm, "1/4 = 25/100 = 0.25")
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawString(bx, y - 53 * mm, "Tip: divide top by bottom (1 \u00f7 2 = 0.5)")
    return y - card_h - 2 * mm


def card_integer_line(c, x, y, w):
    """Big integer number line centred on 0, negatives left, positives right."""
    card_h = 56 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    int_line_vec(c, bx, y - 16 * mm, bw, -5, 5, marks=[(-3, "-3"), (4, "+4")])
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 10)
    c.drawString(bx, y - 26 * mm, "Left of 0 = negative (-)")
    c.drawString(bx, y - 32 * mm, "Right of 0 = positive (+)")
    c.drawString(bx, y - 38 * mm, "0 is neither + nor -")
    c.setFont("Helvetica-Oblique", 9.5); c.setFillColor(MGRAY)
    c.drawString(bx, y - 46 * mm, "Bigger number is further RIGHT.")
    c.drawString(bx, y - 52 * mm, "So -3 < -1 < 0 < 2 < 4")
    return y - card_h - 2 * mm


def card_int_addsub(c, x, y, w):
    """Add/subtract on a number line: 7 + (-4) = 3."""
    card_h = 58 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    int_line_vec(c, bx, y - 18 * mm, bw, -2, 8, jump=(7, -4, "-4"), marks=[(3, "3")])
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, y - 30 * mm, "7 + (-4) = 3")
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawString(bx, y - 38 * mm, "Add a positive \u2192 move RIGHT.")
    c.drawString(bx, y - 44 * mm, "Add a negative \u2192 move LEFT.")
    c.drawString(bx, y - 50 * mm, "Subtract = add the opposite.")
    return y - card_h - 2 * mm


def card_int_signs(c, x, y, w):
    """Sign rules for multiply/divide."""
    card_h = 56 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, y - 8 * mm, "Multiply / Divide sign rules:")
    sign_rule_vec(c, bx, y - 11 * mm, bw,
                  [("(+)(+)", "+"), ("(-)(-)", "+"),
                   ("(+)(-)", "-"), ("(-)(+)", "-")])
    c.setFont("Helvetica-Bold", 10); c.setFillColor(GREEN)
    c.drawString(bx, y - 44 * mm, "Same signs \u2192 +")
    c.setFillColor(PINK)
    c.drawString(bx, y - 50 * mm, "Different signs \u2192 -")
    return y - card_h - 2 * mm


# ───────────────────────────────────────────────────────────────────────────────
# Registry — rich concept content per sublevel (sheet 1 only)
# ───────────────────────────────────────────────────────────────────────────────
def get_concept_page(sublevel_code, level_num, topic):
    """Return a spec dict for the rich concept page, or None if not defined."""
    if level_num == 6:
        return _L6.get(sublevel_code)
    if level_num == 7:
        return _L7.get(sublevel_code)
    if level_num == 8:
        return _L8.get(sublevel_code)
    return None


# ───────────────────────────────────────────────────────────────────────────────
# LEVEL 6 — Fractions: concept page specs (sheet 1 of each sublevel)
# ───────────────────────────────────────────────────────────────────────────────
_L6 = {
    # ---- 6A Fraction concept ----
    "6A": {
        "title": "Fractions — Concept",
        "intro": [
            "A fraction = part of a whole.",
            "Split the whole into EQUAL parts.",
            "Top number = parts we take.",
            "Bottom number = total equal parts.",
            "Example: 3/4 means 3 parts out of 4.",
        ],
        "real_life": [
            {"text": "1. Pizza: cut into 4, you eat 3 \u2192 3/4",
             "diagram": "fraction_circle", "total": 4, "shaded": 3,
             "caption": "3 of 4 slices eaten = 3/4"},
            {"text": "2. Chocolate bar: 6 pieces, eat 2 \u2192 2/6",
             "diagram": "fraction_bar", "total": 6, "shaded": 2,
             "caption": "2 of 6 pieces = 2/6 = 1/3"},
            {"text": "3. Window: 8 panes, 5 are open \u2192 5/8",
             "diagram": "fraction_grid", "total": 8, "shaded": 5, "cols": 4,
             "caption": "5 of 8 panes open = 5/8"},
        ],
        "card": card_fraction,
        "solved": [
            {"q": "Ex: Ribbon cut in 5 parts, 3 red. Red fraction?",
             "steps": ["Red = 3, total = 5", "Answer = 3/5"]},
        ],
        "tips": [
            "Parts must be EQUAL.",
            "Top = numerator, bottom = denominator.",
            "Top = bottom \u2192 equals 1 whole.",
            "Cancel common factors to simplify.",
        ],
        "try_it": {
            "questions": [
                "1. A cake is cut into 8 equal slices. You eat 3. What fraction did you eat?",
                "2. A box has 10 eggs. 7 are brown. What fraction is brown?",
                "3. Colour 2 of 5 equal boxes. What fraction is coloured?",
            ],
            "answers": "1) 3/8    2) 7/10    3) 2/5",
        },
    },

    # ---- 6B Proper / improper ----
    "6B": {
        "title": "Proper & Improper Fractions",
        "intro": [
            "Proper fraction: top < bottom (less than 1).",
            "Improper fraction: top \u2265 bottom (1 or more).",
            "Example: 3/5 is proper; 7/5 is improper.",
            "9/9 = 1 whole (top = bottom).",
            "Improper fractions can become mixed numbers.",
        ],
        "real_life": [
            {"text": "1. Half a glass of juice \u2192 1/2 (proper)",
             "diagram": "fraction_bar", "total": 2, "shaded": 1,
             "caption": "1/2 < 1, so proper"},
            {"text": "2. One full + half pizza \u2192 3/2 (improper)",
             "diagram": "fraction_circle", "total": 2, "shaded": 2,
             "caption": "more than 1 whole = improper"},
            {"text": "3. 5 quarter-slices of bread \u2192 5/4 (improper)",
             "diagram": "fraction_grid", "total": 4, "shaded": 4, "cols": 4,
             "caption": "4/4 = 1 whole, plus more = improper"},
        ],
        "card": card_proper_improper,
        "solved": [
            {"q": "Ex: Is 9/9 proper or improper?",
             "steps": ["Top = bottom (9 = 9)", "Equals 1 whole \u2192 improper"]},
        ],
        "tips": [
            "Top < bottom \u2192 proper.",
            "Top = or > bottom \u2192 improper.",
            "Improper \u2265 1 whole.",
            "Every whole number is improper (e.g. 2 = 6/3).",
        ],
        "try_it": {
            "questions": [
                "1. Is 4/7 proper or improper?",
                "2. Is 11/8 proper or improper?",
                "3. Is 6/6 proper or improper?",
            ],
            "answers": "1) proper    2) improper    3) improper (= 1)",
        },
    },

    # ---- 6C Equivalent fractions ----
    "6C": {
        "title": "Equivalent Fractions",
        "intro": [
            "Equivalent = same value, different numbers.",
            "Multiply top AND bottom by the same number.",
            "Or divide top AND bottom by the same number.",
            "Example: 1/2 = 2/4 = 3/6.",
            "The shaded amount stays the same.",
        ],
        "real_life": [
            {"text": "1. Half a chocolate = 2 of 4 pieces \u2192 1/2 = 2/4",
             "diagram": "two_bars", "t1": 2, "s1": 1, "t2": 4, "s2": 2,
             "lab1": "1/2", "lab2": "2/4", "caption": "same shaded length"},
            {"text": "2. Half a pizza = 3 of 6 slices \u2192 1/2 = 3/6",
             "diagram": "fraction_circle", "total": 6, "shaded": 3,
             "caption": "3/6 = 1/2"},
            {"text": "3. 2/3 of a tray = 4/6 \u2192 multiply by 2",
             "diagram": "two_bars", "t1": 3, "s1": 2, "t2": 6, "s2": 4,
             "lab1": "2/3", "lab2": "4/6", "caption": "2/3 = 4/6"},
        ],
        "card": card_equivalent,
        "solved": [
            {"q": "Ex: 1/3 = ?/6",
             "steps": ["Bottom \u00d72 (3\u00d72=6)", "So top \u00d72 (1\u00d72=2)", "Answer = 2/6"]},
        ],
        "tips": [
            "Do the SAME to top and bottom.",
            "Multiply up, or divide down.",
            "Simplest form: divide by common factor.",
            "Cross-check: shaded area is equal.",
        ],
        "try_it": {
            "questions": [
                "1. 1/2 = ?/8",
                "2. 2/3 = ?/9",
                "3. Simplify 6/8 to simplest form.",
            ],
            "answers": "1) 4/8    2) 6/9    3) 3/4",
        },
    },

    # ---- 6CUM1 Mixed A+B+C ----
    "6CUM1": {
        "title": "Review: Concept, Proper/Improper, Equivalent",
        "intro": [
            "A fraction = equal part of a whole.",
            "Proper: top < bottom. Improper: top \u2265 bottom.",
            "Equivalent: same value (1/2 = 2/4).",
            "Same change to top and bottom keeps value.",
            "Simplify by dividing common factors.",
        ],
        "real_life": [
            {"text": "1. 3 of 4 slices eaten \u2192 3/4 (proper)",
             "diagram": "fraction_circle", "total": 4, "shaded": 3,
             "caption": "3/4 proper"},
            {"text": "2. 5 quarter-pieces \u2192 5/4 (improper)",
             "diagram": "fraction_bar", "total": 4, "shaded": 4,
             "caption": "4/4 = 1, plus more = improper"},
            {"text": "3. 1/2 = 2/4 (equivalent)",
             "diagram": "two_bars", "t1": 2, "s1": 1, "t2": 4, "s2": 2,
             "lab1": "1/2", "lab2": "2/4", "caption": "equal shaded"},
        ],
        "card": card_equivalent,
        "solved": [
            {"q": "Ex: Is 8/5 proper? Write an equal fraction.",
             "steps": ["8 > 5 \u2192 improper", "8/5 = 16/10 (\u00d72)"]},
        ],
        "tips": [
            "Equal parts only.",
            "Compare top vs bottom for proper/improper.",
            "Same \u00d7 or \u00f7 for equivalents.",
            "Always simplify the final answer.",
        ],
        "try_it": {
            "questions": [
                "1. Is 7/4 proper or improper?",
                "2. 2/5 = ?/10",
                "3. Simplify 4/8.",
            ],
            "answers": "1) improper    2) 4/10    3) 1/2",
        },
    },

    # ---- 6D Comparison ----
    "6D": {
        "title": "Comparing Fractions",
        "intro": [
            "Same bottom: bigger top = bigger fraction.",
            "Example: 5/7 > 3/7.",
            "Different bottoms: make them equal first.",
            "Use a number line to see which is bigger.",
            "Equal fractions: use the = sign.",
        ],
        "real_life": [
            {"text": "1. 3/7 vs 5/7 of a bar \u2192 5/7 is bigger",
             "diagram": "two_bars", "t1": 7, "s1": 3, "t2": 7, "s2": 5,
             "lab1": "3/7", "lab2": "5/7", "caption": "more shaded = bigger"},
            {"text": "2. 1/2 vs 3/4 on a number line",
             "diagram": "number_line", "ticks": 4,
             "marks": [(2, "1/2"), (3, "3/4")], "caption": "3/4 is further right"},
            {"text": "3. 2/3 vs 2/5 \u2192 fewer parts = bigger piece",
             "diagram": "two_bars", "t1": 3, "s1": 2, "t2": 5, "s2": 2,
             "lab1": "2/3", "lab2": "2/5", "caption": "2/3 > 2/5"},
        ],
        "card": card_equivalent,
        "solved": [
            {"q": "Ex: Compare 3/4 and 2/3.",
             "steps": ["LCM of 4,3 = 12", "3/4 = 9/12, 2/3 = 8/12", "9 > 8 \u2192 3/4 > 2/3"]},
        ],
        "tips": [
            "Same bottom \u2192 compare tops.",
            "Different bottoms \u2192 make equal first.",
            "Number line: right = bigger.",
            "Same top \u2192 smaller bottom is bigger.",
        ],
        "try_it": {
            "questions": [
                "1. Which is bigger: 4/9 or 7/9?",
                "2. Compare 1/2 and 2/5.",
                "3. Which is bigger: 3/5 or 3/8?",
            ],
            "answers": "1) 7/9    2) 1/2 > 2/5    3) 3/5",
        },
    },

    # ---- 6E Addition ----
    "6E": {
        "title": "Adding Fractions",
        "intro": [
            "Same bottom: add the tops, keep the bottom.",
            "Example: 1/5 + 2/5 = 3/5.",
            "Different bottoms: make them equal first.",
            "Simplify the answer if you can.",
            "The bottom number never gets added.",
        ],
        "real_life": [
            {"text": "1. 1/5 + 2/5 of a bar = 3/5",
             "diagram": "fraction_bar", "total": 5, "shaded": 3,
             "caption": "1/5 + 2/5 = 3/5"},
            {"text": "2. 1/4 + 1/4 of a pizza = 2/4 = 1/2",
             "diagram": "fraction_circle", "total": 4, "shaded": 2,
             "caption": "2/4 = 1/2"},
            {"text": "3. 3/8 + 4/8 cake = 7/8",
             "diagram": "fraction_grid", "total": 8, "shaded": 7, "cols": 4,
             "caption": "3/8 + 4/8 = 7/8"},
        ],
        "card": card_add_sub,
        "solved": [
            {"q": "Ex: 3/8 + 4/8 = ?",
             "steps": ["Same bottom (8)", "Add tops: 3+4 = 7", "Answer = 7/8"]},
        ],
        "tips": [
            "Add tops only when bottoms match.",
            "Keep the bottom the same.",
            "Different bottoms \u2192 equalise first.",
            "Simplify at the end.",
        ],
        "try_it": {
            "questions": [
                "1. 2/7 + 3/7 = ?",
                "2. 1/6 + 2/6 = ? (simplify)",
                "3. 1/2 + 1/4 = ?",
            ],
            "answers": "1) 5/7    2) 3/6 = 1/2    3) 3/4",
        },
    },

    # ---- 6F Subtraction ----
    "6F": {
        "title": "Subtracting Fractions",
        "intro": [
            "Same bottom: subtract the tops, keep bottom.",
            "Example: 5/7 \u2212 2/7 = 3/7.",
            "Different bottoms: make them equal first.",
            "Simplify the answer if you can.",
            "The bottom never changes when bottoms match.",
        ],
        "real_life": [
            {"text": "1. 5/7 \u2212 2/7 of a ribbon = 3/7",
             "diagram": "fraction_bar", "total": 7, "shaded": 3,
             "caption": "what is left = 3/7"},
            {"text": "2. 3/4 \u2212 1/4 pizza = 2/4 = 1/2",
             "diagram": "fraction_circle", "total": 4, "shaded": 2,
             "caption": "2/4 = 1/2 left"},
            {"text": "3. 8/8 \u2212 3/8 chocolate = 5/8 left",
             "diagram": "fraction_grid", "total": 8, "shaded": 5, "cols": 4,
             "caption": "5/8 remaining"},
        ],
        "card": card_add_sub,
        "solved": [
            {"q": "Ex: 7/9 \u2212 4/9 = ?",
             "steps": ["Same bottom (9)", "Subtract tops: 7\u22124 = 3", "Answer = 3/9 = 1/3"]},
        ],
        "tips": [
            "Subtract tops only when bottoms match.",
            "Keep the bottom the same.",
            "Different bottoms \u2192 equalise first.",
            "Simplify at the end.",
        ],
        "try_it": {
            "questions": [
                "1. 8/11 \u2212 3/11 = ?",
                "2. 5/6 \u2212 1/6 = ? (simplify)",
                "3. 3/4 \u2212 1/2 = ?",
            ],
            "answers": "1) 5/11    2) 4/6 = 2/3    3) 1/4",
        },
    },

    # ---- 6CUM2 Mixed D+E+F ----
    "6CUM2": {
        "title": "Review: Compare, Add, Subtract",
        "intro": [
            "Compare: same bottom \u2192 bigger top wins.",
            "Add: same bottom \u2192 add tops.",
            "Subtract: same bottom \u2192 subtract tops.",
            "Different bottoms \u2192 make them equal first.",
            "Always simplify the final answer.",
        ],
        "real_life": [
            {"text": "1. 3/8 vs 5/8 \u2192 5/8 bigger",
             "diagram": "two_bars", "t1": 8, "s1": 3, "t2": 8, "s2": 5,
             "lab1": "3/8", "lab2": "5/8", "caption": "more shaded = bigger"},
            {"text": "2. 1/5 + 2/5 = 3/5",
             "diagram": "fraction_bar", "total": 5, "shaded": 3,
             "caption": "add tops = 3/5"},
            {"text": "3. 3/4 \u2212 1/4 = 2/4 = 1/2",
             "diagram": "fraction_circle", "total": 4, "shaded": 2,
             "caption": "1/2 left"},
        ],
        "card": card_add_sub,
        "solved": [
            {"q": "Ex: 5/6 \u2212 2/6, then compare with 1/2.",
             "steps": ["5/6 \u2212 2/6 = 3/6 = 1/2", "So it equals 1/2"]},
        ],
        "tips": [
            "Match bottoms before + or \u2212.",
            "Compare tops when bottoms match.",
            "Keep bottom; act on tops.",
            "Simplify the result.",
        ],
        "try_it": {
            "questions": [
                "1. Which is bigger: 2/9 or 5/9?",
                "2. 2/7 + 4/7 = ?",
                "3. 7/8 \u2212 3/8 = ? (simplify)",
            ],
            "answers": "1) 5/9    2) 6/7    3) 4/8 = 1/2",
        },
    },

    # ---- 6G Word problems ----
    "6G": {
        "title": "Fraction Word Problems",
        "intro": [
            "\u2018Fraction of\u2019 means multiply.",
            "Step 1: find the fraction of the total.",
            "2/3 of 30 = 30 \u00f7 3 \u00d7 2 = 20.",
            "Divide by the bottom, times the top.",
            "Answer in the right units (students, Rs...).",
        ],
        "real_life": [
            {"text": "1. Class of 30, 2/3 are girls \u2192 20 girls",
             "diagram": "fraction_bar", "total": 3, "shaded": 2,
             "caption": "2/3 of 30 = 20"},
            {"text": "2. 40 marbles, 3/8 red \u2192 15 red",
             "diagram": "fraction_grid", "total": 8, "shaded": 3, "cols": 4,
             "caption": "3/8 of 40 = 15"},
            {"text": "3. Rs 180, spent 5/9 \u2192 Rs 100 spent",
             "diagram": "fraction_bar", "total": 9, "shaded": 5,
             "caption": "5/9 of 180 = 100"},
        ],
        "card": card_fraction,
        "solved": [
            {"q": "Ex: 3/8 of 40 marbles are red. How many red?",
             "steps": ["40 \u00f7 8 = 5", "5 \u00d7 3 = 15", "Answer = 15 red"]},
        ],
        "tips": [
            "\u2018of\u2019 \u2192 multiply.",
            "Divide by bottom, times top.",
            "Keep the units in the answer.",
            "Check: answer < total for a proper fraction.",
        ],
        "try_it": {
            "questions": [
                "1. 1/4 of 20 apples are green. How many green?",
                "2. 3/5 of Rs 100 is saved. How much saved?",
                "3. 2/7 of 28 students walk to school. How many?",
            ],
            "answers": "1) 5    2) Rs 60    3) 8",
        },
    },

    # ---- 6H Mixed fractions ----
    "6H": {
        "title": "Mixed Numbers",
        "intro": [
            "Mixed number = whole + fraction (e.g. 1\u00be).",
            "Improper \u2192 mixed: divide top by bottom.",
            "7/4 = 1 remainder 3 = 1\u00be.",
            "Mixed \u2192 improper: whole\u00d7bottom + top.",
            "1\u00be = (1\u00d74 + 3)/4 = 7/4.",
        ],
        "real_life": [
            {"text": "1. 1 full + 3/4 pizza = 1\u00be",
             "diagram": "fraction_circle", "total": 4, "shaded": 3,
             "caption": "plus 1 whole = 1\u00be"},
            {"text": "2. 7/4 cakes = 1\u00be cakes",
             "diagram": "fraction_bar", "total": 4, "shaded": 3,
             "caption": "7/4 = 1 whole + 3/4"},
            {"text": "3. 2\u00bd glasses of juice",
             "diagram": "fraction_circle", "total": 2, "shaded": 1,
             "caption": "2 full + 1/2 = 2\u00bd"},
        ],
        "card": card_mixed,
        "solved": [
            {"q": "Ex: Convert 17/6 to a mixed number.",
             "steps": ["17 \u00f7 6 = 2 remainder 5", "Answer = 2 and 5/6"]},
        ],
        "tips": [
            "Improper \u2192 mixed: divide.",
            "Mixed \u2192 improper: \u00d7 then +.",
            "Whole number stays outside.",
            "Keep the same bottom number.",
        ],
        "try_it": {
            "questions": [
                "1. Convert 11/4 to a mixed number.",
                "2. Convert 2 1/3 to an improper fraction.",
                "3. Convert 9/2 to a mixed number.",
            ],
            "answers": "1) 2\u00be    2) 7/3    3) 4\u00bd",
        },
    },

    # ---- 6I Puzzle fractions ----
    "6I": {
        "title": "Fraction Puzzles",
        "intro": [
            "Use clues to find the fraction.",
            "Unit fraction: top = 1 (like 1/5).",
            "List all options that fit every clue.",
            "Check each answer against the clues.",
            "Simplest form: no common factor left.",
        ],
        "real_life": [
            {"text": "1. Unit fractions look like 1/n",
             "diagram": "fraction_bar", "total": 5, "shaded": 1,
             "caption": "1/5 is a unit fraction"},
            {"text": "2. Proper fraction, bottom 8, even top",
             "diagram": "fraction_grid", "total": 8, "shaded": 2, "cols": 4,
             "caption": "2/8, 4/8, 6/8 ..."},
            {"text": "3. Top + bottom = 9, simplest, proper",
             "diagram": "fraction_bar", "total": 5, "shaded": 4,
             "caption": "4/5 (4+5=9)"},
        ],
        "card": card_fraction,
        "solved": [
            {"q": "Ex: Unit fraction, bottom between 4 and 7. List all.",
             "steps": ["Bottoms: 5, 6", "Unit \u2192 top = 1", "Answer: 1/5, 1/6"]},
        ],
        "tips": [
            "Unit fraction \u2192 top is 1.",
            "List every option, then check.",
            "Simplest form: no common factor.",
            "Re-read each clue before finalising.",
        ],
        "try_it": {
            "questions": [
                "1. Unit fraction with bottom between 2 and 5. List all.",
                "2. Proper fraction, bottom 6, odd top. List all.",
                "3. Top + bottom = 7, proper, simplest. List all.",
            ],
            "answers": "1) 1/3, 1/4    2) 1/6, 5/6 (3/6 not simplest)    3) 1/6, 2/5, 3/4",
        },
    },

    # ---- 6CUM3 Mixed G+H+I ----
    "6CUM3": {
        "title": "Review: Word Problems, Mixed, Puzzles",
        "intro": [
            "\u2018Of\u2019 means multiply (fraction of a total).",
            "Improper \u2194 mixed numbers: divide / multiply.",
            "Puzzles: list options, check every clue.",
            "Divide by bottom, times top for \u2018of\u2019.",
            "Always simplify and keep units.",
        ],
        "real_life": [
            {"text": "1. 2/3 of 30 = 20 students",
             "diagram": "fraction_bar", "total": 3, "shaded": 2,
             "caption": "2/3 of 30 = 20"},
            {"text": "2. 7/4 = 1\u00be (mixed number)",
             "diagram": "fraction_bar", "total": 4, "shaded": 3,
             "caption": "7/4 = 1\u00be"},
            {"text": "3. Unit fraction 1/6",
             "diagram": "fraction_circle", "total": 6, "shaded": 1,
             "caption": "1/6 is a unit fraction"},
        ],
        "card": card_mixed,
        "solved": [
            {"q": "Ex: 3/5 of 35, then write 17/6 as mixed.",
             "steps": ["3/5 of 35 = 21", "17/6 = 2 and 5/6"]},
        ],
        "tips": [
            "\u2018of\u2019 \u2192 multiply.",
            "Improper \u2194 mixed by divide / multiply.",
            "Puzzles: list then check.",
            "Simplify; keep units.",
        ],
        "try_it": {
            "questions": [
                "1. 3/4 of 20 = ?",
                "2. Convert 13/5 to a mixed number.",
                "3. Unit fraction with bottom 3 = ?",
            ],
            "answers": "1) 15    2) 2 1/3    3) 1/3",
        },
    },

    # ---- 6J Mixed challenge ----
    "6J": {
        "title": "Fractions — Mixed Challenge",
        "intro": [
            "Mix every skill: of, convert, add, subtract.",
            "\u2018Of\u2019 \u2192 divide by bottom, times top.",
            "Improper \u2194 mixed both ways.",
            "Match bottoms before + or \u2212.",
            "Simplify every final answer.",
        ],
        "real_life": [
            {"text": "1. 3/5 of 35 = 21",
             "diagram": "fraction_bar", "total": 5, "shaded": 3,
             "caption": "3/5 of 35 = 21"},
            {"text": "2. 17/6 = 2 and 5/6 (mixed)",
             "diagram": "fraction_bar", "total": 6, "shaded": 5,
             "caption": "remainder 5 of 6"},
            {"text": "3. 1\u00be + \u00bc = 2 (mixed add)",
             "diagram": "fraction_circle", "total": 4, "shaded": 3,
             "caption": "\u00be + \u00bc = 1 whole"},
        ],
        "card": card_mixed,
        "solved": [
            {"q": "Ex: Convert 4 3/5 to an improper fraction.",
             "steps": ["4\u00d75 + 3 = 23", "Keep bottom 5", "Answer = 23/5"]},
        ],
        "tips": [
            "\u2018of\u2019 \u2192 multiply.",
            "Convert carefully both ways.",
            "Equalise bottoms for + and \u2212.",
            "Simplify the answer.",
        ],
        "try_it": {
            "questions": [
                "1. 2/3 of 24 = ?",
                "2. Convert 19/4 to a mixed number.",
                "3. 2\u00bd + 1\u00bd = ?",
            ],
            "answers": "1) 16    2) 4\u00be    3) 4",
        },
    },

    # ---- 6REV Revision ----
    "6REV": {
        "title": "Level 6 Revision — Fractions",
        "intro": [
            "Fraction = equal part of a whole.",
            "Proper < 1; improper \u2265 1; mixed = whole + part.",
            "Equivalent: same value (1/2 = 2/4).",
            "Add/subtract: match bottoms, act on tops.",
            "\u2018Of\u2019 means multiply; always simplify.",
        ],
        "real_life": [
            {"text": "1. 3/4 of a pizza",
             "diagram": "fraction_circle", "total": 4, "shaded": 3,
             "caption": "3/4"},
            {"text": "2. 1/2 = 2/4 (equivalent)",
             "diagram": "two_bars", "t1": 2, "s1": 1, "t2": 4, "s2": 2,
             "lab1": "1/2", "lab2": "2/4", "caption": "equal shaded"},
            {"text": "3. 1/5 + 2/5 = 3/5",
             "diagram": "fraction_bar", "total": 5, "shaded": 3,
             "caption": "add tops"},
        ],
        "card": card_fraction,
        "solved": [
            {"q": "Ex: 2/3 of 30, then 1/5 + 2/5.",
             "steps": ["2/3 of 30 = 20", "1/5 + 2/5 = 3/5"]},
        ],
        "tips": [
            "Equal parts; top/bottom roles.",
            "Proper vs improper vs mixed.",
            "Match bottoms for + and \u2212.",
            "\u2018of\u2019 \u2192 multiply; simplify always.",
        ],
        "try_it": {
            "questions": [
                "1. Simplify 6/9.",
                "2. 2/7 + 3/7 = ?",
                "3. 1/2 of 18 = ?",
            ],
            "answers": "1) 2/3    2) 5/7    3) 9",
        },
    },
}


# ───────────────────────────────────────────────────────────────────────────────
# LEVEL 7 — Decimals: concept page specs (sheet 1 of each sublevel)
# ───────────────────────────────────────────────────────────────────────────────
_L7 = {
    # ---- 7A Decimal concept ----
    "7A": {
        "title": "Decimals — Concept",
        "intro": [
            "A decimal shows parts smaller than 1.",
            "The dot is the DECIMAL POINT.",
            "Right of the dot: tenths, hundredths...",
            "0.1 = 1 tenth = 1/10.",
            "0.01 = 1 hundredth = 1/100.",
        ],
        "real_life": [
            {"text": "1. 3 tenths of a strip = 0.3",
             "diagram": "tenths_grid", "shaded": 3,
             "caption": "3 of 10 strips = 0.3 = 3/10"},
            {"text": "2. 25 hundredths of a square = 0.25",
             "diagram": "hundredths_grid", "shaded": 25,
             "caption": "25 of 100 = 0.25"},
            {"text": "3. Money: 75 paise = Rs 0.75",
             "diagram": "hundredths_grid", "shaded": 75,
             "caption": "75 of 100 = 0.75"},
        ],
        "card": card_decimal_grid,
        "solved": [
            {"q": "Ex: Write 15 hundredths as a decimal.",
             "steps": ["15 hundredths = 15/100", "Answer = 0.15"]},
        ],
        "tips": [
            "Dot = decimal point.",
            "1st place after dot = tenths.",
            "2nd place after dot = hundredths.",
            "0.5 = 5/10 = half.",
        ],
        "try_it": {
            "questions": [
                "1. Write 7 tenths as a decimal.",
                "2. Write 9 hundredths as a decimal.",
                "3. Write 50 paise in rupees as a decimal.",
            ],
            "answers": "1) 0.7    2) 0.09    3) Rs 0.50",
        },
    },

    # ---- 7B Decimal place value ----
    "7B": {
        "title": "Decimal Place Value",
        "intro": [
            "Each place has a value 10 times smaller.",
            "Ones . tenths hundredths thousandths.",
            "\u00d710 moves the point ONE place right.",
            "\u00f710 moves the point ONE place left.",
            "Example: 5.3 \u00d7 10 = 53.",
        ],
        "real_life": [
            {"text": "1. 3.45 in a place-value chart",
             "diagram": "place_value",
             "headers": ["Ones", ".", "Tenths", "Hund"], "digits": ["3", ".", "4", "5"],
             "caption": "3 ones, 4 tenths, 5 hundredths"},
            {"text": "2. 5.3 \u00d7 10 = 53 (point moves right)",
             "diagram": "place_value",
             "headers": ["Tens", "Ones", ".", "Tenths"], "digits": ["5", "3", ".", "0"],
             "caption": "53.0"},
            {"text": "3. 0.47 \u00d7 100 = 47 (two places right)",
             "diagram": "place_value",
             "headers": ["Tens", "Ones", ".", "T"], "digits": ["4", "7", ".", "0"],
             "caption": "47"},
        ],
        "card": card_decimal_place,
        "solved": [
            {"q": "Ex: 0.47 \u00d7 100 = ?",
             "steps": ["\u00d7100 \u2192 point moves 2 right", "0.47 \u2192 47", "Answer = 47"]},
        ],
        "tips": [
            "\u00d710 \u2192 point 1 step right.",
            "\u00f710 \u2192 point 1 step left.",
            "\u00d7100 \u2192 2 steps; \u00d71000 \u2192 3 steps.",
            "Add zeros if needed.",
        ],
        "try_it": {
            "questions": [
                "1. 5.3 \u00d7 10 = ?",
                "2. 5.3 \u00f7 10 = ?",
                "3. 0.6 \u00d7 100 = ?",
            ],
            "answers": "1) 53    2) 0.53    3) 60",
        },
    },

    # ---- 7C Decimal comparison ----
    "7C": {
        "title": "Comparing Decimals",
        "intro": [
            "Compare the whole-number part first.",
            "Then tenths, then hundredths.",
            "Add zeros to make equal lengths.",
            "0.5 = 0.50 (same value).",
            "More tenths = bigger (if wholes equal).",
        ],
        "real_life": [
            {"text": "1. 0.5 vs 0.3 \u2192 0.5 is bigger",
             "diagram": "two_bars", "t1": 10, "s1": 5, "t2": 10, "s2": 3,
             "lab1": "0.5", "lab2": "0.3", "caption": "5 tenths > 3 tenths"},
            {"text": "2. 0.5 vs 0.47 on a number line",
             "diagram": "number_line", "ticks": 10,
             "marks": [(5, "0.5")], "caption": "0.47 is just left of 0.5"},
            {"text": "3. 1.3 vs 1.29 \u2192 1.3 = 1.30 is bigger",
             "diagram": "two_bars", "t1": 10, "s1": 3, "t2": 10, "s2": 2,
             "lab1": "1.30", "lab2": "1.29", "caption": "30 > 29 hundredths"},
        ],
        "card": card_decimal_grid,
        "solved": [
            {"q": "Ex: Compare 1.3 and 1.29.",
             "steps": ["Make equal: 1.30 vs 1.29", "30 > 29 hundredths", "1.3 > 1.29"]},
        ],
        "tips": [
            "Compare wholes first.",
            "Then tenths, then hundredths.",
            "Add zeros to match length.",
            "0.5 = 0.50 (equal).",
        ],
        "try_it": {
            "questions": [
                "1. Compare 0.7 and 0.6 (use > < =).",
                "2. Compare 0.45 and 0.5.",
                "3. Compare 2.30 and 2.3.",
            ],
            "answers": "1) 0.7 > 0.6    2) 0.45 < 0.5    3) 2.30 = 2.3",
        },
    },

    # ---- 7CUM1 Mixed A+B+C ----
    "7CUM1": {
        "title": "Review: Concept, Place Value, Comparison",
        "intro": [
            "Decimal = parts smaller than 1.",
            "Places: tenths, hundredths, thousandths.",
            "\u00d710 / \u00f710 moves the point one step.",
            "Compare wholes, then tenths, then hundredths.",
            "Add zeros to match: 0.5 = 0.50.",
        ],
        "real_life": [
            {"text": "1. 0.3 = 3 tenths",
             "diagram": "tenths_grid", "shaded": 3,
             "caption": "3 of 10 = 0.3"},
            {"text": "2. 3.45 place value",
             "diagram": "place_value",
             "headers": ["Ones", ".", "Tenths", "Hund"], "digits": ["3", ".", "4", "5"],
             "caption": "3 ones, 4 tenths, 5 hundredths"},
            {"text": "3. 0.5 > 0.3",
             "diagram": "two_bars", "t1": 10, "s1": 5, "t2": 10, "s2": 3,
             "lab1": "0.5", "lab2": "0.3", "caption": "5 tenths > 3 tenths"},
        ],
        "card": card_decimal_place,
        "solved": [
            {"q": "Ex: 0.6 \u00d7 10, then compare with 5.",
             "steps": ["0.6 \u00d7 10 = 6", "6 > 5"]},
        ],
        "tips": [
            "Know each decimal place.",
            "\u00d710 right, \u00f710 left.",
            "Compare wholes first.",
            "Add zeros to match length.",
        ],
        "try_it": {
            "questions": [
                "1. Write 6 tenths as a decimal.",
                "2. 0.8 \u00d7 10 = ?",
                "3. Compare 0.4 and 0.40.",
            ],
            "answers": "1) 0.6    2) 8    3) 0.4 = 0.40",
        },
    },

    # ---- 7D Decimal addition ----
    "7D": {
        "title": "Adding Decimals",
        "intro": [
            "Line up the decimal points.",
            "Add like normal, column by column.",
            "Carry over when a column passes 9.",
            "Keep the point in the same place.",
            "0.4 + 0.3 = 0.7.",
        ],
        "real_life": [
            {"text": "1. 0.4 + 0.3 = 0.7 (tenths)",
             "diagram": "tenths_grid", "shaded": 7,
             "caption": "4 + 3 = 7 tenths"},
            {"text": "2. Shopping: Rs 3.75 + Rs 4.85 = Rs 8.60",
             "diagram": "hundredths_grid", "shaded": 60,
             "caption": "carry the hundredths"},
            {"text": "3. 1.2 + 2.5 = 3.7",
             "diagram": "number_line", "ticks": 10,
             "marks": [(7, "0.7")], "caption": "tenths add to 7"},
        ],
        "card": card_decimal_place,
        "solved": [
            {"q": "Ex: 1.2 + 2.5 = ?",
             "steps": ["Line up points", "12 + 25 tenths logic", "Answer = 3.7"]},
        ],
        "tips": [
            "Line up the points.",
            "Add column by column.",
            "Carry when over 9.",
            "Point stays in line.",
        ],
        "try_it": {
            "questions": [
                "1. 0.6 + 0.5 = ?",
                "2. 1.2 + 2.5 = ?",
                "3. Rs 2.50 + Rs 3.75 = ?",
            ],
            "answers": "1) 1.1    2) 3.7    3) Rs 6.25",
        },
    },

    # ---- 7E Decimal subtraction ----
    "7E": {
        "title": "Subtracting Decimals",
        "intro": [
            "Line up the decimal points.",
            "Add zeros to make equal lengths.",
            "Subtract column by column.",
            "Borrow when the top digit is smaller.",
            "0.8 \u2212 0.3 = 0.5.",
        ],
        "real_life": [
            {"text": "1. 0.8 \u2212 0.3 = 0.5 (tenths)",
             "diagram": "tenths_grid", "shaded": 5,
             "caption": "8 \u2212 3 = 5 tenths left"},
            {"text": "2. Rope: 8.5 m \u2212 3.75 m = 4.75 m",
             "diagram": "hundredths_grid", "shaded": 75,
             "caption": "borrow across the point"},
            {"text": "3. 1.7 \u2212 0.5 = 1.2",
             "diagram": "number_line", "ticks": 10,
             "marks": [(2, "0.2")], "caption": "1.2 remaining"},
        ],
        "card": card_decimal_place,
        "solved": [
            {"q": "Ex: 8.5 \u2212 3.75 = ?",
             "steps": ["Write 8.50 \u2212 3.75", "Borrow as needed", "Answer = 4.75"]},
        ],
        "tips": [
            "Line up the points.",
            "Add zeros to match.",
            "Borrow when needed.",
            "Point stays in line.",
        ],
        "try_it": {
            "questions": [
                "1. 0.9 \u2212 0.4 = ?",
                "2. 1.7 \u2212 0.5 = ?",
                "3. 5.0 \u2212 2.35 = ?",
            ],
            "answers": "1) 0.5    2) 1.2    3) 2.65",
        },
    },

    # ---- 7F Fraction to decimal ----
    "7F": {
        "title": "Fractions to Decimals",
        "intro": [
            "Divide the top by the bottom.",
            "1/2 = 1 \u00f7 2 = 0.5.",
            "Or make the bottom 10 or 100.",
            "1/4 = 25/100 = 0.25.",
            "3/4 = 75/100 = 0.75.",
        ],
        "real_life": [
            {"text": "1. Half a bar: 1/2 = 0.5",
             "diagram": "tenths_grid", "shaded": 5,
             "caption": "1/2 = 5/10 = 0.5"},
            {"text": "2. Quarter: 1/4 = 0.25",
             "diagram": "hundredths_grid", "shaded": 25,
             "caption": "1/4 = 25/100 = 0.25"},
            {"text": "3. Three quarters: 3/4 = 0.75",
             "diagram": "hundredths_grid", "shaded": 75,
             "caption": "3/4 = 75/100 = 0.75"},
        ],
        "card": card_frac_to_dec,
        "solved": [
            {"q": "Ex: Convert 3/4 to a decimal.",
             "steps": ["3 \u00f7 4 = 0.75", "or 3/4 = 75/100", "Answer = 0.75"]},
        ],
        "tips": [
            "Divide top by bottom.",
            "Or make bottom 10 / 100.",
            "1/2 = 0.5, 1/4 = 0.25.",
            "3/4 = 0.75, 1/5 = 0.2.",
        ],
        "try_it": {
            "questions": [
                "1. Convert 1/2 to a decimal.",
                "2. Convert 1/4 to a decimal.",
                "3. Convert 2/5 to a decimal.",
            ],
            "answers": "1) 0.5    2) 0.25    3) 0.4",
        },
    },

    # ---- 7CUM2 Mixed D+E+F ----
    "7CUM2": {
        "title": "Review: Add, Subtract, Fraction-to-Decimal",
        "intro": [
            "Add/subtract: line up the points.",
            "Add zeros to match lengths.",
            "Fraction \u2192 decimal: divide top by bottom.",
            "1/2 = 0.5, 1/4 = 0.25, 3/4 = 0.75.",
            "Keep the point in line in answers.",
        ],
        "real_life": [
            {"text": "1. 0.4 + 0.3 = 0.7",
             "diagram": "tenths_grid", "shaded": 7,
             "caption": "7 tenths"},
            {"text": "2. 0.8 \u2212 0.3 = 0.5",
             "diagram": "tenths_grid", "shaded": 5,
             "caption": "5 tenths left"},
            {"text": "3. 1/4 = 0.25",
             "diagram": "hundredths_grid", "shaded": 25,
             "caption": "25 of 100"},
        ],
        "card": card_frac_to_dec,
        "solved": [
            {"q": "Ex: 1/2 + 0.25 = ?",
             "steps": ["1/2 = 0.5", "0.5 + 0.25 = 0.75"]},
        ],
        "tips": [
            "Line up points for + and \u2212.",
            "Add zeros to match.",
            "Fraction \u2192 decimal: divide.",
            "Know 1/2, 1/4, 3/4 by heart.",
        ],
        "try_it": {
            "questions": [
                "1. 0.6 + 0.7 = ?",
                "2. 1.5 \u2212 0.8 = ?",
                "3. Convert 3/4 to a decimal.",
            ],
            "answers": "1) 1.3    2) 0.7    3) 0.75",
        },
    },

    # ---- 7G Word problems ----
    "7G": {
        "title": "Decimal Word Problems",
        "intro": [
            "Money and measures use decimals.",
            "Total \u2192 add. Left over \u2192 subtract.",
            "Line up the points before working.",
            "Keep units: Rs, m, km, kg.",
            "Check the point is in the right place.",
        ],
        "real_life": [
            {"text": "1. Rs 3.75 + Rs 4.85 = Rs 8.60",
             "diagram": "hundredths_grid", "shaded": 60,
             "caption": "total cost"},
            {"text": "2. Rope 8.5 m \u2212 3.75 m = 4.75 m left",
             "diagram": "tenths_grid", "shaded": 5,
             "caption": "what remains"},
            {"text": "3. Walk 2.4 + cycle 3.75 = 6.15 km",
             "diagram": "number_line", "ticks": 10,
             "marks": [(6, "0.6")], "caption": "total distance"},
        ],
        "card": card_decimal_place,
        "solved": [
            {"q": "Ex: Rs 3.75 + Rs 4.85 = ?",
             "steps": ["Line up points", "375 + 485 paise = 860", "Answer = Rs 8.60"]},
        ],
        "tips": [
            "Total \u2192 add.",
            "Left over \u2192 subtract.",
            "Line up the points.",
            "Keep the units.",
        ],
        "try_it": {
            "questions": [
                "1. Rs 5.50 + Rs 2.75 = ?",
                "2. 6.5 m \u2212 2.25 m = ?",
                "3. 1.2 kg + 0.85 kg = ?",
            ],
            "answers": "1) Rs 8.25    2) 4.25 m    3) 2.05 kg",
        },
    },

    # ---- 7H Mixed decimals ----
    "7H": {
        "title": "Decimals & Fractions Together",
        "intro": [
            "Convert to compare fairly.",
            "Make both decimals, or both fractions.",
            "7/8 = 0.875, so compare with 0.87.",
            "Bigger decimal = bigger value.",
            "Use hundredths to line up.",
        ],
        "real_life": [
            {"text": "1. 7/8 = 0.875 vs 0.87 \u2192 7/8 bigger",
             "diagram": "hundredths_grid", "shaded": 87,
             "caption": "0.875 > 0.87"},
            {"text": "2. 3/5 = 0.6 vs 0.62 \u2192 0.62 bigger",
             "diagram": "hundredths_grid", "shaded": 62,
             "caption": "0.60 < 0.62"},
            {"text": "3. 9/25 = 0.36 vs 0.34 \u2192 9/25 bigger",
             "diagram": "hundredths_grid", "shaded": 36,
             "caption": "0.36 > 0.34"},
        ],
        "card": card_frac_to_dec,
        "solved": [
            {"q": "Ex: Is 3/5 greater than 0.62?",
             "steps": ["3/5 = 0.60", "0.60 < 0.62", "No, 0.62 is greater"]},
        ],
        "tips": [
            "Convert to the same form.",
            "Decimals are easiest to compare.",
            "Line up hundredths.",
            "Bigger digits = bigger value.",
        ],
        "try_it": {
            "questions": [
                "1. Convert 7/8 to a decimal.",
                "2. Which is bigger: 1/2 or 0.45?",
                "3. Which is bigger: 0.7 or 3/5?",
            ],
            "answers": "1) 0.875    2) 1/2 (0.5)    3) 0.7",
        },
    },

    # ---- 7I Decimal puzzles ----
    "7I": {
        "title": "Decimal Puzzles",
        "intro": [
            "Use clues to find the decimal.",
            "Check the whole part and each digit.",
            "List all answers that fit.",
            "Tenths = first digit after the dot.",
            "Re-read each clue to check.",
        ],
        "real_life": [
            {"text": "1. Between 4 and 5, tenths = 5 \u2192 4.5...",
             "diagram": "number_line", "ticks": 10,
             "marks": [(5, "0.5")], "caption": "4.5 fits"},
            {"text": "2. Under 1, 2 places, digits sum 7 \u2192 0.16, 0.25...",
             "diagram": "hundredths_grid", "shaded": 25,
             "caption": "0.25 (2+5=7)"},
            {"text": "3. 0.5 to 0.6, tenths = hundredths \u2192 0.55",
             "diagram": "hundredths_grid", "shaded": 55,
             "caption": "0.55 fits"},
        ],
        "card": card_decimal_grid,
        "solved": [
            {"q": "Ex: Between 0.5 and 0.6, tenths = hundredths.",
             "steps": ["Tenths digit = 5", "hundredths = 5 too", "Answer = 0.55"]},
        ],
        "tips": [
            "Check the whole part first.",
            "Then each decimal digit.",
            "List every option.",
            "Re-check against all clues.",
        ],
        "try_it": {
            "questions": [
                "1. Between 2 and 3, tenths = 4. Give one answer.",
                "2. Under 1, 1 place, digit is even. List some.",
                "3. Between 0.3 and 0.4, tenths = hundredths.",
            ],
            "answers": "1) 2.4    2) 0.2, 0.4, 0.6, 0.8    3) 0.33",
        },
    },

    # ---- 7CUM3 Mixed G+H+I ----
    "7CUM3": {
        "title": "Review: Word Problems, Mixed, Puzzles",
        "intro": [
            "Word problems: add or subtract, keep units.",
            "Convert to compare fractions and decimals.",
            "Puzzles: list options, check clues.",
            "Line up the points for + and \u2212.",
            "1/2 = 0.5, 1/4 = 0.25, 3/4 = 0.75.",
        ],
        "real_life": [
            {"text": "1. Rs 3.75 + Rs 4.85 = Rs 8.60",
             "diagram": "hundredths_grid", "shaded": 60,
             "caption": "total"},
            {"text": "2. 3/5 = 0.6 vs 0.62",
             "diagram": "hundredths_grid", "shaded": 62,
             "caption": "0.62 bigger"},
            {"text": "3. 0.55 fits 0.5\u20130.6, tenths = hundredths",
             "diagram": "number_line", "ticks": 10,
             "marks": [(5, "0.5")], "caption": "0.55"},
        ],
        "card": card_frac_to_dec,
        "solved": [
            {"q": "Ex: 8.5 m \u2212 3.75 m, then convert 1/4.",
             "steps": ["8.50 \u2212 3.75 = 4.75 m", "1/4 = 0.25"]},
        ],
        "tips": [
            "Add/subtract: keep units.",
            "Convert to compare.",
            "Puzzles: list, then check.",
            "Line up the points.",
        ],
        "try_it": {
            "questions": [
                "1. Rs 6.40 + Rs 1.85 = ?",
                "2. Which is bigger: 0.6 or 1/2?",
                "3. Between 0.2 and 0.3, tenths = hundredths.",
            ],
            "answers": "1) Rs 8.25    2) 0.6    3) 0.22",
        },
    },

    # ---- 7J Mixed challenge ----
    "7J": {
        "title": "Decimals — Mixed Challenge",
        "intro": [
            "Mix every skill: write, multiply, convert.",
            "\u00d710 / \u00d7100 / \u00d71000 move the point.",
            "Hundredths = 2 places after the dot.",
            "Line up points for + and \u2212.",
            "Convert fractions to compare.",
        ],
        "real_life": [
            {"text": "1. 8 hundredths = 0.08",
             "diagram": "hundredths_grid", "shaded": 8,
             "caption": "8 of 100 = 0.08"},
            {"text": "2. 5.37 \u00d7 100 = 537",
             "diagram": "place_value",
             "headers": ["H", "T", "O", "."], "digits": ["5", "3", "7", "."],
             "caption": "point moves 2 right"},
            {"text": "3. 0.048 \u00d7 1000 = 48",
             "diagram": "tenths_grid", "shaded": 5,
             "caption": "point moves 3 right"},
        ],
        "card": card_decimal_place,
        "solved": [
            {"q": "Ex: 0.048 \u00d7 1000 = ?",
             "steps": ["\u00d71000 \u2192 3 places right", "0.048 \u2192 48", "Answer = 48"]},
        ],
        "tips": [
            "Count places to move the point.",
            "Hundredths = 2 places.",
            "Line up points for + and \u2212.",
            "Convert to compare.",
        ],
        "try_it": {
            "questions": [
                "1. Write 8 hundredths as a decimal.",
                "2. 2.5 \u00d7 100 = ?",
                "3. Convert 3/4 to a decimal.",
            ],
            "answers": "1) 0.08    2) 250    3) 0.75",
        },
    },

    # ---- 7REV Revision ----
    "7REV": {
        "title": "Level 7 Revision — Decimals",
        "intro": [
            "Decimal = parts smaller than 1.",
            "Places: tenths, hundredths, thousandths.",
            "\u00d710 / \u00f710 move the point one step.",
            "Add/subtract: line up the points.",
            "Fraction \u2192 decimal: divide top by bottom.",
        ],
        "real_life": [
            {"text": "1. 0.3 = 3 tenths",
             "diagram": "tenths_grid", "shaded": 3,
             "caption": "3 of 10"},
            {"text": "2. 0.25 = 25 hundredths",
             "diagram": "hundredths_grid", "shaded": 25,
             "caption": "25 of 100"},
            {"text": "3. 0.5 > 0.3",
             "diagram": "two_bars", "t1": 10, "s1": 5, "t2": 10, "s2": 3,
             "lab1": "0.5", "lab2": "0.3", "caption": "5 > 3 tenths"},
        ],
        "card": card_decimal_place,
        "solved": [
            {"q": "Ex: 0.4 + 0.3, then convert 1/2.",
             "steps": ["0.4 + 0.3 = 0.7", "1/2 = 0.5"]},
        ],
        "tips": [
            "Know the decimal places.",
            "\u00d710 right, \u00f710 left.",
            "Line up points for + and \u2212.",
            "Fraction \u2192 decimal: divide.",
        ],
        "try_it": {
            "questions": [
                "1. Write 4 tenths as a decimal.",
                "2. 0.6 + 0.5 = ?",
                "3. Convert 1/4 to a decimal.",
            ],
            "answers": "1) 0.4    2) 1.1    3) 0.25",
        },
    },
}


# ───────────────────────────────────────────────────────────────────────────────
# LEVEL 8 — Integers: concept page specs (sheet 1 of each sublevel)
# ───────────────────────────────────────────────────────────────────────────────
_L8 = {
    # ---- 8A Integer concept ----
    "8A": {
        "title": "Integers — Concept",
        "intro": [
            "Integers = whole numbers AND their negatives.",
            "..., -3, -2, -1, 0, 1, 2, 3, ...",
            "Positive: right of 0 (1, 2, 3...).",
            "Negative: left of 0 (-1, -2, -3...).",
            "0 is an integer, neither + nor -.",
        ],
        "real_life": [
            {"text": "1. Temperature: -5 C is below zero",
             "diagram": "integer_line", "lo": -6, "hi": 6, "marks": [(-5, "-5")],
             "caption": "-5 is 5 steps left of 0"},
            {"text": "2. Lift: +3 is 3 floors up, -2 is basement",
             "diagram": "integer_line", "lo": -4, "hi": 4,
             "marks": [(-2, "-2"), (3, "+3")], "caption": "below ground = negative"},
            {"text": "3. Money: owe Rs 100 = -100; have Rs 100 = +100",
             "diagram": "integer_line", "lo": -3, "hi": 3, "marks": [(0, "0")],
             "caption": "0 = no money owed or held"},
        ],
        "card": card_integer_line,
        "solved": [
            {"q": "Ex: Is 0 an integer? Is 7 positive or negative?",
             "steps": ["Yes, 0 is an integer", "7 is to the right of 0 \u2192 positive"]},
        ],
        "tips": [
            "Integers include negatives and 0.",
            "Right of 0 = positive.",
            "Left of 0 = negative.",
            "0 is neither + nor -.",
        ],
        "try_it": {
            "questions": [
                "1. Is -4 an integer?",
                "2. Is 9 positive or negative?",
                "3. Is -12 to the left or right of 0?",
            ],
            "answers": "1) Yes    2) positive    3) left",
        },
    },

    # ---- 8B Number line ----
    "8B": {
        "title": "Integers on the Number Line",
        "intro": [
            "Numbers grow bigger to the RIGHT.",
            "Numbers get smaller to the LEFT.",
            "Move right = add; move left = subtract.",
            "-3 is left of 0; 5 is right of 0.",
            "Compare by position: right = bigger.",
        ],
        "real_life": [
            {"text": "1. Mark -3: it is left of 0",
             "diagram": "integer_line", "lo": -6, "hi": 6, "marks": [(-3, "-3")],
             "caption": "-3 sits left of zero"},
            {"text": "2. Start at 0, move 4 right \u2192 4",
             "diagram": "integer_line", "lo": -2, "hi": 6, "jump": (0, 4, "+4"),
             "marks": [(4, "4")], "caption": "move right = add"},
            {"text": "3. Start at 2, move 5 left \u2192 -3",
             "diagram": "integer_line", "lo": -5, "hi": 5, "jump": (2, -5, "-5"),
             "marks": [(-3, "-3")], "caption": "move left = subtract"},
        ],
        "card": card_integer_line,
        "solved": [
            {"q": "Ex: Start at 0 and move 4 right. Where are you?",
             "steps": ["Right = add", "0 + 4 = 4", "Answer = 4"]},
        ],
        "tips": [
            "Right = bigger, add.",
            "Left = smaller, subtract.",
            "0 is the centre.",
            "Count the steps you move.",
        ],
        "try_it": {
            "questions": [
                "1. Is -3 left or right of 0?",
                "2. Start at 0, move 6 right. Where?",
                "3. Start at 1, move 4 left. Where?",
            ],
            "answers": "1) left    2) 6    3) -3",
        },
    },

    # ---- 8C Integer addition ----
    "8C": {
        "title": "Adding Integers",
        "intro": [
            "Add a positive \u2192 move RIGHT.",
            "Add a negative \u2192 move LEFT.",
            "Same signs: add, keep the sign.",
            "Different signs: subtract, keep bigger sign.",
            "7 + (-4) = 3; (-5) + (-3) = -8.",
        ],
        "real_life": [
            {"text": "1. 7 + (-4) = 3 (move 4 left from 7)",
             "diagram": "integer_line", "lo": -2, "hi": 8, "jump": (7, -4, "-4"),
             "marks": [(3, "3")], "caption": "different signs \u2192 subtract"},
            {"text": "2. (-5) + (-3) = -8 (both negative)",
             "diagram": "integer_line", "lo": -9, "hi": 1, "jump": (-5, -3, "-3"),
             "marks": [(-8, "-8")], "caption": "same signs \u2192 add"},
            {"text": "3. (-2) + 6 = 4 (move 6 right)",
             "diagram": "integer_line", "lo": -4, "hi": 6, "jump": (-2, 6, "+6"),
             "marks": [(4, "4")], "caption": "ends right of 0 \u2192 positive"},
        ],
        "card": card_int_addsub,
        "solved": [
            {"q": "Ex: 7 + (-4) = ?",
             "steps": ["Start at 7, add negative \u2192 move left 4", "7 - 4 = 3", "Answer = 3"]},
        ],
        "tips": [
            "Add + \u2192 move right.",
            "Add - \u2192 move left.",
            "Same signs: add, keep sign.",
            "Different signs: subtract, bigger wins.",
        ],
        "try_it": {
            "questions": [
                "1. 5 + 3 = ?",
                "2. (-5) + (-3) = ?",
                "3. 7 + (-4) = ?",
            ],
            "answers": "1) 8    2) -8    3) 3",
        },
    },

    # ---- 8CUM1 Mixed A+B+C ----
    "8CUM1": {
        "title": "Review: Concept, Number Line, Addition",
        "intro": [
            "Integers include negatives and 0.",
            "Right = positive/bigger; left = negative/smaller.",
            "Add + \u2192 right; add - \u2192 left.",
            "Same signs add; different signs subtract.",
            "0 is neither + nor -.",
        ],
        "real_life": [
            {"text": "1. -3 is left of 0",
             "diagram": "integer_line", "lo": -5, "hi": 5, "marks": [(-3, "-3")],
             "caption": "negative = left"},
            {"text": "2. Start 0, move 4 right \u2192 4",
             "diagram": "integer_line", "lo": -2, "hi": 6, "jump": (0, 4, "+4"),
             "marks": [(4, "4")], "caption": "add = move right"},
            {"text": "3. 7 + (-4) = 3",
             "diagram": "integer_line", "lo": -2, "hi": 8, "jump": (7, -4, "-4"),
             "marks": [(3, "3")], "caption": "different signs subtract"},
        ],
        "card": card_int_addsub,
        "solved": [
            {"q": "Ex: (-5) + (-3), then say if it is left or right of 0.",
             "steps": ["Same signs \u2192 add: 5+3 = 8, keep -", "= -8, left of 0"]},
        ],
        "tips": [
            "Negatives sit left of 0.",
            "Add + right, add - left.",
            "Same signs add; different subtract.",
            "Right is always bigger.",
        ],
        "try_it": {
            "questions": [
                "1. Is -7 an integer?",
                "2. Start 0, move 5 left. Where?",
                "3. 6 + (-2) = ?",
            ],
            "answers": "1) Yes    2) -5    3) 4",
        },
    },

    # ---- 8D Integer subtraction ----
    "8D": {
        "title": "Subtracting Integers",
        "intro": [
            "Subtracting = ADD THE OPPOSITE.",
            "a - b becomes a + (-b).",
            "5 - (-3) = 5 + 3 = 8.",
            "3 - 8 = -5 (go below zero).",
            "Two minuses make a plus.",
        ],
        "real_life": [
            {"text": "1. 8 - 3 = 5 (move 3 left)",
             "diagram": "integer_line", "lo": 0, "hi": 10, "jump": (8, -3, "-3"),
             "marks": [(5, "5")], "caption": "ordinary take-away"},
            {"text": "2. 3 - 8 = -5 (cross below zero)",
             "diagram": "integer_line", "lo": -6, "hi": 4, "jump": (3, -8, "-8"),
             "marks": [(-5, "-5")], "caption": "answer goes negative"},
            {"text": "3. 5 - (-3) = 8 (add the opposite)",
             "diagram": "integer_line", "lo": 0, "hi": 10, "jump": (5, 3, "+3"),
             "marks": [(8, "8")], "caption": "minus a minus = plus"},
        ],
        "card": card_int_addsub,
        "solved": [
            {"q": "Ex: 5 - (-3) = ?",
             "steps": ["Add the opposite: 5 + 3", "= 8", "Answer = 8"]},
        ],
        "tips": [
            "Subtract = add the opposite.",
            "Minus a minus = plus.",
            "Going below 0 gives a negative.",
            "Then use the addition rules.",
        ],
        "try_it": {
            "questions": [
                "1. 8 - 3 = ?",
                "2. 3 - 8 = ?",
                "3. 5 - (-3) = ?",
            ],
            "answers": "1) 5    2) -5    3) 8",
        },
    },

    # ---- 8E Integer multiplication ----
    "8E": {
        "title": "Multiplying Integers",
        "intro": [
            "Same signs \u2192 positive answer.",
            "Different signs \u2192 negative answer.",
            "4 \u00d7 5 = 20; 4 \u00d7 (-5) = -20.",
            "(-4) \u00d7 (-5) = +20.",
            "Multiply the numbers, then fix the sign.",
        ],
        "real_life": [
            {"text": "1. (+)(+) and (-)(-) give +",
             "diagram": "sign_rule",
             "pairs": [("(+)(+)", "+"), ("(-)(-)", "+")],
             "caption": "same signs \u2192 positive"},
            {"text": "2. (+)(-) and (-)(+) give -",
             "diagram": "sign_rule",
             "pairs": [("(+)(-)", "-"), ("(-)(+)", "-")],
             "caption": "different signs \u2192 negative"},
            {"text": "3. (-4) \u00d7 5 = -20 on the line (4 jumps of -5)",
             "diagram": "integer_line", "lo": -22, "hi": 2, "marks": [(-20, "-20")],
             "caption": "different signs \u2192 negative"},
        ],
        "card": card_int_signs,
        "solved": [
            {"q": "Ex: (-4) \u00d7 5 = ?",
             "steps": ["Numbers: 4 \u00d7 5 = 20", "Different signs \u2192 negative", "Answer = -20"]},
        ],
        "tips": [
            "Same signs \u2192 +.",
            "Different signs \u2192 -.",
            "Multiply numbers, then sign.",
            "(-)(-) = +.",
        ],
        "try_it": {
            "questions": [
                "1. 4 \u00d7 5 = ?",
                "2. 4 \u00d7 (-5) = ?",
                "3. (-4) \u00d7 (-5) = ?",
            ],
            "answers": "1) 20    2) -20    3) 20",
        },
    },

    # ---- 8F Integer division ----
    "8F": {
        "title": "Dividing Integers",
        "intro": [
            "Same sign rules as multiplication.",
            "Same signs \u2192 positive answer.",
            "Different signs \u2192 negative answer.",
            "12 \u00f7 4 = 3; (-12) \u00f7 4 = -3.",
            "(-12) \u00f7 (-4) = +3.",
        ],
        "real_life": [
            {"text": "1. Same signs \u2192 + (e.g. (-12) \u00f7 (-4) = 3)",
             "diagram": "sign_rule",
             "pairs": [("(+)\u00f7(+)", "+"), ("(-)\u00f7(-)", "+")],
             "caption": "same signs \u2192 positive"},
            {"text": "2. Different signs \u2192 - (e.g. 12 \u00f7 (-4) = -3)",
             "diagram": "sign_rule",
             "pairs": [("(+)\u00f7(-)", "-"), ("(-)\u00f7(+)", "-")],
             "caption": "different signs \u2192 negative"},
            {"text": "3. (-12) \u00f7 4 = -3 on the line",
             "diagram": "integer_line", "lo": -5, "hi": 5, "marks": [(-3, "-3")],
             "caption": "different signs \u2192 negative"},
        ],
        "card": card_int_signs,
        "solved": [
            {"q": "Ex: (-12) \u00f7 4 = ?",
             "steps": ["Numbers: 12 \u00f7 4 = 3", "Different signs \u2192 negative", "Answer = -3"]},
        ],
        "tips": [
            "Same rules as multiply.",
            "Same signs \u2192 +.",
            "Different signs \u2192 -.",
            "Divide numbers, then sign.",
        ],
        "try_it": {
            "questions": [
                "1. 12 \u00f7 4 = ?",
                "2. (-12) \u00f7 4 = ?",
                "3. (-12) \u00f7 (-4) = ?",
            ],
            "answers": "1) 3    2) -3    3) 3",
        },
    },

    # ---- 8CUM2 Mixed D+E+F ----
    "8CUM2": {
        "title": "Review: Subtract, Multiply, Divide",
        "intro": [
            "Subtract = add the opposite.",
            "Multiply/divide: same signs \u2192 +.",
            "Multiply/divide: different signs \u2192 -.",
            "Minus a minus = plus.",
            "Work the numbers, then fix the sign.",
        ],
        "real_life": [
            {"text": "1. 5 - (-3) = 8 (add the opposite)",
             "diagram": "integer_line", "lo": 0, "hi": 10, "jump": (5, 3, "+3"),
             "marks": [(8, "8")], "caption": "minus a minus = plus"},
            {"text": "2. Sign rules for \u00d7 and \u00f7",
             "diagram": "sign_rule",
             "pairs": [("(+)(+)", "+"), ("(-)(-)", "+"), ("(+)(-)", "-"), ("(-)(+)", "-")],
             "caption": "same \u2192 +, different \u2192 -"},
            {"text": "3. (-4) \u00d7 5 = -20",
             "diagram": "integer_line", "lo": -22, "hi": 2, "marks": [(-20, "-20")],
             "caption": "different signs \u2192 negative"},
        ],
        "card": card_int_signs,
        "solved": [
            {"q": "Ex: (-8) \u00f7 4 - (-3) \u00d7 2 = ?",
             "steps": ["(-8)\u00f74 = -2; (-3)\u00d72 = -6", "-2 - (-6) = -2 + 6", "= 4"]},
        ],
        "tips": [
            "Subtract = add opposite.",
            "Same signs \u2192 +.",
            "Different signs \u2192 -.",
            "Do \u00d7 \u00f7 before + -.",
        ],
        "try_it": {
            "questions": [
                "1. 4 - (-6) = ?",
                "2. (-3) \u00d7 4 = ?",
                "3. (-20) \u00f7 5 = ?",
            ],
            "answers": "1) 10    2) -12    3) -4",
        },
    },

    # ---- 8G Word problems ----
    "8G": {
        "title": "Integer Word Problems",
        "intro": [
            "Rise / gain / up \u2192 add.",
            "Fall / drop / down \u2192 subtract.",
            "Below zero, below ground = negative.",
            "Use a number line to picture it.",
            "Keep units: C, m, Rs.",
        ],
        "real_life": [
            {"text": "1. -8 C rises 12 C \u2192 4 C",
             "diagram": "integer_line", "lo": -10, "hi": 6, "jump": (-8, 12, "+12"),
             "marks": [(4, "4")], "caption": "rise = move right"},
            {"text": "2. 5 C falls 14 C \u2192 -9 C",
             "diagram": "integer_line", "lo": -10, "hi": 6, "jump": (5, -14, "-14"),
             "marks": [(-9, "-9")], "caption": "fall = move left"},
            {"text": "3. Submarine -350 m rises 180 m \u2192 -170 m",
             "diagram": "integer_line", "lo": -5, "hi": 5, "marks": [(-2, "-170")],
             "caption": "still below the surface"},
        ],
        "card": card_int_addsub,
        "solved": [
            {"q": "Ex: -8 C rises 12 C. New temperature?",
             "steps": ["Rise \u2192 add: -8 + 12", "= 4", "Answer = 4 C"]},
        ],
        "tips": [
            "Up / gain \u2192 add.",
            "Down / fall \u2192 subtract.",
            "Below 0 = negative.",
            "Keep the units.",
        ],
        "try_it": {
            "questions": [
                "1. -3 C rises 7 C. New temp?",
                "2. 4 C falls 9 C. New temp?",
                "3. Diver at -20 m rises 8 m. New depth?",
            ],
            "answers": "1) 4 C    2) -5 C    3) -12 m",
        },
    },

    # ---- 8H Mixed integers ----
    "8H": {
        "title": "Integer Order of Operations",
        "intro": [
            "Do \u00d7 and \u00f7 before + and -.",
            "Keep the sign rules at each step.",
            "Work left to right within the same level.",
            "(-3) \u00d7 4 = -12, then add/subtract.",
            "Brackets first if present.",
        ],
        "real_life": [
            {"text": "1. (-3) \u00d7 4 = -12 first",
             "diagram": "integer_line", "lo": -14, "hi": 2, "marks": [(-12, "-12")],
             "caption": "do multiply first"},
            {"text": "2. Sign rules guide each step",
             "diagram": "sign_rule",
             "pairs": [("(+)(+)", "+"), ("(-)(-)", "+"), ("(+)(-)", "-"), ("(-)(+)", "-")],
             "caption": "same \u2192 +, different \u2192 -"},
            {"text": "3. (-6) \u00f7 2 = -3 then combine",
             "diagram": "integer_line", "lo": -5, "hi": 5, "marks": [(-3, "-3")],
             "caption": "divide before adding"},
        ],
        "card": card_int_signs,
        "solved": [
            {"q": "Ex: (-3) \u00d7 4 + (-6) \u00f7 2 = ?",
             "steps": ["(-3)\u00d74 = -12; (-6)\u00f72 = -3", "-12 + (-3)", "= -15"]},
        ],
        "tips": [
            "\u00d7 \u00f7 before + -.",
            "Apply sign rules each step.",
            "Brackets first.",
            "Left to right otherwise.",
        ],
        "try_it": {
            "questions": [
                "1. (-2) \u00d7 5 + 4 = ?",
                "2. (-8) \u00f7 4 - 3 = ?",
                "3. 6 + (-2) \u00d7 3 = ?",
            ],
            "answers": "1) -6    2) -5    3) 0",
        },
    },

    # ---- 8I Integer puzzles ----
    "8I": {
        "title": "Integer Puzzles",
        "intro": [
            "Use the two clues together.",
            "A + B and A - B are given.",
            "Add the two: 2A = sum of clues.",
            "Then A is half; find B from A + B.",
            "Check both clues at the end.",
        ],
        "real_life": [
            {"text": "1. A+B = -6, A-B = 4 \u2192 A = -1, B = -5",
             "diagram": "integer_line", "lo": -6, "hi": 2,
             "marks": [(-1, "A"), (-5, "B")], "caption": "add clues: 2A = -2"},
            {"text": "2. A+B = 3, A-B = -9 \u2192 A = -3, B = 6",
             "diagram": "integer_line", "lo": -5, "hi": 7,
             "marks": [(-3, "A"), (6, "B")], "caption": "2A = -6 \u2192 A = -3"},
            {"text": "3. A+B = 0, A-B = 14 \u2192 A = 7, B = -7",
             "diagram": "integer_line", "lo": -8, "hi": 8,
             "marks": [(7, "A"), (-7, "B")], "caption": "opposites sum to 0"},
        ],
        "card": card_integer_line,
        "solved": [
            {"q": "Ex: A+B = -6 and A-B = 4. Find A, B.",
             "steps": ["Add clues: 2A = -2 \u2192 A = -1", "A+B = -6 \u2192 B = -5"]},
        ],
        "tips": [
            "Add the two clues \u2192 2A.",
            "Half of that is A.",
            "Use A+B to get B.",
            "Check both clues.",
        ],
        "try_it": {
            "questions": [
                "1. A+B = 2, A-B = 8. Find A, B.",
                "2. A+B = -4, A-B = -10. Find A, B.",
                "3. A+B = 0, A-B = 6. Find A, B.",
            ],
            "answers": "1) A=5,B=-3    2) A=-7,B=3    3) A=3,B=-3",
        },
    },

    # ---- 8CUM3 Mixed G+H+I ----
    "8CUM3": {
        "title": "Review: Word Problems, Order, Puzzles",
        "intro": [
            "Rise \u2192 add; fall \u2192 subtract.",
            "Do \u00d7 \u00f7 before + -.",
            "Apply sign rules every step.",
            "Puzzles: add the two clues for 2A.",
            "Always check your answer.",
        ],
        "real_life": [
            {"text": "1. -8 C rises 12 C \u2192 4 C",
             "diagram": "integer_line", "lo": -10, "hi": 6, "jump": (-8, 12, "+12"),
             "marks": [(4, "4")], "caption": "rise = add"},
            {"text": "2. (-3) \u00d7 4 = -12 (multiply first)",
             "diagram": "integer_line", "lo": -14, "hi": 2, "marks": [(-12, "-12")],
             "caption": "do \u00d7 before +"},
            {"text": "3. A+B = -6, A-B = 4 \u2192 A = -1, B = -5",
             "diagram": "integer_line", "lo": -6, "hi": 2,
             "marks": [(-1, "A"), (-5, "B")], "caption": "solve with both clues"},
        ],
        "card": card_int_signs,
        "solved": [
            {"q": "Ex: 5 C falls 14 C, then (-3) \u00d7 2.",
             "steps": ["5 - 14 = -9 C", "(-3)\u00d72 = -6"]},
        ],
        "tips": [
            "Up add, down subtract.",
            "\u00d7 \u00f7 before + -.",
            "Add clues \u2192 2A in puzzles.",
            "Check the answer.",
        ],
        "try_it": {
            "questions": [
                "1. -5 C rises 9 C. New temp?",
                "2. (-4) \u00d7 3 + 2 = ?",
                "3. A+B = 4, A-B = 10. Find A, B.",
            ],
            "answers": "1) 4 C    2) -10    3) A=7,B=-3",
        },
    },

    # ---- 8J Mixed challenge ----
    "8J": {
        "title": "Integers — Mixed Challenge",
        "intro": [
            "Absolute value |x| = distance from 0.",
            "|-13| = 13 (always positive).",
            "Opposite of -8 = 8 (flip the sign).",
            "Compare: right on the line is bigger.",
            "-7 < -3 (less negative is bigger).",
        ],
        "real_life": [
            {"text": "1. |-13| = 13 (distance from 0)",
             "diagram": "integer_line", "lo": -3, "hi": 3, "marks": [(0, "0")],
             "caption": "absolute value is always +"},
            {"text": "2. Opposite of -8 is +8",
             "diagram": "integer_line", "lo": -9, "hi": 9,
             "marks": [(-8, "-8"), (8, "+8")], "caption": "same distance, other side"},
            {"text": "3. -7 < -3 (further left is smaller)",
             "diagram": "integer_line", "lo": -9, "hi": 1,
             "marks": [(-7, "-7"), (-3, "-3")], "caption": "-3 is bigger than -7"},
        ],
        "card": card_integer_line,
        "solved": [
            {"q": "Ex: Compare -7 and -3.",
             "steps": ["-3 is further right", "Right = bigger", "So -7 < -3"]},
        ],
        "tips": [
            "|x| = distance from 0 (always +).",
            "Opposite flips the sign.",
            "Right on the line = bigger.",
            "Less negative is bigger.",
        ],
        "try_it": {
            "questions": [
                "1. |-9| = ?",
                "2. Opposite of 5 = ?",
                "3. Compare -2 and -6 (use > < =).",
            ],
            "answers": "1) 9    2) -5    3) -2 > -6",
        },
    },

    # ---- 8REV Revision ----
    "8REV": {
        "title": "Level 8 Revision — Integers",
        "intro": [
            "Integers: negatives, 0, positives.",
            "Right = bigger; left = smaller.",
            "Add + right, add - left.",
            "Subtract = add the opposite.",
            "Multiply/divide: same \u2192 +, different \u2192 -.",
        ],
        "real_life": [
            {"text": "1. -3 is left of 0",
             "diagram": "integer_line", "lo": -5, "hi": 5, "marks": [(-3, "-3")],
             "caption": "negative = left"},
            {"text": "2. 7 + (-4) = 3",
             "diagram": "integer_line", "lo": -2, "hi": 8, "jump": (7, -4, "-4"),
             "marks": [(3, "3")], "caption": "add - = move left"},
            {"text": "3. Sign rules for \u00d7 \u00f7",
             "diagram": "sign_rule",
             "pairs": [("(+)(+)", "+"), ("(-)(-)", "+"), ("(+)(-)", "-"), ("(-)(+)", "-")],
             "caption": "same \u2192 +, different \u2192 -"},
        ],
        "card": card_int_addsub,
        "solved": [
            {"q": "Ex: 5 - (-3), then (-4) \u00d7 (-5).",
             "steps": ["5 + 3 = 8", "(-4)\u00d7(-5) = 20"]},
        ],
        "tips": [
            "Right bigger, left smaller.",
            "Add + right, add - left.",
            "Subtract = add opposite.",
            "Same signs +, different -.",
        ],
        "try_it": {
            "questions": [
                "1. (-6) + (-2) = ?",
                "2. 4 - (-5) = ?",
                "3. (-3) \u00d7 (-4) = ?",
            ],
            "answers": "1) -8    2) 9    3) 12",
        },
    },
}
