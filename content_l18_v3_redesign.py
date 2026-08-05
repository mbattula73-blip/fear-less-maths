"""
Fear Less Maths — LEVEL 18 (Mensuration) v3 worksheet architecture
(2026-08-05)

Same pattern as Levels 10-17: already has 100% SVG diagram coverage,
so this reorganizes existing content rather than authoring new
diagrams. Level 18 has its own diagram-injection wrapper
(_l18_wrap/_l18_visualize in content_l18.py, same structural pattern
as Level 16) -- sourced from the real, fully-wrapped dispatch
(content._DISPATCH) from the start this time, having learned that
lesson from Level 16.

Audited all 14 diagram types used here (rectangle_dims, square_dims,
triangle_area, circle_area, cuboid_3d, cube_3d, cylinder_3d, cone_3d,
sphere_3d, hemisphere_3d, composite_mensuration, circle_sector,
circle_ring, polygon_angle_sum [already fixed via Level 17]).

REAL LEAK FOUND AND FIXED: cone_3d always computed and displayed the
slant height, even on questions explicitly asking "slant = ____" --
confirmed many live questions ask exactly this (18F). Fixed with
blank=True as the new default (no existing call site passed this
parameter), hiding the slant value while keeping r and h (the given
dimensions) visible. All other 13 types only ever show the GIVEN
dimensions, never a computed area/volume/perimeter -- no other leaks.

Diagram-dependency check: every sublevel's questions are 100% self-
contained (state every dimension in the text, diagram is illustrative)
-- no "look at the diagram" dependent questions anywhere in this level,
the cleanest case yet.

  Q1-6   The sheet's own existing diagram questions, Q1-2 worked/Q3-6
         blank re-enforced regardless of the source's own setting.
  Q7-12  6 more of the sheet's own questions, diagram stripped.
  Q13-15 "Quick Review" -- toughened beyond Level 17's tier: 5-digit x
         5-digit multiplication (Level 4), 6-digit / 5-digit division
         (Level 5), a fractions+squares+cubes BODMAS expression harder
         than Level 17's own range.
  Q16-20 "Speed Calculation" -- BODMAS continuing the escalation
         (fractions + "Of" + squares + cubes), bigger ranges and more
         chained operations than Level 17.
"""
import random
import content as _C


def _item_key(item):
    return (item.get("text", ""), repr(item.get("diagram_params")))


_SOURCE_DISPATCH = {code: dict(_C._DISPATCH[code]) for code in (
    "18A", "18B", "18C", "18CUM1", "18D", "18E", "18F", "18CUM2",
    "18G", "18H", "18I", "18CUM3", "18J", "18REV",
)}


def _build_block1(code, sheet):
    items = _SOURCE_DISPATCH[code][sheet]()
    concept_items = [x for x in items if x.get("type") in ("concept_box", "tips_box")]
    qs = [x for x in items if x.get("type") not in ("concept_box", "tips_box")]
    diag_qs = [x for x in qs if x.get("diagram_type")]

    block1a_src = diag_qs[:6]
    block1a = []
    for i, x in enumerate(block1a_src):
        y = dict(x)
        params = dict(y.get("diagram_params") or {})
        params["blank"] = (i >= 2)
        y["diagram_params"] = params
        block1a.append(y)
    used_keys = {_item_key(x) for x in block1a_src}

    pool = [x for x in diag_qs if _item_key(x) not in used_keys]
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
        n = random.randint(3, 20) + idx
        block1b.append(_C.q(f"True or False: a cube with side {n} has all 6 faces equal in area.", "fill", "____ (True/False)"))
        idx += 1

    return concept_items, block1a, block1b


# ───────────────────────── Quick Review (toughened beyond Level 17) ─────────────────────────

def _l18v3_quick_review(sheet):
    """3 questions, toughened beyond Level 17's tier: 5-digit x 5-digit
    multiplication (Level 4), 6-digit / 5-digit division (Level 5), and
    a fractions+squares+cubes BODMAS expression harder than Level 17's
    own range."""
    tiers = {
        1: {"mlo": 15000, "mhi": 40000, "dlo": 15000, "dhi": 40000, "dbig": 9500000, "blo": 12, "bhi": 24},
        2: {"mlo": 20000, "mhi": 50000, "dlo": 18000, "dhi": 45000, "dbig": 9600000, "blo": 13, "bhi": 26},
        3: {"mlo": 25000, "mhi": 60000, "dlo": 20000, "dhi": 50000, "dbig": 9700000, "blo": 14, "bhi": 28},
        4: {"mlo": 30000, "mhi": 70000, "dlo": 22000, "dhi": 55000, "dbig": 9800000, "blo": 15, "bhi": 30},
    }
    t = tiers[sheet]
    items = []

    a = random.randint(t["mlo"], t["mhi"])
    b = random.randint(t["mlo"], t["mhi"])
    items.append(_C.q(f"Quick Review (Level 4): {a} x {b} = ____", "fill", "Answer = ____"))

    d = random.randint(t["dlo"], t["dhi"])
    k_lo = t["dlo"] // 1000
    k_hi = min(t["dhi"] // 1000, t["dbig"] // d)
    if k_hi < k_lo:
        k_hi = k_lo
    k = max(random.randint(k_lo, k_hi), 2)
    n = d * k
    items.append(_C.q(f"Quick Review (Level 5): {n} / {d} = ____", "fill", "Answer = ____"))

    lo, hi = t["blo"], t["bhi"]
    num, den = random.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)])
    k1 = random.randint(lo, hi)
    qty = den * k1
    sq_base = random.randint(4, 10)
    cube_base = random.randint(2, 6)
    items.append(_C.q(f"Quick Review (Level 17, BODMAS): {num}/{den} of {qty} + {sq_base}^2 - {cube_base}^3 = ____", "fill", "Answer = ____"))

    return items


# ───────────────────────── Speed Calculation: BODMAS, escalated further ─────────────────────────

def _l18v3_bodmas_calc(sheet):
    """5 BODMAS questions continuing Levels 14-17's fractions+Of+
    squares+cubes, bigger ranges and more chained operations than
    Level 17. Every random value generated once and reused
    consistently between the display string and the eval string."""
    tiers = {
        1: {"lo": 8, "hi": 24, "sqlo": 4, "sqhi": 12, "fracs": [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5)]},
        2: {"lo": 10, "hi": 28, "sqlo": 4, "sqhi": 13, "fracs": [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5)]},
        3: {"lo": 12, "hi": 32, "sqlo": 5, "sqhi": 14, "fracs": [(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5), (1, 6)]},
        4: {"lo": 14, "hi": 38, "sqlo": 5, "sqhi": 15, "fracs": [(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5), (1, 6), (5, 6)]},
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
    random.seed(18000 + hash(code) % 5000 + sheet * 31)
    concept_items, block1a, block1b = _build_block1(code, sheet)
    out = list(concept_items)
    out += block1a
    out += block1b
    out += _l18v3_quick_review(sheet)
    out += _l18v3_bodmas_calc(sheet)
    return out


LEVEL18_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SOURCE_DISPATCH
}
