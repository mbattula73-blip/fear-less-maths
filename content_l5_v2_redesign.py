"""
Fear Less Maths — LEVEL 5 REDESIGN (Division, Grade 3-4)

Replaces the original Level 5 in place. Based on detailed analysis of
the original (which jumped into ÷6/÷7 facts alongside ÷2/÷3 with no
easiest-first order, used the verification "check" technique only once
without teaching it, explained "long division" via cramped inline text
with NO visual model at all, mixed remainder and non-remainder problems
in the same word-problem sheet, introduced missing-number/inverse
reasoning with zero strategy explanation, conflated basic fact recall
with the different skill of dividing by 10/100, and jumped to LCM-style
puzzles with no scaffolding) plus research into the modern partial-
quotients ("Big 7") method, which multiple sources recommend over rote
long division because it connects to place value/estimation, paired
with an area-model bridge -- and the universal recommendation to always
teach the multiply-back CHECK step explicitly.

Same worksheet format as Levels 3/4/6/7: ONE worked example, ONE
instruction line stated once, 20 bare-expression questions (15
pictorial blank-diagram + 5 numeral), B&W outline-only diagrams.

Sub-level list (26 total):
  A Concept (sharing/grouping)
  B Easy divisors: /2 /5 /10          C Mid divisors: /3 /4 /6 /9
  D Hard divisors: /7 /8 (last)
  CUM1 review
  E Remainders - concept              F Remainders - the CHECK step (taught)
  CUM2 review
  G Long division - area model bridge H Long division - partial quotients (taught)
  I Long division practice (mixed)
  CUM3 review
  J Word problems - no remainder      K Word problems - with remainder (separated)
  CUM4 review
  L Fact families (pure division)     M Missing numbers (strategy taught)
  CUM5 review
  N Speed - basic facts               O Speed - /10 /100 (separated skill)
  CUM6 review
  P Puzzles - Tier 1                  Q Puzzles - Tier 2 (LCM/digit, taught)
  CUM7 review
  R Mixed challenge                  REV Revision
"""
import random
from content import cb, tb, q

# ───────────────────────── shared helpers ─────────────────────────

def _div_q(dividend, divisor, hint=""):
    suffix = f"  {hint}" if hint else ""
    return q(f"{dividend} / {divisor} = ____{suffix}", "diagram", "____",
              "", "array_blank", {"rows": divisor, "cols": dividend // divisor if dividend % divisor == 0 else max(1, dividend // divisor)})


def _make_sheet(title, bullets, icon, icon_params, instruction, builder, sheet, n_q=20, seed_base=0):
    random.seed(seed_base + sheet)
    items = [cb(title, bullets, "", icon_diagram=icon, icon_params=icon_params)]
    items.append(tb("Instructions", [instruction]))
    questions = [builder(i, sheet) for i in range(n_q)]
    for i in range(15, len(questions)):
        questions[i] = dict(questions[i])
        questions[i]["diagram_type"] = None
        questions[i]["diagram_params"] = {}
    items.extend(questions)
    return items


# ───────────────────────── A: Concept ─────────────────────────

def _A_s(sheet):
    def builder(i, sheet):
        divisor = random.choice([2,3,4,5])
        groups = random.randint(2,6)
        return _div_q(divisor*groups, divisor)
    return _make_sheet(
        "Worked Example",
        ["Dividing means sharing or grouping equally.",
         "12 / 3 = 4: share 12 into 3 equal groups, each has 4."],
        "array_example", {"rows": 3, "cols": 4},
        "Share or group equally, then write how many in each.", builder, sheet, seed_base=10)


# ───────────────────────── B/C/D: Division facts, easiest first ─────────────────────────

def _B_s(sheet):
    """/2, /5, /10 -- easiest, anchor facts."""
    def builder(i, sheet):
        divisor = random.choice([2,5,10])
        n = random.randint(1,9)
        return _div_q(divisor*n, divisor)
    return _make_sheet(
        "Worked Example",
        ["/2, /5, and /10 are the easiest -- they connect straight to your easiest times tables."],
        "array_example", {"rows": 2, "cols": 6},
        "Think: what number times the divisor gives the dividend?", builder, sheet, seed_base=20)


def _C_s(sheet):
    """/3, /4, /6, /9."""
    def builder(i, sheet):
        divisor = random.choice([3,4,6,9])
        n = random.randint(1,9)
        return _div_q(divisor*n, divisor)
    return _make_sheet(
        "Worked Example", ["Use your x3, x4, x6, and x9 facts in reverse to divide."],
        "array_example", {"rows": 4, "cols": 6},
        "Think: what number times the divisor gives the dividend?", builder, sheet, seed_base=30)


def _D_s(sheet):
    """/7, /8 -- hardest, last."""
    def builder(i, sheet):
        divisor = random.choice([7,8])
        n = random.randint(1,9)
        return _div_q(divisor*n, divisor)
    return _make_sheet(
        "Worked Example",
        ["/7 and /8 are the hardest -- use a known nearby fact and adjust if you're not sure."],
        "array_example", {"rows": 7, "cols": 6},
        "Use your x7 and x8 facts in reverse.", builder, sheet, seed_base=40)


def _CUM1_s(sheet):
    def builder(i, sheet):
        divisor = random.choice([2,3,4,5,6,7,8,9,10])
        n = random.randint(1,9)
        return _div_q(divisor*n, divisor)
    return _make_sheet(
        "Review", ["Mix of all division facts, 2 through 10."],
        "array_example", {"rows": 4, "cols": 6},
        "Use your times tables in reverse for each one.", builder, sheet, seed_base=100)


# ───────────────────────── E/F: Remainders ─────────────────────────

def _E_s(sheet):
    def builder(i, sheet):
        divisor = random.choice([2,3,4,5])
        groups = random.randint(2,6)
        leftover = random.randint(1, divisor-1)
        total = divisor*groups + leftover
        return q(f"{total} / {divisor} = ____ R ____", "diagram", "____  R  ____",
                  "", "array_blank", {"rows": divisor, "cols": groups})
    return _make_sheet(
        "Worked Example",
        ["Sometimes things don't share evenly -- what's left over is the remainder.",
         "13 / 4: 3 groups of 4 = 12, with 1 left over. 13 / 4 = 3 R 1."],
        "array_example", {"rows": 4, "cols": 3},
        "Find the groups first, then count what's left over.", builder, sheet, seed_base=50)


def _F_s(sheet):
    """The CHECK step, explicitly taught."""
    def builder(i, sheet):
        divisor = random.choice([2,3,4,5,6])
        groups = random.randint(2,6)
        leftover = random.randint(1, divisor-1)
        total = divisor*groups + leftover
        return q(f"{total} / {divisor} = ____ R ____.  Check: ____ x {divisor} + ____ = {total}",
                  "diagram", "____  R  ____", "", "array_blank", {"rows": divisor, "cols": groups})
    return _make_sheet(
        "Worked Example",
        ["Always CHECK your division: quotient x divisor + remainder should equal the dividend.",
         "13 / 4 = 3 R 1. Check: 3 x 4 + 1 = 12 + 1 = 13. Correct!"],
        "array_example", {"rows": 4, "cols": 3},
        "After dividing, check by multiplying the quotient by the divisor and adding the remainder.",
        builder, sheet, seed_base=60)


def _CUM2_s(sheet):
    def builder(i, sheet):
        divisor = random.choice([2,3,4,5,6])
        groups = random.randint(2,6)
        leftover = random.randint(1, divisor-1)
        total = divisor*groups + leftover
        return q(f"{total} / {divisor} = ____ R ____. Check your answer!", "diagram", "____  R  ____",
                  "", "array_blank", {"rows": divisor, "cols": groups})
    return _make_sheet(
        "Review", ["Mix of remainder division -- always check your answer."],
        "array_example", {"rows": 4, "cols": 3},
        "Find groups and leftover, then check: quotient x divisor + remainder = dividend.",
        builder, sheet, seed_base=200)


# ───────────────────────── G/H/I: Long division ─────────────────────────

def _G_s(sheet):
    """Area model bridge."""
    def builder(i, sheet):
        divisor = random.choice([3,4])
        tens = random.randint(2,4)
        ones_groups = random.randint(1,divisor-1) if divisor > 1 else 0
        dividend = divisor*tens*10 + divisor*ones_groups
        rows_total = tens*10 + ones_groups
        return q(f"{dividend} / {divisor} = ____  (split into tens and ones to help)",
                  "diagram", "____", "", "array_blank", {"rows": divisor, "cols": rows_total})
    return _make_sheet(
        "Worked Example",
        ["Split a bigger number into a 'friendly' chunk (like tens) plus the rest.",
         "84 / 4: split 84 = 80 + 4. 80/4=20, 4/4=1. Total: 20+1=21."],
        "array_example", {"rows": 4, "cols": 21},
        "Split the dividend into a friendly chunk plus the rest, divide each part, then add.",
        builder, sheet, seed_base=70)


def _H_s(sheet):
    """Partial quotients, taught with the Big 7 box."""
    def builder(i, sheet):
        divisor = random.choice([3,4,5])
        q1 = 10
        q2 = random.randint(2,9)
        dividend = divisor*(q1+q2)
        return q(f"{dividend} / {divisor} = ____  (use the box: subtract friendly chunks)",
                  "diagram", "____", "", "division_box_blank", {"dividend": dividend, "divisor": divisor})
    return _make_sheet(
        "Worked Example",
        ["Subtract a friendly multiple of the divisor (like 10x), then keep going with what's left.",
         "78 / 3: subtract 10x3=30 (left:48), then 10x3=30 again (left:18), then 6x3=18 (left:0). 10+10+6=26."],
        "division_box_example", {"dividend": 78, "divisor": 3, "partials": [(10, 48), (10, 18), (6, 0)]},
        "Subtract friendly chunks (like 10x the divisor) one at a time, then add up your partial quotients.",
        builder, sheet, seed_base=80)


def _I_s(sheet):
    """Practice, mixed (no remainder / with remainder, labeled)."""
    def builder(i, sheet):
        divisor = random.choice([3,4,5,6])
        if i % 2 == 0:
            n = random.randint(11,30)
            dividend = divisor*n
            return q(f"{dividend} / {divisor} = ____  (no remainder)", "diagram", "____",
                      "", "division_box_blank", {"dividend": dividend, "divisor": divisor})
        else:
            n = random.randint(11,30)
            leftover = random.randint(1, divisor-1)
            dividend = divisor*n + leftover
            return q(f"{dividend} / {divisor} = ____ R ____", "diagram", "____  R  ____",
                      "", "division_box_blank", {"dividend": dividend, "divisor": divisor})
    return _make_sheet(
        "Worked Example", ["Practice the box method -- some have a remainder, some don't."],
        "division_box_example", {"dividend": 78, "divisor": 3, "partials": [(10, 48), (10, 18), (6, 0)]},
        "Use the box to subtract friendly chunks until nothing (or less than the divisor) is left.",
        builder, sheet, seed_base=90)


def _CUM3_s(sheet):
    def builder(i, sheet):
        divisor = random.choice([3,4,5,6])
        n = random.randint(11,25)
        dividend = divisor*n
        return q(f"{dividend} / {divisor} = ____", "diagram", "____",
                  "", "division_box_blank", {"dividend": dividend, "divisor": divisor})
    return _make_sheet(
        "Review", ["Practice long division using the box method."],
        "division_box_example", {"dividend": 78, "divisor": 3, "partials": [(10, 48), (10, 18), (6, 0)]},
        "Subtract friendly chunks, then add your partial quotients.", builder, sheet, seed_base=300)


# ───────────────────────── J/K: Word problems (tiered) ─────────────────────────

def _J_s(sheet):
    """No remainder."""
    templates = [
        "{t} apples shared equally among {d} baskets. Each basket has ____.",
        "{t} books on {d} shelves equally. Books per shelf = ____.",
        "{t} students in teams of {d}. Number of teams = ____.",
    ]
    def builder(i, sheet):
        d = random.choice([2,3,4,5,6])
        n = random.randint(3,9)
        t = d*n
        txt = random.choice(templates).format(t=t, d=d)
        return q(txt, "diagram", "____", "", "array_blank", {"rows": d, "cols": n})
    return _make_sheet(
        "Worked Example", ["Find the total and how many groups, then divide evenly."],
        "array_example", {"rows": 4, "cols": 6},
        "One step: total / groups = how many in each.", builder, sheet, seed_base=110)


def _K_s(sheet):
    """With remainder, separated as harder."""
    def builder(i, sheet):
        d = random.choice([3,4,5,6])
        n = random.randint(5,10)
        leftover = random.randint(1, d-1)
        t = d*n + leftover
        return q(f"(Has a remainder) {t} pencils in packs of {d}. Complete packs = ____, leftover = ____.",
                  "diagram", "____  R  ____", "", "array_blank", {"rows": d, "cols": n})
    return _make_sheet(
        "Worked Example",
        ["These don't share perfectly evenly -- find the complete groups AND what's left over."],
        "array_example", {"rows": 4, "cols": 3},
        "Find the complete groups, then count the leftover separately.", builder, sheet, seed_base=120)


def _CUM4_s(sheet):
    def builder(i, sheet):
        d = random.choice([2,3,4,5,6])
        n = random.randint(3,9)
        if i % 2 == 0:
            t = d*n
            return q(f"{t} shared equally among {d}. Each gets ____.", "diagram", "____", "", "array_blank", {"rows":d,"cols":n})
        else:
            leftover = random.randint(1,d-1)
            t = d*n + leftover
            return q(f"{t} shared in packs of {d}. Packs = ____, leftover = ____.", "diagram", "____  R  ____",
                      "", "array_blank", {"rows":d,"cols":n})
    return _make_sheet(
        "Review", ["Mix of word problems, with and without remainder."],
        "array_example", {"rows": 4, "cols": 6},
        "Check if it divides evenly or has a leftover.", builder, sheet, seed_base=400)


# ───────────────────────── L/M: Fact families & missing numbers ─────────────────────────

def _L_s(sheet):
    def builder(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        product = a*b
        return q(f"{a} x {b} = {product}. So {product} / {a} = ____ and {product} / {b} = ____",
                  "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
    return _make_sheet(
        "Worked Example",
        ["Multiplication and division are linked -- one fact gives you two division facts."],
        "array_example", {"rows": 6, "cols": 7},
        "Use the multiplication fact to find both division facts.", builder, sheet, seed_base=130)


def _M_s(sheet):
    """Missing numbers, strategy explicitly taught."""
    def builder(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        product = a*b
        choice = i % 3
        if choice == 0:
            return q(f"? / {b} = {a}.  Missing = ____  (use: {a} x {b})", "diagram", "____",
                      "", "array_blank", {"rows": a, "cols": b})
        elif choice == 1:
            return q(f"{product} / ? = {a}.  Missing = ____  (use: {product} / {a})", "diagram", "____",
                      "", "array_blank", {"rows": a, "cols": b})
        else:
            return q(f"? / {b} = {a}.  Missing dividend = ____", "diagram", "____",
                      "", "array_blank", {"rows": a, "cols": b})
    return _make_sheet(
        "Worked Example",
        ["To find a missing DIVIDEND, multiply the other two numbers.",
         "To find a missing DIVISOR, divide the dividend by the quotient.",
         "? / 6 = 7: missing dividend = 7 x 6 = 42."],
        "array_example", {"rows": 6, "cols": 7},
        "Missing dividend: multiply. Missing divisor: divide the dividend by the quotient.",
        builder, sheet, seed_base=140)


def _CUM5_s(sheet):
    def builder(i, sheet):
        a, b = random.randint(2,9), random.randint(2,9)
        product = a*b
        if i % 2 == 0:
            return q(f"{a} x {b} = {product}. So {product} / {a} = ____", "diagram", "____", "", "array_blank", {"rows":a,"cols":b})
        else:
            return q(f"? / {b} = {a}. Missing = ____", "diagram", "____", "", "array_blank", {"rows":a,"cols":b})
    return _make_sheet(
        "Review", ["Mix of fact families and missing numbers."],
        "array_example", {"rows": 6, "cols": 7},
        "Use multiplication facts to help with both skills.", builder, sheet, seed_base=500)


# ───────────────────────── N/O: Speed (separated skills) ─────────────────────────

def _N_s(sheet):
    """Basic fact speed."""
    def builder(i, sheet):
        divisor = random.choice([2,3,4,5,6,7,8,9])
        n = random.randint(1,9)
        return _div_q(divisor*n, divisor, "(instant)")
    return _make_sheet(
        "Worked Example", ["Speed round: recall your division facts instantly."],
        "array_example", {"rows": 7, "cols": 6},
        "Answer as quickly as you can.", builder, sheet, seed_base=150)


def _O_s(sheet):
    """/10, /100 -- a different, place-value-based skill."""
    def builder(i, sheet):
        power = random.choice([10,100])
        n = random.randint(2,9)
        dividend = n*power
        return q(f"{dividend} / {power} = ____  (remove a zero for /10, two zeros for /100)",
                  "diagram", "____", "", "array_blank", {"rows": 1, "cols": n})
    return _make_sheet(
        "Worked Example",
        ["Dividing by 10 or 100 is a place-value shortcut, not a fact to memorize.",
         "480 / 10 = 48 (remove one zero). 4800 / 100 = 48 (remove two zeros)."],
        "array_example", {"rows": 1, "cols": 48},
        "Remove one zero for /10, two zeros for /100.", builder, sheet, seed_base=160)


def _CUM6_s(sheet):
    def builder(i, sheet):
        if i % 2 == 0:
            divisor = random.choice([2,3,4,5,6,7,8,9]); n = random.randint(1,9)
            return _div_q(divisor*n, divisor)
        else:
            power = random.choice([10,100]); n = random.randint(2,9)
            return q(f"{n*power} / {power} = ____", "diagram", "____", "", "array_blank", {"rows":1,"cols":n})
    return _make_sheet(
        "Review", ["Mix of basic facts and /10, /100 shortcuts."],
        "array_example", {"rows": 1, "cols": 48},
        "Use instant recall for facts, the zero-shortcut for /10 and /100.", builder, sheet, seed_base=600)


# ───────────────────────── P/Q: Puzzles (tiered) ─────────────────────────

def _P_s(sheet):
    def builder(i, sheet):
        divisor = random.randint(3,9)
        lo = divisor*random.randint(3,6)
        hi = lo + divisor + 2
        return q(f"I am divisible by {divisor}. I am between {lo} and {hi}. What am I?",
                  "diagram", "____", "", "array_blank", {"rows": divisor, "cols": 1})
    return _make_sheet(
        "Worked Example", ["List the multiples of the number, then pick the one in range."],
        "array_example", {"rows": 6, "cols": 5},
        "List multiples, then check the range.", builder, sheet, seed_base=170)


def _Q_s(sheet):
    """Tier 2: LCM/digit constraints, explicitly taught."""
    def builder(i, sheet):
        if i % 2 == 0:
            a, b = random.sample([2,3,4,5,6,7,8], 2)
            limit = random.randint(40,80)
            return q(f"I am divisible by BOTH {a} and {b}. I am less than {limit}. What am I?",
                      "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
        else:
            divisor = random.choice([6,7,8,9])
            ds = random.randint(5,14)
            return q(f"I am a 2-digit number divisible by {divisor}. My digits sum to {ds}. What am I?",
                      "diagram", "____", "", "array_blank", {"rows": divisor, "cols": 1})
    return _make_sheet(
        "Worked Example (Harder)",
        ["A number divisible by BOTH numbers must appear in both their multiple lists -- compare the lists.",
         "Divisible by 2: 2,4,6,8,10,12. Divisible by 3: 3,6,9,12. Both lists: 6 and 12.",
         "For digit-sum clues, list multiples of the divisor and check which one's digits add up correctly."],
        "array_example", {"rows": 6, "cols": 7},
        "List multiples of each number/check digit sums, then find what fits every clue.",
        builder, sheet, seed_base=180)


def _CUM7_s(sheet):
    def builder(i, sheet):
        choice = i % 2
        if choice == 0:
            divisor = random.randint(3,9); lo = divisor*3; hi = lo+divisor+2
            return q(f"Divisible by {divisor}, between {lo} and {hi}?", "diagram", "____", "", "array_blank", {"rows":divisor,"cols":1})
        else:
            a,b = random.sample([2,3,4,5,6],2); limit = random.randint(40,80)
            return q(f"Divisible by both {a} and {b}, less than {limit}?", "diagram", "____", "", "array_blank", {"rows":a,"cols":b})
    return _make_sheet(
        "Review", ["Mix of simple and harder divisibility puzzles."],
        "array_example", {"rows": 6, "cols": 7},
        "Use the strategy that fits the puzzle type.", builder, sheet, seed_base=700)


# ───────────────────────── R/REV ─────────────────────────

def _R_s(sheet):
    def builder(i, sheet):
        choice = i % 5
        divisor = random.randint(2,9); n = random.randint(2,9)
        if choice == 0:
            return _div_q(divisor*n, divisor)
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
    return _make_sheet(
        "Worked Example", ["Mixed challenge: every division skill from this level."],
        "division_box_example", {"dividend": 78, "divisor": 3, "partials": [(10, 48), (10, 18), (6, 0)]},
        "Read each one carefully, then solve.", builder, sheet, seed_base=190)


def _REV_s(sheet):
    def builder(i, sheet):
        choice = i % 6
        divisor = random.randint(2,9); n = random.randint(2,9)
        if choice == 0:
            return _div_q(divisor*n, divisor)
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
    return _make_sheet(
        "Level 5 Revision",
        ["Every division skill: facts, remainders, long division, word problems, and puzzles."],
        "division_box_example", {"dividend": 78, "divisor": 3, "partials": [(10, 48), (10, 18), (6, 0)]},
        "Work through each question using the strategy that fits.", builder, sheet, seed_base=800)


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
