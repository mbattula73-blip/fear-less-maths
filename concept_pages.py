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


def factor_tree_vec(c, x, y, w, root, splits):
    """Draw a simple factor tree. splits = list of (parent_label, left, right)
    drawn top to bottom. The final primes are circled. Returns height used."""
    cxm = x + w / 2
    # root
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(cxm, y - 4 * mm, str(root))
    yy = y - 4 * mm
    level_gap = 11 * mm
    # We draw a left-leaning tree: each step splits into a prime (left) and a
    # quotient (right) that continues down.
    px = cxm
    for i, (prime, quotient, is_prime_quotient) in enumerate(splits):
        ny = yy - level_gap
        lx = px - 9 * mm
        rx = px + 9 * mm
        c.setStrokeColor(MGRAY); c.setLineWidth(0.8)
        c.line(px, yy - 1.5 * mm, lx, ny + 1.5 * mm)
        c.line(px, yy - 1.5 * mm, rx, ny + 1.5 * mm)
        # prime on the left (circled)
        c.setStrokeColor(GREEN); c.setLineWidth(1.1); c.setFillColor(LGREEN)
        c.circle(lx, ny, 3.2 * mm, fill=1, stroke=1)
        c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(lx, ny - 1.3 * mm, str(prime))
        # quotient on the right
        c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
        if is_prime_quotient:
            c.setStrokeColor(GREEN); c.setLineWidth(1.1); c.setFillColor(LGREEN)
            c.circle(rx, ny, 3.2 * mm, fill=1, stroke=1)
            c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(rx, ny - 1.3 * mm, str(quotient))
        else:
            c.drawCentredString(rx, ny - 1.3 * mm, str(quotient))
        px = rx
        yy = ny
    return (y - yy) + 8 * mm


def multiples_strip_vec(c, x, y, w, base, count, accent=GOLD):
    """Skip-counting strip: cells labelled base, 2*base, ... highlighted."""
    cell = w / count
    for i in range(count):
        c.setStrokeColor(BLACK); c.setLineWidth(0.9)
        c.setFillColor(accent)
        c.rect(x + i * cell, y, cell, 8 * mm, fill=1, stroke=1)
        c.setFillColor(WHITE if True else BLACK); c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + i * cell + cell / 2, y + 2.4 * mm, str(base * (i + 1)))
    return 8 * mm


def factor_pairs_vec(c, x, y, w, n, pairs):
    """Show factor pairs of n as rows 'a x b = n'. Returns height."""
    c.setFont("Helvetica-Bold", 10); rh = 5.5 * mm
    for i, (a, b) in enumerate(pairs):
        c.setFillColor(BLACK)
        c.drawString(x + 2 * mm, y - (i + 1) * rh + 1.4 * mm, f"{a} \u00d7 {b} = {n}")
    return len(pairs) * rh + 1 * mm


def venn_hcf_lcm_vec(c, x, y, w, leftname, rightname, left_only, common, right_only,
                     hcf=None, lcm=None):
    """Two overlapping circles showing shared (HCF) and combined (LCM) factors."""
    r = 16 * mm
    cy = y - r - 2 * mm
    lcx = x + r
    rcx = x + w - r
    c.setStrokeColor(BLUE); c.setLineWidth(1.2); c.setFillColor(WHITE)
    c.circle(lcx, cy, r, fill=0, stroke=1)
    c.setStrokeColor(PINK)
    c.circle(rcx, cy, r, fill=0, stroke=1)
    # names
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(BLUE); c.drawCentredString(lcx - r / 2, cy + r + 1 * mm, leftname)
    c.setFillColor(PINK); c.drawCentredString(rcx + r / 2, cy + r + 1 * mm, rightname)
    # contents
    c.setFillColor(BLACK); c.setFont("Helvetica", 9)
    c.drawCentredString(lcx - r / 2, cy, "  ".join(str(v) for v in left_only))
    c.drawCentredString(rcx + r / 2, cy, "  ".join(str(v) for v in right_only))
    midx = (lcx + rcx) / 2
    c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(midx, cy, "  ".join(str(v) for v in common))
    used = 2 * r + 4 * mm
    yy = cy - r - 4 * mm
    if hcf is not None:
        c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + w / 2, yy, f"HCF = biggest shared factor = {hcf}")
        yy -= 5 * mm; used += 5 * mm
    if lcm is not None:
        c.setFillColor(BLUE); c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + w / 2, yy, f"LCM = ({leftname}\u00d7{rightname})\u00f7HCF = {lcm}")
        used += 5 * mm
    return used + 4 * mm


def ratio_bar_vec(c, x, y, w, h, a, b, color_a=GOLD, color_b=BLUE):
    """A single bar split into a+b unit cells: first a cells one colour, the
    rest another colour. Returns the height used."""
    total = a + b
    cell = w / total
    for i in range(total):
        c.setStrokeColor(BLACK); c.setLineWidth(0.9)
        c.setFillColor(color_a if i < a else color_b)
        c.rect(x + i * cell, y, cell, h, fill=1, stroke=1)
    return h


def cross_multiply_vec(c, x, y, w, a, b, c2, d):
    """Bowtie cross-multiplication visual for a/b = c2/d. Returns height used."""
    fw = w * 0.28
    x1 = x + fw * 0.6
    x2 = x + w - fw * 0.6
    topy = y
    boty = y - 13 * mm
    c.setFont("Helvetica-Bold", 13); c.setFillColor(BLACK)
    c.drawCentredString(x1, topy, str(a))
    c.setStrokeColor(BLACK); c.setLineWidth(1)
    c.line(x1 - 6 * mm, topy - 3 * mm, x1 + 6 * mm, topy - 3 * mm)
    c.drawCentredString(x1, boty, str(b))
    midx = (x1 + x2) / 2
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(midx, (topy + boty) / 2 - 2.2 * mm, "=")
    c.drawCentredString(x2, topy, str(c2))
    c.line(x2 - 6 * mm, topy - 3 * mm, x2 + 6 * mm, topy - 3 * mm)
    c.drawCentredString(x2, boty, str(d))
    c.setStrokeColor(GOLD); c.setLineWidth(1.3)
    c.line(x1 + 3 * mm, topy - 1 * mm, x2 - 3 * mm, boty + 2 * mm)
    c.line(x1 + 3 * mm, boty + 2 * mm, x2 - 3 * mm, topy - 1 * mm)
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawCentredString(midx, boty - 8 * mm, f"{a}\u00d7{d} = {a*d}    {b}\u00d7{c2} = {b*c2}")
    return (topy - boty) + 8 * mm + 6 * mm


def small_table_vec(c, x, y, w, headers, rows, accent=BLUE, light=LBLUE):
    """A simple grid table. Returns the height used."""
    n_cols = len(headers)
    col_w = w / n_cols
    row_h = 6.5 * mm
    c.setFillColor(light); c.setStrokeColor(accent); c.setLineWidth(0.8)
    c.rect(x, y - row_h, w, row_h, fill=1, stroke=1)
    c.setFillColor(accent); c.setFont("Helvetica-Bold", 9)
    for i, hd in enumerate(headers):
        c.drawCentredString(x + col_w * (i + 0.5), y - row_h + 1.8 * mm, str(hd))
    yy = y - row_h
    c.setFont("Helvetica", 9)
    for row in rows:
        yy -= row_h
        c.setFillColor(WHITE); c.setStrokeColor(LGRAY); c.setLineWidth(0.5)
        c.rect(x, yy, w, row_h, fill=1, stroke=1)
        c.setFillColor(BLACK)
        for i, cell in enumerate(row):
            c.drawCentredString(x + col_w * (i + 0.5), yy + 1.8 * mm, str(cell))
    c.setStrokeColor(LGRAY); c.setLineWidth(0.5)
    for i in range(1, n_cols):
        c.line(x + col_w * i, yy, x + col_w * i, y - row_h)
    return (len(rows) + 1) * row_h


def balance_scale_vec(c, x, y, w, left_text, right_text):
    """A balance scale showing left_text = right_text (level beam). Returns height."""
    cxm = x + w / 2
    beam_y = y - 6 * mm
    c.setFillColor(MGRAY)
    p = c.beginPath()
    p.moveTo(cxm - 4 * mm, beam_y - 8 * mm)
    p.lineTo(cxm + 4 * mm, beam_y - 8 * mm)
    p.lineTo(cxm, beam_y)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setStrokeColor(BLACK); c.setLineWidth(1.6)
    c.line(x + 8 * mm, beam_y, x + w - 8 * mm, beam_y)
    pan_w = w * 0.32
    lx = x + 8 * mm
    rx = x + w - 8 * mm - pan_w
    pan_y = beam_y - 15 * mm
    c.setStrokeColor(MGRAY); c.setLineWidth(0.8)
    c.line(lx + pan_w / 2, beam_y, lx + pan_w / 2, pan_y + 8 * mm)
    c.line(rx + pan_w / 2, beam_y, rx + pan_w / 2, pan_y + 8 * mm)
    c.setFillColor(LBLUE); c.setStrokeColor(BLUE); c.setLineWidth(1)
    c.rect(lx, pan_y, pan_w, 8 * mm, fill=1, stroke=1)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(lx + pan_w / 2, pan_y + 2.6 * mm, left_text)
    c.setFillColor(LGOLD); c.setStrokeColor(GOLD)
    c.rect(rx, pan_y, pan_w, 8 * mm, fill=1, stroke=1)
    c.setFillColor(BLACK)
    c.drawCentredString(rx + pan_w / 2, pan_y + 2.6 * mm, right_text)
    c.setFont("Helvetica-Bold", 10); c.setFillColor(GREEN)
    c.drawCentredString(cxm, pan_y - 5 * mm, "Balanced \u2014 both sides are EQUAL")
    return (y - pan_y) + 7 * mm


def function_machine_vec(c, x, y, w, input_val, operation, output_val):
    """Input -> operation box -> output. Returns height used."""
    cy = y - 8 * mm
    box_w = w * 0.36
    box_x = x + (w - box_w) / 2
    c.setFont("Helvetica-Bold", 12); c.setFillColor(BLACK)
    c.drawCentredString(x + 9 * mm, cy, str(input_val))
    c.setStrokeColor(GOLD); c.setLineWidth(1.3)
    c.line(x + 14 * mm, cy, box_x - 2 * mm, cy)
    c.line(box_x - 2 * mm, cy, box_x - 5 * mm, cy + 1.6 * mm)
    c.line(box_x - 2 * mm, cy, box_x - 5 * mm, cy - 1.6 * mm)
    c.setFillColor(LGREEN); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.rect(box_x, cy - 6.5 * mm, box_w, 13 * mm, fill=1, stroke=1)
    c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(box_x + box_w / 2, cy - 1.6 * mm, operation)
    c.setStrokeColor(GOLD)
    c.line(box_x + box_w + 2 * mm, cy, x + w - 14 * mm, cy)
    c.line(x + w - 14 * mm, cy, x + w - 17 * mm, cy + 1.6 * mm)
    c.line(x + w - 14 * mm, cy, x + w - 17 * mm, cy - 1.6 * mm)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(x + w - 7 * mm, cy, str(output_val))
    c.setFont("Helvetica-Oblique", 8); c.setFillColor(MGRAY)
    c.drawCentredString(x + 9 * mm, cy - 11 * mm, "in")
    c.drawCentredString(x + w - 7 * mm, cy - 11 * mm, "out")
    return 20 * mm


def term_breakdown_vec(c, x, y, w, coeff, var):
    """Highlight coefficient vs variable in a term like 3x. Returns height."""
    cxm = x + w / 2
    c.setFont("Helvetica-Bold", 24)
    cw = stringWidth(str(coeff), "Helvetica-Bold", 24)
    vw = stringWidth(var, "Helvetica-Bold", 24)
    startx = cxm - (cw + vw) / 2
    c.setFillColor(GOLD)
    c.drawString(startx, y - 8 * mm, str(coeff))
    c.setFillColor(BLUE)
    c.drawString(startx + cw, y - 8 * mm, var)
    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.line(startx + cw / 2, y - 10 * mm, startx + cw / 2, y - 14 * mm)
    c.setStrokeColor(BLUE)
    c.line(startx + cw + vw / 2, y - 10 * mm, startx + cw + vw / 2, y - 14 * mm)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(GOLD)
    c.drawCentredString(startx + cw / 2, y - 18 * mm, "coefficient")
    c.setFillColor(BLUE)
    c.drawCentredString(startx + cw + vw / 2, y - 18 * mm, "variable")
    return 22 * mm


def like_terms_vec(c, x, y, w, group_a, label_a, group_b, label_b):
    """Two coloured boxes grouping like terms. Returns height used."""
    bw = w * 0.46
    bx1 = x
    bx2 = x + w - bw
    by = y - 15 * mm
    c.setFillColor(LBLUE); c.setStrokeColor(BLUE); c.setLineWidth(1.1)
    c.roundRect(bx1, by, bw, 15 * mm, 2 * mm, fill=1, stroke=1)
    c.setFillColor(BLUE); c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(bx1 + bw / 2, by + 9 * mm, "  ".join(group_a))
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(bx1 + bw / 2, by + 3 * mm, label_a)
    c.setFillColor(LPINK); c.setStrokeColor(PINK); c.setLineWidth(1.1)
    c.roundRect(bx2, by, bw, 15 * mm, 2 * mm, fill=1, stroke=1)
    c.setFillColor(PINK); c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(bx2 + bw / 2, by + 9 * mm, "  ".join(group_b))
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(bx2 + bw / 2, by + 3 * mm, label_b)
    return 19 * mm


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
    if kind == "factor_tree":
        used = factor_tree_vec(c, x + 4 * mm, y - 2 * mm, w - 8 * mm,
                              rl["root"], rl["splits"])
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - used - 4 * mm, rl.get("caption", ""))
        return used + 8 * mm
    if kind == "multiples_strip":
        used = multiples_strip_vec(c, x + 4 * mm, y - 10 * mm, w - 8 * mm,
                                  rl["base"], rl["count"])
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - 16 * mm, rl.get("caption", ""))
        return 20 * mm
    if kind == "factor_pairs":
        used = factor_pairs_vec(c, x + 4 * mm, y - 2 * mm, w - 8 * mm,
                               rl["n"], rl["pairs"])
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - used - 5 * mm, rl.get("caption", ""))
        return used + 9 * mm
    if kind == "venn":
        used = venn_hcf_lcm_vec(c, x + 4 * mm, y - 2 * mm, w - 8 * mm,
                               rl["leftname"], rl["rightname"],
                               rl["left_only"], rl["common"], rl["right_only"],
                               rl.get("hcf"), rl.get("lcm"))
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(cxm, y - used - 2 * mm, rl.get("caption", ""))
        return used + 6 * mm
    if kind == "ratio_bar":
        ratio_bar_vec(c, x + 4 * mm, y - 13 * mm, w - 8 * mm, 11 * mm,
                     rl["a"], rl["b"], color_a=GOLD, color_b=BLUE)
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - 20 * mm, rl.get("caption", ""))
        return 24 * mm
    if kind == "cross_multiply":
        used = cross_multiply_vec(c, x + 4 * mm, y - 2 * mm, w - 8 * mm,
                                 rl["a"], rl["b"], rl["c2"], rl["d"])
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - used - 2 * mm, rl.get("caption", ""))
        return used + 6 * mm
    if kind == "table":
        used = small_table_vec(c, x + 4 * mm, y, w - 8 * mm,
                              rl["headers"], rl["rows"])
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - used - 2 * mm, rl.get("caption", ""))
        return used + 7 * mm
    if kind == "balance_scale":
        used = balance_scale_vec(c, x + 4 * mm, y - 2 * mm, w - 8 * mm,
                                rl["left_text"], rl["right_text"])
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - used - 6 * mm, rl.get("caption", ""))
        return used + 10 * mm
    if kind == "function_machine":
        used = function_machine_vec(c, x + 4 * mm, y - 4 * mm, w - 8 * mm,
                                   rl["input_val"], rl["operation"], rl["output_val"])
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - used - 6 * mm, rl.get("caption", ""))
        return used + 10 * mm
    if kind == "term_breakdown":
        used = term_breakdown_vec(c, x + 4 * mm, y, w - 8 * mm,
                                 rl["coeff"], rl["var"])
        c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(cxm, y - used - 2 * mm, rl.get("caption", ""))
        return used + 6 * mm
    if kind == "like_terms":
        used = like_terms_vec(c, x + 4 * mm, y - 2 * mm, w - 8 * mm,
                             rl["group_a"], rl["label_a"], rl["group_b"], rl["label_b"])
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


def card_factors(c, x, y, w):
    """Factor pairs of 12 shown as a card."""
    card_h = 56 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, y - 8 * mm, "Factors of 12 (numbers that divide it exactly):")
    factor_pairs_vec(c, bx, y - 13 * mm, bw, 12,
                     [(1, 12), (2, 6), (3, 4)])
    c.setFont("Helvetica-Bold", 11); c.setFillColor(GREEN)
    c.drawString(bx, y - 36 * mm, "Factors of 12: 1, 2, 3, 4, 6, 12")
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawString(bx, y - 43 * mm, "Check: does it divide with NO remainder?")
    c.drawString(bx, y - 49 * mm, "12 \u00f7 3 = 4 exactly \u2192 3 is a factor.")
    return y - card_h - 2 * mm


def card_multiples(c, x, y, w):
    """Multiples strip for 4."""
    card_h = 50 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, y - 8 * mm, "Multiples of 4 (skip-count by 4):")
    multiples_strip_vec(c, bx, y - 22 * mm, bw, 4, 6)
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawString(bx, y - 30 * mm, "4, 8, 12, 16, 20, 24, ...")
    c.setFont("Helvetica-Bold", 10); c.setFillColor(GREEN)
    c.drawString(bx, y - 38 * mm, "A multiple = the number \u00d7 1, 2, 3, ...")
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawString(bx, y - 44 * mm, "Multiples never stop \u2014 there are infinite!")
    return y - card_h - 2 * mm


def card_factor_tree(c, x, y, w):
    """Factor tree for 12 = 2 x 2 x 3."""
    card_h = 58 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 5 * mm, y - 7 * mm, "Factor Tree of 12:")
    factor_tree_vec(c, x + 4 * mm, y - 11 * mm, w - 8 * mm, 12,
                    [(2, 6, False), (2, 3, True)])
    c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(x + w / 2, y - 44 * mm, "12 = 2 \u00d7 2 \u00d7 3 = 2^2 × 3")
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawCentredString(x + w / 2, y - 51 * mm, "Keep splitting until every branch is PRIME.")
    return y - card_h - 2 * mm


def card_hcf_lcm(c, x, y, w):
    """Venn diagram card for HCF/LCM of 12 and 18."""
    card_h = 62 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 5 * mm, y - 7 * mm, "HCF & LCM of 12 and 18:")
    venn_hcf_lcm_vec(c, x + 4 * mm, y - 11 * mm, w - 8 * mm,
                     "12", "18", [4], [1, 2, 3, 6], [9, 18],
                     hcf=6, lcm=36)
    return y - card_h - 2 * mm


def card_ratio(c, x, y, w):
    """Ratio bar card: 3 red : 5 blue = 3:5."""
    card_h = 58 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    ratio_bar_vec(c, bx, y - 16 * mm, bw, 12 * mm, 3, 5, color_a=GOLD, color_b=BLUE)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 12)
    c.drawString(bx, y - 23 * mm, "3 red : 5 blue  =  3 : 5")
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawString(bx, y - 31 * mm, "Order matters! 3:5 is not the same as 5:3.")
    c.drawString(bx, y - 37 * mm, "A ratio compares two quantities.")
    c.setFont("Helvetica-Bold", 10); c.setFillColor(GOLD)
    c.drawString(bx, y - 45 * mm, "\u25a0 = red (3 parts)")
    c.setFillColor(BLUE)
    c.drawString(bx, y - 51 * mm, "\u25a0 = blue (5 parts)")
    return y - card_h - 2 * mm


def card_simplify_ratio(c, x, y, w):
    """Before/after bars showing simplifying 8:4 to 2:1 using HCF."""
    card_h = 60 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    ratio_bar_vec(c, bx, y - 16 * mm, bw, 11 * mm, 8, 4, color_a=GOLD, color_b=BLUE)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, y - 23 * mm, "8 : 4  (before)")
    ratio_bar_vec(c, bx, y - 36 * mm, bw * 0.5, 11 * mm, 2, 1, color_a=GOLD, color_b=BLUE)
    c.drawString(bx, y - 43 * mm, "2 : 1  (after \u00f7 HCF=4)")
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawString(bx, y - 51 * mm, "Divide BOTH sides by their HCF.")
    return y - card_h - 2 * mm


def card_equivalent_ratio(c, x, y, w):
    """Two bars showing 1:2 scaled to 2:4 (equivalent ratios)."""
    card_h = 60 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    ratio_bar_vec(c, bx, y - 16 * mm, bw * 0.4, 11 * mm, 1, 2, color_a=GOLD, color_b=BLUE)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, y - 23 * mm, "1 : 2")
    ratio_bar_vec(c, bx, y - 38 * mm, bw * 0.8, 11 * mm, 2, 4, color_a=GOLD, color_b=BLUE)
    c.drawString(bx, y - 45 * mm, "2 : 4  (\u00d72, same proportion)")
    c.setFont("Helvetica-Bold", 11); c.setFillColor(GREEN)
    c.drawCentredString(x + w / 2, y - 53 * mm, "1:2 = 2:4 = 3:6  (equivalent)")
    return y - card_h - 2 * mm


def card_proportion(c, x, y, w):
    """Cross-multiplication bowtie card for checking 2:3 = 4:6."""
    card_h = 56 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 5 * mm, y - 7 * mm, "Check: is 2:3 = 4:6 a proportion?")
    cross_multiply_vec(c, x + 4 * mm, y - 13 * mm, w - 8 * mm, 2, 3, 4, 6)
    c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(x + w / 2, y - 44 * mm, "2\u00d76 = 12 and 3\u00d74 = 12 \u2192 EQUAL!")
    c.setFillColor(MGRAY); c.setFont("Helvetica", 9.5)
    c.drawCentredString(x + w / 2, y - 50 * mm, "Cross products match \u2192 it IS a proportion.")
    return y - card_h - 2 * mm


def card_direct_inverse(c, x, y, w):
    """Two small tables contrasting direct and inverse proportion."""
    card_h = 76 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(bx, y - 7 * mm, "Direct: y \u00f7 x = k (constant)")
    small_table_vec(c, bx, y - 10 * mm, bw, ["x", "y"], [["2", "6"], ["4", "12"], ["6", "18"]],
                    accent=GREEN, light=LGREEN)
    c.setFillColor(PINK); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(bx, y - 41 * mm, "Inverse: x \u00d7 y = k (constant)")
    small_table_vec(c, bx, y - 44 * mm, bw, ["x", "y"], [["2", "12"], ["4", "6"], ["6", "4"]],
                    accent=PINK, light=LPINK)
    return y - card_h - 2 * mm


def card_variable(c, x, y, w):
    """A variable as a mystery box that can hold any number."""
    card_h = 56 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    bx = x + 5 * mm; bw = w - 10 * mm
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, y - 8 * mm, "A variable is a MYSTERY BOX:")
    box_w = 22 * mm
    c.setFillColor(LBLUE); c.setStrokeColor(BLUE); c.setLineWidth(1.2)
    c.roundRect(bx, y - 30 * mm, box_w, 16 * mm, 2 * mm, fill=1, stroke=1)
    c.setFillColor(BLUE); c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(bx + box_w / 2, y - 24 * mm, "x")
    c.setStrokeColor(GOLD); c.setLineWidth(1.3)
    c.line(bx + box_w + 2 * mm, y - 22 * mm, bx + box_w + 14 * mm, y - 22 * mm)
    c.line(bx + box_w + 14 * mm, y - 22 * mm, bx + box_w + 11 * mm, y - 20.5 * mm)
    c.line(bx + box_w + 14 * mm, y - 22 * mm, bx + box_w + 11 * mm, y - 23.5 * mm)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 14)
    c.drawString(bx + box_w + 17 * mm, y - 24 * mm, "could be 4, 7, 100...")
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawString(bx, y - 40 * mm, "x is a LETTER that stands for an unknown number.")
    c.drawString(bx, y - 46 * mm, "If x = 4, the box holds 4. Any letter can be used.")
    return y - card_h - 2 * mm


def card_expression_parts(c, x, y, w):
    """Term breakdown card showing coefficient and variable in 3x + 5."""
    card_h = 58 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 5 * mm, y - 7 * mm, "Parts of a term:")
    term_breakdown_vec(c, x + 4 * mm, y - 9 * mm, w - 8 * mm, 3, "x")
    bx = x + 5 * mm
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawString(bx, y - 38 * mm, "3x + 5 has TWO terms: 3x and 5.")
    c.drawString(bx, y - 44 * mm, "3x is a variable term (has a letter).")
    c.drawString(bx, y - 50 * mm, "5 is a constant term (just a number).")
    return y - card_h - 2 * mm


def card_like_unlike(c, x, y, w):
    """Like-terms grouping card: x-terms vs y-terms."""
    card_h = 58 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 5 * mm, y - 7 * mm, "Like terms have the SAME letter:")
    like_terms_vec(c, x + 4 * mm, y - 10 * mm, w - 8 * mm,
                   ["3x", "5x"], "x-terms (LIKE)", ["2y", "7y"], "y-terms (LIKE)")
    bx = x + 5 * mm
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawString(bx, y - 38 * mm, "3x and 5x are LIKE (both have x).")
    c.drawString(bx, y - 44 * mm, "3x and 2y are UNLIKE (different letters).")
    c.setFont("Helvetica-Bold", 10); c.setFillColor(GREEN)
    c.drawString(bx, y - 51 * mm, "Only LIKE terms can be combined.")
    return y - card_h - 2 * mm


def card_substitution(c, x, y, w):
    """Function-machine card for substitution: x + 4, x=3 -> 7."""
    card_h = 56 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 5 * mm, y - 7 * mm, "Substitute: plug in the number for x")
    function_machine_vec(c, x + 4 * mm, y - 13 * mm, w - 8 * mm, "x = 3", "+ 4", "7")
    bx = x + 5 * mm
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawString(bx, y - 38 * mm, "Replace x with its value, then work it out.")
    c.drawString(bx, y - 44 * mm, "x + 4, with x=3, becomes 3 + 4 = 7.")
    c.setFont("Helvetica-Bold", 10); c.setFillColor(GREEN)
    c.drawString(bx, y - 51 * mm, "This works for ANY expression!")
    return y - card_h - 2 * mm


def card_balance(c, x, y, w):
    """Balance scale card for simple equations like x+3=7."""
    card_h = 58 * mm
    c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.1)
    c.roundRect(x, y - card_h, w, card_h, 2 * mm, fill=1, stroke=1)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 5 * mm, y - 7 * mm, "An equation is a BALANCED scale:")
    balance_scale_vec(c, x + 4 * mm, y - 10 * mm, w - 8 * mm, "x + 3", "7")
    bx = x + 5 * mm
    c.setFont("Helvetica", 9.5); c.setFillColor(MGRAY)
    c.drawString(bx, y - 43 * mm, "Both sides must stay EQUAL.")
    c.drawString(bx, y - 49 * mm, "Take 3 from both sides: x = 4.")
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
    if level_num == 9:
        return _L9.get(sublevel_code)
    if level_num == 10:
        return _L10.get(sublevel_code)
    if level_num == 11:
        return _L11.get(sublevel_code)
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


# ───────────────────────────────────────────────────────────────────────────────
# LEVEL 9 — Factors, Multiples & HCF/LCM: concept page specs (sheet 1)
# ───────────────────────────────────────────────────────────────────────────────
_L9 = {
    # ---- 9A Factors ----
    "9A": {
        "title": "Factors",
        "intro": [
            "A factor divides a number with NO remainder.",
            "Check: does it divide exactly?",
            "Every number has 1 and itself as factors.",
            "Factors come in pairs: a \u00d7 b = n.",
            "12 = 1\u00d712 = 2\u00d76 = 3\u00d74.",
        ],
        "real_life": [
            {"text": "1. 12 sweets shared in equal rows: 3\u00d74=12",
             "diagram": "factor_pairs", "n": 12, "pairs": [(1, 12), (2, 6), (3, 4)],
             "caption": "all factor pairs of 12"},
            {"text": "2. Is 5 a factor of 12? 12\u00f75 = 2 r 2 \u2192 No",
             "diagram": "factor_pairs", "n": 12, "pairs": [(2, 6), (3, 4)],
             "caption": "5 does not divide evenly"},
            {"text": "3. Arrange 18 chairs in equal rows: 2\u00d79, 3\u00d76",
             "diagram": "factor_pairs", "n": 18, "pairs": [(1, 18), (2, 9), (3, 6)],
             "caption": "factor pairs of 18"},
        ],
        "card": card_factors,
        "solved": [
            {"q": "Ex: Is 3 a factor of 12?",
             "steps": ["12 \u00f7 3 = 4", "No remainder", "Yes, 3 is a factor"]},
        ],
        "tips": [
            "Factor \u2192 divides exactly (no remainder).",
            "1 and the number itself are always factors.",
            "List factors in pairs.",
            "Check each pair multiplies back to n.",
        ],
        "try_it": {
            "questions": [
                "1. Is 4 a factor of 20?",
                "2. List all factors of 15.",
                "3. Is 6 a factor of 21?",
            ],
            "answers": "1) Yes    2) 1,3,5,15    3) No",
        },
    },

    # ---- 9B Multiples ----
    "9B": {
        "title": "Multiples",
        "intro": [
            "A multiple = the number times 1, 2, 3...",
            "Multiples of 3: 3, 6, 9, 12, 15...",
            "Skip-count to find multiples.",
            "Multiples never stop (infinite).",
            "A number IS a multiple of its own factors.",
        ],
        "real_life": [
            {"text": "1. Multiples of 3: skip-count by 3s",
             "diagram": "multiples_strip", "base": 3, "count": 6,
             "caption": "3, 6, 9, 12, 15, 18"},
            {"text": "2. Multiples of 5: skip-count by 5s",
             "diagram": "multiples_strip", "base": 5, "count": 6,
             "caption": "5, 10, 15, 20, 25, 30"},
            {"text": "3. Multiples of 7: skip-count by 7s",
             "diagram": "multiples_strip", "base": 7, "count": 6,
             "caption": "7, 14, 21, 28, 35, 42"},
        ],
        "card": card_multiples,
        "solved": [
            {"q": "Ex: Write the first 6 multiples of 6.",
             "steps": ["6\u00d71, 6\u00d72, 6\u00d73, ...", "Answer: 6,12,18,24,30,36"]},
        ],
        "tips": [
            "Multiple = number \u00d7 1,2,3,...",
            "Skip-count to list them.",
            "Multiples go on forever.",
            "0 is a multiple of every number.",
        ],
        "try_it": {
            "questions": [
                "1. First 6 multiples of 4.",
                "2. First 6 multiples of 9.",
                "3. Is 28 a multiple of 7?",
            ],
            "answers": "1) 4,8,12,16,20,24    2) 9,18,27,36,45,54    3) Yes",
        },
    },

    # ---- 9C Prime factorisation ----
    "9C": {
        "title": "Prime Factorisation",
        "intro": [
            "Break a number into PRIME factors only.",
            "A prime has exactly 2 factors: 1 and itself.",
            "Use a factor tree: split until all primes.",
            "12 = 2 \u00d7 2 \u00d7 3 = 2^2 × 3.",
            "Write repeated primes with powers.",
        ],
        "real_life": [
            {"text": "1. 8 = 2 \u00d7 2 \u00d7 2 = 2^3",
             "diagram": "factor_tree", "root": 8, "splits": [(2, 4, False), (2, 2, True)],
             "caption": "8 = 2^3"},
            {"text": "2. 18 = 2 \u00d7 3 \u00d7 3 = 2 \u00d7 3^2",
             "diagram": "factor_tree", "root": 18, "splits": [(2, 9, False), (3, 3, True)],
             "caption": "18 = 2 \u00d7 3^2"},
            {"text": "3. 20 = 2 \u00d7 2 \u00d7 5 = 2^2 × 5",
             "diagram": "factor_tree", "root": 20, "splits": [(2, 10, False), (2, 5, True)],
             "caption": "20 = 2^2 × 5"},
        ],
        "card": card_factor_tree,
        "solved": [
            {"q": "Ex: Find the prime factorisation of 12.",
             "steps": ["12 = 2 \u00d7 6", "6 = 2 \u00d7 3", "12 = 2 \u00d7 2 \u00d7 3 = 2^2×3"]},
        ],
        "tips": [
            "Prime = only 1 and itself divide it.",
            "Split until every branch is prime.",
            "Circle the primes on the tree.",
            "Write repeats with a power.",
        ],
        "try_it": {
            "questions": [
                "1. Prime factorise 16.",
                "2. Prime factorise 30.",
                "3. Prime factorise 24.",
            ],
            "answers": "1) 2^4    2) 2\u00d73\u00d75    3) 2^3\u00d73",
        },
    },

    # ---- 9CUM1 Mixed A+B+C ----
    "9CUM1": {
        "title": "Review: Factors, Multiples, Prime Factorisation",
        "intro": [
            "Factor: divides exactly, no remainder.",
            "Multiple: number \u00d7 1, 2, 3...",
            "Prime factorisation: split into primes only.",
            "Use a factor tree for prime factorisation.",
            "Factors are finite; multiples are infinite.",
        ],
        "real_life": [
            {"text": "1. Factors of 12: 1,2,3,4,6,12",
             "diagram": "factor_pairs", "n": 12, "pairs": [(1, 12), (2, 6), (3, 4)],
             "caption": "factor pairs of 12"},
            {"text": "2. Multiples of 3: 3,6,9,12,15,18",
             "diagram": "multiples_strip", "base": 3, "count": 6,
             "caption": "skip-count by 3"},
            {"text": "3. 12 = 2^2 × 3",
             "diagram": "factor_tree", "root": 12, "splits": [(2, 6, False), (2, 3, True)],
             "caption": "prime factorisation"},
        ],
        "card": card_factor_tree,
        "solved": [
            {"q": "Ex: Is 4 a factor of 20? List 3 multiples of 5.",
             "steps": ["20\u00f74=5, yes", "Multiples of 5: 5,10,15"]},
        ],
        "tips": [
            "Factor \u2192 divides exactly.",
            "Multiple \u2192 number \u00d7 1,2,3...",
            "Tree splits to primes only.",
            "Powers show repeated primes.",
        ],
        "try_it": {
            "questions": [
                "1. List all factors of 18.",
                "2. First 5 multiples of 6.",
                "3. Prime factorise 28.",
            ],
            "answers": "1) 1,2,3,6,9,18    2) 6,12,18,24,30    3) 2^2×7",
        },
    },

    # ---- 9D HCF ----
    "9D": {
        "title": "HCF — Highest Common Factor",
        "intro": [
            "HCF = the BIGGEST factor shared by numbers.",
            "List factors of each, find common ones.",
            "Pick the largest common factor.",
            "Factors of 8: 1,2,4,8. Of 12: 1,2,3,4,6,12.",
            "Common: 1,2,4 \u2192 HCF(8,12) = 4.",
        ],
        "real_life": [
            {"text": "1. HCF(8,12) = 4 (shared factors)",
             "diagram": "venn", "leftname": "8", "rightname": "12",
             "left_only": [8], "common": [1, 2, 4], "right_only": [3, 6, 12],
             "hcf": 4, "caption": "biggest shared factor"},
            {"text": "2. HCF(10,15) = 5",
             "diagram": "venn", "leftname": "10", "rightname": "15",
             "left_only": [2, 10], "common": [1, 5], "right_only": [3, 15],
             "hcf": 5, "caption": "shared factors 1,5"},
            {"text": "3. HCF(12,20) = 4",
             "diagram": "venn", "leftname": "12", "rightname": "20",
             "left_only": [3, 6, 12], "common": [1, 2, 4], "right_only": [5, 10, 20],
             "hcf": 4, "caption": "biggest shared = 4"},
        ],
        "card": card_hcf_lcm,
        "solved": [
            {"q": "Ex: Find HCF(12,18).",
             "steps": ["Factors 12: 1,2,3,4,6,12", "Factors 18: 1,2,3,6,9,18",
                       "Common: 1,2,3,6 \u2192 HCF = 6"]},
        ],
        "tips": [
            "HCF = biggest shared factor.",
            "List factors of each number.",
            "Circle the common ones.",
            "Pick the largest.",
        ],
        "try_it": {
            "questions": [
                "1. HCF(6,9) = ?",
                "2. HCF(14,21) = ?",
                "3. HCF(16,24) = ?",
            ],
            "answers": "1) 3    2) 7    3) 8",
        },
    },

    # ---- 9E LCM ----
    "9E": {
        "title": "LCM — Lowest Common Multiple",
        "intro": [
            "LCM = the SMALLEST multiple shared by numbers.",
            "List multiples of each, find common ones.",
            "Pick the smallest common multiple.",
            "Multiples of 3: 3,6,9,12. Of 4: 4,8,12.",
            "Common: 12 \u2192 LCM(3,4) = 12.",
        ],
        "real_life": [
            {"text": "1. LCM(3,4) = 12 (first shared multiple)",
             "diagram": "venn", "leftname": "mult. of 3", "rightname": "mult. of 4",
             "left_only": [3, 6, 9], "common": [12], "right_only": [4, 8, 16],
             "lcm": 12, "caption": "smallest shared multiple"},
            {"text": "2. LCM(4,5) = 20",
             "diagram": "venn", "leftname": "mult. of 4", "rightname": "mult. of 5",
             "left_only": [4, 8, 12], "common": [20], "right_only": [5, 10, 15],
             "lcm": 20, "caption": "smallest shared = 20"},
            {"text": "3. LCM(2,7) = 14",
             "diagram": "venn", "leftname": "mult. of 2", "rightname": "mult. of 7",
             "left_only": [2, 4, 6], "common": [14], "right_only": [7, 21, 28],
             "lcm": 14, "caption": "smallest shared = 14"},
        ],
        "card": card_hcf_lcm,
        "solved": [
            {"q": "Ex: Find LCM(4,6).",
             "steps": ["Multiples of 4: 4,8,12,16", "Multiples of 6: 6,12,18",
                       "First common: 12 \u2192 LCM = 12"]},
        ],
        "tips": [
            "LCM = smallest shared multiple.",
            "List multiples of each.",
            "Find the first match.",
            "LCM is never smaller than the numbers.",
        ],
        "try_it": {
            "questions": [
                "1. LCM(2,3) = ?",
                "2. LCM(5,6) = ?",
                "3. LCM(4,10) = ?",
            ],
            "answers": "1) 6    2) 30    3) 20",
        },
    },

    # ---- 9CUM2 Mixed D+E+F ----
    "9CUM2": {
        "title": "Review: HCF, LCM, Word Problems",
        "intro": [
            "HCF = biggest shared factor.",
            "LCM = smallest shared multiple.",
            "Equal groups, no leftover \u2192 use HCF.",
            "Events repeating together \u2192 use LCM.",
            "List factors/multiples, then compare.",
        ],
        "real_life": [
            {"text": "1. HCF(12,18) = 6 (equal bundles)",
             "diagram": "venn", "leftname": "12", "rightname": "18",
             "left_only": [4, 12], "common": [1, 2, 3, 6], "right_only": [9, 18],
             "hcf": 6, "caption": "biggest shared factor"},
            {"text": "2. LCM(4,6) = 12 (events repeat together)",
             "diagram": "venn", "leftname": "mult. of 4", "rightname": "mult. of 6",
             "left_only": [4, 8, 16], "common": [12], "right_only": [6, 18, 24],
             "lcm": 12, "caption": "smallest shared multiple"},
            {"text": "3. 24 pens, 36 pencils \u2192 max bundles = HCF = 12",
             "diagram": "venn", "leftname": "24", "rightname": "36",
             "left_only": [8, 24], "common": [1, 2, 3, 4, 6, 12], "right_only": [9, 18, 36],
             "hcf": 12, "caption": "largest equal bundle size"},
        ],
        "card": card_hcf_lcm,
        "solved": [
            {"q": "Ex: 12 pens, 18 pencils \u2014 max equal bundles?",
             "steps": ["Need HCF(12,18)", "= 6", "6 bundles, no leftover"]},
        ],
        "tips": [
            "Bundles/groups \u2192 HCF.",
            "Repeating together \u2192 LCM.",
            "List then compare.",
            "Check the answer fits the story.",
        ],
        "try_it": {
            "questions": [
                "1. HCF(15,25) = ?",
                "2. LCM(3,5) = ?",
                "3. 18 boys, 24 girls, equal teams. Max team size?",
            ],
            "answers": "1) 5    2) 15    3) 6",
        },
    },

    # ---- 9F Word problems ----
    "9F": {
        "title": "HCF/LCM Word Problems",
        "intro": [
            "Equal groups, no leftovers \u2192 HCF.",
            "Cutting into equal pieces \u2192 HCF.",
            "Events that repeat together \u2192 LCM.",
            "Read carefully: \u2018max/largest\u2019 = HCF often.",
            "\u2018first time together\u2019 = LCM often.",
        ],
        "real_life": [
            {"text": "1. 12 pens, 18 pencils, equal bundles: HCF=6",
             "diagram": "venn", "leftname": "12", "rightname": "18",
             "left_only": [4, 12], "common": [1, 2, 3, 6], "right_only": [9, 18],
             "hcf": 6, "caption": "max bundle size = 6"},
            {"text": "2. Ropes 24m, 36m, equal pieces: HCF=12",
             "diagram": "venn", "leftname": "24", "rightname": "36",
             "left_only": [8, 24], "common": [1, 2, 3, 4, 6, 12], "right_only": [9, 18, 36],
             "hcf": 12, "caption": "longest equal piece = 12m"},
            {"text": "3. 48 boys, 60 girls, equal teams: HCF=12",
             "diagram": "venn", "leftname": "48", "rightname": "60",
             "left_only": [16, 48], "common": [1, 2, 3, 4, 6, 12], "right_only": [20, 60],
             "hcf": 12, "caption": "largest team size = 12"},
        ],
        "card": card_hcf_lcm,
        "solved": [
            {"q": "Ex: 24m and 36m ropes cut equally, no waste. Longest piece?",
             "steps": ["Need HCF(24,36)", "= 12", "Longest piece = 12 m"]},
        ],
        "tips": [
            "Equal groups/pieces \u2192 HCF.",
            "Repeats together \u2192 LCM.",
            "\u2018Max/largest\u2019 often means HCF.",
            "Check units in the final answer.",
        ],
        "try_it": {
            "questions": [
                "1. 16 apples, 24 oranges, equal baskets. Max baskets?",
                "2. Ropes 18m, 30m, equal pieces. Longest piece?",
                "3. 20 boys, 28 girls, equal teams. Max team size?",
            ],
            "answers": "1) 8    2) 6 m    3) 4",
        },
    },

    # ---- 9G Applications ----
    "9G": {
        "title": "Simplifying Fractions with HCF",
        "intro": [
            "Find HCF of top and bottom.",
            "Divide BOTH by the HCF.",
            "Result is in simplest form.",
            "6/9: HCF(6,9)=3 \u2192 6\u00f73 / 9\u00f73 = 2/3.",
            "If HCF = 1, already simplest.",
        ],
        "real_life": [
            {"text": "1. Simplify 6/9 using HCF=3",
             "diagram": "venn", "leftname": "6", "rightname": "9",
             "left_only": [2, 6], "common": [1, 3], "right_only": [9],
             "hcf": 3, "caption": "6/9 = 2/3"},
            {"text": "2. Simplify 8/12 using HCF=4",
             "diagram": "venn", "leftname": "8", "rightname": "12",
             "left_only": [2, 8], "common": [1, 2, 4], "right_only": [3, 6, 12],
             "hcf": 4, "caption": "8/12 = 2/3"},
            {"text": "3. Simplify 15/20 using HCF=5",
             "diagram": "venn", "leftname": "15", "rightname": "20",
             "left_only": [3, 15], "common": [1, 5], "right_only": [4, 20],
             "hcf": 5, "caption": "15/20 = 3/4"},
        ],
        "card": card_hcf_lcm,
        "solved": [
            {"q": "Ex: Simplify 15/20.",
             "steps": ["HCF(15,20) = 5", "15\u00f75=3, 20\u00f75=4", "Answer = 3/4"]},
        ],
        "tips": [
            "Find HCF of top and bottom.",
            "Divide both by the HCF.",
            "HCF=1 means already simplest.",
            "Check: no more common factor left.",
        ],
        "try_it": {
            "questions": [
                "1. Simplify 10/15.",
                "2. Simplify 9/12.",
                "3. Simplify 14/21.",
            ],
            "answers": "1) 2/3    2) 3/4    3) 2/3",
        },
    },

    # ---- 9H Mixed ----
    "9H": {
        "title": "Factors & Multiples — Mixed",
        "intro": [
            "Mix factors, multiples, and checks.",
            "Factors: divide exactly, list in pairs.",
            "Multiples: skip-count, list in order.",
            "Check division: remainder 0 means factor.",
            "Bigger numbers may have many factors.",
        ],
        "real_life": [
            {"text": "1. All factors of 42",
             "diagram": "factor_pairs", "n": 42, "pairs": [(1, 42), (2, 21), (3, 14), (6, 7)],
             "caption": "1,2,3,6,7,14,21,42"},
            {"text": "2. First 6 multiples of 9",
             "diagram": "multiples_strip", "base": 9, "count": 6,
             "caption": "9,18,27,36,45,54"},
            {"text": "3. Is 7 a factor of 56? 56\u00f77=8 \u2192 Yes",
             "diagram": "factor_pairs", "n": 56, "pairs": [(7, 8), (4, 14)],
             "caption": "7\u00d78=56"},
        ],
        "card": card_factors,
        "solved": [
            {"q": "Ex: List all factors of 42.",
             "steps": ["Pairs: 1\u00d742, 2\u00d721, 3\u00d714, 6\u00d77",
                       "Answer: 1,2,3,6,7,14,21,42"]},
        ],
        "tips": [
            "List factor pairs systematically.",
            "Skip-count for multiples.",
            "Remainder 0 \u2192 it's a factor.",
            "Double-check with multiplication.",
        ],
        "try_it": {
            "questions": [
                "1. List all factors of 36.",
                "2. First 5 multiples of 11.",
                "3. Is 8 a factor of 64?",
            ],
            "answers": "1) 1,2,3,4,6,9,12,18,36    2) 11,22,33,44,55    3) Yes",
        },
    },

    # ---- 9I Puzzle ----
    "9I": {
        "title": "Factor & Multiple Puzzles",
        "intro": [
            "Use every clue together.",
            "List options for one clue, then filter.",
            "\u2018Multiple of\u2019 and \u2018factor of\u2019 are different.",
            "Narrow down using range clues (between...).",
            "Check your final answer against ALL clues.",
        ],
        "real_life": [
            {"text": "1. Multiple of 4, factor of 24, between 10-20 \u2192 12",
             "diagram": "factor_pairs", "n": 24, "pairs": [(2, 12), (4, 6)],
             "caption": "12 fits all 3 clues"},
            {"text": "2. Multiple of 6, under 30, factor of 60",
             "diagram": "multiples_strip", "base": 6, "count": 4,
             "caption": "6,12,18,24 \u2014 check factor of 60"},
            {"text": "3. Common factor of 24,36, greater than 5",
             "diagram": "venn", "leftname": "24", "rightname": "36",
             "left_only": [8, 24], "common": [1, 2, 3, 4, 6, 12], "right_only": [9, 18, 36],
             "hcf": 12, "caption": "6 or 12 fit"},
        ],
        "card": card_hcf_lcm,
        "solved": [
            {"q": "Ex: I am a multiple of 4, a factor of 24, between 10-20.",
             "steps": ["Multiples of 4: 4,8,12,16,20", "Factors of 24 in that list: 12",
                       "Between 10-20: 12 fits"]},
        ],
        "tips": [
            "List for the strictest clue first.",
            "Cross-check with each other clue.",
            "Range clues narrow it fast.",
            "Re-verify before finalising.",
        ],
        "try_it": {
            "questions": [
                "1. Multiple of 5, factor of 40, between 15-25.",
                "2. Common factor of 18,30, greater than 3.",
                "3. Multiple of 3, under 20, factor of 36.",
            ],
            "answers": "1) 20    2) 6    3) 3,6,9,12,18",
        },
    },

    # ---- 9CUM3 Mixed G+H+I ----
    "9CUM3": {
        "title": "Review: Applications, Mixed, Puzzles",
        "intro": [
            "Simplify with HCF: divide top & bottom.",
            "List factors/multiples to solve mixes.",
            "Puzzles: use every clue, then check.",
            "HCF \u2192 biggest shared; LCM \u2192 smallest shared.",
            "Re-check answers against the question.",
        ],
        "real_life": [
            {"text": "1. Simplify 8/12 using HCF=4",
             "diagram": "venn", "leftname": "8", "rightname": "12",
             "left_only": [2, 8], "common": [1, 2, 4], "right_only": [3, 6, 12],
             "hcf": 4, "caption": "8/12 = 2/3"},
            {"text": "2. All factors of 36",
             "diagram": "factor_pairs", "n": 36, "pairs": [(1, 36), (2, 18), (3, 12), (4, 9), (6, 6)],
             "caption": "1,2,3,4,6,9,12,18,36"},
            {"text": "3. Multiple of 4, factor of 24, between 10-20 \u2192 12",
             "diagram": "multiples_strip", "base": 4, "count": 5,
             "caption": "checking multiples of 4"},
        ],
        "card": card_factors,
        "solved": [
            {"q": "Ex: Simplify 9/12, then list factors of 9.",
             "steps": ["HCF(9,12)=3 \u2192 9/12 = 3/4", "Factors of 9: 1,3,9"]},
        ],
        "tips": [
            "Simplify: divide by HCF.",
            "List systematically, don't guess.",
            "Puzzles: filter by every clue.",
            "Always double-check.",
        ],
        "try_it": {
            "questions": [
                "1. Simplify 12/16.",
                "2. List all factors of 28.",
                "3. Multiple of 6, factor of 48, under 20.",
            ],
            "answers": "1) 3/4    2) 1,2,4,7,14,28    3) 6,12",
        },
    },

    # ---- 9J Mixed challenge ----
    "9J": {
        "title": "Factors/Multiples — Mixed Challenge",
        "intro": [
            "Mix every skill from this level.",
            "Factors: list in pairs, check division.",
            "Multiples: skip-count, list in order.",
            "Use HCF/LCM where the story needs it.",
            "Prime factorise for power-of forms.",
        ],
        "real_life": [
            {"text": "1. All factors of 48",
             "diagram": "factor_pairs", "n": 48, "pairs": [(1, 48), (2, 24), (3, 16), (4, 12), (6, 8)],
             "caption": "1,2,3,4,6,8,12,16,24,48"},
            {"text": "2. First 5 multiples of 8",
             "diagram": "multiples_strip", "base": 8, "count": 5,
             "caption": "8,16,24,32,40"},
            {"text": "3. Is 9 a factor of 72? 72\u00f79=8 \u2192 Yes",
             "diagram": "factor_pairs", "n": 72, "pairs": [(9, 8), (6, 12)],
             "caption": "9\u00d78=72"},
        ],
        "card": card_factor_tree,
        "solved": [
            {"q": "Ex: List all factors of 48, then check if 9 is a factor of 72.",
             "steps": ["Factors of 48: 1,2,3,4,6,8,12,16,24,48",
                       "72\u00f79=8, no remainder \u2192 yes"]},
        ],
        "tips": [
            "List factor pairs in order.",
            "Skip-count for multiples.",
            "Check remainder for factor tests.",
            "Use HCF/LCM where needed.",
        ],
        "try_it": {
            "questions": [
                "1. List all factors of 40.",
                "2. First 5 multiples of 12.",
                "3. Is 8 a factor of 96?",
            ],
            "answers": "1) 1,2,4,5,8,10,20,40    2) 12,24,36,48,60    3) Yes",
        },
    },

    # ---- 9REV Revision ----
    "9REV": {
        "title": "Level 9 Revision — Factors, Multiples, HCF/LCM",
        "intro": [
            "Factor: divides exactly, no remainder.",
            "Multiple: number \u00d7 1,2,3... (infinite).",
            "Prime factorisation: split to primes only.",
            "HCF = biggest shared factor.",
            "LCM = smallest shared multiple.",
        ],
        "real_life": [
            {"text": "1. Factors of 12: 1,2,3,4,6,12",
             "diagram": "factor_pairs", "n": 12, "pairs": [(1, 12), (2, 6), (3, 4)],
             "caption": "factor pairs of 12"},
            {"text": "2. HCF(12,18)=6, LCM(12,18)=36",
             "diagram": "venn", "leftname": "12", "rightname": "18",
             "left_only": [4, 12], "common": [1, 2, 3, 6], "right_only": [9, 18],
             "hcf": 6, "lcm": 36, "caption": "shared and combined"},
            {"text": "3. 12 = 2^2 × 3 (prime factorisation)",
             "diagram": "factor_tree", "root": 12, "splits": [(2, 6, False), (2, 3, True)],
             "caption": "prime factor tree"},
        ],
        "card": card_hcf_lcm,
        "solved": [
            {"q": "Ex: HCF and LCM of 8 and 12.",
             "steps": ["Factors: 8\u21921,2,4,8  12\u21921,2,3,4,6,12", "HCF=4",
                       "Multiples meet at 24 \u2192 LCM=24"]},
        ],
        "tips": [
            "Factor: divides exactly.",
            "Multiple: skip-counts, infinite.",
            "HCF: biggest shared factor.",
            "LCM: smallest shared multiple.",
        ],
        "try_it": {
            "questions": [
                "1. List all factors of 20.",
                "2. HCF(15,20) = ?",
                "3. LCM(6,8) = ?",
            ],
            "answers": "1) 1,2,4,5,10,20    2) 5    3) 24",
        },
    },
}


# ───────────────────────────────────────────────────────────────────────────────
# LEVEL 10 — Ratio & Proportion: concept page specs (sheet 1)
# ───────────────────────────────────────────────────────────────────────────────
_L10 = {
    # ---- 10A Ratio concept ----
    "10A": {
        "title": "Ratio — Concept",
        "intro": [
            "A ratio compares two quantities.",
            "Written as a : b (read \u2018a to b\u2019).",
            "Order matters: 3:5 is not 5:3.",
            "3 red, 5 blue \u2192 ratio of red to blue = 3:5.",
            "Keep the same units on both sides.",
        ],
        "real_life": [
            {"text": "1. 3 red, 5 blue marbles \u2192 3:5",
             "diagram": "ratio_bar", "a": 3, "b": 5, "caption": "red to blue = 3:5"},
            {"text": "2. 2 cats, 7 dogs \u2192 2:7",
             "diagram": "ratio_bar", "a": 2, "b": 7, "caption": "cats to dogs = 2:7"},
            {"text": "3. 6 apples, 4 oranges \u2192 6:4",
             "diagram": "ratio_bar", "a": 6, "b": 4, "caption": "apples to oranges = 6:4"},
        ],
        "card": card_ratio,
        "solved": [
            {"q": "Ex: 5 boys, 3 girls. Ratio of boys to girls?",
             "steps": ["Boys = 5, girls = 3", "Answer = 5:3"]},
        ],
        "tips": [
            "Ratio compares two amounts.",
            "Order matters: a:b \u2260 b:a.",
            "Same units both sides.",
            "Write as a:b, not a fraction.",
        ],
        "try_it": {
            "questions": [
                "1. 4 pens, 6 pencils. Ratio of pens to pencils?",
                "2. 9 boys, 2 girls. Ratio of girls to boys?",
                "3. 7 red, 3 blue. Ratio of red to blue?",
            ],
            "answers": "1) 4:6    2) 2:9    3) 7:3",
        },
    },

    # ---- 10B Simplifying ratios ----
    "10B": {
        "title": "Simplifying Ratios",
        "intro": [
            "Find the HCF of both numbers.",
            "Divide BOTH sides by the HCF.",
            "Result is the simplest form.",
            "4:2 \u2192 HCF=2 \u2192 2:1.",
            "If HCF=1, already simplest.",
        ],
        "real_life": [
            {"text": "1. 4:2 \u2192 HCF=2 \u2192 2:1",
             "diagram": "ratio_bar", "a": 4, "b": 2, "caption": "before simplifying"},
            {"text": "2. 6:3 \u2192 HCF=3 \u2192 2:1",
             "diagram": "ratio_bar", "a": 6, "b": 3, "caption": "before simplifying"},
            {"text": "3. 8:4 \u2192 HCF=4 \u2192 2:1",
             "diagram": "ratio_bar", "a": 8, "b": 4, "caption": "before simplifying"},
        ],
        "card": card_simplify_ratio,
        "solved": [
            {"q": "Ex: Simplify 8:4.",
             "steps": ["HCF(8,4) = 4", "8\u00f74=2, 4\u00f74=1", "Answer = 2:1"]},
        ],
        "tips": [
            "Find HCF of both numbers.",
            "Divide both sides by HCF.",
            "Check: no common factor left.",
            "Order is kept after simplifying.",
        ],
        "try_it": {
            "questions": [
                "1. Simplify 10:5.",
                "2. Simplify 9:6.",
                "3. Simplify 12:8.",
            ],
            "answers": "1) 2:1    2) 3:2    3) 3:2",
        },
    },

    # ---- 10C Equivalent ratios ----
    "10C": {
        "title": "Equivalent Ratios",
        "intro": [
            "Multiply BOTH sides by the same number.",
            "1:3 = 2:6 = 3:9 (all equivalent).",
            "Same proportion, different numbers.",
            "Scaling up or down keeps it equal.",
            "Check: cross products are equal.",
        ],
        "real_life": [
            {"text": "1. 1:3 \u00d72 = 2:6",
             "diagram": "ratio_bar", "a": 2, "b": 6, "caption": "scaled up \u00d72"},
            {"text": "2. 1:3 \u00d73 = 3:9",
             "diagram": "ratio_bar", "a": 3, "b": 9, "caption": "scaled up \u00d73"},
            {"text": "3. 2:5 \u00d72 = 4:10",
             "diagram": "ratio_bar", "a": 4, "b": 10, "caption": "scaled up \u00d72"},
        ],
        "card": card_equivalent_ratio,
        "solved": [
            {"q": "Ex: Find an equivalent ratio to 2:5 (\u00d73).",
             "steps": ["2\u00d73=6, 5\u00d73=15", "Answer = 6:15"]},
        ],
        "tips": [
            "Multiply both sides equally.",
            "Same proportion, new numbers.",
            "Can also divide both sides.",
            "Check with cross multiplication.",
        ],
        "try_it": {
            "questions": [
                "1. 1:4 \u00d72 = ?",
                "2. 3:5 \u00d72 = ?",
                "3. 2:3 \u00d74 = ?",
            ],
            "answers": "1) 2:8    2) 6:10    3) 8:12",
        },
    },

    # ---- 10CUM1 Mixed A+B+C ----
    "10CUM1": {
        "title": "Review: Concept, Simplify, Equivalent",
        "intro": [
            "Ratio compares two quantities, order matters.",
            "Simplify: divide both by HCF.",
            "Equivalent: multiply both by same number.",
            "All equivalent ratios represent the same split.",
            "Always keep units consistent.",
        ],
        "real_life": [
            {"text": "1. 3 red : 5 blue = 3:5",
             "diagram": "ratio_bar", "a": 3, "b": 5, "caption": "basic ratio"},
            {"text": "2. 8:4 simplifies to 2:1",
             "diagram": "ratio_bar", "a": 8, "b": 4, "caption": "before simplifying"},
            {"text": "3. 1:3 = 2:6 (equivalent)",
             "diagram": "ratio_bar", "a": 2, "b": 6, "caption": "scaled \u00d72"},
        ],
        "card": card_equivalent_ratio,
        "solved": [
            {"q": "Ex: Simplify 6:9, then find an equivalent of 1:2.",
             "steps": ["HCF(6,9)=3 \u2192 6:9 = 2:3", "1:2 \u00d74 = 4:8"]},
        ],
        "tips": [
            "Order matters in a ratio.",
            "Simplify with HCF.",
            "Equivalent: scale up/down equally.",
            "Cross products check equivalence.",
        ],
        "try_it": {
            "questions": [
                "1. 5 boys, 2 girls. Ratio?",
                "2. Simplify 14:21.",
                "3. 2:7 \u00d73 = ?",
            ],
            "answers": "1) 5:2    2) 2:3    3) 6:21",
        },
    },

    # ---- 10D Proportion ----
    "10D": {
        "title": "Proportion",
        "intro": [
            "A proportion says two ratios are EQUAL.",
            "a:b = c:d means a\u00d7d = b\u00d7c.",
            "Cross-multiply to check.",
            "If cross products match \u2192 it IS a proportion.",
            "2:3 = 4:6 because 2\u00d76 = 3\u00d74 = 12.",
        ],
        "real_life": [
            {"text": "1. Is 2:3 = 4:6? Cross multiply to check",
             "diagram": "cross_multiply", "a": 2, "b": 3, "c2": 4, "d": 6,
             "caption": "12 = 12 \u2192 yes, proportion"},
            {"text": "2. Is 1:2 = 3:6?",
             "diagram": "cross_multiply", "a": 1, "b": 2, "c2": 3, "d": 6,
             "caption": "6 = 6 \u2192 yes, proportion"},
            {"text": "3. Is 3:4 = 9:12?",
             "diagram": "cross_multiply", "a": 3, "b": 4, "c2": 9, "d": 12,
             "caption": "36 = 36 \u2192 yes, proportion"},
        ],
        "card": card_proportion,
        "solved": [
            {"q": "Ex: Is 2:3 = 4:6 a proportion?",
             "steps": ["2\u00d76=12", "3\u00d74=12", "Equal \u2192 yes, a proportion"]},
        ],
        "tips": [
            "Cross-multiply both sides.",
            "Equal products \u2192 proportion.",
            "Different products \u2192 not a proportion.",
            "Order: a:b = c:d \u2192 a\u00d7d, b\u00d7c.",
        ],
        "try_it": {
            "questions": [
                "1. Is 2:5 = 6:15 a proportion?",
                "2. Is 3:4 = 5:8 a proportion?",
                "3. Is 1:6 = 2:12 a proportion?",
            ],
            "answers": "1) Yes    2) No    3) Yes",
        },
    },

    # ---- 10E Solving proportions ----
    "10E": {
        "title": "Solving Proportions",
        "intro": [
            "Find the value of ONE unit first.",
            "Then multiply for the amount needed.",
            "4 pens cost Rs 12 \u2192 1 pen = Rs 3.",
            "So 6 pens = 6 \u00d7 3 = Rs 18.",
            "This is the \u2018unitary method\u2019.",
        ],
        "real_life": [
            {"text": "1. 4 pens = Rs 12 \u2192 1 pen = Rs 3",
             "diagram": "table", "headers": ["Pens", "Cost"],
             "rows": [["4", "12"], ["1", "3"], ["6", "18"]],
             "caption": "find 1 unit, then scale"},
            {"text": "2. 5 books = Rs 30 \u2192 1 book = Rs 6",
             "diagram": "table", "headers": ["Books", "Cost"],
             "rows": [["5", "30"], ["1", "6"], ["8", "48"]],
             "caption": "unitary method"},
            {"text": "3. 3 kg = Rs 18 \u2192 1 kg = Rs 6",
             "diagram": "table", "headers": ["kg", "Cost"],
             "rows": [["3", "18"], ["1", "6"], ["5", "30"]],
             "caption": "unitary method"},
        ],
        "card": card_direct_inverse,
        "solved": [
            {"q": "Ex: 4 pens cost Rs 12. Find the cost of 6 pens.",
             "steps": ["1 pen = 12\u00f74 = Rs 3", "6 pens = 6\u00d73", "= Rs 18"]},
        ],
        "tips": [
            "Find the value of 1 unit first.",
            "Divide total by quantity.",
            "Multiply for the new quantity.",
            "Keep the units (Rs, kg...).",
        ],
        "try_it": {
            "questions": [
                "1. 3 pens cost Rs 9. Cost of 5 pens?",
                "2. 6 books cost Rs 60. Cost of 4 books?",
                "3. 4 kg costs Rs 100. Cost of 7 kg?",
            ],
            "answers": "1) Rs 15    2) Rs 40    3) Rs 175",
        },
    },

    # ---- 10CUM2 Mixed D+E+F ----
    "10CUM2": {
        "title": "Review: Proportion, Solving, Word Problems",
        "intro": [
            "Proportion: two ratios are equal.",
            "Cross-multiply to check.",
            "Unitary method: find 1 unit, then scale.",
            "Sharing: total parts \u2192 1 part \u2192 each share.",
            "Always check the answer fits the story.",
        ],
        "real_life": [
            {"text": "1. Is 2:3 = 4:6?",
             "diagram": "cross_multiply", "a": 2, "b": 3, "c2": 4, "d": 6,
             "caption": "12 = 12 \u2192 yes"},
            {"text": "2. 4 pens = Rs 12 \u2192 1 pen = Rs 3",
             "diagram": "table", "headers": ["Pens", "Cost"],
             "rows": [["4", "12"], ["1", "3"]], "caption": "unitary method"},
            {"text": "3. Share Rs 30 in 1:2 \u2192 Rs 10 and Rs 20",
             "diagram": "ratio_bar", "a": 1, "b": 2, "caption": "3 parts total"},
        ],
        "card": card_proportion,
        "solved": [
            {"q": "Ex: Share Rs 30 in ratio 1:2.",
             "steps": ["Total parts = 1+2 = 3", "1 part = 30\u00f73 = 10",
                       "Shares: Rs 10 and Rs 20"]},
        ],
        "tips": [
            "Cross-multiply to check proportion.",
            "Unitary method: find 1 unit.",
            "Sharing: add parts, divide total.",
            "Check shares add to the total.",
        ],
        "try_it": {
            "questions": [
                "1. Is 3:5 = 9:15 a proportion?",
                "2. 5 books cost Rs 25. Cost of 8?",
                "3. Share Rs 40 in ratio 3:5.",
            ],
            "answers": "1) Yes    2) Rs 40    3) Rs 15 and Rs 25",
        },
    },

    # ---- 10F Word problems ----
    "10F": {
        "title": "Sharing in a Ratio",
        "intro": [
            "Add the ratio parts for the total parts.",
            "Divide the total amount by total parts.",
            "That gives the value of ONE part.",
            "Multiply each ratio number by that value.",
            "Check: shares add up to the total.",
        ],
        "real_life": [
            {"text": "1. Share Rs 30 in 1:2 \u2192 Rs 10, Rs 20",
             "diagram": "ratio_bar", "a": 1, "b": 2, "caption": "3 parts \u2192 Rs 10 each"},
            {"text": "2. Share Rs 40 in 3:5 \u2192 Rs 15, Rs 25",
             "diagram": "ratio_bar", "a": 3, "b": 5, "caption": "8 parts \u2192 Rs 5 each"},
            {"text": "3. Share Rs 60 in 1:2 \u2192 Rs 20, Rs 40",
             "diagram": "ratio_bar", "a": 1, "b": 2, "caption": "3 parts \u2192 Rs 20 each"},
        ],
        "card": card_ratio,
        "solved": [
            {"q": "Ex: Share Rs 40 in ratio 3:5.",
             "steps": ["Total parts = 3+5 = 8", "1 part = 40\u00f78 = 5",
                       "Shares: 3\u00d75=15, 5\u00d75=25"]},
        ],
        "tips": [
            "Add the ratio numbers for total parts.",
            "Divide total amount by total parts.",
            "Multiply back for each share.",
            "Shares must add to the total.",
        ],
        "try_it": {
            "questions": [
                "1. Share Rs 50 in ratio 2:3.",
                "2. Share Rs 70 in ratio 3:4.",
                "3. Share Rs 90 in ratio 4:5.",
            ],
            "answers": "1) Rs 20, Rs 30    2) Rs 30, Rs 40    3) Rs 40, Rs 50",
        },
    },

    # ---- 10G Direct proportion ----
    "10G": {
        "title": "Direct Proportion",
        "intro": [
            "Both quantities increase together.",
            "y \u00f7 x = k (a constant value).",
            "Find k, then use it for new values.",
            "x=2,y=6 \u2192 k=3. When x=4, y=k\u00d74=12.",
            "More of one means more of the other.",
        ],
        "real_life": [
            {"text": "1. x=2,y=6 (k=3). When x=4, y=12",
             "diagram": "table", "headers": ["x", "y"],
             "rows": [["2", "6"], ["4", "12"]], "caption": "y = 3x"},
            {"text": "2. x=3,y=9 (k=3). When x=5, y=15",
             "diagram": "table", "headers": ["x", "y"],
             "rows": [["3", "9"], ["5", "15"]], "caption": "y = 3x"},
            {"text": "3. x=4,y=12 (k=3). When x=7, y=21",
             "diagram": "table", "headers": ["x", "y"],
             "rows": [["4", "12"], ["7", "21"]], "caption": "y = 3x"},
        ],
        "card": card_direct_inverse,
        "solved": [
            {"q": "Ex: x=2,y=6. Find y when x=4.",
             "steps": ["k = y\u00f7x = 6\u00f72 = 3", "y = k\u00d7x = 3\u00d74", "Answer = 12"]},
        ],
        "tips": [
            "Direct: both rise together.",
            "k = y \u00f7 x (constant).",
            "y = k \u00d7 x for new values.",
            "More x means more y.",
        ],
        "try_it": {
            "questions": [
                "1. x=3,y=12. Find k.",
                "2. Using k from above, find y when x=5.",
                "3. x=2,y=8. Find y when x=6.",
            ],
            "answers": "1) k=4    2) y=20    3) y=24",
        },
    },

    # ---- 10H Inverse proportion ----
    "10H": {
        "title": "Inverse Proportion",
        "intro": [
            "One quantity increases, the other decreases.",
            "x \u00d7 y = k (a constant value).",
            "Find k, then use it for new values.",
            "x=2,y=12 \u2192 k=24. When x=4, y=24\u00f74=6.",
            "More of one means LESS of the other.",
        ],
        "real_life": [
            {"text": "1. x=2,y=12 (k=24). When x=4, y=6",
             "diagram": "table", "headers": ["x", "y"],
             "rows": [["2", "12"], ["4", "6"]], "caption": "x\u00d7y = 24"},
            {"text": "2. x=3,y=8 (k=24). When x=6, y=4",
             "diagram": "table", "headers": ["x", "y"],
             "rows": [["3", "8"], ["6", "4"]], "caption": "x\u00d7y = 24"},
            {"text": "3. x=4,y=6 (k=24). When x=8, y=3",
             "diagram": "table", "headers": ["x", "y"],
             "rows": [["4", "6"], ["8", "3"]], "caption": "x\u00d7y = 24"},
        ],
        "card": card_direct_inverse,
        "solved": [
            {"q": "Ex: x=2,y=12. Find y when x=4.",
             "steps": ["k = x\u00d7y = 2\u00d712 = 24", "y = k\u00f7x = 24\u00f74", "Answer = 6"]},
        ],
        "tips": [
            "Inverse: one up, other down.",
            "k = x \u00d7 y (constant).",
            "y = k \u00f7 x for new values.",
            "More x means LESS y.",
        ],
        "try_it": {
            "questions": [
                "1. x=3,y=10. Find k.",
                "2. Using k from above, find y when x=5.",
                "3. x=4,y=9. Find y when x=6.",
            ],
            "answers": "1) k=30    2) y=6    3) y=6",
        },
    },

    # ---- 10I Mixed ----
    "10I": {
        "title": "Ratio & Proportion — Mixed",
        "intro": [
            "Simplify ratios using HCF.",
            "Share totals using ratio parts.",
            "Check proportions with cross multiply.",
            "Direct: y\u00f7x=k. Inverse: x\u00d7y=k.",
            "Read carefully to pick the right method.",
        ],
        "real_life": [
            {"text": "1. Simplify 15:20 \u2192 HCF=5 \u2192 3:4",
             "diagram": "ratio_bar", "a": 15, "b": 20, "caption": "before simplifying"},
            {"text": "2. Share Rs 60 in 2:3 \u2192 Rs 24, Rs 36",
             "diagram": "ratio_bar", "a": 2, "b": 3, "caption": "5 parts \u2192 Rs 12 each"},
            {"text": "3. Is 4:6 = 6:9?",
             "diagram": "cross_multiply", "a": 4, "b": 6, "c2": 6, "d": 9,
             "caption": "36 = 36 \u2192 yes"},
        ],
        "card": card_proportion,
        "solved": [
            {"q": "Ex: Simplify 15:20, then share Rs 60 in 2:3.",
             "steps": ["15:20 \u2192 3:4 (\u00f75)", "Rs 60 in 2:3 \u2192 Rs 24, Rs 36"]},
        ],
        "tips": [
            "Simplify with HCF.",
            "Share: total parts \u2192 1 part \u2192 scale.",
            "Cross-multiply to check proportion.",
            "Pick direct or inverse carefully.",
        ],
        "try_it": {
            "questions": [
                "1. Simplify 18:24.",
                "2. Share Rs 100 in ratio 2:3.",
                "3. Is 5:8 = 10:16 a proportion?",
            ],
            "answers": "1) 3:4    2) Rs 40, Rs 60    3) Yes",
        },
    },

    # ---- 10CUM3 Mixed G+H+I ----
    "10CUM3": {
        "title": "Review: Direct, Inverse, Mixed",
        "intro": [
            "Direct: y\u00f7x=k, both rise together.",
            "Inverse: x\u00d7y=k, one up other down.",
            "Find k first, then use it for new values.",
            "Simplify and share use HCF and parts.",
            "Always identify which type applies.",
        ],
        "real_life": [
            {"text": "1. Direct: x=2,y=6 \u2192 k=3",
             "diagram": "table", "headers": ["x", "y"],
             "rows": [["2", "6"], ["4", "12"]], "caption": "y = 3x"},
            {"text": "2. Inverse: x=2,y=12 \u2192 k=24",
             "diagram": "table", "headers": ["x", "y"],
             "rows": [["2", "12"], ["4", "6"]], "caption": "x\u00d7y = 24"},
            {"text": "3. Simplify 12:16 \u2192 3:4",
             "diagram": "ratio_bar", "a": 12, "b": 16, "caption": "before simplifying"},
        ],
        "card": card_direct_inverse,
        "solved": [
            {"q": "Ex: x=3,y=9 (direct). Find y when x=6.",
             "steps": ["k = 9\u00f73 = 3", "y = 3\u00d76", "= 18"]},
        ],
        "tips": [
            "Direct: both rise (y\u00f7x=k).",
            "Inverse: one rises, other falls (x\u00d7y=k).",
            "Find k from the given pair first.",
            "Re-check by substituting back.",
        ],
        "try_it": {
            "questions": [
                "1. Direct: x=4,y=20. Find y when x=6.",
                "2. Inverse: x=5,y=8. Find y when x=10.",
                "3. Simplify 16:20.",
            ],
            "answers": "1) y=30    2) y=4    3) 4:5",
        },
    },

    # ---- 10J Mixed challenge ----
    "10J": {
        "title": "Ratio & Proportion — Mixed Challenge",
        "intro": [
            "Mix every skill: simplify, scale, solve.",
            "Find missing values using proportions.",
            "3:5 = ?:25 \u2192 scale factor is 25\u00f75=5.",
            "So missing = 3\u00d75 = 15.",
            "Always check with cross multiplication.",
        ],
        "real_life": [
            {"text": "1. Simplify 8:14 \u2192 4:7",
             "diagram": "ratio_bar", "a": 8, "b": 14, "caption": "before simplifying"},
            {"text": "2. Simplify 36:24 \u2192 3:2",
             "diagram": "ratio_bar", "a": 36, "b": 24, "caption": "before simplifying"},
            {"text": "3. 3:5 = ?:25 \u2192 missing = 15",
             "diagram": "cross_multiply", "a": 3, "b": 5, "c2": 15, "d": 25,
             "caption": "75 = 75 \u2192 missing is 15"},
        ],
        "card": card_proportion,
        "solved": [
            {"q": "Ex: 3:5 = ?:25. Find the missing number.",
             "steps": ["Scale factor: 25\u00f75 = 5", "3\u00d75 = 15", "Answer = 15"]},
        ],
        "tips": [
            "Find the scale factor first.",
            "Apply it to the other side.",
            "Simplify using HCF.",
            "Check with cross multiplication.",
        ],
        "try_it": {
            "questions": [
                "1. Write ratio 10:15 in simplest form.",
                "2. Simplify 42:28.",
                "3. 2:7 = ?:21. Find the missing number.",
            ],
            "answers": "1) 2:3    2) 3:2    3) 6",
        },
    },

    # ---- 10REV Revision ----
    "10REV": {
        "title": "Level 10 Revision — Ratio & Proportion",
        "intro": [
            "Ratio: a:b compares two quantities.",
            "Simplify with HCF; scale for equivalents.",
            "Proportion: cross products are equal.",
            "Direct: y\u00f7x=k. Inverse: x\u00d7y=k.",
            "Sharing: total parts \u2192 1 part \u2192 scale.",
        ],
        "real_life": [
            {"text": "1. 3 red : 5 blue = 3:5",
             "diagram": "ratio_bar", "a": 3, "b": 5, "caption": "basic ratio"},
            {"text": "2. Is 2:3 = 4:6?",
             "diagram": "cross_multiply", "a": 2, "b": 3, "c2": 4, "d": 6,
             "caption": "12 = 12 \u2192 yes"},
            {"text": "3. Direct: x=2,y=6 \u2192 k=3",
             "diagram": "table", "headers": ["x", "y"],
             "rows": [["2", "6"], ["4", "12"]], "caption": "y = 3x"},
        ],
        "card": card_proportion,
        "solved": [
            {"q": "Ex: Simplify 9:6, then share Rs 50 in 2:3.",
             "steps": ["9:6 \u2192 3:2 (\u00f73)", "Rs 50 in 2:3 \u2192 Rs 20, Rs 30"]},
        ],
        "tips": [
            "Order matters in a ratio.",
            "Simplify with HCF.",
            "Cross-multiply to check proportion.",
            "Direct rises together; inverse one falls.",
        ],
        "try_it": {
            "questions": [
                "1. Simplify 20:16.",
                "2. Is 3:4 = 6:8 a proportion?",
                "3. Share Rs 80 in ratio 3:5.",
            ],
            "answers": "1) 5:4    2) Yes    3) Rs 30, Rs 50",
        },
    },
}


# ───────────────────────────────────────────────────────────────────────────────
# LEVEL 11 — Algebra (Expressions): concept page specs (sheet 1)
# ───────────────────────────────────────────────────────────────────────────────
_L11 = {
    # ---- 11A Variables ----
    "11A": {
        "title": "Variables",
        "intro": [
            "A variable is a LETTER for an unknown number.",
            "x, y, n are common variable letters.",
            "If x = 4, the letter x stands for 4.",
            "Variables can take different values.",
            "Think of it as a labelled mystery box.",
        ],
        "real_life": [
            {"text": "1. x = 4: the box holds 4",
             "diagram": "function_machine", "input_val": "x", "operation": "= 4",
             "output_val": "4", "caption": "x stands for 4"},
            {"text": "2. y = 7: the box holds 7",
             "diagram": "function_machine", "input_val": "y", "operation": "= 7",
             "output_val": "7", "caption": "y stands for 7"},
            {"text": "3. n = 10: the box holds 10",
             "diagram": "function_machine", "input_val": "n", "operation": "= 10",
             "output_val": "10", "caption": "n stands for 10"},
        ],
        "card": card_variable,
        "solved": [
            {"q": "Ex: If x = 4, what number does x stand for?",
             "steps": ["x is the variable", "Its value is given as 4", "Answer = 4"]},
        ],
        "tips": [
            "A variable is just a letter.",
            "It stands for an unknown number.",
            "Its value can change or be given.",
            "Any letter can be a variable.",
        ],
        "try_it": {
            "questions": [
                "1. If a = 9, what does a stand for?",
                "2. If m = 12, what is m?",
                "3. If k = 0, what is k?",
            ],
            "answers": "1) 9    2) 12    3) 0",
        },
    },

    # ---- 11B Algebraic expressions ----
    "11B": {
        "title": "Algebraic Expressions",
        "intro": [
            "An expression has NO equals sign.",
            "An equation HAS an equals sign.",
            "x + 3 is an expression.",
            "x + 3 = 7 is an equation.",
            "A term is a part separated by + or -.",
        ],
        "real_life": [
            {"text": "1. x + 3 has no '=' \u2192 expression",
             "diagram": "term_breakdown", "coeff": 1, "var": "x",
             "caption": "1 term shown: x"},
            {"text": "2. 3x + 5 has 2 terms: 3x and 5",
             "diagram": "term_breakdown", "coeff": 3, "var": "x",
             "caption": "coefficient 3, variable x"},
            {"text": "3. x + 3 = 7 HAS '=' \u2192 equation",
             "diagram": "balance_scale", "left_text": "x + 3", "right_text": "7",
             "caption": "balanced \u2192 it's an equation"},
        ],
        "card": card_expression_parts,
        "solved": [
            {"q": "Ex: How many terms are in 3x + 5?",
             "steps": ["Terms are separated by + or -", "3x and 5", "Answer = 2 terms"]},
        ],
        "tips": [
            "No '=' \u2192 expression.",
            "Has '=' \u2192 equation.",
            "Terms split at + or -.",
            "Coefficient is the number in front.",
        ],
        "try_it": {
            "questions": [
                "1. Is '5y - 2' an expression or equation?",
                "2. How many terms in 2x + 3y - 4?",
                "3. What is the coefficient in 7n?",
            ],
            "answers": "1) expression    2) 3 terms    3) 7",
        },
    },

    # ---- 11C Simplifying expressions ----
    "11C": {
        "title": "Simplifying Expressions",
        "intro": [
            "Combine LIKE terms (same letter).",
            "Add or subtract their coefficients.",
            "2x + 3x = (2+3)x = 5x.",
            "Keep the letter the same.",
            "Different letters can't combine.",
        ],
        "real_life": [
            {"text": "1. 2x + 3x = 5x",
             "diagram": "like_terms", "group_a": ["2x", "3x"], "label_a": "combine \u2192 5x",
             "group_b": ["5x"], "label_b": "simplified",
             "caption": "add coefficients: 2+3=5"},
            {"text": "2. 5x + 4x = 9x",
             "diagram": "like_terms", "group_a": ["5x", "4x"], "label_a": "combine \u2192 9x",
             "group_b": ["9x"], "label_b": "simplified",
             "caption": "add coefficients: 5+4=9"},
            {"text": "3. 7n - 2n = 5n",
             "diagram": "like_terms", "group_a": ["7n", "-2n"], "label_a": "combine \u2192 5n",
             "group_b": ["5n"], "label_b": "simplified",
             "caption": "subtract: 7-2=5"},
        ],
        "card": card_like_unlike,
        "solved": [
            {"q": "Ex: Simplify 5x + 4x.",
             "steps": ["Same letter x", "Add coefficients: 5+4=9", "Answer = 9x"]},
        ],
        "tips": [
            "Only combine LIKE terms.",
            "Add/subtract the coefficients.",
            "The letter stays the same.",
            "Unlike terms stay separate.",
        ],
        "try_it": {
            "questions": [
                "1. Simplify 3y + 6y.",
                "2. Simplify 9n - 4n.",
                "3. Simplify 4x + 2x + x.",
            ],
            "answers": "1) 9y    2) 5n    3) 7x",
        },
    },

    # ---- 11CUM1 Mixed A+B+C ----
    "11CUM1": {
        "title": "Review: Variables, Expressions, Simplifying",
        "intro": [
            "Variable: a letter for an unknown number.",
            "Expression: no '='; equation: has '='.",
            "Terms split at + or -.",
            "Simplify by combining like terms.",
            "Add/subtract coefficients, keep the letter.",
        ],
        "real_life": [
            {"text": "1. x = 4 (variable holds a value)",
             "diagram": "function_machine", "input_val": "x", "operation": "= 4",
             "output_val": "4", "caption": "x stands for 4"},
            {"text": "2. 3x + 5 has 2 terms",
             "diagram": "term_breakdown", "coeff": 3, "var": "x",
             "caption": "coefficient 3, variable x"},
            {"text": "3. 2x + 3x = 5x",
             "diagram": "like_terms", "group_a": ["2x", "3x"], "label_a": "combine \u2192 5x",
             "group_b": ["5x"], "label_b": "simplified",
             "caption": "combine like terms"},
        ],
        "card": card_expression_parts,
        "solved": [
            {"q": "Ex: If x=5, how many terms in 3x+5, and simplify 2x+3x?",
             "steps": ["3x+5 has 2 terms", "2x+3x = 5x"]},
        ],
        "tips": [
            "Variable = unknown letter.",
            "Expression has no '='.",
            "Terms split at + or -.",
            "Combine like terms only.",
        ],
        "try_it": {
            "questions": [
                "1. If y=8, what does y stand for?",
                "2. How many terms in 4x+2y-1?",
                "3. Simplify 6x+2x.",
            ],
            "answers": "1) 8    2) 3 terms    3) 8x",
        },
    },

    # ---- 11D Like/unlike terms ----
    "11D": {
        "title": "Like & Unlike Terms",
        "intro": [
            "Like terms have the SAME letter.",
            "3x and 5x are like terms (both x).",
            "3x and 5y are UNLIKE (different letters).",
            "Only like terms can be added/subtracted.",
            "The number in front can differ.",
        ],
        "real_life": [
            {"text": "1. 3x and 5x are like (both x)",
             "diagram": "like_terms", "group_a": ["3x", "5x"], "label_a": "LIKE",
             "group_b": ["3y"], "label_b": "different letter",
             "caption": "same letter = like terms"},
            {"text": "2. 4y and 2y are like (both y)",
             "diagram": "like_terms", "group_a": ["4y", "2y"], "label_a": "LIKE",
             "group_b": ["4x"], "label_b": "different letter",
             "caption": "same letter = like terms"},
            {"text": "3. 3x and 5y are unlike",
             "diagram": "like_terms", "group_a": ["3x"], "label_a": "x-term",
             "group_b": ["5y"], "label_b": "y-term (UNLIKE)",
             "caption": "different letters = unlike"},
        ],
        "card": card_like_unlike,
        "solved": [
            {"q": "Ex: Are 4y and 2y like or unlike?",
             "steps": ["Both have letter y", "Same letter", "Answer: LIKE"]},
        ],
        "tips": [
            "Same letter \u2192 like terms.",
            "Different letter \u2192 unlike.",
            "Coefficients can be different.",
            "Only combine like terms.",
        ],
        "try_it": {
            "questions": [
                "1. Are 7a and 3a like or unlike?",
                "2. Are 5m and 5n like or unlike?",
                "3. Are 2x and 9x like or unlike?",
            ],
            "answers": "1) like    2) unlike    3) like",
        },
    },

    # ---- 11E Substitution ----
    "11E": {
        "title": "Substitution",
        "intro": [
            "Substitution = replace the letter with its value.",
            "x + 4, with x = 3, becomes 3 + 4.",
            "Then work out the sum: 3 + 4 = 7.",
            "Always replace EVERY occurrence of the letter.",
            "Works for any expression.",
        ],
        "real_life": [
            {"text": "1. x=3: x+4 \u2192 3+4 = 7",
             "diagram": "function_machine", "input_val": "x=3", "operation": "+ 4",
             "output_val": "7", "caption": "substitute then add"},
            {"text": "2. x=5: x+2 \u2192 5+2 = 7",
             "diagram": "function_machine", "input_val": "x=5", "operation": "+ 2",
             "output_val": "7", "caption": "substitute then add"},
            {"text": "3. n=7: n-3 \u2192 7-3 = 4",
             "diagram": "function_machine", "input_val": "n=7", "operation": "- 3",
             "output_val": "4", "caption": "substitute then subtract"},
        ],
        "card": card_substitution,
        "solved": [
            {"q": "Ex: If x = 5, find x + 2.",
             "steps": ["Replace x with 5", "5 + 2", "Answer = 7"]},
        ],
        "tips": [
            "Replace the letter with its value.",
            "Keep the operation the same.",
            "Then calculate the answer.",
            "Works for + - \u00d7 \u00f7.",
        ],
        "try_it": {
            "questions": [
                "1. If x=6, find x+5.",
                "2. If n=9, find n-4.",
                "3. If y=2, find y+8.",
            ],
            "answers": "1) 11    2) 5    3) 10",
        },
    },

    # ---- 11F Expression evaluation ----
    "11F": {
        "title": "Evaluating Expressions",
        "intro": [
            "Evaluate = substitute, then calculate.",
            "Multiply BEFORE adding (order of operations).",
            "2x means 2 \u00d7 x.",
            "3x + 1, with x=2: 3\u00d72+1 = 7.",
            "Always follow the correct order.",
        ],
        "real_life": [
            {"text": "1. x+5, x=3 \u2192 8",
             "diagram": "function_machine", "input_val": "x=3", "operation": "+ 5",
             "output_val": "8", "caption": "evaluate the expression"},
            {"text": "2. 2x, x=6 \u2192 12",
             "diagram": "function_machine", "input_val": "x=6", "operation": "\u00d7 2",
             "output_val": "12", "caption": "2x means 2 times x"},
            {"text": "3. 3x+1, x=2 \u2192 7",
             "diagram": "function_machine", "input_val": "x=2", "operation": "\u00d73, +1",
             "output_val": "7", "caption": "multiply first, then add"},
        ],
        "card": card_substitution,
        "solved": [
            {"q": "Ex: Evaluate 3x + 1 when x = 2.",
             "steps": ["3\u00d72 = 6", "6 + 1 = 7", "Answer = 7"]},
        ],
        "tips": [
            "Substitute the value first.",
            "Multiply/divide before add/subtract.",
            "2x = 2 \u00d7 x.",
            "Check your arithmetic.",
        ],
        "try_it": {
            "questions": [
                "1. Evaluate x+7 when x=4.",
                "2. Evaluate 5x when x=3.",
                "3. Evaluate 2x+3 when x=4.",
            ],
            "answers": "1) 11    2) 15    3) 11",
        },
    },

    # ---- 11CUM2 Mixed D+E+F ----
    "11CUM2": {
        "title": "Review: Like Terms, Substitution, Evaluation",
        "intro": [
            "Like terms: same letter, can combine.",
            "Substitution: replace letter with its value.",
            "Evaluation: substitute then calculate.",
            "Multiply before adding.",
            "Always check every step.",
        ],
        "real_life": [
            {"text": "1. 3x and 5x are like terms",
             "diagram": "like_terms", "group_a": ["3x", "5x"], "label_a": "LIKE",
             "group_b": ["3y"], "label_b": "different letter",
             "caption": "same letter = like"},
            {"text": "2. x=3: x+4 \u2192 7",
             "diagram": "function_machine", "input_val": "x=3", "operation": "+ 4",
             "output_val": "7", "caption": "substitute then add"},
            {"text": "3. 3x+1, x=2 \u2192 7",
             "diagram": "function_machine", "input_val": "x=2", "operation": "\u00d73,+1",
             "output_val": "7", "caption": "evaluate"},
        ],
        "card": card_substitution,
        "solved": [
            {"q": "Ex: Are 2x,7x like? Evaluate 2x+1 when x=3.",
             "steps": ["2x,7x: same letter \u2192 like", "2\u00d73+1 = 7"]},
        ],
        "tips": [
            "Same letter \u2192 like terms.",
            "Substitute, then compute.",
            "Multiply before adding.",
            "Re-check each step.",
        ],
        "try_it": {
            "questions": [
                "1. Are 4n,9n like terms?",
                "2. If x=5, find x+6.",
                "3. Evaluate 4x+2 when x=3.",
            ],
            "answers": "1) Yes    2) 11    3) 14",
        },
    },

    # ---- 11G Word problems ----
    "11G": {
        "title": "Writing Expressions from Words",
        "intro": [
            "Translate words into algebra.",
            "\u2018more than\u2019 \u2192 add. \u2018less than\u2019 \u2192 subtract.",
            "\u2018times\u2019 / \u2018of\u2019 \u2192 multiply.",
            "Use a letter for the unknown amount.",
            "Ravi has x sweets, gets 4 more \u2192 x + 4.",
        ],
        "real_life": [
            {"text": "1. Ravi has x sweets, gets 4 more \u2192 x+4",
             "diagram": "term_breakdown", "coeff": 1, "var": "x",
             "caption": "x represents Ravi's sweets"},
            {"text": "2. Meena has y pens, gives away 2 \u2192 y-2",
             "diagram": "function_machine", "input_val": "y", "operation": "- 2",
             "output_val": "y-2", "caption": "subtract for 'gives away'"},
            {"text": "3. A book costs n rupees, 5 books \u2192 5n",
             "diagram": "function_machine", "input_val": "n", "operation": "\u00d7 5",
             "output_val": "5n", "caption": "multiply for 'groups of'"},
        ],
        "card": card_expression_parts,
        "solved": [
            {"q": "Ex: A pen costs p rupees. Cost of 3 pens?",
             "steps": ["3 groups of p", "3 \u00d7 p", "Answer = 3p"]},
        ],
        "tips": [
            "More than \u2192 add.",
            "Less than / gives away \u2192 subtract.",
            "Times / groups of \u2192 multiply.",
            "Pick a letter for the unknown.",
        ],
        "try_it": {
            "questions": [
                "1. x apples, 6 more given. Expression?",
                "2. y toys, 3 given away. Expression?",
                "3. n rupees per book, 4 books. Expression?",
            ],
            "answers": "1) x+6    2) y-3    3) 4n",
        },
    },

    # ---- 11H Mixed expressions ----
    "11H": {
        "title": "Expressions — Mixed",
        "intro": [
            "Mix substitution, evaluation, and writing.",
            "Replace the letter, then calculate.",
            "Translate words carefully.",
            "Combine like terms where needed.",
            "Double-check the operation used.",
        ],
        "real_life": [
            {"text": "1. x=5: x+7 \u2192 12",
             "diagram": "function_machine", "input_val": "x=5", "operation": "+ 7",
             "output_val": "12", "caption": "substitute then add"},
            {"text": "2. n=3: 4n \u2192 12",
             "diagram": "function_machine", "input_val": "n=3", "operation": "\u00d7 4",
             "output_val": "12", "caption": "4n means 4 times n"},
            {"text": "3. '5 more than x' \u2192 x+5",
             "diagram": "term_breakdown", "coeff": 1, "var": "x",
             "caption": "translate words to algebra"},
        ],
        "card": card_substitution,
        "solved": [
            {"q": "Ex: If x=5, find x+7. Write '5 more than x'.",
             "steps": ["x+7 = 5+7 = 12", "'5 more than x' = x+5"]},
        ],
        "tips": [
            "Substitute carefully.",
            "4n means 4\u00d7n.",
            "'More than' \u2192 add after the letter.",
            "Check the final answer.",
        ],
        "try_it": {
            "questions": [
                "1. If x=6, find x+9.",
                "2. If n=4, find 5n.",
                "3. Write '3 less than y'.",
            ],
            "answers": "1) 15    2) 20    3) y-3",
        },
    },

    # ---- 11I Puzzle algebra ----
    "11I": {
        "title": "Solving Simple Equations",
        "intro": [
            "Keep the equation BALANCED.",
            "Do the same thing to both sides.",
            "x + 3 = 7 \u2192 subtract 3 from both sides.",
            "x = 7 - 3 = 4.",
            "Check by substituting back.",
        ],
        "real_life": [
            {"text": "1. x+3=7 \u2192 x=4 (balance both sides)",
             "diagram": "balance_scale", "left_text": "x + 3", "right_text": "7",
             "caption": "subtract 3 from both sides"},
            {"text": "2. x+5=9 \u2192 x=4",
             "diagram": "balance_scale", "left_text": "x + 5", "right_text": "9",
             "caption": "subtract 5 from both sides"},
            {"text": "3. x+2=10 \u2192 x=8",
             "diagram": "balance_scale", "left_text": "x + 2", "right_text": "10",
             "caption": "subtract 2 from both sides"},
        ],
        "card": card_balance,
        "solved": [
            {"q": "Ex: Solve x + 5 = 9.",
             "steps": ["Subtract 5 from both sides", "x = 9 - 5", "Answer: x = 4"]},
        ],
        "tips": [
            "Keep both sides equal.",
            "Same operation on both sides.",
            "Undo + with -, and \u00d7 with \u00f7.",
            "Check by substituting back.",
        ],
        "try_it": {
            "questions": [
                "1. Solve x+4=10.",
                "2. Solve x+6=11.",
                "3. Solve x+1=8.",
            ],
            "answers": "1) x=6    2) x=5    3) x=7",
        },
    },

    # ---- 11CUM3 Mixed G+H+I ----
    "11CUM3": {
        "title": "Review: Word Problems, Mixed, Solving",
        "intro": [
            "Translate words into expressions.",
            "Substitute and evaluate carefully.",
            "Solve equations by balancing both sides.",
            "Undo the operation to find the letter.",
            "Always check your final answer.",
        ],
        "real_life": [
            {"text": "1. x sweets +4 more \u2192 x+4",
             "diagram": "term_breakdown", "coeff": 1, "var": "x",
             "caption": "translate words"},
            {"text": "2. x=5: x+7 \u2192 12",
             "diagram": "function_machine", "input_val": "x=5", "operation": "+ 7",
             "output_val": "12", "caption": "evaluate"},
            {"text": "3. x+3=7 \u2192 x=4",
             "diagram": "balance_scale", "left_text": "x + 3", "right_text": "7",
             "caption": "solve the equation"},
        ],
        "card": card_balance,
        "solved": [
            {"q": "Ex: Write 'y pens minus 2', then solve x+2=10.",
             "steps": ["y pens minus 2 = y-2", "x+2=10 \u2192 x=8"]},
        ],
        "tips": [
            "Translate carefully.",
            "Substitute, then calculate.",
            "Balance both sides to solve.",
            "Check the answer fits.",
        ],
        "try_it": {
            "questions": [
                "1. Write 'n minus 5'.",
                "2. If x=4, find 3x+1.",
                "3. Solve x+7=15.",
            ],
            "answers": "1) n-5    2) 13    3) x=8",
        },
    },

    # ---- 11J Mixed challenge ----
    "11J": {
        "title": "Algebra — Mixed Challenge",
        "intro": [
            "Mix every skill from this level.",
            "Substitute carefully into expressions.",
            "4n means 4 times n.",
            "Translate words to algebra precisely.",
            "Solve simple equations by balancing.",
        ],
        "real_life": [
            {"text": "1. x=7: x+3 \u2192 10",
             "diagram": "function_machine", "input_val": "x=7", "operation": "+ 3",
             "output_val": "10", "caption": "substitute then add"},
            {"text": "2. n=4: 3n \u2192 12",
             "diagram": "function_machine", "input_val": "n=4", "operation": "\u00d7 3",
             "output_val": "12", "caption": "3n means 3 times n"},
            {"text": "3. '5 more than x' \u2192 x+5",
             "diagram": "term_breakdown", "coeff": 1, "var": "x",
             "caption": "translate to algebra"},
        ],
        "card": card_balance,
        "solved": [
            {"q": "Ex: If x=7, find x+3. Write '5 more than x'.",
             "steps": ["x+3 = 7+3 = 10", "'5 more than x' = x+5"]},
        ],
        "tips": [
            "Substitute carefully.",
            "3n = 3 \u00d7 n.",
            "Translate words precisely.",
            "Balance both sides to solve.",
        ],
        "try_it": {
            "questions": [
                "1. If x=8, find x+2.",
                "2. If n=5, find 4n.",
                "3. Solve x+3=12.",
            ],
            "answers": "1) 10    2) 20    3) x=9",
        },
    },

    # ---- 11REV Revision ----
    "11REV": {
        "title": "Level 11 Revision — Algebra (Expressions)",
        "intro": [
            "Variable: a letter for an unknown number.",
            "Expression: no '='; equation: has '='.",
            "Like terms (same letter) can combine.",
            "Substitution: replace letter, then calculate.",
            "Solve equations by balancing both sides.",
        ],
        "real_life": [
            {"text": "1. x = 4 (variable)",
             "diagram": "function_machine", "input_val": "x", "operation": "= 4",
             "output_val": "4", "caption": "x stands for 4"},
            {"text": "2. 2x + 3x = 5x (like terms)",
             "diagram": "like_terms", "group_a": ["2x", "3x"], "label_a": "combine \u2192 5x",
             "group_b": ["5x"], "label_b": "simplified",
             "caption": "combine like terms"},
            {"text": "3. x+3=7 \u2192 x=4 (solve)",
             "diagram": "balance_scale", "left_text": "x + 3", "right_text": "7",
             "caption": "balance to solve"},
        ],
        "card": card_balance,
        "solved": [
            {"q": "Ex: Simplify 4x+2x, then solve x+5=9.",
             "steps": ["4x+2x = 6x", "x+5=9 \u2192 x=4"]},
        ],
        "tips": [
            "Variable = unknown letter.",
            "Combine only like terms.",
            "Substitute then calculate.",
            "Balance both sides to solve.",
        ],
        "try_it": {
            "questions": [
                "1. If n=6, what is n?",
                "2. Simplify 7x-3x.",
                "3. Solve x+4=12.",
            ],
            "answers": "1) 6    2) 4x    3) x=8",
        },
    },
}
