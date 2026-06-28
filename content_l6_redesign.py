"""
Fear Less Maths — LEVEL 6 REDESIGN v2 (Fractions, Grade 5+)

Replaces the original Level 6 in place. v1 already fixed the major
content gaps (added GCF/LCM, fraction multiplication, fraction
division, none of which existed before). v2 fixes the "same worksheet
for every sheet" problem using the SAME shared architecture as Levels 7
and 8 (question_formats.py): each sub-level has up to 6 question-format
builders (computation, True/False, missing-number, numeral,
multi-select, matching) and 4 SHEET TEMPLATES, each picking a different
combination/order of formats. Worked examples stay inline on the
worksheet (every sheet).

Sub-level list (21 total, unchanged from v1):
  A Fraction concept       B Unit fractions & decomposition    C Proper/improper/mixed
  CUM1 review
  D Equivalent fractions   E Simplify via GCF                  F Compare via LCM/benchmarks
  CUM2 review
  G Add/sub LIKE            H Add/sub UNLIKE                    I Add/sub mixed numbers
  CUM3 review
  J Multiply fractions     K Multiply mixed numbers            L Divide fractions
  CUM4 review
  M Word problems          N Estimation & benchmarks           O Speed & puzzles
  P Mixed challenge        REV Revision
"""
import random
import math
from content import cb, tb, q
from question_formats import TEMPLATES, diff_range, make_rotated_sheet, make_format_builders


def _gcd(a, b):
    return math.gcd(a, b)


def _rand_fraction(max_den=8):
    den = random.randint(2, max_den)
    num = random.randint(1, den - 1)
    return num, den


# ───────────────────────── A: Fraction concept ─────────────────────────

def _A_s(sheet):
    def comp(i, sheet):
        num, den = _rand_fraction(6)
        return q(f"{num}/{den} = ____ (shade and write)", "diagram", "____", "", "fraction_bar_blank", {"den": den})
    def tf(i, sheet):
        num, den = _rand_fraction(6)
        shown_correct = random.random() > 0.4
        claim = f"{num} of {den} parts" if shown_correct else f"{den-num} of {den} parts"
        return q(f"True or False: {num}/{den} means {claim} shaded.", "fill", "____ (True/False)")
    def missing(i, sheet):
        den = random.randint(3, 8)
        return q(f"____ /{den} means half the parts are shaded (den is even).", "diagram", "____",
                  "", "fraction_bar_blank", {"den": den})
    def numeral(i, sheet):
        num, den = _rand_fraction(6)
        return q(f"{num}/{den} means ____ of ____ equal parts.", "fill", "____")
    def multisel(i, sheet):
        den = random.randint(4, 8)
        opts = [f"{den-1}/{den}", f"1/{den}", f"{den}/{den}", f"0/{den}"]
        return q(f"Which fractions show MOST of the whole shaded? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        dens = random.sample(range(2, 8), 3)
        lefts = [f"1/{d}" for d in dens]
        rights = [f"{d} equal parts, 1 shaded" for d in dens]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each fraction to its meaning: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["A fraction shows parts of ONE whole.",
         "3/4 means: split the whole into 4 equal parts, take 3 of them."],
        "fraction_bar_example", {"num": 3, "den": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=10)


# ───────────────────────── B: Unit fractions & decomposition ─────────────────────────

def _B_s(sheet):
    def comp(i, sheet):
        den = random.randint(3, 8); num = random.randint(2, den - 1)
        return q(f"{num}/{den} = 1/{den} + 1/{den} + ... = ____ (how many 1/{den}s?)",
                  "diagram", "____", "", "fraction_bar_blank", {"den": den})
    def tf(i, sheet):
        den = random.randint(3, 8); num = random.randint(2, den - 1)
        shown = num if random.random() > 0.4 else num + 1
        return q(f"True or False: {num}/{den} is made of {shown} unit fractions of 1/{den}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        den = random.randint(3, 8); num = random.randint(2, den - 1)
        return q(f"____ /{den} = 1/{den} repeated {num} times.", "diagram", "____", "", "fraction_bar_blank", {"den": den})
    def numeral(i, sheet):
        den = random.randint(3, 8); num = random.randint(2, den - 1)
        return q(f"{num}/{den} = how many 1/{den}'s? ____", "fill", "____")
    def multisel(i, sheet):
        den = random.randint(4, 8)
        opts = [f"3/{den}", f"1/{den}+1/{den}+1/{den}", f"{den}/{den}", f"2/{den}+1/{den}"]
        return q(f"Which equal 3/{den}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        dens = random.sample(range(3, 8), 3)
        nums = [random.randint(2, d-1) for d in dens]
        lefts = [f"{n}/{d}" for n, d in zip(nums, dens)]
        rights = [f"{n} unit fractions of 1/{d}" for n, d in zip(nums, dens)]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each fraction to its decomposition: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Every fraction is built from unit fractions (numerator 1).",
         "3/8 = 1/8 + 1/8 + 1/8 -- three 1/8 pieces."],
        "fraction_bar_example", {"num": 3, "den": 8, "label": "3/8 = 1/8+1/8+1/8"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=20)


# ───────────────────────── C: Proper/improper/mixed ─────────────────────────

def _C_s(sheet):
    def comp(i, sheet):
        whole = random.randint(1, 3); den = random.randint(2, 6); extra = random.randint(0, den - 1)
        total_num = whole*den + extra
        return q(f"{total_num}/{den} = ____ (mixed number)", "diagram", "____",
                  "", "fraction_bar_blank", {"den": den, "segments": whole + (1 if extra else 0)})
    def tf(i, sheet):
        whole = random.randint(1, 3); den = random.randint(2, 6); extra = random.randint(1, den-1)
        total_num = whole*den + extra
        shown = f"{whole} {extra}/{den}" if random.random() > 0.4 else f"{whole+1} {extra}/{den}"
        return q(f"True or False: {total_num}/{den} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        den = random.randint(2, 6); whole = random.randint(1, 3)
        return q(f"____ /{den} = {whole} wholes exactly (no remainder)", "diagram", "____",
                  "", "fraction_bar_blank", {"den": den, "segments": whole})
    def numeral(i, sheet):
        whole = random.randint(1, 3); den = random.randint(2, 6); extra = random.randint(0, den - 1)
        total_num = whole*den + extra
        return q(f"{total_num}/{den} = ____ (mixed number)", "fill", "____")
    def multisel(i, sheet):
        den = random.randint(3, 6)
        opts = [f"{den+1}/{den}", f"{den-1}/{den}", f"{den}/{den}", f"{2*den+1}/{den}"]
        return q(f"Which are IMPROPER fractions (numerator >= denominator)? Select ALL: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        den = random.randint(3, 6)
        wholes = random.sample(range(1, 4), 3)
        lefts = [f"{w*den}/{den}" for w in wholes]
        rights = [str(w) for w in wholes]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each improper fraction to its whole number: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["An IMPROPER fraction (numerator bigger than denominator) can be written as a MIXED number.",
         "7/3 = 2 whole bars + 1/3 left over = 2 1/3."],
        "fraction_bar_example", {"num": 1, "den": 3, "label": "7/3 = 2 wholes + 1/3"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=30)


def _CUM1_s(sheet):
    def comp(i, sheet):
        choice = i % 2
        if choice == 0:
            num, den = _rand_fraction(6)
            return q(f"{num}/{den} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den})
        whole = random.randint(1, 2); den = random.randint(2, 5); extra = random.randint(1, den-1)
        return q(f"{whole*den+extra}/{den} = ____ (mixed number)", "diagram", "____",
                  "", "fraction_bar_blank", {"den": den, "segments": whole+1})
    def tf(i, sheet):
        den = random.randint(3, 8); num = random.randint(2, den - 1)
        shown = num if random.random() > 0.4 else num + 1
        return q(f"True or False: {num}/{den} is {shown} unit fractions of 1/{den}.", "fill", "____ (True/False)")
    def missing(i, sheet):
        den = random.randint(3, 8); num = random.randint(2, den - 1)
        return q(f"____ /{den} = 1/{den} repeated {num} times.", "diagram", "____", "", "fraction_bar_blank", {"den": den})
    def numeral(i, sheet):
        num, den = _rand_fraction(6)
        return q(f"{num}/{den} = ____ (in words: ____ of ____ parts)", "fill", "____")
    def multisel(i, sheet):
        den = random.randint(4, 8)
        opts = [f"{den-1}/{den}", f"1/{den}", f"{den}/{den}", f"0/{den}"]
        return q(f"Which show MOST of the whole shaded? Select ALL: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        den = random.randint(3, 6)
        wholes = random.sample(range(1, 4), 3)
        lefts = [f"{w*den}/{den}" for w in wholes]; rights = [str(w) for w in wholes]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of fraction concept, decomposition, and mixed numbers."],
        "fraction_bar_example", {"num": 3, "den": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=100)


# ───────────────────────── D: Equivalent fractions ─────────────────────────

def _D_s(sheet):
    def comp(i, sheet):
        den1 = random.randint(2, 5); mult = random.randint(2, 4)
        num1 = random.randint(1, den1-1); den2 = den1*mult
        return q(f"{num1}/{den1} = ____/{den2}", "diagram", "____", "", "two_bars_blank", {"den1": den1, "den2": den2})
    def tf(i, sheet):
        den1 = random.randint(2, 5); mult = random.randint(2, 4)
        num1 = random.randint(1, den1-1); den2 = den1*mult
        correct = num1*mult
        shown = correct if random.random() > 0.4 else correct+1
        return q(f"True or False: {num1}/{den1} = {shown}/{den2}", "fill", "____ (True/False)")
    def missing(i, sheet):
        den1 = random.randint(2, 5); num1 = random.randint(1, den1-1)
        return q(f"{num1}/{den1} = {num1*2}/____", "diagram", "____", "", "two_bars_blank", {"den1": den1, "den2": den1*2})
    def numeral(i, sheet):
        den1 = random.randint(2, 5); mult = random.randint(2, 4)
        num1 = random.randint(1, den1-1); den2 = den1*mult
        return q(f"{num1}/{den1} = ____/{den2}", "fill", "____")
    def multisel(i, sheet):
        opts = ["1/2", "2/4", "3/6", "2/3"]
        return q(f"Which are equivalent to 1/2? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        den1 = random.randint(2, 4)
        nums = random.sample(range(1, den1), min(3, den1-1)) or [1]
        while len(nums) < 3: nums.append(random.randint(1, den1-1))
        lefts = [f"{n}/{den1}" for n in nums[:3]]
        rights = [f"{n*2}/{den1*2}" for n in nums[:3]]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each fraction to its equivalent: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Equivalent fractions look different but show the SAME amount.",
         "1/3 = 2/6: the bars are split differently, but the same portion is shaded."],
        "two_bars_example", {"num1": 1, "den1": 3, "num2": 2, "den2": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=40)


# ───────────────────────── E: Simplify via GCF ─────────────────────────

def _E_s(sheet):
    def comp(i, sheet):
        den = random.choice([4, 6, 8, 9, 10, 12]); num = random.randint(2, den-1)
        return q(f"{num}/{den} = ____ (simplify using the GCF)", "diagram", "____", "", "fraction_bar_blank", {"den": den})
    def tf(i, sheet):
        den = random.choice([6, 8, 9, 10, 12]); num = random.randint(2, den-1)
        g = _gcd(num, den)
        correct = f"{num//g}/{den//g}"
        shown = correct if random.random() > 0.4 else f"{num}/{den}"
        return q(f"True or False: {num}/{den} simplifies to {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        den = random.choice([6, 8, 9, 10, 12])
        return q(f"____ /{den} simplifies to 1/2 (find a numerator that works)", "diagram", "____",
                  "", "fraction_bar_blank", {"den": den})
    def numeral(i, sheet):
        den = random.choice([4, 6, 8, 9, 10, 12]); num = random.randint(2, den-1)
        return q(f"{num}/{den} = ____ (simplest form)", "fill", "____")
    def multisel(i, sheet):
        opts = ["4/8", "6/12", "3/6", "2/5"]
        return q(f"Which simplify to 1/2? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(4,8),(6,12),(3,9),(2,10)]
        chosen = random.sample(pairs, 3)
        lefts = [f"{n}/{d}" for n, d in chosen]
        rights = [f"{n//_gcd(n,d)}/{d//_gcd(n,d)}" for n, d in chosen]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each to its simplest form: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Find the GCF (Greatest Common Factor) of the numerator and denominator.",
         "8/12: GCF of 8 and 12 is 4. Divide both by 4: 8/12 = 2/3."],
        "fraction_bar_example", {"num": 2, "den": 3, "label": "8/12 = 2/3 (GCF=4)"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=50)


# ───────────────────────── F: Compare via LCM/benchmarks ─────────────────────────

def _F_s(sheet):
    def comp(i, sheet):
        den1, den2 = random.sample([2,3,4,5,6,8], 2)
        num1 = random.randint(1, den1-1); num2 = random.randint(1, den2-1)
        return q(f"{num1}/{den1} ___ {num2}/{den2}  (>, < or =)", "diagram", "____", "", "two_bars_blank", {"den1": den1, "den2": den2})
    def tf(i, sheet):
        den1, den2 = random.sample([2,3,4,5,6], 2)
        num1 = random.randint(1, den1-1); num2 = random.randint(1, den2-1)
        correct = ">" if num1/den1 > num2/den2 else ("<" if num1/den1 < num2/den2 else "=")
        shown = correct if random.random() > 0.4 else random.choice([s for s in [">","<","="] if s != correct])
        return q(f"True or False: {num1}/{den1} {shown} {num2}/{den2}", "fill", "____ (True/False)")
    def missing(i, sheet):
        den1 = random.randint(2, 6); num1 = random.randint(1, den1-1)
        return q(f"{num1}/{den1} > ____  (give a smaller fraction)", "diagram", "____", "", "two_bars_blank", {"den1": den1, "den2": den1+2})
    def numeral(i, sheet):
        den1, den2 = random.sample([2,3,4,5,6,8], 2)
        num1 = random.randint(1, den1-1); num2 = random.randint(1, den2-1)
        return q(f"{num1}/{den1} ___ {num2}/{den2}", "fill", "____")
    def multisel(i, sheet):
        opts = ["1/2", "3/4", "1/4", "2/3"]
        return q(f"Which are GREATER than 1/2? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        fracs = [(1,4),(1,2),(3,4)]
        lefts = [f"{n}/{d}" for n, d in fracs]
        rights = ["near 0", "near 1/2", "near 1"]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each fraction to its benchmark: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Use the LCM of the denominators to compare fairly.",
         "1/3 vs 2/4: LCM of 3,4 is 12. 1/3=4/12, 2/4=6/12, so 1/3 < 2/4.",
         "Or use benchmarks: is each fraction closer to 0, 1/2, or 1?"],
        "two_bars_example", {"num1": 1, "den1": 3, "num2": 2, "den2": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=60)


def _CUM2_s(sheet):
    def comp(i, sheet):
        choice = i % 3
        if choice == 0:
            den1 = random.randint(2,5); mult = random.randint(2,3)
            num1 = random.randint(1, den1-1)
            return q(f"{num1}/{den1} = ____/{den1*mult}", "diagram", "____", "", "two_bars_blank", {"den1": den1, "den2": den1*mult})
        elif choice == 1:
            den = random.choice([6,8,9,10]); num = random.randint(2, den-1)
            return q(f"{num}/{den} = ____ (simplest form)", "diagram", "____", "", "fraction_bar_blank", {"den": den})
        else:
            den1, den2 = random.sample([2,3,4,5,6], 2)
            num1 = random.randint(1, den1-1); num2 = random.randint(1, den2-1)
            return q(f"{num1}/{den1} ___ {num2}/{den2}", "diagram", "____", "", "two_bars_blank", {"den1": den1, "den2": den2})
    def tf(i, sheet):
        den1, den2 = random.sample([2,3,4,5,6], 2)
        num1 = random.randint(1, den1-1); num2 = random.randint(1, den2-1)
        correct = ">" if num1/den1 > num2/den2 else "<"
        return q(f"True or False: {num1}/{den1} {correct} {num2}/{den2}", "fill", "____ (True/False)")
    def missing(i, sheet):
        den = random.choice([6,8,9,10])
        return q(f"____ /{den} simplifies to 1/2", "diagram", "____", "", "fraction_bar_blank", {"den": den})
    def numeral(i, sheet):
        den = random.choice([6,8,9,10]); num = random.randint(2, den-1)
        return q(f"{num}/{den} = ____ (simplest form)", "fill", "____")
    def multisel(i, sheet):
        opts = ["4/8", "1/2", "3/4", "2/5"]
        return q(f"Which equal 1/2? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(4,8),(6,12),(3,9)]
        lefts = [f"{n}/{d}" for n, d in pairs]
        rights = [f"{n//_gcd(n,d)}/{d//_gcd(n,d)}" for n, d in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of equivalent fractions, simplifying, and comparing."],
        "two_bars_example", {"num1": 1, "den1": 3, "num2": 2, "den2": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=200)


# ───────────────────────── G: Add/subtract LIKE denominators ─────────────────────────

def _G_s(sheet):
    def comp(i, sheet):
        den = random.randint(3, 8); n1 = random.randint(1, den-1); n2 = random.randint(1, den-n1)
        op = "+" if i % 2 == 0 else "-"
        if op == "-" and n1 < n2: n1, n2 = n2, n1
        return q(f"{n1}/{den} {op} {n2}/{den} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den})
    def tf(i, sheet):
        den = random.randint(3, 8); n1 = random.randint(1, den-1); n2 = random.randint(1, max(den-n1,1))
        correct = n1+n2
        shown = correct if random.random() > 0.4 else correct+1
        return q(f"True or False: {n1}/{den} + {n2}/{den} = {shown}/{den}", "fill", "____ (True/False)")
    def missing(i, sheet):
        den = random.randint(3, 8); n1 = random.randint(1, den-1)
        target = random.randint(n1, den)
        return q(f"{n1}/{den} + ____/{den} = {target}/{den}", "diagram", "____", "", "fraction_bar_blank", {"den": den})
    def numeral(i, sheet):
        den = random.randint(3, 8); n1 = random.randint(1, den-1); n2 = random.randint(1, max(den-n1,1))
        op = "+" if i % 2 == 0 else "-"
        if op == "-" and n1 < n2: n1, n2 = n2, n1
        return q(f"{n1}/{den} {op} {n2}/{den} = ____", "fill", "____")
    def multisel(i, sheet):
        den = 8
        opts = ["2/8+3/8", "5/8-1/8", "1/8+4/8", "6/8-1/8"]
        return q(f"Which equal 5/8? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        den = random.randint(5, 8)
        pairs = [(random.randint(1,den-2), random.randint(1,2)) for _ in range(3)]
        lefts = [f"{n1}/{den}+{n2}/{den}" for n1, n2 in pairs]
        rights = [f"{n1+n2}/{den}" for n1, n2 in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its sum: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Same denominator: just add or subtract the numerators.",
         "2/8 + 3/8 = 5/8 (denominator stays the same)."],
        "fraction_bar_example", {"num": 5, "den": 8, "label": "2/8 + 3/8 = 5/8"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=70)


# ───────────────────────── H: Add/subtract UNLIKE denominators ─────────────────────────

def _H_s(sheet):
    def comp(i, sheet):
        den1, den2 = random.sample([2,3,4,5,6], 2)
        n1 = random.randint(1, den1-1); n2 = random.randint(1, den2-1)
        op = "+" if i % 2 == 0 else "-"
        return q(f"{n1}/{den1} {op} {n2}/{den2} = ____", "diagram", "____", "", "two_bars_blank", {"den1": den1, "den2": den2})
    def tf(i, sheet):
        den1, den2 = random.sample([2,3,4], 2)
        n1, n2 = 1, 1
        common = den1*den2
        correct_val = (common//den1)*n1 + (common//den2)*n2
        shown = correct_val if random.random() > 0.4 else correct_val+1
        return q(f"True or False: 1/{den1} + 1/{den2} = {shown}/{common}", "fill", "____ (True/False)")
    def missing(i, sheet):
        den1, den2 = random.sample([2,3,4,5], 2)
        n1 = random.randint(1, den1-1)
        return q(f"{n1}/{den1} + ____/{den2} = a fraction bigger than {n1}/{den1}", "diagram", "____",
                  "", "two_bars_blank", {"den1": den1, "den2": den2})
    def numeral(i, sheet):
        den1, den2 = random.sample([2,3,4,5,6], 2)
        n1 = random.randint(1, den1-1); n2 = random.randint(1, den2-1)
        op = "+" if i % 2 == 0 else "-"
        return q(f"{n1}/{den1} {op} {n2}/{den2} = ____", "fill", "____")
    def multisel(i, sheet):
        opts = ["1/3+1/4", "1/2+1/4", "1/3+1/6", "1/2+1/3"]
        return q(f"Which equal 1/2? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(1,3,1,4),(1,2,1,4),(1,3,1,6)]
        lefts = [f"{a}/{b}+{c}/{d}" for a,b,c,d in pairs]
        rights = ["7/12", "3/4", "1/2"]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its sum: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Different denominators: find the LCM first, convert both fractions, then add/subtract.",
         "1/3 + 1/4: LCM=12. 1/3=4/12, 1/4=3/12. 4/12+3/12=7/12."],
        "two_bars_example", {"num1": 1, "den1": 3, "num2": 1, "den2": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=80)


# ───────────────────────── I: Add/subtract mixed numbers ─────────────────────────

def _I_s(sheet):
    def comp(i, sheet):
        w1, w2 = random.randint(1,3), random.randint(1,2)
        den = random.randint(2,6); n1, n2 = random.randint(1,den-1), random.randint(1,den-1)
        op = "+" if i % 2 == 0 else "-"
        if op == "-": w1 = max(w1,w2)+1
        return q(f"{w1} {n1}/{den} {op} {w2} {n2}/{den} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den, "segments": w1+1})
    def tf(i, sheet):
        w1, w2 = random.randint(1,2), random.randint(1,2)
        den = random.randint(2,4); n1, n2 = 1, 1
        correct = w1+w2
        shown = correct if random.random() > 0.4 else correct+1
        return q(f"True or False: {w1} 1/{den} + {w2} 1/{den} = {shown} 2/{den}", "fill", "____ (True/False)")
    def missing(i, sheet):
        w1 = random.randint(1,3); den = random.randint(2,5); n1 = random.randint(1,den-1)
        return q(f"{w1} {n1}/{den} + ____ = {w1+1} {n1}/{den}", "diagram", "____", "", "fraction_bar_blank", {"den": den, "segments": w1+2})
    def numeral(i, sheet):
        w1, w2 = random.randint(1,3), random.randint(1,2)
        den = random.randint(2,6); n1, n2 = random.randint(1,den-1), random.randint(1,den-1)
        op = "+" if i % 2 == 0 else "-"
        if op == "-": w1 = max(w1,w2)+1
        return q(f"{w1} {n1}/{den} {op} {w2} {n2}/{den} = ____", "fill", "____")
    def multisel(i, sheet):
        opts = ["1 1/4+1 1/4", "2 1/4+0 1/4", "1 1/2+1 0/4", "3 0/4-0 1/4"]
        return q(f"Which equal 2 1/2 (or close forms)? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        den = random.randint(2,4)
        pairs = [(random.randint(1,2), random.randint(1,2)) for _ in range(3)]
        lefts = [f"{w1} 1/{den}+{w2} 1/{den}" for w1, w2 in pairs]
        rights = [f"{w1+w2} 2/{den}" for w1, w2 in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its sum: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Add/subtract the whole numbers and the fractions separately, then combine.",
         "2 1/4 + 1 2/4 = (2+1) + (1/4+2/4) = 3 + 3/4 = 3 3/4."],
        "fraction_bar_example", {"num": 3, "den": 4, "label": "2 1/4 + 1 2/4 = 3 3/4"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=90)


def _CUM3_s(sheet):
    def comp(i, sheet):
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
    def tf(i, sheet):
        den = random.randint(3,8); n1=random.randint(1,den-1); n2=random.randint(1,max(den-n1,1))
        return q(f"True or False: {n1}/{den} + {n2}/{den} = {n1+n2}/{den}", "fill", "____ (True/False)")
    def missing(i, sheet):
        den = random.randint(3,8); n1 = random.randint(1, den-1)
        return q(f"{n1}/{den} + ____/{den} = {den}/{den}", "diagram", "____", "", "fraction_bar_blank", {"den": den})
    def numeral(i, sheet):
        den1,den2 = random.sample([2,3,4,5,6],2); n1=random.randint(1,den1-1); n2=random.randint(1,den2-1)
        return q(f"{n1}/{den1} + {n2}/{den2} = ____", "fill", "____")
    def multisel(i, sheet):
        opts = ["1/3+1/4", "1/2+1/4", "1/3+1/6", "1/2+1/3"]
        return q(f"Which equal 1/2? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(1,3,1,4),(1,2,1,4),(1,3,1,6)]
        lefts = [f"{a}/{b}+{c}/{d}" for a,b,c,d in pairs]
        rights = ["7/12", "3/4", "1/2"]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of like, unlike, and mixed-number addition/subtraction."],
        "two_bars_example", {"num1":1,"den1":3,"num2":1,"den2":4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=300)


# ───────────────────────── J: Multiply fractions ─────────────────────────

def _J_s(sheet):
    def comp(i, sheet):
        n1, d1 = _rand_fraction(5); n2, d2 = _rand_fraction(5)
        return q(f"{n1}/{d1} x {n2}/{d2} = ____", "diagram", "____", "", "fraction_area_blank", {"den1": d1, "den2": d2})
    def tf(i, sheet):
        n1, d1 = _rand_fraction(5); n2, d2 = _rand_fraction(5)
        correct_num, correct_den = n1*n2, d1*d2
        shown = f"{correct_num}/{correct_den}" if random.random() > 0.4 else f"{correct_num+1}/{correct_den}"
        return q(f"True or False: {n1}/{d1} x {n2}/{d2} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        n1, d1 = _rand_fraction(5)
        return q(f"{n1}/{d1} x ____ = a fraction smaller than {n1}/{d1}", "diagram", "____",
                  "", "fraction_area_blank", {"den1": d1, "den2": 4})
    def numeral(i, sheet):
        n1, d1 = _rand_fraction(5); n2, d2 = _rand_fraction(5)
        return q(f"{n1}/{d1} x {n2}/{d2} = ____", "fill", "____")
    def multisel(i, sheet):
        opts = ["1/2x1/2", "1/3x3/4", "1/2x1/4", "2/3x3/4"]
        return q(f"Which equal 1/4? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(1,2,1,2),(1,3,1,2),(2,3,1,2)]
        lefts = [f"{a}/{b}x{c}/{d}" for a,b,c,d in pairs]
        rights = ["1/4", "1/6", "1/3"]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its product: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Shade columns for the first fraction, rows for the second.",
         "The double-shaded squares out of the total squares are the answer.",
         "2/3 x 3/4: 6 of 12 squares double-shaded = 6/12 = 1/2."],
        "fraction_area_example", {"num1": 2, "den1": 3, "num2": 3, "den2": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=110)


# ───────────────────────── K: Multiply mixed numbers ─────────────────────────

def _K_s(sheet):
    def comp(i, sheet):
        whole = random.randint(2,5); n, d = _rand_fraction(6)
        return q(f"{whole} x {n}/{d} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": d, "segments": whole})
    def tf(i, sheet):
        whole = random.randint(2,4); n, d = _rand_fraction(5)
        correct_num = whole*n
        shown = f"{correct_num}/{d}" if random.random() > 0.4 else f"{correct_num+1}/{d}"
        return q(f"True or False: {whole} x {n}/{d} = {shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        n, d = _rand_fraction(5)
        return q(f"____ x {n}/{d} = {2*n}/{d}  (what whole number?)", "diagram", "____", "", "fraction_bar_blank", {"den": d, "segments": 2})
    def numeral(i, sheet):
        whole = random.randint(2,5); n, d = _rand_fraction(6)
        return q(f"{whole} x {n}/{d} = ____", "fill", "____")
    def multisel(i, sheet):
        opts = ["3x1/4", "2x2/4", "4x1/4", "1x4/4"]
        return q(f"Which equal 1 (a whole)? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(2,1,4),(3,1,3),(4,1,2)]
        lefts = [f"{w}x{n}/{d}" for w, n, d in pairs]
        rights = [f"{w*n}/{d}" for w, n, d in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its product: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Multiplying a whole number by a fraction means repeating that fraction.",
         "3 x 2/5 = 2/5 + 2/5 + 2/5 = 6/5 = 1 1/5."],
        "fraction_bar_example", {"num": 1, "den": 5, "label": "3 x 2/5 = 6/5 = 1 1/5"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=120)


# ───────────────────────── L: Divide fractions ─────────────────────────

def _L_s(sheet):
    def comp(i, sheet):
        if i % 2 == 0:
            den = random.randint(2,6); whole = random.randint(2,4)
            return q(f"1/{den} / {whole} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den*whole})
        den = random.randint(2,5)
        return q(f"{random.randint(2,5)} / 1/{den} = ____", "diagram", "____", "", "fraction_numberline_blank", {"den": den})
    def tf(i, sheet):
        den = random.randint(2,5); whole = random.randint(2,4)
        correct = den*whole
        shown = correct if random.random() > 0.4 else correct+1
        return q(f"True or False: 1/{den} / {whole} = 1/{shown}", "fill", "____ (True/False)")
    def missing(i, sheet):
        den = random.randint(2,5)
        return q(f"2 / ____ = {2*den}  (what unit fraction divisor?)", "diagram", "____", "", "fraction_numberline_blank", {"den": den})
    def numeral(i, sheet):
        if i % 2 == 0:
            den = random.randint(2,6); whole = random.randint(2,4)
            return q(f"1/{den} / {whole} = ____", "fill", "____")
        den = random.randint(2,5)
        return q(f"{random.randint(2,5)} / 1/{den} = ____", "fill", "____")
    def multisel(i, sheet):
        opts = ["1/2 / 2", "1/4", "2 / 1/4", "8"]
        return q(f"Which describe the SAME value? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(1,2,2),(1,3,3),(1,4,2)]
        lefts = [f"1/{d}/{w}" for d, w, r in pairs]
        rights = [f"1/{d*w}" for d, w, r in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its quotient: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Dividing a unit fraction by a whole number splits it into even smaller pieces.",
         "1/3 / 2 = 1/6 (split each third in half).",
         "Dividing a whole number by a unit fraction counts how many pieces fit.",
         "2 / 1/4 = 8 (there are 8 quarters in 2 wholes)."],
        "fraction_bar_example", {"num": 1, "den": 6, "label": "1/3 / 2 = 1/6"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=130)


def _CUM4_s(sheet):
    def comp(i, sheet):
        choice = i % 3
        if choice == 0:
            n1,d1=_rand_fraction(5); n2,d2=_rand_fraction(5)
            return q(f"{n1}/{d1} x {n2}/{d2} = ____", "diagram", "____", "", "fraction_area_blank", {"den1": d1, "den2": d2})
        elif choice == 1:
            whole=random.randint(2,4); n,d=_rand_fraction(5)
            return q(f"{whole} x {n}/{d} = ____", "diagram", "____", "", "fraction_bar_blank", {"den":d,"segments":whole})
        else:
            den=random.randint(2,5); whole=random.randint(2,4)
            return q(f"1/{den} / {whole} = ____", "diagram", "____", "", "fraction_bar_blank", {"den":den*whole})
    def tf(i, sheet):
        n1,d1=_rand_fraction(5); n2,d2=_rand_fraction(5)
        correct = f"{n1*n2}/{d1*d2}"
        return q(f"True or False: {n1}/{d1} x {n2}/{d2} = {correct}", "fill", "____ (True/False)")
    def missing(i, sheet):
        n, d = _rand_fraction(5)
        return q(f"____ x {n}/{d} = {2*n}/{d}", "diagram", "____", "", "fraction_bar_blank", {"den": d, "segments": 2})
    def numeral(i, sheet):
        n1,d1=_rand_fraction(5); n2,d2=_rand_fraction(5)
        return q(f"{n1}/{d1} x {n2}/{d2} = ____", "fill", "____")
    def multisel(i, sheet):
        opts = ["1/2x1/2", "1/3x3/4", "1/2x1/4", "2/3x3/4"]
        return q(f"Which equal 1/4? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(1,2,1,2),(1,3,1,2),(2,3,1,2)]
        lefts = [f"{a}/{b}x{c}/{d}" for a,b,c,d in pairs]
        rights = ["1/4", "1/6", "1/3"]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review", ["Mix of multiplying and dividing fractions."],
        "fraction_area_example", {"num1":2,"den1":3,"num2":3,"den2":4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=400)


# ───────────────────────── M: Word problems ─────────────────────────

def _M_s(sheet):
    templates_add = [
        "A recipe needs {n1}/{d1} cup sugar and {n2}/{d1} cup flour. Total = ____.",
        "A jug has {n1}/{d1} L of juice, then {n2}/{d1} L more is added. Total = ____.",
    ]
    templates_sub = [
        "A ribbon is {n1}/{d1} m long. {n2}/{d1} m is cut off. Left = ____.",
        "{n1}/{d1} of a cake is left, then {n2}/{d1} is eaten. Left = ____.",
    ]
    def comp(i, sheet):
        d1 = random.randint(3,8); n1 = random.randint(1, d1-1); n2 = random.randint(1, d1-n1) if d1-n1>0 else 1
        if i % 2 == 0:
            txt = random.choice(templates_add).format(n1=n1, n2=n2, d1=d1)
        else:
            txt = random.choice(templates_sub).format(n1=n1, n2=n2, d1=d1)
        return q(txt, "diagram", "____", "", "fraction_bar_blank", {"den": d1})
    def tf(i, sheet):
        d1 = random.randint(3,8); n1 = random.randint(1, d1-2); n2 = random.randint(1, d1-n1)
        correct = n1+n2
        shown = correct if random.random() > 0.4 else correct+1
        return q(f"True or False: {n1}/{d1} + {n2}/{d1} of the same recipe = {shown}/{d1}", "fill", "____ (True/False)")
    def missing(i, sheet):
        d1 = random.randint(3,8); n1 = random.randint(1,d1-1)
        return q(f"A ribbon is {d1}/{d1} m (whole). {n1}/{d1} m is cut off. ____/{d1} m is left.",
                  "diagram", "____", "", "fraction_bar_blank", {"den": d1})
    def numeral(i, sheet):
        d1 = random.randint(3,8); n1 = random.randint(1, d1-1); n2 = random.randint(1, d1-n1) if d1-n1>0 else 1
        txt = random.choice(templates_add + templates_sub).format(n1=n1, n2=n2, d1=d1)
        return q(txt, "fill", "____")
    def multisel(i, sheet):
        opts = ["1/2 cake eaten, 1/2 left", "1/4 cut, 3/4 left", "1/3 used, 2/3 left", "1/2 used, 1/4 left"]
        return q(f"Which statements are mathematically consistent? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        d1 = random.randint(4, 8)
        cuts = random.sample(range(1, d1), 3)
        lefts = [f"{d1}/{d1} - {c}/{d1}" for c in cuts]
        rights = [f"{d1-c}/{d1}" for c in cuts]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each situation to what's left: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Read carefully: are parts being joined, removed, shared, or repeated?",
         "'Half the cake is left, then 1/4 is eaten' means subtract: 1/2 - 1/4 = 1/4."],
        "fraction_bar_example", {"num": 1, "den": 4, "label": "1/2 - 1/4 = 1/4"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=140)


# ───────────────────────── N: Estimation / benchmarks ─────────────────────────

def _N_s(sheet):
    def comp(i, sheet):
        n, d = _rand_fraction(8)
        return q(f"Place {n}/{d} on the number line.", "diagram", "____", "", "fraction_numberline_blank", {"den": d})
    def tf(i, sheet):
        n, d = _rand_fraction(8)
        claim_half = n/d < 0.5
        shown_correct = random.random() > 0.4
        word = "less than" if (claim_half == shown_correct) else "greater than"
        return q(f"True or False: {n}/{d} is {word} 1/2.", "fill", "____ (True/False)")
    def missing(i, sheet):
        return q("0/8 < ____ < 1  (give a fraction between 0 and 1)", "diagram", "____", "", "fraction_numberline_blank", {"den": 8})
    def numeral(i, sheet):
        n, d = _rand_fraction(8)
        return q(f"Is {n}/{d} closer to 0, 1/2, or 1? ____", "fill", "____")
    def multisel(i, sheet):
        opts = ["1/8", "7/8", "4/9", "1/10"]
        return q(f"Which fractions are CLOSE to 0? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        fracs = ["1/10", "5/9", "9/10"]
        rights = ["near 0", "near 1/2", "near 1"]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(fracs))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match each fraction to its benchmark: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example",
        ["Compare each fraction to the benchmarks 0, 1/2, and 1.",
         "3/8 is just under 1/2, so place it slightly left of the middle."],
        "fraction_numberline_example", {"num": 1, "den": 2},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=150)


# ───────────────────────── O/P/REV ─────────────────────────

def _O_s(sheet):
    def comp(i, sheet):
        choice = i % 4
        if choice == 0:
            n,d = _rand_fraction(6); return q(f"{n}/{d} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": d})
        elif choice == 1:
            n1,d1=_rand_fraction(5); n2,d2=_rand_fraction(5)
            return q(f"{n1}/{d1} x {n2}/{d2} = ____", "diagram", "____", "", "fraction_area_blank", {"den1": d1, "den2": d2})
        elif choice == 2:
            den1,den2 = random.sample([2,3,4,5,6],2); n1=random.randint(1,den1-1); n2=random.randint(1,den2-1)
            return q(f"{n1}/{den1} + {n2}/{den2} = ____", "diagram", "____", "", "two_bars_blank", {"den1":den1,"den2":den2})
        else:
            n,d = _rand_fraction(8); return q(f"Place {n}/{d} on the number line.", "diagram", "____", "", "fraction_numberline_blank", {"den": d})
    def tf(i, sheet):
        n, d = _rand_fraction(6)
        return q(f"True or False: {n}/{d} is in simplest form.", "fill", "____ (True/False)")
    def missing(i, sheet):
        den = random.choice([6,8,9,10])
        return q(f"____ /{den} simplifies to 1/2", "diagram", "____", "", "fraction_bar_blank", {"den": den})
    def numeral(i, sheet):
        n1,d1=_rand_fraction(5); n2,d2=_rand_fraction(5)
        return q(f"{n1}/{d1} x {n2}/{d2} = ____", "fill", "____")
    def multisel(i, sheet):
        opts = ["1/2", "2/4", "3/6", "2/3"]
        return q(f"Which are equivalent to 1/2? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(4,8),(6,12),(3,9)]
        lefts = [f"{n}/{d}" for n, d in pairs]
        rights = [f"{n//_gcd(n,d)}/{d//_gcd(n,d)}" for n, d in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example", ["Speed round: work quickly but carefully through each picture."],
        "fraction_bar_example", {"num": 3, "den": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=160)


def _P_s(sheet):
    def comp(i, sheet):
        choice = i % 5
        if choice == 0:
            n,d = _rand_fraction(6); return q(f"{n}/{d} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": d})
        elif choice == 1:
            n1,d1=_rand_fraction(5); n2,d2=_rand_fraction(5)
            return q(f"{n1}/{d1} x {n2}/{d2} = ____", "diagram", "____", "", "fraction_area_blank", {"den1": d1, "den2": d2})
        elif choice == 2:
            den1,den2 = random.sample([2,3,4,5,6],2); n1=random.randint(1,den1-1); n2=random.randint(1,den2-1)
            sym = "-" if n1*den2>n2*den1 else "+"
            return q(f"{n1}/{den1} {sym} {n2}/{den2} = ____", "diagram", "____", "", "two_bars_blank", {"den1":den1,"den2":den2})
        elif choice == 3:
            den=random.randint(2,5); whole=random.randint(2,4)
            return q(f"1/{den} / {whole} = ____", "diagram", "____", "", "fraction_bar_blank", {"den":den*whole})
        else:
            n,d = _rand_fraction(8); return q(f"Place {n}/{d} on the number line.", "diagram", "____", "", "fraction_numberline_blank", {"den": d})
    def tf(i, sheet):
        n1,d1=_rand_fraction(5); n2,d2=_rand_fraction(5)
        return q(f"True or False: {n1}/{d1} x {n2}/{d2} = {n1*n2}/{d1*d2}", "fill", "____ (True/False)")
    def missing(i, sheet):
        n, d = _rand_fraction(5)
        return q(f"____ x {n}/{d} = {2*n}/{d}", "diagram", "____", "", "fraction_bar_blank", {"den": d, "segments": 2})
    def numeral(i, sheet):
        den1,den2 = random.sample([2,3,4,5,6],2); n1=random.randint(1,den1-1); n2=random.randint(1,den2-1)
        return q(f"{n1}/{den1} + {n2}/{den2} = ____", "fill", "____")
    def multisel(i, sheet):
        opts = ["1/2x1/2", "1/3x3/4", "1/2x1/4", "2/3x3/4"]
        return q(f"Which equal 1/4? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(1,2,1,2),(1,3,1,2),(2,3,1,2)]
        lefts = [f"{a}/{b}x{c}/{d}" for a,b,c,d in pairs]
        rights = ["1/4", "1/6", "1/3"]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Worked Example", ["Mixed challenge: every fraction skill from this level."],
        "fraction_area_example", {"num1":2,"den1":3,"num2":3,"den2":4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=170)


def _REV_s(sheet):
    def comp(i, sheet):
        choice = i % 6
        if choice == 0:
            n,d = _rand_fraction(6); return q(f"{n}/{d} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": d})
        elif choice == 1:
            n1,d1=_rand_fraction(5); n2,d2=_rand_fraction(5)
            return q(f"{n1}/{d1} x {n2}/{d2} = ____", "diagram", "____", "", "fraction_area_blank", {"den1": d1, "den2": d2})
        elif choice == 2:
            den1,den2 = random.sample([2,3,4,5,6],2); n1=random.randint(1,den1-1); n2=random.randint(1,den2-1)
            return q(f"{n1}/{den1} + {n2}/{den2} = ____", "diagram", "____", "", "two_bars_blank", {"den1":den1,"den2":den2})
        elif choice == 3:
            den=random.randint(2,5); whole=random.randint(2,4)
            return q(f"1/{den} / {whole} = ____", "diagram", "____", "", "fraction_bar_blank", {"den":den*whole})
        elif choice == 4:
            n,d = _rand_fraction(8); return q(f"Place {n}/{d} on the number line.", "diagram", "____", "", "fraction_numberline_blank", {"den": d})
        else:
            den=random.choice([6,8,9,10]); num=random.randint(2,den-1)
            return q(f"{num}/{den} = ____ (simplest form)", "diagram", "____", "", "fraction_bar_blank", {"den":den})
    def tf(i, sheet):
        n, d = _rand_fraction(8)
        return q(f"True or False: {n}/{d} is already in simplest form (check the GCF).", "fill", "____ (True/False)")
    def missing(i, sheet):
        den = random.choice([6,8,9,10])
        return q(f"____ /{den} simplifies to 1/2", "diagram", "____", "", "fraction_bar_blank", {"den": den})
    def numeral(i, sheet):
        den1,den2 = random.sample([2,3,4,5,6],2); n1=random.randint(1,den1-1); n2=random.randint(1,den2-1)
        op = random.choice(["+","-","x"])
        return q(f"{n1}/{den1} {op} {n2}/{den2} = ____", "fill", "____")
    def multisel(i, sheet):
        opts = ["1/2", "2/4", "3/6", "2/3"]
        return q(f"Which are equivalent to 1/2? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")
    def matching(i, sheet):
        pairs = [(4,8),(6,12),(3,9)]
        lefts = [f"{n}/{d}" for n, d in pairs]
        rights = [f"{n//_gcd(n,d)}/{d//_gcd(n,d)}" for n, d in pairs]
        shuffled = rights[:]; random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")
    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Level 6 Revision",
        ["Every fraction skill: concept, equivalence, operations, and word problems."],
        "two_bars_example", {"num1":1,"den1":3,"num2":2,"den2":4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=500)


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
