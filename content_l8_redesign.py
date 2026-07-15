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
        kind = i % 4
        if kind == 0:
            return q(f"Write the opposite of {v}. ____", "fill", "____")
        elif kind == 1:
            return q(f"Write the successor of {v} (the next integer). ____", "fill", "____")
        elif kind == 2:
            return q(f"Write the predecessor of {v} (the integer just before it). ____", "fill", "____")
        else:
            return q(f"Is {v} a Natural number, a Whole number, and/or an Integer? List ALL that apply. ____", "fill", "____")
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
        kind = i % 5
        a, b, c = random.randint(-hi, hi), random.randint(-hi, hi), random.randint(-hi, hi)
        if kind == 0:
            return q(f"({a}) + ({b}) = ____. Is the result always an integer? (This is the Closure Property.)", "fill", "____")
        elif kind == 1:
            return q(f"Verify: ({a}) + ({b}) = ({b}) + ({a})? Compute both sides. Which property does this show?", "fill", "____")
        elif kind == 2:
            return q(f"Verify: [({a})+({b})]+({c}) = ({a})+[({b})+({c})]? Compute both sides. Which property does this show?", "fill", "____")
        elif kind == 3:
            return q(f"({a}) + 0 = ____. Which property does this show? (Hint: 0 is the Additive Identity.)", "fill", "____")
        else:
            return q(f"Is ({a}) - ({b}) the same as ({b}) - ({a})? Compute both sides. Is subtraction of integers commutative?", "fill", "____")
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
        kind = (i + sheet) % 6
        a, b, c = random.randint(-hi, hi) or 1, random.randint(-hi, hi) or 1, random.randint(-hi, hi) or 1
        if kind == 0:
            return q(f"({a}) x ({b}) = ____. Is the result always an integer? (This is the Closure Property.)", "fill", "____")
        elif kind == 1:
            return q(f"Verify: ({a}) x ({b}) = ({b}) x ({a})? Compute both sides. Which property does this show?", "fill", "____")
        elif kind == 2:
            return q(f"Verify: [({a})x({b})]x({c}) = ({a})x[({b})x({c})]? Compute both sides. Which property does this show?", "fill", "____")
        elif kind == 3:
            return q(f"({a}) x 1 = ____. Which property does this show? (Hint: 1 is the Multiplicative Identity.)", "fill", "____")
        elif kind == 4:
            return q(f"Verify: ({a}) x [({b})+({c})] = ({a})x({b}) + ({a})x({c})? Compute both sides. Which property does this show?", "fill", "____")
        else:
            return q(f"Is ({a}) / ({b}) always an integer? Give an example where it is NOT. (Division does NOT satisfy the Closure Property.)", "fill", "____")
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
    lo, hi = _diff_range(sheet, base_lo=3, base_hi=10, step=2)
    def gen(sheet):
        return tuple(random.randint(lo, hi) * random.choice([1, -1]) for _ in range(4))
    def expr_and_answer(kind, sheet):
        a, b, c, d = gen(sheet)
        if a == 0: a = lo
        if b == 0: b = lo
        if c == 0: c = lo
        if d == 0: d = lo
        if kind == 0:
            return f"({a}) + ({b}) x ({c})", a + b*c
        elif kind == 1:
            return f"({a}) - ({b}) x ({c})", a - b*c
        elif kind == 2:
            return f"[({a}) + ({b})] x ({c})", (a+b)*c
        elif kind == 3:
            return f"({a}) x ({b}) + ({c}) x ({d})", a*b + c*d
        elif kind == 4:
            return f"({a}) + ({b}) - ({c}) x ({d})", a + b - c*d
        else:
            return f"[({a}) - ({b})] x [({c}) + ({d})]", (a-b)*(c+d)
    def comp(i, sheet):
        kind = (i + sheet) % 6
        expr, ans = expr_and_answer(kind, sheet)
        return q(f"{expr} = ____  (apply BODMAS)", "fill", "____")
    def tf(i, sheet):
        kind = (i + sheet + 1) % 6
        expr, ans = expr_and_answer(kind, sheet)
        shown = ans if random.random() > 0.4 else ans + random.choice([2, -2, 3, -3])
        return q(f"True or False: {expr} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b, c, d = gen(sheet)
        if a == 0: a = lo
        if b == 0: b = lo
        if c == 0: c = lo
        target = a + b*c
        return q(f"({a}) + ({b}) x ____ = {target}. Find the missing number (apply BODMAS).", "fill", "____")
    def numeral(i, sheet):
        kind = (i + sheet + 2) % 6
        expr, ans = expr_and_answer(kind, sheet)
        return q(f"Evaluate using BODMAS: {expr} = ____", "fill", "____")
    def multisel(i, sheet):
        a, b, c, _ = gen(sheet)
        if a == 0: a = lo
        if b == 0: b = lo
        if c == 0: c = lo
        left_to_right = (a + b) * c
        bodmas_order = a + b*c
        return q(f"For ({a}) + ({b}) x ({c}): Priya computed {left_to_right} (working left to right). "
                  f"Raj computed {bodmas_order} (using BODMAS order). Who is correct? ____ (Priya/Raj)", "fill", "____")
    def matching(i, sheet):
        exprs, anss = [], []
        for k in range(3):
            kind = (k + sheet) % 6
            e, ans = expr_and_answer(kind, sheet)
            exprs.append(e); anss.append(str(ans))
        shuffled = anss[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(exprs))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each expression to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "BODMAS / Order of Operations",
        ["Order: Brackets first, then Of (powers), then Division/Multiplication (left to right), then Addition/Subtraction (left to right).",
         "(-2) + (3) x (4) = (-2) + 12 = 10 -- multiply BEFORE adding, even with negative numbers."],
        "array_example", {"rows": 3, "cols": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching. This bridges into Level 9's multi-step factor/HCF-LCM problems.",
        fmt, sheet, seed_base=300)


# ───────────────────────── 8G: Word problems (rotated contexts) ─────────────────────────

def _G_s(sheet):
    lo, hi = _diff_range(sheet)
    def gen(sheet):
        return (random.randint(-hi, hi), random.randint(-hi, hi))
    def word_problem(i, sheet):
        """Returns (text, answer). Cycles through 6 word-problem kinds so
        8G exercises all four operations in real contexts -- the original
        3 kinds only ever did single-step +/- across 3 nouns. Kinds 3-5
        add a multiplication-rate context, a fair-share division context,
        and a genuine 2-step chain."""
        kind = (i + sheet) % 6
        if kind == 0:
            a, b = gen(sheet)
            return f"Temperature was {a} degrees, then changed by {b} degrees. Now it is ____.", a + b
        elif kind == 1:
            a, b = gen(sheet)
            return f"A diver was at {a} m (sea level=0), then moved {b} m. Now at ____.", a + b
        elif kind == 2:
            a, b = gen(sheet)
            return f"An account had ${a}, then a transaction of ${b}. New balance: ____.", a + b
        elif kind == 3:
            r = random.choice([x for x in range(-hi, hi + 1) if x != 0])
            h = random.randint(2, 5)
            return f"Temperature changes by {r} degrees every hour, for {h} hours in a row. Total change = ____.", r * h
        elif kind == 4:
            n = random.choice([2, 3, 4, 5, 6])
            per = random.randint(1, max(hi, 2))
            return f"A total debt of ${per*n} is shared equally among {n} people. Each person's share = ____.", -per
        else:
            a, b, c = random.randint(-hi, hi), random.randint(-hi, hi), random.randint(-hi, hi)
            return f"Started at {a}, changed by {b}, then changed again by {c}. Now at ____.", a + b + c
    def comp(i, sheet):
        txt, ans = word_problem(i, sheet)
        return q(txt, "diagram", "____", "", "vertical_numberline_blank", {"lo": min(0, ans) - 5, "hi": max(0, ans) + 5})
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
        txt, ans = word_problem(i, sheet)
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
    lo, hi = _diff_range(sheet, base_lo=20, base_hi=100, step=20)
    DIVS = [2, 3, 4, 5, 6, 8, 9, 10, 11]
    def gen(sheet):
        n = random.randint(-hi, hi)
        if n == 0: n = hi
        d = random.choice(DIVS)
        return n, d
    def comp(i, sheet):
        n, d = gen(sheet)
        return q(f"Is {n} divisible by {d}? Use the divisibility rule for {d} to decide.", "fill", "____ (Yes/No)")
    def tf(i, sheet):
        n, d = gen(sheet)
        actual = "Yes" if n % d == 0 else "No"
        wrong = "No" if actual == "Yes" else "Yes"
        shown = actual if random.random() > 0.4 else wrong
        return q(f"True or False: {n} is divisible by {d} — {shown}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        n = random.randint(-hi, hi)
        if n == 0: n = hi
        dv = random.choice(DIVS)
        return q(f"What is the smallest number GREATER than {n} that IS divisible by {dv}? ____", "fill", "____")
    def numeral(i, sheet):
        n, d = gen(sheet)
        return q(f"Is {n} divisible by {d}? Answer Yes or No. ____", "fill", "____")
    def multisel(i, sheet):
        n = random.randint(max(lo, 12), hi)
        candidates = random.sample(DIVS, 4)
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(candidates))
        return q(f"Which of these numbers is {n} divisible by? Select ALL that apply: {opts_str}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(random.randint(lo, hi), random.choice(DIVS)) for _ in range(3)]
        lefts = [f"{n} by {d}" for n, d in pairs]
        rights = ["Yes" if n % d == 0 else "No" for n, d in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each check to Yes/No: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Divisibility Rules",
        ["2: last digit even. 3: digit sum divisible by 3. 4: last 2 digits divisible by 4.",
         "5: ends in 0 or 5. 6: divisible by BOTH 2 and 3. 8: last 3 digits divisible by 8.",
         "9: digit sum divisible by 9. 10: ends in 0. 11: alternating digit sum divisible by 11.",
         "The sign of the number doesn't matter -- check the digits the same way."],
        "array_example", {"rows": 4, "cols": 5},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching. This bridges into Level 9 (Factors & HCF/LCM).",
        fmt, sheet, seed_base=400)


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
    lo, hi = _diff_range(sheet, base_lo=10, base_hi=70, step=15)
    def is_prime(n):
        n = abs(n)
        if n < 2: return False
        for k in range(2, int(n**0.5) + 1):
            if n % k == 0: return False
        return True
    def comp(i, sheet):
        n = random.randint(max(lo, 2), hi)
        return q(f"Is {n} a PRIME number or a COMPOSITE number? Show your working.  [1 point]", "fill", "____ (Prime/Composite)")
    def tf(i, sheet):
        n = random.randint(max(lo, 2), hi)
        actual = "Prime" if is_prime(n) else "Composite"
        wrong = "Composite" if actual == "Prime" else "Prime"
        shown = actual if random.random() > 0.4 else wrong
        return q(f"True or False: {n} is {shown}.  [1 point]", "fill", "____ (True/False)")
    def missing(i, sheet):
        n = random.randint(-hi, hi)
        if n == 0: n = hi
        return q(f"|{n}| = ____  (absolute value = distance from 0)  [2 points]", "fill", "____")
    def numeral(i, sheet):
        n = random.choice([-1, 1]) * random.randint(max(lo, 2), hi)
        extra = random.randint(2, 9)
        return q(f"Find |{n}| + {extra}.  [2 points]", "fill", "____")
    def multisel(i, sheet):
        nums = random.sample(range(max(lo, 2), hi), 4)
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(nums))
        return q(f"Which of these are PRIME numbers? Select ALL that apply: {opts_str}  [2 points]",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        vals = [random.choice([-1, 1]) * random.randint(max(lo, 2), hi) for _ in range(3)]
        lefts = [f"|{v}|" for v in vals]; rights = [str(abs(v)) for v in vals]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its absolute value: {left_str}  to  {right_str}  [2 points]", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    items = _make_rotated_sheet(
        "Prime & Composite + Absolute Value",
        ["Speed challenge: each question has a point value. Add up your own score at the end!",
         "A PRIME number has exactly 2 factors: 1 and itself. A COMPOSITE number has more than 2 factors.",
         "|x| (absolute value) = distance from 0 on the number line -- always positive or zero.",
         "Bronze: 20+ points. Silver: 30+ points. Gold: 38+ points (all correct)."],
        "vertical_numberline_example", {"value": -13, "lo": -20, "hi": 20},
        "Formats rotate each sheet. Solve each question, then add up your points (shown in brackets). This bridges into Level 9 (Factors & Prime Factorisation).",
        fmt, sheet, seed_base=500)
    items.append(tb("Your Score", ["My total score: _____.  My badge: Bronze / Silver / Gold (circle one)"]))
    return items


def _REV_s(sheet):
    lo, hi = _diff_range(sheet, base_lo=8, base_hi=25, step=8)
    def comp(i, sheet):
        a, b = random.randint(-hi, hi), random.randint(-hi, hi)
        op = random.choice(["+", "-"])
        return q(f"({a}) {op} ({b}) = ____", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a, b)-5, "hi": max(a, b)+5})
    def tf(i, sheet):
        a, b = random.randint(lo, hi), random.randint(lo, hi)
        if i == 0:
            correct_prop = random.choice(["Commutative", "Associative", "Closure", "Distributive"])
            wrong_prop = random.choice([p for p in ["Commutative", "Associative", "Closure", "Distributive"] if p != correct_prop])
            shown_prop = correct_prop if random.random() > 0.4 else wrong_prop
            examples = {
                "Commutative": f"({a}) + ({b}) = ({b}) + ({a})",
                "Associative": f"[({a})+({b})]+(2) = ({a})+[({b})+(2)]",
                "Closure": f"({a}) - ({b}) is always an integer",
                "Distributive": f"({a}) x [({b})+(2)] = ({a})x({b}) + ({a})x(2)",
            }
            return q(f"True or False: '{examples[correct_prop]}' is an example of the {shown_prop} Property.", "fill", "____ (True/False)")
        correct = a*b
        shown = correct if random.random() > 0.4 else -correct
        return q(f"True or False: (-{a}) x (-{b}) = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        kind = i % 4
        if kind == 0:
            a = random.randint(-hi, hi); t = random.randint(-hi, hi)
            return q(f"({a}) + ____ = {t}", "diagram", "____", "", "vertical_numberline_blank", {"lo": min(a, t)-3, "hi": max(a, t)+3})
        elif kind == 1:
            n = random.randint(-hi, hi)
            if n == 0: n = hi
            dv = random.choice([2, 3, 4, 5, 6, 8, 9, 10, 11])
            return q(f"What is the smallest number GREATER than {n} that IS divisible by {dv}? ____", "fill", "____")
        elif kind == 2:
            a, b, c = random.randint(-hi, hi) or 1, random.randint(-hi, hi) or 1, random.randint(2, 9)
            target = a + b*c
            return q(f"({a}) + ({b}) x ____ = {target}. Find the missing number (apply BODMAS).", "fill", "____")
        else:
            n = random.randint(-hi, hi)
            if n == 0: n = hi
            return q(f"|{n}| = ____  (absolute value)", "fill", "____")
    def numeral(i, sheet):
        kind = i % 4
        if kind == 0:
            a, b = random.randint(-hi, hi), random.randint(-hi, hi) or 1
            op = random.choice(["+", "-", "x"])
            return q(f"({a}) {op} ({b}) = ____", "fill", "____")
        elif kind == 1:
            n = random.randint(max(lo, 2), hi)
            return q(f"Is {n} PRIME or COMPOSITE?", "fill", "____ (Prime/Composite)")
        elif kind == 2:
            a, b, c = random.randint(lo, hi), random.randint(lo, hi), random.randint(lo, hi)
            return q(f"({a}) - ({b}) x ({c}) = ____  (apply BODMAS)", "fill", "____")
        else:
            n = random.randint(-hi, hi)
            if n == 0: n = hi
            dv = random.choice([2, 3, 4, 5, 6, 8, 9, 10, 11])
            return q(f"Is {n} divisible by {dv}? Answer Yes or No.", "fill", "____")
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
        ["Every integer skill: concept, ordering, the four operations, properties, divisibility, BODMAS, primes, absolute value, word problems, and puzzles."],
        "vertical_numberline_example", {"value": 2, "lo": -10, "hi": 10},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=900)


# ───────────────────────── Dispatcher (REPLACES original Level 8) ─────────────────────────

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL8_DISPATCH = {
    "8A": _wrap(_A_s), "8B": _wrap(_B_s), "8C": _wrap(_C_s), "8CUM1": _wrap(_CUM1_s),
    "8D": _wrap(_D_s), "8E": _wrap(_E_s), "8F": _wrap(_F_s), "8CUM2": _wrap(_CUM2_s),
    "8G": _wrap(_G_s), "8H": _wrap(_CUM3_s), "8I": _wrap(_I_s), "8CUM3": _wrap(_H_s),
    "8J": _wrap(_J_s), "8REV": _wrap(_REV_s),
}
