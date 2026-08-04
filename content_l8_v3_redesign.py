"""
Fear Less Maths — LEVEL 8 (Decimals) v3 worksheet architecture
(2026-08-04)

Per direct request, a variant of the Level 6/7 v3 pattern:

  Q1-6   Freshly-authored diagram questions using the sheet's own topic,
         built on NEW SVG decimal diagrams (grid boxes, place-value
         chart, number line, area model, decimal-point-shift, add/sub
         alignment) added to diagram_engine.py specifically for this
         level -- not reused PNG diagrams, and not procedural/matching
         formats. Q1-2 worked (fully shown), Q3-6 blank (student fills
         in), same concrete-before-abstract fade used throughout FLM.
  Q7-12  Text-based questions on the same topic, no diagram -- sampled
         from the sheet's own already-vetted non-diagram content for
         variety, same principle as Level 6/7's Block 1b.
  Q13-15 "Quick Review" (PYQ) -- TOUGHENED prerequisite check: 2-digit x
         3-digit multiplication (Level 4), 3-digit / 2-digit division
         (Level 5), and decimal<->fraction conversion at a harder range
         than Level 7's own teaching tier (Level 7 -- the most directly
         relevant skill, since a decimal literally IS a fraction).
  Q16-20 "Speed Calculation" -- 5 TOUGHENED whole-number arithmetic
         questions (multiplication/division/subtraction, 2-3 digit),
         escalating across sheets 1-4 -- deliberately harder than Level
         7's version of this block, continuing the escalation, and
         deliberately whole-number (not decimal) so it stays distinct
         from the sheet's own topic and from Quick Review.
"""
import random
import math
from content import cb, q
import content_l7_redesign as _L8


def _gcd(a, b):
    return math.gcd(a, b)


# ───────────────────────── Block 1a: fresh SVG diagram questions ─────────────────────────

_TIERS = {
    1: {"den2": 10, "wholemax": 9, "mulf": (12, 30), "sub": (200, 500)},
    2: {"den2": 100, "wholemax": 30, "mulf": (15, 40), "sub": (300, 700)},
    3: {"den2": 100, "wholemax": 60, "mulf": (20, 55), "sub": (400, 850)},
    4: {"den2": 1000, "wholemax": 99, "mulf": (25, 80), "sub": (500, 999)},
}


def _mk(text, dtype, params):
    return q(text, "diagram", "____", "", dtype, params)


def _block1a_A(sheet):
    """8A: Tenths & hundredths -- decimal grid, size alternating 10/100."""
    items = []
    for i in range(6):
        size = 10 if i % 2 == 0 else 100
        shaded = random.randint(1, size - 1)
        blank = i >= 2
        items.append(_mk(f"Shade {shaded}/{size} on the grid. What decimal is this?",
                          "decimal_grid", {"shaded": shaded, "size": size, "blank": blank}))
    return items


def _block1b_extra_A(sheet):
    return []


def _block1a_B(sheet):
    """8B: Thousandths, place value -- place-value chart."""
    items = []
    for i in range(6):
        whole = random.randint(0, 99)
        frac_len = 3 if i % 2 == 1 else 2
        frac = random.randint(0, 10**frac_len - 1)
        number = f"{whole}.{str(frac).zfill(frac_len)}"
        blank = i >= 2
        items.append(_mk(f"Fill the place value chart for {number}.",
                          "decimal_place_chart", {"number": number, "blank": blank}))
    return items


def _block1a_C(sheet):
    """8C: Comparing decimals -- number line with one value marked."""
    items = []
    for i in range(6):
        lo, hi = 0.0, 1.0
        mark = round(random.randint(1, 9) / 10, 1)
        blank = i >= 2
        items.append(_mk(f"Where does {mark} sit on the number line?",
                          "decimal_numberline", {"lo": lo, "hi": hi, "mark": mark, "divisions": 10, "blank": blank}))
    return items


def _block1a_D(sheet):
    """8D: Spot the Mistake -- place-value chart to check digit placement."""
    items = []
    for i in range(6):
        whole = random.randint(1, 40)
        frac = random.randint(1, 99)
        number = f"{whole}.{str(frac).zfill(2)}"
        blank = i >= 2
        items.append(_mk(f"Fill the place value chart for {number}, then check: which digit is in the hundredths place?",
                          "decimal_place_chart", {"number": number, "blank": blank}))
    return items


def _block1a_E(sheet):
    """8E: Decimal <-> Fraction -- grid shows both at once."""
    items = []
    for i in range(6):
        size = 10 if i % 2 == 0 else 100
        shaded = random.randint(1, size - 1)
        blank = i >= 2
        items.append(_mk(f"Shade {shaded}/{size}. Write it as BOTH a fraction and a decimal.",
                          "decimal_grid", {"shaded": shaded, "size": size, "blank": blank}))
    return items


def _block1a_F(sheet):
    """8F: Decimals on a number line -- direct fit."""
    items = []
    for i in range(6):
        mark = round(random.randint(1, 99) / 100, 2)
        blank = i >= 2
        items.append(_mk(f"Mark {mark} on the number line.",
                          "decimal_numberline", {"lo": 0.0, "hi": 1.0, "mark": mark, "divisions": 10, "blank": blank}))
    return items


def _block1a_G(sheet):
    """8G: Add & subtract decimals -- alignment diagram."""
    items = []
    for i in range(6):
        a = round(random.uniform(1, 40), 1)
        b = round(random.uniform(1, 40), 2)
        op = "+" if i % 2 == 0 else "-"
        if op == "-" and a < b:
            a, b = b, a
        blank = i >= 2
        items.append(_mk(f"{a} {op} {b} = ? Line up the decimal point first.",
                          "decimal_align", {"num1": str(a), "num2": str(b), "op": op, "blank": blank}))
    return items


def _block1a_H(sheet):
    """8H: Multiply decimals -- area model."""
    items = []
    for i in range(6):
        d1 = random.randint(2, 9)
        d2 = random.randint(2, 9)
        blank = i >= 2
        items.append(_mk(f"{d1/10:.1f} x {d2/10:.1f} = ? Use the area model.",
                          "decimal_area_model", {"d1": d1, "d2": d2, "dec1": 1, "dec2": 1, "blank": blank}))
    return items


def _block1a_I(sheet):
    """8I: Divide decimals -- point-shift (make the divisor a whole number)."""
    items = []
    for i in range(6):
        number = f"{random.randint(1,90)}.{random.randint(1,9)}"
        op = random.choice(["x10", "x100"])
        blank = i >= 2
        items.append(_mk(f"To divide by a decimal, first shift the point: {number} {op} = ?",
                          "decimal_shift", {"number": number, "op": op, "blank": blank}))
    return items


def _block1a_J(sheet):
    """8J: Money, measurement & rounding -- place-value chart (money = decimal)."""
    items = []
    for i in range(6):
        rupees = random.randint(1, 999)
        paise = random.randint(0, 99)
        number = f"{rupees}.{str(paise).zfill(2)}"
        blank = i >= 2
        items.append(_mk(f"Rs {number}: fill the place value chart. Round to the nearest whole rupee.",
                          "decimal_place_chart", {"number": number, "blank": blank}))
    return items


_BLOCK1A_BUILDERS = {
    "8A": _block1a_A, "8B": _block1a_B, "8C": _block1a_C, "8CUM1": _block1a_C,
    "8D": _block1a_D, "8E": _block1a_E, "8F": _block1a_F, "8CUM2": _block1a_F,
    "8G": _block1a_G, "8H": _block1a_H, "8I": _block1a_I, "8CUM3": _block1a_G,
    "8J": _block1a_J, "8REV": _block1a_E,
}


# ───────────────────────── Quick Review (toughened) ─────────────────────────

def _l8v3_quick_review(sheet):
    """3 questions: 2-digit x 3-digit multiplication (Level 4), 3-digit /
    2-digit division (Level 5), decimal<->fraction conversion at a
    harder range than Level 7's own teaching tier (Level 7 -- the most
    directly relevant skill, since a decimal literally IS a fraction)."""
    tiers = {
        1: {"mlo": 12, "mhi": 25, "mbig": 150, "dlo": 12, "dhi": 20, "fden": 10},
        2: {"mlo": 15, "mhi": 35, "mbig": 300, "dlo": 15, "dhi": 30, "fden": 20},
        3: {"mlo": 20, "mhi": 50, "mbig": 500, "dlo": 20, "dhi": 45, "fden": 25},
        4: {"mlo": 25, "mhi": 75, "mbig": 800, "dlo": 25, "dhi": 60, "fden": 50},
    }
    t = tiers[sheet]
    items = []

    a = random.randint(t["mlo"], t["mhi"])
    b = random.randint(100, t["mbig"])
    items.append(q(f"Quick Review (Level 4): {a} x {b} = ____", "fill", "Answer = ____"))

    d = random.randint(t["dlo"], t["dhi"])
    k = random.randint(t["dlo"], t["dhi"])
    n = d * k
    items.append(q(f"Quick Review (Level 5): {n} / {d} = ____", "fill", "Answer = ____"))

    den_choices = [d for d in (4, 5, 8, 10, 20, 25, 40, 50) if d <= t["fden"] * 2]
    den = random.choice(den_choices)
    num = random.randint(1, den - 1)
    if sheet % 2 == 1:
        items.append(q(f"Quick Review (Level 7): Write {num}/{den} as a decimal.", "fill", "Answer = ____"))
    else:
        whole = random.randint(0, 3)
        dec_digits = random.choice([1, 2])
        frac = random.randint(1, 10**dec_digits - 1)
        dec_str = f"{whole}.{str(frac).zfill(dec_digits)}"
        items.append(q(f"Quick Review (Level 7): Write {dec_str} as a fraction in simplest form.", "fill", "Answer = ____"))

    return items


# ───────────────────────── Speed Calculation (toughened) ─────────────────────────

def _l8v3_speed_calc(sheet):
    """5 rapid whole-number arithmetic questions, tougher than Level 7's
    version of this block (continuing the escalation) -- deliberately
    whole-number, not decimal, so it stays distinct from the sheet's own
    topic."""
    tiers = {
        1: {"mul_lo": 15, "mul_hi": 35, "div_hi": 15, "sub_lo": 200, "sub_hi": 600},
        2: {"mul_lo": 20, "mul_hi": 50, "div_hi": 18, "sub_lo": 300, "sub_hi": 750},
        3: {"mul_lo": 25, "mul_hi": 65, "div_hi": 22, "sub_lo": 400, "sub_hi": 900},
        4: {"mul_lo": 30, "mul_hi": 90, "div_hi": 25, "sub_lo": 500, "sub_hi": 999},
    }
    t = tiers[sheet]
    items = []
    shapes = ["mul2x1", "div", "sub3", "mul2x2", "div"]
    random.shuffle(shapes)
    for shape in shapes:
        if shape == "mul2x1":
            a = random.randint(t["mul_lo"], t["mul_hi"])
            b = random.randint(2, 9)
            items.append(q(f"Speed Calculation: {a} x {b} = ____", "fill", "Answer = ____"))
        elif shape == "mul2x2":
            a = random.randint(t["mul_lo"], t["mul_hi"])
            b = random.randint(11, t["div_hi"] + 12)
            items.append(q(f"Speed Calculation: {a} x {b} = ____", "fill", "Answer = ____"))
        elif shape == "div":
            b = random.randint(2, t["div_hi"])
            k = random.randint(t["mul_lo"] // 2, t["mul_hi"])
            a = b * k
            items.append(q(f"Speed Calculation: {a} / {b} = ____", "fill", "Answer = ____"))
        else:
            a = random.randint(t["sub_lo"], t["sub_hi"])
            b = random.randint(50, a - 20)
            items.append(q(f"Speed Calculation: {a} - {b} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── Assembly ─────────────────────────

_SOURCE_FN = {
    "8A": _L8._A_s, "8B": _L8._B_s, "8C": _L8._C_s, "8CUM1": _L8._CUM1_s,
    "8D": _L8._D_s, "8E": _L8._E_s, "8F": _L8._F_s, "8CUM2": _L8._CUM2_s,
    "8G": _L8._G_s, "8H": _L8._H_s, "8I": _L8._I_s, "8CUM3": _L8._CUM3_s,
    "8J": _L8._J_s, "8REV": _L8._REV_s,
}


def _item_key(item):
    return (item.get("text", ""), repr(item.get("diagram_params")))


def _build_block1b(code, sheet, exclude_keys):
    items = _SOURCE_FN[code](sheet)
    concept_items = [x for x in items if x.get("type") in ("concept_box", "tips_box")]
    qs = [x for x in items if x.get("type") not in ("concept_box", "tips_box")]
    tail_qs = [x for x in qs if not x.get("diagram_type") and _item_key(x) not in exclude_keys]
    tail_sorted = sorted(range(len(tail_qs)), key=lambda i: len(tail_qs[i].get("text", "")))
    block1b = [tail_qs[i] for i in tail_sorted[:6]] if tail_qs else []
    block1b.sort(key=lambda x: tail_qs.index(x))
    idx = 0
    while len(block1b) < 6:
        # Fallback: plain rounding/place-value fill question, always safe
        n = random.randint(10, 999) + idx
        block1b.append(q(f"Round {n/10:.1f} to the nearest whole number.", "fill", "Answer = ____"))
        idx += 1
    return concept_items, block1b


def build_v3_sheet(code, sheet):
    random.seed(8000 + hash(code) % 5000 + sheet * 31)
    block1a = _BLOCK1A_BUILDERS[code](sheet)
    used = {_item_key(x) for x in block1a}
    concept_items, block1b = _build_block1b(code, sheet, used)
    out = list(concept_items)
    out += block1a
    out += block1b
    out += _l8v3_quick_review(sheet)
    out += _l8v3_speed_calc(sheet)
    return out


LEVEL8_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _BLOCK1A_BUILDERS
}
