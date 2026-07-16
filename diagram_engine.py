"""
Fear Less Maths — Diagram Engine
Generates PIL diagrams as BytesIO PNG objects.
"""
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# ─── COLORS ────────────────────────────────────────────────────────────────────
C_BG       = "#FFFFFF"
C_BLUE     = "#D6EAF8"
C_BLUE_D   = "#2E86C1"
C_AMBER    = "#FFF3CD"
C_AMBER_D  = "#B7950B"
C_TEAL     = "#D5F5E3"
C_TEAL_D   = "#1E8449"
C_RED      = "#FADBD8"
C_RED_D    = "#CB4335"
C_GRAY     = "#F2F3F4"
C_GRAY_D   = "#7F8C8D"
C_BORDER   = "#2C3E50"
C_TEXT     = "#1C2833"
C_MARK     = "#E74C3C"
C_ACCENT   = "#8E44AD"
C_HOP      = "#E67E22"

def _font(size=14):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except:
        return ImageFont.load_default()

def _font_reg(size=12):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

def _to_bytes(img: Image.Image) -> BytesIO:
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def _blank(w=500, h=200, bg=C_BG):
    img = Image.new("RGB", (w, h), bg)
    return img, ImageDraw.Draw(img)


def mascot_splitter(message: str, **kw) -> BytesIO:
    """Draws 'Splitter' -- a simple round-faced mascot character with a
    basket/container body (representing grouping/sharing things into equal
    parts) next to a speech bubble containing the given message. Used to
    open Type-3 'Groups & Parts' illustrated worksheets (multiplication,
    division, fractions, factors/HCF/LCM, mensuration).

    Built entirely from the same primitives (circles, lines, rectangles,
    text) already used by every other diagram in this file -- no new
    library or external artwork required.
    """
    from textwrap import wrap
    char_w = 130
    lines = wrap(message, width=46)
    line_h = 22
    bubble_h = max(70, len(lines) * line_h + 30)
    w = char_w + 480
    h = max(180, bubble_h + 40)
    img, d = _blank(w, h)

    # --- character: round head + basket body -------------------------------
    cx, cy = 65, h - 70
    # basket body (trapezoid-ish container)
    d.polygon([(cx-38, cy+10), (cx+38, cy+10), (cx+28, cy+55), (cx-28, cy+55)],
              outline=C_BORDER, width=3, fill="#FDEBD0")
    # basket weave lines
    for lx in range(-24, 28, 12):
        d.line([(cx+lx, cy+14), (cx+lx-4, cy+52)], fill=C_BORDER, width=1)
    # a few "items" peeking out of the basket (small circles = grouped objects)
    for ox, oy, col in [(-14, cy-6, C_TEAL_D), (0, cy-12, C_AMBER_D), (14, cy-6, C_RED_D)]:
        d.ellipse([cx+ox-8, oy-8, cx+ox+8, oy+8], outline=C_BORDER, width=2, fill=col)
    # head
    d.ellipse([cx-30, cy-70, cx+30, cy-10], outline=C_BORDER, width=3, fill="#FFF8E7")
    # eyes
    d.ellipse([cx-14, cy-48, cx-6, cy-40], fill=C_BORDER)
    d.ellipse([cx+6, cy-48, cx+14, cy-40], fill=C_BORDER)
    # smile
    d.arc([cx-14, cy-42, cx+14, cy-24], start=20, end=160, fill=C_BORDER, width=3)
    # little arms
    d.line([(cx-30, cy-25), (cx-45, cy-5)], fill=C_BORDER, width=3)
    d.line([(cx+30, cy-25), (cx+45, cy-5)], fill=C_BORDER, width=3)

    # --- speech bubble -------------------------------------------------------
    bx0, by0 = char_w, 15
    bx1, by1 = w - 15, 15 + bubble_h
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=16, outline=C_BORDER, width=3, fill="#FFFFFF")
    # little pointer triangle back toward the character
    d.polygon([(bx0+30, by1-4), (bx0+8, by1+22), (bx0+55, by1-4)],
              outline=C_BORDER, width=3, fill="#FFFFFF")
    d.line([(bx0+31, by1-2), (bx0+54, by1-2)], fill="#FFFFFF", width=5)  # erase seam
    fnt = _font_reg(17)
    ty = by0 + 16
    for ln in lines:
        d.text((bx0 + 20, ty), ln, fill=C_TEXT, font=fnt)
        ty += line_h
    return _to_bytes(img)


def mascot_splitter_intro():
    """Standard opening line used across Type-3 worksheets. Individual
    sheets can call mascot_splitter() directly with custom text instead."""
    return mascot_splitter(
        "Hi, I'm Splitter! I love breaking numbers into equal groups. "
        "If it splits evenly with nothing left over, that's a FACTOR!"
    )


def factor_groups_icon(number=12, group_size=3, **kw) -> BytesIO:
    """Small icon showing `number` dots split into equal groups of
    `group_size` -- used as the BIG IDEA box illustration for factor
    concepts. E.g. 12 dots arranged as 4 groups of 3."""
    n_groups = number // group_size
    w, h = 220, 90
    img, d = _blank(w, h)
    dot_r = 6
    gap_within = 16
    gap_between = 14
    x = 8
    fnt = _font_reg(13)
    for g in range(n_groups):
        gy = 20
        gw = gap_within * (group_size - 1) + dot_r * 2 + 10
        d.rounded_rectangle([x - 5, gy - dot_r - 6, x + gw - 5, gy + dot_r + 6],
                             radius=8, outline=C_TEAL_D, width=2)
        for i in range(group_size):
            cx = x + i * gap_within
            d.ellipse([cx - dot_r, gy - dot_r, cx + dot_r, gy + dot_r],
                      outline=C_BORDER, width=2, fill=C_TEAL)
        x += gw + gap_between
    d.text((8, 55), f"{number} = {n_groups} groups of {group_size}", fill=C_TEXT, font=fnt)
    return _to_bytes(img)




def tenths_grid(shaded=3, total=10, **kw) -> BytesIO:
    """Row of boxes, some shaded = tenths."""
    w, h = 50 * total + 20, 80
    img, d = _blank(w, h)
    for i in range(total):
        x0, y0, x1, y1 = 10 + i*50, 15, 58 + i*50, 65
        fill = C_BLUE if i < shaded else C_GRAY
        d.rectangle([x0, y0, x1, y1], fill=fill, outline=C_BORDER, width=2)
        if i < shaded:
            d.text((x0+18, y0+18), str(i+1), fill=C_TEXT, font=_font(14))
    d.text((10, 68), f"Shaded: {shaded} out of {total}", fill=C_GRAY_D, font=_font_reg(11))
    return _to_bytes(img)


def hundredths_grid(shaded=25, **kw) -> BytesIO:
    """10×10 grid with some squares shaded = hundredths."""
    cell = 22
    w, h = 10 * cell + 20, 10 * cell + 30
    img, d = _blank(w, h)
    for row in range(10):
        for col in range(10):
            idx = row * 10 + col
            x0 = 10 + col * cell
            y0 = 5 + row * cell
            fill = C_BLUE if idx < shaded else C_GRAY
            d.rectangle([x0, y0, x0+cell, y0+cell], fill=fill, outline=C_BORDER, width=1)
    d.text((10, h - 22), f"Shaded: {shaded}/100 = {shaded/100:.2f}", fill=C_TEXT, font=_font_reg(11))
    return _to_bytes(img)


def number_line(start=0, end=10, divisions=10, mark=None, marks=None,
                hide_mark=False, hop_from=None, hop_by=None, **kw) -> BytesIO:
    """Generic number line with optional marks and hops."""
    w, h = 520, 100
    img, d = _blank(w, h)
    pad = 40
    line_y = 55
    total = end - start
    scale = (w - 2 * pad) / total

    # Main line
    d.line([(pad, line_y), (w - pad, line_y)], fill=C_BORDER, width=3)

    # Tick marks and labels
    step = total / divisions
    for i in range(divisions + 1):
        val = start + i * step
        x = int(pad + (val - start) * scale)
        d.line([(x, line_y - 8), (x, line_y + 8)], fill=C_BORDER, width=2)
        lbl = str(int(val)) if val == int(val) else f"{val:.1f}"
        d.text((x - 10, line_y + 12), lbl, fill=C_TEXT, font=_font_reg(11))

    # Arrow heads
    d.polygon([(w-pad, line_y), (w-pad-10, line_y-5), (w-pad-10, line_y+5)], fill=C_BORDER)

    # Hop arrow
    if hop_from is not None and hop_by is not None:
        x1 = int(pad + (hop_from - start) * scale)
        hop_to = hop_from + hop_by
        x2 = int(pad + (hop_to - start) * scale)
        mid_x = (x1 + x2) // 2
        arc_y = line_y - 30
        d.line([(x1, line_y-8), (x1, line_y-8)], fill=C_HOP, width=2)
        d.arc([min(x1,x2), arc_y, max(x1,x2), line_y-8], 0, 180, fill=C_HOP, width=2)
        d.ellipse([x1-5, line_y-13, x1+5, line_y-3], fill=C_HOP)
        d.text((mid_x - 10, arc_y - 16), f"+{hop_by}" if hop_by > 0 else str(hop_by),
               fill=C_HOP, font=_font(12))

    # Single mark
    if mark is not None and not hide_mark:
        x = int(pad + (mark - start) * scale)
        d.ellipse([x-7, line_y-7, x+7, line_y+7], fill=C_MARK)
        d.text((x-8, line_y-25), str(mark), fill=C_MARK, font=_font(13))
    elif mark is not None and hide_mark:
        x = int(pad + (mark - start) * scale)
        d.polygon([(x, line_y-12), (x-6, line_y-24), (x+6, line_y-24)], fill=C_MARK)
        d.text((x-6, line_y-38), "?", fill=C_MARK, font=_font(14))

    # Multiple marks
    if marks:
        for m in marks:
            x = int(pad + (m - start) * scale)
            d.ellipse([x-6, line_y-6, x+6, line_y+6], fill=C_ACCENT)
            d.text((x-8, line_y-24), str(m), fill=C_ACCENT, font=_font(12))

    return _to_bytes(img)


def integer_line(start=-6, end=6, marks=None, hop_from=None, hop_by=None, **kw) -> BytesIO:
    """Integer number line with negative numbers."""
    w, h = 520, 100
    img, d = _blank(w, h)
    pad = 40
    line_y = 55
    total = end - start
    scale = (w - 2 * pad) / total

    d.line([(pad, line_y), (w-pad, line_y)], fill=C_BORDER, width=3)
    d.polygon([(w-pad, line_y), (w-pad-10, line_y-5), (w-pad-10, line_y+5)], fill=C_BORDER)
    d.polygon([(pad, line_y), (pad+10, line_y-5), (pad+10, line_y+5)], fill=C_BORDER)

    for i in range(total + 1):
        val = start + i
        x = int(pad + i * scale)
        d.line([(x, line_y-8), (x, line_y+8)], fill=C_BORDER, width=2)
        label = str(val) if val != 0 else "0"
        d.text((x - 6, line_y + 12), label, fill=C_TEXT, font=_font_reg(10))
        if val == 0:
            d.line([(x, line_y-15), (x, line_y+15)], fill=C_BORDER, width=3)

    if marks:
        colors = [C_MARK, C_ACCENT, C_HOP, C_TEAL_D]
        for idx, m in enumerate(marks):
            x = int(pad + (m - start) * scale)
            fill = colors[idx % len(colors)]
            d.ellipse([x-7, line_y-7, x+7, line_y+7], fill=fill)
            d.text((x-8, line_y-26), str(m), fill=fill, font=_font(12))

    if hop_from is not None and hop_by is not None:
        x1 = int(pad + (hop_from - start) * scale)
        hop_to = hop_from + hop_by
        x2 = int(pad + (hop_to - start) * scale)
        arc_y = line_y - 28
        d.arc([min(x1,x2), arc_y, max(x1,x2), line_y-8], 0, 180, fill=C_HOP, width=3)
        d.ellipse([x1-6, line_y-14, x1+6, line_y-2], fill=C_BLUE_D)
        d.ellipse([x2-6, line_y-14, x2+6, line_y-2], fill=C_MARK)
        mid_x = (x1 + x2) // 2
        label = f"+{hop_by}" if hop_by >= 0 else str(hop_by)
        d.text((mid_x-12, arc_y-18), label, fill=C_HOP, font=_font(13))

    return _to_bytes(img)


def place_value_chart(number="3.47", **kw) -> BytesIO:
    """Place value chart showing ones, tenths, hundredths, thousandths."""
    cols = ["Thousands", "Hundreds", "Tens", "Ones", ".", "Tenths", "Hundredths", "Thousandths"]
    w, h = 580, 90
    img, d = _blank(w, h)
    col_w = w // len(cols)

    # Parse number
    digits = {}
    parts = number.replace("-", "").split(".")
    whole = parts[0].zfill(4)
    decimal = (parts[1] if len(parts) > 1 else "").ljust(3, "0")
    digit_map = {
        "Thousands": whole[0], "Hundreds": whole[1], "Tens": whole[2], "Ones": whole[3],
        ".": ".", "Tenths": decimal[0], "Hundredths": decimal[1], "Thousandths": decimal[2]
    }

    for i, col in enumerate(cols):
        x0 = i * col_w
        if col == ".":
            d.rectangle([x0, 5, x0+col_w, h-5], fill="#FDFEFE", outline=C_BORDER)
            d.text((x0+5, 10), ".", fill=C_TEXT, font=_font(22))
            continue
        fill = C_AMBER if col in ["Tenths", "Hundredths", "Thousandths"] else C_BLUE
        d.rectangle([x0, 5, x0+col_w, 42], fill=fill, outline=C_BORDER)
        d.rectangle([x0, 42, x0+col_w, h-5], fill=C_GRAY, outline=C_BORDER)
        d.text((x0+2, 8), col[:5], fill=C_TEXT, font=_font_reg(9))
        val = digit_map.get(col, "0")
        if val != "0" or col == "Ones":
            d.text((x0 + col_w//2 - 5, 48), val, fill=C_BORDER, font=_font(18))

    return _to_bytes(img)


def fraction_bar(total=4, shaded=1, **kw) -> BytesIO:
    """Fraction bar with shaded parts."""
    cell_w = min(70, 400 // total)
    w = cell_w * total + 20
    h = 80
    img, d = _blank(w, h)
    for i in range(total):
        x0 = 10 + i * cell_w
        fill = C_TEAL if i < shaded else C_GRAY
        d.rectangle([x0, 15, x0+cell_w, 65], fill=fill, outline=C_BORDER, width=2)
    d.text((12, 68), f"{shaded}/{total}", fill=C_TEXT, font=_font(14))
    return _to_bytes(img)


def fraction_circle(total=4, shaded=1, **kw) -> BytesIO:
    """Circle divided into equal parts, some shaded."""
    from math import pi, cos, sin
    w, h = 160, 160
    img, d = _blank(w, h)
    cx, cy, r = 80, 80, 65
    angle_per = 360 / total
    for i in range(total):
        start_angle = -90 + i * angle_per
        end_angle = start_angle + angle_per
        fill = C_TEAL if i < shaded else C_GRAY
        d.pieslice([cx-r, cy-r, cx+r, cy+r], start_angle, end_angle,
                   fill=fill, outline=C_BORDER, width=2)
    d.text((5, 140), f"Fraction = {shaded}/{total}", fill=C_TEXT, font=_font_reg(11))
    return _to_bytes(img)


def dot_array(rows=2, cols=4, **kw) -> BytesIO:
    """Array of dots for counting."""
    size = 24
    pad = 12
    w = cols * (size + pad) + pad
    h = rows * (size + pad) + pad + 20
    img, d = _blank(w, h)
    for r in range(rows):
        for c in range(cols):
            x = pad + c * (size + pad) + size//2
            y = pad + r * (size + pad) + size//2
            d.ellipse([x-size//2, y-size//2, x+size//2, y+size//2],
                      fill=C_BLUE_D, outline=C_BORDER)
    total = rows * cols
    d.text((10, h-18), f"Total dots = {total}", fill=C_TEXT, font=_font_reg(11))
    return _to_bytes(img)


def ten_frames(count=23, **kw) -> BytesIO:
    """Ten frames for counting. Each frame = 10 dots."""
    frames = (count // 10) + (1 if count % 10 else 0)
    cell, pad, gap = 22, 6, 8
    w = frames * (10 * cell // 2 + 2 * pad + gap) + 20
    h = 90
    img, d = _blank(w, h)
    filled = count
    x_off = 10
    for f in range(frames):
        for row in range(2):
            for col in range(5):
                idx = f * 10 + row * 5 + col
                x0 = x_off + col * cell
                y0 = pad + row * cell
                fill = C_BLUE_D if idx < filled else C_GRAY
                d.ellipse([x0+1, y0+1, x0+cell-1, y0+cell-1], fill=fill, outline=C_BORDER, width=1)
        x_off += 5 * cell + gap
    d.text((10, h-18), f"Count = {count}", fill=C_TEXT, font=_font_reg(11))
    return _to_bytes(img)


def array_diagram(rows=2, cols=3, **kw) -> BytesIO:
    """Multiplication array of dots."""
    size = 26
    pad = 10
    w = cols * (size + pad) + pad
    h = rows * (size + pad) + pad + 25
    img, d = _blank(w, h)
    for r in range(rows):
        for c in range(cols):
            x = pad + c * (size + pad) + size//2
            y = pad + r * (size + pad) + size//2
            d.ellipse([x-size//2, y-size//2, x+size//2, y+size//2],
                      fill=C_TEAL, outline=C_TEAL_D, width=2)
    d.text((10, h-20), f"{rows} × {cols} = {rows*cols}", fill=C_TEXT, font=_font(13))
    return _to_bytes(img)


def dot_addition(a=3, b=2, **kw) -> BytesIO:
    """Two groups of dots showing addition."""
    size = 22
    pad = 10
    total = a + b
    w = total * (size + pad) + 80
    h = 70
    img, d = _blank(w, h)
    for i in range(a):
        x = pad + i * (size + pad) + size//2
        d.ellipse([x-size//2, 15, x+size//2, 15+size], fill=C_BLUE, outline=C_BLUE_D, width=2)
    plus_x = pad + a * (size + pad) + 5
    d.text((plus_x, 18), "+", fill=C_TEXT, font=_font(22))
    for i in range(b):
        x = plus_x + 25 + i * (size + pad) + size//2
        d.ellipse([x-size//2, 15, x+size//2, 15+size], fill=C_AMBER, outline=C_AMBER_D, width=2)
    d.text((10, h-18), f"{a} + {b} = {a+b}", fill=C_TEXT, font=_font(14))
    return _to_bytes(img)


def labeled_rectangle(width=6, height=4, show_grid=False, **kw) -> BytesIO:
    """Labeled rectangle with optional grid for area."""
    scale = 40
    pad = 50
    w = width * scale + 2 * pad
    h = height * scale + 2 * pad
    img, d = _blank(max(w, 200), max(h, 150))
    x0, y0 = pad, pad
    x1, y1 = pad + width*scale, pad + height*scale

    if show_grid:
        for i in range(width+1):
            d.line([(x0+i*scale, y0), (x0+i*scale, y1)], fill="#BFC9CA", width=1)
        for j in range(height+1):
            d.line([(x0, y0+j*scale), (x1, y0+j*scale)], fill="#BFC9CA", width=1)

    d.rectangle([x0, y0, x1, y1], fill=C_BLUE, outline=C_BORDER, width=2)

    # Labels
    d.text(((x0+x1)//2 - 10, y0 - 22), f"{width} cm", fill=C_TEXT, font=_font(13))
    d.text((x1 + 6, (y0+y1)//2 - 8), f"{height} cm", fill=C_TEXT, font=_font(13))
    if show_grid:
        area = width * height
        d.text(((x0+x1)//2 - 20, (y0+y1)//2 - 8), f"A={area}cm²", fill=C_BORDER, font=_font(12))

    return _to_bytes(img)


def labeled_square(side=5, show_grid=False, **kw) -> BytesIO:
    return labeled_rectangle(side, side, show_grid)


def labeled_triangle(a=5, b=7, c=6, **kw) -> BytesIO:
    """Simple triangle with labeled sides."""
    w, h = 300, 200
    img, d = _blank(w, h)
    pts = [(150, 20), (20, 170), (280, 170)]
    d.polygon(pts, fill=C_TEAL, outline=C_BORDER)
    d.line([pts[0], pts[1]], fill=C_BORDER, width=2)
    d.line([pts[0], pts[2]], fill=C_BORDER, width=2)
    d.line([pts[1], pts[2]], fill=C_BORDER, width=2)
    # Labels
    d.text((60, 90), f"{a} cm", fill=C_TEXT, font=_font(13))
    d.text((200, 90), f"{b} cm", fill=C_TEXT, font=_font(13))
    d.text((130, 175), f"{c} cm", fill=C_TEXT, font=_font(13))
    d.text((110, 5), f"Perimeter = {a}+{b}+{c} = {a+b+c} cm", fill=C_GRAY_D, font=_font_reg(11))
    return _to_bytes(img)


def _draw_object(d, x, y, r, kind):
    """Draw one kid-friendly object icon centered at (x,y) with radius r."""
    if kind == "balloon":
        d.ellipse([x-r, y-r, x+r, y+r*1.15], fill=C_BLUE_D, outline=C_BORDER, width=2)
        d.line([x, y+r*1.15, x, y+r*1.15+10], fill=C_GRAY_D, width=1)
    elif kind == "star":
        import math
        pts = []
        for i in range(10):
            ang = math.pi/2 + i*math.pi/5
            rad = r if i % 2 == 0 else r*0.45
            pts.append((x+rad*math.cos(ang), y-rad*math.sin(ang)))
        d.polygon(pts, fill=C_AMBER_D, outline=C_BORDER)
    elif kind == "flower":
        petal_r = r*0.55
        import math
        for i in range(5):
            ang = i*(2*math.pi/5)
            px, py = x+petal_r*math.cos(ang), y+petal_r*math.sin(ang)
            d.ellipse([px-petal_r, py-petal_r, px+petal_r, py+petal_r],
                      fill="#F1948A", outline=C_BORDER)
        d.ellipse([x-r*0.4, y-r*0.4, x+r*0.4, y+r*0.4], fill=C_AMBER_D, outline=C_BORDER)
    elif kind == "leaf":
        d.ellipse([x-r*0.6, y-r, x+r*0.6, y+r], fill=C_TEAL_D, outline=C_BORDER)
    else:  # "apple" default — circle with stem + leaf dot
        d.ellipse([x-r, y-r, x+r, y+r], fill=C_RED_D, outline=C_BORDER, width=2)
        d.line([x, y-r, x, y-r-8], fill="#6E4A2E", width=2)
        d.ellipse([x+2, y-r-9, x+7, y-r-4], fill=C_TEAL_D)


def object_group(count=5, kind="apple", group_size=5, show_icon=True, icon_label="count", **kw) -> BytesIO:
    """Concrete/Pictorial counting diagram: real-world objects in rows,
    grouped by `group_size` (default 5) with a visible gap between groups
    to support subitizing. Used for Pre-Level / CPA 'Intro' and 'Concept' sheets.
    No answer text is ever rendered on the image. A mascot+flag is drawn
    above by default (set show_icon=False to omit). icon_label lets
    other levels reuse this same grouping layout with a different
    mascot keyword (e.g. 'divide' for division-as-sharing) without
    affecting any existing caller, which all still default to 'count'."""
    r = 16
    cell = r*2 + 14
    gap = 22
    cols = group_size
    rows = (count + group_size - 1) // group_size
    w = cols * cell + gap
    icon_h = 70 if show_icon else 0
    h = rows * cell + 20 + icon_h
    img, d = _blank(w, h)
    if show_icon:
        _draw_mini_mascot_flag(d, w/2 - 14, 26, 22, icon_label)
    for row in range(rows):
        in_row = min(group_size, count - row*group_size)
        for c in range(in_row):
            x = 10 + r + c * cell
            y = 10 + r + row * cell + icon_h
            _draw_object(d, x, y, r, kind)
    return _to_bytes(img)


def object_compare(left_count=4, right_count=6, kind="apple", **kw) -> BytesIO:
    """Two object groups side-by-side for visual greater/smaller comparison
    (no symbols, no numbers shown)."""
    r = 14
    cell = r*2 + 10
    cols_each = 5
    rows_l = (left_count + cols_each - 1)//cols_each
    rows_r = (right_count + cols_each - 1)//cols_each
    rows = max(rows_l, rows_r)
    half_w = cols_each*cell + 10
    w = half_w*2 + 30
    h = rows*cell + 20
    img, d = _blank(w, h)
    d.line([half_w+15, 5, half_w+15, h-5], fill=C_GRAY_D, width=2)
    for i in range(left_count):
        row, col = divmod(i, cols_each)
        _draw_object(d, 10+r+col*cell, 10+r+row*cell, r, kind)
    for i in range(right_count):
        row, col = divmod(i, cols_each)
        _draw_object(d, half_w+30+r+col*cell, 10+r+row*cell, r, kind)
    return _to_bytes(img)


def base10_blocks(tens=3, ones=4, **kw) -> BytesIO:
    """Singapore-style base-10 blocks: tall rods = tens, small squares = ones.
    Black-and-white outline-only (shape distinguishes tens/ones, not color),
    with a VALUE mascot+flag, a short 'Find the total value' caption, AND
    small TENS/ONES text labels under each group."""
    rod_w, rod_h = 32, 150
    unit = 32
    gap = 12
    cols_per_row_tens = 5
    rows_tens = (tens + cols_per_row_tens - 1) // cols_per_row_tens if tens else 0
    cols_per_row_ones = 5
    rows_ones = (ones + cols_per_row_ones - 1) // cols_per_row_ones if ones else 0
    icon_h = 70
    label_h = 20
    w = max(cols_per_row_tens * (rod_w + gap), cols_per_row_ones * (unit + gap)) * 2 + 50
    h = max(rows_tens * (rod_h + gap), rows_ones * (unit + gap)) + 20 + icon_h + label_h
    img, d = _blank(w, h)
    _draw_mini_mascot_flag(d, w/2 - 14, 26, 22, "value")
    top = icon_h

    tens_block_w = cols_per_row_tens * (rod_w + gap)
    # Draw tens rods on the left half (outline only, tall shape = tens)
    for i in range(tens):
        row, col = divmod(i, cols_per_row_tens)
        x = 15 + col * (rod_w + gap)
        y = 15 + row * (rod_h + gap) + top
        d.rectangle([x, y, x + rod_w, y + rod_h], outline=C_BORDER, width=3)
        for seg in range(1, 10):
            sy = y + seg * (rod_h / 10)
            d.line([x, sy, x + rod_w, sy], fill=C_BORDER, width=1)
    tens_bottom = 15 + max(rows_tens, 1) * (rod_h + gap) + top
    fnt = _font_reg(14)
    tw = d.textlength("TENS", font=fnt)
    d.text((15 + tens_block_w/2 - tw/2, tens_bottom + 2), "TENS", fill=C_BORDER, font=fnt)
    # Draw ones units on the right half (outline only, small shape = ones)
    ones_x_off = w // 2 + 15
    for i in range(ones):
        row, col = divmod(i, cols_per_row_ones)
        x = ones_x_off + col * (unit + gap)
        y = 15 + row * (unit + gap) + top
        d.rectangle([x, y, x + unit, y + unit], outline=C_BORDER, width=3)
    ones_block_w = cols_per_row_ones * (unit + gap)
    tw2 = d.textlength("ONES", font=fnt)
    d.text((ones_x_off + ones_block_w/2 - tw2/2, tens_bottom + 2), "ONES", fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def _draw_big_symbol(d, x, y, size, symbol):
    """Draw a big +, -, or = symbol centered at (x,y)."""
    t = size * 0.18
    if symbol == "+":
        d.rectangle([x - t/2, y - size/2, x + t/2, y + size/2], fill=C_BORDER)
        d.rectangle([x - size/2, y - t/2, x + size/2, y + t/2], fill=C_BORDER)
    elif symbol == "-":
        d.rectangle([x - size/2, y - t/2, x + size/2, y + t/2], fill=C_BORDER)
    elif symbol == "=":
        gap = size * 0.22
        d.rectangle([x - size/2, y - gap - t/2, x + size/2, y - gap + t/2], fill=C_BORDER)
        d.rectangle([x - size/2, y + gap - t/2, x + size/2, y + gap + t/2], fill=C_BORDER)


def _draw_mini_mascot_flag(d, cx, top_y, r, op_or_label):
    """Compact OUTLINE-ONLY (ink-saving) mascot holding a flag-on-a-stick.
    Accepts either a known op key ('+','-','>','<','=') which is mapped to
    its keyword via _OP_LABELS, or any literal label string directly."""
    label = _OP_LABELS.get(op_or_label, op_or_label)
    cy = top_y + r

    # Stick (thin line up from the mascot's head)
    stick_top = top_y - 22
    d.line([cx + r*0.6, cy - r*0.7, cx + r*0.6, stick_top], fill=C_BORDER, width=2)

    # Flag (outline only, no fill) with small label
    fnt = _font(10)
    tw = d.textlength(label, font=fnt) if label else 14
    flag_w, flag_h = tw + 10, 18
    fx0, fy0 = cx + r*0.6, stick_top
    fx1, fy1 = fx0 + flag_w, fy0 + flag_h
    d.polygon([(fx0, fy0), (fx1, fy0+flag_h*0.2), (fx1, fy1), (fx0, fy1-flag_h*0.2)],
              outline=C_BORDER, width=2)
    d.text((fx0 + 5, fy0 + 2), label, fill=C_BORDER, font=fnt)

    # Body (outline circle, no fill)
    d.ellipse([cx-r, cy-r*0.95, cx+r, cy+r*1.05], outline=C_BORDER, width=2)

    # Eyes (outline circles + tiny filled pupil -- negligible ink)
    eye_w, eye_h = r*0.26, r*0.32
    for dx in (-r*0.32, r*0.32):
        ex, ey = cx+dx, cy-r*0.15
        d.ellipse([ex-eye_w, ey-eye_h, ex+eye_w, ey+eye_h], outline=C_BORDER, width=1)
        pr = eye_w*0.4
        d.ellipse([ex-pr, ey-pr+1, ex+pr, ey+pr+1], fill=C_BORDER)

    # Smile (outline arc)
    d.arc([cx-r*0.32, cy+r*0.05, cx+r*0.32, cy+r*0.5], 20, 160, fill=C_BORDER, width=2)
    return fy1 - top_y + (cy + r*1.05 - top_y)  # total height used


def visual_equation(left=3, right=2, kind="apple", op="+", **kw) -> BytesIO:
    """Fully self-contained visual equation with NO text required to solve:
    (mascot+flag above, centered)
    [objects] [+ or -] [objects] [=] [blank box]
    Both addition AND subtraction show TWO separate object groups (same
    layout) -- subtraction no longer crosses out objects within one group,
    it shows a second group being taken away, exactly mirroring addition."""
    big = max(left, right) > 20
    r = 7 if big else 14
    cell = r*2 + (4 if big else 8)
    cols = 10 if big else 5
    sym_w = 50
    box_w, box_h = 60, 60
    mascot_r = 22
    mascot_area_h = 70

    def group_dims(n):
        rows = (n + cols - 1) // cols if n else 1
        return cols*cell, rows*cell

    gw1, gh1 = group_dims(left)
    gw2, gh2 = group_dims(right)

    row_h = max(gh1, gh2, box_h)
    h = mascot_area_h + row_h + 30
    w = max(gw1 + sym_w + gw2 + sym_w + box_w + 30, 160)
    img, d = _blank(w, h)
    cy = mascot_area_h + row_h/2 + 8

    _draw_mini_mascot_flag(d, w/2 - 14, 26, mascot_r, op)

    x = 15
    # First group
    for i in range(left):
        row, col = divmod(i, cols)
        cx_obj, cy_obj = x + r + col*cell, (mascot_area_h+8) + r + row*cell
        _draw_object(d, cx_obj, cy_obj, r, kind)
    x += gw1 + 10

    # Operator symbol
    _draw_big_symbol(d, x + sym_w/2, cy, 22, "+" if op == "+" else "-")
    x += sym_w

    # Second group (always shown as a separate group, for BOTH + and -)
    for i in range(right):
        row, col = divmod(i, cols)
        cx_obj, cy_obj = x + r + col*cell, (mascot_area_h+8) + r + row*cell
        _draw_object(d, cx_obj, cy_obj, r, kind)
    x += gw2 + 10

    # Equals symbol
    _draw_big_symbol(d, x + sym_w/2, cy, 26, "=")
    x += sym_w

    # Answer box
    d.rectangle([x, cy - box_h/2, x + box_w, cy + box_h/2], outline=C_BORDER, width=3)

    return _to_bytes(img)


def compare_choice(left_count=4, right_count=6, kind="apple", **kw) -> BytesIO:
    """Two object groups side by side PLUS three tick-boxes (>, <, =) at the
    bottom for the child to mark — fully wordless comparison question."""
    r = 13
    cell = r*2 + 8
    cols_each = 5
    rows_l = (left_count + cols_each - 1)//cols_each
    rows_r = (right_count + cols_each - 1)//cols_each
    rows = max(rows_l, rows_r, 1)
    half_w = cols_each*cell + 10
    w = half_w*2 + 30
    icon_h = 70
    h = rows*cell + 70 + icon_h
    img, d = _blank(w, h)
    _draw_mini_mascot_flag(d, w/2 - 14, 26, 22, "compare")
    d.line([half_w+15, 5+icon_h, half_w+15, rows*cell+15+icon_h], fill=C_GRAY_D, width=2)
    for i in range(left_count):
        row, col = divmod(i, cols_each)
        _draw_object(d, 10+r+col*cell, 10+r+row*cell+icon_h, r, kind)
    for i in range(right_count):
        row, col = divmod(i, cols_each)
        _draw_object(d, half_w+30+r+col*cell, 10+r+row*cell+icon_h, r, kind)
    # Tick boxes for >, <, = drawn as actual symbols (no words)
    box_y = rows*cell + 25 + icon_h
    box_size = 30
    gap = 20
    start_x = (w - (box_size*3 + gap*2)) / 2
    symbols = [">", "<", "="]
    for i, sym in enumerate(symbols):
        bx = start_x + i*(box_size+gap)
        d.rectangle([bx, box_y, bx+box_size, box_y+box_size], outline=C_BORDER, width=2)
        cx, cy_s = bx+box_size/2, box_y+box_size/2
        if sym == "=":
            d.line([cx-8, cy_s-5, cx+8, cy_s-5], fill=C_BORDER, width=3)
            d.line([cx-8, cy_s+5, cx+8, cy_s+5], fill=C_BORDER, width=3)
        elif sym == ">":
            d.line([cx-7, cy_s-8, cx+7, cy_s], fill=C_BORDER, width=3)
            d.line([cx-7, cy_s+8, cx+7, cy_s], fill=C_BORDER, width=3)
        else:
            d.line([cx+7, cy_s-8, cx-7, cy_s], fill=C_BORDER, width=3)
            d.line([cx+7, cy_s+8, cx-7, cy_s], fill=C_BORDER, width=3)
    return _to_bytes(img)


def number_card(n=4, **kw) -> BytesIO:
    """Big numeral on the left + an empty box on the right for the child to
    draw that many objects. No words anywhere on the image."""
    w, h = 220, 90
    img, d = _blank(w, h)
    d.rectangle([5, 5, 75, h-5], outline=C_BORDER, width=2)
    d.text((25, 15), str(n), fill=C_BLUE_D, font=_font(48))
    d.rectangle([90, 5, w-5, h-5], outline=C_BORDER, width=2)
    return _to_bytes(img)


def numline_jump(start=0, end=10, mark=5, hop_by=1, **kw) -> BytesIO:
    """Number line with unlabeled tick marks (so the answer is never leaked),
    one labeled starting point, a hop arrow showing +1/-1/+2 etc, and an
    empty answer box at the destination tick. Fully wordless, with a
    BEFORE/AFTER mascot+flag above indicating direction."""
    w, h = 420, 110
    icon_h = 70
    img, d = _blank(w, h + icon_h)
    label = "after" if hop_by > 0 else "before"
    _draw_mini_mascot_flag(d, w/2 - 14, 26, 22, label)
    pad = 30
    line_y = 60 + icon_h
    total = end - start
    scale = (w - 2*pad) / max(total, 1)
    d.line([(pad, line_y), (w - pad, line_y)], fill=C_BORDER, width=3)
    for i in range(total + 1):
        val = start + i
        x = int(pad + (val - start) * scale)
        d.line([(x, line_y - 7), (x, line_y + 7)], fill=C_BORDER, width=2)
    d.polygon([(w-pad, line_y), (w-pad-9, line_y-5), (w-pad-9, line_y+5)], fill=C_BORDER)
    d.polygon([(pad, line_y), (pad+9, line_y-5), (pad+9, line_y+5)], fill=C_BORDER)

    mx = int(pad + (mark - start) * scale)
    d.ellipse([mx-7, line_y-7, mx+7, line_y+7], outline=C_BORDER, width=2)
    d.text((mx-7, line_y-26), str(mark), fill=C_BORDER, font=_font(14))

    dest = mark + hop_by
    dx = int(pad + (dest - start) * scale)
    arc_y = line_y - 26
    d.arc([min(mx,dx), arc_y, max(mx,dx), line_y-8], 0, 180, fill=C_BORDER, width=2)
    sym = "+" if hop_by > 0 else "-"
    d.text(((mx+dx)//2 - 8, arc_y - 16), f"{sym}{abs(hop_by)}", fill=C_BORDER, font=_font(12))

    box = 22
    d.rectangle([dx-box//2, line_y+14, dx+box//2, line_y+14+box], outline=C_BORDER, width=2)
    return _to_bytes(img)


_MASCOT_COLORS = {
    "+": ("#F5A623", "#D88A0E"),   # orange body, darker orange shadow/limbs
    "-": ("#5DADE2", "#2E86C1"),   # blue body
    "=": ("#52BE80", "#27884B"),   # green body
    ">": ("#AF7AC5", "#7D3C98"),   # purple body
    "<": ("#AF7AC5", "#7D3C98"),
}
_OP_LABELS = {"+": "ADD", "-": "SUBTRACT", "=": "EQUALS", ">": "MORE", "<": "LESS",
              "count": "COUNT", "compare": "COMPARE", "after": "AFTER", "before": "BEFORE",
              "pattern": "PATTERN", "missing": "MISSING", "value": "VALUE",
              "evenodd": "EVEN OR ODD?", "primecomp": "PRIME OR NOT?", "group": "GROUP",
              "multiply": "MULTIPLY", "divide": "DIVIDE", "share": "SHARE EQUALLY",
              "barmodel": "BAR MODEL", "factfamily": "FACT FAMILY"}


def _draw_mascot(d, cx, cy, r, op):
    """Rounded cartoon mascot character: blob body, big eyes, blush cheeks,
    smile, two simple arms, and the operation symbol held on its belly."""
    body, shadow = _MASCOT_COLORS.get(op, _MASCOT_COLORS["+"])

    # Arms (simple rounded limbs behind the body)
    d.ellipse([cx-r*1.35, cy+r*0.1, cx-r*0.75, cy+r*0.55], fill=shadow)
    d.ellipse([cx+r*0.75, cy+r*0.1, cx+r*1.35, cy+r*0.55], fill=shadow)

    # Body (slightly squashed circle for a friendly blob look)
    d.ellipse([cx-r, cy-r*0.95, cx+r, cy+r*1.05], fill=body, outline=shadow, width=3)

    # Feet
    foot_r = r*0.28
    d.ellipse([cx-r*0.5-foot_r, cy+r*0.95, cx-r*0.5+foot_r, cy+r*0.95+foot_r*1.4], fill=shadow)
    d.ellipse([cx+r*0.5-foot_r, cy+r*0.95, cx+r*0.5+foot_r, cy+r*0.95+foot_r*1.4], fill=shadow)

    # Eyes (big white ovals + black pupils, slight squash for charm)
    eye_w, eye_h = r*0.28, r*0.34
    for dx in (-r*0.32, r*0.32):
        ex, ey = cx+dx, cy-r*0.15
        d.ellipse([ex-eye_w, ey-eye_h, ex+eye_w, ey+eye_h], fill="#FFFFFF", outline=C_BORDER, width=2)
        pr = eye_w*0.45
        d.ellipse([ex-pr, ey-pr+2, ex+pr, ey+pr+2], fill=C_BORDER)

    # Blush cheeks
    blush_r = r*0.14
    for dx in (-r*0.55, r*0.55):
        d.ellipse([cx+dx-blush_r, cy+r*0.18-blush_r, cx+dx+blush_r, cy+r*0.18+blush_r],
                  fill="#FFFFFF", outline=None)
        d.ellipse([cx+dx-blush_r, cy+r*0.18-blush_r, cx+dx+blush_r, cy+r*0.18+blush_r],
                  fill="#F1948A")

    # Smile
    d.arc([cx-r*0.32, cy+r*0.05, cx+r*0.32, cy+r*0.5], 20, 160, fill=C_BORDER, width=3)

    # Operation symbol on the belly (white badge + symbol)
    badge_r = r*0.4
    d.ellipse([cx-badge_r, cy+r*0.42-badge_r, cx+badge_r, cy+r*0.42+badge_r], fill="#FFFFFF", outline=shadow, width=2)
    sym_t, sym_s = badge_r*0.22, badge_r*0.55
    bx, by = cx, cy+r*0.42
    if op == "+":
        d.rectangle([bx-sym_t, by-sym_s, bx+sym_t, by+sym_s], fill=shadow)
        d.rectangle([bx-sym_s, by-sym_t, bx+sym_s, by+sym_t], fill=shadow)
    elif op == "-":
        d.rectangle([bx-sym_s, by-sym_t, bx+sym_s, by+sym_t], fill=shadow)
    elif op == "=":
        d.rectangle([bx-sym_s, by-sym_t-4, bx+sym_s, by+sym_t-4], fill=shadow)
        d.rectangle([bx-sym_s, by-sym_t+4, bx+sym_s, by+sym_t+4], fill=shadow)
    elif op in (">", "<"):
        pts = ([(bx-sym_s, by-sym_s), (bx+sym_s, by), (bx-sym_s, by+sym_s)] if op == "<"
               else [(bx+sym_s, by-sym_s), (bx-sym_s, by), (bx+sym_s, by+sym_s)])
        d.line(pts, fill=shadow, width=int(sym_t*1.6), joint="curve")


def _draw_banner(d, cx, top_y, w, text, color):
    """Ribbon-style banner: rounded rect body + small triangular ribbon tails
    at each end, with bold white text centered."""
    h = 26
    tail = 10
    x0, x1 = cx - w/2, cx + w/2
    y0, y1 = top_y, top_y + h
    # Ribbon tails (small notched triangles)
    d.polygon([(x0-tail, y0), (x0, y0), (x0, y1), (x0-tail, y1), (x0-tail+5, (y0+y1)/2)], fill=color)
    d.polygon([(x1+tail, y0), (x1, y0), (x1, y1), (x1+tail, y1), (x1+tail-5, (y0+y1)/2)], fill=color)
    d.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=color)
    fnt = _font(13)
    tw = d.textlength(text, font=fnt)
    d.text((cx - tw/2, y0 + (h-13)/2 - 1), text, fill="#FFFFFF", font=fnt)


def instruction_icon(symbols=("+", "-"), **kw) -> BytesIO:
    """Black-and-white, outline-only (ink-saving) instruction card per
    symbol: a friendly line-art mascot face with a flag-on-a-stick
    spelling out the keyword (ADD / SUBTRACT / MORE / LESS / EQUALS)."""
    card_w = 90
    gap = 10
    n = len(symbols)
    w = n * card_w + (n - 1) * gap + 20
    h = 110
    img, d = _blank(w, h)
    for i, sym in enumerate(symbols):
        cx = 10 + i * (card_w + gap) + card_w/2
        _draw_mini_mascot_flag(d, cx - 14, 26, 28, sym)
    return _to_bytes(img)


def sequence_boxes(seq=None, blank_indices=None, label="pattern", **kw) -> BytesIO:
    """Row of boxes showing a number sequence -- known numbers printed
    inside their box, blank positions left empty. Used to replace plain
    'n, ___, m' text with a pictorial box-row + mascot instruction.
    seq: list of ints/None where None marks a blank position (alternative
    to passing blank_indices)."""
    if seq is None:
        seq = [1, 2, 3]
    if blank_indices is None:
        blank_indices = [i for i, v in enumerate(seq) if v is None]
    box = 40
    gap = 10
    n = len(seq)
    icon_h = 70
    w = n*box + (n-1)*gap + 20
    h = box + 20 + icon_h
    img, d = _blank(w, h)
    _draw_mini_mascot_flag(d, w/2 - 14, 26, 22, label)
    fnt = _font(16)
    for i, val in enumerate(seq):
        x0 = 10 + i*(box+gap)
        y0 = icon_h + 10
        d.rectangle([x0, y0, x0+box, y0+box], outline=C_BORDER, width=2)
        if i not in blank_indices and val is not None:
            text = str(val)
            tw = d.textlength(text, font=fnt)
            d.text((x0 + box/2 - tw/2, y0 + box/2 - 10), text, fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def compare_blocks(left=47, right=52, **kw) -> BytesIO:
    """Compare two numbers using base-10 blocks side by side (for numbers
    too large to draw as individual dots, e.g. 1-100 range), plus the
    same >/</= tick-boxes as compare_choice. Wordless, with COMPARE mascot."""
    icon_h = 70
    block_area_h = 190   # fits up to 2 rows of bigger rods (tens digit 0-9) + TENS/ONES labels
    half_w = 235
    w = half_w*2 + 30
    h = icon_h + block_area_h + 50
    img, d = _blank(w, h)
    _draw_mini_mascot_flag(d, w/2 - 14, 26, 22, "compare")
    d.line([half_w+15, icon_h+5, half_w+15, icon_h+block_area_h-15], fill=C_GRAY_D, width=2)

    def draw_side(n, x_off):
        tens, ones = divmod(n, 10)
        rod_w, rod_h, unit, gap = 14, 70, 14, 6
        for i in range(tens):
            row, col = divmod(i, 5)
            x = x_off + 10 + col*(rod_w+gap)
            y = icon_h + 10 + row*(rod_h+gap)
            d.rectangle([x, y, x+rod_w, y+rod_h], outline=C_BORDER, width=2)
        fnt = _font_reg(11)
        tw = d.textlength("TENS", font=fnt)
        d.text((x_off + 10 + 50 - tw/2, icon_h + 165), "TENS", fill=C_BORDER, font=fnt)
        ones_x = x_off + 125
        for i in range(ones):
            row, col = divmod(i, 5)
            x = ones_x + col*(unit+gap)
            y = icon_h + 10 + row*(unit+gap)
            d.rectangle([x, y, x+unit, y+unit], outline=C_BORDER, width=2)
        tw2 = d.textlength("ONES", font=fnt)
        d.text((ones_x + 50 - tw2/2, icon_h + 165), "ONES", fill=C_BORDER, font=fnt)

    draw_side(left, 0)
    draw_side(right, half_w+30)

    box_y = icon_h + block_area_h + 8
    box_size = 26
    gap = 16
    start_x = (w - (box_size*3 + gap*2)) / 2
    for i, sym in enumerate([">", "<", "="]):
        bx = start_x + i*(box_size+gap)
        d.rectangle([bx, box_y, bx+box_size, box_y+box_size], outline=C_BORDER, width=2)
        cx, cy_s = bx+box_size/2, box_y+box_size/2
        if sym == "=":
            d.line([cx-7, cy_s-4, cx+7, cy_s-4], fill=C_BORDER, width=2)
            d.line([cx-7, cy_s+4, cx+7, cy_s+4], fill=C_BORDER, width=2)
        elif sym == ">":
            d.line([cx-6, cy_s-7, cx+6, cy_s], fill=C_BORDER, width=2)
            d.line([cx-6, cy_s+7, cx+6, cy_s], fill=C_BORDER, width=2)
        else:
            d.line([cx+6, cy_s-7, cx-6, cy_s], fill=C_BORDER, width=2)
            d.line([cx+6, cy_s+7, cx-6, cy_s], fill=C_BORDER, width=2)
    return _to_bytes(img)


def pair_grouping(count=6, kind="apple", **kw) -> BytesIO:
    """Objects grouped into pairs with a loop drawn around each pair; if
    count is odd, the last object stands alone with no loop (visually
    showing 'leftover'). EVEN OR ODD? mascot above + EVEN/ODD tick boxes
    at the bottom. Wordless except the two tick-box keywords."""
    r = 14
    cell = r*2 + 10
    pair_gap = 26
    cols = 5  # pairs per row
    n_pairs = count // 2
    has_leftover = count % 2 == 1
    icon_h = 70
    w = cols * (cell*2 + pair_gap) + 30
    rows = (n_pairs + (1 if has_leftover else 0) + cols - 1) // cols
    rows = max(rows, 1)
    h = icon_h + rows*(cell+20) + 60
    img, d = _blank(w, h)
    _draw_mini_mascot_flag(d, w/2 - 14, 26, 22, "evenodd")

    idx = 0
    for p in range(n_pairs):
        row, col = divmod(p, cols)
        x0 = 15 + col*(cell*2+pair_gap)
        y0 = icon_h + 10 + row*(cell+20)
        cx1, cy1 = x0+r, y0+r
        cx2, cy2 = x0+cell+r, y0+r
        _draw_object(d, cx1, cy1, r, kind)
        _draw_object(d, cx2, cy2, r, kind)
        d.ellipse([x0-6, y0-6, x0+cell*2-2, y0+cell+2], outline=C_BORDER, width=2)
        idx += 1
    if has_leftover:
        row, col = divmod(n_pairs, cols)
        x0 = 15 + col*(cell*2+pair_gap)
        y0 = icon_h + 10 + row*(cell+20)
        _draw_object(d, x0+r, y0+r, r, kind)

    box_y = h - 45
    box_w, box_h = 70, 30
    gap = 20
    start_x = (w - (box_w*2 + gap)) / 2
    fnt = _font_reg(13)
    for i, label in enumerate(["EVEN", "ODD"]):
        bx = start_x + i*(box_w+gap)
        d.rectangle([bx, box_y, bx+box_w, box_y+box_h], outline=C_BORDER, width=2)
        tw = d.textlength(label, font=fnt)
        d.text((bx+box_w/2-tw/2, box_y+box_h/2-8), label, fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def array_grid(n=6, rows=2, **kw) -> BytesIO:
    """Dots arranged in a grid (rows x cols=n/rows) to visually teach
    prime vs composite: a single straight LINE (1 row) = PRIME, a
    rectangular GRID (2+ rows) = COMPOSITE. PRIME OR NOT? mascot above +
    PRIME/COMPOSITE tick boxes at the bottom."""
    cols = max(1, n // max(rows, 1))
    r = 12
    cell = r*2 + 10
    icon_h = 70
    w = max(cols*cell + 30, 260)
    grid_w = cols * cell
    x_start = (w - grid_w) / 2
    h = icon_h + rows*cell + 80
    img, d = _blank(w, h)
    _draw_mini_mascot_flag(d, w/2 - 14, 26, 22, "primecomp")
    for i in range(n):
        row, col = divmod(i, cols)
        cx = x_start + r + col*cell
        cy = icon_h + 10 + r + row*cell
        d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=C_BORDER, width=2)

    box_y = h - 45
    box_w, box_h = 95, 30
    gap = 20
    start_x = (w - (box_w*2 + gap)) / 2
    fnt = _font_reg(12)
    for i, label in enumerate(["PRIME", "COMPOSITE"]):
        bx = start_x + i*(box_w+gap)
        d.rectangle([bx, box_y, bx+box_w, box_y+box_h], outline=C_BORDER, width=2)
        tw = d.textlength(label, font=fnt)
        d.text((bx+box_w/2-tw/2, box_y+box_h/2-8), label, fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def multiply_grid(rows=3, cols=4, kind="apple", **kw) -> BytesIO:
    """Objects arranged in `rows` rows of `cols` each, MULTIPLY mascot
    above, blank answer box below -- visualizes rows x cols as repeated
    equal groups. Shrinks object size automatically for big totals so
    the grid never gets squeezed illegibly."""
    n = rows * cols
    big = n > 30
    r = 8 if big else 13
    cell = r*2 + (4 if big else 8)
    icon_h = 70
    grid_w = cols * cell
    w = max(grid_w + 30, 200)
    h = icon_h + rows*cell + 70
    img, d = _blank(w, h)
    _draw_mini_mascot_flag(d, w/2 - 14, 26, 22, "multiply")
    x_start = (w - grid_w) / 2
    for i in range(n):
        row, col = divmod(i, cols)
        cx = x_start + r + col*cell
        cy = icon_h + 10 + r + row*cell
        _draw_object(d, cx, cy, r, kind)
    box_w, box_h = 60, 40
    bx = w/2 - box_w/2
    by = icon_h + rows*cell + 20
    d.rectangle([bx, by, bx+box_w, by+box_h], outline=C_BORDER, width=3)
    return _to_bytes(img)


def repeated_groups(groups=3, size=4, kind="apple", **kw) -> BytesIO:
    """Multiplication as REPEATED EQUAL GROUPS, visually distinct from
    multiply_grid: each group is a separate cluster with a gap between
    them (like looking at 3 separate baskets of 4 apples each), with a
    small x{size} label under each cluster -- bridges the addition
    concept (separate piles) into multiplication (groups x size)."""
    r = 11
    cell = r*2 + 6
    cluster_cols = min(size, 5)
    cluster_rows = (size + cluster_cols - 1) // cluster_cols
    cluster_w = cluster_cols * cell
    cluster_h = cluster_rows * cell
    gap_between = 22
    icon_h = 70
    label_h = 18
    w = groups * cluster_w + (groups - 1) * gap_between + 20
    h = icon_h + cluster_h + label_h + 60
    img, d = _blank(max(w, 200), h)
    _draw_mini_mascot_flag(d, max(w, 200)/2 - 14, 26, 22, "multiply")
    fnt = _font_reg(11)
    for g in range(groups):
        x0 = 10 + g*(cluster_w + gap_between)
        for i in range(size):
            row, col = divmod(i, cluster_cols)
            cx = x0 + r + col*cell
            cy = icon_h + 10 + r + row*cell
            _draw_object(d, cx, cy, r, kind)
        label = f"x {size}"
        tw = d.textlength(label, font=fnt)
        d.rectangle([x0-4, icon_h+8, x0+cluster_w+4, icon_h+cluster_h+8], outline=C_GRAY_D, width=1)
        d.text((x0 + cluster_w/2 - tw/2, icon_h + cluster_h + 14), label, fill=C_BORDER, font=fnt)
    box_w, box_h = 60, 36
    bx = max(w, 200)/2 - box_w/2
    by = h - 45
    d.rectangle([bx, by, bx+box_w, by+box_h], outline=C_BORDER, width=3)
    return _to_bytes(img)


def sharing_baskets(total=12, num_baskets=3, kind="apple", **kw) -> BytesIO:
    """EQUAL SHARING (distinct from equal GROUPING): objects are shown
    as a loose, SCATTERED pile (not pre-arranged into rows), with a
    fixed number of empty basket outlines below. The child must mentally
    share the pile evenly among the baskets -- unlike object_group's
    grouping view, this picture does NOT pre-arrange the answer for them.
    Per Singapore Math research, equal sharing ('how many in each
    basket?') is a distinct concept from equal grouping ('how many
    groups?') and should be taught as its own visual."""
    import random as _r
    rnd = _r.Random(total * 31 + num_baskets * 7)
    r = 11
    icon_h = 70
    pile_w, pile_h = 220, 90
    basket_w, basket_h = 60, 44
    basket_gap = 16
    baskets_w = num_baskets * basket_w + (num_baskets - 1) * basket_gap
    w = max(pile_w, baskets_w) + 30
    h = icon_h + pile_h + 30 + basket_h + 20
    img, d = _blank(w, h)
    _draw_mini_mascot_flag(d, w/2 - 14, 26, 22, "share")

    # Scattered pile (jittered positions within the pile area, no grid)
    pile_x0 = (w - pile_w) / 2
    pile_y0 = icon_h
    placed = []
    attempts = 0
    while len(placed) < total and attempts < total * 30:
        attempts += 1
        cx = pile_x0 + r + rnd.uniform(0, pile_w - 2*r)
        cy = pile_y0 + r + rnd.uniform(0, pile_h - 2*r)
        if all((cx-px)**2 + (cy-py)**2 > (r*1.7)**2 for px, py in placed):
            placed.append((cx, cy))
    for cx, cy in placed:
        _draw_object(d, cx, cy, r, kind)

    # Empty baskets in a row below the pile
    by0 = icon_h + pile_h + 25
    bx0 = (w - baskets_w) / 2
    for i in range(num_baskets):
        x0 = bx0 + i*(basket_w + basket_gap)
        d.line([x0, by0, x0+basket_w*0.15, by0+basket_h], fill=C_BORDER, width=2)
        d.line([x0+basket_w, by0, x0+basket_w*0.85, by0+basket_h], fill=C_BORDER, width=2)
        d.line([x0+basket_w*0.15, by0+basket_h, x0+basket_w*0.85, by0+basket_h], fill=C_BORDER, width=2)
        d.line([x0, by0, x0+basket_w, by0], fill=C_BORDER, width=2)
    return _to_bytes(img)


def division_bar_model(total=12, parts=3, **kw) -> BytesIO:
    """Singapore Math's signature BAR MODEL: a single rectangle bar
    split into `parts` equal segments by vertical lines, with the total
    value labeled above the whole bar and a '?' in one segment --
    the abstract/bridge representation of division as splitting a whole
    into equal parts."""
    icon_h = 70
    bar_w, bar_h = max(40*parts, 200), 50
    w = bar_w + 40
    h = icon_h + bar_h + 60
    img, d = _blank(w, h)
    _draw_mini_mascot_flag(d, w/2 - 14, 26, 22, "barmodel")
    bx0 = (w - bar_w) / 2
    by0 = icon_h + 30
    d.rectangle([bx0, by0, bx0+bar_w, by0+bar_h], outline=C_BORDER, width=3)
    seg_w = bar_w / parts
    for i in range(1, parts):
        x = bx0 + i*seg_w
        d.line([x, by0, x, by0+bar_h], fill=C_BORDER, width=2)
    # Total label above the bar, with brackets showing it spans the whole bar
    fnt = _font(14)
    total_str = str(total)
    tw = d.textlength(total_str, font=fnt)
    d.text((bx0 + bar_w/2 - tw/2, by0 - 24), total_str, fill=C_BORDER, font=fnt)
    d.line([bx0, by0-8, bx0+bar_w, by0-8], fill=C_BORDER, width=1)
    d.line([bx0, by0-8, bx0, by0-2], fill=C_BORDER, width=1)
    d.line([bx0+bar_w, by0-8, bx0+bar_w, by0-2], fill=C_BORDER, width=1)
    # Question mark in the first segment (every segment is equal, so one suffices)
    qfnt = _font(16)
    qtw = d.textlength("?", font=qfnt)
    d.text((bx0 + seg_w/2 - qtw/2, by0 + bar_h/2 - 11), "?", fill=C_BORDER, font=qfnt)
    return _to_bytes(img)


def fraction_area_blank(den1=3, den2=4, **kw) -> BytesIO:
    """EMPTY grid (den1 columns x den2 rows), outline only, no shading,
    no colour -- the child shades it themselves by hand. Black-and-white,
    ink-saving (just grid lines)."""
    w, h = 280, 200
    img, d = _blank(w, h)
    gx0, gy0 = 30, 20
    gw, gh = 220, 160
    col_w = gw / den1
    row_h = gh / den2
    for c in range(den1+1):
        x = gx0 + c*col_w
        d.line([x, gy0, x, gy0+gh], fill=C_BORDER, width=2)
    for r in range(den2+1):
        y = gy0 + r*row_h
        d.line([gx0, y, gx0+gw, y], fill=C_BORDER, width=2)
    return _to_bytes(img)


def fraction_area_example(num1=2, den1=3, num2=3, den2=4, **kw) -> BytesIO:
    """The ONE worked example shown step by step, using black-and-white
    HATCHING patterns instead of flat colour fills (vertical hatch =
    first fraction's columns, horizontal hatch = second fraction's rows,
    cross-hatch = the overlap/product) -- ink-saving and colour-free."""
    w, h = 300, 240
    img, d = _blank(w, h)
    gx0, gy0 = 30, 15
    gw, gh = 220, 160
    col_w = gw / den1
    row_h = gh / den2

    def hatch_vert(x0, y0, x1, y1, step=6):
        x = x0
        while x < x1:
            d.line([x, y0, x, y1], fill=C_BORDER, width=1)
            x += step

    def hatch_horiz(x0, y0, x1, y1, step=6):
        y = y0
        while y < y1:
            d.line([x0, y, x1, y], fill=C_BORDER, width=1)
            y += step

    for r in range(den2):
        for c in range(den1):
            x0, y0 = gx0 + c*col_w, gy0 + r*row_h
            x1, y1 = x0+col_w, y0+row_h
            in_col = c < num1
            in_row = r < num2
            if in_col and in_row:
                hatch_vert(x0, y0, x1, y1)
                hatch_horiz(x0, y0, x1, y1)
            elif in_col:
                hatch_vert(x0, y0, x1, y1)
            elif in_row:
                hatch_horiz(x0, y0, x1, y1)

    for c in range(den1+1):
        x = gx0 + c*col_w
        d.line([x, gy0, x, gy0+gh], fill=C_BORDER, width=2)
    for r in range(den2+1):
        y = gy0 + r*row_h
        d.line([gx0, y, gx0+gw, y], fill=C_BORDER, width=2)

    fnt = _font_reg(13)
    d.text((gx0, gy0+gh+10),
            f"{num1}/{den1} x {num2}/{den2} = {num1*num2}/{den1*den2}", fill=C_BORDER, font=fnt)
    return _to_bytes(img)




def fraction_bar(num=3, den=4, kind="rect", **kw) -> BytesIO:
    """Simple fraction bar model: a rectangle split into `den` equal
    parts, `num` of them shaded -- the core Singapore pictorial tool
    for fraction concept/comparison/addition at any grade."""
    w, h = max(den*36, 160), 70
    img, d = _blank(w, h)
    x0, y0 = 10, 10
    seg_w = (w - 20) / den
    seg_h = 40
    for i in range(den):
        x = x0 + i*seg_w
        fill = "#AED6F1" if i < num else "#FFFFFF"
        d.rectangle([x, y0, x+seg_w, y0+seg_h], fill=fill, outline=C_BORDER, width=2)
    return _to_bytes(img)


def _hatch_cell(d, x0, y0, x1, y1, style, step=6):
    """style: 'v' vertical, 'h' horizontal, 'x' cross, '' blank."""
    if style in ("v", "x"):
        x = x0
        while x < x1:
            d.line([x, y0, x, y1], fill=C_BORDER, width=1)
            x += step
    if style in ("h", "x"):
        y = y0
        while y < y1:
            d.line([x0, y, x1, y], fill=C_BORDER, width=1)
            y += step


def fraction_bar_blank(den=4, segments=1, **kw) -> BytesIO:
    """One or more EMPTY bars stacked, each split into `den` equal
    segments -- for the child to shade themselves. `segments`>1 is used
    for mixed numbers (one bar per whole + a final partial bar)."""
    seg_w = 36
    bar_w = seg_w * den
    bar_h = 40
    gap = 10
    w = bar_w + 20
    h = segments*(bar_h+gap) + 10
    img, d = _blank(max(w, 160), h)
    for s in range(segments):
        y0 = 10 + s*(bar_h+gap)
        for i in range(den):
            x0 = 10 + i*seg_w
            d.rectangle([x0, y0, x0+seg_w, y0+bar_h], outline=C_BORDER, width=2)
    return _to_bytes(img)


def fraction_bar_example(num=3, den=4, label=None, **kw) -> BytesIO:
    """ONE worked-example bar: `num` of `den` segments hatched (B&W),
    with the fraction labeled underneath."""
    seg_w = 36
    bar_w = seg_w * den
    bar_h = 40
    w = bar_w + 20
    h = bar_h + 35
    img, d = _blank(max(w, 160), h)
    for i in range(den):
        x0 = 10 + i*seg_w
        if i < num:
            _hatch_cell(d, x0, 10, x0+seg_w, 10+bar_h, "v")
        d.rectangle([x0, 10, x0+seg_w, 10+bar_h], outline=C_BORDER, width=2)
    fnt = _font_reg(13)
    txt = label if label else f"{num}/{den}"
    d.text((10, 10+bar_h+8), txt, fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def two_bars_blank(den1=3, den2=4, **kw) -> BytesIO:
    """Two EMPTY bars stacked (different denominators) -- for
    comparing, finding equivalents, or adding/subtracting unlike
    fractions. The child shades and/or re-partitions them by hand."""
    seg_w = 30
    bar_h = 36
    gap = 14
    w = max(den1, den2) * seg_w + 20
    h = bar_h*2 + gap + 10
    img, d = _blank(max(w, 160), h)
    for i in range(den1):
        x0 = 10 + i*seg_w
        d.rectangle([x0, 10, x0+seg_w, 10+bar_h], outline=C_BORDER, width=2)
    y2 = 10 + bar_h + gap
    for i in range(den2):
        x0 = 10 + i*seg_w
        d.rectangle([x0, y2, x0+seg_w, y2+bar_h], outline=C_BORDER, width=2)
    return _to_bytes(img)


def two_bars_example(num1=1, den1=3, num2=2, den2=4, op="compare", **kw) -> BytesIO:
    """Worked example: two hatched bars (different hatch direction per
    bar) stacked for comparison, or shown with a +/- label between them."""
    seg_w = 30
    bar_h = 36
    gap = 20
    w = max(den1, den2) * seg_w + 20
    h = bar_h*2 + gap + 35
    img, d = _blank(max(w, 160), h)
    for i in range(den1):
        x0 = 10 + i*seg_w
        if i < num1:
            _hatch_cell(d, x0, 10, x0+seg_w, 10+bar_h, "v")
        d.rectangle([x0, 10, x0+seg_w, 10+bar_h], outline=C_BORDER, width=2)
    fnt = _font_reg(12)
    d.text((10, 10+bar_h+2), f"{num1}/{den1}", fill=C_BORDER, font=fnt)
    y2 = 10 + bar_h + gap
    for i in range(den2):
        x0 = 10 + i*seg_w
        if i < num2:
            _hatch_cell(d, x0, y2, x0+seg_w, y2+bar_h, "h")
        d.rectangle([x0, y2, x0+seg_w, y2+bar_h], outline=C_BORDER, width=2)
    d.text((10, y2+bar_h+2), f"{num2}/{den2}", fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def fraction_numberline_blank(den=4, **kw) -> BytesIO:
    """A 0-to-1 number line split into `den` equal ticks, unlabeled --
    for placing/estimating fractions (benchmark 0, 1/2, 1 reasoning)."""
    w, h = 260, 70
    img, d = _blank(w, h)
    pad = 20
    y = 35
    d.line([pad, y, w-pad, y], fill=C_BORDER, width=2)
    for i in range(den+1):
        x = pad + i*(w-2*pad)/den
        d.line([x, y-8, x, y+8], fill=C_BORDER, width=2)
    fnt = _font_reg(11)
    d.text((pad-4, y+12), "0", fill=C_BORDER, font=fnt)
    d.text((w-pad-6, y+12), "1", fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def fraction_numberline_example(num=1, den=2, **kw) -> BytesIO:
    """Worked example: a marked point on the 0-1 number line at num/den."""
    w, h = 260, 80
    img, d = _blank(w, h)
    pad = 20
    y = 35
    d.line([pad, y, w-pad, y], fill=C_BORDER, width=2)
    for i in range(den+1):
        x = pad + i*(w-2*pad)/den
        d.line([x, y-8, x, y+8], fill=C_BORDER, width=2)
    mx = pad + num*(w-2*pad)/den
    d.ellipse([mx-5, y-5, mx+5, y+5], outline=C_BORDER, width=2)
    fnt = _font_reg(11)
    d.text((pad-4, y+12), "0", fill=C_BORDER, font=fnt)
    d.text((w-pad-6, y+12), "1", fill=C_BORDER, font=fnt)
    fnt2 = _font(12)
    lbl = f"{num}/{den}"
    tw = d.textlength(lbl, font=fnt2)
    d.text((mx-tw/2, y-26), lbl, fill=C_BORDER, font=fnt2)
    return _to_bytes(img)


def hundredths_grid_blank(**kw) -> BytesIO:
    """EMPTY 10x10 grid (100 squares), outline only -- for the child to
    shade hundredths themselves. No answer leaked."""
    cell = 18
    w, h = 10*cell + 20, 10*cell + 20
    img, d = _blank(w, h)
    for row in range(10):
        for col in range(10):
            x0, y0 = 10+col*cell, 10+row*cell
            d.rectangle([x0, y0, x0+cell, y0+cell], outline=C_BORDER, width=1)
    return _to_bytes(img)


def hundredths_grid_example(shaded=25, **kw) -> BytesIO:
    """Worked example: `shaded` of 100 squares hatched (B&W), labeled."""
    cell = 18
    w, h = 10*cell + 20, 10*cell + 35
    img, d = _blank(w, h)
    for row in range(10):
        for col in range(10):
            idx = row*10 + col
            x0, y0 = 10+col*cell, 10+row*cell
            if idx < shaded:
                _hatch_cell(d, x0, y0, x0+cell, y0+cell, "v", step=4)
            d.rectangle([x0, y0, x0+cell, y0+cell], outline=C_BORDER, width=1)
    fnt = _font_reg(12)
    d.text((10, h-22), f"{shaded}/100 = 0.{str(shaded).zfill(2)}", fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def decimal_place_blank(has_ones=True, n_decimal=2, **kw) -> BytesIO:
    """EMPTY place-value chart: column headers only (Ones | . | Tenths |
    Hundredths...), boxes left blank for the child to fill in digits."""
    labels = (["Ones"] if has_ones else []) + ["."] + \
             ["Tenths", "Hundredths", "Thousandths"][:n_decimal]
    col_w = 60
    w = col_w * len(labels) + 20
    h = 90
    img, d = _blank(w, h)
    fnt = _font_reg(10)
    for i, lbl in enumerate(labels):
        x0 = 10 + i*col_w
        if lbl == ".":
            d.text((x0+col_w/2-4, 35), ".", fill=C_BORDER, font=_font(20))
            continue
        d.rectangle([x0, 30, x0+col_w-6, 30+40], outline=C_BORDER, width=2)
        tw = d.textlength(lbl, font=fnt)
        d.text((x0+(col_w-6)/2-tw/2, 8), lbl, fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def decimal_place_example(number="3.47", **kw) -> BytesIO:
    """Worked example: a place-value chart with the digits of `number`
    actually filled in, B&W, for the ONE worked instance per sub-level."""
    parts = number.split(".")
    whole = parts[0]
    dec = parts[1] if len(parts) > 1 else ""
    dec_labels = ["Tenths", "Hundredths", "Thousandths"][:max(len(dec), 1)]
    labels = ["Ones", "."] + dec_labels
    col_w = 60
    w = col_w * len(labels) + 20
    h = 95
    img, d = _blank(w, h)
    fnt = _font_reg(10)
    fnt_big = _font(18)
    digit_idx = 0
    for i, lbl in enumerate(labels):
        x0 = 10 + i*col_w
        if lbl == ".":
            d.text((x0+col_w/2-4, 38), ".", fill=C_BORDER, font=_font(20))
            continue
        d.rectangle([x0, 30, x0+col_w-6, 30+40], outline=C_BORDER, width=2)
        tw = d.textlength(lbl, font=fnt)
        d.text((x0+(col_w-6)/2-tw/2, 8), lbl, fill=C_BORDER, font=fnt)
        if lbl == "Ones":
            digit = whole[-1] if whole else "0"
        else:
            di = dec_labels.index(lbl)
            digit = dec[di] if di < len(dec) else "0"
        tw2 = d.textlength(digit, font=fnt_big)
        d.text((x0+(col_w-6)/2-tw2/2, 38), digit, fill=C_BORDER, font=fnt_big)
    return _to_bytes(img)


def decimal_numberline_blank(lo=0.0, hi=1.0, divisions=10, **kw) -> BytesIO:
    """A blank decimal number line from lo to hi with unlabeled ticks
    (except the endpoints) -- for placing/comparing/ordering decimals."""
    w, h = 280, 70
    img, d = _blank(w, h)
    pad = 25
    y = 35
    d.line([pad, y, w-pad, y], fill=C_BORDER, width=2)
    for i in range(divisions+1):
        x = pad + i*(w-2*pad)/divisions
        d.line([x, y-7, x, y+7], fill=C_BORDER, width=2)
    fnt = _font_reg(11)
    d.text((pad-6, y+12), str(lo), fill=C_BORDER, font=fnt)
    d.text((w-pad-10, y+12), str(hi), fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def decimal_numberline_example(value=0.5, lo=0.0, hi=1.0, divisions=10, **kw) -> BytesIO:
    """Worked example: a marked point at `value` on the lo-hi number line."""
    w, h = 280, 80
    img, d = _blank(w, h)
    pad = 25
    y = 35
    d.line([pad, y, w-pad, y], fill=C_BORDER, width=2)
    for i in range(divisions+1):
        x = pad + i*(w-2*pad)/divisions
        d.line([x, y-7, x, y+7], fill=C_BORDER, width=2)
    frac = (value-lo)/(hi-lo) if hi != lo else 0
    mx = pad + frac*(w-2*pad)
    d.ellipse([mx-5, y-5, mx+5, y+5], outline=C_BORDER, width=2)
    fnt = _font_reg(11)
    d.text((pad-6, y+12), str(lo), fill=C_BORDER, font=fnt)
    d.text((w-pad-10, y+12), str(hi), fill=C_BORDER, font=fnt)
    fnt2 = _font(12)
    lbl = str(value)
    tw = d.textlength(lbl, font=fnt2)
    d.text((mx-tw/2, y-26), lbl, fill=C_BORDER, font=fnt2)
    return _to_bytes(img)


def regroup_ones_blank(ones1=7, ones2=5, **kw) -> BytesIO:
    """CARRYING (concrete): two loose clusters of ones units (one per
    addend) shown separately with a + between them, plus an empty
    'trade' area below (a blank rod outline + blank ones row) for the
    child to combine the ones, see if they reach 10+, and draw the
    regrouped result themselves. Outline only, no colour."""
    r = 10
    cell = r*2+4
    cols = 5
    def cluster_dims(n):
        rows = (n+cols-1)//cols if n else 1
        return cols*cell, rows*cell
    w1, h1 = cluster_dims(ones1)
    w2, h2 = cluster_dims(ones2)
    top_h = max(h1, h2) + 20
    w = w1 + 40 + w2 + 30
    h = top_h + 110
    img, d = _blank(max(w, 240), h)
    x = 10
    for i in range(ones1):
        row, col = divmod(i, cols)
        cx, cy = x+r+col*cell, 10+r+row*cell
        d.rectangle([cx-r, cy-r, cx+r, cy+r], outline=C_BORDER, width=2)
    x += w1 + 10
    _draw_big_symbol(d, x+15, top_h/2, 18, "+")
    x += 40
    for i in range(ones2):
        row, col = divmod(i, cols)
        cx, cy = x+r+col*cell, 10+r+row*cell
        d.rectangle([cx-r, cy-r, cx+r, cy+r], outline=C_BORDER, width=2)

    # Trade area below: blank rod outline + blank ones row
    ty = top_h + 20
    rod_w, rod_h = 22, 70
    d.rectangle([15, ty, 15+rod_w, ty+rod_h], outline=C_GRAY_D, width=2)
    ox = 15+rod_w+20
    for i in range(4):
        d.rectangle([ox+i*(r*2+4), ty+rod_h-2*r, ox+i*(r*2+4)+2*r, ty+rod_h], outline=C_GRAY_D, width=2)
    fnt = _font_reg(10)
    d.text((15, ty+rod_h+6), "If 10 or more ones, trade for a ten.", fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def regroup_break_blank(tens=4, ones=3, **kw) -> BytesIO:
    """BORROWING (concrete): `tens` rod outlines + `ones` unit outlines
    for the minuend, with the LAST rod marked with a dashed break-line
    (so the child can mentally/physically break it into 10 loose ones),
    plus a blank area below for the regrouped redraw."""
    rod_w, rod_h = 20, 90
    unit = 16
    gap = 8
    w = max(tens*(rod_w+gap) + ones*(unit+gap) + 40, 240)
    h = rod_h + 90
    img, d = _blank(w, h)
    for i in range(tens):
        x0 = 15 + i*(rod_w+gap)
        d.rectangle([x0, 10, x0+rod_w, 10+rod_h], outline=C_BORDER, width=2)
        if i == tens-1:
            # dashed break line across the middle of the last rod
            yseg = 10 + rod_h/2
            xx = x0
            while xx < x0+rod_w:
                d.line([xx, yseg, min(xx+4, x0+rod_w), yseg], fill=C_BORDER, width=2)
                xx += 7
    ox = 15 + tens*(rod_w+gap) + 15
    for i in range(ones):
        x0 = ox + i*(unit+gap)
        d.rectangle([x0, 10+rod_h-unit, x0+unit, 10+rod_h], outline=C_BORDER, width=2)
    fnt = _font_reg(10)
    d.text((15, rod_h+20), "Break one ten into 10 ones if you need more.", fill=C_BORDER, font=fnt)
    # Blank redraw area
    d.rectangle([15, rod_h+40, w-15, rod_h+85], outline=C_GRAY_D, width=1)
    return _to_bytes(img)


def number_bond_blank(known=7, **kw) -> BytesIO:
    """Number bond: a top circle (the whole, blank) connected to two
    bottom circles (one shows the known part, one is blank) -- the
    classic 'make ten' decomposition diagram."""
    w, h = 160, 140
    img, d = _blank(w, h)
    top_r = 22
    bot_r = 20
    tx, ty = w/2, 25
    lx, ly = w/2-40, h-35
    rx, ry = w/2+40, h-35
    d.line([tx, ty, lx, ly], fill=C_BORDER, width=2)
    d.line([tx, ty, rx, ry], fill=C_BORDER, width=2)
    d.ellipse([tx-top_r, ty-top_r, tx+top_r, ty+top_r], outline=C_BORDER, width=2)
    d.ellipse([lx-bot_r, ly-bot_r, lx+bot_r, ly+bot_r], outline=C_BORDER, width=2)
    d.ellipse([rx-bot_r, ry-bot_r, rx+bot_r, ry+bot_r], outline=C_BORDER, width=2)
    fnt = _font(16)
    ks = str(known)
    tw = d.textlength(ks, font=fnt)
    d.text((lx-tw/2, ly-9), ks, fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def make_ten_frame_blank(given=7, **kw) -> BytesIO:
    """A 10-frame (2 rows of 5) with `given` boxes pre-marked (small dot,
    outline only) and the rest empty -- for the 'how many more to make
    10?' bond-to-10 strategy."""
    cell = 30
    w, h = 5*cell+20, 2*cell+20
    img, d = _blank(w, h)
    for i in range(10):
        row, col = divmod(i, 5)
        x0, y0 = 10+col*cell, 10+row*cell
        d.rectangle([x0, y0, x0+cell-4, y0+cell-4], outline=C_BORDER, width=2)
        if i < given:
            cx, cy = x0+(cell-4)/2, y0+(cell-4)/2
            d.ellipse([cx-5, cy-5, cx+5, cy+5], outline=C_BORDER, width=2)
    return _to_bytes(img)


def equal_groups_blank(groups=3, size=4, **kw) -> BytesIO:
    """`groups` separate clusters of `size` empty unit squares each --
    for repeated-addition/equal-groups multiplication concept and word
    problems. Outline only, no colour."""
    r = 10
    cell = r*2+4
    cols = min(size, 5)
    rows = (size+cols-1)//cols
    cluster_w, cluster_h = cols*cell, rows*cell
    gap = 18
    w = groups*cluster_w + (groups-1)*gap + 20
    h = cluster_h + 20
    img, d = _blank(max(w, 160), h)
    for g in range(groups):
        x0 = 10 + g*(cluster_w+gap)
        for i in range(size):
            row, col = divmod(i, cols)
            cx, cy = x0+r+col*cell, 10+r+row*cell
            d.rectangle([cx-r, cy-r, cx+r, cy+r], outline=C_BORDER, width=2)
    return _to_bytes(img)


def equal_groups_example(groups=3, size=4, **kw) -> BytesIO:
    """Worked example: `groups` clusters of `size` units, hatched, with
    the repeated-addition expression labeled underneath."""
    r = 10
    cell = r*2+4
    cols = min(size, 5)
    rows = (size+cols-1)//cols
    cluster_w, cluster_h = cols*cell, rows*cell
    gap = 18
    w = groups*cluster_w + (groups-1)*gap + 20
    h = cluster_h + 35
    img, d = _blank(max(w, 160), h)
    for g in range(groups):
        x0 = 10 + g*(cluster_w+gap)
        for i in range(size):
            row, col = divmod(i, cols)
            cx, cy = x0+r+col*cell, 10+r+row*cell
            _hatch_cell(d, cx-r, cy-r, cx+r, cy+r, "v", step=4)
            d.rectangle([cx-r, cy-r, cx+r, cy+r], outline=C_BORDER, width=2)
    fnt = _font_reg(11)
    label = " + ".join([str(size)]*groups) + f" = {groups} x {size} = {groups*size}"
    d.text((10, h-20), label, fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def array_blank(rows=3, cols=4, **kw) -> BytesIO:
    """Empty rows x cols grid -- the array model for multiplication,
    outline only, for the child to count/fill themselves."""
    cell = 26
    w, h = cols*cell+20, rows*cell+20
    img, d = _blank(max(w,120), max(h,80))
    for r in range(rows):
        for c in range(cols):
            x0, y0 = 10+c*cell, 10+r*cell
            d.rectangle([x0, y0, x0+cell, y0+cell], outline=C_BORDER, width=2)
    return _to_bytes(img)


def array_example(rows=3, cols=4, **kw) -> BytesIO:
    """Worked example: a fully-hatched rows x cols grid, with the
    multiplication fact labeled underneath."""
    cell = 26
    w, h = cols*cell+20, rows*cell+35
    img, d = _blank(max(w,120), max(h,95))
    for r in range(rows):
        for c in range(cols):
            x0, y0 = 10+c*cell, 10+r*cell
            _hatch_cell(d, x0, y0, x0+cell, y0+cell, "x", step=5)
            d.rectangle([x0, y0, x0+cell, y0+cell], outline=C_BORDER, width=2)
    fnt = _font_reg(12)
    d.text((10, h-22), f"{rows} x {cols} = {rows*cols}", fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def division_box_blank(dividend=158, divisor=4, **kw) -> BytesIO:
    """The 'Big 7' / partial-quotients division frame: divisor outside a
    bracket, dividend inside, a blank scratch column on the right for
    the child to jot partial quotients (multiples of the divisor
    subtracted), and a blank line on top for the final quotient."""
    w, h = 280, 140
    img, d = _blank(w, h)
    bx, by = 60, 30
    bw, bh = 110, 70
    fnt = _font(16)
    fnt_s = _font_reg(11)
    # quotient blank line
    d.line([bx, by-8, bx+bw, by-8], fill=C_GRAY_D, width=1)
    d.text((bx+bw/2-15, by-30), "____", fill=C_BORDER, font=fnt_s)
    # bracket: vertical + top horizontal (the "7" shape)
    d.line([bx, by, bx, by+bh], fill=C_BORDER, width=3)
    d.line([bx, by, bx+bw, by], fill=C_BORDER, width=3)
    d.text((bx-35, by+bh/2-10), str(divisor), fill=C_BORDER, font=fnt)
    d.text((bx+10, by+5), str(dividend), fill=C_BORDER, font=fnt)
    # scratch column for partial quotients, to the right
    d.line([bx+bw+15, by, bx+bw+15, by+bh], fill=C_GRAY_D, width=1)
    d.text((bx+bw+20, by+5), "partial", fill=C_GRAY_D, font=fnt_s)
    d.text((bx+bw+20, by+20), "quotients", fill=C_GRAY_D, font=fnt_s)
    return _to_bytes(img)


def division_box_example(dividend=158, divisor=4, partials=None, **kw) -> BytesIO:
    """Worked example: the same frame, but with actual partial-quotient
    steps filled in on the scratch column (e.g. subtract 100, then 25,
    then 8...), and the final quotient written on top."""
    if partials is None:
        partials = [(100, dividend - 100*divisor if dividend >= 100*divisor else 0)]
    w, h = 290, 150
    img, d = _blank(w, h)
    bx, by = 60, 35
    bw, bh = 120, 75
    fnt = _font(15)
    fnt_s = _font_reg(10)
    quotient = sum(p[0] for p in partials)
    qtxt = str(quotient)
    qtw = d.textlength(qtxt, font=fnt)
    d.text((bx+bw/2-qtw/2, by-22), qtxt, fill=C_BORDER, font=fnt)
    d.line([bx, by, bx, by+bh], fill=C_BORDER, width=3)
    d.line([bx, by, bx+bw, by], fill=C_BORDER, width=3)
    d.text((bx-35, by+bh/2-10), str(divisor), fill=C_BORDER, font=fnt)
    d.text((bx+10, by+5), str(dividend), fill=C_BORDER, font=fnt)
    d.line([bx+bw+15, by, bx+bw+15, by+bh], fill=C_GRAY_D, width=1)
    yy = by
    for mult, rem in partials:
        d.text((bx+bw+20, yy), f"{mult} (x{divisor}={mult*divisor})", fill=C_BORDER, font=fnt_s)
        yy += 16
    return _to_bytes(img)


def integer_chips_blank(pos=5, neg=3, **kw) -> BytesIO:
    """Positive and negative counter chips, SCATTERED and MIXED together
    (not pre-paired) -- for the discovery task: 'find the zero pairs
    yourself, then see what's left over.' + chips are plain circles,
    - chips are circles with a minus inside (shape-coded, not colour-
    coded, since this stays B&W)."""
    import random as _r
    rnd = _r.Random(pos*13 + neg*7)
    r = 14
    total = pos + neg
    cols = min(total, 6)
    rows = (total + cols - 1) // cols
    w = cols*(r*2+10) + 20
    h = rows*(r*2+10) + 30
    img, d = _blank(max(w,160), h)
    chips = ["+"]*pos + ["-"]*neg
    rnd.shuffle(chips)
    for i, sym in enumerate(chips):
        row, col = divmod(i, cols)
        cx, cy = 15+r+col*(r*2+10), 15+r+row*(r*2+10)
        d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=C_BORDER, width=2)
        if sym == "+":
            d.line([cx-6, cy, cx+6, cy], fill=C_BORDER, width=2)
            d.line([cx, cy-6, cx, cy+6], fill=C_BORDER, width=2)
        else:
            d.line([cx-6, cy, cx+6, cy], fill=C_BORDER, width=2)
    return _to_bytes(img)


def integer_chips_example(pos=5, neg=3, **kw) -> BytesIO:
    """Worked example: same chips, but with zero pairs circled (a loop
    drawn around each matched +/- pair) so the child sees how pairing
    works before trying it themselves."""
    import random as _r
    rnd = _r.Random(pos*13 + neg*7)
    r = 14
    total = pos + neg
    cols = min(total, 6)
    rows = (total + cols - 1) // cols
    w = cols*(r*2+10) + 20
    h = rows*(r*2+10) + 50
    img, d = _blank(max(w,160), h)
    chips = ["+"]*pos + ["-"]*neg
    rnd.shuffle(chips)
    positions = []
    for i, sym in enumerate(chips):
        row, col = divmod(i, cols)
        cx, cy = 15+r+col*(r*2+10), 15+r+row*(r*2+10)
        d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=C_BORDER, width=2)
        if sym == "+":
            d.line([cx-6, cy, cx+6, cy], fill=C_BORDER, width=2)
            d.line([cx, cy-6, cx, cy+6], fill=C_BORDER, width=2)
        else:
            d.line([cx-6, cy, cx+6, cy], fill=C_BORDER, width=2)
        positions.append((cx, cy, sym))
    # Loop a dashed circle around each matched +/- zero pair found greedily
    pos_list = [p for p in positions if p[2] == "+"]
    neg_list = [p for p in positions if p[2] == "-"]
    n_pairs = min(len(pos_list), len(neg_list))
    for k in range(n_pairs):
        x1, y1, _ = pos_list[k]
        x2, y2, _ = neg_list[k]
        mx, my = (x1+x2)/2, (y1+y2)/2
        rad = max(abs(x1-x2), abs(y1-y2))/2 + r + 4
        d.ellipse([mx-rad, my-rad, mx+rad, my+rad], outline=C_GRAY_D, width=1)
    leftover = abs(pos - neg)
    sign = "+" if pos > neg else "-"
    fnt = _font_reg(12)
    d.text((10, h-22), f"{n_pairs} zero pairs cancel out. Leftover = {sign}{leftover}", fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def vertical_numberline_blank(lo=-10, hi=10, **kw) -> BytesIO:
    """A VERTICAL number line (like a thermometer) -- research-recommended
    specifically for integers since most real contexts (temperature,
    elevation) are vertical. Unlabeled ticks except endpoints."""
    w, h = 90, 240
    img, d = _blank(w, h)
    pad = 20
    x = 45
    d.line([x, pad, x, h-pad], fill=C_BORDER, width=2)
    divisions = hi - lo
    step = max(1, divisions // 10)
    n_ticks = divisions // step
    for i in range(n_ticks+1):
        y = (h-pad) - i*(h-2*pad)/n_ticks
        d.line([x-7, y, x+7, y], fill=C_BORDER, width=2)
    fnt = _font_reg(10)
    d.text((x+12, h-pad-6), str(lo), fill=C_BORDER, font=fnt)
    d.text((x+12, pad-6), str(hi), fill=C_BORDER, font=fnt)
    d.text((x+12, (h-pad+pad)/2-6), "0", fill=C_GRAY_D, font=fnt)
    return _to_bytes(img)


def vertical_numberline_example(value=-3, lo=-10, hi=10, **kw) -> BytesIO:
    """Worked example: a marked point at `value` on the vertical line."""
    w, h = 100, 240
    img, d = _blank(w, h)
    pad = 20
    x = 45
    d.line([x, pad, x, h-pad], fill=C_BORDER, width=2)
    divisions = hi - lo
    step = max(1, divisions // 10)
    n_ticks = divisions // step
    for i in range(n_ticks+1):
        y = (h-pad) - i*(h-2*pad)/n_ticks
        d.line([x-7, y, x+7, y], fill=C_BORDER, width=2)
    fnt = _font_reg(10)
    d.text((x+12, h-pad-6), str(lo), fill=C_BORDER, font=fnt)
    d.text((x+12, pad-6), str(hi), fill=C_BORDER, font=fnt)
    frac = (value-lo)/(hi-lo) if hi != lo else 0
    my = (h-pad) - frac*(h-2*pad)
    d.ellipse([x-6, my-6, x+6, my+6], outline=C_BORDER, width=2)
    fnt2 = _font(13)
    d.text((x-35, my-7), str(value), fill=C_BORDER, font=fnt2)
    return _to_bytes(img)


def magic_square_blank(size=3, given=None, **kw) -> BytesIO:
    """A size x size grid with some cells pre-filled (given) and the
    rest blank, for integer magic-square puzzles (rows/cols/diagonals
    sum to the same value)."""
    if given is None:
        given = {}
    cell = 50
    w, h = size*cell+20, size*cell+20
    img, d = _blank(w, h)
    fnt = _font(16)
    for r in range(size):
        for c in range(size):
            x0, y0 = 10+c*cell, 10+r*cell
            d.rectangle([x0, y0, x0+cell, y0+cell], outline=C_BORDER, width=2)
            val = given.get((r, c))
            if val is not None:
                txt = str(val)
                tw = d.textlength(txt, font=fnt)
                d.text((x0+cell/2-tw/2, y0+cell/2-10), txt, fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def matching_vertical_blank(lefts=None, rights=None, **kw) -> BytesIO:
    """Proper VERTICAL matching layout: numbered items stacked in a left
    column, lettered items stacked (shuffled) in a right column, each
    with a small connector dot -- the child draws a line or writes the
    matching letter in the blank box. This is the standard elementary
    matching-exercise format (two vertical columns), not a single
    cramped line of text."""
    if lefts is None: lefts = ["1", "2", "3"]
    if rights is None: rights = ["A", "B", "C"]
    n = len(lefts)
    row_h = 68
    fnt = _font_reg(26)  # ~15pt effective in the PDF -- clearly larger than body text
    box = 40
    # Size columns dynamically from the ACTUAL content so nothing clips,
    # instead of guessing a fixed width that breaks on longer text.
    tmp_img, tmp_d = _blank(10, 10)
    left_texts = [f"{i+1}) {item}" for i, item in enumerate(lefts)]
    right_texts = [f"{chr(65+i)}) {item}" for i, item in enumerate(rights)]
    left_w = max(tmp_d.textlength(t, font=fnt) for t in left_texts)
    right_w = max(tmp_d.textlength(t, font=fnt) for t in right_texts)
    col_gap = 18
    dot_r = 8
    x_left = 10
    x_dot1 = x_left + left_w + col_gap
    x_box = x_dot1 + dot_r + col_gap
    x_dot2 = x_box + box + col_gap
    x_right = x_dot2 + dot_r + col_gap
    w = int(x_right + right_w + 12)
    h = n * row_h + 36
    img, d = _blank(w, h)
    for i, item in enumerate(lefts):
        y = 18 + i*row_h + row_h/2
        d.text((x_left, y-18), left_texts[i], fill=C_BORDER, font=fnt)
        d.ellipse([x_dot1-dot_r, y-dot_r, x_dot1+dot_r, y+dot_r], outline=C_BORDER, width=3)
        # small answer box for writing the matching letter
        d.rectangle([x_box, y-20, x_box+box, y-20+40], outline=C_BORDER, width=3)
    for i, item in enumerate(rights):
        y = 18 + i*row_h + row_h/2
        d.ellipse([x_dot2-dot_r, y-dot_r, x_dot2+dot_r, y+dot_r], outline=C_BORDER, width=3)
        d.text((x_right, y-18), right_texts[i], fill=C_BORDER, font=fnt)
    return _to_bytes(img)


def matching_vertical_example(lefts=None, rights=None, lines=None, **kw) -> BytesIO:
    """Worked example: same vertical layout, with the correct lines
    already drawn connecting matched pairs."""
    if lefts is None: lefts = ["1+1", "2+2", "3+3"]
    if rights is None: rights = ["6", "2", "4"]
    if lines is None: lines = [0, 2, 1]  # left index i connects to right index lines[i]
    n = len(lefts)
    row_h = 68
    fnt = _font_reg(26)  # ~15pt effective in the PDF -- clearly larger than body text
    tmp_img, tmp_d = _blank(10, 10)
    left_texts = [f"{i+1}) {item}" for i, item in enumerate(lefts)]
    right_texts = [f"{chr(65+i)}) {item}" for i, item in enumerate(rights)]
    left_w = max(tmp_d.textlength(t, font=fnt) for t in left_texts)
    right_w = max(tmp_d.textlength(t, font=fnt) for t in right_texts)
    col_gap = 24
    dot_r = 10
    x_left = 12
    x_dot1 = x_left + left_w + col_gap
    x_dot2 = x_dot1 + 2*dot_r + col_gap
    x_right = x_dot2 + dot_r + col_gap
    w = int(x_right + right_w + 14)
    h = n * row_h + 50
    img, d = _blank(w, h)
    for i, item in enumerate(lefts):
        y = 25 + i*row_h + row_h/2
        d.text((x_left, y-23), left_texts[i], fill=C_BORDER, font=fnt)
        d.ellipse([x_dot1-dot_r, y-dot_r, x_dot1+dot_r, y+dot_r], outline=C_BORDER, width=3)
    for i, item in enumerate(rights):
        y = 25 + i*row_h + row_h/2
        d.ellipse([x_dot2-dot_r, y-dot_r, x_dot2+dot_r, y+dot_r], outline=C_BORDER, width=3)
        d.text((x_right, y-23), right_texts[i], fill=C_BORDER, font=fnt)
    for li, ri in enumerate(lines):
        y1 = 25 + li*row_h + row_h/2
        y2 = 25 + ri*row_h + row_h/2
        d.line([x_dot1+dot_r, y1, x_dot2-dot_r, y2], fill=C_BORDER, width=3)
    return _to_bytes(img)


def math_maze_blank(start=5, step1=3, step2_even=2, step2_odd=4, **kw) -> BytesIO:
    """A genuinely VISUAL math maze with a real fork: START -> add step1
    -> the path PHYSICALLY splits into an EVEN branch (top) and an ODD
    branch (bottom), each leading to its own final step box, both
    converging on FINISH. The child solves step 1, follows whichever
    branch matches (even/odd), then solves that branch's step to reach
    the finish -- the geometry itself shows the decision, not just a
    text label on a straight line."""
    w, h = 520, 220
    img, d = _blank(w, h)
    fnt = _font_reg(13)
    fnt_b = _font(13)
    box_w, box_h = 80, 44
    mid_y = h/2

    def draw_box(cx, cy, text, sub=""):
        d.rectangle([cx-box_w/2, cy-box_h/2, cx+box_w/2, cy+box_h/2], outline=C_BORDER, width=2)
        tw = d.textlength(text, font=fnt_b)
        d.text((cx-tw/2, cy-box_h/2+6), text, fill=C_BORDER, font=fnt_b)
        if sub:
            tw2 = d.textlength(sub, font=fnt)
            d.text((cx-tw2/2, cy+2), sub, fill=C_BORDER, font=fnt)

    def arrow(x0, y0, x1, y1):
        d.line([x0, y0, x1, y1], fill=C_BORDER, width=2)
        import math as _m
        ang = _m.atan2(y1-y0, x1-x0)
        ax, ay = x1 - 9*_m.cos(ang), y1 - 9*_m.sin(ang)
        d.polygon([(x1, y1), (ax-5*_m.sin(ang), ay-5*_m.cos(ang)), (ax+5*_m.sin(ang), ay+5*_m.cos(ang))], fill=C_BORDER)

    x_start = 50
    x_step1 = 180
    x_branch = 340
    x_finish = 470

    draw_box(x_start, mid_y, "START", f"= {start}")
    arrow(x_start+box_w/2, mid_y, x_step1-box_w/2-4, mid_y)
    d.text((x_start+box_w/2+8, mid_y-box_h/2-16), f"+ {step1}", fill=C_BORDER, font=fnt)
    draw_box(x_step1, mid_y, "STEP 1", "= ____")

    top_y = mid_y - 55
    bot_y = mid_y + 55
    arrow(x_step1+box_w/2, mid_y-8, x_branch-box_w/2-4, top_y)
    arrow(x_step1+box_w/2, mid_y+8, x_branch-box_w/2-4, bot_y)
    d.text(((x_step1+x_branch)/2-30, top_y-22), "if EVEN", fill=C_BORDER, font=fnt)
    d.text(((x_step1+x_branch)/2-30, bot_y+8), "if ODD", fill=C_BORDER, font=fnt)
    draw_box(x_branch, top_y, "EVEN PATH", f"+ {step2_even}")
    draw_box(x_branch, bot_y, "ODD PATH", f"+ {step2_odd}")

    arrow(x_branch+box_w/2, top_y, x_finish-box_w/2-4, mid_y-8)
    arrow(x_branch+box_w/2, bot_y, x_finish-box_w/2-4, mid_y+8)
    draw_box(x_finish, mid_y, "FINISH", "= ____")
    return _to_bytes(img)


def function_machine_blank(input_val=5, ops=None, mode="forward", **kw) -> BytesIO:
    """A chain of 'machine' boxes: INPUT -> [operation] -> [operation] ->
    OUTPUT. Forward mode shows the input, leaves output blank. Reverse
    mode shows the output, leaves input blank -- specifically targets
    the documented mistake where kids apply the same operation forward
    instead of undoing it."""
    if ops is None:
        ops = ["+ 3"]
    n = len(ops)
    box_w, box_h = 70, 50
    gap = 55
    w = box_w*2 + n*(box_w+gap) + gap + 20
    h = 90
    img, d = _blank(w, h)
    fnt = _font(14)
    fnt_s = _font_reg(12)
    mid_y = h/2

    def draw_box(cx, cy, top, bottom, double=False):
        if double:
            d.rectangle([cx-box_w/2-3, cy-box_h/2-3, cx+box_w/2+3, cy+box_h/2+3], outline=C_BORDER, width=2)
        d.rectangle([cx-box_w/2, cy-box_h/2, cx+box_w/2, cy+box_h/2], outline=C_BORDER, width=2)
        tw = d.textlength(top, font=fnt)
        d.text((cx-tw/2, cy-box_h/2+8), top, fill=C_BORDER, font=fnt)
        if bottom:
            tw2 = d.textlength(bottom, font=fnt_s)
            d.text((cx-tw2/2, cy+2), bottom, fill=C_BORDER, font=fnt_s)

    def arrow(x0, x1, y):
        d.line([x0, y, x1, y], fill=C_BORDER, width=2)
        d.polygon([(x1, y-5), (x1+8, y), (x1, y+5)], fill=C_BORDER)

    x = 30
    in_label = str(input_val) if mode == "forward" else "____"
    draw_box(x+box_w/2, mid_y, "IN", in_label)
    x += box_w
    for op in ops:
        arrow(x, x+gap-8, mid_y)
        x += gap
        draw_box(x+box_w/2, mid_y, "MACHINE", op, double=True)
        x += box_w
    arrow(x, x+gap-8, mid_y)
    x += gap
    out_label = "____" if mode == "forward" else str(input_val)
    draw_box(x+box_w/2, mid_y, "OUT", out_label)
    return _to_bytes(img)


def number_pyramid_blank(rows=4, given=None, **kw) -> BytesIO:
    """A triangular number pyramid: each brick = sum of the two bricks
    directly below it. Some bricks are pre-filled (given), the rest are
    blank for the child to work out."""
    if given is None:
        given = {}
    cell = 46
    w = rows * cell + 20
    h = rows * cell + 20
    img, d = _blank(w, h)
    fnt = _font(15)
    for r in range(rows):
        # row r (0 = top) has r+1 cells, centered
        n_cells = r + 1
        row_w = n_cells * cell
        x0 = (w - row_w) / 2
        y0 = 10 + r*cell
        for c in range(n_cells):
            cx0 = x0 + c*cell
            d.rectangle([cx0, y0, cx0+cell-4, y0+cell-4], outline=C_BORDER, width=2)
            val = given.get((r, c))
            if val is not None:
                txt = str(val)
                tw = d.textlength(txt, font=fnt)
                d.text((cx0+(cell-4)/2-tw/2, y0+(cell-4)/2-10), txt, fill=C_BORDER, font=fnt)
    return _to_bytes(img)


# ─── FACTOR TREE & VENN DIAGRAM (Level 9 additions) ────────────────────────────

def _is_prime_ft(x):
    if x < 2: return False
    for k in range(2, int(x**0.5) + 1):
        if x % k == 0: return False
    return True

def _smallest_factor(n):
    for p in range(2, int(n**0.5) + 1):
        if n % p == 0:
            return p, n // p
    return None, None

def factor_tree(n=60, **kw) -> BytesIO:
    """Draws a factor tree for n down to prime leaves, splitting off the
    smallest prime factor at each step (the standard way students draw it
    by hand)."""
    def build(n):
        if _is_prime_ft(n) or n < 2:
            return (n, None, None)
        p, rest = _smallest_factor(n)
        left = (p, None, None)
        right = build(rest)
        return (n, left, right)

    tree = build(n)

    def depth(node):
        if node[1] is None: return 1
        return 1 + max(depth(node[1]), depth(node[2]))
    d_levels = depth(tree)

    def leaves(node):
        if node[1] is None: return [node[0]]
        return leaves(node[1]) + leaves(node[2])
    prime_leaves = sorted(leaves(tree))

    w = max(500, 130 * (2 ** (d_levels - 1)))
    h = 110 * d_levels + 70
    img, dr = _blank(w, h)
    fnt = _font(15)
    radius = 24

    def draw(node, x, y, spread):
        val, l, r = node
        is_leaf = l is None
        color = C_RED if is_leaf else C_BLUE
        dr.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color, outline=C_BORDER, width=2)
        txt = str(val)
        tw = dr.textlength(txt, font=fnt)
        dr.text((x - tw/2, y - 9), txt, fill=C_TEXT, font=fnt)
        if not is_leaf:
            ny = y + 95
            lx, rx = x - spread, x + spread
            dr.line([x, y + radius, lx, ny - radius], fill=C_BORDER, width=2)
            dr.line([x, y + radius, rx, ny - radius], fill=C_BORDER, width=2)
            draw(l, lx, ny, spread / 2)
            draw(r, rx, ny, spread / 2)

    draw(tree, w // 2, 35, w // 4)
    caption = f"{n} = " + " x ".join(str(p) for p in prime_leaves)
    cw = dr.textlength(caption, font=_font(14))
    dr.text((w/2 - cw/2, h - 28), caption, fill=C_TEAL_D, font=_font(14))
    return _to_bytes(img)


def venn_two(a_only=None, common=None, b_only=None, label_a="A", label_b="B", **kw) -> BytesIO:
    """Two-circle Venn diagram for shared vs. unique prime factors --
    standard visual for building HCF/LCM intuition. a_only/common/b_only
    are lists of numbers (or strings) to place in each region."""
    a_only = a_only or []; common = common or []; b_only = b_only or []
    w, h = 560, 340
    img, dr = _blank(w, h)
    r = 130
    cx_a, cx_b, cy = w//2 - 70, w//2 + 70, 160
    fnt = _font_reg(13)
    fnt_lab = _font(15)

    dr.ellipse([cx_a - r, cy - r, cx_a + r, cy + r], outline=C_BLUE_D, width=3)
    dr.ellipse([cx_b - r, cy - r, cx_b + r, cy + r], outline=C_TEAL_D, width=3)

    la = f"{label_a} only"; lb = f"{label_b} only"
    dr.text((cx_a - r - 10, cy - r - 24), la, fill=C_BLUE_D, font=fnt_lab)
    dr.text((cx_b + r - dr.textlength(lb, font=fnt_lab) + 10, cy - r - 24), lb, fill=C_TEAL_D, font=fnt_lab)
    dr.text((w/2 - dr.textlength("common", font=fnt_lab)/2, cy + r + 6), "common", fill=C_BORDER, font=fnt_lab)

    def place_list(items, cx, cy_offset):
        text = ", ".join(str(x) for x in items) if items else "--"
        tw = dr.textlength(text, font=fnt)
        dr.text((cx - tw/2, cy + cy_offset), text, fill=C_TEXT, font=fnt)

    place_list(a_only, cx_a - 45, -8)
    place_list(common, w//2, -8)
    place_list(b_only, cx_b + 45, -8)
    return _to_bytes(img)




# ─── RATIO BAR & PROPORTION GRAPH (Level 10 additions) ─────────────────────────

def ratio_bar(parts=None, labels=None, **kw) -> BytesIO:
    """Horizontal bar split into segments proportional to a ratio (e.g.
    parts=[2,3] for a 2:3 ratio), each segment coloured and labelled."""
    parts = parts or [2, 3]
    labels = labels or [str(p) for p in parts]
    total = sum(parts) if sum(parts) else 1
    w, h = 560, 150
    img, dr = _blank(w, h)
    bar_w, bar_h = 480, 70
    x0 = (w - bar_w) // 2
    y0 = 30
    colors = [C_BLUE, C_TEAL, C_AMBER, C_RED, C_ACCENT]
    fnt = _font(14)
    x = x0
    for i, p in enumerate(parts):
        seg_w = bar_w * p / total
        color = colors[i % len(colors)]
        dr.rectangle([x, y0, x + seg_w, y0 + bar_h], fill=color, outline=C_BORDER, width=2)
        label = str(labels[i])
        tw = dr.textlength(label, font=fnt)
        if seg_w > tw + 6:
            dr.text((x + seg_w/2 - tw/2, y0 + bar_h/2 - 9), label, fill=C_TEXT, font=fnt)
        x += seg_w
    caption = ":".join(str(p) for p in parts) + f"  (total = {total} parts)"
    cw = dr.textlength(caption, font=_font_reg(13))
    dr.text((w/2 - cw/2, y0 + bar_h + 15), caption, fill=C_TEAL_D, font=_font_reg(13))
    return _to_bytes(img)


def proportion_graph(kind="direct", k=2, xmax=10, **kw) -> BytesIO:
    """Plots y=kx (direct -- straight line through origin) or y=k/x
    (inverse -- a curve), so the defining visual difference between the
    two is actually shown, not just described."""
    w, h = 400, 400
    img, dr = _blank(w, h)
    margin = 45
    plot_w, plot_h = w - 2*margin, h - 2*margin
    ox, oy = margin, h - margin
    dr.line([ox, margin, ox, oy], fill=C_BORDER, width=2)
    dr.line([ox, oy, w - margin, oy], fill=C_BORDER, width=2)
    fnt = _font_reg(12)
    dr.text((w - margin - 5, oy + 8), "x", fill=C_TEXT, font=fnt)
    dr.text((ox - 18, margin - 8), "y", fill=C_TEXT, font=fnt)

    xs = [x for x in range(1, xmax + 1)]
    if kind == "direct":
        ys = [k * x for x in xs]
    else:
        ys = [k / x for x in xs]
    ymax = max(ys) if ys else 1

    def to_px(x, y):
        return ox + (x / xmax) * plot_w, oy - (y / ymax) * plot_h

    pts = [to_px(x, y) for x, y in zip(xs, ys)]
    color = C_BLUE_D if kind == "direct" else C_RED_D
    for i in range(len(pts) - 1):
        dr.line([pts[i], pts[i + 1]], fill=color, width=3)
    for p in pts:
        dr.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=color)

    label = f"y = {k}x  (Direct Proportion)" if kind == "direct" else f"y = {k}/x  (Inverse Proportion)"
    lw = dr.textlength(label, font=_font(12))
    dr.text((w/2 - lw/2, 10), label, fill=color, font=_font(12))
    return _to_bytes(img)


DIAGRAM_FUNCTIONS = {
    "tenths_grid": tenths_grid,
    "hundredths_grid": hundredths_grid,
    "number_line": number_line,
    "integer_line": integer_line,
    "place_value_chart": place_value_chart,
    "fraction_bar": fraction_bar,
    "fraction_circle": fraction_circle,
    "dot_array": dot_array,
    "ten_frames": ten_frames,
    "array_diagram": array_diagram,
    "dot_addition": dot_addition,
    "labeled_rectangle": labeled_rectangle,
    "labeled_square": labeled_square,
    "labeled_triangle": labeled_triangle,
    "object_group": object_group,
    "object_compare": object_compare,
    "base10_blocks": base10_blocks,
    "visual_equation": visual_equation,
    "compare_choice": compare_choice,
    "number_card": number_card,
    "numline_jump": numline_jump,
    "instruction_icon": instruction_icon,
    "sequence_boxes": sequence_boxes,
    "compare_blocks": compare_blocks,
    "pair_grouping": pair_grouping,
    "array_grid": array_grid,
    "multiply_grid": multiply_grid,
    "repeated_groups": repeated_groups,
    "sharing_baskets": sharing_baskets,
    "division_bar_model": division_bar_model,
    "fraction_area_blank": fraction_area_blank,
    "fraction_area_example": fraction_area_example,
    "fraction_bar_blank": fraction_bar_blank,
    "fraction_bar_example": fraction_bar_example,
    "two_bars_blank": two_bars_blank,
    "two_bars_example": two_bars_example,
    "fraction_numberline_blank": fraction_numberline_blank,
    "fraction_numberline_example": fraction_numberline_example,
    "fraction_bar": fraction_bar,
    "hundredths_grid_blank": hundredths_grid_blank,
    "hundredths_grid_example": hundredths_grid_example,
    "decimal_place_blank": decimal_place_blank,
    "decimal_place_example": decimal_place_example,
    "decimal_numberline_blank": decimal_numberline_blank,
    "decimal_numberline_example": decimal_numberline_example,
    "regroup_ones_blank": regroup_ones_blank,
    "regroup_break_blank": regroup_break_blank,
    "number_bond_blank": number_bond_blank,
    "make_ten_frame_blank": make_ten_frame_blank,
    "equal_groups_blank": equal_groups_blank,
    "equal_groups_example": equal_groups_example,
    "array_blank": array_blank,
    "array_example": array_example,
    "division_box_blank": division_box_blank,
    "division_box_example": division_box_example,
    "integer_chips_blank": integer_chips_blank,
    "integer_chips_example": integer_chips_example,
    "vertical_numberline_blank": vertical_numberline_blank,
    "vertical_numberline_example": vertical_numberline_example,
    "magic_square_blank": magic_square_blank,
    "matching_vertical_blank": matching_vertical_blank,
    "matching_vertical_example": matching_vertical_example,
    "math_maze_blank": math_maze_blank,
    "function_machine_blank": function_machine_blank,
    "number_pyramid_blank": number_pyramid_blank,
    "mascot_splitter": mascot_splitter,
    "factor_groups_icon": factor_groups_icon,
    "factor_tree": factor_tree,
    "venn_two": venn_two,
    "ratio_bar": ratio_bar,
    "proportion_graph": proportion_graph,
}


# ─── SVG DIAGRAMS (Level 11 trial -- vector output for sharper print) ──────────

def algebra_tiles_svg(pos_x=0, pos_const=0, neg_x=0, neg_const=0, **kw):
    """Renders an algebraic expression as physical tiles: long rectangles
    for x-terms, small squares for constants. Blue = positive x, amber =
    positive unit, red = negative. Includes a built-in legend so the
    tiles are self-explanatory without relying on a separate worked
    example. Returns a raw SVG string."""
    tile_w, tile_h, unit, gap = 78, 34, 34, 12
    legend_h = 34
    x = 18
    y = 18 + legend_h + 12
    parts = []

    defs = '''<defs>
<linearGradient id="gBlue" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#EAF4FC"/><stop offset="1" stop-color="#BFDDF5"/>
</linearGradient>
<linearGradient id="gAmber" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#FFF8E1"/><stop offset="1" stop-color="#FCE7A6"/>
</linearGradient>
<linearGradient id="gRed" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#FDEDEB"/><stop offset="1" stop-color="#F5C2BA"/>
</linearGradient>
<filter id="tileShadow" x="-20%" y="-20%" width="140%" height="140%">
<feDropShadow dx="0" dy="1.5" stdDeviation="1.2" flood-color="#000000" flood-opacity="0.25"/>
</filter>
</defs>'''
    parts.append(defs)

    def add_x_tile(positive):
        nonlocal x
        grad, stroke, tcol, label = ("url(#gBlue)", "#1B5E8C", "#0C3A5C", "x") if positive else ("url(#gRed)", "#A6362B", "#6E1F18", "-x")
        parts.append(f'<rect x="{x}" y="{y}" width="{tile_w}" height="{tile_h}" rx="6" fill="{grad}" stroke="{stroke}" stroke-width="2" filter="url(#tileShadow)"/>')
        parts.append(f'<text x="{x+tile_w/2:.1f}" y="{y+tile_h/2+6:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="18" fill="{tcol}">{label}</text>')
        x += tile_w + gap

    def add_unit_tile(positive):
        nonlocal x
        grad, stroke, tcol, label = ("url(#gAmber)", "#9A7209", "#5c4708", "1") if positive else ("url(#gRed)", "#A6362B", "#6E1F18", "-1")
        parts.append(f'<rect x="{x}" y="{y}" width="{unit}" height="{unit}" rx="6" fill="{grad}" stroke="{stroke}" stroke-width="2" filter="url(#tileShadow)"/>')
        parts.append(f'<text x="{x+unit/2:.1f}" y="{y+unit/2+6:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="{tcol}">{label}</text>')
        x += unit + gap

    for _ in range(pos_x): add_x_tile(True)
    for _ in range(neg_x): add_x_tile(False)
    for _ in range(pos_const): add_unit_tile(True)
    for _ in range(neg_const): add_unit_tile(False)

    width = max(x + 12, 300)
    height = y + tile_h + 16

    # Legend, top-left: small sample tiles next to "= x" / "= 1" labels
    lx, ly = 18, 16
    legend = f'''
<rect x="{lx}" y="{ly}" width="30" height="16" rx="4" fill="url(#gBlue)" stroke="#1B5E8C" stroke-width="1.5"/>
<text x="{lx+37}" y="{ly+13}" font-family="Helvetica-Bold" font-size="13" fill="#0C3A5C">= x</text>
<rect x="{lx+95}" y="{ly}" width="16" height="16" rx="4" fill="url(#gAmber)" stroke="#9A7209" stroke-width="1.5"/>
<text x="{lx+119}" y="{ly+13}" font-family="Helvetica-Bold" font-size="13" fill="#5c4708">= 1</text>
<rect x="{lx+170}" y="{ly}" width="30" height="16" rx="4" fill="url(#gRed)" stroke="#A6362B" stroke-width="1.5"/>
<text x="{lx+207}" y="{ly+13}" font-family="Helvetica-Bold" font-size="13" fill="#6E1F18">= negative</text>
<line x1="{lx}" y1="{ly+legend_h-8}" x2="{width-18}" y2="{ly+legend_h-8}" stroke="#D5D8DC" stroke-width="1"/>'''
    parts.insert(1, legend)

    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">' + "".join(parts) + "</svg>"


def balance_scale_svg(left_text="x + 3", right_text="7", w=380, **kw):
    """Renders a balance scale in equilibrium with the two sides of an
    equation on each pan -- the standard visual for equation solving.
    Returns a raw SVG string."""
    h = 220
    cx = w / 2
    beam_y = 64
    left_x, right_x = 68, w - 68
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
<linearGradient id="gPanL" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#EAF4FC"/><stop offset="1" stop-color="#BFDDF5"/>
</linearGradient>
<linearGradient id="gPanR" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#E7F8ED"/><stop offset="1" stop-color="#B7E8C7"/>
</linearGradient>
<linearGradient id="gBase" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#F7F8F9"/><stop offset="1" stop-color="#D6D9DC"/>
</linearGradient>
<filter id="panShadow" x="-30%" y="-30%" width="160%" height="160%">
<feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-color="#000000" flood-opacity="0.28"/>
</filter>
</defs>
<line x1="{cx}" y1="{beam_y+42}" x2="{cx}" y2="{h-24}" stroke="#2C3E50" stroke-width="5"/>
<polygon points="{cx-74},{h-24} {cx+74},{h-24} {cx+54},{h-6} {cx-54},{h-6}" fill="url(#gBase)" stroke="#2C3E50" stroke-width="2"/>
<polygon points="{cx-22},{beam_y+42} {cx+22},{beam_y+42} {cx},{beam_y}" fill="url(#gBase)" stroke="#2C3E50" stroke-width="2"/>
<line x1="{left_x}" y1="{beam_y}" x2="{right_x}" y2="{beam_y}" stroke="#2C3E50" stroke-width="4" stroke-linecap="round"/>
<circle cx="{cx}" cy="{beam_y}" r="5" fill="#2C3E50"/>
<line x1="{left_x}" y1="{beam_y}" x2="{left_x}" y2="{beam_y+52}" stroke="#2C3E50" stroke-width="2"/>
<polygon points="{left_x-48},{beam_y+52} {left_x+48},{beam_y+52} {left_x+34},{beam_y+86} {left_x-34},{beam_y+86}" fill="url(#gPanL)" stroke="#1B5E8C" stroke-width="2" filter="url(#panShadow)"/>
<text x="{left_x}" y="{beam_y+74}" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#0C3A5C">{left_text}</text>
<line x1="{right_x}" y1="{beam_y}" x2="{right_x}" y2="{beam_y+52}" stroke="#2C3E50" stroke-width="2"/>
<polygon points="{right_x-48},{beam_y+52} {right_x+48},{beam_y+52} {right_x+34},{beam_y+86} {right_x-34},{beam_y+86}" fill="url(#gPanR)" stroke="#1E7A44" stroke-width="2" filter="url(#panShadow)"/>
<text x="{right_x}" y="{beam_y+74}" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#0B4F30">{right_text}</text>
<text x="{cx}" y="18" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#5D6D7E">Both sides are EQUAL</text>
</svg>'''


def term_label_svg(coefficient=5, variable="x", exponent=None, **kw):
    """Breaks a term like '5x' or '5x^2' into its parts, with a labelled
    connector under each piece: Coefficient / Variable / Exponent."""
    fs = 34
    char_w = fs * 0.62
    inter_part_gap = 60
    coef_str = str(coefficient)
    var_str = str(variable)
    exp_str = str(exponent) if exponent not in (None, "") else None
    coef_w = char_w * len(coef_str)
    var_w = char_w * len(var_str)
    exp_w = char_w * len(exp_str) * 0.6 if exp_str else 0

    x0 = 30
    y_term = 68
    width = max(coef_w + inter_part_gap + var_w + inter_part_gap + exp_w + 60, 300)
    height = 150

    parts = []
    cx = x0
    parts.append(f'<text x="{cx}" y="{y_term}" font-family="Helvetica-Bold" font-size="{fs}" fill="#1B5E8C">{coef_str}</text>')
    coef_mid = cx + coef_w / 2
    cx += coef_w + inter_part_gap
    parts.append(f'<text x="{cx}" y="{y_term}" font-family="Helvetica-Bold" font-size="{fs}" fill="#1E7A44">{var_str}</text>')
    var_mid = cx + var_w / 2
    cx += var_w + inter_part_gap
    exp_mid = None
    if exp_str:
        parts.append(f'<text x="{cx}" y="{y_term-16}" font-family="Helvetica-Bold" font-size="{fs*0.6:.0f}" fill="#A6362B">{exp_str}</text>')
        exp_mid = cx + exp_w / 2

    label_y = y_term + 46

    def add_label(mid_x, text, color):
        parts.append(f'<line x1="{mid_x}" y1="{y_term+12}" x2="{mid_x}" y2="{label_y-16}" stroke="{color}" stroke-width="1.5" stroke-dasharray="3,2"/>')
        tw = len(text) * 6.8
        parts.append(f'<rect x="{mid_x-tw/2-7}" y="{label_y-16}" width="{tw+14}" height="22" rx="11" fill="{color}" fill-opacity="0.13" stroke="{color}" stroke-width="1.3"/>')
        parts.append(f'<text x="{mid_x}" y="{label_y-1}" text-anchor="middle" font-family="Helvetica-Bold" font-size="11.5" fill="{color}">{text}</text>')

    add_label(coef_mid, "Coefficient", "#1B5E8C")
    add_label(var_mid, "Variable", "#1E7A44")
    if exp_mid is not None:
        add_label(exp_mid, "Exponent", "#A6362B")

    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">' + "".join(parts) + "</svg>"


def like_terms_sort_svg(groups=None, **kw):
    """Sorts a set of terms into labelled, colour-coded groups (e.g.
    x-terms, y-terms, constants) inside dashed boundary boxes -- the
    visual for 'collecting like terms'."""
    groups = groups or {"x-terms": ["3x", "2x"], "constants": ["5", "1"]}
    palette = [("#1B5E8C", "#EAF4FC"), ("#1E7A44", "#E7F8ED"), ("#A6362B", "#FDEDEB"), ("#7D3C98", "#F3E9F8")]
    card_w, card_h, gap, pad, group_gap = 54, 34, 10, 18, 30
    x = 16
    y_top = 42
    parts = []
    for gi, (label, terms) in enumerate(groups.items()):
        color, fill = palette[gi % len(palette)]
        group_w = max(len(terms) * (card_w + gap) - gap, card_w) + 2 * pad
        parts.append(f'<rect x="{x}" y="{y_top}" width="{group_w}" height="{card_h+2*pad}" rx="14" fill="{fill}" stroke="{color}" stroke-width="2" stroke-dasharray="6,3"/>')
        parts.append(f'<text x="{x+group_w/2}" y="{y_top-10}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="{color}">{label}</text>')
        tx, ty = x + pad, y_top + pad
        for term in terms:
            parts.append(f'<rect x="{tx}" y="{ty}" width="{card_w}" height="{card_h}" rx="8" fill="white" stroke="{color}" stroke-width="1.8"/>')
            parts.append(f'<text x="{tx+card_w/2}" y="{ty+card_h/2+5}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="{color}">{term}</text>')
            tx += card_w + gap
        x += group_w + group_gap
    width = x - group_gap + 16
    height = y_top + card_h + 2 * pad + 16
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">' + "".join(parts) + "</svg>"


def function_machine_svg(input_val=3, expression="x + 5", output_val=8, **kw):
    """Input -> RULE machine -> Output, for substitution/evaluation.
    Pass output_val=None to leave the output blank (student solves it)."""
    w, h = 420, 160
    out_label = str(output_val) if output_val is not None else "?"
    parts = []
    parts.append('<circle cx="50" cy="80" r="34" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<text x="50" y="87" text-anchor="middle" font-family="Helvetica-Bold" font-size="20" fill="#0C3A5C">{input_val}</text>')
    parts.append('<text x="50" y="128" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#5D6D7E">INPUT (x)</text>')
    parts.append('<line x1="90" y1="80" x2="136" y2="80" stroke="#2C3E50" stroke-width="2.5"/>')
    parts.append('<polygon points="136,80 124,73 124,87" fill="#2C3E50"/>')
    parts.append('<rect x="145" y="45" width="130" height="70" rx="10" fill="#FFF8E1" stroke="#9A7209" stroke-width="2.5"/>')
    parts.append(f'<text x="210" y="87" text-anchor="middle" font-family="Helvetica-Bold" font-size="18" fill="#5c4708">{expression}</text>')
    parts.append('<text x="210" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#5D6D7E">RULE</text>')
    parts.append('<line x1="280" y1="80" x2="326" y2="80" stroke="#2C3E50" stroke-width="2.5"/>')
    parts.append('<polygon points="326,80 314,73 314,87" fill="#2C3E50"/>')
    parts.append('<circle cx="370" cy="80" r="34" fill="#E7F8ED" stroke="#1E7A44" stroke-width="2.5"/>')
    parts.append(f'<text x="370" y="87" text-anchor="middle" font-family="Helvetica-Bold" font-size="20" fill="#0B4F30">{out_label}</text>')
    parts.append('<text x="370" y="128" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#5D6D7E">OUTPUT</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def substitution_steps_svg(steps=None, **kw):
    """A vertical chain of boxes showing a substitution worked step by
    step, e.g. '2x+1' -> '2(3)+1' -> '6+1' -> '7', the last box
    highlighted as the final answer."""
    steps = steps or ["2x + 1", "2(3) + 1", "6 + 1", "7"]
    w, box_h, gap = 260, 40, 24
    h = len(steps) * (box_h + gap) - gap + 26
    parts = []
    y = 14
    for i, s in enumerate(steps):
        is_last = (i == len(steps) - 1)
        fill, stroke, tcol = ("#E7F8ED", "#1E7A44", "#0B4F30") if is_last else ("#EAF4FC", "#1B5E8C", "#0C3A5C")
        parts.append(f'<rect x="20" y="{y}" width="{w-40}" height="{box_h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        parts.append(f'<text x="{w/2}" y="{y+box_h/2+6}" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="{tcol}">{s}</text>')
        if not is_last:
            ay = y + box_h
            parts.append(f'<line x1="{w/2}" y1="{ay+3}" x2="{w/2}" y2="{ay+gap-7}" stroke="#2C3E50" stroke-width="2"/>')
            parts.append(f'<polygon points="{w/2},{ay+gap-2} {w/2-6},{ay+gap-11} {w/2+6},{ay+gap-11}" fill="#2C3E50"/>')
        y += box_h + gap
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def repeated_addition_svg(coefficient=3, variable="x", **kw):
    """Shows a term like '3x' as repeated addition: x + x + x -- builds
    the intuition for what a coefficient means."""
    box_w, box_h, gap = 50, 42, 16
    x, y = 16, 36
    parts = []
    for i in range(max(coefficient, 1)):
        parts.append(f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="8" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2"/>')
        parts.append(f'<text x="{x+box_w/2}" y="{y+box_h/2+6}" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#0C3A5C">{variable}</text>')
        x += box_w
        if i < coefficient - 1:
            parts.append(f'<text x="{x+gap/2}" y="{y+box_h/2+7}" text-anchor="middle" font-family="Helvetica-Bold" font-size="19" fill="#2C3E50">+</text>')
            x += gap
    width = x + 16
    height = y + box_h + 46
    cap = f"{coefficient}{variable}  =  " + " + ".join([variable] * coefficient)
    parts.append(f'<text x="{width/2}" y="{height-14}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#5D6D7E">{cap}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">' + "".join(parts) + "</svg>"


def _fmt_term(coef, var):
    """Formats a coefficient*variable term with correct sign, e.g. -1x -> '-x'."""
    if coef == 1:
        return f"+ {var}"
    if coef == -1:
        return f"- {var}"
    if coef >= 0:
        return f"+ {coef}{var}"
    return f"- {abs(coef)}{var}"


def _fmt_equation(a, b, c):
    """Formats ax + by = c as readable text, e.g. (2,-3,6) -> '2x - 3y = 6'."""
    parts = []
    parts.append(f"{a}x" if a != 1 else "x")
    parts.append(_fmt_term(b, "y"))
    return " ".join(parts) + f" = {c}"


def _line_points(a, b, c, rng):
    """Returns two endpoint (x,y) pairs where the line ax+by=c crosses the
    boundary of a [-rng,rng] x [-rng,rng] box, for drawing purposes."""
    candidates = []
    if b != 0:
        for xv in (-rng, rng):
            yv = (c - a * xv) / b
            if -rng - 1e-9 <= yv <= rng + 1e-9:
                candidates.append((xv, yv))
    if a != 0:
        for yv in (-rng, rng):
            xv = (c - b * yv) / a
            if -rng - 1e-9 <= xv <= rng + 1e-9:
                candidates.append((xv, yv))
    uniq = []
    for p in candidates:
        if not any(abs(p[0]-u[0]) < 1e-6 and abs(p[1]-u[1]) < 1e-6 for u in uniq):
            uniq.append(p)
    if len(uniq) < 2:
        return None
    uniq.sort()
    return uniq[0], uniq[-1]


def _grid_svg_base(rng=10, size=340, margin=36):
    """Builds the shared axes/gridlines for a coordinate-plane SVG.
    Returns (parts_list, to_px_function)."""
    def to_px(x, y):
        plot = size - 2 * margin
        px = margin + (x + rng) / (2 * rng) * plot
        py = size - margin - (y + rng) / (2 * rng) * plot
        return px, py

    parts = []
    for i in range(-rng, rng + 1, 2):
        if i == 0: continue
        gx, _ = to_px(i, 0)
        _, gy = to_px(0, i)
        parts.append(f'<line x1="{gx:.1f}" y1="{margin}" x2="{gx:.1f}" y2="{size-margin}" stroke="#EEF1F3" stroke-width="1"/>')
        parts.append(f'<line x1="{margin}" y1="{gy:.1f}" x2="{size-margin}" y2="{gy:.1f}" stroke="#EEF1F3" stroke-width="1"/>')
    ox, oy = to_px(0, 0)
    parts.append(f'<line x1="{margin}" y1="{oy:.1f}" x2="{size-margin}" y2="{oy:.1f}" stroke="#2C3E50" stroke-width="2"/>')
    parts.append(f'<line x1="{ox:.1f}" y1="{margin}" x2="{ox:.1f}" y2="{size-margin}" stroke="#2C3E50" stroke-width="2"/>')
    parts.append(f'<text x="{size-margin+10}" y="{oy+4:.1f}" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">x</text>')
    parts.append(f'<text x="{ox-6:.1f}" y="{margin+2}" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">y</text>')
    return parts, to_px


def linear_equation_graph_svg(a=1, b=1, c=6, rng=10, **kw):
    """Plots the single line ax+by=c on a coordinate grid, marking its
    x- and y-intercepts. The core visual for graphing linear equations."""
    size = 340
    parts, to_px = _grid_svg_base(rng, size)
    pts = _line_points(a, b, c, rng)
    if pts:
        (x1, y1), (x2, y2) = pts
        px1, py1 = to_px(x1, y1)
        px2, py2 = to_px(x2, y2)
        parts.append(f'<line x1="{px1:.1f}" y1="{py1:.1f}" x2="{px2:.1f}" y2="{py2:.1f}" stroke="#1B5E8C" stroke-width="3"/>')
    if a != 0:
        xi = c / a
        if -rng <= xi <= rng:
            px, py = to_px(xi, 0)
            parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#A6362B"/>')
            xi_lbl = int(xi) if xi == int(xi) else round(xi, 1)
            parts.append(f'<text x="{px+7:.1f}" y="{py-7:.1f}" font-family="Helvetica-Bold" font-size="11" fill="#A6362B">({xi_lbl},0)</text>')
    if b != 0:
        yi = c / b
        if -rng <= yi <= rng:
            px, py = to_px(0, yi)
            parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#1E7A44"/>')
            yi_lbl = int(yi) if yi == int(yi) else round(yi, 1)
            parts.append(f'<text x="{px+7:.1f}" y="{py-7:.1f}" font-family="Helvetica-Bold" font-size="11" fill="#1E7A44">(0,{yi_lbl})</text>')
    eqn = _fmt_equation(a, b, c)
    parts.insert(0, f'<text x="{size/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#2C3E50">{eqn}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"


def two_line_graph_svg(a1=1, b1=1, c1=6, a2=1, b2=-1, c2=2, rng=10, **kw):
    """Plots two lines on one grid and marks their intersection, or notes
    if they're parallel/coincident -- the visual for the graphical method
    and for consistent/inconsistent/dependent systems."""
    size = 360
    parts, to_px = _grid_svg_base(rng, size)
    for (a, b, c, color) in [(a1, b1, c1, "#1B5E8C"), (a2, b2, c2, "#1E7A44")]:
        pts = _line_points(a, b, c, rng)
        if pts:
            (x1, y1), (x2, y2) = pts
            px1, py1 = to_px(x1, y1)
            px2, py2 = to_px(x2, y2)
            parts.append(f'<line x1="{px1:.1f}" y1="{py1:.1f}" x2="{px2:.1f}" y2="{py2:.1f}" stroke="{color}" stroke-width="3"/>')

    det = a1 * b2 - a2 * b1
    status_text = ""
    if det != 0:
        xi = (c1 * b2 - c2 * b1) / det
        yi = (a1 * c2 - a2 * c1) / det
        if -rng <= xi <= rng and -rng <= yi <= rng:
            px, py = to_px(xi, yi)
            parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="#A6362B" stroke="white" stroke-width="1.5"/>')
            xi_lbl = int(xi) if xi == int(xi) else round(xi, 2)
            yi_lbl = int(yi) if yi == int(yi) else round(yi, 2)
            parts.append(f'<text x="{px+8:.1f}" y="{py-8:.1f}" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">({xi_lbl},{yi_lbl})</text>')
        status_text = "Intersecting -- ONE solution"
    else:
        prop_c = (a1 * c2 == a2 * c1) and (b1 * c2 == b2 * c1)
        status_text = "Coincident -- INFINITE solutions" if prop_c else "Parallel -- NO solution"

    eqn1 = _fmt_equation(a1, b1, c1)
    eqn2 = _fmt_equation(a2, b2, c2)
    parts.insert(0, f'<text x="{size/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{eqn1}   and   {eqn2}</text>')
    parts.append(f'<text x="{size/2}" y="{size-8}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#5D6D7E">{status_text}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"


def _svg_power_label(x, y, exp, font_size=13, color="#000", weight="Helvetica-Bold", anchor="end"):
    """Returns SVG for '10^exp' with a TRUE raised, smaller exponent --
    built from two ordinary text elements rather than unicode superscript
    characters, which don't reliably render via svglib's font handling
    (they showed as missing-glyph boxes when tested)."""
    base_str = "10"
    exp_str = str(exp)
    sup_size = font_size * 0.66
    sup_dy = -font_size * 0.42
    base_w = len(base_str) * font_size * 0.62
    exp_w = len(exp_str) * sup_size * 0.64
    if anchor == "end":
        bx = x - base_w - exp_w
    else:
        bx = x
    out = f'<text x="{bx:.1f}" y="{y}" font-family="{weight}" font-size="{font_size}" fill="{color}">{base_str}</text>'
    out += f'<text x="{bx+base_w:.1f}" y="{y+sup_dy:.1f}" font-family="{weight}" font-size="{sup_size:.1f}" fill="{color}">{exp_str}</text>'
    return out


def powers_of_ten_scale_svg(lo=-8, hi=8, highlight=None, **kw):
    """A two-column 'order of magnitude' scale from 10^hi down to 10^lo
    metres, with real-world reference objects marked -- makes abstract
    exponents like 10⁻⁶ vs 10⁸ viscerally comparable. Two columns use
    the worksheet box's width and height far more evenly than a single
    long vertical list, giving each row more room."""
    references = [
        (-9, "DNA width"), (-7, "Virus"), (-6, "Bacterium"),
        (-3, "Grain of sand"), (-2, "Ant"), (0, "Human height"),
        (2, "Football field"), (4, "Mt. Everest"), (7, "Earth's diameter"),
        (8, "10x Earth"),
    ]
    ref_map = {e: lbl for e, lbl in references if lo <= e <= hi}
    exps = list(range(hi, lo - 1, -1))
    n = len(exps)
    half = (n + 1) // 2
    col1, col2 = exps[:half], exps[half:]

    row_h = 32
    margin_left = 54
    label_w = 118
    col_w = margin_left + 20 + label_w
    inter_col_gap = 24
    top_margin = 24
    max_rows = max(len(col1), len(col2), 1)
    h = top_margin + max_rows * row_h + 14
    w = col_w * (2 if col2 else 1) + (inter_col_gap if col2 else 0)

    parts = []
    weight = "Helvetica-Bold"

    def draw_column(exps_list, x0):
        y = top_margin
        for exp in exps_list:
            label = ref_map.get(exp)
            is_hi = (highlight == exp)
            color = "#A6362B" if is_hi else ("#1B5E8C" if label else "#95A5A6")
            lx = x0 + margin_left
            parts.append(f'<line x1="{lx}" y1="{y}" x2="{x0+col_w-10}" y2="{y}" stroke="#EEF1F3" stroke-width="1"/>')
            parts.append(_svg_power_label(lx - 8, y + 5, exp, font_size=13, color=color))
            if label:
                parts.append(f'<circle cx="{lx+13}" cy="{y}" r="4.5" fill="{color}"/>')
                parts.append(f'<text x="{lx+24}" y="{y+5}" font-family="{weight}" font-size="12" fill="{color}">{label}</text>')
            elif is_hi:
                parts.append(f'<circle cx="{lx+13}" cy="{y}" r="4.5" fill="{color}"/>')
            y += row_h

    draw_column(col1, 0)
    if col2:
        draw_column(col2, col_w + inter_col_gap)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def exponential_growth_svg(start=1, factor=2, steps=5, mode="growth", **kw):
    """A sequence of bars, each scaled by 'factor' from the last (growth:
    multiply, decay: divide), so the explosive/vanishing effect of
    repeated multiplication is actually visible, not just stated."""
    values = [start]
    for _ in range(steps - 1):
        values.append(values[-1] * factor if mode == "growth" else values[-1] / factor)
    max_val = max(values) if max(values) > 0 else 1
    w = max(520, steps * 95)
    h = 260
    margin = 44
    bar_w = 50
    gap = (w - 2 * margin - steps * bar_w) / max(steps - 1, 1)
    max_bar_h = h - margin - 56
    parts = []
    x = margin
    color = "#1B5E8C" if mode == "growth" else "#A6362B"
    fillc = "#EAF4FC" if mode == "growth" else "#FDEDEB"
    for i, v in enumerate(values):
        bar_h = max(max_bar_h * (v / max_val), 3)
        y = h - margin - bar_h
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w}" height="{bar_h:.1f}" fill="{fillc}" stroke="{color}" stroke-width="2"/>')
        vlabel = int(v) if float(v).is_integer() else round(v, 3)
        parts.append(f'<text x="{x+bar_w/2:.1f}" y="{y-8:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="{color}">{vlabel:g}</text>')
        parts.append(f'<text x="{x+bar_w/2:.1f}" y="{h-margin+18:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#5D6D7E">step {i}</text>')
        x += bar_w + gap
    title = f"{'Growth' if mode=='growth' else 'Decay'}: {'x' if mode=='growth' else chr(247)}{factor} each step"
    parts.insert(0, f'<text x="{w/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{title}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def _poly_term_str(coef, power, var="x"):
    """Formats coef*var^power as readable text, e.g. (3,1,'x')->'3x',
    (-1,2,'x')->'-x²', (1,3,'x')->'x³', (0,anything)->'0', (5,0)->'5'.
    Uses the Latin-1 superscript characters ²/³ (confirmed to render
    correctly via svglib, unlike the general Unicode superscript block
    which renders as missing-glyph boxes) for powers 2-3; higher powers
    fall back to a caret since they're not needed at this level."""
    if coef == 0:
        return "0"
    sign = "-" if coef < 0 else ""
    mag = abs(coef)
    if power == 0:
        return f"{sign}{mag}"
    coefstr = "" if mag == 1 else str(mag)
    if power == 1:
        varstr = var
    elif power == 2:
        varstr = f"{var}²"
    elif power == 3:
        varstr = f"{var}³"
    else:
        varstr = f"{var}^{power}"
    return f"{sign}{coefstr}{varstr}"


def area_model_svg(a=1, b=3, c=1, d=2, var="x", **kw):
    """(ax+b)(cx+d) shown as a 4-region area-model rectangle -- the
    standard visual for binomial multiplication (FOIL made concrete)."""
    col_labels = [_poly_term_str(a, 1, var), (f"+{b}" if b >= 0 else f"-{abs(b)}")]
    row_labels = [_poly_term_str(c, 1, var), (f"+{d}" if d >= 0 else f"-{abs(d)}")]
    cells = [
        [_poly_term_str(a * c, 2, var), _poly_term_str(a * d, 1, var)],
        [_poly_term_str(b * c, 1, var), _poly_term_str(b * d, 0, var)],
    ]
    cell_w, cell_h = 92, 62
    x0, y0 = 56, 46
    w = x0 + 2 * cell_w + 20
    h = y0 + 2 * cell_h + 44
    parts = []
    expr = f"({_poly_term_str(a,1,var)}{'+' if b>=0 else '-'}{abs(b)})({_poly_term_str(c,1,var)}{'+' if d>=0 else '-'}{abs(d)})"
    parts.append(f'<text x="{w/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">{expr}</text>')
    for j, lbl in enumerate(col_labels):
        cx = x0 + j * cell_w + cell_w / 2
        parts.append(f'<text x="{cx:.1f}" y="{y0-12}" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#1B5E8C">{lbl}</text>')
    for i, lbl in enumerate(row_labels):
        cy = y0 + i * cell_h + cell_h / 2
        parts.append(f'<text x="{x0-12:.1f}" y="{cy+5:.1f}" text-anchor="end" font-family="Helvetica-Bold" font-size="16" fill="#1E7A44">{lbl}</text>')
    bgs = ["#EAF4FC", "#FFF8E1", "#FFF8E1", "#E7F8ED"]
    for i in range(2):
        for j in range(2):
            cx, cy = x0 + j * cell_w, y0 + i * cell_h
            parts.append(f'<rect x="{cx}" y="{cy}" width="{cell_w}" height="{cell_h}" fill="{bgs[i*2+j]}" stroke="#2C3E50" stroke-width="1.5"/>')
            parts.append(f'<text x="{cx+cell_w/2:.1f}" y="{cy+cell_h/2+6:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">{cells[i][j]}</text>')
    parts.append(f'<text x="{w/2}" y="{y0+2*cell_h+24}" text-anchor="middle" font-family="Helvetica-Oblique" font-size="11" fill="#5D6D7E">Add all 4 areas together</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def polynomial_graph_svg(coeffs=None, xrange=6, **kw):
    """Plots y=p(x) for a polynomial (coeffs = highest degree first, e.g.
    [1,-5,6] for x²-5x+6), marking the real zeroes (x-intercepts) found
    within the visible range -- the geometric meaning of a zero."""
    coeffs = coeffs or [1, -5, 6]

    def evaluate(x):
        y = 0
        for c in coeffs:
            y = y * x + c
        return y

    n_pts = 100
    xs = [-xrange + i * (2 * xrange) / n_pts for i in range(n_pts + 1)]
    ys = [evaluate(x) for x in xs]
    yr = max(1.0, min(max(abs(min(ys)), abs(max(ys))), xrange * 5))

    size = 340
    margin = 36

    def to_px(x, y):
        yc = max(-yr, min(yr, y))
        px = margin + (x + xrange) / (2 * xrange) * (size - 2 * margin)
        py = size - margin - (yc + yr) / (2 * yr) * (size - 2 * margin)
        return px, py

    parts = []
    for i in range(-int(xrange), int(xrange) + 1, 2):
        if i == 0: continue
        gx, _ = to_px(i, 0)
        parts.append(f'<line x1="{gx:.1f}" y1="{margin}" x2="{gx:.1f}" y2="{size-margin}" stroke="#F2F3F4" stroke-width="1"/>')
    ox, oy = to_px(0, 0)
    parts.append(f'<line x1="{margin}" y1="{oy:.1f}" x2="{size-margin}" y2="{oy:.1f}" stroke="#2C3E50" stroke-width="2"/>')
    parts.append(f'<line x1="{ox:.1f}" y1="{margin}" x2="{ox:.1f}" y2="{size-margin}" stroke="#2C3E50" stroke-width="2"/>')
    parts.append(f'<text x="{size-margin+8}" y="{oy+4:.1f}" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">x</text>')
    parts.append(f'<text x="{ox-6:.1f}" y="{margin+2}" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">y</text>')

    pts = [to_px(x, y) for x, y in zip(xs, ys)]
    path_d = "M " + " L ".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    parts.append(f'<path d="{path_d}" stroke="#1B5E8C" stroke-width="2.5" fill="none"/>')

    zeroes = []
    for i in range(len(xs) - 1):
        if abs(ys[i]) < 1e-9:
            zeroes.append(xs[i])
        elif ys[i] * ys[i + 1] < 0:
            zx = xs[i] - ys[i] * (xs[i + 1] - xs[i]) / (ys[i + 1] - ys[i])
            zeroes.append(zx)
    for zx in zeroes:
        px, py = to_px(zx, 0)
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="#A6362B"/>')
        zx_lbl = round(zx, 1)
        zx_lbl = int(zx_lbl) if zx_lbl == int(zx_lbl) else zx_lbl
        parts.append(f'<text x="{px:.1f}" y="{py+18:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#A6362B">{zx_lbl}</text>')

    terms = [_poly_term_str(c, len(coeffs) - 1 - i, "x") for i, c in enumerate(coeffs) if c != 0]
    eqn = "y = " + " + ".join(terms).replace("+ -", "- ")
    parts.insert(0, f'<text x="{size/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{eqn}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"


SVG_DIAGRAM_FUNCTIONS = {
    "algebra_tiles": algebra_tiles_svg,
    "balance_scale": balance_scale_svg,
    "term_label": term_label_svg,
    "like_terms_sort": like_terms_sort_svg,
    "function_machine_svg": function_machine_svg,
    "substitution_steps": substitution_steps_svg,
    "repeated_addition": repeated_addition_svg,
    "linear_equation_graph": linear_equation_graph_svg,
    "two_line_graph": two_line_graph_svg,
    "powers_of_ten_scale": powers_of_ten_scale_svg,
    "exponential_growth": exponential_growth_svg,
    "area_model": area_model_svg,
    "polynomial_graph": polynomial_graph_svg,
}


def generate_svg_diagram(diagram_type: str, params: dict) -> str | None:
    """Returns a raw SVG string for vector-based diagram types, or None if
    diagram_type isn't one of them. Used by pdf_engine to distinguish SVG
    diagrams (rendered via svglib as true vector PDF content) from the
    PNG raster diagrams above."""
    fn = SVG_DIAGRAM_FUNCTIONS.get(diagram_type)
    if fn is None:
        return None
    try:
        return fn(**params)
    except Exception as e:
        print(f"SVG diagram error [{diagram_type}]: {e}")
        return None

def generate_diagram(diagram_type: str, params: dict) -> BytesIO | None:
    """Main entry point. Returns BytesIO PNG or None if type unknown."""
    fn = DIAGRAM_FUNCTIONS.get(diagram_type)
    if fn is None:
        return None
    try:
        return fn(**params)
    except Exception as e:
        print(f"Diagram error [{diagram_type}]: {e}")
        return None
