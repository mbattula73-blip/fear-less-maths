"""
Fear Less Maths — LEVEL 9 (Integers + Percentage) v3 worksheet architecture
(2026-08-04)

Same pattern as Level 8's v3 rewrite, with review/calculation content
toughened FURTHER than Level 8's own tier per direct request:

  Q1-6   Freshly-authored diagram questions using the sheet's own topic,
         built on NEW SVG diagrams (integer number line, integer "hop"
         jump visualization, sign-rule chart, percentage grid, percentage
         bar model, discount/markup price tag) added to diagram_engine.py
         specifically for this level. Q1-2 worked, Q3-6 blank.
  Q7-12  Text-based questions on the same topic, no diagram -- sampled
         from the sheet's own already-vetted non-diagram content.
  Q13-15 "Quick Review" (PYQ) -- toughened BEYOND Level 8's tier: 3-digit
         x 2-digit multiplication (Level 4), 4-digit / 2-digit division
         (Level 5), and a decimal operation at a harder range than
         Level 8's own teaching tier (Level 8 -- the most directly
         relevant skill, since percentages ARE decimals: 15% = 0.15).
  Q16-20 "Speed Calculation" -- 5 questions, toughened beyond Level 8's
         version of this block -- bigger multiplication/division/
         subtraction, escalating across sheets 1-4.
"""
import random
from content import cb, q
import content_l8_redesign as _L9


# ───────────────────────── Block 1a: fresh SVG diagram questions ─────────────────────────

def _mk(text, dtype, params):
    return q(text, "diagram", "____", "", dtype, params)


def _block1a_A(sheet):
    """9A: Integer concept & number line."""
    rng = {1: 10, 2: 15, 3: 20, 4: 25}[sheet]
    items = []
    for i in range(6):
        mark = random.randint(-rng, rng)
        blank = i >= 2
        items.append(_mk(f"Mark {mark} on the integer number line.",
                          "integer_numberline", {"lo": -rng, "hi": rng, "mark": mark, "blank": blank}))
    return items


def _block1a_B(sheet):
    """9B: Integer addition & subtraction -- hop visualization."""
    rng = {1: 8, 2: 12, 3: 16, 4: 20}[sheet]
    items = []
    for i in range(6):
        start = random.randint(-rng, rng)
        jump = random.randint(-rng, rng) or 3
        blank = i >= 2
        items.append(_mk(f"{start} {'+' if jump>=0 else ''}{jump} = ? Show the hop on the number line.",
                          "integer_hop", {"start": start, "jump": jump, "blank": blank}))
    return items


def _block1a_C(sheet):
    """9C: Properties of addition/subtraction -- hop, same-magnitude reversed."""
    rng = {1: 8, 2: 12, 3: 16, 4: 20}[sheet]
    items = []
    for i in range(6):
        start = random.randint(-rng, rng)
        jump = random.randint(-rng, rng) or -4
        blank = i >= 2
        items.append(_mk(f"{start} {'+' if jump>=0 else ''}{jump} = ? Show the hop.",
                          "integer_hop", {"start": start, "jump": jump, "blank": blank}))
    return items


def _block1a_D(sheet):
    """9D: Integer multiplication & division -- sign-rule chart."""
    rng = {1: 6, 2: 9, 3: 12, 4: 15}[sheet]
    items = []
    for i in range(6):
        a = random.choice([1, -1]) * random.randint(2, rng)
        b = random.choice([1, -1]) * random.randint(2, rng)
        op = "x" if i % 2 == 0 else "/"
        blank = i >= 2
        items.append(_mk(f"({a}) {op} ({b}) = ? Use the sign rule.",
                          "sign_rule_chart", {"a": a, "b": b, "op": op, "blank": blank}))
    return items


def _block1a_E(sheet):
    """9E: Properties of multiplication/division -- sign-rule chart."""
    return _block1a_D(sheet)


def _block1a_F(sheet):
    """9F: Word problems + BODMAS -- integer hop for the running total."""
    rng = {1: 10, 2: 15, 3: 20, 4: 25}[sheet]
    items = []
    for i in range(6):
        start = random.randint(-rng, rng)
        jump = random.randint(-rng, rng) or 5
        blank = i >= 2
        items.append(_mk(f"A submarine at {start}m moves {jump}m. New depth?",
                          "integer_hop", {"start": start, "jump": jump, "blank": blank}))
    return items


def _block1a_G(sheet):
    """9G: Integers mastery -- mixed hop challenge."""
    return _block1a_B(sheet)


def _block1a_H(sheet):
    """9H: Percentage concept -- grid."""
    items = []
    for i in range(6):
        shaded = random.randint(5, 95)
        blank = i >= 2
        items.append(_mk(f"Shade {shaded}% on the grid.",
                          "percent_grid", {"shaded": shaded, "blank": blank}))
    return items


def _block1a_I(sheet):
    """9I: Percentage of a quantity -- bar model."""
    tiers = {1: (100, 500), 2: (200, 800), 3: (300, 1200), 4: (400, 2000)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        percent = random.choice([10, 20, 25, 40, 50, 60, 75])
        qty = random.randint(lo, hi)
        blank = i >= 2
        items.append(_mk(f"Find {percent}% of {qty}.",
                          "percent_bar", {"percent": percent, "quantity": qty, "blank": blank}))
    return items


def _block1a_J(sheet):
    """9J: Percentage increase & decrease -- price tag both directions."""
    tiers = {1: (100, 400), 2: (200, 600), 3: (300, 900), 4: (400, 1500)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        original = random.randint(lo, hi)
        percent = random.choice([5, 10, 15, 20, 25, 30])
        kind = "markup" if i % 2 == 0 else "discount"
        blank = i >= 2
        verb = "increases" if kind == "markup" else "decreases"
        items.append(_mk(f"Rs {original} {verb} by {percent}%. New price?",
                          "price_tag", {"original": original, "percent": percent, "kind": kind, "blank": blank}))
    return items


def _block1a_K(sheet):
    """9K: Discount & profit/loss -- price tag (discount)."""
    tiers = {1: (200, 600), 2: (300, 900), 3: (400, 1200), 4: (500, 2000)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        original = random.randint(lo, hi)
        percent = random.choice([10, 15, 20, 25, 30, 40])
        blank = i >= 2
        items.append(_mk(f"Marked price Rs {original}, discount {percent}%. Selling price?",
                          "price_tag", {"original": original, "percent": percent, "kind": "discount", "blank": blank}))
    return items


def _block1a_L(sheet):
    """9L: Simple interest & tax -- price tag as markup (tax addition)."""
    tiers = {1: (200, 600), 2: (300, 900), 3: (400, 1200), 4: (500, 2000)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        original = random.randint(lo, hi)
        percent = random.choice([5, 8, 10, 12, 15, 18])
        blank = i >= 2
        items.append(_mk(f"Bill Rs {original} + {percent}% tax. Total?",
                          "price_tag", {"original": original, "percent": percent, "kind": "markup", "blank": blank}))
    return items


def _block1a_M(sheet):
    """9M: Multi-step percentage word problems -- bar model."""
    return _block1a_I(sheet)


def _block1a_N(sheet):
    """9N: mastery/revision -- grid."""
    return _block1a_H(sheet)


_BLOCK1A_BUILDERS = {
    "9A": _block1a_A, "9B": _block1a_B, "9C": _block1a_C, "9D": _block1a_D,
    "9E": _block1a_E, "9F": _block1a_F, "9G": _block1a_G, "9H": _block1a_H,
    "9I": _block1a_I, "9J": _block1a_J, "9K": _block1a_K, "9L": _block1a_L,
    "9M": _block1a_M, "9N": _block1a_N,
}


# ───────────────────────── Quick Review (toughened beyond Level 8) ─────────────────────────

def _l9v3_quick_review(sheet):
    """3 questions, toughened BEYOND Level 8's tier: 3-digit x 2-digit
    multiplication (Level 4), 4-digit / 2-digit division (Level 5), and
    a decimal operation harder than Level 8's own teaching range
    (Level 8 -- the most directly relevant skill, since percentages ARE
    decimals: 15% = 0.15)."""
    tiers = {
        1: {"mlo": 100, "mhi": 300, "mmul": 25, "dlo": 15, "dhi": 30, "dbig": 3000, "declo": 5, "dechi": 90},
        2: {"mlo": 150, "mhi": 400, "mmul": 40, "dlo": 20, "dhi": 45, "dbig": 5000, "declo": 10, "dechi": 150},
        3: {"mlo": 200, "mhi": 600, "mmul": 60, "dlo": 25, "dhi": 60, "dbig": 7000, "declo": 20, "dechi": 250},
        4: {"mlo": 300, "mhi": 900, "mmul": 90, "dlo": 30, "dhi": 80, "dbig": 9000, "declo": 30, "dechi": 400},
    }
    t = tiers[sheet]
    items = []

    a = random.randint(t["mlo"], t["mhi"])
    b = random.randint(11, t["mmul"])
    items.append(q(f"Quick Review (Level 4): {a} x {b} = ____", "fill", "Answer = ____"))

    d = random.randint(t["dlo"], t["dhi"])
    k_lo = t["dlo"]
    k_hi = min(t["dhi"], t["dbig"] // d)
    if k_hi < k_lo:
        k_hi = k_lo
    k = random.randint(k_lo, k_hi)
    n = d * k
    items.append(q(f"Quick Review (Level 5): {n} / {d} = ____", "fill", "Answer = ____"))

    op = random.choice(["+", "-", "x"])
    if op in ("+", "-"):
        x1 = round(random.uniform(t["declo"], t["dechi"]), 2)
        x2 = round(random.uniform(t["declo"], t["dechi"]), 2)
        if op == "-" and x1 < x2:
            x1, x2 = x2, x1
        items.append(q(f"Quick Review (Level 8): {x1} {op} {x2} = ____", "fill", "Answer = ____"))
    else:
        x1 = round(random.uniform(t["declo"], t["dechi"] / 4), 1)
        x2 = random.randint(2, 12)
        items.append(q(f"Quick Review (Level 8): {x1} x {x2} = ____", "fill", "Answer = ____"))

    return items


# ───────────────────────── Speed Calculation (toughened beyond Level 8) ─────────────────────────

def _l9v3_speed_calc(sheet):
    """5 rapid whole-number arithmetic questions, toughened beyond Level
    8's version of this block."""
    tiers = {
        1: {"mul_lo": 30, "mul_hi": 90, "div_hi": 22, "sub_lo": 500, "sub_hi": 900},
        2: {"mul_lo": 40, "mul_hi": 120, "div_hi": 28, "sub_lo": 600, "sub_hi": 999},
        3: {"mul_lo": 50, "mul_hi": 150, "div_hi": 35, "sub_lo": 700, "sub_hi": 1500},
        4: {"mul_lo": 60, "mul_hi": 200, "div_hi": 45, "sub_lo": 800, "sub_hi": 2000},
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
            b = random.randint(11, t["div_hi"] + 15)
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
    "9A": _L9._A_s, "9B": _L9._B_s, "9C": _L9._C_s, "9D": _L9._D_s,
    "9E": _L9._E_s, "9F": _L9._F_s, "9G": _L9._G_s, "9H": _L9._H_s,
    "9I": _L9._I_s, "9J": _L9._J_s, "9K": _L9._K_s, "9L": _L9._L_s,
    "9M": _L9._M_s, "9N": _L9._N_s,
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
        n = random.randint(-50, 50) + idx
        block1b.append(q(f"True or False: {n} is greater than {n-5}.", "fill", "____ (True/False)"))
        idx += 1
    return concept_items, block1b


def build_v3_sheet(code, sheet):
    random.seed(9000 + hash(code) % 5000 + sheet * 31)
    block1a = _BLOCK1A_BUILDERS[code](sheet)
    used = {_item_key(x) for x in block1a}
    concept_items, block1b = _build_block1b(code, sheet, used)
    out = list(concept_items)
    out += block1a
    out += block1b
    out += _l9v3_quick_review(sheet)
    out += _l9v3_speed_calc(sheet)
    return out


LEVEL9_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _BLOCK1A_BUILDERS
}
