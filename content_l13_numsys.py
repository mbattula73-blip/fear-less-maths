"""
Fear Less Maths — Question Content: Level 13 (Number Systems)
REPLACES the old Level 13 (Powers & Indices) content entirely -- Number
Systems is the genuine CBSE Class 9 chapter gap; Powers & Indices content
is superseded here rather than kept alongside it as a separate level.
CBSE Class 9 Number Systems chapter, full 14-sublevel treatment.

Design rules (v2, after feedback that questions felt repetitive and flat):
  - Every sheet's 20 questions ESCALATE in difficulty from Q1 to Q20 --
    no sheet is a flat block of "same template, random number" repeats.
  - Each question type has 3-5 distinct phrasings, cycled so consecutive
    questions never read identically even when testing the same skill.
Sheet 1=Intuition, Sheet 2=Concept, Sheet 3=Practice, Sheet 4=Mastery
"""
from content import cb, tb, q
import random
import math


# ═══ Escalation & variety helpers ═══
def _esc_ints(lo, hi, n, used=None):
    """n integers escalating from near lo to near hi, monotonic trend
    with light jitter, guaranteed distinct (retries on collision; widens
    the clamp range slightly if the requested span is too tight to fit
    n unique integers). If `used` is passed, also avoids repeating any
    integer already produced by an earlier call sharing that set."""
    if used is None:
        used = set()
    span = max(hi - lo, 1)
    if span + 1 < n:  # not enough integers in [lo,hi] for n unique picks
        hi = lo + n + max(2, n // 3)
        span = hi - lo
    jitter_amt = max(1, span // 10)
    vals = []
    for i in range(n):
        frac = i / max(n - 1, 1)
        center = lo + span * frac
        v = int(round(center + random.randint(-jitter_amt, jitter_amt)))
        v = max(lo, min(hi, v))
        tries = 0
        while v in used and tries < 40:
            v = v + 1 if v < hi else v - 1
            if v in used and v == (hi if tries % 2 else lo):
                v = random.randint(lo, hi)
            tries += 1
        used.add(v)
        vals.append(v)
    return vals


def _esc_pick(pool, n, used=None):
    """n items escalating through a sorted pool (by value), spread across
    its full range. Guarantees NO exact value repeats anywhere in the
    sequence as long as the pool has >= n unused values (raises the
    pool's effective size by falling back to any unused value if the
    local neighbourhood is exhausted). If `used` is passed (a set),
    picks are also excluded from -- and added to -- it, so multiple
    calls sharing the same `used` set never repeat a value across
    different question blocks in the same worksheet."""
    pool_sorted = sorted(set(pool))
    m = len(pool_sorted)
    if used is None:
        used = set()
    available = [v for v in pool_sorted if v not in used]
    out = []
    for i in range(n):
        if not available:
            # pool truly exhausted (n > total distinct values ever offered) --
            # only happens if a pool is far too small; reuse is the least-bad
            # fallback here, but this should be rare after pool expansion.
            available = [v for v in pool_sorted if v not in (set(out) - {out[-1] if out else None})] or pool_sorted
        idx = int(round(i / max(n - 1, 1) * (len(available) - 1)))
        idx = max(0, min(len(available) - 1, idx))
        # small jitter around the target index, but only among *available* values
        lo_idx = max(0, idx - 1)
        hi_idx = min(len(available) - 1, idx + 1)
        pick_idx = random.randint(lo_idx, hi_idx)
        choice = available.pop(pick_idx)
        used.add(choice)
        out.append(choice)
    return out


def _cycle(templates, i):
    return templates[i % len(templates)]


# ═══ Math helpers (all pure) ═══
def _gcd(a, b):
    return math.gcd(int(a), int(b))


def _terminates(den):
    d = abs(int(den))
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def _simplify_surd(n):
    n = int(n)
    best_k, best_rest = 1, n
    for k in range(int(math.isqrt(n)), 0, -1):
        if n % (k * k) == 0:
            best_k, best_rest = k, n // (k * k)
            break
    return best_k, best_rest


# ═══════════════════════════════════════════════════════════════════════════════
# 13A — Natural, Whole & Integers (classification + hierarchy + closure)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13A_s(sheet):
    random.seed(1300 + sheet)
    ranges = {1: (-8, 8), 2: (-20, 20), 3: (-60, 60), 4: (-150, 150)}
    lo, hi = ranges[sheet]
    items = [
        cb("Natural, Whole & Integer Numbers", [
            "N (Natural): 1, 2, 3, ...  W (Whole): 0, 1, 2, ...  Z (Integers): ..., -1, 0, 1, ...",
            "N \u2286 W \u2286 Z. CLOSED under an operation = result always stays in that set -- N isn't closed under subtraction (3-5=-2), Z is.",
        ], "-4 is an Integer only. 0 is Whole & Integer, not Natural. 7 is all three."),
    ]
    classify_templates = [
        "Classify {n}: Natural, Whole, Integer, or None of these?",
        "Which sets contain {n} -- Natural, Whole, and/or Integer?",
        "Is {n} a Natural number, a Whole number, an Integer, or none of these?",
        "Where does {n} sit in the N / W / Z hierarchy?",
    ]
    hierarchy_templates = [
        "True or False: every Natural number is also a Whole number.",
        "True or False: every Whole number is also an Integer.",
        "Give one number that is in Z but NOT in W.",
        "Give one number that is in W but NOT in N.",
    ]
    nums = _esc_ints(lo, hi, 8)
    for i, n in enumerate(nums):
        template = _cycle(classify_templates, i)
        text = template.format(n=n)
        if i % 3 == 0:
            memb = "natural" if n >= 1 else ("whole" if n == 0 else "integer")
            items.append(q(text, "diagram", "____", "", "number_hierarchy", {"number": str(n), "memberships": [memb]}))
        else:
            items.append(q(text, "fill", "Answer = ____"))
    ab_hi = max(8, (hi - lo) // 5)
    a_seq = _esc_ints(2, ab_hi, 8)
    b_seq = _esc_ints(2, ab_hi, 8)[::-1]  # reversed so a and b diverge instead of tracking together
    ab_pairs = [(a, b if b != a else b + 1) for a, b in zip(a_seq, b_seq)]
    ops_sets = [("N", "-"), ("W", "-"), ("Z", "-"), ("N", "\u00f7"), ("W", "\u00f7"), ("N", "+"), ("Z", "\u00d7"), ("W", "+")]
    closure_templates = [
        "Is {s} closed under \u201c{op}\u201d? Test with {a} {op} {b}.",
        "Test closure: does {s} stay closed when you compute {a} {op} {b}?",
        "{a} {op} {b} -- does the result stay inside {s}?",
    ]
    for i, (a, b) in enumerate(ab_pairs):
        s, op = ops_sets[i % len(ops_sets)]
        template = _cycle(closure_templates, i)
        text = template.format(s=s, op=op, a=a, b=b)
        if i % 2 == 0:
            items.append(q(text, "diagram", "____", "", "closure_test", {"a": a, "b": b, "op": op, "set_name": s}))
        else:
            items.append(q(text, "fill", "Answer = ____"))
    for i in range(4):
        items.append(q(_cycle(hierarchy_templates, i), "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 13B — Rational Numbers
# ═══════════════════════════════════════════════════════════════════════════════
def _L13B_s(sheet):
    random.seed(1310 + sheet)
    ranges = {1: (2, 10), 2: (2, 18), 3: (2, 35), 4: (2, 60)}
    lo, hi = ranges[sheet]
    items = [
        cb("Rational Numbers (Q)", [
            "A rational number is p/q, where p and q are integers and q \u2260 0.",
            "Every integer is rational (5 = 5/1). Two fractions are EQUIVALENT if they simplify to the same p/q.",
        ], "3/4 and 6/8 are equivalent -- both simplify to 3/4."),
    ]
    denoms = _esc_ints(lo, hi, 6)
    is_rational_templates = [
        "Is {p}/{q} a rational number? Why?",
        "Explain why {p}/{q} fits the definition of a rational number.",
        "Can {p}/{q} be written as an integer divided by a nonzero integer?",
    ]
    for i, den in enumerate(denoms):
        p = random.randint(1, den)
        items.append(q(_cycle(is_rational_templates, i).format(p=p, q=den), "fill", "Answer = ____"))
    equiv_templates = [
        "Is {pk}/{qk} equivalent to {p}/{q}?",
        "Do {p}/{q} and {pk}/{qk} represent the same rational number?",
        "Check: are {p}/{q} and {pk}/{qk} equivalent fractions?",
    ]
    base_pairs = list(zip(_esc_ints(1, max(3, lo), 5), _esc_ints(2, max(4, lo + 1), 5)))
    for i, (p, qd) in enumerate(base_pairs):
        k = random.randint(2, 5)
        items.append(q(_cycle(equiv_templates, i).format(p=p, q=qd, pk=p * k, qk=qd * k), "fill", "Answer = ____"))
    simplify_templates = [
        "Write {p}/{q} in simplest form.",
        "Reduce {p}/{q} to lowest terms.",
        "Simplify the fraction {p}/{q}.",
    ]
    gs = _esc_ints(2, max(4, lo), 5)
    for i, g in enumerate(gs):
        p, qd = g * random.randint(2, 9), g * random.randint(2, 9)
        while p == qd:
            qd = g * random.randint(2, 9)
        items.append(q(_cycle(simplify_templates, i).format(p=p, q=qd), "fill", "Answer = ____"))
    express_templates = [
        "Express the integer {n} as a rational number p/q.",
        "Write {n} in the form p/q.",
        "Show {n} as a fraction with denominator 1.",
    ]
    ints = _esc_ints(-hi, hi, 4)
    for i, n in enumerate(ints):
        items.append(q(_cycle(express_templates, i).format(n=n), "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 13C — Decimal Expansions (terminating vs recurring)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13C_s(sheet):
    random.seed(1320 + sheet)
    term_dens_by_tier = {1: [2, 4, 5], 2: [2, 4, 5, 8, 10], 3: [8, 10, 16, 20, 25], 4: [16, 20, 25, 40, 50]}
    other_primes_by_tier = {1: [3, 6], 2: [3, 6, 7, 9], 3: [7, 9, 11, 12], 4: [11, 12, 13, 15, 18, 22]}
    term_dens, other_primes = term_dens_by_tier[sheet], other_primes_by_tier[sheet]
    items = [
        cb("Predicting a Decimal Expansion", [
            "Write the fraction in lowest terms, then look at the denominator's prime factors.",
            "Only 2s and/or 5s -> TERMINATES. Any other prime (3, 7, 11...) -> RECURS.",
        ], "1/8: denominator 8=2x2x2 -> terminates (0.125). 1/3: denominator 3 -> recurs (0.333...)."),
    ]
    predict_templates = [
        "Will {num}/{den} terminate or recur? Check the denominator's prime factors.",
        "Predict the decimal expansion of {num}/{den} without dividing.",
        "Does {num}/{den} give a terminating or a recurring decimal?",
    ]
    mixed_dens = _esc_pick(term_dens + other_primes, 10)
    for i, den in enumerate(mixed_dens):
        num = random.randint(1, den - 1)
        g = _gcd(num, den)
        text = _cycle(predict_templates, i).format(num=num // g, den=den // g)
        if i % 2 == 0:
            items.append(q(text, "diagram", "____", "", "decimal_expansion", {"num": num // g, "den": den // g}))
        else:
            items.append(q(text, "fill", "Answer = ____"))
    den_only_templates = [
        "Without dividing: does a fraction with denominator {den} (lowest terms) terminate?",
        "A fraction has denominator {den} in lowest terms -- terminating or recurring?",
    ]
    for i, den in enumerate(_esc_pick(term_dens + other_primes, 5)):
        items.append(q(_cycle(den_only_templates, i).format(den=den), "fill", "Answer = ____"))
    for i, den in enumerate(_esc_pick(term_dens + other_primes, 5)):
        verdict = "terminates" if _terminates(den) else "recurs"
        shown = verdict if random.random() > 0.35 else ("recurs" if verdict == "terminates" else "terminates")
        items.append(q(f"True or False: a fraction with denominator {den} (lowest terms) {shown}.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 13CUM1 — Recurring decimal -> fraction
# ═══════════════════════════════════════════════════════════════════════════════
def _L13CUM1_s(sheet):
    random.seed(1330 + sheet)
    used = set()
    # difficulty here is genuinely driven by the period length and how many
    # digits are involved, not which digit -- so singles draw from the full
    # 1-9 pool at every tier, and doubles' pool widens with the sheet tier.
    singles = list(range(1, 10))
    doubles_by_tier = {
        1: [12, 18, 27, 36, 45, 54, 63, 72, 81, 9],
        2: [18, 27, 36, 45, 54, 63, 72, 81, 9, 90],
        3: [27, 36, 45, 54, 63, 72, 81, 9, 90, 18],
        4: [36, 45, 54, 63, 72, 81, 9, 18, 27, 90],
    }
    doubles = sorted(set(doubles_by_tier[sheet]))
    items = [
        cb("Converting a Recurring Decimal to a Fraction", [
            "Let x = the decimal. Multiply by 10^(period length) to shift one repeat past the point.",
            "Subtract the original x -- the repeating part cancels. Solve for x.",
        ], "x = 0.333...  ->  10x = 3.333...  ->  10x-x=3  ->  9x=3  ->  x=3/9=1/3."),
    ]
    single_templates = [
        "Convert 0.{d}{d}{d}... (recurring) to a fraction.",
        "Write 0.{d}{d}{d}... as a fraction in the form p/q.",
        "0.{d} recurring -- what fraction is this?",
    ]
    seq = _esc_pick(singles, 6, used=used)
    for i, d in enumerate(seq):
        text = _cycle(single_templates, i).format(d=d)
        if i % 3 == 0:
            items.append(q(text, "diagram", "____", "", "recurring_to_fraction", {"digits": str(d), "period_len": 1}))
        else:
            items.append(q(text, "fill", "Answer = ____"))
    double_templates = [
        "Convert 0.{d}{d}... (recurring) to a fraction.",
        "Write 0.{d} recurring as a fraction.",
        "0.{d}{d}... -- express this as p/q.",
    ]
    used_d = set()
    seq2 = _esc_pick(doubles, 8, used=used_d)
    for i, d in enumerate(seq2):
        dstr = f"{d:02d}"
        text = _cycle(double_templates, i).format(d=dstr)
        if i % 3 == 0:
            items.append(q(text, "diagram", "____", "", "recurring_to_fraction", {"digits": dstr, "period_len": 2}))
        else:
            items.append(q(text, "fill", "Answer = ____"))
    remaining_doubles = [d for d in doubles if d not in used_d]
    extra = _esc_pick(remaining_doubles if len(remaining_doubles) >= 6 else doubles, 6, used=set())
    for i, d in enumerate(extra):
        dstr = f"{d:02d}"
        items.append(q(f"Convert 0.{dstr} recurring to a fraction and simplify if possible.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 13D — Irrational Numbers
# ═══════════════════════════════════════════════════════════════════════════════
def _L13D_s(sheet):
    random.seed(1340 + sheet)
    perfect_by_tier = {1: [4, 9, 16, 25], 2: [9, 16, 25, 36, 49], 3: [25, 36, 49, 64, 81, 100], 4: [49, 64, 81, 100, 121, 144, 169]}
    non_perfect_by_tier = {
        1: [2, 3, 5, 6, 7, 8, 10, 11],
        2: [5, 6, 7, 8, 10, 11, 12, 13, 14, 15],
        3: [8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20],
        4: [12, 13, 15, 17, 18, 19, 20, 21, 22, 23, 26, 28],
    }
    perfect, non_perfect = perfect_by_tier[sheet], non_perfect_by_tier[sheet]
    used = set()
    items = [
        cb("Irrational Numbers", [
            "An irrational number cannot be written as p/q -- its decimal never terminates or repeats.",
            "\u221an is irrational whenever n is NOT a perfect square. \u221a4=2 is rational; \u221a5 is irrational.",
        ], "\u221a16 = 4 -> rational. \u221a17 -> irrational (17 isn't a perfect square)."),
    ]
    templates = [
        "Is \u221a{n} rational or irrational?",
        "Classify \u221a{n}: rational or irrational?",
        "Rational or irrational -- \u221a{n}?",
    ]
    mixed = _esc_pick(perfect + non_perfect, 12, used=used)
    for i, n in enumerate(mixed):
        text = _cycle(templates, i).format(n=n)
        if i % 3 == 0:
            memb = "natural" if math.isqrt(n) ** 2 == n else "irrational"
            label = f"\u221a{n} = {math.isqrt(n)}" if memb == "natural" else f"\u221a{n}"
            items.append(q(text, "diagram", "____", "", "number_hierarchy", {"number": label, "memberships": [memb]}))
        else:
            items.append(q(text, "fill", "Answer = ____"))
    items.append(q("True or False: 22/7 is exactly equal to \u03c0 (not just an approximation).", "fill", "Answer = ____"))
    items.append(q("True or False: every square root is irrational.", "fill", "Answer = ____"))
    explain_templates = [
        "Explain in one sentence why \u221a{n} is irrational.",
        "In your own words, why can't \u221a{n} be written as a fraction?",
    ]
    remaining_np = [n for n in non_perfect if n not in used]
    for i, n in enumerate(_esc_pick(remaining_np if len(remaining_np) >= 3 else non_perfect, 3, used=set())):
        items.append(q(_cycle(explain_templates, i).format(n=n), "fill", "Answer = ____"))
    items.append(q("Give an example of an irrational number that is NOT a square root.", "fill", "Answer = ____"))
    items.append(q("Is the sum of a rational and an irrational number (e.g. 2 + \u221a3) rational or irrational?", "fill", "Answer = ____"))
    items.append(q("Is the product of a nonzero rational and an irrational number (e.g. 3 x \u221a2) rational or irrational?", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 13E — The Real Number Line (successive magnification)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13E_s(sheet):
    random.seed(1350 + sheet)
    non_perfect_by_tier = {
        1: [2, 3, 5, 6, 7, 8, 10, 11, 12, 13],
        2: [5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17],
        3: [10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21],
        4: [14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 26, 28],
    }
    non_perfect = non_perfect_by_tier[sheet]
    items = [
        cb("The Real Number Line", [
            "Every point on the number line is exactly one real number -- rational or irrational.",
            "Locate an irrational (like \u221a2) between two consecutive integers, then zoom in decimal by decimal -- SUCCESSIVE MAGNIFICATION.",
        ], "\u221a2 \u2248 1.414: between 1 and 2, then 1.4 and 1.5, then 1.41 and 1.42..."),
    ]
    int_templates = [
        "Between which two consecutive integers does \u221a{n} lie?",
        "\u221a{n} falls between which pair of whole numbers?",
        "Name the two consecutive integers that \u221a{n} lies between.",
    ]
    seq = _esc_pick(non_perfect, 8, used=set())
    for i, n in enumerate(seq):
        items.append(q(_cycle(int_templates, i).format(n=n), "fill", "Answer = ____"))
    zoom_templates = [
        "\u221a{n} is between {lo1:.1f} and {hi1:.1f}. Narrow it to one more decimal place.",
        "Zoom in on \u221a{n}: it's between {lo1:.1f} and {hi1:.1f} -- which two values (2 d.p.) is it between?",
    ]
    seq2 = _esc_pick(non_perfect, 8, used=set())
    for i, n in enumerate(seq2):
        val = math.sqrt(n)
        lo1 = math.floor(val * 10) / 10
        hi1 = lo1 + 0.1
        items.append(q(_cycle(zoom_templates, i).format(n=n, lo1=lo1, hi1=hi1), "fill", "Answer = ____"))
    items.append(q("True or False: every point on the number line is a rational number.", "fill", "Answer = ____"))
    items.append(q("True or False: between any two rational numbers there is always another rational number.", "fill", "Answer = ____"))
    items.append(q("True or False: irrational numbers have their own separate number line.", "fill", "Answer = ____"))
    items.append(q("True or False: successive magnification narrows down an irrational number's location one decimal place at a time.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 13CUM2 — Review B-E (Rational, Decimals, Irrational, Real Line)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13CUM2_s(sheet):
    random.seed(1360 + sheet)
    perfect_by_tier = {1: [4, 9, 16], 2: [9, 16, 25, 36], 3: [25, 36, 49, 64], 4: [36, 49, 64, 81]}
    non_perfect_by_tier = {1: [2, 3, 5, 6, 7], 2: [5, 6, 7, 8, 10], 3: [7, 10, 11, 12, 13], 4: [10, 12, 13, 15, 17]}
    term_dens_by_tier = {1: [2, 4, 5, 8], 2: [4, 5, 8, 10, 16], 3: [8, 10, 20, 25], 4: [10, 20, 25, 40]}
    other_primes_by_tier = {1: [3, 6, 7, 9], 2: [6, 7, 9, 11], 3: [9, 11, 12, 13], 4: [9, 11, 12, 13, 18]}
    perfect, non_perfect = perfect_by_tier[sheet], non_perfect_by_tier[sheet]
    term_dens, other_primes = term_dens_by_tier[sheet], other_primes_by_tier[sheet]
    items = [
        cb("Review: Rationals, Decimals, Irrationals, the Real Line", [
            "Rational = p/q form, terminating or recurring decimal. Irrational = never terminates, never repeats.",
            "\u221an is irrational unless n is a perfect square. Rationals + irrationals together = the REAL numbers.",
        ], ""),
    ]
    rat_templates = ["Is {p}/{q} rational?", "Does {p}/{q} fit the definition of a rational number?"]
    for i, qd in enumerate(_esc_ints(2, 12, 5)):
        p = random.randint(1, qd)
        items.append(q(_cycle(rat_templates, i).format(p=p, q=qd), "fill", "Answer = ____"))
    dec_templates = ["Denominator {den} (lowest terms) -- terminates or recurs?", "A fraction with denominator {den}: terminating or recurring decimal?"]
    for i, den in enumerate(_esc_pick(term_dens + other_primes, 5, used=set())):
        items.append(q(_cycle(dec_templates, i).format(den=den), "fill", "Answer = ____"))
    irr_templates = ["Is \u221a{n} rational or irrational?", "Classify \u221a{n}."]
    irr_used = set()
    for i, n in enumerate(_esc_pick(perfect + non_perfect, 5, used=irr_used)):
        items.append(q(_cycle(irr_templates, i).format(n=n), "fill", "Answer = ____"))
    line_templates = ["Between which two consecutive integers does \u221a{n} lie?", "\u221a{n} falls between which whole numbers?"]
    remaining_np = [n for n in non_perfect if n not in irr_used]
    for i, n in enumerate(_esc_pick(remaining_np if len(remaining_np) >= 5 else non_perfect, 5, used=set())):
        items.append(q(_cycle(line_templates, i).format(n=n), "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 13F — Surds — Simplifying
# ═══════════════════════════════════════════════════════════════════════════════
def _L13F_s(sheet):
    random.seed(1370 + sheet)
    # generate genuine simplifiable surds (n = k^2 * m, k>=2) within each
    # tier's magnitude band -- programmatic, so there's always enough
    # unique values (small fixed lists ran out after ~5-7 items).
    bands = {1: (8, 75), 2: (18, 100), 3: (40, 150), 4: (60, 250)}
    band_lo, band_hi = bands[sheet]
    pool = sorted({k * k * m for k in range(2, 8) for m in (2, 3, 5, 6, 7, 10, 11, 13)
                   if band_lo <= k * k * m <= band_hi})
    used = set()
    items = [
        cb("Simplifying Surds", [
            "\u221an is in SIMPLEST FORM when n has no perfect-square factor left (other than 1).",
            "To simplify: find the largest perfect square dividing n, split \u221an = \u221a(k\u00b2\u00d7m) = k\u221am.",
        ], "\u221a72 = \u221a(36\u00d72) = 6\u221a2."),
    ]
    simp_templates = ["Simplify \u221a{n} to simplest form.", "Reduce \u221a{n} to its simplest surd form.", "Write \u221a{n} in the form k\u221am."]
    seq = _esc_pick(pool, 12, used=used)
    for i, n in enumerate(seq):
        text = _cycle(simp_templates, i).format(n=n)
        if i % 2 == 0:
            items.append(q(text, "diagram", "____", "", "surd_simplify_tree", {"n": n}))
        else:
            items.append(q(text, "fill", "Answer = ____"))
    check_templates = ["Is \u221a{n} already in simplest form? If not, simplify it.", "Can \u221a{n} be simplified further? Show the result."]
    for i, n in enumerate(_esc_pick(pool, 4, used=used)):
        items.append(q(_cycle(check_templates, i).format(n=n), "fill", "Answer = ____"))
    coeff_templates = ["Simplify {a}\u221a{n} (combine the outside coefficient with the simplified surd).", "{a}\u221a{n} -- simplify fully."]
    for i, n in enumerate(_esc_pick(pool, 4, used=used)):
        a = random.randint(2, 6)
        items.append(q(_cycle(coeff_templates, i).format(a=a, n=n), "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 13G — Rationalising the Denominator (single term)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13G_s(sheet):
    random.seed(1380 + sheet)
    ranges = {
        1: [2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15],
        2: [3, 5, 6, 7, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20],
        3: [6, 7, 10, 11, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23],
        4: [10, 11, 13, 15, 17, 18, 19, 20, 21, 22, 23, 26, 28, 30],
    }
    pool = ranges[sheet]
    used = set()
    items = [
        cb("Rationalising a Single-Term Surd Denominator", [
            "1/\u221an has an irrational denominator -- not allowed in simplest form.",
            "Multiply top AND bottom by \u221an: 1/\u221an \u00d7 \u221an/\u221an = \u221an/n.",
        ], "1/\u221a5 = \u221a5/5."),
    ]
    single_templates = ["Rationalise the denominator: 1/\u221a{n}", "Remove the surd from the denominator of 1/\u221a{n}.", "Rationalise: 1/\u221a{n} = ?"]
    seq = _esc_pick(pool, 10, used=used)
    for i, n in enumerate(seq):
        text = _cycle(single_templates, i).format(n=n)
        if i % 2 == 0:
            items.append(q(text, "diagram", "____", "", "rationalize_steps", {"kind": "single", "b": n}))
        else:
            items.append(q(text + " = ____", "fill", "Answer = ____"))
    coeff_templates = ["Rationalise the denominator: {c}/\u221a{n}", "Simplify {c}/\u221a{n} with a rational denominator."]
    for i, n in enumerate(_esc_pick(pool, 6, used=used)):
        c = random.randint(2, 9)
        items.append(q(_cycle(coeff_templates, i).format(c=c, n=n) + " = ____", "fill", "Answer = ____"))
    for i, n in enumerate(_esc_pick(pool, 4, used=used)):
        items.append(q(f"What must you multiply 1/\u221a{n} by (top and bottom) to rationalise it?", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 13H — Rationalising the Denominator (binomial / conjugate)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13H_s(sheet):
    random.seed(1390 + sheet)
    a_range = {1: (1, 4), 2: (2, 5), 3: (2, 7), 4: (3, 9)}
    c_pool_by_tier = {1: [2, 3, 5, 6, 7], 2: [2, 3, 5, 6, 7, 10, 11], 3: [3, 5, 6, 7, 10, 11, 13], 4: [5, 6, 7, 10, 11, 13, 15, 17]}
    alo, ahi = a_range[sheet]
    c_pool = c_pool_by_tier[sheet]
    items = [
        cb("Rationalising with a Conjugate", [
            "For a denominator like (a+\u221ac), multiply top and bottom by its CONJUGATE (a-\u221ac).",
            "(a+\u221ac)(a-\u221ac) = a\u00b2-c -- the surd disappears from the denominator.",
        ], "1/(2+\u221a3): multiply by (2-\u221a3)/(2-\u221a3) -> (2-\u221a3)/(4-3) = 2-\u221a3."),
    ]
    all_pairs = [(a, c) for a in range(alo, ahi + 1) for c in c_pool if a * a != c]
    random.shuffle(all_pairs)
    used_pairs = set()

    def _ac_pairs(n):
        out = []
        pool_left = [p for p in all_pairs if p not in used_pairs]
        for _ in range(n):
            if not pool_left:
                pool_left = [p for p in all_pairs if p not in used_pairs] or all_pairs
            pair = pool_left.pop(0)
            used_pairs.add(pair)
            out.append(pair)
        out.sort(key=lambda p: p[0] + p[1] / 20)  # roughly escalating
        return out

    rat_templates = ["Rationalise the denominator: 1/({a}+\u221a{c})", "Remove the surd from the denominator of 1/({a}+\u221a{c})."]
    for i, (a, c) in enumerate(_ac_pairs(10)):
        text = _cycle(rat_templates, i).format(a=a, c=c)
        if i % 2 == 0:
            items.append(q(text, "diagram", "____", "", "rationalize_steps", {"kind": "binomial", "a": a, "c": c}))
        else:
            items.append(q(text + " = ____", "fill", "Answer = ____"))
    conj_templates = ["What is the conjugate of ({a}+\u221a{c})?", "Name the conjugate of the expression ({a}+\u221a{c})."]
    for i, (a, c) in enumerate(_ac_pairs(5)):
        items.append(q(_cycle(conj_templates, i).format(a=a, c=c), "fill", "Answer = ____"))
    for i, (a, c) in enumerate(_ac_pairs(5)):
        items.append(q(f"({a}+\u221a{c})({a}-\u221a{c}) = ____ (the surd should vanish -- simplify)", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 13CUM3 — Mixed review: Surds & Rationalising (F/G/H)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13CUM3_s(sheet):
    random.seed(1400 + sheet)
    bands = {1: (8, 60), 2: (18, 100), 3: (27, 150), 4: (45, 200)}
    band_lo, band_hi = bands[sheet]
    surd_pool = sorted({k * k * m for k in range(2, 7) for m in (2, 3, 5, 6, 7, 10, 11)
                         if band_lo <= k * k * m <= band_hi})
    single_by_tier = {1: [2, 3, 5, 6, 7], 2: [3, 5, 6, 7, 10, 11], 3: [5, 6, 7, 10, 11, 13, 15], 4: [7, 10, 11, 13, 15, 17, 19]}
    single_pool = single_by_tier[sheet]
    surd_used = set()
    items = [
        cb("Review: Surds & Rationalising", [
            "Simplify a surd by pulling out the largest perfect-square factor.",
            "Rationalise: single-term denominators using that surd; binomial denominators using the conjugate.",
        ], ""),
    ]
    simp_templates = ["Simplify \u221a{n}.", "Reduce \u221a{n} to simplest surd form."]
    for i, n in enumerate(_esc_pick(surd_pool, 6, used=surd_used)):
        items.append(q(_cycle(simp_templates, i).format(n=n), "fill", "Answer = ____"))
    rat_templates = ["Rationalise: 1/\u221a{n}", "Remove the surd from 1/\u221a{n}"]
    for i, n in enumerate(_esc_pick(single_pool, 6, used=set())):
        items.append(q(_cycle(rat_templates, i).format(n=n) + " = ____", "fill", "Answer = ____"))
    binom_pairs = [(a, c) for a in range(2, 7) for c in (2, 3, 5, 6, 7) if a * a != c]
    random.shuffle(binom_pairs)
    for i, (a, c) in enumerate(binom_pairs[:4]):
        items.append(q(f"Rationalise: 1/({a}+\u221a{c}) = ____", "fill", "Answer = ____"))
    remaining_surds = [n for n in surd_pool if n not in surd_used]
    for i, n in enumerate(_esc_pick(remaining_surds if len(remaining_surds) >= 4 else surd_pool, 4, used=set())):
        items.append(q(f"True or False: \u221a{n} is already in simplest form.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 13I — Laws of Exponents for Real Numbers
# ═══════════════════════════════════════════════════════════════════════════════
def _L13I_s(sheet):
    random.seed(1410 + sheet)
    base_by_tier = {1: [2, 3], 2: [2, 3, 5], 3: [2, 3, 4, 5], 4: [2, 3, 5, 7, 10]}
    bases = base_by_tier[sheet]
    items = [
        cb("Laws of Exponents for Real Numbers", [
            "These laws work for ANY real base and ANY real exponent (including fractions):",
            "a^m\u00d7a^n=a^(m+n)   a^m\u00f7a^n=a^(m-n)   (a^m)^n=a^(mn)   a^(1/n)=\u207f\u221aa",
        ], "a^(1/2) means \u221aa. So 9^(1/2) = \u221a9 = 3."),
    ]
    mult_templates = ["Simplify: {a}^{m} \u00d7 {a}^{n} = {a}^____", "Combine: {a}^{m} times {a}^{n}, as a single power of {a}."]
    for i in range(5):
        a = bases[i % len(bases)]
        m, n = 2 + i, 2 + (i + 1) % 4
        items.append(q(_cycle(mult_templates, i).format(a=a, m=m, n=n), "fill", "Answer = ____"))
    div_templates = ["Simplify: {a}^{m} \u00f7 {a}^{n} = {a}^____", "Divide: {a}^{m} by {a}^{n}, as a single power of {a}."]
    for i in range(5):
        a = bases[i % len(bases)]
        m, n = 5 + i, 1 + i % 3
        items.append(q(_cycle(div_templates, i).format(a=a, m=m, n=n), "fill", "Answer = ____"))
    pow_templates = ["Simplify: ({a}^{m})^{n} = {a}^____", "Raise a power to a power: ({a}^{m})^{n}, as a single power of {a}."]
    for i in range(5):
        a = bases[i % len(bases)]
        m, n = 2 + i % 3, 2 + i % 2
        items.append(q(_cycle(pow_templates, i).format(a=a, m=m, n=n), "fill", "Answer = ____"))
    root_bases = [4, 9, 16, 25, 8, 27, 64, 32]
    root_templates = ["Evaluate: {a}^(1/{n}) = ____", "Find the value of {a} raised to the power 1/{n}."]
    for i, a in enumerate(_esc_pick(root_bases, 5)):
        n = 2 if a in (4, 9, 16, 25, 64) else (3 if a in (8, 27) else 5)
        items.append(q(_cycle(root_templates, i).format(a=a, n=n), "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 13J — Word Problems
# ═══════════════════════════════════════════════════════════════════════════════
def _L13J_s(sheet):
    random.seed(1420 + sheet)
    side_range = {1: (2, 8), 2: (5, 15), 3: (8, 25), 4: (15, 40)}
    lo, hi = side_range[sheet]
    items = [
        cb("Number Systems in the Real World", [
            "A square of side s has diagonal s\u221a2 -- almost always irrational.",
            "Correctly classifying a number (rational vs irrational) matters for how precisely you can measure or represent it.",
        ], "A square field of side 5m has diagonal 5\u221a2 m \u2248 7.07m -- an irrational length."),
    ]
    diag_templates = [
        "A square has side {s}m. Its diagonal is {s}\u221a2 m. Is this length rational or irrational?",
        "A square field of side {s}m has a diagonal path of length {s}\u221a2 m. Rational or irrational?",
    ]
    for i, s in enumerate(_esc_ints(lo, hi, 5)):
        items.append(q(_cycle(diag_templates, i).format(s=s), "fill", "Answer = ____"))
    recipe_templates = [
        "A recipe needs {num}/{den} of a cup of flour. Will the decimal amount terminate or recur?",
        "A container holds {num}/{den} litres. Terminating or recurring decimal?",
    ]
    for i in range(5):
        num = random.randint(1, 9)
        den = [3, 6, 7, 9, 11][i % 5]
        items.append(q(_cycle(recipe_templates, i).format(num=num, den=den), "fill", "Answer = ____"))
    circle_templates = [
        "A circle has radius {r}cm. Its circumference is 2\u03c0{r}cm. Is \u03c0 (and so the circumference) rational or irrational?",
        "A wheel of radius {r}cm rolls once -- distance covered is 2\u03c0{r}cm. Rational or irrational?",
    ]
    for i, r in enumerate(_esc_ints(2, hi, 5)):
        items.append(q(_cycle(circle_templates, i).format(r=r), "fill", "Answer = ____"))
    approx_templates = [
        "A student says \u221a{n} \u2248 {v} is the EXACT value. Is the student correct? Explain.",
        "True or False: rounding \u221a{n} to {v} gives its exact value.",
    ]
    for i, n in enumerate([2, 3, 5, 6, 7]):
        v = round(math.sqrt(n), 2)
        items.append(q(_cycle(approx_templates, i).format(n=n, v=v), "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 13REV — Level 13 Revision (mixed across all sublevels)
# ═══════════════════════════════════════════════════════════════════════════════
def _L13REV_s(sheet):
    random.seed(1430 + sheet)
    lo_hi = {1: 15, 2: 25, 3: 40, 4: 60}[sheet]
    perfect = [4, 9, 16, 25, 36, 49]
    non_perfect = [2, 3, 5, 6, 7, 10, 11, 12, 13, 15]
    surd_pool = [8, 12, 18, 20, 24, 27, 32, 45, 48, 50]
    term_dens = [2, 4, 5, 8, 10, 20]
    other_primes = [3, 6, 7, 9, 11]
    items = [
        cb("Level 13 Revision — Number Systems", [
            "N \u2286 W \u2286 Z \u2286 Q \u2286 R. Denominator only 2s/5s -> terminates, otherwise recurs.",
            "Simplify surds via perfect-square factors; rationalise using the surd itself (single) or its conjugate (binomial).",
        ], ""),
    ]
    for i, n in enumerate(_esc_ints(-lo_hi, lo_hi, 3)):
        items.append(q(f"Classify {n}: Natural, Whole, Integer, or None of these?", "fill", "Answer = ____"))
    ops = ["+", "-", "\u00d7"]
    a_seq_rev = _esc_ints(2, 10, 3)
    b_seq_rev = _esc_ints(2, 10, 3)[::-1]
    ab_pairs_rev = [(a, b if b != a else b + 1) for a, b in zip(a_seq_rev, b_seq_rev)]
    for i, (a, b) in enumerate(ab_pairs_rev):
        s = ["N", "W", "Z"][i % 3]
        items.append(q(f"Is {s} closed under \u201c{ops[i%3]}\u201d? Test with {a} {ops[i%3]} {b}.", "fill", "Answer = ____"))
    for i, den in enumerate(_esc_pick(term_dens + other_primes, 3)):
        items.append(q(f"Denominator {den} (lowest terms): terminating or recurring decimal?", "fill", "Answer = ____"))
    for i, n in enumerate(_esc_pick(perfect + non_perfect, 3)):
        items.append(q(f"Is \u221a{n} rational or irrational?", "fill", "Answer = ____"))
    for i, n in enumerate(_esc_pick(surd_pool, 3)):
        items.append(q(f"Simplify \u221a{n}.", "fill", "Answer = ____"))
    for i, n in enumerate([2, 3, 5]):
        items.append(q(f"Rationalise: 1/\u221a{n} = ____", "fill", "Answer = ____"))
    for i in range(2):
        a = [2, 3, 5][i % 3]
        m, n = 2 + i, 3 + i
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
