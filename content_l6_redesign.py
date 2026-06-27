"""
Fear Less Maths — LEVEL 6 REDESIGN (Fractions, Class 5+)

Replaces the original Level 6 in place (per approval). Research-based on
Singapore Math (CPA + bar models), Common Core 5.NF standards, and
mainstream grade-5 curricula. Key gap fixed: the original Level 6 had
NO fraction multiplication or division, and no explicit GCF/LCM
treatment, despite both being mandatory grade-5 content everywhere.

Worksheet format per sub-level (consistent across all 4 sheets):
  - ONE worked example (concept_box with an icon diagram) showing a
    single fully-solved instance step by step -- no abstract rule list.
  - ONE instruction line (tips_box) stated once for all 20 questions.
  - 20 questions: bare "a/b OP c/d = ____" expressions only, no
    repeated sentence -- pictorial (blank shade-it-yourself diagram)
    for the first 15, plain numeral for the last 5 (CPA structure,
    matching every other level in this app).

Sub-level list (21 total -- bigger than other levels because real
content was missing):
  A Fraction concept       B Unit fractions & decomposition    C Proper/improper/mixed
  CUM1 review
  D Equivalent fractions   E Simplify via GCF                  F Compare via LCM/benchmarks
  CUM2 review
  G Add/sub LIKE            H Add/sub UNLIKE                    I Add/sub mixed numbers
  CUM3 review
  J Multiply fractions     K Multiply mixed numbers            L Divide fractions
  CUM4 review
  M Word problems          N Estimation/benchmarks             O Speed/puzzles
  P Mixed challenge        REV Revision
"""
import random
import math
from content import cb, tb, q

# ───────────────────────── shared helpers ─────────────────────────

def _gcd(a, b):
    return math.gcd(a, b)


def _lcm(a, b):
    return a * b // math.gcd(a, b)


def _rand_fraction(max_den=8):
    den = random.randint(2, max_den)
    num = random.randint(1, den - 1)
    return num, den


def _bar_q(num, den):
    return q(f"{num}/{den} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den})


def _two_bar_q(num1, den1, num2, den2, op_symbol):
    return q(f"{num1}/{den1} {op_symbol} {num2}/{den2} = ____", "diagram", "____",
              "", "two_bars_blank", {"den1": den1, "den2": den2})


def _area_q(n1, d1, n2, d2):
    return q(f"{n1}/{d1} x {n2}/{d2} = ____", "diagram", "____", "", "fraction_area_blank",
              {"den1": d1, "den2": d2})


def _numline_q(num, den):
    return q(f"Place {num}/{den} on the number line.", "diagram", "____",
              "", "fraction_numberline_blank", {"den": den})


def _make_sheet(title_for_example, example_bullets, example_icon, example_params,
                instruction_text, question_builder, sheet, n_q=20, seed_base=0):
    """Standard sub-level sheet builder: 1 worked example + 1 instruction
    + n_q bare-expression questions. The first 15 questions keep their
    pictorial diagram; the last 5 have the diagram stripped (text is
    already the bare numeral expression, so removing the image alone
    gives the CPA 'Abstract' stage, matching every other level)."""
    random.seed(seed_base + sheet)
    items = [cb(title_for_example, example_bullets, "", icon_diagram=example_icon,
                icon_params=example_params)]
    items.append(tb("Instructions", [instruction_text]))
    questions = [question_builder(i, sheet) for i in range(n_q)]
    for i in range(15, len(questions)):
        questions[i] = dict(questions[i])
        questions[i]["diagram_type"] = None
        questions[i]["diagram_params"] = {}
    items.extend(questions)
    return items


# ───────────────────────── A: Fraction concept ─────────────────────────

def _A_s(sheet):
    def builder(i, sheet):
        num, den = _rand_fraction(6)
        return _bar_q(num, den)
    return _make_sheet(
        "Worked Example",
        ["A fraction shows parts of ONE whole.",
         "3/4 means: split the whole into 4 equal parts, take 3 of them."],
        "fraction_bar_example", {"num": 3, "den": 4},
        "Shade the bar to show each fraction.",
        builder, sheet, seed_base=10)


# ───────────────────────── B: Unit fractions & decomposition ─────────────────────────

def _B_s(sheet):
    def builder(i, sheet):
        den = random.randint(3, 8)
        num = random.randint(2, den - 1)
        return q(f"{num}/{den} = 1/{den} + 1/{den} + ... = ____ (how many 1/{den}s?)",
                  "diagram", "____", "", "fraction_bar_blank", {"den": den})
    return _make_sheet(
        "Worked Example",
        ["Every fraction is built from unit fractions (numerator 1).",
         "3/8 = 1/8 + 1/8 + 1/8 -- three 1/8 pieces."],
        "fraction_bar_example", {"num": 3, "den": 8, "label": "3/8 = 1/8+1/8+1/8"},
        "Shade the bar one unit piece at a time, then count how many you shaded.",
        builder, sheet, seed_base=20)


# ───────────────────────── C: Proper/improper/mixed ─────────────────────────

def _C_s(sheet):
    def builder(i, sheet):
        whole = random.randint(1, 3)
        den = random.randint(2, 6)
        extra = random.randint(0, den - 1)
        total_num = whole*den + extra
        return q(f"{total_num}/{den} = ____ (write as a mixed number)", "diagram", "____",
                  "", "fraction_bar_blank", {"den": den, "segments": whole + (1 if extra else 0)})
    return _make_sheet(
        "Worked Example",
        ["An IMPROPER fraction (numerator bigger than denominator) can be written as a MIXED number.",
         "7/3 = 2 whole bars + 1/3 left over = 2 1/3."],
        "fraction_bar_example", {"num": 1, "den": 3, "label": "7/3 = 2 wholes + 1/3"},
        "Shade whole bars first, then the leftover part, to convert each fraction.",
        builder, sheet, seed_base=30)


def _CUM1_s(sheet):
    def builder(i, sheet):
        choice = i % 3
        if choice == 0:
            num, den = _rand_fraction(6)
            return _bar_q(num, den)
        elif choice == 1:
            den = random.randint(3, 8)
            num = random.randint(2, den-1)
            return q(f"{num}/{den} = 1/{den} + ... = ____ pieces", "diagram", "____",
                      "", "fraction_bar_blank", {"den": den})
        else:
            whole = random.randint(1, 2)
            den = random.randint(2, 5)
            extra = random.randint(1, den-1)
            return q(f"{whole*den+extra}/{den} = ____ (mixed number)", "diagram", "____",
                      "", "fraction_bar_blank", {"den": den, "segments": whole+1})
    return _make_sheet(
        "Review", ["Mix of fraction concept, decomposition, and mixed numbers."],
        "fraction_bar_example", {"num": 3, "den": 4},
        "Shade each bar to solve.", builder, sheet, seed_base=100)


# ───────────────────────── D: Equivalent fractions ─────────────────────────

def _D_s(sheet):
    def builder(i, sheet):
        den1 = random.randint(2, 5)
        mult = random.randint(2, 4)
        num1 = random.randint(1, den1-1)
        den2 = den1*mult
        return q(f"{num1}/{den1} = ____/{den2}", "diagram", "____",
                  "", "two_bars_blank", {"den1": den1, "den2": den2})
    return _make_sheet(
        "Worked Example",
        ["Equivalent fractions look different but show the SAME amount.",
         "1/3 = 2/6: the bars are split differently, but the same portion is shaded."],
        "two_bars_example", {"num1": 1, "den1": 3, "num2": 2, "den2": 6},
        "Shade the same amount in both bars, then count the second bar's pieces.",
        builder, sheet, seed_base=40)


# ───────────────────────── E: Simplify via GCF ─────────────────────────

def _E_s(sheet):
    def builder(i, sheet):
        den = random.choice([4, 6, 8, 9, 10, 12])
        num = random.randint(2, den-1)
        g = _gcd(num, den)
        if g == 1:
            num = num*2 if num*2 < den else num
            g = _gcd(num, den)
        return q(f"{num}/{den} = ____ (simplify using the GCF)", "diagram", "____",
                  "", "fraction_bar_blank", {"den": den})
    return _make_sheet(
        "Worked Example",
        ["Find the GCF (Greatest Common Factor) of the numerator and denominator.",
         "8/12: GCF of 8 and 12 is 4. Divide both by 4: 8/12 = 2/3."],
        "fraction_bar_example", {"num": 2, "den": 3, "label": "8/12 = 2/3 (GCF=4)"},
        "Find the GCF of each fraction's numerator and denominator, then simplify.",
        builder, sheet, seed_base=50)


# ───────────────────────── F: Compare via LCM/benchmarks ─────────────────────────

def _F_s(sheet):
    def builder(i, sheet):
        den1, den2 = random.sample([2,3,4,5,6,8], 2)
        num1 = random.randint(1, den1-1)
        num2 = random.randint(1, den2-1)
        return q(f"{num1}/{den1} ___ {num2}/{den2}  (>, < or =)", "diagram", "____",
                  "", "two_bars_blank", {"den1": den1, "den2": den2})
    return _make_sheet(
        "Worked Example",
        ["Use the LCM of the denominators to compare fairly.",
         "1/3 vs 2/4: LCM of 3,4 is 12. 1/3=4/12, 2/4=6/12, so 1/3 < 2/4.",
         "Or use benchmarks: is each fraction closer to 0, 1/2, or 1?"],
        "two_bars_example", {"num1": 1, "den1": 3, "num2": 2, "den2": 4},
        "Use the LCM to compare, or compare to the 1/2 benchmark.",
        builder, sheet, seed_base=60)


def _CUM2_s(sheet):
    def builder(i, sheet):
        choice = i % 3
        if choice == 0:
            den1 = random.randint(2,5); mult = random.randint(2,3)
            num1 = random.randint(1, den1-1)
            return q(f"{num1}/{den1} = ____/{den1*mult}", "diagram", "____",
                      "", "two_bars_blank", {"den1": den1, "den2": den1*mult})
        elif choice == 1:
            den = random.choice([6,8,9,10])
            num = random.randint(2, den-1)
            return q(f"{num}/{den} = ____ (simplest form)", "diagram", "____",
                      "", "fraction_bar_blank", {"den": den})
        else:
            den1, den2 = random.sample([2,3,4,5,6], 2)
            num1 = random.randint(1, den1-1); num2 = random.randint(1, den2-1)
            return q(f"{num1}/{den1} ___ {num2}/{den2}", "diagram", "____",
                      "", "two_bars_blank", {"den1": den1, "den2": den2})
    return _make_sheet(
        "Review", ["Mix of equivalent fractions, simplifying, and comparing."],
        "two_bars_example", {"num1": 1, "den1": 3, "num2": 2, "den2": 6},
        "Use bars, GCF, or LCM as needed.", builder, sheet, seed_base=200)


# ───────────────────────── G/H/I: Add/Subtract ─────────────────────────

def _G_s(sheet):
    """LIKE denominators."""
    def builder(i, sheet):
        den = random.randint(3, 8)
        n1 = random.randint(1, den-1)
        n2 = random.randint(1, den-n1)
        op = "+" if i % 2 == 0 else "-"
        if op == "-":
            n1, n2 = max(n1,n2), min(n1,n2)
        return q(f"{n1}/{den} {op} {n2}/{den} = ____", "diagram", "____",
                  "", "fraction_bar_blank", {"den": den})
    return _make_sheet(
        "Worked Example",
        ["Same denominator: just add or subtract the numerators.",
         "2/8 + 3/8 = 5/8 (denominator stays the same)."],
        "fraction_bar_example", {"num": 5, "den": 8, "label": "2/8 + 3/8 = 5/8"},
        "Shade the bar to find each sum or difference, keeping the denominator the same.",
        builder, sheet, seed_base=70)


def _H_s(sheet):
    """UNLIKE denominators."""
    def builder(i, sheet):
        den1, den2 = random.sample([2,3,4,5,6], 2)
        n1 = random.randint(1, den1-1)
        n2 = random.randint(1, den2-1)
        op = "+" if i % 2 == 0 else "-"
        return q(f"{n1}/{den1} {op} {n2}/{den2} = ____", "diagram", "____",
                  "", "two_bars_blank", {"den1": den1, "den2": den2})
    return _make_sheet(
        "Worked Example",
        ["Different denominators: find the LCM first, convert both fractions, then add/subtract.",
         "1/3 + 1/4: LCM=12. 1/3=4/12, 1/4=3/12. 4/12+3/12=7/12."],
        "two_bars_example", {"num1": 1, "den1": 3, "num2": 1, "den2": 4},
        "Find the LCM, convert both fractions to that denominator, then add or subtract.",
        builder, sheet, seed_base=80)


def _I_s(sheet):
    """Mixed numbers."""
    def builder(i, sheet):
        w1, w2 = random.randint(1,3), random.randint(1,2)
        den = random.randint(2,6)
        n1, n2 = random.randint(1,den-1), random.randint(1,den-1)
        op = "+" if i % 2 == 0 else "-"
        if op == "-":
            w1 = max(w1,w2)+1
        return q(f"{w1} {n1}/{den} {op} {w2} {n2}/{den} = ____", "diagram", "____",
                  "", "fraction_bar_blank", {"den": den, "segments": w1+1})
    return _make_sheet(
        "Worked Example",
        ["Add/subtract the whole numbers and the fractions separately, then combine.",
         "2 1/4 + 1 2/4 = (2+1) + (1/4+2/4) = 3 + 3/4 = 3 3/4."],
        "fraction_bar_example", {"num": 3, "den": 4, "label": "2 1/4 + 1 2/4 = 3 3/4"},
        "Shade whole bars and fraction parts separately, then combine.",
        builder, sheet, seed_base=90)


def _CUM3_s(sheet):
    def builder(i, sheet):
        choice = i % 3
        if choice == 0:
            den = random.randint(3,8); n1=random.randint(1,den-1); n2=random.randint(1,den-n1)
            return q(f"{n1}/{den} + {n2}/{den} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den})
        elif choice == 1:
            den1,den2 = random.sample([2,3,4,5,6],2); n1=random.randint(1,den1-1); n2=random.randint(1,den2-1)
            return q(f"{n1}/{den1} + {n2}/{den2} = ____", "diagram", "____", "", "two_bars_blank", {"den1":den1,"den2":den2})
        else:
            w1=random.randint(1,2); den=random.randint(2,5); n1=random.randint(1,den-1)
            return q(f"{w1} {n1}/{den} + 1/{den} = ____", "diagram", "____", "", "fraction_bar_blank", {"den":den,"segments":w1+1})
    return _make_sheet(
        "Review", ["Mix of like, unlike, and mixed-number addition/subtraction."],
        "two_bars_example", {"num1":1,"den1":3,"num2":1,"den2":4},
        "Identify like vs unlike denominators, then solve.", builder, sheet, seed_base=300)


# ───────────────────────── J/K/L: Multiply/Divide ─────────────────────────

def _J_s(sheet):
    def builder(i, sheet):
        n1,d1 = _rand_fraction(5); n2,d2 = _rand_fraction(5)
        return _area_q(n1,d1,n2,d2)
    return _make_sheet(
        "Worked Example",
        ["Shade columns for the first fraction, rows for the second.",
         "The double-shaded squares out of the total squares are the answer.",
         "2/3 x 3/4: 6 of 12 squares double-shaded = 6/12 = 1/2."],
        "fraction_area_example", {"num1":2,"den1":3,"num2":3,"den2":4},
        "Shade the grid for each fraction pair, then write the answer in simplest form.",
        builder, sheet, seed_base=110)


def _K_s(sheet):
    def builder(i, sheet):
        whole = random.randint(2,5)
        n,d = _rand_fraction(6)
        return q(f"{whole} x {n}/{d} = ____", "diagram", "____", "", "fraction_bar_blank",
                  {"den": d, "segments": whole})
    return _make_sheet(
        "Worked Example",
        ["Multiplying a whole number by a fraction means repeating that fraction.",
         "3 x 2/5 = 2/5 + 2/5 + 2/5 = 6/5 = 1 1/5."],
        "fraction_bar_example", {"num":1,"den":5,"label":"3 x 2/5 = 6/5 = 1 1/5"},
        "Shade the fraction that many times, then add up the total.",
        builder, sheet, seed_base=120)


def _L_s(sheet):
    def builder(i, sheet):
        if i % 2 == 0:
            den = random.randint(2,6); whole = random.randint(2,4)
            return q(f"1/{den} / {whole} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den*whole})
        else:
            den = random.randint(2,5)
            return q(f"{random.randint(2,5)} / 1/{den} = ____", "diagram", "____",
                      "", "fraction_numberline_blank", {"den": den})
    return _make_sheet(
        "Worked Example",
        ["Dividing a unit fraction by a whole number splits it into even smaller pieces.",
         "1/3 / 2 = 1/6 (split each third in half).",
         "Dividing a whole number by a unit fraction counts how many pieces fit.",
         "2 / 1/4 = 8 (there are 8 quarters in 2 wholes)."],
        "fraction_bar_example", {"num":1,"den":6,"label":"1/3 / 2 = 1/6"},
        "Shade or mark the diagram to find each quotient.",
        builder, sheet, seed_base=130)


def _CUM4_s(sheet):
    def builder(i, sheet):
        choice = i % 3
        if choice == 0:
            n1,d1=_rand_fraction(5); n2,d2=_rand_fraction(5)
            return _area_q(n1,d1,n2,d2)
        elif choice == 1:
            whole=random.randint(2,4); n,d=_rand_fraction(5)
            return q(f"{whole} x {n}/{d} = ____", "diagram", "____", "", "fraction_bar_blank", {"den":d,"segments":whole})
        else:
            den=random.randint(2,5); whole=random.randint(2,4)
            return q(f"1/{den} / {whole} = ____", "diagram", "____", "", "fraction_bar_blank", {"den":den*whole})
    return _make_sheet(
        "Review", ["Mix of multiplying and dividing fractions."],
        "fraction_area_example", {"num1":2,"den1":3,"num2":3,"den2":4},
        "Use the grid or bar to solve each one.", builder, sheet, seed_base=400)


# ───────────────────────── M: Word problems ─────────────────────────

def _M_s(sheet):
    templates = [
        ("A recipe needs {n1}/{d1} cup sugar and {n2}/{d1} cup flour. How much in total?", "+"),
        ("A ribbon is {n1}/{d1} m long. {n2}/{d1} m is cut off. How much is left?", "-"),
        ("{whole} friends share {n2}/{d1} of a pizza equally. How much does each get?", "div"),
        ("A jug has {n1}/{d1} L of juice. {whole} more jugs are added. How much juice now?", "mul"),
    ]
    def builder(i, sheet):
        d1 = random.randint(3,8)
        n1 = random.randint(1, d1-1)
        n2 = random.randint(1, d1-n1) if d1-n1 > 0 else 1
        whole = random.randint(2,4)
        text, op = templates[i % len(templates)]
        txt = text.format(n1=n1, n2=n2, d1=d1, whole=whole)
        return q(txt, "diagram", "____", "", "fraction_bar_blank", {"den": d1})
    return _make_sheet(
        "Worked Example",
        ["Read carefully: are parts being joined, removed, shared, or repeated?",
         "'Half the cake is left, then 1/4 is eaten' means subtract: 1/2 - 1/4 = 1/4."],
        "fraction_bar_example", {"num":1,"den":4,"label":"1/2 - 1/4 = 1/4"},
        "Picture the story with the bar, then solve.",
        builder, sheet, seed_base=140)


# ───────────────────────── N: Estimation / benchmarks ─────────────────────────

def _N_s(sheet):
    def builder(i, sheet):
        n, d = _rand_fraction(8)
        return _numline_q(n, d)
    return _make_sheet(
        "Worked Example",
        ["Compare each fraction to the benchmarks 0, 1/2, and 1.",
         "3/8 is just under 1/2, so place it slightly left of the middle."],
        "fraction_numberline_example", {"num":1,"den":2},
        "Mark each fraction's position on the number line using 0, 1/2, and 1 as guides.",
        builder, sheet, seed_base=150)


# ───────────────────────── O/P/REV ─────────────────────────

def _O_s(sheet):
    def builder(i, sheet):
        choice = i % 4
        if choice == 0:
            n,d = _rand_fraction(6); return _bar_q(n,d)
        elif choice == 1:
            n1,d1=_rand_fraction(5); n2,d2=_rand_fraction(5); return _area_q(n1,d1,n2,d2)
        elif choice == 2:
            den1,den2=random.sample([2,3,4,5,6],2); n1=random.randint(1,den1-1); n2=random.randint(1,den2-1)
            return q(f"{n1}/{den1} + {n2}/{den2} = ____", "diagram", "____", "", "two_bars_blank", {"den1":den1,"den2":den2})
        else:
            n,d = _rand_fraction(8); return _numline_q(n,d)
    return _make_sheet(
        "Worked Example", ["Speed round: work quickly but carefully through each picture."],
        "fraction_bar_example", {"num":3,"den":4},
        "Solve each one as quickly as you can.", builder, sheet, seed_base=160)


def _P_s(sheet):
    def builder(i, sheet):
        choice = i % 5
        if choice == 0:
            n,d = _rand_fraction(6); return _bar_q(n,d)
        elif choice == 1:
            n1,d1=_rand_fraction(5); n2,d2=_rand_fraction(5); return _area_q(n1,d1,n2,d2)
        elif choice == 2:
            den1,den2=random.sample([2,3,4,5,6],2); n1=random.randint(1,den1-1); n2=random.randint(1,den2-1)
            return q(f"{n1}/{den1} - {n2}/{den2} = ____" if n1*den2>n2*den1 else f"{n2}/{den2} - {n1}/{den1} = ____",
                      "diagram", "____", "", "two_bars_blank", {"den1":den1,"den2":den2})
        elif choice == 3:
            den=random.randint(2,5); whole=random.randint(2,4)
            return q(f"1/{den} / {whole} = ____", "diagram", "____", "", "fraction_bar_blank", {"den":den*whole})
        else:
            n,d = _rand_fraction(8); return _numline_q(n,d)
    return _make_sheet(
        "Worked Example", ["Mixed challenge: every fraction skill from this level."],
        "fraction_area_example", {"num1":2,"den1":3,"num2":3,"den2":4},
        "Read each one carefully, then solve.", builder, sheet, seed_base=170)


def _REV_s(sheet):
    def builder(i, sheet):
        choice = i % 6
        if choice == 0:
            n,d = _rand_fraction(6); return _bar_q(n,d)
        elif choice == 1:
            n1,d1=_rand_fraction(5); n2,d2=_rand_fraction(5); return _area_q(n1,d1,n2,d2)
        elif choice == 2:
            den1,den2=random.sample([2,3,4,5,6],2); n1=random.randint(1,den1-1); n2=random.randint(1,den2-1)
            return q(f"{n1}/{den1} + {n2}/{den2} = ____", "diagram", "____", "", "two_bars_blank", {"den1":den1,"den2":den2})
        elif choice == 3:
            den=random.randint(2,5); whole=random.randint(2,4)
            return q(f"1/{den} / {whole} = ____", "diagram", "____", "", "fraction_bar_blank", {"den":den*whole})
        elif choice == 4:
            n,d = _rand_fraction(8); return _numline_q(n,d)
        else:
            den=random.choice([6,8,9,10]); num=random.randint(2,den-1)
            return q(f"{num}/{den} = ____ (simplest form)", "diagram", "____", "", "fraction_bar_blank", {"den":den})
    return _make_sheet(
        "Level 6 Revision", ["Every fraction skill: concept, equivalence, operations, and word problems."],
        "two_bars_example", {"num1":1,"den1":3,"num2":2,"den2":4},
        "Work through each question using the bars, grids, or number lines.",
        builder, sheet, seed_base=500)


# ───────────────────────── Dispatcher (REPLACES original Level 6) ─────────────────────────

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL6_DISPATCH = {
    "6A": _wrap(_A_s), "6B": _wrap(_B_s), "6C": _wrap(_C_s), "6CUM1": _wrap(_CUM1_s),
    "6D": _wrap(_D_s), "6E": _wrap(_E_s), "6F": _wrap(_F_s), "6CUM2": _wrap(_CUM2_s),
    "6G": _wrap(_G_s), "6H": _wrap(_H_s), "6I": _wrap(_I_s), "6CUM3": _wrap(_CUM3_s),
    "6J": _wrap(_J_s), "6K": _wrap(_K_s), "6L": _wrap(_L_s), "6CUM4": _wrap(_CUM4_s),
    "6M": _wrap(_M_s), "6N": _wrap(_N_s), "6O": _wrap(_O_s), "6P": _wrap(_P_s),
    "6REV": _wrap(_REV_s),
}
