"""
Fear Less Maths — LEVEL 11 (Algebra — Expressions) v3 worksheet architecture
(2026-08-04)

Same pattern as Level 10: already has 100% SVG diagram coverage from an
earlier campaign, so this reorganizes existing content into the four-
block structure rather than authoring new diagrams, and audits every
diagram type for answer leaks.

REAL BUG FOUND AND FIXED (diagram_engine.py, not just this file):
term_label_svg had NO blank parameter at all -- it always labelled
which part of a term was the Coefficient/Variable/Exponent, even when
288 questions across this level were asking the student to identify
exactly that ("In 3x, the coefficient is ____"). Fixed at the source
with blank=True as the new default.

  Q1-6   The sheet's own existing diagram questions, diagram-DEPENDENT
         ones (11H's algebra-tiles questions -- "the tiles show an
         expression" -- can't be answered without the picture)
         prioritized since they can't go in Q7-12.
  Q7-12  6 more of the sheet's own questions, self-contained text,
         diagram stripped.
  Q13-15 "Quick Review" -- toughened beyond Level 10's tier: 3-digit x
         3-digit multiplication (Level 4), 4-digit / 3-digit division
         (Level 5), and a ratio-simplification question harder than
         Level 10's own range (Level 10 -- the most directly relevant
         skill, since simplifying an algebraic expression and
         simplifying a ratio use the same "divide out the common
         factor" reasoning).
  Q16-20 "Speed Calculation" -- 5 questions, toughened beyond Level 10's
         version, per direct request to keep increasing calculation
         difficulty at each higher level.
"""
import random
import math
import content as _C


_DEP_KEYWORDS = ("graph", "diagram", "shown", "pictured", "picture",
                  "table shows", "bar shows", "chart", "the model",
                  "the tiles", "the scale", "the machine")


def _is_dependent(text):
    t = (text or "").lower()
    return any(k in t for k in _DEP_KEYWORDS)


def _item_key(item):
    return (item.get("text", ""), repr(item.get("diagram_params")))


_SOURCE_DISPATCH = {code: dict(_C._DISPATCH[code]) for code in (
    "11A", "11B", "11C", "11CUM1", "11D", "11E", "11F", "11CUM2",
    "11G", "11H", "11I", "11CUM3", "11J", "11REV",
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
        n = random.randint(2, 20) + idx
        block1b.append(_C.q(f"True or False: {n}x + {n}x = {2*n}x.", "fill", "____ (True/False)"))
        idx += 1

    return concept_items, block1a, block1b


# ───────────────────────── Quick Review (toughened beyond Level 10) ─────────────────────────

def _l11v3_quick_review(sheet):
    """3 questions, toughened beyond Level 10's tier: 3-digit x 3-digit
    multiplication (Level 4), 4-digit / 3-digit division (Level 5), and
    ratio simplification harder than Level 10's own range (Level 10 --
    simplifying an expression and simplifying a ratio both come down to
    dividing out a common factor)."""
    tiers = {
        1: {"mlo": 100, "mhi": 300, "dlo": 100, "dhi": 300, "dbig": 9000, "rlo": 20, "rhi": 80},
        2: {"mlo": 150, "mhi": 400, "dlo": 120, "dhi": 350, "dbig": 9500, "rlo": 30, "rhi": 100},
        3: {"mlo": 200, "mhi": 500, "dlo": 150, "dhi": 400, "dbig": 9700, "rlo": 40, "rhi": 130},
        4: {"mlo": 250, "mhi": 600, "dlo": 180, "dhi": 450, "dbig": 9900, "rlo": 50, "rhi": 160},
    }
    t = tiers[sheet]
    items = []

    a = random.randint(t["mlo"], t["mhi"])
    b = random.randint(t["mlo"], t["mhi"])
    items.append(_C.q(f"Quick Review (Level 4): {a} x {b} = ____", "fill", "Answer = ____"))

    d = random.randint(t["dlo"], t["dhi"])
    k = random.randint(t["dlo"] // 10, min(t["dhi"] // 10, t["dbig"] // d))
    k = max(k, 2)
    n = d * k
    items.append(_C.q(f"Quick Review (Level 5): {n} / {d} = ____", "fill", "Answer = ____"))

    shared = random.randint(4, 10)
    k1, k2 = random.sample(range(3, 9), 2)
    r1, r2 = shared * k1, shared * k2
    while r1 > t["rhi"] or r2 > t["rhi"]:
        shared = random.randint(3, 7)
        k1, k2 = random.sample(range(2, 6), 2)
        r1, r2 = shared * k1, shared * k2
    items.append(_C.q(f"Quick Review (Level 10): Simplify the ratio {r1}:{r2}.", "fill", "Answer = ____"))

    return items


# ───────────────────────── Speed Calculation (toughened beyond Level 10) ─────────────────────────

def _l11v3_speed_calc(sheet):
    tiers = {
        1: {"mul_lo": 50, "mul_hi": 130, "div_hi": 30, "sub_lo": 1000, "sub_hi": 1800},
        2: {"mul_lo": 60, "mul_hi": 170, "div_hi": 38, "sub_lo": 1200, "sub_hi": 2400},
        3: {"mul_lo": 75, "mul_hi": 220, "div_hi": 46, "sub_lo": 1500, "sub_hi": 3200},
        4: {"mul_lo": 90, "mul_hi": 280, "div_hi": 55, "sub_lo": 1800, "sub_hi": 4000},
    }
    t = tiers[sheet]
    items = []
    shapes = ["mul2x1", "div", "sub3", "mul2x2", "div"]
    random.shuffle(shapes)
    for shape in shapes:
        if shape == "mul2x1":
            a = random.randint(t["mul_lo"], t["mul_hi"])
            b = random.randint(2, 9)
            items.append(_C.q(f"Speed Calculation: {a} x {b} = ____", "fill", "Answer = ____"))
        elif shape == "mul2x2":
            a = random.randint(t["mul_lo"], t["mul_hi"])
            b = random.randint(11, t["div_hi"] + 20)
            items.append(_C.q(f"Speed Calculation: {a} x {b} = ____", "fill", "Answer = ____"))
        elif shape == "div":
            b = random.randint(2, t["div_hi"])
            k = random.randint(t["mul_lo"] // 2, t["mul_hi"])
            a = b * k
            items.append(_C.q(f"Speed Calculation: {a} / {b} = ____", "fill", "Answer = ____"))
        else:
            a = random.randint(t["sub_lo"], t["sub_hi"])
            b = random.randint(50, a - 20)
            items.append(_C.q(f"Speed Calculation: {a} - {b} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── Assembly ─────────────────────────

def build_v3_sheet(code, sheet):
    random.seed(11000 + hash(code) % 5000 + sheet * 31)
    concept_items, block1a, block1b = _build_block1(code, sheet)
    out = list(concept_items)
    out += block1a
    out += block1b
    out += _l11v3_quick_review(sheet)
    out += _l11v3_speed_calc(sheet)
    return out


LEVEL11_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SOURCE_DISPATCH
}
