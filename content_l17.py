"""
Fear Less Maths — Question Content: Level 17 (Quadrilaterals, Circles & Polygons)
Continues the plane-geometry flow from Level 16: Quadrilaterals -> Circles -> Polygons.
"""
from content import cb, tb, q
import random

_QUAD_PROPS = {
    "parallelogram": "opposite sides parallel and equal, opposite angles equal, diagonals bisect each other",
    "rectangle": "a parallelogram with all four angles = 90 degrees; diagonals are equal AND bisect each other",
    "rhombus": "a parallelogram with all four sides equal; diagonals bisect each other at right angles",
    "square": "a rectangle AND a rhombus -- all sides equal, all angles 90 degrees, diagonals equal, perpendicular, and bisecting",
    "trapezium": "exactly one pair of parallel sides -- the other two sides are not parallel or equal",
    "kite": "two pairs of adjacent (not opposite) sides equal; diagonals meet at right angles",
}


# ═══════════════════════════════════════════════════════════════════════════════
# 17A — Quadrilaterals: Types & Properties
# ═══════════════════════════════════════════════════════════════════════════════
def _L17A_s(sheet):
    random.seed(1740 + sheet)
    items = [
        cb("Types of Quadrilaterals", [
            "Parallelogram: opposite sides parallel & equal, opposite angles equal.",
            "Rectangle: a parallelogram with all angles 90 degrees.",
            "Rhombus: a parallelogram with all sides equal. Square: both rectangle AND rhombus.",
            "Trapezium: exactly ONE pair of parallel sides.",
            "Kite: two pairs of ADJACENT (not opposite) equal sides.",
        ], "A square is always a rhombus and a rectangle -- but a rhombus isn't always a square."),
    ]
    kinds = list(_QUAD_PROPS.keys())
    for _ in range(5):
        kind = random.choice(kinds)
        items.append(q(f"Identify this quadrilateral from its marked sides and angles.", "diagram", "____", "", "quadrilateral_types", {"kind": kind}))
    for _ in range(4):
        kind = random.choice(kinds)
        items.append(q(f"Name the quadrilateral that has: {_QUAD_PROPS[kind]}.", "fill", "Answer = ____"))
    for _ in range(4):
        items.append(q("Is every square a rhombus? Is every rhombus a square? Explain.", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("What is the key difference between a parallelogram and a trapezium?", "fill", "Answer = ____"))
    for _ in range(2):
        items.append(q("A kite has equal ADJACENT sides. Does a parallelogram also have this property, or does it have equal OPPOSITE sides?", "fill", "Answer = ____"))
    for _ in range(2):
        kind = random.choice(kinds)
        shown = kind if random.random() > 0.4 else random.choice(kinds)
        items.append(q(f"True or False: A shape with {_QUAD_PROPS[kind]} is called a {shown}.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 17B — Quadrilaterals: Angle Sum, Diagonals & Converse Conditions
# ═══════════════════════════════════════════════════════════════════════════════
def _L17B_s(sheet):
    random.seed(1750 + sheet)
    ranges = {1: (40, 100), 2: (30, 120), 3: (20, 140), 4: (10, 150)}
    lo, hi = ranges[sheet]
    items = [
        cb("Angle Sum of a Quadrilateral", [
            "The four angles of ANY quadrilateral always add up to 360 degrees.",
            "Given three angles, the fourth = 360 minus the sum of the other three.",
        ], "Angles 90,90,90: fourth = 360-270 = 90 (it's a rectangle)."),
        cb("Diagonals & Converse Conditions", [
            "Parallelogram family: diagonals BISECT each other (cut each other in half).",
            "Rectangle/square: diagonals are also EQUAL in length. Rhombus/square: diagonals are PERPENDICULAR.",
            "CONVERSE: if a quadrilateral's diagonals bisect each other, IT MUST BE a parallelogram.",
        ], "If diagonals bisect each other AND are equal, the shape is a rectangle."),
    ]
    for _ in range(5):
        kind = random.choice(list(_QUAD_PROPS.keys()))
        items.append(q("The diagonals are shown. Based on where they cross, what can you say about this shape?", "diagram", "____", "", "quadrilateral_diagonals", {"kind": kind}))
    for _ in range(5):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        c = random.randint(lo, hi)
        while a + b + c >= 355: c = random.randint(lo, hi)
        items.append(q(f"A quadrilateral has angles {a}°, {b}°, {c}°. Find the fourth angle.", "fill", "Answer = ____"))
    for _ in range(4):
        items.append(q("If a quadrilateral's diagonals bisect each other, what type of quadrilateral MUST it be (the converse condition)?", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("A parallelogram's diagonals are found to be EQUAL in length. What extra property does this tell you the shape has (beyond being a parallelogram)?", "fill", "Answer = ____"))
    for _ in range(3):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        c = random.randint(lo, hi)
        while a + b + c >= 355: c = random.randint(lo, hi)
        correct = 360 - a - b - c
        shown = correct if random.random() > 0.4 else correct + 10
        items.append(q(f"True or False: Angles {a}°, {b}°, {c}°, and {shown}° sum to 360°.", "fill", "Answer = ____"))
    return items

# ═══════════════════════════════════════════════════════════════════════════════
# 17C — Circle Basics & Radius/Diameter
# ═══════════════════════════════════════════════════════════════════════════════
def _L17C_s(sheet):
    random.seed(1760 + sheet)
    ranges = {1: (3, 20), 2: (3, 30), 3: (4, 45), 4: (5, 60)}
    lo, hi = ranges[sheet]
    items = [
        cb("Parts of a Circle", [
            "Centre: the fixed middle point. Radius: centre to any point on the circle.",
            "Diameter: a chord through the centre = 2 x radius (the LONGEST chord).",
            "Circumference: the distance all the way around. Chord: joins two points on the circle.",
            "Arc: part of the edge. Sector: a 'pizza slice'. Segment: region between a chord and its arc.",
        ], "Radius 5cm -> diameter 10cm. The diameter is always the longest possible chord."),
    ]
    items.append(q("In the diagram, O is the centre, OB is a radius, and AB is a diameter. Name the radius and the diameter.", "diagram", "____", "", "circle_basics", {}))
    items.append(q("Using the diagram, if radius OB = 6 cm, what is the length of diameter AB?", "diagram", "____", "", "circle_basics", {}))
    for _ in range(6):
        r = random.randint(lo, hi)
        items.append(q(f"Radius = {r} cm. Find the diameter.", "fill", "Answer = ____"))
    for _ in range(5):
        d = random.randint(lo, hi) * 2
        items.append(q(f"Diameter = {d} cm. Find the radius.", "fill", "Answer = ____"))
    for _ in range(4):
        term = random.choice(["centre", "radius", "diameter", "circumference", "chord", "arc", "sector", "segment"])
        prompts = {
            "centre": "What is the fixed middle point of a circle called?",
            "radius": "What do you call the distance from the centre to any point on the circle?",
            "diameter": "What do you call a chord that passes through the centre?",
            "circumference": "What is the distance all the way around a circle called?",
            "chord": "What do you call a line segment joining two points on the circle?",
            "arc": "What is a part of the circle's edge called?",
            "sector": "What do you call the 'pizza slice' region bounded by two radii and an arc?",
            "segment": "What do you call the region between a chord and its arc?",
        }
        items.append(q(prompts[term], "fill", "Answer = ____"))
    for _ in range(3):
        r = random.randint(lo, hi)
        shown = r * 2 if random.random() > 0.4 else r * 2 + 2
        items.append(q(f"True or False: Radius {r} cm gives diameter {shown} cm.", "fill", "Answer = ____"))
    for _ in range(2):
        items.append(q("True or False: The diameter is the longest possible chord of a circle.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 17CUM1 — Chords
# ═══════════════════════════════════════════════════════════════════════════════
def _L17CUM1_s(sheet):
    random.seed(1770 + sheet)
    ranges = {1: (3, 8), 2: (4, 10), 3: (5, 13), 4: (6, 16)}
    lo, hi = ranges[sheet]
    items = [
        cb("Chords of a Circle", [
            "A PERPENDICULAR from the centre to a chord BISECTS the chord (cuts it exactly in half).",
            "EQUAL chords are the SAME distance from the centre (and vice versa -- the converse holds too).",
            "The radius, half-chord, and distance-to-centre form a right triangle -- use Pythagoras.",
        ], "Chord 8, radius 5: half-chord=4, distance to centre = sqrt(25-16)=3."),
    ]
    _chord_variants = [(200, 340), (215, 325), (195, 345), (220, 320)]
    ca1, ca2 = _chord_variants[(sheet - 1) % 4]
    items.append(q("In the diagram, OM is drawn perpendicular from the centre to chord AB. What does this tell you about AM and MB?", "diagram", "____", "", "circle_chord", {"chord_ang1": ca1, "chord_ang2": ca2}))
    items.append(q("Using the diagram, if AM = 4 cm, what is the length of the full chord AB?", "diagram", "____", "", "circle_chord", {"chord_ang1": ca1, "chord_ang2": ca2}))
    triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)]
    for _ in range(5):
        a, b, c = random.choice(triples)
        k = random.randint(1, 2)
        items.append(q(f"A chord of length {2*a*k} is at distance {b*k} from the centre. Find the radius.", "fill", "Answer = ____"))
    for _ in range(5):
        a, b, c = random.choice(triples)
        k = random.randint(1, 2)
        items.append(q(f"Radius {c*k}, chord distance from centre {b*k}. Find the chord's length (twice the half-chord).", "fill", "Answer = ____"))
    for _ in range(4):
        d = random.randint(lo, hi)
        items.append(q(f"Two chords are both {d} cm from the centre. What can you conclude about their lengths?", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("A perpendicular is drawn from the centre to a chord. What happens to the chord (in terms of the two pieces it's split into)?", "fill", "Answer = ____"))
    for _ in range(3):
        a, b, c = random.choice(triples)
        shown = 2 * a if random.random() > 0.4 else 2 * a + 2
        items.append(q(f"True or False: Radius {c}, distance to centre {b}. Chord length = {shown}.", "fill", "Answer = ____"))
    return items

# ═══════════════════════════════════════════════════════════════════════════════
# 17D — Tangents to a Circle
# ═══════════════════════════════════════════════════════════════════════════════
def _L17D_s(sheet):
    random.seed(1780 + sheet)
    triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15)]
    items = [
        cb("Tangent to a Circle", [
            "A tangent touches the circle at exactly ONE point.",
            "The tangent is PERPENDICULAR (90 degrees) to the radius at that point.",
            "So radius, tangent, and the line to the centre form a right triangle -- use Pythagoras.",
        ], "Distance to centre 13, radius 5: tangent length = sqrt(169-25) = 12."),
        cb("Tangent Length from an External Point", [
            "From any external point, the TWO tangents drawn to a circle are EQUAL in length.",
            "Tangent length = sqrt(distance to centre^2 - radius^2).",
        ], "Two tangents from the same external point are always equal -- a very useful shortcut."),
    ]
    _touch_variants = [30, 45, 55, 65]
    ta = _touch_variants[(sheet - 1) % 4]
    items.append(q("In the diagram, the tangent touches the circle at P, and OP is a radius. What is the angle marked between the tangent and OP?", "diagram", "90°", "", "circle_tangent", {"touch_ang": ta}))
    items.append(q("Using the diagram, if OP = 5 cm and the tangent length PQ = 12 cm, find OQ (the distance from the centre to the external point).", "diagram", "____", "", "circle_tangent", {"touch_ang": ta}))
    for _ in range(6):
        a, b, c = random.choice(triples)
        items.append(q(f"External point is {c} from the centre. Radius is {b}. Find the tangent length.", "fill", "Answer = ____"))
    for _ in range(5):
        a, b, c = random.choice(triples)
        items.append(q(f"A tangent of length {a} touches a circle of radius {b}. Find the distance from the external point to the centre.", "fill", "Answer = ____"))
    for _ in range(4):
        items.append(q("A tangent touches a circle at point P. What is the angle between the tangent and the radius drawn to P?", "fill", "Answer = ____"))
    for _ in range(3):
        val = random.randint(5, 20)
        items.append(q(f"From an external point, one tangent to a circle is {val} cm. Find the length of the OTHER tangent from the same point.", "fill", "Answer = ____"))
    for _ in range(2):
        items.append(q("True or False: A tangent can touch a circle at two different points.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 17E — Circle Theorems
# ═══════════════════════════════════════════════════════════════════════════════
def _L17E_s(sheet):
    random.seed(1790 + sheet)
    ranges = {1: (10, 60), 2: (10, 80), 3: (10, 90), 4: (5, 85)}
    lo, hi = ranges[sheet]
    items = [
        cb("Key Circle Theorems", [
            "The angle at the CENTRE = 2 x the angle at the CIRCUMFERENCE (same arc).",
            "The angle in a SEMICIRCLE is always 90 degrees.",
            "Angles in the SAME SEGMENT (subtending the same arc) are EQUAL.",
        ], "Arc gives 40 degrees at the circumference -> 80 degrees at the centre."),
    ]
    _s_variants = [40, 50, 60, 70]
    s_ = _s_variants[(sheet - 1) % 4]
    items.append(q(f"In the diagram, angle BAC (at the circumference) and angle BOC (at the centre) stand on the same arc BC. If angle BAC = {s_}°, find angle BOC.", "diagram", f"{2*s_}°", "", "circle_central_inscribed_angle", {"b_ang": 270 - s_, "c_ang": 270 + s_, "a_ang": 90}))
    items.append(q("Using the diagram, explain in your own words why the centre angle is always double the circumference angle on the same arc.", "diagram", "____", "", "circle_central_inscribed_angle", {"b_ang": 270 - s_, "c_ang": 270 + s_, "a_ang": 90}))
    for _ in range(5):
        circ = random.randint(lo, min(hi, 89))
        items.append(q(f"Angle at the circumference = {circ}°. Find the angle at the centre (same arc).", "fill", "Answer = ____"))
    for _ in range(5):
        centre = random.randint(lo, min(hi, 178)) * 2 // 2
        while centre % 2 != 0: centre = random.randint(lo, min(hi, 178))
        items.append(q(f"Angle at the centre = {centre}°. Find the angle at the circumference (same arc).", "fill", "Answer = ____"))
    for _ in range(4):
        items.append(q("A triangle is inscribed in a semicircle, with the hypotenuse as the diameter. Find the angle opposite the diameter.", "fill", "Answer = ____"))
    for _ in range(3):
        val = random.randint(lo, hi)
        items.append(q(f"Angle ABC = {val}° and angle ADC subtends the same arc as ABC (same segment). Find angle ADC.", "fill", "Answer = ____"))
    for _ in range(3):
        circ = random.randint(lo, min(hi, 89))
        shown = circ * 2 if random.random() > 0.4 else circ * 2 + 10
        items.append(q(f"True or False: Circumference angle {circ}° gives a centre angle of {shown}°.", "fill", "Answer = ____"))
    return items

# ═══════════════════════════════════════════════════════════════════════════════
# 17F — Cyclic Quadrilaterals
# ═══════════════════════════════════════════════════════════════════════════════
def _L17F_s(sheet):
    random.seed(1800 + sheet)
    ranges = {1: (50, 110), 2: (40, 130), 3: (30, 140), 4: (20, 150)}
    lo, hi = ranges[sheet]
    items = [
        cb("Cyclic Quadrilaterals", [
            "A cyclic quadrilateral has ALL FOUR corners on the circle.",
            "Its OPPOSITE angles are SUPPLEMENTARY -- they add up to 180 degrees.",
            "An EXTERIOR angle of a cyclic quadrilateral equals the OPPOSITE interior angle.",
            "This connects circles back to quadrilaterals -- a cyclic quadrilateral is still a real quadrilateral (angle sum 360), but with this extra circle property.",
        ], "If one angle is 70°, its opposite angle is 110° (70+110=180)."),
    ]
    _angs_variants = [(100, 200, 260, 340), (95, 190, 255, 330), (110, 205, 265, 350), (90, 195, 250, 335)]
    av = _angs_variants[(sheet - 1) % 4]
    items.append(q("In the diagram, ABCD is a cyclic quadrilateral with all four angles marked. Which pairs of angles are supplementary?", "diagram", "____", "", "cyclic_quadrilateral_theorem", {"angs": av}))
    items.append(q("Using the diagram, angle A and angle C are opposite angles of the cyclic quadrilateral. Confirm they add to 180°.", "diagram", "180°", "", "cyclic_quadrilateral_theorem", {"angs": av}))
    for _ in range(6):
        a = random.randint(lo, hi)
        items.append(q(f"Cyclic quadrilateral: one angle is {a}°. Find its OPPOSITE angle.", "fill", "Answer = ____"))
    for _ in range(5):
        a = random.randint(lo, hi)
        items.append(q(f"Cyclic quadrilateral: an exterior angle is {a}°. Find the OPPOSITE interior angle.", "fill", "Answer = ____"))
    for _ in range(4):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        while a + b >= 355: b = random.randint(lo, hi)
        items.append(q(f"Cyclic quadrilateral ABCD: angle A={a}°, angle B={b}°. Find angle C (opposite A) and angle D (opposite B).", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("Explain why a cyclic quadrilateral's opposite angles must sum to 360-360+180=180 (using both the quadrilateral angle sum AND the circle property).", "fill", "Answer = ____"))
    for _ in range(2):
        a = random.randint(lo, hi)
        correct = 180 - a
        shown = correct if random.random() > 0.4 else correct + 10
        items.append(q(f"True or False: Cyclic quadrilateral angle {a}° has opposite angle {shown}°.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 17CUM2 — Angle in a Circle
# ═══════════════════════════════════════════════════════════════════════════════
def _L17CUM2_s(sheet):
    random.seed(1810 + sheet)
    ranges = {1: (10, 70), 2: (10, 85), 3: (5, 88), 4: (5, 89)}
    lo, hi = ranges[sheet]
    items = [
        cb("Angle in a Circle — Further Practice", [
            "Combine the centre/circumference theorem, semicircle theorem, and same-segment theorem.",
            "Look for the arc each angle stands on -- that tells you which theorem applies.",
        ], "Angle in a semicircle is always 90 -- no calculation needed once you spot the diameter."),
    ]
    _s_variants2 = [35, 45, 55, 65]
    s2 = _s_variants2[(sheet - 1) % 4]
    items.append(q(f"In the diagram, angle BAC = {s2}° at the circumference. Find angle BOC at the centre (same arc).", "diagram", f"{2*s2}°", "", "circle_central_inscribed_angle", {"b_ang": 270 - s2, "c_ang": 270 + s2, "a_ang": 90}))
    for _ in range(6):
        circ = random.randint(lo, hi)
        items.append(q(f"Angle at the circumference = {circ}°. Find the angle at the centre.", "fill", "Answer = ____"))
    for _ in range(5):
        items.append(q("A chord is also the diameter. A triangle is formed with a point on the circumference. Find the angle at that point.", "fill", "Answer = ____"))
    for _ in range(5):
        val = random.randint(lo, hi)
        items.append(q(f"Two angles stand on the same arc, in the same segment. One is {val}°. Find the other.", "fill", "Answer = ____"))
    for _ in range(4):
        circ = random.randint(lo, hi)
        shown = circ * 2 if random.random() > 0.4 else circ + 90
        items.append(q(f"True or False: Circumference angle {circ}° means the centre angle is {shown}°.", "fill", "Answer = ____"))
    return items

# ═══════════════════════════════════════════════════════════════════════════════
# 17G — Applications of Circles
# ═══════════════════════════════════════════════════════════════════════════════
def _L17G_s(sheet):
    random.seed(1820 + sheet)
    triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15)]
    items = [
        cb("Applications of Circles", [
            "Circles model wheels, satellite orbits, running tracks, pipes, and pulley belts.",
            "Tangent problems often model a ladder or line of sight just touching a curved edge.",
        ], "A satellite's line of sight to the horizon is tangent to the Earth's circle."),
    ]
    for _ in range(6):
        a, b, c = random.choice(triples)
        items.append(q(f"A ladder (tangent line) reaches an external point {c}m from a circular tower's centre (radius {b}m). Find the tangent length.", "fill", "Answer = ____"))
    for _ in range(5):
        r = random.randint(5, 20)
        items.append(q(f"A circular running track has radius {r}m. Find its diameter.", "fill", "Answer = ____"))
    for _ in range(5):
        a = random.randint(60, 150)
        items.append(q(f"A cyclic quadrilateral window frame has one angle {a}°. Find the opposite angle.", "fill", "Answer = ____"))
    for _ in range(4):
        circ = random.randint(20, 80)
        items.append(q(f"A circular arch: the angle at the circumference is {circ}°. Find the angle at the centre.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 17H — Polygons: Interior Angle Sum
# ═══════════════════════════════════════════════════════════════════════════════
def _L17H_s(sheet):
    random.seed(1830 + sheet)
    n_ranges = {1: (5, 7), 2: (5, 8), 3: (6, 9), 4: (6, 10)}
    lo_n, hi_n = n_ranges[sheet]
    items = [
        cb("Interior Angle Sum of a Polygon", [
            "Any n-sided polygon can be split into (n-2) triangles from one vertex.",
            "Since each triangle's angles sum to 180, the polygon's INTERIOR angle sum = (n-2) x 180.",
            "For a REGULAR polygon (all angles equal), each interior angle = (n-2) x 180 / n.",
        ], "A pentagon (n=5): (5-2)x180 = 540. Regular pentagon: each angle = 540/5 = 108."),
    ]
    for _ in range(6):
        n = random.randint(lo_n, hi_n)
        items.append(q(f"Use the diagram to find the interior angle sum of this {n}-sided polygon.", "diagram", "____", "", "polygon_angle_sum", {"n": n}))
    for _ in range(5):
        n = random.randint(lo_n, hi_n + 2)
        items.append(q(f"Find the interior angle sum of a {n}-sided polygon using (n-2) x 180.", "fill", "Answer = ____"))
    for _ in range(4):
        n = random.randint(lo_n, hi_n + 2)
        total = (n - 2) * 180
        items.append(q(f"A regular {n}-sided polygon has interior angle sum {total}°. Find EACH interior angle.", "fill", "Answer = ____"))
    for _ in range(3):
        n = random.randint(lo_n, hi_n)
        items.append(q(f"How many triangles do you get when you triangulate an {n}-sided polygon from one vertex?", "fill", "Answer = ____"))
    for _ in range(2):
        n = random.randint(lo_n, hi_n + 2)
        correct = (n - 2) * 180
        shown = correct if random.random() > 0.4 else correct + 180
        items.append(q(f"True or False: A {n}-sided polygon has interior angle sum {shown}°.", "fill", "Answer = ____"))
    return items

# ═══════════════════════════════════════════════════════════════════════════════
# 17I — Puzzle Problems
# ═══════════════════════════════════════════════════════════════════════════════
def _L17I_s(sheet):
    random.seed(1840 + sheet)
    ranges = {1: (20, 60), 2: (15, 80), 3: (10, 90), 4: (5, 100)}
    lo, hi = ranges[sheet]
    items = [
        cb("Circle & Quadrilateral Puzzles", [
            "Combine several theorems together: cyclic quadrilateral + circle theorems + tangents.",
            "Set up an equation from what's given, then solve step by step.",
        ], "Cyclic quad angle 3x, opposite x: 3x+x=180 -> x=45."),
    ]
    for _ in range(5):
        x_val = random.randint(20, 60)
        items.append(q(f"Cyclic quadrilateral: one angle is 3x, its opposite is x. If x={x_val}, verify 3x+x=180 works. Find both angles.", "fill", "Answer = ____"))
    for _ in range(5):
        items.append(q("Cyclic quadrilateral: opposite angles are 2x+10 and x+50. Find x.", "fill", "Answer = ____"))
    for _ in range(4):
        val = random.randint(lo, hi)
        items.append(q(f"Two tangents from an external point form an angle of {val}° between them. If the radius makes a right angle with each tangent, find the angle at the circle's centre between the two radii (hint: quadrilateral angle sum).", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("A triangle is inscribed in a semicircle. One other angle is 35°. Find the third angle (remember the semicircle angle is 90°).", "fill", "Answer = ____"))
    for _ in range(3):
        val = random.randint(lo, hi)
        items.append(q(f"Angle at circumference = 2x, angle at centre = {val}°. Find x.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 17CUM3 — Polygons: Exterior Angles & Regular Polygons
# ═══════════════════════════════════════════════════════════════════════════════
def _L17CUM3_s(sheet):
    random.seed(1850 + sheet)
    n_ranges = {1: (5, 8), 2: (5, 9), 3: (6, 10), 4: (6, 12)}
    lo_n, hi_n = n_ranges[sheet]
    items = [
        cb("Exterior Angles & Regular Polygons", [
            "The exterior angles of ANY polygon always add up to 360 degrees -- no matter how many sides!",
            "For a REGULAR polygon: each exterior angle = 360 / n.",
            "Interior + exterior at each vertex = 180 (they're a linear pair).",
        ], "Regular hexagon (n=6): each exterior angle = 360/6 = 60. Each interior = 180-60 = 120."),
    ]
    for _ in range(5):
        n = random.randint(lo_n, hi_n)
        while 360 % n != 0: n = random.randint(lo_n, hi_n)
        items.append(q(f"A regular {n}-sided polygon. Find each exterior angle (360/n).", "fill", "Answer = ____"))
    for _ in range(5):
        n = random.randint(lo_n, hi_n)
        while 360 % n != 0: n = random.randint(lo_n, hi_n)
        ext = 360 // n
        items.append(q(f"A regular polygon has exterior angle {ext}°. Find the number of sides (360/exterior angle).", "fill", "Answer = ____"))
    for _ in range(4):
        n = random.randint(lo_n, hi_n)
        while 360 % n != 0: n = random.randint(lo_n, hi_n)
        ext = 360 // n
        interior = 180 - ext
        items.append(q(f"A regular {n}-gon has exterior angle {ext}°. Find each interior angle (180 - exterior).", "fill", "Answer = ____"))
    for _ in range(3):
        items.append(q("True or False: The exterior angles of a polygon always sum to 360°, no matter how many sides it has.", "fill", "Answer = ____"))
    for _ in range(3):
        n = random.randint(lo_n, hi_n)
        while 360 % n != 0: n = random.randint(lo_n, hi_n)
        correct = 360 // n
        shown = correct if random.random() > 0.4 else correct + 5
        items.append(q(f"True or False: A regular {n}-gon has exterior angle {shown}°.", "fill", "Answer = ____"))
    return items

# ═══════════════════════════════════════════════════════════════════════════════
# 17J — Quadrilaterals, Circles & Polygons Mastery Challenge
# ═══════════════════════════════════════════════════════════════════════════════
def _L17J_s(sheet):
    random.seed(1860 + sheet)
    triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)]
    items = [
        cb("Quadrilaterals, Circles & Polygons Mastery Challenge", [
            "Every skill: quadrilateral properties, circle theorems, tangents, polygon angle sums.",
            "Bigger numbers here -- this challenge covers the whole level.",
            "Speed challenge: each question has a point value.",
        ], "Bronze 20+, Silver 30+, Gold 38+ (all correct)"),
    ]
    for _ in range(4):
        a = random.randint(50, 150)
        b = random.randint(30, 100)
        c = random.randint(30, 100)
        while a + b + c >= 355: c = random.randint(30, 100)
        items.append(q(f"Quadrilateral angles {a}°, {b}°, {c}°. Find the fourth.  [1 point]", "fill", "Answer = ____"))
    for _ in range(4):
        a = random.randint(40, 140)
        items.append(q(f"Cyclic quadrilateral angle {a}°. Find its opposite angle.  [1 point]", "fill", "Answer = ____"))
    for _ in range(4):
        a, b, c = random.choice(triples)
        k = random.randint(1, 3)
        items.append(q(f"Distance to centre {c*k}, radius {b*k}. Find the tangent length.  [2 points]", "fill", "Answer = ____"))
    for _ in range(4):
        n = random.choice([5, 6, 8, 9, 10])
        items.append(q(f"Find the interior angle sum of a {n}-sided polygon.  [2 points]", "fill", "Answer = ____"))
    for _ in range(2):
        n = random.choice([5, 6, 8, 9, 10])
        while 360 % n != 0: n = random.choice([5, 6, 8, 9, 10])
        items.append(q(f"A regular {n}-gon: find each exterior angle.  [2 points]", "fill", "Answer = ____"))
    for _ in range(2):
        items.append(q("True or False: The exterior angles of any polygon sum to 360°.  [1 point]", "fill", "Answer = ____ (True/False)"))
    items.append(tb("Your Score", ["My total score: _____.  My badge: Bronze / Silver / Gold (circle one)"]))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# 17REV — Level 17 Revision
# ═══════════════════════════════════════════════════════════════════════════════
def _L17REV_s(sheet):
    random.seed(1870 + sheet)
    triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)]
    items = [
        tb("Level 17 Revision — Tips", [
            "Quadrilaterals: know each type's defining property. Angle sum always 360.",
            "Diagonals bisect each other in the parallelogram family (converse holds too).",
            "Circles: angle at centre = 2x circumference angle. Semicircle angle = 90.",
            "Cyclic quadrilateral: opposite angles sum to 180. Tangent perpendicular to radius.",
            "Polygons: interior sum = (n-2)x180. Exterior angles ALWAYS sum to 360.",
        ]),
    ]
    for _ in range(2):
        kind = random.choice(list(_QUAD_PROPS.keys()))
        items.append(q(f"Name the quadrilateral with: {_QUAD_PROPS[kind]}.", "fill", "Answer = ____"))
    for _ in range(2):
        a = random.randint(60, 150)
        b = random.randint(40, 100)
        c = random.randint(40, 100)
        while a + b + c >= 355: c = random.randint(40, 100)
        items.append(q(f"Quadrilateral angles {a}°, {b}°, {c}°. Find the fourth.", "fill", "Answer = ____"))
    for _ in range(2):
        r = random.randint(5, 30)
        items.append(q(f"Radius {r} cm. Find the diameter.", "fill", "Answer = ____"))
    for _ in range(2):
        a, b, c = random.choice(triples)
        items.append(q(f"Chord distance from centre {b}, radius {c}. Find the chord length.", "fill", "Answer = ____"))
    for _ in range(2):
        a, b, c = random.choice(triples)
        items.append(q(f"Distance to centre {c}, radius {b}. Find the tangent length.", "fill", "Answer = ____"))
    for _ in range(2):
        circ = random.randint(20, 80)
        items.append(q(f"Angle at circumference {circ}°. Find the angle at the centre.", "fill", "Answer = ____"))
    for _ in range(2):
        a = random.randint(50, 140)
        items.append(q(f"Cyclic quadrilateral angle {a}°. Find the opposite angle.", "fill", "Answer = ____"))
    for _ in range(2):
        n = random.choice([5, 6, 7, 8])
        items.append(q(f"Interior angle sum of a {n}-sided polygon?", "fill", "Answer = ____"))
    for _ in range(2):
        n = random.choice([5, 6, 8, 9])
        while 360 % n != 0: n = random.choice([5, 6, 8, 9])
        items.append(q(f"Regular {n}-gon: find each exterior angle.", "fill", "Answer = ____"))
    for _ in range(2):
        items.append(q("True or False: Diagonals of a rectangle are equal in length.", "fill", "Answer = ____"))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# DISPATCH for Level 17
# ═══════════════════════════════════════════════════════════════════════════════
DISPATCH_L17 = {
    "17A":    {1: lambda: _L17A_s(1), 2: lambda: _L17A_s(2), 3: lambda: _L17A_s(3), 4: lambda: _L17A_s(4)},
    "17B":    {1: lambda: _L17B_s(1), 2: lambda: _L17B_s(2), 3: lambda: _L17B_s(3), 4: lambda: _L17B_s(4)},
    "17C":    {1: lambda: _L17C_s(1), 2: lambda: _L17C_s(2), 3: lambda: _L17C_s(3), 4: lambda: _L17C_s(4)},
    "17CUM1": {1: lambda: _L17CUM1_s(1), 2: lambda: _L17CUM1_s(2), 3: lambda: _L17CUM1_s(3), 4: lambda: _L17CUM1_s(4)},
    "17D":    {1: lambda: _L17D_s(1), 2: lambda: _L17D_s(2), 3: lambda: _L17D_s(3), 4: lambda: _L17D_s(4)},
    "17E":    {1: lambda: _L17E_s(1), 2: lambda: _L17E_s(2), 3: lambda: _L17E_s(3), 4: lambda: _L17E_s(4)},
    "17F":    {1: lambda: _L17F_s(1), 2: lambda: _L17F_s(2), 3: lambda: _L17F_s(3), 4: lambda: _L17F_s(4)},
    "17CUM2": {1: lambda: _L17CUM2_s(1), 2: lambda: _L17CUM2_s(2), 3: lambda: _L17CUM2_s(3), 4: lambda: _L17CUM2_s(4)},
    "17G":    {1: lambda: _L17G_s(1), 2: lambda: _L17G_s(2), 3: lambda: _L17G_s(3), 4: lambda: _L17G_s(4)},
    "17H":    {1: lambda: _L17H_s(1), 2: lambda: _L17H_s(2), 3: lambda: _L17H_s(3), 4: lambda: _L17H_s(4)},
    "17I":    {1: lambda: _L17I_s(1), 2: lambda: _L17I_s(2), 3: lambda: _L17I_s(3), 4: lambda: _L17I_s(4)},
    "17CUM3": {1: lambda: _L17CUM3_s(1), 2: lambda: _L17CUM3_s(2), 3: lambda: _L17CUM3_s(3), 4: lambda: _L17CUM3_s(4)},
    "17J":    {1: lambda: _L17J_s(1), 2: lambda: _L17J_s(2), 3: lambda: _L17J_s(3), 4: lambda: _L17J_s(4)},
    "17REV":  {1: lambda: _L17REV_s(1), 2: lambda: _L17REV_s(2), 3: lambda: _L17REV_s(3), 4: lambda: _L17REV_s(4)},
}
