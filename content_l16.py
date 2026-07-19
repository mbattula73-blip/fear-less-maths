"""
Fear Less Maths — Question Content: Level 16 (Lines, Angles & Triangles)
Complete plane-geometry flow: Point -> Line/Ray -> Angle -> Angle Properties
-> Parallel Lines & Transversal -> Triangles (types, congruence, inequality,
similarity, BPT, Pythagoras) -> Areas on the same base.
"""
from content import cb, tb, q
import random


# ═══ Helpers ═══
def _can_form_triangle(a, b, c):
    return a + b > c and b + c > a and a + c > b


def _classify_by_sides(a, b, c):
    x, y, z = sorted([a, b, c])
    lhs, rhs = x * x + y * y, z * z
    if lhs == rhs: return "right"
    if lhs > rhs: return "acute"
    return "obtuse"


# ═══════════════════════════════════════════════════════════════════════════════
# 16A — Point, Line, Ray, Line Segment & Types of Angles
# ═══════════════════════════════════════════════════════════════════════════════
def _L16A_s(sheet):
    random.seed(1600 + sheet)
    ranges = {1: (10, 60), 2: (10, 90), 3: (10, 150), 4: (10, 175)}
    lo, hi = ranges[sheet]
    items = [
        cb("Point, Line, Ray & Line Segment", [
            "A POINT has a position but no size -- just a location, marked with a dot.",
            "A LINE extends forever in BOTH directions -- no endpoints.",
            "A RAY starts at one point and extends forever in ONE direction.",
            "A LINE SEGMENT has two fixed endpoints -- a definite length.",
        ], "Line AB extends both ways. Ray AB starts at A, goes through B, forever. Segment AB stops at both A and B."),
        cb("Types of Angles", [
            "Acute: less than 90°. Right: exactly 90°. Obtuse: between 90° and 180°.",
            "Straight: exactly 180° (a straight line). Reflex: more than 180°.",
            "An angle is measured in degrees using a protractor.",
        ], "A 40° angle is acute. A 120° angle is obtuse. A 250° angle is reflex."),
    ]
    for _ in range(4):
        kind = random.choice(["point", "line", "ray", "segment"])
        prompts = {
            "point": "Which geometric object has a position but NO size or length?",
            "line": "Which geometric object extends forever in BOTH directions?",
            "ray": "Which geometric object starts at one point and extends forever in ONE direction?",
            "segment": "Which geometric object has two fixed endpoints and a definite length?",
        }
        items.append(q(prompts[kind], "diagram", "____", "", "points_lines_rays", {}))
    for _ in range(4):
        angle = random.randint(lo, hi)
        while angle == 90 or angle == 180:
            angle = random.randint(lo, hi)
        items.append(q(f"Classify this angle: {angle}°. Is it acute, right, obtuse, straight, or reflex?", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("Ray AB and Ray BA -- are they the same ray? Explain.", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("How many endpoints does a line segment have? A ray? A line?", "fill", "Answer = ____"))
    for _ in range(3):
        angle = random.randint(lo, hi)
        while angle in (90, 180): angle = random.randint(lo, hi)
        correct = "acute" if angle < 90 else ("obtuse" if angle < 180 else "reflex")
        shown = correct if random.random() > 0.4 else random.choice(["acute", "obtuse", "reflex", "right"])
        items.append(q(f"True or False: A {angle}° angle is {shown}.", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("True or False: A line has two endpoints.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 16B — Angle Pair Properties
# ═══════════════════════════════════════════════════════════════════════════════
def _L16B_s(sheet):
    random.seed(1610 + sheet)
    ranges = {1: (20, 60), 2: (15, 75), 3: (10, 80), 4: (5, 85)}
    lo, hi = ranges[sheet]
    items = [
        cb("Angle Pair Properties", [
            "Complementary angles: add up to 90°.",
            "Supplementary angles: add up to 180°.",
            "Linear pair: two ADJACENT angles on a straight line -- they are supplementary.",
            "Vertically opposite angles: formed by two crossing lines -- always EQUAL.",
            "Angles around a single point add up to 360°.",
        ], "40° and 50° are complementary. 110° and 70° are supplementary."),
    ]
    for _ in range(4):
        a1 = random.randint(lo, min(hi, 85))
        items.append(q(f"These two angles are complementary. One is {a1}°. Find the other.", "diagram", "____", "", "angle_pair", {"kind": "complementary", "a1": a1}))
    for _ in range(4):
        a1 = random.randint(lo, min(hi, 175))
        items.append(q(f"These two angles are supplementary. One is {a1}°. Find the other.", "diagram", "____", "", "angle_pair", {"kind": "supplementary", "a1": a1}))
    for _ in range(3):
        a1 = random.randint(lo, min(hi, 80))
        items.append(q("These two lines cross. Find the vertically opposite angle marked x.", "diagram", "____", "", "angle_pair", {"kind": "vertical", "a1": a1}))
    for _ in range(3):
        a1 = random.randint(10, 80)
        items.append(q(f"Two complementary angles: one is {a1}°. Find the other.", "fill", "Answer = ____"))
    for _ in range(3):
        a1 = random.randint(20, 160)
        items.append(q(f"Two supplementary angles: one is {a1}°. Find the other.", "fill", "Answer = ____"))
    for _ in range(3):
        a1 = random.randint(10, 80)
        correct = 90 - a1
        shown = correct if random.random() > 0.4 else correct + 5
        items.append(q(f"True or False: Complementary to {a1}° is {shown}°.", "fill", "Answer = ____"))
    return items

# ═══════════════════════════════════════════════════════════════════════════════
# 16C — Parallel Lines & a Transversal
# ═══════════════════════════════════════════════════════════════════════════════
def _L16C_s(sheet):
    random.seed(1620 + sheet)
    ranges = {1: (40, 80), 2: (30, 100), 3: (20, 120), 4: (10, 140)}
    lo, hi = ranges[sheet]
    items = [
        cb("Parallel Lines Cut by a Transversal", [
            "CORRESPONDING angles (same position at each crossing) are EQUAL.",
            "ALTERNATE INTERIOR angles (opposite sides, between the lines) are EQUAL.",
            "CO-INTERIOR angles (same side, between the lines) are SUPPLEMENTARY (sum 180°).",
            "CONVERSE: if corresponding angles are equal (or alternate angles equal, or co-interior supplementary), the lines ARE parallel.",
        ], "Angle 1 = 70°. Angle 5 (corresponding) = 70°. Angle 4 (alternate interior) = 70°."),
    ]
    for _ in range(6):
        val = random.randint(lo, hi)
        kind = random.choice(["corresponding", "alternate interior", "vertically opposite"])
        items.append(q(f"In this diagram, angle 1 = {val}°. Find the angle that is {kind} to it (they are EQUAL).", "diagram", "____", "", "transversal_angles", {}))
    for _ in range(4):
        val = random.randint(lo, hi)
        items.append(q(f"Two parallel lines cut by a transversal. One angle is {val}°. Find its co-interior angle (they are supplementary).", "fill", "Answer = ____"))
    for _ in range(4):
        val = random.randint(lo, hi)
        items.append(q(f"Angle 1 = {val}°. Angle 1 and angle 2 are a linear pair. Find angle 2.", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("If two lines are cut by a transversal and the corresponding angles are equal, what can you conclude about the two lines?", "fill", "Answer = ____"))
    for _ in range(3):
        val = random.randint(lo, hi)
        shown = val if random.random() > 0.4 else val + 10
        items.append(q(f"True or False: If angle 1 = {val}° then its alternate interior angle is also {shown}°.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 16CUM1 — Types of Triangles, Angle Sum & Exterior Angle
# ═══════════════════════════════════════════════════════════════════════════════
def _L16CUM1_s(sheet):
    random.seed(1630 + sheet)
    ranges = {1: (30, 70), 2: (20, 90), 3: (20, 110), 4: (10, 130)}
    lo, hi = ranges[sheet]
    items = [
        cb("Triangles: Types, Angle Sum & Exterior Angle", [
            "By sides: equilateral (all equal), isosceles (2 equal), scalene (all different).",
            "By angles: acute (all <90), right (one =90), obtuse (one >90).",
            "ANGLE SUM: the three angles of any triangle always add up to 180°.",
            "EXTERIOR ANGLE THEOREM: an exterior angle equals the sum of the two remote (non-adjacent) interior angles.",
        ], "Angles 50, 60, 70 -> sum 180 (valid triangle). Exterior angle = 50+60=110 if opposite interior is 70... exterior at that vertex = remote pair sum."),
    ]
    for _ in range(4):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        while a + b >= 175: b = random.randint(lo, hi)
        items.append(q(f"A triangle has angles {a}° and {b}°. Find the third angle.", "fill", "Answer = ____"))
    for _ in range(3):
        s1, s2, s3 = sorted([random.randint(3, hi // 5 + 3) for _ in range(3)])
        kind = "equilateral" if s1 == s2 == s3 else ("isosceles" if s1 == s2 or s2 == s3 else "scalene")
        items.append(q(f"Sides {s1}, {s2}, {s3}: classify this triangle by its sides.", "fill", "Answer = ____"))
    for _ in range(4):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        while a + b >= 175: b = random.randint(lo, hi)
        ext = a + b
        items.append(q(f"A triangle's two remote interior angles are {a}° and {b}°. Find the exterior angle at the third vertex.", "fill", "Answer = ____"))
    for _ in range(3):
        ext = random.randint(lo + 40, min(hi + 60, 170))
        a = random.randint(20, ext - 20)
        b = ext - a
        items.append(q(f"An exterior angle is {ext}°. One remote interior angle is {a}°. Find the other remote interior angle.", "fill", "Answer = ____"))
    for _ in range(3):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        while a + b >= 175: b = random.randint(lo, hi)
        correct = 180 - a - b
        shown = correct if random.random() > 0.4 else correct + 10
        items.append(q(f"True or False: A triangle with angles {a}° and {b}° has a third angle of {shown}°.", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("True or False: The exterior angle of a triangle equals the sum of the two remote interior angles.", "fill", "Answer = ____"))
    return items

# ═══════════════════════════════════════════════════════════════════════════════
# 16D — Congruence of Triangles
# ═══════════════════════════════════════════════════════════════════════════════
def _L16D_s(sheet):
    random.seed(1640 + sheet)
    items = [
        cb("Congruent Triangles", [
            "Congruent = same shape AND same size (one fits exactly on the other).",
            "Congruence rules: SSS (3 sides), SAS (2 sides + included angle), ASA (2 angles + included side),",
            "AAS (2 angles + non-included side), RHS (right angle, hypotenuse, side -- right triangles only).",
            "AAA is NOT a congruence rule -- equal angles alone only give SIMILAR triangles.",
        ], "SAS needs the angle BETWEEN the two given sides."),
        cb("Applying the Rules", [
            "Match the given information to the pattern: 3 sides -> SSS; 2 sides+angle between -> SAS.",
            "2 angles + the side between them -> ASA; 2 angles + a side NOT between -> AAS.",
            "If triangles are congruent, ALL corresponding parts are equal (CPCT).",
        ], "Triangle ABC ≅ DEF means AB=DE, BC=EF, AC=DF, and all matching angles equal too."),
    ]
    given_cases = [
        ("three sides equal", "SSS"),
        ("two sides and the INCLUDED angle equal", "SAS"),
        ("two angles and the INCLUDED side equal", "ASA"),
        ("two angles and a NON-included side equal", "AAS"),
        ("a right angle, hypotenuse, and one side equal (right triangles)", "RHS"),
    ]
    for _ in range(6):
        desc, rule = random.choice(given_cases)
        items.append(q(f"Two triangles have {desc}. Which congruence rule applies?", "fill", "Answer = ____"))
    for _ in range(4):
        val = random.randint(3, 15)
        items.append(q(f"Triangle ABC ≅ Triangle DEF. AB = {val}. Find DE (using CPCT).", "fill", "Answer = ____"))
    for _ in range(4):
        val = random.randint(20, 130)
        items.append(q(f"Triangle ABC ≅ Triangle DEF. Angle A = {val}°. Find angle D (using CPCT).", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("Is AAA (three equal angles) enough to prove two triangles congruent? Explain.", "fill", "Answer = ____"))
    for _ in range(3):
        desc, rule = random.choice(given_cases)
        shown = rule if random.random() > 0.4 else random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
        items.append(q(f"True or False: Given {desc}, the rule is {shown}.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 16E — Triangle Inequality & the Isosceles Triangle Theorem
# ═══════════════════════════════════════════════════════════════════════════════
def _L16E_s(sheet):
    random.seed(1650 + sheet)
    ranges = {1: (3, 10), 2: (3, 14), 3: (4, 18), 4: (4, 22)}
    lo, hi = ranges[sheet]
    items = [
        cb("Triangle Inequality", [
            "The sum of any TWO sides of a triangle must be GREATER than the third side.",
            "Check ALL THREE pairs -- if even one fails, the triangle can't be formed.",
            "Quick check: add the two SMALLER sides -- if their sum beats the largest side, it's valid.",
        ], "3,4,5: 3+4=7>5 ✓. 1,2,5: 1+2=3, not >5 -- INVALID, no triangle."),
        cb("The Isosceles Triangle Theorem", [
            "THEOREM: angles opposite EQUAL sides are EQUAL (base angles of an isosceles triangle match).",
            "CONVERSE: if two angles are equal, the sides opposite them are also equal.",
            "Both directions are true -- equal sides <-> equal angles.",
        ], "Sides 5,5,8: the two 5-sides are equal, so their opposite (base) angles are equal too."),
    ]

    def gen_valid(hi):
        while True:
            a, b, c = sorted([random.randint(lo, hi) for _ in range(3)])
            if _can_form_triangle(a, b, c):
                return a, b, c

    def gen_invalid(hi):
        while True:
            a, b, c = sorted([random.randint(lo, hi) for _ in range(3)])
            if not _can_form_triangle(a, b, c):
                return a, b, c

    for _ in range(4):
        a, b, c = gen_valid(hi) if random.random() > 0.4 else gen_invalid(hi)
        items.append(q(f"Can a triangle be formed with sides {a}, {b}, {c}? Check the triangle inequality.", "fill", "Answer = ____"))
    for _ in range(4):
        a, b, c = gen_invalid(hi)
        items.append(q(f"Sides {a}, {b}, {c}: which pair of sides fails the triangle inequality?", "fill", "Answer = ____"))
    for _ in range(4):
        base = random.randint(lo, hi)
        angle = random.randint(30, 80)
        items.append(q(f"Isosceles triangle: two equal sides, and the base angle opposite one of them is {angle}°. Find the OTHER base angle.", "fill", "Answer = ____"))
    for _ in range(3):
        vertex = random.randint(20, 100)
        base_angle = (180 - vertex) / 2
        items.append(q(f"Isosceles triangle: vertex angle {vertex}°, base angles equal. Find each base angle.", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("A triangle has two equal ANGLES. What can you conclude about the sides opposite them (the converse)?", "fill", "Answer = ____"))
    for _ in range(2):
        a, b, c = gen_valid(hi)
        shown = "Yes" if random.random() > 0.4 else "No"
        items.append(q(f"True or False: Sides {a}, {b}, {c} can form a triangle -- Answer: {shown}.", "fill", "Answer = ____"))
    return items

# ═══════════════════════════════════════════════════════════════════════════════
# 16F — Similar Triangles
# ═══════════════════════════════════════════════════════════════════════════════
def _L16F_s(sheet):
    random.seed(1660 + sheet)
    ranges = {1: (2, 5), 2: (2, 6), 3: (3, 7), 4: (3, 9)}
    lo, hi = ranges[sheet]
    items = [
        cb("Similar Triangles", [
            "Similar = same shape, possibly different size. Corresponding angles equal, sides in the same ratio.",
            "Similarity rules: AA (2 angles), SSS (all sides in ratio), SAS (2 sides in ratio + included angle).",
            "Scale factor = ratio of corresponding sides. Areas scale by the SQUARE of the scale factor.",
        ], "Sides 3,4,5 and 6,8,10 are similar -- scale factor 2. Area ratio = 4."),
    ]
    for _ in range(4):
        k = random.randint(2, 5)
        a, b, c = random.randint(lo, hi), random.randint(lo, hi), random.randint(lo, hi)
        items.append(q(f"Triangle sides {a},{b},{c} are scaled by factor {k}. Find the new sides.", "fill", "Answer = ____"))
    for _ in range(4):
        a = random.randint(lo, hi)
        k = random.randint(2, 5)
        items.append(q(f"Two similar triangles: a side of {a} corresponds to a side of {a*k}. Find the scale factor.", "fill", "Answer = ____"))
    for _ in range(4):
        k = random.randint(2, 4)
        area = random.randint(lo, hi)
        items.append(q(f"Two similar triangles have scale factor {k}. The smaller triangle has area {area}. Find the larger triangle's area.", "fill", "Answer = ____"))
    for _ in range(3):
        pole, shadow, obj_shadow = random.randint(2, 6), random.randint(2, 6), random.randint(10, 40)
        height = pole * obj_shadow / shadow
        if height == int(height):
            items.append(q(f"A {pole}m pole casts a {shadow}m shadow. A tree casts a {obj_shadow}m shadow at the same time. Find the tree's height.", "fill", "Answer = ____"))
        else:
            items.append(q(f"Two triangles are similar with sides {lo} and {hi}. Find the scale factor.", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("Two triangles have all three pairs of corresponding angles equal. Which similarity rule applies, and are they necessarily congruent?", "fill", "Answer = ____"))
    for _ in range(2):
        k = random.randint(2, 4)
        shown = k * k if random.random() > 0.4 else k * k + 1
        items.append(q(f"True or False: Scale factor {k} means the area ratio is {shown}.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 16CUM2 — Basic Proportionality Theorem & Midpoint Theorem
# ═══════════════════════════════════════════════════════════════════════════════
def _L16CUM2_s(sheet):
    random.seed(1670 + sheet)
    ranges = {1: (2, 5), 2: (2, 6), 3: (3, 8), 4: (3, 10)}
    lo, hi = ranges[sheet]
    items = [
        cb("Basic Proportionality Theorem (Thales)", [
            "If DE is parallel to BC in triangle ABC (D on AB, E on AC), then AD/DB = AE/EC.",
            "CONVERSE: if AD/DB = AE/EC, then DE MUST be parallel to BC.",
            "This is the foundation theorem behind similar triangles.",
        ], "AD=4,DB=2,AE=6: since 4/2=2, EC must be 3 for DE||BC (6/3=2)."),
        cb("The Midpoint Theorem", [
            "The segment joining the MIDPOINTS of two sides of a triangle is PARALLEL to the third side.",
            "That segment is also exactly HALF the length of the third side.",
            "CONVERSE: a line through the midpoint of one side, parallel to another side, bisects the third side.",
        ], "Midpoints of two sides of a triangle with third side 10: the midsegment is 5, parallel to it."),
    ]

    def gen_bpt(hi):
        db = random.randint(lo, hi)
        mult = random.randint(1, 3)
        ad = db * mult
        ec = random.randint(lo, hi)
        ae = ad * ec // db if (ad * ec) % db == 0 else db * random.randint(1, 3)
        if (ad * ec) % db != 0:
            ec = db * random.randint(1, 3)
            ae = ad * ec // db
        return ad, db, ae, ec

    for _ in range(6):
        ad, db, ae, ec = gen_bpt(hi)
        items.append(q(f"DE || BC in triangle ABC. AD={ad}, DB={db}, AE={ae}. Find EC.", "diagram", "____", "", "bpt_triangle", {"ad": ad, "db": db, "ae": ae, "ec": ec}))
    for _ in range(5):
        ad, db, ae, ec = gen_bpt(hi)
        items.append(q(f"DE || BC in triangle ABC. AD={ad}, DB={db}, AE={ae}. Find EC using AD/DB=AE/EC.", "fill", "Answer = ____"))
    for _ in range(4):
        third_side = random.randint(lo * 2, hi * 2)
        items.append(q(f"The third side of a triangle is {third_side}. Find the length of the midsegment (joining the midpoints of the other two sides).", "fill", "Answer = ____"))
    for _ in range(3):
        midseg = random.randint(lo, hi)
        items.append(q(f"The midsegment of a triangle is {midseg}. Find the length of the third side (parallel to it).", "fill", "Answer = ____"))
    for _ in range(2):
        ad, db, ae, ec = gen_bpt(hi)
        shown = ec if random.random() > 0.4 else ec + 1
        items.append(q(f"True or False: DE||BC, AD={ad}, DB={db}, AE={ae}. This means EC={shown}.", "fill", "Answer = ____"))
    return items

# ═══════════════════════════════════════════════════════════════════════════════
# 16G — Pythagoras Theorem & its Converse
# ═══════════════════════════════════════════════════════════════════════════════
def _L16G_s(sheet):
    random.seed(1680 + sheet)
    triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 40, 41), (20, 21, 29)]
    items = [
        cb("Pythagoras Theorem", [
            "In a right triangle: (hypotenuse)^2 = (leg)^2 + (leg)^2.",
            "Common triples: 3-4-5, 5-12-13, 8-15-17, 7-24-25 (and their multiples).",
        ], "Legs 3,4: hyp = sqrt(9+16) = 5."),
        cb("The CONVERSE of Pythagoras", [
            "Given three side lengths, compare (longest)^2 to the sum of the other two squares.",
            "EQUAL -> right triangle. Sum GREATER than longest^2 -> acute. Sum LESS -> obtuse.",
            "This lets you classify a triangle just from its side lengths, no angles needed.",
        ], "Sides 4,5,6: 16+25=41 > 36, so it's ACUTE. Sides 4,5,8: 16+25=41 < 64, so it's OBTUSE."),
    ]
    for _ in range(5):
        a, b, c = random.choice(triples)
        if random.random() > 0.5:
            items.append(q(f"Legs {a} and {b}: find the hypotenuse.", "fill", "Answer = ____"))
        else:
            items.append(q(f"Hypotenuse {c}, one leg {a}: find the other leg.", "fill", "Answer = ____"))
    for _ in range(6):
        kind = random.choice(["right", "acute", "obtuse"])
        a, b, c = random.choice(triples)
        if kind == "right":
            sides = (a, b, c)
        elif kind == "acute":
            sides = (a, b, c - random.randint(1, 2))
        else:
            sides = (a, b, c + random.randint(1, 3))
        s1, s2, s3 = sides
        items.append(q(f"Sides {s1}, {s2}, {s3}. Use the converse of Pythagoras to classify this triangle: right, acute, or obtuse?", "fill", "Answer = ____"))
    for _ in range(4):
        a, b, c = random.choice(triples)
        items.append(q(f"Verify: does {a}^2 + {b}^2 = {c}^2? Show both sides.", "fill", "Answer = ____"))
    for _ in range(3):
        a, b, c = random.choice(triples)
        shown = "right" if random.random() > 0.4 else random.choice(["acute", "obtuse"])
        items.append(q(f"True or False: Sides {a}, {b}, {c} form a {shown} triangle.", "fill", "Answer = ____"))
    for _ in range(2):
        items.append(q("A triangle has sides where (longest side)^2 is LESS than the sum of the squares of the other two. What type of triangle is it?", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 16H — Applications of Triangles
# ═══════════════════════════════════════════════════════════════════════════════
def _L16H_s(sheet):
    random.seed(1690 + sheet)
    ranges = {1: (3, 8), 2: (4, 10), 3: (5, 13), 4: (6, 16)}
    lo, hi = ranges[sheet]
    triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15)]
    items = [
        cb("Applications of Triangles", [
            "Triangles model ladders, ramps, roofs, shadows, and navigation.",
            "Draw a diagram, label what's known, then apply angle-sum, Pythagoras, or similarity.",
        ], "Ladder 5m against a wall, base 3m from wall: height = sqrt(25-9) = 4m."),
    ]
    for _ in range(5):
        a, b, c = random.choice(triples)
        k = random.choice([1, 1, 2])
        a, b, c = a * k, b * k, c * k
        items.append(q(f"A ladder {c}m long leans against a wall, its base {a}m from the wall. Find the height it reaches.", "fill", "Answer = ____"))
    for _ in range(4):
        a, b, c = random.choice(triples)
        items.append(q(f"A ramp rises {a}m over a horizontal distance of {b}m. Find the ramp's length.", "fill", "Answer = ____"))
    for _ in range(4):
        base_angle = random.randint(30, 75)
        apex = 180 - 2 * base_angle
        items.append(q(f"A roof truss (isosceles triangle) has base angles of {base_angle}° each. Find the apex angle.", "fill", "Answer = ____"))
    for _ in range(4):
        a, b, c = random.choice(triples)
        items.append(q(f"Two roads meet at 90°. A car drives {a}km then turns and drives {b}km. Find the straight-line distance back to the start.", "fill", "Answer = ____"))
    for _ in range(3):
        pole, shadow = random.choice([(2, 3), (3, 4), (4, 5)])
        obj_shadow = shadow * random.randint(3, 6)
        height = pole * obj_shadow / shadow
        items.append(q(f"A {pole}m pole casts a {shadow}m shadow. A building casts a {obj_shadow}m shadow. Find the building's height.", "fill", "Answer = ____"))
    return items

# ═══════════════════════════════════════════════════════════════════════════════
# 16I — Puzzle Geometry
# ═══════════════════════════════════════════════════════════════════════════════
def _L16I_s(sheet):
    random.seed(1700 + sheet)
    ranges = {1: (10, 40), 2: (10, 60), 3: (5, 70), 4: (5, 80)}
    lo, hi = ranges[sheet]
    items = [
        cb("Puzzle Geometry", [
            "Combine several rules together: angle sum, exterior angle, isosceles properties, parallel lines.",
            "Look for isosceles marks, parallel-line arrows, and right angles in the description.",
            "Set up an equation from what you're told, then solve step by step.",
        ], "Isosceles triangle, vertex 2x, base angles x each: 2x+x+x=180 -> x=45."),
    ]
    for _ in range(5):
        x_val = random.randint(15, 50)
        vertex = 2 * x_val
        items.append(q(f"Isosceles triangle: vertex angle 2x, base angles x each. If x={x_val}, verify the angle sum works. Find the vertex angle.", "fill", "Answer = ____"))
    for _ in range(4):
        x_val = random.randint(10, 40)
        items.append(q(f"Three angles: x, x+{random.randint(10,30)}, x+{random.randint(31,60)} sum to 180°. Find x.", "fill", "Answer = ____"))
    for _ in range(4):
        rem1 = random.randint(lo, hi)
        x_coef = random.randint(2, 4)
        ext = x_coef * random.randint(2, 5)
        items.append(q(f"Exterior angle {x_coef}x equals the sum of remote interior angles x and {rem1}. Find x.", "fill", "Answer = ____"))
    for _ in range(4):
        acute = random.randint(20, 44)
        items.append(q(f"A right triangle has one acute angle 2x and the other 3x. Find x, then both acute angles.", "fill", "Answer = ____"))
    for _ in range(3):
        val = random.randint(lo, hi)
        items.append(q(f"Two parallel lines cut by a transversal. One angle is 3x and its co-interior angle is 2x. Find x.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 16CUM3 — Areas of Triangles & Parallelograms on the Same Base
# ═══════════════════════════════════════════════════════════════════════════════
def _L16CUM3_s(sheet):
    random.seed(1710 + sheet)
    ranges = {1: (4, 10), 2: (5, 14), 3: (6, 18), 4: (8, 22)}
    lo, hi = ranges[sheet]
    items = [
        cb("Areas on the Same Base, Between the Same Parallels", [
            "Parallelograms on the SAME base and between the SAME parallels have EQUAL area.",
            "A triangle on the same base and between the same parallels as a parallelogram has HALF its area.",
            "Triangles on the same base and between the same parallels have EQUAL area.",
            "The key idea: area only depends on base x height -- the SLANT doesn't matter.",
        ], "Parallelogram base 8, height 5: area=40. A triangle on the same base/parallels has area 20."),
    ]
    for _ in range(5):
        b = random.randint(lo, hi)
        h = random.randint(lo, hi)
        items.append(q(f"Parallelogram P1 has base {b} and height {h} (area={b*h}). Parallelogram P2 sits on the SAME base, between the SAME parallels. Find P2's area.", "fill", "Answer = ____"))
    for _ in range(5):
        b = random.randint(lo, hi)
        h = random.randint(lo, hi)
        para_area = b * h
        items.append(q(f"A parallelogram has base {b} and height {h} (area={para_area}). A triangle sits on the same base, between the same parallels. Find the triangle's area.", "fill", "Answer = ____"))
    for _ in range(4):
        b = random.randint(lo, hi)
        h = random.randint(lo, hi)
        tri_area = 0.5 * b * h
        items.append(q(f"Triangle T1 has base {b}, height {h} (area={tri_area:g}). Triangle T2 sits on the same base, between the same parallels. Find T2's area.", "fill", "Answer = ____"))
    for _ in range(3):
        b = random.randint(lo, hi)
        h = random.randint(lo, hi)
        para_area = b * h
        shown = para_area // 2 if random.random() > 0.4 else para_area
        items.append(q(f"True or False: A parallelogram (base {b}, height {h}, area {para_area}) and a triangle on the same base/parallels -- the triangle's area is {shown}.", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("Two parallelograms share the same base and lie between the same two parallel lines. What can you say about their areas, even if their shapes (slant) differ?", "fill", "Answer = ____"))
    return items

# ═══════════════════════════════════════════════════════════════════════════════
# 16J — Lines, Angles & Triangles Mastery Challenge
# ═══════════════════════════════════════════════════════════════════════════════
def _L16J_s(sheet):
    random.seed(1720 + sheet)
    ranges = {1: (10, 60), 2: (15, 90), 3: (20, 120), 4: (25, 150)}
    lo, hi = ranges[sheet]
    triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 40, 41)]
    items = [
        cb("Lines, Angles & Triangles Mastery Challenge", [
            "Every skill: angle pairs, transversals, triangle rules, BPT, Pythagoras, areas.",
            "Bigger numbers here -- this challenge covers the whole level.",
            "Speed challenge: each question has a point value.",
        ], "Bronze 20+, Silver 30+, Gold 38+ (all correct)"),
    ]
    for _ in range(4):
        a1 = random.randint(20, 85)
        items.append(q(f"Complementary angles: one is {a1}°. Find the other.  [1 point]", "fill", "Answer = ____"))
    for _ in range(4):
        a1 = random.randint(30, 170)
        items.append(q(f"Supplementary angles: one is {a1}°. Find the other.  [1 point]", "fill", "Answer = ____"))
    for _ in range(4):
        db = random.randint(2, 8)
        mult = random.randint(1, 3)
        ad = db * mult
        ec = random.randint(2, 8)
        ae = ad * ec // db if (ad * ec) % db == 0 else db
        if (ad * ec) % db != 0:
            ec = db
            ae = ad
        items.append(q(f"DE||BC: AD={ad}, DB={db}, AE={ae}. Find EC.  [2 points]", "fill", "Answer = ____"))
    for _ in range(4):
        a, b, c = random.choice(triples)
        k = random.randint(1, 3)
        items.append(q(f"Legs {a*k} and {b*k}: find the hypotenuse.  [2 points]", "fill", "Answer = ____"))
    for _ in range(2):
        a, b, c = random.choice(triples)
        items.append(q(f"Sides {a}, {b}, {c+1}: classify using the converse of Pythagoras (right/acute/obtuse).  [2 points]", "fill", "Answer = ____"))
    for _ in range(2):
        items.append(q("True or False: AAA proves two triangles are congruent.  [1 point]", "fill", "Answer = ____ (True/False)"))
    items.append(tb("Your Score", ["My total score: _____.  My badge: Bronze / Silver / Gold (circle one)"]))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 16REV — Level 16 Revision
# ═══════════════════════════════════════════════════════════════════════════════
def _L16REV_s(sheet):
    random.seed(1730 + sheet)
    ranges = {1: (10, 40), 2: (15, 60), 3: (20, 90), 4: (25, 120)}
    lo, hi = ranges[sheet]
    triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)]
    items = [
        tb("Level 16 Revision — Tips", [
            "Angle pairs: complementary (90), supplementary (180), vertically opposite (equal).",
            "Transversal: corresponding/alternate angles equal; co-interior angles supplementary.",
            "Triangle: angle sum=180, exterior=sum of remote interiors, inequality (2 sides>3rd).",
            "Congruence (SSS/SAS/ASA/AAS/RHS) vs Similarity (AA/SSS/SAS ratios). BPT: AD/DB=AE/EC.",
            "Pythagoras a^2+b^2=c^2 and its converse. Areas on same base/parallels are equal.",
        ]),
    ]
    for _ in range(2):
        a1 = random.randint(20, 85)
        items.append(q(f"Complementary angles: one is {a1}°. Find the other.", "fill", "Answer = ____"))
    for _ in range(2):
        a1 = random.randint(30, 170)
        items.append(q(f"Supplementary angles: one is {a1}°. Find the other.", "fill", "Answer = ____"))
    for _ in range(2):
        val = random.randint(lo, hi)
        items.append(q(f"Two parallel lines, transversal angle {val}°. Find its corresponding angle.", "fill", "Answer = ____"))
    for _ in range(2):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        while a + b >= 175: b = random.randint(lo, hi)
        items.append(q(f"Triangle angles {a}° and {b}°. Find the third.", "fill", "Answer = ____"))
    for _ in range(2):
        s1, s2, s3 = sorted([random.randint(3, 15) for _ in range(3)])
        items.append(q(f"Can sides {s1}, {s2}, {s3} form a triangle?", "fill", "Answer = ____"))
    for _ in range(2):
        db = random.randint(2, 6)
        ad = db * random.randint(1, 3)
        ec = random.randint(2, 6)
        items.append(q(f"DE||BC: AD={ad}, DB={db}, EC={ec}. Find AE.", "fill", "Answer = ____"))
    for _ in range(2):
        a, b, c = random.choice(triples)
        items.append(q(f"Legs {a} and {b}: find the hypotenuse.", "fill", "Answer = ____"))
    for _ in range(2):
        a, b, c = random.choice(triples)
        items.append(q(f"Sides {a}, {b}, {c}: is this a right triangle? Use the converse of Pythagoras.", "fill", "Answer = ____"))
    for _ in range(2):
        b = random.randint(lo, hi)
        h = random.randint(lo, hi)
        items.append(q(f"Parallelogram base {b}, height {h}. A triangle sits on the same base, between the same parallels. Find its area.", "fill", "Answer = ____"))
    for _ in range(2):
        desc = random.choice(["three sides equal", "two sides and the included angle", "two angles and the included side"])
        items.append(q(f"Congruence rule for: {desc}?", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# DISPATCH for Level 16
# ═══════════════════════════════════════════════════════════════════════════════
DISPATCH_L16 = {
    "16A":    {1: lambda: _L16A_s(1), 2: lambda: _L16A_s(2), 3: lambda: _L16A_s(3), 4: lambda: _L16A_s(4)},
    "16B":    {1: lambda: _L16B_s(1), 2: lambda: _L16B_s(2), 3: lambda: _L16B_s(3), 4: lambda: _L16B_s(4)},
    "16C":    {1: lambda: _L16C_s(1), 2: lambda: _L16C_s(2), 3: lambda: _L16C_s(3), 4: lambda: _L16C_s(4)},
    "16CUM1": {1: lambda: _L16CUM1_s(1), 2: lambda: _L16CUM1_s(2), 3: lambda: _L16CUM1_s(3), 4: lambda: _L16CUM1_s(4)},
    "16D":    {1: lambda: _L16D_s(1), 2: lambda: _L16D_s(2), 3: lambda: _L16D_s(3), 4: lambda: _L16D_s(4)},
    "16E":    {1: lambda: _L16E_s(1), 2: lambda: _L16E_s(2), 3: lambda: _L16E_s(3), 4: lambda: _L16E_s(4)},
    "16F":    {1: lambda: _L16F_s(1), 2: lambda: _L16F_s(2), 3: lambda: _L16F_s(3), 4: lambda: _L16F_s(4)},
    "16CUM2": {1: lambda: _L16CUM2_s(1), 2: lambda: _L16CUM2_s(2), 3: lambda: _L16CUM2_s(3), 4: lambda: _L16CUM2_s(4)},
    "16G":    {1: lambda: _L16G_s(1), 2: lambda: _L16G_s(2), 3: lambda: _L16G_s(3), 4: lambda: _L16G_s(4)},
    "16H":    {1: lambda: _L16H_s(1), 2: lambda: _L16H_s(2), 3: lambda: _L16H_s(3), 4: lambda: _L16H_s(4)},
    "16I":    {1: lambda: _L16I_s(1), 2: lambda: _L16I_s(2), 3: lambda: _L16I_s(3), 4: lambda: _L16I_s(4)},
    "16CUM3": {1: lambda: _L16CUM3_s(1), 2: lambda: _L16CUM3_s(2), 3: lambda: _L16CUM3_s(3), 4: lambda: _L16CUM3_s(4)},
    "16J":    {1: lambda: _L16J_s(1), 2: lambda: _L16J_s(2), 3: lambda: _L16J_s(3), 4: lambda: _L16J_s(4)},
    "16REV":  {1: lambda: _L16REV_s(1), 2: lambda: _L16REV_s(2), 3: lambda: _L16REV_s(3), 4: lambda: _L16REV_s(4)},
}

# ═══════════════════════════════════════════════════════════════════════════════
# Level 16 auto-visualizer: gives every Level 16 (Lines, Angles &
# Triangles) question a matching diagram built from its OWN numbers.
# First 2 diagrams per sheet worked (demo), rest blank scaffolds.
# ═══════════════════════════════════════════════════════════════════════════════
import re as _l16_re


def _l16_infer_diagram(text, sublevel_code=""):
    t = text

    # --- angle pairs (16B) ---
    m = _l16_re.search(r'complementary\. One is (\d+)°', t)
    if m:
        return "angle_pair", {"kind": "complementary", "a1": int(m.group(1))}
    m = _l16_re.search(r'supplementary\. One is (\d+)°', t)
    if m:
        return "angle_pair", {"kind": "supplementary", "a1": int(m.group(1))}
    m = _l16_re.search(r'Two complementary angles: one is (\d+)°', t)
    if m:
        return "angle_pair", {"kind": "complementary", "a1": int(m.group(1))}
    m = _l16_re.search(r'Two supplementary angles: one is (\d+)°', t)
    if m:
        return "angle_pair", {"kind": "supplementary", "a1": int(m.group(1))}
    m = _l16_re.search(r'vertically opposite angle', t)
    if m:
        return "angle_pair", {"kind": "vertical", "a1": 50}

    # --- parallel lines / transversal (16C) ---
    if 'transversal' in t.lower() or 'alternate interior' in t.lower() or 'co-interior' in t.lower():
        return "transversal_angles", {}
    if 'corresponding' in t.lower() and ('parallel' in t.lower() or 'diagram' in t.lower()):
        return "transversal_angles", {}

    # --- triangle type / angle sum / exterior angle (16CUM1) ---
    m = _l16_re.search(r'has angles (\d+)° and (\d+)°\. Find the third angle', t)
    if m:
        return "angle_sum_triangle", {"a": int(m.group(1)), "b": int(m.group(2)), "mode": "sum"}
    m = _l16_re.search(r'remote interior angles are (\d+)° and (\d+)°', t)
    if m:
        return "angle_sum_triangle", {"a": int(m.group(1)), "b": int(m.group(2)), "mode": "exterior"}
    m = _l16_re.search(r'exterior angle is (\d+)°\. One remote interior angle is (\d+)°', t)
    if m:
        ext, rem = int(m.group(1)), int(m.group(2))
        other = ext - rem
        return "angle_sum_triangle", {"a": rem, "b": other, "mode": "exterior"}
    m = _l16_re.search(r'Sides (\d+), (\d+), (\d+): classify this triangle by its sides', t)
    if m:
        s1, s2, s3 = (int(x) for x in m.groups())
        return "triangle_classify", {"angles": [60, 60, 60], "sides": [s1, s2, s3]}

    # --- congruence (16D) ---
    m = _l16_re.search(r'three sides equal', t)
    if m:
        return "congruence", {"rule": "SSS"}
    m = _l16_re.search(r'two sides and the INCLUDED angle equal', t)
    if m:
        return "congruence", {"rule": "SAS"}
    m = _l16_re.search(r'two angles and the INCLUDED side equal', t)
    if m:
        return "congruence", {"rule": "ASA"}
    m = _l16_re.search(r'two angles and a NON-included side equal', t)
    if m:
        return "congruence", {"rule": "AAS"}
    m = _l16_re.search(r'right angle, hypotenuse, and one side', t)
    if m:
        return "congruence", {"rule": "RHS"}
    m = _l16_re.search(r'Given (.+?), the rule is (\w+)', t)
    if m:
        rule_map = {"three sides equal": "SSS", "two sides and the INCLUDED angle equal": "SAS",
                    "two angles and the INCLUDED side equal": "ASA", "two angles and a NON-included side equal": "AAS",
                    "a right angle, hypotenuse, and one side equal (right triangles)": "RHS"}
        rule = rule_map.get(m.group(1), "SSS")
        return "congruence", {"rule": rule}

    # --- triangle inequality / isosceles (16E) ---
    m = _l16_re.search(r'sides (\d+), (\d+), (\d+)\? Check the triangle inequality', t)
    if m:
        a, b, c = (int(x) for x in m.groups())
        return "triangle_inequality", {"a": a, "b": b, "c": c}
    m = _l16_re.search(r'Sides (\d+), (\d+), (\d+): which pair', t)
    if m:
        a, b, c = (int(x) for x in m.groups())
        return "triangle_inequality", {"a": a, "b": b, "c": c}
    m = _l16_re.search(r'base angle opposite one of them is (\d+)°', t)
    if m:
        return "isosceles_theorem", {"base_angle": int(m.group(1))}
    m = _l16_re.search(r'vertex angle (\d+)°, base angles equal', t)
    if m:
        vertex = int(m.group(1))
        base = (180 - vertex) / 2
        return "isosceles_theorem", {"base_angle": base}

    # --- similar triangles (16F) ---
    m = _l16_re.search(r'Triangle sides (\d+),(\d+),(\d+) are scaled by factor (\d+)', t)
    if m:
        a, b, c, k = (int(x) for x in m.groups())
        return "similar_triangles", {"sides1": (a, b, c), "k": k}
    m = _l16_re.search(r'a side of (\d+) corresponds to a side of (\d+)', t)
    if m:
        a, ak = int(m.group(1)), int(m.group(2))
        k = ak // a if a and ak % a == 0 else 2
        return "similar_triangles", {"sides1": (a, a+1, a+2), "k": k}

    # --- BPT / midpoint theorem (16CUM2) ---
    m = _l16_re.search(r'AD=(\d+), DB=(\d+), AE=(\d+)', t)
    if m:
        ad, db, ae = (int(x) for x in m.groups())
        ec = ae * db // ad if ad else 1
        return "bpt_triangle", {"ad": ad, "db": db, "ae": ae, "ec": ec}
    m = _l16_re.search(r'third side of a triangle is (\d+)\. Find the length of the midsegment', t)
    if m:
        return "midpoint_theorem", {"third_side": int(m.group(1))}
    m = _l16_re.search(r'midsegment of a triangle is (\d+)\. Find the length of the third side', t)
    if m:
        return "midpoint_theorem", {"third_side": int(m.group(1)) * 2}

    # --- Pythagoras (16G, 16H) ---
    m = _l16_re.search(r'Legs (\d+) and (\d+): find the hypotenuse', t)
    if m:
        a, b = (int(x) for x in m.groups())
        import math as _m
        c = _m.isqrt(a*a + b*b)
        return "pythagoras", {"a": a, "b": b, "c": c, "find": "hyp"}
    m = _l16_re.search(r'Hypotenuse (\d+), one leg (\d+): find the other leg', t)
    if m:
        c, a = (int(x) for x in m.groups())
        import math as _m
        b = _m.isqrt(c*c - a*a)
        return "pythagoras", {"a": a, "b": b, "c": c, "find": "leg_b"}
    m = _l16_re.search(r'Sides (\d+), (\d+), (\d+)\. Use the converse', t)
    if m:
        a, b, c = sorted(int(x) for x in m.groups())
        return "pythagoras", {"a": a, "b": b, "c": c, "find": "hyp"}
    m = _l16_re.search(r'Verify: does (\d+)\^2 \+ (\d+)\^2 = (\d+)\^2', t)
    if m:
        a, b, c = (int(x) for x in m.groups())
        return "pythagoras", {"a": a, "b": b, "c": c, "find": "hyp"}
    m = _l16_re.search(r'ladder (\d+)m long leans against a wall, its base (\d+)m from the wall', t)
    if m:
        c, a = (int(x) for x in m.groups())
        import math as _m
        b2 = c*c - a*a
        b = _m.isqrt(b2) if b2 > 0 else 1
        return "pythagoras", {"a": a, "b": b, "c": c, "find": "leg_b"}
    m = _l16_re.search(r'ramp rises (\d+)m over a horizontal distance of (\d+)m', t)
    if m:
        a, b = (int(x) for x in m.groups())
        import math as _m
        c = round((a*a + b*b) ** 0.5, 1)
        return "pythagoras", {"a": a, "b": b, "c": c, "find": "hyp"}
    m = _l16_re.search(r'drives (\d+)km then turns and drives (\d+)km', t)
    if m:
        a, b = (int(x) for x in m.groups())
        c = round((a*a + b*b) ** 0.5, 1)
        return "pythagoras", {"a": a, "b": b, "c": c, "find": "hyp"}
    m = _l16_re.search(r'roof truss \(isosceles triangle\) has base angles of (\d+)°', t)
    if m:
        return "isosceles_theorem", {"base_angle": int(m.group(1))}

    # --- areas on same base (16CUM3) ---
    m = _l16_re.search(r'Parallelogram P1 has base (\d+) and height (\d+).*?SAME base.*?SAME parallels', t)
    if m:
        b, h = (int(x) for x in m.groups())
        return "area_same_base", {"base": b, "height": h, "shape": "para_para"}
    m = _l16_re.search(r'parallelogram has base (\d+) and height (\d+).*?triangle sits on the same base', t)
    if m:
        b, h = (int(x) for x in m.groups())
        return "area_same_base", {"base": b, "height": h, "shape": "para_tri"}
    m = _l16_re.search(r'Triangle T1 has base (\d+), height (\d+).*?Triangle T2 sits on the same base', t)
    if m:
        b, h = (int(x) for x in m.groups())
        return "area_same_base", {"base": b, "height": h, "shape": "tri_tri"}

    return None


_L16_FAMILY_FALLBACK = {
    "16A": ("points_lines_rays", {}),
    "16B": ("angle_pair", {"kind": "complementary", "a1": 35}),
    "16C": ("transversal_angles", {}),
    "16CUM1": ("angle_sum_triangle", {"a": 60, "b": 70, "mode": "sum"}),
    "16D": ("congruence", {"rule": "SAS"}),
    "16E": ("triangle_inequality", {"a": 3, "b": 4, "c": 5}),
    "16F": ("similar_triangles", {"sides1": (3, 4, 5), "k": 2}),
    "16CUM2": ("bpt_triangle", {"ad": 4, "db": 2, "ae": 6, "ec": 3}),
    "16G": ("pythagoras", {"a": 3, "b": 4, "c": 5, "find": "hyp"}),
    "16H": ("pythagoras", {"a": 3, "b": 4, "c": 5, "find": "hyp"}),
    "16I": ("angle_sum_triangle", {"a": 60, "b": 70, "mode": "sum"}),
    "16CUM3": ("area_same_base", {"base": 8, "height": 5, "shape": "para_para"}),
    "16J": ("triangle_classify", {"angles": [90, 45, 45], "sides": [5, 5, 7]}),
    "16REV": ("pythagoras", {"a": 3, "b": 4, "c": 5, "find": "hyp"}),
}


def _l16_fallback(sublevel_code):
    for key in sorted(_L16_FAMILY_FALLBACK, key=len, reverse=True):
        if sublevel_code.startswith(key):
            return _L16_FAMILY_FALLBACK[key]
    return ("points_lines_rays", {})


def _l16_visualize(items, sublevel_code):
    fb_type, fb_params = _l16_fallback(sublevel_code)
    out = []
    diagram_count = 0
    for item in items:
        new_item = dict(item)
        if item.get("type") in ("fill", "word"):
            inferred = _l16_infer_diagram(item["text"], sublevel_code)
            new_item["type"] = "diagram"
            if inferred:
                new_item["diagram_type"], params = inferred
            else:
                new_item["diagram_type"], params = fb_type, fb_params
            params = dict(params)
            params["blank"] = diagram_count >= 2
            new_item["diagram_params"] = params
            diagram_count += 1
        elif item.get("type") == "diagram":
            params = dict(item.get("diagram_params") or {})
            params["blank"] = diagram_count >= 2
            new_item["diagram_params"] = params
            diagram_count += 1
        out.append(new_item)
    return out


def _l16_wrap(fn, sublevel_code):
    return lambda: _l16_visualize(fn(), sublevel_code)


DISPATCH_L16 = {
    sub: {sheet: _l16_wrap(fn, sub) for sheet, fn in sheets.items()}
    for sub, sheets in DISPATCH_L16.items()
}
