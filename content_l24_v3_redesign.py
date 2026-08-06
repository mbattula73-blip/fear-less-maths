"""
Fear Less Maths — LEVEL 24 (Pre Level 4 — Multiplication) v3
architecture (2026-08-06)

Per direct request: consolidated from 10 core sublevels down to 5
(old B/C/D/E/J all opened "Find the product" -- 5 of 10 duplicated).
Merged by SKILL, sheets carry the difficulty escalation.

  24A  Multiplication Concept & Tables 2-5   (was A,B)
  24B  Tables 6-10                            (was C)
  24C  Multi-digit & Word Problems             (was D,E,F)
  24D  Patterns & Speed                        (was G,H)
  24E  Picture Puzzles & Mixed Challenge       (was I,J)

100% diagrammatic. Diagram audit: multiply_grid (objects in a grid,
blank answer box, no leaked text at all) and repeated_groups (separate
clusters with an "x{size}" label under each -- labels a GIVEN factor
as an intentional scaffold per its own docstring, never the total/
product) both already correctly designed, no leaks. sequence_boxes
already audited safe in Levels 21/22.
"""
import random
from content import q


def _grid(rows, cols, kind=None):
    return q("Find the product.", "diagram", "____", "", "multiply_grid",
              {"rows": rows, "cols": cols, "kind": kind or random.choice(["apple", "star", "balloon", "flower"])})


def _groups(groups, size, kind=None, text="Find the total in all the groups."):
    return q(text, "diagram", "____", "", "repeated_groups",
              {"groups": groups, "size": size, "kind": kind or random.choice(["apple", "star", "balloon"])})


# ───────────────────────── 24A: Concept & Tables 2-5 ─────────────────────────

def _24A(sheet):
    tiers = {1: (2, 3), 2: (2, 4), 3: (2, 5), 4: (3, 5)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        factor = random.randint(lo, hi)
        other = random.randint(2, 6)
        if i % 2 == 0:
            items.append(_groups(other, factor))
        else:
            items.append(_grid(factor, other))
    return items


# ───────────────────────── 24B: Tables 6-10 ─────────────────────────

def _24B(sheet):
    tiers = {1: (6, 7), 2: (6, 8), 3: (7, 9), 4: (8, 10)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        factor = random.randint(lo, hi)
        other = random.randint(2, 6)
        if i % 2 == 0:
            items.append(_grid(factor, other))
        else:
            items.append(_groups(other, factor))
    return items


# ───────────────────────── 24C: Multi-digit & Word Problems ─────────────────────────

def _24C(sheet):
    tiers = {1: (2, 6), 2: (3, 8), 3: (4, 9), 4: (5, 10)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        if i % 3 == 0:
            items.append(_groups(a, b, text="How many are there in total?"))
        else:
            items.append(_grid(a, b))
    return items


# ───────────────────────── 24D: Patterns & Speed ─────────────────────────

def _24D(sheet):
    tiers = {1: (2, 5), 2: (2, 8), 3: (3, 9), 4: (4, 10)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        if i % 4 == 0:
            step = random.randint(2, 9)
            start = step * random.randint(1, 4)
            seq = [start + j * step for j in range(4)]
            blank_pos = random.choice([1, 2, 3])
            seq_display = list(seq)
            seq_display[blank_pos] = None
            items.append(q("Find the missing number in the pattern.", "diagram", "____", "", "sequence_boxes",
                            {"seq": seq_display, "label": "pattern"}))
        else:
            a = random.randint(lo, hi)
            b = random.randint(lo, hi)
            items.append(q("Multiply quickly.", "diagram", "____", "", "multiply_grid",
                            {"rows": a, "cols": b, "kind": random.choice(["apple", "star"])}))
    return items


# ───────────────────────── 24E: Picture Puzzles & Mixed Challenge ─────────────────────────

def _24E(sheet):
    tiers = {1: (2, 6), 2: (3, 8), 3: (4, 9), 4: (5, 10)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        variant = i % 3
        if variant == 0:
            items.append(q("Solve the picture puzzle.", "diagram", "____", "", "repeated_groups",
                            {"groups": a, "size": b, "kind": random.choice(["apple", "flower", "balloon"])}))
        elif variant == 1:
            items.append(_grid(a, b))
        else:
            step = random.randint(2, 8)
            start = step * random.randint(1, 4)
            seq = [start + j * step for j in range(4)]
            blank_pos = random.choice([1, 2, 3])
            seq_display = list(seq)
            seq_display[blank_pos] = None
            items.append(q("Find the missing number in the pattern.", "diagram", "____", "", "sequence_boxes",
                            {"seq": seq_display, "label": "pattern"}))
    return items


_SUBLEVEL_BUILDERS = {
    "A": _24A, "B": _24B, "C": _24C, "D": _24D, "E": _24E,
}

_TOPIC_NAMES = {
    "A": "Multiplication Concept & Tables 2-5",
    "B": "Tables 6-10",
    "C": "Multi-digit & Word Problems",
    "D": "Patterns & Speed",
    "E": "Picture Puzzles & Mixed Challenge",
}


def build_v3_sheet(code, sheet):
    random.seed(24000 + hash(code) % 5000 + sheet * 31)
    items = _SUBLEVEL_BUILDERS[code](sheet)
    return items[:20]


LEVEL24_V3_DISPATCH = {
    f"__L24__{code}": {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SUBLEVEL_BUILDERS
}
