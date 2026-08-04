"""
Fear Less Maths — LEVEL 10 (Ratio & Proportion) v3 worksheet architecture
(2026-08-04)

Level 10 already has full SVG diagram coverage (100% of questions,
built in an earlier campaign) -- unlike Levels 6-9, the job here isn't
adding diagrams, it's REORGANIZING into the same four-block structure
and verifying no answer leaks:

  Q1-6   The sheet's own already-existing diagram questions (ratio_
         objects, ratio_table, double_number_line, continued_ratio_bar,
         unit_rate, cross_multiply_bowtie, ladder_division, proportion_
         graph, scale_comparison, similar_figures, ratio_bar -- all
         already SVG, already have a proper worked/blank toggle).
         Diagram-DEPENDENT questions (text says "look at the graph" /
         "the bar shows" etc, so the picture IS the question, not
         decoration) are prioritized here since they can't go in Block
         1b. Verified: every worked (blank=False) instance is a
         genuine Q1-2 teaching example, never a naked answer leak on a
         practice item -- checked every diagram type's blank=True path
         actually hides the computed value, not just relabels it.
  Q7-12  6 more of the sheet's own questions, chosen from the ones
         whose TEXT IS SELF-CONTAINED (states every number needed, the
         diagram there was decoration not information) -- diagram
         stripped so they render as plain text. Falls back to a safe
         synthesized true/false question if a sublevel runs short.
  Q13-15 "Quick Review" -- toughened BEYOND Level 9's tier: 3-digit x
         2-digit multiplication (Level 4), 4-digit / 2-digit division
         (Level 5), and a percentage-of-a-quantity question harder than
         Level 9's own range (Level 9 -- the most directly relevant
         skill, since a ratio simplifies the same way a percentage
         does, and rate/unit-rate work leans on both).
  Q16-20 "Speed Calculation" -- 5 questions, toughened beyond Level 9's
         version, escalating across sheets 1-4.
"""
import random
import content as _C


_DEP_KEYWORDS = ("graph", "diagram", "shown", "pictured", "picture",
                  "table shows", "bar shows", "chart", "the model")


def _is_dependent(text):
    t = (text or "").lower()
    return any(k in t for k in _DEP_KEYWORDS)


def _item_key(item):
    return (item.get("text", ""), repr(item.get("diagram_params")))


_SOURCE_DISPATCH = {code: dict(_C._DISPATCH[code]) for code in (
    "10A", "10B", "10C", "10CUM1", "10D", "10E", "10F", "10CUM2",
    "10G", "10H", "10I", "10CUM3", "10J", "10REV",
)}


def _build_block1(code, sheet):
    items = _SOURCE_DISPATCH[code][sheet]()
    concept_items = [x for x in items if x.get("type") in ("concept_box", "tips_box")]
    qs = [x for x in items if x.get("type") not in ("concept_box", "tips_box")]
    diag_qs = [x for x in qs if x.get("diagram_type")]
    dependent = [x for x in diag_qs if _is_dependent(x.get("text", ""))]
    independent = [x for x in diag_qs if not _is_dependent(x.get("text", ""))]

    # Block 1a: prioritize diagram-dependent questions (can't go anywhere
    # else), backfill with independent ones if a sublevel has too few.
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

    # Block 1b: self-contained (independent) questions not already used,
    # diagram stripped so they render as plain text.
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
        m = random.randint(2, 20) + idx
        block1b.append(_C.q(f"True or False: the ratio {n}:{m} is the same as {n*2}:{m*2}.",
                             "fill", "____ (True/False)"))
        idx += 1

    return concept_items, block1a, block1b


# ───────────────────────── Quick Review (toughened beyond Level 9) ─────────────────────────

def _l10v3_quick_review(sheet):
    """3 questions, toughened beyond Level 9's tier: 3-digit x 2-digit
    multiplication (Level 4), 4-digit / 2-digit division (Level 5), and
    percentage-of-a-quantity harder than Level 9's own range (Level 9 --
    ratios simplify the same way percentages do, and rate work leans on
    both)."""
    tiers = {
        1: {"mlo": 100, "mhi": 400, "mmul": 30, "dlo": 20, "dhi": 40, "dbig": 4000, "plo": 500, "phi": 1500},
        2: {"mlo": 150, "mhi": 500, "mmul": 45, "dlo": 25, "dhi": 55, "dbig": 6000, "plo": 800, "phi": 2500},
        3: {"mlo": 200, "mhi": 700, "mmul": 65, "dlo": 30, "dhi": 70, "dbig": 8000, "plo": 1200, "phi": 3500},
        4: {"mlo": 300, "mhi": 900, "mmul": 95, "dlo": 35, "dhi": 90, "dbig": 9500, "plo": 1500, "phi": 5000},
    }
    t = tiers[sheet]
    items = []

    a = random.randint(t["mlo"], t["mhi"])
    b = random.randint(11, t["mmul"])
    items.append(_C.q(f"Quick Review (Level 4): {a} x {b} = ____", "fill", "Answer = ____"))

    d = random.randint(t["dlo"], t["dhi"])
    k = random.randint(t["dlo"], min(t["dhi"], t["dbig"] // d))
    n = d * k
    items.append(_C.q(f"Quick Review (Level 5): {n} / {d} = ____", "fill", "Answer = ____"))

    percent = random.choice([5, 10, 15, 20, 25, 30, 40, 60, 75])
    qty = random.randint(t["plo"], t["phi"])
    items.append(_C.q(f"Quick Review (Level 9): Find {percent}% of {qty}.", "fill", "Answer = ____"))

    return items


# ───────────────────────── Speed Calculation (toughened beyond Level 9) ─────────────────────────

def _l10v3_speed_calc(sheet):
    tiers = {
        1: {"mul_lo": 40, "mul_hi": 100, "div_hi": 25, "sub_lo": 600, "sub_hi": 999},
        2: {"mul_lo": 50, "mul_hi": 140, "div_hi": 32, "sub_lo": 800, "sub_hi": 1500},
        3: {"mul_lo": 60, "mul_hi": 180, "div_hi": 40, "sub_lo": 1000, "sub_hi": 2000},
        4: {"mul_lo": 70, "mul_hi": 220, "div_hi": 50, "sub_lo": 1200, "sub_hi": 3000},
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
            b = random.randint(11, t["div_hi"] + 15)
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
    random.seed(10000 + hash(code) % 5000 + sheet * 31)
    concept_items, block1a, block1b = _build_block1(code, sheet)
    out = list(concept_items)
    out += block1a
    out += block1b
    out += _l10v3_quick_review(sheet)
    out += _l10v3_speed_calc(sheet)
    return out


LEVEL10_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SOURCE_DISPATCH
}
