"""
Fear Less Maths — LEVEL 25 ("Pre Level 5" — Division, Class 1-2)

Redesigned based on Singapore Math / Maths-No-Problem research: division
has TWO distinct conceptual structures that should be taught as separate,
visually distinct experiences, not one repeated picture:

  - EQUAL GROUPING ("how many groups?") -- objects are arranged into
    rows of a KNOWN size; the child counts the rows. Research (Maths
    No Problem) suggests teaching grouping FIRST for deeper conceptual
    understanding, since sharing is over-relied on by default.
  - EQUAL SHARING ("how many in each?") -- a fixed number of empty
    containers is shown alongside a SCATTERED (not pre-arranged) pile;
    the child must mentally distribute the pile evenly. This is
    visually different on purpose -- it does not hand the grouping to
    the child the way the grouping picture does.

Singapore Math's signature pictorial-to-abstract bridge, the BAR MODEL
(a rectangle split into equal segments with the total above and a "?"
in one segment), is introduced as its own sub-level rather than skipped.

Same conventions as content_pre.py / content_l1-4_redesign.py otherwise:
every question has an image + short instruction, mascot above every
question, black-and-white outline-only diagrams. Registered as Level 25
using namespaced plain-letter codes so it never collides with any other
level, including the original, untouched Level 5.

Sub-level list:
  A  Equal Grouping (how many groups?)      B  Equal Sharing (how many each?)
  CUM1  Review: Grouping vs Sharing
  C  Division with remainder - Grouping     D  Division with remainder - Sharing
  CUM2  Review: Remainders
  E  Bar Model division (Singapore method)  F  Multiplication & Division fact families
  CUM3  Review: Bar Models & Fact Families
  G  Real-life word problems (varied themes: sweets, apples, balloons, books)
  H  Speed division
  I  Picture puzzles
  J  Mixed challenge
  REV  Level 25 Revision
"""
import random
from content import cb, tb, q

OBJ_KINDS = ["apple", "star", "balloon", "flower"]


def _kind(i):
    return OBJ_KINDS[i % len(OBJ_KINDS)]


def _group_q(total, group_size, text="Find the number of groups.", ans="____"):
    """Equal GROUPING: objects pre-arranged into rows of group_size."""
    return q(text, "diagram", ans, "", "object_group",
              {"count": total, "kind": _kind(total), "group_size": group_size, "icon_label": "divide"})


def _share_q(total, num_baskets, text="Share the pile equally.", ans="____"):
    """Equal SHARING: scattered pile + empty baskets, not pre-arranged."""
    return q(text, "diagram", ans, "", "sharing_baskets",
              {"total": total, "num_baskets": num_baskets, "kind": _kind(total + num_baskets)})


def _bar_q(total, parts):
    return q("Find the value of one part.", "diagram", "____", "", "division_bar_model",
              {"total": total, "parts": parts})


def _mult_q(rows, cols):
    return q("Multiply the rows.", "diagram", "____", "", "multiply_grid",
              {"rows": rows, "cols": cols, "kind": _kind(rows + cols)})


# ───────────────────────── A: Equal Grouping ─────────────────────────

def _A_s(sheet):
    random.seed(10 + sheet)
    if sheet == 1:
        items = [cb("Equal Grouping",
                     ["Make groups that are all the same size.",
                      "Count how many groups you made."], "")]
    elif sheet == 2:
        items = [cb("Grouping — Practice", ["Each row is one group of the same size."], "")]
    elif sheet == 3:
        items = [tb("Grouping Tips", ["Count the rows — that is how many groups."])]
    else:
        items = [cb("Grouping — Speed Round", ["Count the groups quickly."], "")]
    for idx in range(19):
        gs = random.choice([2, 3, 4])
        groups = random.randint(2, 5)
        items.append(_group_q(gs*groups, gs))
    return items


# ───────────────────────── B: Equal Sharing ─────────────────────────

def _B_s(sheet):
    random.seed(100 + sheet)
    if sheet == 1:
        items = [cb("Equal Sharing",
                     ["Share the whole pile evenly among the baskets.",
                      "Every basket must end up with the same amount."], "")]
    elif sheet == 2:
        items = [cb("Sharing — Practice", ["Picture sharing one object at a time into each basket."], "")]
    elif sheet == 3:
        items = [tb("Sharing Tips", ["Count the whole pile first, then think how to split it evenly."])]
    else:
        items = [cb("Sharing — Speed Round", ["Share quickly and check your count."], "")]
    for idx in range(19):
        nb = random.choice([2, 3, 4])
        per = random.randint(2, 5)
        items.append(_share_q(nb*per, nb))
    return items


def _CUM1_s(sheet):
    random.seed(200 + sheet)
    items = [cb("Review: Grouping vs Sharing",
                 ["Grouping asks 'how many groups?'. Sharing asks 'how many in each?'."], "")] \
        if sheet != 3 else [tb("Review Tips", ["Same total, two different questions."])]
    for idx in range(19):
        gs = random.choice([2, 3, 4])
        n = random.randint(2, 5)
        if idx % 2 == 0:
            items.append(_group_q(gs*n, gs))
        else:
            items.append(_share_q(gs*n, gs))
    return items


# ───────────────────────── C/D: Division with remainder ─────────────────────────

def _C_s(sheet):
    """Remainder - Grouping: leftover objects don't fill a complete row."""
    random.seed(300 + sheet)
    items = [cb("Remainder — Grouping",
                 ["Full rows are complete groups.",
                  "Leftover objects that don't fill a row are the remainder."], "")] \
        if sheet != 3 else [tb("Tips", ["Count full rows for groups, then count what's left over."])]
    for idx in range(19):
        gs = random.choice([2, 3, 4])
        groups = random.randint(2, 4)
        leftover = random.randint(1, gs - 1)
        items.append(_group_q(gs*groups + leftover, gs,
                               "Find the groups and the remainder.", ans="____  R ____"))
    return items


def _D_s(sheet):
    """Remainder - Sharing: pile can't be shared perfectly evenly."""
    random.seed(400 + sheet)
    items = [cb("Remainder — Sharing",
                 ["Sometimes a pile cannot be shared perfectly evenly.",
                  "Share as much as possible, then count what's left."], "")] \
        if sheet != 3 else [tb("Tips", ["Share evenly first, then see how many are left over."])]
    for idx in range(19):
        nb = random.choice([2, 3, 4])
        per = random.randint(2, 4)
        leftover = random.randint(1, nb - 1)
        items.append(_share_q(nb*per + leftover, nb,
                               "Share equally and find what's left.", ans="____  R ____"))
    return items


def _CUM2_s(sheet):
    random.seed(500 + sheet)
    items = [cb("Review: Remainders", ["Mix of grouping and sharing, both with leftovers."], "")] \
        if sheet != 3 else [tb("Review Tips", ["Always count the leftover separately from the groups."])]
    for idx in range(19):
        gs = random.choice([2, 3, 4])
        n = random.randint(2, 4)
        leftover = random.randint(1, gs - 1)
        if idx % 2 == 0:
            items.append(_group_q(gs*n + leftover, gs, "Find the groups and the remainder.", ans="____  R ____"))
        else:
            items.append(_share_q(gs*n + leftover, gs, "Share equally and find what's left.", ans="____  R ____"))
    return items


# ───────────────────────── E: Bar Model ─────────────────────────

def _E_s(sheet):
    random.seed(600 + sheet)
    if sheet == 1:
        items = [cb("Bar Model Division",
                     ["The bar shows the WHOLE amount, split into equal parts.",
                      "Find the value of just one part."], "")]
    elif sheet == 2:
        items = [cb("Bar Model — Practice", ["Every part of the bar is the same size."], "")]
    elif sheet == 3:
        items = [tb("Bar Model Tips", ["Total divided by the number of parts = one part's value."])]
    else:
        items = [cb("Bar Model — Speed Round", ["Work out one part quickly."], "")]
    for idx in range(19):
        parts = random.choice([2, 3, 4, 5])
        per = random.randint(2, 9)
        items.append(_bar_q(parts*per, parts))
    return items


# ───────────────────────── F: Multiplication & Division fact families ─────────────────────────

def _F_s(sheet):
    random.seed(700 + sheet)
    items = [cb("Fact Families",
                 ["Multiplication and division are opposite actions.",
                  "If 3 groups of 4 make 12, then 12 shared into 3 groups makes 4 each."], "")] \
        if sheet != 3 else [tb("Tips", ["The same three numbers connect a multiplication and a division fact."])]
    for idx in range(19):
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        if idx % 2 == 0:
            items.append(_mult_q(a, b))
        else:
            items.append(_group_q(a*b, b))
    return items


def _CUM3_s(sheet):
    random.seed(800 + sheet)
    items = [cb("Review: Bar Models & Fact Families", ["Mix of both skills."], "")] \
        if sheet != 3 else [tb("Review Tips", ["A bar's total split evenly is the same as division."])]
    for idx in range(19):
        choice = idx % 3
        if choice == 0:
            parts = random.choice([2, 3, 4, 5])
            items.append(_bar_q(parts * random.randint(2, 8), parts))
        elif choice == 1:
            a, b = random.randint(2, 9), random.randint(2, 9)
            items.append(_mult_q(a, b))
        else:
            a, b = random.randint(2, 9), random.randint(2, 9)
            items.append(_group_q(a*b, b))
    return items


# ───────────────────────── G: Real-life word problems (varied themes) ─────────────────────────

def _G_s(sheet):
    """Varied real-life contexts via object kind rotation + alternating
    grouping/sharing framing, per Singapore Math's emphasis on relatable
    contexts (sweets among friends, apples in baskets, etc)."""
    random.seed(900 + sheet)
    themes = [
        ("apple", "Share the apples equally among the baskets."),
        ("star", "Group the stickers into equal packs."),
        ("balloon", "Share the balloons equally among the children."),
        ("flower", "Group the flowers into equal bunches."),
    ]
    items = [cb("Real-Life Word Problems",
                 ["Picture real things: sweets, apples, balloons, flowers.",
                  "Decide if you are grouping or sharing, then solve."], "")] if sheet != 3 else \
        [tb("Tips", ["Look at the picture: rows = grouping, baskets = sharing."])]
    for idx in range(19):
        kind, text = themes[idx % len(themes)]
        n = random.randint(2, 5)
        size = random.randint(2, 5)
        if idx % 2 == 0:
            items.append(q(text, "diagram", "____", "", "object_group",
                            {"count": n*size, "kind": kind, "group_size": size, "icon_label": "divide"}))
        else:
            items.append(q(text, "diagram", "____", "", "sharing_baskets",
                            {"total": n*size, "num_baskets": n, "kind": kind}))
    return items


# ───────────────────────── H: Speed ─────────────────────────

def _H_s(sheet):
    random.seed(1000 + sheet)
    items = [cb("Speed Division", ["Work quickly and check your count."], "")] if sheet != 3 else \
        [tb("Speed Tips", ["Count fast but carefully."])]
    for idx in range(19):
        gs = random.choice([2, 3, 4, 5, 10])
        n = random.randint(2, 8)
        if idx % 2 == 0:
            items.append(_group_q(gs*n, gs, "Find the number of groups, quickly."))
        else:
            items.append(_share_q(gs*n, gs, "Share equally, quickly."))
    return items


# ───────────────────────── I: Puzzles ─────────────────────────

def _I_s(sheet):
    random.seed(1100 + sheet)
    items = [cb("Picture Puzzles", ["Look carefully — is it grouping or sharing?"], "")] if sheet != 3 else \
        [tb("Puzzle Tips", ["Check for a remainder before you answer."])]
    for idx in range(19):
        gs = random.choice([2, 3, 4])
        n = random.randint(2, 5)
        choice = idx % 3
        if choice == 0:
            leftover = random.randint(1, gs - 1)
            items.append(_group_q(gs*n + leftover, gs, "Solve the picture puzzle.", ans="____  R ____"))
        elif choice == 1:
            items.append(_share_q(gs*n, gs, "Solve the picture puzzle."))
        else:
            parts = gs
            items.append(_bar_q(parts*n, parts))
    return items


# ───────────────────────── J/REV: Mixed ─────────────────────────

def _J_s(sheet):
    random.seed(1200 + sheet)
    items = [cb("Mixed Challenge", ["Every division skill, mixed together."], "")]
    for idx in range(19):
        gs = random.choice([2, 3, 4, 5])
        n = random.randint(2, 7)
        choice = idx % 4
        if choice == 0:
            leftover = random.randint(1, gs - 1)
            items.append(_group_q(gs*n + leftover, gs, "Find the groups and the remainder.", ans="____  R ____"))
        elif choice == 1:
            items.append(_share_q(gs*n, gs))
        elif choice == 2:
            items.append(_mult_q(n, gs))
        else:
            items.append(_bar_q(gs*n, gs))
    return items


def _REV_s(sheet):
    random.seed(1300 + sheet)
    items = [cb("Level 25 Revision",
                 ["Grouping, sharing, remainders, bar models, and fact families, all mixed."], "")]
    for idx in range(19):
        gs = random.choice([2, 3, 4, 5])
        n = random.randint(2, 7)
        choice = idx % 5
        if choice == 0:
            leftover = random.randint(1, gs - 1)
            items.append(_group_q(gs*n + leftover, gs, "Find the groups and the remainder.", ans="____  R ____"))
        elif choice == 1:
            leftover = random.randint(1, gs - 1)
            items.append(_share_q(gs*n + leftover, gs, "Share equally and find what's left.", ans="____  R ____"))
        elif choice == 2:
            items.append(_mult_q(n, gs))
        elif choice == 3:
            items.append(_bar_q(gs*n, gs))
        else:
            items.append(_group_q(gs*n, gs))
    return items


# ───────────────────────── Dispatcher ─────────────────────────

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL25_NS = "__L25__"

LEVEL5_DISPATCH = {
    f"{LEVEL25_NS}A": _wrap(_A_s), f"{LEVEL25_NS}B": _wrap(_B_s),
    f"{LEVEL25_NS}CUM1": _wrap(_CUM1_s),
    f"{LEVEL25_NS}C": _wrap(_C_s), f"{LEVEL25_NS}D": _wrap(_D_s),
    f"{LEVEL25_NS}CUM2": _wrap(_CUM2_s),
    f"{LEVEL25_NS}E": _wrap(_E_s), f"{LEVEL25_NS}F": _wrap(_F_s),
    f"{LEVEL25_NS}CUM3": _wrap(_CUM3_s),
    f"{LEVEL25_NS}G": _wrap(_G_s), f"{LEVEL25_NS}H": _wrap(_H_s), f"{LEVEL25_NS}I": _wrap(_I_s),
    f"{LEVEL25_NS}J": _wrap(_J_s), f"{LEVEL25_NS}REV": _wrap(_REV_s),
}
