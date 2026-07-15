"""
Fear Less Maths — LEVEL 8 REDESIGN v3 (Integers + Percentages, Grade 6-8)

Level 8 is split into two halves, 7 sublevels each, sharing the same
14-slot structure so nothing else in the app needs to change:
  8A-8G: Integers (condensed from the old 14-sublevel version -- merges
         removed the "generic mixed review" redundancy; each of these 7
         now has a distinct identity, several combining two old topics).
  8H-8N: Percentages (new content -- concept, of-a-quantity, increase/
         decrease, discount/profit-loss, simple interest/tax, multi-step
         word problems, and a gamified mastery/revision capstone that
         also reviews the Integers half).
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

NICE_PERCENTS = [5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90]
DIVS = [2, 3, 4, 5, 6, 8, 9, 10, 11]


def _is_prime(n):
    n = abs(n)
    if n < 2: return False
    for k in range(2, int(n**0.5) + 1):
        if n % k == 0: return False
    return True


# ═══════════════════════ PART 1: INTEGERS (8A-8G) ═══════════════════════

# ───────────────────────── 8A: Concept & Number Line ─────────────────────────

def _A_s(sheet):
    lo, hi = _diff_range(sheet, base_lo=5, base_hi=20, step=5)
    def gen(sheet):
        v = random.choice([x for x in range(-hi-3, hi+4) if abs(x) >= lo])
        return (v, 0)
    def comp(i, sheet):
        v, _ = gen(sheet)
        ctx, template = CONTEXTS[i % len(CONTEXTS)]
        return q(f"{template.format(v=v)} Mark it on the number line.", "diagram", "____",
                  "", "vertical_numberline_blank", {"lo": -hi-5, "hi": hi+5})
    def tf(i, sheet):
        kind = i % 2
        if kind == 0:
            v, _ = gen(sheet)
            shown_sign = random.choice([True, False])
            word = "below" if v < 0 else "above"
            wrong_word = "above" if v < 0 else "below"
            return q(f"True or False: {v} is {word if shown_sign else wrong_word} zero.", "fill", "____ (True/False)")
        else:
            a, b = gen(sheet)[0], gen(sheet)[0]
            actual = "True" if a < b else "False"
            shown = actual if random.random() > 0.4 else ("False" if actual == "True" else "True")
            return q(f"True or False: {a} < {b}  ({shown})", "fill", "____ (True/False)")
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
        target = random.randint(-hi, hi)
        opts = [str(x) for x in [target-3, target-1, target+2, target+5]]
        correct_opts = [o for o in opts if int(o) < target]
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(opts))
        return q(f"Which of these are LESS THAN {target}? Select ALL that apply: {opts_str}",
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
        "Integer Concept & Number Line",
        ["Real situations use integers: temperature, elevation, money owed, electric charge.",
         "-5 degrees means 5 below zero. On the number line, right = bigger, left = smaller."],
        "vertical_numberline_example", {"value": -5, "lo": -10, "hi": 10},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=10)


# ───────────────────────── 8B: Addition & Subtraction ─────────────────────────

def _B_s(sheet):
    lo, hi = _diff_range(sheet, base_lo=15, base_hi=50, step=10)
    def gen(sheet):
        return (random.randint(-hi, hi), random.randint(-hi, hi))
    def comp(i, sheet):
        a, b = gen(sheet)
        op = random.choice(["+", "-"])
        ans = a + b if op == "+" else a - b
        return q(f"({a}) {op} ({b}) = ____", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(0, ans) - 8, "hi": max(0, ans) + 8})
    def tf(i, sheet):
        a, b = gen(sheet)
        op = random.choice(["+", "-"])
        correct = a+b if op == "+" else a-b
        shown = correct if random.random() > 0.4 else correct + random.choice([2, -3, 5])
        return q(f"True or False: ({a}) {op} ({b}) = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a = random.randint(-hi, hi); t = random.randint(-hi, hi)
        op = random.choice(["+", "-"])
        return q(f"({a}) {op} ____ = {t}", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a, t)-5, "hi": max(a, t)+5})
    def numeral(i, sheet):
        a, b = gen(sheet)
        op = random.choice(["+", "-"])
        return q(f"({a}) {op} ({b}) = ____", "fill", "____")
    def multisel(i, sheet):
        target = random.randint(-hi, hi)
        opts = [f"({target-2})+(2)", f"({target+1})-(1)", f"({target})+(0)", f"({target+4})-(4)"]
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(opts))
        return q(f"Which equal {target}? Select ALL that apply: {opts_str}", "fill", "____ (list all letters)")
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
        "Integer Addition & Subtraction",
        ["Add a positive -> move RIGHT. Add a negative -> move LEFT.",
         "Keep, Change, Change for subtraction: KEEP the first number, CHANGE subtraction to addition, CHANGE the sign of the second number. (-3) - (5) becomes (-3) + (-5) = -8."],
        "vertical_numberline_example", {"value": -8, "lo": -15, "hi": 8},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=20)


# ───────────────────────── 8C: Properties of Addition/Subtraction ─────────────────────────

def _C_s(sheet):
    lo, hi = _diff_range(sheet, base_lo=10, base_hi=40, step=8)
    def gen(sheet):
        op = random.choice(["+", "-"])
        a = random.randint(-hi, hi); b = random.randint(lo, hi)
        return (a, b if op == "+" else b)
    def comp(i, sheet):
        op = random.choice(["+", "-"]); a = random.randint(-hi, hi); b = random.randint(lo, hi)
        return q(f"({a}) {op} ({b}) = ____", "diagram", "____", "", "vertical_numberline_blank", {"lo": a-b-5, "hi": a+b+5})
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
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(opts))
        return q(f"Which equal {target}? Select ALL that apply: {opts_str}", "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(random.randint(-hi, hi), random.randint(lo, hi)) for _ in range(3)]
        lefts = [f"({a})+({b})" for a, b in pairs]; rights = [str(a+b) for a, b in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Properties of Addition/Subtraction",
        ["Closure: a+b is always an integer. Commutative: a+b=b+a. Associative: (a+b)+c=a+(b+c). Identity: a+0=a.",
         "Subtraction does NOT have these properties -- a-b is usually NOT equal to b-a."],
        "integer_chips_example", {"pos": 5, "neg": 3},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=30)


# ───────────────────────── 8D: Multiplication & Division ─────────────────────────

def _D_s(sheet):
    lo, hi = _diff_range(sheet, base_lo=5, base_hi=15, step=3)
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
        product = a*b
        shown = product if random.random() > 0.4 else -product
        return q(f"True or False: (-{a}) x (-{b}) = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b = gen(sheet)
        product = a*b
        return q(f"(-{product}) / ____ = {b}", "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
    def numeral(i, sheet):
        a, b = gen(sheet)
        op = random.choice(["x", "/"])
        if op == "/": a = a*b
        signs = random.choice([("", ""), ("", "-"), ("-", ""), ("-", "-")])
        return q(f"({signs[0]}{a}) {op} ({signs[1]}{b}) = ____", "fill", "____")
    def multisel(i, sheet):
        a, b = gen(sheet)
        target = a*b
        opts = [f"(-{a})x(-{b})", f"({a})x(-{b})", f"(-{a})x({b})", f"({a})x({b})"]
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(opts))
        return q(f"Which equal {target}? Select ALL that apply: {opts_str}", "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"(-{a})x(-{b})" for a, b in pairs]; rights = [str(a*b) for a, b in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Integer Multiplication & Division",
        ["Discover the Sign Rule. Pattern: 3x2=6, 3x1=3, 3x0=0, 3x(-1)=?, 3x(-2)=? What rule do you notice?",
         "Same signs give POSITIVE. Different signs give NEGATIVE. Division follows the same rule."],
        "array_example", {"rows": 3, "cols": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=40)


# ───────────────────────── 8E: Properties of Multiplication/Division ─────────────────────────

def _E_s(sheet):
    lo, hi = _diff_range(sheet, base_lo=5, base_hi=15, step=3)
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
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(opts))
        return q(f"Which equal {target}? Select ALL that apply: {opts_str}", "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(random.randint(-hi, hi), random.randint(lo, hi)) for _ in range(3)]
        lefts = [f"({a})-({b})" for a, b in pairs]; rights = [str(a-b) for a, b in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Properties of Multiplication/Division",
        ["Multiplication: Closure, Commutative (axb=bxa), Associative, Identity (ax1=a), Distributive (ax(b+c)=axb+axc).",
         "Division does NOT satisfy Closure -- e.g. (-7)/2 is not an integer."],
        "vertical_numberline_example", {"value": -8, "lo": -12, "hi": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=50)


# ───────────────────────── 8F: Word Problems + BODMAS ─────────────────────────

def _F_s(sheet):
    lo, hi = _diff_range(sheet, base_lo=10, base_hi=40, step=8)
    blo, bhi = _diff_range(sheet, base_lo=3, base_hi=10, step=2)
    def word_problem(i, sheet):
        kind = i % 6
        if kind == 0:
            a, b = random.randint(-hi, hi), random.randint(-hi, hi)
            return f"Temperature was {a} degrees, then changed by {b} degrees. Now it is ____.", a + b
        elif kind == 1:
            a, b = random.randint(-hi, hi), random.randint(-hi, hi)
            return f"A diver was at {a} m (sea level=0), then moved {b} m. Now at ____.", a + b
        elif kind == 2:
            a, b = random.randint(-hi, hi), random.randint(-hi, hi)
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
    def bodmas_expr(kind, sheet):
        a, b, c, d = tuple(random.randint(blo, bhi) * random.choice([1, -1]) for _ in range(4))
        if a == 0: a = blo
        if b == 0: b = blo
        if c == 0: c = blo
        if d == 0: d = blo
        if kind == 0:
            return f"({a}) + ({b}) x ({c})", a + b*c
        elif kind == 1:
            return f"({a}) - ({b}) x ({c})", a - b*c
        elif kind == 2:
            return f"[({a}) + ({b})] x ({c})", (a+b)*c
        else:
            return f"({a}) x ({b}) + ({c}) x ({d})", a*b + c*d
    def comp(i, sheet):
        if i % 2 == 0:
            txt, ans = word_problem(i, sheet)
            return q(txt, "diagram", "____", "", "vertical_numberline_blank", {"lo": min(0, ans) - 5, "hi": max(0, ans) + 5})
        expr, ans = bodmas_expr(i % 4, sheet)
        return q(f"{expr} = ____  (apply BODMAS)", "fill", "____")
    def tf(i, sheet):
        a, b = random.randint(-hi, hi), random.randint(-hi, hi)
        op = random.choice(["+", "-"])
        correct = a+b if op == "+" else a-b
        shown = correct if random.random() > 0.4 else correct+3
        return q(f"True or False: ({a}) {op} ({b}) = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b, c = random.randint(blo, bhi) or 1, random.randint(blo, bhi) or 1, random.randint(2, 9)
        target = a + b*c
        return q(f"({a}) + ({b}) x ____ = {target}. Find the missing number (apply BODMAS).", "fill", "____")
    def numeral(i, sheet):
        txt, ans = word_problem(i, sheet)
        return q(txt, "fill", "____")
    def multisel(i, sheet):
        a, b, c = random.randint(blo, bhi) or 1, random.randint(blo, bhi) or 1, random.randint(blo, bhi) or 1
        left_to_right = (a + b) * c
        bodmas_order = a + b*c
        return q(f"For ({a}) + ({b}) x ({c}): Priya computed {left_to_right} (left to right). "
                  f"Raj computed {bodmas_order} (BODMAS order). Who is correct? ____ (Priya/Raj)", "fill", "____")
    def matching(i, sheet):
        pairs = [(random.randint(-hi, hi), random.randint(-hi, hi)) for _ in range(3)]
        lefts = [f"({a})+({b})" for a, b in pairs]; rights = [str(a+b) for a, b in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Word Problems + BODMAS",
        ["Picture real situations: temperature, elevation, money, charge.",
         "BODMAS order: Brackets, Of (powers), Division/Multiplication (left to right), Addition/Subtraction (left to right)."],
        "vertical_numberline_example", {"value": 2, "lo": -10, "hi": 10},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=60)


# ───────────────────────── 8G: Mastery Challenge (divisibility, primes, absolute value, puzzles) ─────────────────────────

def _G_s(sheet):
    lo, hi = _diff_range(sheet, base_lo=20, base_hi=100, step=20)
    plo, phi = _diff_range(sheet, base_lo=10, base_hi=70, step=15)
    def comp(i, sheet):
        n = random.randint(-hi, hi)
        if n == 0: n = hi
        d = random.choice(DIVS)
        return q(f"Is {n} divisible by {d}? Use the divisibility rule for {d} to decide.  [1 point]", "fill", "____ (Yes/No)")
    def tf(i, sheet):
        n = random.randint(max(plo, 2), phi)
        actual = "Prime" if _is_prime(n) else "Composite"
        wrong = "Composite" if actual == "Prime" else "Prime"
        shown = actual if random.random() > 0.4 else wrong
        return q(f"True or False: {n} is {shown}.  [1 point]", "fill", "____ (True/False)")
    def missing(i, sheet):
        n = random.randint(-hi, hi)
        if n == 0: n = hi
        return q(f"|{n}| = ____  (absolute value = distance from 0)  [2 points]", "fill", "____")
    def numeral(i, sheet):
        kind = i % 3
        if kind == 0:
            n = random.randint(-hi, hi)
            if n == 0: n = hi
            dv = random.choice(DIVS)
            return q(f"Is {n} divisible by {dv}? Answer Yes or No.  [1 point]", "fill", "____")
        elif kind == 1:
            n = random.randint(max(plo, 2), phi)
            return q(f"Is {n} PRIME or COMPOSITE?  [1 point]", "fill", "____ (Prime/Composite)")
        else:
            n = random.choice([-1, 1]) * random.randint(max(plo, 2), phi)
            extra = random.randint(2, 9)
            return q(f"Find |{n}| + {extra}.  [2 points]", "fill", "____")
    def multisel(i, sheet):
        nums = random.sample(range(max(plo, 2), phi), 4)
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(nums))
        return q(f"Which of these are PRIME numbers? Select ALL that apply: {opts_str}  [2 points]",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        vals = [random.choice([-1, 1]) * random.randint(max(plo, 2), phi) for _ in range(3)]
        lefts = [f"|{v}|" for v in vals]; rights = [str(abs(v)) for v in vals]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its absolute value: {left_str}  to  {right_str}  [2 points]", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    items = _make_rotated_sheet(
        "Integers Mastery Challenge",
        ["Speed challenge: each question has a point value. Add up your own score at the end!",
         "Divisibility: 2,5,10 check the last digit. 3,9 check the digit sum. A PRIME number has exactly 2 factors.",
         "|x| (absolute value) = distance from 0 -- always positive or zero.",
         "Bronze: 20+ points. Silver: 30+ points. Gold: 38+ points (all correct)."],
        "vertical_numberline_example", {"value": -13, "lo": -20, "hi": 20},
        "Formats rotate each sheet. Solve each question, then add up your points (shown in brackets).",
        fmt, sheet, seed_base=70)
    items.append(tb("Your Score", ["My total score: _____.  My badge: Bronze / Silver / Gold (circle one)"]))
    return items


# ═══════════════════════ PART 2: PERCENTAGES (8H-8N) ═══════════════════════

# ───────────────────────── 8H: Percentage Concept ─────────────────────────

def _H_s(sheet):
    s = min(sheet - 1, 3)
    kmax = 5 + s * 5  # sheet1: k up to 5, sheet4: up to 20
    def gen_p(sheet):
        return random.choice(NICE_PERCENTS)
    def simplify(p):
        from math import gcd
        g = gcd(p, 100)
        return p // g, 100 // g
    def comp(i, sheet):
        p = gen_p(sheet)
        return q(f"Shade the grid to show {p}%. Then write {p}% as a decimal.", "diagram", "____",
                  "", "hundredths_grid", {"shaded": p})
    def tf(i, sheet):
        p = gen_p(sheet)
        num, den = simplify(p)
        correct = f"{num}/{den}"
        wrong = f"{num+1}/{den}"
        shown = correct if random.random() > 0.4 else wrong
        return q(f"True or False: {p}% = {shown} (in simplest form).", "fill", "____ (True/False)")
    def missing(i, sheet):
        p = gen_p(sheet)
        num, den = simplify(p)
        return q(f"{num}/{den} = ____ %  (convert the fraction to a percent)", "fill", "____")
    def numeral(i, sheet):
        kind = i % 4
        p = gen_p(sheet)
        if kind == 0:
            return q(f"Write {p}% as a decimal. ____", "fill", "____")
        elif kind == 1:
            dec = p / 100
            return q(f"Write {dec} as a percent. ____", "fill", "____")
        elif kind == 2:
            num, den = simplify(p)
            return q(f"Write {p}% as a fraction in simplest form. ____", "fill", "____")
        else:
            num, den = simplify(p)
            return q(f"Write {num}/{den} as a percent. ____", "fill", "____")
    def multisel(i, sheet):
        p = gen_p(sheet)
        num, den = simplify(p)
        correct = f"{num}/{den}"
        opts = [correct, f"{p}/1000", f"{num+1}/{den}", f"{p/10}"]
        random.shuffle(opts)
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(opts))
        return q(f"Which of these equal {p}%? Select ALL that apply: {opts_str}", "fill", "____ (list all letters)")
    def matching(i, sheet):
        ps = random.sample(NICE_PERCENTS, 3)
        lefts = [f"{p}%" for p in ps]; rights = [str(p/100) for p in ps]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each percent to its decimal: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Percentage Concept",
        ["Percent means 'per hundred'. x% = x/100.",
         "25% = 25/100 = 1/4 = 0.25. To go from fraction to percent, multiply by 100.",
         "To go from decimal to percent, move the decimal point 2 places right."],
        "hundredths_grid_example", {"shaded": 25},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching. This is new ground -- Level 8 now covers Percentages too.",
        fmt, sheet, seed_base=600)


# ───────────────────────── 8I: Finding Percentage of a Quantity ─────────────────────────

def _I_s(sheet):
    s = min(sheet - 1, 3)
    kmax = 5 + s * 5
    def gen(sheet):
        p = random.choice(NICE_PERCENTS)
        n = 20 * random.randint(1, kmax)
        return p, n
    def comp(i, sheet):
        p, n = gen(sheet)
        return q(f"Find {p}% of {n}.", "diagram", "____", "", "hundredths_grid", {"shaded": p})
    def tf(i, sheet):
        p, n = gen(sheet)
        correct = p * n // 100
        shown = correct if random.random() > 0.4 else correct + random.choice([2, -3, 5])
        return q(f"True or False: {p}% of {n} = {shown}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        p, n = gen(sheet)
        result = p * n // 100
        return q(f"{p}% of ____ = {result}. Find the missing number.", "fill", "____")
    def numeral(i, sheet):
        p, n = gen(sheet)
        return q(f"Find {p}% of {n}. ____", "fill", "____")
    def multisel(i, sheet):
        p, n = gen(sheet)
        target = p * n // 100
        opts = [f"{p}% of {n}", f"{p+10}% of {n}", f"{100-p}% of {n}", f"{p}% of {n+20}"]
        random.shuffle(opts)
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(opts))
        return q(f"Which of these equal {target}? Select ALL that apply: {opts_str}", "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{p}% of {n}" for p, n in pairs]; rights = [str(p*n//100) for p, n in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Percentage of a Quantity",
        ["To find x% of n: multiply n by x, then divide by 100.",
         "Example: 25% of 80 = (25 x 80)/100 = 2000/100 = 20."],
        "hundredths_grid_example", {"shaded": 25},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=610)


# ───────────────────────── 8J: Percentage Increase & Decrease ─────────────────────────

def _J_s(sheet):
    s = min(sheet - 1, 3)
    kmax = 5 + s * 5
    def gen(sheet):
        p = random.choice(NICE_PERCENTS)
        n = 20 * random.randint(1, kmax)
        return p, n
    def comp(i, sheet):
        p, n = gen(sheet)
        direction = random.choice(["increases", "decreases"])
        change = p * n // 100
        new = n + change if direction == "increases" else n - change
        return q(f"A quantity of {n} {direction} by {p}%. New value = ____.", "fill", "____")
    def tf(i, sheet):
        p, n = gen(sheet)
        direction = random.choice(["increase", "decrease"])
        change = p * n // 100
        correct = n + change if direction == "increase" else n - change
        shown = correct if random.random() > 0.4 else correct + random.choice([3, -4])
        return q(f"True or False: A {p}% {direction} on {n} gives {shown}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        p, n = gen(sheet)
        change = p * n // 100
        new = n + change
        return q(f"A quantity increases from {n} to {new}. Find the percentage increase. ____%", "fill", "____")
    def numeral(i, sheet):
        p, n = gen(sheet)
        direction = random.choice(["increases", "decreases"])
        change = p * n // 100
        new = n + change if direction == "increases" else n - change
        return q(f"{n} {direction} by {p}%. New value = ____.", "fill", "____")
    def multisel(i, sheet):
        p, n = gen(sheet)
        change = p * n // 100
        target = n + change
        opts = [f"{n} increased by {p}%", f"{n} increased by {p+10}%", f"{n-change} increased by {p}%", f"{n} decreased by {p}%"]
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(opts))
        return q(f"Which of these equal {target}? Select ALL that apply: {opts_str}", "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{n} + {p}%" for p, n in pairs]; rights = [str(n + p*n//100) for p, n in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its increased value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Percentage Increase & Decrease",
        ["Increase: new = original + (percent% of original). Decrease: new = original - (percent% of original).",
         "Percentage change = (change/original) x 100."],
        "hundredths_grid_example", {"shaded": 20},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=620)


# ───────────────────────── 8K: Applications — Discount & Profit/Loss ─────────────────────────

def _K_s(sheet):
    s = min(sheet - 1, 3)
    kmax = 10 + s * 15
    def gen(sheet):
        p = random.choice(NICE_PERCENTS)
        n = 20 * random.randint(1, kmax)
        return p, n
    def comp(i, sheet):
        p, mp = gen(sheet)
        discount = p * mp // 100
        return q(f"A shirt marked at ${mp} has a discount of {p}%. Find the discount amount and the sale price.", "fill", "____")
    def tf(i, sheet):
        p, cp = gen(sheet)
        kind = random.choice(["profit", "loss"])
        change = p * cp // 100
        correct = cp + change if kind == "profit" else cp - change
        shown = correct if random.random() > 0.4 else correct + random.choice([5, -6])
        return q(f"True or False: Cost price ${cp} with a {p}% {kind} gives a selling price of ${shown}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        p, cp = gen(sheet)
        sp = cp + p * cp // 100
        return q(f"An item bought for ${cp} is sold for ${sp}. Find the profit percentage. ____%", "fill", "____")
    def numeral(i, sheet):
        p, mp = gen(sheet)
        discount = p * mp // 100
        sale = mp - discount
        return q(f"Marked price ${mp}, discount {p}%. Sale price = ____.", "fill", "____")
    def multisel(i, sheet):
        p, cp = gen(sheet)
        sp = cp + p * cp // 100
        opts = [f"CP ${cp}, profit {p}%", f"CP ${cp}, profit {p+10}%", f"CP ${cp-p*cp//100}, profit {p}%", f"CP ${cp}, loss {p}%"]
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(opts))
        return q(f"Which of these give a selling price of ${sp}? Select ALL that apply: {opts_str}", "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"MP ${mp}, discount {p}%" for p, mp in pairs]; rights = [str(mp - p*mp//100) for p, mp in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its sale price: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Discount & Profit/Loss",
        ["Sale price = Marked price - Discount. Discount = (discount% x Marked price)/100.",
         "Profit % = (Profit/Cost Price) x 100. Selling Price = Cost Price + Profit (or - Loss)."],
        "hundredths_grid_example", {"shaded": 30},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=630)


# ───────────────────────── 8L: Applications — Simple Interest & Tax ─────────────────────────

def _L_s(sheet):
    s = min(sheet - 1, 3)
    mmax = 5 + s * 10
    RATES = [2, 3, 4, 5, 6, 8, 10, 12]
    def gen(sheet):
        p = 100 * random.randint(1, mmax)
        r = random.choice(RATES)
        t = random.randint(1, 5)
        return p, r, t
    def comp(i, sheet):
        p, r, t = gen(sheet)
        return q(f"Find the simple interest on ${p} at {r}% per year for {t} years.  (SI = P x R x T / 100)", "fill", "____")
    def tf(i, sheet):
        p, r, t = gen(sheet)
        si = p * r * t // 100
        shown = si if random.random() > 0.4 else si + random.choice([10, -20])
        return q(f"True or False: Simple interest on ${p} at {r}% for {t} years = ${shown}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        p, r, t = gen(sheet)
        si = p * r * t // 100
        return q(f"Simple interest on ${p} at ____% for {t} years = ${si}. Find the missing rate.", "fill", "____")
    def numeral(i, sheet):
        kind = i % 2
        if kind == 0:
            p, r, t = gen(sheet)
            return q(f"Find the simple interest on ${p} at {r}% per year for {t} years. ____", "fill", "____")
        else:
            p = 20 * random.randint(1, mmax)
            tax = random.choice(NICE_PERCENTS)
            return q(f"An item costs ${p} before tax. Sales tax is {tax}%. Find the total price. ____", "fill", "____")
    def multisel(i, sheet):
        p, r, t = gen(sheet)
        si = p * r * t // 100
        opts = [f"P=${p}, R={r}%, T={t}yr", f"P=${p}, R={r+2}%, T={t}yr", f"P=${p//2}, R={r*2}%, T={t}yr", f"P=${p}, R={r}%, T={t+1}yr"]
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(opts))
        return q(f"Which of these give simple interest ${si}? Select ALL that apply: {opts_str}", "fill", "____ (list all letters)")
    def matching(i, sheet):
        triples = [gen(sheet) for _ in range(3)]
        lefts = [f"P=${p},R={r}%,T={t}yr" for p, r, t in triples]; rights = [str(p*r*t//100) for p, r, t in triples]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its simple interest: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Simple Interest & Tax",
        ["Simple Interest = (Principal x Rate x Time) / 100.",
         "Total price with tax = Original price + (tax% of original price)."],
        "hundredths_grid_example", {"shaded": 10},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=640)


# ───────────────────────── 8M: Multi-step Percentage Word Problems ─────────────────────────

def _M_s(sheet):
    s = min(sheet - 1, 3)
    kmax = 5 + s * 5
    def comp(i, sheet):
        kind = i % 4
        if kind == 0:
            total = 20 * random.randint(1, kmax)
            scored = random.randint(total // 4, total)
            return q(f"A student scored {scored} out of {total} marks. Find the percentage score.", "fill", "____%")
        elif kind == 1:
            n = 20 * random.randint(1, kmax)
            p1 = random.choice(NICE_PERCENTS)
            after1 = n + p1 * n // 100
            p2 = random.choice(NICE_PERCENTS)
            return q(f"A population of {n} increases by {p1}% in year 1. Find the population after year 1. Then it increases by another {p2}% in year 2 -- find the final population.", "fill", "____")
        elif kind == 2:
            whole = 20 * random.randint(1, kmax)
            p1 = random.choice(NICE_PERCENTS)
            part = p1 * whole // 100
            p2 = random.choice(NICE_PERCENTS)
            return q(f"Find {p2}% of {p1}% of {whole}.", "fill", "____")
        else:
            price = 20 * random.randint(1, kmax)
            disc = random.choice(NICE_PERCENTS)
            tax = random.choice(NICE_PERCENTS)
            return q(f"An item marked ${price} has a {disc}% discount applied first, then {tax}% tax added to the discounted price. Find the final price.", "fill", "____")
    def tf(i, sheet):
        total = 20 * random.randint(1, kmax)
        scored = random.randint(total // 4, total)
        pct = scored * 100 // total if total != 0 else 0
        shown = pct if random.random() > 0.4 else pct + random.choice([5, -5])
        return q(f"True or False: {scored} out of {total} is {shown}%.", "fill", "____ (True/False)")
    def missing(i, sheet):
        total = 20 * random.randint(1, kmax)
        pct = random.choice(NICE_PERCENTS)
        scored = pct * total // 100
        return q(f"A student scored ____ out of {total}, which is {pct}%. Find the marks scored.", "fill", "____")
    def numeral(i, sheet):
        whole = 20 * random.randint(1, kmax)
        p1 = random.choice(NICE_PERCENTS)
        part = p1 * whole // 100
        p2 = random.choice(NICE_PERCENTS)
        return q(f"Find {p2}% of {p1}% of {whole}. ____", "fill", "____")
    def multisel(i, sheet):
        total = 20 * random.randint(1, kmax)
        pct = random.choice(NICE_PERCENTS)
        scored = pct * total // 100
        opts = [f"{scored} out of {total}", f"{scored+2} out of {total}", f"{scored} out of {total+20}", f"{pct}% of {total}"]
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(opts))
        return q(f"Which of these equal {scored}? Select ALL that apply: {opts_str}", "fill", "____ (list all letters)")
    def matching(i, sheet):
        triples = []
        for _ in range(3):
            total = 20 * random.randint(1, kmax)
            pct = random.choice(NICE_PERCENTS)
            triples.append((total, pct))
        lefts = [f"{pct}% of {total}" for total, pct in triples]; rights = [str(pct*total//100) for total, pct in triples]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return _make_rotated_sheet(
        "Multi-step Percentage Word Problems",
        ["Chain percentage steps one at a time -- find the first result, then apply the next percentage to THAT result, not the original.",
         "'x% of y%' means multiply: convert both to decimals and multiply, or apply one after the other."],
        "hundredths_grid_example", {"shaded": 60},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=650)


# ───────────────────────── 8N: Mastery Challenge + Level 8 Revision ─────────────────────────

def _N_s(sheet):
    lo, hi = _diff_range(sheet, base_lo=10, base_hi=40, step=8)
    s = min(sheet - 1, 3)
    kmax = 5 + s * 5
    def comp(i, sheet):
        # Integers side: mixed operation
        a, b = random.randint(-hi, hi), random.randint(-hi, hi)
        op = random.choice(["+", "-"])
        return q(f"({a}) {op} ({b}) = ____  [1 point]", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a, b)-5, "hi": max(a, b)+5})
    def tf(i, sheet):
        kind = i % 2
        if kind == 0:
            a, b = random.randint(lo, hi), random.randint(lo, hi)
            correct_prop = random.choice(["Commutative", "Associative", "Closure", "Distributive"])
            wrong_prop = random.choice([p for p in ["Commutative", "Associative", "Closure", "Distributive"] if p != correct_prop])
            shown_prop = correct_prop if random.random() > 0.4 else wrong_prop
            examples = {
                "Commutative": f"({a}) + ({b}) = ({b}) + ({a})",
                "Associative": f"[({a})+({b})]+(2) = ({a})+[({b})+(2)]",
                "Closure": f"({a}) - ({b}) is always an integer",
                "Distributive": f"({a}) x [({b})+(2)] = ({a})x({b}) + ({a})x(2)",
            }
            return q(f"True or False: '{examples[correct_prop]}' is an example of the {shown_prop} Property.  [1 point]", "fill", "____ (True/False)")
        else:
            p = random.choice(NICE_PERCENTS)
            n = 20 * random.randint(1, kmax)
            correct = p * n // 100
            shown = correct if random.random() > 0.4 else correct + random.choice([2, -3])
            return q(f"True or False: {p}% of {n} = {shown}.  [1 point]", "fill", "____ (True/False)")
    def missing(i, sheet):
        kind = i % 3
        if kind == 0:
            n = random.randint(-hi, hi)
            if n == 0: n = hi
            dv = random.choice(DIVS)
            return q(f"What is the smallest number GREATER than {n} that IS divisible by {dv}?  [2 points]", "fill", "____")
        elif kind == 1:
            n = random.randint(-hi, hi)
            if n == 0: n = hi
            return q(f"|{n}| = ____  [2 points]", "fill", "____")
        else:
            p = random.choice(NICE_PERCENTS)
            n = 20 * random.randint(1, kmax)
            result = p * n // 100
            return q(f"{p}% of ____ = {result}. Find the missing number.  [2 points]", "fill", "____")
    def numeral(i, sheet):
        kind = i % 3
        if kind == 0:
            n = random.randint(max(lo, 2), hi)
            return q(f"Is {n} PRIME or COMPOSITE?  [2 points]", "fill", "____ (Prime/Composite)")
        elif kind == 1:
            a, b, c = random.randint(3, 10), random.randint(3, 10), random.randint(3, 10)
            return q(f"({a}) - ({b}) x ({c}) = ____  (apply BODMAS)  [2 points]", "fill", "____")
        else:
            p, n = random.choice(NICE_PERCENTS), 20 * random.randint(1, kmax)
            direction = random.choice(["increases", "decreases"])
            change = p * n // 100
            new = n + change if direction == "increases" else n - change
            return q(f"{n} {direction} by {p}%. New value = ____.  [2 points]", "fill", "____")
    def multisel(i, sheet):
        p, n = random.choice(NICE_PERCENTS), 20 * random.randint(1, kmax)
        target = p * n // 100
        opts = [f"{p}% of {n}", f"{p+10}% of {n}", f"{100-p}% of {n}", f"{p}% of {n+20}"]
        random.shuffle(opts)
        opts_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(opts))
        return q(f"Which of these equal {target}? Select ALL that apply: {opts_str}  [2 points]", "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(random.randint(-hi, hi), random.randint(-hi, hi)) for _ in range(3)]
        lefts = [f"({a})+({b})" for a, b in pairs]; rights = [str(a+b) for a, b in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}  [2 points]", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    items = _make_rotated_sheet(
        "Level 8 Mastery Challenge & Revision",
        ["Every Level 8 skill: integer operations, properties, divisibility, BODMAS, primes, absolute value, AND percentages.",
         "Speed challenge: each question has a point value. Add up your own score at the end!",
         "Bronze: 20+ points. Silver: 30+ points. Gold: 38+ points (all correct)."],
        "vertical_numberline_example", {"value": 2, "lo": -10, "hi": 10},
        "Formats rotate each sheet. Solve each question, then add up your points (shown in brackets).",
        fmt, sheet, seed_base=900)
    items.append(tb("Your Score", ["My total score: _____.  My badge: Bronze / Silver / Gold (circle one)"]))
    return items


# ───────────────────────── Dispatcher (REPLACES original Level 8) ─────────────────────────

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL8_DISPATCH = {
    "8A": _wrap(_A_s), "8B": _wrap(_B_s), "8C": _wrap(_C_s), "8D": _wrap(_D_s),
    "8E": _wrap(_E_s), "8F": _wrap(_F_s), "8G": _wrap(_G_s), "8H": _wrap(_H_s),
    "8I": _wrap(_I_s), "8J": _wrap(_J_s), "8K": _wrap(_K_s), "8L": _wrap(_L_s),
    "8M": _wrap(_M_s), "8N": _wrap(_N_s),
}
