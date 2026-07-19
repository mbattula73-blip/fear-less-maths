"""
Fear Less Maths — Question Content: Level 13 (Number Systems)
REPLACES the old Level 13 (Powers & Indices) content entirely -- Number
Systems is the genuine CBSE Class 9 chapter gap; Powers & Indices content
is superseded here rather than kept alongside it as a separate level.
CBSE Class 9 Number Systems chapter, full 14-sublevel treatment.
Flow: N/W/Z classification & closure -> Rational numbers -> Decimal
expansions -> Recurring-to-fraction -> Irrational numbers -> The real
number line -> Surds -> Rationalising (single, then binomial) ->
Laws of exponents for real numbers -> Word problems -> Revision.
Sheet 1=Intuition, Sheet 2=Concept, Sheet 3=Practice, Sheet 4=Mastery
"""
from content import cb, tb, q
import random
import math


# ═══ Helpers (all pure, no side effects) ═══
def _classify_nwz(n):
    """Returns the tightest label for an integer/decimal n."""
    if isinstance(n, float) and not n.is_integer():
        return "None of these (not an integer)"
    n = int(n)
    if n >= 1:
        return "Natural, Whole & Integer"
    if n == 0:
        return "Whole & Integer (not Natural)"
    return "Integer only (not Whole or Natural)"


def _in_set(x, set_name):
    if x is None:
        return False
    if set_name == "N":
        return x == int(x) and x >= 1
    if set_name == "W":
        return x == int(x) and x >= 0
    if set_name == "Z":
        return x == int(x)
    return True  # Q, R


def _closure_result(a, b, op):
    try:
        if op == "+": return a + b
        if op == "-": return a - b
        if op == "×": return a * b
        if op == "÷": return a / b if b != 0 else None
    except Exception:
        return None


def _prime_factor_multiset(n):
    n = abs(int(n))
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def _terminates(den):
    """A fraction in lowest terms terminates iff denominator's only
    prime factors are 2 and/or 5."""
    d = abs(int(den))
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def _gcd(a, b):
    return math.gcd(int(a), int(b))


def _simplify_surd(n):
    """Returns (k, m) such that sqrt(n) = k*sqrt(m), m squarefree-ish
    (largest perfect square factor pulled out)."""
    n = int(n)
    best_k = 1
    best_rest = n
    for k in range(int(math.isqrt(n)), 0, -1):
        if n % (k * k) == 0:
            best_k = k
            best_rest = n // (k * k)
            break
    return best_k, best_rest


def _is_perfect_square(n):
    r = math.isqrt(int(n))
    return r * r == n


# ═══════════════════════════════════════════════════════════════════════════════
# 26A — Natural, Whole & Integers (merged: classification + hierarchy + closure)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13A_s(sheet):
    random.seed(2600 + sheet)
    ranges = {1: (-10, 10), 2: (-20, 20), 3: (-50, 50), 4: (-100, 100)}
    lo, hi = ranges[sheet]
    items = [
        cb("Natural, Whole & Integer Numbers", [
            "N (Natural): 1, 2, 3, ...  W (Whole): 0, 1, 2, ...  Z (Integers): ..., -1, 0, 1, ...",
            "N \u2286 W \u2286 Z -- each set contains the one before it, plus more.",
            "CLOSED under an operation = the result always stays in that set. N isn't closed under subtraction (3-5=-2); Z is -- that's why negatives exist.",
        ], "-4 is an Integer only. 0 is Whole & Integer, not Natural. 7 is all three."),
    ]
    for _ in range(4):
        n = random.randint(lo, hi)
        items.append(q(f"Classify {n}: Natural, Whole, Integer, or None of these?", "diagram", "____",
                        "", "number_hierarchy", {"number": str(n), "memberships": (["natural"] if n >= 1 else ["whole"] if n == 0 else ["integer"])}))
    for _ in range(4):
        n = random.randint(lo, hi)
        items.append(q(f"Classify {n}: Natural, Whole, Integer, or None of these?", "fill", "Answer = ____"))
    for _ in range(4):
        setpair = random.choice([("N", "W"), ("W", "Z"), ("N", "Z")])
        items.append(q(f"True or False: Every {('Natural' if setpair[0]=='N' else 'Whole')} number is also {('a Whole' if setpair[1]=='W' else 'an Integer')} number.", "fill", "Answer = ____"))
    for _ in range(4):
        set_name = random.choice(["N", "W", "Z"])
        op = random.choice(["+", "-", "×", "÷"])
        a = random.randint(2, 12)
        b = random.randint(2, 12)
        if op == "-" and random.random() > 0.4:
            a, b = min(a, b), max(a, b)  # bias toward a<b so subtraction often leaves the set (more interesting)
        items.append(q(f"Is {set_name} closed under \u201c{op}\u201d? Test with {a} {op} {b}.", "diagram", "____",
                        "", "closure_test", {"a": a, "b": b, "op": op, "set_name": set_name}))
    for _ in range(4):
        set_name = random.choice(["N", "W", "Z"])
        items.append(q(f"Give one number that is in Z but NOT in {set_name}. ____", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 26B — Rational Numbers
# ═══════════════════════════════════════════════════════════════════════════════
def _L13B_s(sheet):
    random.seed(2610 + sheet)
    ranges = {1: (2, 12), 2: (2, 20), 3: (2, 40), 4: (2, 60)}
    lo, hi = ranges[sheet]
    items = [
        cb("Rational Numbers (Q)", [
            "A rational number is p/q, where p and q are integers and q \u2260 0.",
            "Every integer is rational (5 = 5/1). Two fractions are EQUIVALENT if they simplify to the same p/q.",
        ], "3/4 and 6/8 are equivalent -- both simplify to 3/4."),
    ]
    for _ in range(5):
        p = random.randint(1, hi)
        qd = random.randint(2, hi)
        items.append(q(f"Is {p}/{qd} a rational number? Why?", "fill", "Answer = ____"))
    for _ in range(5):
        k = random.randint(2, 6)
        p = random.randint(1, lo)
        qd = random.randint(2, lo)
        items.append(q(f"Is {p*k}/{qd*k} equivalent to {p}/{qd}?", "fill", "Answer = ____"))
    for _ in range(5):
        g = random.randint(2, 8)
        p = g * random.randint(2, 9)
        qd = g * random.randint(2, 9)
        while p == qd:
            qd = g * random.randint(2, 9)
        simplified_p, simplified_q = p // _gcd(p, qd), qd // _gcd(p, qd)
        items.append(q(f"Write {p}/{qd} in simplest form. ____", "fill", "Answer = ____"))
    for _ in range(5):
        n = random.randint(-hi, hi)
        items.append(q(f"Express the integer {n} as a rational number p/q. ____", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 26C — Decimal Expansions (terminating vs recurring)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13C_s(sheet):
    random.seed(2620 + sheet)
    term_dens = [2, 4, 5, 8, 10, 16, 20, 25, 40, 50]
    other_primes = [3, 6, 7, 9, 11, 12, 13, 15, 18, 22]
    items = [
        cb("Predicting a Decimal Expansion", [
            "Write the fraction in lowest terms, then look at the denominator's prime factors.",
            "Only 2s and/or 5s -> TERMINATES. Any other prime (3, 7, 11...) -> RECURS.",
        ], "1/8: denominator 8=2x2x2 -> terminates (0.125). 1/3: denominator 3 -> recurs (0.333...)."),
    ]
    for _ in range(5):
        den = random.choice(term_dens)
        num = random.randint(1, den - 1)
        g = _gcd(num, den)
        items.append(q(f"Will {num}/{den} terminate or recur? Check the denominator's prime factors.", "diagram", "____",
                        "", "decimal_expansion", {"num": num // g, "den": den // g}))
    for _ in range(5):
        den = random.choice(other_primes)
        num = random.randint(1, den - 1)
        g = _gcd(num, den)
        items.append(q(f"Will {num}/{den} terminate or recur? Check the denominator's prime factors.", "diagram", "____",
                        "", "decimal_expansion", {"num": num // g, "den": den // g}))
    for _ in range(5):
        den = random.choice(term_dens + other_primes)
        items.append(q(f"Without dividing: does a fraction with denominator {den} (in lowest terms) terminate? ____", "fill", "Answer = ____"))
    for _ in range(5):
        den = random.choice(term_dens + other_primes)
        verdict = "terminates" if _terminates(den) else "recurs"
        shown = verdict if random.random() > 0.35 else ("recurs" if verdict == "terminates" else "terminates")
        items.append(q(f"True or False: A fraction with denominator {den} (lowest terms) {shown}.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 26CUM1 — Recurring decimal -> fraction
# ═══════════════════════════════════════════════════════════════════════════════
def _L13CUM1_s(sheet):
    random.seed(2630 + sheet)
    single_digit_periods = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    two_digit_periods = ["12", "18", "27", "36", "45", "54", "63", "72", "81", "09"]
    items = [
        cb("Converting a Recurring Decimal to a Fraction", [
            "Let x = the decimal. Multiply by 10^(period length) to shift one repeat past the point.",
            "Subtract the original x -- the repeating part cancels. Solve for x.",
        ], "x = 0.333...  ->  10x = 3.333...  ->  10x-x=3  ->  9x=3  ->  x=3/9=1/3."),
    ]
    for _ in range(6):
        d = random.choice(single_digit_periods)
        items.append(q(f"Convert 0.{d}{d}{d}... (recurring) to a fraction.", "diagram", "____",
                        "", "recurring_to_fraction", {"digits": d, "period_len": 1}))
    for _ in range(6):
        d = random.choice(two_digit_periods)
        items.append(q(f"Convert 0.{d}{d}... (recurring) to a fraction.", "diagram", "____",
                        "", "recurring_to_fraction", {"digits": d, "period_len": 2}))
    for _ in range(4):
        d = random.choice(single_digit_periods)
        items.append(q(f"Convert 0.{d}{d}{d}... to a fraction. ____", "fill", "Answer = ____"))
    for _ in range(4):
        d = random.choice(two_digit_periods)
        items.append(q(f"Convert 0.{d}{d}... to a fraction. ____", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 26D — Irrational Numbers
# ═══════════════════════════════════════════════════════════════════════════════
def _L13D_s(sheet):
    random.seed(2640 + sheet)
    perfect = [4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]
    non_perfect = [2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 17, 18, 20]
    items = [
        cb("Irrational Numbers", [
            "An irrational number cannot be written as p/q -- its decimal never terminates or repeats.",
            "\u221an is irrational whenever n is NOT a perfect square. \u221a4=2 is rational; \u221a5 is irrational.",
        ], "\u221a16 = 4 -> rational. \u221a17 -> irrational (17 isn't a perfect square)."),
    ]
    for _ in range(5):
        n = random.choice(perfect)
        items.append(q(f"Is \u221a{n} rational or irrational?", "diagram", "____",
                        "", "number_hierarchy", {"number": f"\u221a{n} = {math.isqrt(n)}", "memberships": ["natural"]}))
    for _ in range(5):
        n = random.choice(non_perfect)
        items.append(q(f"Is \u221a{n} rational or irrational?", "diagram", "____",
                        "", "number_hierarchy", {"number": f"\u221a{n}", "memberships": ["irrational"]}))
    for _ in range(4):
        n = random.choice(perfect + non_perfect)
        items.append(q(f"Is \u221a{n} rational or irrational? ____", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("True or False: 22/7 is exactly equal to \u03c0.", "fill", "Answer = ____"))
    for _ in range(3):
        n = random.choice(non_perfect)
        items.append(q(f"Explain in one sentence why \u221a{n} is irrational.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 26E — The Real Number Line (successive magnification)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13E_s(sheet):
    random.seed(2650 + sheet)
    non_perfect = [2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 26, 30]
    items = [
        cb("The Real Number Line", [
            "Every point on the number line is exactly one real number -- rational or irrational.",
            "Locate an irrational (like \u221a2) between two consecutive integers, then zoom in decimal by decimal -- SUCCESSIVE MAGNIFICATION.",
        ], "\u221a2 \u2248 1.414: between 1 and 2, then 1.4 and 1.5, then 1.41 and 1.42..."),
    ]
    for _ in range(6):
        n = random.choice(non_perfect)
        r = math.isqrt(n)
        items.append(q(f"Between which two consecutive integers does \u221a{n} lie?", "fill", "Answer = ____"))
    for _ in range(6):
        n = random.choice(non_perfect)
        val = math.sqrt(n)
        lo1 = math.floor(val * 10) / 10
        hi1 = lo1 + 0.1
        items.append(q(f"\u221a{n} is between {lo1:.1f} and {hi1:.1f}. Narrow it down to one more decimal place (between which two values to 2 d.p.?)", "fill", "Answer = ____"))
    for _ in range(4):
        items.append(q("True or False: Every point on the number line is a rational number.", "fill", "Answer = ____"))
    for _ in range(4):
        items.append(q("True or False: Between any two rational numbers there is always another rational number.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 26CUM2 — Review B-E (Rational, Decimals, Irrational, Real Number Line)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13CUM2_s(sheet):
    random.seed(2660 + sheet)
    perfect = [4, 9, 16, 25, 36, 49, 64]
    non_perfect = [2, 3, 5, 6, 7, 10, 11, 12, 13, 15]
    term_dens = [2, 4, 5, 8, 10, 20, 25]
    other_primes = [3, 6, 7, 9, 11, 12]
    items = [
        cb("Review: Rationals, Decimals, Irrationals, the Real Line", [
            "Rational = p/q form, terminating or recurring decimal. Irrational = never terminates, never repeats.",
            "\u221an is irrational unless n is a perfect square. Rationals + irrationals together = the REAL numbers.",
        ], ""),
    ]
    for _ in range(5):
        p, qd = random.randint(1, 12), random.randint(2, 12)
        items.append(q(f"Is {p}/{qd} rational? ____", "fill", "Answer = ____"))
    for _ in range(5):
        den = random.choice(term_dens + other_primes)
        verdict = "terminates" if _terminates(den) else "recurs"
        items.append(q(f"A fraction with denominator {den} (lowest terms) -- terminates or recurs? ____", "fill", "Answer = ____"))
    for _ in range(5):
        n = random.choice(perfect + non_perfect)
        items.append(q(f"Is \u221a{n} rational or irrational? ____", "fill", "Answer = ____"))
    for _ in range(5):
        n = random.choice(non_perfect)
        items.append(q(f"Between which two consecutive integers does \u221a{n} lie? ____", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 26F — Surds — Simplifying
# ═══════════════════════════════════════════════════════════════════════════════
def _L13F_s(sheet):
    random.seed(2670 + sheet)
    ranges = {1: [8, 12, 18, 20, 27], 2: [24, 32, 45, 48, 50], 3: [50, 63, 72, 75, 80], 4: [72, 90, 98, 108, 125]}
    pool = ranges[sheet]
    items = [
        cb("Simplifying Surds", [
            "\u221an is in SIMPLEST FORM when n has no perfect-square factor left (other than 1).",
            "To simplify: find the largest perfect square that divides n, split \u221an = \u221a(k\u00b2 \u00d7 m) = k\u221am.",
        ], "\u221a72 = \u221a(36\u00d72) = 6\u221a2."),
    ]
    for _ in range(6):
        n = random.choice(pool)
        items.append(q(f"Simplify \u221a{n} to simplest form.", "diagram", "____", "", "surd_simplify_tree", {"n": n}))
    for _ in range(6):
        n = random.choice(pool)
        items.append(q(f"Simplify \u221a{n}. ____", "fill", "Answer = ____"))
    for _ in range(4):
        n = random.choice(pool)
        k, m = _simplify_surd(n)
        items.append(q(f"Is \u221a{n} already in simplest form? If not, what is it?", "fill", "Answer = ____"))
    for _ in range(4):
        a = random.randint(2, 6)
        n = random.choice(pool)
        items.append(q(f"Simplify {a}\u221a{n} (multiply the outside coefficient by the simplified surd's coefficient).", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 26G — Rationalising the Denominator (single term)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13G_s(sheet):
    random.seed(2680 + sheet)
    ranges = {1: [2, 3, 5, 7], 2: [3, 5, 6, 7, 10, 11], 3: [5, 6, 7, 10, 11, 13, 15], 4: [7, 10, 11, 13, 15, 17, 19]}
    pool = ranges[sheet]
    items = [
        cb("Rationalising a Single-Term Surd Denominator", [
            "1/\u221an has an irrational (surd) denominator -- not allowed in simplest form.",
            "Multiply top AND bottom by \u221an: 1/\u221an \u00d7 \u221an/\u221an = \u221an/n.",
        ], "1/\u221a5 = \u221a5/5."),
    ]
    for _ in range(6):
        n = random.choice(pool)
        items.append(q(f"Rationalise the denominator: 1/\u221a{n}", "diagram", "____", "", "rationalize_steps", {"kind": "single", "b": n}))
    for _ in range(6):
        n = random.choice(pool)
        items.append(q(f"Rationalise the denominator: 1/\u221a{n} = ____", "fill", "Answer = ____"))
    for _ in range(4):
        c = random.randint(2, 9)
        n = random.choice(pool)
        items.append(q(f"Rationalise the denominator: {c}/\u221a{n} = ____", "fill", "Answer = ____"))
    for _ in range(4):
        n = random.choice(pool)
        items.append(q(f"What must you multiply 1/\u221a{n} by (top and bottom) to rationalise it? ____", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 26H — Rationalising the Denominator (binomial / conjugate)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13H_s(sheet):
    random.seed(2690 + sheet)
    a_range = {1: (1, 3), 2: (2, 4), 3: (2, 6), 4: (3, 8)}
    c_pool = {1: [2, 3, 5], 2: [2, 3, 5, 6, 7], 3: [2, 3, 5, 6, 7, 10, 11], 4: [3, 5, 6, 7, 10, 11, 13]}
    alo, ahi = a_range[sheet]
    items = [
        cb("Rationalising with a Conjugate", [
            "For a denominator like (a + \u221ac), multiply top and bottom by its CONJUGATE (a - \u221ac).",
            "(a+\u221ac)(a-\u221ac) = a\u00b2 - c -- the surd disappears from the denominator.",
        ], "1/(2+\u221a3): multiply by (2-\u221a3)/(2-\u221a3) -> (2-\u221a3)/(4-3) = (2-\u221a3)/1 = 2-\u221a3."),
    ]
    for _ in range(6):
        a = random.randint(alo, ahi)
        c = random.choice(c_pool[sheet])
        while a * a == c:
            c = random.choice(c_pool[sheet])
        items.append(q(f"Rationalise the denominator: 1/({a}+\u221a{c})", "diagram", "____", "", "rationalize_steps", {"kind": "binomial", "a": a, "c": c}))
    for _ in range(6):
        a = random.randint(alo, ahi)
        c = random.choice(c_pool[sheet])
        while a * a == c:
            c = random.choice(c_pool[sheet])
        items.append(q(f"Rationalise the denominator: 1/({a}+\u221a{c}) = ____", "fill", "Answer = ____"))
    for _ in range(4):
        a = random.randint(alo, ahi)
        c = random.choice(c_pool[sheet])
        items.append(q(f"What is the conjugate of ({a}+\u221a{c})? ____", "fill", "Answer = ____"))
    for _ in range(4):
        a = random.randint(alo, ahi)
        c = random.choice(c_pool[sheet])
        items.append(q(f"({a}+\u221a{c})({a}-\u221a{c}) = ____ (simplify -- the surd should vanish)", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 26CUM3 — Mixed review: Surds & Rationalising (F/G/H)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13CUM3_s(sheet):
    random.seed(2700 + sheet)
    surd_pool = [8, 12, 18, 20, 24, 27, 32, 45, 48, 50, 72]
    single_pool = [2, 3, 5, 6, 7, 10, 11]
    items = [
        cb("Review: Surds & Rationalising", [
            "Simplify a surd by pulling out the largest perfect-square factor.",
            "Rationalise: single-term denominators using that surd; binomial denominators using the conjugate.",
        ], ""),
    ]
    for _ in range(6):
        n = random.choice(surd_pool)
        items.append(q(f"Simplify \u221a{n}. ____", "fill", "Answer = ____"))
    for _ in range(6):
        n = random.choice(single_pool)
        items.append(q(f"Rationalise: 1/\u221a{n} = ____", "fill", "Answer = ____"))
    for _ in range(4):
        a = random.randint(2, 5)
        c = random.choice([2, 3, 5])
        items.append(q(f"Rationalise: 1/({a}+\u221a{c}) = ____", "fill", "Answer = ____"))
    for _ in range(4):
        n = random.choice(surd_pool)
        items.append(q(f"True or False: \u221a{n} is already in simplest form.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 26I — Laws of Exponents for Real Numbers
# ═══════════════════════════════════════════════════════════════════════════════
def _L13I_s(sheet):
    random.seed(2710 + sheet)
    base_pool = {1: [2, 3, 5], 2: [2, 3, 4, 5], 3: [2, 3, 4, 5, 6], 4: [2, 3, 5, 7, 10]}
    bases = base_pool[sheet]
    items = [
        cb("Laws of Exponents for Real Numbers", [
            "These laws work for ANY real number base and ANY real exponent (including fractions):",
            "a^m \u00d7 a^n = a^(m+n)     a^m \u00f7 a^n = a^(m-n)     (a^m)^n = a^(mn)     a^(1/n) = \u207f\u221aa",
        ], "a^(1/2) means \u221aa. So 9^(1/2) = \u221a9 = 3."),
    ]
    for _ in range(5):
        a = random.choice(bases)
        m = random.randint(2, 5)
        n = random.randint(2, 5)
        items.append(q(f"Simplify: {a}^{m} \u00d7 {a}^{n} = {a}^____", "fill", "Answer = ____"))
    for _ in range(5):
        a = random.choice(bases)
        m = random.randint(4, 9)
        n = random.randint(1, 3)
        items.append(q(f"Simplify: {a}^{m} \u00f7 {a}^{n} = {a}^____", "fill", "Answer = ____"))
    for _ in range(5):
        a = random.choice(bases)
        m = random.randint(2, 4)
        n = random.randint(2, 3)
        items.append(q(f"Simplify: ({a}^{m})^{n} = {a}^____", "fill", "Answer = ____"))
    for _ in range(5):
        a = random.choice([4, 9, 16, 25, 8, 27])
        n = 2 if a in (4, 9, 16, 25) else 3
        root = round(a ** (1 / n))
        items.append(q(f"Evaluate: {a}^(1/{n}) = ____", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 26J — Word Problems
# ═══════════════════════════════════════════════════════════════════════════════
def _L13J_s(sheet):
    random.seed(2720 + sheet)
    items = [
        cb("Number Systems in the Real World", [
            "A square of side s has diagonal s\u221a2 -- almost always irrational.",
            "Correctly classifying a number (rational vs irrational) matters for how precisely you can measure or represent it.",
        ], "A square field of side 5m has diagonal 5\u221a2 m \u2248 7.07m -- an irrational length."),
    ]
    for _ in range(5):
        side = random.randint(2, 20)
        items.append(q(f"A square has side {side}m. Its diagonal is {side}\u221a2 m. Is this length rational or irrational?", "fill", "Answer = ____"))
    for _ in range(5):
        num = random.randint(1, 9)
        den = random.choice([3, 6, 7, 9, 11])
        items.append(q(f"A recipe needs {num}/{den} of a cup of flour. Will the decimal amount terminate or recur?", "fill", "Answer = ____"))
    for _ in range(5):
        r = random.randint(2, 15)
        items.append(q(f"A circle has radius {r}cm. Its circumference is 2\u03c0{r}cm. Is \u03c0 (and so the circumference) rational or irrational?", "fill", "Answer = ____"))
    for _ in range(5):
        n = random.choice([2, 3, 5, 6, 7, 10, 11, 13])
        items.append(q(f"A student says \u221a{n} \u2248 {round(math.sqrt(n),2)} is the EXACT value. Is the student correct? Explain.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 26REV — Level 26 Revision (mixed across all sublevels)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13REV_s(sheet):
    random.seed(2730 + sheet)
    perfect = [4, 9, 16, 25, 36, 49]
    non_perfect = [2, 3, 5, 6, 7, 10, 11, 12, 13, 15]
    surd_pool = [8, 12, 18, 20, 24, 27, 32, 45, 48, 50]
    term_dens = [2, 4, 5, 8, 10, 20]
    other_primes = [3, 6, 7, 9, 11]
    items = [
        cb("Level 26 Revision — Number Systems", [
            "N \u2286 W \u2286 Z \u2286 Q \u2286 R. Denominator only 2s/5s -> terminates, otherwise recurs.",
            "Simplify surds via perfect-square factors; rationalise using the surd itself (single) or its conjugate (binomial).",
        ], ""),
    ]
    for _ in range(3):
        n = random.randint(-30, 30)
        items.append(q(f"Classify {n}: Natural, Whole, Integer, or None of these? ____", "fill", "Answer = ____"))
    for _ in range(3):
        set_name = random.choice(["N", "W", "Z"])
        op = random.choice(["+", "-", "×"])
        a, b = random.randint(2, 10), random.randint(2, 10)
        items.append(q(f"Is {set_name} closed under \u201c{op}\u201d? Test with {a} {op} {b}.", "fill", "Answer = ____"))
    for _ in range(3):
        den = random.choice(term_dens + other_primes)
        items.append(q(f"Denominator {den} (lowest terms): terminating or recurring decimal? ____", "fill", "Answer = ____"))
    for _ in range(3):
        n = random.choice(perfect + non_perfect)
        items.append(q(f"Is \u221a{n} rational or irrational? ____", "fill", "Answer = ____"))
    for _ in range(3):
        n = random.choice(surd_pool)
        items.append(q(f"Simplify \u221a{n}. ____", "fill", "Answer = ____"))
    for _ in range(3):
        n = random.choice([2, 3, 5, 6, 7, 10])
        items.append(q(f"Rationalise: 1/\u221a{n} = ____", "fill", "Answer = ____"))
    for _ in range(2):
        a = random.choice([2, 3, 5])
        m, n = random.randint(2, 5), random.randint(2, 4)
        items.append(q(f"Simplify: {a}^{m} \u00d7 {a}^{n} = {a}^____", "fill", "Answer = ____"))
    return items


DISPATCH_L13NS = {
    "13A": {1: lambda: _L13A_s(1), 2: lambda: _L13A_s(2), 3: lambda: _L13A_s(3), 4: lambda: _L13A_s(4)},
    "13B": {1: lambda: _L13B_s(1), 2: lambda: _L13B_s(2), 3: lambda: _L13B_s(3), 4: lambda: _L13B_s(4)},
    "13C": {1: lambda: _L13C_s(1), 2: lambda: _L13C_s(2), 3: lambda: _L13C_s(3), 4: lambda: _L13C_s(4)},
    "13CUM1": {1: lambda: _L13CUM1_s(1), 2: lambda: _L13CUM1_s(2), 3: lambda: _L13CUM1_s(3), 4: lambda: _L13CUM1_s(4)},
    "13D": {1: lambda: _L13D_s(1), 2: lambda: _L13D_s(2), 3: lambda: _L13D_s(3), 4: lambda: _L13D_s(4)},
    "13E": {1: lambda: _L13E_s(1), 2: lambda: _L13E_s(2), 3: lambda: _L13E_s(3), 4: lambda: _L13E_s(4)},
    "13CUM2": {1: lambda: _L13CUM2_s(1), 2: lambda: _L13CUM2_s(2), 3: lambda: _L13CUM2_s(3), 4: lambda: _L13CUM2_s(4)},
    "13F": {1: lambda: _L13F_s(1), 2: lambda: _L13F_s(2), 3: lambda: _L13F_s(3), 4: lambda: _L13F_s(4)},
    "13G": {1: lambda: _L13G_s(1), 2: lambda: _L13G_s(2), 3: lambda: _L13G_s(3), 4: lambda: _L13G_s(4)},
    "13H": {1: lambda: _L13H_s(1), 2: lambda: _L13H_s(2), 3: lambda: _L13H_s(3), 4: lambda: _L13H_s(4)},
    "13CUM3": {1: lambda: _L13CUM3_s(1), 2: lambda: _L13CUM3_s(2), 3: lambda: _L13CUM3_s(3), 4: lambda: _L13CUM3_s(4)},
    "13I": {1: lambda: _L13I_s(1), 2: lambda: _L13I_s(2), 3: lambda: _L13I_s(3), 4: lambda: _L13I_s(4)},
    "13J": {1: lambda: _L13J_s(1), 2: lambda: _L13J_s(2), 3: lambda: _L13J_s(3), 4: lambda: _L13J_s(4)},
    "13REV": {1: lambda: _L13REV_s(1), 2: lambda: _L13REV_s(2), 3: lambda: _L13REV_s(3), 4: lambda: _L13REV_s(4)},
}


# ═══════════════════════════════════════════════════════════════════════════════
# Blank/worked wrapper: first 2 diagram questions per sheet are fully worked
# (a demo), the rest are blank scaffolds -- same pattern as every other level.
# ═══════════════════════════════════════════════════════════════════════════════
def _l13ns_visualize(items):
    out = []
    diagram_count = 0
    for item in items:
        new_item = dict(item)
        if item.get("type") == "diagram":
            params = dict(item.get("diagram_params") or {})
            params["blank"] = diagram_count >= 2
            new_item["diagram_params"] = params
            diagram_count += 1
        out.append(new_item)
    return out


def _l13ns_wrap(fn):
    return lambda: _l13ns_visualize(fn())


DISPATCH_L13NS = {
    sub: {sheet: _l13ns_wrap(fn) for sheet, fn in sheets.items()}
    for sub, sheets in DISPATCH_L13NS.items()
}
