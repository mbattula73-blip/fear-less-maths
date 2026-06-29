"""
Fear Less Maths — LEVEL 5 REDESIGN v3 (Division, Grade 3-4)

v3 applies the full question_formats.py rotation architecture plus the
fun-format pool (Math Maze, Function Machine, Number Pyramid, Code
Breaker, proper vertical Matching) to the Speed/Puzzle/Mixed
sub-levels. All v2 pedagogical content (easiest-divisor-first order,
the CHECK step taught, area-model + partial-quotients long division,
tiered word problems, missing-number strategy taught, /10-/100
separated from basic facts, LCM/digit puzzles taught) is preserved.
"""
import random
from content import cb, tb, q
from question_formats import (TEMPLATES, diff_range, make_rotated_sheet, make_fun_sheet,
                               make_format_builders, matching_q, maze_q, function_machine_q,
                               pyramid_q, codebreaker_q)


# ───────────────────────── A: Concept ─────────────────────────

def _A_s(sheet):
    def gen(sheet):
        divisor = random.choice([2,3,4,5]); groups = random.randint(2,6)
        return (divisor*groups, divisor)
    fmt = make_format_builders(gen, "array_blank", lambda dividend,d: {"rows": d, "cols": dividend//d}, "/", lambda dividend,d: dividend//d)
    return make_rotated_sheet(
        "Worked Example",
        ["Dividing means sharing or grouping equally.", "12 / 3 = 4: share 12 into 3 equal groups, each has 4."],
        "array_example", {"rows": 3, "cols": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=10)


# ───────────────────────── B/C/D/CUM1: Division facts ─────────────────────────

def _B_s(sheet):
    def gen(sheet):
        divisor = random.choice([2,5,10]); n = random.randint(1,9)
        return (divisor*n, divisor)
    fmt = make_format_builders(gen, "array_blank", lambda dividend,d: {"rows": d, "cols": dividend//d}, "/", lambda dividend,d: dividend//d)
    return make_rotated_sheet(
        "Worked Example", ["/2, /5, and /10 are the easiest -- they connect straight to your easiest times tables."],
        "array_example", {"rows": 2, "cols": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=20)


def _C_s(sheet):
    def gen(sheet):
        divisor = random.choice([3,4,6,9]); n = random.randint(1,9)
        return (divisor*n, divisor)
    fmt = make_format_builders(gen, "array_blank", lambda dividend,d: {"rows": d, "cols": dividend//d}, "/", lambda dividend,d: dividend//d)
    return make_rotated_sheet(
        "Worked Example", ["Use your x3, x4, x6, and x9 facts in reverse to divide."],
        "array_example", {"rows": 4, "cols": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=30)


def _D_s(sheet):
    def gen(sheet):
        divisor = random.choice([7,8]); n = random.randint(1,9)
        return (divisor*n, divisor)
    fmt = make_format_builders(gen, "array_blank", lambda dividend,d: {"rows": d, "cols": dividend//d}, "/", lambda dividend,d: dividend//d)
    return make_rotated_sheet(
        "Worked Example", ["/7 and /8 are the hardest -- use a known nearby fact and adjust if you're not sure."],
        "array_example", {"rows": 7, "cols": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=40)


def _CUM1_s(sheet):
    def gen(sheet):
        divisor = random.choice([2,3,4,5,6,7,8,9,10]); n = random.randint(1,9)
        return (divisor*n, divisor)
    fmt = make_format_builders(gen, "array_blank", lambda dividend,d: {"rows": d, "cols": dividend//d}, "/", lambda dividend,d: dividend//d)
    return make_rotated_sheet(
        "Review", ["Mix of all division facts, 2 through 10."],
        "array_example", {"rows": 4, "cols": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=100)


# ───────────────────────── E/F/CUM2: Remainders ─────────────────────────

def _E_s(sheet):
    def comp(i, sheet):
        divisor = random.choice([2,3,4,5]); groups = random.randint(2,6)
        leftover = random.randint(1, divisor-1); total = divisor*groups + leftover
        return q(f"{total} / {divisor} = ____ R ____", "diagram", "____  R  ____", "", "array_blank", {"rows": divisor, "cols": groups})
    def tf(i, sheet):
        divisor = random.choice([2,3,4,5]); groups = random.randint(2,6)
        leftover = random.randint(1, divisor-1); total = divisor*groups + leftover
        shown = leftover if random.random() > 0.4 else leftover+1
        return q(f"True or False: {total} / {divisor} = {groups} R {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        divisor = random.choice([2,3,4,5]); groups = random.randint(2,6)
        leftover = random.randint(1, divisor-1); total = divisor*groups + leftover
        return q(f"{total} / {divisor} = {groups} R ____", "fill", "____")
    def numeral(i, sheet):
        divisor = random.choice([2,3,4,5]); groups = random.randint(2,6)
        leftover = random.randint(1, divisor-1); total = divisor*groups + leftover
        return q(f"{total} / {divisor} = ____ R ____", "fill", "____  R  ____")
    def multisel(i, sheet):
        divisor = random.choice([3,4]); opts = []
        for k in range(4):
            g = random.randint(2,5); l = random.randint(0, divisor-1)
            opts.append(f"{divisor*g+l}/{divisor}")
        return q(f"Which division has NO remainder? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4,5])
        pairs = [(random.randint(2,5), random.randint(1,divisor-1)) for _ in range(3)]
        lefts = [f"{divisor*g+l}/{divisor}" for g,l in pairs]
        rights = [f"{g} R {l}" for g,l in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Sometimes things don't share evenly -- what's left over is the remainder.",
         "13 / 4: 3 groups of 4 = 12, with 1 left over. 13 / 4 = 3 R 1."],
        "array_example", {"rows": 4, "cols": 3},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=50)


def _F_s(sheet):
    def comp(i, sheet):
        divisor = random.choice([2,3,4,5,6]); groups = random.randint(2,6)
        leftover = random.randint(1, divisor-1); total = divisor*groups + leftover
        return q(f"{total} / {divisor} = ____ R ____.  Check: ____ x {divisor} + ____ = {total}",
                  "diagram", "____  R  ____", "", "array_blank", {"rows": divisor, "cols": groups})
    def tf(i, sheet):
        divisor = random.choice([2,3,4,5]); groups = random.randint(2,6); leftover = random.randint(1, divisor-1)
        total = divisor*groups + leftover; check = groups*divisor + leftover
        shown = "matches" if check == total else "does not match"
        return q(f"True or False: {groups} x {divisor} + {leftover} {shown} {total} (the check works).", "fill", "____ (True/False)")
    def missing(i, sheet):
        divisor = random.choice([2,3,4,5]); groups = random.randint(2,6); leftover = random.randint(1, divisor-1)
        total = divisor*groups + leftover
        return q(f"Check: {groups} x {divisor} + ____ = {total}", "fill", "____")
    def numeral(i, sheet):
        divisor = random.choice([2,3,4,5,6]); groups = random.randint(2,6); leftover = random.randint(1, divisor-1)
        total = divisor*groups + leftover
        return q(f"{total} / {divisor} = ____ R ____", "fill", "____  R  ____")
    def multisel(i, sheet):
        divisor, groups, leftover = 4, 3, 2; total = divisor*groups+leftover
        opts = [f"{groups}x{divisor}+{leftover}={total}", f"{groups}x{divisor}={total}", f"{groups+1}x{divisor}={total}", f"{groups}x{divisor}+{leftover+1}={total}"]
        return q(f"Which CHECK statements are correct? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4,5])
        pairs = [(random.randint(2,5), random.randint(1,divisor-1)) for _ in range(3)]
        lefts = [f"{divisor*g+l}/{divisor}" for g,l in pairs]; rights = [f"{g} R {l}" for g,l in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Always CHECK your division: quotient x divisor + remainder should equal the dividend.",
         "13 / 4 = 3 R 1. Check: 3 x 4 + 1 = 12 + 1 = 13. Correct!"],
        "array_example", {"rows": 4, "cols": 3},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=60)


def _CUM2_s(sheet):
    def comp(i, sheet):
        divisor = random.choice([2,3,4,5,6]); groups = random.randint(2,6); leftover = random.randint(1, divisor-1)
        total = divisor*groups + leftover
        return q(f"{total} / {divisor} = ____ R ____. Check your answer!", "diagram", "____  R  ____", "", "array_blank", {"rows": divisor, "cols": groups})
    def tf(i, sheet):
        divisor = random.choice([2,3,4,5]); groups = random.randint(2,6); leftover = random.randint(1, divisor-1)
        total = divisor*groups + leftover
        return q(f"True or False: {total} / {divisor} = {groups} R {leftover}", "fill", "____ (True/False)")
    def missing(i, sheet):
        divisor = random.choice([2,3,4,5]); groups = random.randint(2,6); leftover = random.randint(1, divisor-1)
        total = divisor*groups + leftover
        return q(f"{total} / {divisor} = {groups} R ____", "fill", "____")
    def numeral(i, sheet):
        divisor = random.choice([2,3,4,5,6]); groups = random.randint(2,6); leftover = random.randint(1, divisor-1)
        total = divisor*groups + leftover
        return q(f"{total} / {divisor} = ____ R ____", "fill", "____  R  ____")
    def multisel(i, sheet):
        divisor = random.choice([3,4]); opts = []
        for k in range(4):
            g = random.randint(2,5); l = random.randint(0, divisor-1)
            opts.append(f"{divisor*g+l}/{divisor}")
        return q(f"Which division has NO remainder? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4,5])
        pairs = [(random.randint(2,5), random.randint(1,divisor-1)) for _ in range(3)]
        lefts = [f"{divisor*g+l}/{divisor}" for g,l in pairs]; rights = [f"{g} R {l}" for g,l in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of remainder division -- always check your answer."],
        "array_example", {"rows": 4, "cols": 3},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=200)


# ───────────────────────── G/H/I/CUM3: Long division ─────────────────────────

def _G_s(sheet):
    def comp(i, sheet):
        divisor = random.choice([3,4]); tens = random.randint(2,4); ones_groups = random.randint(1,divisor-1) if divisor>1 else 0
        dividend = divisor*tens*10 + divisor*ones_groups; rows_total = tens*10 + ones_groups
        return q(f"{dividend} / {divisor} = ____  (split into tens and ones to help)", "diagram", "____", "", "array_blank", {"rows": divisor, "cols": rows_total})
    def tf(i, sheet):
        divisor = random.choice([3,4]); n = random.randint(15,30); dividend = divisor*n
        shown = n if random.random() > 0.4 else n+1
        return q(f"True or False: {dividend} / {divisor} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        divisor = random.choice([3,4]); n = random.randint(15,30); dividend = divisor*n
        return q(f"{dividend} / ____ = {n}", "fill", "____")
    def numeral(i, sheet):
        divisor = random.choice([3,4]); n = random.randint(15,30); dividend = divisor*n
        return q(f"{dividend} / {divisor} = ____", "fill", "____")
    def multisel(i, sheet):
        divisor = 4; target = random.randint(15,25)
        opts = [f"{target*divisor}/{divisor}", f"{(target+1)*divisor}/{divisor}", f"{target*divisor}/2", f"{target}x{divisor}/{divisor}"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4])
        ns = random.sample(range(15,30), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Split a bigger number into a 'friendly' chunk (like tens) plus the rest.",
         "84 / 4: split 84 = 80 + 4. 80/4=20, 4/4=1. Total: 20+1=21."],
        "array_example", {"rows": 4, "cols": 21},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=70)


def _H_s(sheet):
    def comp(i, sheet):
        divisor = random.choice([3,4,5]); q1 = 10; q2 = random.randint(2,9); dividend = divisor*(q1+q2)
        return q(f"{dividend} / {divisor} = ____  (use the box: subtract friendly chunks)", "diagram", "____",
                  "", "division_box_blank", {"dividend": dividend, "divisor": divisor})
    def tf(i, sheet):
        divisor = random.choice([3,4,5]); n = random.randint(12,30); dividend = divisor*n
        shown = n if random.random() > 0.4 else n+2
        return q(f"True or False: {dividend} / {divisor} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        divisor = random.choice([3,4,5]); n = random.randint(12,30); dividend = divisor*n
        return q(f"{dividend} / ____ = {n}", "fill", "____")
    def numeral(i, sheet):
        divisor = random.choice([3,4,5]); n = random.randint(12,30); dividend = divisor*n
        return q(f"{dividend} / {divisor} = ____", "fill", "____")
    def multisel(i, sheet):
        divisor = random.choice([3,4]); n = random.randint(15,25)
        opts = [f"{divisor*n}/{divisor}", f"{divisor*(n+1)}/{divisor}", f"{divisor*n}/{divisor+1}", f"{divisor*n}/{divisor}"]
        return q(f"Which equal {n}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4,5])
        ns = random.sample(range(12,30), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Subtract a friendly multiple of the divisor (like 10x), then keep going with what's left.",
         "78 / 3: subtract 10x3=30 (left:48), then 10x3=30 again (left:18), then 6x3=18 (left:0). 10+10+6=26."],
        "division_box_example", {"dividend": 78, "divisor": 3, "partials": [(10, 48), (10, 18), (6, 0)]},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=80)


def _I_s(sheet):
    def comp(i, sheet):
        divisor = random.choice([3,4,5,6])
        if i % 2 == 0:
            n = random.randint(11,30); dividend = divisor*n
            return q(f"{dividend} / {divisor} = ____  (no remainder)", "diagram", "____", "", "division_box_blank", {"dividend": dividend, "divisor": divisor})
        n = random.randint(11,30); leftover = random.randint(1, divisor-1); dividend = divisor*n + leftover
        return q(f"{dividend} / {divisor} = ____ R ____", "diagram", "____  R  ____", "", "division_box_blank", {"dividend": dividend, "divisor": divisor})
    def tf(i, sheet):
        divisor = random.choice([3,4,5,6]); n = random.randint(11,25); dividend = divisor*n
        shown = n if random.random() > 0.4 else n+1
        return q(f"True or False: {dividend} / {divisor} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        divisor = random.choice([3,4,5,6]); n = random.randint(11,25); dividend = divisor*n
        return q(f"{dividend} / ____ = {n}", "fill", "____")
    def numeral(i, sheet):
        divisor = random.choice([3,4,5,6]); n = random.randint(11,25); dividend = divisor*n
        return q(f"{dividend} / {divisor} = ____", "fill", "____")
    def multisel(i, sheet):
        divisor = random.choice([3,4]); n = random.randint(15,25)
        opts = [f"{divisor*n}/{divisor}", f"{divisor*(n+1)}/{divisor}", f"{divisor*n}/{divisor+1}", f"{divisor*n}/{divisor}"]
        return q(f"Which equal {n}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4,5,6])
        ns = random.sample(range(11,25), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example", ["Practice the box method -- some have a remainder, some don't."],
        "division_box_example", {"dividend": 78, "divisor": 3, "partials": [(10, 48), (10, 18), (6, 0)]},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=90)


def _CUM3_s(sheet):
    def comp(i, sheet):
        divisor = random.choice([3,4,5,6]); n = random.randint(11,25); dividend = divisor*n
        return q(f"{dividend} / {divisor} = ____", "diagram", "____", "", "division_box_blank", {"dividend": dividend, "divisor": divisor})
    def tf(i, sheet):
        divisor = random.choice([3,4,5]); n = random.randint(11,25); dividend = divisor*n
        shown = n if random.random() > 0.4 else n+1
        return q(f"True or False: {dividend} / {divisor} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        divisor = random.choice([3,4,5]); n = random.randint(11,25); dividend = divisor*n
        return q(f"{dividend} / ____ = {n}", "fill", "____")
    def numeral(i, sheet):
        divisor = random.choice([3,4,5,6]); n = random.randint(11,25); dividend = divisor*n
        return q(f"{dividend} / {divisor} = ____", "fill", "____")
    def multisel(i, sheet):
        divisor = random.choice([3,4]); n = random.randint(15,25)
        opts = [f"{divisor*n}/{divisor}", f"{divisor*(n+1)}/{divisor}", f"{divisor*n}/{divisor+1}", f"{divisor*n}/{divisor}"]
        return q(f"Which equal {n}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4,5])
        ns = random.sample(range(11,25), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Practice long division using the box method."],
        "division_box_example", {"dividend": 78, "divisor": 3, "partials": [(10, 48), (10, 18), (6, 0)]},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=300)


# ───────────────────────── J/K/CUM4: Word problems (tiered) ─────────────────────────

def _J_s(sheet):
    templates = ["{t} apples shared equally among {d} baskets. Each basket has ____.",
                 "{t} books on {d} shelves equally. Books per shelf = ____.",
                 "{t} students in teams of {d}. Number of teams = ____."]
    def gen(sheet):
        d = random.choice([2,3,4,5,6]); n = random.randint(3,9)
        return (d*n, d)
    def comp(i, sheet):
        t, d = gen(sheet)
        return q(templates[i % len(templates)].format(t=t, d=d), "diagram", "____", "", "array_blank", {"rows": d, "cols": t//d})
    def tf(i, sheet):
        t, d = gen(sheet); correct = t//d
        shown = correct if random.random() > 0.4 else correct+1
        return q(f"True or False: {t} shared among {d} gives {shown} each.", "fill", "____ (True/False)")
    def missing(i, sheet):
        t, d = gen(sheet)
        return q(f"{t} shared among ____ baskets gives {t//d} each. How many baskets?", "fill", "____")
    def numeral(i, sheet):
        t, d = gen(sheet)
        return q(templates[i % len(templates)].format(t=t, d=d), "fill", "____")
    def multisel(i, sheet):
        target = random.randint(3,9)
        opts = [f"{target*2}/2", f"{target*3}/3", f"{target}/1", f"{target+1}/1"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{t} shared among {d}" for t,d in pairs]; rights = [str(t//d) for t,d in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example", ["Find the total and how many groups, then divide evenly."],
        "array_example", {"rows": 4, "cols": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=110)


def _K_s(sheet):
    def gen(sheet):
        d = random.choice([3,4,5,6]); n = random.randint(5,10); leftover = random.randint(1, d-1)
        return (d*n+leftover, d)
    def comp(i, sheet):
        t, d = gen(sheet)
        return q(f"(Has a remainder) {t} pencils in packs of {d}. Complete packs = ____, leftover = ____.",
                  "diagram", "____  R  ____", "", "array_blank", {"rows": d, "cols": t//d})
    def tf(i, sheet):
        t, d = gen(sheet); correct = t//d
        shown = correct if random.random() > 0.4 else correct+1
        return q(f"True or False: {t} pencils in packs of {d} gives {shown} complete packs.", "fill", "____ (True/False)")
    def missing(i, sheet):
        t, d = gen(sheet)
        return q(f"{t} / {d} = {t//d} R ____. What's the leftover?", "fill", "____")
    def numeral(i, sheet):
        t, d = gen(sheet)
        return q(f"{t} pencils in packs of {d}. Packs = ____, leftover = ____.", "fill", "____  R  ____")
    def multisel(i, sheet):
        d = 4; opts = []
        for k in range(4):
            n = random.randint(3,8); l = random.randint(0,d-1)
            opts.append(f"{d*n+l}/{d}")
        return q(f"Which leave NO remainder when divided by {d}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{t}/{d}" for t,d in pairs]; rights = [f"{t//d} R {t%d}" for t,d in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["These don't share perfectly evenly -- find the complete groups AND what's left over."],
        "array_example", {"rows": 4, "cols": 3},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=120)


def _CUM4_s(sheet):
    def gen(sheet):
        d = random.choice([2,3,4,5,6]); n = random.randint(3,9)
        return (d, n)
    def comp(i, sheet):
        d, n = gen(sheet)
        if i % 2 == 0:
            t = d*n
            return q(f"{t} shared equally among {d}. Each gets ____.", "diagram", "____", "", "array_blank", {"rows":d,"cols":n})
        leftover = random.randint(1,d-1); t = d*n+leftover
        return q(f"{t} shared in packs of {d}. Packs = ____, leftover = ____.", "diagram", "____  R  ____", "", "array_blank", {"rows":d,"cols":n})
    def tf(i, sheet):
        d, n = gen(sheet); t = d*n
        return q(f"True or False: {t} shared among {d} gives {n} each.", "fill", "____ (True/False)")
    def missing(i, sheet):
        d, n = gen(sheet); t = d*n
        return q(f"{t} / {d} = ____", "fill", "____")
    def numeral(i, sheet):
        d, n = gen(sheet); leftover = random.randint(0,d-1); t = d*n+leftover
        return q(f"{t} / {d} = ____ R ____", "fill", "____  R  ____")
    def multisel(i, sheet):
        target = random.randint(3,9)
        opts = [f"{target*2}/2", f"{target*3}/3", f"{target}/1", f"{target+1}/1"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{d*n}/{d}" for d,n in pairs]; rights = [str(n) for d,n in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of word problems, with and without remainder."],
        "array_example", {"rows": 4, "cols": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=400)


# ───────────────────────── L/M/CUM5: Fact families & missing numbers ─────────────────────────

def _L_s(sheet):
    def gen(sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        return (a, b)
    def comp(i, sheet):
        a, b = gen(sheet); product = a*b
        return q(f"{a} x {b} = {product}. So {product} / {a} = ____ and {product} / {b} = ____",
                  "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
    def tf(i, sheet):
        a, b = gen(sheet); product = a*b
        shown = b if random.random() > 0.4 else b+1
        return q(f"True or False: {a} x {b} = {product}, so {product} / {a} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b = gen(sheet); product = a*b
        return q(f"{a} x ____ = {product}. So {product} / {a} = ____", "fill", "____")
    def numeral(i, sheet):
        a, b = gen(sheet); product = a*b
        return q(f"{a} x {b} = {product}. So {product} / {a} = ____", "fill", "____")
    def multisel(i, sheet):
        a, b = gen(sheet); product = a*b
        opts = [f"{product}/{a}", f"{product}/{b}", f"{product}/{a+1}", f"{product}/{b+1}"]
        return q(f"Which division facts come from {a}x{b}={product}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{a}x{b}" for a,b in pairs]; rights = [str(a*b) for a,b in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example", ["Multiplication and division are linked -- one fact gives you two division facts."],
        "array_example", {"rows": 6, "cols": 7},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=130)


def _M_s(sheet):
    def gen(sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        return (a, b)
    def comp(i, sheet):
        a, b = gen(sheet); product = a*b
        choice = i % 2
        if choice == 0:
            return q(f"? / {b} = {a}.  Missing = ____  (use: {a} x {b})", "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
        return q(f"{product} / ? = {a}.  Missing = ____  (use: {product} / {a})", "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
    def tf(i, sheet):
        a, b = gen(sheet); product = a*b
        shown = product if random.random() > 0.4 else product+b
        return q(f"True or False: ? / {b} = {a} means missing number = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b = gen(sheet)
        return q(f"? / {b} = {a}.  Missing dividend = ____", "fill", "____")
    def numeral(i, sheet):
        a, b = gen(sheet); product = a*b
        return q(f"{product} / ? = {a}.  Missing divisor = ____", "fill", "____")
    def multisel(i, sheet):
        a, b = gen(sheet); product = a*b
        opts = [str(product), str(product+b), str(product-b), str(a*b)]
        return q(f"Which is the correct missing dividend for ?/{b}={a}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"?/{b}={a}" for a,b in pairs]; rights = [str(a*b) for a,b in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["To find a missing DIVIDEND, multiply the other two numbers.",
         "To find a missing DIVISOR, divide the dividend by the quotient.",
         "? / 6 = 7: missing dividend = 7 x 6 = 42."],
        "array_example", {"rows": 6, "cols": 7},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=140)


def _CUM5_s(sheet):
    def gen(sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        return (a, b)
    def comp(i, sheet):
        a, b = gen(sheet); product = a*b
        if i % 2 == 0:
            return q(f"{a} x {b} = {product}. So {product} / {a} = ____", "diagram", "____", "", "array_blank", {"rows":a,"cols":b})
        return q(f"? / {b} = {a}. Missing = ____", "diagram", "____", "", "array_blank", {"rows":a,"cols":b})
    def tf(i, sheet):
        a, b = gen(sheet); product = a*b
        return q(f"True or False: {a} x {b} = {product}", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b = gen(sheet)
        return q(f"? / {b} = {a}. Missing = ____", "fill", "____")
    def numeral(i, sheet):
        a, b = gen(sheet); product = a*b
        return q(f"{product} / {a} = ____", "fill", "____")
    def multisel(i, sheet):
        a, b = gen(sheet); product = a*b
        opts = [str(product), str(product+b), str(product-b), str(a*b)]
        return q(f"Which is correct for ?/{b}={a}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{a}x{b}" for a,b in pairs]; rights = [str(a*b) for a,b in pairs]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of fact families and missing numbers."], "array_example", {"rows": 6, "cols": 7},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=500)


# ───────────────────────── N: Speed - basic facts (fun formats) ─────────────────────────

def _N_s(sheet):
    def gen(sheet):
        divisor = random.choice([2,3,4,5,6,7,8,9]); n = random.randint(1,9)
        return (divisor*n, divisor)
    def comp(i, sheet):
        dividend, divisor = gen(sheet)
        return q(f"{dividend} / {divisor} = ____", "diagram", "____", "", "array_blank", {"rows": divisor, "cols": dividend//divisor})
    def tf(i, sheet):
        dividend, divisor = gen(sheet); correct = dividend//divisor
        shown = correct if random.random() > 0.4 else correct+1
        return q(f"True or False: {dividend} / {divisor} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        dividend, divisor = gen(sheet)
        return q(f"{dividend} / ____ = {dividend//divisor}", "fill", "____")
    def numeral(i, sheet):
        dividend, divisor = gen(sheet)
        return q(f"{dividend} / {divisor} = ____", "fill", "____")
    def multisel(i, sheet):
        divisor = random.randint(2,9); n = random.randint(2,9); target = n
        opts = [f"{divisor*n}/{divisor}", f"{divisor*(n+1)}/{divisor}", f"{divisor*n}/{divisor+1}", f"{divisor*n}/{divisor}"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4,5,6])
        ns = random.sample(range(2,9), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(2,8), random.randint(2,4), 2, 3)
    def fun2(i, sheet):
        divisor = random.choice([2,3,4])
        return function_machine_q(divisor*random.randint(2,8), [f"/ {divisor}"], mode=random.choice(["forward","reverse"]))
    def fun3(i, sheet):
        base = random.randint(2,5)
        given = {(3,0): base, (3,1): base+1, (3,2): base, (3,3): base+1}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"8/2", None), (f"9/3", None)]
        parts = [(e, eval(e.replace("/","//"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{d}/{di}" for d,di in pairs]; rights = [str(d//di) for d,di in pairs]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Worked Example", ["Speed round: recall your division facts instantly."],
        "array_example", {"rows": 7, "cols": 6},
        "First 15: speed facts. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=150)


# ───────────────────────── O/CUM6: Speed /10 /100 (fun formats) ─────────────────────────

def _O_s(sheet):
    def gen(sheet):
        power = random.choice([10,100]); n = random.randint(2,9)
        return (n*power, power)
    def comp(i, sheet):
        dividend, power = gen(sheet)
        return q(f"{dividend} / {power} = ____  (remove a zero for /10, two for /100)", "diagram", "____", "", "array_blank", {"rows": 1, "cols": dividend//power})
    def tf(i, sheet):
        dividend, power = gen(sheet); correct = dividend//power
        shown = correct if random.random() > 0.4 else correct*10
        return q(f"True or False: {dividend} / {power} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        dividend, power = gen(sheet)
        return q(f"{dividend} / ____ = {dividend//power}", "fill", "____")
    def numeral(i, sheet):
        dividend, power = gen(sheet)
        return q(f"{dividend} / {power} = ____", "fill", "____")
    def multisel(i, sheet):
        divisor = random.randint(2,9); n = random.randint(2,9); target = n
        opts = [f"{divisor*n}/{divisor}", f"{divisor*(n+1)}/{divisor}", f"{divisor*n}/{divisor+1}", f"{divisor*n}/{divisor}"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4,5,6])
        ns = random.sample(range(2,9), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(20,80), random.randint(10,20), 5, 10)
    def fun2(i, sheet):
        return function_machine_q(random.randint(2,9)*10, ["/ 10"], mode=random.choice(["forward","reverse"]))
    def fun3(i, sheet):
        base = random.randint(10,30)
        given = {(3,0): base, (3,1): base+10, (3,2): base, (3,3): base+10}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"40/10", None), (f"90/10", None)]
        parts = [(e, eval(e.replace("/","//"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{d}/{p}" for d,p in pairs]; rights = [str(d//p) for d,p in pairs]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Worked Example",
        ["Dividing by 10 or 100 is a place-value shortcut, not a fact to memorize.",
         "480 / 10 = 48 (remove one zero). 4800 / 100 = 48 (remove two zeros)."],
        "array_example", {"rows": 1, "cols": 48},
        "First 15: /10 and /100 practice. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=160)


def _CUM6_s(sheet):
    def gen(sheet):
        if random.random() > 0.5:
            divisor = random.choice([2,3,4,5,6,7,8,9]); n = random.randint(1,9)
            return (divisor*n, divisor)
        power = random.choice([10,100]); n = random.randint(2,9)
        return (n*power, power)
    def comp(i, sheet):
        dividend, divisor = gen(sheet)
        return q(f"{dividend} / {divisor} = ____", "diagram", "____", "", "array_blank", {"rows": min(divisor,9), "cols": dividend//divisor})
    def tf(i, sheet):
        dividend, divisor = gen(sheet); correct = dividend//divisor
        shown = correct if random.random() > 0.4 else correct+1
        return q(f"True or False: {dividend} / {divisor} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        dividend, divisor = gen(sheet)
        return q(f"{dividend} / ____ = {dividend//divisor}", "fill", "____")
    def numeral(i, sheet):
        dividend, divisor = gen(sheet)
        return q(f"{dividend} / {divisor} = ____", "fill", "____")
    def multisel(i, sheet):
        divisor = random.randint(2,9); n = random.randint(2,9); target = n
        opts = [f"{divisor*n}/{divisor}", f"{divisor*(n+1)}/{divisor}", f"{divisor*n}/{divisor+1}", f"{divisor*n}/{divisor}"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4,5,6])
        ns = random.sample(range(2,9), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(20,60), random.randint(10,20), 5, 10)
    def fun2(i, sheet):
        return function_machine_q(random.randint(2,9)*10, ["/ 10"], mode="forward")
    def fun3(i, sheet):
        base = random.randint(2,5)
        given = {(3,0): base, (3,1): base+1, (3,2): base+2, (3,3): base}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"8/2", None), (f"9/3", None)]
        parts = [(e, eval(e.replace("/","//"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{d}/{p}" for d,p in pairs]; rights = [str(d//p) for d,p in pairs]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Review", ["Mix of basic facts and /10, /100 shortcuts."], "array_example", {"rows": 1, "cols": 48},
        "First 15: review. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=600)


# ───────────────────────── P/Q/CUM7: Puzzles (fun formats) ─────────────────────────

def _P_s(sheet):
    def comp(i, sheet):
        divisor = random.randint(3,9); lo = divisor*random.randint(3,6); hi = lo + divisor + 2
        return q(f"I am divisible by {divisor}. I am between {lo} and {hi}. What am I?", "diagram", "____", "", "array_blank", {"rows": divisor, "cols": 1})
    def tf(i, sheet):
        divisor = random.randint(3,9); n = divisor*random.randint(2,6)
        return q(f"True or False: {n} is divisible by {divisor}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        divisor = random.randint(3,9); n = random.randint(2,6)
        return q(f"{divisor} x ____ = {divisor*n}. Missing factor?", "fill", "____")
    def numeral(i, sheet):
        divisor = random.randint(3,9); lo = divisor*random.randint(3,6); hi = lo+divisor+2
        return q(f"Divisible by {divisor}, between {lo} and {hi}? ____", "fill", "____")
    def multisel(i, sheet):
        divisor = random.randint(2,9); n = random.randint(2,9); target = n
        opts = [f"{divisor*n}/{divisor}", f"{divisor*(n+1)}/{divisor}", f"{divisor*n}/{divisor+1}", f"{divisor*n}/{divisor}"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4,5,6])
        ns = random.sample(range(2,9), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(10,30), random.randint(5,10), 2, 4)
    def fun2(i, sheet):
        divisor = random.choice([2,3,4])
        return function_machine_q(divisor*random.randint(3,8), [f"/ {divisor}"], mode=random.choice(["forward","reverse"]))
    def fun3(i, sheet):
        base = random.randint(2,5)
        given = {(3,0): base, (3,1): base+1, (3,2): base+2, (3,3): base}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"12/4", None), (f"6/2", None)]
        parts = [(e, eval(e.replace("/","//"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        divisor = random.choice([3,4,5])
        ns = random.sample(range(11,25), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Worked Example", ["List the multiples of the number, then pick the one that fits between the two numbers."],
        "array_example", {"rows": 6, "cols": 5},
        "First 15: simple divisibility puzzles. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=170)


def _Q_s(sheet):
    def comp(i, sheet):
        if i % 2 == 0:
            a, b = random.sample([2,3,4,5,6,7,8], 2); limit = random.randint(40,80)
            return q(f"I am divisible by BOTH {a} and {b}. I am less than {limit}. What am I?", "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
        divisor = random.choice([6,7,8,9]); ds = random.randint(5,14)
        return q(f"I am a 2-digit number divisible by {divisor}. My digits sum to {ds}. What am I?", "diagram", "____", "", "array_blank", {"rows": divisor, "cols": 1})
    def tf(i, sheet):
        a, b = random.sample([2,3,4,5,6], 2); n = a*b
        return q(f"True or False: {n} is divisible by both {a} and {b}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        divisor = random.choice([6,7,8,9]); n = random.randint(2,4)
        return q(f"{divisor} x ____ = {divisor*n}", "fill", "____")
    def numeral(i, sheet):
        a, b = random.sample([2,3,4,5,6], 2); limit = random.randint(40,80)
        return q(f"Divisible by both {a} and {b}, less than {limit}? ____", "fill", "____")
    def multisel(i, sheet):
        divisor = random.randint(2,9); n = random.randint(2,9); target = n
        opts = [f"{divisor*n}/{divisor}", f"{divisor*(n+1)}/{divisor}", f"{divisor*n}/{divisor+1}", f"{divisor*n}/{divisor}"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4,5,6])
        ns = random.sample(range(2,9), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(10,30), random.randint(5,10), 3, 5)
    def fun2(i, sheet):
        divisor = random.choice([2,3])
        return function_machine_q(divisor*random.randint(4,9), [f"/ {divisor}", "+ 1"], mode="forward")
    def fun3(i, sheet):
        base = random.randint(2,5)
        given = {(3,0): base, (3,1): base+2, (3,2): base+1, (3,3): base+3}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"16/4", None), (f"21/3", None)]
        parts = [(e, eval(e.replace("/","//"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        a, b = random.sample([2,3,4,5], 2)
        ns = [a*b, a*b*2, a*b*3]
        lefts = [f"multiple of {a} and {b}" for _ in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Worked Example (Harder)",
        ["A COMMON multiple fits BOTH tables -- check multiples of one table against the other.",
         "FACTOR PAIRS are two numbers that multiply to make the target."],
        "array_example", {"rows": 6, "cols": 7},
        "First 15: harder puzzles. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=180)


def _CUM7_s(sheet):
    def comp(i, sheet):
        choice = i % 2
        if choice == 0:
            divisor = random.randint(3,9); lo = divisor*3; hi = lo+divisor+2
            return q(f"Divisible by {divisor}, between {lo} and {hi}?", "diagram", "____", "", "array_blank", {"rows":divisor,"cols":1})
        a,b = random.sample([2,3,4,5,6],2); limit = random.randint(40,80)
        return q(f"Divisible by both {a} and {b}, less than {limit}?", "diagram", "____", "", "array_blank", {"rows":a,"cols":b})
    def tf(i, sheet):
        divisor = random.randint(3,9); n = divisor*random.randint(2,6)
        return q(f"True or False: {n} is divisible by {divisor}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        divisor = random.randint(3,9); n = random.randint(2,6)
        return q(f"{divisor} x ____ = {divisor*n}", "fill", "____")
    def numeral(i, sheet):
        divisor = random.randint(3,9); lo = divisor*3; hi = lo+divisor+2
        return q(f"Divisible by {divisor}, between {lo} and {hi}? ____", "fill", "____")
    def multisel(i, sheet):
        divisor = random.randint(2,9); n = random.randint(2,9); target = n
        opts = [f"{divisor*n}/{divisor}", f"{divisor*(n+1)}/{divisor}", f"{divisor*n}/{divisor+1}", f"{divisor*n}/{divisor}"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4,5,6])
        ns = random.sample(range(2,9), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(10,30), random.randint(5,10), 2, 4)
    def fun2(i, sheet):
        divisor = random.choice([2,3,4])
        return function_machine_q(divisor*random.randint(3,8), [f"/ {divisor}"], mode=random.choice(["forward","reverse"]))
    def fun3(i, sheet):
        base = random.randint(2,5)
        given = {(3,0): base, (3,1): base+1, (3,2): base+2, (3,3): base}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"12/4", None), (f"15/3", None)]
        parts = [(e, eval(e.replace("/","//"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        divisor = random.choice([3,4,5])
        ns = random.sample(range(11,25), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Review", ["Mix of simple and harder divisibility puzzles."], "array_example", {"rows": 6, "cols": 7},
        "First 15: review. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=700)


# ───────────────────────── R/REV ─────────────────────────

def _R_s(sheet):
    def comp(i, sheet):
        choice = i % 5
        divisor = random.randint(2,9); n = random.randint(2,9)
        if choice == 0:
            return q(f"{divisor*n} / {divisor} = ____", "diagram", "____", "", "array_blank", {"rows":divisor,"cols":n})
        elif choice == 1:
            leftover = random.randint(1,divisor-1)
            return q(f"{divisor*n+leftover} / {divisor} = ____ R ____", "diagram", "____  R  ____", "", "array_blank", {"rows":divisor,"cols":n})
        elif choice == 2:
            return q(f"{divisor*n*10} / {divisor} = ____", "diagram", "____", "", "division_box_blank", {"dividend":divisor*n*10,"divisor":divisor})
        elif choice == 3:
            a,b = random.randint(2,9), random.randint(2,9)
            return q(f"{a} x {b} = {a*b}. So {a*b} / {a} = ____", "diagram", "____", "", "array_blank", {"rows":a,"cols":b})
        else:
            return q(f"{n*10} / 10 = ____", "diagram", "____", "", "array_blank", {"rows":1,"cols":n})
    def tf(i, sheet):
        divisor = random.randint(2,9); n = random.randint(2,9); correct = divisor*n
        shown = correct if random.random() > 0.4 else correct+divisor
        return q(f"True or False: {divisor} x {n} = {correct} means {correct}/{divisor}={shown//divisor if shown%divisor==0 else n}", "fill", "____ (True/False)")
    def missing(i, sheet):
        divisor = random.randint(2,9); n = random.randint(2,9)
        return q(f"{divisor*n} / ____ = {n}", "fill", "____")
    def numeral(i, sheet):
        divisor = random.randint(2,9); n = random.randint(2,9)
        return q(f"{divisor*n} / {divisor} = ____", "fill", "____")
    def multisel(i, sheet):
        divisor = random.randint(2,9); n = random.randint(2,9); target = n
        opts = [f"{divisor*n}/{divisor}", f"{divisor*(n+1)}/{divisor}", f"{divisor*n}/{divisor+1}", f"{divisor*n}/{divisor}"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4,5,6])
        ns = random.sample(range(2,9), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(10,30), random.randint(5,10), 2, 4)
    def fun2(i, sheet):
        divisor = random.choice([2,3,4])
        return function_machine_q(divisor*random.randint(3,8), [f"/ {divisor}"], mode=random.choice(["forward","reverse"]))
    def fun3(i, sheet):
        base = random.randint(2,5)
        given = {(3,0): base, (3,1): base+1, (3,2): base+2, (3,3): base+1}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"10/2", None), (f"18/3", None)]
        parts = [(e, eval(e.replace("/","//"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        divisor = random.choice([3,4,5])
        ns = random.sample(range(11,25), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Worked Example", ["Mixed challenge: every division skill from this level."],
        "division_box_example", {"dividend": 78, "divisor": 3, "partials": [(10, 48), (10, 18), (6, 0)]},
        "First 15: mixed review. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=190)


def _REV_s(sheet):
    def comp(i, sheet):
        choice = i % 6
        divisor = random.randint(2,9); n = random.randint(2,9)
        if choice == 0:
            return q(f"{divisor*n} / {divisor} = ____", "diagram", "____", "", "array_blank", {"rows":divisor,"cols":n})
        elif choice == 1:
            leftover = random.randint(1,divisor-1)
            return q(f"{divisor*n+leftover} / {divisor} = ____ R ____", "diagram", "____  R  ____", "", "array_blank", {"rows":divisor,"cols":n})
        elif choice == 2:
            return q(f"{divisor*n*10} / {divisor} = ____", "diagram", "____", "", "division_box_blank", {"dividend":divisor*n*10,"divisor":divisor})
        elif choice == 3:
            a,b = random.randint(2,9), random.randint(2,9)
            return q(f"{a} x {b} = {a*b}. So {a*b} / {a} = ____", "diagram", "____", "", "array_blank", {"rows":a,"cols":b})
        elif choice == 4:
            return q(f"{n*10} / 10 = ____", "diagram", "____", "", "array_blank", {"rows":1,"cols":n})
        else:
            lo = divisor*3; hi = lo+divisor+2
            return q(f"Divisible by {divisor}, between {lo} and {hi}?", "diagram", "____", "", "array_blank", {"rows":divisor,"cols":1})
    def tf(i, sheet):
        divisor = random.randint(2,9); n = random.randint(2,9)
        return q(f"True or False: {divisor*n} / {divisor} = {n}", "fill", "____ (True/False)")
    def missing(i, sheet):
        divisor = random.randint(2,9); n = random.randint(2,9)
        return q(f"{divisor*n} / ____ = {n}", "fill", "____")
    def numeral(i, sheet):
        divisor = random.randint(2,9); n = random.randint(2,9)
        return q(f"{divisor*n} / {divisor} = ____", "fill", "____")
    def multisel(i, sheet):
        divisor = random.randint(2,9); n = random.randint(2,9); target = n
        opts = [f"{divisor*n}/{divisor}", f"{divisor*(n+1)}/{divisor}", f"{divisor*n}/{divisor+1}", f"{divisor*n}/{divisor}"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        divisor = random.choice([3,4,5,6])
        ns = random.sample(range(2,9), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    def fun1(i, sheet):
        return maze_q(random.randint(10,30), random.randint(5,10), 2, 4)
    def fun2(i, sheet):
        divisor = random.choice([2,3,4])
        return function_machine_q(divisor*random.randint(3,8), [f"/ {divisor}"], mode=random.choice(["forward","reverse"]))
    def fun3(i, sheet):
        base = random.randint(2,5)
        given = {(3,0): base, (3,1): base+1, (3,2): base+2, (3,3): base}
        return pyramid_q(4, given)
    def fun4(i, sheet):
        parts = [(f"14/2", None), (f"24/4", None)]
        parts = [(e, eval(e.replace("/","//"))) for e, _ in parts]
        return codebreaker_q(parts, "")
    def fun5(i, sheet):
        divisor = random.choice([3,4,5])
        ns = random.sample(range(11,25), 3)
        lefts = [f"{divisor*n}/{divisor}" for n in ns]; rights = [str(n) for n in ns]
        return matching_q(lefts, rights)
    fun_builders = [fun1, fun2, fun3, fun4, fun5]
    return make_fun_sheet(
        "Level 5 Revision",
        ["Every division skill: facts, remainders, long division, word problems, and puzzles."],
        "division_box_example", {"dividend": 78, "divisor": 3, "partials": [(10, 48), (10, 18), (6, 0)]},
        "First 15: full revision. Last 5: fun formats!", fmt, fun_builders, sheet, seed_base=800)


# ───────────────────────── Dispatcher (REPLACES original Level 5) ─────────────────────────

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL5_V2_DISPATCH = {
    "5A": _wrap(_A_s), "5B": _wrap(_B_s), "5C": _wrap(_C_s), "5D": _wrap(_D_s), "5CUM1": _wrap(_CUM1_s),
    "5E": _wrap(_E_s), "5F": _wrap(_F_s), "5CUM2": _wrap(_CUM2_s),
    "5G": _wrap(_G_s), "5H": _wrap(_H_s), "5I": _wrap(_I_s), "5CUM3": _wrap(_CUM3_s),
    "5J": _wrap(_J_s), "5K": _wrap(_K_s), "5CUM4": _wrap(_CUM4_s),
    "5L": _wrap(_L_s), "5M": _wrap(_M_s), "5CUM5": _wrap(_CUM5_s),
    "5N": _wrap(_N_s), "5O": _wrap(_O_s), "5CUM6": _wrap(_CUM6_s),
    "5P": _wrap(_P_s), "5Q": _wrap(_Q_s), "5CUM7": _wrap(_CUM7_s),
    "5R": _wrap(_R_s), "5REV": _wrap(_REV_s),
}
