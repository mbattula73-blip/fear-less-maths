"""
Fear Less Maths — LEVEL 7 (Fractions) v3 worksheet architecture
(2026-08-04)

Same three-block structure as the Level 6 (Factors/HCF/LCM) v3 rewrite,
adapted to Level 7's different underlying content shape (rotating
comp/tf/missing/numeral/multisel/matching formats via question_formats.py,
not the diagram-cluster-then-tail shape Level 6 used) and with TOUGHER
review/calculation content per direct request:

  Q1-12  This sheet's own topic (e.g. Fraction concept for 7A):
         Q1-6  WITH a diagram, taken from the sheet's own already-vetted
               diagram questions (falls back to synthesizing extra
               fraction-bar diagrams for the rare sublevel/sheet that
               doesn't have 6 -- 7B sheet 1 has zero)
         Q7-12 NO diagram, adaptively picking 6 that fit the page budget
               while preserving format variety (computation/True-False/
               missing-number/word-style/multi-select/matching)
  Q13-15 "Quick Review" -- TOUGHENED prerequisite check, one each from
         three skills fraction work leans on hardest: 3-digit subtraction
         with regrouping (Level 3), 2-digit x 2-digit multiplication
         (Level 4), and HCF/LCM at a harder number range than Level 6's
         own teaching range (the most directly relevant skill --
         simplifying a fraction IS finding an HCF).
  Q16-20 "Speed Calculation" -- 5 TOUGHENED rapid arithmetic questions
         (multiplication/division/subtraction mixed, 2-3 digit numbers),
         escalating across sheets 1-4. Deliberately harder than Level 6's
         version of this block, and deliberately NOT fraction questions
         -- this is whole-number computational fluency practice, not a
         second dose of the sheet's own topic.
"""
import random
import math
from content import cb, q
import content_l9_fractions as _L7


def _gcd(a, b):
    return math.gcd(a, b)


def _l7v3_hcf_lcm(a, b, want):
    g = math.gcd(a, b)
    if want == "hcf":
        return g
    return a * b // g


# ───────────────────────── Quick Review (toughened) ─────────────────────────

def _l7v3_quick_review(sheet):
    """3 questions: 3-digit subtraction with regrouping (Level 3),
    2-digit x 2-digit multiplication (Level 4), HCF or LCM at a harder
    range than Level 6's own teaching range (Level 6) -- deliberately
    tougher than simple fact-recall since by Level 7 students should
    handle these fluently at a real working size, not just single-digit
    facts."""
    tiers = {
        1: {"sub_hi": 500, "sub_lo": 200, "mul_hi": 30, "mul_lo": 12, "hcflcm_hi": 48, "hcflcm_lo": 12},
        2: {"sub_hi": 700, "sub_lo": 300, "mul_hi": 45, "mul_lo": 15, "hcflcm_hi": 60, "hcflcm_lo": 18},
        3: {"sub_hi": 900, "sub_lo": 400, "mul_hi": 60, "mul_lo": 20, "hcflcm_hi": 84, "hcflcm_lo": 24},
        4: {"sub_hi": 999, "sub_lo": 500, "mul_hi": 90, "mul_lo": 25, "hcflcm_hi": 96, "hcflcm_lo": 30},
    }
    t = tiers[sheet]
    items = []

    # 3-digit subtraction, forced to require at least one regroup/borrow
    for _ in range(30):
        a = random.randint(t["sub_lo"], t["sub_hi"])
        b = random.randint(100, a - 50)
        # require at least one column where the top digit < bottom digit
        da, db = str(a).zfill(3), str(b).zfill(3)
        if any(int(da[i]) < int(db[i]) for i in range(3)):
            break
    items.append(q(f"Quick Review (Level 3): {a} - {b} = ____", "fill", "Answer = ____"))

    # 2-digit x 2-digit multiplication
    m1 = random.randint(t["mul_lo"], t["mul_hi"])
    m2 = random.randint(t["mul_lo"], t["mul_hi"])
    items.append(q(f"Quick Review (Level 4): {m1} x {m2} = ____", "fill", "Answer = ____"))

    # HCF or LCM at a harder range than Level 6's own teaching sublevels.
    # Constructed to share a real common factor (not just two random
    # numbers that might be coprime/one prime) so the question actually
    # exercises HCF-finding, not a lucky "it's 1" guess.
    shared = random.randint(3, 8)
    k1, k2 = random.sample(range(2, 9), 2)
    h1, h2 = shared * k1, shared * k2
    while h1 > t["hcflcm_hi"] or h2 > t["hcflcm_hi"]:
        shared = random.randint(2, 6)
        k1, k2 = random.sample(range(2, 7), 2)
        h1, h2 = shared * k1, shared * k2
    want = "hcf" if sheet % 2 == 1 else "lcm"
    label = "HCF" if want == "hcf" else "LCM"
    items.append(q(f"Quick Review (Level 6): Find the {label} of {h1} and {h2}.", "fill", "Answer = ____"))

    return items


# ───────────────────────── Speed Calculation (toughened) ─────────────────────────

def _l7v3_speed_calc(sheet):
    """5 rapid whole-number arithmetic questions -- multiplication,
    division, and subtraction mixed, 2-3 digit numbers, escalating by
    sheet. Deliberately NOT fraction questions -- separate computational
    fluency practice, distinct from both the sheet's own topic and the
    Quick Review breadth-check above."""
    tiers = {
        1: {"mul_lo": 12, "mul_hi": 25, "div_hi": 9, "sub_lo": 100, "sub_hi": 400},
        2: {"mul_lo": 15, "mul_hi": 35, "div_hi": 12, "sub_lo": 200, "sub_hi": 600},
        3: {"mul_lo": 20, "mul_hi": 50, "div_hi": 15, "sub_lo": 300, "sub_hi": 800},
        4: {"mul_lo": 25, "mul_hi": 75, "div_hi": 18, "sub_lo": 400, "sub_hi": 999},
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
            b = random.randint(11, t["div_hi"] + 10)
            items.append(q(f"Speed Calculation: {a} x {b} = ____", "fill", "Answer = ____"))
        elif shape == "div":
            b = random.randint(2, t["div_hi"])
            k = random.randint(t["mul_lo"] // 2, t["mul_hi"])
            a = b * k
            items.append(q(f"Speed Calculation: {a} / {b} = ____", "fill", "Answer = ____"))
        else:  # sub3
            a = random.randint(t["sub_lo"], t["sub_hi"])
            b = random.randint(50, a - 20)
            items.append(q(f"Speed Calculation: {a} - {b} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── Block 1: sheet's own topic ─────────────────────────

_SOURCE_FN = {
    "7A": _L7._A_s, "7B": _L7._B_s, "7C": _L7._C_s, "7CUM1": _L7._CUM1_s,
    "7D": _L7._D_s, "7E": _L7._E_s, "7F": _L7._F_s, "7CUM2": _L7._CUM2_s,
    "7G": _L7._G_s, "7H": _L7._H_s, "7I": _L7._I_s, "7CUM3": _L7._CUM3_s,
    "7J": _L7._J_s, "7REV": _L7._REV_s,
}

_FALLBACK_DEN = {"7A": 8, "7B": 6, "7C": 12, "7CUM1": 8, "7D": 24, "7E": 12,
                  "7F": 6, "7CUM2": 12, "7G": 8, "7H": 6, "7I": 6, "7CUM3": 8,
                  "7J": 8, "7REV": 12}


def _synth_diagram_q(code, sheet, idx):
    """Synthesizes an extra diagram question for the rare sublevel/sheet
    that has fewer than 6 available (7B in particular has zero on sheet
    1) -- uses the same fraction_bar_blank diagram already used
    throughout this file, so it's a proven-safe, visually-consistent
    type, just with fresh numbers so it doesn't repeat anything already
    on the sheet.

    For 7B (Proper/improper/mixed) specifically, this is made
    topic-aware: alternates single-bar (proper, num<den, shades part of
    ONE whole) and multi-segment-bar (improper/mixed, num>=den, needs
    MORE than one whole) diagrams, so the picture actually teaches the
    proper-vs-improper distinction instead of generic unit-fraction
    shading."""
    den = _FALLBACK_DEN.get(code, 8) + idx
    if code == "7B":
        if idx % 2 == 0:
            num = random.randint(1, den - 1)
            return q(f"{num}/{den}: shade to show this fraction. Proper or improper?",
                      "diagram", "____", "", "fraction_bar_blank", {"den": den})
        else:
            whole = random.randint(1, 2)
            rem = random.randint(1, den - 1)
            num = whole * den + rem
            return q(f"{num}/{den}: shade to show this fraction. Proper or improper?",
                      "diagram", "____", "", "fraction_bar_blank", {"den": den, "segments": whole + 1})
    num = random.randint(1, den - 1)
    return q(f"{num}/{den} = ____ (shade and write)", "diagram", "____", "",
              "fraction_bar_blank", {"den": den})


def _item_key(item):
    return (item.get("text", ""), repr(item.get("diagram_params")))


_VISUAL_TYPES = ("fraction_bar_blank", "two_bars_blank", "fraction_numberline_blank",
                  "fraction_area_blank", "mixed_number_area_blank", "reciprocal_flip")


def _build_block1(code, sheet):
    items = _SOURCE_FN[code](sheet)
    concept_items = [x for x in items if x.get("type") in ("concept_box", "tips_box")]
    qs = [x for x in items if x.get("type") not in ("concept_box", "tips_box")]
    diagram_qs = [x for x in qs if x.get("diagram_type")]
    tail_qs = [x for x in qs if not x.get("diagram_type")]

    # Diagram slot selection is biased toward genuine concept-teaching
    # visuals (fraction bars, number lines, area models) over
    # procedural/testing diagram formats (matching_vertical_blank,
    # cross_multiply_bowtie) -- matching alone outnumbers every visual
    # type combined in the raw content, and would otherwise crowd out
    # the actual concept-teaching pictures if picked first-come-first-
    # served. Visual types fill the 6 slots first; matching/procedural
    # only backfills if fewer than 6 visuals exist.
    visual_qs = [x for x in diagram_qs if x.get("diagram_type") in _VISUAL_TYPES]
    block1a = list(visual_qs[:6])
    extra_idx = 0
    while len(block1a) < 6:
        block1a.append(_synth_diagram_q(code, sheet, extra_idx))
        extra_idx += 1

    # Adaptive tail selection: pick the 6 that best preserve format
    # variety while keeping total footprint modest, same principle as
    # the Level 6 rewrite -- sort by text length and take the shortest 6.
    tail_sorted = sorted(range(len(tail_qs)), key=lambda i: len(tail_qs[i].get("text", "")))
    block1b = [tail_qs[i] for i in tail_sorted[:6]] if tail_qs else []
    block1b.sort(key=lambda x: tail_qs.index(x))
    while len(block1b) < 6:
        block1b.append(_synth_diagram_q(code, sheet, 100 + len(block1b)))

    return concept_items, block1a, block1b


def build_v3_sheet(code, sheet):
    random.seed(7000 + hash(code) % 5000 + sheet * 31)
    concept_items, block1a, block1b = _build_block1(code, sheet)
    used = set()
    out = list(concept_items)
    for it in block1a + block1b:
        k = _item_key(it)
        if k in used:
            continue
        used.add(k)
        out.append(it)
    out += _l7v3_quick_review(sheet)
    out += _l7v3_speed_calc(sheet)
    return out


LEVEL7_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SOURCE_FN
}
