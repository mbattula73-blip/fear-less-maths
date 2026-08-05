"""
Fear Less Maths — LEVEL 14 (Polynomials) v3 worksheet architecture
(2026-08-04)

Same pattern as Levels 10-12: already has 100% SVG diagram coverage,
so this reorganizes existing content rather than authoring new
diagrams. Audited all 10 diagram types used here (identity_square,
poly_anatomy, like_terms_sort, area_model, factor_x_method,
polynomial_graph, division_algorithm_box, substitution_steps,
hcf_factor_boxes, degree_staircase) for answer leaks -- all already
correctly built, no leaks found (cleanest audit this session).

  Q1-6   The sheet's own existing diagram questions, diagram-DEPENDENT
         ones prioritized (14H/14CUM3/14REV have some -- "the graph
         shows..." can't be answered without the picture).
  Q7-12  6 more of the sheet's own questions, self-contained text,
         diagram stripped.
  Q13-15 "Quick Review" -- toughened beyond Level 13's tier: 4-digit x
         3-digit multiplication (Level 4), 5-digit / 3-digit division
         (Level 5), a BODMAS expression harder than Level 13's own
         range (Level 13 -- the most directly relevant skill, since
         evaluating a polynomial at a value IS a BODMAS calculation).
  Q16-20 "Speed Calculation" -- BODMAS extended with FRACTIONS and the
         "Of" operation per direct request, making expressions longer
         than Level 13's: "1/2 of 20 + 3 x 4" style terms combined with
         brackets/exponents/other operations, 5-6 chained operations
         per expression by sheet 4. Same guaranteed-clean construction
         (every fraction-of-quantity built to divide exactly, retried
         until non-negative integer result).
"""
import random
import content as _C


_DEP_KEYWORDS = ("graph", "diagram", "shown", "pictured", "picture",
                  "table shows", "bar shows", "chart", "the model",
                  "the tiles", "the scale", "the machine", "the ladder",
                  "the boxes", "the square", "the staircase")


def _is_dependent(text):
    t = (text or "").lower()
    return any(k in t for k in _DEP_KEYWORDS)


def _item_key(item):
    return (item.get("text", ""), repr(item.get("diagram_params")))


_SOURCE_DISPATCH = {code: dict(_C._DISPATCH[code]) for code in (
    "14A", "14B", "14C", "14CUM1", "14D", "14E", "14F", "14CUM2",
    "14G", "14H", "14I", "14CUM3", "14J", "14REV",
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
        n = random.randint(2, 8) + idx
        block1b.append(_C.q(f"True or False: {n}x^2 and {n+1}x^2 are like terms.", "fill", "____ (True/False)"))
        idx += 1

    return concept_items, block1a, block1b


# ───────────────────────── Quick Review (toughened beyond Level 13) ─────────────────────────

def _l14v3_quick_review(sheet):
    """3 questions, toughened beyond Level 13's tier: 4-digit x 3-digit
    multiplication (Level 4), 5-digit / 3-digit division (Level 5),
    and a BODMAS expression harder than Level 13's own range (Level 13
    -- evaluating a polynomial at a value IS a BODMAS calculation)."""
    tiers = {
        1: {"mlo": 1000, "mhi": 3000, "mmul": 200, "dlo": 200, "dhi": 500, "dbig": 90000, "blo": 8, "bhi": 25},
        2: {"mlo": 1500, "mhi": 4000, "mmul": 300, "dlo": 250, "dhi": 600, "dbig": 95000, "blo": 10, "bhi": 30},
        3: {"mlo": 2000, "mhi": 5000, "mmul": 400, "dlo": 300, "dhi": 700, "dbig": 97000, "blo": 12, "bhi": 35},
        4: {"mlo": 2500, "mhi": 6000, "mmul": 500, "dlo": 350, "dhi": 800, "dbig": 99000, "blo": 15, "bhi": 40},
    }
    t = tiers[sheet]
    items = []

    a = random.randint(t["mlo"], t["mhi"])
    b = random.randint(100, t["mmul"])
    items.append(_C.q(f"Quick Review (Level 4): {a} x {b} = ____", "fill", "Answer = ____"))

    d = random.randint(t["dlo"], t["dhi"])
    k_lo = t["dlo"]
    k_hi = min(t["dhi"], t["dbig"] // d)
    if k_hi < k_lo:
        k_hi = k_lo
    k = max(random.randint(k_lo, k_hi), 2)
    n = d * k
    items.append(_C.q(f"Quick Review (Level 5): {n} / {d} = ____", "fill", "Answer = ____"))

    lo, hi = t["blo"], t["bhi"]
    a1, b1 = random.randint(lo, hi), random.randint(lo, hi)
    c1 = random.randint(2, 9)
    a1, b1 = max(a1, b1), min(a1, b1)
    items.append(_C.q(f"Quick Review (Level 13, BODMAS): ({a1} - {b1}) x {c1} + {random.randint(lo,hi)} = ____", "fill", "Answer = ____"))

    return items


# ───────────────────────── Speed Calculation: BODMAS + fractions + "Of" ─────────────────────────

def _l14v3_bodmas_calc(sheet):
    """5 BODMAS questions extended with fractions and the 'Of' operation
    per direct request, making expressions LONGER than Level 13's --
    5-6 chained operations by sheet 4. Every fraction-of-quantity term
    is constructed so the quantity divides the fraction's denominator
    exactly (a clean integer result), and the whole expression is
    retried (bounded) until it evaluates to a non-negative integer."""
    tiers = {
        1: {"lo": 5, "hi": 20, "fracs": [(1, 2), (1, 4), (1, 5)]},
        2: {"lo": 6, "hi": 25, "fracs": [(1, 2), (1, 3), (1, 4), (2, 5)]},
        3: {"lo": 8, "hi": 30, "fracs": [(1, 3), (2, 3), (1, 4), (3, 4), (2, 5)]},
        4: {"lo": 10, "hi": 35, "fracs": [(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5)]},
    }
    t = tiers[sheet]
    lo, hi = t["lo"], t["hi"]
    fracs = t["fracs"]

    def r():
        return random.randint(lo, hi)

    def of_term():
        """A 'num/den of quantity' term that divides exactly -- returns
        (display_string, python_eval_string, value)."""
        num, den = random.choice(fracs)
        k = random.randint(lo, hi)
        qty = den * k
        val = num * k
        disp = f"{num}/{den} of {qty}"
        pyeval = f"({num}/{den}*{qty})"
        return disp, pyeval, val

    def ordered_pair():
        a, b = r(), r()
        return (a, b) if a >= b else (b, a)

    def clean_div(min_q=2, max_q=None):
        max_q = max_q or hi
        divisor = random.randint(2, max(2, hi // 2))
        quotient = random.randint(min_q, max_q)
        return divisor * quotient, divisor

    def build_tier1():
        disp, pyev, val = of_term()
        a, b = r(), r()
        variant = random.choice(["add_mul", "bracket_of_plus"])
        if variant == "add_mul":
            disp_full = f"{disp} + {a} x {b}"
            py_full = f"{pyev} + {a}*{b}"
        else:
            disp_full = f"({a} + {disp}) x 2"
            py_full = f"({a} + {pyev}) * 2"
        return disp_full, py_full

    def build_tier2():
        d1, p1, v1 = of_term()
        p, q = ordered_pair()
        variant = random.choice(["two_terms", "of_minus_mul"])
        if variant == "two_terms":
            d2, p2, v2 = of_term()
            n = random.randint(lo, hi)
            disp_full = f"{d1} + {d2} - {n}"
            py_full = f"{p1} + {p2} - {n}"
        else:
            disp_full = f"{d1} x 2 - {p} + {q}"
            py_full = f"{p1} * 2 - {p} + {q}"
        return disp_full, py_full

    def build_tier3():
        d1, p1, v1 = of_term()
        d2, p2, v2 = of_term()
        p, q = ordered_pair()
        variant = random.choice(["bracket_two_of", "of_bracket"])
        if variant == "bracket_two_of":
            n = random.randint(lo, hi)
            disp_full = f"({d1} + {d2}) x 2 - {n}"
            py_full = f"({p1} + {p2}) * 2 - {n}"
        else:
            n, d = clean_div(min_q=2, max_q=6)
            disp_full = f"{d1} - ({p} - {q}) + {n} / {d}"
            py_full = f"{p1} - ({p} - {q}) + {n} / {d}"
        return disp_full, py_full

    def build_tier4():
        d1, p1, v1 = of_term()
        d2, p2, v2 = of_term()
        p, q = ordered_pair()
        variant = random.choice(["two_of_bracket_mul", "of_squared_mix"])
        if variant == "two_of_bracket_mul":
            e = random.randint(2, 5)
            f2 = random.randint(2, 5)
            disp_full = f"({d1} + {d2}) x {e} - {p} x {f2}"
            py_full = f"({p1} + {p2}) * {e} - {p} * {f2}"
        else:
            n, d = clean_div(min_q=2, max_q=6)
            dd = d if d > 0 else 2
            disp_full = f"{d1} + {p}^2 / {dd} - {d2}"
            py_full = f"{p1} + {p}**2 / {dd} - {p2}"
        return disp_full, py_full

    builders = {1: build_tier1, 2: build_tier2, 3: build_tier3, 4: build_tier4}
    build = builders[sheet]

    items = []
    for _ in range(5):
        disp_full = py_full = None
        for _try in range(80):
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
            disp, pyev, v = of_term()
            disp_full = f"{disp} + {r()}"
            py_full = f"{pyev} + {r()}"
        items.append(_C.q(f"Speed Calculation (BODMAS): {disp_full} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── Assembly ─────────────────────────

def build_v3_sheet(code, sheet):
    random.seed(14000 + hash(code) % 5000 + sheet * 31)
    concept_items, block1a, block1b = _build_block1(code, sheet)
    out = list(concept_items)
    out += block1a
    out += block1b
    out += _l14v3_quick_review(sheet)
    out += _l14v3_bodmas_calc(sheet)
    return out


LEVEL14_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SOURCE_DISPATCH
}
