"""
Fear Less Maths — LEVEL 3 REDESIGN (Addition & Subtraction, Grade 2-3)

Replaces the original Level 3 in place. Based on detailed analysis of
the original content (which jumped from single-digit straight to
2-digit+2-digit addition with no bridge, introduced borrowing with only
ONE scaffolded hint question, and used mental-math strategy labels like
"bond to 10"/"compensation" without ever teaching the strategy first)
plus research into the standard concrete -> expanded-form -> algorithm
progression for regrouping (used across multiple teaching guides) and
the specific visual that was missing throughout: showing the TRADE
itself (10 ones circled into a new ten / a ten broken into 10 ones),
not just static blocks.

Same worksheet format as Levels 6/7: ONE worked example (no abstract
rule list), ONE instruction line stated once, 20 bare-expression
questions (15 pictorial blank-diagram + 5 numeral), B&W outline-only
diagrams.

Sub-level list (25 total -- bigger than the original 14, to properly
space out the progression):
  A Addition - single digit            B Addition - 2digit+1digit, no carry (NEW)
  C Addition - 2digit+2digit, no carry
  CUM1 review
  D Carrying - concrete (trade action)  E Carrying - algorithm practice
  CUM2 review
  F Subtraction - single digit          G Subtraction - 2digit, no borrow (NEW)
  CUM3 review
  H Borrowing - concrete (trade action) I Borrowing - expanded form bridge
  J Borrowing - algorithm practice
  CUM4 review
  K Addition+Subtraction mixed (tiered) L Word problems (tiered)
  CUM5 review
  M Bond-to-10 & Doubles (taught)       N Compensation strategy (taught)
  O Puzzles - Tier 1 (simple)           P Puzzles - Tier 2 (harder, separated)
  CUM6 review
  Q Speed round                        R Mixed challenge
  REV Revision
"""
import random
from content import cb, tb, q

# ───────────────────────── shared helpers ─────────────────────────

def _eq_q(a, op, b, hint=""):
    suffix = f"  {hint}" if hint else ""
    return q(f"{a} {op} {b} = ____{suffix}", "diagram", "____", "", "regroup_ones_blank",
              {"ones1": a % 10 if a < 100 else a, "ones2": b % 10 if b < 100 else b})


def _make_sheet(title, bullets, icon, icon_params, instruction, builder, sheet, n_q=20, seed_base=0):
    random.seed(seed_base + sheet)
    items = [cb(title, bullets, "", icon_diagram=icon, icon_params=icon_params)]
    items.append(tb("Instructions", [instruction]))
    questions = [builder(i, sheet) for i in range(n_q)]
    for i in range(15, len(questions)):
        questions[i] = dict(questions[i])
        questions[i]["diagram_type"] = None
        questions[i]["diagram_params"] = {}
    items.extend(questions)
    return items


# ───────────────────────── A/B/C: Addition foundation ─────────────────────────

def _A_s(sheet):
    def builder(i, sheet):
        a, b = random.randint(1,9), random.randint(1,9)
        return q(f"{a} + {b} = ____", "diagram", "____", "", "regroup_ones_blank", {"ones1": a, "ones2": b})
    return _make_sheet(
        "Worked Example",
        ["Count both groups of ones, then add them together."],
        "regroup_ones_blank", {"ones1": 4, "ones2": 3},
        "Count the ones in each group, then add.", builder, sheet, seed_base=10)


def _B_s(sheet):
    """NEW bridge: 2-digit + 1-digit, no carry."""
    def builder(i, sheet):
        a = random.randint(10, 80)
        ones_a = a % 10
        b = random.randint(1, 9 - ones_a) if ones_a < 9 else 1
        return q(f"{a} + {b} = ____", "diagram", "____", "", "regroup_ones_blank",
                  {"ones1": ones_a, "ones2": b})
    return _make_sheet(
        "Worked Example",
        ["The tens digit stays the same -- only add the ones.",
         "23 + 4: tens stay at 2, ones become 3+4=7, so the answer is 27."],
        "regroup_ones_blank", {"ones1": 3, "ones2": 4},
        "Add the ones only -- the tens digit doesn't change.", builder, sheet, seed_base=20)


def _C_s(sheet):
    def builder(i, sheet):
        a_tens, b_tens = random.randint(1,4), random.randint(1,4)
        a_ones = random.randint(0,9)
        b_ones = random.randint(0, 9-a_ones)
        a, b = a_tens*10+a_ones, b_tens*10+b_ones
        return q(f"{a} + {b} = ____", "diagram", "____", "", "regroup_ones_blank",
                  {"ones1": a_ones, "ones2": b_ones})
    return _make_sheet(
        "Worked Example",
        ["Add the ones first, then add the tens.",
         "23 + 14: ones 3+4=7, tens 2+1=3, answer = 37."],
        "regroup_ones_blank", {"ones1": 3, "ones2": 4},
        "Add the ones, then add the tens separately.", builder, sheet, seed_base=30)


def _CUM1_s(sheet):
    def builder(i, sheet):
        choice = i % 2
        if choice == 0:
            a,b = random.randint(1,9), random.randint(1,9)
            return q(f"{a} + {b} = ____", "diagram", "____", "", "regroup_ones_blank", {"ones1":a,"ones2":b})
        else:
            a = random.randint(10,80); ao=a%10; b=random.randint(1,9-ao) if ao<9 else 1
            return q(f"{a} + {b} = ____", "diagram", "____", "", "regroup_ones_blank", {"ones1":ao,"ones2":b})
    return _make_sheet(
        "Review", ["Mix of single-digit and 2-digit addition (no carrying yet)."],
        "regroup_ones_blank", {"ones1": 3, "ones2": 4},
        "Add the ones, then the tens if needed.", builder, sheet, seed_base=100)


# ───────────────────────── D/E: Carrying ─────────────────────────

def _D_s(sheet):
    """Concrete: show the TRADE (10+ ones circled into a new ten)."""
    def builder(i, sheet):
        a_ones = random.randint(5,9)
        b_ones = random.randint(11-a_ones, 9)
        return q(f"{a_ones} ones + {b_ones} ones = ____ ones. 10 or more? Trade for a ten!",
                  "diagram", "____", "", "regroup_ones_blank", {"ones1": a_ones, "ones2": b_ones})
    return _make_sheet(
        "Worked Example",
        ["When the ones add up to 10 or more, trade 10 ones for 1 new ten.",
         "7 ones + 5 ones = 12 ones = 1 ten + 2 ones."],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "Add the ones. If you get 10 or more, trade 10 ones for 1 ten.",
        builder, sheet, seed_base=40)


def _E_s(sheet):
    def builder(i, sheet):
        a_ones = random.randint(5,9); b_ones = random.randint(11-a_ones,9)
        a_tens, b_tens = random.randint(1,4), random.randint(1,4)
        a, b = a_tens*10+a_ones, b_tens*10+b_ones
        return q(f"{a} + {b} = ____", "diagram", "____", "", "regroup_ones_blank",
                  {"ones1": a_ones, "ones2": b_ones})
    return _make_sheet(
        "Worked Example",
        ["Add the ones, trade if 10 or more, then add the tens (plus the new ten)."],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "Add the ones, trade for a ten if needed, then add the tens.",
        builder, sheet, seed_base=50)


def _CUM2_s(sheet):
    def builder(i, sheet):
        a_ones = random.randint(4,9); b_ones = random.randint(max(1,11-a_ones),9)
        a_tens, b_tens = random.randint(1,4), random.randint(1,4)
        a, b = a_tens*10+a_ones, b_tens*10+b_ones
        return q(f"{a} + {b} = ____", "diagram", "____", "", "regroup_ones_blank", {"ones1":a_ones,"ones2":b_ones})
    return _make_sheet(
        "Review", ["Practice carrying with different two-digit numbers."],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "Remember: 10+ ones means trade for a new ten.", builder, sheet, seed_base=200)


# ───────────────────────── F/G: Subtraction foundation ─────────────────────────

def _F_s(sheet):
    def builder(i, sheet):
        a = random.randint(2,9); b = random.randint(1,a)
        return q(f"{a} - {b} = ____", "diagram", "____", "", "regroup_break_blank",
                  {"tens": 0, "ones": a})
    return _make_sheet(
        "Worked Example", ["Count the group, then take away that many."],
        "regroup_break_blank", {"tens": 0, "ones": 8},
        "Count, then take away.", builder, sheet, seed_base=60)


def _G_s(sheet):
    """NEW: 2-digit subtraction, no borrow."""
    def builder(i, sheet):
        a_tens = random.randint(2,8); a_ones = random.randint(0,9)
        b_ones = random.randint(0, a_ones)
        b_tens = random.randint(1, a_tens-1) if a_tens > 1 else 0
        a, b = a_tens*10+a_ones, b_tens*10+b_ones
        return q(f"{a} - {b} = ____", "diagram", "____", "", "regroup_break_blank",
                  {"tens": a_tens, "ones": a_ones})
    return _make_sheet(
        "Worked Example",
        ["Subtract the ones first, then the tens. No breaking needed yet.",
         "47 - 23: ones 7-3=4, tens 4-2=2, answer = 24."],
        "regroup_break_blank", {"tens": 4, "ones": 7},
        "Subtract the ones, then the tens.", builder, sheet, seed_base=70)


def _CUM3_s(sheet):
    def builder(i, sheet):
        choice = i % 2
        if choice == 0:
            a=random.randint(2,9); b=random.randint(1,a)
            return q(f"{a} - {b} = ____", "diagram", "____", "", "regroup_break_blank", {"tens":0,"ones":a})
        else:
            at=random.randint(2,8); ao=random.randint(0,9); bo=random.randint(0,ao); bt=random.randint(1,at-1) if at>1 else 0
            a,b = at*10+ao, bt*10+bo
            return q(f"{a} - {b} = ____", "diagram", "____", "", "regroup_break_blank", {"tens":at,"ones":ao})
    return _make_sheet(
        "Review", ["Mix of single-digit and 2-digit subtraction (no borrowing yet)."],
        "regroup_break_blank", {"tens": 4, "ones": 7},
        "Subtract the ones, then the tens.", builder, sheet, seed_base=300)


# ───────────────────────── H/I/J: Borrowing ─────────────────────────

def _H_s(sheet):
    """Concrete: show breaking a ten into 10 ones."""
    def builder(i, sheet):
        a_tens = random.randint(2,6)
        a_ones = random.randint(0,4)
        b_ones = random.randint(a_ones+1, 9)
        a = a_tens*10 + a_ones
        return q(f"{a} - {b_ones}: not enough ones? Break a ten into 10 ones!",
                  "diagram", "____", "", "regroup_break_blank", {"tens": a_tens, "ones": a_ones})
    return _make_sheet(
        "Worked Example",
        ["If there aren't enough ones to subtract, break one ten into 10 loose ones.",
         "43: not enough ones to take away 7. Break a ten: 3 tens + 13 ones."],
        "regroup_break_blank", {"tens": 4, "ones": 3},
        "If you don't have enough ones, break a ten into 10 ones first.",
        builder, sheet, seed_base=80)


def _I_s(sheet):
    """Expanded form bridge."""
    def builder(i, sheet):
        a_tens = random.randint(2,7); a_ones = random.randint(0,5)
        b_ones = random.randint(a_ones+1, 9)
        return q(f"{a_tens}{a_ones} = {a_tens-1}0 + {10+a_ones} (expanded). Now subtract {b_ones} ones.",
                  "diagram", "____", "", "regroup_break_blank", {"tens": a_tens, "ones": a_ones})
    return _make_sheet(
        "Worked Example",
        ["Write the number in expanded form after breaking a ten.",
         "43 = 30 + 13 (after breaking one ten into ten ones)."],
        "regroup_break_blank", {"tens": 4, "ones": 3},
        "Rewrite in expanded form after breaking a ten, then subtract.",
        builder, sheet, seed_base=90)


def _J_s(sheet):
    def builder(i, sheet):
        a_tens = random.randint(2,8); a_ones = random.randint(0,5)
        b_ones = random.randint(a_ones+1, 9)
        b_tens = random.randint(1, a_tens-1) if a_tens > 1 else 0
        a, b = a_tens*10+a_ones, b_tens*10+b_ones
        return q(f"{a} - {b} = ____", "diagram", "____", "", "regroup_break_blank",
                  {"tens": a_tens, "ones": a_ones})
    return _make_sheet(
        "Worked Example",
        ["Break a ten if needed, then subtract ones, then subtract tens."],
        "regroup_break_blank", {"tens": 4, "ones": 3},
        "Break a ten if needed, then subtract the ones, then the tens.",
        builder, sheet, seed_base=95)


def _CUM4_s(sheet):
    def builder(i, sheet):
        a_tens = random.randint(2,8); a_ones = random.randint(0,5)
        b_ones = random.randint(a_ones+1, 9)
        b_tens = random.randint(1, a_tens-1) if a_tens > 1 else 0
        a, b = a_tens*10+a_ones, b_tens*10+b_ones
        return q(f"{a} - {b} = ____", "diagram", "____", "", "regroup_break_blank", {"tens":a_tens,"ones":a_ones})
    return _make_sheet(
        "Review", ["Practice borrowing with different two-digit numbers."],
        "regroup_break_blank", {"tens": 4, "ones": 3},
        "Break a ten if you don't have enough ones.", builder, sheet, seed_base=400)


# ───────────────────────── K/L: Mixed & word problems ─────────────────────────

def _K_s(sheet):
    def builder(i, sheet):
        op = "+" if i % 2 == 0 else "-"
        a_tens = random.randint(1,5); a_ones = random.randint(0,9)
        a = a_tens*10+a_ones
        if op == "+":
            b = random.randint(1, 20)
            return q(f"{a} + {b} = ____", "diagram", "____", "", "regroup_ones_blank",
                      {"ones1": a_ones, "ones2": b % 10})
        else:
            b = random.randint(1, a)
            return q(f"{a} - {b} = ____", "diagram", "____", "", "regroup_break_blank",
                      {"tens": a_tens, "ones": a_ones})
    return _make_sheet(
        "Worked Example", ["Check the symbol first: + or -? Then solve using the same steps as before."],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "Check the symbol, then solve step by step.", builder, sheet, seed_base=110)


def _L_s(sheet):
    templates_add = [
        "{a} red balls and {b} blue balls. Total = ____.",
        "{a} students in class A, {b} in class B. Total = ____.",
    ]
    templates_sub = [
        "{a} oranges, {b} are rotten. Good ones = ____.",
        "Had {a} rupees, spent {b}. Left = ____.",
    ]
    def builder(i, sheet):
        a = random.randint(10,60); b = random.randint(5,30)
        if i % 2 == 0:
            txt = random.choice(templates_add).format(a=a, b=b)
            return q(txt, "diagram", "____", "", "regroup_ones_blank", {"ones1": a%10, "ones2": b%10})
        else:
            b = min(b, a)
            txt = random.choice(templates_sub).format(a=a, b=b)
            return q(txt, "diagram", "____", "", "regroup_break_blank", {"tens": a//10, "ones": a%10})
    return _make_sheet(
        "Worked Example",
        ["Decide: are things being joined (add) or taken away (subtract)?"],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "Read carefully, decide add or subtract, then solve.", builder, sheet, seed_base=120)


def _CUM5_s(sheet):
    def builder(i, sheet):
        op = "+" if i % 2 == 0 else "-"
        a = random.randint(15,60)
        if op == "+":
            b = random.randint(5,30)
            return q(f"{a} + {b} = ____", "diagram", "____", "", "regroup_ones_blank", {"ones1":a%10,"ones2":b%10})
        else:
            b = random.randint(1,a)
            return q(f"{a} - {b} = ____", "diagram", "____", "", "regroup_break_blank", {"tens":a//10,"ones":a%10})
    return _make_sheet(
        "Review", ["Mix of addition, subtraction, and word problems."],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "Solve each one step by step.", builder, sheet, seed_base=500)


# ───────────────────────── M/N: Mental math (taught) ─────────────────────────

def _M_s(sheet):
    """Bond-to-10 and doubles, explicitly taught with the ten-frame/bond diagrams."""
    def builder(i, sheet):
        if i % 2 == 0:
            given = random.randint(2,9)
            return q(f"{given} + ____ = 10  (how many more to make 10?)", "diagram", "____",
                      "", "make_ten_frame_blank", {"given": given})
        else:
            n = random.randint(2,9)
            return q(f"{n} + {n} = ____  (double)", "diagram", "____",
                      "", "number_bond_blank", {"known": n})
    return _make_sheet(
        "Worked Example",
        ["Bond to 10: how many more does a number need to reach 10?",
         "7 + 3 = 10, because 7 needs 3 more to fill the ten-frame.",
         "Doubles: adding a number to itself. 6 + 6 = 12."],
        "make_ten_frame_blank", {"given": 7},
        "Fill in how many more to make 10, or find the double.", builder, sheet, seed_base=130)


def _N_s(sheet):
    """Compensation strategy, taught with the number line."""
    def builder(i, sheet):
        a = random.randint(15, 60)
        b = random.randint(15, 60)
        return q(f"{a} + {b} = ____  (move to a friendly number first)", "diagram", "____",
                  "", "decimal_numberline_blank", {"lo": a, "hi": a+b+5, "divisions": 8})
    return _make_sheet(
        "Worked Example",
        ["Move one number to a nearby 'friendly' (round) number, then adjust back.",
         "36 + 56: 36 is 4 away from 40. 40+56=96, then 96-4=92. So 36+56=92."],
        "decimal_numberline_example", {"value": 40, "lo": 30, "hi": 60, "divisions": 6},
        "Find a friendly (round) number nearby, solve, then adjust back.",
        builder, sheet, seed_base=140)


def _CUM6_s(sheet):
    def builder(i, sheet):
        choice = i % 3
        if choice == 0:
            given = random.randint(2,9)
            return q(f"{given} + ____ = 10", "diagram", "____", "", "make_ten_frame_blank", {"given": given})
        elif choice == 1:
            n = random.randint(2,9)
            return q(f"{n} + {n} = ____", "diagram", "____", "", "number_bond_blank", {"known": n})
        else:
            a,b = random.randint(15,60), random.randint(15,60)
            return q(f"{a} + {b} = ____", "diagram", "____", "", "decimal_numberline_blank", {"lo":a,"hi":a+b+5,"divisions":8})
    return _make_sheet(
        "Review", ["Mix of bond-to-10, doubles, and compensation."],
        "make_ten_frame_blank", {"given": 7},
        "Use the strategy that fits best.", builder, sheet, seed_base=600)


# ───────────────────────── O/P: Puzzles (tiered) ─────────────────────────

def _O_s(sheet):
    """Tier 1: simple logic, matched to the rest of the level's difficulty."""
    def builder(i, sheet):
        a = random.randint(10,40); b = random.randint(5,20)
        if i % 2 == 0:
            return q(f"What number plus {b} equals {a+b}? ____", "diagram", "____",
                      "", "regroup_ones_blank", {"ones1": a%10, "ones2": b%10})
        else:
            return q(f"What number minus {b} equals {max(a-b,0)}? ____", "diagram", "____",
                      "", "regroup_break_blank", {"tens": a//10, "ones": a%10})
    return _make_sheet(
        "Worked Example", ["Work backwards: undo the operation to find the missing number."],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "Work backwards to find the missing number.", builder, sheet, seed_base=150)


def _P_s(sheet):
    """Tier 2: harder, kept clearly separate."""
    riddles = [
        "Two numbers add to {s}. One is {d} more than the other. Find both.",
        "I am between {lo} and {hi}. I am even. What could I be?",
        "I am between {lo} and {hi}. My digits add to {ds}. What could I be?",
    ]
    def builder(i, sheet):
        lo = random.randint(10,40); hi = lo+10
        s = random.randint(20,60); d = random.randint(2,10)
        ds = random.randint(5,12)
        txt = riddles[i % len(riddles)].format(s=s, d=d, lo=lo, hi=hi, ds=ds)
        return q(txt, "diagram", "____", "", "regroup_ones_blank", {"ones1": 5, "ones2": 3})
    return _make_sheet(
        "Worked Example (Harder)",
        ["These puzzles need extra thinking -- try a few numbers and check if they fit ALL the clues."],
        "number_bond_blank", {"known": 5},
        "Try different numbers until all the clues fit.", builder, sheet, seed_base=160)


def _CUM6b_s(sheet):
    pass  # not used; CUM placed before puzzles already


# ───────────────────────── Q/R/REV ─────────────────────────

def _Q_s(sheet):
    def builder(i, sheet):
        choice = i % 2
        a = random.randint(10,70)
        if choice == 0:
            b = random.randint(5,29)
            return q(f"{a} + {b} = ____", "diagram", "____", "", "regroup_ones_blank", {"ones1":a%10,"ones2":b%10})
        else:
            b = random.randint(1,a)
            return q(f"{a} - {b} = ____", "diagram", "____", "", "regroup_break_blank", {"tens":a//10,"ones":a%10})
    return _make_sheet(
        "Worked Example", ["Speed round: work quickly but carefully."],
        "regroup_ones_blank", {"ones1": 7, "ones2": 5},
        "Solve each one as quickly as you can.", builder, sheet, seed_base=170)


def _R_s(sheet):
    def builder(i, sheet):
        choice = i % 5
        a = random.randint(10,70)
        if choice == 0:
            b = random.randint(5,29)
            return q(f"{a} + {b} = ____", "diagram", "____", "", "regroup_ones_blank", {"ones1":a%10,"ones2":b%10})
        elif choice == 1:
            b = random.randint(1,a)
            return q(f"{a} - {b} = ____", "diagram", "____", "", "regroup_break_blank", {"tens":a//10,"ones":a%10})
        elif choice == 2:
            given = random.randint(2,9)
            return q(f"{given} + ____ = 10", "diagram", "____", "", "make_ten_frame_blank", {"given": given})
        elif choice == 3:
            n = random.randint(2,9)
            return q(f"{n} + {n} = ____", "diagram", "____", "", "number_bond_blank", {"known": n})
        else:
            return q(f"{a} + {random.randint(15,40)} = ____  (use a friendly number)", "diagram", "____",
                      "", "decimal_numberline_blank", {"lo": a, "hi": a+50, "divisions": 8})
    return _make_sheet(
        "Worked Example", ["Mixed challenge: every addition and subtraction skill from this level."],
        "regroup_break_blank", {"tens": 4, "ones": 3},
        "Read each one carefully, then solve.", builder, sheet, seed_base=180)


def _REV_s(sheet):
    def builder(i, sheet):
        choice = i % 6
        a = random.randint(10,70)
        if choice == 0:
            b = random.randint(1,9); return q(f"{b}+{random.randint(1,9)} = ____", "diagram", "____", "", "regroup_ones_blank", {"ones1":b,"ones2":random.randint(1,9)})
        elif choice == 1:
            b = random.randint(5,29)
            return q(f"{a} + {b} = ____", "diagram", "____", "", "regroup_ones_blank", {"ones1":a%10,"ones2":b%10})
        elif choice == 2:
            b = random.randint(1,a)
            return q(f"{a} - {b} = ____", "diagram", "____", "", "regroup_break_blank", {"tens":a//10,"ones":a%10})
        elif choice == 3:
            given = random.randint(2,9)
            return q(f"{given} + ____ = 10", "diagram", "____", "", "make_ten_frame_blank", {"given": given})
        elif choice == 4:
            n = random.randint(2,9)
            return q(f"{n} + {n} = ____", "diagram", "____", "", "number_bond_blank", {"known": n})
        else:
            return q(f"{a} + {random.randint(15,40)} = ____", "diagram", "____",
                      "", "decimal_numberline_blank", {"lo": a, "hi": a+50, "divisions": 8})
    return _make_sheet(
        "Level 3 Revision",
        ["Every addition and subtraction skill: carrying, borrowing, mental math, and word problems."],
        "regroup_break_blank", {"tens": 4, "ones": 3},
        "Work through each question step by step.", builder, sheet, seed_base=700)


# ───────────────────────── Dispatcher (REPLACES original Level 3) ─────────────────────────

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL3_V2_DISPATCH = {
    "3A": _wrap(_A_s), "3B": _wrap(_B_s), "3C": _wrap(_C_s), "3CUM1": _wrap(_CUM1_s),
    "3D": _wrap(_D_s), "3E": _wrap(_E_s), "3CUM2": _wrap(_CUM2_s),
    "3F": _wrap(_F_s), "3G": _wrap(_G_s), "3CUM3": _wrap(_CUM3_s),
    "3H": _wrap(_H_s), "3I": _wrap(_I_s), "3J": _wrap(_J_s), "3CUM4": _wrap(_CUM4_s),
    "3K": _wrap(_K_s), "3L": _wrap(_L_s), "3CUM5": _wrap(_CUM5_s),
    "3M": _wrap(_M_s), "3N": _wrap(_N_s), "3CUM6": _wrap(_CUM6_s),
    "3O": _wrap(_O_s), "3P": _wrap(_P_s),
    "3Q": _wrap(_Q_s), "3R": _wrap(_R_s), "3REV": _wrap(_REV_s),
}
