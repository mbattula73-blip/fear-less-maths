"""
Fear Less Maths — LEVEL 7 REDESIGN (Decimals, Class 5+)

Replaces the original Level 7 in place. Research-based on documented,
persistent decimal misconceptions (Resnick et al. 1989; DeWolf &
Vosniadou 2014; Durkin & Rittle-Johnson) that standard practice alone
does not fix:
  - "Longer-is-larger": 0.45 thought > 0.5 (whole-number overgeneralization)
  - "Shorter-is-larger": 0.25 thought > 0.8 (fraction-reasoning error)
  - Trailing-zero distrust: 0.4 = 0.40 = 0.400 not believed
  - "Multiplication always bigger, division always smaller" -- breaks
    down for decimals (4 / 0.5 = 8)
  - Fraction-decimal disconnect (0.5 not spontaneously linked to 1/2)

The single most evidence-backed remedy found (Durkin & Rittle-Johnson):
having students compare CORRECT and INCORRECT worked examples side by
side measurably reduces these errors more than standard practice alone.
This is built in directly as its own sub-level (F, "Spot the Mistake"),
not left as an afterthought.

Same worksheet format as Level 6: ONE worked example (no abstract rule
list), ONE instruction line stated once, 20 bare-expression questions
(15 pictorial/blank-diagram + 5 numeral), all diagrams black-and-white
outline-only with hatching (not flat colour) for the one worked example.

Sub-level list (20 total):
  A Tenths (bar model)         B Hundredths (100-grid)        C Thousandths & place value
  CUM1 review
  D Trailing zeros don't change value     E Comparing via place-value chart
  F Spot the Mistake (research-backed misconception correction)
  CUM2 review
  G Decimal <-> Fraction       H Decimals on a number line (ordering/magnitude)
  CUM3 review
  I Add/subtract decimals      J Multiply decimals (x10/100, decimal x decimal)
  K Divide decimals (incl. quotient > dividend, busting the "division shrinks" myth)
  CUM4 review
  L Money word problems        M Rounding decimals          N Speed & puzzles
  O Mixed challenge            REV Revision
"""
import random
from content import cb, tb, q

# ───────────────────────── shared helpers ─────────────────────────

def _bar_q(num, den=10):
    return q(f"{num}/{den} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den})


def _grid100_q(shaded):
    return q(f"{shaded}/100 = ____", "diagram", "____", "", "hundredths_grid_blank", {})


def _place_q(number, n_decimal=2):
    return q(f"Write {number} in the place value chart.", "diagram", "____",
              "", "decimal_place_blank", {"n_decimal": n_decimal})


def _numline_q(lo, hi, divisions):
    return q(f"Place the decimal on the number line.", "diagram", "____",
              "", "decimal_numberline_blank", {"lo": lo, "hi": hi, "divisions": divisions})


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


# ───────────────────────── A/B/C: Place value foundation ─────────────────────────

def _A_s(sheet):
    def builder(i, sheet):
        return _bar_q(random.randint(1, 9), 10)
    return _make_sheet(
        "Worked Example",
        ["A decimal's tenths digit means 'out of 10 equal parts'.",
         "0.7 means 7 of the 10 parts are shaded."],
        "fraction_bar_example", {"num": 7, "den": 10, "label": "0.7 = 7/10"},
        "Shade the bar to show each decimal, then write it as a fraction over 10.",
        builder, sheet, seed_base=10)


def _B_s(sheet):
    def builder(i, sheet):
        return _grid100_q(random.randint(5, 95))
    return _make_sheet(
        "Worked Example",
        ["A decimal's hundredths digit means 'out of 100 equal squares'.",
         "0.25 means 25 of the 100 squares are shaded."],
        "hundredths_grid_example", {"shaded": 25},
        "Shade the grid to show each decimal as hundredths.",
        builder, sheet, seed_base=20)


def _C_s(sheet):
    def builder(i, sheet):
        whole = random.randint(1, 9)
        dec = random.randint(0, 999)
        number = f"{whole}.{str(dec).zfill(3)}"
        return _place_q(number, 3)
    return _make_sheet(
        "Worked Example",
        ["Thousandths extend the place value chart one more column to the right.",
         "3.470: 3 ones, 4 tenths, 7 hundredths, 0 thousandths."],
        "decimal_place_example", {"number": "3.470"},
        "Write each number into the place value chart, one digit per box.",
        builder, sheet, seed_base=30)


def _CUM1_s(sheet):
    def builder(i, sheet):
        choice = i % 3
        if choice == 0:
            return _bar_q(random.randint(1,9), 10)
        elif choice == 1:
            return _grid100_q(random.randint(5,95))
        else:
            whole = random.randint(1,9); dec = random.randint(0,99)
            return _place_q(f"{whole}.{str(dec).zfill(2)}", 2)
    return _make_sheet(
        "Review", ["Mix of tenths, hundredths, and place value."],
        "decimal_place_example", {"number": "3.47"},
        "Use the bar, grid, or chart to answer.", builder, sheet, seed_base=100)


# ───────────────────────── D/E/F: Misconception-busting ─────────────────────────

def _D_s(sheet):
    """Trailing zeros don't change value."""
    def builder(i, sheet):
        whole = random.randint(0,9); dec = random.randint(1,9)
        n_zeros = random.randint(1,2)
        a = f"{whole}.{dec}"
        b = f"{whole}.{dec}{'0'*n_zeros}"
        return q(f"{a} ___ {b}  (>, < or =)", "diagram", "____",
                  "", "decimal_place_blank", {"n_decimal": 1+n_zeros})
    return _make_sheet(
        "Worked Example",
        ["Adding zeros to the END of a decimal does NOT change its value.",
         "0.4 = 0.40 = 0.400 -- they all show exactly 4 tenths."],
        "decimal_place_example", {"number": "0.400"},
        "Compare each pair. Remember: trailing zeros don't change the value.",
        builder, sheet, seed_base=40)


def _E_s(sheet):
    """Comparing via place-value chart, digit by digit from the left."""
    def builder(i, sheet):
        whole = random.randint(0,9)
        d1 = random.randint(0,99); d2 = random.randint(0,99)
        a = f"{whole}.{str(d1).zfill(2)}"
        b = f"{whole}.{str(d2).zfill(2)}"
        return q(f"{a} ___ {b}  (>, < or =)", "diagram", "____",
                  "", "decimal_place_blank", {"n_decimal": 2})
    return _make_sheet(
        "Worked Example",
        ["Compare digit by digit, starting from the LEFT of the decimal point.",
         "4.859 vs 4.869: ones match (4), tenths match (8), hundredths differ: 5<6, so 4.859 < 4.869."],
        "decimal_place_example", {"number": "4.869"},
        "Fill in the place value chart for both numbers, then compare digit by digit from the left.",
        builder, sheet, seed_base=50)


def _F_s(sheet):
    """Spot the Mistake -- research-backed: compare correct vs incorrect reasoning."""
    wrong_examples = [
        ("'0.45 > 0.5 because 45 > 5.' Right or wrong? Compare 0.45 and 0.5.", False),
        ("'0.7 = 0.07 because same digits.' Right or wrong? Compare 0.7 and 0.07.", False),
        ("'0.25 > 0.8 because 25 > 8.' Right or wrong? Compare 0.25 and 0.8.", False),
        ("'0.3 = 0.30.' Right or wrong? Compare 0.3 and 0.30.", True),
        ("'0.6 > 0.59 because 6 > 5.' Right or wrong? Compare 0.6 and 0.59.", True),
        ("'0.09 > 0.1 because it has more digits.' Right or wrong?", False),
    ]
    def builder(i, sheet):
        text, correct = wrong_examples[i % len(wrong_examples)]
        return q(text, "diagram", "____ (RIGHT/WRONG)", "", "decimal_place_blank", {"n_decimal": 2})
    return _make_sheet(
        "Worked Example",
        ["Some students make mistakes by treating decimals like whole numbers.",
         "'0.45 > 0.5 because 45 > 5' is WRONG -- 0.5 = 0.50, and 50 > 45, so 0.5 is bigger."],
        "decimal_place_example", {"number": "0.50"},
        "Read what the student said. Use the place value chart to decide if they are right or wrong.",
        builder, sheet, seed_base=60)


def _CUM2_s(sheet):
    def builder(i, sheet):
        choice = i % 3
        whole = random.randint(0,9)
        if choice == 0:
            dec = random.randint(1,9); nz = random.randint(1,2)
            return q(f"{whole}.{dec} ___ {whole}.{dec}{'0'*nz}", "diagram", "____", "", "decimal_place_blank", {"n_decimal": 1+nz})
        elif choice == 1:
            d1,d2 = random.randint(0,99), random.randint(0,99)
            return q(f"{whole}.{str(d1).zfill(2)} ___ {whole}.{str(d2).zfill(2)}", "diagram", "____", "", "decimal_place_blank", {"n_decimal":2})
        else:
            return q(f"Is 0.{random.randint(1,9)}{random.randint(0,9)} bigger or smaller than 0.5? Check carefully.",
                      "diagram", "____", "", "decimal_place_blank", {"n_decimal": 2})
    return _make_sheet(
        "Review", ["Mix of trailing zeros, comparing, and spotting mistakes."],
        "decimal_place_example", {"number": "0.50"},
        "Use the place value chart every time -- never guess from the number of digits.",
        builder, sheet, seed_base=200)


# ───────────────────────── G/H: Fraction-decimal bridge ─────────────────────────

def _G_s(sheet):
    def builder(i, sheet):
        den = random.choice([2,4,5,10,20,25])
        num = random.randint(1, den-1)
        if i % 2 == 0:
            return q(f"{num}/{den} = ____ (write as a decimal)", "diagram", "____",
                      "", "fraction_bar_blank", {"den": den})
        else:
            return q(f"0.{random.choice([5,25,75,2,4,6,8])} = ____ (write as a fraction)",
                      "diagram", "____", "", "fraction_bar_blank", {"den": 10})
    return _make_sheet(
        "Worked Example",
        ["A fraction with denominator 10, 100, or that simplifies to one, can be written as a decimal.",
         "1/2 = 0.5  and  0.5 = 1/2 -- they are the same value, just different notation."],
        "fraction_bar_example", {"num": 1, "den": 2, "label": "1/2 = 0.5"},
        "Convert each one, using the bar model to help you see the connection.",
        builder, sheet, seed_base=70)


def _H_s(sheet):
    def builder(i, sheet):
        whole = random.randint(0,2)
        dec = round(random.uniform(0,1), 2)
        value = round(whole+dec, 2)
        return _numline_q(whole, whole+1, 10)
    return _make_sheet(
        "Worked Example",
        ["Decimals can be placed exactly on a number line -- this shows their TRUE size.",
         "0.45 is just before 0.5 (the midpoint), NOT bigger than it."],
        "decimal_numberline_example", {"value": 0.45, "lo": 0.0, "hi": 1.0, "divisions": 10},
        "Mark each decimal's position on its number line.",
        builder, sheet, seed_base=80)


def _CUM3_s(sheet):
    def builder(i, sheet):
        choice = i % 2
        if choice == 0:
            den = random.choice([2,4,5,10]); num = random.randint(1,den-1)
            return q(f"{num}/{den} = ____ (decimal)", "diagram", "____", "", "fraction_bar_blank", {"den": den})
        else:
            return _numline_q(0, 1, 10)
    return _make_sheet(
        "Review", ["Mix of fraction-decimal conversion and number line placement."],
        "decimal_numberline_example", {"value": 0.45, "lo": 0.0, "hi": 1.0, "divisions": 10},
        "Convert or place each decimal as shown.", builder, sheet, seed_base=300)


# ───────────────────────── I/J/K: Operations ─────────────────────────

def _I_s(sheet):
    def builder(i, sheet):
        whole = random.randint(0,9)
        d1, d2 = random.randint(1,9), random.randint(1,9)
        op = "+" if i % 2 == 0 else "-"
        if op == "-" and d1 < d2:
            d1, d2 = d2, d1
        return q(f"{whole}.{d1} {op} 0.{d2} = ____", "diagram", "____",
                  "", "decimal_place_blank", {"n_decimal": 1})
    return _make_sheet(
        "Worked Example",
        ["Line up the decimal points, then add or subtract column by column, just like whole numbers.",
         "3.4 + 0.8 = 4.2 (the tenths add up to 12, carry 1 to the ones)."],
        "decimal_place_example", {"number": "4.2"},
        "Line up the decimal points in the chart, then add or subtract.",
        builder, sheet, seed_base=90)


def _J_s(sheet):
    def builder(i, sheet):
        if i % 2 == 0:
            d = round(random.uniform(0.1, 9.9), 1)
            power = random.choice([10, 100])
            return q(f"{d} x {power} = ____", "diagram", "____", "", "decimal_place_blank", {"n_decimal": 2})
        else:
            a = round(random.uniform(0.1, 0.9), 1)
            b = round(random.uniform(0.1, 0.9), 1)
            return q(f"{a} x {b} = ____", "diagram", "____", "", "hundredths_grid_blank", {})
    return _make_sheet(
        "Worked Example",
        ["Multiplying by 10 shifts every digit one place to the LEFT (decimal point moves right).",
         "0.4 x 0.3 = 0.12 (use the 100-grid: shade 4 columns and 3 rows, overlap = 12 squares = 0.12)."],
        "hundredths_grid_example", {"shaded": 12},
        "Use the place value chart for x10/x100, and the grid for decimal x decimal.",
        builder, sheet, seed_base=110)


def _K_s(sheet):
    """Includes cases where quotient > dividend, busting the 'division shrinks' myth."""
    def builder(i, sheet):
        if i % 2 == 0:
            # whole number / decimal less than 1 -> quotient BIGGER than dividend
            whole = random.randint(2,8)
            divisor = random.choice([0.5, 0.25, 0.2])
            return q(f"{whole} / {divisor} = ____  (is the answer bigger or smaller than {whole}?)",
                      "diagram", "____", "", "decimal_numberline_blank", {"lo": 0, "hi": whole*4, "divisions": 8})
        else:
            d = round(random.uniform(1.0, 9.0), 1)
            power = random.choice([10, 100])
            return q(f"{d} / {power} = ____", "diagram", "____", "", "decimal_place_blank", {"n_decimal": 3})
    return _make_sheet(
        "Worked Example",
        ["Dividing by a number SMALLER than 1 makes the answer BIGGER, not smaller!",
         "4 / 0.5 = 8 (there are 8 halves in 4 wholes) -- the answer is bigger than 4."],
        "decimal_numberline_example", {"value": 8, "lo": 0, "hi": 10, "divisions": 10},
        "Work out each answer. For division, check: is your answer bigger or smaller than you expected?",
        builder, sheet, seed_base=120)


def _CUM4_s(sheet):
    def builder(i, sheet):
        choice = i % 3
        whole = random.randint(0,9)
        if choice == 0:
            d1,d2 = random.randint(1,9), random.randint(1,9)
            return q(f"{whole}.{d1} + 0.{d2} = ____", "diagram", "____", "", "decimal_place_blank", {"n_decimal":1})
        elif choice == 1:
            d = round(random.uniform(0.1,9.9),1)
            return q(f"{d} x 10 = ____", "diagram", "____", "", "decimal_place_blank", {"n_decimal":2})
        else:
            w = random.randint(2,8)
            return q(f"{w} / 0.5 = ____", "diagram", "____", "", "decimal_numberline_blank", {"lo":0,"hi":w*3,"divisions":6})
    return _make_sheet(
        "Review", ["Mix of adding, subtracting, multiplying, and dividing decimals."],
        "decimal_numberline_example", {"value": 8, "lo": 0, "hi": 10, "divisions": 10},
        "Watch out: dividing by a number less than 1 makes the answer bigger.",
        builder, sheet, seed_base=400)


# ───────────────────────── L/M/N/O/REV ─────────────────────────

def _L_s(sheet):
    templates = [
        "A pencil costs ${a}.{b}. How much do 2 pencils cost?",
        "You have $5.00 and spend ${a}.{b}. How much is left?",
        "A juice box costs ${a}.{b}. How much for 3 boxes?",
    ]
    def builder(i, sheet):
        a = random.randint(0,4); b = random.randint(10,99)
        txt = templates[i % len(templates)].format(a=a, b=b)
        return q(txt, "diagram", "____", "", "decimal_place_blank", {"n_decimal": 2})
    return _make_sheet(
        "Worked Example",
        ["Money is a natural decimal: dollars are ones, cents are hundredths.",
         "$3.47 means 3 dollars and 47 cents -- exactly like the place value chart."],
        "decimal_place_example", {"number": "3.47"},
        "Use the place value chart to work out each money problem.",
        builder, sheet, seed_base=130)


def _M_s(sheet):
    def builder(i, sheet):
        whole = random.randint(0,9); dec = random.randint(0,999)
        number = f"{whole}.{str(dec).zfill(3)}"
        place = random.choice(["nearest tenth", "nearest hundredth", "nearest whole number"])
        return q(f"Round {number} to the {place}.", "diagram", "____",
                  "", "decimal_place_blank", {"n_decimal": 3})
    return _make_sheet(
        "Worked Example",
        ["Look at the digit just after the place you're rounding to.",
         "3.47 rounded to the nearest tenth: look at the hundredths digit (7), round up -> 3.5."],
        "decimal_place_example", {"number": "3.47"},
        "Use the place value chart to round each decimal.",
        builder, sheet, seed_base=140)


def _N_s(sheet):
    def builder(i, sheet):
        choice = i % 4
        if choice == 0: return _bar_q(random.randint(1,9), 10)
        elif choice == 1: return _grid100_q(random.randint(5,95))
        elif choice == 2:
            whole=random.randint(0,9); d1,d2=random.randint(0,99),random.randint(0,99)
            return q(f"{whole}.{str(d1).zfill(2)} ___ {whole}.{str(d2).zfill(2)}", "diagram", "____", "", "decimal_place_blank", {"n_decimal":2})
        else: return _numline_q(0,1,10)
    return _make_sheet(
        "Worked Example", ["Speed round: work quickly but carefully."],
        "decimal_place_example", {"number": "3.47"},
        "Solve each one as quickly as you can.", builder, sheet, seed_base=150)


def _O_s(sheet):
    def builder(i, sheet):
        choice = i % 5
        whole = random.randint(0,9)
        if choice == 0: return _grid100_q(random.randint(5,95))
        elif choice == 1:
            d1,d2=random.randint(1,9),random.randint(1,9)
            return q(f"{whole}.{d1} + 0.{d2} = ____", "diagram", "____", "", "decimal_place_blank", {"n_decimal":1})
        elif choice == 2: return _numline_q(0,1,10)
        elif choice == 3:
            den=random.choice([2,4,5,10]); num=random.randint(1,den-1)
            return q(f"{num}/{den} = ____ (decimal)", "diagram", "____", "", "fraction_bar_blank", {"den":den})
        else:
            w=random.randint(2,8)
            return q(f"{w} / 0.5 = ____", "diagram", "____", "", "decimal_numberline_blank", {"lo":0,"hi":w*3,"divisions":6})
    return _make_sheet(
        "Worked Example", ["Mixed challenge: every decimal skill from this level."],
        "hundredths_grid_example", {"shaded": 25},
        "Read each one carefully, then solve.", builder, sheet, seed_base=160)


def _REV_s(sheet):
    def builder(i, sheet):
        choice = i % 6
        whole = random.randint(0,9)
        if choice == 0: return _bar_q(random.randint(1,9), 10)
        elif choice == 1: return _grid100_q(random.randint(5,95))
        elif choice == 2:
            d1,d2=random.randint(0,99),random.randint(0,99)
            return q(f"{whole}.{str(d1).zfill(2)} ___ {whole}.{str(d2).zfill(2)}", "diagram", "____", "", "decimal_place_blank", {"n_decimal":2})
        elif choice == 3: return _numline_q(0,1,10)
        elif choice == 4:
            d1,d2=random.randint(1,9),random.randint(1,9)
            return q(f"{whole}.{d1} + 0.{d2} = ____", "diagram", "____", "", "decimal_place_blank", {"n_decimal":1})
        else:
            w=random.randint(2,8)
            return q(f"{w} / 0.5 = ____", "diagram", "____", "", "decimal_numberline_blank", {"lo":0,"hi":w*3,"divisions":6})
    return _make_sheet(
        "Level 7 Revision",
        ["Every decimal skill: place value, comparing, fractions, operations, and money."],
        "decimal_place_example", {"number": "3.47"},
        "Work through each question using the bar, grid, chart, or number line.",
        builder, sheet, seed_base=500)


# ───────────────────────── Dispatcher (REPLACES original Level 7) ─────────────────────────

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL7_DISPATCH = {
    "7A": _wrap(_A_s), "7B": _wrap(_B_s), "7C": _wrap(_C_s), "7CUM1": _wrap(_CUM1_s),
    "7D": _wrap(_D_s), "7E": _wrap(_E_s), "7F": _wrap(_F_s), "7CUM2": _wrap(_CUM2_s),
    "7G": _wrap(_G_s), "7H": _wrap(_H_s), "7CUM3": _wrap(_CUM3_s),
    "7I": _wrap(_I_s), "7J": _wrap(_J_s), "7K": _wrap(_K_s), "7CUM4": _wrap(_CUM4_s),
    "7L": _wrap(_L_s), "7M": _wrap(_M_s), "7N": _wrap(_N_s), "7O": _wrap(_O_s),
    "7REV": _wrap(_REV_s),
}
