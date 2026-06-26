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
    return q("", "diagram", "____", "", "object_group",
              {"count": n, "kind": kind, "group_size": group_size})


def _count_frame_q(n):
    return q("", "diagram", "____", "", "ten_frames", {"count": n})


def _numline_after_q(n, lo, hi):
    span = max(5, min(10, hi - lo if hi - lo >= 5 else 5))
    start = max(0, n - span // 2)
    return q("", "diagram", "____", "", "numline_jump",
              {"start": start, "end": start + span, "mark": n, "hop_by": 1})


def _numline_before_q(n, lo, hi):
    span = max(5, min(10, hi - lo if hi - lo >= 5 else 5))
    start = max(0, n - span // 2)
    return q("", "diagram", "____", "", "numline_jump",
              {"start": start, "end": start + span, "mark": n, "hop_by": -1})


def _eq_q(left, right, kind, op):
    """Visual addition/subtraction equation, zero text."""
    return q("", "diagram", "____", "", "visual_equation",
              {"left": left, "right": right, "kind": kind, "op": op})


def _compare_obj_q(left, right, kind):
    """Wordless comparison with >/</= tick-boxes baked into the image."""
    return q("", "diagram", "____", "", "compare_choice",
              {"left_count": left, "right_count": right, "kind": kind})


def _base10_q(tens, ones):
    return q("", "diagram", "____", "", "base10_blocks", {"tens": tens, "ones": ones})


def _compare_obj_q(left, right, kind):
    return q("", "diagram", "____", "", "compare_choice",
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
        items.append(q(f"{n} + 1 = ____", "fill", "____"))
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
            items.append(q(f"{n} + 1 = ____", "fill", "____"))
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
                items.append(q(f"{n} + 1 = ____", "fill", "____"))
            elif mode == "before":
                items.append(q(f"{n} - 1 = ____", "fill", "____"))
            else:
                items.append(q(f"___, {n}, ___", "fill", "____"))
        return items

    items = [cb(f"{title} — Numbers Only", ["Apply +1 or -1 directly."], "")]
    for n in picks:
        if mode == "both":
            items.append(q(f"___, {n}, ___", "fill", "____"))
        elif mode == "after":
            items.append(q(f"{n} + 1 = ____", "fill", "____"))
        else:
            items.append(q(f"{n} - 1 = ____", "fill", "____"))
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
        items.append(q(f"___, {n}, ___", "fill", "____"))
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
            items.append(q(f"{l} ___ {r}", "fill", "____"))
        return items
    items = [cb("Comparing Numbers", ["Compare directly without pictures."], "")]
    for l, r in pairs:
        items.append(q(f"{l} ___ {r}", "fill", "____"))
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
        items.append(q(f"{l} ___ {r}", "fill", "____"))
    return items


def _1CUM3_s(sheet):
    random.seed(900 + sheet)
    pairs = [(random.randint(1, 100), random.randint(1, 100)) for _ in range(19)]
    items = [cb("Review: Greater & Smaller", ["Mix of small and large numbers."], "")]
    for l, r in pairs:
        items.append(q(f"{l} ___ {r}", "fill", "____"))
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
        items_out.append(q(f"{', '.join(display)}", "fill", "____"))
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
        items.append(q(f"{', '.join(display)}", "fill", "____"))
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
            items.append(q(f"____ x 10 + ____ = {n}", "fill", "____"))
        else:
            items.append(q(f"{tens} x 10 + {ones} = ____", "fill", "____"))
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
            items.append(q(f"{tens} x 10 + {ones} = ____", "fill", "____"))
    return items


# ───────────────────────── 1P: Counting objects & puzzles ─────────────────────────

def _1P_s(sheet):
    random.seed(1400 + sheet)
    if sheet == 1:
        items = [cb("Counting & Simple Puzzles",
                     ["Each picture shows objects, a + or - sign, and a blank box to fill."], "")]
        fixed = [(12,7,"-","apple"), (8,9,"+","star"), (15,6,"-","balloon"), (23,14,"-","flower")]
    elif sheet == 2:
        items = [cb("Picture Puzzles — Groups", [""], "")]
        fixed = [(34,0,"+","apple"), (45,20,"-","star"), (67,0,"+","balloon"), (58,9,"+","flower")]
    elif sheet == 3:
        items = [tb("Puzzle Tips", ["+ joins groups together. - takes a group away."])]
        fixed = [(72,35,"-","apple"), (48,26,"+","star"), (90,47,"-","balloon")]
    else:
        items = [cb("Number Puzzles — No Pictures", ["Solve using numbers only."], "")]
        fixed = []
    for l, r, op, kind in fixed:
        if r == 0:
            items.append(q(f"{l} = ____", "fill", "____"))
        else:
            items.append(q("", "diagram", "____", "", "visual_equation",
                            {"left": l, "right": r, "kind": kind, "op": op}))
    # Top up to 19 real items with symbolic +1 equations (no sentences)
    random.seed(1450 + sheet)
    while len([i for i in items if i["type"] not in ("concept_box", "tips_box")]) < 19:
        n = random.randint(10, 99)
        items.append(q(f"{n} + 1 = ____", "fill", "____"))
    return items


def _1Q_s(sheet):
    """Mixed challenge — pulls from every Level 1 skill."""
    random.seed(1500 + sheet)
    items = [cb("Level 1 Mixed Challenge",
                 ["This sheet mixes counting, before/after, comparing, missing numbers, patterns and place value."],
                 "")]
    builders = [
        lambda: q(f"{random.randint(1,99)} + 1 = ____", "fill", "____"),
        lambda: q(f"{random.randint(2,100)} - 1 = ____", "fill", "____"),
        lambda: q(f"{random.randint(1,100)} ___ {random.randint(1,100)}", "fill", "____"),
        lambda: (lambda n: q(f"{n//10} x 10 + {n%10} = ____", "fill", "____"))(random.randint(10,99)),
        lambda: q(f"{(s:=random.randint(1,40))}, {s+2}, {s+4}, ___", "fill", "____"),
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
        lambda: q(f"{random.randint(1,99)} + 1 = ____", "fill", "____"),
        lambda: q(f"{random.randint(2,100)} - 1 = ____", "fill", "____"),
        lambda: q(f"{random.randint(1,100)} ___ {random.randint(1,100)}", "fill", "____"),
        lambda: (lambda n: q(f"{n//10} x 10 + {n%10} = ____", "fill", "____"))(random.randint(10,99)),
        lambda: q(f"{(s:=random.randint(1,40))}, {s+5}, {s+10}, ___", "fill", "____"),
        lambda: q(f"{(s2:=random.randint(1,90))}, ___, {s2+2}", "fill", "____"),
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
# Registered as a brand-new level (Level 21 — display name "Counting &
# Numbers — Foundation, Class 1-2, Small Steps") using PLAIN letter codes,
# namespaced internally as "__L21__<code>" so they never collide with
# Pre-Level's own plain letters (A, B, C...) or with the original,
# untouched Level 1 (1A, 1B... still intact, unaffected by this file).

def _wrap(fn):
    return {1: lambda: fn(1), 2: lambda: fn(2), 3: lambda: fn(3), 4: lambda: fn(4)}


LEVEL21_NS = "__L21__"

LEVEL1_DISPATCH = {
    f"{LEVEL21_NS}A": _wrap(_1A_s), f"{LEVEL21_NS}B": _wrap(_1B_s),
    f"{LEVEL21_NS}C": _wrap(_1C_s), f"{LEVEL21_NS}CUM1": _wrap(_1CUM1_s),
    f"{LEVEL21_NS}D": _wrap(_1D_s), f"{LEVEL21_NS}E": _wrap(_1E_s),
    f"{LEVEL21_NS}F": _wrap(_1F_s), f"{LEVEL21_NS}G": _wrap(_1G_s),
    f"{LEVEL21_NS}CUM2": _wrap(_1CUM2_s),
    f"{LEVEL21_NS}H": _wrap(_1H_s), f"{LEVEL21_NS}I": _wrap(_1I_s),
    f"{LEVEL21_NS}CUM3": _wrap(_1CUM3_s),
    f"{LEVEL21_NS}J": _wrap(_1J_s), f"{LEVEL21_NS}K": _wrap(_1K_s),
    f"{LEVEL21_NS}CUM4": _wrap(_1CUM4_s),
    f"{LEVEL21_NS}L": _wrap(_1L_s), f"{LEVEL21_NS}M": _wrap(_1M_s),
    f"{LEVEL21_NS}CUM5": _wrap(_1CUM5_s),
    f"{LEVEL21_NS}N": _wrap(_1N_s), f"{LEVEL21_NS}O": _wrap(_1O_s),
    f"{LEVEL21_NS}CUM6": _wrap(_1CUM6_s),
    f"{LEVEL21_NS}P": _wrap(_1P_s), f"{LEVEL21_NS}Q": _wrap(_1Q_s),
    f"{LEVEL21_NS}REV": _wrap(_1REV_s),
}
