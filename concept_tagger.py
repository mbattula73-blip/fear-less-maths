"""
concept_tagger.py — Heuristic auto-tagger for per-question concept labels.

Scans a question's text for distinctive mathematical vocabulary and returns
a specific concept label (e.g. "HCF", "Congruence", "Trigonometry"). Falls
back to the worksheet's sublevel topic when nothing distinctive is found —
this makes the tagger purely additive: it can only make wrong-answer
analysis MORE granular than today, never less accurate, since the fallback
matches today's existing behaviour exactly.

Used by:
  - bulk_tag_worksheets.py (one-time script to pre-populate db.worksheet_tags)
  - the "Concept Tags" Streamlit tab (live auto-suggest while editing)
"""
import re

# Ordered list of (pattern, tag). Checked top-to-bottom; first match wins.
# More specific / multi-word phrases are placed before generic single words
# so they don't get shadowed by a broader rule lower down.
_RULES = [
    # Number theory
    (r"prime factor|factor tree", "Prime Factorisation"),
    (r"\bHCF\b|highest common factor", "HCF"),
    (r"\bLCM\b|lowest common multiple", "LCM"),
    (r"multiples? of\b", "Multiples"),
    (r"factors? of\b|common factor", "Factors"),
    (r"factori[sz]e|factori[sz]ation", "Factorisation"),

    # Ratio & proportion
    (r"share (rs|\d+).*ratio|share.*in (the )?ratio|in ratio \d+:\d+", "Sharing in a Ratio"),
    (r"equivalent ratio", "Equivalent Ratios"),
    (r"simplify.*ratio|ratio.*simplest", "Simplifying Ratios"),
    (r"unitary method|cost of \d+.*find|price of \d+.*find", "Unitary Method"),
    (r"direct proportion", "Direct Proportion"),
    (r"inverse proportion", "Inverse Proportion"),
    (r"\bproportion\b|cross.?multiply", "Proportion"),

    # Decimals / fractions / percentages
    (r"\bdecimal\b|decimal point|place value", "Decimals"),
    (r"\bfraction\b|numerator|denominator", "Fractions"),
    (r"per ?cent|%", "Percentages"),

    # Integers
    (r"number line|integer", "Integers"),

    # Algebra: expressions & equations
    (r"write the expression|write an expression", "Writing Expressions"),
    (r"like terms|combine.*terms", "Like Terms"),
    (r"simplify.*expression", "Simplifying Expressions"),
    (r"substitut", "Substitution"),
    (r"think of a number|my number|i think of", "Number Puzzles"),
    (r"solve for x|solve the equation|solve:? *-?\d*x", "Solving Equations"),

    # Polynomials
    (r"degree of|polynomial", "Polynomials"),
    (r"identity|\(x ?[+-] ?[a-z0-9]\)\^?2|expand (the )?(bracket|expression)", "Algebraic Identities"),

    # Trigonometry (checked BEFORE roots, since surds appear in trig too)
    (r"angle of elevation|angle of depression|\bladder\b|height.*distance.*tan", "Heights & Distances"),
    (r"sin\s*\u03b8|cos\s*\u03b8|tan\s*\u03b8|\u03b8\s*=|sec\s*\u03b8|cosec\s*\u03b8|cot\s*\u03b8", "Trigonometry"),

    # Powers & indices (no bare caret/digit catch-all -- too broad, would
    # match unit notation like cm^2/m^3 everywhere)
    (r"scientific notation", "Scientific Notation"),
    (r"square root|cube root", "Roots"),
    (r"negative power|negative exponent|negative index", "Negative Powers"),
    (r"power of|\bexponent\b|\bindex\b|\bindices\b", "Powers & Indices"),

    # Coordinate geometry
    (r"mid ?point", "Midpoint"),
    (r"distance (formula|between|from)|distance from origin", "Distance Formula"),
    (r"section formula|divides.*ratio", "Section Formula"),
    (r"slope|gradient", "Slope"),
    (r"y-intercept|line graph|graph of|y *= *-?\d*x", "Graphing Lines"),
    (r"quadrant|\(x,y\)|coordinate", "Coordinate Plane"),

    # Triangles
    (r"isosceles|equilateral|scalene", "Triangle Types"),
    (r"exterior angle", "Exterior Angle"),
    (r"angle sum|sum of (the )?angles", "Angle Sum Property"),
    (r"congruent|congruence|\bSSS\b|\bSAS\b|\bASA\b|\bRHS\b", "Congruence"),
    (r"similar triangle|scale factor", "Similar Triangles"),
    (r"pythagoras|hypotenuse", "Pythagoras Theorem"),

    # Circles
    (r"\btangent\b", "Tangents"),
    (r"\bchord\b", "Chords"),
    (r"centre angle|circumference angle|angle.*semicircle|semicircle.*angle|inscribed angle", "Circle Theorems"),
    (r"distance per turn|one lap|circumference", "Circumference"),

    # Mensuration: shape + area/volume combos checked before generic radius
    # catch, so e.g. "Pizza radius 14: area=" tags as Area of Circle, not
    # just Circle Parts
    (r"(triangle.*\barea\b|\barea\b.*triangle)", "Area of Triangle"),
    (r"(circle.*\barea\b|\barea\b.*circle|circular (garden|track|field)|pizza.*(area|radius|slice|sector)|(area|radius|sector).*pizza)", "Area of Circle"),
    (r"((square|rectangle).*\barea\b|\barea\b.*(square|rectangle))", "Area of Rectangle/Square"),
    (r"(ring|annulus).*\barea\b|\barea\b.*(ring|annulus)", "Area of a Ring"),
    (r"\bperimeter\b", "Perimeter"),
    (r"\btsa\b|total surface area", "Total Surface Area"),
    (r"\bcsa\b|curved surface area", "Curved Surface Area"),
    (r"surface area|\bSA\s*=", "Surface Area"),
    (r"\bsphere\b|\bhemisphere\b", "Sphere/Hemisphere"),
    (r"\bcylinder\b", "Cylinder"),
    (r"\bcone\b", "Cone"),
    (r"\bvolume\b", "Volume"),
    (r"\bradius\b|\bdiameter\b", "Circle Parts"),
    (r"\barea\b", "Area"),

    # Statistics & probability
    (r"\bmean of\b|\bmedian\b|\bmode\b|\baverage\b", "Mean, Median, Mode"),
    (r"probability|\bdice\b|\bcoin\b|\bcard(s)? (drawn|picked)", "Probability"),
    (r"arithmetic progression|\bAP\b|common difference|nth term", "Arithmetic Progression"),
]

_COMPILED = [(re.compile(p, re.IGNORECASE), tag) for p, tag in _RULES]


def auto_tag_question(text: str, fallback_topic: str) -> str:
    """Return a specific concept tag for a single question's text, or the
    sublevel's fallback topic if nothing distinctive is detected."""
    if not text:
        return fallback_topic
    for pattern, tag in _COMPILED:
        if pattern.search(text):
            return tag
    return fallback_topic


def auto_tag_worksheet(numbered_questions: list, fallback_topic: str) -> dict:
    """numbered_questions: [(q_num, preview_text), ...] as returned by
    ws_helpers.numbered_questions(). Returns {q_num: tag}."""
    return {
        q_num: auto_tag_question(text, fallback_topic)
        for q_num, text in numbered_questions
    }
