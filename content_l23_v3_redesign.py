"""
Fear Less Maths — LEVEL 23 (Pre Level 3 — Addition & Subtraction) v3
architecture (2026-08-06)

Per direct request: consolidated from 10 core sublevels down to 5
(old A/B/E all opened "Add the numbers", C/D/F/H/J all opened
"Subtract the numbers" -- just 2 question styles spread across 10
sublevels). Merged by SKILL, sheets carry the difficulty escalation.

  23A  Addition            (was A,B,E -- single digit through carrying)
  23B  Subtraction         (was C,D,F -- single digit through borrowing)
  23C  Carrying & Borrowing (mixed, tougher than A/B on their own)
  23D  Speed Addition & Subtraction (was G,H)
  23E  Picture Puzzles & Mixed Challenge (was I,J)

100% diagrammatic (Level 23 already excluded from the PICTORIAL_LEVELS
abstract-fade). Diagram type used throughout: `visual_equation`,
already audited safe during Level 21's work (no answer text, empty
answer box only).
"""
import random
from content import q


def _visual(left, right, op, kind=None):
    return q("Add the numbers." if op == "+" else "Subtract the numbers.",
              "diagram", "____", "", "visual_equation",
              {"left": left, "right": right, "kind": kind or random.choice(["apple", "star", "balloon", "flower"]), "op": op})


# ───────────────────────── 23A: Addition ─────────────────────────

def _23A(sheet):
    def _carry_pair():
        a = random.randint(15, 84)
        hi_b = max(15, 99 - a)
        b = random.randint(15, hi_b)
        return a, b

    items = []
    for i in range(20):
        if sheet == 1:
            a, b = random.randint(1, 9), random.randint(1, 9)
        elif sheet == 2:
            a = random.randint(10, 40)
            b = random.randint(10, min(40, 89 - a))
        elif sheet == 3:
            a = random.randint(20, 60)
            b = random.randint(10, min(35, 89 - a))
        else:
            a, b = _carry_pair()
        items.append(_visual(a, b, "+"))
    return items


# ───────────────────────── 23B: Subtraction ─────────────────────────

def _23B(sheet):
    items = []
    for i in range(20):
        if sheet == 1:
            a = random.randint(2, 9)
            b = random.randint(1, a)
        elif sheet == 2:
            a = random.randint(20, 50)
            b = random.randint(10, min(a, 30))
        elif sheet == 3:
            a = random.randint(30, 70)
            b = random.randint(10, min(a, 40))
        else:
            # borrowing likely: units digit of b > units digit of a
            a = random.randint(21, 90)
            b = random.randint(max(1, a - 60), a - 1)
        items.append(_visual(a, b, "-"))
    return items


# ───────────────────────── 23C: Carrying & Borrowing ─────────────────────────

def _23C(sheet):
    tiers = {1: (10, 40), 2: (15, 60), 3: (20, 75), 4: (25, 90)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        op = "+" if i % 2 == 0 else "-"
        if op == "+":
            a = random.randint(lo, hi)
            ones_a = a % 10
            # force a carry: ones_a + ones_b >= 10, so ones_b in
            # [max(1, 10-ones_a), 9] (clamped so the low end never
            # exceeds 9, e.g. when ones_a=0).
            ones_b_lo = min(max(1, 10 - ones_a), 9)
            ones_b = random.randint(ones_b_lo, 9)
            tens_b_max = max(0, (99 - a - ones_b) // 10)
            tens_b = random.randint(0, tens_b_max) if tens_b_max > 0 else 0
            b = max(1, tens_b * 10 + ones_b)
            items.append(_visual(a, b, "+"))
        else:
            a = random.randint(lo + 10, hi + 10)
            ones_a = a % 10
            if ones_a >= 9:
                # no ones digit can force a borrow against a 9 -- just
                # use a plain, still-valid subtraction instead.
                b = random.randint(1, a - 1)
            else:
                # force a borrow: ones_b in [ones_a+1, 9]
                ones_b = random.randint(ones_a + 1, 9)
                tens_a = a // 10
                tens_b = random.randint(0, min(tens_a, 9))
                b = tens_b * 10 + ones_b
                if b >= a:
                    b = max(1, a - 1)
            items.append(_visual(a, b, "-"))
    return items


# ───────────────────────── 23D: Speed Addition & Subtraction ─────────────────────────

def _23D(sheet):
    tiers = {1: (1, 15), 2: (5, 30), 3: (10, 50), 4: (15, 70)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        op = "+" if i % 2 == 0 else "-"
        if op == "+":
            a = random.randint(lo, hi)
            b = random.randint(lo, hi)
        else:
            a = random.randint(lo, hi)
            b = random.randint(1, a) if a > 1 else 1
        items.append(_visual(a, b, op))
    return items


# ───────────────────────── 23E: Picture Puzzles & Mixed Challenge ─────────────────────────

def _23E(sheet):
    tiers = {1: (5, 25), 2: (10, 40), 3: (20, 60), 4: (25, 90)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        op = random.choice(["+", "-"])
        if op == "+":
            a = random.randint(lo, hi)
            b = random.randint(lo, max(lo, min(hi, 99 - a)))
        else:
            a = random.randint(lo, hi)
            b = random.randint(1, a)
        items.append(_visual(a, b, op))
    return items


_SUBLEVEL_BUILDERS = {
    "A": _23A, "B": _23B, "C": _23C, "D": _23D, "E": _23E,
}

_TOPIC_NAMES = {
    "A": "Addition",
    "B": "Subtraction",
    "C": "Carrying & Borrowing",
    "D": "Speed Addition & Subtraction",
    "E": "Picture Puzzles & Mixed Challenge",
}


def build_v3_sheet(code, sheet):
    random.seed(23000 + hash(code) % 5000 + sheet * 31)
    items = _SUBLEVEL_BUILDERS[code](sheet)
    return items[:20]


LEVEL23_V3_DISPATCH = {
    f"__L23__{code}": {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SUBLEVEL_BUILDERS
}
