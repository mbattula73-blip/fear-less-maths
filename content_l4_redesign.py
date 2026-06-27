"""
Fear Less Maths — LEVEL 24 ("Pre Level 4" — Multiplication, Class 1-2)
Same conventions as content_pre.py / content_l1/2/3_redesign.py.
Registered as a brand-new level using namespaced plain-letter codes
(__L24__A, __L24__B...) so it never collides with any other level,
including the original, untouched Level 4.

Sub-level list:
  A  Multiplication concept (small arrays)   B  Tables 2-5
  C  Tables 6-10
  CUM1  Review: Tables
  D  Multiplication practice (mixed tables)  E  Multi-digit (bigger grids)
  F  Word problems (same visuals, bigger range)
  CUM2  Review: Practice/Multi-digit/Word problems
  G  Multiplication patterns (skip counting)
  H  Speed multiplication
  I  Picture puzzles
  CUM3  Review: Patterns/Speed/Puzzles
  J  Mixed challenge
  REV  Level 24 Revision
"""
import random
from content import cb, tb, q

OBJ_KINDS = ["apple", "star", "balloon", "flower"]


def _kind(i):
    return OBJ_KINDS[i % len(OBJ_KINDS)]


def _mult_q(rows, cols, kind):
    return q("Multiply the rows.", "diagram", "____", "", "multiply_grid",
              {"rows": rows, "cols": cols, "kind": kind})


def _seq_mult_q(seq, label="pattern"):
    return q("Find the missing number in the pattern.", "diagram", "____",
              "", "sequence_boxes", {"seq": seq, "label": label})


def _A_s(sheet):
    random.seed(10 + sheet)
    if sheet == 1:
        items = [cb("Multiplication Concept",
                     ["Multiplying means adding equal groups together.",
                      "Count the rows, then count how many in each row."], "")]
    elif sheet == 2:
        items = [cb("Equal Groups", ["Each row is one equal group."], "")]
    elif sheet == 3:
        items = [tb("Concept Tips", ["Count one row, then count how many rows there are."])]
    else:
        items = [cb("Concept - Speed Round", ["Multiply quickly and check your total."], "")]
    pairs = [(random.randint(2, 3), random.randint(2, 4)) for _ in range(19)]
    for idx, (r, c) in enumerate(pairs):
        items.append(_mult_q(r, c, _kind(idx)))
    return items


def _tables_block(lo, hi, sheet, title):
    random.seed(hash(title) % 1000 + sheet)
    if sheet == 1:
        items = [cb(title, ["Each row has the same number of objects."], "")]
    elif sheet == 2:
        items = [cb(f"{title} - Practice", ["Count rows, then count objects in one row."], "")]
    elif sheet == 3:
        items = [tb(f"{title} Tips", ["Multiply rows by the number in one row."])]
    else:
        items = [cb(f"{title} - Speed Round", ["Multiply quickly and check your total."], "")]
    for idx in range(19):
        table_num = random.randint(lo, hi)
        rows = random.randint(1, 10)
        items.append(_mult_q(rows, table_num, _kind(idx)))
    return items


def _B_s(sheet): return _tables_block(2, 5, sheet, "Tables 2-5")
def _C_s(sheet): return _tables_block(6, 10, sheet, "Tables 6-10")


def _CUM1_s(sheet):
    random.seed(100 + sheet)
    items = [cb("Review: Tables 2-10", ["Mix of small and bigger tables."], "")] if sheet != 3 else \
        [tb("Review Tips", ["Count rows, then multiply by the row size."])]
    for idx in range(19):
        table_num = random.randint(2, 10)
        rows = random.randint(1, 10)
        items.append(_mult_q(rows, table_num, _kind(idx)))
    return items


def _D_s(sheet):
    random.seed(200 + sheet)
    items = [cb("Multiplication Practice", ["Mixed tables, all sizes."], "")] if sheet != 3 else \
        [tb("Practice Tips", ["Take your time and count carefully."])]
    for idx in range(19):
        items.append(_mult_q(random.randint(2, 9), random.randint(2, 9), _kind(idx)))
    return items


def _E_s(sheet):
    random.seed(300 + sheet)
    items = [cb("Multi-Digit Multiplication", ["Bigger groups - count carefully."], "")] if sheet != 3 else \
        [tb("Tips", ["Use the rows of 5 (or 10) inside the grid to count faster."])]
    for idx in range(19):
        items.append(_mult_q(random.randint(6, 9), random.randint(6, 9), _kind(idx)))
    return items


def _F_s(sheet):
    random.seed(400 + sheet)
    items = [cb("Picture Word Problems", ["Each picture tells a multiplication story."], "")] if sheet != 3 else \
        [tb("Tips", ["Rows = groups. Columns = how many in each group."])]
    for idx in range(19):
        items.append(_mult_q(random.randint(2, 8), random.randint(2, 8), _kind(idx)))
    return items


def _CUM2_s(sheet):
    random.seed(500 + sheet)
    items = [cb("Review: Practice & Multi-Digit", ["Mix of all sizes."], "")] if sheet != 3 else \
        [tb("Review Tips", ["Count carefully, row by row."])]
    for idx in range(19):
        items.append(_mult_q(random.randint(2, 9), random.randint(2, 9), _kind(idx)))
    return items


def _G_s(sheet):
    random.seed(600 + sheet)
    items = [cb("Multiplication Patterns",
                 ["Skip counting by a number IS multiplying by that number."], "")] if sheet != 3 else \
        [tb("Pattern Tips", ["Each jump is the same size - that size is the table number."])]
    for i in range(19):
        step = random.choice([2,3,4,5,10])
        start = step * random.randint(1, 5)
        seq = [start, start+step, start+step*2, start+step*3]
        hide = random.randint(1, 3)
        seq_display = [v if j != hide else None for j, v in enumerate(seq)]
        items.append(_seq_mult_q(seq_display, "pattern"))
    return items


def _H_s(sheet):
    random.seed(700 + sheet)
    items = [cb("Speed Multiplication", ["Work quickly and check your answer."], "")] if sheet != 3 else \
        [tb("Speed Tips", ["Count fast but carefully."])]
    for idx in range(19):
        items.append(_mult_q(random.randint(2, 10), random.randint(2, 10), _kind(idx)))
    return items


def _I_s(sheet):
    random.seed(800 + sheet)
    items = [cb("Picture Puzzles", ["Look carefully, then multiply."], "")] if sheet != 3 else \
        [tb("Puzzle Tips", ["Count the rows first, then the columns."])]
    for idx in range(19):
        items.append(_mult_q(random.randint(2, 8), random.randint(2, 8), _kind(idx)))
    return items


def _CUM3_s(sheet):
    random.seed(900 + sheet)
    items = [cb("Review: Patterns, Speed & Puzzles", ["Mix of all three skills."], "")] if sheet != 3 else \
        [tb("Review Tips", ["Patterns jump by the table number. Grids show rows x columns."])]
    for i in range(19):
        if i % 2 == 0:
            items.append(_mult_q(random.randint(2, 9), random.randint(2, 9), _kind(i)))
        else:
            step = random.choice([2,3,4,5])
            start = step * random.randint(1, 6)
            seq = [start, start+step, start+step*2, start+step*3]
            hide = random.randint(1, 3)
            seq_display = [v if j != hide else None for j, v in enumerate(seq)]
            items.append(_seq_mult_q(seq_display, "pattern"))
    return items


def _J_s(sheet):
    random.seed(1000 + sheet)
    items = [cb("Mixed Challenge", ["Every multiplication skill, mixed together."], "")]
    for idx in range(19):
        items.append(_mult_q(random.randint(2, 10), random.randint(2, 10), _kind(idx)))
    return items


def _REV_s(sheet):
    random.seed(1100 + sheet)
    items = [cb("Level 24 Revision", ["Tables, patterns, and bigger grids, all mixed."], "")]
    for i in range(19):
        if i % 4 == 3:
            step = random.choice([2,3,4,5,10])
            start = step * random.randint(1, 5)
            seq = [start, start+step, start+step*2, start+step*3]
            hide = random.randint(1, 3)
            seq_display = [v if j != hide else None for j, v in enumerate(seq)]
            items.append(_seq_mult_q(seq_display, "pattern"))
        else:
            items.append(_mult_q(random.randint(2, 10), random.randint(2, 10), _kind(i)))
    return items


def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL24_NS = "__L24__"

LEVEL4_DISPATCH = {
    f"{LEVEL24_NS}A": _wrap(_A_s), f"{LEVEL24_NS}B": _wrap(_B_s), f"{LEVEL24_NS}C": _wrap(_C_s),
    f"{LEVEL24_NS}CUM1": _wrap(_CUM1_s),
    f"{LEVEL24_NS}D": _wrap(_D_s), f"{LEVEL24_NS}E": _wrap(_E_s), f"{LEVEL24_NS}F": _wrap(_F_s),
    f"{LEVEL24_NS}CUM2": _wrap(_CUM2_s),
    f"{LEVEL24_NS}G": _wrap(_G_s), f"{LEVEL24_NS}H": _wrap(_H_s), f"{LEVEL24_NS}I": _wrap(_I_s),
    f"{LEVEL24_NS}CUM3": _wrap(_CUM3_s),
    f"{LEVEL24_NS}J": _wrap(_J_s), f"{LEVEL24_NS}REV": _wrap(_REV_s),
}
