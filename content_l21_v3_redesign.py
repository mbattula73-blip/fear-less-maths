"""
Fear Less Maths — LEVEL 21 (Pre Level 1 — Counting & Numbers) v3
architecture (2026-08-06)

Per direct request: consolidated from 17 core sublevels down to 5,
removing heavy repetition (the old A/B/C all opened "Count the
objects", E/F/G all opened "Find the number before", etc). Merged by
SKILL rather than narrow numeric range -- the 4 sheets (Intuition ->
Concept -> Practice -> Mastery) now carry the difficulty escalation
that used to require separate sublevels.

  21A  Counting 1-100        (was A,B,C -- range escalates via sheets)
  21B  Before/After/Between  (was D,E,F,G)
  21C  Greater/Smaller       (was H,I)
  21D  Missing Numbers & Patterns (was J,K,L,M)
  21E  Place Value & Mixed Challenge (was N,O,P,Q)

100% diagrammatic (every one of the 20 questions has a diagram) --
this level is EXCLUDED from the standard PICTORIAL_LEVELS abstract-
fade (see get_questions() in content.py) per direct request, so no
question silently loses its diagram.

REAL LEAK FOUND AND FIXED (diagram_engine.py): ten_frames always
printed "Count = {count}" directly on the image for "Count the
objects" questions -- the exact skill being tested was handed away.
Removed the text entirely; the other 7 Pre-Level diagram types
(object_group, base10_blocks, visual_equation, compare_choice,
numline_jump, sequence_boxes, compare_blocks) were already correctly
designed with no leaks.

Diagram box enlarged (pdf_engine.py, new `pre_level_diag` category,
80x34mm) -- 6 of these 8 types had never been box-categorized at all
and were rendering at the smallest possible default box (68x18mm),
the opposite of what young children need.
"""
import random
from content import q


# ───────────────────────── 21A: Counting 1-100 ─────────────────────────

def _21A(sheet):
    tiers = {1: (1, 20), 2: (10, 50), 3: (30, 80), 4: (50, 100)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        n = random.randint(lo, hi)
        if n <= 20:
            items.append(q("Count the objects.", "diagram", "____", "", "object_group",
                            {"count": n, "kind": random.choice(["apple", "star", "balloon", "flower"]), "group_size": 5}))
        else:
            items.append(q("Count the dots.", "diagram", "____", "", "ten_frames", {"count": n}))
    return items


# ───────────────────────── 21B: Before/After/Between ─────────────────────────

def _21B(sheet):
    tiers = {1: (1, 20), 2: (10, 50), 3: (30, 80), 4: (50, 99)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        n = random.randint(lo, hi)
        mode = random.choice(["after", "before", "between"])
        if mode == "after":
            seq = [n, None]
            label = "after"
        elif mode == "before":
            seq = [None, n]
            label = "before"
        else:
            seq = [n - 1, None, n + 1]
            label = "missing"
        items.append(q("Fill in the missing number.", "diagram", "____", "", "sequence_boxes",
                        {"seq": seq, "label": label}))
    return items


# ───────────────────────── 21C: Greater/Smaller ─────────────────────────

def _21C(sheet):
    tiers = {1: (1, 15), 2: (5, 20), 3: (15, 60), 4: (30, 99)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        while a == b:
            b = random.randint(lo, hi)
        if hi <= 20:
            items.append(q("Compare. Tick >, < or =.", "diagram", "____", "", "compare_choice",
                            {"left_count": a, "right_count": b, "kind": random.choice(["apple", "star", "balloon"])}))
        else:
            items.append(q("Compare. Tick >, < or =.", "diagram", "____", "", "compare_blocks",
                            {"left": a, "right": b}))
    return items


# ───────────────────────── 21D: Missing Numbers & Patterns ─────────────────────────

def _21D(sheet):
    tiers = {1: (1, 20, 1), 2: (10, 50, 2), 3: (20, 80, 5), 4: (10, 90, 10)}
    lo, hi, default_step = tiers[sheet]
    items = []
    for i in range(20):
        use_pattern = i % 2 == 1 or sheet >= 3
        step = random.choice([2, 5, 10]) if use_pattern else 1
        start = random.randint(lo, max(lo, hi - step * 4))
        seq = [start + j * step for j in range(4)]
        blank_pos = random.choice([1, 2, 3])
        seq_display = list(seq)
        seq_display[blank_pos] = None
        label = "pattern" if use_pattern else "missing"
        items.append(q("Find the missing number." if not use_pattern else "Find the missing number in the pattern.",
                        "diagram", "____", "", "sequence_boxes",
                        {"seq": seq_display, "label": label}))
    return items


# ───────────────────────── 21E: Place Value & Mixed Challenge ─────────────────────────

def _21E(sheet):
    tiers = {1: (1, 20), 2: (10, 50), 3: (20, 80), 4: (30, 99)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        n = random.randint(lo, hi)
        variant = i % 4
        if variant == 0:
            tens, ones = divmod(n, 10)
            items.append(q("Find the value (Tens & Ones).", "diagram", "____", "", "base10_blocks",
                            {"tens": tens, "ones": ones}))
        elif variant == 1:
            if n <= 20:
                items.append(q("Count the objects.", "diagram", "____", "", "object_group",
                                {"count": n, "kind": random.choice(["apple", "star", "flower"]), "group_size": 5}))
            else:
                items.append(q("Count the dots.", "diagram", "____", "", "ten_frames", {"count": n}))
        elif variant == 2:
            step = random.choice([1, 2, 5])
            seq = [n, n + step, None, n + 3 * step]
            items.append(q("Find the missing number.", "diagram", "____", "", "sequence_boxes",
                            {"seq": seq, "label": "pattern"}))
        else:
            a, b = n, random.randint(lo, hi)
            while a == b:
                b = random.randint(lo, hi)
            if hi <= 20:
                items.append(q("Compare. Tick >, < or =.", "diagram", "____", "", "compare_choice",
                                {"left_count": a, "right_count": b, "kind": "apple"}))
            else:
                items.append(q("Compare. Tick >, < or =.", "diagram", "____", "", "compare_blocks",
                                {"left": a, "right": b}))
    return items


_SUBLEVEL_BUILDERS = {
    "A": _21A, "B": _21B, "C": _21C, "D": _21D, "E": _21E,
}

_TOPIC_NAMES = {
    "A": "Counting 1-100",
    "B": "Before, After & Between",
    "C": "Greater or Smaller",
    "D": "Missing Numbers & Patterns",
    "E": "Place Value & Mixed Challenge",
}


def build_v3_sheet(code, sheet):
    random.seed(21000 + hash(code) % 5000 + sheet * 31)
    items = _SUBLEVEL_BUILDERS[code](sheet)
    return items[:20]


LEVEL21_V3_DISPATCH = {
    f"__L21__{code}": {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SUBLEVEL_BUILDERS
}
