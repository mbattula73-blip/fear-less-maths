"""
Fear Less Maths — LEVEL 8 REDESIGN (Integers, Grade 6-7, higher students)

Replaces the original Level 8 in place, reusing the EXACT same 14
sub-level codes (8A-8J, 8CUM1-3, 8REV) so the existing rich "Concept &
Tips" study pages (concept_pages.py) remain untouched and correctly
matched to their topics.

Three things this redesign does differently from a plain CPA worksheet:

1. ~50% CPA (not the 15/5 pictorial/numeral split used in Pre-Levels)
   -- these are older students, so less hand-holding is appropriate.

2. QUESTION ORIENTATION ROTATION (the core fix): every 20-question sheet
   is split into 4 blocks of 5, each a DIFFERENT task format around the
   same skill, instead of one format repeated 20 times:
     Block 1 (Q1-5):   standard computation (diagram + bare expression)
     Block 2 (Q6-10):  True/False (including deliberately wrong
                        statements -- the research-backed "compare
                        correct vs incorrect" technique)
     Block 3 (Q11-15): missing-number / fill-in-the-blank variant
                        (same skill, asked from a different angle)
     Block 4 (Q16-20): pure numeral, no diagram (CPA Abstract stage)

3. Integer-specific pedagogy researched separately: two-colour zero-pair
   counters (discovery-based, not told the rule), vertical number lines
   (research-recommended over horizontal for temperature/elevation
   contexts), "Keep-Change-Change" for subtraction, discovering the
   multiplication sign rule from a number pattern instead of being told,
   rotating real-world contexts (temperature/elevation/money/charge),
   integer magic squares, and a self-scored speed round.
"""
import random
from content import cb, tb, q

CONTEXTS = [
    ("temperature", "The temperature is {v} degrees."),
    ("elevation", "A point is at {v} m relative to sea level."),
    ("money", "An account balance is {v} dollars (negative = owed)."),
    ("charge", "An electric charge reads {v}."),
]


def _kind_ctx(i):
    return CONTEXTS[i % len(CONTEXTS)]


def _chip_q(pos, neg, op="+"):
    return q(f"({pos}) {op} (-{neg}) = ____", "diagram", "____", "", "integer_chips_blank",
              {"pos": pos, "neg": neg})


def _vline_q(lo, hi):
    return q("Mark the value on the number line.", "diagram", "____",
              "", "vertical_numberline_blank", {"lo": lo, "hi": hi})


def _array_int_q(rows, cols, sign_row, sign_col):
    return q(f"({sign_row}{rows}) x ({sign_col}{cols}) = ____", "diagram", "____",
              "", "array_blank", {"rows": rows, "cols": cols})


def _make_4block_sheet(title, bullets, icon, icon_params, instruction, block_builders, sheet, seed_base=0):
    random.seed(seed_base + sheet)
    items = [cb(title, bullets, "", icon_diagram=icon, icon_params=icon_params)]
    items.append(tb("Instructions", [instruction]))
    for builder in block_builders:
        for i in range(5):
            items.append(builder(i, sheet))
    return items


# ───────────────────────── 8A: Integer concept ─────────────────────────

def _A_s(sheet):
    def b1(i, sheet):
        ctx, template = _kind_ctx(i)
        v = random.choice([-8,-5,-3,-1,2,4,6,9])
        return q(f"{template.format(v=v)} Mark it on the number line.", "diagram", "____",
                  "", "vertical_numberline_blank", {"lo": -10, "hi": 10})
    def b2(i, sheet):
        v = random.choice([-7,-4,-2,3,5,8])
        claim = random.choice([True, False])
        shown = v if claim else -v
        return q(f"True or False: {shown} is {'below' if shown<0 else 'above'} zero.", "fill", "____ (True/False)")
    def b3(i, sheet):
        v = random.choice([-9,-6,-4,2,5,7])
        return q(f"The opposite of {v} is ____.", "diagram", "____", "", "vertical_numberline_blank", {"lo":-10,"hi":10})
    def b4(i, sheet):
        v = random.randint(-9,9)
        return q(f"Write the opposite of {v}. ____", "fill", "____")
    return _make_4block_sheet(
        "Worked Example",
        ["Real situations use integers: temperature, elevation, money owed, electric charge.",
         "-5 degrees means 5 below zero. +5 m means 5 above sea level."],
        "vertical_numberline_example", {"value": -5, "lo": -10, "hi": 10},
        "Q1-5: mark the value. Q6-10: True/False. Q11-15: find the opposite. Q16-20: write the opposite, no picture.",
        [b1, b2, b3, b4], sheet, seed_base=10)


# ───────────────────────── 8B: Number line / ordering ─────────────────────────

def _B_s(sheet):
    def b1(i, sheet):
        v = random.randint(-9,9)
        return q(f"Mark {v} on the number line.", "diagram", "____", "", "vertical_numberline_blank", {"lo":-10,"hi":10})
    def b2(i, sheet):
        a, b = random.sample(range(-9,10), 2)
        claim_true = a > b
        stmt_a, stmt_b = (a,b) if random.random()>0.3 else (b,a)
        return q(f"True or False: {stmt_a} > {stmt_b}", "fill", "____ (True/False)")
    def b3(i, sheet):
        a, b = sorted(random.sample(range(-9,9), 2))
        mid = (a+b)//2
        return q(f"{a} < ____ < {b}  (give one number that fits)", "diagram", "____",
                  "", "vertical_numberline_blank", {"lo": a-2, "hi": b+2})
    def b4(i, sheet):
        a, b = random.sample(range(-9,10), 2)
        return q(f"{a} ___ {b}  (>, < or =)", "fill", "____")
    return _make_4block_sheet(
        "Worked Example",
        ["On a vertical number line, UP is bigger, DOWN is smaller.",
         "-3 is above -7, so -3 > -7."],
        "vertical_numberline_example", {"value": -3, "lo": -10, "hi": 10},
        "Q1-5: mark the number. Q6-10: True/False. Q11-15: find a number in between. Q16-20: compare, no picture.",
        [b1, b2, b3, b4], sheet, seed_base=20)


def _CUM1_s(sheet):
    def b1(i, sheet):
        v = random.randint(-9,9)
        return q(f"Mark {v} on the number line.", "diagram", "____", "", "vertical_numberline_blank", {"lo":-10,"hi":10})
    def b2(i, sheet):
        pos, neg = random.randint(2,8), random.randint(2,8)
        return q(f"True or False: ({pos}) + (-{neg}) = {pos-neg}", "fill", "____ (True/False)")
    def b3(i, sheet):
        pos, neg = random.randint(2,8), random.randint(2,8)
        return _chip_q(pos, neg)
    def b4(i, sheet):
        a, b = random.sample(range(-9,10), 2)
        return q(f"{a} ___ {b}", "fill", "____")
    return _make_4block_sheet(
        "Review", ["Mix of concept, ordering, and your first integer addition."],
        "integer_chips_example", {"pos":5,"neg":3},
        "Mixed review of Q1-5/6-10/11-15/16-20 styles.", [b1,b2,b3,b4], sheet, seed_base=100)


# ───────────────────────── 8C: Addition (zero pairs) ─────────────────────────

def _C_s(sheet):
    def b1(i, sheet):
        pos, neg = random.randint(2,8), random.randint(2,8)
        return _chip_q(pos, neg)
    def b2(i, sheet):
        a, b = random.randint(-9,-1), random.randint(1,9)
        correct = a+b
        shown = correct if random.random()>0.4 else correct + random.choice([-2,2,3])
        return q(f"True or False: ({a}) + ({b}) = {shown}", "fill", "____ (True/False)")
    def b3(i, sheet):
        a = random.randint(-9,-1); target = random.randint(-5,8)
        return q(f"({a}) + ____ = {target}", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a,target)-3, "hi": max(a,target)+3})
    def b4(i, sheet):
        a, b = random.randint(-9,9), random.randint(-9,9)
        return q(f"({a}) + ({b}) = ____", "fill", "____")
    return _make_4block_sheet(
        "Worked Example — Discover the Zero Pair Rule",
        ["Try pairing one (+) chip with one (-) chip before reading on.",
         "A (+) and a (-) together cancel out -- a ZERO PAIR.",
         "Whatever is left over (no partner) gives the answer."],
        "integer_chips_example", {"pos":5,"neg":3},
        "Q1-5: circle zero pairs to add. Q6-10: True/False. Q11-15: find the missing addend. Q16-20: add, no picture.",
        [b1,b2,b3,b4], sheet, seed_base=30)


# ───────────────────────── 8D: Subtraction (Keep-Change-Change) ─────────────────────────

def _D_s(sheet):
    def b1(i, sheet):
        a, b = random.randint(-9,9), random.randint(1,9)
        return q(f"({a}) - ({b}) = ____  (Keep {a}, Change - to +, Change {b} to -{b})",
                  "diagram", "____", "", "vertical_numberline_blank", {"lo": a-b-3, "hi": a+3})
    def b2(i, sheet):
        a, b = random.randint(-9,9), random.randint(1,9)
        correct = a-b
        shown = correct if random.random()>0.4 else a+b
        return q(f"True or False: ({a}) - ({b}) = {shown}", "fill", "____ (True/False)")
    def b3(i, sheet):
        a = random.randint(-9,9); target = random.randint(-9,9)
        return q(f"({a}) - ____ = {target}", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a,target)-3, "hi": max(a,target)+3})
    def b4(i, sheet):
        a, b = random.randint(-9,9), random.randint(-9,9)
        return q(f"({a}) - ({b}) = ____", "fill", "____")
    return _make_4block_sheet(
        "Worked Example — Keep, Change, Change",
        ["KEEP the first number, CHANGE subtraction to addition, CHANGE the sign of the second number.",
         "(-3) - (5) becomes (-3) + (-5) = -8."],
        "vertical_numberline_example", {"value": -8, "lo": -12, "hi": 4},
        "Q1-5: use Keep-Change-Change. Q6-10: True/False. Q11-15: find the missing number. Q16-20: subtract, no picture.",
        [b1,b2,b3,b4], sheet, seed_base=40)


def _CUM2_s(sheet):
    def b1(i, sheet):
        pos, neg = random.randint(2,8), random.randint(2,8)
        return _chip_q(pos, neg) if i%2==0 else q(f"({-neg}) - ({pos}) = ____", "diagram", "____",
                                                     "", "vertical_numberline_blank", {"lo":-20,"hi":5})
    def b2(i, sheet):
        a,b = random.randint(-8,8), random.randint(1,8)
        return q(f"True or False: ({a}) - ({b}) = {a+b}", "fill", "____ (True/False)")
    def b3(i, sheet):
        a = random.randint(-9,9); t = random.randint(-9,9)
        return q(f"({a}) {'+ ' if random.random()>0.5 else '- '}____ = {t}", "diagram", "____",
                  "", "vertical_numberline_blank", {"lo": min(a,t)-3, "hi": max(a,t)+3})
    def b4(i, sheet):
        a,b = random.randint(-9,9), random.randint(-9,9)
        return q(f"({a}) {'+' if i%2==0 else '-'} ({b}) = ____", "fill", "____")
    return _make_4block_sheet(
        "Review", ["Mix of addition and subtraction."],
        "vertical_numberline_example", {"value": -8, "lo": -12, "hi": 4},
        "Mixed review of all 4 question styles.", [b1,b2,b3,b4], sheet, seed_base=200)


# ───────────────────────── 8E: Multiplication (discover the sign rule) ─────────────────────────

def _E_s(sheet):
    def b1(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        signs = random.choice([("","-"), ("-",""), ("-","-"), ("","")])
        return _array_int_q(a, b, signs[0], signs[1])
    def b2(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        correct = a*b
        shown = -correct if random.random()>0.4 else correct
        return q(f"True or False: (-{a}) x (-{b}) = {shown}", "fill", "____ (True/False)")
    def b3(i, sheet):
        a = random.randint(2,9); product = a * random.randint(2,9)
        return q(f"(-{a}) x ____ = {-product}", "diagram", "____", "", "array_blank", {"rows": a, "cols": product//a})
    def b4(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        signs = random.choice([("",""), ("","-"), ("-",""), ("-","-")])
        return q(f"({signs[0]}{a}) x ({signs[1]}{b}) = ____", "fill", "____")
    return _make_4block_sheet(
        "Worked Example — Discover the Sign Rule",
        ["Look at the pattern: 3x2=6, 3x1=3, 3x0=0, 3x(-1)=____, 3x(-2)=____. What rule do you notice?",
         "Same signs (+x+ or -x-) give a POSITIVE answer. Different signs give a NEGATIVE answer."],
        "array_example", {"rows": 3, "cols": 4},
        "Q1-5: multiply using the grid. Q6-10: True/False. Q11-15: find the missing factor. Q16-20: multiply, no picture.",
        [b1,b2,b3,b4], sheet, seed_base=50)


# ───────────────────────── 8F: Division (fact families) ─────────────────────────

def _F_s(sheet):
    def b1(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        product = a*b
        signs = random.choice([("",""), ("","-"), ("-",""), ("-","-")])
        return q(f"({signs[0]}{product}) / ({signs[1]}{a}) = ____", "diagram", "____", "", "array_blank", {"rows":a,"cols":b})
    def b2(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        correct = a*b
        shown = correct if random.random()>0.4 else -correct
        return q(f"True or False: (-{correct}) / (-{a}) = {b if shown==correct else -b}", "fill", "____ (True/False)")
    def b3(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        product = a*b
        return q(f"(-{product}) / ____ = {b}", "diagram", "____", "", "array_blank", {"rows":a,"cols":b})
    def b4(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        product = a*b
        signs = random.choice([("",""), ("","-"), ("-",""), ("-","-")])
        return q(f"({signs[0]}{product}) / ({signs[1]}{a}) = ____", "fill", "____")
    return _make_4block_sheet(
        "Worked Example",
        ["Division follows the SAME sign rule as multiplication.",
         "(-12) / (-3) = 4 (same signs -> positive). (-12) / 3 = -4 (different signs -> negative)."],
        "array_example", {"rows": 3, "cols": 4},
        "Q1-5: divide using the grid. Q6-10: True/False. Q11-15: find the missing divisor. Q16-20: divide, no picture.",
        [b1,b2,b3,b4], sheet, seed_base=60)


def _CUM3_s(sheet):
    def b1(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        signs = random.choice([("",""), ("","-"), ("-",""), ("-","-")])
        return _array_int_q(a, b, signs[0], signs[1]) if i%2==0 else q(
            f"({signs[0]}{a*b}) / ({signs[1]}{a}) = ____", "diagram", "____", "", "array_blank", {"rows":a,"cols":b})
    def b2(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        return q(f"True or False: (-{a}) x (-{b}) = {a*b}", "fill", "____ (True/False)")
    def b3(i, sheet):
        a = random.randint(2,9); product = a*random.randint(2,9)
        return q(f"(-{a}) x ____ = {-product}", "diagram", "____", "", "array_blank", {"rows":a,"cols":product//a})
    def b4(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        op = random.choice(["x","/"])
        if op == "/": a = a*b
        return q(f"(-{a}) {op} ({b}) = ____", "fill", "____")
    return _make_4block_sheet(
        "Review", ["Mix of multiplying and dividing integers."],
        "array_example", {"rows": 3, "cols": 4},
        "Mixed review of all 4 question styles.", [b1,b2,b3,b4], sheet, seed_base=300)


# ───────────────────────── 8G: Word problems (rotated contexts) ─────────────────────────

def _G_s(sheet):
    templates = [
        "Temperature was {a} degrees, then changed by {b} degrees. Now it is ____.",
        "A diver was at {a} m (relative to sea level), then moved {b} m. Now at ____.",
        "An account had ${a}, then a transaction of ${b}. New balance: ____.",
    ]
    def b1(i, sheet):
        a = random.randint(-9,9); b = random.randint(-9,9)
        txt = random.choice(templates).format(a=a, b=b)
        return q(txt, "diagram", "____", "", "vertical_numberline_blank", {"lo": min(a,a+b)-3, "hi": max(a,a+b)+3})
    def b2(i, sheet):
        a, b = random.randint(-9,9), random.randint(-9,9)
        correct = a+b
        shown = correct if random.random()>0.4 else correct+2
        return q(f"True or False: starting at {a} and changing by {b} gives {shown}.", "fill", "____ (True/False)")
    def b3(i, sheet):
        a = random.randint(-9,9); final = random.randint(-9,9)
        return q(f"Started at {a}, ended at {final}. The change was ____.", "diagram", "____",
                  "", "vertical_numberline_blank", {"lo": min(a,final)-3, "hi": max(a,final)+3})
    def b4(i, sheet):
        a, b = random.randint(-9,9), random.randint(-9,9)
        txt = random.choice(templates).format(a=a, b=b)
        return q(txt, "fill", "____")
    return _make_4block_sheet(
        "Worked Example",
        ["Picture real situations: temperature, elevation, money, charge.",
         "Started at -3, changed by 5: -3 + 5 = 2."],
        "vertical_numberline_example", {"value": 2, "lo": -10, "hi": 10},
        "Q1-5: solve with the number line. Q6-10: True/False. Q11-15: find the change. Q16-20: solve, no picture.",
        [b1,b2,b3,b4], sheet, seed_base=70)


# ───────────────────────── 8H: Mixed integers ─────────────────────────

def _H_s(sheet):
    def b1(i, sheet):
        a, b = random.randint(-9,9), random.randint(-9,9)
        op = random.choice(["+","-"])
        return q(f"({a}) {op} ({b}) = ____", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a,b,a+b,a-b)-3, "hi": max(a,b,a+b,a-b)+3})
    def b2(i, sheet):
        a, b = random.randint(-9,9), random.randint(-9,9)
        op = random.choice(["+","-"])
        correct = a+b if op=="+" else a-b
        shown = correct if random.random()>0.4 else correct+3
        return q(f"True or False: ({a}) {op} ({b}) = {shown}", "fill", "____ (True/False)")
    def b3(i, sheet):
        a = random.randint(-9,9); t = random.randint(-9,9)
        op = random.choice(["+","-"])
        return q(f"({a}) {op} ____ = {t}", "diagram", "____", "", "vertical_numberline_blank", {"lo": min(a,t)-3,"hi":max(a,t)+3})
    def b4(i, sheet):
        a, b = random.randint(-9,9), random.randint(-9,9)
        op = random.choice(["+","-","x"])
        return q(f"({a}) {op} ({b}) = ____", "fill", "____")
    return _make_4block_sheet(
        "Worked Example", ["Check the operation symbol first, then use the right strategy."],
        "vertical_numberline_example", {"value": 2, "lo": -10, "hi": 10},
        "Q1-5: solve with the number line. Q6-10: True/False. Q11-15: find the missing number. Q16-20: solve, no picture.",
        [b1,b2,b3,b4], sheet, seed_base=80)


# ───────────────────────── 8I: Puzzles (magic squares + spot the mistake) ─────────────────────────

def _I_s(sheet):
    def b1(i, sheet):
        start = random.randint(-9,5); step = random.choice([-3,-2,2,3])
        seq = [start, start+step, start+2*step]
        return q(f"{seq[0]}, {seq[1]}, {seq[2]}, ____  (continue the pattern)", "diagram", "____",
                  "", "vertical_numberline_blank", {"lo": min(seq)-5, "hi": max(seq)+5})
    def b2(i, sheet):
        a, b, c = random.randint(-9,9), random.randint(-9,9), random.randint(-9,9)
        claim = (a+b+c)
        shown = claim if random.random()>0.4 else claim+1
        return q(f"True or False: {a} + {b} + {c} = {shown}", "fill", "____ (True/False)")
    def b3(i, sheet):
        center = random.randint(-5,5)
        given = {(0,0): center-1, (1,1): center, (2,2): center+1}
        total = 3*center
        return q(f"Magic square: every row, column, and diagonal sums to {total}. Fill in the rest.",
                  "diagram", "____", "", "magic_square_blank", {"size": 3, "given": given})
    def b4(i, sheet):
        a = random.randint(-9,9)
        return q(f"I am the opposite of the opposite of {a}. What number am I? ____", "fill", "____")
    return _make_4block_sheet(
        "Worked Example",
        ["A magic square: every row, column, and diagonal adds to the SAME total.",
         "Use the given numbers to work out the pattern, then fill in the rest."],
        "magic_square_blank", {"size": 3, "given": {(0,0):-1, (1,1):0, (2,2):1}},
        "Q1-5: continue the pattern. Q6-10: True/False. Q11-15: complete the magic square. Q16-20: solve, no picture.",
        [b1,b2,b3,b4], sheet, seed_base=90)


def _CUM3b_s(sheet):
    """8CUM3: review G/H/I."""
    def b1(i, sheet):
        a, b = random.randint(-9,9), random.randint(-9,9)
        op = random.choice(["+","-"])
        return q(f"({a}) {op} ({b}) = ____", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a,b)-5, "hi": max(a,b)+5})
    def b2(i, sheet):
        a, b, c = random.randint(-9,9), random.randint(-9,9), random.randint(-9,9)
        return q(f"True or False: {a} + {b} + {c} = {a+b+c}", "fill", "____ (True/False)")
    def b3(i, sheet):
        center = random.randint(-5,5)
        given = {(0,0): center-1, (1,1): center}
        return q("Magic square: complete using the pattern.", "diagram", "____", "", "magic_square_blank",
                  {"size": 3, "given": given})
    def b4(i, sheet):
        a, b = random.randint(-9,9), random.randint(-9,9)
        return q(f"({a}) + ({b}) = ____", "fill", "____")
    return _make_4block_sheet(
        "Review", ["Mix of word problems, mixed operations, and puzzles."],
        "magic_square_blank", {"size": 3, "given": {(0,0):-1,(1,1):0,(2,2):1}},
        "Mixed review of all 4 question styles.", [b1,b2,b3,b4], sheet, seed_base=400)


# ───────────────────────── 8J: Mixed challenge (self-scored speed) ─────────────────────────

def _J_s(sheet):
    def b1(i, sheet):
        a, b = random.randint(-9,9), random.randint(-9,9)
        op = random.choice(["+","-"])
        return q(f"({a}) {op} ({b}) = ____  [1 point]", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a,b)-5, "hi": max(a,b)+5})
    def b2(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        correct = a*b
        shown = correct if random.random()>0.4 else -correct
        return q(f"True or False: (-{a}) x (-{b}) = {shown}  [1 point]", "fill", "____ (True/False)")
    def b3(i, sheet):
        a = random.randint(-9,9); t = random.randint(-9,9)
        return q(f"({a}) + ____ = {t}  [2 points]", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a,t)-3, "hi": max(a,t)+3})
    def b4(i, sheet):
        a, b = random.randint(-9,9), random.randint(-9,9)
        op = random.choice(["+","-","x"])
        return q(f"({a}) {op} ({b}) = ____  [2 points]", "fill", "____")
    items = _make_4block_sheet(
        "Worked Example",
        ["Speed challenge: each question has a point value. Add up your own score at the end!",
         "Bronze: 20+ points. Silver: 30+ points. Gold: 38+ points (all correct)."],
        "vertical_numberline_example", {"value": 2, "lo": -10, "hi": 10},
        "Solve each question, then add up your points. Bronze=20+, Silver=30+, Gold=38+ (all correct).",
        [b1,b2,b3,b4], sheet, seed_base=110)
    items.append(tb("Your Score", ["My total score: _____ / 40.  My badge: Bronze / Silver / Gold (circle one)"]))
    return items


def _REV_s(sheet):
    def b1(i, sheet):
        a, b = random.randint(-9,9), random.randint(-9,9)
        op = random.choice(["+","-"])
        return q(f"({a}) {op} ({b}) = ____", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a,b)-5, "hi": max(a,b)+5})
    def b2(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        correct = a*b
        shown = correct if random.random()>0.4 else -correct
        return q(f"True or False: (-{a}) x (-{b}) = {shown}", "fill", "____ (True/False)")
    def b3(i, sheet):
        a = random.randint(-9,9); t = random.randint(-9,9)
        return q(f"({a}) + ____ = {t}", "diagram", "____", "", "vertical_numberline_blank",
                  {"lo": min(a,t)-3, "hi": max(a,t)+3})
    def b4(i, sheet):
        a, b = random.randint(-9,9), random.randint(-9,9)
        op = random.choice(["+","-","x","/"]) if b != 0 else "+"
        return q(f"({a}) {op} ({b}) = ____", "fill", "____")
    return _make_4block_sheet(
        "Level 8 Revision",
        ["Every integer skill: concept, ordering, the four operations, word problems, and puzzles."],
        "vertical_numberline_example", {"value": 2, "lo": -10, "hi": 10},
        "Work through each block using the strategy that fits.", [b1,b2,b3,b4], sheet, seed_base=900)


# ───────────────────────── Dispatcher (REPLACES original Level 8) ─────────────────────────

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL8_DISPATCH = {
    "8A": _wrap(_A_s), "8B": _wrap(_B_s), "8C": _wrap(_C_s), "8CUM1": _wrap(_CUM1_s),
    "8D": _wrap(_D_s), "8E": _wrap(_E_s), "8F": _wrap(_F_s), "8CUM2": _wrap(_CUM2_s),
    "8G": _wrap(_G_s), "8H": _wrap(_H_s), "8I": _wrap(_I_s), "8CUM3": _wrap(_CUM3b_s),
    "8J": _wrap(_J_s), "8REV": _wrap(_REV_s),
}
