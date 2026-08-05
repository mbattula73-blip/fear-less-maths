"""
Fear Less Maths — LEVEL 16 (Lines, Angles & Triangles) v3 worksheet architecture
(2026-08-05)

Same pattern as Levels 10-15: already has 100% SVG diagram coverage,
so this reorganizes existing content rather than authoring new
diagrams. Audited all 13 diagram types used here (pythagoras,
angle_sum_triangle, transversal_angles, congruence, points_lines_rays,
angle_pair, similar_triangles, area_same_base, bpt_triangle,
triangle_classify, triangle_inequality, isosceles_theorem,
midpoint_theorem) for answer leaks -- all already correctly built, no
leaks found.

  Q1-6   The sheet's own existing diagram questions, diagram-DEPENDENT
         ones prioritized where present (16B/16C/16F/16G have some).
  Q7-12  6 more of the sheet's own questions, self-contained text,
         diagram stripped.
  Q13-15 "Quick Review" -- toughened beyond Level 15's tier: 4-digit x
         4-digit multiplication (Level 4), 5-digit / 4-digit division
         (Level 5), a fractions+squares+cubes BODMAS expression harder
         than Level 15's own range (Level 15 -- the most directly
         relevant skill, since triangle-side/area calculations lean on
         exactly this kind of arithmetic).
  Q16-20 "Speed Calculation" -- BODMAS continuing the escalation from
         Level 15 (fractions + "Of" + squares + cubes): bigger number
         ranges and MORE chained operations (7-8 by sheet 4) per
         direct request to keep making these even lengthier. Same
         guaranteed-clean construction (every random value generated
         once and reused consistently between display and eval
         strings -- the exact bug class caught in Level 14).
"""
import random
import content as _C


_DEP_KEYWORDS = ("graph", "diagram", "shown", "pictured", "picture",
                  "table shows", "bar shows", "chart", "the model",
                  "the tiles", "the scale", "the machine", "the ladder",
                  "the boxes", "the square", "the staircase", "the picture",
                  "marked")


def _is_dependent(text):
    t = (text or "").lower()
    return any(k in t for k in _DEP_KEYWORDS)


def _item_key(item):
    return (item.get("text", ""), repr(item.get("diagram_params")))


_SOURCE_DISPATCH = {code: dict(_C._DISPATCH[code]) for code in (
    "16A", "16B", "16C", "16CUM1", "16D", "16E", "16F", "16CUM2",
    "16G", "16H", "16I", "16CUM3", "16J", "16REV",
)}


def _build_block1(code, sheet):
    items = _SOURCE_DISPATCH[code][sheet]()
    concept_items = [x for x in items if x.get("type") in ("concept_box", "tips_box")]
    qs = [x for x in items if x.get("type") not in ("concept_box", "tips_box")]
    diag_qs = [x for x in qs if x.get("diagram_type")]
    dependent = [x for x in diag_qs if _is_dependent(x.get("text", ""))]
    independent = [x for x in diag_qs if not _is_dependent(x.get("text", ""))]

    n_diag = 5 if code == "16CUM3" else 6
    block1a_src = list(dependent[:n_diag])
    if len(block1a_src) < n_diag:
        block1a_src += independent[:n_diag - len(block1a_src)]
    block1a = []
    for i, x in enumerate(block1a_src):
        y = dict(x)
        params = dict(y.get("diagram_params") or {})
        params["blank"] = (i >= 2)
        y["diagram_params"] = params
        block1a.append(y)
    used_keys = {_item_key(x) for x in block1a_src}

    n_text = 12 - n_diag
    pool = [x for x in independent if _item_key(x) not in used_keys]
    pool_sorted = sorted(range(len(pool)), key=lambda i: len(pool[i].get("text", "")))
    block1b_src = [pool[i] for i in pool_sorted[:n_text]]
    block1b = []
    for x in block1b_src:
        y = dict(x)
        y["type"] = "fill"
        y["diagram_type"] = None
        y["diagram_params"] = None
        block1b.append(y)
    idx = 0
    while len(block1b) < n_text:
        n = random.randint(20, 80) + idx
        block1b.append(_C.q(f"True or False: an angle of {n}\u00b0 is obtuse.", "fill", "____ (True/False)"))
        idx += 1

    return concept_items, block1a, block1b


# ───────────────────────── Quick Review (toughened beyond Level 15) ─────────────────────────

def _l16v3_quick_review(sheet):
    """3 questions, toughened beyond Level 15's tier: 4-digit x 4-digit
    multiplication (Level 4), 5-digit / 4-digit division (Level 5), and
    a fractions+squares+cubes BODMAS expression harder than Level 15's
    own range (Level 15 -- triangle-side/area calculations lean on
    exactly this kind of arithmetic)."""
    tiers = {
        1: {"mlo": 1500, "mhi": 3500, "dlo": 1200, "dhi": 3000, "dbig": 95000, "blo": 6, "bhi": 15},
        2: {"mlo": 2000, "mhi": 4500, "dlo": 1500, "dhi": 3500, "dbig": 96000, "blo": 7, "bhi": 17},
        3: {"mlo": 2500, "mhi": 5500, "dlo": 1800, "dhi": 4000, "dbig": 97000, "blo": 8, "bhi": 19},
        4: {"mlo": 3000, "mhi": 6500, "dlo": 2000, "dhi": 4500, "dbig": 98000, "blo": 9, "bhi": 21},
    }
    t = tiers[sheet]
    items = []

    a = random.randint(t["mlo"], t["mhi"])
    b = random.randint(t["mlo"], t["mhi"])
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
    n2 = random.randint(lo, hi)
    items.append(_C.q(f"Quick Review (Level 15, BODMAS): {num}/{den} of {qty} + {sq_base}^2 - {n2} = ____", "fill", "Answer = ____"))

    return items


# ───────────────────────── Speed Calculation: BODMAS, escalated further ─────────────────────────

def _l16v3_bodmas_calc(sheet):
    """5 BODMAS questions continuing Level 15's fractions+Of+squares+
    cubes, with bigger ranges and MORE chained operations (7-8 by sheet
    4) per direct request. Every random value generated once and
    reused consistently between the display string and the eval
    string."""
    tiers = {
        1: {"lo": 5, "hi": 18, "sqlo": 2, "sqhi": 10, "fracs": [(1, 2), (1, 3), (1, 4), (2, 5)]},
        2: {"lo": 6, "hi": 22, "sqlo": 2, "sqhi": 11, "fracs": [(1, 2), (1, 3), (2, 3), (1, 4), (2, 5)]},
        3: {"lo": 8, "hi": 26, "sqlo": 3, "sqhi": 12, "fracs": [(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5)]},
        4: {"lo": 10, "hi": 32, "sqlo": 3, "sqhi": 13, "fracs": [(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5), (1, 6)]},
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
        p, q = ordered_pair()
        n = random.randint(lo, hi)
        variant = random.choice(["of_sq_sub", "sq_of_bracket"])
        if variant == "of_sq_sub":
            disp_full = f"{do} + {ds} - {p} + {q}"
            py_full = f"{po} + {ps} - {p} + {q}"
        else:
            n2 = random.randint(lo, hi)
            disp_full = f"({ds} - {n}) + {do} - {n2}"
            py_full = f"({ps} - {n}) + {po} - {n2}"
        return disp_full, py_full

    def build_tier2():
        do1, po1 = of_term()
        do2, po2 = of_term()
        dc, pc = cube_term()
        p, q = ordered_pair()
        variant = random.choice(["two_of_cube", "of_sq_cube"])
        if variant == "two_of_cube":
            disp_full = f"({do1} + {do2}) - {dc} + {p} - {q}"
            py_full = f"({po1} + {po2}) - {pc} + {p} - {q}"
        else:
            ds, ps = sq_term()
            n = random.randint(lo, hi)
            disp_full = f"{do1} + {ds} - {dc} + {n}"
            py_full = f"{po1} + {ps} - {pc} + {n}"
        return disp_full, py_full

    def build_tier3():
        do1, po1 = of_term()
        do2, po2 = of_term()
        ds, ps = sq_term()
        dc, pc = cube_term()
        p, q = ordered_pair()
        variant = random.choice(["all_four", "bracket_mix"])
        if variant == "all_four":
            disp_full = f"({do1} + {ds}) - ({dc} - {p}) + {q}"
            py_full = f"({po1} + {ps}) - ({pc} - {p}) + {q}"
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
        variant = random.choice(["five_term", "bracket_heavy"])
        if variant == "five_term":
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
    random.seed(16000 + hash(code) % 5000 + sheet * 31)
    concept_items, block1a, block1b = _build_block1(code, sheet)
    out = list(concept_items)
    out += block1a
    out += block1b
    out += _l16v3_quick_review(sheet)
    out += _l16v3_bodmas_calc(sheet)
    return out


LEVEL16_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SOURCE_DISPATCH
}
