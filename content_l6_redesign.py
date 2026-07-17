"""
Fear Less Maths — LEVEL 6 REDESIGN v3 (Fractions, Grade 5+)

Compresses v2's 21 sublevels down to the standard 10+3+1 pattern (14
total) used across the rest of this session's work, matching the
established "no more than ~5 questions per single idea" rule. Closes
two genuine depth gaps found on research: general fraction/fraction
division via the reciprocal method (previously only unit-fraction
cases existed), and true mixed-number x mixed-number multiplication
(the old 6K was mislabeled -- it only ever taught whole x fraction).
Also adds cross-multiplication as a second comparison technique.

Sub-level list (14 total):
  A Fraction concept + unit fractions      B Proper/improper/mixed
  C Equivalent fractions
  CUM1 review
  D Simplify via GCF                        E Compare (LCM, benchmark, cross-mult)
  F Add & subtract fractions (like+unlike)
  CUM2 review
  G Add & subtract mixed numbers            H Multiply fractions & mixed numbers
  I Divide fractions (incl. general case via reciprocal)
  CUM3 review
  J Word problems & estimation
  REV Revision
"""
import random
import math
from content import cb, tb, q
from question_formats import TEMPLATES, diff_range, make_rotated_sheet, make_format_builders, matching_q


def _gcd(a, b):
    return math.gcd(a, b)


def _rand_fraction(max_den=8):
    den = random.randint(2, max_den)
    num = random.randint(1, den - 1)
    return num, den


def _rand_proper_frac(max_den=8, min_den=2):
    den = random.randint(min_den, max_den)
    num = random.randint(1, den - 1)
    return num, den


# ═══════════════════════ A: Fraction Concept + Unit Fractions ═══════════════════════
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
        rights = [f"{d} equal parts, 1 shaded (a UNIT fraction)" for d in dens]
        return matching_q(lefts, rights)

    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Fractions & Unit Fractions",
        ["A fraction shows parts of ONE whole. 3/4 means: split into 4 equal parts, take 3.",
         "A UNIT fraction has numerator 1 (like 1/5) -- one single piece.",
         "Any fraction is just N copies of its unit fraction: 3/5 = three 1/5's."],
        "fraction_bar_example", {"num": 3, "den": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=10)


# ═══════════════════════ B: Proper, Improper & Mixed Numbers ═══════════════════════
def _B_s(sheet):
    def comp(i, sheet):
        den = random.randint(2, 6)
        num = random.randint(den + 1, den * 3)
        return q(f"{num}/{den}: is this proper or improper? Convert to a mixed number.", "fill", "____")

    def tf(i, sheet):
        den = random.randint(2, 6)
        num = random.randint(1, den * 3)
        is_proper = num < den
        shown = "proper" if random.random() > 0.4 else "improper"
        return q(f"True or False: {num}/{den} is a {shown} fraction.", "fill", "____ (True/False)")

    def missing(i, sheet):
        den = random.randint(2, 6)
        whole = random.randint(1, 4)
        rem = random.randint(1, den - 1)
        num = whole * den + rem
        return q(f"{num}/{den} = {whole} ____/{den}. Find the missing numerator.", "fill", "____")

    def numeral(i, sheet):
        den = random.randint(2, 6)
        whole = random.randint(1, 4)
        rem = random.randint(1, den - 1)
        return q(f"Convert {whole} {rem}/{den} to an improper fraction.", "fill", "____")

    def multisel(i, sheet):
        den = random.randint(3, 6)
        opts = [random.randint(1, den * 2) for _ in range(4)]
        opts_str = "  ".join(f"{chr(65+k)}) {opts[k]}/{den}" for k in range(4))
        return q(f"Which of these are IMPROPER fractions (numerator >= denominator)? Select ALL: {opts_str}", "fill", "____ (list all letters)")

    def matching(i, sheet):
        pairs = []
        for _ in range(3):
            den = random.randint(2, 6)
            whole = random.randint(1, 3)
            rem = random.randint(1, den - 1)
            pairs.append((whole * den + rem, den, whole, rem))
        lefts = [f"{n}/{d}" for n, d, w, r in pairs]
        rights = [f"{w} {r}/{d}" for n, d, w, r in pairs]
        return matching_q(lefts, rights)

    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Proper, Improper & Mixed Numbers",
        ["Proper: numerator < denominator (less than a whole), like 3/4.",
         "Improper: numerator >= denominator (a whole or more), like 7/4.",
         "Mixed number: a whole number + a proper fraction, like 1 3/4.",
         "Convert improper -> mixed: divide: quotient=whole, remainder=new numerator."],
        "fraction_bar_example", {"num": 7, "den": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=20)


# ═══════════════════════ C: Equivalent Fractions ═══════════════════════
def _C_s(sheet):
    def comp(i, sheet):
        num, den = _rand_proper_frac(6)
        k = random.randint(2, 4)
        return q(f"{num}/{den} = ____/{den*k}  (scale up by {k})", "diagram", "____", "", "two_bars_blank", {"den1": den, "den2": den * k})

    def tf(i, sheet):
        num, den = _rand_proper_frac(6)
        k = random.randint(2, 4)
        shown_correct = random.random() > 0.4
        shown_num = num * k if shown_correct else num * k + 1
        return q(f"True or False: {num}/{den} = {shown_num}/{den*k}.", "fill", "____ (True/False)")

    def missing(i, sheet):
        num, den = _rand_proper_frac(5)
        k = random.randint(2, 5)
        return q(f"{num}/{den} = {num*k}/____  Find the missing denominator.", "fill", "____")

    def numeral(i, sheet):
        num, den = _rand_proper_frac(6)
        k = random.randint(2, 4)
        return q(f"Find an equivalent fraction to {num}/{den} with denominator {den*k}.", "fill", "____")

    def multisel(i, sheet):
        num, den = _rand_proper_frac(4)
        opts = [(num * 2, den * 2), (num * 3, den * 3), (num + 1, den + 1), (num * 2, den * 3)]
        opts_str = "  ".join(f"{chr(65+k)}) {n}/{d}" for k, (n, d) in enumerate(opts))
        return q(f"Which are equivalent to {num}/{den}? Select ALL that apply: {opts_str}", "fill", "____ (list all letters)")

    def matching(i, sheet):
        pairs = []
        for _ in range(3):
            num, den = _rand_proper_frac(5)
            k = random.randint(2, 4)
            pairs.append((num, den, k))
        lefts = [f"{n}/{d}" for n, d, k in pairs]
        rights = [f"{n*k}/{d*k}" for n, d, k in pairs]
        return matching_q(lefts, rights)

    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Equivalent Fractions",
        ["Multiply (or divide) the numerator AND denominator by the SAME number.",
         "The fraction's VALUE never changes -- only how it's split.",
         "1/2 = 2/4 = 3/6 = 4/8 ... all the same amount, different pieces."],
        "two_bars_example", {"num1": 1, "den1": 2, "num2": 2, "den2": 4, "op": "compare"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=30)

# ═══════════════════════ CUM1: Review A + B + C ═══════════════════════
def _CUM1_s(sheet):
    def comp(i, sheet):
        choice = i % 3
        if choice == 0:
            num, den = _rand_fraction(6)
            return q(f"{num}/{den} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den})
        elif choice == 1:
            den = random.randint(2, 6); whole = random.randint(1, 3); rem = random.randint(1, den - 1)
            return q(f"{whole*den+rem}/{den} = ____ (mixed number)", "diagram", "____", "", "fraction_bar_blank", {"den": den, "segments": whole + 1})
        else:
            den1 = random.randint(2, 5); mult = random.randint(2, 4); num1 = random.randint(1, den1 - 1)
            return q(f"{num1}/{den1} = ____/{den1*mult}", "diagram", "____", "", "two_bars_blank", {"den1": den1, "den2": den1 * mult})

    def tf(i, sheet):
        den = random.randint(3, 8); num = random.randint(2, den - 1)
        shown = num if random.random() > 0.4 else num + 1
        return q(f"True or False: {num}/{den} is {shown} copies of the unit fraction 1/{den}.", "fill", "____ (True/False)")

    def missing(i, sheet):
        den = random.randint(2, 6); whole = random.randint(1, 3); rem = random.randint(1, den - 1)
        num = whole * den + rem
        return q(f"{num}/{den} = {whole} ____/{den}. Find the missing numerator.", "fill", "____")

    def numeral(i, sheet):
        num, den = _rand_fraction(6)
        return q(f"{num}/{den}: is it proper or improper? What is it in words?", "fill", "____")

    def multisel(i, sheet):
        den = random.randint(4, 8)
        opts = [f"{den-1}/{den}", f"1/{den}", f"{den}/{den}", f"0/{den}"]
        return q(f"Which show MOST of the whole shaded? Select ALL: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")

    def matching(i, sheet):
        den = random.randint(3, 6)
        wholes = random.sample(range(1, 4), 3)
        lefts = [f"{w*den}/{den}" for w in wholes]
        rights = [str(w) for w in wholes]
        return matching_q(lefts, rights)

    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review: Fraction Concept, Mixed Numbers, Equivalence",
        ["Mix of fraction concept, unit fractions, proper/improper/mixed numbers, and equivalent fractions."],
        "fraction_bar_example", {"num": 3, "den": 4},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=100)


# ═══════════════════════ D: Simplify via GCF ═══════════════════════
def _D_s(sheet):
    def comp(i, sheet):
        den = random.choice([4, 6, 8, 9, 10, 12]); num = random.randint(2, den - 1)
        return q(f"{num}/{den} = ____ (simplify using the GCF)", "diagram", "____", "", "fraction_bar_blank", {"den": den})

    def tf(i, sheet):
        den = random.choice([6, 8, 9, 10, 12]); num = random.randint(2, den - 1)
        g = _gcd(num, den)
        correct = f"{num//g}/{den//g}"
        shown = correct if random.random() > 0.4 else f"{num}/{den}"
        return q(f"True or False: {num}/{den} simplifies to {shown}", "fill", "____ (True/False)")

    def missing(i, sheet):
        den = random.choice([6, 8, 9, 10, 12])
        return q(f"____ /{den} simplifies to 1/2 (find a numerator that works)", "diagram", "____", "", "fraction_bar_blank", {"den": den})

    def numeral(i, sheet):
        den = random.choice([4, 6, 8, 9, 10, 12]); num = random.randint(2, den - 1)
        return q(f"{num}/{den} = ____ (simplest form)", "fill", "____")

    def multisel(i, sheet):
        tn, td = random.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)])
        k1, k2 = random.sample(range(2, 5), 2)
        opts = [f"{tn*k1}/{td*k1}", f"{tn*k2}/{td*k2}", f"{tn*k1+1}/{td*k1}", f"{random.randint(1,6)}/{random.randint(2,7)}"]
        random.shuffle(opts)
        return q(f"Which simplify to {tn}/{td}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}", "fill", "____ (list all letters)")

    def matching(i, sheet):
        pairs = [(4, 8), (6, 12), (3, 9), (2, 10)]
        chosen = random.sample(pairs, 3)
        lefts = [f"{n}/{d}" for n, d in chosen]
        rights = [f"{n//_gcd(n,d)}/{d//_gcd(n,d)}" for n, d in chosen]
        return matching_q(lefts, rights)

    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Simplify via the GCF",
        ["Find the GCF (Greatest Common Factor) of the numerator and denominator.",
         "8/12: GCF of 8 and 12 is 4. Divide both by 4: 8/12 = 2/3."],
        "fraction_bar_example", {"num": 2, "den": 3, "label": "8/12 = 2/3 (GCF=4)"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=50)

# ═══════════════════════ E: Compare Fractions (LCM, benchmark, cross-multiplication) ═══════════════════════
def _E_s(sheet):
    def comp(i, sheet):
        den1, den2 = random.sample([2, 3, 4, 5, 6, 8], 2)
        num1 = random.randint(1, den1 - 1); num2 = random.randint(1, den2 - 1)
        return q(f"{num1}/{den1} ___ {num2}/{den2}  (>, < or =)", "diagram", "____", "", "two_bars_blank", {"den1": den1, "den2": den2})

    def tf(i, sheet):
        den1, den2 = random.sample([2, 3, 4, 5, 6], 2)
        num1 = random.randint(1, den1 - 1); num2 = random.randint(1, den2 - 1)
        correct = ">" if num1 / den1 > num2 / den2 else ("<" if num1 / den1 < num2 / den2 else "=")
        shown = correct if random.random() > 0.4 else random.choice([s for s in [">", "<", "="] if s != correct])
        return q(f"True or False: {num1}/{den1} {shown} {num2}/{den2}", "fill", "____ (True/False)")

    def missing(i, sheet):
        # NEW: cross-multiplication method, using the bowtie diagram
        den1, den2 = random.sample([2, 3, 4, 5, 6, 7], 2)
        num1 = random.randint(1, den1 - 1); num2 = random.randint(1, den2 - 1)
        return q(f"Compare {num1}/{den1} and {num2}/{den2} using cross-multiplication (find both cross products, then compare).",
                  "diagram", "____", "", "cross_multiply_bowtie", {"num1": num1, "den1": den1, "num2": num2, "den2": den2})

    def numeral(i, sheet):
        den1, den2 = random.sample([2, 3, 4, 5, 6, 8], 2)
        num1 = random.randint(1, den1 - 1); num2 = random.randint(1, den2 - 1)
        return q(f"Cross-multiply to compare: {num1}/{den1} ___ {num2}/{den2}", "fill", "____")

    def multisel(i, sheet):
        bn, bd = random.choice([(1, 2), (1, 3), (2, 3)])
        opts_pool = [(bn * 2, bd * 2 - 1), (bn, bd), (1, bd * 3), (bn * 2 + 1, bd * 2)]
        random.shuffle(opts_pool)
        opts = [f"{n}/{d}" for n, d in opts_pool]
        return q(f"Which are GREATER than {bn}/{bd}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")

    def matching(i, sheet):
        fracs = [(1, 4), (1, 2), (3, 4)]
        lefts = [f"{n}/{d}" for n, d in fracs]
        rights = ["near 0", "near 1/2", "near 1"]
        return matching_q(lefts, rights)

    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Comparing Fractions — Three Methods",
        ["LCM method: rewrite both with a common denominator, then compare numerators.",
         "Benchmark method: is each fraction closer to 0, 1/2, or 1?",
         "CROSS-MULTIPLICATION: for a/b vs c/d, compare a x d to c x b -- bigger cross-product wins.",
         "2/3 vs 3/5: 2x5=10 and 3x3=9. Since 10>9, 2/3 > 3/5."],
        "two_bars_example", {"num1": 1, "den1": 3, "num2": 2, "den2": 4},
        "Formats rotate each sheet: computation, True/False, cross-multiplication, numeral, multi-select, matching.",
        fmt, sheet, seed_base=60)

# ═══════════════════════ F: Add & Subtract Fractions (like + unlike) ═══════════════════════
def _F_s(sheet):
    def comp(i, sheet):
        den = random.randint(3, 8); n1 = random.randint(1, den - 1); n2 = random.randint(1, den - n1)
        op = "+" if i % 2 == 0 else "-"
        if op == "-" and n1 < n2: n1, n2 = n2, n1
        return q(f"{n1}/{den} {op} {n2}/{den} = ____  (LIKE denominators)", "diagram", "____", "", "fraction_bar_blank", {"den": den})

    def tf(i, sheet):
        den = random.randint(3, 8); n1 = random.randint(1, den - 1); n2 = random.randint(1, max(den - n1, 1))
        correct = n1 + n2
        shown = correct if random.random() > 0.4 else correct + 1
        return q(f"True or False: {n1}/{den} + {n2}/{den} = {shown}/{den}", "fill", "____ (True/False)")

    def missing(i, sheet):
        den1, den2 = random.sample([2, 3, 4, 5, 6], 2)
        n1 = random.randint(1, den1 - 1); n2 = random.randint(1, den2 - 1)
        op = "+" if i % 2 == 0 else "-"
        return q(f"{n1}/{den1} {op} {n2}/{den2} = ____  (UNLIKE denominators -- find the LCM first)", "diagram", "____", "", "two_bars_blank", {"den1": den1, "den2": den2})

    def numeral(i, sheet):
        den1, den2 = random.sample([2, 3, 4, 5, 6], 2)
        n1 = random.randint(1, den1 - 1); n2 = random.randint(1, den2 - 1)
        op = "+" if i % 2 == 0 else "-"
        return q(f"{n1}/{den1} {op} {n2}/{den2} = ____  (UNLIKE denominators)", "fill", "____")

    def multisel(i, sheet):
        bn, bd = random.choice([(1, 2), (2, 3), (1, 3)])
        pairs = []
        for _ in range(4):
            da, db = random.sample([2, 3, 4, 6], 2)
            na, nb = random.randint(1, da - 1), random.randint(1, db - 1)
            pairs.append((na, da, nb, db))
        opts_str = "  ".join(f"{chr(65+k)}) {na}/{da}+{nb}/{db}" for k, (na, da, nb, db) in enumerate(pairs))
        return q(f"Compute each sum. Which are GREATER than {bn}/{bd}? Select ALL that apply: {opts_str}", "fill", "____ (list all letters)")

    def matching(i, sheet):
        pairs = [(1, 3, 1, 4), (1, 2, 1, 4), (1, 3, 1, 6)]
        lefts = [f"{a}/{b}+{c}/{d}" for a, b, c, d in pairs]
        rights = ["7/12", "3/4", "1/2"]
        return matching_q(lefts, rights)

    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Add & Subtract Fractions",
        ["SAME denominator: just add/subtract the numerators. 2/8+3/8=5/8.",
         "DIFFERENT denominators: find the LCM first, convert both, then add/subtract.",
         "1/3 + 1/4: LCM=12. 1/3=4/12, 1/4=3/12. 4/12+3/12=7/12."],
        "fraction_bar_example", {"num": 5, "den": 8, "label": "2/8 + 3/8 = 5/8"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=70)

# ═══════════════════════ CUM2: Review D + E + F ═══════════════════════
def _CUM2_s(sheet):
    def comp(i, sheet):
        choice = i % 3
        if choice == 0:
            den = random.choice([6, 8, 9, 10]); num = random.randint(2, den - 1)
            return q(f"{num}/{den} = ____ (simplest form)", "diagram", "____", "", "fraction_bar_blank", {"den": den})
        elif choice == 1:
            den1, den2 = random.sample([2, 3, 4, 5, 6], 2)
            num1 = random.randint(1, den1 - 1); num2 = random.randint(1, den2 - 1)
            return q(f"{num1}/{den1} ___ {num2}/{den2}", "diagram", "____", "", "two_bars_blank", {"den1": den1, "den2": den2})
        else:
            den = random.randint(3, 8); n1 = random.randint(1, den - 1); n2 = random.randint(1, den - n1)
            return q(f"{n1}/{den} + {n2}/{den} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den})

    def tf(i, sheet):
        den1, den2 = random.sample([2, 3, 4, 5, 6], 2)
        num1 = random.randint(1, den1 - 1); num2 = random.randint(1, den2 - 1)
        correct = ">" if num1 / den1 > num2 / den2 else "<"
        return q(f"True or False: {num1}/{den1} {correct} {num2}/{den2}", "fill", "____ (True/False)")

    def missing(i, sheet):
        den = random.choice([6, 8, 9, 10])
        return q(f"____ /{den} simplifies to 1/2", "diagram", "____", "", "fraction_bar_blank", {"den": den})

    def numeral(i, sheet):
        den1, den2 = random.sample([2, 3, 4, 5, 6], 2)
        n1 = random.randint(1, den1 - 1); n2 = random.randint(1, den2 - 1)
        return q(f"{n1}/{den1} + {n2}/{den2} = ____", "fill", "____")

    def multisel(i, sheet):
        tn, td = random.choice([(1, 2), (1, 3), (2, 3), (1, 4)])
        k1, k2 = random.sample(range(2, 5), 2)
        opts = [f"{tn*k1}/{td*k1}", f"{tn}/{td}", f"{tn*k2}/{td*k2}", f"{random.randint(1,6)}/{random.randint(2,7)}"]
        random.shuffle(opts)
        return q(f"Which are equivalent to {tn}/{td}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}", "fill", "____ (list all letters)")

    def matching(i, sheet):
        pairs = [(4, 8), (6, 12), (3, 9)]
        lefts = [f"{n}/{d}" for n, d in pairs]
        rights = [f"{n//_gcd(n,d)}/{d//_gcd(n,d)}" for n, d in pairs]
        return matching_q(lefts, rights)

    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review: Simplify, Compare, Add & Subtract",
        ["Mix of simplifying via GCF, comparing fractions, and adding/subtracting."],
        "two_bars_example", {"num1": 1, "den1": 3, "num2": 2, "den2": 6},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=200)


# ═══════════════════════ G: Add & Subtract Mixed Numbers ═══════════════════════
def _G_s(sheet):
    def comp(i, sheet):
        w1, w2 = random.randint(1, 3), random.randint(1, 2)
        den = random.randint(2, 6); n1, n2 = random.randint(1, den - 1), random.randint(1, den - 1)
        op = "+" if i % 2 == 0 else "-"
        if op == "-": w1 = max(w1, w2) + 1
        return q(f"{w1} {n1}/{den} {op} {w2} {n2}/{den} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den, "segments": w1 + 1})

    def tf(i, sheet):
        w1, w2 = random.randint(1, 2), random.randint(1, 2)
        den = random.randint(2, 4)
        correct = w1 + w2
        shown = correct if random.random() > 0.4 else correct + 1
        return q(f"True or False: {w1} 1/{den} + {w2} 1/{den} = {shown} 2/{den}", "fill", "____ (True/False)")

    def missing(i, sheet):
        # Regrouping/borrowing: minuend's fraction part is SMALLER, so you must
        # "borrow" a whole (turn it into den/den) before subtracting.
        den = random.randint(3, 6)
        n1 = random.randint(1, den - 2)
        n2 = random.randint(n1 + 1, den - 1)
        w1 = random.randint(3, 6)
        w2 = random.randint(1, w1 - 1)
        return q(f"{w1} {n1}/{den} - {w2} {n2}/{den} = ____  (the fraction part needs REGROUPING -- borrow a whole first)",
                  "diagram", "____", "", "fraction_bar_blank", {"den": den, "segments": w1 + 1})

    def numeral(i, sheet):
        w1, w2 = random.randint(1, 3), random.randint(1, 2)
        den = random.randint(2, 6); n1, n2 = random.randint(1, den - 1), random.randint(1, den - 1)
        op = "+" if i % 2 == 0 else "-"
        if op == "-": w1 = max(w1, w2) + 1
        return q(f"{w1} {n1}/{den} {op} {w2} {n2}/{den} = ____", "fill", "____")

    def multisel(i, sheet):
        w1, w2 = random.randint(1, 2), random.randint(1, 2)
        den = random.randint(2, 4)
        target = f"{w1+w2} {random.randint(1,den-1)}/{den}"
        opts_str = "  ".join(f"{chr(65+k)}) {random.randint(1,2)} {random.randint(1,den-1)}/{den}+{random.randint(1,2)} {random.randint(1,den-1)}/{den}" for k in range(4))
        return q(f"Compute each sum. Which are close to {target}? Select ALL that apply: {opts_str}", "fill", "____ (list all letters)")

    def matching(i, sheet):
        den = random.randint(2, 4)
        pairs = [(random.randint(1, 2), random.randint(1, 2)) for _ in range(3)]
        lefts = [f"{w1} 1/{den}+{w2} 1/{den}" for w1, w2 in pairs]
        rights = [f"{w1+w2} 2/{den}" for w1, w2 in pairs]
        return matching_q(lefts, rights)

    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Add & Subtract Mixed Numbers",
        ["Add/subtract the whole numbers and the fractions separately, then combine.",
         "2 1/4 + 1 2/4 = (2+1) + (1/4+2/4) = 3 + 3/4 = 3 3/4.",
         "REGROUPING: if the fraction you're subtracting is bigger, borrow a whole first.",
         "5 1/4 - 2 3/4: borrow -> 4 5/4 - 2 3/4 = 2 2/4 = 2 1/2."],
        "fraction_bar_example", {"num": 3, "den": 4, "label": "2 1/4 + 1 2/4 = 3 3/4"},
        "Formats rotate each sheet: computation, True/False, missing-number, numeral, multi-select, matching.",
        fmt, sheet, seed_base=90)

# ═══════════════════════ H: Multiply Fractions & Mixed Numbers ═══════════════════════
def _H_s(sheet):
    def comp(i, sheet):
        n1, d1 = _rand_fraction(5); n2, d2 = _rand_fraction(5)
        return q(f"{n1}/{d1} x {n2}/{d2} = ____", "diagram", "____", "", "fraction_area_blank", {"den1": d1, "den2": d2})

    def tf(i, sheet):
        n1, d1 = _rand_fraction(5); n2, d2 = _rand_fraction(5)
        correct_num, correct_den = n1 * n2, d1 * d2
        shown = f"{correct_num}/{correct_den}" if random.random() > 0.4 else f"{correct_num+1}/{correct_den}"
        return q(f"True or False: {n1}/{d1} x {n2}/{d2} = {shown}", "fill", "____ (True/False)")

    def missing(i, sheet):
        # NEW: genuine mixed-number x mixed-number, via the 4-part area model.
        w1 = random.randint(1, 3); d1 = random.randint(2, 4); n1 = random.randint(1, d1 - 1)
        w2 = random.randint(1, 3); d2 = random.randint(2, 4); n2 = random.randint(1, d2 - 1)
        return q(f"{w1} {n1}/{d1} x {w2} {n2}/{d2} = ____  (use the area model: 4 parts, then add them up)",
                  "diagram", "____", "", "mixed_number_area_blank", {"w1": w1, "n1": n1, "d1": d1, "w2": w2, "n2": n2, "d2": d2})

    def numeral(i, sheet):
        w = random.randint(1, 5); n2, d2 = _rand_fraction(5)
        return q(f"{w} x {n2}/{d2} = ____  (whole number x fraction)", "fill", "____")

    def multisel(i, sheet):
        tn, td = random.choice([(1, 4), (1, 6), (1, 2), (1, 3)])
        f1 = random.choice([(1, 2), (1, 3), (1, 4)])
        f2n, f2d = tn * f1[1], td * f1[0]
        opts = [f"{f1[0]}/{f1[1]}x{f2n}/{f2d}", f"{tn}/{td}x1/1", f"{random.randint(1,3)}/{random.randint(2,5)}x{random.randint(1,3)}/{random.randint(2,5)}", f"{random.randint(1,3)}/{random.randint(2,5)}x{random.randint(1,3)}/{random.randint(2,5)}"]
        random.shuffle(opts)
        return q(f"Which equal {tn}/{td}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}", "fill", "____ (list all letters)")

    def matching(i, sheet):
        pairs = [(1, 2, 1, 2), (1, 3, 1, 2), (2, 3, 1, 2)]
        lefts = [f"{a}/{b}x{c}/{d}" for a, b, c, d in pairs]
        rights = ["1/4", "1/6", "1/3"]
        return matching_q(lefts, rights)

    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Multiply Fractions & Mixed Numbers",
        ["Fraction x fraction: shade columns for the first, rows for the second. Overlap = the answer.",
         "2/3 x 3/4: 6 of 12 squares double-shaded = 6/12 = 1/2.",
         "MIXED numbers: split each into whole+fraction, use a 2x2 area grid (4 partial products), then add all 4.",
         "1 1/2 x 2 1/3: (1x2) + (1x1/3) + (1/2x2) + (1/2x1/3) = 2 + 1/3 + 1 + 1/6 = 3 1/2."],
        "fraction_area_example", {"num1": 2, "den1": 3, "num2": 3, "den2": 4},
        "Formats rotate each sheet: computation, True/False, area-model, numeral, multi-select, matching.",
        fmt, sheet, seed_base=110)

# ═══════════════════════ I: Divide Fractions ═══════════════════════
def _I_s(sheet):
    def comp(i, sheet):
        if i % 2 == 0:
            den = random.randint(2, 6); whole = random.randint(2, 4)
            return q(f"1/{den} / {whole} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den * whole})
        den = random.randint(2, 5)
        return q(f"{random.randint(2,5)} / 1/{den} = ____", "diagram", "____", "", "fraction_numberline_blank", {"den": den})

    def tf(i, sheet):
        den = random.randint(2, 5); whole = random.randint(2, 4)
        correct = den * whole
        shown = correct if random.random() > 0.4 else correct + 1
        return q(f"True or False: 1/{den} / {whole} = 1/{shown}", "fill", "____ (True/False)")

    def missing(i, sheet):
        # NEW: reciprocal as its own concept, using the flip diagram.
        n, d = _rand_fraction(7)
        return q(f"Find the RECIPROCAL of {n}/{d} (swap the numerator and denominator).",
                  "diagram", "____", "", "reciprocal_flip", {"num": n, "den": d})

    def numeral(i, sheet):
        # NEW: general fraction / fraction, via "flip and multiply".
        n1, d1 = _rand_fraction(6); n2, d2 = _rand_fraction(6)
        return q(f"{n1}/{d1} / {n2}/{d2} = ____  (flip the second fraction, then multiply)", "fill", "____")

    def multisel(i, sheet):
        den = random.randint(2, 5); whole = random.randint(2, 4)
        val = f"1/{den*whole}"
        opts = [f"1/{den} / {whole}", val, f"{whole} / 1/{den}", f"1/{den+1} / {whole}"]
        random.shuffle(opts)
        return q(f"Which describe the SAME value as {val}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}",
                  "fill", "____ (list all letters)")

    def matching(i, sheet):
        pairs = [(*_rand_fraction(5), *_rand_fraction(5)) for _ in range(3)]
        lefts = [f"{a}/{b} div {c}/{d}" for a, b, c, d in pairs]
        rights = [f"{a*d}/{b*c}" for a, b, c, d in pairs]
        return matching_q(lefts, rights)

    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Divide Fractions",
        ["Dividing a unit fraction by a whole splits it smaller: 1/3 / 2 = 1/6.",
         "Dividing a whole by a unit fraction counts how many fit: 2 / 1/4 = 8.",
         "GENERAL RULE: to divide by any fraction, FLIP it (find its reciprocal) and MULTIPLY instead.",
         "2/3 / 4/5 = 2/3 x 5/4 = 10/12 = 5/6."],
        "fraction_bar_example", {"num": 1, "den": 6, "label": "1/3 / 2 = 1/6"},
        "Formats rotate each sheet: computation, True/False, reciprocal, numeral, multi-select, matching.",
        fmt, sheet, seed_base=130)

# ═══════════════════════ CUM3: Review G + H + I ═══════════════════════
def _CUM3_s(sheet):
    def comp(i, sheet):
        choice = i % 3
        if choice == 0:
            w1, w2 = random.randint(1, 3), random.randint(1, 2)
            den = random.randint(2, 6); n1, n2 = random.randint(1, den - 1), random.randint(1, den - 1)
            return q(f"{w1} {n1}/{den} + {w2} {n2}/{den} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den, "segments": w1 + 1})
        elif choice == 1:
            n1, d1 = _rand_fraction(5); n2, d2 = _rand_fraction(5)
            return q(f"{n1}/{d1} x {n2}/{d2} = ____", "diagram", "____", "", "fraction_area_blank", {"den1": d1, "den2": d2})
        else:
            den = random.randint(2, 6); whole = random.randint(2, 4)
            return q(f"1/{den} / {whole} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den * whole})

    def tf(i, sheet):
        n1, d1 = _rand_fraction(5); n2, d2 = _rand_fraction(5)
        correct_num, correct_den = n1 * n2, d1 * d2
        shown = f"{correct_num}/{correct_den}" if random.random() > 0.4 else f"{correct_num+1}/{correct_den}"
        return q(f"True or False: {n1}/{d1} x {n2}/{d2} = {shown}", "fill", "____ (True/False)")

    def missing(i, sheet):
        n, d = _rand_fraction(7)
        return q(f"Find the RECIPROCAL of {n}/{d}.", "diagram", "____", "", "reciprocal_flip", {"num": n, "den": d})

    def numeral(i, sheet):
        n1, d1 = _rand_fraction(6); n2, d2 = _rand_fraction(6)
        return q(f"{n1}/{d1} / {n2}/{d2} = ____  (flip and multiply)", "fill", "____")

    def multisel(i, sheet):
        w1, w2 = random.randint(1, 2), random.randint(1, 2)
        den = random.randint(2, 4)
        target_sum = f"{w1+w2} {random.randint(1,den-1)}/{den}"
        tn, td = random.choice([(1, 4), (1, 6)])
        raw_opts = [
            f"{random.randint(1,2)} 1/{den}+{random.randint(1,2)} 1/{den}",
            f"{random.randint(1,3)}/{random.randint(2,5)}x{random.randint(1,3)}/{random.randint(2,5)}",
            f"{random.randint(2,4)} / 1/{random.randint(2,4)}",
            f"{random.randint(1,3)}/{random.randint(2,5)}x{random.randint(1,3)}/{random.randint(2,5)}",
        ]
        opts_str = "  ".join(f"{chr(65+k)}) {v}" for k, v in enumerate(raw_opts))
        return q(f"Compute each. Which give a result of {tn}/{td} or {target_sum}? Select ALL that apply: {opts_str}",
                  "fill", "____ (list all letters)")

    def matching(i, sheet):
        pairs = [(1, 2, 1, 2), (1, 3, 1, 2), (2, 3, 1, 2)]
        lefts = [f"{a}/{b}x{c}/{d}" for a, b, c, d in pairs]
        rights = ["1/4", "1/6", "1/3"]
        return matching_q(lefts, rights)

    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Review: Mixed Numbers, Multiply, Divide",
        ["Mix of mixed-number addition/subtraction, multiplication, and division."],
        "fraction_area_example", {"num1": 2, "den1": 3, "num2": 3, "den2": 4},
        "Formats rotate each sheet: computation, True/False, reciprocal, numeral, multi-select, matching.",
        fmt, sheet, seed_base=300)


# ═══════════════════════ J: Word Problems & Estimation ═══════════════════════
def _J_s(sheet):
    templates_add = [
        "A recipe needs {n1}/{d1} cup sugar and {n2}/{d1} cup flour. Total = ____.",
        "A jug has {n1}/{d1} L of juice, then {n2}/{d1} L more is added. Total = ____.",
    ]
    templates_sub = [
        "A ribbon is {n1}/{d1} m long. {n2}/{d1} m is cut off. Left = ____.",
        "{n1}/{d1} of a cake is left, then {n2}/{d1} is eaten. Left = ____.",
    ]

    def comp(i, sheet):
        d1 = random.randint(3, 8); n1 = random.randint(1, d1 - 1); n2 = random.randint(1, d1 - n1) if d1 - n1 > 0 else 1
        txt = random.choice(templates_add if i % 2 == 0 else templates_sub).format(n1=n1, n2=n2, d1=d1)
        return q(txt, "diagram", "____", "", "fraction_bar_blank", {"den": d1})

    def tf(i, sheet):
        d1 = random.randint(3, 8); n1 = random.randint(1, d1 - 2); n2 = random.randint(1, d1 - n1)
        correct = n1 + n2
        shown = correct if random.random() > 0.4 else correct + 1
        return q(f"True or False: {n1}/{d1} + {n2}/{d1} of the same recipe = {shown}/{d1}", "fill", "____ (True/False)")

    def missing(i, sheet):
        # Estimation/benchmark placement, folded in from old N.
        n, d = _rand_fraction(8)
        return q(f"Estimate: is {n}/{d} closer to 0, 1/2, or 1? Place it on the number line.",
                  "diagram", "____", "", "fraction_numberline_blank", {"den": d})

    def numeral(i, sheet):
        d1 = random.randint(3, 8); n1 = random.randint(1, d1 - 1); n2 = random.randint(1, d1 - n1) if d1 - n1 > 0 else 1
        txt = random.choice(templates_add + templates_sub).format(n1=n1, n2=n2, d1=d1)
        return q(txt, "fill", "____")

    def multisel(i, sheet):
        bench, bench_lbl = random.choice([(0, "0"), (1, "1")])
        d = random.randint(6, 12)
        near = [1, d - 1] if bench == 0 else [d - 1, 1]
        opts_pool = [f"1/{d}", f"{d-1}/{d}", f"{random.randint(3,d//2)}/{d}", f"1/{random.randint(8,14)}"]
        random.shuffle(opts_pool)
        return q(f"Which fractions are CLOSE to {bench_lbl}? Select ALL that apply: A) {opts_pool[0]} B) {opts_pool[1]} C) {opts_pool[2]} D) {opts_pool[3]}",
                  "fill", "____ (list all letters)")

    def matching(i, sheet):
        d1 = random.randint(4, 8)
        cuts = random.sample(range(1, d1), 3)
        lefts = [f"{d1}/{d1} - {c}/{d1}" for c in cuts]
        rights = [f"{d1-c}/{d1}" for c in cuts]
        return matching_q(lefts, rights)

    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Word Problems & Estimation",
        ["Read carefully: are parts being joined, removed, shared, or repeated?",
         "'Half the cake is left, then 1/4 is eaten' means subtract: 1/2 - 1/4 = 1/4.",
         "Before calculating exactly, ESTIMATE: is the answer closer to 0, 1/2, or 1?"],
        "fraction_bar_example", {"num": 1, "den": 4, "label": "1/2 - 1/4 = 1/4"},
        "Formats rotate each sheet: computation, True/False, estimation, numeral, multi-select, matching.",
        fmt, sheet, seed_base=140)

# ═══════════════════════ REV: Level 6 Revision ═══════════════════════
def _REV_s(sheet):
    def comp(i, sheet):
        choice = i % 7
        if choice == 0:
            n, d = _rand_fraction(6); return q(f"{n}/{d} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": d})
        elif choice == 1:
            n1, d1 = _rand_fraction(5); n2, d2 = _rand_fraction(5)
            return q(f"{n1}/{d1} x {n2}/{d2} = ____", "diagram", "____", "", "fraction_area_blank", {"den1": d1, "den2": d2})
        elif choice == 2:
            den1, den2 = random.sample([2, 3, 4, 5, 6], 2); n1 = random.randint(1, den1 - 1); n2 = random.randint(1, den2 - 1)
            return q(f"{n1}/{den1} + {n2}/{den2} = ____", "diagram", "____", "", "two_bars_blank", {"den1": den1, "den2": den2})
        elif choice == 3:
            den = random.randint(2, 5); whole = random.randint(2, 4)
            return q(f"1/{den} / {whole} = ____", "diagram", "____", "", "fraction_bar_blank", {"den": den * whole})
        elif choice == 4:
            n, d = _rand_fraction(8); return q(f"Place {n}/{d} on the number line.", "diagram", "____", "", "fraction_numberline_blank", {"den": d})
        elif choice == 5:
            den = random.choice([6, 8, 9, 10]); num = random.randint(2, den - 1)
            return q(f"{num}/{den} = ____ (simplest form)", "diagram", "____", "", "fraction_bar_blank", {"den": den})
        else:
            w1 = random.randint(1, 2); d1 = random.randint(2, 4); n1 = random.randint(1, d1 - 1)
            w2 = random.randint(1, 2); d2 = random.randint(2, 4); n2 = random.randint(1, d2 - 1)
            return q(f"{w1} {n1}/{d1} x {w2} {n2}/{d2} = ____ (area model)", "diagram", "____", "", "mixed_number_area_blank",
                      {"w1": w1, "n1": n1, "d1": d1, "w2": w2, "n2": n2, "d2": d2})

    def tf(i, sheet):
        n, d = _rand_fraction(8)
        return q(f"True or False: {n}/{d} is already in simplest form (check the GCF).", "fill", "____ (True/False)")

    def missing(i, sheet):
        if i % 2 == 0:
            den = random.choice([6, 8, 9, 10])
            return q(f"____ /{den} simplifies to 1/2", "diagram", "____", "", "fraction_bar_blank", {"den": den})
        n1, d1 = _rand_fraction(6); n2, d2 = _rand_fraction(6)
        return q(f"Compare {n1}/{d1} and {n2}/{d2} using cross-multiplication.", "diagram", "____", "", "cross_multiply_bowtie",
                  {"num1": n1, "den1": d1, "num2": n2, "den2": d2})

    def numeral(i, sheet):
        den1, den2 = random.sample([2, 3, 4, 5, 6], 2); n1 = random.randint(1, den1 - 1); n2 = random.randint(1, den2 - 1)
        op = random.choice(["+", "-", "x", "/"])
        return q(f"{n1}/{den1} {op} {n2}/{den2} = ____", "fill", "____")

    def multisel(i, sheet):
        tn, td = random.choice([(1, 2), (1, 3), (2, 3), (1, 4)])
        k1, k2 = random.sample(range(2, 5), 2)
        opts = [f"{tn*k1}/{td*k1}", f"{tn*k2}/{td*k2}", f"{tn}/{td}", f"{random.randint(1,6)}/{random.randint(2,7)}"]
        random.shuffle(opts)
        return q(f"Which are equivalent to {tn}/{td}? Select ALL that apply: A) {opts[0]} B) {opts[1]} C) {opts[2]} D) {opts[3]}", "fill", "____ (list all letters)")

    def matching(i, sheet):
        pairs = [(4, 8), (6, 12), (3, 9)]
        lefts = [f"{n}/{d}" for n, d in pairs]
        rights = [f"{n//_gcd(n,d)}/{d//_gcd(n,d)}" for n, d in pairs]
        return matching_q(lefts, rights)

    fmt = {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
    return make_rotated_sheet(
        "Level 6 Revision",
        ["Every fraction skill: concept, equivalence, all four operations, mixed numbers, and comparison techniques."],
        "two_bars_example", {"num1": 1, "den1": 3, "num2": 2, "den2": 4},
        "Formats rotate each sheet: computation, True/False, cross-multiplication, numeral, multi-select, matching.",
        fmt, sheet, seed_base=500)


# ───────────────────────── Dispatcher (REPLACES original Level 6) ─────────────────────────
def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL6_DISPATCH = {
    "6A": _wrap(_A_s), "6B": _wrap(_B_s), "6C": _wrap(_C_s), "6CUM1": _wrap(_CUM1_s),
    "6D": _wrap(_D_s), "6E": _wrap(_E_s), "6F": _wrap(_F_s), "6CUM2": _wrap(_CUM2_s),
    "6G": _wrap(_G_s), "6H": _wrap(_H_s), "6I": _wrap(_I_s), "6CUM3": _wrap(_CUM3_s),
    "6J": _wrap(_J_s), "6REV": _wrap(_REV_s),
}
