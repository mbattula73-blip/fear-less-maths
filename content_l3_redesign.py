"""
Fear Less Maths — LEVEL 23 ("Pre Level 3" — Addition & Subtraction, Class 1-2)
Same conventions as content_pre.py / content_l1_redesign.py / content_l2_redesign.py:
  - Every question has an image AND a short instruction line (not bold,
    same size as the question number).
  - Black-and-white, outline-only diagrams (ink-saving).
  - A mascot+flag-on-a-stick appears above every question.
  - Registered as a brand-new level using namespaced plain-letter codes
    (__L23__A, __L23__B...) so it never collides with Pre-Level, Pre
    Level 1/2, or the original, untouched Level 3.

Sub-level list:
  A  Addition — single digit          B  Addition — two digit (no carry)
  CUM1  Review: Addition
  C  Subtraction — single digit       D  Subtraction — two digit (no borrow)
  CUM2  Review: Subtraction
  E  Addition WITH carrying           F  Subtraction WITH borrowing
  CUM3  Review: Carrying/Borrowing
  G  Speed addition                   H  Speed subtraction
  I  Picture puzzles                  J  Mixed challenge
  REV  Level 23 Revision
"""
import random
from content import cb, tb, q

OBJ_KINDS = ["apple", "star", "balloon", "flower"]


def _kind(i):
    return OBJ_KINDS[i % len(OBJ_KINDS)]


def _eq_q(left, right, kind, op):
    text = "Add the numbers." if op == "+" else "Subtract the numbers."
    return q(text, "diagram", "____", "", "visual_equation",
              {"left": left, "right": right, "kind": kind, "op": op})


def _add_block(pairs_fn, sheet, title_base):
    random.seed(hash(title_base) % 1000 + sheet)
    pairs = pairs_fn()
    if sheet == 1:
        items = [cb(title_base, ["Count both groups, then put them together."], "")]
    elif sheet == 2:
        items = [cb(f"{title_base} - Practice", ["Count carefully, then write the total."], "")]
    elif sheet == 3:
        items = [tb(f"{title_base} Tips", ["Count the first group, then keep counting for the second."])]
    else:
        items = [cb(f"{title_base} - Speed Round", ["Add quickly and check your answer."], "")]
    for idx, (l, r) in enumerate(pairs):
        items.append(_eq_q(l, r, _kind(idx), "+"))
    return items


def _A_s(sheet):
    def gen():
        random.seed(10 + sheet)
        return [(random.randint(1, 9), random.randint(1, 9)) for _ in range(19)]
    return _add_block(gen, sheet, "Addition - Single Digit")


def _B_s(sheet):
    def gen():
        random.seed(20 + sheet)
        out = []
        for _ in range(19):
            a = random.randint(10, 40)
            ones_a = a % 10
            b_ones = random.randint(0, 9 - ones_a)
            b_tens = random.randint(1, 3) * 10
            out.append((a, b_tens + b_ones))
        return out
    return _add_block(gen, sheet, "Addition - Two Digit (No Carry)")


def _CUM1_s(sheet):
    random.seed(100 + sheet)
    items = [cb("Review: Addition", ["Mix of single and two-digit addition."], "")] if sheet != 3 else \
        [tb("Review Tips", ["Count both groups fully, then combine."])]
    for idx in range(19):
        if idx % 2 == 0:
            items.append(_eq_q(random.randint(1, 9), random.randint(1, 9), _kind(idx), "+"))
        else:
            a = random.randint(10, 30)
            items.append(_eq_q(a, random.randint(1, 9), _kind(idx), "+"))
    return items


def _sub_block(pairs_fn, sheet, title_base):
    random.seed(hash(title_base) % 1000 + sheet + 50)
    pairs = pairs_fn()
    if sheet == 1:
        items = [cb(title_base, ["Show the first group, then take away the second."], "")]
    elif sheet == 2:
        items = [cb(f"{title_base} - Practice", ["Count what is left after taking away."], "")]
    elif sheet == 3:
        items = [tb(f"{title_base} Tips", ["The first number must always be bigger or equal."])]
    else:
        items = [cb(f"{title_base} - Speed Round", ["Subtract quickly and check your answer."], "")]
    for idx, (l, r) in enumerate(pairs):
        items.append(_eq_q(l, r, _kind(idx), "-"))
    return items


def _C_s(sheet):
    def gen():
        random.seed(30 + sheet)
        out = []
        for _ in range(19):
            l = random.randint(2, 9)
            r = random.randint(1, l)
            out.append((l, r))
        return out
    return _sub_block(gen, sheet, "Subtraction - Single Digit")


def _D_s(sheet):
    def gen():
        random.seed(40 + sheet)
        out = []
        for _ in range(19):
            tens = random.randint(1, 4) * 10
            ones_l = random.randint(0, 9)
            l = tens + ones_l
            r = random.randint(1, ones_l) if ones_l > 0 else 1
            out.append((l, r))
        return out
    return _sub_block(gen, sheet, "Subtraction - Two Digit (No Borrow)")


def _CUM2_s(sheet):
    random.seed(200 + sheet)
    items = [cb("Review: Subtraction", ["Mix of single and two-digit subtraction."], "")] if sheet != 3 else \
        [tb("Review Tips", ["Take away from the first group only."])]
    for idx in range(19):
        if idx % 2 == 0:
            l = random.randint(2, 9)
            items.append(_eq_q(l, random.randint(1, l), _kind(idx), "-"))
        else:
            l = random.randint(10, 30)
            r = min(l % 10 if l % 10 > 0 else 1, l)
            items.append(_eq_q(l, r, _kind(idx), "-"))
    return items


def _E_s(sheet):
    """Addition WITH carrying: ones digits sum to 10 or more."""
    random.seed(300 + sheet)
    pairs = []
    for _ in range(19):
        a_ones = random.randint(5, 9)
        b_ones = random.randint(11 - a_ones, 9)
        a = random.randint(1, 4) * 10 + a_ones
        b = random.randint(0, 2) * 10 + b_ones
        pairs.append((a, b))
    if sheet == 1:
        items = [cb("Addition With Carrying",
                     ["Sometimes the ones add up to 10 or more.",
                      "Count everything together carefully."], "")]
    elif sheet == 2:
        items = [cb("Carrying - Practice", ["Count both groups fully, then combine them."], "")]
    elif sheet == 3:
        items = [tb("Carrying Tips", ["Count slowly - the total may cross into the next ten."])]
    else:
        items = [cb("Carrying - Speed Round", ["Add quickly and check your total."], "")]
    for idx, (a, b) in enumerate(pairs):
        items.append(_eq_q(a, b, _kind(idx), "+"))
    return items


def _F_s(sheet):
    """Subtraction WITH borrowing: ones digit of minuend < ones digit of subtrahend."""
    random.seed(400 + sheet)
    pairs = []
    for _ in range(19):
        l_ones = random.randint(0, 4)
        r_ones = random.randint(l_ones + 1, 9)
        l_tens = random.randint(2, 4) * 10
        l = l_tens + l_ones
        r = r_ones
        r = min(r, l - 1)
        pairs.append((l, max(r, 1)))
    if sheet == 1:
        items = [cb("Subtraction With Borrowing",
                     ["Sometimes there are not enough ones to take away.",
                      "Count carefully across the whole group."], "")]
    elif sheet == 2:
        items = [cb("Borrowing - Practice", ["Count what is left after taking the second group away."], "")]
    elif sheet == 3:
        items = [tb("Borrowing Tips", ["Count slowly - you may need to break into the tens."])]
    else:
        items = [cb("Borrowing - Speed Round", ["Subtract quickly and check your answer."], "")]
    for idx, (a, b) in enumerate(pairs):
        items.append(_eq_q(a, b, _kind(idx), "-"))
    return items


def _CUM3_s(sheet):
    random.seed(500 + sheet)
    items = [cb("Review: Carrying & Borrowing", ["Mix of both skills."], "")] if sheet != 3 else \
        [tb("Review Tips", ["Take your time - count fully each time."])]
    for idx in range(19):
        if idx % 2 == 0:
            a = random.randint(15, 39)
            b = random.randint(15, 39)
            items.append(_eq_q(a, b, _kind(idx), "+"))
        else:
            l = random.randint(20, 49)
            r = random.randint(1, l - 1)
            items.append(_eq_q(l, r, _kind(idx), "-"))
    return items


def _G_s(sheet):
    random.seed(600 + sheet)
    items = [cb("Speed Addition", ["Work as quickly and accurately as you can."], "")] if sheet != 3 else \
        [tb("Speed Tips", ["Don't rush so much that you lose count."])]
    for idx in range(19):
        a = random.randint(1, 45)
        b = random.randint(1, min(45 - a if 45 - a > 0 else 1, 20))
        items.append(_eq_q(a, b, _kind(idx), "+"))
    return items


def _H_s(sheet):
    random.seed(700 + sheet)
    items = [cb("Speed Subtraction", ["Work as quickly and accurately as you can."], "")] if sheet != 3 else \
        [tb("Speed Tips", ["Always check the first number is bigger."])]
    for idx in range(19):
        l = random.randint(5, 50)
        r = random.randint(1, l - 1)
        items.append(_eq_q(l, r, _kind(idx), "-"))
    return items


def _I_s(sheet):
    random.seed(800 + sheet)
    items = [cb("Picture Puzzles", ["Look carefully, then add or subtract."], "")] if sheet != 3 else \
        [tb("Puzzle Tips", ["Check the symbol first: + or -?"])]
    for idx in range(19):
        op = "+" if idx % 2 == 0 else "-"
        if op == "+":
            items.append(_eq_q(random.randint(1, 30), random.randint(1, 20), _kind(idx), "+"))
        else:
            l = random.randint(5, 40)
            items.append(_eq_q(l, random.randint(1, l - 1), _kind(idx), "-"))
    return items


def _J_s(sheet):
    random.seed(900 + sheet)
    items = [cb("Mixed Challenge", ["Addition and subtraction, easy and hard, all mixed."], "")]
    for idx in range(19):
        op = "+" if random.random() > 0.5 else "-"
        if op == "+":
            items.append(_eq_q(random.randint(1, 40), random.randint(1, 30), _kind(idx), "+"))
        else:
            l = random.randint(5, 50)
            items.append(_eq_q(l, random.randint(1, l - 1), _kind(idx), "-"))
    return items


def _REV_s(sheet):
    random.seed(1000 + sheet)
    items = [cb("Level 23 Revision", ["Every addition and subtraction skill, mixed together."], "")]
    for idx in range(19):
        op = "+" if random.random() > 0.5 else "-"
        if op == "+":
            items.append(_eq_q(random.randint(1, 45), random.randint(1, 30), _kind(idx), "+"))
        else:
            l = random.randint(5, 50)
            items.append(_eq_q(l, random.randint(1, l - 1), _kind(idx), "-"))
    return items


def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL23_NS = "__L23__"

LEVEL3_DISPATCH = {
    f"{LEVEL23_NS}A": _wrap(_A_s), f"{LEVEL23_NS}B": _wrap(_B_s),
    f"{LEVEL23_NS}CUM1": _wrap(_CUM1_s),
    f"{LEVEL23_NS}C": _wrap(_C_s), f"{LEVEL23_NS}D": _wrap(_D_s),
    f"{LEVEL23_NS}CUM2": _wrap(_CUM2_s),
    f"{LEVEL23_NS}E": _wrap(_E_s), f"{LEVEL23_NS}F": _wrap(_F_s),
    f"{LEVEL23_NS}CUM3": _wrap(_CUM3_s),
    f"{LEVEL23_NS}G": _wrap(_G_s), f"{LEVEL23_NS}H": _wrap(_H_s),
    f"{LEVEL23_NS}I": _wrap(_I_s), f"{LEVEL23_NS}J": _wrap(_J_s),
    f"{LEVEL23_NS}REV": _wrap(_REV_s),
}
