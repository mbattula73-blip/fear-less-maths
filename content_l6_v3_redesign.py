"""
Fear Less Maths — LEVEL 6 (Factors, Multiples, HCF & LCM)
v3 REWRITE (2026-08-04) — new worksheet architecture per direct request:

  20 questions per sheet, in three purposeful blocks instead of one flat
  block of 20 same-topic questions:

  Block 1 (Q1-12) — THIS SHEET'S topic (e.g. Factors for 6A), following
    Concrete->Abstract:
      Q1-6  concrete, WITH a diagram (factor array: Q1-2 worked/shown,
            Q3-6 blank scaffold for the student to fill in)
      Q7-12 abstract, NO diagram, same skill at slightly harder numbers,
            deliberately varied in shape (computation, word problem,
            reverse-thinking, error-spotting, true/false) so the block
            still exercises more than rote recall

  Block 2 (Q13-15) — "Quick Review": one question each pulled from the
    THREE prior levels that Factors/HCF/LCM is directly built on --
    Level 2 (primes), Level 4 (multiplication facts), Level 5 (division
    facts). Spaced-repetition checkpoint across the actual prerequisite
    skills, not random old content.

  Block 3 (Q16-20) — "Speed Calculation": five rapid multiplication/
    division fact questions, no diagram, no story -- the specific
    computational fluency (times tables + division facts) a student
    needs to find factors quickly. This is deliberately distinct from
    Block 2: Block 2 is a breadth checkpoint (one of each skill), Block
    3 is depth practice on the exact facts this level leans on hardest.

  Both new blocks escalate in difficulty across sheets 1->4 the same way
  Block 1 does, so the whole sheet keeps one coherent difficulty curve.
"""
import random
from content import cb, q


def _l6v3_is_prime(n):
    if n < 2:
        return False
    for k in range(2, int(n ** 0.5) + 1):
        if n % k == 0:
            return False
    return True


def _l6v3_factors_of(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def _l6v3_esc_pick(pool, n, used=None):
    pool_sorted = sorted(set(pool))
    if used is None:
        used = set()
    available = [v for v in pool_sorted if v not in used]
    out = []
    for i in range(n):
        if not available:
            available = [v for v in pool_sorted if v not in set(out)] or pool_sorted
        idx = int(round(i / max(n - 1, 1) * (len(available) - 1)))
        idx = max(0, min(len(available) - 1, idx))
        lo_idx, hi_idx = max(0, idx - 1), min(len(available) - 1, idx + 1)
        pick_idx = random.randint(lo_idx, hi_idx)
        choice = available.pop(pick_idx)
        used.add(choice)
        out.append(choice)
    return out


def _l6v3_quick_review(sheet):
    """3 questions: one prime check (Level 2), one multiplication fact
    (Level 4), one division fact (Level 5) -- the three skills Factors/
    HCF/LCM is built directly on top of. Difficulty escalates with sheet
    the same way Block 1 does."""
    prime_ranges = {1: (11, 40), 2: (20, 60), 3: (30, 80), 4: (40, 100)}
    fact_ranges = {1: (2, 6), 2: (3, 8), 3: (5, 10), 4: (6, 12)}
    plo, phi = prime_ranges[sheet]
    flo, fhi = fact_ranges[sheet]

    n = random.randint(plo, phi)
    is_p = _l6v3_is_prime(n)
    items = [q(f"Quick Review (Level 2): Is {n} prime or composite?", "fill", "Answer = ____")]

    a, b = random.randint(flo, fhi), random.randint(flo, fhi)
    items.append(q(f"Quick Review (Level 4): {a} x {b} = ____", "fill", "Answer = ____"))

    b2 = random.randint(flo, fhi)
    k = random.randint(flo, fhi)
    a2 = b2 * k
    items.append(q(f"Quick Review (Level 5): {a2} / {b2} = ____", "fill", "Answer = ____"))

    return items


def _l6v3_speed_calc(sheet):
    """5 rapid multiplication/division fact questions -- the exact
    computational fluency behind quick factor-finding. No diagram, no
    story, no HCF/LCM framing -- pure speed practice."""
    fact_ranges = {1: (2, 7), 2: (3, 9), 3: (5, 11), 4: (7, 12)}
    lo, hi = fact_ranges[sheet]
    items = []
    for i in range(5):
        if i % 2 == 0:
            a, b = random.randint(lo, hi), random.randint(lo, hi)
            items.append(q(f"Speed Calculation: {a} x {b} = ____", "fill", "Answer = ____"))
        else:
            b = random.randint(lo, hi)
            k = random.randint(lo, hi)
            a = b * k
            items.append(q(f"Speed Calculation: {a} / {b} = ____", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 6A v3 — Factors
# ═══════════════════════════════════════════════════════════════════════════════
def _L6A_v3_s(sheet):
    random.seed(6100 + sheet)
    ranges = {1: (8, 30), 2: (16, 48), 3: (24, 72), 4: (36, 100)}
    lo, hi = ranges[sheet]
    items = [
        cb("Factors", [
            "A factor of a number divides it EXACTLY, with no remainder.",
            "Every number has 1 and itself as factors.",
        ], "Factors of 12: 1, 2, 3, 4, 6, 12."),
    ]

    # Block 1a: Q1-6, concrete, WITH diagram (Q1-2 worked, Q3-6 blank scaffold)
    concrete_pool = _l6v3_esc_pick(range(lo, hi), 6)
    for i, n in enumerate(concrete_pool):
        blank = i >= 2
        items.append(q(f"List ALL factors of {n}.", "diagram", "Answer = ____", "",
                        "factor_array", {"n": n, "blank": blank}))

    # Block 1b: Q7-12, abstract, NO diagram, deliberately varied shapes
    used = set(concrete_pool)
    abstract_pool = _l6v3_esc_pick(range(lo, hi), 2, used=used)
    for n in abstract_pool:
        items.append(q(f"List ALL factors of {n}.", "fill", "Answer = ____"))

    n = random.randint(lo, hi)
    ctx = random.choice([
        f"A gardener has {n} plants to place in equal rows with no leftovers. List every row-size that works.",
        f"{n} sweets are shared equally among some friends with none left over. List every possible number of friends.",
    ])
    items.append(q(ctx, "word", "Answer = ____"))

    n = random.randint(lo, hi)
    d = random.choice(_l6v3_factors_of(n))
    wrong = d + random.choice([1, -1, 2])
    items.append(q(f"{n} has a factor that is one of: {d}, {wrong}. Which one is the TRUE factor, and why does the other one fail?", "word", "Answer = ____"))

    n = random.randint(lo, hi)
    fake_factor = random.choice([n + 1, n - 1] + [d for d in range(2, 12) if n % d != 0])
    items.append(q(f"A student says {fake_factor} is a factor of {n}. Check by dividing -- are they right? If not, what's the remainder?", "word", "Answer = ____"))

    n = random.randint(lo, hi)
    claim = random.choice([True, False])
    if claim:
        d = random.choice(_l6v3_factors_of(n))
        items.append(q(f"True or False: {d} is a factor of {n}.", "fill", "Answer = ____"))
    else:
        d = n + random.choice([1, 3])
        items.append(q(f"True or False: {d} is a factor of {n}.", "fill", "Answer = ____"))

    # Block 2: Q13-15, Quick Review (Levels 2, 4, 5)
    items += _l6v3_quick_review(sheet)

    # Block 3: Q16-20, Speed Calculation
    items += _l6v3_speed_calc(sheet)

    return items


def _l6v3_short_prompt(item):
    """Some Level 6 diagram questions carry long word-problem phrasing
    (e.g. 'A school has 24 boys and 30 girls for team photos -- largest
    group size...' for a ladder-division HCF question). That phrasing is
    great for the abstract/application block, but for Block 1a -- the
    concrete teaching block, short prompt + rich diagram -- a terse
    direct prompt using the same numbers and same diagram fits the
    purpose better AND costs far less vertical space. factor_array's
    existing 'List ALL factors of N' is already short and is left as-is."""
    dt = item.get("diagram_type")
    p = item.get("diagram_params") or {}
    if dt == "ladder_division":
        mode = p.get("mode", "hcf").upper()
        return f"Find the {mode} of {p.get('a')} and {p.get('b')} (ladder method)."
    if dt == "euclidean_algorithm":
        return f"Use the Euclidean Algorithm to find HCF({p.get('a')}, {p.get('b')})."
    if dt == "venn_two":
        return f"Venn diagram: prime factors of {p.get('label_a')} and {p.get('label_b')}."
    if dt == "hundred_grid_highlight":
        n = p.get("n", (p.get("highlight") or [""])[0])
        return f"Is {n} prime or composite? (hundred grid)"
    if dt == "factor_array" and "n" in p:
        return f"List ALL factors of {p['n']}."
    return item.get("text", "")


def _l6v3_build_from_existing(sublevel_fn, sheet):
    """Applies the v3 architecture (Block1: 12 topic Qs w/ 6 diagrams,
    Block2: 3 Quick Review, Block3: 5 Speed Calc) to ANY existing Level 6
    sublevel function, by sampling from its already-curriculum-vetted 20
    questions rather than re-authoring content per topic.

    Every _L6X_s function in content_l6_redesign.py follows the same
    fixed internal shape (verified across sublevels): the diagram
    questions come first (already split 2 worked / rest blank by the
    _Sheet class), followed by a fixed-order tail of 4 word-context + 3
    reverse-thinking + 2 error-spotting + 1 True/False questions. We take
    the first 6 diagram questions as-is (their worked/blank split is
    already correct) and a representative 6 from the tail -- 2 word, 2
    reverse, 1 error, 1 T/F -- preserving the question-type variety
    instead of just truncating to the first 6."""
    items = sublevel_fn(sheet)
    concept_items = [x for x in items if x.get("type") in ("concept_box", "tips_box")]
    qs = [x for x in items if x.get("type") not in ("concept_box", "tips_box")]
    diagram_qs = [x for x in qs if x.get("diagram_type")]
    tail_qs = [x for x in qs if not x.get("diagram_type")]

    block1a = []
    for x in diagram_qs[:6]:
        y = dict(x)
        y["text"] = _l6v3_short_prompt(x)
        block1a.append(y)
    # Pick 6 tail questions favouring variety first, length second: walk the
    # known type-order (word/word/reverse/reverse/error/T-F) and within that
    # preference always take whichever remaining tail item is shortest, so
    # verbose topics (Euclidean Algorithm reasoning, Venn-diagram word
    # problems) don't blow the page budget the way a fixed-position pick
    # would.
    tail_sorted = sorted(range(len(tail_qs)), key=lambda i: len(tail_qs[i].get("text", "")))
    block1b = [tail_qs[i] for i in tail_sorted[:6]]
    block1b.sort(key=lambda x: tail_qs.index(x))

    block2 = _l6v3_quick_review(sheet)
    block3 = _l6v3_speed_calc(sheet)
    return concept_items + block1a + block1b + block2 + block3


# ═══════════════════════════════════════════════════════════════════════════════
# Every Level 6 sublevel, v3 architecture
# ═══════════════════════════════════════════════════════════════════════════════
import content_l6_redesign as _L6

_V3_SOURCE_FN = {
    "6A": _L6._L6A_s, "6B": _L6._L6B_s, "6C": _L6._L6C_s,
    "6CUM1": _L6._L6CUM1_s, "6D": _L6._L6D_s, "6E": _L6._L6E_s,
    "6F": _L6._L6F_s, "6CUM2": _L6._L6CUM2_s, "6G": _L6._L6G_s,
    "6H": _L6._L6H_s, "6I": _L6._L6I_s, "6CUM3": _L6._L6CUM3_s,
    "6J": _L6._L6J_s, "6REV": _L6._L6REV_s,
}


def build_v3_sheet(sublevel_code, sheet):
    if sublevel_code == "6A":
        return _L6A_v3_s(sheet)
    src = _V3_SOURCE_FN[sublevel_code]
    return _l6v3_build_from_existing(src, sheet)


LEVEL6_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _V3_SOURCE_FN
}
