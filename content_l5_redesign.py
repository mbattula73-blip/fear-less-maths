"""
Fear Less Maths — LEVEL 25 ("Pre Level 5" — Division, Class 1-2)
Same conventions as content_pre.py / content_l1-4_redesign.py.
Registered as a brand-new level using namespaced plain-letter codes
(__L25__A, __L25__B...) so it never collides with any other level,
including the original, untouched Level 5.

Division-as-sharing reuses the equal-grouping diagram (object_group)
already used for Level 22's factor-intro and Level 24's multiplication
concept -- division is the same picture, just asking a different
question (how many groups / how many in each group, instead of the
total). Remainder questions use a total that does NOT divide evenly,
so the final row is naturally a partial "leftover" group, with the
answer label asking for both the group count and the leftover.

Sub-level list:
  A  Division concept (sharing)         B  Division - single digit
  C  Division with remainder
  CUM1  Review: A/B/C
  D  Long division (bigger numbers)     E  Multiplication & Division link
  F  Picture word problems
  CUM2  Review: D/E/F
  G  Missing numbers (find the divisor or quotient)
  H  Speed division
  I  Picture puzzles
  CUM3  Review: G/H/I
  J  Mixed challenge
  REV  Level 25 Revision
"""
import random
from content import cb, tb, q

OBJ_KINDS = ["apple", "star", "balloon", "flower"]


def _kind(i):
    return OBJ_KINDS[i % len(OBJ_KINDS)]


def _div_q(total, group_size, ans="____"):
    """Division-as-sharing: total objects arranged in rows of group_size.
    Quotient = number of rows. ans label can request remainder too."""
    return q("Share into equal groups.", "diagram", ans, "", "object_group",
              {"count": total, "kind": _kind(total), "group_size": group_size, "icon_label": "divide"})


def _mult_q(rows, cols):
    return q("Multiply the rows.", "diagram", "____", "", "multiply_grid",
              {"rows": rows, "cols": cols, "kind": _kind(rows+cols)})


def _seq_q(seq, label="pattern"):
    return q("Find the missing number in the pattern.", "diagram", "____",
              "", "sequence_boxes", {"seq": seq, "label": label})


# ───────────────────────── A: Division concept ─────────────────────────

def _A_s(sheet):
    random.seed(10 + sheet)
    if sheet == 1:
        items = [cb("Division Concept",
                     ["Dividing means sharing into equal groups.",
                      "Count how many groups, or how many in each group."], "")]
    elif sheet == 2:
        items = [cb("Sharing Equally", ["Each row is one equal share."], "")]
    elif sheet == 3:
        items = [tb("Concept Tips", ["Count the rows — that is how many equal groups you made."])]
    else:
        items = [cb("Concept — Speed Round", ["Share quickly and check your count."], "")]
    for idx in range(19):
        gs = random.choice([2, 3])
        groups = random.randint(2, 4)
        items.append(_div_q(gs*groups, gs))
    return items


# ───────────────────────── B: Single digit division ─────────────────────────

def _B_s(sheet):
    random.seed(100 + sheet)
    if sheet == 1:
        items = [cb("Division — Single Digit", ["Share a small group equally."], "")]
    elif sheet == 2:
        items = [cb("Division — Practice", ["Count the rows to find the answer."], "")]
    elif sheet == 3:
        items = [tb("Tips", ["Divisor = size of each group. Quotient = number of groups."])]
    else:
        items = [cb("Division — Speed Round", ["Share quickly and check your count."], "")]
    for idx in range(19):
        gs = random.choice([2,3,4,5])
        groups = random.randint(1, 4)
        items.append(_div_q(gs*groups, gs))
    return items


# ───────────────────────── C: Division with remainder ─────────────────────────

def _C_s(sheet):
    random.seed(200 + sheet)
    if sheet == 1:
        items = [cb("Division With Remainder",
                     ["Sometimes objects don't share equally.",
                      "Full rows are the groups. Leftover objects are the remainder."], "")]
    elif sheet == 2:
        items = [cb("Remainder — Practice", ["The last partial row is what's left over."], "")]
    elif sheet == 3:
        items = [tb("Remainder Tips", ["Count full rows for groups, then count what's left."])]
    else:
        items = [cb("Remainder — Speed Round", ["Find groups and leftover quickly."], "")]
    for idx in range(19):
        gs = random.choice([2,3,4])
        groups = random.randint(2, 4)
        leftover = random.randint(1, gs - 1)
        total = gs*groups + leftover
        items.append(_div_q(total, gs, ans="____  R ____"))
    return items


def _CUM1_s(sheet):
    random.seed(300 + sheet)
    items = [cb("Review: Division Basics", ["Mix of even sharing and remainders."], "")] if sheet != 3 else \
        [tb("Review Tips", ["Count full rows first, then any leftover."])]
    for idx in range(19):
        gs = random.choice([2,3,4,5])
        groups = random.randint(1, 4)
        if idx % 3 == 0:
            leftover = random.randint(1, gs - 1)
            items.append(_div_q(gs*groups + leftover, gs, ans="____  R ____"))
        else:
            items.append(_div_q(gs*groups, gs))
    return items


# ───────────────────────── D: Long division (bigger numbers) ─────────────────────────

def _D_s(sheet):
    random.seed(400 + sheet)
    items = [cb("Bigger Sharing", ["The same rule works for bigger groups."], "")] if sheet != 3 else \
        [tb("Tips", ["Count the rows carefully — there may be many."])]
    for idx in range(19):
        gs = random.choice([2,3,4,5])
        groups = random.randint(5, 9)
        items.append(_div_q(gs*groups, gs))
    return items


# ───────────────────────── E: Multiplication & Division link ─────────────────────────

def _E_s(sheet):
    random.seed(500 + sheet)
    items = [cb("Multiplication & Division Together",
                 ["Multiplying joins equal groups. Dividing splits them apart.",
                  "They are opposite actions."], "")] if sheet != 3 else \
        [tb("Tips", ["If 3 groups of 4 = 12, then 12 shared into 3 groups = 4."])]
    for idx in range(19):
        gs = random.choice([2,3,4,5])
        groups = random.randint(2, 6)
        if idx % 2 == 0:
            items.append(_mult_q(groups, gs))
        else:
            items.append(_div_q(gs*groups, gs))
    return items


# ───────────────────────── F: Picture word problems ─────────────────────────

def _F_s(sheet):
    random.seed(600 + sheet)
    items = [cb("Picture Word Problems", ["Each picture tells a sharing story."], "")] if sheet != 3 else \
        [tb("Tips", ["Count the rows for the answer."])]
    for idx in range(19):
        gs = random.choice([2,3,4,5])
        groups = random.randint(2, 6)
        items.append(_div_q(gs*groups, gs))
    return items


def _CUM2_s(sheet):
    random.seed(700 + sheet)
    items = [cb("Review: Long Division & Word Problems", ["Mix of bigger sharing and multiplication links."], "")] \
        if sheet != 3 else [tb("Review Tips", ["Multiplication and division undo each other."])]
    for idx in range(19):
        gs = random.choice([2,3,4,5])
        groups = random.randint(2, 8)
        if idx % 3 == 0:
            items.append(_mult_q(groups, gs))
        else:
            items.append(_div_q(gs*groups, gs))
    return items


# ───────────────────────── G: Missing numbers ─────────────────────────

def _G_s(sheet):
    random.seed(800 + sheet)
    items = [cb("Missing Numbers",
                 ["Look at the picture and find the missing piece of the equation."], "")] if sheet != 3 else \
        [tb("Tips", ["Count the rows and the group size separately."])]
    for idx in range(19):
        gs = random.choice([2,3,4,5])
        groups = random.randint(2, 6)
        items.append(_div_q(gs*groups, gs))
    return items


# ───────────────────────── H: Speed ─────────────────────────

def _H_s(sheet):
    random.seed(900 + sheet)
    items = [cb("Speed Division", ["Work quickly and check your count."], "")] if sheet != 3 else \
        [tb("Speed Tips", ["Count fast but carefully."])]
    for idx in range(19):
        gs = random.choice([2,3,4,5,10])
        groups = random.randint(2, 8)
        items.append(_div_q(gs*groups, gs))
    return items


# ───────────────────────── I: Puzzles ─────────────────────────

def _I_s(sheet):
    random.seed(1000 + sheet)
    items = [cb("Picture Puzzles", ["Look carefully, then share equally."], "")] if sheet != 3 else \
        [tb("Puzzle Tips", ["Check for a remainder before you answer."])]
    for idx in range(19):
        gs = random.choice([2,3,4])
        groups = random.randint(2, 5)
        if idx % 3 == 0:
            leftover = random.randint(1, gs - 1)
            items.append(_div_q(gs*groups + leftover, gs, ans="____  R ____"))
        else:
            items.append(_div_q(gs*groups, gs))
    return items


def _CUM3_s(sheet):
    random.seed(1100 + sheet)
    items = [cb("Review: Missing Numbers, Speed & Puzzles", ["Mix of all three skills."], "")] if sheet != 3 else \
        [tb("Review Tips", ["Take your time and check for remainders."])]
    for idx in range(19):
        gs = random.choice([2,3,4,5])
        groups = random.randint(2, 7)
        if idx % 4 == 0:
            leftover = random.randint(1, gs - 1)
            items.append(_div_q(gs*groups + leftover, gs, ans="____  R ____"))
        else:
            items.append(_div_q(gs*groups, gs))
    return items


# ───────────────────────── J/REV: Mixed ─────────────────────────

def _J_s(sheet):
    random.seed(1200 + sheet)
    items = [cb("Mixed Challenge", ["Every division skill, mixed together."], "")]
    for idx in range(19):
        gs = random.choice([2,3,4,5])
        groups = random.randint(2, 8)
        choice = idx % 3
        if choice == 0:
            leftover = random.randint(1, gs - 1)
            items.append(_div_q(gs*groups + leftover, gs, ans="____  R ____"))
        elif choice == 1:
            items.append(_mult_q(groups, gs))
        else:
            items.append(_div_q(gs*groups, gs))
    return items


def _REV_s(sheet):
    random.seed(1300 + sheet)
    items = [cb("Level 25 Revision", ["Sharing, remainders, and the link to multiplication."], "")]
    for idx in range(19):
        gs = random.choice([2,3,4,5])
        groups = random.randint(2, 8)
        choice = idx % 4
        if choice == 0:
            leftover = random.randint(1, gs - 1)
            items.append(_div_q(gs*groups + leftover, gs, ans="____  R ____"))
        elif choice == 1:
            items.append(_mult_q(groups, gs))
        elif choice == 2:
            step = random.choice([2,3,4,5])
            start = step * random.randint(1, 5)
            seq = [start, start+step, start+step*2, start+step*3]
            hide = random.randint(1, 3)
            seq_display = [v if j != hide else None for j, v in enumerate(seq)]
            items.append(_seq_q(seq_display, "pattern"))
        else:
            items.append(_div_q(gs*groups, gs))
    return items


# ───────────────────────── Dispatcher ─────────────────────────

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL25_NS = "__L25__"

LEVEL5_DISPATCH = {
    f"{LEVEL25_NS}A": _wrap(_A_s), f"{LEVEL25_NS}B": _wrap(_B_s), f"{LEVEL25_NS}C": _wrap(_C_s),
    f"{LEVEL25_NS}CUM1": _wrap(_CUM1_s),
    f"{LEVEL25_NS}D": _wrap(_D_s), f"{LEVEL25_NS}E": _wrap(_E_s), f"{LEVEL25_NS}F": _wrap(_F_s),
    f"{LEVEL25_NS}CUM2": _wrap(_CUM2_s),
    f"{LEVEL25_NS}G": _wrap(_G_s), f"{LEVEL25_NS}H": _wrap(_H_s), f"{LEVEL25_NS}I": _wrap(_I_s),
    f"{LEVEL25_NS}CUM3": _wrap(_CUM3_s),
    f"{LEVEL25_NS}J": _wrap(_J_s), f"{LEVEL25_NS}REV": _wrap(_REV_s),
}
