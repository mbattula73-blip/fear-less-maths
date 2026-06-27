"""
Fear Less Maths — LEVEL 4 REDESIGN (Multiplication, Grade 2-3)

Replaces the original Level 4 in place. Based on detailed analysis of
the original content (which bundled tables 2-5 and 6-10 with zero
strategy connection between them, introduced the "split method" and
three different mental-math tricks by showing them mid-question with no
teaching step, used the term "square numbers" without ever defining it,
and jumped from simple word problems straight to a 2-step/3-number
problem and from basic facts straight to LCM/factor-pair puzzles) plus
research into the internationally-consistent times-table teaching order:
0s/1s -> 2s (doubling) -> 10s (place value) -> 5s (half of 10s) -> 3s ->
4s (double the 2s) -> 6s -> 9s (x10 minus one group) -> 8s (double the
4s) -> 7s (hardest, last, derived from known facts). Crucially, each
new table is explicitly taught as a CONNECTION to one already known,
not a fresh, disconnected fact set.

Same worksheet format as Levels 3/6/7: ONE worked example, ONE
instruction line stated once, 20 bare-expression questions (15
pictorial blank-diagram + 5 numeral), B&W outline-only diagrams.

Sub-level list (25 total):
  A Concept (repeated addition + arrays)
  B x0 and x1 (confidence builders)     C x2 and x10 (doubling / place value)
  D x5 (half of x10)
  CUM1 review
  E x3 and x4 (4s = double the 2s)      F x6 and x9 (9s = x10 minus one group)
  CUM2 review
  G x8 (double the 4s)                  H x7 (hardest, last, derived facts)
  CUM3 review
  I Square numbers (explicitly defined) J Multi-digit / split method (taught)
  CUM4 review
  K Word problems - single step         L Word problems - two step (separated)
  CUM5 review
  M Patterns (skip count/digit patterns) N Speed drills (strategies already taught)
  CUM6 review
  O Puzzles - Tier 1 (simple)           P Puzzles - Tier 2 (LCM/factors, taught)
  CUM7 review
  Q Mixed challenge                     REV Revision
"""
import random
from content import cb, tb, q

# ───────────────────────── shared helpers ─────────────────────────

def _array_q(rows, cols):
    return q(f"{rows} x {cols} = ____", "diagram", "____", "", "array_blank", {"rows": rows, "cols": cols})


def _groups_q(groups, size):
    return q(f"{groups} x {size} = ____", "diagram", "____", "", "equal_groups_blank",
              {"groups": groups, "size": size})


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
        groups = random.randint(2,4); size = random.randint(2,5)
        if i % 2 == 0:
            return _groups_q(groups, size)
        else:
            return _array_q(groups, size)
    return _make_sheet(
        "Worked Example",
        ["Multiplication means adding the same group over and over.",
         "3 groups of 4 = 4+4+4 = 3 x 4 = 12. An array shows the same idea as rows and columns."],
        "equal_groups_example", {"groups": 3, "size": 4},
        "Count the groups and the size of each, then multiply.", builder, sheet, seed_base=10)


# ───────────────────────── B/C/D: Easy tables ─────────────────────────

def _B_s(sheet):
    """x0 and x1."""
    def builder(i, sheet):
        n = random.randint(1,9)
        if i % 2 == 0:
            return q(f"{n} x 1 = ____", "diagram", "____", "", "array_blank", {"rows": 1, "cols": n})
        else:
            return q(f"{n} x 0 = ____", "diagram", "____", "", "array_blank", {"rows": 1, "cols": 1})
    return _make_sheet(
        "Worked Example",
        ["Any number x 1 stays the same -- 1 group of that size.",
         "Any number x 0 is always 0 -- 0 groups means nothing there."],
        "array_example", {"rows": 1, "cols": 5},
        "Remember: x1 keeps the number the same, x0 always makes 0.",
        builder, sheet, seed_base=20)


def _C_s(sheet):
    """x2 (doubling) and x10 (place value)."""
    def builder(i, sheet):
        n = random.randint(1,9)
        if i % 2 == 0:
            return q(f"{n} x 2 = ____  (double {n})", "diagram", "____", "", "array_blank", {"rows": 2, "cols": n})
        else:
            return q(f"{n} x 10 = ____", "diagram", "____", "", "array_blank", {"rows": 1, "cols": n})
    return _make_sheet(
        "Worked Example",
        ["x2 means double the number.",
         "x10 means add a zero -- 7 x 10 = 70, because 7 tens = 70."],
        "array_example", {"rows": 2, "cols": 6},
        "For x2, double the number. For x10, add a zero.",
        builder, sheet, seed_base=30)


def _D_s(sheet):
    """x5, explicitly linked to x10."""
    def builder(i, sheet):
        n = random.randint(1,9)
        return q(f"{n} x 5 = ____  (half of {n} x 10 = half of {n*10})", "diagram", "____",
                  "", "array_blank", {"rows": 5, "cols": n})
    return _make_sheet(
        "Worked Example",
        ["x5 is HALF of x10 -- you already know your x10 facts!",
         "6 x 5: first 6 x 10 = 60, then half of 60 = 30."],
        "array_example", {"rows": 5, "cols": 6},
        "Find x10 first, then take half to get x5.", builder, sheet, seed_base=40)


def _CUM1_s(sheet):
    def builder(i, sheet):
        n = random.randint(1,9)
        choice = i % 4
        if choice == 0: return q(f"{n} x 1 = ____", "diagram", "____", "", "array_blank", {"rows":1,"cols":n})
        elif choice == 1: return q(f"{n} x 2 = ____", "diagram", "____", "", "array_blank", {"rows":2,"cols":n})
        elif choice == 2: return q(f"{n} x 10 = ____", "diagram", "____", "", "array_blank", {"rows":1,"cols":n})
        else: return q(f"{n} x 5 = ____", "diagram", "____", "", "array_blank", {"rows":5,"cols":n})
    return _make_sheet(
        "Review", ["Mix of x0, x1, x2, x10, and x5."],
        "array_example", {"rows": 2, "cols": 6},
        "Use the strategy you learned for each table.", builder, sheet, seed_base=100)


# ───────────────────────── E/F: Linked tables ─────────────────────────

def _E_s(sheet):
    """x3 and x4, with x4 = double the x2."""
    def builder(i, sheet):
        n = random.randint(1,9)
        if i % 2 == 0:
            return q(f"{n} x 3 = ____", "diagram", "____", "", "array_blank", {"rows": 3, "cols": n})
        else:
            return q(f"{n} x 4 = ____  (double of {n} x 2 = double of {n*2})", "diagram", "____",
                      "", "array_blank", {"rows": 4, "cols": n})
    return _make_sheet(
        "Worked Example",
        ["x4 is DOUBLE your x2 facts!",
         "6 x 4: first 6 x 2 = 12, then double 12 = 24."],
        "array_example", {"rows": 4, "cols": 6},
        "For x4, find x2 first, then double it.", builder, sheet, seed_base=50)


def _F_s(sheet):
    """x6 and x9, with x9 = x10 minus one group."""
    def builder(i, sheet):
        n = random.randint(1,9)
        if i % 2 == 0:
            return q(f"{n} x 6 = ____", "diagram", "____", "", "array_blank", {"rows": 6, "cols": n})
        else:
            return q(f"{n} x 9 = ____  ({n} x 10 minus one group of {n})", "diagram", "____",
                      "", "array_blank", {"rows": 9, "cols": n})
    return _make_sheet(
        "Worked Example",
        ["x9 is x10 MINUS one group -- one less than the x10 fact.",
         "7 x 9: first 7 x 10 = 70, then subtract one 7: 70 - 7 = 63."],
        "array_example", {"rows": 9, "cols": 7},
        "For x9, find x10 first, then subtract one group.", builder, sheet, seed_base=60)


def _CUM2_s(sheet):
    def builder(i, sheet):
        n = random.randint(1,9)
        choice = i % 4
        if choice == 0: return q(f"{n} x 3 = ____", "diagram", "____", "", "array_blank", {"rows":3,"cols":n})
        elif choice == 1: return q(f"{n} x 4 = ____", "diagram", "____", "", "array_blank", {"rows":4,"cols":n})
        elif choice == 2: return q(f"{n} x 6 = ____", "diagram", "____", "", "array_blank", {"rows":6,"cols":n})
        else: return q(f"{n} x 9 = ____", "diagram", "____", "", "array_blank", {"rows":9,"cols":n})
    return _make_sheet(
        "Review", ["Mix of x3, x4 (double x2), x6, and x9 (x10 minus one group)."],
        "array_example", {"rows": 9, "cols": 7},
        "Use the connection strategy for x4 and x9.", builder, sheet, seed_base=200)


# ───────────────────────── G/H: Hardest tables ─────────────────────────

def _G_s(sheet):
    """x8, double the x4."""
    def builder(i, sheet):
        n = random.randint(1,9)
        return q(f"{n} x 8 = ____  (double of {n} x 4 = double of {n*4})", "diagram", "____",
                  "", "array_blank", {"rows": 8, "cols": n})
    return _make_sheet(
        "Worked Example",
        ["x8 is DOUBLE your x4 facts (which were already double x2)!",
         "6 x 8: 6 x 4 = 24, then double 24 = 48."],
        "array_example", {"rows": 8, "cols": 6},
        "Find x4 first, then double it to get x8.", builder, sheet, seed_base=70)


def _H_s(sheet):
    """x7, last, derived from known facts."""
    def builder(i, sheet):
        n = random.randint(1,9)
        return q(f"{n} x 7 = ____  (use {n} x 6 + {n} more, or {n} x 8 - {n})", "diagram", "____",
                  "", "array_blank", {"rows": 7, "cols": n})
    return _make_sheet(
        "Worked Example",
        ["x7 is the last one -- use facts you already know to find it.",
         "6 x 7: you know 6 x 6 = 36, so add one more 6: 36 + 6 = 42."],
        "array_example", {"rows": 7, "cols": 6},
        "Use a nearby known fact (x6 or x8) and adjust by one group.",
        builder, sheet, seed_base=80)


def _CUM3_s(sheet):
    def builder(i, sheet):
        n = random.randint(1,9)
        return q(f"{n} x {random.choice([7,8])} = ____", "diagram", "____", "", "array_blank",
                  {"rows": random.choice([7,8]), "cols": n})
    return _make_sheet(
        "Review", ["The two hardest tables: x7 and x8. Use your connection strategies."],
        "array_example", {"rows": 8, "cols": 6},
        "Derive from a known fact rather than guessing.", builder, sheet, seed_base=300)


# ───────────────────────── I/J: Squares & multi-digit ─────────────────────────

def _I_s(sheet):
    def builder(i, sheet):
        n = random.randint(2,9)
        return q(f"{n} x {n} = ____  (the square of {n})", "diagram", "____", "", "array_blank",
                  {"rows": n, "cols": n})
    return _make_sheet(
        "Worked Example",
        ["A SQUARE NUMBER is a number multiplied by itself -- it makes a perfect square array.",
         "4 x 4 = 16 is a square number, because the array is a perfect square shape."],
        "array_example", {"rows": 5, "cols": 5},
        "Multiply each number by itself to find its square.", builder, sheet, seed_base=90)


def _J_s(sheet):
    def builder(i, sheet):
        tens = random.randint(1,4); ones = random.randint(1,9)
        n = tens*10+ones
        m = random.randint(2,5)
        return q(f"{n} x {m} = ({tens}0 x {m}) + ({ones} x {m}) = ____", "diagram", "____",
                  "", "array_blank", {"rows": m, "cols": ones})
    return _make_sheet(
        "Worked Example",
        ["Split the bigger number into tens and ones, multiply each part, then add.",
         "21 x 3 = (20 x 3) + (1 x 3) = 60 + 3 = 63."],
        "array_example", {"rows": 3, "cols": 1},
        "Split into tens and ones, multiply each part, then add the results.",
        builder, sheet, seed_base=95)


def _CUM4_s(sheet):
    def builder(i, sheet):
        if i % 2 == 0:
            n = random.randint(2,9)
            return q(f"{n} x {n} = ____", "diagram", "____", "", "array_blank", {"rows":n,"cols":n})
        else:
            tens=random.randint(1,4); ones=random.randint(1,9); m=random.randint(2,5)
            return q(f"{tens*10+ones} x {m} = ____", "diagram", "____", "", "array_blank", {"rows":m,"cols":ones})
    return _make_sheet(
        "Review", ["Mix of square numbers and the split method for bigger numbers."],
        "array_example", {"rows": 5, "cols": 5},
        "Use squares or the split method as needed.", builder, sheet, seed_base=400)


# ───────────────────────── K/L: Word problems (tiered) ─────────────────────────

def _K_s(sheet):
    """Single-step word problems."""
    templates = [
        "{g} packs of {s} biscuits. Total biscuits = ____.",
        "{g} baskets with {s} mangoes each. Total mangoes = ____.",
        "{g} rows of {s} chairs. Total chairs = ____.",
    ]
    def builder(i, sheet):
        g, s = random.randint(2,6), random.randint(2,9)
        txt = random.choice(templates).format(g=g, s=s)
        return q(txt, "diagram", "____", "", "equal_groups_blank", {"groups": g, "size": s})
    return _make_sheet(
        "Worked Example",
        ["Find the number of groups and the size of each group, then multiply."],
        "equal_groups_example", {"groups": 3, "size": 4},
        "One step: groups x size = total.", builder, sheet, seed_base=110)


def _L_s(sheet):
    """Two-step word problems, clearly separated as harder."""
    def builder(i, sheet):
        a, b, c = random.randint(2,5), random.randint(2,5), random.randint(2,4)
        return q(f"(Two steps) {a} boxes of {b} packets, each packet has {c} items. Total items = ____.",
                  "diagram", "____", "", "equal_groups_blank", {"groups": a*b, "size": c})
    return _make_sheet(
        "Worked Example",
        ["Two-step problems need TWO multiplications. Solve the first part, then use that answer.",
         "3 boxes of 4 packets = 12 packets. 12 packets x 2 items = 24 items total."],
        "equal_groups_example", {"groups": 3, "size": 4},
        "Solve the first multiplication, then multiply that answer by the last number.",
        builder, sheet, seed_base=120)


def _CUM5_s(sheet):
    def builder(i, sheet):
        if i % 2 == 0:
            g,s = random.randint(2,6), random.randint(2,9)
            return q(f"{g} groups of {s}. Total = ____.", "diagram", "____", "", "equal_groups_blank", {"groups":g,"size":s})
        else:
            a,b,c = random.randint(2,4), random.randint(2,4), random.randint(2,4)
            return q(f"{a} boxes of {b} packets, {c} items each. Total = ____.", "diagram", "____",
                      "", "equal_groups_blank", {"groups": a*b, "size": c})
    return _make_sheet(
        "Review", ["Mix of one-step and two-step word problems."],
        "equal_groups_example", {"groups": 3, "size": 4},
        "Check if it needs one multiplication or two.", builder, sheet, seed_base=500)


# ───────────────────────── M/N: Patterns & speed ─────────────────────────

def _M_s(sheet):
    def builder(i, sheet):
        step = random.choice([2,3,4,5,6])
        start = step*random.randint(1,4)
        return q(f"{start}, {start+step}, {start+step*2}, ____  (skip count by {step})",
                  "diagram", "____", "", "array_blank", {"rows": 1, "cols": step})
    return _make_sheet(
        "Worked Example",
        ["Each table is a skip-counting pattern -- the same jump size every time."],
        "array_example", {"rows": 1, "cols": 4},
        "Find the jump size, then continue the pattern.", builder, sheet, seed_base=130)


def _N_s(sheet):
    """Speed drills -- reuses strategies already taught, no new tricks."""
    def builder(i, sheet):
        n = random.randint(1,9)
        table = random.choice([2,4,5,8,9,10])
        return q(f"{n} x {table} = ____", "diagram", "____", "", "array_blank", {"rows": table, "cols": n})
    return _make_sheet(
        "Worked Example", ["Speed round: use the connection strategy you already learned for each table."],
        "array_example", {"rows": 8, "cols": 6},
        "Work quickly, using the strategy for each table.", builder, sheet, seed_base=140)


def _CUM6_s(sheet):
    def builder(i, sheet):
        if i % 2 == 0:
            step = random.choice([3,4,5,6]); start = step*random.randint(1,4)
            return q(f"{start}, {start+step}, ____, {start+step*3}", "diagram", "____", "", "array_blank", {"rows":1,"cols":step})
        else:
            n = random.randint(1,9); table = random.choice([2,4,5,7,8,9])
            return q(f"{n} x {table} = ____", "diagram", "____", "", "array_blank", {"rows":table,"cols":n})
    return _make_sheet(
        "Review", ["Mix of patterns and speed facts."],
        "array_example", {"rows": 8, "cols": 6},
        "Spot the pattern or use your strategy.", builder, sheet, seed_base=600)


# ───────────────────────── O/P: Puzzles (tiered) ─────────────────────────

def _O_s(sheet):
    """Tier 1: simple multiple-finding."""
    def builder(i, sheet):
        table = random.randint(3,9)
        lo = table*random.randint(2,4)
        hi = lo + table + 2
        return q(f"I am a multiple of {table}. I am between {lo} and {hi}. What am I?",
                  "diagram", "____", "", "array_blank", {"rows": table, "cols": 1})
    return _make_sheet(
        "Worked Example",
        ["List the multiples of the table, then pick the one that fits between the two numbers."],
        "array_example", {"rows": 6, "cols": 5},
        "List multiples of the table number, then check the range.", builder, sheet, seed_base=150)


def _P_s(sheet):
    """Tier 2: common multiples / factor pairs, explicitly taught."""
    def builder(i, sheet):
        if i % 2 == 0:
            a, b = random.sample([2,3,4,5,6], 2)
            limit = random.randint(20,40)
            return q(f"I am a multiple of BOTH {a} and {b}. I am less than {limit}. List me.",
                      "diagram", "____", "", "array_blank", {"rows": a, "cols": b})
        else:
            n = random.choice([12,16,18,20,24,30,36])
            return q(f"Find all factor pairs of {n}.", "diagram", "____", "", "array_blank",
                      {"rows": 2, "cols": n//2})
    return _make_sheet(
        "Worked Example (Harder)",
        ["A COMMON multiple fits BOTH tables -- check multiples of one table against the other.",
         "Multiples of 2: 2,4,6,8,10,12. Multiples of 3: 3,6,9,12. Common: 6 and 12.",
         "FACTOR PAIRS are two numbers that multiply to make the target -- try array shapes that fit exactly."],
        "array_example", {"rows": 3, "cols": 4},
        "For common multiples, list both tables and compare. For factor pairs, try every array shape that fits.",
        builder, sheet, seed_base=160)


def _CUM7_s(sheet):
    def builder(i, sheet):
        choice = i % 3
        if choice == 0:
            table = random.randint(3,9); lo = table*random.randint(2,4); hi = lo+table+2
            return q(f"Multiple of {table}, between {lo} and {hi}. What am I?", "diagram", "____", "", "array_blank", {"rows":table,"cols":1})
        elif choice == 1:
            a,b = random.sample([2,3,4,5,6],2); limit = random.randint(20,40)
            return q(f"Multiple of both {a} and {b}, less than {limit}. List me.", "diagram", "____", "", "array_blank", {"rows":a,"cols":b})
        else:
            n = random.choice([12,16,18,20,24]); return q(f"Find all factor pairs of {n}.", "diagram", "____", "", "array_blank", {"rows":2,"cols":n//2})
    return _make_sheet(
        "Review", ["Mix of simple and harder multiple/factor puzzles."],
        "array_example", {"rows": 3, "cols": 4},
        "Use the strategy that fits the puzzle type.", builder, sheet, seed_base=700)


# ───────────────────────── Q/REV ─────────────────────────

def _Q_s(sheet):
    def builder(i, sheet):
        choice = i % 4
        n = random.randint(1,9)
        if choice == 0:
            table = random.randint(2,9); return q(f"{n} x {table} = ____", "diagram", "____", "", "array_blank", {"rows":table,"cols":n})
        elif choice == 1:
            return q(f"{n} x {n} = ____ (square)", "diagram", "____", "", "array_blank", {"rows":n,"cols":n})
        elif choice == 2:
            g,s = random.randint(2,6), random.randint(2,9)
            return q(f"{g} groups of {s}. Total = ____.", "diagram", "____", "", "equal_groups_blank", {"groups":g,"size":s})
        else:
            table = random.randint(3,9); lo=table*2; hi=lo+table+2
            return q(f"Multiple of {table}, between {lo} and {hi}?", "diagram", "____", "", "array_blank", {"rows":table,"cols":1})
    return _make_sheet(
        "Worked Example", ["Mixed challenge: every multiplication skill from this level."],
        "array_example", {"rows": 6, "cols": 7},
        "Read each one carefully, then solve.", builder, sheet, seed_base=170)


def _REV_s(sheet):
    def builder(i, sheet):
        choice = i % 6
        n = random.randint(1,9)
        if choice == 0:
            return q(f"{n} x 1 = ____", "diagram", "____", "", "array_blank", {"rows":1,"cols":n})
        elif choice == 1:
            table = random.randint(2,6); return q(f"{n} x {table} = ____", "diagram", "____", "", "array_blank", {"rows":table,"cols":n})
        elif choice == 2:
            table = random.choice([7,8,9]); return q(f"{n} x {table} = ____", "diagram", "____", "", "array_blank", {"rows":table,"cols":n})
        elif choice == 3:
            return q(f"{n} x {n} = ____", "diagram", "____", "", "array_blank", {"rows":n,"cols":n})
        elif choice == 4:
            g,s = random.randint(2,6), random.randint(2,9)
            return q(f"{g} groups of {s}. Total = ____.", "diagram", "____", "", "equal_groups_blank", {"groups":g,"size":s})
        else:
            table = random.randint(3,9); lo=table*2; hi=lo+table+2
            return q(f"Multiple of {table}, between {lo} and {hi}?", "diagram", "____", "", "array_blank", {"rows":table,"cols":1})
    return _make_sheet(
        "Level 4 Revision",
        ["Every multiplication skill: tables, squares, word problems, patterns, and puzzles."],
        "array_example", {"rows": 6, "cols": 7},
        "Work through each question using the strategy that fits.", builder, sheet, seed_base=800)


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
