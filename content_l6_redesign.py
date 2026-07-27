"""
Fear Less Maths — LEVEL 6 (Factors, Multiples, HCF & LCM)
v2 REWRITE (2026-07-20) — five improvements applied uniformly:
  1. Diagram cap: only the first 2 questions per sheet get a WORKED
     diagram, the next 4 get a BLANK scaffold, the remaining 14 are
     plain text questions -- no diagram fatigue from 20x the same visual.
  2. Question-type mix per 20-question sheet: 10 computation,
     4 word problems, 3 reverse-thinking, 2 error-spotting, 1 True/False
     (was ~14 computation + ~3 True/False with almost no reverse/error).
  3. Reverse-thinking questions ("HCF of two numbers is 6, one is 24,
     what could the other be?") and error-spotting questions ("A
     student says HCF(12,18)=36 -- what did they mix up?") are new
     question shapes this level never asked before.
  4. Escalation fixed to rise monotonically tier 1->4 (mean operand
     size, not just the max).
  5. 6J (Mastery) is now genuinely the hardest sheet -- multi-step and
     word-problem heavy, not simpler drill than the sublevels before it.
"""
import random
import math
import re as _l6_re
from content import cb, tb, q


# ═══ Math helpers ═══
def _l6_hcf(a, b):
    while b:
        a, b = b, a % b
    return a


def _l6_lcm(a, b):
    return a * b // _l6_hcf(a, b)


def _l6_is_prime(n):
    if n < 2:
        return False
    for k in range(2, int(n ** 0.5) + 1):
        if n % k == 0:
            return False
    return True


def _l6_factors_of(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def _l6_prime_factors_multiset(n):
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


# ═══ Diagram-cap emitter: first 2 worked, next 4 blank, rest plain ═══
class _Sheet:
    """Accumulates up to 20 items for one worksheet. Diagrams cap at 12
    (2 worked + 10 blank) -- high density is good for this level, the
    earlier cap of 6 was overcorrecting; diagrams only get dropped to
    plain text past 12 so a sheet doesn't return to 20/20 diagram
    fatigue on sublevels with lots of diagram-eligible questions."""
    def __init__(self):
        self.items = []
        self.diagram_count = 0

    def add(self, text, ans="Answer = ____", qtype="fill", dtype=None, dparams=None):
        if dtype is not None and self.diagram_count < 12:
            blank = self.diagram_count >= 2
            params = dict(dparams or {})
            params["blank"] = blank
            self.items.append(q(text, "diagram", ans, "", dtype, params))
            self.diagram_count += 1
        else:
            self.items.append(q(text, qtype, ans))

    def extend_concept(self, concept_items):
        self.items = list(concept_items) + self.items

    def result(self):
        return self.items


def _esc_pick(pool, n, used=None):
    """n items escalating through a sorted pool, spread across its full
    range, guaranteed no repeats as long as pool has >= n unused values."""
    pool_sorted = sorted(set(pool))
    if used is None:
        used = set()
    available = [v for v in pool_sorted if v not in used]
    out = []
    for i in range(n):
        if not available:
            available = [v for v in pool_sorted if v not in set(out)] or pool_sorted
        idx = int(round(i / max(n - 1, 1) * (len(available) - 1)))
        idx = max(0, min(len(available) - 1, idx))
        lo_idx, hi_idx = max(0, idx - 1), min(len(available) - 1, idx + 1)
        pick_idx = random.randint(lo_idx, hi_idx)
        choice = available.pop(pick_idx)
        used.add(choice)
        out.append(choice)
    return out


def _pair_pool(lo, hi, n):
    """n distinct (a,b) pairs with a<b, both in [lo,hi], escalating in size."""
    pairs = []
    seen = set()
    tries = 0
    while len(pairs) < n and tries < n * 40:
        tries += 1
        frac = len(pairs) / max(n - 1, 1)
        center = lo + (hi - lo) * frac
        a = max(lo, int(random.gauss(center, (hi - lo) * 0.12)))
        b = max(lo, int(random.gauss(center * 1.3, (hi - lo) * 0.15)))
        a, b = min(a, hi), min(b, hi)
        if a == b:
            b += random.choice([-2, 2])
        a, b = sorted((max(lo, a), max(lo, b)))
        if a == b or (a, b) in seen:
            continue
        seen.add((a, b))
        pairs.append((a, b))
    pairs.sort(key=lambda p: p[0] + p[1])
    return pairs


# ═══════════════════════════════════════════════════════════════════════════════
# 6A — Factors
# ═══════════════════════════════════════════════════════════════════════════════
def _L6A_s(sheet):
    random.seed(600 + sheet)
    ranges = {1: (8, 30), 2: (16, 48), 3: (24, 72), 4: (36, 100)}
    lo, hi = ranges[sheet]
    S = _Sheet()
    S.extend_concept([
        cb("Factors", [
            "A factor of a number divides it EXACTLY, with no remainder.",
            "Every number has 1 and itself as factors.",
        ], "Factors of 12: 1, 2, 3, 4, 6, 12."),
    ])
    comp_pool = _esc_pick(range(lo, hi), 10)
    for i, n in enumerate(comp_pool):
        if i < 10:
            S.add(f"List ALL factors of {n}.", "Answer = ____", dtype="factor_array", dparams={"n": n})
        else:
            S.add(f"List ALL factors of {n}.", "Answer = ____")
    for n in _esc_pick(range(lo, hi), 4, used=set()):
        ctx = random.choice([
            f"A gardener has {n} plants to place in equal rows with no leftovers. List every row-size that works.",
            f"{n} sweets are shared equally among some friends with none left over. List every possible number of friends.",
        ])
        S.add(ctx, "Answer = ____", "word")
    for _ in range(3):
        n = random.randint(lo, hi)
        d = random.choice(_l6_factors_of(n))
        wrong = d + random.choice([1, -1, 2])
        S.add(f"{n} has a factor that is one of: {d}, {wrong}. Which one is the TRUE factor, and why does the other one fail?", "Answer = ____", "word")
    for _ in range(2):
        n = random.randint(lo, hi)
        fake_factor = random.choice([n + 1, n - 1] + [d for d in range(2, 12) if n % d != 0])
        S.add(f"A student says {fake_factor} is a factor of {n}. Check by dividing -- are they right? If not, what's the remainder?", "Answer = ____", "word")
    n = random.randint(lo, hi)
    claim = random.choice([True, False])
    if claim:
        d = random.choice(_l6_factors_of(n))
        S.add(f"True or False: {d} is a factor of {n}.", "Answer = ____")
    else:
        d = n + random.choice([1, 3])
        S.add(f"True or False: {d} is a factor of {n}.", "Answer = ____")
    return S.result()


# ═══════════════════════════════════════════════════════════════════════════════
# 6B — Multiples
# ═══════════════════════════════════════════════════════════════════════════════
def _L6B_s(sheet):
    random.seed(610 + sheet)
    ranges = {1: (2, 9), 2: (4, 12), 3: (6, 15), 4: (8, 20)}
    lo, hi = ranges[sheet]
    S = _Sheet()
    S.extend_concept([
        cb("Multiples", [
            "A multiple of a number is what you get multiplying it by 1, 2, 3...",
            "Multiples never stop -- there's always a bigger one.",
        ], "Multiples of 4: 4, 8, 12, 16, 20..."),
    ])
    for i, n in enumerate(_esc_pick(range(lo, hi), 6)):
        which = random.randint(4, 9)
        text = f"What is the {which}th multiple of {n}?"
        if i < 6:
            S.add(text, "Answer = ____", dtype="multiples_number_line", dparams={"n": n, "count": which + 1})
        else:
            S.add(text, "Answer = ____")
    for n in _esc_pick(range(lo, hi), 4, used=set()):
        S.add(f"List the first 5 multiples of {n}.", "Answer = ____")
    used_b = set()
    for n in _esc_pick(range(lo, hi), 4, used=used_b):
        target = n * random.randint(4, 9) + random.choice([1, -1, 2])
        S.add(f"A bus arrives every {n} minutes starting at 0. Could it arrive at exactly the {target} minute mark? Explain.", "Answer = ____", "word")
    for n in _esc_pick(range(lo, hi), 5, used=used_b):
        candidate = n * random.randint(3, 8)
        off = random.choice([0, 0, 1, -1])
        shown = candidate + off
        S.add(f"A student says {shown} is a multiple of {n}. Check it -- are they right?", "Answer = ____", "word")
    n = random.randint(lo, hi)
    S.add(f"True or False: every multiple of {n} is bigger than {n} itself.", "Answer = ____")
    return S.result()


# ═══════════════════════════════════════════════════════════════════════════════
# 6C — Prime Factorisation
# ═══════════════════════════════════════════════════════════════════════════════
def _L6C_s(sheet):
    random.seed(620 + sheet)
    ranges = {1: (12, 40), 2: (24, 60), 3: (36, 90), 4: (48, 120)}
    lo, hi = ranges[sheet]
    S = _Sheet()
    S.extend_concept([
        cb("Prime Factorisation", [
            "Every number breaks down into a unique product of PRIME factors.",
            "Keep dividing by the smallest prime that fits, until you reach 1.",
        ], "60 = 2 x 2 x 3 x 5."),
    ])
    for i, n in enumerate(_esc_pick(range(lo, hi), 6)):
        text = f"Write the prime factorisation of {n}."
        if i < 6:
            S.add(text, "Answer = ____", dtype="factor_tree", dparams={"n": n})
        else:
            S.add(text, "Answer = ____")
    for n in _esc_pick(range(lo, hi), 4, used=set()):
        S.add(f"How many prime factors does {n} have, counting repeats?", "Answer = ____")
    for _ in range(4):
        n = random.randint(lo, hi)
        pf = _l6_prime_factors_multiset(n)
        missing = random.choice(pf)
        shown = [str(p) for p in pf]
        shown[pf.index(missing)] = "?"
        S.add(f"{n} = {' x '.join(shown)}. What is the missing prime factor?", "Answer = ____", "word")
    for _ in range(5):
        n = random.randint(lo, hi)
        pf = sorted(_l6_prime_factors_multiset(n))
        wrong = pf.copy()
        idx = random.randrange(len(wrong))
        wrong[idx] = wrong[idx] + 1
        S.add(f"A student factorises {n} as {' x '.join(str(p) for p in wrong)}. One factor isn't prime, or the product is wrong -- find the mistake.", "Answer = ____", "word")
    n = random.randint(lo, hi)
    S.add(f"True or False: {n} has exactly one way to be written as a product of primes (ignoring order).", "Answer = ____")
    return S.result()


# ═══════════════════════════════════════════════════════════════════════════════
# 6D — HCF
# ═══════════════════════════════════════════════════════════════════════════════
def _L6D_s(sheet):
    random.seed(630 + sheet)
    ranges = {1: (8, 40), 2: (20, 80), 3: (40, 150), 4: (80, 300)}
    lo, hi = ranges[sheet]
    pairs = _pair_pool(lo, hi, 20)
    S = _Sheet()
    S.extend_concept([
        cb("HCF — Highest Common Factor", [
            "HCF = the BIGGEST factor shared by numbers.",
            "List factors of each, find common ones, take the biggest.",
        ], "HCF(8,12) = 4."),
    ])
    for i, (a, b) in enumerate(pairs[:10]):
        text = f"HCF({a}, {b}) = ____"
        if i < 10:
            S.add(text, "", dtype="ladder_division", dparams={"a": a, "b": b, "mode": "hcf"})
        else:
            S.add(text, "Answer = ____")
    for a, b in pairs[10:14]:
        S.add(f"Two ropes are {a}m and {b}m. Cut both into equal-length pieces with none left over. What's the longest piece length possible?", "Answer = ____", "word")
    used_hd = set()
    for _ in range(3):
        h = random.choice([4, 6, 8, 9, 12])
        a = h * random.randint(2, 6)
        tries = 0
        while (h, a) in used_hd and tries < 10:
            a = h * random.randint(2, 6)
            tries += 1
        used_hd.add((h, a))
        S.add(f"The HCF of two numbers is {h}. One of the numbers is {a}. Give ONE possibility for the other number.", "Answer = ____", "word")
    used_d2 = set()
    for _ in range(2):
        remaining = [p for p in pairs if p not in used_d2] or pairs
        a, b = random.choice(remaining)
        used_d2.add((a, b))
        real_hcf = _l6_hcf(a, b)
        wrong = real_hcf * random.choice([2, 3])
        S.add(f"A student says HCF({a},{b}) = {wrong}. Check: does {wrong} actually divide both numbers? What's the real HCF?", "Answer = ____", "word")
    a, b = random.choice(pairs)
    S.add(f"True or False: HCF({a},{b}) is always less than or equal to both {a} and {b}.", "Answer = ____")
    return S.result()


# ═══════════════════════════════════════════════════════════════════════════════
# 6CUM1 — Factor Trees (review of A/B/C via the visual method)
# ═══════════════════════════════════════════════════════════════════════════════
def _L6CUM1_s(sheet):
    random.seed(640 + sheet)
    ranges = {1: (12, 40), 2: (24, 60), 3: (36, 100), 4: (48, 150)}
    lo, hi = ranges[sheet]
    S = _Sheet()
    S.extend_concept([
        cb("Review: Factors, Multiples & Prime Factorisation", [
            "A factor tree splits a number into prime factors step by step.",
            "The bottom of every branch is always a prime number.",
        ], "36 -> 6x6 -> (2x3)x(2x3) = 2x2x3x3."),
    ])
    pool = _esc_pick(range(lo, hi), 10)
    for i, n in enumerate(pool):
        text = f"Complete the factor tree for {n}."
        if i < 10:
            S.add(text, "Answer = ____", dtype="factor_tree", dparams={"n": n})
        else:
            S.add(text, "Answer = ____")
    for n in _esc_pick(range(lo, hi), 4, used=set()):
        S.add(f"List all factors of {n}, then circle the prime ones.", "Answer = ____", "word")
    for _ in range(3):
        n = random.randint(lo, hi)
        m = random.randint(3, 6)
        S.add(f"Is {n*m} a multiple of {n}? Is {n} a factor of {n*m}? Explain how these are two sides of the same fact.", "Answer = ____", "word")
    for _ in range(2):
        n = random.randint(lo, hi)
        pf = _l6_prime_factors_multiset(n)
        S.add(f"A factor tree for {n} ends with the branch {pf[0]} x {pf[0]} x {n//(pf[0]*pf[0]) if n % (pf[0]*pf[0])==0 else pf[-1]} -- if that product doesn't equal {n}, where did the tree go wrong?", "Answer = ____", "word")
    n = random.randint(lo, hi)
    S.add(f"True or False: a factor tree for {n} can end in more than one different set of prime factors.", "Answer = ____")
    return S.result()


# ═══════════════════════════════════════════════════════════════════════════════
# 6E — LCM
# ═══════════════════════════════════════════════════════════════════════════════
def _L6E_s(sheet):
    random.seed(650 + sheet)
    ranges = {1: (2, 12), 2: (4, 18), 3: (6, 25), 4: (8, 36)}
    lo, hi = ranges[sheet]
    pairs = _pair_pool(lo, hi, 20)
    S = _Sheet()
    S.extend_concept([
        cb("LCM — Lowest Common Multiple", [
            "LCM = the SMALLEST number that's a multiple of both.",
            "List multiples of each, find the smallest one in common.",
        ], "LCM(4,6) = 12."),
    ])
    for i, (a, b) in enumerate(pairs[:10]):
        text = f"LCM({a}, {b}) = ____"
        if i < 10:
            S.add(text, "", dtype="ladder_division", dparams={"a": a, "b": b, "mode": "lcm"})
        else:
            S.add(text, "Answer = ____")
    for a, b in pairs[10:14]:
        S.add(f"Two bells ring every {a} and {b} minutes. If both ring together at 0, when do they next ring together?", "Answer = ____", "word")
    for _ in range(3):
        l = random.choice([12, 18, 24, 36, 48])
        a = random.choice([d for d in range(2, 10) if l % d == 0])
        S.add(f"The LCM of two numbers is {l}. One of the numbers is {a}. Give ONE possibility for the other number.", "Answer = ____", "word")
    for _ in range(2):
        a, b = random.choice(pairs)
        real_lcm = _l6_lcm(a, b)
        wrong = max(1, real_lcm // random.choice([2, 3]))
        S.add(f"A student says LCM({a},{b}) = {wrong}. Check: is {wrong} actually a multiple of both numbers? What's the real LCM?", "Answer = ____", "word")
    a, b = random.choice(pairs)
    S.add(f"True or False: LCM({a},{b}) is always greater than or equal to both {a} and {b}.", "Answer = ____")
    return S.result()


# ═══════════════════════════════════════════════════════════════════════════════
# 6F — Word Problems (mixed HCF/LCM)
# ═══════════════════════════════════════════════════════════════════════════════
def _L6F_s(sheet):
    random.seed(660 + sheet)
    ranges = {1: (12, 40), 2: (24, 60), 3: (36, 100), 4: (48, 150)}
    lo, hi = ranges[sheet]
    S = _Sheet()
    S.extend_concept([
        cb("Choosing HCF or LCM", [
            "SPLITTING into equal, largest groups with nothing left over -> HCF.",
            "Things happening TOGETHER again / lining up -> LCM.",
        ], "Sharing sweets equally, none left over -> HCF. Two events repeating together -> LCM."),
    ])
    hcf_ctx = [
        "Two ribbons are {a}cm and {b}cm. Cut into equal pieces, none wasted -- longest piece?",
        "{a} pens and {b} pencils are packed into identical boxes, none left over -- most boxes possible?",
        "A tiler has {a}cm and {b}cm tiles to line up flush -- shortest matching wall length?" ,
    ]
    lcm_ctx = [
        "Two lights blink every {a}s and {b}s, together at 0 -- when do they next blink together?",
        "Bus A leaves every {a} min, Bus B every {b} min, together at 9:00 -- when do they next leave together?",
        "{a} stickers and {b} stickers come in packs -- fewest packs of each to have equal totals?",
    ]
    pairs = _pair_pool(lo, hi, 17)
    for i, (a, b) in enumerate(pairs[:7]):
        text = random.choice(hcf_ctx).format(a=a, b=b)
        if i < 7:
            S.add(text, "", dtype="ladder_division", dparams={"a": a, "b": b, "mode": "hcf"})
        else:
            S.add(text, "Answer = ____", "word")
    for i, (a, b) in enumerate(pairs[7:11]):
        text = random.choice(lcm_ctx).format(a=a, b=b)
        if i < 4:
            S.add(text, "", dtype="ladder_division", dparams={"a": a, "b": b, "mode": "lcm"})
        else:
            S.add(text, "Answer = ____", "word")
    for a, b in pairs[11:14]:
        which = random.choice(["HCF", "LCM"])
        S.add(f"For {a} and {b}, would you use HCF or LCM to solve \u201csplit into equal groups, nothing left over\u201d? Compute it.", "Answer = ____", "word")
    for a, b in pairs[14:17]:
        S.add(f"For {a} and {b}, would you use HCF or LCM to solve \u201cwhen do these repeat together again\u201d? Compute it.", "Answer = ____", "word")
    for _ in range(2):
        a, b = random.choice(pairs)
        S.add(f"A student is solving a \u2018things repeating together\u2019 problem with {a} and {b} but computes HCF instead of LCM. What will go wrong with their answer?", "Answer = ____", "word")
    a, b = random.choice(pairs)
    S.add(f"True or False: HCF({a},{b}) x LCM({a},{b}) = {a} x {b}.", "Answer = ____")
    return S.result()


# ═══════════════════════════════════════════════════════════════════════════════
# 6CUM2 — HCF/LCM via Venn Diagrams
# ═══════════════════════════════════════════════════════════════════════════════
def _L6CUM2_s(sheet):
    random.seed(670 + sheet)
    ranges = {1: (12, 40), 2: (24, 60), 3: (36, 90), 4: (48, 150)}
    lo, hi = ranges[sheet]
    S = _Sheet()
    S.extend_concept([
        cb("HCF & LCM via Venn Diagrams", [
            "Put each number's prime factors in a circle -- shared primes go in the overlap.",
            "HCF = product of the OVERLAP. LCM = product of EVERYTHING (both circles).",
        ], "12=2x2x3, 18=2x3x3 -> overlap {2,3} -> HCF=6. All primes {2,2,3,3} -> LCM=36."),
    ])
    pairs = _pair_pool(lo, hi, 10)
    for i, (a, b) in enumerate(pairs):
        pa, pb = _l6_prime_factors_multiset(a), _l6_prime_factors_multiset(b)
        common = []
        pb_copy = pb.copy()
        for p in pa:
            if p in pb_copy:
                common.append(p)
                pb_copy.remove(p)
        a_only = pa.copy()
        for p in common:
            a_only.remove(p)
        text = f"Draw the Venn diagram for {a} and {b}'s prime factors, then read off HCF and LCM."
        if i < 10:
            S.add(text, "", dtype="venn_two", dparams={"a_only": a_only, "common": common, "b_only": pb_copy, "label_a": str(a), "label_b": str(b)})
        else:
            S.add(text, "Answer = ____")
    for a, b in _pair_pool(lo, hi, 4):
        S.add(f"{a} and {b}: list the prime factors of each, circle what they share, then find HCF and LCM.", "Answer = ____", "word")
    used_r = set()
    for _ in range(3):
        remaining = [p for p in pairs if p not in used_r] or pairs
        a, b = random.choice(remaining)
        used_r.add((a, b))
        pa, pb = _l6_prime_factors_multiset(a), _l6_prime_factors_multiset(b)
        S.add(f"If {a}'s primes are {pa} and {b}'s primes are {pb}, which primes go in the OVERLAP of the Venn diagram?", "Answer = ____", "word")
    for _ in range(2):
        a, b = random.choice(pairs)
        S.add(f"A student draws the Venn diagram for {a} and {b} but puts a shared prime factor in only ONE circle, not the overlap. How does this affect their HCF answer?", "Answer = ____", "word")
    a, b = random.choice(pairs)
    S.add(f"True or False: a prime factor that appears in BOTH {a} and {b} must be placed in the overlap region.", "Answer = ____")
    return S.result()


# ═══════════════════════════════════════════════════════════════════════════════
# 6G — Applications
# ═══════════════════════════════════════════════════════════════════════════════
def _L6G_s(sheet):
    random.seed(680 + sheet)
    ranges = {1: (12, 40), 2: (24, 60), 3: (36, 100), 4: (48, 150)}
    lo, hi = ranges[sheet]
    S = _Sheet()
    S.extend_concept([
        cb("Applying HCF & LCM", [
            "Real problems don't say \"find the HCF\" -- you decide which one fits.",
            "Ask: am I splitting into equal groups (HCF), or finding when things line up (LCM)?",
        ], "Simplifying a fraction uses HCF. Finding a common denominator uses LCM."),
    ])
    pairs = _pair_pool(lo, hi, 14)
    ctx = [
        "A school has {a} boys and {b} girls for team photos -- largest equal-size teams with no leftovers, using HCF?",
        "Two machines complete a cycle every {a}s and {b}s -- how often do both finish together, using LCM?",
        "{a}kg and {b}kg of rice are split into equal-weight sacks, nothing left over -- heaviest sack size?",
    ]
    for i, (a, b) in enumerate(pairs[:8]):
        text = random.choice(ctx).format(a=a, b=b)
        if i < 8:
            mode = "hcf" if "HCF" in text or "equal" in text.split("using")[0] else "lcm"
            S.add(text, "", dtype="ladder_division", dparams={"a": a, "b": b, "mode": mode})
        else:
            S.add(text, "Answer = ____", "word")
    for a, b in pairs[8:12]:
        S.add(f"To simplify the fraction {a}/{b} to lowest terms, which operation do you need -- HCF or LCM? Do it.", "Answer = ____", "word")
    used_g = set(pairs[8:12])
    for _ in range(5):
        remaining = [p for p in pairs if p not in used_g] or pairs
        a, b = random.choice(remaining)
        used_g.add((a, b))
        S.add(f"You need to add fractions with denominators {a} and {b}. Which operation finds the common denominator -- HCF or LCM? Find it.", "Answer = ____", "word")
    for _ in range(2):
        remaining = [p for p in pairs if p not in used_g] or pairs
        a, b = random.choice(remaining)
        used_g.add((a, b))
        S.add(f"A student simplifying {a}/{b} divides top and bottom by the LCM instead of the HCF. What goes wrong?", "Answer = ____", "word")
    a, b = random.choice(pairs)
    S.add(f"True or False: simplifying a fraction to lowest terms means dividing by the HCF of numerator and denominator.", "Answer = ____")
    return S.result()


# ═══════════════════════════════════════════════════════════════════════════════
# 6H — Euclidean Algorithm for HCF
# ═══════════════════════════════════════════════════════════════════════════════
def _L6H_s(sheet):
    random.seed(690 + sheet)
    ranges = {1: (20, 80), 2: (50, 150), 3: (100, 300), 4: (200, 600)}
    lo, hi = ranges[sheet]
    pairs = _pair_pool(lo, hi, 20)
    S = _Sheet()
    S.extend_concept([
        cb("The Euclidean Algorithm", [
            "Divide the bigger by the smaller, note the remainder.",
            "Repeat with (smaller, remainder) until the remainder is 0 -- the last divisor is the HCF.",
        ], "HCF(48,18): 48=2x18+12, 18=1x12+6, 12=2x6+0 -> HCF=6."),
    ])
    for i, (a, b) in enumerate(pairs[:10]):
        text = f"Use the Euclidean Algorithm to find HCF({b}, {a})."
        if i < 10:
            S.add(text, "", dtype="euclidean_algorithm", dparams={"a": b, "b": a})
        else:
            S.add(text, "Answer = ____")
    for a, b in pairs[10:14]:
        S.add(f"Why is the Euclidean Algorithm faster than listing all factors for HCF({b},{a})? Try both and compare the steps.", "Answer = ____", "word")
    for _ in range(3):
        a, b = random.choice(pairs)
        big, small = max(a, b), min(a, b)
        q_val, r_val = big // small, big % small
        S.add(f"One step of the Euclidean Algorithm gives {big} = {q_val} x {small} + ____. What's the remainder?", "Answer = ____", "word")
    for _ in range(2):
        a, b = random.choice(pairs)
        big, small = max(a, b), min(a, b)
        S.add(f"A student doing HCF({big},{small}) stops as soon as they get a remainder, instead of continuing until the remainder is 0. What mistake are they making?", "Answer = ____", "word")
    a, b = random.choice(pairs)
    S.add(f"True or False: in the Euclidean Algorithm, the HCF is the LAST non-zero remainder... or is it the last divisor? Check with HCF({max(a,b)},{min(a,b)}) and state which one it really is.", "Answer = ____")
    return S.result()


# ═══════════════════════════════════════════════════════════════════════════════
# 6I — Puzzle
# ═══════════════════════════════════════════════════════════════════════════════
def _L6I_s(sheet):
    random.seed(700 + sheet)
    ranges = {1: (12, 40), 2: (24, 60), 3: (36, 100), 4: (48, 150)}
    lo, hi = ranges[sheet]
    S = _Sheet()
    S.extend_concept([
        cb("Factor & Multiple Puzzles", [
            "Puzzles combine several clues -- use one to narrow down, then check the rest.",
            "Write down what you know before guessing.",
        ], "A number under 30, multiple of 4, with exactly 6 factors -> check 12, 20, 28... 12 works."),
    ])
    for i, n in enumerate(_esc_pick(range(lo, hi), 10)):
        nfac = len(_l6_factors_of(n))
        mult_of = random.choice([d for d in _l6_factors_of(n) if d > 1])
        text = f"I'm between {lo}-{hi}, a multiple of {mult_of}, with {nfac} factors. Who am I? (e.g. {n})"
        if i < 10:
            if n <= 15:
                S.add(text, "Answer = ____", dtype="factor_rainbow", dparams={"n": n})
            else:
                S.add(text, "Answer = ____", dtype="factor_array", dparams={"n": n})
        else:
            S.add(text, "Answer = ____", "word")
    for _ in range(4):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        h, l = _l6_hcf(a, b), _l6_lcm(a, b)
        S.add(f"Two numbers have HCF {h} and LCM {l}. Their product is HCF x LCM = ____. If one number is {a}, what's the other?", "Answer = ____", "word")
    for n in _esc_pick(range(lo, hi), 3, used=set()):
        S.add(f"I am under {hi}, a multiple of {random.choice([3,4,5,6])}, and prime-factorises into exactly {len(_l6_prime_factors_multiset(n))} primes (counting repeats). Who am I?", "Answer = ____", "word")
    for _ in range(2):
        n = random.randint(lo, hi)
        wrong_nfac = len(_l6_factors_of(n)) + 1
        S.add(f"A puzzle says \u201cI have {wrong_nfac} factors\u201d for a number that actually has {len(_l6_factors_of(n))}. If the number is {n}, what mistake did the puzzle-writer make?", "Answer = ____", "word")
    n = random.randint(lo, hi)
    S.add(f"True or False: a number can have exactly 2 factors and also be even (other than checking 2 itself).", "Answer = ____")
    return S.result()


# ═══════════════════════════════════════════════════════════════════════════════
# 6CUM3 — Prime Number Enrichment
# ═══════════════════════════════════════════════════════════════════════════════
def _L6CUM3_s(sheet):
    random.seed(710 + sheet)
    ranges = {1: (2, 40), 2: (2, 60), 3: (2, 100), 4: (2, 150)}
    lo, hi = ranges[sheet]
    S = _Sheet()
    S.extend_concept([
        cb("Prime Numbers", [
            "A prime has EXACTLY 2 factors: 1 and itself. 1 is NOT prime (only 1 factor).",
            "2 is the only even prime -- every other even number has 2 as an extra factor.",
        ], "2,3,5,7,11,13,17,19,23,29... primes under 30."),
    ])
    used_c3 = set()
    grid_hi = min(hi, 100)
    for i, n in enumerate(_esc_pick(range(max(lo, 10), grid_hi), 6, used=used_c3)):
        text = f"Is {n} prime or composite? Check using the hundred grid."
        S.add(text, "Answer = ____", dtype="hundred_grid_highlight", dparams={"n": n, "highlight": [n]})
    for n in _esc_pick(range(lo, hi), 4, used=used_c3):
        text = f"Is {n} prime or composite?"
        if n <= 100:
            S.add(text, "Answer = ____", dtype="hundred_grid_highlight", dparams={"n": n, "highlight": [n]})
        else:
            S.add(text, "Answer = ____")
    for _ in range(4):
        n = random.randint(max(lo, 4), hi)
        S.add(f"Find a pair of TWIN primes (differ by 2) near {n}.", "Answer = ____", "word")
    for n in random.sample([9, 15, 21, 25, 27, 33, 35, 49, 51], 3):
        S.add(f"A student says {n} is prime because it's odd and doesn't end in 0 or 5. Find a factor that proves them wrong.", "Answer = ____", "word")
    tf_claims = [
        "True or False: all prime numbers are odd.",
        "True or False: 2 is the only even prime number.",
        "True or False: every odd number is prime.",
    ]
    for claim in tf_claims:
        S.add(claim, "Answer = ____")
    return S.result()


# ═══════════════════════════════════════════════════════════════════════════════
# 6J — Mastery Challenge (genuinely hardest: multi-step, word-problem heavy)
# ═══════════════════════════════════════════════════════════════════════════════
def _L6J_s(sheet):
    random.seed(720 + sheet)
    ranges = {1: (40, 120), 2: (80, 250), 3: (150, 400), 4: (250, 600)}
    lo, hi = ranges[sheet]
    S = _Sheet()
    S.extend_concept([
        cb("Mastery Challenge", [
            "These combine HCF, LCM, primes and word context in one question -- read carefully "
            "and decide what's actually being asked before computing.",
        ], "\u201cLargest equal group, nothing left over\u201d = HCF. \u201cNext time together\u201d = LCM."),
    ])
    triples = []
    while len(triples) < 6:
        a, b, c = random.randint(lo, hi), random.randint(lo, hi), random.randint(lo, hi)
        if len({a, b, c}) == 3:
            triples.append(tuple(sorted((a, b, c))))
    for i, (a, b, c) in enumerate(triples):
        text = f"HCF({a}, {b}, {c}) = ____"
        if i < 6:
            ab = _l6_hcf(a, b)
            S.add(text, "", dtype="ladder_division", dparams={"a": ab, "b": c, "mode": "hcf"})
        else:
            S.add(text, "Answer = ____")
    for a, b, c in triples[:2]:
        S.add(f"LCM({a}, {b}, {c}) = ____", "Answer = ____")
    pairs = _pair_pool(lo, hi, 11)
    for a, b in pairs[:5]:
        ctx = random.choice([
            f"Three lengths of wire {a}cm and {b}cm must be cut into equal pieces with none wasted -- longest piece, then how many total pieces?",
            f"Two alarms ring every {a} and {b} minutes from 6:00am -- next time together, and how many times by noon?",
        ])
        S.add(ctx, "Answer = ____", "word")
    for a, b in pairs[5:9]:
        S.add(f"A number is a multiple of {a} and has HCF {min(a,b)} with {b}. Is this possible? Explain using what you know about HCF and multiples.", "Answer = ____", "word")
    for _ in range(2):
        a, b, c = random.choice(triples)
        wrong = _l6_hcf(a, b)
        S.add(f"A student computes HCF({a},{b},{c}) by finding HCF({a},{b})={wrong} and stopping there, ignoring {c}. What's missing from their method?", "Answer = ____", "word")
    a, b, c = random.choice(triples)
    S.add(f"True or False: HCF({a},{b},{c}) must be less than or equal to HCF({a},{b}).", "Answer = ____")
    return S.result()


# ═══════════════════════════════════════════════════════════════════════════════
# 6REV — Level 6 Revision (mixed, escalating to the hardest of the level)
# ═══════════════════════════════════════════════════════════════════════════════
def _L6REV_s(sheet):
    random.seed(730 + sheet)
    ranges = {1: (20, 80), 2: (40, 150), 3: (80, 300), 4: (150, 500)}
    lo, hi = ranges[sheet]
    S = _Sheet()
    S.extend_concept([
        cb("Level 6 Revision — Factors, Multiples, HCF & LCM", [
            "HCF: biggest shared factor -- splitting into equal groups.",
            "LCM: smallest shared multiple -- things lining up together.",
            "Euclidean Algorithm: fast HCF via repeated division.",
        ], ""),
    ])
    pairs = _pair_pool(lo, hi, 14)
    for i, (a, b) in enumerate(pairs[:6]):
        mode = random.choice(["hcf", "lcm"])
        label = "HCF" if mode == "hcf" else "LCM"
        text = f"{label}({a}, {b}) = ____"
        if i < 6:
            dtype = "euclidean_algorithm" if mode == "hcf" else "ladder_division"
            dparams = {"a": max(a, b), "b": min(a, b)} if mode == "hcf" else {"a": a, "b": b, "mode": "lcm"}
            S.add(text, "", dtype=dtype, dparams=dparams)
        else:
            S.add(text, "Answer = ____")
    for i, (a, b) in enumerate(pairs[6:10]):
        n = random.randint(lo, hi)
        text = f"Is {n} prime? Find its prime factorisation regardless."
        if i < 2:
            S.add(text, "Answer = ____", dtype="factor_tree", dparams={"n": n})
        else:
            S.add(text, "Answer = ____", "word")
    for i, (a, b) in enumerate(pairs[10:14]):
        text = f"Two tapes {a}cm and {b}cm are cut into equal pieces, nothing wasted -- longest piece?"
        if i < 2:
            S.add(text, "", dtype="ladder_division", dparams={"a": a, "b": b, "mode": "hcf"})
        else:
            S.add(text, "Answer = ____", "word")
    for _ in range(3):
        a, b = random.choice(pairs)
        S.add(f"For {a} and {b}: is HCF x LCM = {a} x {b} true here? Verify it.", "Answer = ____", "word")
    for _ in range(2):
        a, b = random.choice(pairs)
        S.add(f"A student mixes up HCF and LCM for {a} and {b}, giving the LCM as their HCF answer. How would you spot this mistake just by checking the size of their answer?", "Answer = ____", "word")
    a, b = random.choice(pairs)
    S.add(f"True or False: for any two numbers, HCF({a},{b}) divides LCM({a},{b}) exactly.", "Answer = ____")
    return S.result()


LEVEL6_DISPATCH = {
    "6A":    {1: lambda: _L6A_s(1), 2: lambda: _L6A_s(2), 3: lambda: _L6A_s(3), 4: lambda: _L6A_s(4)},
    "6B":    {1: lambda: _L6B_s(1), 2: lambda: _L6B_s(2), 3: lambda: _L6B_s(3), 4: lambda: _L6B_s(4)},
    "6C":    {1: lambda: _L6C_s(1), 2: lambda: _L6C_s(2), 3: lambda: _L6C_s(3), 4: lambda: _L6C_s(4)},
    "6CUM1": {1: lambda: _L6CUM1_s(1), 2: lambda: _L6CUM1_s(2), 3: lambda: _L6CUM1_s(3), 4: lambda: _L6CUM1_s(4)},
    "6D":    {1: lambda: _L6D_s(1), 2: lambda: _L6D_s(2), 3: lambda: _L6D_s(3), 4: lambda: _L6D_s(4)},
    "6E":    {1: lambda: _L6E_s(1), 2: lambda: _L6E_s(2), 3: lambda: _L6E_s(3), 4: lambda: _L6E_s(4)},
    "6F":    {1: lambda: _L6F_s(1), 2: lambda: _L6F_s(2), 3: lambda: _L6F_s(3), 4: lambda: _L6F_s(4)},
    "6CUM2": {1: lambda: _L6CUM2_s(1), 2: lambda: _L6CUM2_s(2), 3: lambda: _L6CUM2_s(3), 4: lambda: _L6CUM2_s(4)},
    "6G":    {1: lambda: _L6G_s(1), 2: lambda: _L6G_s(2), 3: lambda: _L6G_s(3), 4: lambda: _L6G_s(4)},
    "6H":    {1: lambda: _L6H_s(1), 2: lambda: _L6H_s(2), 3: lambda: _L6H_s(3), 4: lambda: _L6H_s(4)},
    "6I":    {1: lambda: _L6I_s(1), 2: lambda: _L6I_s(2), 3: lambda: _L6I_s(3), 4: lambda: _L6I_s(4)},
    "6CUM3": {1: lambda: _L6CUM3_s(1), 2: lambda: _L6CUM3_s(2), 3: lambda: _L6CUM3_s(3), 4: lambda: _L6CUM3_s(4)},
    "6J":    {1: lambda: _L6J_s(1), 2: lambda: _L6J_s(2), 3: lambda: _L6J_s(3), 4: lambda: _L6J_s(4)},
    "6REV":  {1: lambda: _L6REV_s(1), 2: lambda: _L6REV_s(2), 3: lambda: _L6REV_s(3), 4: lambda: _L6REV_s(4)},
}
