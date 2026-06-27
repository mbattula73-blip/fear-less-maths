"""
Fear Less Maths — LEVEL 22 ("Pre Level 2" — Even, Odd & Primes, Class 1-2)
Same conventions as content_pre.py / content_l1_redesign.py:
  - Every question has an image AND a short instruction line (not bold,
    same size as the question number).
  - Black-and-white, outline-only diagrams (ink-saving).
  - A mascot+flag-on-a-stick appears above every question, naming the
    skill in 1-3 keywords.
  - Registered as a brand-new level using namespaced plain-letter codes
    (__L22__A, __L22__B...) so they never collide with Pre-Level (0),
    Pre Level 1 / Level 21, or the original, untouched Level 2.

Sub-level list:
  A  Pairing objects 1-10 (concrete)      B  Pairing objects 11-20
  CUM1  Review: Pairing/Even/Odd
  C  Even/Odd patterns (skip count by 2)  D  Even/Odd — bigger numbers
  CUM2  Review: Even/Odd
  E  Equal grouping (factors intro)
  F  Prime numbers (array = single line)  G  Composite numbers (array = grid)
  CUM3  Review: Prime/Composite
  H  Prime factor practice
  I  Picture puzzles
  J  Mixed challenge
  REV  Level 22 Revision
"""
import random
from content import cb, tb, q

OBJ_KINDS = ["apple", "star", "balloon", "flower"]


def _kind(i):
    return OBJ_KINDS[i % len(OBJ_KINDS)]


def _pair_q(n, kind):
    return q("Is this even or odd?", "diagram", "____", "", "pair_grouping",
              {"count": n, "kind": kind})


def _array_q(n, rows):
    return q("Is this number prime?", "diagram", "____", "", "array_grid",
              {"n": n, "rows": rows})


def _group_q(n, group_size, kind):
    return q("Find the group size.", "diagram", "____", "", "object_group",
              {"count": n, "kind": kind, "group_size": group_size})


def _eq_q(left, right, kind, op):
    text = "Add the numbers." if op == "+" else "Subtract the numbers."
    return q(text, "diagram", "____", "", "visual_equation",
              {"left": left, "right": right, "kind": kind, "op": op})


# Smallest prime factor (other than 1 and n) for composite numbers up to 40,
# used to pick a sensible `rows` value for array_grid. Primes map to rows=1.
_PRIMES = {2,3,5,7,11,13,17,19,23,29,31,37}
def _smallest_factor(n):
    """Returns a factor close to sqrt(n) for a compact, near-square grid
    (e.g. 12 -> 3 or 4, not the lopsided 2x6). Primes map to rows=1."""
    if n in _PRIMES or n < 2:
        return 1
    best = 1
    for f in range(2, int(n**0.5) + 1):
        if n % f == 0:
            best = f
    return best if best > 1 else 1


# ───────────────────────── A/B: Pairing objects (concrete) ─────────────────────────

def _pairing_block(lo, hi, sheet):
    random.seed(lo * 7 + sheet)
    picks = [random.choice(range(lo, hi + 1)) for _ in range(19)]
    titles = {1: "Pairing Objects", 2: "Pairing in Rows", 3: "Pairing Tips", 4: "Even or Odd — Fast"}
    if sheet == 1:
        items = [cb("Pairing Objects",
                     ["Put the objects into pairs of 2.",
                      "If every object has a partner, it is EVEN.",
                      "If one is left over, it is ODD."],
                     "")]
    elif sheet == 2:
        items = [cb("Pairing in Rows", ["Loop each pair. Count the loops, then check for a leftover."], "")]
    elif sheet == 3:
        items = [tb("Pairing Tips", ["No leftover = EVEN.", "One leftover = ODD."])]
    else:
        items = [cb("Even or Odd — Fast Round", ["Decide quickly: paired evenly, or one left over?"], "")]
    for idx, n in enumerate(picks):
        items.append(_pair_q(n, _kind(idx)))
    return items


def _A_s(sheet): return _pairing_block(1, 10, sheet)
def _B_s(sheet): return _pairing_block(11, 20, sheet)


def _CUM1_s(sheet):
    random.seed(100 + sheet)
    picks = [random.choice(range(1, 21)) for _ in range(19)]
    items = [cb("Review: Pairing & Even/Odd", ["Mix of small and bigger groups."], "")] if sheet != 3 else \
        [tb("Review Tips", ["Always loop pairs first, then look for a leftover."])]
    for idx, n in enumerate(picks):
        items.append(_pair_q(n, _kind(idx)))
    return items


# ───────────────────────── C/D: Even/Odd patterns & bigger numbers ─────────────────────────

def _C_s(sheet):
    """Even/Odd patterns: skip counting by 2, shown as sequence boxes."""
    random.seed(300 + sheet)
    items = [cb("Even Number Patterns",
                 ["Even numbers go 2, 4, 6, 8... jumping by 2 each time."],
                 "") if sheet == 1 else
             cb("Odd Number Patterns",
                 ["Odd numbers go 1, 3, 5, 7... jumping by 2 each time."], "")
             if sheet == 2 else
             tb("Pattern Tips", ["Every even/odd sequence jumps by 2."]) if sheet == 3 else
             cb("Even/Odd Patterns — Speed Round", ["Find the missing number quickly."], "")]
    for i in range(19):
        start = random.randint(1, 40)
        if sheet in (1, 4):
            start = start - (start % 2)  # force even
        else:
            start = start - (start % 2) + 1  # force odd
        seq = [start, start+2, start+4, start+6]
        hide = random.randint(1, 3)
        seq_display = [v if j != hide else None for j, v in enumerate(seq)]
        items.append(q("Find the missing number in the pattern.", "diagram", "____",
                        "", "sequence_boxes", {"seq": seq_display, "label": "pattern"}))
    return items


def _D_s(sheet):
    """Even/Odd with bigger numbers (21-50), still using pair_grouping."""
    random.seed(400 + sheet)
    picks = [random.choice(range(21, 51)) for _ in range(19)]
    if sheet == 1:
        items = [cb("Even or Odd — Bigger Numbers", ["The same rule works for any size of number."], "")]
    elif sheet == 2:
        items = [cb("Even or Odd — Practice", ["Pair up as many as you can, then check the last one."], "")]
    elif sheet == 3:
        items = [tb("Tip", ["A number is EVEN if its last digit is 0,2,4,6,8.",
                             "A number is ODD if its last digit is 1,3,5,7,9."])]
    else:
        items = [cb("Even or Odd — Mastery", ["Decide using the last digit rule."], "")]
    for idx, n in enumerate(picks):
        # cap visual pairing to a manageable count for legibility; bigger
        # numbers still get the same picture logic, just capped at 20 objects
        items.append(_pair_q(min(n, 20), _kind(idx)))
    return items


def _CUM2_s(sheet):
    random.seed(500 + sheet)
    items = [cb("Review: Even & Odd", ["Mix of patterns and pairing."], "")] if sheet != 3 else \
        [tb("Review Tips", ["No leftover = EVEN. One leftover = ODD."])]
    for i in range(19):
        if i % 2 == 0:
            n = random.randint(1, 20)
            items.append(_pair_q(n, _kind(i)))
        else:
            start = random.randint(1, 40)
            start = start - (start % 2)
            seq = [start, start+2, start+4, start+6]
            hide = random.randint(1, 3)
            seq_display = [v if j != hide else None for j, v in enumerate(seq)]
            items.append(q("Find the missing number in the pattern.", "diagram", "____",
                            "", "sequence_boxes", {"seq": seq_display, "label": "pattern"}))
    return items


# ───────────────────────── E: Equal grouping (factors intro) ─────────────────────────

def _E_s(sheet):
    random.seed(600 + sheet)
    if sheet == 1:
        items = [cb("Equal Grouping",
                     ["Some numbers can be split into equal groups.",
                      "Count how many are in each group."], "")]
        pairs = [(12,3),(10,2),(15,3),(8,2),(9,3),(6,2),(14,2),(18,3)]
    elif sheet == 2:
        items = [cb("Equal Grouping — Practice", ["Look at the rows. Each row is one group."], "")]
        pairs = [(16,4),(20,4),(12,4),(9,3),(15,5),(10,5),(18,2),(21,3)]
    elif sheet == 3:
        items = [tb("Grouping Tips", ["Count the objects in just ONE group — every group is the same size."])]
        pairs = [(24,4),(28,4),(27,3),(32,4),(35,5),(30,5)]
    else:
        items = [cb("Equal Grouping — Speed Round", ["Work out the group size quickly."], "")]
        pairs = [(36,4),(40,4),(45,5),(25,5),(33,3),(22,2)]
    random.seed(650 + sheet)
    while len(pairs) < 19:
        gs = random.choice([2,3,4,5])
        groups = random.randint(2,5)
        pairs.append((gs*groups, gs))
    for n, gs in pairs[:19]:
        items.append(_group_q(n, gs, _kind(n)))
    return items


# ───────────────────────── F/G: Prime / Composite (array shape) ─────────────────────────

def _F_s(sheet):
    """Prime numbers — array always shows a single straight line (1 row)."""
    random.seed(700 + sheet)
    primes_pool = [2,3,5,7,11,13,17,19,23]
    if sheet == 1:
        items = [cb("Prime Numbers",
                     ["A PRIME number can only be drawn as ONE straight line.",
                      "It cannot be arranged into a rectangle."], "")]
    elif sheet == 2:
        items = [cb("Spotting Primes", ["If the dots make a single line, it is PRIME."], "")]
    elif sheet == 3:
        items = [tb("Prime Tips", ["A single straight line of dots = PRIME."])]
    else:
        items = [cb("Primes — Speed Round", ["Decide quickly: line or grid?"], "")]
    random.seed(750 + sheet)
    picks = [random.choice(primes_pool) for _ in range(19)]
    for n in picks:
        items.append(_array_q(n, 1))
    return items


def _G_s(sheet):
    """Composite numbers — array always shows a multi-row grid."""
    random.seed(800 + sheet)
    composites_pool = [4,6,8,9,10,12,14,15,16,18,20,21,22,24,25,26,27,28]
    if sheet == 1:
        items = [cb("Composite Numbers",
                     ["A COMPOSITE number can be arranged into a rectangle (grid).",
                      "It has more than one row."], "")]
    elif sheet == 2:
        items = [cb("Spotting Composites", ["If the dots make a grid with 2+ rows, it is COMPOSITE."], "")]
    elif sheet == 3:
        items = [tb("Composite Tips", ["A grid (2 or more rows) = COMPOSITE."])]
    else:
        items = [cb("Composites — Speed Round", ["Decide quickly: line or grid?"], "")]
    random.seed(850 + sheet)
    picks = [random.choice(composites_pool) for _ in range(19)]
    for n in picks:
        items.append(_array_q(n, _smallest_factor(n)))
    return items


def _CUM3_s(sheet):
    random.seed(900 + sheet)
    pool = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    items = [cb("Review: Prime & Composite", ["Mix of lines and grids."], "")] if sheet != 3 else \
        [tb("Review Tips", ["Line = PRIME.  Grid = COMPOSITE."])]
    picks = [random.choice(pool) for _ in range(19)]
    for n in picks:
        items.append(_array_q(n, _smallest_factor(n)))
    return items


# ───────────────────────── H: Prime factor practice ─────────────────────────

def _H_s(sheet):
    random.seed(1000 + sheet)
    if sheet == 1:
        items = [cb("Breaking Numbers Into Groups",
                     ["Composite numbers can be split into equal groups.",
                      "Find how many groups, or how many in each group."], "")]
        pairs = [(12,3),(8,2),(15,3),(20,4),(9,3),(10,2),(14,2),(18,3)]
    elif sheet == 2:
        items = [cb("Factor Practice", ["Each row shows one equal group."], "")]
        pairs = [(16,4),(21,3),(25,5),(24,4),(27,3),(28,4)]
    elif sheet == 3:
        items = [tb("Factor Tips", ["Count objects in one group — that's the group size."])]
        pairs = [(30,5),(32,4),(35,5),(36,4),(40,4)]
    else:
        items = [cb("Factors — Speed Round", ["Work quickly and check your count."], "")]
        pairs = [(45,5),(33,3),(22,2),(26,2),(34,2)]
    random.seed(1050 + sheet)
    while len(pairs) < 19:
        gs = random.choice([2,3,4,5])
        groups = random.randint(2,6)
        pairs.append((gs*groups, gs))
    for n, gs in pairs[:19]:
        items.append(_group_q(n, gs, _kind(n)))
    return items


# ───────────────────────── I: Picture puzzles ─────────────────────────

def _I_s(sheet):
    random.seed(1100 + sheet)
    items = [cb("Picture Puzzles", ["Look carefully, then decide."], "")] if sheet != 3 else \
        [tb("Puzzle Tips", ["Pairing tells you EVEN/ODD. The dot shape tells you PRIME/COMPOSITE."])]
    for i in range(19):
        choice = i % 3
        if choice == 0:
            items.append(_pair_q(random.randint(1, 20), _kind(i)))
        elif choice == 1:
            n = random.choice([2,3,4,5,6,7,8,9,10,11,12,13,14,15])
            items.append(_array_q(n, _smallest_factor(n)))
        else:
            items.append(_eq_q(random.randint(1, 15), random.randint(1, 5), _kind(i),
                                "+" if i % 2 == 0 else "-"))
    return items


# ───────────────────────── J: Mixed challenge ─────────────────────────

def _J_s(sheet):
    random.seed(1200 + sheet)
    items = [cb("Mixed Challenge", ["Even/odd, prime/composite, grouping, and equations all mixed."], "")]
    builders = [
        lambda: _pair_q(random.randint(1, 20), _kind(random.randint(0,3))),
        lambda: (lambda n: _array_q(n, _smallest_factor(n)))(random.choice([2,3,5,6,7,8,9,10,11,12])),
        lambda: _group_q(random.choice([6,8,9,10,12,14,15,16]), random.choice([2,3,4]), _kind(random.randint(0,3))),
        lambda: _eq_q(random.randint(1,15), random.randint(1,5), _kind(random.randint(0,3)),
                       "+" if random.random() > 0.5 else "-"),
    ]
    for i in range(19):
        items.append(builders[i % len(builders)]())
    return items


def _REV_s(sheet):
    random.seed(1300 + sheet)
    items = [cb("Level 22 Revision", ["Every skill from this level, mixed together."], "")]
    builders = [
        lambda: _pair_q(random.randint(1, 20), _kind(random.randint(0,3))),
        lambda: (lambda n: _array_q(n, _smallest_factor(n)))(random.choice([2,3,4,5,6,7,8,9,10,11,12,13,14,15])),
        lambda: _group_q(random.choice([6,8,9,10,12,14,15,16,18,20]), random.choice([2,3,4,5]), _kind(random.randint(0,3))),
        lambda: _eq_q(random.randint(1,15), random.randint(1,5), _kind(random.randint(0,3)),
                       "+" if random.random() > 0.5 else "-"),
        lambda: (lambda s: q("Find the missing number in the pattern.", "diagram", "____", "",
                              "sequence_boxes", {"seq": [s, s+2, None, s+6], "label": "pattern"}))(
                              (random.randint(1,20) // 2) * 2),
    ]
    for i in range(19):
        items.append(builders[i % len(builders)]())
    return items


# ───────────────────────── Dispatcher ─────────────────────────

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL22_NS = "__L22__"

LEVEL2_DISPATCH = {
    f"{LEVEL22_NS}A": _wrap(_A_s), f"{LEVEL22_NS}B": _wrap(_B_s),
    f"{LEVEL22_NS}CUM1": _wrap(_CUM1_s),
    f"{LEVEL22_NS}C": _wrap(_C_s), f"{LEVEL22_NS}D": _wrap(_D_s),
    f"{LEVEL22_NS}CUM2": _wrap(_CUM2_s),
    f"{LEVEL22_NS}E": _wrap(_E_s),
    f"{LEVEL22_NS}F": _wrap(_F_s), f"{LEVEL22_NS}G": _wrap(_G_s),
    f"{LEVEL22_NS}CUM3": _wrap(_CUM3_s),
    f"{LEVEL22_NS}H": _wrap(_H_s),
    f"{LEVEL22_NS}I": _wrap(_I_s), f"{LEVEL22_NS}J": _wrap(_J_s),
    f"{LEVEL22_NS}REV": _wrap(_REV_s),
}
