"""
Fear Less Maths — LEVEL 4 REDESIGN v3 (Multiplication, Grade 2-3)

v3 applies the full question_formats.py rotation architecture plus the
fun-format pool (Math Maze, Function Machine, Number Pyramid, Code
Breaker, proper vertical Matching) to the Speed/Puzzle/Mixed
sub-levels. All v2 pedagogical content (researched times-table order,
table-to-table connections, squares explicitly defined, split method
taught, tiered word problems, tiered puzzles) is preserved exactly.
"""
import random
from content import cb, tb, q
from question_formats import (TEMPLATES, diff_range, make_rotated_sheet, make_fun_sheet,
                               make_format_builders, matching_q, maze_q, function_machine_q,
                               pyramid_q, codebreaker_q)


def _array_params(rows, cols):
    return {"rows": rows, "cols": cols}


# ───────────────────────── A: Concept ─────────────────────────

def _A_s(sheet):
    def gen(sheet):
        return (random.randint(2,4), random.randint(2,5))
    fmt = make_format_builders(gen, "equal_groups_blank", lambda g,s: {"groups": g, "size": s}, "x", lambda g,s: g*s)
    return make_rotated_sheet(
        "Worked Example",
        ["Multiplication means adding the same group over and over.",
         "3 groups of 4 = 4+4+4 = 3 x 4 = 12. An array shows the same idea as rows and columns."],
        "equal_groups_example", {"groups": 3, "size": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=10)


# ───────────────────────── B/C/D/CUM1: Easy tables ─────────────────────────

def _B_s(sheet):
    def gen(sheet):
        n = random.randint(1,9)
        return (n, random.choice([0,1]))
    fmt = make_format_builders(gen, "array_blank", lambda n,m: {"rows": max(m,1), "cols": n}, "x", lambda n,m: n*m)
    return make_rotated_sheet(
        "Worked Example",
        ["Any number x 1 stays the same -- 1 group of that size.",
         "Any number x 0 is always 0 -- 0 groups means nothing there."],
        "array_example", {"rows": 1, "cols": 5},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=20)


def _C_s(sheet):
    def gen(sheet):
        n = random.randint(1,9)
        return (n, random.choice([2,10]))
    fmt = make_format_builders(gen, "array_blank", lambda n,m: {"rows": m, "cols": n}, "x", lambda n,m: n*m)
    return make_rotated_sheet(
        "Worked Example", ["x2 means double the number.", "x10 means add a zero -- 7 x 10 = 70."],
        "array_example", {"rows": 2, "cols": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=30)


def _D_s(sheet):
    def gen(sheet):
        return (random.randint(1,9), 5)
    fmt = make_format_builders(gen, "array_blank", lambda n,m: {"rows": m, "cols": n}, "x", lambda n,m: n*m)
    return make_rotated_sheet(
        "Worked Example",
        ["x5 is HALF of x10 -- you already know your x10 facts!",
         "6 x 5: first 6 x 10 = 60, then half of 60 = 30."],
        "array_example", {"rows": 5, "cols": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=40)


def _CUM1_s(sheet):
    def gen(sheet):
        n = random.randint(1,9); m = random.choice([0,1,2,5,10])
        return (n, m)
    fmt = make_format_builders(gen, "array_blank", lambda n,m: {"rows": max(m,1), "cols": n}, "x", lambda n,m: n*m)
    return make_rotated_sheet(
        "Review", ["Mix of x0, x1, x2, x10, and x5."],
        "array_example", {"rows": 2, "cols": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=100)


# ───────────────────────── E/F/CUM2: Linked tables ─────────────────────────

def _E_s(sheet):
    def gen(sheet):
        return (random.randint(1,9), random.choice([3,4]))
    fmt = make_format_builders(gen, "array_blank", lambda n,m: {"rows": m, "cols": n}, "x", lambda n,m: n*m)
    return make_rotated_sheet(
        "Worked Example",
        ["x4 is DOUBLE your x2 facts!", "6 x 4: first 6 x 2 = 12, then double 12 = 24."],
        "array_example", {"rows": 4, "cols": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=50)


def _F_s(sheet):
    def gen(sheet):
        return (random.randint(1,9), random.choice([6,9]))
    fmt = make_format_builders(gen, "array_blank", lambda n,m: {"rows": m, "cols": n}, "x", lambda n,m: n*m)
    return make_rotated_sheet(
        "Worked Example",
        ["x9 is x10 MINUS one group -- one less than the x10 fact.",
         "7 x 9: first 7 x 10 = 70, then subtract one 7: 70 - 7 = 63."],
        "array_example", {"rows": 9, "cols": 7},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=60)


def _CUM2_s(sheet):
    def gen(sheet):
        return (random.randint(1,9), random.choice([3,4,6,9]))
    fmt = make_format_builders(gen, "array_blank", lambda n,m: {"rows": m, "cols": n}, "x", lambda n,m: n*m)
    return make_rotated_sheet(
        "Review", ["Mix of x3, x4 (double x2), x6, and x9 (x10 minus one group)."],
        "array_example", {"rows": 9, "cols": 7},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=200)


# ───────────────────────── G/H/CUM3: Hardest tables ─────────────────────────

def _G_s(sheet):
    def gen(sheet):
        return (random.randint(1,9), 8)
    fmt = make_format_builders(gen, "array_blank", lambda n,m: {"rows": m, "cols": n}, "x", lambda n,m: n*m)
    return make_rotated_sheet(
        "Worked Example",
        ["x8 is DOUBLE your x4 facts (which were already double x2)!",
         "6 x 8: 6 x 4 = 24, then double 24 = 48."],
        "array_example", {"rows": 8, "cols": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=70)


def _H_s(sheet):
    def gen(sheet):
        return (random.randint(1,9), 7)
    fmt = make_format_builders(gen, "array_blank", lambda n,m: {"rows": m, "cols": n}, "x", lambda n,m: n*m)
    return make_rotated_sheet(
        "Worked Example",
        ["x7 is the last one -- use facts you already know to find it.",
         "6 x 7: you know 6 x 6 = 36, so add one more 6: 36 + 6 = 42."],
        "array_example", {"rows": 7, "cols": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=80)


def _CUM3_s(sheet):
    def gen(sheet):
        return (random.randint(1,9), random.choice([7,8]))
    fmt = make_format_builders(gen, "array_blank", lambda n,m: {"rows": m, "cols": n}, "x", lambda n,m: n*m)
    return make_rotated_sheet(
        "Review", ["The two hardest tables: x7 and x8. Use your connection strategies."],
        "array_example", {"rows": 8, "cols": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=300)


# ───────────────────────── I/J/CUM4: Squares & multi-digit ─────────────────────────

def _I_s(sheet):
    def gen(sheet):
        n = random.randint(2,9)
        return (n, n)
    fmt = make_format_builders(gen, "array_blank", lambda n,m: {"rows": m, "cols": n}, "x", lambda n,m: n*m)
    return make_rotated_sheet(
        "Worked Example",
        ["A SQUARE NUMBER is a number multiplied by itself -- it makes a perfect square array.",
         "4 x 4 = 16 is a square number, because the array is a perfect square shape."],
        "array_example", {"rows": 5, "cols": 5},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=90)


def _J_s(sheet):
    def comp(i, sheet):
        tens = random.randint(1,4); ones = random.randint(1,9); n = tens*10+ones; m = random.randint(2,5)
        return q(f"{n} x {m} = ({tens}0 x {m}) + ({ones} x {m}) = ____", "diagram", "____", "", "array_blank", {"rows": m, "cols": ones})
    def tf(i, sheet):
        tens = random.randint(1,4); ones = random.randint(1,9); n = tens*10+ones; m = random.randint(2,5)
        correct = n*m
        shown = correct if random.random() > 0.4 else correct+m
        return q(f"True or False: {n} x {m} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        tens = random.randint(1,4); ones = random.randint(1,9); n = tens*10+ones; m = random.randint(2,5)
        return q(f"{n} x ____ = {n*m}  (what number was it multiplied by?)", "diagram", "____", "", "array_blank", {"rows": m, "cols": ones})
    def numeral(i, sheet):
        tens = random.randint(1,4); ones = random.randint(1,9); n = tens*10+ones; m = random.randint(2,5)
        return q(f"{n} x {m} = ____", "fill", "____")
    def multisel(i, sheet):
        m = random.randint(2,5); target = 20*m
        opts = [f"20x{m}", f"10x{m*2}", f"{20+5}x{m}", f"4x{5*m}"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(random.randint(11,40), random.randint(2,5)) for _ in range(3)]
        lefts = [f"{n}x{m}" for n,m in pairs]; rights = [str(n*m) for n,m in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Split the bigger number into tens and ones, multiply each part, then add.",
         "21 x 3 = (20 x 3) + (1 x 3) = 60 + 3 = 63."],
        "array_example", {"rows": 3, "cols": 1},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=95)


def _CUM4_s(sheet):
    def comp(i, sheet):
        if i % 2 == 0:
            n = random.randint(2,9); return q(f"{n} x {n} = ____", "diagram", "____", "", "array_blank", {"rows":n,"cols":n})
        tens=random.randint(1,4); ones=random.randint(1,9); m=random.randint(2,5)
        return q(f"{tens*10+ones} x {m} = ____", "diagram", "____", "", "array_blank", {"rows":m,"cols":ones})
    def tf(i, sheet):
        n = random.randint(2,9); correct = n*n
        shown = correct if random.random() > 0.4 else correct+n
        return q(f"True or False: {n} x {n} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        n = random.randint(2,9)
        return q(f"____ x {n} = {n*n}  (square of {n})", "fill", "____")
    def numeral(i, sheet):
        tens=random.randint(1,4); ones=random.randint(1,9); m=random.randint(2,5)
        return q(f"{tens*10+ones} x {m} = ____", "fill", "____")
    def multisel(i, sheet):
        opts = ["3x3", "4x4", "5x6", "6x6"]
        return q(f"Which are SQUARE numbers (n x n)? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        ns = random.sample(range(2,9), 3)
        lefts = [f"{n}x{n}" for n in ns]; rights = [str(n*n) for n in ns]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of square numbers and the split method for bigger numbers."],
        "array_example", {"rows": 5, "cols": 5},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=400)


# ───────────────────────── K/L/CUM5: Word problems (tiered) ─────────────────────────

def _K_s(sheet):
    templates = ["{g} packs of {s} biscuits. Total biscuits = ____.", "{g} baskets with {s} mangoes each. Total mangoes = ____.", "{g} rows of {s} chairs. Total chairs = ____."]
    def gen(sheet):
        return (random.randint(2,6), random.randint(2,9))
    def comp(i, sheet):
        g, s = gen(sheet)
        return q(random.choice(templates).format(g=g,s=s), "diagram", "____", "", "equal_groups_blank", {"groups": g, "size": s})
    def tf(i, sheet):
        g, s = gen(sheet); correct = g*s
        shown = correct if random.random() > 0.4 else correct+s
        return q(f"True or False: {g} packs of {s} = {shown} total.", "fill", "____ (True/False)")
    def missing(i, sheet):
        g, s = gen(sheet)
        return q(f"{g} packs of ____ biscuits = {g*s} total. Size of each pack?", "fill", "____")
    def numeral(i, sheet):
        g, s = gen(sheet)
        return q(random.choice(templates).format(g=g,s=s), "fill", "____")
    def multisel(i, sheet):
        target = random.randint(12,30)
        opts = [f"{target//2} packs of 2", f"{target} packs of 1", f"{target//3} packs of 3" if target%3==0 else f"{target//2} packs of 2", f"1 pack of {target}"]
        return q(f"Which give {target} total? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{g} packs of {s}" for g,s in pairs]; rights = [str(g*s) for g,s in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example", ["Find the number of groups and the size of each group, then multiply."],
        "equal_groups_example", {"groups": 3, "size": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=110)


def _L_s(sheet):
    def gen(sheet):
        return (random.randint(2,5), random.randint(2,5), random.randint(2,4))
    def comp(i, sheet):
        a, b, c = gen(sheet)
        return q(f"(Two steps) {a} boxes of {b} packets, each packet has {c} items. Total = ____.",
                  "diagram", "____", "", "equal_groups_blank", {"groups": a*b, "size": c})
    def tf(i, sheet):
        a, b, c = gen(sheet); correct = a*b*c
        shown = correct if random.random() > 0.4 else correct+c
        return q(f"True or False: {a} boxes of {b} packets ({c} each) = {shown} items.", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b, c = gen(sheet)
        return q(f"{a} boxes of {b} packets = ____ packets total.", "fill", "____")
    def numeral(i, sheet):
        a, b, c = gen(sheet)
        return q(f"{a} boxes of {b} packets, {c} items each. Total = ____.", "fill", "____")
    def multisel(i, sheet):
        target = random.randint(24,60)
        opts = [f"{target//2} x 2", f"{target} x 1", f"{target//3} x 3" if target%3==0 else f"{target//2} x 2", f"{target//4} x 4" if target%4==0 else f"{target//2} x 2"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{a}x{b} boxes, {c} each" for a,b,c in pairs]; rights = [str(a*b*c) for a,b,c in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Two-step problems need TWO multiplications. Solve the first part, then use that answer.",
         "3 boxes of 4 packets = 12 packets. 12 packets x 2 items = 24 items total."],
        "equal_groups_example", {"groups": 3, "size": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=120)


def _CUM5_s(sheet):
    def gen(sheet):
        return (random.randint(2,6), random.randint(2,9))
    def comp(i, sheet):
        g, s = gen(sheet)
        return q(f"{g} groups of {s}. Total = ____.", "diagram", "____", "", "equal_groups_blank", {"groups":g,"size":s})
    def tf(i, sheet):
        g, s = gen(sheet); correct = g*s
        shown = correct if random.random() > 0.4 else correct+s
        return q(f"True or False: {g} groups of {s} = {shown}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        g, s = gen(sheet)
        return q(f"____ groups of {s} = {g*s}. How many groups?", "fill", "____")
    def numeral(i, sheet):
        a,b,c = random.randint(2,4), random.randint(2,4), random.randint(2,4)
        return q(f"{a} boxes of {b} packets, {c} each. Total = ____.", "fill", "____")
    def multisel(i, sheet):
        target = random.randint(12,30)
        opts = [f"{target//2}x2", f"{target}x1", f"{target//3}x3" if target%3==0 else f"{target//2}x2", f"1x{target}"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{g} groups of {s}" for g,s in pairs]; rights = [str(g*s) for g,s in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of one-step and two-step word problems."],
        "equal_groups_example", {"groups": 3, "size": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=500)


# ───────────────────────── M: Patterns ─────────────────────────

def _M_s(sheet):
    def comp(i, sheet):
        step = random.choice([2,3,4,5,6]); start = step*random.randint(1,4)
        return q(f"{start}, {start+step}, {start+step*2}, ____  (skip count by {step})",
                  "diagram", "____", "", "array_blank", {"rows": 1, "cols": step})
    def tf(i, sheet):
        step = random.choice([2,3,4,5]); start = step*random.randint(1,4)
        correct = start+step*3
        shown = correct if random.random() > 0.4 else correct+1
        return q(f"True or False: {start}, {start+step}, {start+step*2}, {shown} continues the pattern.", "fill", "____ (True/False)")
    def missing(i, sheet):
        step = random.choice([3,4,5,6]); start = step*random.randint(1,4)
        return q(f"{start}, {start+step}, ____, {start+step*3}", "diagram", "____", "", "array_blank", {"rows":1,"cols":step})
    def numeral(i, sheet):
        step = random.choice([2,3,4,5,6]); start = step*random.randint(1,4)
        return q(f"{start}, {start+step}, {start+step*2}, ____", "fill", "____")
    def multisel(i, sheet):
        step = random.choice([3,4,5]); start = step*random.randint(2,5)
        opts = [str(start+step), str(start+step+1), str(start-step), str(start+step*2)]
        return q(f"Which fit the pattern ...,{start},___,...(step {step})? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        steps = random.sample([2,3,4,5], 3)
        lefts = [f"skip count by {s} from {s}" for s in steps]
        rights = [f"{s},{2*s},{3*s}" for s in steps]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example", ["Each table is a skip-counting pattern -- the same jump size every time."],
        "array_example", {"rows": 1, "cols": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=130)


# ───────────────────────── N: Speed (fun formats) ─────────────────────────

def _N_s(sheet):
    def gen(sheet):
        n = random.randint(1,9); table = random.choice([2,4,5,8,9,10])
        return (n, table)
    def comp(i, sheet):
        n, table = gen(sheet)
        return q(f"{n} x {table} = ____", "diagram", "____", "", "array_blank", {"rows": table, "cols": n})
    def tf(i, sheet):
        n, table = gen(sheet); correct = n*table
        shown = correct if random.random() > 0.4 else correct+table
        return q(f"True or False: {n} x {table} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        n, table = gen(sheet)
        return q(f"{n} x ____ = {n*table}", "fill", "____")
    def numeral(i, sheet):
        n, table = gen(sheet)
        return q(f"{n} x {table} = ____", "fill", "____")
    def multisel(i, sheet):
        n, table = gen(sheet)
        target = n * table
        opts = [f"{n}x{table}", f"{n+1}x{table}", f"{n}x{table+1}", f"{target}x1"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{n}x{t}" for n, t in pairs]; rights = [str(n*t) for n, t in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        n = random.randint(2,8)
        return maze_q(n, random.randint(2,5), 2, 3)
    def fun2(i, sheet):
        table = random.choice([2,3,4,5])
        return function_machine_q(random.randint(2,9), [f"x {table}"], mode=random.choice(["forward","reverse"]))
    def fun3(i, sheet):
        base = random.randint(2,5)
        given = {(3,0): base, (3,1): base+1, (3,2): base, (3,3): base+1}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"2x{random.randint(2,4)}", None), (f"3x{random.randint(2,3)}", None)]
        parts = [(e, eval(e.replace("x", "*"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        pairs = [(random.randint(2,9), random.choice([2,3,4,5])) for _ in range(3)]
        lefts = [f"{n}x{t}" for n,t in pairs]; rights = [str(n*t) for n,t in pairs]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Worked Example", ["Speed round: use the connection strategy you already learned for each table."],
        "array_example", {"rows": 8, "cols": 6},
        "First 15: speed practice. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=140)


def _CUM6_s(sheet):
    def gen(sheet):
        return (random.randint(1,9), random.choice([3,4,5,6]))
    def comp(i, sheet):
        if i % 2 == 0:
            step = random.choice([3,4,5,6]); start = step*random.randint(1,4)
            return q(f"{start}, {start+step}, ____, {start+step*3}", "diagram", "____", "", "array_blank", {"rows":1,"cols":step})
        n, table = gen(sheet)
        return q(f"{n} x {table} = ____", "diagram", "____", "", "array_blank", {"rows":table,"cols":n})
    def tf(i, sheet):
        n, table = gen(sheet); correct = n*table
        shown = correct if random.random() > 0.4 else correct+table
        return q(f"True or False: {n} x {table} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        n, table = gen(sheet)
        return q(f"{n} x ____ = {n*table}", "fill", "____")
    def numeral(i, sheet):
        n, table = gen(sheet)
        return q(f"{n} x {table} = ____", "fill", "____")
    def multisel(i, sheet):
        n, table = gen(sheet)
        target = n * table
        opts = [f"{n}x{table}", f"{n+1}x{table}", f"{n}x{table+1}", f"{target}x1"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{n}x{t}" for n, t in pairs]; rights = [str(n*t) for n, t in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(2,8), random.randint(2,5), 2, 3)
    def fun2(i, sheet):
        return function_machine_q(random.randint(2,9), ["x 2"], mode="forward")
    def fun3(i, sheet):
        base = random.randint(2,5)
        given = {(3,0): base, (3,1): base+1, (3,2): base, (3,3): base+2}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"2x{random.randint(2,4)}", None), (f"3x{random.randint(2,3)}", None)]
        parts = [(e, eval(e.replace("x", "*"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        pairs = [(random.randint(2,9), random.choice([2,3,4])) for _ in range(3)]
        lefts = [f"{n}x{t}" for n,t in pairs]; rights = [str(n*t) for n,t in pairs]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Review", ["Mix of patterns and speed facts."], "array_example", {"rows": 8, "cols": 6},
        "First 15: review. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=600)


# ───────────────────────── O/P: Puzzles (fun formats) ─────────────────────────

def _O_s(sheet):
    def comp(i, sheet):
        table = random.randint(3,9); lo = table*random.randint(2,4); hi = lo + table + 2
        return q(f"I am a multiple of {table}. I am between {lo} and {hi}. What am I?", "diagram", "____", "", "array_blank", {"rows": table, "cols": 1})
    def tf(i, sheet):
        table = random.randint(3,9); n = table*random.randint(2,5)
        return q(f"True or False: {n} is a multiple of {table}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        table = random.randint(3,9); n = random.randint(2,6)
        return q(f"{table} x ____ = {table*n}. What is the missing factor?", "fill", "____")
    def numeral(i, sheet):
        table = random.randint(3,9); lo = table*random.randint(2,4); hi = lo + table + 2
        return q(f"Multiple of {table}, between {lo} and {hi}? ____", "fill", "____")
    def multisel(i, sheet):
        table = random.randint(3,9); n = random.randint(2,6)
        target = n * table
        opts = [f"{n}x{table}", f"{n+1}x{table}", f"{n}x{table+1}", f"{target}x1"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(random.randint(2,9), random.randint(3,9)) for _ in range(3)]
        lefts = [f"{n}x{t}" for n, t in pairs]; rights = [str(n*t) for n, t in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(2,6), random.randint(2,5), 2, 3)
    def fun2(i, sheet):
        return function_machine_q(random.randint(2,7), [f"x {random.choice([2,3])}"], mode=random.choice(["forward","reverse"]))
    def fun3(i, sheet):
        base = random.randint(2,5)
        given = {(3,0): base, (3,1): base+1, (3,2): base+2, (3,3): base}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"2x{random.randint(2,4)}", None), (f"3x{random.randint(2,3)}", None)]
        parts = [(e, eval(e.replace("x", "*"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        pairs = [(random.randint(2,9), random.choice([2,3,4])) for _ in range(3)]
        lefts = [f"{n}x{t}" for n,t in pairs]; rights = [str(n*t) for n,t in pairs]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Worked Example", ["List the multiples of the table, then pick the one that fits between the two numbers."],
        "array_example", {"rows": 6, "cols": 5},
        "First 15: simple multiple puzzles. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=150)


def _P_s(sheet):
    def comp(i, sheet):
        if i % 2 == 0:
            a, b = random.sample([2,3,4,5,6], 2); limit = random.randint(20,40)
            return q(f"I am a multiple of BOTH {a} and {b}. I am less than {limit}. List me.", "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
        n = random.choice([12,16,18,20,24,30,36])
        return q(f"Find all factor pairs of {n}.", "diagram", "____", "", "array_blank", {"rows": 2, "cols": n//2})
    def tf(i, sheet):
        a, b = random.sample([2,3,4,5,6], 2); n = a*b
        return q(f"True or False: {n} is a multiple of both {a} and {b}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        n = random.choice([12,16,18,20,24])
        return q(f"{n} = ____ x 2. What is the other factor?", "fill", "____")
    def numeral(i, sheet):
        a, b = random.sample([2,3,4,5,6], 2); limit = random.randint(20,40)
        return q(f"Multiple of both {a} and {b}, less than {limit}? ____", "fill", "____")
    def multisel(i, sheet):
        table = random.randint(3,9); n = random.randint(2,6)
        target = n * table
        opts = [f"{n}x{table}", f"{n+1}x{table}", f"{n}x{table+1}", f"{target}x1"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(random.randint(2,9), random.randint(3,9)) for _ in range(3)]
        lefts = [f"{n}x{t}" for n, t in pairs]; rights = [str(n*t) for n, t in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(2,6), random.randint(2,5), 3, 4)
    def fun2(i, sheet):
        return function_machine_q(random.randint(2,7), [f"x {random.choice([3,4])}", "+ 1"], mode="forward")
    def fun3(i, sheet):
        base = random.randint(2,5)
        given = {(3,0): base, (3,1): base+2, (3,2): base+1, (3,3): base+3}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"3x{random.randint(2,3)}", None), (f"4x{random.randint(1,2)}", None)]
        parts = [(e, eval(e.replace("x", "*"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        pairs = [(random.randint(2,9), random.choice([2,3,4])) for _ in range(3)]
        lefts = [f"{n}x{t}" for n,t in pairs]; rights = [str(n*t) for n,t in pairs]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Worked Example (Harder)",
        ["A COMMON multiple fits BOTH tables. FACTOR PAIRS multiply to make the target."],
        "array_example", {"rows": 3, "cols": 4},
        "First 15: harder multiple/factor puzzles. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=160)


def _CUM7_s(sheet):
    def comp(i, sheet):
        choice = i % 2
        if choice == 0:
            table = random.randint(3,9); lo = table*random.randint(2,4); hi = lo+table+2
            return q(f"Multiple of {table}, between {lo} and {hi}?", "diagram", "____", "", "array_blank", {"rows":table,"cols":1})
        a,b = random.sample([2,3,4,5,6],2); limit = random.randint(20,40)
        return q(f"Multiple of both {a} and {b}, less than {limit}?", "diagram", "____", "", "array_blank", {"rows":a,"cols":b})
    def tf(i, sheet):
        table = random.randint(3,9); n = table*random.randint(2,5)
        return q(f"True or False: {n} is a multiple of {table}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        n = random.choice([12,16,18,20,24])
        return q(f"{n} = ____ x 2", "fill", "____")
    def numeral(i, sheet):
        table = random.randint(3,9); lo = table*random.randint(2,4); hi = lo+table+2
        return q(f"Multiple of {table}, between {lo} and {hi}? ____", "fill", "____")
    def multisel(i, sheet):
        table = random.randint(3,9); n = random.randint(2,6)
        target = n * table
        opts = [f"{n}x{table}", f"{n+1}x{table}", f"{n}x{table+1}", f"{target}x1"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(random.randint(2,9), random.randint(3,9)) for _ in range(3)]
        lefts = [f"{n}x{t}" for n, t in pairs]; rights = [str(n*t) for n, t in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(2,6), random.randint(2,5), 2, 3)
    def fun2(i, sheet):
        return function_machine_q(random.randint(2,7), [f"x {random.choice([2,3])}"], mode=random.choice(["forward","reverse"]))
    def fun3(i, sheet):
        base = random.randint(2,5)
        given = {(3,0): base, (3,1): base+1, (3,2): base+2, (3,3): base}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"2x{random.randint(2,4)}", None), (f"3x{random.randint(2,3)}", None)]
        parts = [(e, eval(e.replace("x", "*"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        pairs = [(random.randint(2,9), random.choice([2,3,4])) for _ in range(3)]
        lefts = [f"{n}x{t}" for n,t in pairs]; rights = [str(n*t) for n,t in pairs]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Review", ["Mix of simple and harder multiple/factor puzzles."], "array_example", {"rows": 3, "cols": 4},
        "First 15: review. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=700)


# ───────────────────────── Q/REV ─────────────────────────

def _Q_s(sheet):
    def gen(sheet):
        return (random.randint(1,9), random.randint(2,9))
    def comp(i, sheet):
        n, table = gen(sheet)
        if i % 3 == 0:
            return q(f"{n} x {n} = ____ (square)", "diagram", "____", "", "array_blank", {"rows":n,"cols":n})
        return q(f"{n} x {table} = ____", "diagram", "____", "", "array_blank", {"rows":table,"cols":n})
    def tf(i, sheet):
        n, table = gen(sheet); correct = n*table
        shown = correct if random.random() > 0.4 else correct+table
        return q(f"True or False: {n} x {table} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        n, table = gen(sheet)
        return q(f"{n} x ____ = {n*table}", "fill", "____")
    def numeral(i, sheet):
        n, table = gen(sheet)
        return q(f"{n} x {table} = ____", "fill", "____")
    def multisel(i, sheet):
        n, table = gen(sheet)
        target = n * table
        opts = [f"{n}x{table}", f"{n+1}x{table}", f"{n}x{table+1}", f"{target}x1"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{n}x{t}" for n, t in pairs]; rights = [str(n*t) for n, t in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(2,7), random.randint(2,5), 2, 3)
    def fun2(i, sheet):
        return function_machine_q(random.randint(2,8), [f"x {random.choice([2,3,4])}"], mode=random.choice(["forward","reverse"]))
    def fun3(i, sheet):
        base = random.randint(2,5)
        given = {(3,0): base, (3,1): base+1, (3,2): base+2, (3,3): base+1}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"2x{random.randint(2,4)}", None), (f"4x{random.randint(1,2)}", None)]
        parts = [(e, eval(e.replace("x", "*"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        pairs = [(random.randint(2,9), random.choice([2,3,4,5])) for _ in range(3)]
        lefts = [f"{n}x{t}" for n,t in pairs]; rights = [str(n*t) for n,t in pairs]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Worked Example", ["Mixed challenge: every multiplication skill from this level."],
        "array_example", {"rows": 6, "cols": 7},
        "First 15: mixed review. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=170)


def _REV_s(sheet):
    def gen(sheet):
        return (random.randint(1,9), random.randint(2,9))
    def comp(i, sheet):
        n, table = gen(sheet)
        choice = i % 4
        if choice == 0: return q(f"{n} x 1 = ____", "diagram", "____", "", "array_blank", {"rows":1,"cols":n})
        elif choice == 1: return q(f"{n} x {table} = ____", "diagram", "____", "", "array_blank", {"rows":table,"cols":n})
        elif choice == 2: return q(f"{n} x {n} = ____", "diagram", "____", "", "array_blank", {"rows":n,"cols":n})
        else:
            g,s = random.randint(2,6), random.randint(2,9)
            return q(f"{g} groups of {s}. Total = ____.", "diagram", "____", "", "equal_groups_blank", {"groups":g,"size":s})
    def tf(i, sheet):
        n, table = gen(sheet); correct = n*table
        shown = correct if random.random() > 0.4 else correct+table
        return q(f"True or False: {n} x {table} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        n, table = gen(sheet)
        return q(f"{n} x ____ = {n*table}", "fill", "____")
    def numeral(i, sheet):
        n, table = gen(sheet)
        return q(f"{n} x {table} = ____", "fill", "____")
    def multisel(i, sheet):
        n, table = gen(sheet)
        target = n * table
        opts = [f"{n}x{table}", f"{n+1}x{table}", f"{n}x{table+1}", f"{target}x1"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{n}x{t}" for n, t in pairs]; rights = [str(n*t) for n, t in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(2,7), random.randint(2,5), 2, 3)
    def fun2(i, sheet):
        return function_machine_q(random.randint(2,8), [f"x {random.choice([2,3])}"], mode=random.choice(["forward","reverse"]))
    def fun3(i, sheet):
        base = random.randint(2,5)
        given = {(3,0): base, (3,1): base+1, (3,2): base, (3,3): base+2}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"2x{random.randint(2,4)}", None), (f"3x{random.randint(2,3)}", None)]
        parts = [(e, eval(e.replace("x", "*"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        pairs = [(random.randint(2,9), random.choice([2,3,4])) for _ in range(3)]
        lefts = [f"{n}x{t}" for n,t in pairs]; rights = [str(n*t) for n,t in pairs]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Level 4 Revision",
        ["Every multiplication skill: tables, squares, word problems, patterns, and puzzles."],
        "array_example", {"rows": 6, "cols": 7},
        "First 15: full revision. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=800)


# ───────────────────────── Dispatcher (REPLACES original Level 4) ─────────────────────────

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL4_V2_DISPATCH = {
    "4A": _wrap(_A_s), "4B": _wrap(_B_s), "4C": _wrap(_C_s), "4D": _wrap(_D_s), "4CUM1": _wrap(_CUM1_s),
    "4E": _wrap(_E_s), "4F": _wrap(_F_s), "4CUM2": _wrap(_CUM2_s),
    "4G": _wrap(_G_s), "4H": _wrap(_H_s), "4CUM3": _wrap(_CUM3_s),
    "4I": _wrap(_I_s), "4J": _wrap(_J_s), "4CUM4": _wrap(_CUM4_s),
    "4K": _wrap(_K_s), "4L": _wrap(_L_s), "4CUM5": _wrap(_CUM5_s),
    "4M": _wrap(_M_s), "4N": _wrap(_N_s), "4CUM6": _wrap(_CUM6_s),
    "4O": _wrap(_O_s), "4P": _wrap(_P_s), "4CUM7": _wrap(_CUM7_s),
    "4Q": _wrap(_Q_s), "4REV": _wrap(_REV_s),
}
