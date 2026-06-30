"""
Fear Less Maths — Answer Key derivation.

Question content (content_l*.py) builds question TEXT but, for the vast
majority of auto-generated "rotation" questions (computation, True/False,
missing-number, numeral, multi-select, matching), never stores the
correct answer in the returned dict — it's implicit in the random
numbers chosen at generation time and then discarded.

Rather than touching every one of the ~thousands of question-generator
closures across content_l5..l19, this module recovers the answer by
re-parsing the already-generated question text / diagram params. This
covers the standard rotation formats (comp, tf, missing, numeral,
multisel, matching) used by make_format_builders / make_rotated_sheet,
which make up the bulk of every main worksheet.

Formats NOT yet covered (return None -> shown as "—" in the key):
  - Free-text word problems with sentence answers
  - Maze / Function-machine / Pyramid / Code-breaker "fun" formats
  - Puzzle-style "I am divisible by X, between A and B" riddles
These need their own per-format derivation and are a planned follow-up.
"""
import re

_OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
        "x": lambda a, b: a * b, "×": lambda a, b: a * b,
        "*": lambda a, b: a * b, "/": lambda a, b: a / b}

_EXPR_RE = re.compile(r"\((-?\d+(?:\.\d+)?)\)\s*([+\-x×*/])\s*\((-?\d+(?:\.\d+)?)\)")
_PLAIN_EXPR_RE = re.compile(r"(?<![\d.])(-?\d+(?:\.\d+)?)\s*([+\-x×*/])\s*(-?\d+(?:\.\d+)?)(?!\s*R)")
_REM_EQ_RE = re.compile(r"(-?\d+)\s*/\s*(-?\d+)\s*=\s*(-?\d+)\s*R\s*(-?\d+)")


def _fmt_num(v):
    """Round-trip a float to int display when it's a whole number."""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, float):
        return f"{v:.2f}".rstrip("0").rstrip(".")
    return str(v)


def _div_with_remainder(a, b):
    """Returns 'Q' or 'Q R r' depending on whether it divides evenly --
    matches the format used by matching_q's division-remainder rights."""
    if b == 0:
        return None
    q, r = divmod(a, b)
    return str(q) if r == 0 else f"{q} R {r}"


def _eval_expr(a, op, b):
    if op == "/":
        return _div_with_remainder(a, b)
    fn = _OPS.get(op)
    return _fmt_num(fn(a, b)) if fn else None


def _eval_simple_expr(text):
    """Finds the first '(a) OP (b)' pattern in text and evaluates it,
    falling back to a plain 'a OP b' match if no parens are present."""
    m = _EXPR_RE.search(text)
    if not m:
        m = _PLAIN_EXPR_RE.search(text)
    if not m:
        return None
    a, op, b = float(m.group(1)), m.group(2), float(m.group(3))
    a = int(a) if a.is_integer() else a
    b = int(b) if b.is_integer() else b
    return _eval_expr(a, op, b)


def _derive_comp_or_numeral(item):
    text = item["text"]
    m = re.search(r"(-?\d+)\s*/\s*(-?\d+)\s*=\s*____\s*R\s*____", text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return _div_with_remainder(a, b) if b else None
    return _eval_simple_expr(text)


def _derive_tf(item):
    text = item["text"]
    m = re.search(r"True or False:\s*(.+)$", text)
    if not m:
        return None
    statement = m.group(1)
    # Remainder form: "total / divisor = groups R shown"
    m_rem = _REM_EQ_RE.search(statement)
    if m_rem:
        total, divisor, groups, shown = (int(m_rem.group(i)) for i in range(1, 5))
        if divisor == 0:
            return None
        correct_groups, correct_rem = divmod(total, divisor)
        return "True" if (correct_groups, correct_rem) == (groups, shown) else "False"
    m2 = re.search(r"(.+?)\s*=\s*(-?\d+(?:\.\d+)?)\s*$", statement)
    if not m2:
        return None
    lhs, shown = m2.group(1), float(m2.group(2))
    m3 = _EXPR_RE.search(lhs) or _PLAIN_EXPR_RE.search(lhs)
    if not m3:
        return None
    a, op, b = float(m3.group(1)), m3.group(2), float(m3.group(3))
    fn = _OPS.get(op)
    if not fn:
        return None
    correct = fn(a, b)
    return "True" if abs(correct - shown) < 1e-9 else "False"


def _derive_missing(item):
    text = item["text"]
    # Remainder forms: "total / divisor = groups R ____"
    m_rem = re.search(r"(-?\d+)\s*/\s*(-?\d+)\s*=\s*(-?\d+)\s*R\s*____", text)
    if m_rem:
        total, divisor, groups = (int(m_rem.group(i)) for i in range(1, 4))
        if divisor == 0:
            return None
        return str(total - divisor * groups)
    # "(a) OP ____ = target"  or  "dividend / ____ = n"  or  "dividend / divisor = ____"
    m = re.search(r"\(?(-?\d+(?:\.\d+)?)\)?\s*([+\-x×*/])\s*____\s*=\s*(-?\d+(?:\.\d+)?)", text)
    if m:
        a, op, target = float(m.group(1)), m.group(2), float(m.group(3))
        if op == "/":
            return _fmt_num(a / target) if target else None
        if op == "x" or op == "×" or op == "*":
            return _fmt_num(target / a) if a else None
        if op == "+":
            return _fmt_num(target - a)
        if op == "-":
            return _fmt_num(a - target)
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*/\s*____\s*=\s*(-?\d+(?:\.\d+)?)", text)
    if m:
        dividend, n = float(m.group(1)), float(m.group(2))
        return _fmt_num(dividend / n) if n else None
    return None


def _derive_multisel(item):
    text = item["text"]
    if "NO remainder" in text:
        opts = re.findall(r"([A-D])\)\s*(-?\d+)\s*/\s*(-?\d+)", text)
        correct_letters = [letter for letter, a, b in opts if int(b) != 0 and int(a) % int(b) == 0]
        return ", ".join(correct_letters) if correct_letters else "(none)"
    m = re.search(r"Which equal (-?\d+(?:\.\d+)?)", text)
    if not m:
        return None
    target = float(m.group(1))
    opts = re.findall(r"([A-D])\)\s*((?:\(-?\d+\)\s*[+\-x×*/]\s*\(-?\d+\))|(?:-?\d+\s*[+\-x×*/]\s*-?\d+)|(?:-?\d+(?:\.\d+)?))", text)
    correct_letters = []
    for letter, expr in opts:
        m2 = _EXPR_RE.search(f"({expr})" if not expr.startswith("(") else expr) or _PLAIN_EXPR_RE.search(expr)
        if m2:
            a, op, b = float(m2.group(1)), m2.group(2), float(m2.group(3))
            fn = _OPS.get(op)
            val = fn(a, b) if fn else None
        else:
            try:
                val = float(expr)
            except ValueError:
                val = None
        if val is not None and abs(val - target) < 1e-9:
            correct_letters.append(letter)
    return ", ".join(correct_letters) if correct_letters else None


def _derive_matching(item):
    params = item.get("diagram_params", {})
    lefts, rights = params.get("lefts"), params.get("rights")
    if not lefts or not rights:
        return None
    pairs = []
    for i, left in enumerate(lefts):
        val = _eval_simple_expr(f"({left})") if "(" not in left else _eval_simple_expr(left)
        if val is None:
            m = re.search(r"(-?\d+(?:\.\d+)?)\s*/\s*(-?\d+(?:\.\d+)?)", left)
            if m:
                val = _div_with_remainder(int(float(m.group(1))), int(float(m.group(2))))
        letter = None
        for j, r in enumerate(rights):
            if str(r).strip() == str(val).strip():
                letter = chr(65 + j)
                break
        pairs.append(f"{i+1}-{letter}" if letter else f"{i+1}-?")
    return ", ".join(pairs)


def _frac_explain(a, b):
    return f"{a}/{b}"


def _explain_and_answer_fraction_patterns(text):
    """Handles the fraction-specific phrasings used in Level 6 (and similar
    wording elsewhere) that don't fit the generic arithmetic patterns.
    Returns (answer, explanation) or (None, '') if no pattern matches."""

    # "True or False: a/b means c of d parts shaded."
    m = re.search(r"True or False:\s*(-?\d+)/(-?\d+)\s+means\s+(-?\d+)\s+of\s+(-?\d+)\s+parts shaded", text)
    if m:
        a, b, c, d = (int(m.group(i)) for i in range(1, 5))
        correct = (a == c and b == d)
        ans = "True" if correct else "False"
        exp = (f"{a}/{b} means {a} of {b} parts shaded — the statement says {c} of {d}, "
               f"which {'matches' if correct else 'does not match'} — so it's {ans}.")
        return ans, exp

    # "____ /D means half the parts are shaded (den is even)."
    m = re.search(r"____\s*/\s*(-?\d+)\s+means half the parts are shaded", text)
    if m:
        d = int(m.group(1))
        ans = str(d // 2)
        return ans, f"Half of {d} is {ans}, so the missing numerator is {ans} (giving {ans}/{d})."

    # "True or False: a/b is made of a unit fractions of 1/b."
    m = re.search(r"True or False:\s*(-?\d+)/(-?\d+)\s+is made of\s+(-?\d+)\s+unit fractions of\s+1/(-?\d+)", text)
    if m:
        a, b, c, d = (int(m.group(i)) for i in range(1, 5))
        correct = (a == c and b == d)
        ans = "True" if correct else "False"
        exp = (f"{a}/{b} is built from {a} pieces of 1/{b} — the statement says {c} pieces of 1/{d}, "
               f"which {'matches' if correct else 'does not match'} — so it's {ans}.")
        return ans, exp

    # "True or False: a/b = w n/d2"  (improper -> mixed number)
    m = re.search(r"True or False:\s*(-?\d+)/(-?\d+)\s*=\s*(-?\d+)\s+(-?\d+)/(-?\d+)\s*$", text)
    if m:
        a, b, w, n, d2 = (int(m.group(i)) for i in range(1, 6))
        if b == 0:
            return None, ""
        cw, cr = divmod(a, b)
        correct = (cw == w and cr == n and d2 == b)
        ans = "True" if correct else "False"
        exp = (f"{a}/{b} = {cw} whole(s) with {cr}/{b} left over (because {b} × {cw} = {a - cr}). "
               f"The statement says {w} {n}/{d2}, which {'matches' if correct else 'does not match'} — so it's {ans}.")
        return ans, exp

    # "____ /D = W wholes exactly (no remainder)"
    m = re.search(r"____\s*/\s*(-?\d+)\s*=\s*(-?\d+)\s+wholes exactly", text)
    if m:
        d, w = int(m.group(1)), int(m.group(2))
        ans = str(d * w)
        return ans, f"{w} whole(s) of {d} equal parts each = {w} × {d} = {ans}, so the missing numerator is {ans}."

    # "True or False: a/b = c/d"  (equivalent fractions)
    m = re.search(r"True or False:\s*(-?\d+)/(-?\d+)\s*=\s*(-?\d+)/(-?\d+)\s*$", text)
    if m:
        a, b, c, d = (int(m.group(i)) for i in range(1, 5))
        correct = (b != 0 and d != 0 and a * d == b * c)
        ans = "True" if correct else "False"
        exp = (f"Cross-multiply: {a} × {d} = {a*d}, and {b} × {c} = {b*c}. These "
               f"{'are equal' if correct else 'are not equal'}, so it's {ans}.")
        return ans, exp

    # "a/b = c/____"  (find missing denominator of an equivalent fraction)
    m = re.search(r"(-?\d+)/(-?\d+)\s*=\s*(-?\d+)/____", text)
    if m:
        a, b, c = (int(m.group(i)) for i in range(1, 4))
        if a == 0:
            return None, ""
        ans = str(c * b // a) if (c * b) % a == 0 else _fmt_num(c * b / a)
        return ans, f"{a}/{b} = {c}/____ → multiply both sides: {b} × ({c}/{a}) = {ans}, so the missing number is {ans}."

    # "True or False: a/b simplifies to c/d"
    m = re.search(r"True or False:\s*(-?\d+)/(-?\d+)\s+simplifies to\s+(-?\d+)/(-?\d+)", text)
    if m:
        import math
        a, b, c, d = (int(m.group(i)) for i in range(1, 5))
        if b == 0:
            return None, ""
        g = math.gcd(a, b)
        sa, sb = a // g, b // g
        correct = (sa == c and sb == d)
        ans = "True" if correct else "False"
        exp = (f"Simplify {a}/{b}: divide both by their greatest common factor ({g}) → {sa}/{sb}. "
               f"The statement says {c}/{d}, which {'matches' if correct else 'does not match'} — so it's {ans}.")
        return ans, exp

    # "a/b = ____ (shade and write)" -- student just restates the fraction
    m = re.search(r"(-?\d+)/(-?\d+)\s*=\s*____\s*\(shade and write\)", text)
    if m:
        a, b = m.group(1), m.group(2)
        return f"{a}/{b}", f"No calculation needed — just write the same fraction: {a}/{b}."

    # "a/b means ____ of ____ equal parts."
    m = re.search(r"(-?\d+)/(-?\d+)\s+means\s+____\s+of\s+____\s+equal parts", text)
    if m:
        a, b = m.group(1), m.group(2)
        return f"{a} of {b}", f"{a}/{b} means {a} out of {b} equal parts."

    # "a ___ b  (>, < or =)"  -- comparison fill-in-the-symbol
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*___\s*(-?\d+(?:\.\d+)?)\s*\(>,?\s*<\s*or\s*=\)", text)
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        sym = ">" if a > b else ("<" if a < b else "=")
        return sym, (f"Compare {_fmt_num(a)} and {_fmt_num(b)}: {_fmt_num(a)} is "
                     f"{'greater than' if sym=='>' else ('less than' if sym=='<' else 'equal to')} "
                     f"{_fmt_num(b)}, so the symbol is '{sym}'.")

    # "True or False: a = b" / "a < b" / "a > b"  (decimal comparisons / equality)
    m = re.search(r"True or False:\s*(-?\d+(?:\.\d+)?)\s*([=<>])\s*(-?\d+(?:\.\d+)?)\s*$", text)
    if m:
        a, sym, b = float(m.group(1)), m.group(2), float(m.group(3))
        correct = {"=": a == b, "<": a < b, ">": a > b}[sym]
        ans = "True" if correct else "False"
        return ans, f"Compare the actual values: {_fmt_num(a)} and {_fmt_num(b)}. The statement '{_fmt_num(a)} {sym} {_fmt_num(b)}' is {ans}."

    # "a = a____  (add a zero, value stays the same)"
    m = re.search(r"(-?\d+\.\d+)\s*=\s*\1____\s*\(add a zero", text)
    if m:
        return "0", "Adding a zero to the end of a decimal doesn't change its value, so the missing digit is 0."

    # "The opposite of X is ____." / "Write the opposite of X."
    m = re.search(r"[Oo]pposite of\s*(-?\d+(?:\.\d+)?)", text)
    if m:
        v = float(m.group(1)); v = int(v) if v.is_integer() else v
        ans = _fmt_num(-v)
        return ans, f"The opposite of a number flips its sign: opposite of {_fmt_num(v)} is {ans}."

    # "Mark X on the number line." / "...Mark it on the number line." (value stated earlier in the sentence)
    if "number line" in text and "Mark" in text:
        m = re.search(r"Mark\s*(-?\d+(?:\.\d+)?)\s*on the number line", text)
        if not m:
            m = re.search(r"(?:is|reads)\s*(-?\d+(?:\.\d+)?)", text)
        if m:
            v = m.group(1)
            return v, f"Find {v} on the number line and mark it there."

    # "X < ____ < Y  (give one number that fits)"
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*<\s*____\s*<\s*(-?\d+(?:\.\d+)?)\s*\(give one number", text)
    if m:
        lo, hi = float(m.group(1)), float(m.group(2))
        mid = lo + 1 if (hi - lo) >= 2 else (lo + hi) / 2
        return _fmt_num(mid), f"Any number strictly between {_fmt_num(lo)} and {_fmt_num(hi)} works — for example {_fmt_num(mid)}."

    # "True or False: in X, the <place> digit is D"
    m = re.search(r"True or False:\s*in\s*(-?\d+\.\d+),\s*the\s*(\w+)\s*digit is\s*(-?\d+)", text)
    if m:
        num_str, place, shown = m.group(1), m.group(2).lower(), int(m.group(3))
        whole, _, frac = num_str.partition(".")
        place_idx = {"tenths": 0, "hundredths": 1, "thousandths": 2}.get(place)
        if place_idx is not None and place_idx < len(frac):
            correct_digit = int(frac[place_idx])
            ans = "True" if correct_digit == shown else "False"
            return ans, (f"In {num_str}, the {place} digit is {correct_digit}. The statement says {shown}, "
                         f"which {'matches' if correct_digit == shown else 'does not match'} — so it's {ans}.")
        if place == "ones" and whole:
            correct_digit = int(whole[-1])
            ans = "True" if correct_digit == shown else "False"
            return ans, (f"In {num_str}, the ones digit is {correct_digit}. The statement says {shown}, "
                         f"which {'matches' if correct_digit == shown else 'does not match'} — so it's {ans}.")

    # "Place X on the number line."
    m = re.search(r"Place\s*(-?\d+(?:\.\d+)?)\s*on the number line", text)
    if m:
        v = m.group(1)
        return v, f"Find {v} on the number line and mark it there."

    # "True or False: X is greater than Y" / "X is less than Y"
    m = re.search(r"True or False:\s*(-?\d+(?:\.\d+)?)\s*is\s*(greater|less)\s*than\s*(-?\d+(?:\.\d+)?)", text)
    if m:
        a, word, b = float(m.group(1)), m.group(2), float(m.group(3))
        correct = (a > b) if word == "greater" else (a < b)
        ans = "True" if correct else "False"
        return ans, f"Compare the actual values: {_fmt_num(a)} and {_fmt_num(b)}. The statement that {_fmt_num(a)} is {word} than {_fmt_num(b)} is {ans}."

    return None, ""


_OP_WORD = {"+": "add", "-": "subtract", "x": "multiply", "×": "multiply", "*": "multiply", "/": "divide"}
_OP_SIGN = {"+": "+", "-": "−", "x": "×", "×": "×", "*": "×", "/": "÷"}


def _explain_simple(a, op, b):
    sign = _OP_SIGN.get(op, op)
    if op == "/":
        if not b or int(b) == 0:
            return ""
        q, r = int(a) // int(b), int(a) % int(b)
        if r == 0:
            return f"{a} {sign} {b} = {q}, because {b} × {q} = {a}."
        return f"{a} {sign} {b} = {q} R {r}, because {b} × {q} = {a - r}, and {a} − {a - r} = {r} left over."
    fn = _OPS.get(op)
    if not fn:
        return ""
    result = fn(a, b)
    return f"{a} {sign} {b} = {_fmt_num(result)}."


def _explain_comp_or_numeral(item, ans):
    text = item["text"]
    m = re.search(r"(-?\d+)\s*/\s*(-?\d+)\s*=\s*____\s*R\s*____", text)
    if m:
        return _explain_simple(int(m.group(1)), "/", int(m.group(2)))
    m = _EXPR_RE.search(text) or _PLAIN_EXPR_RE.search(text)
    if m:
        a, op, b = float(m.group(1)), m.group(2), float(m.group(3))
        a = int(a) if a.is_integer() else a
        b = int(b) if b.is_integer() else b
        return _explain_simple(a, op, b)
    return ""


def _explain_tf(item, ans):
    text = item["text"]
    m = re.search(r"True or False:\s*(.+)$", text)
    if not m:
        return ""
    statement = m.group(1)
    m_rem = _REM_EQ_RE.search(statement)
    if m_rem:
        total, divisor, groups, shown = (int(m_rem.group(i)) for i in range(1, 5))
        if divisor == 0:
            return ""
        cg, cr = divmod(total, divisor)
        base = f"Correct working: {total} ÷ {divisor} = {cg} R {cr} (because {divisor} × {cg} = {total - cr})."
        if (cg, cr) == (groups, shown):
            return base + " The statement matches this, so it's True."
        return base + f" The statement said {groups} R {shown}, which doesn't match — so it's False."
    m2 = re.search(r"(.+?)\s*=\s*(-?\d+(?:\.\d+)?)\s*$", statement)
    if not m2:
        return ""
    lhs, shown = m2.group(1), float(m2.group(2))
    m3 = _EXPR_RE.search(lhs) or _PLAIN_EXPR_RE.search(lhs)
    if not m3:
        return ""
    a, op, b = float(m3.group(1)), m3.group(2), float(m3.group(3))
    fn = _OPS.get(op)
    if not fn:
        return ""
    correct = fn(a, b)
    sign = _OP_SIGN.get(op, op)
    base = f"Correct working: {_fmt_num(a)} {sign} {_fmt_num(b)} = {_fmt_num(correct)}."
    if abs(correct - shown) < 1e-9:
        return base + f" The statement says {_fmt_num(shown)}, which matches — so it's True."
    return base + f" The statement says {_fmt_num(shown)}, which doesn't match — so it's False."


def _explain_missing(item, ans):
    text = item["text"]
    m_rem = re.search(r"(-?\d+)\s*/\s*(-?\d+)\s*=\s*(-?\d+)\s*R\s*____", text)
    if m_rem:
        total, divisor, groups = (int(m_rem.group(i)) for i in range(1, 4))
        if divisor == 0:
            return ""
        rem = total - divisor * groups
        return f"{divisor} × {groups} = {total - rem}. {total} − {total - rem} = {rem}, so the missing remainder is {rem}."
    m = re.search(r"\(?(-?\d+(?:\.\d+)?)\)?\s*([+\-x×*/])\s*____\s*=\s*(-?\d+(?:\.\d+)?)", text)
    if m:
        a, op, target = float(m.group(1)), m.group(2), float(m.group(3))
        opword = _OP_WORD.get(op, op)
        sign = _OP_SIGN.get(op, op)
        if op == "/":
            return (f"{_fmt_num(a)} {sign} ____ = {_fmt_num(target)} → divide {_fmt_num(a)} by "
                    f"{_fmt_num(target)} to undo it: {_fmt_num(a)} ÷ {_fmt_num(target)} = {ans}.")
        if op in ("x", "×", "*"):
            return (f"{_fmt_num(a)} {sign} ____ = {_fmt_num(target)} → divide {_fmt_num(target)} by "
                    f"{_fmt_num(a)} to undo the multiplication: {ans}.")
        if op == "+":
            return f"{_fmt_num(a)} {sign} ____ = {_fmt_num(target)} → subtract: {_fmt_num(target)} − {_fmt_num(a)} = {ans}."
        if op == "-":
            return f"{_fmt_num(a)} {sign} ____ = {_fmt_num(target)} → add: {_fmt_num(a)} − {_fmt_num(target)} = {ans}."
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*/\s*____\s*=\s*(-?\d+(?:\.\d+)?)", text)
    if m:
        dividend, n = float(m.group(1)), float(m.group(2))
        return (f"{_fmt_num(dividend)} ÷ ____ = {_fmt_num(n)} → the missing divisor is "
                f"{_fmt_num(dividend)} ÷ {_fmt_num(n)} = {ans}.")
    return ""


def _explain_multisel(item, ans):
    text = item["text"]
    if "NO remainder" in text:
        opts = re.findall(r"([A-D])\)\s*(-?\d+)\s*/\s*(-?\d+)", text)
        parts = []
        for letter, a, b in opts:
            a, b = int(a), int(b)
            r = a % b if b else None
            parts.append(f"{letter}) {a}÷{b} leaves remainder {r}" if r else f"{letter}) {a}÷{b} leaves no remainder")
        return "Checked each option: " + "; ".join(parts) + "."
    m = re.search(r"Which equal (-?\d+(?:\.\d+)?)", text)
    if not m:
        return ""
    target = m.group(1)
    opts = re.findall(r"([A-D])\)\s*((?:\(-?\d+\)\s*[+\-x×*/]\s*\(-?\d+\))|(?:-?\d+\s*[+\-x×*/]\s*-?\d+)|(?:-?\d+(?:\.\d+)?))", text)
    parts = []
    for letter, expr in opts:
        m2 = _EXPR_RE.search(f"({expr})" if not expr.startswith("(") else expr) or _PLAIN_EXPR_RE.search(expr)
        if m2:
            a, op, b = float(m2.group(1)), m2.group(2), float(m2.group(3))
            fn = _OPS.get(op)
            val = _fmt_num(fn(a, b)) if fn else "?"
        else:
            val = expr
        parts.append(f"{letter}) {expr} = {val}")
    return f"Checked each option against the target ({target}): " + "; ".join(parts) + "."


def _explain_matching(item, ans):
    params = item.get("diagram_params", {})
    lefts = params.get("lefts") or []
    parts = []
    for i, left in enumerate(lefts):
        val = _eval_simple_expr(f"({left})") if "(" not in left else _eval_simple_expr(left)
        if val is None:
            m = re.search(r"(-?\d+(?:\.\d+)?)\s*/\s*(-?\d+(?:\.\d+)?)", left)
            if m:
                val = _div_with_remainder(int(float(m.group(1))), int(float(m.group(2))))
        parts.append(f"{i+1}) {left} = {val}")
    return "Work out each one: " + "; ".join(parts) + ", then match each result to its letter on the right." if parts else ""


_TEXT_MATCH_RE = re.compile(r"Match each.*?:\s*(.+?)\s+to\s+(A\).+)$")
_TEXT_MATCH_LEFT_RE = re.compile(r"\d+\)\s*([^\d]+?)(?=\s*\d+\)|$)")
_TEXT_MATCH_RIGHT_RE = re.compile(r"[A-D]\)\s*([^A-D]+?)(?=\s*[A-D]\)|$)")


def _derive_text_matching(item):
    """Same idea as _derive_matching, but for the 'fill'-type matching
    questions (used by several Level 6-8 sublevels) where the shuffled
    pairs are baked directly into the question text instead of stored
    as diagram_params."""
    text = item.get("text", "")
    m = _TEXT_MATCH_RE.search(text)
    if not m:
        return None
    left_block, right_block = m.group(1), m.group(2)
    lefts = [s.strip().rstrip(".") for s in _TEXT_MATCH_LEFT_RE.findall(left_block)]
    rights = [s.strip().rstrip(".") for s in _TEXT_MATCH_RIGHT_RE.findall(right_block)]
    if not lefts or not rights:
        return None
    pairs = []
    for i, left in enumerate(lefts):
        val = _eval_simple_expr(left)
        if val is None:
            dm = re.search(r"(-?\d+(?:\.\d+)?)\s*/\s*(-?\d+(?:\.\d+)?)", left)
            if dm and "/" in left and not re.search(r"[+\-x×*]", left):
                a, b = dm.group(1), dm.group(2)
                if "." not in a and "." not in b:
                    val = _div_with_remainder(int(a), int(b))
        if val is None:
            val = left  # e.g. plain numbers like "-7" with no operator
        letter = None
        for j, r in enumerate(rights):
            if str(r).strip() == str(val).strip():
                letter = chr(65 + j)
                break
        if letter is None:
            return None  # don't guess -- right side is categorical/descriptive
        pairs.append(f"{i+1}-{letter}")
    return ", ".join(pairs) if len(pairs) == len(lefts) else None


def derive_answer_and_explanation(item):
    """Returns (answer_str, explanation_str) — explanation is a short
    plain-language worked-step a non-maths staff member can follow,
    e.g. '21 ÷ 4 = 5 R 1, because 4 × 5 = 20, and 21 − 20 = 1 left over.'
    Either value may be empty/None if this question's format isn't
    covered yet (see module docstring)."""
    if item.get("type") in ("concept_box", "tips_box"):
        return None, ""
    diag = item.get("diagram_type") or ""
    text = item.get("text", "")
    if diag == "matching_vertical_blank":
        ans = _derive_matching(item)
        return ans, (_explain_matching(item, ans) if ans else "")
    frac_ans, frac_exp = _explain_and_answer_fraction_patterns(text)
    if frac_ans is not None:
        return frac_ans, frac_exp
    if text.startswith("True or False:"):
        ans = _derive_tf(item)
        return ans, (_explain_tf(item, ans) if ans else "")
    if "Select ALL that apply" in text:
        ans = _derive_multisel(item)
        return ans, (_explain_multisel(item, ans) if ans else "")
    if text.startswith("Match each"):
        ans = _derive_text_matching(item)
        return ans, (f"Work out each value and match it to the matching item on the right: {ans}." if ans else "")
    if "____ R ____" in text:
        ans = _derive_comp_or_numeral(item)
        return ans, (_explain_comp_or_numeral(item, ans) if ans else "")
    if "____" in text and (re.search(r"[+\-x×*/]\s*____", text) or "R ____" in text):
        ans = _derive_missing(item)
        return ans, (_explain_missing(item, ans) if ans else "")
    ans = _derive_comp_or_numeral(item)
    return ans, (_explain_comp_or_numeral(item, ans) if ans else "")


def derive_answer(item):
    """Returns just the answer string (back-compat for callers that don't
    need the explanation)."""
    return derive_answer_and_explanation(item)[0]
