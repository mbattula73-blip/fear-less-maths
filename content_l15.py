"""
Fear Less Maths — Question Content: Level 15 (Coordinate Geometry)
Every question hand-written. No placeholders.
Sheet 1=Intuition, Sheet 2=Concept, Sheet 3=Practice (tips box), Sheet 4=Mastery
Remedial variants replace numbers using remedialise() in content.py.

Sublevels:
  15A Coordinate plane      15B Plotting points     15C Distance formula
  15CUM1 Mixed A+B+C        15D Midpoint formula    15E Section concept
  15F Graph basics         15CUM2 Mixed D+E+F       15G Graph applications
  15H Mixed                15I Puzzle graphs        15CUM3 Mixed G+H+I
  15J Mixed challenge      15REV Level 15 Revision
"""
from content import cb, tb, q
import random


# ═══════════════════════════════════════════════════════════════════════════════
# 15A — Coordinate plane
# ═══════════════════════════════════════════════════════════════════════════════
def _L15A_1():
    return [
        cb("The Coordinate Plane", [
            "Two number lines cross at right angles: the x-axis (horizontal) and y-axis (vertical).",
            "They meet at the ORIGIN (0, 0).",
            "A point is written as (x, y): x first, then y.",
        ], "Point (3, 2): go 3 right, 2 up."),
        cb("The Four Quadrants", [
            "Quadrant I: x>0, y>0 (top right).",
            "Quadrant II: x<0, y>0 (top left).",
            "Quadrant III: x<0, y<0 (bottom left). Quadrant IV: x>0, y<0 (bottom right).",
        ], "(3, 2) is in Quadrant I. (-3, 2) is in Quadrant II."),
        q("What are the coordinates of the origin? ____", "fill", "Answer = ____"),
        q("In the point (5, 7), which is the x-coordinate? ____", "fill", "Answer = ____"),
        q("In the point (5, 7), which is the y-coordinate? ____", "fill", "Answer = ____"),
        q("Which axis is horizontal? ____", "fill", "Answer = ____"),
        q("Which axis is vertical? ____", "fill", "Answer = ____"),
        q("Which quadrant is (4, 3) in? ____", "fill", "Answer = ____"),
        q("Which quadrant is (-2, 5) in? ____", "fill", "Answer = ____"),
        q("Which quadrant is (-4, -6) in? ____", "fill", "Answer = ____"),
        q("Which quadrant is (7, -1) in? ____", "fill", "Answer = ____"),
        q("Point (0, 4) lies on which axis? ____", "fill", "Answer = ____"),
        q("Point (6, 0) lies on which axis? ____", "fill", "Answer = ____"),
        q("To plot (3, 2) you go 3 units in which direction first? ____", "fill", "Answer = ____"),
        q("To plot (3, 2) you then go 2 units in which direction? ____", "fill", "Answer = ____"),
        q("True or False: In (x, y), the x-coordinate is written first.", "fill", "Answer = ____"),
        q("True or False: The origin is the point (0, 0).", "fill", "Answer = ____"),
        q("True or False: (-3, -3) is in Quadrant III.", "fill", "Answer = ____"),
        q("True or False: A point on the y-axis has x-coordinate 0.", "fill", "Answer = ____"),
        q("Spot: (-2, 5) is in Quadrant III. Correct? Fix (Quadrant II). ____", "fill", "Answer = ____"),
        q("True or False: The x-axis is the horizontal number line.", "fill", "Answer = ____"),
    ]

def _L15A_2():
    return [
        cb("Reading Coordinates", [
            "The x-coordinate tells how far LEFT (-) or RIGHT (+) from the origin.",
            "The y-coordinate tells how far DOWN (-) or UP (+) from the origin.",
            "Points on an axis have a 0 in one coordinate.",
        ], "(-5, 3): 5 left, 3 up → Quadrant II."),
        q("Name the quadrant or axis for (8, 2): ____", "fill", "Answer = ____"),
        q("Name the quadrant or axis for (-6, -2): ____", "fill", "Answer = ____"),
        q("Name the quadrant or axis for (0, -7): ____", "fill", "Answer = ____"),
        q("Name the quadrant or axis for (-9, 0): ____", "fill", "Answer = ____"),
        q("Name the quadrant or axis for (4, -5): ____", "fill", "Answer = ____"),
        q("How far right is (6, 3) from the y-axis? ____", "fill", "Answer = ____"),
        q("How far up is (6, 3) from the x-axis? ____", "fill", "Answer = ____"),
        q("How far left is (-4, 7) from the y-axis? ____", "fill", "Answer = ____"),
        q("A point has x = 0 and y = 5. Where is it? ____", "fill", "Answer = ____"),
        q("A point has x = -3 and y = 0. Where is it? ____", "fill", "Answer = ____"),
        q("Both coordinates of a point are positive. Which quadrant? ____", "fill", "Answer = ____"),
        q("Both coordinates are negative. Which quadrant? ____", "fill", "Answer = ____"),
        q("x is negative, y is positive. Which quadrant? ____", "fill", "Answer = ____"),
        q("x is positive, y is negative. Which quadrant? ____", "fill", "Answer = ____"),
        q("Write the coordinates: 2 right, 5 up. ____", "fill", "Answer = ____"),
        q("Write the coordinates: 3 left, 4 down. ____", "fill", "Answer = ____"),
        q("True or False: (0, -7) lies on the y-axis.", "fill", "Answer = ____"),
        q("True or False: (4, -5) is in Quadrant IV.", "fill", "Answer = ____"),
        q("Spot: (-6, -2) is in Quadrant II. Correct? Fix (Quadrant III). ____", "fill", "Answer = ____"),
        q("True or False: A point with both coordinates positive is in Quadrant I.", "fill", "Answer = ____"),
    ]

def _L15A_3():
    return [
        tb("Coordinate Plane — Tips", [
            "Always read (x, y): across first, then up/down.",
            "Sign of x and y tells the quadrant: (+,+) I, (-,+) II, (-,-) III, (+,-) IV.",
            "A 0 in a coordinate means the point sits on an axis.",
            "Origin = (0, 0), where the axes cross.",
        ]),
        q("Quadrant of (12, 9): ____", "fill", "Answer = ____"),
        q("Quadrant of (-7, 11): ____", "fill", "Answer = ____"),
        q("Quadrant of (-8, -3): ____", "fill", "Answer = ____"),
        q("Quadrant of (15, -4): ____", "fill", "Answer = ____"),
        q("Where is (0, 13)? ____", "fill", "Answer = ____"),
        q("Where is (-10, 0)? ____", "fill", "Answer = ____"),
        q("x-coordinate of (-6, 8): ____", "fill", "Answer = ____"),
        q("y-coordinate of (-6, 8): ____", "fill", "Answer = ____"),
        q("A point is 7 left and 2 up. Coordinates? ____", "fill", "Answer = ____"),
        q("A point is 5 right and 9 down. Coordinates? ____", "fill", "Answer = ____"),
        q("In which quadrant are BOTH coordinates the same sign and negative? ____", "fill", "Answer = ____"),
        q("Name a point on the x-axis (any). ____", "fill", "Answer = ____"),
        q("Name a point on the y-axis (any). ____", "fill", "Answer = ____"),
        q("If a point is in Quadrant IV, sign of x? ____", "fill", "Answer = ____"),
        q("If a point is in Quadrant IV, sign of y? ____", "fill", "Answer = ____"),
        q("True or False: (-7, 11) is in Quadrant II.", "fill", "Answer = ____"),
        q("True or False: (15, -4) is in Quadrant III.", "fill", "Answer = ____"),
        q("True or False: (0, 13) is on the y-axis.", "fill", "Answer = ____"),
        q("Spot: x-coordinate of (-6, 8) is 8. Correct? Fix (-6). ____", "fill", "Answer = ____"),
        q("True or False: A point in Quadrant I has positive x and positive y.", "fill", "Answer = ____"),
    ]

def _L15A_4():
    return [
        q("Quadrant of (3, 14): ____", "fill", "Answer = ____"),
        q("Quadrant of (-11, 6): ____", "fill", "Answer = ____"),
        q("Quadrant of (-2, -19): ____", "fill", "Answer = ____"),
        q("Quadrant of (8, -7): ____", "fill", "Answer = ____"),
        q("Where does (0, -5) lie? ____", "fill", "Answer = ____"),
        q("Where does (16, 0) lie? ____", "fill", "Answer = ____"),
        q("A point is reflected over the x-axis: (4, 5) → ____", "fill", "Answer = ____"),
        q("A point is reflected over the y-axis: (4, 5) → ____", "fill", "Answer = ____"),
        q("Reflect (−3, 7) over the x-axis → ____", "fill", "Answer = ____"),
        q("Reflect (−3, 7) over the y-axis → ____", "fill", "Answer = ____"),
        q("Point P(2, 3) moves 4 right. New point? ____", "fill", "Answer = ____"),
        q("Point P(2, 3) moves 5 up. New point? ____", "fill", "Answer = ____"),
        q("Point P(7, 2) moves 3 down. New point? ____", "fill", "Answer = ____"),
        q("Distance of (0, 6) from the origin along the axis: ____", "fill", "Answer = ____"),
        q("Distance of (9, 0) from the origin along the axis: ____", "fill", "Answer = ____"),
        q("True or False: Reflecting (4, 5) over the x-axis gives (4, -5).", "fill", "Answer = ____"),
        q("True or False: Reflecting (4, 5) over the y-axis gives (-4, 5).", "fill", "Answer = ____"),
        q("True or False: (-2, -19) is in Quadrant III.", "fill", "Answer = ____"),
        q("Spot: Reflect (-3, 7) over x-axis = (3, 7). Correct? Fix ((-3, -7)). ____", "fill", "Answer = ____"),
        q("True or False: Moving (2, 3) right by 4 gives (6, 3).", "fill", "Answer = ____"),
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# 15B — Plotting points
# ═══════════════════════════════════════════════════════════════════════════════
def _L15B_1():
    return [
        cb("Plotting a Point", [
            "Start at the origin (0, 0).",
            "Move along the x-axis by the x-value (right if +, left if -).",
            "Then move parallel to the y-axis by the y-value (up if +, down if -).",
        ], "Plot (4, 3): 4 right, then 3 up."),
        cb("Points That Form Shapes", [
            "Joining plotted points in order can form lines and shapes.",
            "Same y-value → points lie on a horizontal line.",
            "Same x-value → points lie on a vertical line.",
        ], "(1, 2), (5, 2) share y = 2 → horizontal line."),
        q("To plot (6, 2): first move ____ units right.", "fill", "Answer = ____"),
        q("To plot (6, 2): then move ____ units up.", "fill", "Answer = ____"),
        q("To plot (-3, 4): first move 3 units in which direction? ____", "fill", "Answer = ____"),
        q("To plot (5, -2): the final move is 2 units in which direction? ____", "fill", "Answer = ____"),
        q("Points (2, 5) and (8, 5): horizontal or vertical line? ____", "fill", "Answer = ____"),
        q("Points (3, 1) and (3, 7): horizontal or vertical line? ____", "fill", "Answer = ____"),
        q("(0, 0), (4, 0), (4, 3), (0, 3) form what shape? ____", "fill", "Answer = ____"),
        q("(1, 1), (5, 1), (5, 5), (1, 5) form what shape? ____", "fill", "Answer = ____"),
        q("Plot (0, 5): it lies on which axis? ____", "fill", "Answer = ____"),
        q("Plot (-4, 0): it lies on which axis? ____", "fill", "Answer = ____"),
        q("A point 3 right and 0 up from origin is: ____", "fill", "Answer = ____"),
        q("A point 0 right and -6 down from origin is: ____", "fill", "Answer = ____"),
        q("Which point is further right: (2, 9) or (7, 1)? ____", "fill", "Answer = ____"),
        q("Which point is higher: (2, 9) or (7, 1)? ____", "fill", "Answer = ____"),
        q("True or False: To plot (4, 3), you move up first.", "fill", "Answer = ____"),
        q("True or False: (2, 5) and (8, 5) lie on a horizontal line.", "fill", "Answer = ____"),
        q("True or False: (3, 1) and (3, 7) lie on a vertical line.", "fill", "Answer = ____"),
        q("Spot: (0, 5) lies on the x-axis. Correct? Fix (y-axis). ____", "fill", "Answer = ____"),
        q("True or False: Four points forming equal sides and right angles make a square.", "fill", "Answer = ____"),
    ]

def _L15B_2():
    return [
        cb("Naming and Locating Points", [
            "Each point has exactly one (x, y) name.",
            "Reading a grid: count across (x), then up/down (y).",
            "Shapes are described by listing their corner points (vertices).",
        ], "A triangle with vertices (0,0), (4,0), (0,3)."),
        q("Vertices (0,0), (6,0), (6,4), (0,4): what shape? ____", "fill", "Answer = ____"),
        q("The shape (0,0), (6,0), (6,4), (0,4): length of bottom side? ____", "fill", "Answer = ____"),
        q("The shape (0,0), (6,0), (6,4), (0,4): length of left side? ____", "fill", "Answer = ____"),
        q("Rectangle (0,0),(6,0),(6,4),(0,4): area = length × width = ____", "fill", "Answer = ____"),
        q("Rectangle (0,0),(6,0),(6,4),(0,4): perimeter = ____", "fill", "Answer = ____"),
        q("Points (2,3),(2,8): length of this vertical segment? ____", "fill", "Answer = ____"),
        q("Points (1,5),(9,5): length of this horizontal segment? ____", "fill", "Answer = ____"),
        q("Square with corner (0,0) and side 5 along axes: opposite corner? ____", "fill", "Answer = ____"),
        q("Triangle (0,0),(8,0),(0,6): length of base on x-axis? ____", "fill", "Answer = ____"),
        q("Triangle (0,0),(8,0),(0,6): height along y-axis? ____", "fill", "Answer = ____"),
        q("Triangle (0,0),(8,0),(0,6): area = ½ × base × height = ____", "fill", "Answer = ____"),
        q("Which point is on the x-axis: (0,4) or (4,0)? ____", "fill", "Answer = ____"),
        q("Which point is on the y-axis: (0,4) or (4,0)? ____", "fill", "Answer = ____"),
        q("Move (3,3) up 4 then right 2: new point? ____", "fill", "Answer = ____"),
        q("Move (5,5) down 5 then left 5: new point? ____", "fill", "Answer = ____"),
        q("True or False: Rectangle (0,0),(6,0),(6,4),(0,4) has area 24.", "fill", "Answer = ____"),
        q("True or False: The segment (2,3) to (2,8) has length 5.", "fill", "Answer = ____"),
        q("True or False: Triangle (0,0),(8,0),(0,6) has area 24.", "fill", "Answer = ____"),
        q("Spot: Perimeter of rectangle 6 by 4 = 24. Correct? Fix (20). ____", "fill", "Answer = ____"),
        q("True or False: The horizontal segment (1,5) to (9,5) has length 8.", "fill", "Answer = ____"),
    ]

def _L15B_3():
    return [
        tb("Plotting Points — Tips", [
            "Across then up: (x, y).",
            "Same y → horizontal line; length = difference of x's.",
            "Same x → vertical line; length = difference of y's.",
            "Rectangle area = length × width; triangle area = ½ × base × height.",
        ]),
        q("Length of segment (3,2) to (3,11): ____", "fill", "Answer = ____"),
        q("Length of segment (4,7) to (10,7): ____", "fill", "Answer = ____"),
        q("Rectangle (0,0),(9,0),(9,5),(0,5): area = ____", "fill", "Answer = ____"),
        q("Rectangle (0,0),(9,0),(9,5),(0,5): perimeter = ____", "fill", "Answer = ____"),
        q("Triangle (0,0),(10,0),(0,4): area = ____", "fill", "Answer = ____"),
        q("Square side 7 from (0,0) along axes: opposite corner? ____", "fill", "Answer = ____"),
        q("Square side 7: area = ____", "fill", "Answer = ____"),
        q("Square side 7: perimeter = ____", "fill", "Answer = ____"),
        q("Vertices (2,2),(2,9),(7,9),(7,2): what shape? ____", "fill", "Answer = ____"),
        q("Shape (2,2),(2,9),(7,9),(7,2): width? ____", "fill", "Answer = ____"),
        q("Shape (2,2),(2,9),(7,9),(7,2): height? ____", "fill", "Answer = ____"),
        q("Shape (2,2),(2,9),(7,9),(7,2): area? ____", "fill", "Answer = ____"),
        q("Point (6,1) moves up 8: new point? ____", "fill", "Answer = ____"),
        q("Point (6,1) moves left 6: new point? ____", "fill", "Answer = ____"),
        q("Midpoint of horizontal segment (2,5) to (8,5) has x = ____", "fill", "Answer = ____"),
        q("True or False: Segment (3,2) to (3,11) has length 9.", "fill", "Answer = ____"),
        q("True or False: Square of side 7 has area 49.", "fill", "Answer = ____"),
        q("True or False: Triangle (0,0),(10,0),(0,4) has area 20.", "fill", "Answer = ____"),
        q("Spot: Rectangle 9 by 5 perimeter = 45. Correct? Fix (28). ____", "fill", "Answer = ____"),
        q("True or False: Shape (2,2),(2,9),(7,9),(7,2) has area 35.", "fill", "Answer = ____"),
    ]

def _L15B_4():
    return [
        q("Length of (5,3) to (5,17): ____", "fill", "Answer = ____"),
        q("Length of (2,8) to (14,8): ____", "fill", "Answer = ____"),
        q("Rectangle (0,0),(12,0),(12,7),(0,7): area = ____", "fill", "Answer = ____"),
        q("Rectangle (0,0),(12,0),(12,7),(0,7): perimeter = ____", "fill", "Answer = ____"),
        q("Triangle (0,0),(14,0),(0,10): area = ____", "fill", "Answer = ____"),
        q("Three corners of a rectangle: (1,1),(7,1),(7,4). Fourth corner? ____", "fill", "Answer = ____"),
        q("Three corners of a rectangle: (2,3),(2,9),(6,9). Fourth corner? ____", "fill", "Answer = ____"),
        q("Square (0,0),(a,0),(a,a),(0,a) has area 64. a = ____", "fill", "Answer = ____"),
        q("A rectangle has corners (0,0) and (8,5) opposite. Other two corners? ____", "fill", "Answer = ____"),
        q("Points (1,2),(1,2): distance between them = ____", "fill", "Answer = ____"),
        q("Translate triangle (0,0),(3,0),(0,3) right by 5: new vertices? ____", "fill", "Answer = ____"),
        q("Translate (4,4) by (−2, +3): new point? ____", "fill", "Answer = ____"),
        q("Perimeter of square with vertices (0,0),(6,0),(6,6),(0,6): ____", "fill", "Answer = ____"),
        q("A horizontal line passes through (3,7) and (11,7). Its length: ____", "fill", "Answer = ____"),
        q("Midpoint x of segment (4,0) to (16,0): ____", "fill", "Answer = ____"),
        q("True or False: Rectangle 12 by 7 has area 84.", "fill", "Answer = ____"),
        q("True or False: Triangle (0,0),(14,0),(0,10) has area 70.", "fill", "Answer = ____"),
        q("True or False: Fourth corner of rectangle (1,1),(7,1),(7,4) is (1,4).", "fill", "Answer = ____"),
        q("Spot: Square of area 64 has side 8. Correct? ____", "fill", "Answer = ____"),
        q("True or False: Translating (4,4) by (-2,+3) gives (2,7).", "fill", "Answer = ____"),
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# 15C — Distance formula
# ═══════════════════════════════════════════════════════════════════════════════
def _L15C_1():
    return [
        cb("The Distance Formula", [
            "Distance between (x1, y1) and (x2, y2) = √[(x2-x1)² + (y2-y1)²].",
            "It comes from the Pythagoras theorem on the coordinate grid.",
            "Horizontal gap = x2-x1, vertical gap = y2-y1.",
        ], "Distance (0,0) to (3,4) = √(9+16) = √25 = 5."),
        cb("Special Easy Cases", [
            "Same y: distance = |x2 - x1| (horizontal).",
            "Same x: distance = |y2 - y1| (vertical).",
            "From origin: distance to (x, y) = √(x² + y²).",
        ], "(0,0) to (6,8): √(36+64) = √100 = 10."),
        q("Distance (0,0) to (3,4) = √(9+16) = ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (6,8) = √(36+64) = ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (5,12) = √(25+144) = ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (8,15) = √(64+225) = ____", "fill", "Answer = ____"),
        q("Distance (1,2) to (4,2) (same y) = ____", "fill", "Answer = ____"),
        q("Distance (3,1) to (3,9) (same x) = ____", "fill", "Answer = ____"),
        q("Distance (2,3) to (5,7): horizontal gap = ____", "fill", "Answer = ____"),
        q("Distance (2,3) to (5,7): vertical gap = ____", "fill", "Answer = ____"),
        q("Distance (2,3) to (5,7) = √(9+16) = ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (9,12) = √(81+144) = ____", "fill", "Answer = ____"),
        q("√25 = ____", "fill", "Answer = ____"),
        q("√100 = ____", "fill", "Answer = ____"),
        q("√169 = ____", "fill", "Answer = ____"),
        q("The distance formula comes from which theorem? ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (7,24) = √(49+576) = ____", "fill", "Answer = ____"),
        q("True or False: Distance (0,0) to (3,4) is 5.", "fill", "Answer = ____"),
        q("True or False: Same y-values means a horizontal distance.", "fill", "Answer = ____"),
        q("True or False: Distance (3,1) to (3,9) is 8.", "fill", "Answer = ____"),
        q("Spot: Distance (0,0) to (6,8) = √100 = 14. Correct? Fix (10). ____", "fill", "Answer = ____"),
        q("True or False: √169 = 13.", "fill", "Answer = ____"),
    ]

def _L15C_2():
    return [
        cb("Applying the Distance Formula", [
            "Subtract coordinates, square each, add, take the square root.",
            "Order of subtraction does not matter (it gets squared).",
            "Leave the answer as √n if it is not a perfect square.",
        ], "(1,1) to (4,5): √(9+16) = √25 = 5."),
        q("Distance (1,1) to (4,5) = √(9+16) = ____", "fill", "Answer = ____"),
        q("Distance (2,1) to (5,5) = √(9+16) = ____", "fill", "Answer = ____"),
        q("Distance (-1,-1) to (2,3) = √(9+16) = ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (1,1) = √(1+1) = √2 ≈ ____ (leave as √2)", "fill", "Answer = ____"),
        q("Distance (0,0) to (2,2) = √(4+4) = √8 = 2√2. Simplify form: ____", "fill", "Answer = ____"),
        q("Distance (3,4) to (6,8) = √(9+16) = ____", "fill", "Answer = ____"),
        q("Distance (-2,3) to (1,7) = √(9+16) = ____", "fill", "Answer = ____"),
        q("Distance (5,5) to (5,12) (same x) = ____", "fill", "Answer = ____"),
        q("Distance (2,4) to (10,4) (same y) = ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (10,24) = √(100+576) = ____", "fill", "Answer = ____"),
        q("Distance (1,2) to (1,2) = ____", "fill", "Answer = ____"),
        q("Distance (-3,-4) to (0,0) = √(9+16) = ____", "fill", "Answer = ____"),
        q("Distance (6,0) to (0,8) = √(36+64) = ____", "fill", "Answer = ____"),
        q("Is (0,0),(3,4),(6,0) isosceles? Distance (0,0)-(3,4)=5, (6,0)-(3,4)=5. ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (20,21) = √(400+441) = ____", "fill", "Answer = ____"),
        q("True or False: Distance (1,1) to (4,5) is 5.", "fill", "Answer = ____"),
        q("True or False: Distance (5,5) to (5,12) is 7.", "fill", "Answer = ____"),
        q("True or False: Distance from a point to itself is 0.", "fill", "Answer = ____"),
        q("Spot: Distance (6,0) to (0,8) = √100 = 12. Correct? Fix (10). ____", "fill", "Answer = ____"),
        q("True or False: √(400+441) = 29.", "fill", "Answer = ____"),
    ]

def _L15C_3():
    return [
        tb("Distance Formula — Tips", [
            "d = √[(x2-x1)² + (y2-y1)²].",
            "Memorise Pythagorean triples: 3-4-5, 5-12-13, 8-15-17, 7-24-25, 20-21-29.",
            "Same x or same y → just subtract the differing coordinate.",
            "Not a perfect square? Leave as a simplified surd.",
        ]),
        q("Distance (0,0) to (9,12): ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (8,15): ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (7,24): ____", "fill", "Answer = ____"),
        q("Distance (2,2) to (5,6): ____", "fill", "Answer = ____"),
        q("Distance (-3,2) to (1,5): ____", "fill", "Answer = ____"),
        q("Distance (4,4) to (4,16): ____", "fill", "Answer = ____"),
        q("Distance (3,7) to (15,7): ____", "fill", "Answer = ____"),
        q("Distance (1,1) to (1,1): ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (10,10) = √200 = 10√2. Coefficient outside root? ____", "fill", "Answer = ____"),
        q("Distance (6,8) to (0,0): ____", "fill", "Answer = ____"),
        q("Distance (-5,0) to (0,12): ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (40,42): ____", "fill", "Answer = ____"),
        q("Distance (5,12) to (0,0): ____", "fill", "Answer = ____"),
        q("Triangle (0,0),(5,0),(0,12): hypotenuse length? ____", "fill", "Answer = ____"),
        q("Two points 5 apart on the same horizontal line, one at (2,3). Other (x>2)? ____", "fill", "Answer = ____"),
        q("True or False: 5-12-13 is a Pythagorean triple.", "fill", "Answer = ____"),
        q("True or False: Distance (0,0) to (7,24) is 25.", "fill", "Answer = ____"),
        q("True or False: √200 = 10√2.", "fill", "Answer = ____"),
        q("Spot: Distance (0,0) to (8,15) = 16. Correct? Fix (17). ____", "fill", "Answer = ____"),
        q("True or False: Distance (4,4) to (4,16) is 12.", "fill", "Answer = ____"),
    ]

def _L15C_4():
    return [
        q("Distance (1,2) to (7,10): ____", "fill", "Answer = ____"),
        q("Distance (-2,-3) to (3,9): ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (11,60): ____", "fill", "Answer = ____"),
        q("Distance (2,5) to (2,5): ____", "fill", "Answer = ____"),
        q("Distance (9,0) to (0,40): ____", "fill", "Answer = ____"),
        q("Is triangle (0,0),(6,0),(3,4) isosceles? (sides 5,5,6) ____", "fill", "Answer = ____"),
        q("Is (0,0),(4,0),(4,3),(0,3) a rectangle? (use distances) ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (12,16): ____", "fill", "Answer = ____"),
        q("Distance (-6,-8) to (0,0): ____", "fill", "Answer = ____"),
        q("Show (0,0),(3,4),(8,4),(5,0) is a rhombus: all sides = ____", "fill", "Answer = ____"),
        q("A circle has centre (0,0) and passes through (3,4). Radius = ____", "fill", "Answer = ____"),
        q("A circle has centre (0,0) and passes through (5,12). Radius = ____", "fill", "Answer = ____"),
        q("Point on x-axis equidistant... distance (0,0) to (9,12) = ____", "fill", "Answer = ____"),
        q("Distance (1,1) to (4,5) plus distance (4,5) to (4,5) = ____", "fill", "Answer = ____"),
        q("Perimeter of triangle (0,0),(3,4),(0,8): sides 5, 5, 8. Perimeter = ____", "fill", "Answer = ____"),
        q("True or False: Distance (0,0) to (11,60) is 61.", "fill", "Answer = ____"),
        q("True or False: A circle centre (0,0) through (3,4) has radius 5.", "fill", "Answer = ____"),
        q("True or False: Triangle (0,0),(6,0),(3,4) is isosceles.", "fill", "Answer = ____"),
        q("Spot: Distance (9,0) to (0,40) = 40. Correct? Fix (41). ____", "fill", "Answer = ____"),
        q("True or False: Perimeter of triangle with sides 5,5,8 is 18.", "fill", "Answer = ____"),
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# 15D — Midpoint formula
# ═══════════════════════════════════════════════════════════════════════════════
def _L15D_1():
    return [
        cb("The Midpoint Formula", [
            "Midpoint of (x1, y1) and (x2, y2) = ((x1+x2)/2, (y1+y2)/2).",
            "It is the average of the x-coordinates and the average of the y-coordinates.",
            "The midpoint is exactly halfway between the two points.",
        ], "Midpoint of (2,4) and (6,8) = ((2+6)/2, (4+8)/2) = (4, 6)."),
        q("Midpoint of (0,0) and (4,6) = ____", "fill", "Answer = ____"),
        q("Midpoint of (2,4) and (6,8) = ____", "fill", "Answer = ____"),
        q("Midpoint of (1,1) and (5,5) = ____", "fill", "Answer = ____"),
        q("Midpoint of (0,0) and (10,0) = ____", "fill", "Answer = ____"),
        q("Midpoint of (0,0) and (0,12) = ____", "fill", "Answer = ____"),
        q("Midpoint of (3,5) and (7,5) = ____", "fill", "Answer = ____"),
        q("Midpoint of (-2,4) and (6,8) = ____", "fill", "Answer = ____"),
        q("Midpoint of (-4,-2) and (4,2) = ____", "fill", "Answer = ____"),
        q("Average of x-values 2 and 8 = ____", "fill", "Answer = ____"),
        q("Average of y-values 3 and 11 = ____", "fill", "Answer = ____"),
        q("Midpoint of (2,3) and (8,11) = ____", "fill", "Answer = ____"),
        q("Midpoint of (1,2) and (3,4) = ____", "fill", "Answer = ____"),
        q("Midpoint of (0,0) and (6,6) = ____", "fill", "Answer = ____"),
        q("Midpoint of (5,5) and (5,5) = ____", "fill", "Answer = ____"),
        q("Midpoint of (-6,0) and (6,0) = ____", "fill", "Answer = ____"),
        q("True or False: Midpoint of (2,4),(6,8) is (4,6).", "fill", "Answer = ____"),
        q("True or False: The midpoint averages the coordinates.", "fill", "Answer = ____"),
        q("True or False: Midpoint of (0,0),(10,0) is (5,0).", "fill", "Answer = ____"),
        q("Spot: Midpoint of (1,1),(5,5) = (6,6). Correct? Fix (3,3). ____", "fill", "Answer = ____"),
        q("True or False: Midpoint of (-4,-2),(4,2) is the origin.", "fill", "Answer = ____"),
    ]

def _L15D_2():
    return [
        cb("Finding an Endpoint", [
            "If you know the midpoint M and one endpoint A, the other endpoint B satisfies M = midpoint(A, B).",
            "So x_B = 2·x_M - x_A and y_B = 2·y_M - y_A.",
            "Double the midpoint, subtract the known endpoint.",
        ], "M(4,6), A(2,4): B = (2·4-2, 2·6-4) = (6, 8)."),
        q("Midpoint of (3,2) and (9,10) = ____", "fill", "Answer = ____"),
        q("Midpoint of (-5,3) and (5,9) = ____", "fill", "Answer = ____"),
        q("M(4,6), A(2,4). Find B: ____", "fill", "Answer = ____"),
        q("M(5,5), A(2,3). Find B: ____", "fill", "Answer = ____"),
        q("M(0,0), A(3,4). Find B: ____", "fill", "Answer = ____"),
        q("M(3,3), A(1,1). Find B: ____", "fill", "Answer = ____"),
        q("Midpoint of (2,7) and (10,7) = ____", "fill", "Answer = ____"),
        q("Midpoint of (4,1) and (4,9) = ____", "fill", "Answer = ____"),
        q("Diameter ends (0,0) and (6,8). Centre (midpoint) = ____", "fill", "Answer = ____"),
        q("Diameter ends (-3,-4) and (3,4). Centre = ____", "fill", "Answer = ____"),
        q("M(6,4), A(10,6). Find B: ____", "fill", "Answer = ____"),
        q("Midpoint of (1,1) and (7,1) = ____", "fill", "Answer = ____"),
        q("Midpoint of (-2,-2) and (-8,-8) = ____", "fill", "Answer = ____"),
        q("M(2,2), A(0,0). Find B: ____", "fill", "Answer = ____"),
        q("Midpoint of (3,8) and (9,2) = ____", "fill", "Answer = ____"),
        q("True or False: M(4,6),A(2,4) gives B=(6,8).", "fill", "Answer = ____"),
        q("True or False: Centre of circle = midpoint of a diameter.", "fill", "Answer = ____"),
        q("True or False: Midpoint of (2,7),(10,7) is (6,7).", "fill", "Answer = ____"),
        q("Spot: M(5,5),A(2,3) gives B=(8,7). Correct? ____", "fill", "Answer = ____"),
        q("True or False: Midpoint of (-2,-2),(-8,-8) is (-5,-5).", "fill", "Answer = ____"),
    ]

def _L15D_3():
    return [
        tb("Midpoint Formula — Tips", [
            "M = ((x1+x2)/2, (y1+y2)/2): average each coordinate.",
            "Endpoint from midpoint: B = (2x_M - x_A, 2y_M - y_A).",
            "Centre of a circle = midpoint of any diameter.",
            "Midpoint of a segment splits it into two equal halves.",
        ]),
        q("Midpoint of (4,8) and (10,2): ____", "fill", "Answer = ____"),
        q("Midpoint of (-6,5) and (2,-3): ____", "fill", "Answer = ____"),
        q("Midpoint of (0,0) and (14,20): ____", "fill", "Answer = ____"),
        q("M(7,7), A(3,5). Find B: ____", "fill", "Answer = ____"),
        q("M(0,0), A(-4,6). Find B: ____", "fill", "Answer = ____"),
        q("Diameter ends (2,3),(8,9). Centre: ____", "fill", "Answer = ____"),
        q("Midpoint of (5,0) and (5,14): ____", "fill", "Answer = ____"),
        q("Midpoint of (1,6) and (11,6): ____", "fill", "Answer = ____"),
        q("M(3,4), A(0,0). Find B: ____", "fill", "Answer = ____"),
        q("Midpoint of (-7,-1) and (3,9): ____", "fill", "Answer = ____"),
        q("Midpoint of (8,8) and (2,2): ____", "fill", "Answer = ____"),
        q("M(6,6), A(8,10). Find B: ____", "fill", "Answer = ____"),
        q("Midpoint of (10,4) and (0,4): ____", "fill", "Answer = ____"),
        q("Midpoint of (4,4) and (4,4): ____", "fill", "Answer = ____"),
        q("Diameter (0,6),(0,-6). Centre: ____", "fill", "Answer = ____"),
        q("True or False: Midpoint of (4,8),(10,2) is (7,5).", "fill", "Answer = ____"),
        q("True or False: M(7,7),A(3,5) gives B=(11,9).", "fill", "Answer = ____"),
        q("True or False: Midpoint of (0,0),(14,20) is (7,10).", "fill", "Answer = ____"),
        q("Spot: Midpoint of (-6,5),(2,-3) = (-2,1). Correct? ____", "fill", "Answer = ____"),
        q("True or False: Centre of diameter (2,3),(8,9) is (5,6).", "fill", "Answer = ____"),
    ]

def _L15D_4():
    return [
        q("Midpoint of (3,7) and (15,1): ____", "fill", "Answer = ____"),
        q("Midpoint of (-8,4) and (4,-10): ____", "fill", "Answer = ____"),
        q("M(5,9), A(1,3). Find B: ____", "fill", "Answer = ____"),
        q("M(0,0), A(7,-7). Find B: ____", "fill", "Answer = ____"),
        q("Vertices (0,0),(6,0),(6,4),(0,4). Midpoint of diagonal (0,0)-(6,4): ____", "fill", "Answer = ____"),
        q("Diagonals of a rectangle bisect each other. Other diagonal (6,0)-(0,4) midpoint: ____", "fill", "Answer = ____"),
        q("Triangle (0,0),(8,0),(0,6). Midpoint of hypotenuse: ____", "fill", "Answer = ____"),
        q("Midpoint of (2,2) and (2,2): ____", "fill", "Answer = ____"),
        q("Three collinear points: A(0,0), M(3,4), is M midpoint of A and (6,8)? ____", "fill", "Answer = ____"),
        q("Midpoint of (−5,−5) and (5,5): ____", "fill", "Answer = ____"),
        q("M(4,3) is midpoint of (1,1) and B. B = ____", "fill", "Answer = ____"),
        q("Midpoint of (12,0) and (0,16): ____", "fill", "Answer = ____"),
        q("A(2,5), B(8,5), C(8,11), D(2,11). Centre (midpoint of A-C): ____", "fill", "Answer = ____"),
        q("Midpoint of (9,9) and (1,1): ____", "fill", "Answer = ____"),
        q("M(0,0) is midpoint of (-3,-4) and B. B = ____", "fill", "Answer = ____"),
        q("True or False: Midpoint of (3,7),(15,1) is (9,4).", "fill", "Answer = ____"),
        q("True or False: M(5,9),A(1,3) gives B=(9,15).", "fill", "Answer = ____"),
        q("True or False: Diagonals of a rectangle share the same midpoint.", "fill", "Answer = ____"),
        q("Spot: Midpoint of (-8,4),(4,-10) = (-2,-3). Correct? ____", "fill", "Answer = ____"),
        q("True or False: M(0,0) midpoint of (-3,-4) and (3,4).", "fill", "Answer = ____"),
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# 15E — Section concept (section formula / ratio division)
# ═══════════════════════════════════════════════════════════════════════════════
def _L15E_1():
    return [
        cb("Section Formula (Internal Division)", [
            "A point P divides the join of A(x1,y1) and B(x2,y2) in ratio m:n.",
            "P = ((m·x2 + n·x1)/(m+n), (m·y2 + n·y1)/(m+n)).",
            "Ratio 1:1 gives the midpoint.",
        ], "A(0,0), B(6,0), ratio 1:2 → P = ((1·6+2·0)/3, 0) = (2, 0)."),
        cb("Why It Works", [
            "The point is a weighted average, closer to whichever end has the bigger opposite weight.",
            "m:n means P is m parts from A toward B out of m+n total.",
        ], "Ratio 2:1 from A(0,0) to B(3,0): P=(2,0), two-thirds of the way."),
        q("Midpoint = section formula with ratio ____ : ____", "fill", "Answer = ____"),
        q("A(0,0), B(6,0), ratio 1:1 → P = ____", "fill", "Answer = ____"),
        q("A(0,0), B(6,0), ratio 1:2 → P = ____", "fill", "Answer = ____"),
        q("A(0,0), B(6,0), ratio 2:1 → P = ____", "fill", "Answer = ____"),
        q("A(0,0), B(0,9), ratio 1:2 → P = ____", "fill", "Answer = ____"),
        q("A(0,0), B(0,9), ratio 2:1 → P = ____", "fill", "Answer = ____"),
        q("A(0,0), B(8,0), ratio 3:1 → P = ____", "fill", "Answer = ____"),
        q("A(0,0), B(8,0), ratio 1:3 → P = ____", "fill", "Answer = ____"),
        q("A(2,0), B(8,0), ratio 1:1 → P = ____", "fill", "Answer = ____"),
        q("A(0,0), B(10,0), ratio 2:3 → P = ____", "fill", "Answer = ____"),
        q("A(0,0), B(10,0), ratio 3:2 → P = ____", "fill", "Answer = ____"),
        q("Ratio m:n means P is m parts out of ____ total from A.", "fill", "Answer = ____"),
        q("A(0,0), B(12,0), ratio 1:5 → P = ____", "fill", "Answer = ____"),
        q("A(0,0), B(12,0), ratio 5:1 → P = ____", "fill", "Answer = ____"),
        q("True or False: Ratio 1:1 gives the midpoint.", "fill", "Answer = ____"),
        q("True or False: A(0,0),B(6,0) at 1:2 gives (2,0).", "fill", "Answer = ____"),
        q("True or False: A(0,0),B(6,0) at 2:1 gives (4,0).", "fill", "Answer = ____"),
        q("Spot: A(0,0),B(8,0) at 3:1 gives (2,0). Correct? Fix (6,0). ____", "fill", "Answer = ____"),
        q("True or False: A point dividing 2:3 is closer to A than to B.", "fill", "Answer = ____"),
    ]

def _L15E_2():
    return [
        cb("Applying the Section Formula", [
            "P = ((m·x2 + n·x1)/(m+n), (m·y2 + n·y1)/(m+n)) for ratio m:n from A to B.",
            "Plug in carefully; m multiplies the FAR point B, n multiplies the NEAR point A.",
            "Check with the midpoint case (1:1) to be sure of your setup.",
        ], "A(1,2), B(7,8), ratio 1:1 → midpoint (4,5)."),
        q("A(1,2), B(7,8), ratio 1:1 → P = ____", "fill", "Answer = ____"),
        q("A(2,3), B(8,9), ratio 1:2 → P = ____", "fill", "Answer = ____"),
        q("A(2,3), B(8,9), ratio 2:1 → P = ____", "fill", "Answer = ____"),
        q("A(0,0), B(9,6), ratio 1:2 → P = ____", "fill", "Answer = ____"),
        q("A(0,0), B(9,6), ratio 2:1 → P = ____", "fill", "Answer = ____"),
        q("A(1,1), B(7,7), ratio 1:2 → P = ____", "fill", "Answer = ____"),
        q("A(1,1), B(7,7), ratio 2:1 → P = ____", "fill", "Answer = ____"),
        q("A(-2,0), B(4,0), ratio 1:1 → P = ____", "fill", "Answer = ____"),
        q("A(0,3), B(0,15), ratio 1:3 → P = ____", "fill", "Answer = ____"),
        q("A(0,3), B(0,15), ratio 3:1 → P = ____", "fill", "Answer = ____"),
        q("A(3,3), B(9,9), ratio 1:1 → P = ____", "fill", "Answer = ____"),
        q("A(0,0), B(6,12), ratio 1:2 → P = ____", "fill", "Answer = ____"),
        q("A(0,0), B(6,12), ratio 2:1 → P = ____", "fill", "Answer = ____"),
        q("A point divides (0,0),(15,0) so it is at (5,0). Ratio (from A)? ____", "fill", "Answer = ____"),
        q("A point divides (0,0),(15,0) so it is at (10,0). Ratio (from A)? ____", "fill", "Answer = ____"),
        q("True or False: A(2,3),B(8,9) at 1:2 gives (4,5).", "fill", "Answer = ____"),
        q("True or False: A(2,3),B(8,9) at 2:1 gives (6,7).", "fill", "Answer = ____"),
        q("True or False: Ratio 1:1 always gives the midpoint.", "fill", "Answer = ____"),
        q("Spot: A(0,0),B(9,6) at 2:1 gives (3,2). Correct? Fix (6,4). ____", "fill", "Answer = ____"),
        q("True or False: A point at (5,0) on (0,0)-(15,0) divides it 1:2.", "fill", "Answer = ____"),
    ]

def _L15E_3():
    return [
        tb("Section Formula — Tips", [
            "P = ((m·x2 + n·x1)/(m+n), (m·y2 + n·y1)/(m+n)) for A:B = m:n.",
            "m pairs with the second point B, n with the first point A.",
            "1:1 = midpoint — use it as a quick self-check.",
            "Ratio m:n: P is m/(m+n) of the way from A to B.",
        ]),
        q("A(0,0), B(12,0), 1:3 → P: ____", "fill", "Answer = ____"),
        q("A(0,0), B(12,0), 3:1 → P: ____", "fill", "Answer = ____"),
        q("A(2,2), B(8,8), 1:2 → P: ____", "fill", "Answer = ____"),
        q("A(2,2), B(8,8), 2:1 → P: ____", "fill", "Answer = ____"),
        q("A(1,4), B(7,4), 1:1 → P: ____", "fill", "Answer = ____"),
        q("A(0,0), B(20,10), 2:3 → P: ____", "fill", "Answer = ____"),
        q("A(0,0), B(20,10), 3:2 → P: ____", "fill", "Answer = ____"),
        q("A(0,0), B(0,16), 3:1 → P: ____", "fill", "Answer = ____"),
        q("A(-4,-4), B(4,4), 1:1 → P: ____", "fill", "Answer = ____"),
        q("A(0,0), B(18,0), 1:2 → P: ____", "fill", "Answer = ____"),
        q("A(0,0), B(18,0), 2:1 → P: ____", "fill", "Answer = ____"),
        q("P at (4,0) divides (0,0),(12,0) in ratio (from A): ____", "fill", "Answer = ____"),
        q("P at (8,0) divides (0,0),(12,0) in ratio (from A): ____", "fill", "Answer = ____"),
        q("A(3,0), B(15,0), 1:1 → P: ____", "fill", "Answer = ____"),
        q("Two-thirds from A(0,0) to B(9,0) means ratio 2:1 → P: ____", "fill", "Answer = ____"),
        q("True or False: A(2,2),B(8,8) at 1:2 gives (4,4).", "fill", "Answer = ____"),
        q("True or False: A(0,0),B(12,0) at 3:1 gives (9,0).", "fill", "Answer = ____"),
        q("True or False: m pairs with the second point in the section formula.", "fill", "Answer = ____"),
        q("Spot: A(0,0),B(20,10) at 2:3 gives (8,4). Correct? ____", "fill", "Answer = ____"),
        q("True or False: P at (8,0) on (0,0)-(12,0) divides 2:1.", "fill", "Answer = ____"),
    ]

def _L15E_4():
    return [
        q("A(1,1), B(10,10), 1:2 → P: ____", "fill", "Answer = ____"),
        q("A(1,1), B(10,10), 2:1 → P: ____", "fill", "Answer = ____"),
        q("A(0,0), B(21,14), 4:3 → P: ____", "fill", "Answer = ____"),
        q("A(2,5), B(2,17), 1:3 → P: ____", "fill", "Answer = ____"),
        q("A(-6,0), B(6,0), 1:2 → P: ____", "fill", "Answer = ____"),
        q("Trisection: A(0,0),B(9,9) first point (1:2): ____", "fill", "Answer = ____"),
        q("Trisection: A(0,0),B(9,9) second point (2:1): ____", "fill", "Answer = ____"),
        q("P at (6,0) divides (0,0),(9,0) in ratio (from A): ____", "fill", "Answer = ____"),
        q("Centroid-style: midpoint of (0,0),(6,0) then to (3,9)... midpoint of (0,0),(6,0): ____", "fill", "Answer = ____"),
        q("A(0,0), B(30,0), 1:5 → P: ____", "fill", "Answer = ____"),
        q("A(0,0), B(30,0), 5:1 → P: ____", "fill", "Answer = ____"),
        q("A(4,4), B(16,16), 1:1 → P: ____", "fill", "Answer = ____"),
        q("A(0,0), B(8,12), 3:1 → P: ____", "fill", "Answer = ____"),
        q("A(0,0), B(8,12), 1:3 → P: ____", "fill", "Answer = ____"),
        q("A point three-quarters from A(0,0) to B(8,0) is ratio 3:1 → P: ____", "fill", "Answer = ____"),
        q("True or False: A(1,1),B(10,10) at 1:2 gives (4,4).", "fill", "Answer = ____"),
        q("True or False: A(0,0),B(21,14) at 4:3 gives (12,8).", "fill", "Answer = ____"),
        q("True or False: First trisection point of (0,0),(9,9) is (3,3).", "fill", "Answer = ____"),
        q("Spot: A(0,0),B(8,12) at 3:1 gives (2,3). Correct? Fix (6,9). ____", "fill", "Answer = ____"),
        q("True or False: P at (6,0) divides (0,0),(9,0) in ratio 2:1.", "fill", "Answer = ____"),
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# 15F — Graph basics (lines, slope, intercepts)
# ═══════════════════════════════════════════════════════════════════════════════
def _L15F_1():
    return [
        cb("Straight Lines on a Graph", [
            "A linear equation like y = mx + c graphs as a straight line.",
            "m = slope (steepness): rise over run. c = y-intercept (where it crosses the y-axis).",
            "To find the x-intercept, set y = 0; for the y-intercept, set x = 0.",
        ], "y = 2x + 1: slope 2, crosses y-axis at (0,1)."),
        q("In y = 3x + 5, the slope is ____", "fill", "Answer = ____"),
        q("In y = 3x + 5, the y-intercept is ____", "fill", "Answer = ____"),
        q("In y = -2x + 4, the slope is ____", "fill", "Answer = ____"),
        q("In y = -2x + 4, the y-intercept is ____", "fill", "Answer = ____"),
        q("In y = x, the slope is ____", "fill", "Answer = ____"),
        q("In y = 7, the slope is ____ (horizontal line)", "fill", "Answer = ____"),
        q("y = 2x + 1 at x = 0: y = ____", "fill", "Answer = ____"),
        q("y = 2x + 1 at x = 3: y = ____", "fill", "Answer = ____"),
        q("y = 2x - 6: x-intercept (set y=0): x = ____", "fill", "Answer = ____"),
        q("y = 2x - 6: y-intercept = ____", "fill", "Answer = ____"),
        q("Does (1, 5) lie on y = 2x + 3? ____", "fill", "Answer = ____"),
        q("Does (2, 4) lie on y = 3x - 2? ____", "fill", "Answer = ____"),
        q("Slope of a horizontal line: ____", "fill", "Answer = ____"),
        q("y = 4x: passes through the origin? ____", "fill", "Answer = ____"),
        q("y = 5x - 10: x-intercept = ____", "fill", "Answer = ____"),
        q("True or False: In y = 3x + 5, slope is 3.", "fill", "Answer = ____"),
        q("True or False: y-intercept is where x = 0.", "fill", "Answer = ____"),
        q("True or False: (1,5) lies on y = 2x + 3.", "fill", "Answer = ____"),
        q("Spot: y = 2x - 6 has x-intercept at x = 6. Correct? Fix (3). ____", "fill", "Answer = ____"),
        q("True or False: A horizontal line has slope 0.", "fill", "Answer = ____"),
    ]

def _L15F_2():
    return [
        cb("Slope Between Two Points", [
            "Slope m = (y2 - y1) / (x2 - x1): change in y over change in x.",
            "Positive slope rises left→right; negative slope falls.",
            "Zero slope is horizontal; undefined (vertical) when x2 = x1.",
        ], "Through (1,2) and (3,8): m = (8-2)/(3-1) = 6/2 = 3."),
        q("Slope through (1,2),(3,8) = ____", "fill", "Answer = ____"),
        q("Slope through (0,0),(4,8) = ____", "fill", "Answer = ____"),
        q("Slope through (2,3),(5,3) = ____", "fill", "Answer = ____"),
        q("Slope through (4,1),(4,9) = ____ (vertical)", "fill", "Answer = ____"),
        q("Slope through (0,0),(5,10) = ____", "fill", "Answer = ____"),
        q("Slope through (1,5),(3,1) = ____", "fill", "Answer = ____"),
        q("Slope through (-2,0),(0,4) = ____", "fill", "Answer = ____"),
        q("Slope through (0,6),(3,0) = ____", "fill", "Answer = ____"),
        q("y = mx + c through (0,2) with slope 3: equation? ____", "fill", "Answer = ____"),
        q("Line with slope 0 through (0,5): equation? ____", "fill", "Answer = ____"),
        q("Slope through (1,1),(2,3) = ____", "fill", "Answer = ____"),
        q("Slope through (3,7),(6,13) = ____", "fill", "Answer = ____"),
        q("A line rising left to right has slope (positive/negative)? ____", "fill", "Answer = ____"),
        q("A line falling left to right has slope (positive/negative)? ____", "fill", "Answer = ____"),
        q("Slope through (2,2),(8,8) = ____", "fill", "Answer = ____"),
        q("True or False: Slope through (1,2),(3,8) is 3.", "fill", "Answer = ____"),
        q("True or False: A vertical line has undefined slope.", "fill", "Answer = ____"),
        q("True or False: Slope through (2,3),(5,3) is 0.", "fill", "Answer = ____"),
        q("Spot: Slope through (0,6),(3,0) = 2. Correct? Fix (-2). ____", "fill", "Answer = ____"),
        q("True or False: Slope through (0,0),(5,10) is 2.", "fill", "Answer = ____"),
    ]

def _L15F_3():
    return [
        tb("Graph Basics — Tips", [
            "y = mx + c: m is slope, c is y-intercept.",
            "Slope between points = (y2-y1)/(x2-x1).",
            "x-intercept: set y=0. y-intercept: set x=0.",
            "Horizontal slope 0; vertical slope undefined.",
        ]),
        q("Slope of y = 6x - 1: ____", "fill", "Answer = ____"),
        q("y-intercept of y = 6x - 1: ____", "fill", "Answer = ____"),
        q("Slope through (1,3),(4,12): ____", "fill", "Answer = ____"),
        q("Slope through (2,5),(6,5): ____", "fill", "Answer = ____"),
        q("x-intercept of y = 3x - 9: ____", "fill", "Answer = ____"),
        q("y = 4x + 2 at x = 5: ____", "fill", "Answer = ____"),
        q("Does (3,11) lie on y = 3x + 2? ____", "fill", "Answer = ____"),
        q("Slope through (0,0),(7,21): ____", "fill", "Answer = ____"),
        q("Equation: slope 5, y-intercept -3: ____", "fill", "Answer = ____"),
        q("Slope through (-1,-1),(1,3): ____", "fill", "Answer = ____"),
        q("y = -x + 8: y-intercept: ____", "fill", "Answer = ____"),
        q("y = -x + 8: x-intercept: ____", "fill", "Answer = ____"),
        q("Slope through (5,2),(5,10): ____", "fill", "Answer = ____"),
        q("Slope through (1,4),(3,4): ____", "fill", "Answer = ____"),
        q("y = 2x at x = 9: ____", "fill", "Answer = ____"),
        q("True or False: y = 6x - 1 has slope 6.", "fill", "Answer = ____"),
        q("True or False: x-intercept of y = 3x - 9 is 3.", "fill", "Answer = ____"),
        q("True or False: (3,11) lies on y = 3x + 2.", "fill", "Answer = ____"),
        q("Spot: Slope through (1,3),(4,12) = 4. Correct? Fix (3). ____", "fill", "Answer = ____"),
        q("True or False: Slope through (2,5),(6,5) is 0.", "fill", "Answer = ____"),
    ]

def _L15F_4():
    return [
        q("Slope through (2,1),(8,4): ____", "fill", "Answer = ____"),
        q("Slope through (-3,2),(3,-4): ____", "fill", "Answer = ____"),
        q("Equation of line slope 2 through (0,-5): ____", "fill", "Answer = ____"),
        q("Equation of line slope -3 through (0,4): ____", "fill", "Answer = ____"),
        q("x-intercept of y = 4x - 20: ____", "fill", "Answer = ____"),
        q("y-intercept of y = 4x - 20: ____", "fill", "Answer = ____"),
        q("Do (1,2),(2,4),(3,6) lie on one line through origin? slope each = ____", "fill", "Answer = ____"),
        q("Line through (0,0) and (3,6): equation y = ____", "fill", "Answer = ____"),
        q("Parallel lines have equal ____", "fill", "Answer = ____"),
        q("Slope of any line parallel to y = 5x + 1: ____", "fill", "Answer = ____"),
        q("Line y = 2x + 3: point where x = -1 is (-1, ____)", "fill", "Answer = ____"),
        q("Is (4, 11) on y = 3x - 1? ____", "fill", "Answer = ____"),
        q("Slope through (10,0),(0,5): ____", "fill", "Answer = ____"),
        q("y = -2x + 10: x-intercept: ____", "fill", "Answer = ____"),
        q("Two points (1,1),(5,9): slope = ____", "fill", "Answer = ____"),
        q("True or False: Lines parallel to y = 5x+1 have slope 5.", "fill", "Answer = ____"),
        q("True or False: (1,2),(2,4),(3,6) are collinear.", "fill", "Answer = ____"),
        q("True or False: x-intercept of y = 4x - 20 is 5.", "fill", "Answer = ____"),
        q("Spot: Slope through (-3,2),(3,-4) = 1. Correct? Fix (-1). ____", "fill", "Answer = ____"),
        q("True or False: Equation slope 2 through (0,-5) is y = 2x - 5.", "fill", "Answer = ____"),
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# Multi-sheet families: G, H, I, J, CUM1, CUM2, CUM3, REV use _s(sheet) pattern
# ═══════════════════════════════════════════════════════════════════════════════
def _L15G_s(sheet):
    s1 = [
        cb("Graph Applications", [
            "Coordinate geometry models real situations: distance, cost, motion.",
            "Plot points from a table, read values off the line.",
            "Slope often means a rate (cost per item, speed).",
        ], "Cost y = 50x: slope 50 = price per unit."),
        q("Cost y = 50x. Cost of 3 units: ____", "fill", "Answer = ____"),
        q("Cost y = 50x. Cost of 10 units: ____", "fill", "Answer = ____"),
        q("Distance y = 60x (km in x hours). Distance in 4 hours: ____", "fill", "Answer = ____"),
        q("Distance y = 60x. Time to travel 300 km: ____", "fill", "Answer = ____"),
        q("A line passes (0,0),(2,100). Slope (rate): ____", "fill", "Answer = ____"),
        q("Taxi: y = 30 + 10x. Base fare (x=0): ____", "fill", "Answer = ____"),
        q("Taxi: y = 30 + 10x. Fare for 5 km: ____", "fill", "Answer = ____"),
        q("Plot (1,2),(2,4),(3,6): slope of the line: ____", "fill", "Answer = ____"),
        q("y = 20x: value at x = 7: ____", "fill", "Answer = ____"),
        q("Phone plan y = 100 + 2x (x = minutes). Cost at 0 min: ____", "fill", "Answer = ____"),
        q("Phone plan y = 100 + 2x. Cost at 50 min: ____", "fill", "Answer = ____"),
        q("Savings y = 500 + 100x (months). After 6 months: ____", "fill", "Answer = ____"),
        q("Savings y = 500 + 100x. Start amount: ____", "fill", "Answer = ____"),
        q("Line through (0,10),(5,0): x-intercept: ____", "fill", "Answer = ____"),
        q("Line through (0,10),(5,0): slope: ____", "fill", "Answer = ____"),
        q("True or False: In y = 50x, the rate per unit is 50.", "fill", "Answer = ____"),
        q("True or False: Taxi y = 30 + 10x has base fare 30.", "fill", "Answer = ____"),
        q("True or False: Distance y = 60x covers 240 km in 4 hours.", "fill", "Answer = ____"),
        q("Spot: y = 50x gives 200 for 3 units. Correct? Fix (150). ____", "fill", "Answer = ____"),
        q("True or False: Savings y = 500 + 100x starts at 500.", "fill", "Answer = ____"),
    ]
    s2 = [
        cb("Reading and Building Graphs", [
            "From a table of (x, y), find the rule y = mx + c.",
            "c = value at x=0; m = change in y for each step in x.",
            "Use the rule to predict beyond the table.",
        ], "Table (0,2),(1,5),(2,8): rule y = 3x + 2."),
        q("Table (0,2),(1,5),(2,8): slope m = ____", "fill", "Answer = ____"),
        q("Table (0,2),(1,5),(2,8): intercept c = ____", "fill", "Answer = ____"),
        q("Table (0,2),(1,5),(2,8): rule y = ____", "fill", "Answer = ____"),
        q("Using y = 3x + 2, value at x = 10: ____", "fill", "Answer = ____"),
        q("Table (0,0),(1,4),(2,8): rule y = ____", "fill", "Answer = ____"),
        q("Table (0,7),(1,7),(2,7): rule y = ____", "fill", "Answer = ____"),
        q("Table (0,5),(1,3),(2,1): slope m = ____", "fill", "Answer = ____"),
        q("Table (0,5),(1,3),(2,1): rule y = ____", "fill", "Answer = ____"),
        q("Predict y at x=4 for y = -2x + 5: ____", "fill", "Answer = ____"),
        q("Water tank y = 200 - 20x (x min draining). At x=5: ____", "fill", "Answer = ____"),
        q("Water tank y = 200 - 20x. Empty when y=0 at x = ____", "fill", "Answer = ____"),
        q("Rule from (1,3),(2,6),(3,9): y = ____", "fill", "Answer = ____"),
        q("y = 4x - 1: value at x=6: ____", "fill", "Answer = ____"),
        q("Table (0,10),(2,16),(4,22): slope m = ____", "fill", "Answer = ____"),
        q("Table (0,10),(2,16),(4,22): rule y = ____", "fill", "Answer = ____"),
        q("True or False: Table (0,2),(1,5),(2,8) gives y = 3x + 2.", "fill", "Answer = ____"),
        q("True or False: Tank y = 200 - 20x empties at x = 10.", "fill", "Answer = ____"),
        q("True or False: Table (0,7),(1,7),(2,7) is y = 7.", "fill", "Answer = ____"),
        q("Spot: Table (0,5),(1,3),(2,1) has slope 2. Correct? Fix (-2). ____", "fill", "Answer = ____"),
        q("True or False: y = 4x - 1 gives 23 at x = 6.", "fill", "Answer = ____"),
    ]
    s3 = [
        tb("Graph Applications — Tips", [
            "Rate of change = slope. Starting value = y-intercept (c).",
            "Cost/distance/savings problems are usually y = mx + c.",
            "x-intercept: where the quantity hits zero.",
            "Read tables: m = step change in y, c = value at x = 0.",
        ]),
        q("y = 40x: cost of 6: ____", "fill", "Answer = ____"),
        q("y = 25 + 5x: value at x=10: ____", "fill", "Answer = ____"),
        q("Table (0,3),(1,7),(2,11): rule y = ____", "fill", "Answer = ____"),
        q("Distance y = 80x: time for 400 km: ____", "fill", "Answer = ____"),
        q("y = 100 - 10x: value at x=4: ____", "fill", "Answer = ____"),
        q("y = 100 - 10x: zero at x = ____", "fill", "Answer = ____"),
        q("Slope of line through (0,0),(3,15): ____", "fill", "Answer = ____"),
        q("Savings y = 1000 + 200x: after 5 months: ____", "fill", "Answer = ____"),
        q("Phone y = 50 + 3x: cost at 20 min: ____", "fill", "Answer = ____"),
        q("Table (0,0),(2,10),(4,20): slope: ____", "fill", "Answer = ____"),
        q("y = 6x: value at x = 12: ____", "fill", "Answer = ____"),
        q("Line through (0,20),(4,0): slope: ____", "fill", "Answer = ____"),
        q("Line through (0,20),(4,0): x-intercept: ____", "fill", "Answer = ____"),
        q("Rule from (1,5),(2,8),(3,11): y = ____", "fill", "Answer = ____"),
        q("y = 2x + 7 at x = 0: ____", "fill", "Answer = ____"),
        q("True or False: y = 40x gives 240 for 6 units.", "fill", "Answer = ____"),
        q("True or False: y = 100 - 10x is zero at x = 10.", "fill", "Answer = ____"),
        q("True or False: Table (0,3),(1,7),(2,11) is y = 4x + 3.", "fill", "Answer = ____"),
        q("Spot: Distance y = 80x covers 400 km in 4 hours. Correct? Fix (5). ____", "fill", "Answer = ____"),
        q("True or False: Savings y = 1000 + 200x is 2000 after 5 months.", "fill", "Answer = ____"),
    ]
    s4 = [
        q("A car: y = 70x km. Distance in 6 hours: ____", "fill", "Answer = ____"),
        q("A car: y = 70x. Hours for 490 km: ____", "fill", "Answer = ____"),
        q("Plan y = 200 + 8x: cost at 25 units: ____", "fill", "Answer = ____"),
        q("Plan y = 200 + 8x: base cost: ____", "fill", "Answer = ____"),
        q("Table (0,4),(3,16),(6,28): slope: ____", "fill", "Answer = ____"),
        q("Table (0,4),(3,16),(6,28): rule y = ____", "fill", "Answer = ____"),
        q("Tank y = 500 - 25x: empty at x = ____", "fill", "Answer = ____"),
        q("Tank y = 500 - 25x: amount at x = 8: ____", "fill", "Answer = ____"),
        q("Two plans: A y=10x, B y=50+5x. Equal cost at x = ____", "fill", "Answer = ____"),
        q("At x=10, plan A (y=10x) cost: ____", "fill", "Answer = ____"),
        q("At x=10, plan B (y=50+5x) cost: ____", "fill", "Answer = ____"),
        q("Line through (0,0),(8,24): slope: ____", "fill", "Answer = ____"),
        q("Line through (0,12),(6,0): slope: ____", "fill", "Answer = ____"),
        q("Rule from (2,9),(4,15),(6,21): y = ____", "fill", "Answer = ____"),
        q("y = 3x + 4 at x = 100: ____", "fill", "Answer = ____"),
        q("True or False: y = 70x covers 490 km in 7 hours.", "fill", "Answer = ____"),
        q("True or False: Plans y=10x and y=50+5x are equal at x=10.", "fill", "Answer = ____"),
        q("True or False: Tank y = 500 - 25x empties at x = 20.", "fill", "Answer = ____"),
        q("Spot: Table (0,4),(3,16),(6,28) has slope 3. Correct? Fix (4). ____", "fill", "Answer = ____"),
        q("True or False: Rule from (2,9),(4,15),(6,21) is y = 3x + 3.", "fill", "Answer = ____"),
    ]
    return [s1, s2, s3, s4][sheet - 1]


def _triangle_area2(p1, p2, p3):
    """Returns 2*area (always an integer for integer coordinates)."""
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3
    return x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)


def _gen_triangle(hi=6):
    while True:
        p1 = (random.randint(-hi, hi), random.randint(-hi, hi))
        p2 = (random.randint(-hi, hi), random.randint(-hi, hi))
        p3 = (random.randint(-hi, hi), random.randint(-hi, hi))
        a2 = _triangle_area2(p1, p2, p3)
        if a2 != 0 and a2 % 2 == 0:
            return p1, p2, p3, abs(a2) // 2


# ─── 15H: Area of a Triangle Using Coordinates ────────────────
def _L15H_s(sheet):
    random.seed(1520 + sheet)
    ranges = {1: (4, 6), 2: (5, 7), 3: (6, 8), 4: (6, 10)}
    lo, hi = ranges[sheet]
    items = [
        cb("Area of a Triangle from Coordinates", [
            "For A(x1,y1), B(x2,y2), C(x3,y3):",
            "Area = 1/2 |x1(y2-y3) + x2(y3-y1) + x3(y1-y2)|",
            "The bars mean take the positive value -- area can't be negative.",
        ], "A(0,0), B(6,0), C(3,5): Area = 1/2|0(0-5)+6(5-0)+3(0-0)| = 1/2(30) = 15"),
    ]
    for _ in range(6):
        p1, p2, p3, area = _gen_triangle(hi)
        items.append(q(f"Use the diagram to find the area of triangle ABC with A{p1}, B{p2}, C{p3}.", "diagram", "____", "", "triangle_coords", {"p1": p1, "p2": p2, "p3": p3}))
    for _ in range(6):
        p1, p2, p3, area = _gen_triangle(hi)
        items.append(q(f"Find the area of the triangle with vertices A{p1}, B{p2}, C{p3} using the coordinate formula.", "fill", "Answer = ____"))
    for _ in range(4):
        p1, p2, p3, area = _gen_triangle(hi)
        shown = area if random.random() > 0.4 else area + 1
        items.append(q(f"True or False: The triangle with vertices A{p1}, B{p2}, C{p3} has area {shown}.", "fill", "Answer = ____"))
    for _ in range(4):
        p1, p2, p3, area = _gen_triangle(hi)
        items.append(q(f"A{p1}, B{p2}, C{p3}. Find x1(y2-y3) + x2(y3-y1) + x3(y1-y2) first, then halve and take the positive value.", "fill", "Answer = ____"))
    return items


def _L15I_s(sheet):
    s1 = [
        cb("Puzzle Graphs", [
            "Use coordinate clues to find unknown points.",
            "Combine distance, midpoint and collinearity to solve.",
            "Check answers by substituting back.",
        ], "If (a,0) is 5 from (0,0), a = ±5."),
        q("(a,0) is distance 5 from origin. a (positive)? ____", "fill", "Answer = ____"),
        q("(0,b) is distance 12 from origin. b (positive)? ____", "fill", "Answer = ____"),
        q("Midpoint of (2,k) and (8,10) is (5,7). k = ____", "fill", "Answer = ____"),
        q("Midpoint of (a,3),(9,3) is (6,3). a = ____", "fill", "Answer = ____"),
        q("(x,0) is 13 from (0,0) and x>0: x = ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (8,b) is 10. b (positive)? ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (a,4) is 5. a (positive)? ____", "fill", "Answer = ____"),
        q("(p,p) is distance √8 from origin, p>0. p = ____", "fill", "Answer = ____"),
        q("Midpoint of (0,0),(c,c) is (3,3). c = ____", "fill", "Answer = ____"),
        q("Three points (0,0),(2,2),(k,5) collinear on y=x means k = ____", "fill", "Answer = ____"),
        q("(m,0),(0,m) and origin form a triangle; if m=6, base length: ____", "fill", "Answer = ____"),
        q("Midpoint of (1,1),(x,9) is (4,5). x = ____", "fill", "Answer = ____"),
        q("Distance (3,4) to (3,y) is 5, y>4. y = ____", "fill", "Answer = ____"),
        q("(a,0) and (0,a): if distance between them is √50, a>0: a = ____", "fill", "Answer = ____"),
        q("(0,0),(6,0),(6,h) right triangle hyp 10. h = ____", "fill", "Answer = ____"),
        q("True or False: (a,0) at distance 5 from origin gives a = 5 (positive).", "fill", "Answer = ____"),
        q("True or False: Midpoint of (a,3),(9,3)=(6,3) gives a=3.", "fill", "Answer = ____"),
        q("True or False: Distance (0,0) to (8,b)=10 gives b=6.", "fill", "Answer = ____"),
        q("Spot: (p,p) at √8 from origin gives p=4. Correct? Fix (2). ____", "fill", "Answer = ____"),
        q("True or False: (0,0),(6,0),(6,8) right triangle has hypotenuse 10.", "fill", "Answer = ____"),
    ]
    s2 = [
        cb("Coordinate Puzzles", [
            "Set up equations from the conditions, then solve.",
            "Equidistant points: set the two distances equal.",
            "Collinear: equal slopes between successive points.",
        ], "Point on x-axis equidistant from A and B: set distances equal."),
        q("Midpoint of (k,2),(6,2) is (4,2). k = ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (a,a) = √32, a>0. a = ____", "fill", "Answer = ____"),
        q("Midpoint of (3,y),(3,11) is (3,7). y = ____", "fill", "Answer = ____"),
        q("(x,0) equidistant from (0,0) and (8,0): x = ____", "fill", "Answer = ____"),
        q("Collinear on y=2x: (1,2),(2,4),(3,k). k = ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (9,b) = 15, b>0. b = ____", "fill", "Answer = ____"),
        q("Midpoint of (a,b),(2,4) is origin. a = ____", "fill", "Answer = ____"),
        q("Midpoint of (a,b),(2,4) is origin. b = ____", "fill", "Answer = ____"),
        q("(0,0),(10,0),(5,h) isosceles with equal sides 13. h = ____", "fill", "Answer = ____"),
        q("Distance (2,3) to (2,k) = 6, k>3. k = ____", "fill", "Answer = ____"),
        q("Square (0,0),(s,0),(s,s),(0,s) has diagonal √72. s = ____ (s>0)", "fill", "Answer = ____"),
        q("Three points (0,0),(k,k),(4,4) collinear: any k works on y=x? ____", "fill", "Answer = ____"),
        q("(a,0) is 17 from (0,8). a>0. a = ____", "fill", "Answer = ____"),
        q("Midpoint of (5,5),(x,y) is (8,9). x = ____", "fill", "Answer = ____"),
        q("Midpoint of (5,5),(x,y) is (8,9). y = ____", "fill", "Answer = ____"),
        q("True or False: (x,0) equidistant from (0,0),(8,0) is x=4.", "fill", "Answer = ____"),
        q("True or False: Distance (0,0) to (9,12)=15.", "fill", "Answer = ____"),
        q("True or False: Midpoint of (a,b),(2,4)=origin gives a=-2.", "fill", "Answer = ____"),
        q("Spot: Distance (0,0) to (a,a)=√32 gives a=4. Correct? ____", "fill", "Answer = ____"),
        q("True or False: Square with diagonal √72 has side 6.", "fill", "Answer = ____"),
    ]
    s3 = [
        tb("Coordinate Puzzles — Tips", [
            "Translate each clue into an equation, then solve.",
            "Equidistant → set distances equal (squares are easier).",
            "Collinear → equal slope between consecutive points.",
            "Always substitute your answer back to verify.",
        ]),
        q("Midpoint of (a,0),(10,0) is (7,0). a = ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (a,12) = 13, a>0. a = ____", "fill", "Answer = ____"),
        q("(0,k) is 10 from (6,0)? √(36+k²)=10 → k>0: k = ____", "fill", "Answer = ____"),
        q("Midpoint of (2,2),(x,8) is (5,5). x = ____", "fill", "Answer = ____"),
        q("Collinear y=3x: (1,3),(2,6),(4,k). k = ____", "fill", "Answer = ____"),
        q("(x,0) equidistant from (0,0),(12,0): x = ____", "fill", "Answer = ____"),
        q("Distance (3,4) to (0,0) = ____", "fill", "Answer = ____"),
        q("Square side s, diagonal √50, s>0: s = ____", "fill", "Answer = ____"),
        q("Midpoint of (-3,y),(7,3) is (2,5). y = ____", "fill", "Answer = ____"),
        q("(a,a) distance √18 from origin, a>0: a = ____", "fill", "Answer = ____"),
        q("(0,0),(8,0),(4,h) isosceles equal sides 5. h = ____", "fill", "Answer = ____"),
        q("Distance (5,0) to (5,k) = 9, k>0: k = ____", "fill", "Answer = ____"),
        q("Midpoint of (a,b),(6,8) is (3,4). a = ____", "fill", "Answer = ____"),
        q("Midpoint of (a,b),(6,8) is (3,4). b = ____", "fill", "Answer = ____"),
        q("(p,0) is 25 from (0,7)? p>0... √(p²+49)=25: p = ____", "fill", "Answer = ____"),
        q("True or False: Midpoint of (a,0),(10,0)=(7,0) gives a=4.", "fill", "Answer = ____"),
        q("True or False: Distance (0,0) to (5,12,)=(a,12)=13 gives a=5.", "fill", "Answer = ____"),
        q("True or False: Square with diagonal √50 has side 5.", "fill", "Answer = ____"),
        q("Spot: (a,a) at √18 from origin gives a=3. Correct? ____", "fill", "Answer = ____"),
        q("True or False: (x,0) equidistant from (0,0),(12,0) is x=6.", "fill", "Answer = ____"),
    ]
    s4 = [
        q("Midpoint of (a,5),(11,5) is (7,5). a = ____", "fill", "Answer = ____"),
        q("Distance (0,0) to (a,24) = 25, a>0: a = ____", "fill", "Answer = ____"),
        q("(0,k) is 17 from (8,0), k>0: k = ____", "fill", "Answer = ____"),
        q("Collinear y=4x: (1,4),(3,12),(5,k). k = ____", "fill", "Answer = ____"),
        q("Square diagonal √98, side s>0: s = ____", "fill", "Answer = ____"),
        q("(x,0) equidistant from (2,0),(10,0): x = ____", "fill", "Answer = ____"),
        q("Midpoint of (-5,y),(9,3) is (2,6). y = ____", "fill", "Answer = ____"),
        q("(a,a) distance √72 from origin, a>0: a = ____", "fill", "Answer = ____"),
        q("(0,0),(14,0),(7,h) isosceles equal sides 25. h = ____", "fill", "Answer = ____"),
        q("Distance (6,2) to (6,k) = 10, k>2: k = ____", "fill", "Answer = ____"),
        q("Three points (0,0),(p,2p),(3,6) on y=2x: p can be? ____", "fill", "Answer = ____"),
        q("Midpoint of (a,b),(10,12) is (4,5). a = ____", "fill", "Answer = ____"),
        q("Midpoint of (a,b),(10,12) is (4,5). b = ____", "fill", "Answer = ____"),
        q("(p,0) is 15 from (0,9), p>0: p = ____", "fill", "Answer = ____"),
        q("Rectangle (0,0),(a,0),(a,b),(0,b) diagonal 13, a=12: b = ____", "fill", "Answer = ____"),
        q("True or False: Distance (0,0) to (7,24)=25, so (a,24)=25 gives a=7.", "fill", "Answer = ____"),
        q("True or False: Square diagonal √98 has side 7.", "fill", "Answer = ____"),
        q("True or False: (x,0) equidistant from (2,0),(10,0) is x=6.", "fill", "Answer = ____"),
        q("Spot: (a,a) at √72 from origin gives a=8. Correct? Fix (6). ____", "fill", "Answer = ____"),
        q("True or False: Rectangle diagonal 13 with a=12 gives b=5.", "fill", "Answer = ____"),
    ]
    return [s1, s2, s3, s4][sheet - 1]


# ─── 15J: Coordinate Geometry Mastery Challenge ───────────────
def _L15J_s(sheet):
    random.seed(1540 + sheet)
    ranges = {1: (6, 10), 2: (8, 12), 3: (10, 15), 4: (12, 18)}
    lo, hi = ranges[sheet]
    items = [
        cb("Coordinate Geometry Mastery Challenge", [
            "Every skill: distance, midpoint, section formula, area of a triangle, collinearity.",
            "Bigger numbers here -- this challenge covers the whole level.",
            "Speed challenge: each question has a point value.",
        ], "Bronze 20+, Silver 30+, Gold 38+ (all correct)"),
    ]

    def gen_pythag_points(hi):
        triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15)]
        a, b, c = random.choice(triples)
        if random.random() > 0.5: a, b = b, a
        x1, y1 = random.randint(-hi, hi), random.randint(-hi, hi)
        return (x1, y1), (x1 + a, y1 + b), c

    for _ in range(5):
        p1, p2, dist = gen_pythag_points(hi)
        items.append(q(f"Find the distance between {p1} and {p2}.  [2 points]", "fill", "Answer = ____"))
    for _ in range(4):
        x1, y1 = random.randint(-hi, hi), random.randint(-hi, hi)
        x2, y2 = x1 + 2 * random.randint(1, 5), y1 + 2 * random.randint(1, 5)
        items.append(q(f"Find the midpoint of ({x1},{y1}) and ({x2},{y2}).  [2 points]", "fill", "Answer = ____"))
    for _ in range(4):
        p1, p2, p3, area = _gen_triangle(hi)
        items.append(q(f"Find the area of the triangle A{p1}, B{p2}, C{p3}.  [3 points]", "fill", "Answer = ____"))
    for _ in range(4):
        x1, y1 = random.randint(-hi, hi), random.randint(-hi, hi)
        dx, dy = random.choice([(1, 1), (1, 2), (2, 1), (1, -1)])
        k1, k2 = sorted(random.sample(range(1, 5), 2))
        p1, p2, p3 = (x1, y1), (x1 + k1 * dx, y1 + k1 * dy), (x1 + k2 * dx, y1 + k2 * dy)
        items.append(q(f"Are A{p1}, B{p2}, C{p3} collinear?  [2 points]", "fill", "Answer = ____"))
    for _ in range(3):
        p1, p2, dist = gen_pythag_points(hi)
        shown = dist if random.random() > 0.4 else dist + 1
        items.append(q(f"True or False: Distance between {p1} and {p2} is {shown}.  [1 point]", "fill", "Answer = ____ (True/False)"))
    items.append(tb("Your Score", ["My total score: _____.  My badge: Bronze / Silver / Gold (circle one)"]))
    return items


import random


def _gen_two_points(hi=8):
    x1, y1 = random.randint(-hi, hi), random.randint(-hi, hi)
    x2, y2 = random.randint(-hi, hi), random.randint(-hi, hi)
    while (x1, y1) == (x2, y2):
        x2, y2 = random.randint(-hi, hi), random.randint(-hi, hi)
    return (x1, y1), (x2, y2)


def _gen_pythag_points(hi=6):
    """Two points whose x/y gaps form a clean 3-4-5-style right triangle."""
    triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (7, 24, 25)]
    a, b, c = random.choice(triples)
    if random.random() > 0.5:
        a, b = b, a
    x1, y1 = random.randint(-hi, hi), random.randint(-hi, hi)
    x2, y2 = x1 + a, y1 + b
    return (x1, y1), (x2, y2), c


def _quadrant_of(x, y):
    if x > 0 and y > 0: return "I"
    if x < 0 and y > 0: return "II"
    if x < 0 and y < 0: return "III"
    if x > 0 and y < 0: return "IV"
    return "on an axis"


# ─── 15CUM1: Coordinate Plane, Plotting & Distance — Visual Practice ───
def _L15CUM1_s(sheet):
    random.seed(1500 + sheet)
    ranges = {1: (4, 6), 2: (5, 7), 3: (6, 8), 4: (6, 9)}
    lo, hi = ranges[sheet]
    items = [
        cb("Seeing the Coordinate Plane", [
            "A point (x,y): x tells you how far left/right, y tells you how far up/down.",
            "Distance uses the horizontal and vertical gaps -- it's Pythagoras in disguise.",
        ], "Distance (1,1) to (5,4): horizontal gap 4, vertical gap 3, distance 5."),
    ]
    for _ in range(5):
        pts = [(random.randint(-hi, hi), random.randint(-hi, hi)) for _ in range(2)]
        items.append(q("Plot the points shown. Name the quadrant (or axis) for each.", "diagram", "____", "", "plot_points_grid", {"points": pts, "labels": [f"({x},{y})" for x, y in pts]}))
    for _ in range(6):
        p1, p2, dist = _gen_pythag_points(hi)
        items.append(q(f"The diagram shows the segment from {p1} to {p2}. Use the right triangle to find the distance.", "diagram", "____", "", "distance_segment", {"p1": p1, "p2": p2}))
    for _ in range(4):
        x, y = random.randint(-hi, hi), random.randint(-hi, hi)
        while x == 0 or y == 0: x, y = random.randint(-hi, hi), random.randint(-hi, hi)
        items.append(q(f"Which quadrant is ({x},{y}) in?", "fill", "Answer = ____"))
    for _ in range(3):
        p1, p2, dist = _gen_pythag_points(hi)
        items.append(q(f"Find the distance between {p1} and {p2}.", "fill", "Answer = ____"))
    for _ in range(2):
        p1, p2, dist = _gen_pythag_points(hi)
        shown = dist if random.random() > 0.4 else dist + 1
        items.append(q(f"True or False: The distance between {p1} and {p2} is {shown}.", "fill", "Answer = ____"))
    return items


# ─── 15CUM2: Midpoint, Section & Graphing — Visual Practice ──
def _L15CUM2_s(sheet):
    random.seed(1510 + sheet)
    ranges = {1: (4, 8), 2: (5, 9), 3: (6, 10), 4: (6, 12)}
    lo, hi = ranges[sheet]
    items = [
        cb("Seeing the Midpoint, Section & Graphs", [
            "Midpoint: exactly halfway between two points.",
            "Section formula: a point dividing a segment in a given ratio m:n.",
            "y=mx+c graphs as a straight line -- m is the slope, c is the y-intercept.",
        ], "Midpoint of (1,1) and (7,5) is (4,3)."),
    ]

    def gen_even_points(hi):
        x1, y1 = random.randint(-hi, hi), random.randint(-hi, hi)
        x2 = x1 + 2 * random.randint(1, 4) * random.choice([1, -1])
        y2 = y1 + 2 * random.randint(1, 4) * random.choice([1, -1])
        return (x1, y1), (x2, y2)

    for _ in range(5):
        p1, p2 = gen_even_points(hi)
        items.append(q(f"The diagram shows the segment from {p1} to {p2}. Find the midpoint.", "diagram", "____", "", "midpoint_segment", {"p1": p1, "p2": p2}))
    for _ in range(5):
        x1, y1 = 0, 0
        m, n = random.choice([(1, 1), (1, 2), (1, 3), (2, 1), (3, 1)])
        total = m + n
        x2, y2 = total * random.randint(1, 3), total * random.randint(1, 3)
        items.append(q(f"The diagram shows P dividing AB in ratio {m}:{n}. Find P's coordinates.", "diagram", "____", "", "section_segment", {"p1": (x1, y1), "p2": (x2, y2), "m": m, "n": n}))
    for _ in range(5):
        a = random.randint(-4, 4) or 1
        c = random.randint(-hi, hi)
        items.append(q(f"Graph y={a}x{'+' if c>=0 else ''}{c}. Find the y-intercept.", "diagram", "____", "", "linear_equation_graph", {"a": -a, "b": 1, "c": c}))
    for _ in range(3):
        p1, p2 = gen_even_points(hi)
        items.append(q(f"Find the midpoint of {p1} and {p2}.", "fill", "Answer = ____"))
    for _ in range(2):
        a = random.randint(2, 5)
        c = random.randint(-hi, hi)
        items.append(q(f"In y={a}x{'+' if c>=0 else ''}{c}, what is the slope?", "fill", "Answer = ____"))
    return items


# ─── 15CUM3: Collinearity — the Area=0 Test ───────────────────
def _L15CUM3_s(sheet):
    random.seed(1530 + sheet)
    ranges = {1: (4, 6), 2: (5, 7), 3: (5, 8), 4: (6, 9)}
    lo, hi = ranges[sheet]
    items = [
        cb("Collinearity — the Area Test", [
            "Three points are COLLINEAR (lie on one straight line) exactly when the 'triangle' they form has AREA = 0.",
            "Use the same formula: Area = 1/2|x1(y2-y3)+x2(y3-y1)+x3(y1-y2)|.",
            "This is more reliable than checking slopes -- it works even for vertical lines.",
        ], "A(1,1), B(2,3), C(3,5): area formula gives 0 -- collinear!"),
    ]

    def gen_collinear(hi):
        x1, y1 = random.randint(-hi, hi), random.randint(-hi, hi)
        dx, dy = random.choice([(1, 1), (1, 2), (2, 1), (1, 0), (0, 1), (1, -1), (2, -1), (1, -2)])
        k1, k2 = sorted(random.sample(range(1, 5), 2))
        return (x1, y1), (x1 + k1 * dx, y1 + k1 * dy), (x1 + k2 * dx, y1 + k2 * dy)

    for _ in range(4):
        p1, p2, p3 = gen_collinear(hi)
        items.append(q(f"Use the diagram to check: are A{p1}, B{p2}, C{p3} collinear?", "diagram", "____", "", "triangle_coords", {"p1": p1, "p2": p2, "p3": p3}))
    for _ in range(2):
        p1, p2, p3, area = _gen_triangle(hi)
        items.append(q(f"Use the diagram to check: are A{p1}, B{p2}, C{p3} collinear?", "diagram", "____", "", "triangle_coords", {"p1": p1, "p2": p2, "p3": p3}))
    for _ in range(6):
        p1, p2, p3 = gen_collinear(hi)
        items.append(q(f"Are A{p1}, B{p2}, C{p3} collinear? Use the area test to check.", "fill", "Answer = ____"))
    for _ in range(4):
        p1, p2, p3, area = _gen_triangle(hi)
        items.append(q(f"Are A{p1}, B{p2}, C{p3} collinear? Use the area test to check.", "fill", "Answer = ____"))
    for _ in range(4):
        p1, p2, p3 = gen_collinear(hi)
        items.append(q(f"True or False: A{p1}, B{p2}, C{p3} are collinear (area=0).", "fill", "Answer = ____"))
    return items


# ─── 15REV: Level 15 Revision (samples every topic, climbs in difficulty) ───
def _L15REV_s(sheet):
    random.seed(1550 + sheet)
    ranges = {1: (3, 6), 2: (5, 8), 3: (6, 10), 4: (8, 12)}
    lo, hi = ranges[sheet]
    items = [
        tb("Level 15 Revision — Tips", [
            "Quadrants: (+,+)=I, (-,+)=II, (-,-)=III, (+,-)=IV.",
            "Distance = sqrt[(x2-x1)^2+(y2-y1)^2] -- it's Pythagoras.",
            "Midpoint = average of the x's, average of the y's.",
            "Section formula (ratio m:n): P = ((m x2+n x1)/(m+n), (m y2+n y1)/(m+n)).",
            "Area of a triangle = 1/2|x1(y2-y3)+x2(y3-y1)+x3(y1-y2)|. Area=0 means collinear.",
        ]),
    ]

    def gen_pythag_points(hi):
        triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)]
        a, b, c = random.choice(triples)
        if random.random() > 0.5: a, b = b, a
        x1, y1 = random.randint(-hi, hi), random.randint(-hi, hi)
        return (x1, y1), (x1 + a, y1 + b), c

    for _ in range(2):
        x, y = random.randint(-hi, hi), random.randint(-hi, hi)
        while x == 0 or y == 0: x, y = random.randint(-hi, hi), random.randint(-hi, hi)
        items.append(q(f"Which quadrant is ({x},{y}) in?", "fill", "Answer = ____"))
    for _ in range(3):
        p1, p2, dist = gen_pythag_points(hi)
        items.append(q("The diagram shows a segment. Find its length.", "diagram", "____", "", "distance_segment", {"p1": p1, "p2": p2}))
    for _ in range(2):
        p1, p2, dist = gen_pythag_points(hi)
        items.append(q(f"Find the distance between {p1} and {p2}.", "fill", "Answer = ____"))
    for _ in range(3):
        x1, y1 = random.randint(-hi, hi), random.randint(-hi, hi)
        x2, y2 = x1 + 2 * random.randint(1, 4), y1 + 2 * random.randint(1, 4)
        items.append(q("The diagram shows a segment. Find its midpoint.", "diagram", "____", "", "midpoint_segment", {"p1": (x1, y1), "p2": (x2, y2)}))
    for _ in range(2):
        x1, y1 = 0, 0
        m, n = random.choice([(1, 1), (1, 2), (2, 1)])
        x2, y2 = (m + n) * 2, (m + n) * 2
        items.append(q(f"P divides ({x1},{y1}) to ({x2},{y2}) in ratio {m}:{n}. Find P.", "fill", "Answer = ____"))
    for _ in range(3):
        p1, p2, p3, area = _gen_triangle(hi)
        items.append(q("The diagram shows a triangle. Find its area.", "diagram", "____", "", "triangle_coords", {"p1": p1, "p2": p2, "p3": p3}))
    for _ in range(3):
        p1, p2, p3, area = _gen_triangle(hi)
        items.append(q(f"Find the area of triangle A{p1}, B{p2}, C{p3}.", "fill", "Answer = ____"))
    for _ in range(2):
        x1, y1 = random.randint(-hi, hi), random.randint(-hi, hi)
        dx, dy = random.choice([(1, 1), (1, 2), (2, 1)])
        k1, k2 = sorted(random.sample(range(1, 4), 2))
        p1, p2, p3 = (x1, y1), (x1 + k1 * dx, y1 + k1 * dy), (x1 + k2 * dx, y1 + k2 * dy)
        items.append(q(f"Are A{p1}, B{p2}, C{p3} collinear?", "fill", "Answer = ____"))
    return items

# DISPATCH for Level 15
# ═══════════════════════════════════════════════════════════════════════════════
DISPATCH_L15 = {
    "15A":    {1: _L15A_1, 2: _L15A_2, 3: _L15A_3, 4: _L15A_4},
    "15B":    {1: _L15B_1, 2: _L15B_2, 3: _L15B_3, 4: _L15B_4},
    "15C":    {1: _L15C_1, 2: _L15C_2, 3: _L15C_3, 4: _L15C_4},
    "15D":    {1: _L15D_1, 2: _L15D_2, 3: _L15D_3, 4: _L15D_4},
    "15E":    {1: _L15E_1, 2: _L15E_2, 3: _L15E_3, 4: _L15E_4},
    "15F":    {1: _L15F_1, 2: _L15F_2, 3: _L15F_3, 4: _L15F_4},
    "15G":    {1: lambda: _L15G_s(1), 2: lambda: _L15G_s(2), 3: lambda: _L15G_s(3), 4: lambda: _L15G_s(4)},
    "15H":    {1: lambda: _L15H_s(1), 2: lambda: _L15H_s(2), 3: lambda: _L15H_s(3), 4: lambda: _L15H_s(4)},
    "15I":    {1: lambda: _L15I_s(1), 2: lambda: _L15I_s(2), 3: lambda: _L15I_s(3), 4: lambda: _L15I_s(4)},
    "15J":    {1: lambda: _L15J_s(1), 2: lambda: _L15J_s(2), 3: lambda: _L15J_s(3), 4: lambda: _L15J_s(4)},
    "15CUM1": {1: lambda: _L15CUM1_s(1), 2: lambda: _L15CUM1_s(2), 3: lambda: _L15CUM1_s(3), 4: lambda: _L15CUM1_s(4)},
    "15CUM2": {1: lambda: _L15CUM2_s(1), 2: lambda: _L15CUM2_s(2), 3: lambda: _L15CUM2_s(3), 4: lambda: _L15CUM2_s(4)},
    "15CUM3": {1: lambda: _L15CUM3_s(1), 2: lambda: _L15CUM3_s(2), 3: lambda: _L15CUM3_s(3), 4: lambda: _L15CUM3_s(4)},
    "15REV":  {1: lambda: _L15REV_s(1), 2: lambda: _L15REV_s(2), 3: lambda: _L15REV_s(3), 4: lambda: _L15REV_s(4)},
}
