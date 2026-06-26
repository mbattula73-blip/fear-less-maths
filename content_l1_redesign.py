"""
Fear Less Maths — LEVEL 1 REDESIGN (Counting & Number Sense, Class 1-2)
Smaller step sizes than the original design: each skill is split into its own
sub-level instead of being bundled. Continues the Singapore CPA approach
started in Pre-Level (content_pre.py), gradually shifting from object support
toward number-line / abstract representation as ranges grow (1-20 -> 100),
since drawing 100 individual objects is not developmentally useful at this age.

CPA <-> Sheet mapping (same convention as Pre-Level):
  Sheet 1  Intro     = Concrete/near-concrete  : objects or ten-frames where range allows
  Sheet 2  Concept   = Pictorial                : grouped visuals / number line with marks
  Sheet 3  Practice  = Bridge                   : tips box + number line + light abstract mix
  Sheet 4  Mastery   = Abstract                  : numbers/symbols only

Sub-level list (overrides the old 1A-1J letters; old orphaned codes beyond
this list are no longer referenced by levels_data.py so they will not show
in the app):

  1A Counting 1-20 (bridge/review)      1B Counting 21-50         1C Counting 51-100
  1CUM1 Review: Counting 1-100
  1D Number After (next), 1-50          1E Number Before (prev), 1-50
  1F Before AND After together, 1-50    1G Before/After, 51-100
  1CUM2 Review: Before/After
  1H Greater/Smaller (concrete), 1-20   1I Greater/Smaller (numbers), 1-100
  1CUM3 Review: Greater/Smaller
  1J Missing numbers, 1-50              1K Missing numbers, 51-100
  1CUM4 Review: Missing numbers
  1L Patterns — skip count by 2         1M Patterns — skip count by 5 and 10
  1CUM5 Review: Patterns
  1N Place value — Tens & Ones (concrete)   1O Place value — Tens & Ones (abstract)
  1CUM6 Review: Place value
  1P Counting objects & puzzles         1Q Mixed challenge — all Level 1 skills
  1REV Level 1 Revision
"""
import random
from content import cb, tb, q

OBJ_KINDS = ["apple", "star", "balloon", "flower"]


def _kind(i):
    return OBJ_KINDS[i % len(OBJ_KINDS)]


# ───────────────────────── shared question builders ─────────────────────────

def _count_obj_q(n, kind, group_size=5):
    return q("Count the objects and write the number.", "diagram",
              "Number = ____", "", "object_group",
              {"count": n, "kind": kind, "group_size": group_size})


def _count_frame_q(n):
    return q("Count the objects in the ten-frames and write the total.", "diagram",
              "Number = ____", "", "ten_frames", {"count": n})


def _numline_after_q(n, lo, hi):
    if hi - lo < 5:
        hi = lo + 5
    span = hi - lo
    return q(f"Look at the number line. What number comes just AFTER {n}?", "diagram",
              "Answer = ____", "", "number_line",
              {"start": lo, "end": hi, "divisions": span, "mark": n})


def _numline_before_q(n, lo, hi):
    if hi - lo < 5:
        hi = lo + 5
    span = hi - lo
    return q(f"Look at the number line. What number comes just BEFORE {n}?", "diagram",
              "Answer = ____", "", "number_line",
              {"start": lo, "end": hi, "divisions": span, "mark": n})


def _base10_q(tens, ones):
    return q("Look at the blocks. Write the number they show.", "diagram",
              "Number = ____", "", "base10_blocks", {"tens": tens, "ones": ones})


def _compare_obj_q(left, right, kind):
    return q("Circle the group with MORE objects.", "diagram",
              "Bigger group = Left / Right", "", "object_compare",
              {"left_count": left, "right_count": right, "kind": kind})


# ───────────────────────── 1A/1B/1C: Counting 1-100, split into 3 ranges ─────────────────────────

def _counting_l1_block(lo, hi, sheet):
    random.seed(lo * 7 + sheet)
    span = list(range(lo, hi + 1))
    picks = [random.choice(span) for _ in range(19)]

    if sheet == 1:  # Concrete-ish: objects if small range, ten-frames if large
        items = [cb(f"Counting {lo} to {hi}",
                     ["Count carefully, one number at a time.",
                      "Use the pictures to help you count." if hi <= 20 else
                      "Use the ten-frames — each full frame is 10."],
                     f"Count: {lo}, {lo+1}, {lo+2}...")]
        for idx, n in enumerate(picks):
            if hi <= 20:
                items.append(_count_obj_q(n, _kind(idx)))
            else:
                items.append(_count_frame_q(n))
        return items

    if sheet == 2:  # Pictorial — grouped/ten-frames, subitizing
        items = [cb("Counting in Tens and Extra Ones",
                     ["Every full ten-frame is exactly 10.",
                      "Count the full frames first, then the extra dots."],
                     "2 full frames + 3 dots = 23")]
        for n in picks:
            items.append(_count_frame_q(n))
        return items

    if sheet == 3:  # Bridge — number line + tips
        items = [tb(f"Tips for Counting {lo}-{hi}",
                     ["Use the number line to check your counting.",
                      "If you lose track, count again from the start."])]
        for n in picks:
            items.append(_numline_after_q(n, lo, min(hi, n + 10)))
        return items

    # Abstract
    items = [cb(f"Numbers {lo} to {hi} — No Pictures",
                 ["You can now count without pictures.",
                  f"After {hi-1} comes {hi}."], "")]
    for n in picks:
        items.append(q(f"Write the number that comes just AFTER {n}.", "fill", "Answer = ____"))
    return items


def _1A_s(sheet): return _counting_l1_block(1, 20, sheet)
def _1B_s(sheet): return _counting_l1_block(21, 50, sheet)
def _1C_s(sheet): return _counting_l1_block(51, 100, sheet)


def _1CUM1_s(sheet):
    random.seed(50 + sheet)
    picks = [random.choice(range(1, 101)) for _ in range(19)]
    items = [cb("Review: Counting 1 to 100",
                 ["This sheet mixes small and big numbers.",
                  "Take your time with bigger numbers."], "")]
    for n in picks:
        if sheet in (1, 2):
            items.append(_count_frame_q(n) if n > 20 else _count_obj_q(n, _kind(n % 4)))
        elif sheet == 3:
            items.append(_numline_after_q(n, max(0, n - 5), min(100, n + 5)))
        else:
            items.append(q(f"Write the number that comes just AFTER {n}.", "fill", "Answer = ____"))
    return items


# ───────────────────────── 1D/1E/1F/1G: Before / After ─────────────────────────

def _before_after_block(lo, hi, mode, sheet):
    """mode: 'after', 'before', or 'both'"""
    random.seed(lo * 3 + hi + sheet + (1 if mode == "after" else 2 if mode == "before" else 3))
    picks = [random.choice(range(lo, hi + 1)) for _ in range(19)]
    title = {"after": "Number After", "before": "Number Before", "both": "Before AND After"}[mode]

    if sheet == 1:
        items = [cb(f"{title} ({lo}-{hi})",
                     ["'After' means the next number — add 1.",
                      "'Before' means the previous number — subtract 1."] if mode == "both" else
                     [f"'{title}' means {'add 1 to' if mode=='after' else 'subtract 1 from'} the number."],
                     "")]
        for n in picks:
            if mode == "after":
                items.append(_numline_after_q(n, max(lo, n - 4), min(hi, n + 6)))
            elif mode == "before":
                items.append(_numline_before_q(n, max(lo, n - 6), min(hi, n + 4)))
            else:
                items.append(_numline_after_q(n, max(lo, n - 5), min(hi, n + 5)) if n % 2 == 0
                              else _numline_before_q(n, max(lo, n - 5), min(hi, n + 5)))
        return items

    if sheet == 2:
        items = [cb(f"{title} — Using the Number Line",
                     ["Find the number on the line, then look one step in the right direction."], "")]
        for n in picks:
            items.append(_numline_after_q(n, max(lo, n - 5), min(hi, n + 5)) if mode != "before"
                          else _numline_before_q(n, max(lo, n - 5), min(hi, n + 5)))
        return items

    if sheet == 3:
        items = [tb(f"{title} Tips",
                     ["After = +1.  Before = -1.",
                      "Double-check by counting on your fingers."])]
        for n in picks:
            if mode == "after":
                items.append(q(f"What comes just after {n}?", "fill", "Answer = ____"))
            elif mode == "before":
                items.append(q(f"What comes just before {n}?", "fill", "Answer = ____"))
            else:
                items.append(q(f"What comes just before AND just after {n}?", "fill",
                                "Before = ____  After = ____"))
        return items

    items = [cb(f"{title} — Numbers Only", ["Apply +1 or -1 directly."], "")]
    for n in picks:
        if mode == "both":
            items.append(q(f"{n}: before = ____, after = ____.", "fill", "Before=____ After=____"))
        else:
            items.append(q(f"{title} of {n} is ____.", "fill", "Answer = ____"))
    return items


def _1D_s(sheet): return _before_after_block(1, 50, "after", sheet)
def _1E_s(sheet): return _before_after_block(1, 50, "before", sheet)
def _1F_s(sheet): return _before_after_block(1, 50, "both", sheet)
def _1G_s(sheet): return _before_after_block(51, 100, "both", sheet)


def _1CUM2_s(sheet):
    random.seed(60 + sheet)
    picks = [random.choice(range(1, 101)) for _ in range(19)]
    items = [cb("Review: Before & After", ["Mix of small and big numbers, both directions."], "")]
    for n in picks:
        items.append(q(f"{n}: before = ____, after = ____.", "fill", "Before=____ After=____"))
    return items


# ───────────────────────── 1H/1I: Greater / Smaller ─────────────────────────

def _1H_s(sheet):
    """Greater/Smaller using concrete object comparison, 1-20."""
    random.seed(700 + sheet)
    pairs = [(random.randint(1, 15), random.randint(1, 15)) for _ in range(19)]
    if sheet == 1:
        items = [cb("Bigger or Smaller — With Objects",
                     ["Count both groups, then compare.",
                      "More objects = bigger number."], "")]
        items += [_compare_obj_q(l, r, _kind(i)) for i, (l, r) in enumerate(pairs)]
        return items
    if sheet == 2:
        items = [cb("Comparing Using Groups of 5", ["Use the rows of 5 to compare quickly."], "")]
        items += [_compare_obj_q(l, r, _kind(i)) for i, (l, r) in enumerate(pairs)]
        return items
    if sheet == 3:
        items = [tb("Comparing Tips", ["Always count fully before deciding which is bigger."])]
        for l, r in pairs:
            items.append(q(f"Which is bigger: {l} or {r}?", "fill", "Bigger = ____"))
        return items
    items = [cb("Comparing Numbers", ["Compare directly without pictures."], "")]
    for l, r in pairs:
        items.append(q(f"Fill in: {l} ___ {r}  (>, < or =)", "fill", "Answer = ____"))
    return items


def _1I_s(sheet):
    """Greater/Smaller using numbers only, 1-100."""
    random.seed(800 + sheet)
    pairs = [(random.randint(1, 100), random.randint(1, 100)) for _ in range(19)]
    if sheet == 1:
        items = [cb("Bigger or Smaller — Numbers 1-100",
                     ["Compare the TENS digit first.",
                      "If tens are equal, compare the ONES digit."],
                     "47 vs 52: tens 4 < 5, so 47 is smaller")]
    elif sheet == 2:
        items = [cb("Comparing Two-Digit Numbers", ["Line up the digits to compare place by place."], "")]
    elif sheet == 3:
        items = [tb("Comparing Tips", ["Bigger tens digit always wins, no matter the ones digit."])]
    else:
        items = [cb("Comparing — Speed Round", ["Apply the tens-digit rule quickly."], "")]
    for l, r in pairs:
        items.append(q(f"Fill in: {l} ___ {r}  (>, < or =)", "fill", "Answer = ____"))
    return items


def _1CUM3_s(sheet):
    random.seed(900 + sheet)
    pairs = [(random.randint(1, 100), random.randint(1, 100)) for _ in range(19)]
    items = [cb("Review: Greater & Smaller", ["Mix of small and large numbers."], "")]
    for l, r in pairs:
        items.append(q(f"Fill in: {l} ___ {r}  (>, < or =)", "fill", "Answer = ____"))
    return items


# ───────────────────────── 1J/1K: Missing numbers ─────────────────────────

def _missing_numbers_block(lo, hi, sheet):
    random.seed(lo + hi + sheet * 13)
    items_out = []
    if sheet == 1:
        items_out.append(cb(f"Missing Numbers ({lo}-{hi})",
                             ["Look at the numbers before and after the gap.",
                              "The missing number fits in between, going up by 1."],
                             "5, ___, 7  ->  the missing number is 6"))
    elif sheet == 2:
        items_out.append(cb("Missing Numbers — Using the Number Line",
                             ["Find both known numbers on the line, then count the steps between."], ""))
    elif sheet == 3:
        items_out.append(tb("Missing Number Tips",
                             ["Count forward from the number before the gap.",
                              "Check your answer by counting backward from the number after the gap."]))
    else:
        items_out.append(cb("Missing Numbers — Speed Round", ["Fill in gaps quickly and accurately."], ""))

    for _ in range(19):
        gap_size = 1 if sheet <= 2 else random.choice([1, 1, 2])
        start = random.randint(lo, max(lo, hi - 4 - gap_size))
        seq = list(range(start, start + 3 + gap_size))
        hide_idx = random.randint(1, len(seq) - 2)
        display = [str(x) if i != hide_idx else "___" for i, x in enumerate(seq)]
        items_out.append(q(f"Fill in the missing number: {', '.join(display)}.", "fill", "Answer = ____"))
    return items_out


def _1J_s(sheet): return _missing_numbers_block(1, 50, sheet)
def _1K_s(sheet): return _missing_numbers_block(51, 100, sheet)


def _1CUM4_s(sheet):
    return _missing_numbers_block(1, 100, sheet)


# ───────────────────────── 1L/1M: Number patterns ─────────────────────────

def _pattern_block(step_options, sheet, label):
    random.seed(sum(step_options) * 11 + sheet)
    items = [cb(f"Number Patterns — {label}",
                 [f"Skip counting by {' or '.join(map(str, step_options))} means jumping that many each time.",
                  "Find the jump size first, then continue the pattern."],
                 f"2, 4, 6, 8 — jumps of 2" if 2 in step_options else f"5, 10, 15, 20 — jumps of 5")]
    for i in range(19):
        step = step_options[i % len(step_options)]
        start = random.randint(1, 100 - step * 5)
        start = start - (start % step) if start % step else start
        seq = [start + step * k for k in range(5)]
        hide_idx = random.choice([3, 4]) if sheet in (1, 2) else random.randint(1, 4)
        display = [str(x) if j != hide_idx else "___" for j, x in enumerate(seq)]
        if sheet == 4:
            items.append(q(f"Continue the pattern: {', '.join(display)}.", "fill", "Answer = ____"))
        else:
            tag = "diagram" if False else "fill"  # patterns kept numeric; no dedicated diagram needed
            items.append(q(f"Find the missing number in this pattern: {', '.join(display)}.",
                            "fill", "Answer = ____"))
    return items


def _1L_s(sheet): return _pattern_block([2], sheet, "Skip Counting by 2")
def _1M_s(sheet): return _pattern_block([5, 10], sheet, "Skip Counting by 5 and 10")


def _1CUM5_s(sheet): return _pattern_block([2, 5, 10], sheet, "Review — All Patterns")


# ───────────────────────── 1N/1O: Place value ─────────────────────────

def _1N_s(sheet):
    """Place value, concrete — base-10 blocks."""
    random.seed(1100 + sheet)
    nums = [random.randint(10, 99) for _ in range(19)]
    if sheet == 1:
        items = [cb("Tens and Ones — With Blocks",
                     ["Each tall rod = 10. Each small square = 1.",
                      "Count the rods first, then the squares."],
                     "3 rods + 4 squares = 34")]
    elif sheet == 2:
        items = [cb("Tens and Ones — Grouping Practice",
                     ["Count the rods, write the tens digit.",
                      "Count the squares, write the ones digit."], "")]
    elif sheet == 3:
        items = [tb("Place Value Tips",
                     ["The number of rods is the TENS digit.",
                      "The number of squares is the ONES digit."])]
    else:
        items = [cb("Tens and Ones — Quick Practice", ["Read the blocks and write the number fast."], "")]
    for n in nums:
        tens, ones = divmod(n, 10)
        items.append(_base10_q(tens, ones))
    return items


def _1O_s(sheet):
    """Place value, abstract — numbers only."""
    random.seed(1200 + sheet)
    nums = [random.randint(10, 99) for _ in range(19)]
    if sheet == 1:
        items = [cb("Tens and Ones — Numbers Only",
                     ["The TENS digit tells how many groups of 10.",
                      "The ONES digit tells the extra units."],
                     "47 = 4 tens and 7 ones")]
    elif sheet == 2:
        items = [cb("Building Numbers from Tens and Ones",
                     ["Multiply the tens digit by 10, then add the ones digit."], "")]
    elif sheet == 3:
        items = [tb("Place Value Tips", ["Tens digit x 10, then + ones digit = the number."])]
    else:
        items = [cb("Place Value — Speed Round", ["Work quickly and check your answers."], "")]
    for n in nums:
        tens, ones = divmod(n, 10)
        if sheet == 2:
            items.append(q(f"{tens} tens and {ones} ones = ____.", "fill", "Answer = ____"))
        else:
            items.append(q(f"{n} = ____ tens and ____ ones.", "fill", "Tens = ____  Ones = ____"))
    return items


def _1CUM6_s(sheet):
    random.seed(1300 + sheet)
    nums = [random.randint(10, 99) for _ in range(19)]
    items = [cb("Review: Place Value", ["Mix of block questions and number questions."], "")]
    for i, n in enumerate(nums):
        tens, ones = divmod(n, 10)
        if i % 2 == 0 and sheet in (1, 2):
            items.append(_base10_q(tens, ones))
        else:
            items.append(q(f"{n} = ____ tens and ____ ones.", "fill", "Tens = ____  Ones = ____"))
    return items


# ───────────────────────── 1P: Counting objects & puzzles ─────────────────────────

def _1P_s(sheet):
    random.seed(1400 + sheet)
    if sheet == 1:
        items = [cb("Counting & Simple Puzzles",
                     ["Read carefully and picture the objects in your head."], "")]
        riddles = [
            ("There are 12 apples. 7 are eaten. How many are left?", 5),
            ("8 stars and 9 more appear. How many now?", 17),
            ("15 balloons, 6 pop. How many are left?", 9),
            ("There are 23 flowers. 14 are picked. How many remain?", 9),
        ]
    elif sheet == 2:
        items = [cb("Picture Puzzles — Groups", ["Use tens-and-ones thinking to solve faster."], "")]
        riddles = [
            ("A basket has 3 tens and 4 ones of apples. How many apples?", 34),
            ("There are 45 stars, 20 fly away. How many are left?", 25),
            ("6 tens and 7 ones of balloons are tied. How many balloons?", 67),
            ("There are 58 flowers, 9 more bloom. How many now?", 67),
        ]
    elif sheet == 3:
        items = [tb("Puzzle Tips", ["Underline the numbers, decide add or subtract, then solve."])]
        riddles = [
            ("There were 72 apples, 35 were sold. How many are left?", 37),
            ("48 stars plus 26 more stars. How many now?", 74),
            ("There were 90 balloons, 47 popped. How many left?", 43),
        ]
    else:
        items = [cb("Number Puzzles — No Pictures", ["Solve like a riddle, using numbers only."], "")]
        riddles = [
            ("A number is 1 more than 49. What is it?", 50),
            ("A number has 7 tens and 3 ones. What is it?", 73),
            ("A number is 10 less than 100. What is it?", 90),
        ]
    for text, ans in riddles:
        items.append(q(text, "word", f"Answer = ____ (Answer: {ans})"))
    # Top up to 19 real items with simple generated fill questions
    random.seed(1450 + sheet)
    while len([i for i in items if i["type"] != "concept_box" and i["type"] != "tips_box"]) < 19:
        n = random.randint(10, 99)
        items.append(q(f"Write the number that is 1 more than {n}.", "fill", "Answer = ____"))
    return items


def _1Q_s(sheet):
    """Mixed challenge — pulls from every Level 1 skill."""
    random.seed(1500 + sheet)
    items = [cb("Level 1 Mixed Challenge",
                 ["This sheet mixes counting, before/after, comparing, missing numbers, patterns and place value."],
                 "")]
    builders = [
        lambda: q(f"What comes just after {random.randint(1,99)}?", "fill", "Answer = ____"),
        lambda: q(f"What comes just before {random.randint(2,100)}?", "fill", "Answer = ____"),
        lambda: q(f"Fill in: {random.randint(1,100)} ___ {random.randint(1,100)} (>, < or =)", "fill", "Answer = ____"),
        lambda: q(f"{random.randint(10,99)} = ____ tens and ____ ones.", "fill", "Tens=____ Ones=____"),
        lambda: q(f"Continue: {(s:=random.randint(1,40))}, {s+2}, {s+4}, ___.", "fill", "Answer = ____"),
    ]
    for i in range(19):
        items.append(builders[i % len(builders)]())
    return items


def _1REV_s(sheet):
    random.seed(1600 + sheet)
    items = [cb("Level 1 Revision — All Topics",
                 ["This sheet tests everything from Level 1: counting to 100, before/after, "
                  "greater/smaller, missing numbers, patterns and place value."], "")]
    builders = [
        lambda: q(f"What comes just after {random.randint(1,99)}?", "fill", "Answer = ____"),
        lambda: q(f"What comes just before {random.randint(2,100)}?", "fill", "Answer = ____"),
        lambda: q(f"Fill in: {random.randint(1,100)} ___ {random.randint(1,100)} (>, < or =)", "fill", "Answer = ____"),
        lambda: q(f"{random.randint(10,99)} = ____ tens and ____ ones.", "fill", "Tens=____ Ones=____"),
        lambda: q(f"Continue: {(s:=random.randint(1,40))}, {s+5}, {s+10}, ___.", "fill", "Answer = ____"),
        lambda: q(f"Fill in the missing number: {(s2:=random.randint(1,90))}, ___, {s2+2}.", "fill", "Answer = ____"),
    ]
    if sheet == 1:
        for n in random.sample(range(1, 21), 6):
            items.append(_count_obj_q(n, _kind(n % 4)))
        for i in range(13):
            items.append(builders[i % len(builders)]())
    else:
        for i in range(19):
            items.append(builders[i % len(builders)]())
    return items


# ───────────────────────── Dispatcher ─────────────────────────

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL1_DISPATCH = {
    "1A": _wrap(_1A_s), "1B": _wrap(_1B_s), "1C": _wrap(_1C_s), "1CUM1": _wrap(_1CUM1_s),
    "1D": _wrap(_1D_s), "1E": _wrap(_1E_s), "1F": _wrap(_1F_s), "1G": _wrap(_1G_s),
    "1CUM2": _wrap(_1CUM2_s),
    "1H": _wrap(_1H_s), "1I": _wrap(_1I_s), "1CUM3": _wrap(_1CUM3_s),
    "1J": _wrap(_1J_s), "1K": _wrap(_1K_s), "1CUM4": _wrap(_1CUM4_s),
    "1L": _wrap(_1L_s), "1M": _wrap(_1M_s), "1CUM5": _wrap(_1CUM5_s),
    "1N": _wrap(_1N_s), "1O": _wrap(_1O_s), "1CUM6": _wrap(_1CUM6_s),
    "1P": _wrap(_1P_s), "1Q": _wrap(_1Q_s), "1REV": _wrap(_1REV_s),
}
