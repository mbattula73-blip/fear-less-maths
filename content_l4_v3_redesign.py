"""
Fear Less Maths — LEVEL 4 (Multiplication) v3 architecture (2026-08-19)

Per direct request: Level 4 previously had 25 sublevels but NO genuine
difficulty escalation -- even its "multi-digit" sublevel never exceeded
2-digit x 1-digit multiplication, and one sublevel had a broken/empty
diagram tier. Rebuilt into the standard 14-sublevel (10 core + 3 CUM +
1 REV = 56 worksheets) v3 architecture used for Levels 6-20, with a
genuine escalation arc from the multiplication CONCEPT all the way to
4-digit x 4-digit multiplication by the final sublevels ("at least 4
by 4 multiplication", per direct request):

  4A  Concept -- repeated addition & arrays
  4B  Tables 0, 1, 2, 5, 10 (easy anchor facts)
  4C  Tables 3, 4, 6, 9 (middle facts)
  4CUM1  Review: A-C
  4D  Tables 7, 8 & Squares (hardest single-digit facts)
  4E  2-digit x 1-digit (with carrying)
  4F  2-digit x 2-digit (area/split method)
  4CUM2  Review: D-F
  4G  3-digit x 1-digit and 3-digit x 2-digit
  4H  3-digit x 3-digit
  4I  4-digit x 2-digit and 4-digit x 3-digit
  4CUM3  Review: G-I
  4J  4-digit x 4-digit + word problems + mixed challenge
  4REV  Level 4 Revision (mixed review of everything)

One new diagram built: `split_mult_area` -- the place-value split
(area/box) method, scaling naturally from a 2x1 grid up to a 4x4 grid,
used consistently across every multi-digit sublevel (E-J) instead of
needing a different diagram per size. Verified the partial-product
grid always sums to the exact product across every tested size.
Sublevels A-D reuse the existing, already-audited array_blank/
equal_groups_blank (blank-by-default, no leaked answers).

Every sublevel escalates within its own 4 sheets too (not just across
the whole level) -- sheet 1 = easiest tier of that sublevel's range,
sheet 4 = hardest.
"""
import random
from content import q


# ───────────────────────── shared helpers ─────────────────────────

def _array_q(rows, cols, blank=True, text=None):
    text = text or ("Find the total shown by this array." if blank else f"This array shows {rows} rows of {cols}. Find the total.")
    return q(text, "diagram", "____", "", "array_blank",
              {"rows": rows, "cols": cols})


def _groups_q(groups, size, blank=True, text=None):
    text = text or ("Find the total shown by these equal groups." if blank else f"This shows {groups} equal groups of {size}. Find the total.")
    return q(text, "diagram", "____", "", "equal_groups_blank",
              {"groups": groups, "size": size})


def _split_q(a, b, blank=True, text="Use the split method to find the product."):
    return q(text, "diagram", "____", "", "split_mult_area", {"a": a, "b": b, "blank": blank})


# ───────────────────────── 4A: Concept -- repeated addition & arrays ─────────────────────────

def _4A(sheet):
    tiers = {1: (2, 3), 2: (2, 4), 3: (3, 5), 4: (4, 6)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        blank = i >= 2
        if i % 2 == 0:
            items.append(_array_q(a, b, blank=blank))
        else:
            items.append(_groups_q(a, b, blank=blank))
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        variant = i % 3
        if variant == 0:
            addends = " + ".join([str(b)] * a)
            items.append(q(f"Write as multiplication: {addends} = ____ x ____", "fill", "Answer = ____"))
        elif variant == 1:
            items.append(q(f"{a} rows of {b} = {a} x {b} = ____", "fill", "Answer = ____"))
        else:
            items.append(q(f"True or False: {a} x {b} means {a} groups of {b}.", "fill", "____ (True/False)"))
    return items


# ───────────────────────── 4B: Tables 0, 1, 2, 5, 10 ─────────────────────────

def _4B(sheet):
    diagram_tables = [1, 2, 5, 10]
    fact_tables = [0, 1, 2, 5, 10]
    tiers = {1: (1, 6), 2: (1, 8), 3: (1, 10), 4: (1, 12)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        t = random.choice(diagram_tables)
        n = random.randint(lo, hi)
        blank = i >= 2
        if t <= 5:
            items.append(_groups_q(n, t, blank=blank))
        else:
            items.append(_array_q(n, min(t, 10), blank=blank))
    for i in range(6):
        t = random.choice(fact_tables)
        n = random.randint(lo, hi)
        if i % 2 == 0:
            items.append(q(f"{t} x {n} = ____", "fill", "Answer = ____"))
        else:
            items.append(q(f"{n} x {t} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── 4C: Tables 3, 4, 6, 9 ─────────────────────────

def _4C(sheet):
    tables = [3, 4, 6, 9]
    tiers = {1: (1, 6), 2: (1, 8), 3: (1, 10), 4: (1, 12)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        t = random.choice(tables)
        n = random.randint(lo, hi)
        blank = i >= 2
        items.append(_groups_q(n, t, blank=blank))
    for i in range(6):
        t = random.choice(tables)
        n = random.randint(lo, hi)
        variant = i % 3
        if variant == 0:
            items.append(q(f"{t} x {n} = ____", "fill", "Answer = ____"))
        elif variant == 1:
            items.append(q(f"{n} x {t} = ____", "fill", "Answer = ____"))
        else:
            correct = t * n
            wrong = correct + random.choice([-t, t, -1, 1])
            items.append(q(f"True or False: {t} x {n} = {wrong}.", "fill", "____ (True/False)"))
    return items


# ───────────────────────── 4CUM1: Review A-C ─────────────────────────

def _4CUM1(sheet):
    tiers = {1: (1, 6), 2: (1, 8), 3: (1, 9), 4: (1, 10)}
    lo, hi = tiers[sheet]
    diagram_tables = [1, 2, 3, 4, 5, 6, 9, 10]
    fact_tables = [0, 1, 2, 3, 4, 5, 6, 9, 10]
    items = []
    for i in range(6):
        t = random.choice(diagram_tables)
        n = random.randint(lo, hi)
        blank = i >= 2
        items.append(_groups_q(n, t, blank=blank))
    for i in range(6):
        t = random.choice(fact_tables)
        n = random.randint(lo, hi)
        items.append(q(f"{t} x {n} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── 4D: Tables 7, 8 & Squares ─────────────────────────

def _4D(sheet):
    tiers = {1: (1, 6), 2: (1, 8), 3: (1, 10), 4: (1, 12)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        blank = i >= 2
        if i % 3 == 2:
            n = random.randint(2, min(hi, 12))
            items.append(_array_q(n, n, blank=blank,
                          text=f"This array shows {n} rows of {n} -- a SQUARE number. Find the total." if not blank else "Find the total shown by this square array."))
        else:
            t = random.choice([7, 8])
            n = random.randint(lo, hi)
            items.append(_groups_q(n, t, blank=blank))
    for i in range(6):
        variant = i % 3
        if variant == 2:
            n = random.randint(2, min(hi, 12))
            items.append(q(f"{n} squared = {n} x {n} = ____", "fill", "Answer = ____"))
        else:
            t = random.choice([7, 8])
            n = random.randint(lo, hi)
            items.append(q(f"{t} x {n} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── 4E: 2-digit x 1-digit (with carrying) ─────────────────────────

def _4E(sheet):
    tiers = {1: (11, 30), 2: (20, 50), 3: (35, 75), 4: (50, 99)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(2, 9)
        blank = i >= 2
        items.append(_split_q(a, b, blank=blank,
                     text=f"Use the split method: {a} x {b}." if not blank else "Use the split method to find the product."))
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(2, 9)
        if i % 2 == 0:
            items.append(q(f"{a} x {b} = ____", "fill", "Answer = ____"))
        else:
            tens, ones = divmod(a, 10)
            items.append(q(f"{a} x {b} = ({tens*10} x {b}) + ({ones} x {b}) = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── 4F: 2-digit x 2-digit (area/split method) ─────────────────────────

def _4F(sheet):
    tiers = {1: (11, 30), 2: (15, 45), 3: (25, 65), 4: (40, 99)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        blank = i >= 2
        items.append(_split_q(a, b, blank=blank,
                     text=f"Use the split method: {a} x {b}." if not blank else "Use the split method to find the product."))
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        items.append(q(f"{a} x {b} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── 4CUM2: Review D-F ─────────────────────────

def _4CUM2(sheet):
    tiers = {1: (20, 40), 2: (25, 55), 3: (35, 70), 4: (45, 90)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        blank = i >= 2
        if i % 2 == 0:
            a = random.randint(lo, hi)
            b = random.randint(2, 9)
        else:
            a = random.randint(lo, hi)
            b = random.randint(lo, hi)
        items.append(_split_q(a, b, blank=blank))
    for i in range(6):
        t = random.choice([7, 8])
        n = random.randint(2, 12)
        items.append(q(f"{t} x {n} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── 4G: 3-digit x 1-digit and 3-digit x 2-digit ─────────────────────────

def _4G(sheet):
    tiers = {1: (110, 300), 2: (200, 500), 3: (350, 700), 4: (500, 999)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        a = random.randint(lo, hi)
        blank = i >= 2
        b = random.randint(2, 9) if i % 2 == 0 else random.randint(11, 99)
        items.append(_split_q(a, b, blank=blank,
                     text=f"Use the split method: {a} x {b}." if not blank else "Use the split method to find the product."))
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(2, 9) if i % 2 == 0 else random.randint(11, 99)
        items.append(q(f"{a} x {b} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── 4H: 3-digit x 3-digit ─────────────────────────

def _4H(sheet):
    tiers = {1: (110, 300), 2: (200, 500), 3: (350, 700), 4: (500, 999)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        blank = i >= 2
        items.append(_split_q(a, b, blank=blank,
                     text=f"Use the split method: {a} x {b}." if not blank else "Use the split method to find the product."))
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        items.append(q(f"{a} x {b} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── 4I: 4-digit x 2-digit and 4-digit x 3-digit ─────────────────────────

def _4I(sheet):
    tiers = {1: (1100, 3000), 2: (2000, 5000), 3: (3500, 7000), 4: (5000, 9999)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(11, 99) if i % 2 == 0 else random.randint(110, 999)
        blank = i >= 2
        items.append(_split_q(a, b, blank=blank,
                     text=f"Use the split method: {a} x {b}." if not blank else "Use the split method to find the product."))
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(11, 99) if i % 2 == 0 else random.randint(110, 999)
        items.append(q(f"{a} x {b} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── 4CUM3: Review G-I ─────────────────────────

def _4CUM3(sheet):
    tiers = {1: (200, 900), 2: (500, 2000), 3: (1000, 4000), 4: (2000, 8000)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(11, 99)
        blank = i >= 2
        items.append(_split_q(a, b, blank=blank))
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(11, 99)
        items.append(q(f"{a} x {b} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── 4J: 4-digit x 4-digit + word problems + mixed challenge ─────────────────────────

def _4J(sheet):
    tiers = {1: (1100, 3000), 2: (2000, 5000), 3: (3500, 7000), 4: (5000, 9999)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(4):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        blank = i >= 2
        items.append(_split_q(a, b, blank=blank,
                     text=f"The final challenge: split method for {a} x {b}." if not blank else "Use the split method to find the product."))
    word_templates = [
        lambda a, b: f"A factory makes {a} toys every day. How many toys does it make in {b} days?",
        lambda a, b: f"A stadium has {a} seats in each section, with {b} sections. How many seats in total?",
        lambda a, b: f"A book has {a} words per page. How many words are in {b} pages?",
    ]
    for i in range(2):
        a = random.randint(max(10, lo // 100), max(20, hi // 100))
        b = random.randint(max(2, lo // 10), max(10, hi // 10))
        tmpl = random.choice(word_templates)
        items.append(q(tmpl(a, b), "fill", "Answer = ____"))
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        items.append(q(f"{a} x {b} = ____", "fill", "Answer = ____"))
    for i in range(6):
        a = random.randint(100, 999)
        b = random.randint(2, 99)
        items.append(q(f"{a} x {b} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── 4REV: Level 4 Revision ─────────────────────────

def _4REV(sheet):
    tiers = {1: (2, 12), 2: (10, 99), 3: (100, 999), 4: (1000, 9999)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(6):
        blank = i >= 2
        if sheet == 1:
            a = random.randint(lo, hi)
            b = random.randint(lo, hi)
            items.append(_groups_q(a, b, blank=blank))
        else:
            a = random.randint(lo, hi)
            b = random.randint(2, min(99, hi))
            items.append(_split_q(a, b, blank=blank))
    for i in range(6):
        a = random.randint(lo, hi)
        b = random.randint(2, min(99, hi)) if sheet > 1 else random.randint(lo, hi)
        items.append(q(f"{a} x {b} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── Quick Review (Levels 2-3, real prerequisites) ─────────────────────────

def _l4v3_quick_review(sheet):
    tiers = {1: (5, 20), 2: (15, 40), 3: (30, 70), 4: (50, 120)}
    lo, hi = tiers[min(sheet, 4)]
    items = []
    a = random.randint(lo, hi)
    b = random.randint(lo, hi)
    items.append(q(f"Quick Review (Level 3, Addition): {a} + {b} = ____", "fill", "Answer = ____"))
    c = random.randint(lo, hi)
    d = random.randint(1, c)
    items.append(q(f"Quick Review (Level 3, Subtraction): {c} - {d} = ____", "fill", "Answer = ____"))
    n = random.randint(lo, hi)
    items.append(q(f"Quick Review (Level 2, Even/Odd): Is {n} even or odd?", "fill", "Answer = ____"))
    return items


# ───────────────────────── Speed Calculation ─────────────────────────

_SPEED_TIERS = {
    "4A": {1: (2, 3), 2: (2, 4), 3: (3, 5), 4: (4, 6)},
    "4B": {1: (1, 5), 2: (1, 10), 3: (1, 10), 4: (1, 10)},
    "4C": {1: (1, 6), 2: (1, 9), 3: (1, 9), 4: (1, 9)},
    "4CUM1": {1: (1, 6), 2: (1, 8), 3: (1, 9), 4: (1, 10)},
    "4D": {1: (2, 7), 2: (2, 8), 3: (2, 9), 4: (2, 12)},
    "4E": {1: (11, 30), 2: (20, 50), 3: (35, 75), 4: (50, 99)},
    "4F": {1: (11, 30), 2: (15, 45), 3: (25, 65), 4: (40, 99)},
    "4CUM2": {1: (20, 40), 2: (25, 55), 3: (35, 70), 4: (45, 90)},
    "4G": {1: (110, 300), 2: (200, 500), 3: (350, 700), 4: (500, 999)},
    "4H": {1: (110, 300), 2: (200, 500), 3: (350, 700), 4: (500, 999)},
    "4I": {1: (1100, 3000), 2: (2000, 5000), 3: (3500, 7000), 4: (5000, 9999)},
    "4CUM3": {1: (200, 900), 2: (500, 2000), 3: (1000, 4000), 4: (2000, 8000)},
    "4J": {1: (1100, 3000), 2: (2000, 5000), 3: (3500, 7000), 4: (5000, 9999)},
    "4REV": {1: (2, 12), 2: (10, 99), 3: (100, 999), 4: (1000, 9999)},
}


def _l4v3_speed_calc(code, sheet):
    lo, hi = _SPEED_TIERS[code][sheet]
    items = []
    for _ in range(5):
        a = random.randint(lo, hi)
        if hi > 999:
            b = random.randint(2, 99)
        elif hi > 99:
            b = random.randint(2, 20)
        elif hi > 12:
            b = random.randint(2, 12)
        else:
            b = random.randint(2, hi)
        items.append(q(f"Speed: {a} x {b} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── Assembly ─────────────────────────

_SUBLEVEL_BUILDERS = {
    "4A": _4A, "4B": _4B, "4C": _4C, "4CUM1": _4CUM1,
    "4D": _4D, "4E": _4E, "4F": _4F, "4CUM2": _4CUM2,
    "4G": _4G, "4H": _4H, "4I": _4I, "4CUM3": _4CUM3,
    "4J": _4J, "4REV": _4REV,
}


def build_v3_sheet(code, sheet):
    random.seed(4000 + hash(code) % 5000 + sheet * 31)
    out = _SUBLEVEL_BUILDERS[code](sheet)
    out += _l4v3_quick_review(sheet)
    out += _l4v3_speed_calc(code, sheet)
    return out[:20]


LEVEL4_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SUBLEVEL_BUILDERS
}
