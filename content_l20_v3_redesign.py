"""
Fear Less Maths — LEVEL 20 (Statistics, Probability & AP) v3 worksheet
architecture (2026-08-06)

Level 20 had ZERO diagrams at all (confirmed: 0/80 across every
sublevel) -- like Level 19, needs diagrams authored fully fresh. Three
new SVG diagrams built:
- `ap_sequence`: AP terms as dots on a line with "+cd" arc arrows
  between consecutive terms -- makes the constant common difference
  visually obvious (20A-C/CUM1/J/REV).
- `data_bar_chart`: a small bar chart of the given dataset, for mean/
  median/mode questions (20D-F/CUM2/I/J/REV) -- the data is always
  shown (it's the given, not the answer); can optionally hide one
  bar's value for "missing value given the mean" style questions.
- `probability_bag`: colored balls in a bag with a color legend, for
  probability questions (20G-I/CUM3/J/REV) -- balls are always shown
  (the given setup), blank=True hides only the total-count label so
  the student must count for themselves rather than being handed the
  denominator directly.

Legibility checked BEFORE declaring done (applying the Level 18/19
lesson for a third time): all three new types added to `big_diag`
immediately, verified visually legible, not left to a later fix.

  Q1-6   Freshly authored diagram questions per sublevel, hand-matched
         to ap_sequence / data_bar_chart / probability_bag depending
         on topic, Q1-2 worked/Q3-6 blank.
  Q7-12  6 more of the sheet's own existing text-only content.
  Q13-15 "Quick Review" -- toughened beyond Level 19's tier.
  Q16-20 "PYQ Review" -- continues the standing instruction from Level
         19: 5 cumulative review questions spanning Levels 8-18,
         REPLACING BODMAS, using the exact same generator pool as
         Level 19 for consistency.
"""
import random
import content as _C
import content_l19_v3_redesign as _L19


_SOURCE_DISPATCH = {code: dict(_C._DISPATCH[code]) for code in (
    "20A", "20B", "20C", "20CUM1", "20D", "20E", "20F", "20CUM2",
    "20G", "20H", "20I", "20CUM3", "20J", "20REV",
)}


def _mk(text, dtype, params):
    return _C.q(text, "diagram", "____", "", dtype, params)


def _item_key(item):
    return (item.get("text", ""), repr(item.get("diagram_params")))


# ───────────────────────── Block 1a: fresh diagram questions ─────────────────────────

def _block1a_ap(sheet, topic_text):
    tiers = {1: (1, 5), 2: (2, 7), 3: (3, 9), 4: (4, 12)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        first = random.randint(1, 10)
        cd = random.randint(lo, hi) * random.choice([1, 1, -1])
        n = random.choice([4, 5, 5, 6])
        find_idx = random.choice([n - 1, n - 1, random.randint(1, n - 1)])
        blank = i >= 2
        items.append(_mk(topic_text, "ap_sequence",
                          {"first": first, "cd": cd, "n": n, "find_idx": find_idx, "blank": blank}))
    return items


def _block1a_stats(sheet, topic_text):
    tiers = {1: (2, 15), 2: (2, 20), 3: (2, 25), 4: (2, 30)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        n_vals = random.choice([5, 5, 6])
        data = [random.randint(lo, hi) for _ in range(n_vals)]
        blank = False
        items.append(_mk(topic_text, "data_bar_chart", {"data": data, "blank": blank}))
    return items


def _block1a_prob(sheet, topic_text):
    palettes = [{"red": 4, "blue": 3}, {"red": 5, "blue": 4, "green": 3},
                {"blue": 6, "yellow": 5}, {"red": 3, "green": 4, "blue": 5},
                {"red": 7, "blue": 6}, {"green": 5, "yellow": 4, "red": 3}]
    items = []
    for i in range(6):
        counts = random.choice(palettes)
        blank = i >= 2
        items.append(_mk(topic_text, "probability_bag", {"counts": counts, "blank": blank}))
    return items


def _b1a_A(sheet):
    return _block1a_ap(sheet, "Study this AP. Find the common difference and the missing term.")


def _b1a_B(sheet):
    return _block1a_ap(sheet, "Use this AP to find the missing term.")


def _b1a_C(sheet):
    return _block1a_ap(sheet, "This sequence models a word problem. Find the missing term.")


def _b1a_CUM1(sheet):
    return _block1a_ap(sheet, "Review: find the common difference and the missing term.")


def _b1a_D(sheet):
    return _block1a_stats(sheet, "Find the mean of this data set.")


def _b1a_E(sheet):
    return _block1a_stats(sheet, "Find the median of this data set.")


def _b1a_F(sheet):
    return _block1a_stats(sheet, "Find the mode of this data set.")


def _b1a_CUM2(sheet):
    items = []
    items += _block1a_stats(sheet, "Find the mean, median, or mode of this data set.")[:6]
    return items


def _b1a_G(sheet):
    return _block1a_prob(sheet, "A ball is picked at random from this bag. Find the probability.")


def _b1a_H(sheet):
    return _block1a_prob(sheet, "Find the probability for this bag of balls.")


def _b1a_I(sheet):
    items = _block1a_stats(sheet, "Statistics: find the mean, median or mode.")[:3]
    items += _block1a_prob(sheet, "Probability: find P(event) for this bag.")[:3]
    return items


def _b1a_CUM3(sheet):
    return _block1a_prob(sheet, "Review: find the probability for this bag of balls.")


def _b1a_J(sheet):
    items = _block1a_ap(sheet, "Challenge: find the missing AP term.")[:2]
    items += _block1a_stats(sheet, "Challenge: find the mean/median/mode.")[:2]
    items += _block1a_prob(sheet, "Challenge: find the probability.")[:2]
    return items


def _b1a_REV(sheet):
    items = _block1a_ap(sheet, "Revision: find the missing AP term.")[:2]
    items += _block1a_stats(sheet, "Revision: find the mean/median/mode.")[:2]
    items += _block1a_prob(sheet, "Revision: find the probability.")[:2]
    return items


_BLOCK1A_BUILDERS = {
    "20A": _b1a_A, "20B": _b1a_B, "20C": _b1a_C, "20CUM1": _b1a_CUM1,
    "20D": _b1a_D, "20E": _b1a_E, "20F": _b1a_F, "20CUM2": _b1a_CUM2,
    "20G": _b1a_G, "20H": _b1a_H, "20I": _b1a_I, "20CUM3": _b1a_CUM3,
    "20J": _b1a_J, "20REV": _b1a_REV,
}


def _build_block1b(code, sheet, exclude_keys):
    items = _SOURCE_DISPATCH[code][sheet]()
    concept_items = [x for x in items if x.get("type") in ("concept_box", "tips_box")]
    qs = [x for x in items if x.get("type") not in ("concept_box", "tips_box")]
    tail_qs = [x for x in qs if not x.get("diagram_type") and _item_key(x) not in exclude_keys]
    tail_sorted = sorted(range(len(tail_qs)), key=lambda i: len(tail_qs[i].get("text", "")))
    block1b = [tail_qs[i] for i in tail_sorted[:6]] if tail_qs else []
    block1b.sort(key=lambda x: tail_qs.index(x))
    idx = 0
    while len(block1b) < 6:
        n = random.randint(2, 20) + idx
        block1b.append(_C.q(f"True or False: in the AP 1,3,5,7..., the common difference is {n % 5 + 1}.", "fill", "____ (True/False)"))
        idx += 1
    return concept_items, block1b


# ───────────────────────── Quick Review (toughened beyond Level 19) ─────────────────────────

def _l20v3_quick_review(sheet):
    tiers = {
        1: {"mlo": 40000, "mhi": 90000, "dlo": 40000, "dhi": 90000, "dbig": 9500000, "blo": 18, "bhi": 28},
        2: {"mlo": 50000, "mhi": 100000, "dlo": 45000, "dhi": 95000, "dbig": 9600000, "blo": 19, "bhi": 30},
        3: {"mlo": 60000, "mhi": 120000, "dlo": 50000, "dhi": 99000, "dbig": 9700000, "blo": 20, "bhi": 32},
        4: {"mlo": 70000, "mhi": 150000, "dlo": 55000, "dhi": 99500, "dbig": 9800000, "blo": 21, "bhi": 34},
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
    opp = random.randint(t["blo"] // 2, t["bhi"] // 2)
    hyp = random.randint(t["blo"], t["bhi"])
    items.append(_C.q(f"Quick Review (Level 19, Trig): In a right triangle, opposite = {opp}, hypotenuse = {hyp}. Find sin(theta) as a fraction.", "fill", "Answer = ____"))
    return items


# ───────────────────────── PYQ Review: cumulative Levels 8-18 (continues standing instruction) ─────────────────────────

def _l20v3_pyq_review(sheet, code):
    """Same generator pool as Level 19 -- continues the standing
    instruction (PYQ Review replaces BODMAS from Level 19 onward),
    cumulatively spanning Levels 8-18."""
    offset = (hash(code) % 11 + (sheet - 1) * 5 + 2) % 11
    chosen = [_L19._ALL_PYQ_LEVELS[(offset + i) % 11] for i in range(5)]
    items = []
    for lvl in chosen:
        items.append(_L19._PYQ_GENERATORS[lvl](sheet))
    return items


# ───────────────────────── Assembly ─────────────────────────

def build_v3_sheet(code, sheet):
    random.seed(20000 + hash(code) % 5000 + sheet * 31)
    block1a = _BLOCK1A_BUILDERS[code](sheet)
    used = {_item_key(x) for x in block1a}
    concept_items, block1b = _build_block1b(code, sheet, used)
    out = list(concept_items)
    out += block1a
    out += block1b
    out += _l20v3_quick_review(sheet)
    out += _l20v3_pyq_review(sheet, code)
    return out


LEVEL20_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _BLOCK1A_BUILDERS
}
