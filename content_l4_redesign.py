"""
Fear Less Maths — LEVEL 24 ("Pre Level 4" — Multiplication, Class 1-2)
Same conventions as content_pre.py / content_l1/2/3_redesign.py.
Registered as a brand-new level using namespaced plain-letter codes
(__L24__A, __L24__B...) so it never collides with any other level,
including the original, untouched Level 4.

Redesigned so every sub-level has its own visual identity and matching
instruction, instead of one generic "Multiply the rows" grid repeated
everywhere:
  - Concept / Word Problems / Puzzles -> repeated_groups (separate
    clusters, "x N" labeled) -- bridges from addition's separate piles
    into the idea of equal groups.
  - Tables / Practice / Multi-digit / Speed -> multiply_grid (a packed
    array) -- the more abstract "rows x cols" representation, used once
    children already grasp what a group of N looks like.
  - Patterns -> sequence_boxes (skip-counting, already visually distinct).

Sub-level list:
  A  Multiplication concept (equal groups)   B  Tables 2-5
  C  Tables 6-10
  CUM1  Review: Tables
  D  Multiplication practice (mixed tables)  E  Multi-digit (bigger grids)
  F  Picture word problems (equal groups)
  CUM2  Review: Practice/Multi-digit/Word problems
  G  Multiplication patterns (skip counting)
  H  Speed multiplication
  I  Picture puzzles (equal groups)
  CUM3  Review: Patterns/Speed/Puzzles
  J  Mixed challenge
  REV  Level 24 Revision
"""
import random
from content import cb, tb, q

OBJ_KINDS = ["apple", "star", "balloon", "flower"]


def _kind(i):
    return OBJ_KINDS[i % len(OBJ_KINDS)]


def _grid_q(rows, cols, text="Find the product."):
    return q(text, "diagram", "____", "", "multiply_grid",
              {"rows": rows, "cols": cols, "kind": _kind(rows + cols)})


def _groups_q(groups, size, text="Find the total in all the groups."):
    return q(text, "diagram", "____", "", "repeated_groups",
              {"groups": groups, "size": size, "kind": _kind(groups + size)})


def _seq_mult_q(seq, label="pattern"):
    return q("Find the missing number in the pattern.", "diagram", "____",
              "", "sequence_boxes", {"seq": seq, "label": label})


def _A_s(sheet):
    random.seed(10 + sheet)
    if sheet == 1:
        items = [cb("Multiplication Concept",
                     ["A group of objects repeated many times is multiplication.",
                      "Count the groups, then count how many in one group."], "")]
    elif sheet == 2:
        items = [cb("Equal Groups - Practice", ["Each basket has the same number inside."], "")]
    elif sheet == 3:
        items = [tb("Concept Tips", ["Number of groups x size of one group = total."])]
    else:
        items = [cb("Concept - Speed Round", ["Work out the total quickly."], "")]
    for idx in range(19):
        groups = random.randint(2, 4)
        size = random.randint(2, 4)
        items.append(_groups_q(groups, size))
    return items


def _tables_block(lo, hi, sheet, title):
    random.seed(hash(title) % 1000 + sheet)
    if sheet == 1:
        items = [cb(title, ["Each row of the grid has the same number of dots."], "")]
    elif sheet == 2:
        items = [cb(f"{title} - Practice", ["Count the rows, then count one row."], "")]
    elif sheet == 3:
        items = [tb(f"{title} Tips", ["Rows x objects-per-row = the product."])]
    else:
        items = [cb(f"{title} - Speed Round", ["Find the product quickly."], "")]
    for idx in range(19):
        table_num = random.randint(lo, hi)
        rows = random.randint(1, 10)
        items.append(_grid_q(rows, table_num))
    return items


def _B_s(sheet): return _tables_block(2, 5, sheet, "Tables 2-5")
def _C_s(sheet): return _tables_block(6, 10, sheet, "Tables 6-10")


def _CUM1_s(sheet):
    random.seed(100 + sheet)
    items = [cb("Review: Tables 2-10", ["Mix of small and bigger tables."], "")] if sheet != 3 else \
        [tb("Review Tips", ["Rows x objects-per-row = the product."])]
    for idx in range(19):
        table_num = random.randint(2, 10)
        rows = random.randint(1, 10)
        items.append(_grid_q(rows, table_num))
    return items


def _D_s(sheet):
    random.seed(200 + sheet)
    items = [cb("Multiplication Practice", ["Mixed tables, all sizes."], "")] if sheet != 3 else \
        [tb("Practice Tips", ["Take your time and count carefully."])]
    for idx in range(19):
        items.append(_grid_q(random.randint(2, 9), random.randint(2, 9)))
    return items


def _E_s(sheet):
    random.seed(300 + sheet)
    items = [cb("Multi-Digit Multiplication", ["Bigger grids - count carefully, row by row."], "")] \
        if sheet != 3 else [tb("Tips", ["Look for rows of 5 or 10 inside the grid to count faster."])]
    for idx in range(19):
        items.append(_grid_q(random.randint(6, 9), random.randint(6, 9)))
    return items


def _F_s(sheet):
    random.seed(400 + sheet)
    if sheet == 1:
        items = [cb("Picture Word Problems",
                     ["Imagine each group is a basket, a bag, or a box.",
                      "Find how many objects there are altogether."], "")]
        text = "How many are there in total?"
    elif sheet == 2:
        items = [cb("Word Problems - Practice", ["Count the groups, then the objects in one group."], "")]
        text = "How many are there in total?"
    elif sheet == 3:
        items = [tb("Tips", ["Groups x size of one group = the total."])]
        text = "Find the total."
    else:
        items = [cb("Word Problems - Speed Round", ["Work out the total quickly."], "")]
        text = "Find the total."
    for idx in range(19):
        groups = random.randint(2, 6)
        size = random.randint(2, 8)
        items.append(_groups_q(groups, size, text))
    return items


def _CUM2_s(sheet):
    random.seed(500 + sheet)
    items = [cb("Review: Practice, Multi-Digit & Word Problems", ["Mix of grids and equal groups."], "")] \
        if sheet != 3 else [tb("Review Tips", ["Whichever picture you see, multiply groups by size."])]
    for idx in range(19):
        if idx % 2 == 0:
            items.append(_grid_q(random.randint(2, 9), random.randint(2, 9)))
        else:
            items.append(_groups_q(random.randint(2, 6), random.randint(2, 6),
                                    "How many are there in total?"))
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
        items.append(_grid_q(random.randint(2, 10), random.randint(2, 10), "Multiply quickly."))
    return items


def _I_s(sheet):
    random.seed(800 + sheet)
    items = [cb("Picture Puzzles", ["Look carefully at the groups, then solve."], "")] if sheet != 3 else \
        [tb("Puzzle Tips", ["Count the groups first, then the size of one group."])]
    for idx in range(19):
        groups = random.randint(2, 5)
        size = random.randint(2, 6)
        items.append(_groups_q(groups, size, "Solve the picture puzzle."))
    return items


def _CUM3_s(sheet):
    random.seed(900 + sheet)
    items = [cb("Review: Patterns, Speed & Puzzles", ["Mix of all three skills."], "")] if sheet != 3 else \
        [tb("Review Tips", ["Patterns jump by the table number. Pictures show groups x size."])]
    for i in range(19):
        choice = i % 3
        if choice == 0:
            items.append(_grid_q(random.randint(2, 9), random.randint(2, 9), "Multiply quickly."))
        elif choice == 1:
            items.append(_groups_q(random.randint(2, 5), random.randint(2, 6), "Solve the picture puzzle."))
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
        choice = idx % 3
        if choice == 0:
            items.append(_grid_q(random.randint(2, 10), random.randint(2, 10)))
        elif choice == 1:
            items.append(_groups_q(random.randint(2, 6), random.randint(2, 6),
                                    "How many are there in total?"))
        else:
            step = random.choice([2,3,4,5,10])
            start = step * random.randint(1, 5)
            seq = [start, start+step, start+step*2, start+step*3]
            hide = random.randint(1, 3)
            seq_display = [v if j != hide else None for j, v in enumerate(seq)]
            items.append(_seq_mult_q(seq_display, "pattern"))
    return items


def _REV_s(sheet):
    random.seed(1100 + sheet)
    items = [cb("Level 24 Revision", ["Tables, equal groups, and patterns, all mixed."], "")]
    for i in range(19):
        choice = i % 4
        if choice == 0:
            step = random.choice([2,3,4,5,10])
            start = step * random.randint(1, 5)
            seq = [start, start+step, start+step*2, start+step*3]
            hide = random.randint(1, 3)
            seq_display = [v if j != hide else None for j, v in enumerate(seq)]
            items.append(_seq_mult_q(seq_display, "pattern"))
        elif choice == 1:
            items.append(_groups_q(random.randint(2, 6), random.randint(2, 6),
                                    "How many are there in total?"))
        else:
            items.append(_grid_q(random.randint(2, 10), random.randint(2, 10)))
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
