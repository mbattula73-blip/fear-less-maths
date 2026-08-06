"""
Fear Less Maths — LEVEL 22 (Pre Level 2 — Even/Odd & Grouping) v3
architecture (2026-08-06)

Per direct request: consolidated from 10 core sublevels down to 5,
removing heavy repetition (the old A/B/D/I/J ALL opened "Is this even
or odd?" -- 5 of 10 sublevels). Merged by SKILL, sheets carry the
difficulty escalation.

  22A  Even/Odd Recognition        (was A,B,D,I)
  22B  Skip-Counting Patterns      (was C)
  22C  Equal Grouping              (was E)
  22D  Splitting into Equal Rows   (was F,G,H)
  22E  Mixed Challenge             (was J)

CONTENT-APPROPRIATENESS FIX: the old F/G/H taught "prime numbers",
"composite numbers", and "factor trees" BY NAME -- Class 5-6
vocabulary, not Class 1-2. The underlying visual (array_grid: a single
row of dots = can't split into equal rows > 1; a rectangle = can) is
kept since it's already purely geometric with no text, but the
question framing is now "can these be arranged into more than one
equal row?" with no formal terminology at all.

100% diagrammatic (Level 22 is excluded from the PICTORIAL_LEVELS
abstract-fade in get_questions(), same as Level 21).

Diagram audit: all 4 new types used here (pair_grouping, number_train,
even_odd_numberline, factor_rectangle, array_grid) already correctly
designed with no answer leaks (even_odd_numberline explicitly keeps
the target dot neutral-colored so its own color can't hand over the
answer; factor_rectangle uses brackets with no group-count text).
"""
import random
from content import q


# ───────────────────────── 22A: Even/Odd Recognition ─────────────────────────

def _22A(sheet):
    tiers = {1: (1, 10), 2: (5, 20), 3: (10, 40), 4: (20, 60)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        n = random.randint(lo, hi)
        variant = i % 3
        if variant == 0 and n <= 20:
            items.append(q("Circle pairs. Is it even or odd?", "diagram", "____", "", "pair_grouping",
                            {"count": n, "kind": random.choice(["apple", "star", "balloon"])}))
        elif variant == 1 and n <= 20:
            items.append(q("Is it even or odd?", "diagram", "____", "", "number_train",
                            {"count": n, "kind": random.choice(["apple", "star"])}))
        else:
            items.append(q("Is the circled number even or odd?", "diagram", "____", "", "even_odd_numberline",
                            {"lo": max(1, n - 3), "hi": n + 3, "mark": n}))
    return items


# ───────────────────────── 22B: Skip-Counting Patterns ─────────────────────────

def _22B(sheet):
    tiers = {1: (1, 20, [2]), 2: (10, 40, [2, 5]), 3: (20, 60, [2, 5, 10]), 4: (30, 90, [2, 5, 10])}
    lo, hi, steps = tiers[sheet]
    items = []
    for i in range(20):
        step = random.choice(steps)
        start = random.randint(lo, max(lo, hi - step * 4))
        seq = [start + j * step for j in range(4)]
        blank_pos = random.choice([1, 2, 3])
        seq_display = list(seq)
        seq_display[blank_pos] = None
        items.append(q("Find the missing number in the pattern.", "diagram", "____", "", "sequence_boxes",
                        {"seq": seq_display, "label": "pattern"}))
    return items


# ───────────────────────── 22C: Equal Grouping ─────────────────────────

def _22C(sheet):
    tiers = {1: [(6, 2), (6, 3), (8, 2), (8, 4)], 2: [(10, 2), (10, 5), (12, 3), (12, 4)],
             3: [(15, 3), (15, 5), (16, 4), (18, 3)], 4: [(20, 4), (20, 5), (24, 4), (24, 6)]}
    pool = tiers[sheet]
    items = []
    for i in range(20):
        n, gs = random.choice(pool)
        items.append(q("How many groups? How many in each group?", "diagram", "____", "", "factor_rectangle",
                        {"n": n, "group_size": gs, "kind": random.choice(["apple", "star", "balloon", "flower"])}))
    return items


# ───────────────────────── 22D: Splitting into Equal Rows ─────────────────────────
# (replaces the old prime/composite/factor-tree framing entirely -- same
# geometric array_grid visual, age-appropriate question text, no
# formal vocabulary)

def _22D(sheet):
    tiers = {1: list(range(2, 13)), 2: list(range(2, 19)), 3: list(range(2, 25)), 4: list(range(2, 31))}
    pool = tiers[sheet]
    items = []
    for i in range(20):
        n = random.choice(pool)
        # rows = a genuine factor of n where possible (>1 row), else 1 row
        factors = [r for r in range(2, n) if n % r == 0 and n // r > 1]
        if factors and i % 2 == 0:
            rows = random.choice(factors)
        else:
            rows = 1
        items.append(q("Can you make more than one equal row?",
                        "diagram", "____", "", "array_grid", {"n": n, "rows": rows}))
    return items


# ───────────────────────── 22E: Mixed Challenge ─────────────────────────

def _22E(sheet):
    tiers = {1: (1, 15), 2: (5, 25), 3: (10, 40), 4: (15, 60)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        n = random.randint(lo, hi)
        variant = i % 4
        if variant == 0:
            if n <= 20:
                items.append(q("Is it even or odd?", "diagram", "____", "", "pair_grouping",
                                {"count": n, "kind": random.choice(["apple", "star"])}))
            else:
                items.append(q("Is the circled number even or odd?", "diagram", "____", "", "even_odd_numberline",
                                {"lo": max(1, n - 3), "hi": n + 3, "mark": n}))
        elif variant == 1:
            step = random.choice([2, 5])
            seq = [n, n + step, None, n + 3 * step]
            items.append(q("Find the missing number in the pattern.", "diagram", "____", "", "sequence_boxes",
                            {"seq": seq, "label": "pattern"}))
        elif variant == 2:
            gs = random.choice([2, 3, 4])
            total = gs * random.randint(2, 5)
            items.append(q("How many groups? How many in each group?", "diagram", "____", "", "factor_rectangle",
                            {"n": total, "group_size": gs, "kind": random.choice(["apple", "flower"])}))
        else:
            nn = random.randint(2, 20)
            factors = [r for r in range(2, nn) if nn % r == 0 and nn // r > 1]
            rows = random.choice(factors) if factors else 1
            items.append(q("Can these be arranged into more than one equal row?", "diagram", "____", "", "array_grid",
                            {"n": nn, "rows": rows}))
    return items


_SUBLEVEL_BUILDERS = {
    "A": _22A, "B": _22B, "C": _22C, "D": _22D, "E": _22E,
}

_TOPIC_NAMES = {
    "A": "Even or Odd",
    "B": "Skip-Counting Patterns",
    "C": "Equal Grouping",
    "D": "Splitting into Equal Rows",
    "E": "Mixed Challenge",
}


def build_v3_sheet(code, sheet):
    random.seed(22000 + hash(code) % 5000 + sheet * 31)
    items = _SUBLEVEL_BUILDERS[code](sheet)
    return items[:20]


LEVEL22_V3_DISPATCH = {
    f"__L22__{code}": {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SUBLEVEL_BUILDERS
}
