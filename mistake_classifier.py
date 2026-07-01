"""
Fear Less Maths — Intelligent Mistake Classifier

Given:
  - question item dict (from content.get_questions)
  - correct answer string (from answer_key.derive_answer_and_explanation)
  - what the student actually wrote

Returns:
  - mistake_type: one of the standard MISTAKE_TYPES strings
  - confidence: "high" | "medium" | "low"
  - reason: short plain-English explanation of why this type was chosen
            (shown to staff as a tooltip so they understand / can override)

Design principle: NEVER silently guess wrong. If confidence is low,
return ("Needs review", "low", reason) so staff know to look themselves.
"""

import re

# Must match ws_helpers.MISTAKE_TYPES exactly
MISTAKE_TYPES = [
    "Calculation slip",
    "Concept not understood",
    "Wrong method / formula",
    "Misread the question",
    "Careless / rushed",
    "No attempt",
    "Needs review",
]

_REM_RE = re.compile(r"^(-?\d+)\s*R\s*(-?\d+)$")
_NUM_RE  = re.compile(r"^-?\d+(\.\d+)?$")


def _parse_rem(s):
    """Parse '5 R 1' -> (5, 1), else None."""
    m = _REM_RE.match(s.strip())
    return (int(m.group(1)), int(m.group(2))) if m else None


def _is_num(s):
    return bool(_NUM_RE.match(s.strip()))


def _close(a, b, tol=1):
    """True if two numeric strings are within tol of each other."""
    try:
        return abs(float(a) - float(b)) <= tol
    except Exception:
        return False


def _digit_reversal(a, b):
    """True if b is the reverse of a's digits (e.g. 12 vs 21)."""
    return str(a).replace("-","") == str(b).replace("-","")[::-1]


def _opposite_sign(a, b):
    """True if b == -a (common integer mistake)."""
    try:
        return float(a) == -float(b)
    except Exception:
        return False


def classify(item: dict, correct_ans: str, student_wrote: str) -> tuple:
    """
    Returns (mistake_type: str, confidence: str, reason: str).
    """
    sw = (student_wrote or "").strip()
    ca = (correct_ans or "").strip()

    # ── No attempt ────────────────────────────────────────────────────────────
    if not sw:
        return ("No attempt", "high",
                "Student left the answer blank.")

    # ── Actually correct (staff mis-ticked) ───────────────────────────────────
    if sw.lower() == ca.lower():
        return ("Needs review", "high",
                f"Student wrote '{sw}' which matches the correct answer '{ca}' — "
                "this question was probably mis-ticked as wrong.")

    diag  = item.get("diagram_type") or ""
    text  = item.get("text", "")
    qtype = item.get("type", "fill")

    # ── True / False questions ─────────────────────────────────────────────────
    if text.startswith("True or False:"):
        if sw.lower() in ("true","false") and ca.lower() in ("true","false"):
            return ("Concept not understood", "high",
                    f"Correct is '{ca}' but student wrote '{sw}' — "
                    "flipped True/False means the underlying concept is not clear.")
        return ("Needs review", "low",
                f"Expected True/False, student wrote '{sw}'.")

    # ── Matching questions ────────────────────────────────────────────────────
    if diag == "matching_vertical_blank":
        # e.g. correct = "1-A, 2-C, 3-B", student = "1-A, 2-B, 3-C"
        if not sw:
            return ("No attempt", "high", "No matching answer written.")
        ca_pairs = set(p.strip() for p in ca.split(","))
        sw_pairs = set(p.strip() for p in sw.split(","))
        correct_count = len(ca_pairs & sw_pairs)
        total = len(ca_pairs)
        if correct_count == 0:
            return ("Concept not understood", "high",
                    f"Got 0/{total} pairs correct — doesn't understand the matching concept.")
        if correct_count == total - 1:
            return ("Careless / rushed", "medium",
                    f"Got {correct_count}/{total} pairs right — only one pair wrong, likely a slip.")
        return ("Concept not understood", "medium",
                f"Got only {correct_count}/{total} pairs correct.")

    # ── Remainder / division questions ────────────────────────────────────────
    if "R" in ca:
        ca_rem = _parse_rem(ca)
        sw_rem = _parse_rem(sw)

        if ca_rem:
            ca_q, ca_r = ca_rem

            # Student wrote just the quotient, forgot remainder part
            if _is_num(sw) and int(float(sw)) == ca_q:
                return ("Careless / rushed", "high",
                        f"Correct is '{ca}' — student got the quotient ({ca_q}) right "
                        f"but forgot to write the remainder. Likely careless or rushed.")

            if sw_rem:
                sw_q, sw_r = sw_rem
                # Quotient correct, remainder wrong
                if sw_q == ca_q and sw_r != ca_r:
                    return ("Calculation slip", "high",
                            f"Quotient {ca_q} is right, but remainder is {sw_r} instead of {ca_r}. "
                            f"Small arithmetic slip at the final subtraction step.")
                # Remainder correct, quotient wrong
                if sw_q != ca_q and sw_r == ca_r:
                    return ("Calculation slip", "medium",
                            f"Remainder {ca_r} is right, but quotient is {sw_q} instead of {ca_q}.")
                # Both wrong but close
                if abs(sw_q - ca_q) <= 1:
                    return ("Calculation slip", "medium",
                            f"Quotient off by {abs(sw_q - ca_q)}, remainder also off — small calculation error.")
                # Completely wrong
                return ("Concept not understood", "medium",
                        f"Both quotient and remainder wrong ({sw} vs correct {ca}).")

            # Student wrote something not in Q R format at all
            if _is_num(sw):
                # Check if it's the product (a×b) instead of quotient
                m = re.search(r"(-?\d+)\s*/\s*(-?\d+)", text)
                if m:
                    try:
                        product = int(m.group(1)) * int(m.group(2))
                        if int(float(sw)) == product:
                            return ("Wrong method / formula", "high",
                                    f"Student wrote {sw} which is {m.group(1)}×{m.group(2)} — "
                                    f"multiplied instead of dividing.")
                    except Exception:
                        pass
            return ("Concept not understood", "medium",
                    f"Expected a 'Q R r' answer, student wrote '{sw}'.")

    # ── Numeric computation answers ────────────────────────────────────────────
    if _is_num(ca) and _is_num(sw):
        try:
            ca_f = float(ca)
            sw_f = float(sw)
        except Exception:
            return ("Needs review", "low", "Could not compare numerically.")

        diff = abs(ca_f - sw_f)

        # Check for wrong-operation (e.g. multiplied instead of divided)
        m = re.search(r"(-?\d+(?:\.\d+)?)\s*[/÷]\s*(-?\d+(?:\.\d+)?)", text)
        if m:
            try:
                a, b = float(m.group(1)), float(m.group(2))
                if b != 0 and abs(sw_f - a * b) < 0.01:
                    return ("Wrong method / formula", "high",
                            f"Student wrote {sw} which equals {int(a)}×{int(b)} — "
                            f"multiplied instead of dividing.")
                if abs(sw_f - (a - b)) < 0.01:
                    return ("Wrong method / formula", "medium",
                            f"Student wrote {sw} which looks like subtraction ({int(a)}−{int(b)}) "
                            f"instead of division.")
            except Exception:
                pass

        m2 = re.search(r"(-?\d+(?:\.\d+)?)\s*[x×*]\s*(-?\d+(?:\.\d+)?)", text)
        if m2:
            try:
                a, b = float(m2.group(1)), float(m2.group(2))
                if abs(sw_f - (a + b)) < 0.01:
                    return ("Wrong method / formula", "high",
                            f"Student wrote {sw} which equals {int(a)}+{int(b)} — "
                            f"added instead of multiplying.")
                if abs(sw_f - abs(a - b)) < 0.01:
                    return ("Wrong method / formula", "medium",
                            f"Student wrote {sw} which looks like subtraction — "
                            f"used wrong operation.")
            except Exception:
                pass

        # Digit reversal
        if _digit_reversal(int(ca_f), int(sw_f)):
            return ("Careless / rushed", "high",
                    f"Student wrote {sw} — digits reversed from correct answer {ca}. "
                    f"Likely read/wrote in a hurry.")

        # Opposite sign (common integer mistake)
        if _opposite_sign(ca_f, sw_f):
            return ("Concept not understood", "high",
                    f"Student wrote {sw} (opposite sign of correct {ca}) — "
                    f"doesn't understand positive/negative direction.")

        # Off by 1
        if diff == 1:
            return ("Calculation slip", "high",
                    f"Off by exactly 1 ({sw} vs {ca}) — very small arithmetic slip, "
                    f"concept is understood.")

        # Close (within 10% of the correct value)
        if ca_f != 0 and diff / abs(ca_f) <= 0.10:
            return ("Calculation slip", "medium",
                    f"Answer {sw} is close to correct {ca} — small arithmetic error, "
                    f"method seems right.")

        # Answer is 10x or 100x off — place value error
        if ca_f != 0 and sw_f != 0:
            ratio = sw_f / ca_f
            if abs(ratio - 10) < 0.01 or abs(ratio - 100) < 0.01:
                return ("Careless / rushed", "high",
                        f"Answer {sw} is {int(ratio)}× the correct value {ca} — "
                        f"decimal point or place-value error.")
            if abs(ratio - 0.1) < 0.01 or abs(ratio - 0.01) < 0.01:
                return ("Careless / rushed", "high",
                        f"Answer {sw} is the correct value divided by {int(1/ratio)} — "
                        f"decimal point or place-value error.")

        # Far off — concept problem
        return ("Concept not understood", "medium",
                f"Answer {sw} is far from correct {ca} — suggests the underlying "
                f"method or concept is not clear.")

    # ── Multi-select (A, B, C / list of letters) ──────────────────────────────
    if "Select ALL" in text or "," in ca:
        ca_set = set(p.strip().upper() for p in ca.split(","))
        sw_set = set(p.strip().upper() for p in sw.split(","))
        if ca_set == sw_set:
            return ("Needs review", "high",
                    "Student wrote the correct answer — may have been mis-ticked.")
        overlap = ca_set & sw_set
        if len(overlap) >= len(ca_set) - 1:
            return ("Careless / rushed", "medium",
                    f"Almost correct — missed or added just one option.")
        if not overlap:
            return ("Concept not understood", "high",
                    "None of the selected options are correct.")
        return ("Concept not understood", "medium",
                f"Partially correct ({len(overlap)}/{len(ca_set)} right options selected).")

    # ── Fallback ───────────────────────────────────────────────────────────────
    return ("Needs review", "low",
            f"Could not auto-classify (wrote '{sw}', correct is '{ca}'). "
            f"Please check manually.")


def classify_batch(items: list, correct_answers: list, student_answers: list) -> list:
    """
    Classify multiple questions at once.
    items, correct_answers, student_answers must be same length lists.
    Returns list of (mistake_type, confidence, reason) tuples.
    """
    return [
        classify(item, ca, sa)
        for item, ca, sa in zip(items, correct_answers, student_answers)
    ]
