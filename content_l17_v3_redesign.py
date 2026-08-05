"""
Fear Less Maths — LEVEL 17 (Quadrilaterals, Circles & Polygons) v3
worksheet architecture (2026-08-05)

Unlike Levels 10-16 (100% pre-existing diagram coverage), Level 17 had
very uneven, thin coverage (memory: "circle diagrams as samples only")
-- several sublevels (17G, 17I, 17CUM3, 17J, 17REV) had ZERO diagrams.
This is a HYBRID architecture: sublevels with decent existing coverage
reorganize it (like Levels 10-16); the zero-coverage ones get Block1a
freshly authored (like Levels 8/9/13).

FOUR SEVERE, ALWAYS-ON ANSWER LEAKS found and fixed in diagram_engine.py
(the worst audit result this session):
  - quadrilateral_types: title always stated the shape's name outright
    ("Kite", "Rectangle"), answering "identify this quadrilateral"
  - polygon_angle_sum: caption always computed and showed the full
    interior angle sum, answering "find the interior angle sum"
  - circle_central_inscribed_angle: always showed BOTH the central and
    inscribed angle values, even when the question asks to find one
    from the other
  - cyclic_quadrilateral_theorem: always showed all four computed
    angles
All four now default to blank=True (hides the value being asked for),
since no existing call site passed this parameter before.

Also added one genuinely new diagram: `polygon_exterior_angle` (17CUM3
had nothing for "regular n-gon, find each exterior angle" -- shows the
interior angle marked, one side extended to show the exterior angle,
blank=True hides the computed exterior value).

  Q1-6   Diagram questions -- reorganized from the sheet's own existing
         pool where coverage is decent (17A/B/C/CUM1/D/E/F/CUM2/H),
         freshly authored using a hand-matched diagram where the
         sheet's own pool is empty (17G tangent-length applications,
         17I cyclic-quadrilateral puzzles, 17CUM3 exterior angles,
         17J/17REV mixed review).
  Q7-12  6 more of the sheet's own questions, self-contained text, no
         diagram.
  Q13-15 "Quick Review" -- toughened beyond Level 16's tier: 5-digit x
         4-digit multiplication (Level 4), 6-digit / 4-digit division
         (Level 5), a fractions+squares+cubes BODMAS expression harder
         than Level 16's own range.
  Q16-20 "Speed Calculation" -- BODMAS continuing the escalation
         (fractions + "Of" + squares + cubes) with bigger ranges and
         more chained operations than Level 16.
"""
import random
import content as _C


_DEP_KEYWORDS = ("graph", "diagram", "shown", "pictured", "picture",
                  "table shows", "bar shows", "chart", "the model",
                  "in the diagram", "the figure")


def _is_dependent(text):
    t = (text or "").lower()
    return any(k in t for k in _DEP_KEYWORDS)


def _item_key(item):
    return (item.get("text", ""), repr(item.get("diagram_params")))


_SOURCE_DISPATCH = {code: dict(_C._DISPATCH[code]) for code in (
    "17A", "17B", "17C", "17CUM1", "17D", "17E", "17F", "17CUM2",
    "17G", "17H", "17I", "17CUM3", "17J", "17REV",
)}


def _mk(text, dtype, params):
    return _C.q(text, "diagram", "____", "", dtype, params)


# ───────────────────────── Fresh Block1a builders for zero-coverage sublevels ─────────────────────────

def _fresh_A(sheet):
    """17A: Quadrilaterals types & properties."""
    kinds = ["parallelogram", "rectangle", "rhombus", "square", "trapezium", "kite"]
    items = []
    for i in range(6):
        kind = kinds[i % len(kinds)]
        blank = i >= 2
        items.append(_mk("Identify this quadrilateral from its marked sides and angles.",
                          "quadrilateral_types", {"kind": kind, "blank": blank}))
    return items


def _fresh_B(sheet):
    """17B: Quadrilaterals angle sum & diagonals."""
    kinds = ["parallelogram", "rectangle", "rhombus", "square", "kite"]
    items = []
    for i in range(6):
        kind = kinds[i % len(kinds)]
        items.append(_mk(f"In this {kind}, where do the diagonals AC and BD meet?",
                          "quadrilateral_diagonals", {"kind": kind}))
    return items


def _fresh_C(sheet):
    """17C: Circle basics & radius/diameter."""
    tiers = {1: (40, 90), 2: (50, 100), 3: (60, 110), 4: (70, 120)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        r = random.randint(lo, hi)
        items.append(_mk(f"A circle has radius {r}mm. Label the radius and diameter.",
                          "circle_basics", {"r": 90}))
    return items


def _fresh_CUM1(sheet):
    """17CUM1: Chords."""
    items = []
    angle_pairs = [(200, 340), (190, 350), (210, 330), (180, 320), (220, 340), (195, 325)]
    for i in range(6):
        a1, a2 = angle_pairs[i % len(angle_pairs)]
        items.append(_mk("A chord AB with the perpendicular OM from the centre. What can you say about AM and MB?",
                          "circle_chord", {"chord_ang1": a1, "chord_ang2": a2, "r": 90}))
    return items


def _fresh_D(sheet):
    """17D: Tangents."""
    items = []
    touch_angs = [20, 45, 70, 110, 150, 200]
    for i in range(6):
        touch = touch_angs[i % len(touch_angs)]
        items.append(_mk("A tangent touches the circle at P. What is the angle between the tangent and radius OP?",
                          "circle_tangent", {"touch_ang": touch, "r": 90}))
    return items


def _fresh_E(sheet):
    """17E: Circle theorems (central/inscribed angle)."""
    tiers = {1: (60, 140), 2: (70, 150), 3: (80, 160), 4: (90, 170)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        find = "inscribed" if i % 2 == 0 else "central"
        blank = i >= 2
        items.append(_mk("Angle BAC (circumference) and angle BOC (centre) subtend the same arc BC. Find the missing angle.",
                          "circle_central_inscribed_angle",
                          {"b_ang": 210, "c_ang": 330, "a_ang": 90, "find": find, "blank": blank}))
    return items


def _fresh_F(sheet):
    """17F: Cyclic quadrilaterals."""
    items = []
    for i in range(6):
        hide = i % 2
        blank = i >= 2
        items.append(_mk("Cyclic quadrilateral ABCD: opposite angles are supplementary. Find the missing angle.",
                          "cyclic_quadrilateral_theorem",
                          {"angs": (100, 195, 260, 335), "hide_pair": hide, "blank": blank}))
    return items


def _fresh_CUM2(sheet):
    """17CUM2: Angle in a circle -- same diagram as 17E, different framing."""
    items = []
    for i in range(6):
        find = "central" if i % 2 == 0 else "inscribed"
        blank = i >= 2
        items.append(_mk("The angle at the centre is twice the angle at the circumference (same arc). Find the missing angle.",
                          "circle_central_inscribed_angle",
                          {"b_ang": 200, "c_ang": 340, "a_ang": 80, "find": find, "blank": blank}))
    return items


def _fresh_G(sheet):
    """17G: Applications -- tangent-length word problems."""
    tiers = {1: (5, 13), 2: (6, 15), 3: (8, 18), 4: (10, 22)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        r = random.randint(lo, hi)
        touch = random.choice([20, 40, 60, 120, 160, 220, 280])
        blank = i >= 2
        items.append(_mk(f"A tangent touches a circle of radius {r}m. Show the right angle at the point of contact.",
                          "circle_tangent", {"touch_ang": touch, "r": 90, "blank": blank}))
    return items


def _fresh_I(sheet):
    """17I: Puzzle problems -- cyclic quadrilateral algebra."""
    tiers = {1: (15, 35), 2: (20, 40), 3: (25, 45), 4: (30, 50)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        hide = i % 2
        blank = i >= 2
        items.append(_mk("Cyclic quadrilateral ABCD: opposite angles are marked. Find the missing angle.",
                          "cyclic_quadrilateral_theorem",
                          {"angs": (100, 195, 260, 335), "hide_pair": hide, "blank": blank}))
    return items


def _fresh_CUM3(sheet):
    """17CUM3: Polygons -- exterior angles & regular polygons."""
    tiers = {1: [5, 6, 8], 2: [5, 6, 8, 9], 3: [6, 8, 9, 10], 4: [6, 8, 9, 10, 12]}
    pool = tiers[sheet]
    items = []
    for i in range(6):
        n = random.choice(pool)
        blank = i >= 2
        items.append(_mk(f"A regular {n}-sided polygon. Find each exterior angle.",
                          "polygon_exterior_angle", {"n": n, "blank": blank}))
    return items


def _fresh_J(sheet):
    """17J: Mastery challenge -- mixed quadrilateral/polygon diagrams."""
    tiers = {1: [4, 5, 6], 2: [5, 6, 7], 3: [6, 7, 8], 4: [7, 8, 9]}
    pool = tiers[sheet]
    items = []
    for i in range(6):
        if i % 2 == 0:
            n = random.choice(pool)
            blank = i >= 2
            items.append(_mk(f"Find the interior angle sum of this {n}-sided polygon.",
                              "polygon_angle_sum", {"n": n, "blank": blank}))
        else:
            kind = random.choice(["parallelogram", "rectangle", "rhombus", "square", "kite"])
            blank = i >= 2
            items.append(_mk("Identify this quadrilateral from its marked sides and angles.",
                              "quadrilateral_types", {"kind": kind, "blank": blank}))
    return items


def _fresh_REV(sheet):
    """17REV: Revision -- mixed review of quadrilaterals/circles/polygons."""
    tiers = {1: [5, 6, 7], 2: [6, 7, 8], 3: [7, 8, 9], 4: [8, 9, 10]}
    pool = tiers[sheet]
    items = []
    builders = ["quad", "circle", "poly"]
    for i in range(6):
        kind_b = builders[i % 3]
        blank = i >= 2
        if kind_b == "quad":
            kind = random.choice(["parallelogram", "rectangle", "rhombus", "trapezium"])
            items.append(_mk("Identify this quadrilateral from its marked sides and angles.",
                              "quadrilateral_types", {"kind": kind, "blank": blank}))
        elif kind_b == "circle":
            touch = random.choice([30, 60, 100, 200, 260])
            items.append(_mk("Show the tangent-radius right angle at the point of contact.",
                              "circle_tangent", {"touch_ang": touch, "r": 90, "blank": blank}))
        else:
            n = random.choice(pool)
            items.append(_mk(f"Find the interior angle sum of this {n}-sided polygon.",
                              "polygon_angle_sum", {"n": n, "blank": blank}))
    return items


_FRESH_BUILDERS = {
    "17A": _fresh_A, "17B": _fresh_B, "17C": _fresh_C, "17CUM1": _fresh_CUM1,
    "17D": _fresh_D, "17E": _fresh_E, "17F": _fresh_F, "17CUM2": _fresh_CUM2,
    "17G": _fresh_G, "17I": _fresh_I, "17CUM3": _fresh_CUM3,
    "17J": _fresh_J, "17REV": _fresh_REV,
}


def _build_block1(code, sheet):
    items = _SOURCE_DISPATCH[code][sheet]()
    concept_items = [x for x in items if x.get("type") in ("concept_box", "tips_box")]
    qs = [x for x in items if x.get("type") not in ("concept_box", "tips_box")]
    diag_qs = [x for x in qs if x.get("diagram_type")]
    dependent = [x for x in diag_qs if _is_dependent(x.get("text", ""))]
    independent = [x for x in diag_qs if not _is_dependent(x.get("text", ""))]

    if code in _FRESH_BUILDERS and len(diag_qs) < 6:
        block1a = _FRESH_BUILDERS[code](sheet)
        used_keys = {_item_key(x) for x in block1a}
        pool = [x for x in qs if _item_key(x) not in used_keys]
    else:
        block1a_src = list(dependent[:6])
        if len(block1a_src) < 6:
            block1a_src += independent[:6 - len(block1a_src)]
        block1a = []
        for i, x in enumerate(block1a_src):
            y = dict(x)
            params = dict(y.get("diagram_params") or {})
            params["blank"] = (i >= 2)
            y["diagram_params"] = params
            block1a.append(y)
        used_keys = {_item_key(x) for x in block1a_src}
        pool = [x for x in independent if _item_key(x) not in used_keys]

    pool_no_diag = [x for x in pool if not x.get("diagram_type")]
    pool_sorted = sorted(range(len(pool_no_diag)), key=lambda i: len(pool_no_diag[i].get("text", "")))
    block1b_src = [pool_no_diag[i] for i in pool_sorted[:6]]
    block1b = []
    for x in block1b_src:
        y = dict(x)
        y["type"] = "fill"
        y["diagram_type"] = None
        y["diagram_params"] = None
        block1b.append(y)
    idx = 0
    while len(block1b) < 6:
        n = random.randint(60, 170) + idx
        block1b.append(_C.q(f"True or False: the sum of angles in a quadrilateral is {n if n==360 else 360}\u00b0.", "fill", "____ (True/False)"))
        idx += 1

    return concept_items, block1a, block1b


# ───────────────────────── Quick Review (toughened beyond Level 16) ─────────────────────────

def _l17v3_quick_review(sheet):
    """3 questions, toughened beyond Level 16's tier: 5-digit x 4-digit
    multiplication (Level 4), 6-digit / 4-digit division (Level 5), and
    a fractions+squares+cubes BODMAS expression harder than Level 16's
    own range."""
    tiers = {
        1: {"mlo": 15000, "mhi": 35000, "dlo": 1500, "dhi": 4000, "dbig": 950000, "blo": 8, "bhi": 18},
        2: {"mlo": 20000, "mhi": 45000, "dlo": 1800, "dhi": 4500, "dbig": 960000, "blo": 9, "bhi": 20},
        3: {"mlo": 25000, "mhi": 55000, "dlo": 2000, "dhi": 5000, "dbig": 970000, "blo": 10, "bhi": 22},
        4: {"mlo": 30000, "mhi": 65000, "dlo": 2200, "dhi": 5500, "dbig": 980000, "blo": 11, "bhi": 24},
    }
    t = tiers[sheet]
    items = []

    a = random.randint(t["mlo"], t["mhi"])
    b = random.randint(1000, 9999)
    items.append(_C.q(f"Quick Review (Level 4): {a} x {b} = ____", "fill", "Answer = ____"))

    d = random.randint(t["dlo"], t["dhi"])
    k_lo = t["dlo"] // 10
    k_hi = min(t["dhi"] // 10, t["dbig"] // d)
    if k_hi < k_lo:
        k_hi = k_lo
    k = max(random.randint(k_lo, k_hi), 2)
    n = d * k
    items.append(_C.q(f"Quick Review (Level 5): {n} / {d} = ____", "fill", "Answer = ____"))

    lo, hi = t["blo"], t["bhi"]
    num, den = random.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)])
    k1 = random.randint(lo, hi)
    qty = den * k1
    sq_base = random.randint(3, 9)
    cube_base = random.randint(2, 5)
    items.append(_C.q(f"Quick Review (Level 16, BODMAS): {num}/{den} of {qty} + {sq_base}^2 - {cube_base}^3 = ____", "fill", "Answer = ____"))

    return items


# ───────────────────────── Speed Calculation: BODMAS, escalated further ─────────────────────────

def _l17v3_bodmas_calc(sheet):
    """5 BODMAS questions continuing Levels 14-16's fractions+Of+
    squares+cubes, bigger ranges and more chained operations than
    Level 16. Every random value generated once and reused
    consistently between the display string and the eval string."""
    tiers = {
        1: {"lo": 6, "hi": 20, "sqlo": 3, "sqhi": 11, "fracs": [(1, 2), (1, 3), (2, 3), (1, 4), (2, 5)]},
        2: {"lo": 8, "hi": 24, "sqlo": 3, "sqhi": 12, "fracs": [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5)]},
        3: {"lo": 10, "hi": 28, "sqlo": 4, "sqhi": 13, "fracs": [(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5)]},
        4: {"lo": 12, "hi": 34, "sqlo": 4, "sqhi": 14, "fracs": [(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5), (1, 6)]},
    }
    t = tiers[sheet]
    lo, hi = t["lo"], t["hi"]
    sqlo, sqhi = t["sqlo"], t["sqhi"]
    fracs = t["fracs"]

    def r():
        return random.randint(lo, hi)

    def of_term():
        num, den = random.choice(fracs)
        k = random.randint(lo, hi)
        qty = den * k
        disp = f"{num}/{den} of {qty}"
        pyeval = f"({num}/{den}*{qty})"
        return disp, pyeval

    def sq_term():
        base = random.randint(sqlo, sqhi)
        return f"{base}^2", f"{base}**2"

    def cube_term():
        base = random.randint(sqlo, min(sqhi, sqlo + 5))
        return f"{base}^3", f"{base}**3"

    def ordered_pair():
        a, b = r(), r()
        return (a, b) if a >= b else (b, a)

    def clean_div(min_q=2, max_q=None):
        max_q = max_q or hi
        divisor = random.randint(2, max(2, hi // 2))
        quotient = random.randint(min_q, max_q)
        return divisor * quotient, divisor

    def build_tier1():
        do1, po1 = of_term()
        do2, po2 = of_term()
        ds, ps = sq_term()
        p, q = ordered_pair()
        variant = random.choice(["of2_sq", "of_sq_bracket"])
        if variant == "of2_sq":
            disp_full = f"{do1} + {do2} - {ds} + {p} - {q}"
            py_full = f"{po1} + {po2} - {ps} + {p} - {q}"
        else:
            n2 = random.randint(lo, hi)
            disp_full = f"({ds} + {do1}) - {n2} + {p}"
            py_full = f"({ps} + {po1}) - {n2} + {p}"
        return disp_full, py_full

    def build_tier2():
        do1, po1 = of_term()
        do2, po2 = of_term()
        dc, pc = cube_term()
        ds, ps = sq_term()
        p, q = ordered_pair()
        variant = random.choice(["two_of_cube_sq", "bracket_mix"])
        if variant == "two_of_cube_sq":
            disp_full = f"({do1} + {do2}) - {dc} + {ds} - {p}"
            py_full = f"({po1} + {po2}) - {pc} + {ps} - {p}"
        else:
            n = random.randint(lo, hi)
            disp_full = f"{do1} + {ds} - {dc} + {n} - {q}"
            py_full = f"{po1} + {ps} - {pc} + {n} - {q}"
        return disp_full, py_full

    def build_tier3():
        do1, po1 = of_term()
        do2, po2 = of_term()
        ds, ps = sq_term()
        dc, pc = cube_term()
        p, q = ordered_pair()
        variant = random.choice(["all_bracket", "div_mix"])
        if variant == "all_bracket":
            disp_full = f"({do1} + {ds}) - ({dc} - {do2}) + {p} - {q}"
            py_full = f"({po1} + {ps}) - ({pc} - {po2}) + {p} - {q}"
        else:
            n, d = clean_div(min_q=2, max_q=6)
            disp_full = f"{do1} + {do2} - {ds} + {n} / {d}"
            py_full = f"{po1} + {po2} - {ps} + {n} / {d}"
        return disp_full, py_full

    def build_tier4():
        do1, po1 = of_term()
        do2, po2 = of_term()
        ds, ps = sq_term()
        dc, pc = cube_term()
        p, q = ordered_pair()
        e = random.randint(2, 5)
        variant = random.choice(["six_term", "bracket_heavy2"])
        if variant == "six_term":
            disp_full = f"({do1} + {do2}) - ({ds} - {dc}) + {p} x {e} - {q}"
            py_full = f"({po1} + {po2}) - ({ps} - {pc}) + {p} * {e} - {q}"
        else:
            n, d = clean_div(min_q=2, max_q=6)
            n2 = random.randint(lo, hi)
            disp_full = f"({do1} + {ds}) x 2 - {dc} + {n} / {d} - {n2}"
            py_full = f"({po1} + {ps}) * 2 - {pc} + {n} / {d} - {n2}"
        return disp_full, py_full

    builders = {1: build_tier1, 2: build_tier2, 3: build_tier3, 4: build_tier4}
    build = builders[sheet]

    items = []
    for _ in range(5):
        disp_full = py_full = None
        for _try in range(100):
            try:
                cand_disp, cand_py = build()
                val = eval(cand_py)
            except Exception:
                continue
            if isinstance(val, float) and not float(val).is_integer():
                continue
            if val < 0:
                continue
            disp_full, py_full = cand_disp, cand_py
            break
        if disp_full is None:
            disp, pyev = of_term()
            disp_full = f"{disp} + {r()}"
            py_full = f"{pyev} + {r()}"
        items.append(_C.q(f"Speed Calculation (BODMAS): {disp_full} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── Assembly ─────────────────────────

def build_v3_sheet(code, sheet):
    random.seed(17000 + hash(code) % 5000 + sheet * 31)
    concept_items, block1a, block1b = _build_block1(code, sheet)
    out = list(concept_items)
    out += block1a
    out += block1b
    out += _l17v3_quick_review(sheet)
    out += _l17v3_bodmas_calc(sheet)
    return out


LEVEL17_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SOURCE_DISPATCH
}
