"""
Shared question-orientation-rotation architecture, used by Level 7
(Decimals) and Level 8 (Integers) redesigns, and any future level that
needs the same "4 sheets, 4 different format combinations, slightly
increasing difficulty" structure instead of one repeated question shape.

Six standard formats per skill: computation, True/False, missing-number,
numeral (no picture), multi-select, matching. Each sub-level's sheet
picks 4-of-6 in a different order depending on which of the 4
TEMPLATES the sheet number maps to, so sheets 1-4 of the same sub-level
are genuinely different worksheets, not the same shape with new numbers.
"""
import random
from content import cb, tb, q

TEMPLATES = [
    ["comp", "tf", "missing", "numeral"],
    ["matching", "multisel", "comp", "tf"],
    ["missing", "matching", "numeral", "multisel"],
    ["tf", "numeral", "matching", "comp"],
]


def diff_range(sheet, base_lo=2, base_hi=6, step=1):
    """Slightly widens the range as sheet increases, so sheet 4 is a bit
    harder than sheet 1, not identical difficulty."""
    s = min(sheet - 1, 3)
    return (base_lo + s*step, base_hi + s*step)


def make_rotated_sheet(title, bullets, icon, icon_params, instruction, fmt_builders, sheet, seed_base=0):
    random.seed(seed_base + sheet * 17)
    items = [cb(title, bullets, "", icon_diagram=icon, icon_params=icon_params)]
    items.append(tb("Instructions", [instruction]))
    template = TEMPLATES[(sheet - 1) % 4]
    for key in template:
        for i in range(5):
            items.append(fmt_builders[key](i, sheet))
    return items


def make_format_builders(gen_pair, diagram_fn, diagram_params_fn, op_symbol, op_compute,
                          missing_diagram_fn=None, missing_params_fn=None):
    """Builds the 6 standard format functions for a binary-operation skill."""
    missing_diagram_fn = missing_diagram_fn or diagram_fn
    missing_params_fn = missing_params_fn or diagram_params_fn

    def comp(i, sheet):
        a, b = gen_pair(sheet)
        return q(f"({a}) {op_symbol} ({b}) = ____", "diagram", "____", "", diagram_fn, diagram_params_fn(a, b))

    def tf(i, sheet):
        a, b = gen_pair(sheet)
        correct = op_compute(a, b)
        shown = correct if random.random() > 0.4 else correct + random.choice([-3, -2, 2, 3])
        return q(f"True or False: ({a}) {op_symbol} ({b}) = {shown}", "fill", "____ (True/False)")

    def missing(i, sheet):
        a, b = gen_pair(sheet)
        target = op_compute(a, b)
        return q(f"({a}) {op_symbol} ____ = {target}", "diagram", "____", "", missing_diagram_fn, missing_params_fn(a, b))

    def numeral(i, sheet):
        a, b = gen_pair(sheet)
        return q(f"({a}) {op_symbol} ({b}) = ____", "fill", "____")

    def multisel(i, sheet):
        a, b = gen_pair(sheet)
        target = op_compute(a, b)
        opts = [(a, b)]
        for _ in range(3):
            opts.append(gen_pair(sheet))
        letters = ["A", "B", "C", "D"]
        opts_str = "  ".join(f"{letters[k]}) ({opts[k][0]}){op_symbol}({opts[k][1]})" for k in range(4))
        return q(f"Which equal {target}? Select ALL that apply: {opts_str}", "fill", "____ (list all letters)")

    def matching(i, sheet):
        pairs = [gen_pair(sheet) for _ in range(3)]
        lefts = [f"({a}){op_symbol}({b})" for a, b in pairs]
        rights = [str(op_compute(a, b)) for a, b in pairs]
        shuffled = rights[:]
        random.shuffle(shuffled)
        left_str = "  ".join(f"{idx+1}) {v}" for idx, v in enumerate(lefts))
        right_str = "  ".join(f"{chr(65+idx)}) {v}" for idx, v in enumerate(shuffled))
        return q(f"Match to its value: {left_str}  to  {right_str}", "fill", "____ (e.g. 1-A,2-B...)")

    return {"comp": comp, "tf": tf, "missing": missing, "numeral": numeral, "multisel": multisel, "matching": matching}
