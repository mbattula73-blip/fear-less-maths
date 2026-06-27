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


# ─── DIAGRAM FUNCTIONS ────────────────────────────────────────────────────────

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


def object_group(count=5, kind="apple", group_size=5, show_icon=True, **kw) -> BytesIO:
    """Concrete/Pictorial counting diagram: real-world objects in rows,
    grouped by `group_size` (default 5) with a visible gap between groups
    to support subitizing. Used for Pre-Level / CPA 'Intro' and 'Concept' sheets.
    No answer text is ever rendered on the image. A COUNT mascot+flag is
    drawn above by default (set show_icon=False to omit, e.g. when this
    is reused as a sub-component of another diagram)."""
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
        _draw_mini_mascot_flag(d, w/2 - 14, 26, 22, "count")
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
    with a VALUE mascot+flag above, for consistency with every other
    instructional diagram in Pre-Level / Pre Level 1."""
    rod_w, rod_h = 18, 90
    unit = 18
    gap = 8
    cols_per_row_tens = 5
    rows_tens = (tens + cols_per_row_tens - 1) // cols_per_row_tens if tens else 0
    cols_per_row_ones = 5
    rows_ones = (ones + cols_per_row_ones - 1) // cols_per_row_ones if ones else 0
    icon_h = 70
    w = max(cols_per_row_tens * (rod_w + gap), cols_per_row_ones * (unit + gap)) * 2 + 40
    h = max(rows_tens * (rod_h + gap), rows_ones * (unit + gap)) + 20 + icon_h
    img, d = _blank(w, h)
    _draw_mini_mascot_flag(d, w/2 - 14, 26, 22, "value")
    # Draw tens rods on the left half (outline only, tall shape = tens)
    for i in range(tens):
        row, col = divmod(i, cols_per_row_tens)
        x = 15 + col * (rod_w + gap)
        y = 15 + row * (rod_h + gap) + icon_h
        d.rectangle([x, y, x + rod_w, y + rod_h], outline=C_BORDER, width=2)
        for seg in range(1, 10):
            sy = y + seg * (rod_h / 10)
            d.line([x, sy, x + rod_w, sy], fill=C_BORDER, width=1)
    # Draw ones units on the right half (outline only, small shape = ones)
    ones_x_off = w // 2 + 10
    for i in range(ones):
        row, col = divmod(i, cols_per_row_ones)
        x = ones_x_off + col * (unit + gap)
        y = 15 + row * (unit + gap) + icon_h
        d.rectangle([x, y, x + unit, y + unit], outline=C_BORDER, width=2)
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
              "pattern": "PATTERN", "missing": "MISSING", "value": "VALUE"}


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
    block_area_h = 90
    half_w = 165
    w = half_w*2 + 30
    h = icon_h + block_area_h + 60
    img, d = _blank(w, h)
    _draw_mini_mascot_flag(d, w/2 - 14, 26, 22, "compare")
    d.line([half_w+15, icon_h+5, half_w+15, icon_h+block_area_h], fill=C_GRAY_D, width=2)

    def draw_side(n, x_off):
        tens, ones = divmod(n, 10)
        rod_w, rod_h, unit, gap = 10, 50, 10, 4
        for i in range(min(tens, 10)):
            row, col = divmod(i, 5)
            x = x_off + 10 + col*(rod_w+gap)
            y = icon_h + 10 + row*(rod_h+gap)
            d.rectangle([x, y, x+rod_w, y+rod_h], outline=C_BORDER, width=2)
        ones_x = x_off + 95
        for i in range(ones):
            row, col = divmod(i, 5)
            x = ones_x + col*(unit+gap)
            y = icon_h + 10 + row*(unit+gap)
            d.rectangle([x, y, x+unit, y+unit], outline=C_BORDER, width=2)

    draw_side(left, 0)
    draw_side(right, half_w+30)

    box_y = icon_h + block_area_h + 10
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


# ─── DISPATCHER ───────────────────────────────────────────────────────────────

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
}

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
