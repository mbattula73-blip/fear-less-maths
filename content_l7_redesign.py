"""
Fear Less Maths — LEVEL 7 REDESIGN v2 (Decimals, Grade 5+)

Replaces the original Level 7 in place. v1 already fixed the
misconception-correction gaps (Spot the Mistake, trailing zeros, the
division-makes-bigger myth). v2 fixes the "same worksheet for every
sheet" problem using the SAME shared architecture as Level 8 v2
(question_formats.py): each sub-level has up to 6 question-format
builders (computation, True/False, missing-number, numeral,
multi-select, matching) and 4 SHEET TEMPLATES, each picking a different
combination/order of formats. Worked examples stay inline on the
worksheet (every sheet), per the same engine fix used for Level 8.

Sub-level list (20 total, unchanged from v1):
  A Tenths (bar model)         B Hundredths (100-grid)        C Thousandths & place value
  CUM1 review
  D Trailing zeros don't change value     E Comparing via place-value chart
  F Spot the Mistake (misconception correction)
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
from question_formats import TEMPLATES, diff_range, make_rotated_sheet, make_format_builders

# ───────────────────────── A: Tenths ─────────────────────────

def _A_s(sheet):
    lo, hi = diff_range(sheet, 1, 9)
    def comp(i, sheet):
        num = random.randint(1, 9)
        return q(f"{num}/10 = ____ (decimal)", "diagram", "____", "", "fraction_bar_blank", {"den": 10})
    def tf(i, sheet):
        num = random.randint(1, 9)
        correct = f"0.{num}"
        shown = correct if random.random() > 0.4 else f"0.0{num}"
        return q(f"True or False: {num}/10 = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        num = random.randint(1, 8)
        return q(f"____ /10 = 0.{num+1} minus 0.1", "diagram", "____", "", "fraction_bar_blank", {"den": 10})
    def numeral(i, sheet):
        num = random.randint(1, 9)
        return q(f"{num}/10 = ____", "fill", "____")
    def multisel(i, sheet):
        num = random.randint(1, 9)
        opts = [f"0.{num}", f"{num}/10", f"0.0{num}", f"{num}0/100"]
        return q(f"Which represent the same value as {num} tenths? Select ALL: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        nums = random.sample(range(1, 9), 3)
        lefts = [f"{n}/10" for n in nums]; rights = [f"0.{n}" for n in nums]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each fraction to its decimal: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["A decimal's tenths digit means 'out of 10 equal parts'. 0.7 means 7 of the 10 parts are shaded."],
        "fraction_bar_example", {"num": 7, "den": 10, "label": "0.7 = 7/10"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=10)


# ───────────────────────── B: Hundredths ─────────────────────────

def _B_s(sheet):
    def comp(i, sheet):
        shaded = random.randint(5, 95)
        return q(f"{shaded}/100 = ____", "diagram", "____", "", "hundredths_grid_blank", {})
    def tf(i, sheet):
        shaded = random.randint(5, 95)
        correct = f"0.{str(shaded).zfill(2)}"
        shown = correct if random.random() > 0.4 else f"0.{shaded}0"
        return q(f"True or False: {shaded}/100 = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        shaded = random.randint(5, 95)
        return q(f"____ /100 = 0.{str(shaded).zfill(2)}", "diagram", "____", "", "hundredths_grid_blank", {})
    def numeral(i, sheet):
        shaded = random.randint(5, 95)
        return q(f"{shaded}/100 = ____", "fill", "____")
    def multisel(i, sheet):
        shaded = random.randint(10, 90)
        opts = [f"0.{shaded}", f"{shaded}/100", f"0.0{shaded}", f"{shaded//10}/10"]
        return q(f"Which equal {shaded} hundredths? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        vals = random.sample(range(10, 95), 3)
        lefts = [f"{v}/100" for v in vals]; rights = [f"0.{v}" for v in vals]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each fraction to its decimal: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["A decimal's hundredths digit means 'out of 100 equal squares'. 0.25 means 25 of the 100 squares shaded."],
        "hundredths_grid_example", {"shaded": 25},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=20)


# ───────────────────────── C: Thousandths & place value ─────────────────────────

def _C_s(sheet):
    def comp(i, sheet):
        whole = random.randint(1, 9); dec = random.randint(0, 999)
        return q(f"Write {whole}.{str(dec).zfill(3)} in the place value chart.", "diagram", "____",
                  "", "decimal_place_blank", {"n_decimal": 3})
    def tf(i, sheet):
        whole = random.randint(1, 9); dec = random.randint(0, 999)
        number = f"{whole}.{str(dec).zfill(3)}"
        tenths_digit = str(dec).zfill(3)[0]
        shown_correct = random.random() > 0.4
        shown = tenths_digit if shown_correct else str((int(tenths_digit)+1) % 10)
        return q(f"True or False: in {number}, the tenths digit is {shown}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        whole = random.randint(1, 9); dec = random.randint(0, 999)
        return q(f"{whole}.{str(dec).zfill(3)} has ____ in the hundredths place.", "diagram", "____",
                  "", "decimal_place_blank", {"n_decimal": 3})
    def numeral(i, sheet):
        whole = random.randint(1, 9); dec = random.randint(0, 999)
        return q(f"Write {whole}.{str(dec).zfill(3)} in the place value chart. ____", "fill", "____")
    def multisel(i, sheet):
        whole = random.randint(1, 9); dec = random.randint(100, 999)
        number = f"{whole}.{dec}"
        opts = [f"{whole} ones", f"{str(dec)[0]} tenths", f"{str(dec)[1]} hundredths", f"{str(dec)[2]} thousandths"]
        return q(f"For {number}, which are correct? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        whole = random.randint(1, 9); dec = random.randint(100, 999)
        digits = str(dec)
        lefts = ["Tenths", "Hundredths", "Thousandths"]
        rights = list(digits)
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"For {whole}.{digits}, match each place to its digit: {left_str}  to  {right_str}",
                  "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Thousandths extend the place value chart one more column to the right.",
         "3.470: 3 ones, 4 tenths, 7 hundredths, 0 thousandths."],
        "decimal_place_example", {"number": "3.470"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=30)


def _CUM1_s(sheet):
    def comp(i, sheet):
        choice = i % 2
        if choice == 0:
            num = random.randint(1, 9)
            return q(f"{num}/10 = ____", "diagram", "____", "", "fraction_bar_blank", {"den": 10})
        shaded = random.randint(5, 95)
        return q(f"{shaded}/100 = ____", "diagram", "____", "", "hundredths_grid_blank", {})
    def tf(i, sheet):
        whole = random.randint(1, 9); dec = random.randint(0, 99)
        number = f"{whole}.{str(dec).zfill(2)}"
        return q(f"True or False: {number} has {whole} ones.", "fill", "____ (True/False)")
    def missing(i, sheet):
        whole = random.randint(1, 9); dec = random.randint(0, 99)
        return q(f"{whole}.{str(dec).zfill(2)}: tenths digit = ____", "diagram", "____",
                  "", "decimal_place_blank", {"n_decimal": 2})
    def numeral(i, sheet):
        shaded = random.randint(5, 95)
        return q(f"{shaded}/100 = ____", "fill", "____")
    def multisel(i, sheet):
        num = random.randint(1, 9)
        opts = [f"0.{num}", f"{num}/10", f"0.0{num}", f"{num}0/100"]
        return q(f"Which equal {num} tenths? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        vals = random.sample(range(10, 95), 3)
        lefts = [f"{v}/100" for v in vals]; rights = [f"0.{v}" for v in vals]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of tenths, hundredths, and place value."],
        "decimal_place_example", {"number": "3.47"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=100)


# ───────────────────────── D: Trailing zeros ─────────────────────────

def _D_s(sheet):
    def comp(i, sheet):
        whole = random.randint(0, 9); dec = random.randint(1, 9); nz = random.randint(1, 2)
        return q(f"{whole}.{dec} ___ {whole}.{dec}{'0'*nz}  (>, < or =)", "diagram", "____",
                  "", "decimal_place_blank", {"n_decimal": 1+nz})
    def tf(i, sheet):
        whole = random.randint(0, 9); dec = random.randint(1, 9); nz = random.randint(1, 2)
        return q(f"True or False: {whole}.{dec} = {whole}.{dec}{'0'*nz}", "fill", "____ (True/False)")
    def missing(i, sheet):
        whole = random.randint(0, 9); dec = random.randint(1, 9)
        return q(f"{whole}.{dec} = {whole}.{dec}____  (add a zero, value stays the same)", "diagram", "____",
                  "", "decimal_place_blank", {"n_decimal": 2})
    def numeral(i, sheet):
        whole = random.randint(0, 9); dec = random.randint(1, 9); nz = random.randint(1, 2)
        return q(f"{whole}.{dec} ___ {whole}.{dec}{'0'*nz}", "fill", "____")
    def multisel(i, sheet):
        whole = random.randint(0, 9); dec = random.randint(1, 9)
        opts = [f"{whole}.{dec}0", f"{whole}.{dec}00", f"{whole}.0{dec}", f"{whole}.{dec}"]
        return q(f"Which equal {whole}.{dec}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        vals = random.sample(range(1, 9), 3)
        whole = random.randint(0, 9)
        lefts = [f"{whole}.{v}" for v in vals]
        rights = [f"{whole}.{v}0" for v in vals]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each to its equal value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Adding zeros to the END of a decimal does NOT change its value.",
         "0.4 = 0.40 = 0.400 -- they all show exactly 4 tenths."],
        "decimal_place_example", {"number": "0.400"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=40)


# ───────────────────────── E: Comparing via place value chart ─────────────────────────

def _E_s(sheet):
    def comp(i, sheet):
        whole = random.randint(0, 9); d1 = random.randint(0, 99); d2 = random.randint(0, 99)
        return q(f"{whole}.{str(d1).zfill(2)} ___ {whole}.{str(d2).zfill(2)}  (>, < or =)", "diagram", "____",
                  "", "decimal_place_blank", {"n_decimal": 2})
    def tf(i, sheet):
        whole = random.randint(0, 9); d1 = random.randint(0, 99); d2 = random.randint(0, 99)
        correct = ">" if d1 > d2 else ("<" if d1 < d2 else "=")
        shown = correct if random.random() > 0.4 else random.choice([s for s in [">", "<", "="] if s != correct])
        return q(f"True or False: {whole}.{str(d1).zfill(2)} {shown} {whole}.{str(d2).zfill(2)}", "fill", "____ (True/False)")
    def missing(i, sheet):
        whole = random.randint(0, 9); d1 = random.randint(0, 99)
        return q(f"{whole}.{str(d1).zfill(2)} > ____  (give a smaller decimal with the same whole number)",
                  "diagram", "____", "", "decimal_place_blank", {"n_decimal": 2})
    def numeral(i, sheet):
        whole = random.randint(0, 9); d1 = random.randint(0, 99); d2 = random.randint(0, 99)
        return q(f"{whole}.{str(d1).zfill(2)} ___ {whole}.{str(d2).zfill(2)}", "fill", "____")
    def multisel(i, sheet):
        base = random.randint(0, 9) + random.randint(0, 99)/100
        opts = [round(base+0.1, 2), round(base-0.1, 2), round(base+0.01, 2), round(base, 2)]
        return q(f"Which are GREATER than {base}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        whole = random.randint(0, 9)
        vals = random.sample(range(0, 99), 3)
        lefts = [f"{whole}.{str(v).zfill(2)}" for v in vals]
        rights = [("smallest" if v == min(vals) else ("largest" if v == max(vals) else "middle")) for v in vals]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each decimal to its size rank: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Compare digit by digit, starting from the LEFT of the decimal point.",
         "4.859 vs 4.869: ones match, tenths match, hundredths differ: 5<6, so 4.859 < 4.869."],
        "decimal_place_example", {"number": "4.869"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=50)


# ───────────────────────── F: Spot the Mistake ─────────────────────────

def _F_s(sheet):
    wrong_examples = [
        ("'0.45 > 0.5 because 45 > 5.'", "0.45", "0.5", False),
        ("'0.7 = 0.07 because same digits.'", "0.7", "0.07", False),
        ("'0.25 > 0.8 because 25 > 8.'", "0.25", "0.8", False),
        ("'0.3 = 0.30.'", "0.3", "0.30", True),
        ("'0.6 > 0.59 because 6 > 5.'", "0.6", "0.59", True),
        ("'0.09 > 0.1 because it has more digits.'", "0.09", "0.1", False),
    ]
    def comp(i, sheet):
        text, a, b, correct = wrong_examples[i % len(wrong_examples)]
        return q(f"{text} Right or wrong? Compare {a} and {b}.", "diagram", "____ (RIGHT/WRONG)",
                  "", "decimal_place_blank", {"n_decimal": 2})
    def tf(i, sheet):
        text, a, b, correct = wrong_examples[i % len(wrong_examples)]
        return q(f"True or False: the claim {text} is correct.", "fill", "____ (True/False)")
    def missing(i, sheet):
        a = round(random.uniform(0, 1), 2)
        b = round(a + random.choice([-0.1, 0.1, -0.01, 0.01]), 2)
        return q(f"A student says {a} ___ {b}. Fill in the correct symbol (>,<,=).", "diagram", "____",
                  "", "decimal_place_blank", {"n_decimal": 2})
    def numeral(i, sheet):
        text, a, b, correct = wrong_examples[(i+2) % len(wrong_examples)]
        return q(f"{text} Right or wrong?", "fill", "____ (RIGHT/WRONG)")
    def multisel(i, sheet):
        return q("Which of these student claims are WRONG? Select ALL that apply: "
                  "A) 0.45>0.5 because 45>5  B) 0.3=0.30  C) 0.7=0.07 (same digits)  D) 0.6>0.59 because 6>5",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        claims = ["0.45>0.5", "0.3=0.30", "0.7=0.07", "0.09>0.1"]
        verdicts = ["WRONG", "RIGHT", "WRONG", "WRONG"]
        shuffled = verdicts[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(claims))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each claim to RIGHT or WRONG: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Some students treat decimals like whole numbers by mistake.",
         "'0.45 > 0.5 because 45 > 5' is WRONG -- 0.5 = 0.50, and 50 > 45, so 0.5 is bigger."],
        "decimal_place_example", {"number": "0.50"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=60)


def _CUM2_s(sheet):
    def comp(i, sheet):
        whole = random.randint(0, 9); dec = random.randint(1, 9); nz = random.randint(1, 2)
        return q(f"{whole}.{dec} ___ {whole}.{dec}{'0'*nz}", "diagram", "____", "", "decimal_place_blank", {"n_decimal": 1+nz})
    def tf(i, sheet):
        return q("True or False: '0.45 > 0.5 because 45 > 5' is a correct way to compare decimals.", "fill", "____ (True/False)")
    def missing(i, sheet):
        whole = random.randint(0, 9); d1 = random.randint(0, 99)
        return q(f"{whole}.{str(d1).zfill(2)} > ____", "diagram", "____", "", "decimal_place_blank", {"n_decimal": 2})
    def numeral(i, sheet):
        whole = random.randint(0, 9); d1 = random.randint(0, 99); d2 = random.randint(0, 99)
        return q(f"{whole}.{str(d1).zfill(2)} ___ {whole}.{str(d2).zfill(2)}", "fill", "____")
    def multisel(i, sheet):
        return q("Which are TRUE? Select ALL that apply: A) 0.3=0.30  B) 0.7=0.07  C) 0.6>0.59  D) 0.09>0.1",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        claims = ["0.3=0.30", "0.7=0.07", "0.6>0.59", "0.09>0.1"][:3]
        verdicts = ["RIGHT", "WRONG", "RIGHT"]
        shuffled = verdicts[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(claims))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of trailing zeros, comparing, and spotting mistakes."],
        "decimal_place_example", {"number": "0.50"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=200)


# ───────────────────────── G: Decimal <-> Fraction ─────────────────────────

def _G_s(sheet):
    nice_fracs = [(1,2,0.5),(1,4,0.25),(3,4,0.75),(1,5,0.2),(2,5,0.4),(3,5,0.6),(4,5,0.8),(1,10,0.1)]
    def comp(i, sheet):
        num, den, dec = random.choice(nice_fracs)
        if i % 2 == 0:
            return q(f"{num}/{den} = ____ (decimal)", "diagram", "____", "", "fraction_bar_blank", {"den": den})
        return q(f"{dec} = ____ (fraction)", "diagram", "____", "", "fraction_bar_blank", {"den": 10})
    def tf(i, sheet):
        num, den, dec = random.choice(nice_fracs)
        shown = dec if random.random() > 0.4 else round(dec+0.1, 2)
        return q(f"True or False: {num}/{den} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        num, den, dec = random.choice(nice_fracs)
        return q(f"____ /{den} = {dec}", "diagram", "____", "", "fraction_bar_blank", {"den": den})
    def numeral(i, sheet):
        num, den, dec = random.choice(nice_fracs)
        return q(f"{num}/{den} = ____", "fill", "____")
    def multisel(i, sheet):
        num, den, dec = random.choice(nice_fracs)
        opts = [str(dec), f"{num}/{den}", str(round(dec+0.1,2)), f"{den}/{num}"]
        return q(f"Which equal {num}/{den}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        chosen = random.sample(nice_fracs, 3)
        lefts = [f"{n}/{d}" for n, d, dec in chosen]
        rights = [str(dec) for n, d, dec in chosen]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each fraction to its decimal: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["A fraction with denominator 10, 100, or one that simplifies to one, can become a decimal.",
         "1/2 = 0.5 and 0.5 = 1/2 -- the same value, different notation."],
        "fraction_bar_example", {"num": 1, "den": 2, "label": "1/2 = 0.5"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=70)


# ───────────────────────── H: Decimals on a number line ─────────────────────────

def _H_s(sheet):
    def comp(i, sheet):
        value = round(random.uniform(0, 1), 2)
        return q(f"Place {value} on the number line.", "diagram", "____", "", "decimal_numberline_blank",
                  {"lo": 0.0, "hi": 1.0, "divisions": 10})
    def tf(i, sheet):
        a = round(random.uniform(0, 1), 2)
        claim_half = a < 0.5
        shown_correct = random.random() > 0.4
        word = "less than" if (claim_half == shown_correct) else "greater than"
        return q(f"True or False: {a} is {word} 0.5", "fill", "____ (True/False)")
    def missing(i, sheet):
        a = round(random.uniform(0, 0.4), 2); b = round(random.uniform(0.6, 1), 2)
        return q(f"{a} < ____ < {b}  (give one decimal that fits)", "diagram", "____",
                  "", "decimal_numberline_blank", {"lo": 0.0, "hi": 1.0, "divisions": 10})
    def numeral(i, sheet):
        a, b = round(random.uniform(0,1),2), round(random.uniform(0,1),2)
        return q(f"{a} ___ {b}  (>, < or =)", "fill", "____")
    def multisel(i, sheet):
        opts = [round(random.uniform(0,0.5),2) for _ in range(2)] + [round(random.uniform(0.5,1),2) for _ in range(2)]
        return q(f"Which decimals are LESS than 0.5? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        vals = [round(random.uniform(0,1),2) for _ in range(3)]
        lefts = [str(v) for v in vals]
        rights = [("near 0" if v<0.3 else ("near 1/2" if v<0.7 else "near 1")) for v in vals]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each decimal to its benchmark: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Decimals can be placed exactly on a number line -- this shows their TRUE size.",
         "0.45 is just before 0.5 (the midpoint), NOT bigger than it."],
        "decimal_numberline_example", {"value": 0.45, "lo": 0.0, "hi": 1.0, "divisions": 10},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=80)


def _CUM3_s(sheet):
    nice_fracs = [(1,2,0.5),(1,4,0.25),(3,4,0.75),(1,5,0.2),(2,5,0.4)]
    def comp(i, sheet):
        if i % 2 == 0:
            num, den, dec = random.choice(nice_fracs)
            return q(f"{num}/{den} = ____ (decimal)", "diagram", "____", "", "fraction_bar_blank", {"den": den})
        return q("Place 0.5 on the number line.", "diagram", "____", "", "decimal_numberline_blank", {"lo":0.0,"hi":1.0,"divisions":10})
    def tf(i, sheet):
        num, den, dec = random.choice(nice_fracs)
        return q(f"True or False: {num}/{den} = {dec}", "fill", "____ (True/False)")
    def missing(i, sheet):
        return q("0.2 < ____ < 0.8  (give one decimal that fits)", "diagram", "____",
                  "", "decimal_numberline_blank", {"lo": 0.0, "hi": 1.0, "divisions": 10})
    def numeral(i, sheet):
        num, den, dec = random.choice(nice_fracs)
        return q(f"{num}/{den} = ____", "fill", "____")
    def multisel(i, sheet):
        return q("Which equal 1/2? Select ALL that apply: A) 0.5  B) 0.05  C) 2/4  D) 5/10",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        chosen = random.sample(nice_fracs, 3)
        lefts = [f"{n}/{d}" for n, d, dec in chosen]; rights = [str(dec) for n, d, dec in chosen]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of fraction-decimal conversion and number line placement."],
        "decimal_numberline_example", {"value": 0.45, "lo": 0.0, "hi": 1.0, "divisions": 10},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=300)


# ───────────────────────── I: Add/subtract decimals ─────────────────────────

def _I_s(sheet):
    lo, hi = diff_range(sheet, 1, 9)
    def gen(sheet):
        return (random.randint(0, 9), random.randint(1, 9))
    def comp(i, sheet):
        whole, d1 = gen(sheet); d2 = random.randint(1, 9)
        op = random.choice(["+", "-"])
        if op == "-" and d1 < d2: d1, d2 = d2, d1
        return q(f"{whole}.{d1} {op} 0.{d2} = ____", "diagram", "____", "", "decimal_place_blank", {"n_decimal": 1})
    def tf(i, sheet):
        whole, d1 = gen(sheet); d2 = random.randint(1, 9)
        op = random.choice(["+", "-"])
        if op == "-" and d1 < d2: d1, d2 = d2, d1
        correct = round(whole+d1/10 + d2/10, 1) if op == "+" else round(whole+d1/10 - d2/10, 1)
        shown = correct if random.random() > 0.4 else round(correct+0.1, 1)
        return q(f"True or False: {whole}.{d1} {op} 0.{d2} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        whole, d1 = gen(sheet)
        target = round(whole + d1/10 + random.randint(1,5)/10, 1)
        return q(f"{whole}.{d1} + ____ = {target}", "diagram", "____", "", "decimal_place_blank", {"n_decimal": 1})
    def numeral(i, sheet):
        whole, d1 = gen(sheet); d2 = random.randint(1, 9)
        op = random.choice(["+", "-"])
        if op == "-" and d1 < d2: d1, d2 = d2, d1
        return q(f"{whole}.{d1} {op} 0.{d2} = ____", "fill", "____")
    def multisel(i, sheet):
        whole, d1 = gen(sheet)
        target = round(whole + d1/10, 1)
        opts = [f"{whole}.{max(d1-2,0)} + 0.2", f"{whole}.{d1} + 0.0", f"{whole-1 if whole>0 else 0}.{d1} + 1.0", f"{whole}.{d1}1 - 0.01"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [gen(sheet) for _ in range(3)]
        lefts = [f"{w}.{d} + 0.1" for w, d in pairs]
        rights = [str(round(w+d/10+0.1, 1)) for w, d in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its sum: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Line up the decimal points, then add or subtract column by column, just like whole numbers.",
         "3.4 + 0.8 = 4.2 (the tenths add up to 12, carry 1 to the ones)."],
        "decimal_place_example", {"number": "4.2"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=90)


# ───────────────────────── J: Multiply decimals ─────────────────────────

def _J_s(sheet):
    def comp(i, sheet):
        if i % 2 == 0:
            d = round(random.uniform(0.1, 9.9), 1)
            power = random.choice([10, 100])
            return q(f"{d} x {power} = ____", "diagram", "____", "", "decimal_place_blank", {"n_decimal": 2})
        a = round(random.uniform(0.1, 0.9), 1); b = round(random.uniform(0.1, 0.9), 1)
        return q(f"{a} x {b} = ____", "diagram", "____", "", "hundredths_grid_blank", {})
    def tf(i, sheet):
        d = round(random.uniform(0.1, 9.9), 1); power = random.choice([10, 100])
        correct = round(d*power, 1)
        shown = correct if random.random() > 0.4 else round(correct/10, 1)
        return q(f"True or False: {d} x {power} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        d = round(random.uniform(0.1, 9.9), 1)
        return q(f"{d} x ____ = {round(d*10,1)}", "diagram", "____", "", "decimal_place_blank", {"n_decimal": 2})
    def numeral(i, sheet):
        d = round(random.uniform(0.1, 9.9), 1); power = random.choice([10, 100])
        return q(f"{d} x {power} = ____", "fill", "____")
    def multisel(i, sheet):
        d = round(random.uniform(0.1, 9.9), 1)
        target = round(d*10, 1)
        opts = [f"{d} x 10", f"{d} x 100", f"{round(d/10,2)} x 100", f"{d} x 1"]
        return q(f"Which equal {target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        ds = [round(random.uniform(0.1, 9.9), 1) for _ in range(3)]
        lefts = [f"{d} x 10" for d in ds]; rights = [str(round(d*10, 1)) for d in ds]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its product: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Multiplying by 10 shifts every digit one place LEFT (decimal point moves right).",
         "0.4 x 0.3 = 0.12 (shade 4 columns and 3 rows on the 100-grid; overlap = 12 squares = 0.12)."],
        "hundredths_grid_example", {"shaded": 12},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=110)


# ───────────────────────── K: Divide decimals (myth-busting) ─────────────────────────

def _K_s(sheet):
    def comp(i, sheet):
        if i % 2 == 0:
            whole = random.randint(2, 8); divisor = random.choice([0.5, 0.25, 0.2])
            return q(f"{whole} / {divisor} = ____  (bigger or smaller than {whole}?)", "diagram", "____",
                      "", "decimal_numberline_blank", {"lo": 0, "hi": whole*5, "divisions": 8})
        d = round(random.uniform(1.0, 9.0), 1); power = random.choice([10, 100])
        return q(f"{d} / {power} = ____", "diagram", "____", "", "decimal_place_blank", {"n_decimal": 3})
    def tf(i, sheet):
        whole = random.randint(2, 8); divisor = random.choice([0.5, 0.25])
        correct = round(whole/divisor, 1)
        claim_bigger = correct > whole
        shown_correct = random.random() > 0.4
        word = "BIGGER" if (claim_bigger == shown_correct) else "SMALLER"
        return q(f"True or False: {whole} / {divisor} is {word} than {whole}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        whole = random.randint(2, 8)
        return q(f"{whole} / ____ = {whole*2}  (what divisor doubles {whole}?)", "diagram", "____",
                  "", "decimal_numberline_blank", {"lo": 0, "hi": whole*3, "divisions": 6})
    def numeral(i, sheet):
        d = round(random.uniform(1.0, 9.0), 1); power = random.choice([10, 100])
        return q(f"{d} / {power} = ____", "fill", "____")
    def multisel(i, sheet):
        whole = random.randint(2, 8)
        opts = [f"{whole}/0.5", f"{whole}/2", f"{whole}/0.25", f"{whole}/1"]
        return q(f"Which give an answer BIGGER than {whole}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        whole = random.randint(2, 6)
        divisors = [0.5, 0.25, 1, 2]
        random.shuffle(divisors)
        divisors = divisors[:3]
        lefts = [f"{whole}/{d}" for d in divisors]
        rights = [str(round(whole/d, 2)) for d in divisors]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its quotient: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Dividing by a number SMALLER than 1 makes the answer BIGGER, not smaller!",
         "4 / 0.5 = 8 (there are 8 halves in 4 wholes) -- bigger than 4."],
        "decimal_numberline_example", {"value": 8, "lo": 0, "hi": 10, "divisions": 10},
        "Formats rotate each sheet. Watch for: dividing by less than 1 makes the answer bigger.",
        fmt, sheet, seed_base=120)


def _CUM4_s(sheet):
    def comp(i, sheet):
        choice = i % 3
        whole = random.randint(0, 9)
        if choice == 0:
            d1, d2 = random.randint(1, 9), random.randint(1, 9)
            return q(f"{whole}.{d1} + 0.{d2} = ____", "diagram", "____", "", "decimal_place_blank", {"n_decimal": 1})
        elif choice == 1:
            d = round(random.uniform(0.1, 9.9), 1)
            return q(f"{d} x 10 = ____", "diagram", "____", "", "decimal_place_blank", {"n_decimal": 2})
        else:
            w = random.randint(2, 8)
            return q(f"{w} / 0.5 = ____", "diagram", "____", "", "decimal_numberline_blank", {"lo": 0, "hi": w*3, "divisions": 6})
    def tf(i, sheet):
        whole = random.randint(0, 9); d1, d2 = random.randint(1, 9), random.randint(1, 9)
        correct = round(whole + d1/10 + d2/10, 1)
        shown = correct if random.random() > 0.4 else round(correct+0.1, 1)
        return q(f"True or False: {whole}.{d1} + 0.{d2} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        whole = random.randint(0, 9); d1 = random.randint(1, 9)
        return q(f"{whole}.{d1} + ____ = {round(whole+d1/10+0.3,1)}", "diagram", "____", "", "decimal_place_blank", {"n_decimal": 1})
    def numeral(i, sheet):
        whole = random.randint(0, 9); d1, d2 = random.randint(1, 9), random.randint(1, 9)
        op = random.choice(["+", "-", "x"])
        return q(f"{whole}.{d1} {op} 0.{d2} = ____", "fill", "____")
    def multisel(i, sheet):
        w = random.randint(2, 8)
        opts = [f"{w}/0.5", f"{w}/2", f"{w}/0.25", f"{w}/1"]
        return q(f"Which give an answer BIGGER than {w}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        ds = [round(random.uniform(0.1, 9.9), 1) for _ in range(3)]
        lefts = [f"{d} x 10" for d in ds]; rights = [str(round(d*10, 1)) for d in ds]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of adding, subtracting, multiplying, and dividing decimals."],
        "decimal_numberline_example", {"value": 8, "lo": 0, "hi": 10, "divisions": 10},
        "Watch out: dividing by a number less than 1 makes the answer bigger.",
        fmt, sheet, seed_base=400)


# ───────────────────────── L: Money word problems ─────────────────────────

def _L_s(sheet):
    templates = [
        "A pencil costs ${a}.{b}. How much do 2 pencils cost?",
        "You have $5.00 and spend ${a}.{b}. How much is left?",
        "A juice box costs ${a}.{b}. How much for 3 boxes?",
    ]
    def comp(i, sheet):
        a = random.randint(0, 4); b = random.randint(10, 99)
        return q(templates[i % len(templates)].format(a=a, b=b), "diagram", "____", "", "decimal_place_blank", {"n_decimal": 2})
    def tf(i, sheet):
        a, b = random.randint(0, 4), random.randint(10, 99)
        price = a + b/100
        correct = round(price*2, 2)
        shown = correct if random.random() > 0.4 else round(correct+1, 2)
        return q(f"True or False: 2 items at ${a}.{b} each cost ${shown}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        a, b = random.randint(1, 4), random.randint(10, 99)
        return q(f"You spent ${a}.{b} and have ____ left from $10.00.", "diagram", "____",
                  "", "decimal_place_blank", {"n_decimal": 2})
    def numeral(i, sheet):
        a, b = random.randint(0, 4), random.randint(10, 99)
        return q(templates[i % len(templates)].format(a=a, b=b), "fill", "____")
    def multisel(i, sheet):
        target = round(random.uniform(1, 5), 2)
        opts = [f"${target}", f"${round(target+1,2)}", f"${round(target,2)}", f"${round(target-1,2)}"]
        return q(f"Which show exactly ${target}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        prices = [round(random.uniform(1, 9), 2) for _ in range(3)]
        lefts = [f"${p} x 2" for p in prices]; rights = [f"${round(p*2,2)}" for p in prices]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its total: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Money is a natural decimal: dollars are ones, cents are hundredths.",
         "$3.47 means 3 dollars and 47 cents -- exactly like the place value chart."],
        "decimal_place_example", {"number": "3.47"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=130)


# ───────────────────────── M: Rounding decimals ─────────────────────────

def _M_s(sheet):
    places = ["nearest tenth", "nearest hundredth", "nearest whole number"]
    def comp(i, sheet):
        whole = random.randint(0, 9); dec = random.randint(0, 999)
        return q(f"Round {whole}.{str(dec).zfill(3)} to the {random.choice(places)}.", "diagram", "____",
                  "", "decimal_place_blank", {"n_decimal": 3})
    def tf(i, sheet):
        whole = random.randint(0, 9); dec = random.randint(50, 99)
        number = f"{whole}.{dec}"
        correct = whole + 1
        shown = correct if random.random() > 0.4 else whole
        return q(f"True or False: {number} rounds to {shown} (nearest whole number).", "fill", "____ (True/False)")
    def missing(i, sheet):
        whole = random.randint(0, 9)
        return q(f"____ rounds to {whole+1} (nearest whole number) but is less than {whole+1}.",
                  "diagram", "____", "", "decimal_place_blank", {"n_decimal": 1})
    def numeral(i, sheet):
        whole = random.randint(0, 9); dec = random.randint(0, 999)
        return q(f"Round {whole}.{str(dec).zfill(3)} to the {random.choice(places)}. ____", "fill", "____")
    def multisel(i, sheet):
        whole = random.randint(0, 8)
        opts = [f"{whole}.4", f"{whole}.5", f"{whole}.6", f"{whole}.49"]
        return q(f"Which round UP to {whole+1} (nearest whole)? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        whole = random.randint(0, 8)
        vals = [f"{whole}.2", f"{whole}.5", f"{whole}.8"]
        rights = [str(whole), str(whole+1), str(whole+1)]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(vals))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each to its rounded whole number: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Look at the digit just after the place you're rounding to.",
         "3.47 to the nearest tenth: look at the hundredths digit (7), round up -> 3.5."],
        "decimal_place_example", {"number": "3.47"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=140)


# ───────────────────────── N: Speed & puzzles ─────────────────────────

def _N_s(sheet):
    def comp(i, sheet):
        choice = i % 4
        if choice == 0: return q(f"{random.randint(1,9)}/10 = ____", "diagram", "____", "", "fraction_bar_blank", {"den":10})
        elif choice == 1: return q(f"{random.randint(5,95)}/100 = ____", "diagram", "____", "", "hundredths_grid_blank", {})
        elif choice == 2:
            whole=random.randint(0,9); d1,d2=random.randint(0,99),random.randint(0,99)
            return q(f"{whole}.{str(d1).zfill(2)} ___ {whole}.{str(d2).zfill(2)}", "diagram", "____", "", "decimal_place_blank", {"n_decimal":2})
        else: return q("Place a decimal on the number line.", "diagram", "____", "", "decimal_numberline_blank", {"lo":0.0,"hi":1.0,"divisions":10})
    def tf(i, sheet):
        whole = random.randint(0,9); d = random.randint(1,9)
        return q(f"True or False: {whole}.{d} = {whole}.{d}0", "fill", "____ (True/False)")
    def missing(i, sheet):
        whole = random.randint(0,9); d1 = random.randint(1,9)
        return q(f"{whole}.{d1} + ____ = {round(whole+d1/10+0.2,1)}", "diagram", "____", "", "decimal_place_blank", {"n_decimal":1})
    def numeral(i, sheet):
        whole = random.randint(0,9); d1,d2 = random.randint(1,9), random.randint(1,9)
        return q(f"{whole}.{d1} + 0.{d2} = ____", "fill", "____")
    def multisel(i, sheet):
        return q("Which equal 0.5? Select ALL that apply: A) 1/2  B) 0.50  C) 5/100  D) 50/100",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        nums = random.sample(range(1,9), 3)
        lefts = [f"{n}/10" for n in nums]; rights = [f"0.{n}" for n in nums]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example", ["Speed round: work quickly but carefully through each picture."],
        "decimal_place_example", {"number": "3.47"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=150)


# ───────────────────────── O/REV: Mixed ─────────────────────────

def _O_s(sheet):
    def comp(i, sheet):
        choice = i % 5
        whole = random.randint(0,9)
        if choice == 0: return q(f"{random.randint(5,95)}/100 = ____", "diagram", "____", "", "hundredths_grid_blank", {})
        elif choice == 1:
            d1,d2 = random.randint(1,9), random.randint(1,9)
            return q(f"{whole}.{d1} + 0.{d2} = ____", "diagram", "____", "", "decimal_place_blank", {"n_decimal":1})
        elif choice == 2: return q("Place a decimal on the number line.", "diagram", "____", "", "decimal_numberline_blank", {"lo":0.0,"hi":1.0,"divisions":10})
        elif choice == 3:
            den=random.choice([2,4,5,10]); num=random.randint(1,den-1)
            return q(f"{num}/{den} = ____ (decimal)", "diagram", "____", "", "fraction_bar_blank", {"den":den})
        else:
            w=random.randint(2,8)
            return q(f"{w} / 0.5 = ____", "diagram", "____", "", "decimal_numberline_blank", {"lo":0,"hi":w*3,"divisions":6})
    def tf(i, sheet):
        return q("True or False: dividing by 0.5 makes the answer bigger.", "fill", "____ (True/False)")
    def missing(i, sheet):
        whole = random.randint(0,9); d1 = random.randint(1,9)
        return q(f"{whole}.{d1} + ____ = {round(whole+d1/10+0.3,1)}", "diagram", "____", "", "decimal_place_blank", {"n_decimal":1})
    def numeral(i, sheet):
        whole = random.randint(0,9); d1,d2 = random.randint(1,9), random.randint(1,9)
        op = random.choice(["+","-","x"])
        return q(f"{whole}.{d1} {op} 0.{d2} = ____", "fill", "____")
    def multisel(i, sheet):
        return q("Which are TRUE? Select ALL that apply: A) 0.3=0.30  B) 4/0.5=8  C) 0.7=0.07  D) 1/2=0.5",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        nums = random.sample(range(1,9), 3)
        lefts = [f"{n}/10" for n in nums]; rights = [f"0.{n}" for n in nums]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example", ["Mixed challenge: every decimal skill from this level."],
        "hundredths_grid_example", {"shaded": 25},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=160)


def _REV_s(sheet):
    def comp(i, sheet):
        choice = i % 6
        whole = random.randint(0,9)
        if choice == 0: return q(f"{random.randint(1,9)}/10 = ____", "diagram", "____", "", "fraction_bar_blank", {"den":10})
        elif choice == 1: return q(f"{random.randint(5,95)}/100 = ____", "diagram", "____", "", "hundredths_grid_blank", {})
        elif choice == 2:
            d1,d2 = random.randint(0,99), random.randint(0,99)
            return q(f"{whole}.{str(d1).zfill(2)} ___ {whole}.{str(d2).zfill(2)}", "diagram", "____", "", "decimal_place_blank", {"n_decimal":2})
        elif choice == 3: return q("Place a decimal on the number line.", "diagram", "____", "", "decimal_numberline_blank", {"lo":0.0,"hi":1.0,"divisions":10})
        elif choice == 4:
            d1,d2 = random.randint(1,9), random.randint(1,9)
            return q(f"{whole}.{d1} + 0.{d2} = ____", "diagram", "____", "", "decimal_place_blank", {"n_decimal":1})
        else:
            w=random.randint(2,8)
            return q(f"{w} / 0.5 = ____", "diagram", "____", "", "decimal_numberline_blank", {"lo":0,"hi":w*3,"divisions":6})
    def tf(i, sheet):
        return q("True or False: '0.45 > 0.5 because 45 > 5' is correct.", "fill", "____ (True/False)")
    def missing(i, sheet):
        whole = random.randint(0,9); d1 = random.randint(1,9)
        return q(f"{whole}.{d1} + ____ = {round(whole+d1/10+0.3,1)}", "diagram", "____", "", "decimal_place_blank", {"n_decimal":1})
    def numeral(i, sheet):
        whole = random.randint(0,9); d1,d2 = random.randint(1,9), random.randint(1,9)
        op = random.choice(["+","-","x","/"])
        return q(f"{whole}.{d1} {op} 0.{d2} = ____", "fill", "____")
    def multisel(i, sheet):
        return q("Which are TRUE? Select ALL that apply: A) 0.3=0.30  B) 4/0.5=8  C) 0.7=0.07  D) 1/2=0.5",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        nums = random.sample(range(1,9), 3)
        lefts = [f"{n}/10" for n in nums]; rights = [f"0.{n}" for n in nums]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Level 7 Revision",
        ["Every decimal skill: place value, comparing, fractions, operations, money, and rounding."],
        "decimal_place_example", {"number": "3.47"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=500)


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
