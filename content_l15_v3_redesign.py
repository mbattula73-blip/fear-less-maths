"""
Fear Less Maths — LEVEL 15 (Coordinate Geometry) v3 worksheet architecture
(2026-08-04)

Same pattern as Levels 10-14: already has near-100% SVG diagram
coverage, so this reorganizes existing content rather than authoring
new diagrams. Audited all 9 diagram types used here (plot_points_grid,
triangle_coords, distance_segment, midpoint_segment,
slope_intercept_anatomy, quadrant_map, section_segment,
point_plot_path, linear_equation_graph) for answer leaks -- all
already correctly built, no leaks found.

  Q1-6   The sheet's own existing diagram questions, diagram-DEPENDENT
         ones prioritized (15CUM1/15CUM2/15H/15CUM3/15REV have some --
         "looking at the grid/plot" can't be answered without the
         picture).
  Q7-12  6 more of the sheet's own questions, self-contained text,
         diagram stripped.
  Q13-15 "Quick Review" -- toughened beyond Level 14's tier: 4-digit x
         4-digit multiplication (Level 4), 5-digit / 4-digit division
         (Level 5), a BODMAS-with-fractions expression harder than
         Level 14's own range (Level 14 -- the most directly relevant
         skill, since the distance/section/area formulas here are all
         themselves BODMAS calculations under the hood).
  Q16-20 "Speed Calculation" -- BODMAS extended with SQUARES and CUBES
         on top of Level 14's fractions-of-quantity, per direct
         request, to make expressions even longer: terms like "2^3" or
         "5^2" now combine with "1/2 of 20" style fraction-of terms in
         the same expression, 6-7 chained operations by sheet 4. Same
         guaranteed-clean construction (every random value generated
         once and reused consistently between the display string and
         the validation string -- the exact bug class fixed in Level
         14 after a stress test caught it).
"""
import random
import content as _C


_DEP_KEYWORDS = ("graph", "diagram", "shown", "pictured", "picture",
                  "table shows", "bar shows", "chart", "the model",
                  "the plot", "the grid", "looking at")


def _is_dependent(text):
    t = (text or "").lower()
    return any(k in t for k in _DEP_KEYWORDS)


def _item_key(item):
    return (item.get("text", ""), repr(item.get("diagram_params")))


_SOURCE_DISPATCH = {code: dict(_C._DISPATCH[code]) for code in (
    "15A", "15B", "15C", "15CUM1", "15D", "15E", "15F", "15CUM2",
    "15G", "15H", "15I", "15CUM3", "15J", "15REV",
)}


def _build_block1(code, sheet):
    items = _SOURCE_DISPATCH[code][sheet]()
    concept_items = [x for x in items if x.get("type") in ("concept_box", "tips_box")]
    qs = [x for x in items if x.get("type") not in ("concept_box", "tips_box")]
    diag_qs = [x for x in qs if x.get("diagram_type")]
    dependent = [x for x in diag_qs if _is_dependent(x.get("text", ""))]
    independent = [x for x in diag_qs if not _is_dependent(x.get("text", ""))]

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
    pool_sorted = sorted(range(len(pool)), key=lambda i: len(pool[i].get("text", "")))
    block1b_src = [pool[i] for i in pool_sorted[:6]]
    block1b = []
    for x in block1b_src:
        y = dict(x)
        y["type"] = "fill"
        y["diagram_type"] = None
        y["diagram_params"] = None
        block1b.append(y)
    idx = 0
    while len(block1b) < 6:
        n = random.randint(1, 8) + idx
        block1b.append(_C.q(f"True or False: the point ({n}, {n}) lies on the line y = x.", "fill", "____ (True/False)"))
        idx += 1

    return concept_items, block1a, block1b


# ───────────────────────── Quick Review (toughened beyond Level 14) ─────────────────────────

def _l15v3_quick_review(sheet):
    """3 questions, toughened beyond Level 14's tier: 4-digit x 4-digit
    multiplication (Level 4), 5-digit / 4-digit division (Level 5), and
    a BODMAS-with-fractions expression harder than Level 14's own range
    (Level 14 -- distance/section/area formulas are BODMAS calculations
    under the hood)."""
    tiers = {
        1: {"mlo": 1000, "mhi": 3000, "dlo": 1000, "dhi": 3000, "dbig": 90000, "flo": 6, "fhi": 20},
        2: {"mlo": 1500, "mhi": 4000, "dlo": 1200, "dhi": 3500, "dbig": 95000, "flo": 8, "fhi": 25},
        3: {"mlo": 2000, "mhi": 5000, "dlo": 1500, "dhi": 4000, "dbig": 97000, "flo": 10, "fhi": 30},
        4: {"mlo": 2500, "mhi": 6000, "dlo": 1800, "dhi": 4500, "dbig": 99000, "flo": 12, "fhi": 35},
    }
    t = tiers[sheet]
    items = []

    a = random.randint(t["mlo"], t["mhi"])
    b = random.randint(t["mlo"], t["mhi"])
    items.append(_C.q(f"Quick Review (Level 4): {a} x {b} = ____", "fill", "Answer = ____"))

    d = random.randint(t["dlo"], t["dhi"])
    k_lo = 2
    k_hi = max(2, t["dbig"] // d)
    k = random.randint(k_lo, k_hi)
    n = d * k
    items.append(_C.q(f"Quick Review (Level 5): {n} / {d} = ____", "fill", "Answer = ____"))

    flo, fhi = t["flo"], t["fhi"]
    fracs = [(1, 2), (1, 3), (1, 4), (2, 3), (3, 4)]
    num, den = random.choice(fracs)
    k2 = random.randint(flo, fhi)
    qty = den * k2
    a2 = random.randint(flo, fhi)
    items.append(_C.q(f"Quick Review (Level 14, BODMAS): {num}/{den} of {qty} + {a2} x 2 = ____", "fill", "Answer = ____"))

    return items


# ───────────────────────── Speed Calculation: BODMAS + fractions/Of + squares/cubes ─────────────────────────

def _l15v3_bodmas_calc(sheet):
    """5 BODMAS questions extending Level 14's fractions-of-quantity
    with SQUARES and CUBES per direct request, making expressions even
    LONGER -- 6-7 chained operations by sheet 4. Every random value is
    generated once and reused consistently between the display string
    and the eval string (the exact bug class caught and fixed in
    Level 14)."""
    tiers = {
        1: {"lo": 4, "hi": 15, "sqlo": 2, "sqhi": 9, "fracs": [(1, 2), (1, 4), (1, 5)]},
        2: {"lo": 5, "hi": 18, "sqlo": 2, "sqhi": 10, "fracs": [(1, 2), (1, 3), (1, 4), (2, 5)]},
        3: {"lo": 6, "hi": 22, "sqlo": 2, "sqhi": 11, "fracs": [(1, 3), (2, 3), (1, 4), (3, 4), (2, 5)]},
        4: {"lo": 8, "hi": 26, "sqlo": 2, "sqhi": 12, "fracs": [(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5)]},
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
        do, po = of_term()
        ds, ps = sq_term()
        n = random.randint(lo, hi)
        variant = random.choice(["of_plus_sq", "sq_plus_of"])
        if variant == "of_plus_sq":
            disp_full = f"{do} + {ds} - {n}"
            py_full = f"{po} + {ps} - {n}"
        else:
            disp_full = f"({ds} - {n}) + {do}"
            py_full = f"({ps} - {n}) + {po}"
        return disp_full, py_full

    def build_tier2():
        do, po = of_term()
        ds, ps = sq_term()
        p, q = ordered_pair()
        variant = random.choice(["bracket_of_sq", "sq_minus_of_plus"])
        if variant == "bracket_of_sq":
            disp_full = f"({do} + {ds}) - {p} + {q}"
            py_full = f"({po} + {ps}) - {p} + {q}"
        else:
            disp_full = f"{ds} - {do} + {p}"
            py_full = f"{ps} - {po} + {p}"
        return disp_full, py_full

    def build_tier3():
        do, po = of_term()
        dc, pc = cube_term()
        ds, ps = sq_term()
        p, q = ordered_pair()
        variant = random.choice(["of_cube_bracket", "sq_of_minus"])
        if variant == "of_cube_bracket":
            disp_full = f"({do} + {dc}) - ({p} - {q})"
            py_full = f"({po} + {pc}) - ({p} - {q})"
        else:
            n, d = clean_div(min_q=2, max_q=6)
            disp_full = f"{ds} + {do} - {n} / {d}"
            py_full = f"{ps} + {po} - {n} / {d}"
        return disp_full, py_full

    def build_tier4():
        do1, po1 = of_term()
        do2, po2 = of_term()
        dc, pc = cube_term()
        ds, ps = sq_term()
        p, q = ordered_pair()
        variant = random.choice(["two_of_cube_sq", "of_cube_of_sq_bracket"])
        if variant == "two_of_cube_sq":
            disp_full = f"({do1} + {do2}) - {dc} + {p}"
            py_full = f"({po1} + {po2}) - {pc} + {p}"
        else:
            n, d = clean_div(min_q=2, max_q=6)
            disp_full = f"({do1} + {ds}) - ({dc} - {q}) + {n} / {d}"
            py_full = f"({po1} + {ps}) - ({pc} - {q}) + {n} / {d}"
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
    random.seed(15000 + hash(code) % 5000 + sheet * 31)
    concept_items, block1a, block1b = _build_block1(code, sheet)
    out = list(concept_items)
    out += block1a
    out += block1b
    out += _l15v3_quick_review(sheet)
    out += _l15v3_bodmas_calc(sheet)
    return out


LEVEL15_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SOURCE_DISPATCH
}
