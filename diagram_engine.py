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


def object_group(count=5, kind="apple", group_size=5, **kw) -> BytesIO:
    """Concrete/Pictorial counting diagram: real-world objects in rows,
    grouped by `group_size` (default 5) with a visible gap between groups
    to support subitizing. Used for Pre-Level / CPA 'Intro' and 'Concept' sheets.
    No answer text is ever rendered on the image."""
    r = 16
    cell = r*2 + 14
    gap = 22
    cols = group_size
    rows = (count + group_size - 1) // group_size
    w = cols * cell + gap
    h = rows * cell + 20
    img, d = _blank(w, h)
    for row in range(rows):
        in_row = min(group_size, count - row*group_size)
        for c in range(in_row):
            x = 10 + r + c * cell
            y = 10 + r + row * cell
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
