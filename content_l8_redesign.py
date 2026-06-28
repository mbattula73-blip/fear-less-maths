"""
Fear Less Maths — LEVEL 8 REDESIGN v2 (Integers, Grade 6-7)

Replaces the original Level 8 in place, reusing the EXACT same 14
sub-level codes (8A-8J, 8CUM1-3, 8REV) so the existing rich "Concept &
Tips" study pages (concept_pages.py) stay untouched and correctly
matched to their topics.

v2 fixes the "same worksheet for every sheet" problem: each sub-level
now has 6 question-format builders (computation, True/False,
missing-number, numeral, multi-select, matching) and 4 SHEET TEMPLATES,
each picking a different combination/order of 4 of those 6 formats.
Sheet 1-4 of the same sub-level therefore look genuinely different from
each other, not the same shape with new numbers -- and difficulty
(number range/sign variety) increases slightly sheet to sheet.
"""
import random
from content import cb, tb, q
from question_formats import TEMPLATES, diff_range as _diff_range, make_rotated_sheet as _make_rotated_sheet, make_format_builders

CONTEXTS = [
    ("temperature", "The temperature is {v} degrees."),
    ("elevation", "A point is at {v} m relative to sea level."),
    ("money", "An account balance is {v} dollars (negative = owed)."),
    ("charge", "An electric charge reads {v}."),
]


# ───────────────────────── 8A: Integer concept ─────────────────────────

def _A_s(sheet):
    lo, hi = _diff_range(sheet)
    def gen(sheet):
        v = random.choice([x for x in range(-hi-3, hi+4) if abs(x) >= lo])
        return (v, 0)
    def comp(i, sheet):
        v, _ = gen(sheet)
        ctx, template = CONTEXTS[i % len(CONTEXTS)]
        return q(f"{template.format(v=v)} Mark it on the number line.", "diagram", "____",
                  "", "vertical_numberline_blank", {"lo": -hi-5, "hi": hi+5})
    def tf(i, sheet):
        v, _ = gen(sheet)
        shown_sign = random.choice([True, False])
        word = "below" if v < 0 else "above"
        wrong_word = "above" if v < 0 else "below"
        return q(f"True or False: {v} is {word if shown_sign else wrong_word} zero.", "fill", "____ (True/False)")
    def missing(i, sheet):
        v, _ = gen(sheet)
        return q(f"The opposite of {v} is ____.", "diagram", "____", "", "vertical_numberline_blank", {"lo": -hi-5, "hi": hi+5})
    def numeral(i, sheet):
        v, _ = gen(sheet)
        return q(f"Write the opposite of {v}. ____", "fill", "____")
    def multisel(i, sheet):
        v, _ = gen(sheet)
        opts = [str(-v), str(v), str(-v+1), str(v-1)]
        return q(f"Which of these is the opposite of {v}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        vals = [gen(sheet)[0] for _ in range(3)]
        lefts = [str(v) for v in vals]
        rights = [str(-v) for v in vals]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each number to its opposite: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Worked Example",
        ["Real situations use integers: temperature, elevation, money owed, electric charge.",
         "-5 degrees means 5 below zero. +5 m means 5 above sea level."],
        "vertical_numberline_example", {"value": -5, "lo": -10, "hi": 10},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=10)


# ───────────────────────── 8B: Number line / ordering ─────────────────────────

def _B_s(sheet):
    lo, hi = _diff_range(sheet)
    def gen(sheet):
        return tuple(random.sample(range(-hi-2, hi+3), 2))
    def comp(i, sheet):
        v = random.randint(-hi-2, hi+2)
        return q(f"Mark {v} on the number line.", "diagram", "____", "", "vertical_numberline_blank", {"lo": -hi-5, "hi": hi+5})
    def tf(i, sheet):
        a, b = gen(sheet)
        claim_true = a > b
        show_correct = random.random() > 0.4
        stmt_a, stmt_b = (a, b) if (claim_true == show_correct) else (b, a)
        return q(f"True or False: {stmt_a} > {stmt_b}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b = sorted(gen(sheet))
        return q(f"{a} < ____ < {b}  (give one number that fits)", "diagram", "____",
                  "", "vertical_numberline_blank", {"lo": a-3, "hi": b+3})
    def numeral(i, sheet):
        a, b = gen(sheet)
        return q(f"{a} ___ {b}  (>, < or =)", "fill", "____")
    def multisel(i, sheet):
        base = random.randint(-hi, hi)
        opts = [base+1, base-1, base+5, base-5]
        return q(f"Which of these are greater than {base}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        vals = [random.randint(-hi-2, hi+2) for _ in range(3)]
        lefts = [str(v) for v in vals]
        rights = [("positive" if v > 0 else ("negative" if v < 0 else "zero")) for v in vals]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each number to its type: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Worked Example",
        ["On a vertical number line, UP is bigger, DOWN is smaller.", "-3 is above -7, so -3 > -7."],
        "vertical_numberline_example", {"value": -3, "lo": -10, "hi": 10},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=20)


# ───────────────────────── 8C: Addition (zero pairs) ─────────────────────────

def _C_s(sheet):
    lo, hi = _diff_range(sheet)
    def gen(sheet):
        return (-random.randint(lo, hi), random.randint(lo, hi))
    fmt = make_format_builders(
        gen, "integer_chips_blank", lambda a, b: {"pos": abs(b), "neg": abs(a)}, "+", lambda a, b: a+b,
        missing_diagram_fn="vertical_numberline_blank",
        missing_params_fn=lambda a, b: {"lo": min(a, a+b)-3, "hi": max(a, a+b)+3})
    return _make_rotated_sheet(
        "Worked Example",
        ["Discover the Zero Pair Rule: a (+) and a (-) together cancel out -- a ZERO PAIR.",
         "Whatever is left over (no partner) gives the answer."],
        "integer_chips_example", {"pos": 5, "neg": 3},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=30)


# ───────────────────────── 8D: Subtraction (Keep-Change-Change) ─────────────────────────

def _D_s(sheet):
    lo, hi = _diff_range(sheet)
    def gen(sheet):
        return (random.randint(-hi, hi), random.randint(lo, hi))
    fmt = make_format_builders(
        gen, "vertical_numberline_blank", lambda a, b: {"lo": a-b-3, "hi": a+3}, "-", lambda a, b: a-b)
    return _make_rotated_sheet(
        "Worked Example",
        ["Keep, Change, Change: KEEP the first number, CHANGE subtraction to addition, CHANGE the sign of the second number.",
         "(-3) - (5) becomes (-3) + (-5) = -8."],
        "vertical_numberline_example", {"value": -8, "lo": -12, "hi": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=40)


def _CUM1_s(sheet):
    lo, hi = _diff_range(sheet)
    def gen(sheet):
        op = random.choice(["+", "-"])
        a = random.randint(-hi, hi); b = random.randint(lo, hi)
        return (a, b if op == "+" else b)
    def comp(i, sheet):
        op = random.choice(["+", "-"]); a = random.randint(-hi, hi); b = random.randint(lo, hi)
        return q(f"({a}) {op} ({b}) = ____", "diagram", "____", "", "vertical_numberline_blank", {"lo": a-b-3, "hi": a+b+3})
    def tf(i, sheet):
        a, b = random.randint(-hi, hi), random.randint(lo, hi)
        op = random.choice(["+", "-"]); correct = a+b if op == "+" else a-b
        shown = correct if random.random() > 0.4 else correct+2
        return q(f"True or False: ({a}) {op} ({b}) = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a = random.randint(-hi, hi); t = random.randint(-hi, hi)
        return q(f"({a}) + ____ = {t}", "diagram", "____", "", "vertical_numberline_blank", {"lo": min(a, t)-3, "hi": max(a, t)+3})
    def numeral(i, sheet):
        a, b = random.randint(-hi, hi), random.randint(-hi, hi)
        return q(f"({a}) {random.choice(['+','-'])} ({b}) = ____", "fill", "____")
    def multisel(i, sheet):
        target = random.randint(-hi, hi)
        opts = [f"({target-2})+({2})", f"({target})+({0})", f"({target+3})+({-3})", f"({target+1})+({-2})"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(random.randint(-hi, hi), random.randint(lo, hi)) for _ in range(3)]
        lefts = [f"({a})+({b})" for a, b in pairs]; rights = [str(a+b) for a, b in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Review", ["Mix of concept, ordering, and addition/subtraction."],
        "integer_chips_example", {"pos": 5, "neg": 3},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=100)


def _CUM2_s(sheet):
    lo, hi = _diff_range(sheet)
    def gen(sheet):
        op = random.choice(["+", "-"]); a = random.randint(-hi, hi); b = random.randint(lo, hi)
        return (a, b)
    def comp(i, sheet):
        op = random.choice(["+", "-"]); a = random.randint(-hi, hi); b = random.randint(lo, hi)
        return q(f"({a}) {op} ({b}) = ____", "diagram", "____", "", "vertical_numberline_blank", {"lo": a-b-3, "hi": a+b+3})
    def tf(i, sheet):
        a, b = random.randint(-hi, hi), random.randint(lo, hi)
        op = random.choice(["+", "-"]); correct = a+b if op == "+" else a-b
        shown = correct if random.random() > 0.4 else correct+2
        return q(f"True or False: ({a}) {op} ({b}) = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a = random.randint(-hi, hi); t = random.randint(-hi, hi)
        op = random.choice(["+", "-"])
        return q(f"({a}) {op} ____ = {t}", "diagram", "____", "", "vertical_numberline_blank", {"lo": min(a, t)-3, "hi": max(a, t)+3})
    def numeral(i, sheet):
        a, b = random.randint(-hi, hi), random.randint(-hi, hi)
        return q(f"({a}) {random.choice(['+','-'])} ({b}) = ____", "fill", "____")
    def multisel(i, sheet):
        target = random.randint(-hi, hi)
        opts = [f"({target-2})-({-2})", f"({target})-({0})", f"({target+3})-({3})", f"({target+1})-({2})"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(random.randint(-hi, hi), random.randint(lo, hi)) for _ in range(3)]
        lefts = [f"({a})-({b})" for a, b in pairs]; rights = [str(a-b) for a, b in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Review", ["Mix of multiplying and dividing integers (from D/E/F)."],
        "vertical_numberline_example", {"value": -8, "lo": -12, "hi": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=200)


# ───────────────────────── 8E: Multiplication (discover the sign rule) ─────────────────────────

def _E_s(sheet):
    lo, hi = _diff_range(sheet)
    def gen(sheet):
        return (random.randint(lo, hi), random.randint(lo, hi))
    def comp(i, sheet):
        a, b = gen(sheet)
        signs = random.choice([("", ""), ("", "-"), ("-", ""), ("-", "-")])
        return q(f"({signs[0]}{a}) x ({signs[1]}{b}) = ____", "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
    def tf(i, sheet):
        a, b = gen(sheet)
        correct = a*b
        shown = -correct if random.random() > 0.4 else correct
        return q(f"True or False: (-{a}) x (-{b}) = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b = gen(sheet)
        return q(f"(-{a}) x ____ = {-(a*b)}", "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
    def numeral(i, sheet):
        a, b = gen(sheet)
        signs = random.choice([("", ""), ("", "-"), ("-", ""), ("-", "-")])
        return q(f"({signs[0]}{a}) x ({signs[1]}{b}) = ____", "fill", "____")
    def multisel(i, sheet):
        a, b = gen(sheet)
        target = a*b
        opts = [f"(-{a})x(-{b})", f"({a})x(-{b})", f"(-{a})x({b})", f"({a})x({b})"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"(-{a})x(-{b})" for a, b in pairs]; rights = [str(a*b) for a, b in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Worked Example",
        ["Discover the Sign Rule. Pattern: 3x2=6, 3x1=3, 3x0=0, 3x(-1)=?, 3x(-2)=? What rule do you notice?",
         "Same signs give POSITIVE. Different signs give NEGATIVE."],
        "array_example", {"rows": 3, "cols": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=50)


# ───────────────────────── 8F: Division (fact families) ─────────────────────────

def _F_s(sheet):
    lo, hi = _diff_range(sheet)
    def gen(sheet):
        return (random.randint(lo, hi), random.randint(lo, hi))
    def comp(i, sheet):
        a, b = gen(sheet)
        product = a*b
        signs = random.choice([("", ""), ("", "-"), ("-", ""), ("-", "-")])
        return q(f"({signs[0]}{product}) / ({signs[1]}{a}) = ____", "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
    def tf(i, sheet):
        a, b = gen(sheet)
        product = a*b
        correct = b
        shown = correct if random.random() > 0.4 else -correct
        return q(f"True or False: (-{product}) / (-{a}) = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b = gen(sheet)
        product = a*b
        return q(f"(-{product}) / ____ = {b}", "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
    def numeral(i, sheet):
        a, b = gen(sheet)
        product = a*b
        signs = random.choice([("", ""), ("", "-"), ("-", ""), ("-", "-")])
        return q(f"({signs[0]}{product}) / ({signs[1]}{a}) = ____", "fill", "____")
    def multisel(i, sheet):
        a, b = gen(sheet)
        product = a*b
        target = b
        opts = [f"(-{product})/(-{a})", f"({product})/(-{a})", f"(-{product})/({a})", f"({product})/({a})"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"(-{a*b})/(-{a})" for a, b in pairs]; rights = [str(b) for a, b in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Worked Example",
        ["Division follows the SAME sign rule as multiplication.",
         "(-12)/(-3)=4 (same signs->positive). (-12)/3=-4 (different signs->negative)."],
        "array_example", {"rows": 3, "cols": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=60)


def _CUM3_s(sheet):
    lo, hi = _diff_range(sheet)
    def gen(sheet):
        return (random.randint(lo, hi), random.randint(lo, hi))
    def comp(i, sheet):
        a, b = gen(sheet)
        signs = random.choice([("", ""), ("", "-"), ("-", ""), ("-", "-")])
        if i % 2 == 0:
            return q(f"({signs[0]}{a}) x ({signs[1]}{b}) = ____", "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
        product = a*b
        return q(f"({signs[0]}{product}) / ({signs[1]}{a}) = ____", "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
    def tf(i, sheet):
        a, b = gen(sheet)
        return q(f"True or False: (-{a}) x (-{b}) = {a*b}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b = gen(sheet)
        return q(f"(-{a}) x ____ = {-(a*b)}", "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
    def numeral(i, sheet):
        a, b = gen(sheet)
        op = random.choice(["x", "/"])
        if op == "/": a = a*b
        return q(f"(-{a}) {op} ({b}) = ____", "fill", "____")
    def multisel(i, sheet):
        a, b = gen(sheet)
        target = a*b
        opts = [f"(-{a})x(-{b})", f"({a})x(-{b})", f"(-{a})x({b})", f"({a})x({b})"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"(-{a})x(-{b})" for a, b in pairs]; rights = [str(a*b) for a, b in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Review", ["Mix of multiplying and dividing integers."],
        "array_example", {"rows": 3, "cols": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=300)


# ───────────────────────── 8G: Word problems (rotated contexts) ─────────────────────────

def _G_s(sheet):
    lo, hi = _diff_range(sheet)
    templates = [
        "Temperature was {a} degrees, then changed by {b} degrees. Now it is ____.",
        "A diver was at {a} m (sea level=0), then moved {b} m. Now at ____.",
        "An account had ${a}, then a transaction of ${b}. New balance: ____.",
    ]
    def gen(sheet):
        return (random.randint(-hi, hi), random.randint(-hi, hi))
    def comp(i, sheet):
        a, b = gen(sheet)
        txt = templates[i % len(templates)].format(a=a, b=b)
        return q(txt, "diagram", "____", "", "vertical_numberline_blank", {"lo": min(a, a+b)-3, "hi": max(a, a+b)+3})
    def tf(i, sheet):
        a, b = gen(sheet)
        correct = a+b
        shown = correct if random.random() > 0.4 else correct+2
        return q(f"True or False: starting at {a} and changing by {b} gives {shown}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        a = random.randint(-hi, hi); final = random.randint(-hi, hi)
        return q(f"Started at {a}, ended at {final}. The change was ____.", "diagram", "____",
                  "", "vertical_numberline_blank", {"lo": min(a, final)-3, "hi": max(a, final)+3})
    def numeral(i, sheet):
        a, b = gen(sheet)
        txt = templates[i % len(templates)].format(a=a, b=b)
        return q(txt, "fill", "____")
    def multisel(i, sheet):
        target = random.randint(-hi, hi)
        opts = [f"start {target-2}, change +2", f"start {target}, change +0", f"start {target+3}, change -3", f"start {target+1}, change -2"]
        return q(f"Which give a final value of {target}? Select ALL: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"start {a}, change {b}" for a, b in pairs]; rights = [str(a+b) for a, b in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each to its final value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Worked Example",
        ["Picture real situations: temperature, elevation, money, charge.",
         "Started at -3, changed by 5: -3 + 5 = 2."],
        "vertical_numberline_example", {"value": 2, "lo": -10, "hi": 10},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=70)


# ───────────────────────── 8H: Mixed integers ─────────────────────────

def _H_s(sheet):
    lo, hi = _diff_range(sheet)
    def gen(sheet):
        return (random.randint(-hi, hi), random.randint(-hi, hi))
    def comp(i, sheet):
        a, b = gen(sheet)
        op = random.choice(["+", "-"])
        return q(f"({a}) {op} ({b}) = ____", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a, b, a+b, a-b)-3, "hi": max(a, b, a+b, a-b)+3})
    def tf(i, sheet):
        a, b = gen(sheet)
        op = random.choice(["+", "-"])
        correct = a+b if op == "+" else a-b
        shown = correct if random.random() > 0.4 else correct+3
        return q(f"True or False: ({a}) {op} ({b}) = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a = random.randint(-hi, hi); t = random.randint(-hi, hi)
        op = random.choice(["+", "-"])
        return q(f"({a}) {op} ____ = {t}", "diagram", "____", "", "vertical_numberline_blank", {"lo": min(a, t)-3, "hi": max(a, t)+3})
    def numeral(i, sheet):
        a, b = gen(sheet)
        op = random.choice(["+", "-", "x"])
        return q(f"({a}) {op} ({b}) = ____", "fill", "____")
    def multisel(i, sheet):
        target = random.randint(-hi, hi)
        opts = [f"({target-2})+(2)", f"({target+1})-(1)", f"({target})+(0)", f"({target+4})-(4)"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        ops = [random.choice(["+", "-"]) for _ in range(3)]
        lefts = [f"({a}){op}({b})" for (a, b), op in zip(pairs, ops)]
        rights = [str(a+b if op == "+" else a-b) for (a, b), op in zip(pairs, ops)]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Worked Example", ["Check the operation symbol first, then use the right strategy."],
        "vertical_numberline_example", {"value": 2, "lo": -10, "hi": 10},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=80)


# ───────────────────────── 8I: Puzzles (magic squares + patterns) ─────────────────────────

def _I_s(sheet):
    lo, hi = _diff_range(sheet)
    def comp(i, sheet):
        start = random.randint(-hi, 5); step = random.choice([-3, -2, 2, 3])
        seq = [start, start+step, start+2*step]
        return q(f"{seq[0]}, {seq[1]}, {seq[2]}, ____  (continue the pattern)", "diagram", "____",
                  "", "vertical_numberline_blank", {"lo": min(seq)-5, "hi": max(seq)+5})
    def tf(i, sheet):
        a, b, c = random.randint(-hi, hi), random.randint(-hi, hi), random.randint(-hi, hi)
        claim = a+b+c
        shown = claim if random.random() > 0.4 else claim+1
        return q(f"True or False: {a} + {b} + {c} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        center = random.randint(-5, 5)
        given = {(0, 0): center-1, (1, 1): center, (2, 2): center+1}
        total = 3*center
        return q(f"Magic square: every row/col/diagonal sums to {total}. Fill in the rest.",
                  "diagram", "____", "", "magic_square_blank", {"size": 3, "given": given})
    def numeral(i, sheet):
        a = random.randint(-hi, hi)
        return q(f"I am the opposite of the opposite of {a}. What number am I? ____", "fill", "____")
    def multisel(i, sheet):
        step = random.choice([2, 3])
        start = random.randint(-hi, 5)
        seq_next = start + 3*step
        opts = [seq_next, seq_next+1, seq_next-step, seq_next+step]
        return q(f"The pattern {start},{start+step},{start+2*step},___ continues with which values? Select ALL valid next terms: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        starts = [random.randint(-hi, 5) for _ in range(3)]
        steps = [random.choice([2, 3, -2]) for _ in range(3)]
        lefts = [f"{s},{s+st},{s+2*st},___" for s, st in zip(starts, steps)]
        rights = [str(s+3*st) for s, st in zip(starts, steps)]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each pattern to its next term: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Worked Example",
        ["A magic square: every row, column, and diagonal adds to the SAME total.",
         "Use the given numbers to work out the pattern, then fill in the rest."],
        "magic_square_blank", {"size": 3, "given": {(0, 0): -1, (1, 1): 0, (2, 2): 1}},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=90)


# ───────────────────────── 8J: Mixed challenge (self-scored speed) ─────────────────────────

def _J_s(sheet):
    lo, hi = _diff_range(sheet)
    def comp(i, sheet):
        a, b = random.randint(-hi, hi), random.randint(-hi, hi)
        op = random.choice(["+", "-"])
        return q(f"({a}) {op} ({b}) = ____  [1 point]", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a, b)-5, "hi": max(a, b)+5})
    def tf(i, sheet):
        a, b = random.randint(lo, hi), random.randint(lo, hi)
        correct = a*b
        shown = correct if random.random() > 0.4 else -correct
        return q(f"True or False: (-{a}) x (-{b}) = {shown}  [1 point]", "fill", "____ (True/False)")
    def missing(i, sheet):
        a = random.randint(-hi, hi); t = random.randint(-hi, hi)
        return q(f"({a}) + ____ = {t}  [2 points]", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a, t)-3, "hi": max(a, t)+3})
    def numeral(i, sheet):
        a, b = random.randint(-hi, hi), random.randint(-hi, hi)
        op = random.choice(["+", "-", "x"])
        return q(f"({a}) {op} ({b}) = ____  [2 points]", "fill", "____")
    def multisel(i, sheet):
        target = random.randint(-hi, hi)
        opts = [f"({target-2})+(2)", f"({target})+(0)", f"({target+3})-(3)", f"({target+1})-(2)"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}  [2 points]",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(random.randint(-hi, hi), random.randint(-hi, hi)) for _ in range(3)]
        lefts = [f"({a})+({b})" for a, b in pairs]; rights = [str(a+b) for a, b in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}  [2 points]", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    items = _make_rotated_sheet(
        "Worked Example",
        ["Speed challenge: each question has a point value. Add up your own score at the end!",
         "Bronze: 20+ points. Silver: 30+ points. Gold: 38+ points (all correct)."],
        "vertical_numberline_example", {"value": 2, "lo": -10, "hi": 10},
        "Formats rotate each sheet. Solve each question, then add up your points (shown in brackets).",
        fmt, sheet, seed_base=110)
    items.append(tb("Your Score", ["My total score: _____.  My badge: Bronze / Silver / Gold (circle one)"]))
    return items


def _REV_s(sheet):
    lo, hi = _diff_range(sheet)
    def comp(i, sheet):
        a, b = random.randint(-hi, hi), random.randint(-hi, hi)
        op = random.choice(["+", "-"])
        return q(f"({a}) {op} ({b}) = ____", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a, b)-5, "hi": max(a, b)+5})
    def tf(i, sheet):
        a, b = random.randint(lo, hi), random.randint(lo, hi)
        correct = a*b
        shown = correct if random.random() > 0.4 else -correct
        return q(f"True or False: (-{a}) x (-{b}) = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a = random.randint(-hi, hi); t = random.randint(-hi, hi)
        return q(f"({a}) + ____ = {t}", "diagram", "____", "", "vertical_numberline_blank", {"lo": min(a, t)-3, "hi": max(a, t)+3})
    def numeral(i, sheet):
        a, b = random.randint(-hi, hi), random.randint(-hi, hi) or 1
        op = random.choice(["+", "-", "x"])
        return q(f"({a}) {op} ({b}) = ____", "fill", "____")
    def multisel(i, sheet):
        target = random.randint(-hi, hi)
        opts = [f"({target-2})+(2)", f"({target})+(0)", f"({target+3})-(3)", f"({target+1})-(2)"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(random.randint(-hi, hi), random.randint(-hi, hi)) for _ in range(3)]
        lefts = [f"({a})+({b})" for a, b in pairs]; rights = [str(a+b) for a, b in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Level 8 Revision",
        ["Every integer skill: concept, ordering, the four operations, word problems, and puzzles."],
        "vertical_numberline_example", {"value": 2, "lo": -10, "hi": 10},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=900)


# ───────────────────────── Dispatcher (REPLACES original Level 8) ─────────────────────────

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL8_DISPATCH = {
    "8A": _wrap(_A_s), "8B": _wrap(_B_s), "8C": _wrap(_C_s), "8CUM1": _wrap(_CUM1_s),
    "8D": _wrap(_D_s), "8E": _wrap(_E_s), "8F": _wrap(_F_s), "8CUM2": _wrap(_CUM2_s),
    "8G": _wrap(_G_s), "8H": _wrap(_H_s), "8I": _wrap(_I_s), "8CUM3": _wrap(_CUM3_s),
    "8J": _wrap(_J_s), "8REV": _wrap(_REV_s),
}
