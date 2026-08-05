"""
Fear Less Maths — LEVEL 13 (Number Systems) v3 worksheet architecture
(2026-08-04)

Unlike Levels 10-12 (100% pre-existing diagram coverage, just needed
reorganizing), Level 13 had very uneven coverage -- 7 of its 14
sublevels had ZERO diagrams. All 11 existing diagram types were
audited for answer leaks (none found, already correctly built) and
one new one added: `real_number_line` (13E has no existing diagram at
all for "where does an irrational sit among the integers?").

  Q1-6   Freshly-authored diagram questions per sublevel, hand-matched
         to each topic's existing diagram type where one exists
         (number_hierarchy for 13A/13B/13D classification,
         decimal_expansion for 13C, recurring_to_fraction for 13CUM1,
         real_number_line for 13E [new], surd_simplify_tree for 13F,
         rationalize_steps for 13G/13H, index_law_visual/power_ladder/
         power_expansion for 13I), Q1-2 worked, Q3-6 blank.
  Q7-12  6 more of the sheet's own existing questions, self-contained
         text, no diagram.
  Q13-15 "Quick Review" -- toughened beyond Level 12's tier: 3-digit x
         4-digit multiplication (Level 4), 4-digit / 3-digit division
         (Level 5), simplifying an algebraic expression harder than
         Level 12's own range (Level 12 -- solving equations and
         classifying numbers both depend on manipulating expressions
         correctly first).
  Q16-20 "Speed Calculation" -- BODMAS, difficulty increased FURTHER
         beyond Level 12's tier per direct request: bigger numbers,
         nested brackets, and exponents appear from sheet 1 onward
         (Level 12 only introduced exponents at sheet 3-4).
"""
import random
import math
from content import q as _q
import content_l13_numsys as _L13


def _item_key(item):
    return (item.get("text", ""), repr(item.get("diagram_params")))


def _mk(text, dtype, params):
    return _q(text, "diagram", "____", "", dtype, params)


# ───────────────────────── Block 1a: fresh diagram questions per sublevel ─────────────────────────

def _block1a_A(sheet):
    """13A: Natural, Whole & Integers -- classify via number_hierarchy."""
    tiers = {1: (1, 20), 2: (1, 50), 3: (-20, 50), 4: (-50, 100)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        n = random.randint(lo, hi)
        if n < 0:
            memb = "integer"
        elif n == 0:
            memb = "whole"
        else:
            memb = "natural"
        blank = i >= 2
        items.append(_mk(f"Where does {n} belong: Natural, Whole, or Integers?",
                          "number_hierarchy", {"number": str(n), "memberships": [memb], "blank": blank}))
    return items


def _block1a_B(sheet):
    """13B: Rational numbers -- classify via number_hierarchy."""
    tiers = {1: (2, 8), 2: (2, 12), 3: (2, 16), 4: (2, 20)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        d = random.randint(lo, hi)
        n = random.randint(1, d - 1) if d > 1 else 1
        blank = i >= 2
        items.append(_mk(f"Is {n}/{d} a rational number? Where does it fit?",
                          "number_hierarchy", {"number": f"{n}/{d}", "memberships": ["rational"], "blank": blank}))
    return items


def _block1a_C(sheet):
    """13C: Decimal expansions -- terminating vs recurring."""
    tiers = {1: [4, 5, 8, 10], 2: [8, 16, 20, 25], 3: [12, 24, 32, 40], 4: [16, 40, 48, 64]}
    dens = tiers[sheet]
    items = []
    for i in range(6):
        den = random.choice(dens)
        num = random.randint(1, den - 1)
        g = math.gcd(num, den)
        num, den = num // g, den // g
        blank = i >= 2
        items.append(_mk(f"Predict: is {num}/{den} terminating or recurring?",
                          "decimal_expansion", {"num": num, "den": den, "blank": blank}))
    return items


def _block1a_CUM1(sheet):
    """13CUM1: Recurring decimal to fraction."""
    tiers = {1: (1, 1), 2: (1, 2), 3: (2, 2), 4: (2, 3)}
    dlo, dhi = tiers[sheet]
    items = []
    for i in range(6):
        period_len = random.randint(dlo, dhi)
        digits = "".join(str(random.randint(1, 9)) for _ in range(max(period_len, 1)))
        blank = i >= 2
        items.append(_mk(f"Convert 0.{digits}{digits[-period_len:]}... to a fraction.",
                          "recurring_to_fraction", {"digits": digits, "period_len": period_len, "blank": blank}))
    return items


def _block1a_D(sheet):
    """13D: Irrational numbers -- number_hierarchy classification."""
    tiers = {1: (2, 15), 2: (2, 30), 3: (2, 50), 4: (2, 80)}
    lo, hi = tiers[sheet]
    perfect_squares = {1, 4, 9, 16, 25, 36, 49, 64, 81, 100}
    items = []
    for i in range(6):
        n = random.randint(lo, hi)
        while n in perfect_squares:
            n = random.randint(lo, hi)
        blank = i >= 2
        items.append(_mk(f"Is \u221a{n} rational or irrational? Where does it belong?",
                          "number_hierarchy", {"number": f"\u221a{n}", "memberships": ["irrational"], "blank": blank}))
    return items


def _block1a_E(sheet):
    """13E: Real number line -- real_number_line diagram (new)."""
    tiers = {1: (2, 20), 2: (2, 40), 3: (2, 70), 4: (2, 99)}
    lo, hi = tiers[sheet]
    perfect_squares = {1, 4, 9, 16, 25, 36, 49, 64, 81}
    items = []
    for i in range(6):
        n = random.randint(lo, hi)
        while n in perfect_squares:
            n = random.randint(lo, hi)
        approx = math.sqrt(n)
        blank = i >= 2
        lo_b, hi_b = int(approx), int(approx) + 1
        items.append(_mk(f"Between which two consecutive integers does \u221a{n} lie?",
                          "real_number_line", {"value_str": f"\u221a{n}", "approx": round(approx, 3),
                                                "lo": max(0, lo_b - 1), "hi": hi_b + 1, "blank": blank}))
    return items


def _block1a_CUM2(sheet):
    """13CUM2: Review B-E -- mixed diagram types."""
    builders = [_block1a_B, _block1a_D, _block1a_C, _block1a_E]
    items = []
    for i in range(6):
        fn = builders[i % len(builders)]
        one = fn(sheet)[0]
        y = dict(one)
        items.append(y)
    return items


def _block1a_F(sheet):
    """13F: Surds simplifying."""
    tiers = {1: [8, 12, 18, 20, 27], 2: [24, 32, 45, 48, 50], 3: [50, 72, 75, 98, 108], 4: [80, 96, 128, 147, 162]}
    pool = tiers[sheet]
    items = []
    for i in range(6):
        n = random.choice(pool)
        blank = i >= 2
        items.append(_mk(f"Simplify \u221a{n}.", "surd_simplify_tree", {"n": n, "blank": blank}))
    return items


def _block1a_G(sheet):
    """13G: Rationalising single term."""
    tiers = {1: (2, 10), 2: (2, 15), 3: (5, 20), 4: (5, 30)}
    lo, hi = tiers[sheet]
    perfect_squares = {1, 4, 9, 16, 25}
    items = []
    for i in range(6):
        b = random.randint(lo, hi)
        while b in perfect_squares:
            b = random.randint(lo, hi)
        blank = i >= 2
        items.append(_mk(f"Rationalise: 1/\u221a{b}", "rationalize_steps", {"kind": "single", "b": b, "blank": blank}))
    return items


def _block1a_H(sheet):
    """13H: Rationalising binomial/conjugate."""
    tiers = {1: (1, 5), 2: (2, 7), 3: (3, 9), 4: (4, 12)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        a = random.randint(lo, hi)
        c = random.randint(2, 10)
        while c in (1, 4, 9):
            c = random.randint(2, 10)
        blank = i >= 2
        items.append(_mk(f"Rationalise: 1/({a} + \u221a{c})", "rationalize_steps",
                          {"kind": "binomial", "a": a, "c": c, "blank": blank}))
    return items


def _block1a_CUM3(sheet):
    """13CUM3: Mixed review F/G/H."""
    builders = [_block1a_F, _block1a_G, _block1a_H]
    items = []
    for i in range(6):
        fn = builders[i % len(builders)]
        one = fn(sheet)[0]
        items.append(dict(one))
    return items


def _block1a_I(sheet):
    """13I: Laws of exponents -- index_law_visual + power_ladder."""
    tiers = {1: (2, 2, 5), 2: (2, 2, 7), 3: (3, 2, 8), 4: (3, 3, 9)}
    base_base, mlo, mhi = tiers[sheet]
    items = []
    for i in range(6):
        base = random.choice([2, 3, base_base])
        m = random.randint(mlo, mhi)
        n = random.randint(mlo, mhi)
        mode = "multiply" if i % 2 == 0 else "divide"
        if mode == "divide" and n > m:
            m, n = n, m
        blank = i >= 2
        items.append(_mk(f"{'Combine' if mode=='multiply' else 'Simplify'}: {base}^{m} {'x' if mode=='multiply' else '/'} {base}^{n}",
                          "index_law_visual", {"base": base, "m": m, "n": n, "mode": mode, "blank": blank}))
    return items


def _block1a_J(sheet):
    """13J: Word problems -- surd/irrational context via sqrt_side_area."""
    tiers = {1: [16, 25, 36, 49], 2: [36, 49, 64, 81], 3: [64, 81, 100, 121], 4: [100, 121, 144, 169]}
    pool = tiers[sheet]
    items = []
    for i in range(6):
        area = random.choice(pool)
        blank = i >= 2
        items.append(_mk(f"A square field has area {area} sq.m. Find the side length.",
                          "sqrt_side_area", {"area": area, "blank": blank}))
    return items


def _block1a_REV(sheet):
    """13REV: mixed review of everything."""
    builders = [_block1a_A, _block1a_C, _block1a_D, _block1a_E, _block1a_F, _block1a_I]
    items = []
    for i in range(6):
        fn = builders[i % len(builders)]
        one = fn(sheet)[0]
        items.append(dict(one))
    return items


_BLOCK1A_BUILDERS = {
    "13A": _block1a_A, "13B": _block1a_B, "13C": _block1a_C, "13CUM1": _block1a_CUM1,
    "13D": _block1a_D, "13E": _block1a_E, "13CUM2": _block1a_CUM2,
    "13F": _block1a_F, "13G": _block1a_G, "13H": _block1a_H, "13CUM3": _block1a_CUM3,
    "13I": _block1a_I, "13J": _block1a_J, "13REV": _block1a_REV,
}

_SOURCE_FN = {
    "13A": _L13._L13A_s, "13B": _L13._L13B_s, "13C": _L13._L13C_s, "13CUM1": _L13._L13CUM1_s,
    "13D": _L13._L13D_s, "13E": _L13._L13E_s, "13CUM2": _L13._L13CUM2_s,
    "13F": _L13._L13F_s, "13G": _L13._L13G_s, "13H": _L13._L13H_s, "13CUM3": _L13._L13CUM3_s,
    "13I": _L13._L13I_s, "13J": _L13._L13J_s, "13REV": _L13._L13REV_s,
}


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
        n = random.randint(2, 50) + idx
        block1b.append(_q(f"True or False: {n} is a rational number.", "fill", "____ (True/False)"))
        idx += 1
    return concept_items, block1b


# ───────────────────────── Quick Review (toughened beyond Level 12) ─────────────────────────

def _l13v3_quick_review(sheet):
    """3 questions, toughened beyond Level 12's tier: 3-digit x 4-digit
    multiplication (Level 4), 4-digit / 3-digit division (Level 5),
    simplifying an expression harder than Level 12's own range (Level
    12 -- classifying/manipulating numbers here builds directly on
    simplifying expressions correctly)."""
    tiers = {
        1: {"mlo": 300, "mhi": 700, "mbig": 2000, "dlo": 200, "dhi": 500, "dbig": 9500, "elo": 6, "ehi": 20},
        2: {"mlo": 350, "mhi": 800, "mbig": 3000, "dlo": 220, "dhi": 550, "dbig": 9700, "elo": 8, "ehi": 25},
        3: {"mlo": 400, "mhi": 900, "mbig": 4000, "dlo": 250, "dhi": 600, "dbig": 9800, "elo": 10, "ehi": 30},
        4: {"mlo": 450, "mhi": 999, "mbig": 5000, "dlo": 280, "dhi": 650, "dbig": 9900, "elo": 12, "ehi": 35},
    }
    t = tiers[sheet]
    items = []

    a = random.randint(t["mlo"], t["mhi"])
    b = random.randint(1000, t["mbig"])
    items.append(_q(f"Quick Review (Level 4): {a} x {b} = ____", "fill", "Answer = ____"))

    d = random.randint(t["dlo"], t["dhi"])
    k_lo = t["dlo"] // 10
    k_hi = min(t["dhi"] // 10, t["dbig"] // d)
    if k_hi < k_lo:
        k_hi = k_lo
    k = max(random.randint(k_lo, k_hi), 2)
    n = d * k
    items.append(_q(f"Quick Review (Level 5): {n} / {d} = ____", "fill", "Answer = ____"))

    c1 = random.randint(t["elo"], t["ehi"])
    c2 = random.randint(t["elo"], t["ehi"])
    c3 = random.randint(t["elo"], t["ehi"])
    c4 = random.randint(t["elo"], t["ehi"])
    items.append(_q(f"Quick Review (Level 12): Simplify {c1}x + {c2}y - {c3}x - {c4}y + {c1}x", "fill", "Answer = ____"))

    return items


# ───────────────────────── Speed Calculation: BODMAS, harder than Level 12 ─────────────────────────

def _l13v3_bodmas_calc(sheet):
    """5 BODMAS questions, difficulty increased FURTHER beyond Level
    12's tier per direct request: bigger numbers, and nested brackets/
    exponents appear from sheet 1 onward (Level 12 only introduced
    exponents at sheet 3-4). Same guaranteed-clean construction
    (non-negative integer results) as Level 12."""
    tiers = {
        1: {"lo": 5, "hi": 20},
        2: {"lo": 6, "hi": 25},
        3: {"lo": 8, "hi": 30},
        4: {"lo": 10, "hi": 35},
    }
    t = tiers[sheet]
    lo, hi = t["lo"], t["hi"]

    def r():
        return random.randint(lo, hi)

    def ordered_pair():
        a, b = r(), r()
        return (a, b) if a >= b else (b, a)

    def clean_div(min_q=2, max_q=None):
        max_q = max_q or hi
        divisor = random.randint(2, max(2, hi // 2))
        quotient = random.randint(min_q, max_q)
        return divisor * quotient, divisor

    templates_by_tier = {
        1: [
            lambda: (lambda p, q: f"({r()} + {r()}) x {r()} - {p} x {q}")(*ordered_pair()),
            lambda: (lambda a, b: f"{a} x {r()} - ({b} + {r()}) x {r()%4+2}")(*ordered_pair()),
            lambda: f"({max(r(),lo+1)} - {lo}) x {r()} + {r()} x {r()%5+2}",
            lambda: (lambda p, q: f"{r()}^2 - {p} x {q}")(*ordered_pair()),
            lambda: (lambda n, d: f"({r()} + {n} / {d}) - {min(r(),hi-1)}")(*clean_div()),
        ],
        2: [
            lambda: f"({r()} + {r()}) x ({max(r(),lo+2)} - {lo})",
            lambda: (lambda p, q: f"{r()}^2 + {p} x {q} - {min(r(),hi-1)}")(*ordered_pair()),
            lambda: (lambda n, d: f"({n} - {min(d,n-1)}) / {d}")(*clean_div(min_q=3)),
            lambda: (lambda a, b: f"{r()} x ({r()} + {r()}) - {a} x {b}")(*ordered_pair()),
            lambda: (lambda n, d: f"({r()} + {r()})^2 / {d} - {min(n//d, hi-1)}")(*clean_div(min_q=2, max_q=6)),
        ],
        3: [
            lambda: (lambda p, q: f"({r()} + {r()}) x ({r()} - {r()%6+2}) - {p} x {q}")(*ordered_pair()),
            lambda: (lambda a, b: f"{r()}^2 - ({a} + {b}) x {r()%5+2} + {r()}")(*ordered_pair()),
            lambda: (lambda n, d: f"(({r()} + {r()}) x {r()%4+2} - {n}) / {d}")(*clean_div(min_q=2, max_q=5)),
            lambda: f"({r()}^2 - {r()%8+2}^2) / {r()%6+2}",
            lambda: (lambda p, q: f"({r()} + {r()})^2 / {r()%4+2} - {p} x {q}")(*ordered_pair()),
        ],
        4: [
            lambda: (lambda p, q: f"(({r()} + {r()}) x {r()%5+2} - {p} x {q}) / {r()%4+2}")(*ordered_pair()),
            lambda: (lambda a, b: f"{r()}^2 - ({r()} + {r()})^2 / {r()%5+2} + {a} - {b}")(*(sorted((r()%10, r()%8), reverse=True))),
            lambda: f"({r()}^2 - {r()%9+2}^2) / ({max(r()%12+3,5)} - {r()%5+2})",
            lambda: (lambda n, d: f"({r()} x {r()%4+3} - {n}) / {d} + {r()%10+2}")(*clean_div(min_q=2, max_q=6)),
            lambda: (lambda p, q: f"(({r()} + {r()}) x ({r()%6+2} + {r()%4+1})) - {p} x {q}")(*ordered_pair()),
        ],
    }
    templates = templates_by_tier[sheet]
    chosen = random.sample(templates, 5)
    items = []
    for tmpl in chosen:
        expr = None
        for _ in range(80):
            try:
                candidate = tmpl()
                py_expr = candidate.replace("x", "*").replace("^", "**")
                val = eval(py_expr)
            except Exception:
                continue
            if isinstance(val, float) and not float(val).is_integer():
                continue
            if val < 0:
                continue
            expr = candidate
            break
        if expr is None:
            expr = f"{r()} + {r()} x {r()}"
        items.append(_q(f"Speed Calculation (BODMAS): {expr} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── Assembly ─────────────────────────

def build_v3_sheet(code, sheet):
    random.seed(13000 + hash(code) % 5000 + sheet * 31)
    block1a = _BLOCK1A_BUILDERS[code](sheet)
    used = {_item_key(x) for x in block1a}
    concept_items, block1b = _build_block1b(code, sheet, used)
    out = list(concept_items)
    out += block1a
    out += block1b
    out += _l13v3_quick_review(sheet)
    out += _l13v3_bodmas_calc(sheet)
    return out


LEVEL13_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _BLOCK1A_BUILDERS
}
