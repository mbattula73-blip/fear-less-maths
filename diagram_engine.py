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


def mixed_number_area_blank(w1=1, n1=1, d1=2, w2=2, n2=1, d2=3, **kw) -> BytesIO:
    """Blank 2x2 area grid for multiplying two MIXED numbers:
    (w1 n1/d1) x (w2 n2/d2). Row/column headers show the whole and
    fractional parts; the four cells are left empty for the student to
    compute each partial product themselves (whole x whole, whole x
    fraction, fraction x whole, fraction x fraction), then add them up."""
    cell_w, cell_h = 100, 80
    x0, y0 = 90, 50
    w, h = x0 + 2*cell_w + 20, y0 + 2*cell_h + 20
    img, d = _blank(w, h)
    fnt = _font(14)
    fnt_s = _font_reg(11)
    col_labels = [str(w1), f"{n1}/{d1}"]
    row_labels = [str(w2), f"{n2}/{d2}"]
    for i in range(3):
        x = x0 + i*cell_w
        d.line([x, y0, x, y0+2*cell_h], fill=C_BORDER, width=2)
    for j in range(3):
        y = y0 + j*cell_h
        d.line([x0, y, x0+2*cell_w, y], fill=C_BORDER, width=2)
    for i, lbl in enumerate(col_labels):
        tw = d.textlength(lbl, font=fnt)
        d.text((x0 + i*cell_w + cell_w/2 - tw/2, y0 - 26), lbl, fill=C_BLUE_D, font=fnt)
    for j, lbl in enumerate(row_labels):
        tw = d.textlength(lbl, font=fnt)
        d.text((x0 - 20 - tw, y0 + j*cell_h + cell_h/2 - 8), lbl, fill=C_TEAL_D, font=fnt)
    d.text((6, 6), "x", fill=C_BORDER, font=fnt_s)
    return _to_bytes(img)


def mixed_number_area_example(w1=1, n1=1, d1=2, w2=2, n2=1, d2=3, **kw) -> BytesIO:
    """Worked example: the same 2x2 grid, with each of the 4 partial
    products filled in, plus the final sum written below."""
    cell_w, cell_h = 100, 80
    x0, y0 = 90, 50
    w, h = x0 + 2*cell_w + 20, y0 + 2*cell_h + 46
    img, d = _blank(w, h)
    fnt = _font(14)
    fnt_c = _font(13)
    col_labels = [str(w1), f"{n1}/{d1}"]
    row_labels = [str(w2), f"{n2}/{d2}"]
    cells = [
        [f"{w1*w2}", f"{w1*n2}/{d2}"],
        [f"{n1*w2}/{d1}", f"{n1*n2}/{d1*d2}"],
    ]
    for i in range(3):
        x = x0 + i*cell_w
        d.line([x, y0, x, y0+2*cell_h], fill=C_BORDER, width=2)
    for j in range(3):
        y = y0 + j*cell_h
        d.line([x0, y, x0+2*cell_w, y], fill=C_BORDER, width=2)
    for i, lbl in enumerate(col_labels):
        tw = d.textlength(lbl, font=fnt)
        d.text((x0 + i*cell_w + cell_w/2 - tw/2, y0 - 26), lbl, fill=C_BLUE_D, font=fnt)
    for j, lbl in enumerate(row_labels):
        tw = d.textlength(lbl, font=fnt)
        d.text((x0 - 20 - tw, y0 + j*cell_h + cell_h/2 - 8), lbl, fill=C_TEAL_D, font=fnt)
    for j in range(2):
        for i in range(2):
            lbl = cells[j][i]
            tw = d.textlength(lbl, font=fnt_c)
            d.text((x0 + i*cell_w + cell_w/2 - tw/2, y0 + j*cell_h + cell_h/2 - 8), lbl, fill=C_TEXT, font=fnt_c)
    d.text((10, y0 + 2*cell_h + 14), "Add all 4 pieces together for the total", fill=C_GRAY_D, font=_font_reg(11))
    return _to_bytes(img)


def reciprocal_flip(num=3, den=4, **kw) -> BytesIO:
    """Shows a fraction and an EMPTY matching box beside it -- the
    student draws/writes the reciprocal themselves by swapping
    numerator and denominator. A curved flip-arrow links the two."""
    w, h = 300, 140
    img, d = _blank(w, h)
    fnt = _font(20)
    box_w, box_h = 70, 90
    x1, y1 = 30, 25
    x2, y2 = 200, 25
    d.rectangle([x1, y1, x1+box_w, y1+box_h], outline=C_BORDER, width=2)
    d.line([x1, y1+box_h/2, x1+box_w, y1+box_h/2], fill=C_BORDER, width=2)
    tw = d.textlength(str(num), font=fnt)
    d.text((x1+box_w/2-tw/2, y1+box_h/2-26), str(num), fill=C_BLUE_D, font=fnt)
    tw = d.textlength(str(den), font=fnt)
    d.text((x1+box_w/2-tw/2, y1+box_h/2+6), str(den), fill=C_TEAL_D, font=fnt)
    d.rectangle([x2, y2, x2+box_w, y2+box_h], outline=C_BORDER, width=2)
    d.line([x2, y2+box_h/2, x2+box_w, y2+box_h/2], fill=C_BORDER, width=2)
    ax0, ay0 = x1+box_w+10, y1+box_h/2
    ax1, ay1 = x2-10, y2+box_h/2
    amx, amy = (ax0+ax1)/2, ay0-30
    d.arc([ax0, amy, ax1, ay0+10], start=200, end=340, fill=C_AMBER_D, width=2)
    d.polygon([(ax1-6, amy+22), (ax1+2, amy+30), (ax1-10, amy+34)], fill=C_AMBER_D)
    d.text((amx-18, amy-14), "flip", fill=C_AMBER_D, font=_font_reg(11))
    return _to_bytes(img)


def cross_multiply_bowtie(num1=2, den1=3, num2=3, den2=5, **kw) -> BytesIO:
    """Two fractions side by side with diagonal 'bowtie' arrows
    connecting each numerator to the OTHER fraction's denominator --
    the cross-multiplication comparison technique. Product boxes are
    left empty for the student to fill in and compare."""
    w, h = 320, 180
    img, d = _blank(w, h)
    fnt = _font(18)
    fnt_s = _font_reg(12)
    x1, x2 = 90, 230
    y_num, y_den = 40, 80
    for (x, lbl) in [(x1, str(num1)), (x2, str(num2))]:
        tw = d.textlength(lbl, font=fnt)
        d.text((x-tw/2, y_num), lbl, fill=C_BLUE_D, font=fnt)
    d.line([x1-18, y_den, x1+18, y_den], fill=C_BORDER, width=2)
    d.line([x2-18, y_den, x2+18, y_den], fill=C_BORDER, width=2)
    for (x, lbl) in [(x1, str(den1)), (x2, str(den2))]:
        tw = d.textlength(lbl, font=fnt)
        d.text((x-tw/2, y_den+8), lbl, fill=C_TEAL_D, font=fnt)
    d.line([x1+14, y_num+14, x2-14, y_den+16], fill=C_AMBER_D, width=2)
    d.line([x2-14, y_num+14, x1+14, y_den+16], fill=C_AMBER_D, width=2)
    tw = d.textlength("vs", font=fnt_s)
    d.text(((x1+x2)/2-tw/2, (y_num+y_den)/2-2), "vs", fill=C_GRAY_D, font=fnt_s)
    d.rectangle([x1-30, 130, x1+30, 160], outline=C_BORDER, width=2)
    d.rectangle([x2-30, 130, x2+30, 160], outline=C_BORDER, width=2)
    d.text((x1-tw, 138), f"{num1}x{den2}", fill=C_TEXT, font=_font_reg(10))
    d.text((x2-tw, 138), f"{num2}x{den1}", fill=C_TEXT, font=_font_reg(10))
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


def decimal_mult_area_blank(d1=3, d2=4, **kw) -> BytesIO:
    """A 10x10 grid (100 squares) with the target column (d1) and row
    (d2) boundaries marked -- for shading d1 tenths as columns, d2
    tenths as rows, and finding the overlap = the decimal product.
    e.g. 0.3 x 0.4: mark column 3 and row 4; the overlap is 12 of 100
    squares = 0.12. Same 'decimal squares' technique as fraction
    multiplication, applied to decimals."""
    cell = 18
    x0, y0 = 34, 34
    w, h = x0 + 10 * cell + 10, y0 + 10 * cell + 10
    img, d = _blank(w, h)
    for i in range(11):
        col = C_BLUE_D if i == d1 else C_BORDER
        width = 3 if i in (0, d1, 10) else 1
        d.line([x0 + i * cell, y0, x0 + i * cell, y0 + 10 * cell], fill=col, width=width)
    for j in range(11):
        row = C_TEAL_D if j == d2 else C_BORDER
        width = 3 if j in (0, d2, 10) else 1
        d.line([x0, y0 + j * cell, x0 + 10 * cell, y0 + j * cell], fill=row, width=width)
    fnt = _font_reg(11)
    lbl1 = f"0.{d1}"; tw1 = d.textlength(lbl1, font=fnt)
    d.text((x0 + d1 * cell / 2 - tw1 / 2, y0 - 20), lbl1, fill=C_BLUE_D, font=fnt)
    lbl2 = f"0.{d2}"; tw2 = d.textlength(lbl2, font=fnt)
    d.text((x0 - tw2 - 8, y0 + d2 * cell / 2 - 6), lbl2, fill=C_TEAL_D, font=fnt)
    return _to_bytes(img)


def decimal_mult_area_example(d1=3, d2=4, **kw) -> BytesIO:
    """Worked example: the same 10x10 grid with the d1xd2 overlap
    region cross-hatched, and the product labelled underneath."""
    cell = 18
    x0, y0 = 34, 34
    w, h = x0 + 10 * cell + 10, y0 + 10 * cell + 34
    img, d = _blank(w, h)
    for i in range(d1):
        for j in range(d2):
            cx0, cy0 = x0 + i * cell, y0 + j * cell
            _hatch_cell(d, cx0, cy0, cx0 + cell, cy0 + cell, "x", step=5)
    for i in range(11):
        col = C_BLUE_D if i == d1 else C_BORDER
        width = 3 if i in (0, d1, 10) else 1
        d.line([x0 + i * cell, y0, x0 + i * cell, y0 + 10 * cell], fill=col, width=width)
    for j in range(11):
        row = C_TEAL_D if j == d2 else C_BORDER
        width = 3 if j in (0, d2, 10) else 1
        d.line([x0, y0 + j * cell, x0 + 10 * cell, y0 + j * cell], fill=row, width=width)
    fnt = _font_reg(11)
    lbl1 = f"0.{d1}"; tw1 = d.textlength(lbl1, font=fnt)
    d.text((x0 + d1 * cell / 2 - tw1 / 2, y0 - 20), lbl1, fill=C_BLUE_D, font=fnt)
    lbl2 = f"0.{d2}"; tw2 = d.textlength(lbl2, font=fnt)
    d.text((x0 - tw2 - 8, y0 + d2 * cell / 2 - 6), lbl2, fill=C_TEAL_D, font=fnt)
    result = f"0.{d1} x 0.{d2} = {d1*d2}/100 = 0.{d1*d2:02d}"
    d.text((x0 - 20, y0 + 10 * cell + 10), result, fill=C_TEXT, font=fnt)
    return _to_bytes(img)


def decimal_point_shift_blank(number="3.45", op="x10", **kw) -> BytesIO:
    """Shows a decimal number and an arrow labelled with the operation
    (x10, /10, x100, /100), pointing to a BLANK box for the student to
    write the shifted result -- emphasizes the decimal POINT physically
    moving, rather than a memorized rule."""
    w, h = 300, 110
    img, d = _blank(w, h)
    fnt = _font(20)
    fnt_r = _font_reg(12)
    tw = d.textlength(number, font=fnt)
    d.text((20, 40), number, fill=C_BLUE_D, font=fnt)
    ax0 = 20 + tw + 15
    ax1 = ax0 + 65
    d.line([ax0, 55, ax1, 55], fill=C_AMBER_D, width=3)
    d.polygon([(ax1, 55), (ax1 - 10, 49), (ax1 - 10, 61)], fill=C_AMBER_D)
    optw = d.textlength(op, font=fnt_r)
    d.text((ax0 + (ax1 - ax0) / 2 - optw / 2, 30), op, fill=C_AMBER_D, font=fnt_r)
    d.rectangle([ax1 + 15, 25, ax1 + 105, 65], outline=C_BORDER, width=2)
    return _to_bytes(img)


def decimal_point_shift_example(number="3.45", op="x10", result="34.5", **kw) -> BytesIO:
    """Worked example: same as decimal_point_shift_blank, with the
    result filled in and the moved decimal point highlighted."""
    w, h = 300, 110
    img, d = _blank(w, h)
    fnt = _font(20)
    fnt_r = _font_reg(12)
    tw = d.textlength(number, font=fnt)
    d.text((20, 40), number, fill=C_BLUE_D, font=fnt)
    ax0 = 20 + tw + 15
    ax1 = ax0 + 65
    d.line([ax0, 55, ax1, 55], fill=C_AMBER_D, width=3)
    d.polygon([(ax1, 55), (ax1 - 10, 49), (ax1 - 10, 61)], fill=C_AMBER_D)
    optw = d.textlength(op, font=fnt_r)
    d.text((ax0 + (ax1 - ax0) / 2 - optw / 2, 30), op, fill=C_AMBER_D, font=fnt_r)
    d.rectangle([ax1 + 15, 25, ax1 + 105, 65], outline=C_BORDER, width=2)
    rtw = d.textlength(result, font=fnt)
    d.text((ax1 + 60 - rtw / 2, 35), result, fill=C_TEAL_D, font=fnt)
    return _to_bytes(img)


def decimal_zoom_numberline_blank(lo=0.0, hi=1.0, zoom_lo=0.3, zoom_hi=0.4, **kw) -> BytesIO:
    """Two number lines stacked: the outer line (lo to hi, coarse
    tenths ticks) with a highlighted sub-interval, and the inner line
    showing that SAME sub-interval magnified into finer ticks --
    makes nested place value visible (why 0.09 sits INSIDE 0 to 0.1,
    not beyond it)."""
    w, h = 280, 150
    img, d = _blank(w, h)
    pad = 25
    y1 = 30
    d.line([pad, y1, w - pad, y1], fill=C_BORDER, width=2)
    for i in range(11):
        x = pad + i * (w - 2 * pad) / 10
        d.line([x, y1 - 6, x, y1 + 6], fill=C_BORDER, width=1)
    zx0 = pad + (zoom_lo - lo) / (hi - lo) * (w - 2 * pad)
    zx1 = pad + (zoom_hi - lo) / (hi - lo) * (w - 2 * pad)
    d.rectangle([zx0, y1 - 10, zx1, y1 + 10], outline=C_MARK, width=2)
    fnt = _font_reg(10)
    d.text((pad - 6, y1 + 10), str(lo), fill=C_BORDER, font=fnt)
    d.text((w - pad - 12, y1 + 10), str(hi), fill=C_BORDER, font=fnt)
    y2 = 115
    d.line([zx0, y1 + 10, pad, y2 - 10], fill=C_MARK, width=1)
    d.line([zx1, y1 + 10, w - pad, y2 - 10], fill=C_MARK, width=1)
    d.line([pad, y2, w - pad, y2], fill=C_MARK, width=2)
    for i in range(11):
        x = pad + i * (w - 2 * pad) / 10
        d.line([x, y2 - 6, x, y2 + 6], fill=C_MARK, width=1)
    d.text((pad - 12, y2 + 10), str(zoom_lo), fill=C_MARK, font=fnt)
    d.text((w - pad - 16, y2 + 10), str(zoom_hi), fill=C_MARK, font=fnt)
    return _to_bytes(img)


def decimal_align_blank(num1="3.4", num2="12.75", op="+", **kw) -> BytesIO:
    """Two decimals shown right-aligned by place value with a
    highlighted vertical guide through the decimal POINT column --
    for addition/subtraction, directly targeting the 'misaligned
    decimal point' error."""
    w, h = 220, 130
    img, d = _blank(w, h)
    fnt = _font(20)
    char_w = 17
    max_len = max(len(num1), len(num2)) + 2
    right_x = 30 + max_len * char_w

    def draw_num(s, y):
        x = right_x
        for ch in reversed(s):
            x -= char_w
            d.text((x, y), ch, fill=C_BLUE_D, font=fnt)

    draw_num(num1, 20)
    draw_num(num2, 55)
    d.text((10, 55), op, fill=C_MARK, font=fnt)

    def point_x_from_right(s):
        idx = s.index(".")
        chars_after_point = len(s) - idx - 1
        return right_x - chars_after_point * char_w - char_w / 2

    px1 = point_x_from_right(num1)
    d.line([px1, 10, px1, 100], fill=C_MARK, width=2)
    d.line([30, 100, right_x, 100], fill=C_BORDER, width=2)
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

def factor_tree(n=60, blank=False, **kw) -> BytesIO:
    """Draws a factor tree for n down to prime leaves, splitting off the
    smallest prime factor at each step (the standard way students draw it
    by hand). blank=True draws only the root node (n) with empty branch
    lines going nowhere, for the student to complete by hand."""
    if blank:
        w, h = 480, 360
        img, dr = _blank(w, h)
        fnt = _font(16)
        radius = 26
        cx, cy = w // 2, 50
        dr.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=C_BLUE, outline=C_BORDER, width=2)
        txt = str(n)
        tw = dr.textlength(txt, font=fnt)
        dr.text((cx - tw/2, cy - 10), txt, fill=C_TEXT, font=fnt)
        lx, rx, ny = cx - 110, cx + 110, cy + 110
        dr.line([cx, cy + radius, lx, ny - 30], fill=C_BORDER, width=2)
        dr.line([cx, cy + radius, rx, ny - 30], fill=C_BORDER, width=2)
        dr.ellipse([lx - radius, ny - radius, lx + radius, ny + radius], outline=C_BORDER, width=2)
        dr.ellipse([rx - radius, ny - radius, rx + radius, ny + radius], outline=C_BORDER, width=2)
        cap = "Split into two factors, then keep splitting until every branch ends in a prime."
        cw = dr.textlength(cap, font=_font_reg(13))
        dr.text((w/2 - cw/2, h - 40), cap, fill=C_TEAL_D, font=_font_reg(13))
        return _to_bytes(img)

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


def venn_two(a_only=None, common=None, b_only=None, label_a="A", label_b="B", blank=False, **kw) -> BytesIO:
    """Two-circle Venn diagram for shared vs. unique prime factors --
    standard visual for building HCF/LCM intuition. a_only/common/b_only
    are lists of numbers (or strings) to place in each region.
    blank=True draws the empty circles/labels only, no numbers, so the
    student works out and fills in each region themselves."""
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

    if blank:
        return _to_bytes(img)

    def place_list(items, cx, cy_offset):
        text = ", ".join(str(x) for x in items) if items else "--"
        tw = dr.textlength(text, font=fnt)
        dr.text((cx - tw/2, cy + cy_offset), text, fill=C_TEXT, font=fnt)

    place_list(a_only, cx_a - 45, -8)
    place_list(common, w//2, -8)
    place_list(b_only, cx_b + 45, -8)
    return _to_bytes(img)




# ─── RATIO BAR & PROPORTION GRAPH (Level 10 additions) ─────────────────────────

def ratio_bar(parts=None, labels=None, blank=False, **kw) -> BytesIO:
    """Horizontal bar split into segments proportional to a ratio (e.g.
    parts=[2,3] for a 2:3 ratio), each segment coloured and labelled.
    blank=True draws an undivided bar with just the ratio caption, for
    the student to partition it themselves."""
    parts = parts or [2, 3]
    labels = labels or [str(p) for p in parts]
    total = sum(parts) if sum(parts) else 1
    w, h = 560, 150
    img, dr = _blank(w, h)
    bar_w, bar_h = 480, 70
    x0 = (w - bar_w) // 2
    y0 = 30
    if blank:
        dr.rectangle([x0, y0, x0 + bar_w, y0 + bar_h], outline=C_BORDER, width=2)
        caption = ":".join(str(p) for p in parts) + " -- divide the bar in this ratio"
        cw = dr.textlength(caption, font=_font_reg(13))
        dr.text((w/2 - cw/2, y0 + bar_h + 15), caption, fill=C_TEAL_D, font=_font_reg(13))
        return _to_bytes(img)
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
    "mixed_number_area_blank": mixed_number_area_blank,
    "mixed_number_area_example": mixed_number_area_example,
    "reciprocal_flip": reciprocal_flip,
    "cross_multiply_bowtie": cross_multiply_bowtie,
    "fraction_bar": fraction_bar,
    "hundredths_grid_blank": hundredths_grid_blank,
    "hundredths_grid_example": hundredths_grid_example,
    "decimal_place_blank": decimal_place_blank,
    "decimal_place_example": decimal_place_example,
    "decimal_numberline_blank": decimal_numberline_blank,
    "decimal_numberline_example": decimal_numberline_example,
    "decimal_mult_area_blank": decimal_mult_area_blank,
    "decimal_mult_area_example": decimal_mult_area_example,
    "decimal_point_shift_blank": decimal_point_shift_blank,
    "decimal_point_shift_example": decimal_point_shift_example,
    "decimal_zoom_numberline_blank": decimal_zoom_numberline_blank,
    "decimal_align_blank": decimal_align_blank,
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


def balance_scale_svg(left_text="x + 3", right_text="7", w=380, blank=False, **kw):
    """Renders a balance scale in equilibrium with the two sides of an
    equation on each pan -- the standard visual for equation solving.
    Returns a raw SVG string. (The `blank` flag is accepted for a
    uniform interface but has no effect: the scale shows the equation,
    which IS the question -- there is no answer on it to hide.)"""
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


def like_terms_sort_svg(groups=None, blank=False, **kw):
    """Sorts a set of terms into labelled, colour-coded groups (e.g.
    x-terms, y-terms, constants) inside dashed boundary boxes -- the
    visual for 'collecting like terms'. blank=True instead shows all
    the terms jumbled together in a single unsorted box, so the student
    does the sorting themselves."""
    groups = groups or {"x-terms": ["3x", "2x"], "constants": ["5", "1"]}
    if blank:
        all_terms = [t for terms in groups.values() for t in terms]
        card_w, card_h, gap, pad = 54, 34, 10, 18
        cols = min(len(all_terms), 6)
        rows = -(-len(all_terms) // cols)
        box_w = cols * (card_w + gap) - gap + 2 * pad
        box_h = rows * (card_h + gap) - gap + 2 * pad
        parts = [f'<rect x="16" y="42" width="{box_w}" height="{box_h}" rx="14" fill="#FAFBFC" stroke="#9AA5B1" stroke-width="2" stroke-dasharray="6,3"/>',
                 '<text x="16" y="32" font-family="Helvetica-Bold" font-size="13" fill="#5D6D7E">Sort these into their groups:</text>']
        tx, ty = 16 + pad, 42 + pad
        for i, term in enumerate(all_terms):
            if i and i % cols == 0:
                tx = 16 + pad
                ty += card_h + gap
            parts.append(f'<rect x="{tx}" y="{ty}" width="{card_w}" height="{card_h}" rx="8" fill="white" stroke="#5D6D7E" stroke-width="1.8"/>')
            parts.append(f'<text x="{tx+card_w/2}" y="{ty+card_h/2+5}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">{term}</text>')
            tx += card_w + gap
        width = 16 + box_w + 16
        height = 42 + box_h + 16
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">' + "".join(parts) + "</svg>"
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


def substitution_steps_svg(steps=None, blank=False, **kw):
    """A vertical chain of boxes showing a substitution worked step by
    step, e.g. '2x+1' -> '2(3)+1' -> '6+1' -> '7', the last box
    highlighted as the final answer. blank=True keeps the first step
    (the given expression + substitution) and blanks every step after,
    so the student works the arithmetic out themselves."""
    steps = steps or ["2x + 1", "2(3) + 1", "6 + 1", "7"]
    if blank:
        steps = [steps[0]] + ["____"] * (len(steps) - 1)
    w, box_h, gap = 260, 40, 24
    h = len(steps) * (box_h + gap) - gap + 26
    parts = []
    y = 14
    for i, s in enumerate(steps):
        is_last = (i == len(steps) - 1)
        is_blank_step = blank and i > 0
        if is_blank_step:
            fill, stroke, tcol = ("#FAFBFC", "#9AA5B1", "#5D6D7E")
        else:
            fill, stroke, tcol = ("#E7F8ED", "#1E7A44", "#0B4F30") if is_last else ("#EAF4FC", "#1B5E8C", "#0C3A5C")
        dash = ' stroke-dasharray="6,4"' if is_blank_step else ""
        parts.append(f'<rect x="20" y="{y}" width="{w-40}" height="{box_h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>')
        parts.append(f'<text x="{w/2}" y="{y+box_h/2+6}" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="{tcol}">{s}</text>')
        if not is_last:
            ay = y + box_h
            parts.append(f'<line x1="{w/2}" y1="{ay+3}" x2="{w/2}" y2="{ay+gap-7}" stroke="#2C3E50" stroke-width="2"/>')
            parts.append(f'<polygon points="{w/2},{ay+gap-2} {w/2-6},{ay+gap-11} {w/2+6},{ay+gap-11}" fill="#2C3E50"/>')
        y += box_h + gap
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def repeated_addition_svg(coefficient=3, variable="x", blank=False, **kw):
    """Shows a term like '3x' as repeated addition: x + x + x -- builds
    the intuition for what a coefficient means. blank=True hides the
    caption so the student writes the sum themselves."""
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
    if blank:
        cap = f"{coefficient}{variable}  =  ____ (write it as a sum)"
    else:
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


def linear_equation_graph_svg(a=1, b=1, c=6, rng=10, blank=False, **kw):
    """Plots the single line ax+by=c on a coordinate grid, marking its
    x- and y-intercepts. The core visual for graphing linear equations.
    blank=True shows an empty grid with the equation, for the student to
    plot the line themselves."""
    size = 340
    parts, to_px = _grid_svg_base(rng, size)
    if blank:
        eqn = _fmt_equation(a, b, c)
        parts.insert(0, f'<text x="{size/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#2C3E50">Plot: {eqn}</text>')
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"
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


def two_line_graph_svg(a1=1, b1=1, c1=6, a2=1, b2=-1, c2=2, rng=10, blank=False, **kw):
    """Plots two lines on one grid and marks their intersection, or notes
    if they're parallel/coincident -- the visual for the graphical method
    and for consistent/inconsistent/dependent systems. blank=True shows
    an empty grid with both equations, for the student to plot and read
    off the answer themselves."""
    size = 360
    parts, to_px = _grid_svg_base(rng, size)
    eqn1 = _fmt_equation(a1, b1, c1)
    eqn2 = _fmt_equation(a2, b2, c2)
    if blank:
        parts.insert(0, f'<text x="{size/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{eqn1}   and   {eqn2}</text>')
        parts.append(f'<text x="{size/2}" y="{size-8}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#5D6D7E">Plot both lines -- where do they meet?</text>')
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"
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


def area_model_svg(a=1, b=3, c=1, d=2, var="x", blank=False, **kw):
    """(ax+b)(cx+d) shown as a 4-region area-model rectangle -- the
    standard visual for binomial multiplication (FOIL made concrete).
    blank=True keeps the row/column headers but empties the 4 product
    cells for the student to fill."""
    col_labels = [_poly_term_str(a, 1, var), (f"+{b}" if b >= 0 else f"-{abs(b)}")]
    row_labels = [_poly_term_str(c, 1, var), (f"+{d}" if d >= 0 else f"-{abs(d)}")]
    cells = [
        [_poly_term_str(a * c, 2, var), _poly_term_str(a * d, 1, var)],
        [_poly_term_str(b * c, 1, var), _poly_term_str(b * d, 0, var)],
    ]
    if blank:
        cells = [["?", "?"], ["?", "?"]]
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
            bg = "#FAFBFC" if blank else bgs[i*2+j]
            parts.append(f'<rect x="{cx}" y="{cy}" width="{cell_w}" height="{cell_h}" fill="{bg}" stroke="#2C3E50" stroke-width="1.5"/>')
            parts.append(f'<text x="{cx+cell_w/2:.1f}" y="{cy+cell_h/2+6:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">{cells[i][j]}</text>')
    tip = "Multiply row x column to fill each cell, then add." if blank else "Add all 4 areas together"
    parts.append(f'<text x="{w/2}" y="{y0+2*cell_h+24}" text-anchor="middle" font-family="Helvetica-Oblique" font-size="11" fill="#5D6D7E">{tip}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def polynomial_graph_svg(coeffs=None, xrange=6, blank=False, **kw):
    """Plots y=p(x) for a polynomial (coeffs = highest degree first, e.g.
    [1,-5,6] for x²-5x+6), marking the real zeroes (x-intercepts) found
    within the visible range -- the geometric meaning of a zero.
    blank=True keeps the curve (it IS the question) but hides the
    zero labels so the student reads them off the graph themselves."""
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
    if blank:
        zeroes = []
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


def _quadrant_bg(parts, margin, size, rng):
    """Adds faint quadrant background shading behind the grid."""
    ox = margin + rng / (2 * rng) * (size - 2 * margin)
    colors = ["#F7FBFF", "#FFFBF2", "#FFF7F5", "#F5FBF8"]  # I, II, III, IV (soft tints)
    half = (size - 2 * margin) / 2
    quads = [
        (ox, margin, ox + half, margin + half, colors[1]),          # top-left = QII
        (ox, margin, ox + half, margin + half, colors[1]),
    ]
    # simpler: just tint the 4 rectangles directly
    parts.insert(0, f'<rect x="{ox:.1f}" y="{margin}" width="{half:.1f}" height="{half:.1f}" fill="{colors[0]}"/>')      # QI (top-right)
    parts.insert(0, f'<rect x="{margin}" y="{margin}" width="{half:.1f}" height="{half:.1f}" fill="{colors[1]}"/>')      # QII (top-left)
    parts.insert(0, f'<rect x="{margin}" y="{margin+half:.1f}" width="{half:.1f}" height="{half:.1f}" fill="{colors[2]}"/>')  # QIII (bottom-left)
    parts.insert(0, f'<rect x="{ox:.1f}" y="{margin+half:.1f}" width="{half:.1f}" height="{half:.1f}" fill="{colors[3]}"/>')   # QIV (bottom-right)


def plot_points_grid_svg(points=None, labels=None, rng=8, show_quadrants=True, blank=False, **kw):
    """Plots one or more labelled points on a coordinate grid, with
    optional soft quadrant shading -- the basic 'see where a point is'
    visual for the coordinate plane. blank=True shows the empty grid
    with the point names listed as a task, for the student to plot."""
    points = points or [(3, 2)]
    labels = labels or [f"({x},{y})" for x, y in points]
    size = 320
    margin = 34
    parts, to_px = _grid_svg_base(rng, size, margin)
    if show_quadrants:
        _quadrant_bg(parts, margin, size, rng)
    if blank:
        task = ", ".join(labels)
        parts.insert(0, f'<text x="{size/2}" y="16" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">Plot: {task}</text>')
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"
    colors = ["#A6362B", "#1B5E8C", "#1E7A44", "#7D3C98"]
    for i, (x, y) in enumerate(points):
        px, py = to_px(x, y)
        color = colors[i % len(colors)]
        parts.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px:.1f}" y2="{to_px(0,0)[1]:.1f}" stroke="{color}" stroke-width="1" stroke-dasharray="3,2" opacity="0.6"/>')
        parts.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{to_px(0,0)[0]:.1f}" y2="{py:.1f}" stroke="{color}" stroke-width="1" stroke-dasharray="3,2" opacity="0.6"/>')
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="{color}"/>')
        lbl = labels[i] if i < len(labels) else f"({x},{y})"
        parts.append(f'<text x="{px+9:.1f}" y="{py-9:.1f}" font-family="Helvetica-Bold" font-size="12" fill="{color}">{lbl}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"


def distance_segment_svg(p1=(1, 1), p2=(5, 4), rng=8, blank=False, **kw):
    """Plots two points joined by a segment, WITH the horizontal/vertical
    'legs' shown as a right triangle -- visualizes that the distance
    formula is just Pythagoras on the grid. The caption works the actual
    computation d = sqrt(dx^2 + dy^2). blank=True keeps only the two
    points and the segment: the student draws the legs and computes."""
    import math as _m
    size = 340
    margin = 34
    parts, to_px = _grid_svg_base(rng, size, margin)
    x1, y1 = p1; x2, y2 = p2
    px1, py1 = to_px(x1, y1)
    px2, py2 = to_px(x2, y2)
    pxc, pyc = to_px(x2, y1)  # corner point for the right-angle
    hlen = abs(x2 - x1); vlen = abs(y2 - y1)
    if not blank:
        parts.append(f'<polygon points="{px1:.1f},{py1:.1f} {pxc:.1f},{pyc:.1f} {px2:.1f},{py2:.1f}" fill="#FFF3CD" opacity="0.5" stroke="none"/>')
        parts.append(f'<line x1="{px1:.1f}" y1="{py1:.1f}" x2="{pxc:.1f}" y2="{pyc:.1f}" stroke="#B7950B" stroke-width="2" stroke-dasharray="4,3"/>')
        parts.append(f'<line x1="{pxc:.1f}" y1="{pyc:.1f}" x2="{px2:.1f}" y2="{py2:.1f}" stroke="#B7950B" stroke-width="2" stroke-dasharray="4,3"/>')
    parts.append(f'<line x1="{px1:.1f}" y1="{py1:.1f}" x2="{px2:.1f}" y2="{py2:.1f}" stroke="#1B5E8C" stroke-width="2.5"/>')
    if not blank:
        parts.append(f'<text x="{(px1+pxc)/2:.1f}" y="{pyc+14:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#7D5A00">{hlen:g}</text>')
        parts.append(f'<text x="{pxc+8:.1f}" y="{(pyc+py2)/2:.1f}" font-family="Helvetica-Bold" font-size="11" fill="#7D5A00">{vlen:g}</text>')
    for (px, py, x, y, color) in [(px1, py1, x1, y1, "#A6362B"), (px2, py2, x2, y2, "#1E7A44")]:
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="{color}"/>')
        parts.append(f'<text x="{px+8:.1f}" y="{py-8:.1f}" font-family="Helvetica-Bold" font-size="11" fill="{color}">({x:g},{y:g})</text>')
    if blank:
        caption = "Draw the horizontal and vertical legs, then use Pythagoras."
    else:
        d2 = hlen * hlen + vlen * vlen
        root = _m.isqrt(int(d2))
        d_str = str(root) if root * root == d2 else f"√{d2:g}"
        caption = f"d = √({hlen:g}² + {vlen:g}²) = √{d2:g} = {d_str}"
    parts.insert(0, f'<text x="{size/2}" y="16" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">{caption}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"


def midpoint_segment_svg(p1=(1, 1), p2=(7, 5), rng=8, blank=False, **kw):
    """Plots two points joined by a segment with the midpoint marked,
    and the averaging computation shown in the caption. blank=True keeps
    the endpoints and segment but hides M and the computation."""
    size = 340
    margin = 34
    parts, to_px = _grid_svg_base(rng, size, margin)
    x1, y1 = p1; x2, y2 = p2
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    px1, py1 = to_px(x1, y1)
    px2, py2 = to_px(x2, y2)
    pmx, pmy = to_px(mx, my)
    parts.append(f'<line x1="{px1:.1f}" y1="{py1:.1f}" x2="{px2:.1f}" y2="{py2:.1f}" stroke="#1B5E8C" stroke-width="2.5"/>')
    for (px, py, x, y, color) in [(px1, py1, x1, y1, "#A6362B"), (px2, py2, x2, y2, "#1E7A44")]:
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="{color}"/>')
        parts.append(f'<text x="{px+8:.1f}" y="{py-8:.1f}" font-family="Helvetica-Bold" font-size="11" fill="{color}">({x:g},{y:g})</text>')
    if blank:
        caption = f"M = ((x₁+x₂)/2, (y₁+y₂)/2) -- mark the middle of the segment."
    else:
        parts.append(f'<circle cx="{pmx:.1f}" cy="{pmy:.1f}" r="6.5" fill="#7D3C98" stroke="white" stroke-width="1.5"/>')
        parts.append(f'<text x="{pmx:.1f}" y="{pmy+20:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#7D3C98">M({mx:g},{my:g})</text>')
        caption = f"M = (({x1:g}+{x2:g})/2, ({y1:g}+{y2:g})/2) = ({mx:g}, {my:g})"
    parts.insert(0, f'<text x="{size/2}" y="16" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#7D3C98">{caption}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"


def section_segment_svg(p1=(0, 0), p2=(8, 4), m=1, n=3, rng=8, blank=False, **kw):
    """Plots two points joined by a segment, with the point dividing it
    in ratio m:n marked, plus tick marks splitting the segment into
    m+n equal parts so the ratio is countable. blank=True keeps the
    ticks but hides P and its coordinates."""
    size = 340
    margin = 34
    parts, to_px = _grid_svg_base(rng, size, margin)
    x1, y1 = p1; x2, y2 = p2
    px_, py_ = (m * x2 + n * x1) / (m + n), (m * y2 + n * y1) / (m + n)
    pp1x, pp1y = to_px(x1, y1)
    pp2x, pp2y = to_px(x2, y2)
    ppx, ppy = to_px(px_, py_)
    parts.append(f'<line x1="{pp1x:.1f}" y1="{pp1y:.1f}" x2="{pp2x:.1f}" y2="{pp2y:.1f}" stroke="#1B5E8C" stroke-width="2.5"/>')
    total = m + n
    import math as _m
    seg_dx, seg_dy = pp2x - pp1x, pp2y - pp1y
    seg_len = _m.hypot(seg_dx, seg_dy) or 1
    nx_, ny_ = -seg_dy / seg_len, seg_dx / seg_len
    for k in range(1, total):
        tx = pp1x + seg_dx * k / total
        ty = pp1y + seg_dy * k / total
        parts.append(f'<line x1="{tx-nx_*6:.1f}" y1="{ty-ny_*6:.1f}" x2="{tx+nx_*6:.1f}" y2="{ty+ny_*6:.1f}" stroke="#5D6D7E" stroke-width="1.8"/>')
    for (px, py, x, y, color, name) in [(pp1x, pp1y, x1, y1, "#A6362B", "A"), (pp2x, pp2y, x2, y2, "#1E7A44", "B")]:
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="{color}"/>')
        parts.append(f'<text x="{px+8:.1f}" y="{py-8:.1f}" font-family="Helvetica-Bold" font-size="11" fill="{color}">{name}({x:g},{y:g})</text>')
    if not blank:
        parts.append(f'<circle cx="{ppx:.1f}" cy="{ppy:.1f}" r="6.5" fill="#7D3C98" stroke="white" stroke-width="1.5"/>')
        px_lbl = round(px_, 2); px_lbl = int(px_lbl) if px_lbl == int(px_lbl) else px_lbl
        py_lbl = round(py_, 2); py_lbl = int(py_lbl) if py_lbl == int(py_lbl) else py_lbl
        parts.append(f'<text x="{ppx:.1f}" y="{ppy+20:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#7D3C98">P({px_lbl:g},{py_lbl:g})</text>')
        title = f"P divides AB in ratio {m}:{n} -- {m} parts from A, {n} parts to B"
    else:
        title = f"Mark P dividing AB in ratio {m}:{n} ({total} equal parts shown)"
    parts.insert(0, f'<text x="{size/2}" y="16" text-anchor="middle" font-family="Helvetica-Bold" font-size="11.5" fill="#2C3E50">{title}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"


def triangle_coords_svg(p1=(0, 0), p2=(6, 0), p3=(3, 5), rng=8, blank=False, show_area=None, **kw):
    """Plots three points as a shaded triangle on the coordinate grid --
    the visual for the area-of-a-triangle-by-coordinates formula. In
    worked mode (blank=False) the caption computes the area (or flags
    collinearity when area=0); blank=True shows just the labelled
    triangle for the student to compute."""
    size = 340
    margin = 34
    parts, to_px = _grid_svg_base(rng, size, margin)
    pts_px = [to_px(*p) for p in (p1, p2, p3)]
    poly = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts_px)
    parts.append(f'<polygon points="{poly}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    labels_lc = ["A", "B", "C"]
    colors = ["#A6362B", "#1E7A44", "#7D3C98"]
    for i, ((px, py), (x, y)) in enumerate(zip(pts_px, (p1, p2, p3))):
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="{colors[i]}"/>')
        parts.append(f'<text x="{px+8:.1f}" y="{py-8:.1f}" font-family="Helvetica-Bold" font-size="12" fill="{colors[i]}">{labels_lc[i]}({x:g},{y:g})</text>')
    if not blank:
        (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
        raw = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
        area = abs(raw) / 2
        if area == 0:
            caption = "Area = 0 -- the three points are COLLINEAR!"
        else:
            caption = f"Area = ½|{raw:g}| = {area:g} square units"
        parts.insert(0, f'<text x="{size/2}" y="16" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">{caption}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"


def points_lines_rays_svg(**kw):
    """Shows a point, a line, a ray, and a line segment side by side --
    the four basic building blocks of geometry, visually distinguished."""
    w, h = 600, 190
    parts = []
    panel_w = w / 4
    y = 80

    cx0 = panel_w * 0.5
    parts.append(f'<circle cx="{cx0}" cy="{y}" r="4.5" fill="#1B5E8C"/>')
    parts.append(f'<text x="{cx0}" y="{y-14}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#1B5E8C">A</text>')

    cx1 = panel_w * 1.5
    x1a, x1b = cx1 - 55, cx1 + 55
    parts.append(f'<line x1="{x1a}" y1="{y}" x2="{x1b}" y2="{y}" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<polygon points="{x1a},{y} {x1a+11},{y-5.5} {x1a+11},{y+5.5}" fill="#1B5E8C"/>')
    parts.append(f'<polygon points="{x1b},{y} {x1b-11},{y-5.5} {x1b-11},{y+5.5}" fill="#1B5E8C"/>')
    parts.append(f'<text x="{cx1-32}" y="{y-14}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#1B5E8C">A</text>')
    parts.append(f'<text x="{cx1+32}" y="{y-14}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#1B5E8C">B</text>')

    cx2 = panel_w * 2.5
    x2a, x2b = cx2 - 55, cx2 + 55
    parts.append(f'<line x1="{x2a}" y1="{y}" x2="{x2b}" y2="{y}" stroke="#1E7A44" stroke-width="2.5"/>')
    parts.append(f'<circle cx="{x2a}" cy="{y}" r="4.5" fill="#1E7A44"/>')
    parts.append(f'<polygon points="{x2b},{y} {x2b-11},{y-5.5} {x2b-11},{y+5.5}" fill="#1E7A44"/>')
    parts.append(f'<text x="{x2a}" y="{y-14}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#1E7A44">A</text>')
    parts.append(f'<text x="{x2b}" y="{y-14}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#1E7A44">B</text>')

    cx3 = panel_w * 3.5
    x3a, x3b = cx3 - 55, cx3 + 55
    parts.append(f'<line x1="{x3a}" y1="{y}" x2="{x3b}" y2="{y}" stroke="#A6362B" stroke-width="2.5"/>')
    parts.append(f'<circle cx="{x3a}" cy="{y}" r="4.5" fill="#A6362B"/>')
    parts.append(f'<circle cx="{x3b}" cy="{y}" r="4.5" fill="#A6362B"/>')
    parts.append(f'<text x="{x3a}" y="{y-14}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#A6362B">A</text>')
    parts.append(f'<text x="{x3b}" y="{y-14}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#A6362B">B</text>')

    labels = ["Point", "Line", "Ray", "Line Segment"]
    colors = ["#1B5E8C", "#1B5E8C", "#1E7A44", "#A6362B"]
    for i, lbl in enumerate(labels):
        cx = panel_w * (i + 0.5)
        parts.append(f'<text x="{cx}" y="{y+42}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="{colors[i]}">{lbl}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def angle_pair_svg(kind="complementary", a1=35, blank=False, **kw):
    """Illustrates a pair of angles: complementary (sum 90, right-angle
    mark), supplementary/linear pair (sum 180, straight line), or
    vertical (two crossing lines, opposite angles equal). blank=True
    hides the second (derived) angle's value."""
    import math as _m
    w, h = 320, 260
    cx, cy = 160, 190
    r = 95
    parts = []
    if kind == "complementary":
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+r}" y2="{cy}" stroke="#2C3E50" stroke-width="2.5"/>')
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-r}" stroke="#2C3E50" stroke-width="2.5"/>')
        rad = _m.radians(a1)
        mx, my = cx + r * _m.cos(rad), cy - r * _m.sin(rad)
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{mx:.1f}" y2="{my:.1f}" stroke="#1B5E8C" stroke-width="2.5"/>')
        parts.append(f'<rect x="{cx}" y="{cy-14}" width="14" height="14" fill="none" stroke="#7F8C8D" stroke-width="1.5"/>')
        parts.append(f'<text x="{cx+38:.1f}" y="{cy-18}" font-family="Helvetica-Bold" font-size="14" fill="#A6362B">{a1}°</text>')
        other_str = "?" if blank else f"{90-a1}°"
        parts.append(f'<text x="{cx+12}" y="{cy-60}" font-family="Helvetica-Bold" font-size="14" fill="#1E7A44">{other_str}</text>')
        cap = f"{a1}° + ? = 90°  (Complementary)" if blank else f"{a1}° + {90-a1}° = 90°  (Complementary)"
    elif kind in ("supplementary", "linear"):
        parts.append(f'<line x1="{cx-r}" y1="{cy}" x2="{cx+r}" y2="{cy}" stroke="#2C3E50" stroke-width="2.5"/>')
        rad = _m.radians(a1)
        mx, my = cx + r * _m.cos(rad), cy - r * _m.sin(rad)
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{mx:.1f}" y2="{my:.1f}" stroke="#1B5E8C" stroke-width="2.5"/>')
        parts.append(f'<text x="{cx+42:.1f}" y="{cy-22}" font-family="Helvetica-Bold" font-size="14" fill="#A6362B">{a1}°</text>')
        other_str = "?" if blank else f"{180-a1}°"
        parts.append(f'<text x="{cx-56}" y="{cy-22}" font-family="Helvetica-Bold" font-size="14" fill="#1E7A44">{other_str}</text>')
        nm = "Linear Pair" if kind == "linear" else "Supplementary"
        cap = f"{a1}° + ? = 180°  ({nm})" if blank else f"{a1}° + {180-a1}° = 180°  ({nm})"
    else:
        rad1 = _m.radians(a1)
        x1, y1 = cx + r * _m.cos(rad1), cy - r * _m.sin(rad1)
        x2, y2 = cx - r * _m.cos(rad1), cy + r * _m.sin(rad1)
        rad2 = _m.radians(a1 + 55)
        x3, y3 = cx + r * _m.cos(rad2), cy - r * _m.sin(rad2)
        x4, y4 = cx - r * _m.cos(rad2), cy + r * _m.sin(rad2)
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#1B5E8C" stroke-width="2.5"/>')
        parts.append(f'<line x1="{x3:.1f}" y1="{y3:.1f}" x2="{x4:.1f}" y2="{y4:.1f}" stroke="#A6362B" stroke-width="2.5"/>')
        mid1 = _m.radians(a1 + 27)
        lx1, ly1 = cx + 40 * _m.cos(mid1), cy - 40 * _m.sin(mid1)
        lx2, ly2 = cx - 40 * _m.cos(mid1), cy + 40 * _m.sin(mid1)
        parts.append(f'<text x="{lx1:.1f}" y="{ly1:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#1E7A44">x</text>')
        parts.append(f'<text x="{lx2:.1f}" y="{ly2:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#1E7A44">x</text>')
        cap = "Vertically opposite angles are EQUAL"
    parts.insert(0, f'<text x="{w/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">{cap}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def transversal_angles_svg(**kw):
    """Two parallel lines cut by a transversal, all 8 angles numbered --
    the standard visual for corresponding/alternate/co-interior angles."""
    w, h = 340, 300
    y1, y2 = 90, 210
    x_left, x_right = 30, 310
    parts = []
    parts.append(f'<line x1="{x_left}" y1="{y1}" x2="{x_right}" y2="{y1}" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<line x1="{x_left}" y1="{y2}" x2="{x_right}" y2="{y2}" stroke="#1B5E8C" stroke-width="2.5"/>')
    for yv in (y1, y2):
        parts.append(f'<polyline points="{x_right-26},{yv-7} {x_right-16},{yv} {x_right-26},{yv+7}" fill="none" stroke="#1B5E8C" stroke-width="1.8"/>')
    ix1, iy1 = 148, y1
    ix2, iy2 = 212, y2
    parts.append(f'<line x1="122" y1="42" x2="238" y2="258" stroke="#A6362B" stroke-width="2.5"/>')
    off = 26
    labels1 = {1: (-off, -14), 2: (off * 0.65, -14), 3: (-off, 20), 4: (off * 0.65, 20)}
    labels2 = {5: (-off, -14), 6: (off * 0.65, -14), 7: (-off, 20), 8: (off * 0.65, 20)}
    for num, (dx, dy) in labels1.items():
        parts.append(f'<text x="{ix1+dx:.1f}" y="{iy1+dy:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">{num}</text>')
    for num, (dx, dy) in labels2.items():
        parts.append(f'<text x="{ix2+dx:.1f}" y="{iy2+dy:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">{num}</text>')
    parts.insert(0, f'<text x="{w/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">Parallel lines cut by a transversal</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def bpt_triangle_svg(ad=4, db=2, ae=6, ec=3, blank=False, **kw):
    """Triangle with DE parallel to BC (D on AB, E on AC), illustrating
    the Basic Proportionality Theorem: AD/DB = AE/EC. blank=True hides
    the EC label (the usual unknown), keeping AD/DB/AE visible."""
    w, h = 320, 300
    ax, ay = 160, 45
    bx, by = 40, 260
    cx, cy = 280, 260
    frac = ad / (ad + db)
    dx, dy = ax + (bx - ax) * frac, ay + (by - ay) * frac
    ex, ey = ax + (cx - ax) * frac, ay + (cy - ay) * frac
    parts = []
    parts.append(f'<polygon points="{ax},{ay} {bx},{by} {cx},{cy}" fill="none" stroke="#2C3E50" stroke-width="2.5"/>')
    parts.append(f'<line x1="{dx:.1f}" y1="{dy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#1B5E8C" stroke-width="2.5" stroke-dasharray="5,3"/>')
    for (px, py, lbl) in [(ax, ay, "A"), (bx, by, "B"), (cx, cy, "C"), (dx, dy, "D"), (ex, ey, "E")]:
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="#A6362B"/>')
        if lbl == "A":
            lx, ly = px, py + 18
        elif lbl in ("B", "D"):
            lx, ly = px - 14, py + (16 if lbl == "B" else -10)
        else:
            lx, ly = px + 14, py + (16 if lbl == "C" else -10)
        parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{lbl}</text>')
    parts.append(f'<text x="{(ax+dx)/2-20:.1f}" y="{(ay+dy)/2:.1f}" font-family="Helvetica-Bold" font-size="11" fill="#1E7A44">{ad}</text>')
    parts.append(f'<text x="{(dx+bx)/2-20:.1f}" y="{(dy+by)/2:.1f}" font-family="Helvetica-Bold" font-size="11" fill="#1E7A44">{db}</text>')
    parts.append(f'<text x="{(ax+ex)/2+10:.1f}" y="{(ay+ey)/2:.1f}" font-family="Helvetica-Bold" font-size="11" fill="#1E7A44">{ae}</text>')
    ec_str = "?" if blank else str(ec)
    parts.append(f'<text x="{(ex+cx)/2+10:.1f}" y="{(ey+cy)/2:.1f}" font-family="Helvetica-Bold" font-size="11" fill="#1E7A44">{ec_str}</text>')
    parts.insert(0, f'<text x="{w/2}" y="18" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">DE || BC:  AD/DB = AE/EC</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


_QUAD_SHAPES = {
    "parallelogram": {"pts": [(60, 220), (200, 220), (240, 80), (100, 80)], "ticks": [(0, 1, 1), (2, 3, 1), (1, 2, 2), (3, 0, 2)], "right_angles": []},
    "rectangle":     {"pts": [(60, 220), (260, 220), (260, 80), (60, 80)], "ticks": [(0, 1, 1), (2, 3, 1), (1, 2, 2), (3, 0, 2)], "right_angles": [0, 1, 2, 3]},
    "rhombus":       {"pts": [(160, 230), (240, 150), (160, 70), (80, 150)], "ticks": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1)], "right_angles": []},
    "square":        {"pts": [(80, 220), (240, 220), (240, 60), (80, 60)], "ticks": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1)], "right_angles": [0, 1, 2, 3]},
    "trapezium":     {"pts": [(60, 220), (260, 220), (200, 80), (120, 80)], "ticks": [], "right_angles": []},
    "kite":          {"pts": [(160, 230), (225, 145), (160, 60), (95, 145)], "ticks": [(0, 1, 1), (1, 2, 1), (2, 3, 2), (3, 0, 2)], "right_angles": []},
}


def _side_ticks(p1, p2, n):
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    length = (dx ** 2 + dy ** 2) ** 0.5 or 1
    ux, uy = -dy / length, dx / length
    out = []
    for i in range(n):
        off = (i - (n - 1) / 2) * 7
        cx_, cy_ = mx + ux * 0 + (dx / length) * off, my + uy * 0 + (dy / length) * off
        out.append(f'<line x1="{cx_-ux*6:.1f}" y1="{cy_-uy*6:.1f}" x2="{cx_+ux*6:.1f}" y2="{cy_+uy*6:.1f}" stroke="#B7950B" stroke-width="2"/>')
    return "".join(out)


def quadrilateral_types_svg(kind="parallelogram", **kw):
    """Draws the given quadrilateral type with tick marks for equal
    sides and right-angle marks where applicable."""
    cfg = _QUAD_SHAPES.get(kind, _QUAD_SHAPES["parallelogram"])
    pts = cfg["pts"]
    w, h = 320, 280
    parts = []
    poly = " ".join(f"{x},{y}" for x, y in pts)
    parts.append(f'<polygon points="{poly}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    for i, j, n in cfg["ticks"]:
        parts.append(_side_ticks(pts[i], pts[j], n))
    for vi in cfg["right_angles"]:
        x, y = pts[vi]
        parts.append(f'<rect x="{x-10}" y="{y-10}" width="10" height="10" fill="none" stroke="#7F8C8D" stroke-width="1.3"/>')
    vertex_labels = ["A", "B", "C", "D"]
    for (x, y), lbl in zip(pts, vertex_labels):
        parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#A6362B"/>')
        ly = y - 12 if y < 150 else y + 18
        parts.append(f'<text x="{x}" y="{ly}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">{lbl}</text>')
    parts.insert(0, f'<text x="{w/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{kind.title()}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def quadrilateral_diagonals_svg(kind="parallelogram", **kw):
    """Draws the given quadrilateral with its diagonals, marking the
    intersection point -- for bisection/perpendicularity properties."""
    cfg = _QUAD_SHAPES.get(kind, _QUAD_SHAPES["parallelogram"])
    pts = cfg["pts"]
    w, h = 320, 280
    parts = []
    poly = " ".join(f"{x},{y}" for x, y in pts)
    parts.append(f'<polygon points="{poly}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<line x1="{pts[0][0]}" y1="{pts[0][1]}" x2="{pts[2][0]}" y2="{pts[2][1]}" stroke="#A6362B" stroke-width="2" stroke-dasharray="5,3"/>')
    parts.append(f'<line x1="{pts[1][0]}" y1="{pts[1][1]}" x2="{pts[3][0]}" y2="{pts[3][1]}" stroke="#1E7A44" stroke-width="2" stroke-dasharray="5,3"/>')
    (ax_, ay_), (cx_, cy_) = pts[0], pts[2]
    (bx_, by_), (dx_, dy_) = pts[1], pts[3]
    denom = (ax_ - cx_) * (by_ - dy_) - (ay_ - cy_) * (bx_ - dx_)
    if abs(denom) > 1e-9:
        t = ((ax_ - bx_) * (by_ - dy_) - (ay_ - by_) * (bx_ - dx_)) / denom
        ox = ax_ + t * (cx_ - ax_)
        oy = ay_ + t * (cy_ - ay_)
    else:
        ox, oy = (ax_ + cx_) / 2, (ay_ + cy_) / 2
    parts.append(f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="4.5" fill="#7D3C98"/>')
    vertex_labels = ["A", "B", "C", "D"]
    for (x, y), lbl in zip(pts, vertex_labels):
        parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#2C3E50"/>')
        ly = y - 12 if y < 150 else y + 18
        parts.append(f'<text x="{x}" y="{ly}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">{lbl}</text>')
    parts.insert(0, f'<text x="{w/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{kind.title()} -- diagonals AC and BD</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def polygon_angle_sum_svg(n=5, **kw):
    """A regular n-gon triangulated from one vertex -- the standard
    visual proof that interior angle sum = (n-2) x 180."""
    import math as _m
    w, h = 320, 320
    cx, cy, r = 160, 168, 108
    pts = []
    for i in range(n):
        ang = -_m.pi / 2 + i * 2 * _m.pi / n
        pts.append((cx + r * _m.cos(ang), cy + r * _m.sin(ang)))
    parts = []
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    parts.append(f'<polygon points="{poly}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    x0, y0 = pts[0]
    for i in range(2, n - 1):
        xi, yi = pts[i]
        parts.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{xi:.1f}" y2="{yi:.1f}" stroke="#A6362B" stroke-width="1.5" stroke-dasharray="4,3"/>')
    for x, y in pts:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#1E7A44"/>')
    n_tri = n - 2
    cap = f"{n}-gon: {n_tri} triangles x 180 = {n_tri*180}"
    parts.insert(0, f'<text x="{w/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{cap}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def _angle_wedge(vx, vy, ang1, ang2, radius, color="#A6362B", width=2):
    """Small polyline arc at vertex (vx,vy) sweeping the shorter way
    from ang1 to ang2 (degrees, screen convention: 0=east, 90=south) --
    used to mark an angle at a vertex."""
    import math as _m
    d = (ang2 - ang1) % 360
    if d > 180:
        d -= 360
    steps = 10
    pts = []
    for i in range(steps + 1):
        a = _m.radians(ang1 + d * i / steps)
        pts.append((vx + radius * _m.cos(a), vy + radius * _m.sin(a)))
    path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="{width}"/>'


def _right_angle_mark(vx, vy, u1x, u1y, u2x, u2y, size=10, color="#7F8C8D"):
    """Small square-corner mark at (vx,vy) between two unit directions
    u1 and u2 -- used to flag a 90-degree angle."""
    p1 = (vx + u1x * size, vy + u1y * size)
    p2 = (vx + u1x * size + u2x * size, vy + u1y * size + u2y * size)
    p3 = (vx + u2x * size, vy + u2y * size)
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in [p1, p2, p3])
    return f'<polyline points="{poly}" fill="none" stroke="{color}" stroke-width="1.3"/>'


def _angle_between_vectors(v1, v2):
    import math as _m
    d1, d2 = _m.hypot(*v1), _m.hypot(*v2)
    cosv = (v1[0] * v2[0] + v1[1] * v2[1]) / (d1 * d2 or 1)
    cosv = max(-1.0, min(1.0, cosv))
    return _m.degrees(_m.acos(cosv))


def circle_basics_svg(r=100, **kw):
    """Labeled circle showing the centre O, a radius OB and a diameter
    AB -- the foundation diagram for Level 17C (circle basics)."""
    w, h = 320, 280
    cx, cy = 160, 150
    parts = []
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="#2C3E50"/>')
    parts.append(f'<text x="{cx-14}" y="{cy-8}" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">O</text>')
    rx, ry = cx + r, cy
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{rx}" y2="{ry}" stroke="#A6362B" stroke-width="2.5"/>')
    parts.append(f'<circle cx="{rx}" cy="{ry}" r="3.5" fill="#A6362B"/>')
    parts.append(f'<text x="{(cx+rx)/2}" y="{cy-10}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">r</text>')
    parts.append(f'<text x="{rx+8}" y="{ry+4}" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">B</text>')
    dx1 = cx - r
    parts.append(f'<line x1="{dx1}" y1="{cy}" x2="{rx}" y2="{cy}" stroke="#1E7A44" stroke-width="1.6" stroke-dasharray="6,3"/>')
    parts.append(f'<circle cx="{dx1}" cy="{cy}" r="3.5" fill="#1E7A44"/>')
    parts.append(f'<text x="{dx1-14}" y="{cy+4}" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">A</text>')
    parts.append(f'<text x="{cx}" y="{cy+r+26}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#1E7A44">diameter AB = 2r</text>')
    parts.insert(0, f'<text x="{w/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">Circle: radius &amp; diameter</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def circle_chord_svg(chord_ang1=210, chord_ang2=330, r=100, **kw):
    """Circle with a chord AB and the perpendicular OM from the centre
    to the chord -- shows OM ⊥ AB and AM = MB (Level 17 chords)."""
    import math as _m
    w, h = 320, 280
    cx, cy = 160, 150
    a1, a2 = _m.radians(chord_ang1), _m.radians(chord_ang2)
    ax, ay = cx + r * _m.cos(a1), cy + r * _m.sin(a1)
    bx, by = cx + r * _m.cos(a2), cy + r * _m.sin(a2)
    mx, my = (ax + bx) / 2, (ay + by) / 2
    parts = []
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="#A6362B" stroke-width="2.5"/>')
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{mx:.1f}" y2="{my:.1f}" stroke="#1E7A44" stroke-width="2" stroke-dasharray="5,3"/>')
    ab_len = _m.hypot(bx - ax, by - ay) or 1
    u1x, u1y = (ax - mx) / ab_len * 2, (ay - my) / ab_len * 2
    om_len = _m.hypot(cx - mx, cy - my) or 1
    u2x, u2y = (cx - mx) / om_len, (cy - my) / om_len
    parts.append(_right_angle_mark(mx, my, u1x, u1y, u2x, u2y, size=9))
    parts.append(_side_ticks((ax, ay), (mx, my), 1))
    parts.append(_side_ticks((mx, my), (bx, by), 1))
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="#2C3E50"/>')
    parts.append(f'<text x="{cx-14}" y="{cy-8}" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">O</text>')
    for (x, y), lbl, col in [((ax, ay), "A", "#2C3E50"), ((bx, by), "B", "#2C3E50"), ((mx, my), "M", "#7D3C98")]:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{col}"/>')
        parts.append(f'<text x="{x+8:.1f}" y="{y-6:.1f}" font-family="Helvetica-Bold" font-size="12" fill="{col}">{lbl}</text>')
    parts.insert(0, f'<text x="{w/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="12.5" fill="#2C3E50">Perpendicular from centre bisects the chord</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def circle_tangent_svg(touch_ang=40, r=100, **kw):
    """Circle with a tangent line at point P and radius OP, showing
    tangent ⊥ radius at the point of contact (Level 17 tangents)."""
    import math as _m
    w, h = 320, 320
    cx, cy = 150, 140
    a = _m.radians(touch_ang)
    ux, uy = _m.cos(a), _m.sin(a)
    px, py = cx + r * ux, cy + r * uy
    tx, ty = -uy, ux
    tl = 70
    t1 = (px - tx * tl, py - ty * tl)
    t2 = (px + tx * tl, py + ty * tl)
    parts = []
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="#2C3E50"/>')
    parts.append(f'<text x="{cx-14}" y="{cy-8}" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">O</text>')
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="#A6362B" stroke-width="2.5"/>')
    parts.append(f'<line x1="{t1[0]:.1f}" y1="{t1[1]:.1f}" x2="{t2[0]:.1f}" y2="{t2[1]:.1f}" stroke="#1E7A44" stroke-width="2.5"/>')
    parts.append(_right_angle_mark(px, py, -ux, -uy, tx, ty, size=11))
    parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.5" fill="#7D3C98"/>')
    parts.append(f'<text x="{px+8*ux:.1f}" y="{py+8*uy-6:.1f}" font-family="Helvetica-Bold" font-size="12" fill="#7D3C98">P</text>')
    label_pt = t1 if t1[1] < t2[1] else t2
    lx = min(max(label_pt[0], 40), w - 40)
    ly = min(max(label_pt[1] - 10, 26), h - 14)
    parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-family="Helvetica" font-size="11" fill="#1E7A44">tangent</text>')
    parts.insert(0, f'<text x="{w/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="12.5" fill="#2C3E50">Tangent is perpendicular to the radius</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def circle_central_inscribed_angle_svg(b_ang=210, c_ang=330, a_ang=90, r=100, **kw):
    """Circle showing the central angle BOC and an inscribed angle BAC
    on the same major arc -- angle at centre = 2 x angle at
    circumference (Level 17 circle theorems)."""
    import math as _m
    w, h = 340, 320
    cx, cy = 170, 165
    def pt(deg):
        a = _m.radians(deg)
        return cx + r * _m.cos(a), cy + r * _m.sin(a)
    bx, by = pt(b_ang)
    ccx, ccy = pt(c_ang)
    ax, ay = pt(a_ang)
    parts = []
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{bx:.1f}" y2="{by:.1f}" stroke="#A6362B" stroke-width="2"/>')
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{ccx:.1f}" y2="{ccy:.1f}" stroke="#A6362B" stroke-width="2"/>')
    parts.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="#1E7A44" stroke-width="2"/>')
    parts.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{ccx:.1f}" y2="{ccy:.1f}" stroke="#1E7A44" stroke-width="2"/>')
    ang_ob = _m.degrees(_m.atan2(by - cy, bx - cx))
    ang_oc = _m.degrees(_m.atan2(ccy - cy, ccx - cx))
    ang_ab = _m.degrees(_m.atan2(by - ay, bx - ax))
    ang_ac = _m.degrees(_m.atan2(ccy - ay, ccx - ax))
    parts.append(_angle_wedge(cx, cy, ang_ob, ang_oc, 26, color="#A6362B", width=2.5))
    parts.append(_angle_wedge(ax, ay, ang_ab, ang_ac, 20, color="#1E7A44", width=2.5))
    central = _angle_between_vectors((bx - cx, by - cy), (ccx - cx, ccy - cy))
    inscribed = _angle_between_vectors((bx - ax, by - ay), (ccx - ax, ccy - ay))
    parts.append(f'<text x="{cx:.1f}" y="{cy-34:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">{central:.0f}°</text>')
    parts.append(f'<text x="{ax:.1f}" y="{ay-24:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#1E7A44">{inscribed:.0f}°</text>')
    for (x, y), lbl in [((bx, by), "B"), ((ccx, ccy), "C"), ((ax, ay), "A")]:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#2C3E50"/>')
        parts.append(f'<text x="{x+8:.1f}" y="{y-6:.1f}" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">{lbl}</text>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="#2C3E50"/>')
    parts.append(f'<text x="{cx-14}" y="{cy-8}" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">O</text>')
    parts.insert(0, f'<text x="{w/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">Angle at centre = 2 x angle at circumference</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def cyclic_quadrilateral_theorem_svg(angs=(100, 200, 260, 340), r=100, **kw):
    """Quadrilateral ABCD inscribed in a circle with all four angles
    marked -- shows opposite angles are supplementary (Level 17F)."""
    import math as _m
    w, h = 360, 340
    cx, cy = 180, 175
    def pt(deg):
        a = _m.radians(deg)
        return cx + r * _m.cos(a), cy + r * _m.sin(a)
    pts = [pt(d) for d in angs]
    parts = []
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2"/>')
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    parts.append(f'<polygon points="{poly}" fill="none" stroke="#A6362B" stroke-width="2.5"/>')
    labels = ["A", "B", "C", "D"]
    n = 4
    vals = []
    for i, (x, y) in enumerate(pts):
        prev = pts[(i - 1) % n]
        nxt = pts[(i + 1) % n]
        v1 = (prev[0] - x, prev[1] - y)
        v2 = (nxt[0] - x, nxt[1] - y)
        ang1 = _m.degrees(_m.atan2(v1[1], v1[0]))
        ang2 = _m.degrees(_m.atan2(v2[1], v2[0]))
        col = "#1E7A44" if i in (0, 2) else "#7D3C98"
        parts.append(_angle_wedge(x, y, ang1, ang2, 16, color=col, width=2.2))
        val = _angle_between_vectors(v1, v2)
        vals.append(val)
        dxn, dyn = x - cx, y - cy
        dl = _m.hypot(dxn, dyn) or 1
        # value sits just inside the vertex (toward centre); letter sits outside the circle
        vx, vy = x - dxn / dl * 24, y - dyn / dl * 24
        lblx, lbly = x + dxn / dl * 28, y + dyn / dl * 28
        parts.append(f'<text x="{vx:.1f}" y="{vy:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="{col}">{val:.0f}°</text>')
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#2C3E50"/>')
        parts.append(f'<text x="{lblx:.1f}" y="{lbly:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">{labels[i]}</text>')
    parts.insert(0, f'<text x="{w/2}" y="22" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">Cyclic quadrilateral: opposite angles are supplementary</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def rectangle_dims_svg(length=8, width=5, **kw):
    """A rectangle with length and width labeled via dimension arrows --
    for perimeter / area of rectangle (Level 18A/18B)."""
    w_svg, h_svg = 340, 280
    max_lw, max_lh = 210, 130
    scale = min(max_lw / max(length, 1), max_lh / max(width, 1), 26)
    Lp, Wp = length * scale, width * scale
    ox, oy = (w_svg - Lp) / 2 + 20, 90
    parts = []
    parts.append(f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{Lp:.1f}" height="{Wp:.1f}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    ay = oy + Wp + 22
    parts.append(f'<line x1="{ox:.1f}" y1="{ay:.1f}" x2="{ox+Lp:.1f}" y2="{ay:.1f}" stroke="#A6362B" stroke-width="1.4"/>')
    for xx in (ox, ox + Lp):
        parts.append(f'<line x1="{xx:.1f}" y1="{ay-5:.1f}" x2="{xx:.1f}" y2="{ay+5:.1f}" stroke="#A6362B" stroke-width="1.4"/>')
    parts.append(f'<text x="{ox+Lp/2:.1f}" y="{ay+18:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">length = {length}</text>')
    ax = ox - 18
    parts.append(f'<line x1="{ax:.1f}" y1="{oy:.1f}" x2="{ax:.1f}" y2="{oy+Wp:.1f}" stroke="#1E7A44" stroke-width="1.4"/>')
    for yy in (oy, oy + Wp):
        parts.append(f'<line x1="{ax-5:.1f}" y1="{yy:.1f}" x2="{ax+5:.1f}" y2="{yy:.1f}" stroke="#1E7A44" stroke-width="1.4"/>')
    parts.append(f'<text x="{ax-10:.1f}" y="{oy+Wp/2:.1f}" text-anchor="end" font-family="Helvetica-Bold" font-size="12" fill="#1E7A44">w = {width}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">Rectangle</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def square_dims_svg(side=6, **kw):
    """A square with its side labeled -- for perimeter / area of a
    square (Level 18A/18B)."""
    w_svg, h_svg = 300, 280
    scale = min(160 / max(side, 1), 24)
    S = side * scale
    ox, oy = (w_svg - S) / 2, 80
    parts = []
    parts.append(f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{S:.1f}" height="{S:.1f}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    ay = oy + S + 22
    parts.append(f'<line x1="{ox:.1f}" y1="{ay:.1f}" x2="{ox+S:.1f}" y2="{ay:.1f}" stroke="#A6362B" stroke-width="1.4"/>')
    for xx in (ox, ox + S):
        parts.append(f'<line x1="{xx:.1f}" y1="{ay-5:.1f}" x2="{xx:.1f}" y2="{ay+5:.1f}" stroke="#A6362B" stroke-width="1.4"/>')
    parts.append(f'<text x="{ox+S/2:.1f}" y="{ay+18:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">side = {side}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">Square</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def triangle_area_svg(base=6, height=4, **kw):
    """A triangle with its base and the perpendicular height (dashed
    altitude, right-angle marked) labeled -- Level 18C."""
    w_svg, h_svg = 320, 280
    scale = min(200 / max(base, 1), 140 / max(height, 1), 26)
    Bp, Hp = base * scale, height * scale
    ox, oy = (w_svg - Bp) / 2, 210
    apex_x = ox + Bp * 0.4
    A = (ox, oy)
    B = (ox + Bp, oy)
    C = (apex_x, oy - Hp)
    foot = (apex_x, oy)
    parts = []
    tri = " ".join(f"{x:.1f},{y:.1f}" for x, y in [A, B, C])
    parts.append(f'<polygon points="{tri}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<line x1="{C[0]:.1f}" y1="{C[1]:.1f}" x2="{foot[0]:.1f}" y2="{foot[1]:.1f}" stroke="#1E7A44" stroke-width="1.6" stroke-dasharray="5,3"/>')
    parts.append(_right_angle_mark(foot[0], foot[1], 0, -1, -1 if apex_x > ox else 1, 0, size=9))
    ay = oy + 22
    parts.append(f'<line x1="{A[0]:.1f}" y1="{ay:.1f}" x2="{B[0]:.1f}" y2="{ay:.1f}" stroke="#A6362B" stroke-width="1.4"/>')
    parts.append(f'<text x="{(A[0]+B[0])/2:.1f}" y="{ay+16:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">base = {base}</text>')
    parts.append(f'<text x="{foot[0]+10:.1f}" y="{(C[1]+foot[1])/2:.1f}" font-family="Helvetica-Bold" font-size="12" fill="#1E7A44">height = {height}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">Triangle: base &amp; height</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def circle_area_svg(r=5, **kw):
    """A shaded circle with radius labeled -- for area of a circle
    (Level 18D)."""
    w_svg, h_svg = 300, 280
    scale = min(100 / max(r, 1), 22)
    R = r * scale
    cx, cy = w_svg / 2, 155
    parts = []
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="#2C3E50"/>')
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+R:.1f}" y2="{cy}" stroke="#A6362B" stroke-width="2.5"/>')
    parts.append(f'<text x="{cx+R/2:.1f}" y="{cy-10:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">r = {r}</text>')
    parts.append(f'<text x="{cx}" y="{cy+R+28:.1f}" text-anchor="middle" font-family="Helvetica" font-size="11" fill="#2C3E50">Area = πr²</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">Circle</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def cuboid_3d_svg(l=6, w=4, h=3, title="Cuboid", **kw):
    """Pseudo-3D cuboid (oblique projection, three shaded faces) with
    length, width and height labeled -- Level 18E/18H."""
    import math as _m
    w_svg, h_svg = 360, 320
    scale = min(150 / max(l, 1), 130 / max(h, 1), 90 / max(w, 1), 26)
    Lp, Wp, Hp = l * scale, w * scale, h * scale
    depth_ang = _m.radians(35)
    ddx, ddy = _m.cos(depth_ang) * Wp * 0.65, -_m.sin(depth_ang) * Wp * 0.65
    ox, oy = 70, 250
    A = (ox, oy)
    B = (ox + Lp, oy)
    C = (ox + Lp, oy - Hp)
    D = (ox, oy - Hp)
    A2, B2, C2, D2 = ((p[0] + ddx, p[1] + ddy) for p in (A, B, C, D))
    parts = []
    top = " ".join(f"{x:.1f},{y:.1f}" for x, y in [D, C, C2, D2])
    parts.append(f'<polygon points="{top}" fill="#CFE4F3" stroke="#1B5E8C" stroke-width="2"/>')
    side = " ".join(f"{x:.1f},{y:.1f}" for x, y in [B, C, C2, B2])
    parts.append(f'<polygon points="{side}" fill="#AFCBE3" stroke="#1B5E8C" stroke-width="2"/>')
    front = " ".join(f"{x:.1f},{y:.1f}" for x, y in [A, B, C, D])
    parts.append(f'<polygon points="{front}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<text x="{(A[0]+B[0])/2:.1f}" y="{A[1]+20:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">l = {l}</text>')
    parts.append(f'<text x="{A[0]-14:.1f}" y="{(A[1]+D[1])/2:.1f}" text-anchor="end" font-family="Helvetica-Bold" font-size="12" fill="#1E7A44">h = {h}</text>')
    mx, my = (B[0] + B2[0]) / 2, (B[1] + B2[1]) / 2
    parts.append(f'<text x="{mx+8:.1f}" y="{my-4:.1f}" text-anchor="start" font-family="Helvetica-Bold" font-size="12" fill="#7D3C98">w = {w}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{title}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def cube_3d_svg(side=5, **kw):
    """Pseudo-3D cube (special case of the cuboid) with the side
    labeled -- Level 18E/18H."""
    return cuboid_3d_svg(l=side, w=side, h=side, title="Cube", **kw)


def cuboid_net_svg(l=6, w=4, h=3, **kw):
    """The unfolded net of a cuboid (6 rectangles: 4 around the belt,
    plus top and bottom) -- the standard surface-area teaching visual
    (Level 18E)."""
    w_svg, h_svg = 400, 320
    scale = min(300 / (2 * (l + w)), 220 / (h + 2 * w), 22)
    Lp, Wp, Hp = l * scale, w * scale, h * scale
    total_w = 2 * (Lp + Wp)
    x0 = (w_svg - total_w) / 2
    y0 = (h_svg - (Hp + 2 * Wp)) / 2 + Wp
    faces = [
        ("L", x0, y0, Wp, Hp),
        ("Front (l x h)", x0 + Wp, y0, Lp, Hp),
        ("R", x0 + Wp + Lp, y0, Wp, Hp),
        ("Back", x0 + Wp + Lp + Wp, y0, Lp, Hp),
    ]
    parts = []
    for lbl, fx, fy, fw, fh in faces:
        parts.append(f'<rect x="{fx:.1f}" y="{fy:.1f}" width="{fw:.1f}" height="{fh:.1f}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2"/>')
        if fw > 30:
            parts.append(f'<text x="{fx+fw/2:.1f}" y="{fy+fh/2:.1f}" text-anchor="middle" font-family="Helvetica" font-size="10" fill="#2C3E50">{lbl}</text>')
    top_x, top_y = x0 + Wp, y0 - Wp
    parts.append(f'<rect x="{top_x:.1f}" y="{top_y:.1f}" width="{Lp:.1f}" height="{Wp:.1f}" fill="#CFE4F3" stroke="#1B5E8C" stroke-width="2"/>')
    parts.append(f'<text x="{top_x+Lp/2:.1f}" y="{top_y+Wp/2+4:.1f}" text-anchor="middle" font-family="Helvetica" font-size="10" fill="#2C3E50">Top (l x w)</text>')
    bot_x, bot_y = x0 + Wp, y0 + Hp
    parts.append(f'<rect x="{bot_x:.1f}" y="{bot_y:.1f}" width="{Lp:.1f}" height="{Wp:.1f}" fill="#CFE4F3" stroke="#1B5E8C" stroke-width="2"/>')
    parts.append(f'<text x="{bot_x+Lp/2:.1f}" y="{bot_y+Wp/2+4:.1f}" text-anchor="middle" font-family="Helvetica" font-size="10" fill="#2C3E50">Bottom</text>')
    parts.append(f'<text x="{x0+Wp+Lp/2:.1f}" y="{y0+Hp+Wp+22:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#A6362B">l={l}, w={w}, h={h}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">Net of a cuboid — 6 faces</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def cylinder_3d_svg(r=3, h=6, **kw):
    """Pseudo-3D cylinder (ellipse top/bottom) with radius and height
    labeled -- Level 18F/18H."""
    w_svg, h_svg = 300, 320
    scale = min(70 / max(r, 1), 200 / max(h, 1), 24)
    R, H = r * scale, h * scale
    cx = w_svg / 2
    top_y = 70
    bot_y = top_y + H
    ry = max(R * 0.32, 10)
    parts = []
    parts.append(f'<line x1="{cx-R:.1f}" y1="{top_y:.1f}" x2="{cx-R:.1f}" y2="{bot_y:.1f}" stroke="#1B5E8C" stroke-width="2.2"/>')
    parts.append(f'<line x1="{cx+R:.1f}" y1="{top_y:.1f}" x2="{cx+R:.1f}" y2="{bot_y:.1f}" stroke="#1B5E8C" stroke-width="2.2"/>')
    parts.append(f'<path d="M {cx-R:.1f} {bot_y:.1f} A {R:.1f} {ry:.1f} 0 1 0 {cx+R:.1f} {bot_y:.1f}" fill="#AFCBE3" stroke="#1B5E8C" stroke-width="2"/>')
    parts.append(f'<rect x="{cx-R:.1f}" y="{top_y:.1f}" width="{2*R:.1f}" height="{bot_y-top_y:.1f}" fill="#EAF4FC" opacity="0.001"/>')
    parts.append(f'<ellipse cx="{cx:.1f}" cy="{top_y:.1f}" rx="{R:.1f}" ry="{ry:.1f}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.2"/>')
    parts.append(f'<line x1="{cx:.1f}" y1="{top_y:.1f}" x2="{cx+R:.1f}" y2="{top_y:.1f}" stroke="#A6362B" stroke-width="2"/>')
    parts.append(f'<text x="{cx+R/2:.1f}" y="{top_y-8:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">r = {r}</text>')
    parts.append(f'<line x1="{cx-R-16:.1f}" y1="{top_y:.1f}" x2="{cx-R-16:.1f}" y2="{bot_y:.1f}" stroke="#1E7A44" stroke-width="1.4" stroke-dasharray="4,3"/>')
    parts.append(f'<text x="{cx-R-24:.1f}" y="{(top_y+bot_y)/2:.1f}" text-anchor="end" font-family="Helvetica-Bold" font-size="12" fill="#1E7A44">h = {h}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">Cylinder</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def cone_3d_svg(r=3, h=6, **kw):
    """Pseudo-3D cone (apex + base ellipse) with radius, height (dashed)
    and slant height labeled -- Level 18F/18H."""
    import math as _m
    w_svg, h_svg = 300, 320
    scale = min(70 / max(r, 1), 190 / max(h, 1), 24)
    R, H = r * scale, h * scale
    cx = w_svg / 2
    apex = (cx, 60)
    base_y = apex[1] + H
    ry = max(R * 0.32, 10)
    slant = _m.hypot(r, h)
    parts = []
    parts.append(f'<path d="M {cx-R:.1f} {base_y:.1f} A {R:.1f} {ry:.1f} 0 1 0 {cx+R:.1f} {base_y:.1f}" fill="#AFCBE3" stroke="#1B5E8C" stroke-width="2"/>')
    parts.append(f'<line x1="{apex[0]:.1f}" y1="{apex[1]:.1f}" x2="{cx-R:.1f}" y2="{base_y:.1f}" stroke="#1B5E8C" stroke-width="2.2"/>')
    parts.append(f'<line x1="{apex[0]:.1f}" y1="{apex[1]:.1f}" x2="{cx+R:.1f}" y2="{base_y:.1f}" stroke="#1B5E8C" stroke-width="2.2"/>')
    parts.append(f'<ellipse cx="{cx:.1f}" cy="{base_y:.1f}" rx="{R:.1f}" ry="{ry:.1f}" fill="none" stroke="#1B5E8C" stroke-width="1.4" stroke-dasharray="4,3"/>')
    parts.append(f'<line x1="{cx:.1f}" y1="{apex[1]:.1f}" x2="{cx:.1f}" y2="{base_y:.1f}" stroke="#1E7A44" stroke-width="1.4" stroke-dasharray="4,3"/>')
    parts.append(f'<text x="{cx-10:.1f}" y="{(apex[1]+base_y)/2:.1f}" text-anchor="end" font-family="Helvetica-Bold" font-size="12" fill="#1E7A44">h = {h}</text>')
    slant_mx, slant_my = apex[0] + 0.6 * (cx + R - apex[0]), apex[1] + 0.6 * (base_y - apex[1])
    parts.append(f'<text x="{slant_mx+12:.1f}" y="{slant_my:.1f}" text-anchor="start" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">l = {slant:.1f}</text>')
    parts.append(f'<line x1="{cx:.1f}" y1="{base_y:.1f}" x2="{cx+R:.1f}" y2="{base_y:.1f}" stroke="#7D3C98" stroke-width="2"/>')
    parts.append(f'<text x="{cx+R/2:.1f}" y="{base_y+18:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#7D3C98">r = {r}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">Cone</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def sphere_3d_svg(r=4, **kw):
    """A shaded sphere with an equator ellipse (to suggest roundness)
    and radius labeled -- Level 18G."""
    w_svg, h_svg = 300, 280
    scale = min(90 / max(r, 1), 22)
    R = r * scale
    cx, cy = w_svg / 2, 150
    parts = []
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{R:.1f}" ry="{R*0.3:.1f}" fill="none" stroke="#1B5E8C" stroke-width="1.4" stroke-dasharray="4,3"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="#2C3E50"/>')
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+R*0.7:.1f}" y2="{cy-R*0.7:.1f}" stroke="#A6362B" stroke-width="2.5"/>')
    parts.append(f'<text x="{cx+R*0.35:.1f}" y="{cy-R*0.42:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">r = {r}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">Sphere</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def hemisphere_3d_svg(r=4, **kw):
    """A hemisphere -- dome (half-circle arc) on a flat circular (drawn
    as an ellipse) base -- with radius labeled -- Level 18G."""
    w_svg, h_svg = 300, 260
    scale = min(90 / max(r, 1), 22)
    R = r * scale
    cx, base_y = w_svg / 2, 160
    ry = max(R * 0.3, 8)
    parts = []
    parts.append(f'<path d="M {cx-R:.1f} {base_y:.1f} A {R:.1f} {R:.1f} 0 0 1 {cx+R:.1f} {base_y:.1f}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<ellipse cx="{cx}" cy="{base_y}" rx="{R:.1f}" ry="{ry:.1f}" fill="#CFE4F3" stroke="#1B5E8C" stroke-width="2.2"/>')
    parts.append(f'<circle cx="{cx}" cy="{base_y}" r="3.5" fill="#2C3E50"/>')
    parts.append(f'<line x1="{cx}" y1="{base_y}" x2="{cx+R:.1f}" y2="{base_y}" stroke="#A6362B" stroke-width="2.5"/>')
    parts.append(f'<text x="{cx+R/2:.1f}" y="{base_y-8:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">r = {r}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">Hemisphere</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def composite_mensuration_svg(l=10, w=4, **kw):
    """A rectangle with a semicircular cap on the right end (a
    'stadium' shape) -- for composite / mixed mensuration problems
    (Level 18I)."""
    w_svg, h_svg = 340, 260
    scale = min(200 / max(l, 1), 100 / max(w, 1), 22)
    Lp, Wp = l * scale, w * scale
    ox, oy = 66, 100
    rad = Wp / 2
    parts = []
    parts.append(f'<path d="M {ox:.1f} {oy:.1f} L {ox+Lp:.1f} {oy:.1f} A {rad:.1f} {rad:.1f} 0 0 1 {ox+Lp:.1f} {oy+Wp:.1f} L {ox:.1f} {oy+Wp:.1f} Z" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    ay = oy + Wp + 22
    parts.append(f'<line x1="{ox:.1f}" y1="{ay:.1f}" x2="{ox+Lp:.1f}" y2="{ay:.1f}" stroke="#A6362B" stroke-width="1.4"/>')
    parts.append(f'<text x="{ox+Lp/2:.1f}" y="{ay+18:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">l = {l}</text>')
    ax = ox - 18
    parts.append(f'<line x1="{ax:.1f}" y1="{oy:.1f}" x2="{ax:.1f}" y2="{oy+Wp:.1f}" stroke="#1E7A44" stroke-width="1.4"/>')
    parts.append(f'<text x="{ax-10:.1f}" y="{oy+Wp/2:.1f}" text-anchor="end" font-family="Helvetica-Bold" font-size="12" fill="#1E7A44">w = {w}</text>')
    parts.append(f'<text x="{ox+Lp+8:.1f}" y="{oy+Wp/2:.1f}" font-family="Helvetica-Bold" font-size="11" fill="#7D3C98">r = {w/2:g}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">Composite shape: rectangle + semicircle</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def circle_sector_svg(r=7, angle=90, **kw):
    """A circle with one sector (pie-slice) shaded and the radius and
    angle labeled -- for sector-area questions (Level 18D)."""
    import math as _m
    w_svg, h_svg = 300, 280
    scale = min(100 / max(r, 1), 22)
    R = r * scale
    cx, cy = w_svg / 2, 155
    a1 = -90.0
    a2 = a1 + angle
    p1 = (cx + R * _m.cos(_m.radians(a1)), cy + R * _m.sin(_m.radians(a1)))
    p2 = (cx + R * _m.cos(_m.radians(a2)), cy + R * _m.sin(_m.radians(a2)))
    large = 1 if angle > 180 else 0
    parts = []
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="none" stroke="#1B5E8C" stroke-width="2"/>')
    parts.append(f'<path d="M {cx:.1f} {cy:.1f} L {p1[0]:.1f} {p1[1]:.1f} A {R:.1f} {R:.1f} 0 {large} 1 {p2[0]:.1f} {p2[1]:.1f} Z" fill="#AFCBE3" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="#2C3E50"/>')
    mid_a = _m.radians((a1 + a2) / 2)
    lx, ly = cx + R * 0.55 * _m.cos(mid_a), cy + R * 0.55 * _m.sin(mid_a)
    parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">{angle:g}°</text>')
    parts.append(f'<text x="{(cx+p1[0])/2-10:.1f}" y="{(cy+p1[1])/2:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#1E7A44">r={r:g}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">Sector</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def circle_ring_svg(outer_r=14, inner_r=7, **kw):
    """Two concentric circles (an annulus/ring) with outer and inner
    radii labeled -- for ring-area questions (Level 18D)."""
    w_svg, h_svg = 300, 280
    scale = min(90 / max(outer_r, 1), 20)
    R, rr = outer_r * scale, inner_r * scale
    cx, cy = w_svg / 2, 155
    parts = []
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="#AFCBE3" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{rr:.1f}" fill="white" stroke="#1B5E8C" stroke-width="2"/>')
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+R:.1f}" y2="{cy}" stroke="#A6362B" stroke-width="2"/>')
    parts.append(f'<text x="{cx+R/2:.1f}" y="{cy-8:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#A6362B">R = {outer_r:g}</text>')
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+rr:.1f}" y2="{cy+16:.1f}" stroke="#1E7A44" stroke-width="2"/>')
    parts.append(f'<text x="{cx+rr/2:.1f}" y="{cy+30:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#1E7A44">r = {inner_r:g}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">Ring (Annulus)</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def factor_array_svg(n=12, rows=3, cols=4, blank=False, **kw):
    """A rectangular array (rows x cols grid) showing that rows and cols
    are a factor pair of n -- the array model for factors (Level 9A).
    blank=True hides the grid/caption, leaving just an empty box for the
    student to sketch and work out themselves."""
    w_svg, h_svg = 380, 300
    if blank:
        parts = []
        bw, bh = 220, 150
        ox, oy = (w_svg - bw) / 2, (h_svg - bh) / 2 + 10
        parts.append(f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{bw}" height="{bh}" fill="#FAFBFC" stroke="#1B5E8C" stroke-width="2.5" stroke-dasharray="8,5"/>')
        parts.append(f'<text x="{w_svg/2}" y="{oy+bh+30:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#A6362B">n = {n}: sketch an array (rows x cols)</text>')
        parts.insert(0, f'<text x="{w_svg/2}" y="28" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">Array model of {n}</text>')
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"
    cell = min(220 / max(cols, 1), 150 / max(rows, 1), 34)
    gw, gh = cols * cell, rows * cell
    ox, oy = (w_svg - gw) / 2, (h_svg - gh) / 2 + 6
    parts = []
    for r in range(int(rows)):
        for c in range(int(cols)):
            x = ox + c * cell
            y = oy + r * cell
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell:.1f}" height="{cell:.1f}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2"/>')
    parts.append(f'<text x="{w_svg/2}" y="{oy+gh+32:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#A6362B">{rows} rows x {cols} cols = {n}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="28" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">Array model of {n}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def factor_rainbow_svg(n=12, blank=False, **kw):
    """A number line 1..n with arcs ('rainbows') connecting each factor
    pair -- the classic factor-rainbow visual (Level 9A). blank=True
    shows only the number line, no arcs, so the student draws them."""
    n = int(n)
    factors = [d for d in range(1, n + 1) if n % d == 0]
    w_svg = min(max(420, 26 * n + 100), 720)
    h_svg = 280
    ox = 50
    step = (w_svg - 2 * ox) / max(n - 1, 1)
    y_line = 190
    parts = []
    parts.append(f'<line x1="{ox}" y1="{y_line}" x2="{w_svg-ox}" y2="{y_line}" stroke="#1B5E8C" stroke-width="3"/>')
    for i in range(1, n + 1):
        x = ox + (i - 1) * step
        parts.append(f'<line x1="{x:.1f}" y1="{y_line-7}" x2="{x:.1f}" y2="{y_line+7}" stroke="#1B5E8C" stroke-width="2"/>')
        parts.append(f'<text x="{x:.1f}" y="{y_line+26}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{i}</text>')
    if blank:
        parts.append(f'<text x="{w_svg/2}" y="{y_line-100:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#A6362B">Draw an arc for each factor pair of {n}</text>')
        parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">Factor rainbow for {n}</text>')
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"
    colors = ["#A6362B", "#1E7A44", "#7D3C98", "#B8860B", "#1B5E8C"]
    pairs = [(f, n // f) for f in factors if f <= n // f]
    for idx, (a, b) in enumerate(pairs):
        xa = ox + (a - 1) * step
        xb = ox + (b - 1) * step
        rx = max((xb - xa) / 2, 1)
        ry = min(30 + idx * 16, 160)
        col = colors[idx % len(colors)]
        parts.append(f'<path d="M {xa:.1f} {y_line:.1f} A {rx:.1f} {ry:.1f} 0 0 1 {xb:.1f} {y_line:.1f}" fill="none" stroke="{col}" stroke-width="3"/>')
    parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">Factor rainbow for {n}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def multiples_number_line_svg(n=6, count=8, blank=False, **kw):
    """A number line marking the first several multiples of n --
    a skip-counting visual (Level 9B). blank=True shows only the bare
    number line (start/end labeled), no multiples marked."""
    n, count = int(n), int(count)
    top = n * count
    w_svg, h_svg = 460, 200
    ox, oy = 40, 110
    step = (w_svg - 2 * ox) / max(top, 1)
    parts = []
    parts.append(f'<line x1="{ox}" y1="{oy}" x2="{w_svg-ox}" y2="{oy}" stroke="#1B5E8C" stroke-width="3"/>')
    if blank:
        for i in (0, top):
            x = ox + i * step
            parts.append(f'<line x1="{x:.1f}" y1="{oy-10}" x2="{x:.1f}" y2="{oy+10}" stroke="#1B5E8C" stroke-width="2.5"/>')
            parts.append(f'<text x="{x:.1f}" y="{oy+32}" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#2C3E50">{i}</text>')
        parts.append(f'<text x="{w_svg/2}" y="{oy-40:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#A6362B">Mark the multiples of {n} on the line</text>')
        parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">Multiples of {n}</text>')
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"
    show_minor = top <= 30
    for i in range(0, top + 1):
        is_mult = (i % n == 0)
        if not is_mult and not show_minor:
            continue
        x = ox + i * step
        h = 12 if is_mult else 6
        col = "#A6362B" if is_mult else "#9AA5B1"
        parts.append(f'<line x1="{x:.1f}" y1="{oy-h}" x2="{x:.1f}" y2="{oy+h}" stroke="{col}" stroke-width="{2.5 if is_mult else 1.4}"/>')
        if is_mult:
            parts.append(f'<circle cx="{x:.1f}" cy="{oy}" r="5" fill="#A6362B"/>')
            parts.append(f'<text x="{x:.1f}" y="{oy+32}" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#A6362B">{i}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">Multiples of {n}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def hundred_grid_highlight_svg(n=None, highlight=None, blank=False, **kw):
    """A 1-100 grid with certain numbers highlighted -- multiples of n
    if n is given, otherwise the explicit highlight list (also usable
    for a prime-sieve view) (Level 9B/9C). blank=True shows the plain
    numbered grid with nothing highlighted."""
    if highlight is None and n:
        highlight = list(range(int(n), 101, int(n)))
    highlight = set(highlight or [])
    w_svg, h_svg = 420, 470
    cell = 37
    ox, oy = (w_svg - 10 * cell) / 2, 65
    parts = []
    for i in range(1, 101):
        r, c = (i - 1) // 10, (i - 1) % 10
        x, y = ox + c * cell, oy + r * cell
        is_hi = (not blank) and i in highlight
        fill = "#A6362B" if is_hi else "#EAF4FC"
        txt_col = "white" if is_hi else "#2C3E50"
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" fill="{fill}" stroke="#1B5E8C" stroke-width="1"/>')
        parts.append(f'<text x="{x+cell/2:.1f}" y="{y+cell/2+5:.1f}" text-anchor="middle" font-family="Helvetica" font-size="13" fill="{txt_col}">{i}</text>')
    if blank:
        title = f"Shade the multiples of {n} up to 100" if n else "Shade the requested numbers"
    else:
        title = f"Multiples of {n} up to 100" if n else "Highlighted numbers"
    parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">{title}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def ladder_division_svg(a=24, b=36, mode="hcf", blank=False, **kw):
    """The 'ladder' (cake) method: repeatedly divide two numbers by a
    common prime, shown as steps down a ladder -- used to find HCF or
    LCM (Level 9D/9E/9G). blank=True shows only the starting row and
    empty ladder rows for the student to complete themselves."""
    a, b = int(a), int(b)

    def _common_prime(x, y):
        d = 2
        while d <= min(x, y):
            if x % d == 0 and y % d == 0:
                return d
            d += 1
        return None

    if blank:
        n_blank_rows = 4
        w_svg = 320
        row_h = 46
        h_svg = 90 + row_h * n_blank_rows + 65
        ox, oy = 120, 90
        parts = []
        parts.append(f'<line x1="{ox-20:.1f}" y1="{oy-18:.1f}" x2="{ox-20:.1f}" y2="{oy+row_h*n_blank_rows-18:.1f}" stroke="#1B5E8C" stroke-width="2.5"/>')
        parts.append(f'<line x1="{ox-20:.1f}" y1="{oy-18:.1f}" x2="{ox+110:.1f}" y2="{oy-18:.1f}" stroke="#1B5E8C" stroke-width="2"/>')
        parts.append(f'<text x="{ox+28:.1f}" y="{oy:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="18" fill="#2C3E50">{a}</text>')
        parts.append(f'<text x="{ox+86:.1f}" y="{oy:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="18" fill="#2C3E50">{b}</text>')
        for i in range(1, n_blank_rows):
            ry = oy + i * row_h
            parts.append(f'<line x1="{ox-20:.1f}" y1="{ry-18:.1f}" x2="{ox+110:.1f}" y2="{ry-18:.1f}" stroke="#1B5E8C" stroke-width="1.6" stroke-dasharray="5,4"/>')
        caption = ("Divide both numbers by a common prime, row by row.\nMultiply the divisors (left) to find the HCF." if mode == "hcf"
                   else "Divide both numbers by a common prime, row by row.\nMultiply divisors x the final row to find the LCM.")
        ty = oy + row_h * n_blank_rows + 14
        for j, line in enumerate(caption.split("\n")):
            parts.append(f'<text x="{w_svg/2}" y="{ty+j*16:.1f}" text-anchor="middle" font-family="Helvetica" font-size="12" fill="#1E7A44">{line}</text>')
        parts.insert(0, f'<text x="{w_svg/2}" y="28" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">Ladder method: {a} and {b}</text>')
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"

    rows = []
    x, y = a, b
    while True:
        d = _common_prime(x, y)
        if not d:
            break
        rows.append((d, x, y))
        x, y = x // d, y // d
    rows.append((None, x, y))
    w_svg = 320
    row_h = 40
    h_svg = 90 + row_h * len(rows) + 65
    ox, oy = 120, 90
    parts = []
    parts.append(f'<line x1="{ox-20:.1f}" y1="{oy-18:.1f}" x2="{ox-20:.1f}" y2="{oy+row_h*len(rows)-18:.1f}" stroke="#1B5E8C" stroke-width="2.5"/>')
    for i, (d, xx, yy) in enumerate(rows):
        ry = oy + i * row_h
        parts.append(f'<line x1="{ox-20:.1f}" y1="{ry-18:.1f}" x2="{ox+110:.1f}" y2="{ry-18:.1f}" stroke="#1B5E8C" stroke-width="2"/>')
        if d:
            parts.append(f'<text x="{ox-38:.1f}" y="{ry:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#A6362B">{d}</text>')
        parts.append(f'<text x="{ox+28:.1f}" y="{ry:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">{xx}</text>')
        parts.append(f'<text x="{ox+86:.1f}" y="{ry:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">{yy}</text>')
    caption = ("Multiply the divisors in the left column to find the HCF." if mode == "hcf"
               else "Multiply the divisors AND the bottom row together to find the LCM.")
    ty = oy + row_h * len(rows) + 22
    parts.append(f'<text x="{w_svg/2}" y="{ty:.1f}" text-anchor="middle" font-family="Helvetica" font-size="12.5" fill="#1E7A44">{caption}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="28" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">Ladder method: {a} and {b}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def euclidean_algorithm_svg(a=48, b=18, blank=False, **kw):
    """The Euclidean algorithm's repeated-division steps (a = b*q + r)
    shown as a ladder of equations down to remainder 0 (Level 9H).
    blank=True shows only the first equation as a fill-in-the-blank
    template, with empty lines below for the student to continue."""
    a, b = int(a), int(b)
    w_svg, row_h = 420, 34
    if blank:
        h_svg = 90 + row_h * 4 + 55
        ox, oy = 34, 90
        parts = []
        parts.append(f'<text x="{ox:.1f}" y="{oy:.1f}" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">{a} = {b} x ____ + ____</text>')
        for i in range(1, 4):
            ry = oy + i * row_h
            parts.append(f'<line x1="{ox:.1f}" y1="{ry:.1f}" x2="{w_svg-ox:.1f}" y2="{ry:.1f}" stroke="#9AA5B1" stroke-width="1.4" stroke-dasharray="5,4"/>')
        parts.append(f'<text x="{ox:.1f}" y="{oy+row_h*4+16:.1f}" font-family="Helvetica" font-size="12.5" fill="#1E7A44">Keep dividing (bigger = smaller x q + r) until r = 0 --</text>')
        parts.append(f'<text x="{ox:.1f}" y="{oy+row_h*4+32:.1f}" font-family="Helvetica" font-size="12.5" fill="#1E7A44">the last non-zero remainder is the HCF.</text>')
        parts.insert(0, f'<text x="{w_svg/2}" y="28" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">Euclidean Algorithm: HCF({a},{b})</text>')
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"
    steps = []
    x, y = a, b
    while y != 0:
        qq, r = x // y, x % y
        steps.append((x, y, qq, r))
        x, y = y, r
    h_svg = 80 + row_h * len(steps) + 75
    ox, oy = 34, 80
    parts = []
    for i, (xx, yy, qq, r) in enumerate(steps):
        ry = oy + i * row_h
        parts.append(f'<text x="{ox:.1f}" y="{ry:.1f}" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">{xx} = {yy} x {qq} + {r}</text>')
    parts.append(f'<text x="{ox:.1f}" y="{oy+row_h*len(steps)+22:.1f}" font-family="Helvetica" font-size="12.5" fill="#1E7A44">Keep going until the remainder is 0 --</text>')
    parts.append(f'<text x="{ox:.1f}" y="{oy+row_h*len(steps)+40:.1f}" font-family="Helvetica" font-size="12.5" fill="#1E7A44">the last non-zero remainder is the HCF.</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="28" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">Euclidean Algorithm: HCF({a},{b})</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def ratio_objects_svg(a=3, b=5, label_a="Red", label_b="Blue", blank=False, **kw):
    """A grid of coloured squares showing a:b as actual counted objects
    -- the concrete concept behind a ratio (Level 10A). blank=True shows
    (a+b) empty outlined squares only, for the student to colour in."""
    a, b = int(a), int(b)
    total = a + b
    cols = min(total, 8)
    rows = -(-total // cols)
    cell = 46
    w_svg = max(360, cols * cell + 80)
    h_svg = 90 + rows * cell + 70
    ox, oy = (w_svg - cols * cell) / 2, 80
    parts = []
    for i in range(total):
        r, c = i // cols, i % cols
        x, y = ox + c * cell, oy + r * cell
        if blank:
            fill = "#FAFBFC"
        else:
            fill = "#C0392B" if i < a else "#1B5E8C"
        parts.append(f'<rect x="{x+4:.1f}" y="{y+4:.1f}" width="{cell-8}" height="{cell-8}" rx="6" fill="{fill}" stroke="#2C3E50" stroke-width="2"/>')
    cap_y = oy + rows * cell + 34
    if blank:
        parts.append(f'<text x="{w_svg/2}" y="{cap_y:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#A6362B">Colour {a} squares for "{label_a}" and {b} for "{label_b}"</text>')
    else:
        parts.append(f'<rect x="{w_svg/2-70:.1f}" y="{cap_y-16:.1f}" width="16" height="16" fill="#C0392B"/>')
        parts.append(f'<text x="{w_svg/2-50:.1f}" y="{cap_y-3:.1f}" font-family="Helvetica-Bold" font-size="14" fill="#2C3E50">{label_a} = {a}</text>')
        parts.append(f'<rect x="{w_svg/2+30:.1f}" y="{cap_y-16:.1f}" width="16" height="16" fill="#1B5E8C"/>')
        parts.append(f'<text x="{w_svg/2+50:.1f}" y="{cap_y-3:.1f}" font-family="Helvetica-Bold" font-size="14" fill="#2C3E50">{label_b} = {b}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">Ratio as objects: {label_a} to {label_b}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def ratio_table_svg(a=2, b=3, cols=4, blank=False, **kw):
    """An equivalent-ratios table: a row of multiples of a above a row
    of multiples of b, column-aligned -- shows a:b, 2a:2b, 3a:3b, ...
    (Level 10C). blank=True fills only the first (given) column."""
    a, b, cols = int(a), int(b), int(cols)
    w_svg = 90 + cols * 90
    h_svg = 260
    ox, oy = 90, 90
    cw = 90
    parts = []
    parts.append(f'<text x="30" y="{oy+8:.1f}" font-family="Helvetica-Bold" font-size="16" fill="#A6362B">A</text>')
    parts.append(f'<text x="30" y="{oy+cw-2:.1f}" font-family="Helvetica-Bold" font-size="16" fill="#1E7A44">B</text>')
    for i in range(cols):
        x = ox + i * cw
        parts.append(f'<rect x="{x:.1f}" y="{oy-30:.1f}" width="{cw}" height="{cw}" fill="none" stroke="#1B5E8C" stroke-width="2"/>')
        parts.append(f'<rect x="{x:.1f}" y="{oy+cw-30:.1f}" width="{cw}" height="{cw}" fill="none" stroke="#1B5E8C" stroke-width="2"/>')
        show = (i == 0) or not blank
        va = a * (i + 1)
        vb = b * (i + 1)
        ta = str(va) if show else "?"
        tb = str(vb) if show else "?"
        parts.append(f'<text x="{x+cw/2:.1f}" y="{oy+8:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="20" fill="#A6362B">{ta}</text>')
        parts.append(f'<text x="{x+cw/2:.1f}" y="{oy+cw-2:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="20" fill="#1E7A44">{tb}</text>')
        parts.append(f'<text x="{x+cw/2:.1f}" y="{oy+2*cw-38:.1f}" text-anchor="middle" font-family="Helvetica" font-size="11" fill="#7D3C98">x{i+1}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">Equivalent ratios: {a}:{b}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def double_number_line_svg(a=3, b=5, steps=5, blank=False, **kw):
    """Two parallel number lines, one scaled in steps of a and the other
    in steps of b, aligned so equivalent ratios line up vertically --
    the classic double-number-line proportion visual (Level 10C/10D).
    blank=True marks only the first (given) pair."""
    a, b, steps = int(a), int(b), int(steps)
    w_svg = max(420, 80 * steps + 100)
    h_svg = 220
    ox = 70
    step_w = (w_svg - 2 * ox) / steps
    y_top, y_bot = 90, 160
    parts = []
    parts.append(f'<line x1="{ox}" y1="{y_top}" x2="{w_svg-ox}" y2="{y_top}" stroke="#A6362B" stroke-width="3"/>')
    parts.append(f'<line x1="{ox}" y1="{y_bot}" x2="{w_svg-ox}" y2="{y_bot}" stroke="#1B5E8C" stroke-width="3"/>')
    for i in range(steps + 1):
        x = ox + i * step_w
        show = (i <= 1) or not blank
        parts.append(f'<line x1="{x:.1f}" y1="{y_top-9}" x2="{x:.1f}" y2="{y_top+9}" stroke="#A6362B" stroke-width="2.5"/>')
        parts.append(f'<line x1="{x:.1f}" y1="{y_bot-9}" x2="{x:.1f}" y2="{y_bot+9}" stroke="#1B5E8C" stroke-width="2.5"/>')
        parts.append(f'<line x1="{x:.1f}" y1="{y_top+9}" x2="{x:.1f}" y2="{y_bot-9}" stroke="#CCCCCC" stroke-width="1" stroke-dasharray="3,3"/>')
        ta = str(a * i) if show else "?"
        tb = str(b * i) if show else "?"
        parts.append(f'<text x="{x:.1f}" y="{y_top-16}" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#A6362B">{ta}</text>')
        parts.append(f'<text x="{x:.1f}" y="{y_bot+26}" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#1B5E8C">{tb}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">Double number line: {a} : {b}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def continued_ratio_bar_svg(parts_list=None, labels=None, total=None, blank=False, **kw):
    """A bar split into segments proportional to a ratio with 2 or more
    terms (e.g. 2:3:4, or a partnership split) -- Level 10CUM1/CUM3.
    blank=True shows an undivided bar with only the ratio and total (if
    given) labeled, for the student to partition themselves."""
    parts_list = parts_list or [2, 3, 4]
    parts_list = [int(p) for p in parts_list]
    n = len(parts_list)
    labels = labels or [chr(65 + i) for i in range(n)]
    tot_parts = sum(parts_list) or 1
    w_svg, h_svg = 460, 230
    bar_w, bar_h = 380, 80
    ox, oy = (w_svg - bar_w) / 2, 80
    colors = ["#A6362B", "#1E7A44", "#7D3C98", "#B8860B", "#1B5E8C"]
    parts = []
    if blank:
        parts.append(f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{bar_w}" height="{bar_h}" fill="#FAFBFC" stroke="#1B5E8C" stroke-width="2.5" stroke-dasharray="8,5"/>')
        ratio_str = ":".join(str(p) for p in parts_list)
        cap = f"Ratio {ratio_str}" + (f"  |  Total = {total}" if total else "")
        parts.append(f'<text x="{w_svg/2}" y="{oy+bar_h+34:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#A6362B">{cap} -- split the bar</text>')
        parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">Bar model: {ratio_str}</text>')
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"
    x = ox
    for i, p in enumerate(parts_list):
        seg_w = bar_w * p / tot_parts
        col = colors[i % len(colors)]
        parts.append(f'<rect x="{x:.1f}" y="{oy:.1f}" width="{seg_w:.1f}" height="{bar_h}" fill="{col}" stroke="#2C3E50" stroke-width="2"/>')
        if seg_w > 30:
            parts.append(f'<text x="{x+seg_w/2:.1f}" y="{oy+bar_h/2+6:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="white">{labels[i]}: {p}</text>')
        x += seg_w
    ratio_str = ":".join(str(p) for p in parts_list)
    cap = f"{ratio_str}  (total = {tot_parts} parts)" + (f", grand total = {total}" if total else "")
    parts.append(f'<text x="{w_svg/2}" y="{oy+bar_h+30:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#2C3E50">{cap}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">Bar model: {ratio_str}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def unit_rate_svg(qty=6, cost=90, qty_unit="items", cost_unit="Rs", blank=False, **kw):
    """Shows 'qty items -> cost' scaled down to '1 item -> unit rate' --
    the standard unitary-method visual (Level 10CUM2 rates). blank=True
    hides the computed unit rate."""
    qty, cost = int(qty), int(cost)
    unit_val = cost / qty if qty else 0
    unit_str = f"{unit_val:g}" if not blank else "____"
    w_svg, h_svg = 400, 220
    parts = []
    parts.append(f'<rect x="40" y="60" width="150" height="60" rx="8" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<text x="115" y="96" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">{qty} {qty_unit} = {cost_unit} {cost}</text>')
    parts.append(f'<line x1="115" y1="120" x2="115" y2="150" stroke="#A6362B" stroke-width="2.5"/>')
    parts.append(f'<polygon points="110,146 120,146 115,155" fill="#A6362B"/>')
    parts.append(f'<text x="128" y="140" font-family="Helvetica" font-size="11" fill="#A6362B">÷ {qty}</text>')
    parts.append(f'<rect x="40" y="150" width="220" height="55" rx="8" fill="#FDEDEC" stroke="#A6362B" stroke-width="2.5"/>')
    parts.append(f'<text x="150" y="184" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#A6362B">1 {qty_unit[:-1] if qty_unit.endswith("s") else qty_unit} = {cost_unit} {unit_str}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">Unit rate (unitary method)</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def similar_figures_svg(w1=4, h1=3, scale=2, blank=False, **kw):
    """Two similar rectangles drawn to proportion, the smaller fully
    labeled and the larger labeled only with the scale factor -- for
    similar-figures / scale-factor questions (Level 10J). blank=True
    also hides the larger rectangle's relationship label."""
    w1, h1, scale = float(w1), float(h1), float(scale)
    w2, h2 = w1 * scale, h1 * scale
    unit = min(220 / max(w2, w1), 120 / max(h2, h1), 30)
    w_svg, h_svg = 420, 260
    ox1, oy1 = 50, 190
    ox2, oy2 = 220, 190
    parts = []
    parts.append(f'<rect x="{ox1:.1f}" y="{oy1-h1*unit:.1f}" width="{w1*unit:.1f}" height="{h1*unit:.1f}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<text x="{ox1+w1*unit/2:.1f}" y="{oy1+16:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#A6362B">{w1:g}</text>')
    parts.append(f'<text x="{ox1-14:.1f}" y="{oy1-h1*unit/2:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#1E7A44">{h1:g}</text>')
    parts.append(f'<rect x="{ox2:.1f}" y="{oy2-h2*unit:.1f}" width="{w2*unit:.1f}" height="{h2*unit:.1f}" fill="#FDEDEC" stroke="#A6362B" stroke-width="2.5"/>')
    if blank:
        w2s, h2s = "?", "?"
    else:
        w2s, h2s = f"{w2:g}", f"{h2:g}"
    parts.append(f'<text x="{ox2+w2*unit/2:.1f}" y="{oy2+16:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#A6362B">{w2s}</text>')
    parts.append(f'<text x="{ox2-14:.1f}" y="{oy2-h2*unit/2:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#1E7A44">{h2s}</text>')
    parts.append(f'<text x="{w_svg/2}" y="{h_svg-24:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#7D3C98">Scale factor = {scale:g}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">Similar figures</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def scale_comparison_svg(real_len=5, real_unit="km", model_len=1, model_unit="cm", blank=False, find="real", **kw):
    """A short 'model' bar next to a long 'real world' bar with the
    scale ratio labeled -- for map/scale-drawing questions (Level 10J).
    blank=True hides whichever length is being asked for (find="real"
    or find="model"), so the other value is always safe to show."""
    w_svg, h_svg = 420, 220
    blank_real = blank and find != "model"
    blank_model = blank and find == "model"
    parts = []
    model_str = "?" if blank_model else f"{model_len:g}"
    parts.append(f'<rect x="40" y="70" width="60" height="30" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<text x="70" y="63" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#1B5E8C">{model_str} {model_unit}</text>')
    parts.append('<text x="70" y="120" text-anchor="middle" font-family="Helvetica" font-size="12" fill="#2C3E50">on the map/drawing</text>')
    real_str = "?" if blank_real else f"{real_len:g}"
    parts.append(f'<rect x="40" y="160" width="340" height="30" fill="#FDEDEC" stroke="#A6362B" stroke-width="2.5"/>')
    parts.append(f'<text x="210" y="153" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#A6362B">{real_str} {real_unit}</text>')
    parts.append('<text x="210" y="210" text-anchor="middle" font-family="Helvetica" font-size="12" fill="#2C3E50">in real life</text>')
    title_val = "?" if blank_real else f"{real_len:g}"
    title_model = "?" if blank_model else f"{model_len:g}"
    parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">Scale: {title_model} {model_unit} = {title_val} {real_unit}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def word_to_expression_svg(phrase="5 more than x", expression="x + 5", blank=False, **kw):
    """Shows a word phrase above its matching algebraic expression, with
    a connecting bracket -- the translation-to-algebra visual (Level
    11B/11G). blank=True hides the expression."""
    w_svg = max(360, len(phrase) * 11 + 80, len(expression) * 14 + 80)
    h_svg = 180
    parts = []
    parts.append(f'<rect x="30" y="60" width="{w_svg-60}" height="46" rx="10" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<text x="{w_svg/2}" y="89" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#0C3A5C">"{phrase}"</text>')
    parts.append(f'<line x1="{w_svg/2}" y1="106" x2="{w_svg/2}" y2="128" stroke="#2C3E50" stroke-width="2.5"/>')
    parts.append(f'<polygon points="{w_svg/2},133 {w_svg/2-7},121 {w_svg/2+7},121" fill="#2C3E50"/>')
    expr_str = "?" if blank else expression
    parts.append(f'<rect x="30" y="136" width="{w_svg-60}" height="40" rx="10" fill="#E7F8ED" stroke="#1E7A44" stroke-width="2.5"/>')
    parts.append(f'<text x="{w_svg/2}" y="162" text-anchor="middle" font-family="Helvetica-Bold" font-size="18" fill="#0B4F30">{expr_str}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">Words to algebra</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def single_bracket_area_svg(a=3, b=4, var="x", op="+", blank=False, **kw):
    """a(x+b) as a single-row area-model rectangle: one column for the
    'x' part, one for the 'b' part -- the distributive-property visual
    (Level 11CUM3). blank=True leaves the two product cells empty."""
    b_disp = b if op == "+" else -b
    col_labels = [var, (f"+{b}" if op == "+" else f"-{b}")]
    cell_w, cell_h = 110, 70
    x0, y0 = 70, 70
    w_svg = x0 + 2 * cell_w + 30
    h_svg = y0 + cell_h + 60
    parts = []
    expr = f"{a}({var} {op} {b})"
    parts.append(f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">{expr}</text>')
    for j, lbl in enumerate(col_labels):
        cx = x0 + j * cell_w + cell_w / 2
        parts.append(f'<text x="{cx:.1f}" y="{y0-14}" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#1B5E8C">{lbl}</text>')
    parts.append(f'<text x="{x0-16:.1f}" y="{y0+cell_h/2+6:.1f}" text-anchor="end" font-family="Helvetica-Bold" font-size="17" fill="#1E7A44">{a}</text>')
    cell1 = "?" if blank else f"{a}{var}"
    cell2 = "?" if blank else (f"{a*b}" if op == "+" else f"-{a*b}")
    bgs = ["#EAF4FC", "#FFF8E1"]
    cells = [cell1, cell2]
    for j in range(2):
        cx = x0 + j * cell_w
        parts.append(f'<rect x="{cx}" y="{y0}" width="{cell_w}" height="{cell_h}" fill="{bgs[j]}" stroke="#2C3E50" stroke-width="1.5"/>')
        parts.append(f'<text x="{cx+cell_w/2:.1f}" y="{y0+cell_h/2+7:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="19" fill="#2C3E50">{cells[j]}</text>')
    parts.append(f'<text x="{w_svg/2}" y="{y0+cell_h+30}" text-anchor="middle" font-family="Helvetica-Oblique" font-size="12" fill="#5D6D7E">Add the two cells together</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def solve_equation_ladder_svg(a=2, b=3, op="+", total=11, var="x", blank=False, **kw):
    """A vertical 'undo the operations' ladder for a two-step equation
    ax +/- b = total: shows each line down to x = answer, with the
    inverse operation labelled on the right at each step (Level 12C).
    blank=True keeps the starting equation and blanks the steps below."""
    a, b, total = int(a), int(b), int(total)
    if op == "+":
        after_b = total - b
    else:
        after_b = total + b
    ans = after_b // a if a else after_b
    inv1 = f"{'-' if op == '+' else '+'} {b} both sides"
    inv2 = f"÷ {a} both sides"
    lines = [
        (f"{a}{var} {op} {b} = {total}", ""),
        (f"{a}{var} = {after_b}", inv1),
        (f"{var} = {ans}", inv2),
    ]
    if blank:
        lines = [lines[0], ("____", inv1), ("____", inv2)]
    w_svg = 340
    row_h = 54
    h_svg = 70 + row_h * len(lines) + 20
    ox, oy = 40, 80
    parts = []
    for i, (eq, note) in enumerate(lines):
        ry = oy + i * row_h
        is_last = (i == len(lines) - 1)
        fill, stroke, tcol = ("#E7F8ED", "#1E7A44", "#0B4F30") if (is_last and not blank) else ("#EAF4FC", "#1B5E8C", "#0C3A5C")
        if blank and i > 0:
            fill, stroke, tcol = ("#FAFBFC", "#9AA5B1", "#5D6D7E")
        dash = ' stroke-dasharray="6,4"' if (blank and i > 0) else ""
        parts.append(f'<rect x="{ox:.1f}" y="{ry:.1f}" width="170" height="38" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>')
        parts.append(f'<text x="{ox+85:.1f}" y="{ry+25:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="{tcol}">{eq}</text>')
        if note:
            parts.append(f'<text x="{ox+180:.1f}" y="{ry+24:.1f}" font-family="Helvetica" font-size="12" fill="#A6362B">{note}</text>')
        if not is_last:
            ay = ry + 38
            parts.append(f'<line x1="{ox+85:.1f}" y1="{ay+2:.1f}" x2="{ox+85:.1f}" y2="{ay+row_h-40:.1f}" stroke="#2C3E50" stroke-width="2"/>')
            parts.append(f'<polygon points="{ox+85},{ay+row_h-38} {ox+79},{ay+row_h-47} {ox+91},{ay+row_h-47}" fill="#2C3E50"/>')
    parts.insert(0, f'<text x="{w_svg/2}" y="28" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">Solve step by step</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def inverse_machine_svg(a=2, b=3, op="+", total=11, var="x", blank=False, **kw):
    """A two-row 'forward / backward' machine for a two-step equation:
    top row shows x -> (xa) -> (+b) -> total; bottom row shows the same
    boxes reversed with inverse operations, ending at x -- makes 'undo
    in reverse order' concrete (Level 12B/12C/12I). blank=True hides the
    recovered x value at the end of the backward row."""
    a, b, total = int(a), int(b), int(total)
    inv_op = "-" if op == "+" else "+"
    w_svg, h_svg = 460, 220
    parts = []
    # forward row
    fy = 55
    boxes_f = [(var, "#EAF4FC", "#1B5E8C"), (f"×{a}", "#FFF8E1", "#9A7209"), (f"{op}{b}", "#FFF8E1", "#9A7209"), (str(total), "#E7F8ED", "#1E7A44")]
    bx = 30
    bw, gap = 80, 24
    parts.append(f'<text x="20" y="{fy-14}" font-family="Helvetica-Bold" font-size="12" fill="#5D6D7E">FORWARD</text>')
    for i, (lbl, fill, stroke) in enumerate(boxes_f):
        parts.append(f'<rect x="{bx}" y="{fy}" width="{bw}" height="42" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        parts.append(f'<text x="{bx+bw/2}" y="{fy+27}" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">{lbl}</text>')
        if i < len(boxes_f) - 1:
            parts.append(f'<line x1="{bx+bw}" y1="{fy+21}" x2="{bx+bw+gap}" y2="{fy+21}" stroke="#2C3E50" stroke-width="2"/>')
            parts.append(f'<polygon points="{bx+bw+gap},{fy+21} {bx+bw+gap-9},{fy+16} {bx+bw+gap-9},{fy+26}" fill="#2C3E50"/>')
        bx += bw + gap
    # backward row
    by = 140
    ans = (total - b) // a if op == "+" else (total + b) // a
    ans_str = "?" if blank else str(ans)
    boxes_b = [(str(total), "#E7F8ED", "#1E7A44"), (f"{inv_op}{b}", "#FDEDEB", "#A6362B"), (f"÷{a}", "#FDEDEB", "#A6362B"), (ans_str, "#EAF4FC", "#1B5E8C")]
    bx = 30
    parts.append(f'<text x="20" y="{by-14}" font-family="Helvetica-Bold" font-size="12" fill="#5D6D7E">BACKWARD (undo)</text>')
    for i, (lbl, fill, stroke) in enumerate(boxes_b):
        parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="42" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        parts.append(f'<text x="{bx+bw/2}" y="{by+27}" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">{lbl}</text>')
        if i < len(boxes_b) - 1:
            parts.append(f'<line x1="{bx+bw}" y1="{by+21}" x2="{bx+bw+gap}" y2="{by+21}" stroke="#2C3E50" stroke-width="2"/>')
            parts.append(f'<polygon points="{bx+bw+gap},{by+21} {bx+bw+gap-9},{by+16} {bx+bw+gap-9},{by+26}" fill="#2C3E50"/>')
        bx += bw + gap
    parts.insert(0, f'<text x="{w_svg/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">{a}{var} {op} {b} = {total}  --  undo in reverse</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def consecutive_bar_svg(count=3, step=1, total=27, kind="integer", blank=False, **kw):
    """A stacked bar model for 'consecutive numbers sum to total' word
    problems: `count` bars, each = x plus an offset (0, step, 2*step...),
    all summing to total (Level 12I). blank=True hides the computed x.
    kind='integer' uses +1 steps, 'even'/'odd' use +2."""
    count, step, total = int(count), int(step), int(total)
    offsets = [i * step for i in range(count)]
    x_val = (total - sum(offsets)) // count
    w_svg, h_svg = 440, 90 + count * 46
    ox, oy = 40, 70
    bar_unit = 20
    parts = []
    labels_desc = {"integer": "consecutive numbers", "even": "consecutive even numbers", "odd": "consecutive odd numbers"}
    desc = labels_desc.get(kind, "consecutive numbers")
    for i, off in enumerate(offsets):
        by = oy + i * 46
        xw = 120
        parts.append(f'<rect x="{ox}" y="{by}" width="{xw}" height="34" rx="6" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2"/>')
        parts.append(f'<text x="{ox+xw/2}" y="{by+23}" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#0C3A5C">x</text>')
        if off > 0:
            ow = off * bar_unit
            parts.append(f'<rect x="{ox+xw}" y="{by}" width="{ow}" height="34" rx="6" fill="#FFF8E1" stroke="#9A7209" stroke-width="2"/>')
            parts.append(f'<text x="{ox+xw+ow/2}" y="{by+23}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#5c4708">+{off}</text>')
        lbl = f"x+{off}" if off else "x"
        parts.append(f'<text x="{ox+xw+off*bar_unit+12}" y="{by+23}" font-family="Helvetica" font-size="13" fill="#5D6D7E">= {lbl}</text>')
    ty = oy + count * 46 + 4
    ans_str = "____" if blank else str(x_val)
    parts.append(f'<text x="{ox}" y="{ty+14}" font-family="Helvetica-Bold" font-size="14" fill="#A6362B">Total = {total}   so   {count}x + {sum(offsets)} = {total},  x = {ans_str}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="28" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">{count} {desc} add to {total}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def _pow_txt(x, y, base, exp, font_size=18, color="#2C3E50", anchor="start"):
    """SVG for base^exp with a TRUE raised smaller exponent (two text
    elements -- unicode superscripts don't render via svglib)."""
    base_str, exp_str = str(base), str(exp)
    sup_size = font_size * 0.62
    sup_dy = -font_size * 0.45
    base_w = len(base_str) * font_size * 0.60
    exp_w = len(exp_str) * sup_size * 0.62
    total_w = base_w + exp_w + 2
    if anchor == "middle":
        bx = x - total_w / 2
    elif anchor == "end":
        bx = x - total_w
    else:
        bx = x
    out = f'<text x="{bx:.1f}" y="{y:.1f}" font-family="Helvetica-Bold" font-size="{font_size}" fill="{color}">{base_str}</text>'
    out += f'<text x="{bx+base_w+1:.1f}" y="{y+sup_dy:.1f}" font-family="Helvetica-Bold" font-size="{sup_size:.1f}" fill="{color}">{exp_str}</text>'
    return out


def power_expansion_svg(base=2, exp=4, blank=False, **kw):
    """The anatomy of a power: base^exp with BASE and INDEX labelled,
    then the expansion chain base x base x ... = value (Level 13A).
    blank=True hides the expansion and the final value."""
    base, exp = int(base), int(exp)
    value = base ** exp
    w_svg, h_svg = 460, 250
    parts = []
    cx = 90
    parts.append(_pow_txt(cx, 80, base, exp, font_size=40, color="#1B5E8C"))
    base_w = len(str(base)) * 40 * 0.60
    parts.append(f'<line x1="{cx+base_w/2:.1f}" y1="92" x2="{cx+base_w/2:.1f}" y2="116" stroke="#1B5E8C" stroke-width="1.5" stroke-dasharray="3,2"/>')
    parts.append(f'<rect x="{cx+base_w/2-34:.1f}" y="116" width="68" height="22" rx="11" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="1.3"/>')
    parts.append(f'<text x="{cx+base_w/2:.1f}" y="131" text-anchor="middle" font-family="Helvetica-Bold" font-size="11.5" fill="#1B5E8C">BASE</text>')
    exp_x = cx + base_w + len(str(exp)) * 24 * 0.62 / 2
    parts.append(f'<line x1="{exp_x:.1f}" y1="50" x2="{exp_x+40:.1f}" y2="34" stroke="#A6362B" stroke-width="1.5" stroke-dasharray="3,2"/>')
    parts.append(f'<rect x="{exp_x+40:.1f}" y="22" width="60" height="22" rx="11" fill="#FDEDEB" stroke="#A6362B" stroke-width="1.3"/>')
    parts.append(f'<text x="{exp_x+70:.1f}" y="37" text-anchor="middle" font-family="Helvetica-Bold" font-size="11.5" fill="#A6362B">INDEX</text>')
    if blank:
        chain = " x ".join(["____"] * exp)
        parts.append(f'<text x="{cx:.1f}" y="185" font-family="Helvetica-Bold" font-size="17" fill="#5D6D7E">= {chain} = ____</text>')
        parts.append(f'<text x="{cx:.1f}" y="218" font-family="Helvetica" font-size="12" fill="#1E7A44">Write {base} that many times, then multiply.</text>')
    else:
        chain = " x ".join([str(base)] * exp)
        parts.append(f'<text x="{cx:.1f}" y="185" font-family="Helvetica-Bold" font-size="19" fill="#2C3E50">= {chain} = {value}</text>')
        parts.append(f'<text x="{cx:.1f}" y="218" font-family="Helvetica" font-size="12" fill="#1E7A44">The index counts how many times the base is multiplied.</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def square_dots_grid_svg(n=4, blank=False, **kw):
    """n^2 as a literal n x n grid of squares -- WHY 'squared' is called
    squared (Level 13A/13E). blank=True shows an empty n x n outline."""
    n = int(n)
    cell = min(200 // max(n, 1), 40)
    gw = n * cell
    w_svg = max(gw + 120, 320)
    h_svg = gw + 120
    ox, oy = (w_svg - gw) / 2, 70
    parts = []
    for r in range(n):
        for c in range(n):
            fill = "#FAFBFC" if blank else "#AFCBE3"
            parts.append(f'<rect x="{ox+c*cell:.1f}" y="{oy+r*cell:.1f}" width="{cell}" height="{cell}" fill="{fill}" stroke="#1B5E8C" stroke-width="1.5"/>')
    parts.append(f'<text x="{ox+gw/2:.1f}" y="{oy+gw+24:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#A6362B">{n} across</text>')
    parts.append(f'<text x="{ox-12:.1f}" y="{oy+gw/2:.1f}" text-anchor="end" font-family="Helvetica-Bold" font-size="14" fill="#1E7A44">{n} down</text>')
    title_val = "____" if blank else str(n * n)
    parts.insert(0, _pow_txt(w_svg/2 - 40, 34, n, 2, font_size=20, color="#2C3E50"))
    parts.insert(1, f'<text x="{w_svg/2 - 8:.1f}" y="34" font-family="Helvetica-Bold" font-size="20" fill="#2C3E50">= {n} x {n} = {title_val}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def cube_stack_3d_svg(n=3, blank=False, **kw):
    """n^3 as a pseudo-3D n x n x n stack of unit cubes -- WHY 'cubed'
    is called cubed (Level 13A/13E). blank=True hides the total count."""
    import math as _m
    n = int(n)
    u = min(120 // max(n, 1), 34)
    dx, dy = u * 0.5, -u * 0.29
    w_svg, h_svg = 400, 320
    ox = 110
    oy = 240
    parts = []
    for z in range(n):          # depth (back to front handled by draw order)
        for y_ in range(n):     # height
            for x_ in range(n): # width
                X = ox + x_ * u + z * dx
                Y = oy - y_ * u + z * dy
                # front face
                parts.append(f'<rect x="{X:.1f}" y="{Y-u:.1f}" width="{u}" height="{u}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="1.2"/>')
                # top face
                top = f"{X:.1f},{Y-u:.1f} {X+dx:.1f},{Y-u+dy:.1f} {X+u+dx:.1f},{Y-u+dy:.1f} {X+u:.1f},{Y-u:.1f}"
                parts.append(f'<polygon points="{top}" fill="#CFE4F3" stroke="#1B5E8C" stroke-width="1.2"/>')
                # right face
                right = f"{X+u:.1f},{Y-u:.1f} {X+u+dx:.1f},{Y-u+dy:.1f} {X+u+dx:.1f},{Y+dy:.1f} {X+u:.1f},{Y:.1f}"
                parts.append(f'<polygon points="{right}" fill="#AFCBE3" stroke="#1B5E8C" stroke-width="1.2"/>')
    title_val = "____" if blank else str(n ** 3)
    parts.append(_pow_txt(150, 40, n, 3, font_size=20, color="#2C3E50"))
    parts.append(f'<text x="182" y="40" font-family="Helvetica-Bold" font-size="20" fill="#2C3E50">= {n} x {n} x {n} = {title_val}</text>')
    parts.append(f'<text x="{w_svg/2}" y="{h_svg-14}" text-anchor="middle" font-family="Helvetica" font-size="12" fill="#1E7A44">{n} wide, {n} deep, {n} tall -- count the unit cubes</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def index_law_visual_svg(base=2, m=3, n=4, mode="multiply", blank=False, **kw):
    """The index laws made visible. multiply: (b·b·b) x (b·b·b·b)
    merge into one group of m+n factors. divide: m factors over n
    factors with n pairs cancelled, leaving m-n. (Level 13B/13CUM1).
    blank=True hides the merged/net result."""
    base, m, n = int(base), int(m), int(n)
    w_svg, h_svg = 480, 240
    parts = []
    b = str(base)
    if mode == "multiply":
        g1 = " x ".join([b] * m)
        g2 = " x ".join([b] * n)
        parts.append(f'<rect x="30" y="60" width="{m*26+24}" height="40" rx="9" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2"/>')
        parts.append(f'<text x="{30+(m*26+24)/2:.1f}" y="86" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#0C3A5C">{g1}</text>')
        parts.append(_pow_txt(30 + (m*26+24)/2, 48, base, m, font_size=14, color="#1B5E8C", anchor="middle"))
        x2 = 30 + m*26 + 24 + 34
        parts.append(f'<text x="{x2-22:.1f}" y="86" font-family="Helvetica-Bold" font-size="18" fill="#2C3E50">x</text>')
        parts.append(f'<rect x="{x2}" y="60" width="{n*26+24}" height="40" rx="9" fill="#E7F8ED" stroke="#1E7A44" stroke-width="2"/>')
        parts.append(f'<text x="{x2+(n*26+24)/2:.1f}" y="86" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#0B4F30">{g2}</text>')
        parts.append(_pow_txt(x2 + (n*26+24)/2, 48, base, n, font_size=14, color="#1E7A44", anchor="middle"))
        parts.append(f'<line x1="{w_svg/2}" y1="108" x2="{w_svg/2}" y2="136" stroke="#2C3E50" stroke-width="2.5"/>')
        parts.append(f'<polygon points="{w_svg/2},142 {w_svg/2-7},130 {w_svg/2+7},130" fill="#2C3E50"/>')
        if blank:
            parts.append(f'<text x="{w_svg/2}" y="172" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#5D6D7E">____ factors of {base} altogether</text>')
            parts.append(f'<text x="{w_svg/2}" y="205" text-anchor="middle" font-family="Helvetica" font-size="13" fill="#A6362B">Count all the {base}s -- ADD the indices.</text>')
        else:
            total = m + n
            allf = " x ".join([b] * total)
            parts.append(f'<text x="{w_svg/2}" y="168" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#2C3E50">{allf}</text>')
            parts.append(_pow_txt(w_svg/2 - 46, 200, base, m, font_size=15, color="#1B5E8C", anchor="middle"))
            parts.append(_pow_txt(w_svg/2 - 14, 200, base, n, font_size=15, color="#1E7A44", anchor="middle"))
            parts.append(f'<text x="{w_svg/2-30:.1f}" y="200" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">x</text>')
            parts.append(f'<text x="{w_svg/2+8:.1f}" y="200" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">=</text>')
            parts.append(_pow_txt(w_svg/2 + 42, 200, base, m + n, font_size=15, color="#A6362B", anchor="middle"))
            parts.append(f'<text x="{w_svg/2+90:.1f}" y="200" font-family="Helvetica" font-size="12" fill="#A6362B">({m}+{n}={m+n})</text>')
        title = "Multiplying powers: ADD the indices"
    else:
        top = " x ".join([b] * m)
        bot = " x ".join([b] * n)
        cxm = w_svg / 2
        parts.append(f'<text x="{cxm}" y="78" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#0C3A5C">{top}</text>')
        parts.append(f'<line x1="{cxm-m*15:.1f}" y1="92" x2="{cxm+m*15:.1f}" y2="92" stroke="#2C3E50" stroke-width="2.5"/>')
        parts.append(f'<text x="{cxm}" y="118" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#0B4F30">{bot}</text>')
        # cancellation strokes over the first n factors top and bottom
        for i in range(min(n, m)):
            fx = cxm - m * 15 + 8 + i * 30
            parts.append(f'<line x1="{fx:.1f}" y1="80" x2="{fx+14:.1f}" y2="64" stroke="#A6362B" stroke-width="2"/>')
            bx2 = cxm - n * 15 + 8 + i * 30
            parts.append(f'<line x1="{bx2:.1f}" y1="120" x2="{bx2+14:.1f}" y2="104" stroke="#A6362B" stroke-width="2"/>')
        if blank:
            parts.append(f'<text x="{cxm}" y="170" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#5D6D7E">____ factors of {base} survive</text>')
            parts.append(f'<text x="{cxm}" y="202" text-anchor="middle" font-family="Helvetica" font-size="13" fill="#A6362B">Cancel pairs top and bottom -- SUBTRACT the indices.</text>')
        else:
            parts.append(_pow_txt(cxm - 60, 172, base, m, font_size=15, color="#1B5E8C", anchor="middle"))
            parts.append(f'<text x="{cxm-38:.1f}" y="172" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">÷</text>')
            parts.append(_pow_txt(cxm - 8, 172, base, n, font_size=15, color="#1E7A44", anchor="middle"))
            parts.append(f'<text x="{cxm+14:.1f}" y="172" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">=</text>')
            parts.append(_pow_txt(cxm + 48, 172, base, m - n, font_size=15, color="#A6362B", anchor="middle"))
            parts.append(f'<text x="{cxm+92:.1f}" y="172" font-family="Helvetica" font-size="12" fill="#A6362B">({m}-{n}={m-n})</text>')
        title = "Dividing powers: SUBTRACT the indices"
    parts.insert(0, f'<text x="{w_svg/2}" y="28" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">{title}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def power_ladder_svg(base=2, top_exp=3, bottom_exp=-2, blank=False, **kw):
    """The dividing ladder: base^top ... down to base^bottom, each row
    = previous ÷ base -- the canonical picture of WHY a^0 = 1 and why
    negative powers are fractions (Level 13A/13D). blank=True keeps the
    top two rows and blanks the values below."""
    from fractions import Fraction
    base, top_exp, bottom_exp = int(base), int(top_exp), int(bottom_exp)
    rows = []
    for e in range(top_exp, bottom_exp - 1, -1):
        v = Fraction(base) ** e
        v_str = str(v.numerator) if v.denominator == 1 else f"1/{v.denominator}"
        rows.append((e, v_str))
    w_svg = 340
    row_h = 40
    h_svg = 70 + row_h * len(rows) + 16
    ox, oy = 70, 76
    parts = []
    for i, (e, v_str) in enumerate(rows):
        ry = oy + i * row_h
        hide = blank and i >= 2
        val = "____" if hide else v_str
        col = "#A6362B" if e == 0 and not hide else "#2C3E50"
        parts.append(_pow_txt(ox, ry, base, e, font_size=17, color="#1B5E8C"))
        parts.append(f'<text x="{ox+58:.1f}" y="{ry:.1f}" font-family="Helvetica-Bold" font-size="17" fill="{col}">= {val}</text>')
        if i < len(rows) - 1:
            parts.append(f'<text x="{ox+170:.1f}" y="{ry+row_h/2+4:.1f}" font-family="Helvetica" font-size="12" fill="#1E7A44">÷ {base}</text>')
            parts.append(f'<line x1="{ox+160:.1f}" y1="{ry+8:.1f}" x2="{ox+160:.1f}" y2="{ry+row_h-6:.1f}" stroke="#1E7A44" stroke-width="1.6"/>')
            parts.append(f'<polygon points="{ox+160},{ry+row_h-2} {ox+155},{ry+row_h-10} {ox+165},{ry+row_h-10}" fill="#1E7A44"/>')
    parts.insert(0, f'<text x="{w_svg/2}" y="28" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">Each step down: divide by {base}</text>')
    parts.insert(1, f'<text x="{w_svg/2}" y="48" text-anchor="middle" font-family="Helvetica" font-size="11.5" fill="#5D6D7E">Keep the pattern going past zero...</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def sqrt_side_area_svg(area=25, blank=False, **kw):
    """A square with its AREA printed inside; the side length is the
    square root -- makes a^(1/2) concrete (Level 13E). blank=True hides
    the side value."""
    import math as _m
    area = int(area)
    side = _m.isqrt(area)
    S = 150
    w_svg, h_svg = 360, 260
    ox, oy = 110, 60
    parts = []
    parts.append(f'<rect x="{ox}" y="{oy}" width="{S}" height="{S}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<text x="{ox+S/2:.1f}" y="{oy+S/2-6:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">Area</text>')
    parts.append(f'<text x="{ox+S/2:.1f}" y="{oy+S/2+18:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="19" fill="#A6362B">= {area}</text>')
    side_str = "?" if blank else str(side)
    parts.append(f'<line x1="{ox:.1f}" y1="{oy+S+18:.1f}" x2="{ox+S:.1f}" y2="{oy+S+18:.1f}" stroke="#1E7A44" stroke-width="1.6"/>')
    parts.append(f'<text x="{ox+S/2:.1f}" y="{oy+S+38:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#1E7A44">side = √{area} = {side_str}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">Square root = the side of the square</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def sci_notation_slider_svg(number=56000, blank=False, **kw):
    """Decimal-point hop diagram for scientific notation: the digits of
    the number with numbered arc hops showing how many places the point
    moves, ending at 'a x 10^n' (Level 13F). blank=True hides the power.
    Works for large numbers (positive power) and decimals (negative)."""
    from decimal import Decimal
    num = Decimal(str(number))
    s = format(num, 'f')
    if '.' in s:
        s = s.rstrip('0').rstrip('.') if s.rstrip('0').rstrip('.') else '0'
        if num < 1 and '.' not in s:
            s = format(num, 'f')
    is_small = num < 1
    digits = s.replace(".", "")
    digits = digits.lstrip("0") if is_small else digits
    lead = digits[0]
    rest = digits[1:].rstrip("0")
    mant = lead + ("." + rest if rest else "")
    if is_small:
        frac = s.split(".")[1]
        n_exp = -(len(frac) - len(frac.lstrip("0")) + 1)
    else:
        n_exp = len(s.split(".")[0]) - 1
    w_svg, h_svg = 440, 230
    parts = []
    ch_w = 30
    disp = s
    x0 = (w_svg - len(disp) * ch_w) / 2
    y0 = 100
    for i, ch in enumerate(disp):
        parts.append(f'<text x="{x0+i*ch_w+ch_w/2:.1f}" y="{y0:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="26" fill="#2C3E50">{ch}</text>')
    hops = abs(n_exp)
    if is_small:
        pt_idx = disp.index(".")
        hop_start = pt_idx
        direction = 1
    else:
        hop_start = len(disp)
        direction = -1
    for h in range(hops):
        a = x0 + (hop_start + direction * h) * ch_w
        b2 = x0 + (hop_start + direction * (h + 1)) * ch_w
        mid = (a + b2) / 2
        parts.append(f'<path d="M {a:.1f} {y0+8:.1f} Q {mid:.1f} {y0+34:.1f} {b2:.1f} {y0+8:.1f}" fill="none" stroke="#A6362B" stroke-width="2"/>')
        parts.append(f'<text x="{mid:.1f}" y="{y0+46:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#A6362B">{h+1}</text>')
    exp_str = "____" if blank else str(n_exp)
    parts.append(f'<text x="{w_svg/2 - 60:.1f}" y="188" text-anchor="middle" font-family="Helvetica-Bold" font-size="19" fill="#1B5E8C">= {mant} x 10</text>')
    sup_x = w_svg/2 - 60 + (len(f"= {mant} x 10") * 19 * 0.30)
    parts.append(f'<text x="{sup_x+12:.1f}" y="179" font-family="Helvetica-Bold" font-size="13" fill="#A6362B">{exp_str}</text>')
    dirn = "right" if is_small else "left"
    parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">Move the decimal point {dirn} -- count the hops</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def surd_simplify_tree_svg(n=72, blank=False, **kw):
    """Simplifying a surd: √n split into √(square x rest) = k√rest,
    shown as a mini two-branch tree (Level 13CUM2). blank=True shows
    only √n with empty branches."""
    import math as _m
    n = int(n)
    best_k = 1
    for k in range(2, int(_m.isqrt(n)) + 1):
        if n % (k * k) == 0:
            best_k = k
    sq = best_k * best_k
    rest = n // sq
    w_svg, h_svg = 380, 260
    cx = w_svg / 2
    parts = []
    parts.append(f'<circle cx="{cx}" cy="66" r="34" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<text x="{cx}" y="73" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#0C3A5C">√{n}</text>')
    lx, rx, ny = cx - 90, cx + 90, 160
    parts.append(f'<line x1="{cx-16:.1f}" y1="94" x2="{lx+12:.1f}" y2="{ny-26}" stroke="#2C3E50" stroke-width="2"/>')
    parts.append(f'<line x1="{cx+16:.1f}" y1="94" x2="{rx-12:.1f}" y2="{ny-26}" stroke="#2C3E50" stroke-width="2"/>')
    if blank:
        parts.append(f'<circle cx="{lx}" cy="{ny}" r="30" fill="#FAFBFC" stroke="#9AA5B1" stroke-width="2" stroke-dasharray="6,4"/>')
        parts.append(f'<circle cx="{rx}" cy="{ny}" r="30" fill="#FAFBFC" stroke="#9AA5B1" stroke-width="2" stroke-dasharray="6,4"/>')
        parts.append(f'<text x="{cx}" y="226" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#A6362B">Split out the largest PERFECT SQUARE factor.</text>')
    else:
        parts.append(f'<circle cx="{lx}" cy="{ny}" r="30" fill="#E7F8ED" stroke="#1E7A44" stroke-width="2.5"/>')
        parts.append(f'<text x="{lx}" y="{ny+6}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#0B4F30">√{sq}</text>')
        parts.append(f'<circle cx="{rx}" cy="{ny}" r="30" fill="#FFF8E1" stroke="#9A7209" stroke-width="2.5"/>')
        parts.append(f'<text x="{rx}" y="{ny+6}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#5c4708">√{rest}</text>')
        parts.append(f'<text x="{lx}" y="{ny+48}" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#1E7A44">= {best_k}</text>')
        parts.append(f'<text x="{cx}" y="230" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#A6362B">√{n} = √({sq} x {rest}) = {best_k}√{rest}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="26" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">Simplify the surd</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def identity_square_svg(a_lbl="a", b_lbl="b", mode="plus", blank=False, **kw):
    """THE canonical geometric proof of (a+b)^2 = a^2 + 2ab + b^2: a
    square of side (a+b) split into four area-proportional regions --
    a^2, two ab rectangles, and b^2 (Level 14E). mode='minus' captions
    the (a-b)^2 identity instead; mode='diff' captions (a+b)(a-b).
    blank=True empties the region labels for the student to fill."""
    a_frac = 0.62
    S = 190
    ox, oy = 90, 66
    A = S * a_frac
    B = S - A
    w_svg, h_svg = 400, 340
    parts = []
    regions = [
        (ox, oy, A, A, "#EAF4FC", f"{a_lbl}²" if not blank else "?", "#0C3A5C"),
        (ox + A, oy, B, A, "#FFF8E1", f"{a_lbl}{b_lbl}" if not blank else "?", "#5c4708"),
        (ox, oy + A, A, B, "#FFF8E1", f"{a_lbl}{b_lbl}" if not blank else "?", "#5c4708"),
        (ox + A, oy + A, B, B, "#E7F8ED", f"{b_lbl}²" if not blank else "?", "#0B4F30"),
    ]
    for (rx, ry, rw, rh, fill, lbl, tcol) in regions:
        parts.append(f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{rw:.1f}" height="{rh:.1f}" fill="{fill}" stroke="#2C3E50" stroke-width="2"/>')
        fs = 19 if min(rw, rh) > 60 else 15
        parts.append(f'<text x="{rx+rw/2:.1f}" y="{ry+rh/2+6:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="{fs}" fill="{tcol}">{lbl}</text>')
    parts.append(f'<text x="{ox+A/2:.1f}" y="{oy-12:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#1B5E8C">{a_lbl}</text>')
    parts.append(f'<text x="{ox+A+B/2:.1f}" y="{oy-12:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#1E7A44">{b_lbl}</text>')
    parts.append(f'<text x="{ox-14:.1f}" y="{oy+A/2+5:.1f}" text-anchor="end" font-family="Helvetica-Bold" font-size="15" fill="#1B5E8C">{a_lbl}</text>')
    parts.append(f'<text x="{ox-14:.1f}" y="{oy+A+B/2+5:.1f}" text-anchor="end" font-family="Helvetica-Bold" font-size="15" fill="#1E7A44">{b_lbl}</text>')
    if blank:
        caption = f"Whole square = ({a_lbl}+{b_lbl})² -- add the four regions."
    else:
        simple = a_lbl.isalpha() and b_lbl.isalpha() and len(a_lbl) == 1 and len(b_lbl) == 1
        ab = f"{a_lbl}{b_lbl}" if simple else f"({a_lbl})({b_lbl})"
        if mode == "minus":
            caption = f"({a_lbl}-{b_lbl})² = {a_lbl}² - 2{ab} + {b_lbl}²  (same picture, subtract the strips)"
        elif mode == "diff":
            caption = f"({a_lbl}+{b_lbl})({a_lbl}-{b_lbl}) = {a_lbl}² - {b_lbl}²  (cut and rearrange)"
        else:
            caption = f"({a_lbl}+{b_lbl})² = {a_lbl}² + 2{ab} + {b_lbl}²  -- read it off the picture!"
    parts.append(f'<text x="{w_svg/2}" y="{h_svg-20}" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#A6362B">{caption}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="28" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">A square of side ({a_lbl}+{b_lbl})</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def factor_x_method_svg(b=5, c=6, blank=False, **kw):
    """The international 'X method' (diamond) for factorising
    x^2 + bx + c: PRODUCT c on top, SUM b on bottom, the two numbers
    that satisfy both go in the side cells; then the factors read off
    as (x+p)(x+q) (Level 14F). blank=True leaves the side cells and
    factorisation empty."""
    b, c = int(b), int(c)
    p = q = None
    for cand in range(-abs(c) - 1, abs(c) + 2):
        if cand == 0 or c % cand != 0:
            continue
        other = c // cand
        if cand + other == b:
            p, q = cand, other
            break
    if p is None:
        for cand in range(-40, 41):
            for other in range(-40, 41):
                if cand * other == c and cand + other == b:
                    p, q = cand, other
                    break
            if p is not None:
                break
    w_svg, h_svg = 380, 320
    cx, cy = w_svg / 2, 150
    r = 78
    parts = []
    parts.append(f'<line x1="{cx-r}" y1="{cy-r}" x2="{cx+r}" y2="{cy+r}" stroke="#2C3E50" stroke-width="2.5"/>')
    parts.append(f'<line x1="{cx+r}" y1="{cy-r}" x2="{cx-r}" y2="{cy+r}" stroke="#2C3E50" stroke-width="2.5"/>')
    parts.append(f'<text x="{cx}" y="{cy-r+16:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="20" fill="#A6362B">{c}</text>')
    parts.append(f'<text x="{cx}" y="{cy-r-8:.1f}" text-anchor="middle" font-family="Helvetica" font-size="11" fill="#A6362B">PRODUCT</text>')
    parts.append(f'<text x="{cx}" y="{cy+r-4:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="20" fill="#1E7A44">{b}</text>')
    parts.append(f'<text x="{cx}" y="{cy+r+18:.1f}" text-anchor="middle" font-family="Helvetica" font-size="11" fill="#1E7A44">SUM</text>')
    p_str = "?" if blank else str(p)
    q_str = "?" if blank else str(q)
    parts.append(f'<text x="{cx-r+14:.1f}" y="{cy+7:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="22" fill="#1B5E8C">{p_str}</text>')
    parts.append(f'<text x="{cx+r-14:.1f}" y="{cy+7:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="22" fill="#1B5E8C">{q_str}</text>')
    if blank:
        bottom = f"Find two numbers: multiply to {c}, add to {b}."
    else:
        def sgn(v):
            return f"+{v}" if v >= 0 else str(v)
        bottom = f"x² {'+' if b>=0 else '-'} {abs(b)}x {'+' if c>=0 else '-'} {abs(c)} = (x{sgn(p)})(x{sgn(q)})"
    parts.append(f'<text x="{w_svg/2}" y="{h_svg-24}" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#2C3E50">{bottom}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="28" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">The X method</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def poly_anatomy_svg(terms=None, blank=False, **kw):
    """Full anatomy of a polynomial: each term boxed, coefficients and
    the constant labelled, and a DEGREE crown over the highest power
    (Level 14A). terms = list of (coeff, power). blank=True hides the
    labels so the student identifies the parts."""
    terms = terms or [(3, 2), (5, 1), (-7, 0)]
    w_svg, h_svg = 470, 260
    parts = []
    x = 40
    y = 120
    term_centers = []
    for i, (co, pw) in enumerate(terms):
        if i > 0:
            sign = "+" if co >= 0 else "-"
            parts.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica-Bold" font-size="22" fill="#2C3E50">{sign}</text>')
            x += 26
        mag = abs(co)
        if pw == 0:
            tstr = str(mag)
            tw = len(tstr) * 14 + 26
        elif pw == 1:
            tstr = f"{mag if mag != 1 else ''}x"
            tw = len(tstr) * 14 + 26
        else:
            tstr = f"{mag if mag != 1 else ''}x"
            tw = len(tstr) * 14 + 40
        if i == 0 and co < 0:
            parts.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica-Bold" font-size="22" fill="#2C3E50">-</text>')
            x += 20
        parts.append(f'<rect x="{x-8:.1f}" y="{y-30:.1f}" width="{tw}" height="44" rx="9" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2"/>')
        parts.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica-Bold" font-size="21" fill="#0C3A5C">{tstr}</text>')
        if pw >= 2:
            sup_x = x + len(tstr) * 13
            parts.append(f'<text x="{sup_x:.1f}" y="{y-11:.1f}" font-family="Helvetica-Bold" font-size="14" fill="#0C3A5C">{pw}</text>')
        term_centers.append((x - 8 + tw / 2, pw, mag if pw > 0 else co))
        x += tw + 10
    max_pw = max(pw for _, pw in terms)
    for (tcx, pw, coval) in term_centers:
        if pw == max_pw and not blank:
            parts.append(f'<polygon points="{tcx-16},{y-44} {tcx-10},{y-58} {tcx-4},{y-46} {tcx+2},{y-58} {tcx+8},{y-46} {tcx+14},{y-58} {tcx+18},{y-44}" fill="#B8860B"/>')
            parts.append(f'<text x="{tcx:.1f}" y="{y-66:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#B8860B">DEGREE = {max_pw}</text>')
    if not blank:
        first = term_centers[0]
        parts.append(f'<line x1="{first[0]:.1f}" y1="{y+18:.1f}" x2="{first[0]:.1f}" y2="{y+44:.1f}" stroke="#A6362B" stroke-width="1.5" stroke-dasharray="3,2"/>')
        parts.append(f'<text x="{first[0]:.1f}" y="{y+62:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">coefficient {first[2]}</text>')
        last = term_centers[-1]
        if terms[-1][1] == 0:
            parts.append(f'<line x1="{last[0]:.1f}" y1="{y+18:.1f}" x2="{last[0]:.1f}" y2="{y+84:.1f}" stroke="#1E7A44" stroke-width="1.5" stroke-dasharray="3,2"/>')
            parts.append(f'<text x="{last[0]:.1f}" y="{y+100:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#1E7A44">constant term {last[2]}</text>')
        parts.append(f'<text x="{w_svg/2}" y="{h_svg-8}" text-anchor="middle" font-family="Helvetica" font-size="11.5" fill="#5D6D7E">{len(terms)} terms -- degree = highest power</text>')
    else:
        parts.append(f'<text x="{w_svg/2}" y="{h_svg-14}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#A6362B">Label: terms, coefficients, constant, and the DEGREE.</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="30" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">Anatomy of a polynomial</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def degree_staircase_svg(terms=None, blank=False, **kw):
    """Terms of a polynomial placed on a staircase by power -- constant
    on step 0, x-term on step 1, x^2 on step 2... The highest occupied
    step IS the degree (Level 14A). blank=True leaves the steps empty
    for the student to place the terms."""
    terms = terms or [(3, 2), (5, 1), (-7, 0)]
    max_pw = max(pw for _, pw in terms)
    n_steps = max_pw + 1
    step_w, step_h = 100, 52
    w_svg = 80 + n_steps * step_w
    h_svg = 110 + n_steps * step_h
    ox = 40
    base_y = h_svg - 40
    parts = []
    by_pw = {pw: co for co, pw in terms}
    for s in range(n_steps):
        sx = ox + s * step_w
        sy = base_y - (s + 1) * step_h
        parts.append(f'<rect x="{sx}" y="{sy}" width="{step_w}" height="{(s+1)*step_h}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2"/>')
        parts.append(f'<text x="{sx+step_w/2:.1f}" y="{base_y+22:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#5D6D7E">power {s}</text>')
        if s in by_pw and not blank:
            co = by_pw[s]
            if s == 0:
                lbl = str(co)
            elif s == 1:
                lbl = f"{co if co not in (1,-1) else ('-' if co==-1 else '')}x"
            else:
                lbl = f"{co if co not in (1,-1) else ('-' if co==-1 else '')}x^{s}"
            parts.append(f'<rect x="{sx+12}" y="{sy+8}" width="{step_w-24}" height="34" rx="8" fill="#FFF8E1" stroke="#9A7209" stroke-width="2"/>')
            parts.append(f'<text x="{sx+step_w/2:.1f}" y="{sy+31:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#5c4708">{lbl}</text>')
    if not blank:
        top_x = ox + (n_steps - 1) * step_w + step_w / 2
        top_y = base_y - n_steps * step_h
        parts.append(f'<text x="{top_x:.1f}" y="{top_y-12:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#A6362B">highest step = DEGREE {max_pw}</text>')
    else:
        parts.append(f'<text x="{w_svg/2}" y="{h_svg-8}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#A6362B">Place each term on its power step. Highest step = degree.</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="26" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">Degree staircase</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def hcf_factor_boxes_svg(terms=None, hcf="3x", rests=None, blank=False, **kw):
    """Common-factor factorisation: each term boxed and split into
    HCF x rest, with the shared HCF highlighted, concluding
    HCF(rest1 + rest2 ...) (Level 14F). blank=True hides the splits."""
    terms = terms or ["6x²", "9x"]
    rests = rests or ["2x", "3"]
    w_svg = max(420, 120 * len(terms) + 140)
    h_svg = 250
    parts = []
    x = 40
    y = 78
    for i, (t, r) in enumerate(zip(terms, rests)):
        if i > 0:
            parts.append(f'<text x="{x:.1f}" y="{y+24:.1f}" font-family="Helvetica-Bold" font-size="20" fill="#2C3E50">+</text>')
            x += 26
        parts.append(f'<rect x="{x}" y="{y}" width="104" height="40" rx="8" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2"/>')
        parts.append(f'<text x="{x+52:.1f}" y="{y+26:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#0C3A5C">{t}</text>')
        parts.append(f'<line x1="{x+52:.1f}" y1="{y+42:.1f}" x2="{x+52:.1f}" y2="{y+62:.1f}" stroke="#2C3E50" stroke-width="1.8"/>')
        if blank:
            parts.append(f'<rect x="{x+2}" y="{y+64}" width="100" height="34" rx="7" fill="#FAFBFC" stroke="#9AA5B1" stroke-width="1.8" stroke-dasharray="5,3"/>')
            parts.append(f'<text x="{x+52:.1f}" y="{y+86:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#5D6D7E">? x ?</text>')
        else:
            parts.append(f'<rect x="{x+2}" y="{y+64}" width="100" height="34" rx="7" fill="#FFF8E1" stroke="#9A7209" stroke-width="1.8"/>')
            parts.append(f'<text x="{x+52:.1f}" y="{y+86:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="14" fill="#A6362B">{hcf} x {r}</text>')
        x += 116
    if blank:
        bottom = "Split each term into (common factor) x (what's left)."
    else:
        inner = " + ".join(rests)
        bottom = f"= {hcf}({inner})"
    parts.append(f'<text x="{w_svg/2}" y="{h_svg-30}" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#A6362B">{bottom}</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="28" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">Take out the common factor</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def division_algorithm_box_svg(p_str="x³-6x²+11x-6", d_str="x-1", q_str="x²-5x+6", r_val=0, blank=False, **kw):
    """The Division Algorithm p(x) = divisor x quotient + remainder as
    nested labelled boxes (Level 14CUM3). blank=True hides quotient and
    remainder."""
    w_svg, h_svg = 470, 250
    parts = []
    parts.append(f'<rect x="30" y="56" width="{w_svg-60}" height="52" rx="10" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<text x="{w_svg/2}" y="88" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#0C3A5C">p(x) = {p_str}</text>')
    parts.append(f'<line x1="{w_svg/2}" y1="110" x2="{w_svg/2}" y2="132" stroke="#2C3E50" stroke-width="2.5"/>')
    parts.append(f'<polygon points="{w_svg/2},138 {w_svg/2-7},126 {w_svg/2+7},126" fill="#2C3E50"/>')
    q_disp = "?" if blank else q_str
    r_disp = "?" if blank else str(r_val)
    y2 = 146
    parts.append(f'<rect x="30" y="{y2}" width="120" height="44" rx="9" fill="#E7F8ED" stroke="#1E7A44" stroke-width="2.5"/>')
    parts.append(f'<text x="90" y="{y2+28}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#0B4F30">({d_str})</text>')
    parts.append(f'<text x="162" y="{y2+28}" text-anchor="middle" font-family="Helvetica-Bold" font-size="18" fill="#2C3E50">x</text>')
    parts.append(f'<rect x="176" y="{y2}" width="170" height="44" rx="9" fill="#FFF8E1" stroke="#9A7209" stroke-width="2.5"/>')
    parts.append(f'<text x="261" y="{y2+28}" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#5c4708">{q_disp}</text>')
    parts.append(f'<text x="358" y="{y2+28}" text-anchor="middle" font-family="Helvetica-Bold" font-size="18" fill="#2C3E50">+</text>')
    parts.append(f'<rect x="372" y="{y2}" width="66" height="44" rx="9" fill="#FDEDEB" stroke="#A6362B" stroke-width="2.5"/>')
    parts.append(f'<text x="405" y="{y2+28}" text-anchor="middle" font-family="Helvetica-Bold" font-size="16" fill="#A6362B">{r_disp}</text>')
    parts.append(f'<text x="90" y="{y2+62}" text-anchor="middle" font-family="Helvetica" font-size="11" fill="#1E7A44">divisor</text>')
    parts.append(f'<text x="261" y="{y2+62}" text-anchor="middle" font-family="Helvetica" font-size="11" fill="#9A7209">quotient</text>')
    parts.append(f'<text x="405" y="{y2+62}" text-anchor="middle" font-family="Helvetica" font-size="11" fill="#A6362B">remainder</text>')
    parts.insert(0, f'<text x="{w_svg/2}" y="28" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">Division Algorithm: p(x) = divisor x quotient + remainder</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}">' + "".join(parts) + "</svg>"


def quadrant_map_svg(point=None, blank=False, **kw):
    """The four-quadrant map: each quadrant tinted and labelled with its
    Roman numeral AND its sign pattern (+,+), (-,+), (-,-), (+,-). If a
    point is given, it is plotted with its home quadrant highlighted
    (Level 15A). blank=True shows the tinted plane with empty label
    boxes for the student to fill in the numerals and signs."""
    size = 360
    margin = 36
    rng = 8
    parts, to_px = _grid_svg_base(rng, size, margin)
    cx, cy = to_px(0, 0)
    tint = [
        ("I", "(+, +)", (cx, margin, size - margin, cy), "#E7F8ED", (rng/2, rng/2)),
        ("II", "(-, +)", (margin, margin, cx, cy), "#EAF4FC", (-rng/2, rng/2)),
        ("III", "(-, -)", (margin, cy, cx, size - margin), "#FDEDEB", (-rng/2, -rng/2)),
        ("IV", "(+, -)", (cx, cy, size - margin, size - margin), "#FFF8E1", (rng/2, -rng/2)),
    ]
    overlay = []
    for numeral, signs, (rx1, ry1, rx2, ry2), fill, (qx, qy) in tint:
        overlay.append(f'<rect x="{rx1:.1f}" y="{ry1:.1f}" width="{rx2-rx1:.1f}" height="{ry2-ry1:.1f}" fill="{fill}" opacity="0.55"/>')
        lx, ly = to_px(qx, qy)
        if blank:
            overlay.append(f'<rect x="{lx-34:.1f}" y="{ly-24:.1f}" width="68" height="44" rx="8" fill="white" stroke="#9AA5B1" stroke-width="1.6" stroke-dasharray="5,3"/>')
            overlay.append(f'<text x="{lx:.1f}" y="{ly+4:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#9AA5B1">?</text>')
        else:
            overlay.append(f'<text x="{lx:.1f}" y="{ly-2:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="17" fill="#2C3E50">{numeral}</text>')
            overlay.append(f'<text x="{lx:.1f}" y="{ly+16:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#5D6D7E">{signs}</text>')
    parts[1:1] = overlay  # under grid lines but over background
    if point:
        px, py = to_px(*point)
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="#A6362B" stroke="white" stroke-width="1.5"/>')
        parts.append(f'<text x="{px+9:.1f}" y="{py-9:.1f}" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">({point[0]:g},{point[1]:g})</text>')
    title = "Which quadrant? Match the SIGNS." if blank else "The four quadrants and their sign patterns"
    parts.insert(0, f'<text x="{size/2}" y="16" text-anchor="middle" font-family="Helvetica-Bold" font-size="12.5" fill="#2C3E50">{title}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"


def point_plot_path_svg(point=(3, 2), blank=False, **kw):
    """Plotting a point as a JOURNEY from the origin: a horizontal
    arrow along the x-axis ('3 right'), then a vertical arrow ('2 up'),
    ending at the plotted point (Level 15A/15B). blank=True shows just
    the empty grid with the instruction, for the student to draw the
    path themselves."""
    x, y = point
    rng = max(abs(int(x)), abs(int(y)), 4) + 2
    size = 340
    margin = 34
    parts, to_px = _grid_svg_base(rng, size, margin)
    ox_px, oy_px = to_px(0, 0)
    h_dir = "right" if x >= 0 else "left"
    v_dir = "up" if y >= 0 else "down"
    if blank:
        title = f"Plot ({x:g}, {y:g}): draw the path -- {abs(x):g} {h_dir}, then {abs(y):g} {v_dir}"
        parts.insert(0, f'<text x="{size/2}" y="16" text-anchor="middle" font-family="Helvetica-Bold" font-size="11.5" fill="#A6362B">{title}</text>')
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"
    tx_px, ty0_px = to_px(x, 0)
    px_px, py_px = to_px(x, y)
    # horizontal leg
    parts.append(f'<line x1="{ox_px:.1f}" y1="{oy_px:.1f}" x2="{tx_px:.1f}" y2="{ty0_px:.1f}" stroke="#A6362B" stroke-width="3"/>')
    ah = 8 if x >= 0 else -8
    parts.append(f'<polygon points="{tx_px:.1f},{ty0_px:.1f} {tx_px-ah:.1f},{ty0_px-5:.1f} {tx_px-ah:.1f},{ty0_px+5:.1f}" fill="#A6362B"/>')
    parts.append(f'<text x="{(ox_px+tx_px)/2:.1f}" y="{ty0_px+18:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">{abs(x):g} {h_dir}</text>')
    # vertical leg
    parts.append(f'<line x1="{tx_px:.1f}" y1="{ty0_px:.1f}" x2="{px_px:.1f}" y2="{py_px:.1f}" stroke="#1E7A44" stroke-width="3"/>')
    av = 8 if y >= 0 else -8
    parts.append(f'<polygon points="{px_px:.1f},{py_px:.1f} {px_px-5:.1f},{py_px+av:.1f} {px_px+5:.1f},{py_px+av:.1f}" fill="#1E7A44"/>')
    parts.append(f'<text x="{px_px+9:.1f}" y="{(ty0_px+py_px)/2:.1f}" font-family="Helvetica-Bold" font-size="12" fill="#1E7A44">{abs(y):g} {v_dir}</text>')
    parts.append(f'<circle cx="{px_px:.1f}" cy="{py_px:.1f}" r="6" fill="#1B5E8C" stroke="white" stroke-width="1.5"/>')
    parts.append(f'<text x="{px_px+9:.1f}" y="{py_px-9:.1f}" font-family="Helvetica-Bold" font-size="12" fill="#1B5E8C">({x:g},{y:g})</text>')
    parts.insert(0, f'<text x="{size/2}" y="16" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">Plot ({x:g}, {y:g}): x first, then y</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"


def slope_intercept_anatomy_svg(m=2, c=1, blank=False, **kw):
    """The anatomy of y = mx + c: the equation with SLOPE and
    Y-INTERCEPT callouts, the line drawn on a grid, the intercept dot
    at (0,c), and a rise/run staircase step showing the slope (Level
    15F). blank=True labels the callouts with '?' and hides the
    staircase numbers."""
    size = 360
    margin = 36
    rng = 8
    parts, to_px = _grid_svg_base(rng, size, margin)
    # the line y = mx + c
    pts = []
    for xx in (-rng, rng):
        yy = m * xx + c
        if -rng <= yy <= rng:
            pts.append((xx, yy))
    if len(pts) < 2:
        for yy in (-rng, rng):
            if m != 0:
                xx = (yy - c) / m
                if -rng <= xx <= rng:
                    pts.append((xx, yy))
    if len(pts) >= 2:
        (x1, y1), (x2, y2) = pts[0], pts[-1]
        px1, py1 = to_px(x1, y1)
        px2, py2 = to_px(x2, y2)
        parts.append(f'<line x1="{px1:.1f}" y1="{py1:.1f}" x2="{px2:.1f}" y2="{py2:.1f}" stroke="#1B5E8C" stroke-width="3"/>')
    # intercept dot
    ic_px, ic_py = to_px(0, c)
    parts.append(f'<circle cx="{ic_px:.1f}" cy="{ic_py:.1f}" r="6" fill="#1E7A44" stroke="white" stroke-width="1.5"/>')
    if not blank:
        parts.append(f'<text x="{ic_px+9:.1f}" y="{ic_py+4:.1f}" font-family="Helvetica-Bold" font-size="11.5" fill="#1E7A44">(0, {c:g})</text>')
    # rise/run staircase from a point on the line
    x0 = 1 if -rng < (m * 1 + c) < rng - abs(m) else 0
    sx, sy = to_px(x0, m * x0 + c)
    ex, ey = to_px(x0 + 1, m * x0 + c)
    fx, fy = to_px(x0 + 1, m * (x0 + 1) + c)
    parts.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#A6362B" stroke-width="2.5"/>')
    parts.append(f'<line x1="{ex:.1f}" y1="{ey:.1f}" x2="{fx:.1f}" y2="{fy:.1f}" stroke="#A6362B" stroke-width="2.5"/>')
    if not blank:
        parts.append(f'<text x="{(sx+ex)/2:.1f}" y="{ey+15:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#A6362B">run 1</text>')
        parts.append(f'<text x="{fx+7:.1f}" y="{(ey+fy)/2+4:.1f}" font-family="Helvetica-Bold" font-size="11" fill="#A6362B">rise {m:g}</text>')
    # equation anatomy header
    m_disp = "?" if blank else f"{m:g}"
    c_disp = "?" if blank else f"{c:g}"
    parts.insert(0, f'<text x="{size/2}" y="16" text-anchor="middle" font-family="Helvetica-Bold" font-size="15" fill="#2C3E50">y = {m_disp}x + {c_disp}</text>')
    parts.insert(1, f'<text x="{size/2-56}" y="30" text-anchor="middle" font-family="Helvetica" font-size="9.5" fill="#A6362B">slope (rise/run)</text>')
    parts.insert(2, f'<text x="{size/2+58}" y="30" text-anchor="middle" font-family="Helvetica" font-size="9.5" fill="#1E7A44">y-intercept</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + "".join(parts) + "</svg>"


def _triangle_pts(kind="scalene", w=300, h=240, top_pad=50, side_pad=40):
    """Returns (A,B,C) pixel points for a triangle of the given family,
    shaped to visually match its type (used across several Level 16
    diagrams so the picture always matches the label)."""
    bx0, by = side_pad, h - 30
    bx1 = w - side_pad
    if kind == "equilateral":
        apex_x = (bx0 + bx1) / 2
    elif kind == "isosceles":
        apex_x = (bx0 + bx1) / 2
    elif kind == "right":
        apex_x = bx0
    elif kind == "obtuse":
        apex_x = bx0 - 30
    else:  # scalene
        apex_x = bx0 + (bx1 - bx0) * 0.38
    apex_y = top_pad
    return (apex_x, apex_y), (bx0, by), (bx1, by)


def triangle_classify_svg(angles=None, sides=None, blank=False, **kw):
    """Draws a triangle shaped to match the given angles/sides, with
    tick marks on equal sides and arc marks on equal/right angles, and
    classifies it both ways (by angle: acute/right/obtuse; by side:
    equilateral/isosceles/scalene) (Level 16 CUM1). blank=True hides
    the classification words, leaving only the marked-up picture."""
    angles = angles or [60, 60, 60]
    sides = sides or None
    a1, a2, a3 = angles
    if max(angles) > 90:
        kind = "obtuse"; ang_label = "OBTUSE"
    elif max(angles) == 90:
        kind = "right"; ang_label = "RIGHT"
    else:
        kind = "acute"; ang_label = "ACUTE"
    if sides:
        s1, s2, s3 = sides
        if s1 == s2 == s3:
            side_label = "EQUILATERAL"; shape_kind = "equilateral"
        elif s1 == s2 or s2 == s3 or s1 == s3:
            side_label = "ISOSCELES"; shape_kind = "isosceles"
        else:
            side_label = "SCALENE"; shape_kind = "scalene"
    else:
        side_label = None
        shape_kind = "right" if kind == "right" else ("equilateral" if a1 == a2 == a3 else "scalene")
    w, h = 320, 280
    A, B, C = _triangle_pts(shape_kind, w, h)
    parts = []
    parts.append(f'<polygon points="{A[0]:.1f},{A[1]:.1f} {B[0]:.1f},{B[1]:.1f} {C[0]:.1f},{C[1]:.1f}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    # angle labels at each vertex
    for (pt, ang, name) in [(A, a1, "A"), (B, a2, "B"), (C, a3, "C")]:
        parts.append(f'<text x="{pt[0]:.1f}" y="{pt[1]+(20 if pt is not A else -12):.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">{ang}°</text>')
    if sides:
        mids = [((B[0]+C[0])/2, (B[1]+C[1])/2+16), ((A[0]+C[0])/2+14, (A[1]+C[1])/2), ((A[0]+B[0])/2-14, (A[1]+B[1])/2)]
        for (mx, my), sv in zip(mids, [sides[0], sides[1], sides[2]]):
            parts.append(f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="11" fill="#1E7A44">{sv}</text>')
    if blank:
        cap = "Classify by angle AND by side."
    else:
        cap = f"By angle: {ang_label}" + (f"   |   By side: {side_label}" if side_label else "")
    parts.insert(0, f'<text x="{w/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{cap}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def angle_sum_triangle_svg(a=60, b=70, mode="sum", blank=False, **kw):
    """A triangle with two interior angles labelled and the third left
    for the student (mode='sum': third interior angle via 180° sum), OR
    an exterior-angle diagram where the exterior angle at one vertex is
    shown equal to the sum of the two remote interior angles
    (mode='exterior') (Level 16 CUM1). blank=True hides the computed
    value only -- the given angles always stay visible."""
    a, b = int(a), int(b)
    c = 180 - a - b
    w, h = 320, 280
    kind = "obtuse" if max(a, b, c) > 90 else ("right" if max(a, b, c) == 90 else "acute")
    A, B, C = _triangle_pts(kind, w, h)
    parts = []
    parts.append(f'<polygon points="{A[0]:.1f},{A[1]:.1f} {B[0]:.1f},{B[1]:.1f} {C[0]:.1f},{C[1]:.1f}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<text x="{A[0]:.1f}" y="{A[1]-12:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#A6362B">{a}°</text>')
    parts.append(f'<text x="{B[0]+14:.1f}" y="{B[1]+18:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#A6362B">{b}°</text>')
    c_str = "?" if blank else f"{c}°"
    if mode == "exterior":
        # extend BC beyond C to show the exterior angle at C
        ext_x = C[0] + (C[0] - B[0]) * 0.5
        ext_y = C[1] + (C[1] - B[1]) * 0.5
        parts.append(f'<line x1="{B[0]:.1f}" y1="{B[1]:.1f}" x2="{ext_x:.1f}" y2="{ext_y:.1f}" stroke="#1B5E8C" stroke-width="2" stroke-dasharray="5,3"/>')
        ext_val = a + b
        ext_str = "?" if blank else f"{ext_val}°"
        parts.append(f'<text x="{C[0]-10:.1f}" y="{C[1]+16:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#7D3C98">{c_str}</text>')
        parts.append(f'<text x="{ext_x+14:.1f}" y="{ext_y-2:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#1E7A44">{ext_str}</text>')
        cap = f"Exterior angle = {a}° + {b}° = {ext_str}  (remote interior angles)" if not blank else "Exterior angle = sum of the two remote interior angles"
    else:
        parts.append(f'<text x="{C[0]:.1f}" y="{C[1]+16:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#7D3C98">{c_str}</text>')
        cap = f"{a}° + {b}° + {c_str} = 180°" if not blank else f"{a}° + {b}° + ? = 180°"
    parts.insert(0, f'<text x="{w/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{cap}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def congruence_svg(rule="SAS", blank=False, **kw):
    """Two triangles side by side with the matching parts marked
    exactly as the given congruence rule requires: tick marks (single/
    double/triple) on equal sides, arc marks on equal angles, a square
    for the right angle in RHS. This is the picture that makes 'which
    parts must match' concrete (Level 16D). blank=True removes the rule
    name from the caption, leaving only the marks for the student to
    read off the rule."""
    w, h = 420, 240
    gap = 210
    def tri(ox):
        A = (ox + 70, 40)
        B = (ox, 200)
        C = (ox + 150, 200)
        return A, B, C
    A1, B1, C1 = tri(20)
    A2, B2, C2 = tri(20 + gap)
    parts = []

    def draw(A, B, C, color):
        return f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="#EAF4FC" stroke="{color}" stroke-width="2.5"/>'

    def tick(P, Q, n, color, offset=0.5):
        mx, my = P[0] + (Q[0]-P[0])*offset, P[1] + (Q[1]-P[1])*offset
        import math as _m
        dx, dy = Q[0]-P[0], Q[1]-P[1]
        ln = _m.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        out = []
        for k in range(n):
            off_along = (k - (n-1)/2) * 7
            px, py = mx + (dx/ln)*off_along, my + (dy/ln)*off_along
            out.append(f'<line x1="{px-nx*5:.1f}" y1="{py-ny*5:.1f}" x2="{px+nx*5:.1f}" y2="{py+ny*5:.1f}" stroke="{color}" stroke-width="2"/>')
        return "".join(out)

    parts.append(draw(A1, B1, C1, "#1B5E8C"))
    parts.append(draw(A2, B2, C2, "#A6362B"))
    for (P, lbl) in [(A1, "A"), (B1, "B"), (C1, "C")]:
        parts.append(f'<text x="{P[0]:.1f}" y="{P[1]+(-8 if P[1]<100 else 16):.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#1B5E8C">{lbl}</text>')
    for (P, lbl) in [(A2, "D"), (B2, "E"), (C2, "F")]:
        parts.append(f'<text x="{P[0]:.1f}" y="{P[1]+(-8 if P[1]<100 else 16):.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">{lbl}</text>')

    mark_color = "#1E7A44"
    if rule == "SSS":
        for n, (P1, Q1, P2, Q2) in enumerate([(A1,B1,A2,B2), (B1,C1,B2,C2), (A1,C1,A2,C2)], start=1):
            parts.append(tick(P1, Q1, n, mark_color)); parts.append(tick(P2, Q2, n, mark_color))
    elif rule == "SAS":
        parts.append(tick(A1, B1, 1, mark_color)); parts.append(tick(A2, B2, 1, mark_color))
        parts.append(tick(A1, C1, 2, mark_color)); parts.append(tick(A2, C2, 2, mark_color))
        parts.append(f'<path d="M {A1[0]-14:.1f} {A1[1]+18:.1f} Q {A1[0]:.1f} {A1[1]+8:.1f} {A1[0]+14:.1f} {A1[1]+18:.1f}" fill="none" stroke="#7D3C98" stroke-width="2"/>')
        parts.append(f'<path d="M {A2[0]-14:.1f} {A2[1]+18:.1f} Q {A2[0]:.1f} {A2[1]+8:.1f} {A2[0]+14:.1f} {A2[1]+18:.1f}" fill="none" stroke="#7D3C98" stroke-width="2"/>')
    elif rule in ("ASA", "AAS"):
        parts.append(f'<path d="M {B1[0]+10:.1f} {B1[1]-18:.1f} Q {B1[0]+18:.1f} {B1[1]-8:.1f} {B1[0]+22:.1f} {B1[1]-2:.1f}" fill="none" stroke="#7D3C98" stroke-width="2"/>')
        parts.append(f'<path d="M {B2[0]+10:.1f} {B2[1]-18:.1f} Q {B2[0]+18:.1f} {B2[1]-8:.1f} {B2[0]+22:.1f} {B2[1]-2:.1f}" fill="none" stroke="#7D3C98" stroke-width="2"/>')
        parts.append(f'<path d="M {C1[0]-22:.1f} {C1[1]-2:.1f} Q {C1[0]-18:.1f} {C1[1]-8:.1f} {C1[0]-10:.1f} {C1[1]-18:.1f}" fill="none" stroke="#B8860B" stroke-width="2"/>')
        parts.append(f'<path d="M {C2[0]-22:.1f} {C2[1]-2:.1f} Q {C2[0]-18:.1f} {C2[1]-8:.1f} {C2[0]-10:.1f} {C2[1]-18:.1f}" fill="none" stroke="#B8860B" stroke-width="2"/>')
        parts.append(tick(B1, C1, 1, mark_color)); parts.append(tick(B2, C2, 1, mark_color))
    elif rule == "RHS":
        for (P, Q, R) in [(A1, B1, C1), (A2, B2, C2)]:
            sx = 1 if R[0] > P[0] else -1
            parts.append(f'<rect x="{P[0]-2:.1f}" y="{P[1]-2:.1f}" width="10" height="10" fill="none" stroke="#B8860B" stroke-width="1.6"/>')
        parts.append(tick(B1, C1, 1, mark_color)); parts.append(tick(B2, C2, 1, mark_color))
        parts.append(tick(A1, B1, 2, mark_color)); parts.append(tick(A2, B2, 2, mark_color))

    if blank:
        cap = "Which parts are marked equal? Name the congruence rule."
    else:
        cap = f"Marked parts match the {rule} rule -- so Triangle ABC = Triangle DEF"
    parts.insert(0, f'<text x="{w/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{cap}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def triangle_inequality_svg(a=3, b=4, c=5, blank=False, **kw):
    """Shows the three side lengths as bars, with the two shorter ones
    stacked to compare against the longest -- makes the triangle
    inequality check (sum of two smaller sides vs the largest) visual
    instead of purely arithmetic (Level 16E). blank=True hides the
    verdict, keeping the bars and the given lengths."""
    a, b, c = float(a), float(b), float(c)
    s1, s2, s3 = sorted([a, b, c])  # s1<=s2<=s3
    valid = (s1 + s2) > s3
    w, h = 360, 220
    unit = min(280 / max(s1+s2, s3), 30)
    bar_h = 26
    parts = []
    y1 = 50
    parts.append(f'<rect x="40" y="{y1}" width="{s1*unit:.1f}" height="{bar_h}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2"/>')
    parts.append(f'<text x="{40+s1*unit/2:.1f}" y="{y1+bar_h/2+5:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#1B5E8C">{s1:g}</text>')
    parts.append(f'<rect x="{40+s1*unit:.1f}" y="{y1}" width="{s2*unit:.1f}" height="{bar_h}" fill="#E7F8ED" stroke="#1E7A44" stroke-width="2"/>')
    parts.append(f'<text x="{40+s1*unit+s2*unit/2:.1f}" y="{y1+bar_h/2+5:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#1E7A44">{s2:g}</text>')
    parts.append(f'<text x="{40+(s1+s2)*unit+8:.1f}" y="{y1+bar_h/2+5:.1f}" font-family="Helvetica-Bold" font-size="12" fill="#5D6D7E">= {s1+s2:g} together</text>')
    y2 = y1 + bar_h + 24
    parts.append(f'<rect x="40" y="{y2}" width="{s3*unit:.1f}" height="{bar_h}" fill="#FDEDEB" stroke="#A6362B" stroke-width="2"/>')
    parts.append(f'<text x="{40+s3*unit/2:.1f}" y="{y2+bar_h/2+5:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">{s3:g} (longest side)</text>')
    # comparison guide line at s3 length, dropped down to compare visually
    parts.append(f'<line x1="{40+s3*unit:.1f}" y1="{y1-8:.1f}" x2="{40+s3*unit:.1f}" y2="{y2+bar_h+8:.1f}" stroke="#9AA5B1" stroke-width="1.4" stroke-dasharray="4,3"/>')
    if blank:
        cap = f"Do the two shorter sides ({s1:g} + {s2:g}) beat the longest ({s3:g})?"
    else:
        verdict = "VALID triangle" if valid else "NOT a triangle"
        symbol = "beats" if valid else "does not beat"
        cap = f"{s1:g} + {s2:g} = {s1+s2:g}, which {symbol} {s3:g}  -->  {verdict}"
    parts.insert(0, f'<text x="{w/2}" y="22" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{cap}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def isosceles_theorem_svg(base_angle=65, blank=False, **kw):
    """An isosceles triangle with the two equal sides tick-marked and
    the two equal base angles arc-marked -- the picture behind 'angles
    opposite equal sides are equal' (Level 16E). blank=True hides the
    second base-angle's value, keeping the tick/arc marks (the given
    fact) visible."""
    base_angle = float(base_angle)
    vertex = 180 - 2 * base_angle
    w, h = 320, 260
    A = (160, 40)
    B = (50, 210)
    C = (270, 210)
    parts = []
    parts.append(f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    for (P, Q) in [(A, B), (A, C)]:
        mx, my = (P[0]+Q[0])/2, (P[1]+Q[1])/2
        import math as _m
        dx, dy = Q[0]-P[0], Q[1]-P[1]
        ln = _m.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        parts.append(f'<line x1="{mx-nx*5:.1f}" y1="{my-ny*5:.1f}" x2="{mx+nx*5:.1f}" y2="{my+ny*5:.1f}" stroke="#1E7A44" stroke-width="2.2"/>')
    parts.append(f'<text x="{A[0]:.1f}" y="{A[1]-12:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#7D3C98">{vertex:g}°</text>')
    parts.append(f'<text x="{B[0]+16:.1f}" y="{B[1]-6:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#A6362B">{base_angle:g}°</text>')
    other_str = "?" if blank else f"{base_angle:g}°"
    parts.append(f'<text x="{C[0]-16:.1f}" y="{C[1]-6:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#A6362B">{other_str}</text>')
    parts.append(f'<path d="M {B[0]+22:.1f} {B[1]:.1f} A 22 22 0 0 1 {B[0]+10:.1f} {B[1]-19:.1f}" fill="none" stroke="#B8860B" stroke-width="1.8"/>')
    parts.append(f'<path d="M {C[0]-22:.1f} {C[1]:.1f} A 22 22 0 0 0 {C[0]-10:.1f} {C[1]-19:.1f}" fill="none" stroke="#B8860B" stroke-width="1.8"/>')
    cap = "Equal sides (tick marks) -> equal base angles" if blank else f"Equal sides -> base angles equal: both {base_angle:g}°"
    parts.insert(0, f'<text x="{w/2}" y="22" text-anchor="middle" font-family="Helvetica-Bold" font-size="12.5" fill="#2C3E50">{cap}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def similar_triangles_svg(sides1=(3, 4, 5), k=2, blank=False, **kw):
    """Two similar triangles drawn to true relative scale, small one
    fully labelled, large one showing the scale factor -- makes 'same
    shape, different size, sides in the same ratio' concrete (Level
    16F). blank=True hides the large triangle's side lengths."""
    a, b, c = sides1
    k = float(k)
    w, h = 420, 260
    unit1 = 60 / max(a, b, c)
    unit2 = unit1  # keep both drawn at a readable size; scale is shown by side length text, not by literal pixel scale, so the small triangle stays legible
    A1 = (70, 60); B1 = (70 - 0, 60 + b*unit1); 
    # build small right-ish triangle using a,b as legs for a clean look, hyp c labeled along hypotenuse
    A1 = (70, 190)
    B1 = (70, 190 - b*unit1)
    C1 = (70 + a*unit1, 190)
    scale2 = 70 + a*unit1 + 60
    A2 = (scale2, 190)
    B2 = (scale2, 190 - b*unit1*1.5)
    C2 = (scale2 + a*unit1*1.5, 190)
    parts = []
    parts.append(f'<polygon points="{A1[0]},{A1[1]} {B1[0]},{B1[1]} {C1[0]},{C1[1]}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2.5"/>')
    parts.append(f'<polygon points="{A2[0]},{A2[1]} {B2[0]},{B2[1]} {C2[0]},{C2[1]}" fill="#FDEDEB" stroke="#A6362B" stroke-width="2.5"/>')
    parts.append(f'<text x="{(A1[0]+B1[0])/2-12:.1f}" y="{(A1[1]+B1[1])/2:.1f}" font-family="Helvetica-Bold" font-size="12" fill="#1B5E8C">{b:g}</text>')
    parts.append(f'<text x="{(A1[0]+C1[0])/2:.1f}" y="{A1[1]+16:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#1B5E8C">{a:g}</text>')
    parts.append(f'<text x="{(B1[0]+C1[0])/2+14:.1f}" y="{(B1[1]+C1[1])/2:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#1B5E8C">{c:g}</text>')
    b2, a2v, c2v = ("?", "?", "?") if blank else (f"{b*k:g}", f"{a*k:g}", f"{c*k:g}")
    parts.append(f'<text x="{(A2[0]+B2[0])/2-14:.1f}" y="{(A2[1]+B2[1])/2:.1f}" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">{b2}</text>')
    parts.append(f'<text x="{(A2[0]+C2[0])/2:.1f}" y="{A2[1]+16:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">{a2v}</text>')
    parts.append(f'<text x="{(B2[0]+C2[0])/2+16:.1f}" y="{(B2[1]+C2[1])/2:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#A6362B">{c2v}</text>')
    # right-angle squares to make the correspondence obvious
    parts.append(f'<rect x="{A1[0]:.1f}" y="{A1[1]-9:.1f}" width="9" height="9" fill="none" stroke="#5D6D7E" stroke-width="1.4"/>')
    parts.append(f'<rect x="{A2[0]:.1f}" y="{A2[1]-9:.1f}" width="9" height="9" fill="none" stroke="#5D6D7E" stroke-width="1.4"/>')
    cap = f"Scale factor = {k:g}  --  corresponding sides all x{k:g}"
    parts.insert(0, f'<text x="{w/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{cap}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def midpoint_theorem_svg(third_side=10, blank=False, **kw):
    """Triangle ABC with D, E the true MIDPOINTS of AB and AC, DE drawn
    parallel to BC and visibly half its length -- the picture for the
    Midpoint Theorem (Level 16 CUM2). blank=True hides DE's computed
    length."""
    third_side = float(third_side)
    w, h = 320, 300
    A = (160, 45); B = (40, 260); C = (280, 260)
    D = ((A[0]+B[0])/2, (A[1]+B[1])/2)
    E = ((A[0]+C[0])/2, (A[1]+C[1])/2)
    parts = []
    parts.append(f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="none" stroke="#2C3E50" stroke-width="2.5"/>')
    parts.append(f'<line x1="{D[0]:.1f}" y1="{D[1]:.1f}" x2="{E[0]:.1f}" y2="{E[1]:.1f}" stroke="#1B5E8C" stroke-width="2.5"/>')
    for (P, Q) in [(A, D), (D, B), (A, E), (E, C)]:
        mx, my = (P[0]+Q[0])/2, (P[1]+Q[1])/2
        import math as _m
        dx, dy = Q[0]-P[0], Q[1]-P[1]
        ln = _m.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        parts.append(f'<line x1="{mx-nx*4:.1f}" y1="{my-ny*4:.1f}" x2="{mx+nx*4:.1f}" y2="{my+ny*4:.1f}" stroke="#1E7A44" stroke-width="2"/>')
    for (P, lbl) in [(A, "A"), (B, "B"), (C, "C"), (D, "D"), (E, "E")]:
        parts.append(f'<circle cx="{P[0]:.1f}" cy="{P[1]:.1f}" r="4" fill="#A6362B"/>')
        ly = P[1] - 12 if lbl in ("A",) else (P[1] + 16 if lbl in ("B","C") else P[1] - 10)
        lx = P[0] - 14 if lbl in ("B", "D") else (P[0] + 14 if lbl in ("C", "E") else P[0])
        parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#2C3E50">{lbl}</text>')
    de_str = "?" if blank else f"{third_side/2:g}"
    parts.append(f'<text x="{(D[0]+E[0])/2:.1f}" y="{(D[1]+E[1])/2-10:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#1B5E8C">DE = {de_str}</text>')
    parts.append(f'<text x="{(B[0]+C[0])/2:.1f}" y="{B[1]+22:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#5D6D7E">BC = {third_side:g}</text>')
    cap = "D, E are midpoints -- DE || BC and DE = ½ BC"
    parts.insert(0, f'<text x="{w/2}" y="20" text-anchor="middle" font-family="Helvetica-Bold" font-size="12.5" fill="#2C3E50">{cap}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def pythagoras_svg(a=3, b=4, c=5, find="hyp", blank=False, **kw):
    """A right triangle with a literal square constructed on each side,
    each square labelled with its area (a², b², c²) -- the classic
    'squares on the sides' proof picture, with a² + b² = c² read
    straight off the areas. find='hyp' or 'leg' controls which square
    is left blank as the unknown. blank=True additionally hides the
    numeric equation at the bottom (keeps only the square-area labels
    appropriate to what's given vs asked)."""
    a, b, c = float(a), float(b), float(c)
    scale = 130 / max(a, b, c, 6)
    aw, bw = a*scale, b*scale
    w, h = 420, 380
    # place right angle at origin-ish
    ox, oy = 150, 230
    Bp = (ox, oy)          # right angle vertex
    Cp = (ox + aw, oy)     # along +x
    Ap = (ox, oy - bw)     # along -y
    parts = []
    # square on base (a) below
    parts.append(f'<rect x="{Bp[0]:.1f}" y="{oy:.1f}" width="{aw:.1f}" height="{aw:.1f}" fill="#EAF4FC" stroke="#1B5E8C" stroke-width="2"/>')
    a2_str = "?" if (blank and find == "leg_a") else f"{a:g}²={a*a:g}"
    parts.append(f'<text x="{Bp[0]+aw/2:.1f}" y="{oy+aw/2+5:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#1B5E8C">{a2_str}</text>')
    # square on height (b) to the left
    parts.append(f'<rect x="{ox-bw:.1f}" y="{oy-bw:.1f}" width="{bw:.1f}" height="{bw:.1f}" fill="#E7F8ED" stroke="#1E7A44" stroke-width="2"/>')
    b2_str = "?" if (blank and find == "leg_b") else f"{b:g}²={b*b:g}"
    parts.append(f'<text x="{ox-bw/2:.1f}" y="{oy-bw/2+5:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#1E7A44">{b2_str}</text>')
    # triangle itself
    parts.append(f'<polygon points="{Ap[0]},{Ap[1]} {Bp[0]},{Bp[1]} {Cp[0]},{Cp[1]}" fill="#FFF8E1" stroke="#2C3E50" stroke-width="2.5"/>')
    parts.append(f'<rect x="{Bp[0]:.1f}" y="{Bp[1]-10:.1f}" width="10" height="10" fill="none" stroke="#2C3E50" stroke-width="1.5"/>')
    # square on hypotenuse, rotated -- approximate with a polygon using perpendicular offset
    import math as _m
    hx, hy = Cp[0]-Ap[0], Cp[1]-Ap[1]
    hl = _m.hypot(hx, hy) or 1
    nx, ny = -hy/hl, hx/hl
    P1, P2 = Ap, Cp
    P3 = (P2[0] + nx*hl, P2[1] + ny*hl)
    P4 = (P1[0] + nx*hl, P1[1] + ny*hl)
    parts.append(f'<polygon points="{P1[0]:.1f},{P1[1]:.1f} {P2[0]:.1f},{P2[1]:.1f} {P3[0]:.1f},{P3[1]:.1f} {P4[0]:.1f},{P4[1]:.1f}" fill="#FDEDEB" stroke="#A6362B" stroke-width="2"/>')
    cx_h, cy_h = (P1[0]+P2[0]+P3[0]+P4[0])/4, (P1[1]+P2[1]+P3[1]+P4[1])/4
    c2_str = "?" if (blank and find == "hyp") else f"{c:g}²={c*c:g}"
    parts.append(f'<text x="{cx_h:.1f}" y="{cy_h+5:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="13" fill="#A6362B">{c2_str}</text>')
    if find == "hyp":
        cap = f"a² + b² = c²  -->  {a:g}² + {b:g}² = c²" if blank else f"{a:g}² + {b:g}² = {a*a:g} + {b*b:g} = {a*a+b*b:g} = c²  -->  c = {c:g}"
    elif find == "leg_b":
        cap = "a² + b² = c²  -->  find the missing leg" if blank else f"{c:g}² - {a:g}² = {c*c:g} - {a*a:g} = {b*b:g}  -->  b = {b:g}"
    else:
        cap = "a² + b² = c²  -->  find the missing leg" if blank else f"{c:g}² - {b:g}² = {c*c:g} - {b*b:g} = {a*a:g}  -->  a = {a:g}"
    parts.insert(0, f'<text x="{w/2}" y="24" text-anchor="middle" font-family="Helvetica-Bold" font-size="12.5" fill="#2C3E50">{cap}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def area_same_base_svg(base=8, height=5, shape="para_para", blank=False, **kw):
    """Two shapes (parallelogram-parallelogram, parallelogram-triangle,
    or triangle-triangle) drawn sharing the SAME base and squeezed
    between the SAME pair of parallel lines, with different slants --
    makes 'area only depends on base x height, not the slant' visible
    at a glance (Level 16 CUM3). blank=True hides the computed areas."""
    base, height = float(base), float(height)
    w, h = 420, 220
    scale = min(280 / base, 22)
    bw = base * scale
    ht = height * scale
    x0 = 60
    y_top = 40
    y_bot = y_top + ht
    parts = []
    parts.append(f'<line x1="10" y1="{y_top}" x2="{w-10}" y2="{y_top}" stroke="#9AA5B1" stroke-width="1.6" stroke-dasharray="5,3"/>')
    parts.append(f'<line x1="10" y1="{y_bot}" x2="{w-10}" y2="{y_bot}" stroke="#9AA5B1" stroke-width="1.6" stroke-dasharray="5,3"/>')
    parts.append(f'<line x1="{x0}" y1="{y_bot}" x2="{x0+bw}" y2="{y_bot}" stroke="#2C3E50" stroke-width="3"/>')
    slant1, slant2 = 18, -26
    def shape_pts(kind, slant):
        if kind == "para":
            return [(x0, y_bot), (x0+bw, y_bot), (x0+bw+slant, y_top), (x0+slant, y_top)]
        else:  # triangle apex
            apex_x = x0 + bw/2 + slant
            return [(x0, y_bot), (x0+bw, y_bot), (apex_x, y_top)]
    k1, k2 = shape.split("_")
    pts1 = shape_pts(k1, slant1)
    pts2 = shape_pts(k2, slant2)
    poly1 = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts1)
    poly2 = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts2)
    parts.append(f'<polygon points="{poly1}" fill="#1B5E8C" opacity="0.28" stroke="#1B5E8C" stroke-width="2.2"/>')
    parts.append(f'<polygon points="{poly2}" fill="#A6362B" opacity="0.22" stroke="#A6362B" stroke-width="2.2"/>')
    parts.append(f'<line x1="{x0+8:.1f}" y1="{y_bot:.1f}" x2="{x0+8:.1f}" y2="{y_top:.1f}" stroke="#1E7A44" stroke-width="1.6" stroke-dasharray="3,2"/>')
    h_str = "?" if blank else f"{height:g}"
    parts.append(f'<text x="{x0+14:.1f}" y="{(y_top+y_bot)/2:.1f}" font-family="Helvetica-Bold" font-size="11" fill="#1E7A44">h={h_str}</text>')
    parts.append(f'<text x="{x0+bw/2:.1f}" y="{y_bot+18:.1f}" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">base = {base:g}</text>')
    para_area = base * height
    tri_area = base * height / 2
    if blank:
        cap = "Same base, same parallels -- what can you say about the areas?"
    elif shape == "para_para":
        cap = f"Both area = base x height = {base:g} x {height:g} = {para_area:g}  (EQUAL)"
    elif k1 == "para":
        cap = f"Parallelogram = {para_area:g}   Triangle = ½ x {para_area:g} = {tri_area:g}"
    else:
        cap = f"Both triangles: area = ½ x {base:g} x {height:g} = {tri_area:g}  (EQUAL)"
    parts.insert(0, f'<text x="{w/2}" y="18" text-anchor="middle" font-family="Helvetica-Bold" font-size="12" fill="#2C3E50">{cap}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


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
    "plot_points_grid": plot_points_grid_svg,
    "distance_segment": distance_segment_svg,
    "midpoint_segment": midpoint_segment_svg,
    "section_segment": section_segment_svg,
    "triangle_coords": triangle_coords_svg,
    "points_lines_rays": points_lines_rays_svg,
    "angle_pair": angle_pair_svg,
    "transversal_angles": transversal_angles_svg,
    "bpt_triangle": bpt_triangle_svg,
    "quadrilateral_types": quadrilateral_types_svg,
    "quadrilateral_diagonals": quadrilateral_diagonals_svg,
    "polygon_angle_sum": polygon_angle_sum_svg,
    "circle_basics": circle_basics_svg,
    "circle_chord": circle_chord_svg,
    "circle_tangent": circle_tangent_svg,
    "circle_central_inscribed_angle": circle_central_inscribed_angle_svg,
    "cyclic_quadrilateral_theorem": cyclic_quadrilateral_theorem_svg,
    "rectangle_dims": rectangle_dims_svg,
    "square_dims": square_dims_svg,
    "triangle_area_diagram": triangle_area_svg,
    "circle_area_diagram": circle_area_svg,
    "cuboid_3d": cuboid_3d_svg,
    "cube_3d": cube_3d_svg,
    "cuboid_net": cuboid_net_svg,
    "cylinder_3d": cylinder_3d_svg,
    "cone_3d": cone_3d_svg,
    "sphere_3d": sphere_3d_svg,
    "hemisphere_3d": hemisphere_3d_svg,
    "composite_mensuration": composite_mensuration_svg,
    "circle_sector": circle_sector_svg,
    "circle_ring": circle_ring_svg,
    "factor_array": factor_array_svg,
    "factor_rainbow": factor_rainbow_svg,
    "multiples_number_line": multiples_number_line_svg,
    "hundred_grid_highlight": hundred_grid_highlight_svg,
    "ladder_division": ladder_division_svg,
    "euclidean_algorithm": euclidean_algorithm_svg,
    "ratio_objects": ratio_objects_svg,
    "ratio_table": ratio_table_svg,
    "double_number_line": double_number_line_svg,
    "continued_ratio_bar": continued_ratio_bar_svg,
    "unit_rate": unit_rate_svg,
    "similar_figures": similar_figures_svg,
    "scale_comparison": scale_comparison_svg,
    "word_to_expression": word_to_expression_svg,
    "single_bracket_area": single_bracket_area_svg,
    "solve_equation_ladder": solve_equation_ladder_svg,
    "inverse_machine": inverse_machine_svg,
    "consecutive_bar": consecutive_bar_svg,
    "power_expansion": power_expansion_svg,
    "square_dots_grid": square_dots_grid_svg,
    "cube_stack_3d": cube_stack_3d_svg,
    "index_law_visual": index_law_visual_svg,
    "power_ladder": power_ladder_svg,
    "sqrt_side_area": sqrt_side_area_svg,
    "sci_notation_slider": sci_notation_slider_svg,
    "surd_simplify_tree": surd_simplify_tree_svg,
    "identity_square": identity_square_svg,
    "factor_x_method": factor_x_method_svg,
    "poly_anatomy": poly_anatomy_svg,
    "degree_staircase": degree_staircase_svg,
    "hcf_factor_boxes": hcf_factor_boxes_svg,
    "division_algorithm_box": division_algorithm_box_svg,
    "quadrant_map": quadrant_map_svg,
    "point_plot_path": point_plot_path_svg,
    "slope_intercept_anatomy": slope_intercept_anatomy_svg,
    "triangle_classify": triangle_classify_svg,
    "angle_sum_triangle": angle_sum_triangle_svg,
    "congruence": congruence_svg,
    "triangle_inequality": triangle_inequality_svg,
    "isosceles_theorem": isosceles_theorem_svg,
    "similar_triangles": similar_triangles_svg,
    "midpoint_theorem": midpoint_theorem_svg,
    "pythagoras": pythagoras_svg,
    "area_same_base": area_same_base_svg,
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
