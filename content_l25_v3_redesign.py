"""
Fear Less Maths — LEVEL 25 (Pre Level 5 — Division) v3 architecture
(2026-08-06)

Per direct request: consolidated from 10 core sublevels down to 5
(old A/H, C/J, and B/D/G each duplicated framing). Merged by SKILL,
sheets carry the difficulty escalation.

  25A  Equal Grouping & Sharing   (was A,B)
  25B  Remainders                 (was C,D)
  25C  Bar Models & Fact Families (was E,F)
  25D  Word Problems & Speed      (was G,H)
  25E  Picture Puzzles & Mixed Challenge (was I,J)

100% diagrammatic. Diagram audit: object_group (reused from counting,
no leaked text), sharing_baskets (scattered pile + empty basket
outlines, no per-basket answer shown -- the child must share it
themselves), division_bar_model (bar split into segments, total
labeled, '?' in one segment, never the per-segment value), multiply_grid
(reused from Level 24, no text) -- all already correctly designed,
no leaks.
"""
import random
from content import q


def _grouping(count, group_size, kind=None, label="Find the number of groups."):
    return q(label, "diagram", "____", "", "object_group",
              {"count": count, "kind": kind or random.choice(["apple", "star", "balloon", "flower"]), "group_size": group_size})


def _sharing(total, num_baskets, kind=None, label="Share the pile equally."):
    return q(label, "diagram", "____", "", "sharing_baskets",
              {"total": total, "num_baskets": num_baskets, "kind": kind or random.choice(["apple", "star", "balloon", "flower"])})


def _remainder_group(count, group_size, kind=None):
    return q("Find the groups and the remainder.", "diagram", "____", "", "object_group",
              {"count": count, "kind": kind or random.choice(["apple", "star", "balloon"]), "group_size": group_size, "icon_label": "divide"})


def _remainder_share(total, num_baskets, kind=None):
    return q("Share equally and find what's left.", "diagram", "____", "", "sharing_baskets",
              {"total": total, "num_baskets": num_baskets, "kind": kind or random.choice(["flower", "star", "apple"])})


def _bar_model(total, parts):
    return q("Find the value of one part.", "diagram", "____", "", "division_bar_model",
              {"total": total, "parts": parts})


def _fact_grid(rows, cols, kind=None):
    return q("Multiply the rows.", "diagram", "____", "", "multiply_grid",
              {"rows": rows, "cols": cols, "kind": kind or random.choice(["apple", "flower", "star"])})


def _fact_group(count, group_size, kind=None):
    return q("Now find the number of groups.", "diagram", "____", "", "object_group",
              {"count": count, "kind": kind or random.choice(["apple", "flower", "star"]), "group_size": group_size, "icon_label": "divide"})


# ───────────────────────── 25A: Equal Grouping & Sharing ─────────────────────────

def _25A(sheet):
    tiers = {1: [(6, 2), (6, 3), (8, 2), (8, 4)], 2: [(10, 2), (10, 5), (12, 3), (12, 4)],
             3: [(15, 3), (15, 5), (16, 4), (18, 3)], 4: [(20, 4), (20, 5), (24, 4), (24, 6)]}
    pool = tiers[sheet]
    items = []
    for i in range(20):
        total, gs = random.choice(pool)
        num_baskets = total // gs
        if i % 2 == 0:
            items.append(_grouping(total, gs))
        else:
            items.append(_sharing(total, num_baskets, label="Share the pile equally among the baskets."))
    return items


# ───────────────────────── 25B: Remainders ─────────────────────────

def _25B(sheet):
    tiers = {1: (10, 20), 2: (15, 30), 3: (20, 40), 4: (25, 50)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        gs = random.choice([2, 3, 4, 5])
        total = random.randint(lo, hi)
        if total % gs == 0:
            total += random.randint(1, gs - 1)
        if i % 2 == 0:
            items.append(_remainder_group(total, gs))
        else:
            num_baskets = random.choice([2, 3, 4])
            items.append(_remainder_share(total, num_baskets))
    return items


# ───────────────────────── 25C: Bar Models & Fact Families ─────────────────────────

def _25C(sheet):
    tiers = {1: [(6, 2), (6, 3), (8, 2), (10, 2)], 2: [(12, 3), (12, 4), (15, 3), (16, 4)],
             3: [(18, 3), (20, 4), (21, 3), (24, 4)], 4: [(24, 6), (30, 5), (32, 4), (36, 6)]}
    pool = tiers[sheet]
    items = []
    for i in range(20):
        total, parts = random.choice(pool)
        if i % 3 == 2:
            rows = parts
            cols = total // parts
            items.append(_fact_grid(rows, cols))
        else:
            items.append(_bar_model(total, parts))
    return items


# ───────────────────────── 25D: Word Problems & Speed ─────────────────────────

def _25D(sheet):
    tiers = {1: [(6, 2), (8, 4), (10, 2), (12, 3)], 2: [(12, 4), (15, 3), (16, 4), (18, 3)],
             3: [(18, 6), (20, 4), (21, 3), (24, 4)], 4: [(24, 6), (28, 4), (30, 5), (32, 4)]}
    pool = tiers[sheet]
    items = []
    for i in range(20):
        total, gs = random.choice(pool)
        num_baskets = total // gs
        variant = i % 3
        if variant == 0:
            items.append(_sharing(total, num_baskets, label="Share the apples equally among the baskets."))
        elif variant == 1:
            items.append(_grouping(total, gs, label="Find the number of groups, quickly."))
        else:
            items.append(_bar_model(total, num_baskets))
    return items


# ───────────────────────── 25E: Picture Puzzles & Mixed Challenge ─────────────────────────

def _25E(sheet):
    tiers = {1: (10, 20), 2: (12, 28), 3: (16, 36), 4: (20, 48)}
    lo, hi = tiers[sheet]
    items = []
    for i in range(20):
        gs = random.choice([2, 3, 4, 5, 6])
        total = random.randint(lo, hi)
        variant = i % 4
        if variant == 0:
            items.append(_grouping(total, gs, label="Solve the picture puzzle: find the groups."))
        elif variant == 1:
            has_rem = total % gs != 0
            items.append(_remainder_group(total, gs) if has_rem else _grouping(total, gs))
        elif variant == 2:
            num_baskets = max(2, total // gs)
            items.append(_sharing(total, num_baskets, label="Share the pile equally."))
        else:
            parts = random.choice([2, 3, 4])
            clean_total = parts * random.randint(3, 9)
            items.append(_bar_model(clean_total, parts))
    return items


_SUBLEVEL_BUILDERS = {
    "A": _25A, "B": _25B, "C": _25C, "D": _25D, "E": _25E,
}

_TOPIC_NAMES = {
    "A": "Equal Grouping & Sharing",
    "B": "Remainders",
    "C": "Bar Models & Fact Families",
    "D": "Word Problems & Speed",
    "E": "Picture Puzzles & Mixed Challenge",
}


def build_v3_sheet(code, sheet):
    random.seed(25000 + hash(code) % 5000 + sheet * 31)
    items = _SUBLEVEL_BUILDERS[code](sheet)
    return items[:20]


LEVEL25_V3_DISPATCH = {
    f"__L25__{code}": {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SUBLEVEL_BUILDERS
}
