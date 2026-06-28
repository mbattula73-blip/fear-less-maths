"""
Fear Less Maths — LEVEL 3 REDESIGN v3 (Addition & Subtraction, Grade 2-3)

v3 applies the full question_formats.py rotation architecture (same fix
shipped to Levels 6/7/8) PLUS the new "fun format" pool (Math Maze,
Function Machine, Number Pyramid, Code Breaker, proper vertical
Matching) for the Puzzle/Speed/Mixed sub-levels, where they fit
thematically. Every sub-level's 4 sheets are genuinely different
worksheets (rotating format templates), and difficulty widens slightly
sheet to sheet. All v1/v2 pedagogical content (concrete carrying/
borrowing trade visuals, Keep-Change-Change, taught mental-math
strategies, tiered puzzles) is preserved.
"""
import random
from content import cb, tb, q
from question_formats import (TEMPLATES, diff_range, make_rotated_sheet, make_fun_sheet,
                               make_format_builders, matching_q, maze_q, function_machine_q,
                               pyramid_q, codebreaker_q)

# ───────────────────────── A/B/C: Addition foundation ─────────────────────────

def _A_s(sheet):
    lo, hi = diff_range(sheet, 1, 9)
    def gen(sheet):
        return (random.randint(1, 9), random.randint(1, 9))
    fmt = make_format_builders(gen, "regroup_ones_blank",
                                lambda a, b: {"ones1": a, "ones2": b}, "+", lambda a, b: a+b)
    return make_rotated_sheet(
        "Worked Example", ["Count both groups of ones, then add them together."],
        "regroup_ones_blank", {"ones1": 4, "ones2": 3},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=10)


def _B_s(sheet):
    def gen(sheet):
        a = random.randint(10, 80); ao = a % 10
        b = random.randint(1, 9-ao) if ao < 9 else 1
        return (a, b)
    def diagram_params(a, b):
        return {"ones1": a % 10, "ones2": b}
    fmt = make_format_builders(gen, "regroup_ones_blank", diagram_params, "+", lambda a, b: a+b)
    return make_rotated_sheet(
        "Worked Example",
        ["The tens digit stays the same -- only add the ones.",
         "23 + 4: tens stay at 2, ones become 3+4=7, so the answer is 27."],
        "regroup_ones_blank", {"ones1": 3, "ones2": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=20)


def _C_s(sheet):
    def gen(sheet):
        a_tens, b_tens = random.randint(1,4), random.randint(1,4)
        a_ones = random.randint(0,9); b_ones = random.randint(0, 9-a_ones)
        return (a_tens*10+a_ones, b_tens*10+b_ones)
    def diagram_params(a, b):
        return {"ones1": a % 10, "ones2": b % 10}
    fmt = make_format_builders(gen, "regroup_ones_blank", diagram_params, "+", lambda a, b: a+b)
    return make_rotated_sheet(
        "Worked Example",
        ["Add the ones first, then add the tens.", "23 + 14: ones 3+4=7, tens 2+1=3, answer = 37."],
        "regroup_ones_blank", {"ones1": 3, "ones2": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=30)


def _CUM1_s(sheet):
    def gen(sheet):
        choice = random.random()
        if choice < 0.5:
            return (random.randint(1,9), random.randint(1,9))
        a = random.randint(10,80); ao = a % 10
        return (a, random.randint(1,9-ao) if ao<9 else 1)
    def diagram_params(a, b):
        return {"ones1": a % 10, "ones2": b % 10}
    fmt = make_format_builders(gen, "regroup_ones_blank", diagram_params, "+", lambda a, b: a+b)
    return make_rotated_sheet(
        "Review", ["Mix of single-digit and 2-digit addition (no carrying yet)."],
        "regroup_ones_blank", {"ones1": 3, "ones2": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=100)


# ───────────────────────── D/E/CUM2: Carrying ─────────────────────────

def _D_s(sheet):
    def gen(sheet):
        a_ones = random.randint(5,9); b_ones = random.randint(11-a_ones, 9)
        return (a_ones, b_ones)
    fmt = make_format_builders(gen, "regroup_ones_blank", lambda a,b: {"ones1":a,"ones2":b}, "+", lambda a,b: a+b)
    return make_rotated_sheet(
        "Worked Example",
        ["When the ones add up to 10 or more, trade 10 ones for 1 new ten.",
         "7 ones + 5 ones = 12 ones = 1 ten + 2 ones."],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=40)


def _E_s(sheet):
    def gen(sheet):
        a_ones = random.randint(5,9); b_ones = random.randint(11-a_ones,9)
        a_tens, b_tens = random.randint(1,4), random.randint(1,4)
        return (a_tens*10+a_ones, b_tens*10+b_ones)
    def diagram_params(a, b):
        return {"ones1": a % 10, "ones2": b % 10}
    fmt = make_format_builders(gen, "regroup_ones_blank", diagram_params, "+", lambda a,b: a+b)
    return make_rotated_sheet(
        "Worked Example", ["Add the ones, trade if 10 or more, then add the tens (plus the new ten)."],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=50)


def _CUM2_s(sheet):
    def gen(sheet):
        a_ones = random.randint(4,9); b_ones = random.randint(max(1,11-a_ones),9)
        a_tens, b_tens = random.randint(1,4), random.randint(1,4)
        return (a_tens*10+a_ones, b_tens*10+b_ones)
    def diagram_params(a, b):
        return {"ones1": a % 10, "ones2": b % 10}
    fmt = make_format_builders(gen, "regroup_ones_blank", diagram_params, "+", lambda a,b: a+b)
    return make_rotated_sheet(
        "Review", ["Practice carrying with different two-digit numbers."],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=200)


# ───────────────────────── F/G/CUM3: Subtraction foundation ─────────────────────────

def _F_s(sheet):
    def gen(sheet):
        a = random.randint(2,9); b = random.randint(1,a)
        return (a, b)
    fmt = make_format_builders(gen, "regroup_break_blank", lambda a,b: {"tens":0,"ones":a}, "-", lambda a,b: a-b)
    return make_rotated_sheet(
        "Worked Example", ["Count the group, then take away that many."],
        "regroup_break_blank", {"tens": 0, "ones": 8},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=60)


def _G_s(sheet):
    def gen(sheet):
        at = random.randint(2,8); ao = random.randint(0,9); bo = random.randint(0,ao)
        bt = random.randint(1,at-1) if at>1 else 0
        return (at*10+ao, bt*10+bo)
    def diagram_params(a, b):
        return {"tens": a//10, "ones": a%10}
    fmt = make_format_builders(gen, "regroup_break_blank", diagram_params, "-", lambda a,b: a-b)
    return make_rotated_sheet(
        "Worked Example",
        ["Subtract the ones first, then the tens. No breaking needed yet.",
         "47 - 23: ones 7-3=4, tens 4-2=2, answer = 24."],
        "regroup_break_blank", {"tens": 4, "ones": 7},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=70)


def _CUM3_s(sheet):
    def gen(sheet):
        choice = random.random()
        if choice < 0.5:
            a = random.randint(2,9); return (a, random.randint(1,a))
        at = random.randint(2,8); ao = random.randint(0,9); bo = random.randint(0,ao)
        bt = random.randint(1,at-1) if at>1 else 0
        return (at*10+ao, bt*10+bo)
    def diagram_params(a, b):
        return {"tens": a//10, "ones": a%10}
    fmt = make_format_builders(gen, "regroup_break_blank", diagram_params, "-", lambda a,b: a-b)
    return make_rotated_sheet(
        "Review", ["Mix of single-digit and 2-digit subtraction (no borrowing yet)."],
        "regroup_break_blank", {"tens": 4, "ones": 7},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=300)


# ───────────────────────── H/I/J/CUM4: Borrowing ─────────────────────────

def _H_s(sheet):
    def gen(sheet):
        a_tens = random.randint(2,6); a_ones = random.randint(0,4)
        b_ones = random.randint(a_ones+1, 9)
        return (a_tens*10+a_ones, b_ones)
    def diagram_params(a, b):
        return {"tens": a//10, "ones": a%10}
    fmt = make_format_builders(gen, "regroup_break_blank", diagram_params, "-", lambda a,b: a-b)
    return make_rotated_sheet(
        "Worked Example",
        ["If there aren't enough ones to subtract, break one ten into 10 loose ones.",
         "43: not enough ones to take away 7. Break a ten: 3 tens + 13 ones."],
        "regroup_break_blank", {"tens": 4, "ones": 3},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=80)


def _I_s(sheet):
    def gen(sheet):
        a_tens = random.randint(2,7); a_ones = random.randint(0,5)
        b_ones = random.randint(a_ones+1, 9)
        return (a_tens*10+a_ones, b_ones)
    def diagram_params(a, b):
        return {"tens": a//10, "ones": a%10}
    fmt = make_format_builders(gen, "regroup_break_blank", diagram_params, "-", lambda a,b: a-b)
    return make_rotated_sheet(
        "Worked Example",
        ["Write the number in expanded form after breaking a ten.",
         "43 = 30 + 13 (after breaking one ten into ten ones)."],
        "regroup_break_blank", {"tens": 4, "ones": 3},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=90)


def _J_s(sheet):
    def gen(sheet):
        a_tens = random.randint(2,8); a_ones = random.randint(0,5)
        b_ones = random.randint(a_ones+1, 9); b_tens = random.randint(1, a_tens-1) if a_tens>1 else 0
        return (a_tens*10+a_ones, b_tens*10+b_ones)
    def diagram_params(a, b):
        return {"tens": a//10, "ones": a%10}
    fmt = make_format_builders(gen, "regroup_break_blank", diagram_params, "-", lambda a,b: a-b)
    return make_rotated_sheet(
        "Worked Example", ["Break a ten if needed, then subtract ones, then subtract tens."],
        "regroup_break_blank", {"tens": 4, "ones": 3},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=95)


def _CUM4_s(sheet):
    def gen(sheet):
        a_tens = random.randint(2,8); a_ones = random.randint(0,5)
        b_ones = random.randint(a_ones+1, 9); b_tens = random.randint(1, a_tens-1) if a_tens>1 else 0
        return (a_tens*10+a_ones, b_tens*10+b_ones)
    def diagram_params(a, b):
        return {"tens": a//10, "ones": a%10}
    fmt = make_format_builders(gen, "regroup_break_blank", diagram_params, "-", lambda a,b: a-b)
    return make_rotated_sheet(
        "Review", ["Practice borrowing with different two-digit numbers."],
        "regroup_break_blank", {"tens": 4, "ones": 3},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=400)


# ───────────────────────── K/L/CUM5: Mixed & word problems ─────────────────────────

def _K_s(sheet):
    def gen(sheet):
        op = random.choice(["+","-"])
        a_tens = random.randint(1,5); a_ones = random.randint(0,9); a = a_tens*10+a_ones
        b = random.randint(1, 20) if op == "+" else random.randint(1, a)
        return (a, b)
    def diagram_params(a, b):
        return {"tens": a//10, "ones": a%10} if False else {"ones1": a%10, "ones2": b%10}
    def comp(i, sheet):
        a, b = gen(sheet); op = "+" if i % 2 == 0 else "-"
        if op == "-": b = min(b, a)
        dfn = "regroup_ones_blank" if op == "+" else "regroup_break_blank"
        dp = {"ones1": a%10, "ones2": b%10} if op == "+" else {"tens": a//10, "ones": a%10}
        return q(f"{a} {op} {b} = ____", "diagram", "____", "", dfn, dp)
    def tf(i, sheet):
        a, b = gen(sheet); op = "+" if i % 2 == 0 else "-"
        if op == "-": b = min(b, a)
        correct = a+b if op == "+" else a-b
        shown = correct if random.random() > 0.4 else correct+2
        return q(f"True or False: {a} {op} {b} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b = gen(sheet); op = "+" if i % 2 == 0 else "-"
        if op == "-": b = min(b, a)
        target = a+b if op == "+" else a-b
        return q(f"{a} {op} ____ = {target}", "fill", "____")
    def numeral(i, sheet):
        a, b = gen(sheet); op = "+" if i % 2 == 0 else "-"
        if op == "-": b = min(b, a)
        return q(f"{a} {op} {b} = ____", "fill", "____")
    def multisel(i, sheet):
        target = random.randint(10, 60)
        opts = [f"{target-5}+5", f"{target}+0", f"{target+3}-3", f"{target+1}-2"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{a}+{b}" for a, b in pairs]; rights = [str(a+b) for a, b in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example", ["Check the symbol first: + or -? Then solve using the same steps as before."],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=110)


def _L_s(sheet):
    templates_add = ["{a} red balls and {b} blue balls. Total = ____.", "{a} students in class A, {b} in class B. Total = ____."]
    templates_sub = ["{a} oranges, {b} are rotten. Good ones = ____.", "Had {a} rupees, spent {b}. Left = ____."]
    def gen(sheet):
        a = random.randint(10,60); b = random.randint(5,30)
        return (a, b)
    def comp(i, sheet):
        a, b = gen(sheet)
        if i % 2 == 0:
            return q(random.choice(templates_add).format(a=a,b=b), "diagram", "____", "", "regroup_ones_blank", {"ones1":a%10,"ones2":b%10})
        b = min(b, a)
        return q(random.choice(templates_sub).format(a=a,b=b), "diagram", "____", "", "regroup_break_blank", {"tens":a//10,"ones":a%10})
    def tf(i, sheet):
        a, b = gen(sheet)
        correct = a+b
        shown = correct if random.random() > 0.4 else correct+3
        return q(f"True or False: {a} red and {b} blue balls = {shown} total.", "fill", "____ (True/False)")
    def missing(i, sheet):
        a = random.randint(10,60)
        return q(f"Had {a} rupees, spent ____, now have {a-15}. How much spent?", "fill", "____")
    def numeral(i, sheet):
        a, b = gen(sheet)
        txt = random.choice(templates_add + templates_sub).format(a=a, b=min(b,a))
        return q(txt, "fill", "____")
    def multisel(i, sheet):
        target = random.randint(15,50)
        opts = [f"{target-5} balls + 5 more", f"{target} balls + 0 more", f"{target+10} balls - 10", f"{target+2} balls - 1"]
        return q(f"Which give {target} total? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{a} + {b}" for a,b in pairs]; rights = [str(a+b) for a,b in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example", ["Decide: are things being joined (add) or taken away (subtract)?"],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=120)


def _CUM5_s(sheet):
    def gen(sheet):
        a = random.randint(15,60); b = random.randint(5,30)
        return (a, b)
    def comp(i, sheet):
        a, b = gen(sheet); op = "+" if i % 2 == 0 else "-"
        b = min(b, a) if op == "-" else b
        dfn = "regroup_ones_blank" if op == "+" else "regroup_break_blank"
        dp = {"ones1":a%10,"ones2":b%10} if op == "+" else {"tens":a//10,"ones":a%10}
        return q(f"{a} {op} {b} = ____", "diagram", "____", "", dfn, dp)
    def tf(i, sheet):
        a, b = gen(sheet); correct = a+b
        shown = correct if random.random() > 0.4 else correct+2
        return q(f"True or False: {a} + {b} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b = gen(sheet)
        return q(f"{a} + ____ = {a+b}", "fill", "____")
    def numeral(i, sheet):
        a, b = gen(sheet); op = "+" if i % 2 == 0 else "-"
        b = min(b, a) if op == "-" else b
        return q(f"{a} {op} {b} = ____", "fill", "____")
    def multisel(i, sheet):
        target = random.randint(15,50)
        opts = [f"{target-5}+5", f"{target}+0", f"{target+10}-10", f"{target+1}-2"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{a}+{b}" for a,b in pairs]; rights = [str(a+b) for a,b in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of addition, subtraction, and word problems."],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=500)


# ───────────────────────── M/N/CUM6: Mental math (taught) ─────────────────────────

def _M_s(sheet):
    def comp(i, sheet):
        if i % 2 == 0:
            given = random.randint(2,9)
            return q(f"{given} + ____ = 10  (how many more to make 10?)", "diagram", "____", "", "make_ten_frame_blank", {"given": given})
        n = random.randint(2,9)
        return q(f"{n} + {n} = ____  (double)", "diagram", "____", "", "number_bond_blank", {"known": n})
    def tf(i, sheet):
        given = random.randint(2,9)
        correct = 10-given
        shown = correct if random.random() > 0.4 else correct+1
        return q(f"True or False: {given} + {shown} = 10", "fill", "____ (True/False)")
    def missing(i, sheet):
        n = random.randint(2,9)
        return q(f"{n} + {n} = ____  (this is a double)", "diagram", "____", "", "number_bond_blank", {"known": n})
    def numeral(i, sheet):
        given = random.randint(2,9)
        return q(f"{given} + ____ = 10", "fill", "____")
    def multisel(i, sheet):
        opts = ["3+7", "4+6", "2+9", "5+5"]
        return q(f"Which make exactly 10? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        nums = random.sample(range(2,9), 3)
        lefts = [f"{n}+{n}" for n in nums]; rights = [str(n*2) for n in nums]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Bond to 10: how many more does a number need to reach 10?",
         "7 + 3 = 10, because 7 needs 3 more to fill the ten-frame.",
         "Doubles: adding a number to itself. 6 + 6 = 12."],
        "make_ten_frame_blank", {"given": 7},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=130)


def _N_s(sheet):
    def comp(i, sheet):
        a = random.randint(15, 60); b = random.randint(15, 60)
        return q(f"{a} + {b} = ____  (move to a friendly number first)", "diagram", "____",
                  "", "decimal_numberline_blank", {"lo": a, "hi": a+b+5, "divisions": 8})
    def tf(i, sheet):
        a, b = random.randint(15,60), random.randint(15,60)
        correct = a+b
        shown = correct if random.random() > 0.4 else correct+5
        return q(f"True or False: {a} + {b} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a = random.randint(15,60); target = random.randint(a+10, a+50)
        return q(f"{a} + ____ = {target}", "fill", "____")
    def numeral(i, sheet):
        a, b = random.randint(15,60), random.randint(15,60)
        return q(f"{a} + {b} = ____", "fill", "____")
    def multisel(i, sheet):
        target = random.randint(40,80)
        opts = [f"{target-10}+10", f"{target}+0", f"{target+5}-5", f"{target+20}-20"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(random.randint(15,60), random.randint(15,60)) for _ in range(3)]
        lefts = [f"{a}+{b}" for a,b in pairs]; rights = [str(a+b) for a,b in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Move one number to a nearby 'friendly' (round) number, then adjust back.",
         "36 + 56: 36 is 4 away from 40. 40+56=96, then 96-4=92. So 36+56=92."],
        "decimal_numberline_example", {"value": 40, "lo": 30, "hi": 60, "divisions": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=140)


def _CUM6_s(sheet):
    def comp(i, sheet):
        if i % 2 == 0:
            given = random.randint(2,9)
            return q(f"{given} + ____ = 10", "diagram", "____", "", "make_ten_frame_blank", {"given": given})
        a, b = random.randint(15,60), random.randint(15,60)
        return q(f"{a} + {b} = ____", "diagram", "____", "", "decimal_numberline_blank", {"lo":a,"hi":a+b+5,"divisions":8})
    def tf(i, sheet):
        n = random.randint(2,9); correct = n*2
        shown = correct if random.random() > 0.4 else correct+1
        return q(f"True or False: {n} + {n} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        given = random.randint(2,9)
        return q(f"{given} + ____ = 10", "fill", "____")
    def numeral(i, sheet):
        a, b = random.randint(15,60), random.randint(15,60)
        return q(f"{a} + {b} = ____", "fill", "____")
    def multisel(i, sheet):
        opts = ["3+7", "4+6", "2+9", "5+5"]
        return q(f"Which make exactly 10? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        nums = random.sample(range(2,9), 3)
        lefts = [f"{n}+{n}" for n in nums]; rights = [str(n*2) for n in nums]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of bond-to-10, doubles, and compensation."],
        "make_ten_frame_blank", {"given": 7},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=600)


# ───────────────────────── O/P: Puzzles (with fun formats) ─────────────────────────

def _O_s(sheet):
    """Tier 1 puzzles: standard formats + a fun-format finale block."""
    def gen(sheet):
        a = random.randint(10,40); b = random.randint(5,20)
        return (a, b)
    def comp(i, sheet):
        a, b = gen(sheet)
        return q(f"What number plus {b} equals {a+b}? ____", "diagram", "____", "", "regroup_ones_blank", {"ones1":a%10,"ones2":b%10})
    def tf(i, sheet):
        a, b = gen(sheet); correct = a+b
        shown = correct if random.random() > 0.4 else correct+3
        return q(f"True or False: a number plus {b} equals {shown}, and that number is {a}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b = gen(sheet)
        return q(f"What number minus {b} equals {max(a-b,0)}? ____", "diagram", "____", "", "regroup_break_blank", {"tens":a//10,"ones":a%10})
    def numeral(i, sheet):
        a, b = gen(sheet)
        return q(f"What number plus {b} equals {a+b}? ____", "fill", "____")
    def multisel(i, sheet):
        a, b = gen(sheet)
        target = a + b
        opts = [f"{a}+{b}", f"{a+1}+{b-1}" if b > 1 else f"{a}+{b}", f"{a-1}+{b+1}" if a > 1 else f"{a}+{b}", f"{target}+0"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{a}+{b}" for a, b in pairs]; rights = [str(a+b) for a, b in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        a, b = gen(sheet)
        return maze_q(a%10, b%10 or 3, 2, 4)
    def fun2(i, sheet):
        return function_machine_q(random.randint(2,9), ["+ 3"], mode=random.choice(["forward","reverse"]))
    def fun3(i, sheet):
        base = random.randint(2,6)
        given = {(3,0): base, (3,1): base+1, (3,2): base+2, (3,3): base+3}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        a1, a2, a3 = random.randint(2,4), random.randint(5,8), random.randint(2,6)
        parts = [(f"{a1}+1", a1+1), (f"{a2}-1", a2-1), (f"{a3}+2", a3+2)]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        l = [str(random.randint(2,9)) + "+" + str(random.randint(2,9)) for _ in range(3)]
        vals = [eval(x) for x in l]
        return matching_q(l, [str(v) for v in vals])
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Worked Example", ["Work backwards: undo the operation to find the missing number."],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "First 15: standard puzzle formats. Last 5: fun formats (maze, function machine, pyramid, code breaker, matching)!",
        fmt, fun_builders, sheet, seed_base=150)


def _P_s(sheet):
    """Tier 2: harder puzzles + fun-format finale."""
    riddles = [
        "Two numbers add to {s}. One is {d} more than the other. Find both.",
        "I am between {lo} and {hi}. I am even. What could I be?",
        "I am between {lo} and {hi}. My digits add to {ds}. What could I be?",
    ]
    def gen(sheet):
        return (random.randint(10,40), random.randint(10,40)+10)
    def comp(i, sheet):
        lo = random.randint(10,40); hi = lo+10; s = random.randint(20,60); d = random.randint(2,10); ds = random.randint(5,12)
        txt = riddles[i % len(riddles)].format(s=s, d=d, lo=lo, hi=hi, ds=ds)
        return q(txt, "diagram", "____", "", "regroup_ones_blank", {"ones1": 5, "ones2": 3})
    def tf(i, sheet):
        lo, hi = random.randint(10,30), random.randint(31,50)
        n = random.randint(lo, hi)
        return q(f"True or False: {n} is between {lo} and {hi}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        s, d = random.randint(20,60), random.randint(2,10)
        return q(f"Two numbers add to {s}, one is {d} more. The smaller is ____.", "fill", "____")
    def numeral(i, sheet):
        lo = random.randint(10,40); hi = lo+10
        return q(f"I am between {lo} and {hi} and even. What could I be? ____", "fill", "____")
    def multisel(i, sheet):
        a, b = gen(sheet)
        target = a + b
        opts = [f"{a}+{b}", f"{a+1}+{b-1}" if b > 1 else f"{a}+{b}", f"{a-1}+{b+1}" if a > 1 else f"{a}+{b}", f"{target}+0"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{a}+{b}" for a, b in pairs]; rights = [str(a+b) for a, b in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(3,9), random.randint(2,6), 3, 5)
    def fun2(i, sheet):
        return function_machine_q(random.randint(2,9), ["+ 4", "- 1"], mode="forward")
    def fun3(i, sheet):
        base = random.randint(3,7)
        given = {(3,0): base, (3,1): base+2, (3,2): base+1, (3,3): base+3}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"{random.randint(2,5)}+3", None), (f"{random.randint(4,7)}-2", None)]
        parts = [(e, eval(e)) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        l = [f"{random.randint(10,30)}+{random.randint(5,20)}" for _ in range(3)]
        vals = [eval(x) for x in l]
        return matching_q(l, [str(v) for v in vals])
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Worked Example (Harder)",
        ["These puzzles need extra thinking -- try a few numbers and check if they fit ALL the clues."],
        "number_bond_blank", {"known": 5},
        "First 15: harder puzzle formats. Last 5: fun formats!",
        fmt, fun_builders, sheet, seed_base=160)


# ───────────────────────── Q/R/REV: Speed, Mixed, Revision (fun formats) ─────────────────────────

def _Q_s(sheet):
    def gen(sheet):
        a = random.randint(10,70); b = random.randint(5,29)
        return (a, b)
    def comp(i, sheet):
        a, b = gen(sheet)
        return q(f"{a} + {b} = ____", "diagram", "____", "", "regroup_ones_blank", {"ones1":a%10,"ones2":b%10})
    def tf(i, sheet):
        a, b = gen(sheet); correct = a+b
        shown = correct if random.random() > 0.4 else correct+2
        return q(f"True or False: {a} + {b} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a = random.randint(10,70); b = random.randint(1,a)
        return q(f"{a} - ____ = {a-b}", "fill", "____")
    def numeral(i, sheet):
        a, b = gen(sheet)
        return q(f"{a} + {b} = ____", "fill", "____")
    def multisel(i, sheet):
        a, b = gen(sheet)
        target = a + b
        opts = [f"{a}+{b}", f"{a+1}+{b-1}" if b > 1 else f"{a}+{b}", f"{a-1}+{b+1}" if a > 1 else f"{a}+{b}", f"{target}+0"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{a}+{b}" for a, b in pairs]; rights = [str(a+b) for a, b in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(2,8), random.randint(2,6), 2, 4)
    def fun2(i, sheet):
        return function_machine_q(random.randint(2,9), ["+ 5"], mode=random.choice(["forward","reverse"]))
    def fun3(i, sheet):
        base = random.randint(2,6)
        given = {(3,0): base, (3,1): base+1, (3,2): base, (3,3): base+2}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"{random.randint(2,5)}+2", None), (f"{random.randint(4,7)}+1", None)]
        parts = [(e, eval(e)) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        l = [f"{random.randint(10,50)}+{random.randint(5,25)}" for _ in range(3)]
        vals = [eval(x) for x in l]
        return matching_q(l, [str(v) for v in vals])
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Worked Example", ["Speed round: work quickly but carefully."],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "First 15: speed practice. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=170)


def _R_s(sheet):
    def gen(sheet):
        a = random.randint(10,70); b = random.randint(5,29)
        return (a, b)
    def comp(i, sheet):
        a, b = gen(sheet); op = "+" if i % 2 == 0 else "-"
        b = min(b, a) if op == "-" else b
        dfn = "regroup_ones_blank" if op == "+" else "regroup_break_blank"
        dp = {"ones1":a%10,"ones2":b%10} if op == "+" else {"tens":a//10,"ones":a%10}
        return q(f"{a} {op} {b} = ____", "diagram", "____", "", dfn, dp)
    def tf(i, sheet):
        given = random.randint(2,9)
        return q(f"True or False: {given} + {10-given} = 10", "fill", "____ (True/False)")
    def missing(i, sheet):
        n = random.randint(2,9)
        return q(f"{n} + {n} = ____", "fill", "____")
    def numeral(i, sheet):
        a, b = gen(sheet); op = "+" if i % 2 == 0 else "-"
        b = min(b, a) if op == "-" else b
        return q(f"{a} {op} {b} = ____", "fill", "____")
    def multisel(i, sheet):
        a, b = gen(sheet)
        target = a + b
        opts = [f"{a}+{b}", f"{a+1}+{b-1}" if b > 1 else f"{a}+{b}", f"{a-1}+{b+1}" if a > 1 else f"{a}+{b}", f"{target}+0"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{a}+{b}" for a, b in pairs]; rights = [str(a+b) for a, b in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(2,9), random.randint(2,6), 3, 5)
    def fun2(i, sheet):
        return function_machine_q(random.randint(2,9), ["+ 3", "+ 2"], mode="forward")
    def fun3(i, sheet):
        base = random.randint(2,6)
        given = {(3,0): base, (3,1): base+2, (3,2): base+1, (3,3): base}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"{random.randint(2,6)}+1", None), (f"{random.randint(3,7)}+2", None)]
        parts = [(e, eval(e)) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        l = [f"{random.randint(10,60)}-{random.randint(2,9)}" for _ in range(3)]
        vals = [eval(x) for x in l]
        return matching_q(l, [str(v) for v in vals])
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Worked Example", ["Mixed challenge: every addition and subtraction skill from this level."],
        "regroup_break_blank", {"tens": 4, "ones": 3},
        "First 15: mixed review. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=180)


def _REV_s(sheet):
    def gen(sheet):
        a = random.randint(10,70); b = random.randint(5,29)
        return (a, b)
    def comp(i, sheet):
        a, b = gen(sheet); op = "+" if i % 2 == 0 else "-"
        b = min(b, a) if op == "-" else b
        dfn = "regroup_ones_blank" if op == "+" else "regroup_break_blank"
        dp = {"ones1":a%10,"ones2":b%10} if op == "+" else {"tens":a//10,"ones":a%10}
        return q(f"{a} {op} {b} = ____", "diagram", "____", "", dfn, dp)
    def tf(i, sheet):
        a, b = gen(sheet); correct = a+b
        shown = correct if random.random() > 0.4 else correct+2
        return q(f"True or False: {a} + {b} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a = random.randint(10,70); t = random.randint(a,a+30)
        return q(f"{a} + ____ = {t}", "fill", "____")
    def numeral(i, sheet):
        a, b = gen(sheet); op = "+" if i % 2 == 0 else "-"
        b = min(b, a) if op == "-" else b
        return q(f"{a} {op} {b} = ____", "fill", "____")
    def multisel(i, sheet):
        a, b = gen(sheet)
        target = a + b
        opts = [f"{a}+{b}", f"{a+1}+{b-1}" if b > 1 else f"{a}+{b}", f"{a-1}+{b+1}" if a > 1 else f"{a}+{b}", f"{target}+0"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{a}+{b}" for a, b in pairs]; rights = [str(a+b) for a, b in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(2,9), random.randint(2,6), 2, 4)
    def fun2(i, sheet):
        return function_machine_q(random.randint(2,9), ["+ 3"], mode=random.choice(["forward","reverse"]))
    def fun3(i, sheet):
        base = random.randint(2,6)
        given = {(3,0): base, (3,1): base+1, (3,2): base+2, (3,3): base+1}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"{random.randint(2,5)}+1", None), (f"{random.randint(3,6)}+3", None)]
        parts = [(e, eval(e)) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        l = [f"{random.randint(10,60)}+{random.randint(5,25)}" for _ in range(3)]
        vals = [eval(x) for x in l]
        return matching_q(l, [str(v) for v in vals])
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Level 3 Revision",
        ["Every addition and subtraction skill: carrying, borrowing, mental math, and word problems."],
        "regroup_break_blank", {"tens": 4, "ones": 3},
        "First 15: full revision. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=700)


# ───────────────────────── Dispatcher (REPLACES original Level 3) ─────────────────────────

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL3_V2_DISPATCH = {
    "3A": _wrap(_A_s), "3B": _wrap(_B_s), "3C": _wrap(_C_s), "3CUM1": _wrap(_CUM1_s),
    "3D": _wrap(_D_s), "3E": _wrap(_E_s), "3CUM2": _wrap(_CUM2_s),
    "3F": _wrap(_F_s), "3G": _wrap(_G_s), "3CUM3": _wrap(_CUM3_s),
    "3H": _wrap(_H_s), "3I": _wrap(_I_s), "3J": _wrap(_J_s), "3CUM4": _wrap(_CUM4_s),
    "3K": _wrap(_K_s), "3L": _wrap(_L_s), "3CUM5": _wrap(_CUM5_s),
    "3M": _wrap(_M_s), "3N": _wrap(_N_s), "3CUM6": _wrap(_CUM6_s),
    "3O": _wrap(_O_s), "3P": _wrap(_P_s),
    "3Q": _wrap(_Q_s), "3R": _wrap(_R_s), "3REV": _wrap(_REV_s),
}
