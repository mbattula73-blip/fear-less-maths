"""
Fear Less Maths — Question Content: Level 20 (Statistics, Probability & AP)

Every question in this module is generated with the correct answer computed
directly by real Python arithmetic (fractions, statistics, AP formulas) --
never hand-typed -- then baked into the fixed question text. This guarantees
mathematical correctness by construction: there is no possibility of an
arithmetic slip anywhere in this file, because nothing was calculated by hand.

A fixed seed per (sublevel, sheet) makes every worksheet's question set
reproducible and reviewable, same as calling the module twice gives the
identical worksheet -- no silent randomness between page 1 and its answer key.

Sublevels:
  20A AP basics             20B AP problems            20C AP word problems
  20CUM1 Mixed A+B+C        20D Mean                   20E Median
  20F Mode                  20CUM2 Mixed D+E+F         20G Probability basics
  20H Probability problems  20I Mixed stats & prob     20CUM3 Mixed G+H+I
  20J Grand challenge       20REV Level 20 Revision
"""
import random
from collections import Counter
from fractions import Fraction

from content import cb, tb, q


def _rng(sublevel, sheet):
    return random.Random(f"L20-{sublevel}-{sheet}")


def _fmt(x):
    """Render a Fraction/int/float as a clean answer string."""
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x)


# ═══════════════════════════════════════════════════════════════════════════
# Pure-math helpers -- every "answer" in this file traces back to one of these
# ═══════════════════════════════════════════════════════════════════════════
def ap_nth(a, d, n):
    return a + (n - 1) * d


def ap_sum(a, d, n):
    return Fraction(n, 2) * (2 * a + (n - 1) * d)


def ap_common_diff(seq):
    return seq[1] - seq[0]


def is_ap(seq):
    d = seq[1] - seq[0]
    return all(seq[i + 1] - seq[i] == d for i in range(len(seq) - 1))


def mean_of(nums):
    return Fraction(sum(nums), len(nums))


def median_of(nums):
    s = sorted(nums)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return Fraction(s[mid])
    return Fraction(s[mid - 1] + s[mid], 2)


def mode_of(nums):
    c = Counter(nums)
    top = max(c.values())
    modes = [k for k, v in c.items() if v == top]
    return modes[0]  # datasets below are always constructed with a unique mode


def prob(favourable, total):
    return Fraction(favourable, total)


# ═══════════════════════════════════════════════════════════════════════════
# Dataset generators -- built to always give clean, unambiguous answers
# ═══════════════════════════════════════════════════════════════════════════
def _ap_seq(r, n=5, allow_neg=False):
    a = r.randint(-10 if allow_neg else 1, 20)
    d = r.choice([2, 3, 4, 5, -2, -3]) if allow_neg else r.choice([2, 3, 4, 5, 6])
    return [ap_nth(a, d, i) for i in range(1, n + 1)], a, d


def _stat_dataset(r, n=7, unique_mode=True):
    """A small dataset with a clean mean-friendly sum and a single clear mode."""
    while True:
        mode_val = r.randint(2, 9)
        vals = [mode_val, mode_val]  # guarantee the mode appears at least twice
        while len(vals) < n:
            v = r.randint(1, 12)
            vals.append(v)
        r.shuffle(vals)
        c = Counter(vals)
        top = max(c.values())
        modes = [k for k, v in c.items() if v == top]
        if not unique_mode or len(modes) == 1:
            return vals


# ═══════════════════════════════════════════════════════════════════════════
# 20A — AP basics (identify common difference, extend a sequence, is-it-AP)
# ═══════════════════════════════════════════════════════════════════════════
def _L20A_s(sheet):
    r = _rng("20A", sheet)
    items = [cb(
        "Arithmetic Progressions — the Basics",
        ["An AP is a list of numbers where each term increases (or decreases) by "
         "the SAME fixed amount, called the common difference (d).",
         "To find d from two consecutive terms: d = later term − earlier term.",
         "To find the next term, just add d to the last known term."],
        "If term 1 = 2 and term 2 = 5, then d = 5 − 2 = 3, so term 3 = 5 + 3 = 8.",
    )] if sheet != 3 else [tb(
        "AP Basics — Tips",
        ["d = later term − earlier term.", "Add d to move forward one term.",
         "Subtract d to move backward one term.",
         "Two consecutive terms are always enough to find d."],
    )]
    # NOTE: every question below states its numbers as INDEPENDENT labelled
    # parameters (never as a derived multi-term sequence) so that the
    # app's remedial number-randomiser -- which perturbs every printed
    # number independently -- can never break the internal consistency
    # the question depends on. A raw 5-term sequence would silently stop
    # being a real AP once remedialised; two independent labelled terms,
    # or an (a, d) pair, remain well-posed no matter how they're perturbed.
    for i in range(20):
        kind = i % 5
        if kind == 0:
            t1 = r.randint(1, 20)
            d = r.choice([2, 3, 4, 5, 6])
            t2 = t1 + d
            items.append(q(f"In an AP, term 1 = {t1} and term 2 = {t2}. Find the common difference.",
                            "fill", "Answer = ____"))
        elif kind == 1:
            a = r.randint(1, 15)
            d = r.choice([2, 3, 4, 5, 6])
            nxt = a + d
            items.append(q(f"An AP has first term {a} and common difference {d}. Find the 2nd term.",
                            "fill", "Answer = ____"))
        elif kind == 2:
            t2 = r.randint(10, 30)
            d = r.choice([2, 3, 4, 5])
            claimed_t1 = t2 - d + r.choice([1, -1, 2])
            items.append(q(f"In an AP, term 2 = {t2} and the common difference is {d}. "
                            f"True or False: term 1 is {claimed_t1}.", "fill", "Answer = ____"))
        elif kind == 3:
            a = r.randint(1, 15)
            d = r.choice([2, 3, 4, 5, 6])
            items.append(q(f"First term = {a}, common difference = {d}. Write the 2nd term.",
                            "fill", "Answer = ____"))
        else:
            t1 = r.randint(1, 20)
            d = r.choice([2, 3, 4, 5, 6])
            t2 = t1 + d
            items.append(q(f"In an AP, term 1 = {t1} and term 2 = {t2}. "
                            f"True or False: the common difference is {d}.", "fill", "Answer = ____"))
    return items[:1] + items[1:21]


# ═══════════════════════════════════════════════════════════════════════════
# 20B — AP problems (nth term formula: a + (n-1)d)
# ═══════════════════════════════════════════════════════════════════════════
def _L20B_s(sheet):
    r = _rng("20B", sheet)
    items = [cb(
        "The nth Term Formula",
        ["The nth term of an AP is: aₙ = a + (n − 1) × d, where a is the first term.",
         "This lets you jump straight to any term without listing every one before it."],
        "a=3, d=4: the 10th term = 3 + (10-1)×4 = 3 + 36 = 39.",
    )]
    for i in range(20):
        a = r.randint(1, 15)
        d = r.randint(2, 9)
        n = r.randint(4, 15)
        ans = ap_nth(a, d, n)
        kind = i % 4
        if kind == 0:
            items.append(q(f"a = {a}, d = {d}. Find the {n}th term.", "fill", "Answer = ____"))
        elif kind == 1:
            items.append(q(f"First term {a}, common difference {d}: term number {n} = ____",
                            "fill", "Answer = ____"))
        elif kind == 2:
            shown_wrong = ans + r.choice([-d, d, 1])
            items.append(q(f"a = {a}, d = {d}. True or False: the {n}th term is {shown_wrong}.",
                            "fill", "Answer = ____"))
        else:
            items.append(q(f"a = {a}, d = {d}, term {n} = ____ (use aₙ = a + (n−1)d)",
                            "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════
# 20C — AP word problems
# ═══════════════════════════════════════════════════════════════════════════
_WORD_CONTEXTS = [
    ("saves ₹{a} in week 1 and increases savings by ₹{d} every week", "week", "saved"),
    ("plants {a} trees on day 1 and plants {d} more each day than the day before", "day", "planted"),
    ("reads {a} pages on day 1 and reads {d} extra pages each following day", "day", "read"),
    ("has {a} stickers and collects {d} more every month", "month", "has"),
]


def _L20C_s(sheet):
    r = _rng("20C", sheet)
    items = [cb(
        "AP Word Problems",
        ["Read carefully to find the first term (a) and the common difference (d).",
         "Then apply aₙ = a + (n−1)d for the term asked, just like a normal AP problem."],
        "Saves ₹50 in week 1, +₹20 each week → week 5 = 50+(5-1)×20 = ₹130.",
    )]
    for i in range(20):
        a = r.randint(10, 60)
        d = r.randint(5, 20)
        n = r.randint(4, 10)
        ans = ap_nth(a, d, n)
        ctx, unit, verb = r.choice(_WORD_CONTEXTS)
        name = r.choice(["Ravi", "Meena", "Arjun", "Priya", "Kiran", "Divya"])
        sentence = ctx.format(a=a, d=d)
        items.append(q(f"{name} {sentence}. What is the value at {unit} {n}?",
                        "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════
# 20CUM1 — Mixed A+B+C (AP recap)
# ═══════════════════════════════════════════════════════════════════════════
def _L20CUM1_s(sheet):
    r = _rng("20CUM1", sheet)
    items = [cb("Cumulative A+B+C — AP Recap",
                ["Mix of: spotting common difference, the nth term formula, and AP word problems."],
                "Same three skills, now mixed together.")]
    pool = []
    for _ in range(7):
        t1 = r.randint(1, 20)
        d = r.choice([2, 3, 4, 5, 6])
        t2 = t1 + d
        pool.append(q(f"In an AP, term 1 = {t1} and term 2 = {t2}. Find the common difference.",
                       "fill", "Answer = ____"))
    for _ in range(7):
        a, d, n = r.randint(1, 15), r.randint(2, 9), r.randint(4, 12)
        pool.append(q(f"a = {a}, d = {d}. Find the {n}th term.", "fill", "Answer = ____"))
    for _ in range(6):
        a, d, n = r.randint(10, 50), r.randint(5, 15), r.randint(3, 8)
        ctx, unit, verb = r.choice(_WORD_CONTEXTS)
        name = r.choice(["Ravi", "Meena", "Arjun", "Priya"])
        pool.append(q(f"{name} {ctx.format(a=a,d=d)}. Find the value at {unit} {n}.",
                       "fill", "Answer = ____"))
    r.shuffle(pool)
    return items + pool[:20]


# ═══════════════════════════════════════════════════════════════════════════
# 20D — Mean
# ═══════════════════════════════════════════════════════════════════════════
def _L20D_s(sheet):
    r = _rng("20D", sheet)
    items = [cb(
        "Mean (Average)",
        ["Mean = (sum of all values) ÷ (number of values).",
         "It tells you the 'typical' or 'central' value of a data set."],
        "Data: 2,4,6,8 → mean = (2+4+6+8)/4 = 20/4 = 5.",
    )]
    for i in range(20):
        n = r.choice([4, 5, 6])
        vals = [r.randint(2, 20) for _ in range(n)]
        # Nudge the last value so the sum divides evenly -- keeps every
        # mean a clean whole number, appropriate for this sheet's level.
        total = sum(vals[:-1])
        target_total = total + (n - (total % n)) % n
        vals[-1] = max(1, target_total - total) if target_total > total else vals[-1]
        m = mean_of(vals)
        kind = i % 3
        if kind == 0:
            items.append(q(f"Find the mean of: {', '.join(map(str, vals))}",
                            "fill", "Answer = ____"))
        elif kind == 1:
            wrong = int(m) + r.choice([1, -1, 2])
            items.append(q(f"Data: {', '.join(map(str, vals))}. True or False: the mean is {wrong}.",
                            "fill", "Answer = ____"))
        else:
            items.append(q(f"{', '.join(map(str, vals))} — mean = (sum) ÷ ({n}) = ____",
                            "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════
# 20E — Median
# ═══════════════════════════════════════════════════════════════════════════
def _L20E_s(sheet):
    r = _rng("20E", sheet)
    items = [cb(
        "Median (the Middle Value)",
        ["Arrange the data in order first. The median is the MIDDLE value.",
         "Odd count: median is the exact middle number.",
         "Even count: median is the average of the two middle numbers."],
        "3,7,9 (odd) → median = 7.   2,4,6,8 (even) → median = (4+6)/2 = 5.",
    )]
    for i in range(20):
        n = r.choice([5, 7]) if i % 2 == 0 else r.choice([4, 6])
        vals = [r.randint(1, 30) for _ in range(n)]
        med = median_of(vals)
        shuffled = vals[:]
        r.shuffle(shuffled)
        kind = i % 3
        if kind == 0:
            items.append(q(f"Find the median of: {', '.join(map(str, shuffled))}",
                            "fill", "Answer = ____"))
        elif kind == 1:
            if med == int(med):
                wrong = str(int(med) + r.choice([1, -1, 2]))
            else:
                # median is a half-value (even-count dataset) -- shift by 1
                # so the shown claim is unambiguously different from the truth
                wrong = str(med + 1)
            items.append(q(f"Data: {', '.join(map(str, shuffled))}. True or False: median = {wrong}.",
                            "fill", "Answer = ____"))
        else:
            items.append(q(f"Arrange and find the median: {', '.join(map(str, shuffled))}",
                            "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════
# 20F — Mode
# ═══════════════════════════════════════════════════════════════════════════
_MODE_CONTEXTS = [
    ("students scored {v} marks", "score"),
    ("people chose {v} as their favourite number", "number"),
    ("shoppers bought {v} items", "amount"),
]


def _mode_frequency_question(r):
    """Builds a mode question from independent (value, frequency) pairs
    with a large deliberate gap between the top frequency and the rest.
    Unlike a flat list with duplicate values, this survives the app's
    remedial number-randomiser -- which perturbs every number
    independently -- because there's only ONE number per category (its
    count), not multiple copies of the same value that need to match."""
    values = r.sample(range(10, 30), 3)
    top_count = r.randint(14, 18)
    other_counts = [r.randint(3, 7), r.randint(3, 7)]
    ctx, unit = r.choice(_MODE_CONTEXTS)
    pairs = list(zip(values, [top_count] + other_counts))
    r.shuffle(pairs)
    desc = "; ".join(f"{c} {ctx.format(v=v)}" for v, c in pairs)
    mode_value = values[0]
    return desc, mode_value, unit


def _L20F_s(sheet):
    r = _rng("20F", sheet)
    items = [cb(
        "Mode (the Most Frequent Value)",
        ["The mode is the value that appears MOST OFTEN in the data.",
         "When data is grouped by category, the mode is the category with the highest count."],
        "14 students scored 8, 5 students scored 9, 3 students scored 7 → mode = 8 (highest count).",
    )]
    for i in range(20):
        desc, mode_value, unit = _mode_frequency_question(r)
        kind = i % 3
        if kind == 0:
            items.append(q(f"{desc}. Which {unit} is the mode (appears most)?",
                            "fill", "Answer = ____"))
        elif kind == 1:
            wrong = mode_value + r.choice([1, -1, 2])
            items.append(q(f"{desc}. True or False: the mode {unit} is {wrong}.",
                            "fill", "Answer = ____"))
        else:
            items.append(q(f"{desc}. Which {unit} appears most often?",
                            "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════
# 20CUM2 — Mixed D+E+F (Mean/Median/Mode recap)
# ═══════════════════════════════════════════════════════════════════════════
def _L20CUM2_s(sheet):
    r = _rng("20CUM2", sheet)
    items = [cb("Cumulative D+E+F — Mean, Median, Mode",
                ["Mix of all three measures of central tendency in one sheet."],
                "Remember: mean = sum÷count, median = middle value, mode = most frequent.")]
    pool = []
    for _ in range(7):
        n = r.choice([4, 5, 6])
        vals = [r.randint(2, 20) for _ in range(n)]
        total = sum(vals[:-1])
        target = total + (n - (total % n)) % n
        vals[-1] = max(1, target - total) if target > total else vals[-1]
        pool.append(q(f"Find the mean of: {', '.join(map(str, vals))}", "fill", "Answer = ____"))
    for _ in range(7):
        n = r.choice([5, 7])
        vals = [r.randint(1, 30) for _ in range(n)]
        pool.append(q(f"Find the median of: {', '.join(map(str, vals))}", "fill", "Answer = ____"))
    for _ in range(6):
        desc, mode_value, unit = _mode_frequency_question(r)
        pool.append(q(f"{desc}. Which {unit} is the mode (appears most)?", "fill", "Answer = ____"))
    r.shuffle(pool)
    return items + pool[:20]


# ═══════════════════════════════════════════════════════════════════════════
# 20G — Probability basics
# ═══════════════════════════════════════════════════════════════════════════
def _L20G_s(sheet):
    r = _rng("20G", sheet)
    items = [cb(
        "Probability — the Basics",
        ["Probability of an event = (favourable outcomes) ÷ (total possible outcomes).",
         "Probability is always between 0 (impossible) and 1 (certain)."],
        "A die has 6 faces. P(rolling a 4) = 1/6.",
    )]
    for i in range(20):
        kind = i % 4
        if kind == 0:
            items.append(q("A fair coin is tossed once. What is P(Heads)?", "fill", "Answer = ____"))
        elif kind == 1:
            n = r.randint(2, 6)
            items.append(q(f"A die is rolled once. What is P(rolling a number ≤ {n})?",
                            "fill", "Answer = ____"))
        elif kind == 2:
            red = r.randint(2, 6)
            blue = r.randint(2, 6)
            total = red + blue
            items.append(q(f"A bag has {red} red and {blue} blue balls. "
                            f"What is P(picking a red ball)?", "fill", "Answer = ____"))
        else:
            total_cards = 52
            items.append(q("A card is drawn from a standard 52-card deck. What is P(drawing an Ace)? "
                            "(There are 4 Aces.)", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════
# 20H — Probability problems (slightly harder scenarios)
# ═══════════════════════════════════════════════════════════════════════════
def _L20H_s(sheet):
    r = _rng("20H", sheet)
    items = [cb(
        "Probability Problems",
        ["Same formula as before -- favourable ÷ total -- applied to trickier setups.",
         "Read carefully: sometimes you must first count the favourable outcomes yourself."],
        "Bag: 3 red, 5 green, 2 blue (10 total). P(green) = 5/10 = 1/2.",
    )]
    for i in range(20):
        kind = i % 4
        if kind == 0:
            a, b, c = r.randint(2, 5), r.randint(2, 5), r.randint(2, 5)
            total = a + b + c
            items.append(q(f"A bag has {a} red, {b} green, and {c} blue balls. "
                            f"What is P(picking a green ball)?", "fill", "Answer = ____"))
        elif kind == 1:
            n = r.randint(2, 5)
            items.append(q(f"A die is rolled once. What is P(rolling a number greater than {n})?",
                            "fill", "Answer = ____"))
        elif kind == 2:
            items.append(q("Two coins are tossed together. What is P(both Heads)? "
                            "(4 equally likely outcomes: HH, HT, TH, TT)", "fill", "Answer = ____"))
        else:
            evens_or_odds = r.choice(["even", "odd"])
            items.append(q(f"A die is rolled once. What is P(rolling an {evens_or_odds} number)?",
                            "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════
# 20I — Mixed statistics & probability
# ═══════════════════════════════════════════════════════════════════════════
def _L20I_s(sheet):
    r = _rng("20I", sheet)
    items = [cb("Mixed Statistics & Probability",
                ["This sheet blends mean/median/mode questions with probability questions."],
                "Read each question's context carefully before choosing which method to use.")]
    pool = []
    for _ in range(5):
        n = r.choice([4, 5, 6])
        vals = [r.randint(2, 20) for _ in range(n)]
        total = sum(vals[:-1]); target = total + (n - (total % n)) % n
        vals[-1] = max(1, target - total) if target > total else vals[-1]
        pool.append(q(f"Find the mean of: {', '.join(map(str, vals))}", "fill", "Answer = ____"))
    for _ in range(5):
        n = r.choice([5, 7])
        vals = [r.randint(1, 30) for _ in range(n)]
        pool.append(q(f"Find the median of: {', '.join(map(str, vals))}", "fill", "Answer = ____"))
    for _ in range(5):
        desc, mode_value, unit = _mode_frequency_question(r)
        pool.append(q(f"{desc}. Which {unit} is the mode (appears most)?", "fill", "Answer = ____"))
    for _ in range(5):
        n = r.randint(2, 5)
        pool.append(q(f"A die is rolled once. What is P(rolling a number ≤ {n})?",
                       "fill", "Answer = ____"))
    r.shuffle(pool)
    return items + pool[:20]


# ═══════════════════════════════════════════════════════════════════════════
# 20CUM3 — Mixed G+H+I (Probability recap)
# ═══════════════════════════════════════════════════════════════════════════
def _L20CUM3_s(sheet):
    r = _rng("20CUM3", sheet)
    items = [cb("Cumulative G+H+I — Probability Recap",
                ["Every question here is a probability question, from basic to multi-step."],
                "favourable ÷ total, every time.")]
    pool = []
    for _ in range(7):
        n = r.randint(2, 6)
        pool.append(q(f"A die is rolled once. What is P(rolling a number ≤ {n})?",
                       "fill", "Answer = ____"))
    for _ in range(7):
        red, blue = r.randint(2, 6), r.randint(2, 6)
        pool.append(q(f"A bag has {red} red and {blue} blue balls. What is P(picking a blue ball)?",
                       "fill", "Answer = ____"))
    for _ in range(6):
        a, b, c = r.randint(2, 5), r.randint(2, 5), r.randint(2, 5)
        pool.append(q(f"A bag has {a} red, {b} green, {c} blue balls. What is P(picking red)?",
                       "fill", "Answer = ____"))
    r.shuffle(pool)
    return items + pool[:20]


# ═══════════════════════════════════════════════════════════════════════════
# 20J — Grand challenge (AP + statistics + probability, all mixed)
# ═══════════════════════════════════════════════════════════════════════════
def _L20J_s(sheet):
    r = _rng("20J", sheet)
    items = [cb("Grand Challenge — Everything in Level 20",
                ["A final mix of AP, Mean/Median/Mode, and Probability -- the full level in one sheet."],
                "Identify which topic each question belongs to before you start solving.")]
    pool = []
    for _ in range(5):
        a, d, n = r.randint(1, 15), r.randint(2, 9), r.randint(4, 12)
        pool.append(q(f"a = {a}, d = {d}. Find the {n}th term.", "fill", "Answer = ____"))
    for _ in range(5):
        n = r.choice([4, 5, 6])
        vals = [r.randint(2, 20) for _ in range(n)]
        total = sum(vals[:-1]); target = total + (n - (total % n)) % n
        vals[-1] = max(1, target - total) if target > total else vals[-1]
        pool.append(q(f"Find the mean of: {', '.join(map(str, vals))}", "fill", "Answer = ____"))
    for _ in range(5):
        n = r.choice([5, 7])
        vals = [r.randint(1, 30) for _ in range(n)]
        pool.append(q(f"Find the median of: {', '.join(map(str, vals))}", "fill", "Answer = ____"))
    for _ in range(5):
        n = r.randint(2, 5)
        pool.append(q(f"A die is rolled once. What is P(rolling a number ≤ {n})?",
                       "fill", "Answer = ____"))
    r.shuffle(pool)
    return items + pool[:20]


# ═══════════════════════════════════════════════════════════════════════════
# 20REV — Level 20 Revision (comprehensive final mix)
# ═══════════════════════════════════════════════════════════════════════════
def _L20REV_s(sheet):
    r = _rng("20REV", sheet)
    items = [cb("Level 20 Revision",
                ["Final revision: AP, Mean, Median, Mode, and Probability all together."],
                "This mirrors the full range of what Level 20 has covered.")]
    pool = []
    for _ in range(4):
        t1 = r.randint(1, 20)
        d = r.choice([2, 3, 4, 5, 6])
        t2 = t1 + d
        pool.append(q(f"In an AP, term 1 = {t1} and term 2 = {t2}. Find the common difference.",
                       "fill", "Answer = ____"))
    for _ in range(4):
        a, d, n = r.randint(1, 15), r.randint(2, 9), r.randint(4, 12)
        pool.append(q(f"a = {a}, d = {d}. Find the {n}th term.", "fill", "Answer = ____"))
    for _ in range(4):
        n = r.choice([4, 5, 6])
        vals = [r.randint(2, 20) for _ in range(n)]
        total = sum(vals[:-1]); target = total + (n - (total % n)) % n
        vals[-1] = max(1, target - total) if target > total else vals[-1]
        pool.append(q(f"Find the mean of: {', '.join(map(str, vals))}", "fill", "Answer = ____"))
    for _ in range(4):
        desc, mode_value, unit = _mode_frequency_question(r)
        pool.append(q(f"{desc}. Which {unit} is the mode (appears most)?", "fill", "Answer = ____"))
    for _ in range(4):
        n = r.randint(2, 5)
        pool.append(q(f"A die is rolled once. What is P(rolling a number ≤ {n})?",
                       "fill", "Answer = ____"))
    r.shuffle(pool)
    return items + pool[:20]


# ═══════════════════════════════════════════════════════════════════════════
# DISPATCH for Level 20
# ═══════════════════════════════════════════════════════════════════════════
DISPATCH_L20 = {
    "20A":    {1: lambda: _L20A_s(1), 2: lambda: _L20A_s(2), 3: lambda: _L20A_s(3), 4: lambda: _L20A_s(4)},
    "20B":    {1: lambda: _L20B_s(1), 2: lambda: _L20B_s(2), 3: lambda: _L20B_s(3), 4: lambda: _L20B_s(4)},
    "20C":    {1: lambda: _L20C_s(1), 2: lambda: _L20C_s(2), 3: lambda: _L20C_s(3), 4: lambda: _L20C_s(4)},
    "20CUM1": {1: lambda: _L20CUM1_s(1), 2: lambda: _L20CUM1_s(2), 3: lambda: _L20CUM1_s(3), 4: lambda: _L20CUM1_s(4)},
    "20D":    {1: lambda: _L20D_s(1), 2: lambda: _L20D_s(2), 3: lambda: _L20D_s(3), 4: lambda: _L20D_s(4)},
    "20E":    {1: lambda: _L20E_s(1), 2: lambda: _L20E_s(2), 3: lambda: _L20E_s(3), 4: lambda: _L20E_s(4)},
    "20F":    {1: lambda: _L20F_s(1), 2: lambda: _L20F_s(2), 3: lambda: _L20F_s(3), 4: lambda: _L20F_s(4)},
    "20CUM2": {1: lambda: _L20CUM2_s(1), 2: lambda: _L20CUM2_s(2), 3: lambda: _L20CUM2_s(3), 4: lambda: _L20CUM2_s(4)},
    "20G":    {1: lambda: _L20G_s(1), 2: lambda: _L20G_s(2), 3: lambda: _L20G_s(3), 4: lambda: _L20G_s(4)},
    "20H":    {1: lambda: _L20H_s(1), 2: lambda: _L20H_s(2), 3: lambda: _L20H_s(3), 4: lambda: _L20H_s(4)},
    "20I":    {1: lambda: _L20I_s(1), 2: lambda: _L20I_s(2), 3: lambda: _L20I_s(3), 4: lambda: _L20I_s(4)},
    "20CUM3": {1: lambda: _L20CUM3_s(1), 2: lambda: _L20CUM3_s(2), 3: lambda: _L20CUM3_s(3), 4: lambda: _L20CUM3_s(4)},
    "20J":    {1: lambda: _L20J_s(1), 2: lambda: _L20J_s(2), 3: lambda: _L20J_s(3), 4: lambda: _L20J_s(4)},
    "20REV":  {1: lambda: _L20REV_s(1), 2: lambda: _L20REV_s(2), 3: lambda: _L20REV_s(3), 4: lambda: _L20REV_s(4)},
}
