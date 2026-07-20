"""
Fear Less Maths — LEVEL 6 (Factors, Multiples, HCF & LCM)
Swapped into the Level 6 position (was Level 9) on 2026-07-20: Factors/
Multiples/HCF/LCM now comes before Fractions (previously Level 6, now
moved to Level 9) since HCF/LCM is a genuine prerequisite for
simplifying fractions and finding a common denominator.
Every question has a matching diagram (auto-inferred from its own
numbers), first 2 per sheet fully worked, rest blank scaffolds.
"""
import random
import math
import re as _l6_re
from content import cb, tb, q

def _L9A_1():
    return [
        cb("", [], "", icon_diagram="mascot_splitter",
           icon_params={"message": "Hi, I'm Splitter! I love breaking numbers into equal "
                                    "groups. If it splits evenly with nothing left over, "
                                    "that's a FACTOR!"}),
        cb("BIG IDEA — A factor divides EXACTLY, no remainder", [
            "[1] ↓ 2 ↓ 3 ↓ 4     You are on Sheet 1.",
            "12 splits evenly into groups of 1, 2, 3, 4, 6, or 12 — these are ALL its factors.",
            "Is 4 a factor of 20?  →  20 ÷ 4 = 5, nothing left over  →  YES.",
            "Is 7 a factor of 20?  →  20 ÷ 7 = 2 remainder 6  →  NO (something is left over).",
        ], "", icon_diagram="factor_groups_icon", icon_params={"number": 12, "group_size": 3}),
        q("Is 3 a factor of 12? 12÷3 = ____. Remainder? ____. Answer: ____", "fill", "Answer = ____", tier="INTUITION"),
        q("Is 5 a factor of 12? 12÷5 = ____ r ____. Answer: ____", "fill", "Answer = ____", tier="INTUITION"),
        q("Is 4 a factor of 20? 20÷4 = ____. Answer: ____", "fill", "Answer = ____", tier="CONCEPT"),
        q("Is 6 a factor of 30? 30÷6 = ____. Answer: ____", "fill", "Answer = ____", tier="CONCEPT"),
        q("Is 7 a factor of 35? 35÷7 = ____. Answer: ____", "fill", "Answer = ____", tier="CONCEPT"),
        q("Is 9 a factor of 40? 40÷9 = ____ r ____. Answer: ____", "fill", "Answer = ____", tier="CONCEPT"),
        q("List ALL factors of 6: ____", "fill", "Factors = ____", tier="PRACTICE"),
        q("List ALL factors of 10: ____", "fill", "Factors = ____", tier="PRACTICE"),
        q("List ALL factors of 15: ____", "fill", "Factors = ____", tier="PRACTICE"),
        q("List ALL factors of 16: ____", "fill", "Factors = ____", tier="PRACTICE"),
        q("List ALL factors of 18: ____", "fill", "Factors = ____", tier="PRACTICE"),
        q("List ALL factors of 24: ____", "fill", "Factors = ____", tier="PRACTICE"),
        q("How many factors does 6 have? ____", "fill", "Answer = ____", tier="CONCEPT"),
        q("How many factors does 12 have? ____", "fill", "Answer = ____", tier="CONCEPT"),
        q("How many factors does 7 have? (7 is prime) ____", "fill", "Answer = ____", tier="CONCEPT"),
        q("Write all factor pairs of 24: ____", "fill", "Answer = ____", tier="PRACTICE"),
        q("True or False: 1 is a factor of every whole number.", "fill", "Answer = ____", tier="CONCEPT"),
        q("True or False: 6 is a factor of 30.", "fill", "Answer = ____", tier="CONCEPT"),
        q("Spot the mistake: Splitter listed the factors of 10 as 2, 5, 10. "
          "One factor is missing — which one, and why did he miss it?", "fill", "Answer = ____", tier="MASTERY"),
        q("Splitter says: 'If a number divides evenly with nothing left over, it's a factor.' "
          "Is 9 a factor of 36? Explain your answer in one line.", "fill", "Answer = ____", tier="MASTERY"),
    ]

def _L9A_2():
    return [
        cb("Common Factors", [
            "A COMMON FACTOR divides BOTH numbers exactly.",
            "Step 1: List all factors of each number.",
            "Step 2: Find numbers that appear in BOTH lists.",
        ], "Factors of 12: 1,2,3,4,6,12. Factors of 18: 1,2,3,6,9,18. Common factors: 1,2,3,6"),
        q("Factors of 8: ____", "fill", "Answer = ____"),
        q("Factors of 12: ____", "fill", "Answer = ____"),
        q("Common factors of 8 and 12: ____", "fill", "Answer = ____"),
        q("Factors of 15: ____", "fill", "Answer = ____"),
        q("Factors of 25: ____", "fill", "Answer = ____"),
        q("Common factors of 15 and 25: ____", "fill", "Answer = ____"),
        q("Factors of 18: ____", "fill", "Answer = ____"),
        q("Factors of 24: ____", "fill", "Answer = ____"),
        q("Common factors of 18 and 24: ____", "fill", "Answer = ____"),
        q("Common factors of 6 and 9: ____", "fill", "Answer = ____"),
        q("Common factors of 20 and 30: ____", "fill", "Answer = ____"),
        q("Is 4 a common factor of 16 and 20? ____", "fill", "Answer = ____"),
        q("Is 5 a common factor of 15 and 25? ____", "fill", "Answer = ____"),
        q("Is 7 a common factor of 14 and 21? ____", "fill", "Answer = ____"),
        q("Is 6 a common factor of 18 and 30? ____", "fill", "Answer = ____"),
        q("How many common factors do 8 and 12 have? ____", "fill", "Answer = ____"),
        q("True or False: 1 is always a common factor of any two numbers.", "fill", "Answer = ____"),
        q("True or False: 3 is a common factor of 12 and 18.", "fill", "Answer = ____"),
        q("True or False: 4 is a factor of both 16 and 24.", "fill", "Answer = ____"),
        q("Spot: Common factors of 6 and 9 are 1, 3, 9. What is wrong? ____", "fill", "Answer = ____"),
    ]

def _L9A_3():
    return [
        tb("Factors — Tips", [
            "Factor: divides the number with NO remainder.",
            "List all factors: try 1, 2, 3, ... up to the number. Keep those that divide exactly.",
            "Factors come in PAIRS: if a is a factor of n, then n÷a is also a factor.",
            "1 and the number itself are ALWAYS factors.",
            "Common factor: divides BOTH numbers exactly.",
        ]),
        q("List ALL factors of 30: ____", "fill", "Answer = ____"),
        q("List ALL factors of 36: ____", "fill", "Answer = ____"),
        q("List ALL factors of 48: ____", "fill", "Answer = ____"),
        q("Is 8 a factor of 48? 48÷8 = ____", "fill", "Answer = ____"),
        q("Is 7 a factor of 42? 42÷7 = ____", "fill", "Answer = ____"),
        q("Is 9 a factor of 45? 45÷9 = ____", "fill", "Answer = ____"),
        q("How many factors does 30 have? ____", "fill", "Answer = ____"),
        q("How many factors does 36 have? ____", "fill", "Answer = ____"),
        q("Common factors of 24 and 36: ____", "fill", "Answer = ____"),
        q("Common factors of 30 and 45: ____", "fill", "Answer = ____"),
        q("Common factors of 20 and 28: ____", "fill", "Answer = ____"),
        q("Write all factor pairs of 36: ____", "fill", "Answer = ____"),
        q("A number has factors 1, 2, 4, 8, 16. The number is ____", "fill", "Answer = ____"),
        q("True or False: 6 is a factor of both 24 and 30.", "fill", "Answer = ____"),
        q("True or False: Every even number has 2 as a factor.", "fill", "Answer = ____"),
        q("True or False: A prime number has exactly 2 factors.", "fill", "Answer = ____"),
        q("True or False: 12 is a factor of 36.", "fill", "Answer = ____"),
        q("True or False: Factors of 48 include 1, 2, 3, 4, 6, 8, 12, 16, 24, 48.", "fill", "Answer = ____"),
        q("Spot: Factors of 30 are 2, 3, 5, 6, 10, 15, 30. What is missing? ____", "fill", "Answer = ____"),
        q("True or False: Common factors of 24 and 36 include 12.", "fill", "Answer = ____"),
    ]

def _L9A_4():
    return [
        tb("Factors — Mastery Tips", [
            "Square numbers have an ODD number of factors (e.g. 9 has 1, 3, 9 → 3 factors).",
            "A prime number has exactly 2 factors: 1 and itself.",
            "To count factors using prime factorisation: if n = 2^a × 3^b, factors = (a+1)(b+1).",
            "Common factors of two numbers include all factors of their HCF.",
        ]),
        q("List ALL factors of 60: ____", "fill", "Answer = ____"),
        q("List ALL factors of 72: ____", "fill", "Answer = ____"),
        q("How many factors does 60 have? ____", "fill", "Answer = ____"),
        q("How many factors does 72 have? ____", "fill", "Answer = ____"),
        q("Common factors of 48 and 72: ____", "fill", "Answer = ____"),
        q("Common factors of 60 and 90: ____", "fill", "Answer = ____"),
        q("List all factors of 100: ____", "fill", "Answer = ____"),
        q("How many factors does 100 have? ____", "fill", "Answer = ____"),
        q("True or False: 9 has an odd number of factors (1, 3, 9).", "fill", "Answer = ____"),
        q("True or False: 16 has factors 1, 2, 4, 8, 16 — an odd count.", "fill", "Answer = ____"),
        q("True or False: 36 has 9 factors.", "fill", "Answer = ____"),
        q("True or False: All multiples of 12 have 12 as a factor.", "fill", "Answer = ____"),
        q("True or False: Common factors of 48 and 72 include 24.", "fill", "Answer = ____"),
        q("A classroom of 24 students can sit in equal rows. List all possible row sizes: ____", "word", "Answer = ____", "factors of 24"),
        q("Rs 60 shared equally. List all possible group sizes: ____", "word", "Answer = ____", "factors of 60"),
        q("Find a number between 20 and 30 with exactly 4 factors: ____", "fill", "Answer = ____"),
        q("True or False: 100 has exactly 9 factors.", "fill", "Answer = ____"),
        q("True or False: 72 has more factors than 60.", "fill", "Answer = ____"),
        q("Spot: Factors of 72 do not include 24. Correct? ____", "fill", "Answer = ____"),
        q("True or False: Every factor of 36 is also a factor of 72.", "fill", "Answer = ____"),
    ]


# ─── 9B: Multiples ──────────────────────────────────────────
def _L9B_1():
    return [
        cb("What are Multiples?", [
            "Multiples of n are: n×1, n×2, n×3, n×4, ...",
            "They are the numbers you say in the n-times table.",
            "To check: divide and see if the remainder is 0.",
        ], "Multiples of 4: 4, 8, 12, 16, 20, 24, 28, 32, ..."),
        cb("Checking Multiples", [
            "Is 18 a multiple of 3? 18÷3 = 6, no remainder → YES.",
            "Is 22 a multiple of 4? 22÷4 = 5 r 2 → NO.",
        ], "Is 35 a multiple of 7? 35÷7=5 → YES. Is 35 a multiple of 6? 35÷6=5 r 5 → NO"),
        q("Write first 6 multiples of 3: ____", "fill", "Answer = ____"),
        q("Write first 6 multiples of 5: ____", "fill", "Answer = ____"),
        q("Write first 6 multiples of 7: ____", "fill", "Answer = ____"),
        q("Write first 6 multiples of 9: ____", "fill", "Answer = ____"),
        q("Is 24 a multiple of 6? 24÷6 = ____. Answer: ____", "fill", "Answer = ____"),
        q("Is 35 a multiple of 8? 35÷8 = ____ r ____. Answer: ____", "fill", "Answer = ____"),
        q("Is 42 a multiple of 7? 42÷7 = ____. Answer: ____", "fill", "Answer = ____"),
        q("Is 50 a multiple of 9? 50÷9 = ____ r ____. Answer: ____", "fill", "Answer = ____"),
        q("Is 36 a multiple of 4? ____", "fill", "Answer = ____"),
        q("Is 36 a multiple of 9? ____", "fill", "Answer = ____"),
        q("Is 36 a multiple of 8? ____", "fill", "Answer = ____"),
        q("Write first 5 multiples of 11: ____", "fill", "Answer = ____"),
        q("Write first 5 multiples of 12: ____", "fill", "Answer = ____"),
        q("True or False: Every multiple of 6 is also a multiple of 2.", "fill", "Answer = ____"),
        q("True or False: Every multiple of 6 is also a multiple of 4.", "fill", "Answer = ____"),
        q("True or False: 15 is a multiple of both 3 and 5.", "fill", "Answer = ____"),
        q("Spot: Multiples of 4: 4, 8, 12, 18, 20, 24. Find the mistake. ____", "fill", "Answer = ____"),
        q("True or False: 0 is a multiple of every number.", "fill", "Answer = ____"),
        q("True or False: 72 is a multiple of both 8 and 9.", "fill", "Answer = ____"),
        q("True or False: Every multiple of 4 is also a multiple of 2.", "fill", "Answer = ____"),
    ]

def _L9B_2():
    return [
        cb("Common Multiples", [
            "A COMMON MULTIPLE appears in BOTH lists of multiples.",
            "Step 1: List multiples of each number.",
            "Step 2: Find numbers that appear in both lists.",
        ], "Multiples of 4: 4,8,12,16,20,24. Multiples of 6: 6,12,18,24. Common: 12, 24, ..."),
        q("Write first 8 multiples of 4: ____", "fill", "Answer = ____"),
        q("Write first 8 multiples of 6: ____", "fill", "Answer = ____"),
        q("Common multiples of 4 and 6 (first 3): ____", "fill", "Answer = ____"),
        q("Write first 8 multiples of 3: ____", "fill", "Answer = ____"),
        q("Write first 8 multiples of 5: ____", "fill", "Answer = ____"),
        q("Common multiples of 3 and 5 (first 3): ____", "fill", "Answer = ____"),
        q("Write first 8 multiples of 2: ____", "fill", "Answer = ____"),
        q("Write first 8 multiples of 7: ____", "fill", "Answer = ____"),
        q("Common multiples of 2 and 7 (first 3): ____", "fill", "Answer = ____"),
        q("First common multiple of 4 and 5: ____", "fill", "Answer = ____"),
        q("First common multiple of 3 and 8: ____", "fill", "Answer = ____"),
        q("First common multiple of 6 and 9: ____", "fill", "Answer = ____"),
        q("Is 36 a common multiple of 4 and 9? ____", "fill", "Answer = ____"),
        q("Is 30 a common multiple of 3 and 7? ____", "fill", "Answer = ____"),
        q("Is 60 a common multiple of 4 and 6? ____", "fill", "Answer = ____"),
        q("True or False: 12 is a common multiple of 3 and 4.", "fill", "Answer = ____"),
        q("True or False: 24 is a common multiple of 6 and 8.", "fill", "Answer = ____"),
        q("True or False: All common multiples of 3 and 5 end in 0 or 5.", "fill", "Answer = ____"),
        q("Spot: 60 is NOT a common multiple of 4 and 6. Correct? ____", "fill", "Answer = ____"),
        q("True or False: Every common multiple of 4 and 6 is also a multiple of 2.", "fill", "Answer = ____"),
    ]

def _L9B_3():
    return [
        tb("Multiples — Tips", [
            "Multiples of n: n, 2n, 3n, 4n, ... (just the n-times table).",
            "To check if k is a multiple of n: divide k by n. No remainder → YES.",
            "Common multiple: appears in BOTH times tables.",
            "Multiples go on forever. There is no largest multiple.",
            "Every multiple of n is also a multiple of every factor of n.",
        ]),
        q("Is 63 a multiple of 9? 63÷9 = ____", "fill", "Answer = ____"),
        q("Is 84 a multiple of 7? 84÷7 = ____", "fill", "Answer = ____"),
        q("Is 52 a multiple of 6? 52÷6 = ____ r ____", "fill", "Answer = ____"),
        q("Is 72 a multiple of 8? 72÷8 = ____", "fill", "Answer = ____"),
        q("Write first 5 multiples of 8 greater than 50: ____", "fill", "Answer = ____"),
        q("Write multiples of 9 between 20 and 80: ____", "fill", "Answer = ____"),
        q("Common multiples of 5 and 6 (first 3): ____", "fill", "Answer = ____"),
        q("Common multiples of 4 and 8 (first 4): ____", "fill", "Answer = ____"),
        q("First common multiple of 4 and 9: ____", "fill", "Answer = ____"),
        q("First common multiple of 5 and 8: ____", "fill", "Answer = ____"),
        q("First common multiple of 6 and 10: ____", "fill", "Answer = ____"),
        q("Bus runs every 4 min. Another every 6 min. Both leave together. Next time together = ____ min", "word", "Minutes = ____", "first common multiple of 4 and 6"),
        q("True or False: 72 is a multiple of both 8 and 9.", "fill", "Answer = ____"),
        q("True or False: All multiples of 10 are also multiples of 5.", "fill", "Answer = ____"),
        q("True or False: Every multiple of 12 is also a multiple of 6.", "fill", "Answer = ____"),
        q("True or False: Common multiples of 5 and 6 include 30, 60, 90.", "fill", "Answer = ____"),
        q("True or False: The smallest common multiple of 4 and 8 is 8.", "fill", "Answer = ____"),
        q("Spot: First common multiple of 4 and 9 is 27. Correct? Fix. ____", "fill", "Answer = ____"),
        q("List first 4 common multiples of 4 and 8: ____", "fill", "Answer = ____"),
        q("True or False: 24 is a common multiple of 4 and 8.", "fill", "Answer = ____"),
    ]

def _L9B_4():
    return [
        tb("Multiples — Mastery Tips", [
            "Common multiples of a and b are all multiples of LCM(a,b).",
            "If a is a multiple of b, then LCM(a,b) = a.",
            "To find the nth common multiple: multiply LCM by n.",
            "How many multiples of n are there up to m? Answer: m÷n (whole part).",
        ]),
        q("How many multiples of 7 are between 1 and 100? ____", "fill", "Answer = ____"),
        q("How many multiples of 9 are between 1 and 100? ____", "fill", "Answer = ____"),
        q("List all multiples of 9 between 1 and 100: ____", "fill", "Answer = ____"),
        q("Common multiples of 6 and 9 up to 100: ____", "fill", "Answer = ____"),
        q("Common multiples of 5 and 8 up to 100: ____", "fill", "Answer = ____"),
        q("The 5th common multiple of 4 and 6: ____", "fill", "Answer = ____"),
        q("The 4th common multiple of 3 and 8: ____", "fill", "Answer = ____"),
        q("First 3 common multiples of 7 and 8: ____", "fill", "Answer = ____"),
        q("First 3 common multiples of 6 and 8: ____", "fill", "Answer = ____"),
        q("Lamp flashes every 4 sec, another every 6 sec. In 1 minute, how many times do they flash together? ____", "word", "Times = ____", "60 divided by LCM(4,6)"),
        q("True or False: The 5th common multiple of 4 and 6 is 60.", "fill", "Answer = ____"),
        q("True or False: All multiples of 18 are also multiples of both 6 and 9.", "fill", "Answer = ____"),
        q("True or False: There are 14 multiples of 7 between 1 and 100.", "fill", "Answer = ____"),
        q("True or False: Common multiples of 6 and 9 are multiples of 18.", "fill", "Answer = ____"),
        q("True or False: LCM(4,8)=8 because 8 is already a multiple of 4.", "fill", "Answer = ____"),
        q("True or False: First 3 common multiples of 7 and 8 are 56, 112, 168.", "fill", "Answer = ____"),
        q("True or False: Common multiples of 5 and 8 up to 100 are 40 and 80.", "fill", "Answer = ____"),
        q("Spot: 5th common multiple of 3 and 8 is 40. Correct? (LCM=24, 5th=120) ____", "fill", "Answer = ____"),
        q("True or False: Every common multiple of 6 and 9 is also a multiple of 3.", "fill", "Answer = ____"),
        q("True or False: There are 11 multiples of 9 between 1 and 100.", "fill", "Answer = ____"),
    ]


# ─── 9C: Prime factorisation ────────────────────────────────
def _L9C_1():
    return [
        cb("Prime Factorisation", [
            "Every number can be written as a product of PRIME numbers.",
            "Use a FACTOR TREE: keep splitting until all branches are prime.",
            "Write the answer using index notation: 2×2×3 = 2²×3.",
        ], "12 = 2×6 = 2×2×3 = 2²×3"),
        cb("Factor Tree Steps", [
            "Step 1: Split the number into any two factors.",
            "Step 2: If a factor is not prime, split it again.",
            "Step 3: Stop when ALL factors are prime. Collect them.",
        ], "18 → 2×9 → 2×3×3 = 2×3²"),
        q("Complete: 8 = 2×4 = 2×2×____ = 2³", "fill", "Answer = ____"),
        q("Complete: 18 = 2×9 = 2×3×____ = 2×3²", "fill", "Answer = ____"),
        q("Check: 2×2×3 = ____. Is this 12? ____", "fill", "Answer = ____"),
        q("Prime factorisation of 12: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 20: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 24: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 30: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 36: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 45: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 48: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 60: ____", "fill", "Answer = ____"),
        q("Which is correct for 30: (a) 5×6  (b) 2×3×5  (c) 2×15? ____", "fill", "Answer = ____"),
        q("True or False: 2²×3 = 12.", "fill", "Answer = ____"),
        q("True or False: 2×3² = 18.", "fill", "Answer = ____"),
        q("True or False: Prime factorisation of 36 = 2²×3².", "fill", "Answer = ____"),
        q("True or False: 2×3² = 18. Check: 2×9 = ____", "fill", "Answer = ____"),
        q("Spot: Prime factorisation of 20 = 4×5. What is wrong? ____", "fill", "Answer = ____"),
        q("Prime factorisation of 72: ____", "fill", "Answer = ____"),
        q("True or False: 72 = 2³×3².", "fill", "Answer = ____"),
        q("True or False: 60 = 2²×3×5. Check: 4×3×5=60 ✓", "fill", "Answer = ____"),
    ]

def _L9C_2():
    return [
        cb("Using Prime Factorisation", [
            "To find the value: replace powers and multiply. 2³×5 = 8×5 = 40.",
            "ALL prime factors must be prime numbers: 2, 3, 5, 7, 11, 13, ...",
            "4×5 is NOT a prime factorisation because 4 is not prime.",
        ], "40 = 2×20 = 2×4×5 = 2×2×2×5 = 2³×5"),
        q("Prime factorisation of 40: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 50: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 56: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 90: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 84: ____", "fill", "Answer = ____"),
        q("2³×5 = ____", "fill", "Answer = ____"),
        q("2²×7 = ____", "fill", "Answer = ____"),
        q("3²×5 = ____", "fill", "Answer = ____"),
        q("2×3×5 = ____", "fill", "Answer = ____"),
        q("2²×3² = ____", "fill", "Answer = ____"),
        q("Is 2×4×3 a prime factorisation? Why not? ____", "fill", "Answer = ____"),
        q("Is 2×3×7 a prime factorisation of 42? Check: 2×3×7 = ____", "fill", "Answer = ____"),
        q("Rewrite as prime factorisation: 28 = 4×7 → ____", "fill", "Answer = ____"),
        q("Rewrite as prime factorisation: 45 = 9×5 → ____", "fill", "Answer = ____"),
        q("True or False: 2³×5 = 40.", "fill", "Answer = ____"),
        q("True or False: 2²×3² = 36.", "fill", "Answer = ____"),
        q("True or False: 90 = 2×3²×5.", "fill", "Answer = ____"),
        q("True or False: The prime factorisation of any number is unique.", "fill", "Answer = ____"),
        q("Spot: Prime factorisation of 56 = 8×7. Fix it. ____", "fill", "Answer = ____"),
        q("True or False: 84 = 2²×3×7.", "fill", "Answer = ____"),
    ]

def _L9C_3():
    return [
        tb("Prime Factorisation — Tips", [
            "Start dividing by smallest prime (2), then 3, then 5, then 7 etc.",
            "Keep dividing until you get 1. Collect all the prime divisors.",
            "Write using index notation: 2×2×2×3 = 2³×3.",
            "Check: multiply back to get original number.",
            "4, 6, 8, 9, 10 are NOT prime — always split them further.",
        ]),
        q("Prime factorisation of 32: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 54: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 75: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 98: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 120: ____", "fill", "Answer = ____"),
        q("2⁵ = ____", "fill", "Answer = ____"),
        q("2³×3² = ____", "fill", "Answer = ____"),
        q("2²×3×7 = ____", "fill", "Answer = ____"),
        q("Check: 2³×5 = ____. Is this 40? ____", "fill", "Answer = ____"),
        q("Check: 3²×5² = ____. What number is this? ____", "fill", "Answer = ____"),
        q("True or False: 32 = 2⁵.", "fill", "Answer = ____"),
        q("True or False: 54 = 2×3³.", "fill", "Answer = ____"),
        q("True or False: 75 = 3×5².", "fill", "Answer = ____"),
        q("True or False: 98 = 2×7².", "fill", "Answer = ____"),
        q("True or False: 120 = 2³×3×5.", "fill", "Answer = ____"),
        q("Write as a single number: 2⁴×3 = ____", "fill", "Answer = ____"),
        q("Write as a single number: 2×5³ = ____", "fill", "Answer = ____"),
        q("Spot: Prime factorisation of 54 = 2×27. Fix it. ____", "fill", "Answer = ____"),
        q("Spot: 120 = 2×4×3×5. Fix as proper prime factorisation. ____", "fill", "Answer = ____"),
        q("True or False: 2²×3×7 = 84.", "fill", "Answer = ____"),
    ]

def _L9C_4():
    return [
        tb("Prime Factorisation — Mastery Tips", [
            "To find HCF using prime factorisation: common primes with LOWEST powers.",
            "To find LCM using prime factorisation: all primes with HIGHEST powers.",
            "Number of factors = (a+1)(b+1)... if n = 2^a × 3^b × ...",
            "1000 = 10³ = (2×5)³ = 2³×5³.",
        ]),
        q("Prime factorisation of 144: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 180: ____", "fill", "Answer = ____"),
        q("Prime factorisation of 210: ____", "fill", "Answer = ____"),
        q("2⁴×3² = ____", "fill", "Answer = ____"),
        q("2³×3×5 = ____", "fill", "Answer = ____"),
        q("How many factors does 2³×3 have? Use (3+1)(1+1) = ____", "fill", "Answer = ____"),
        q("How many factors does 2²×3² have? Use (2+1)(2+1) = ____", "fill", "Answer = ____"),
        q("How many factors does 2⁴ have? ____", "fill", "Answer = ____"),
        q("Find n: n = 2²×3×5×7. n = ____", "fill", "n = ____"),
        q("Find n: n = 2³×3²×5. n = ____", "fill", "n = ____"),
        q("True or False: 144 = 2⁴×3².", "fill", "Answer = ____"),
        q("True or False: 180 = 2²×3²×5.", "fill", "Answer = ____"),
        q("True or False: 210 = 2×3×5×7.", "fill", "Answer = ____"),
        q("True or False: 2⁴×3² = 144.", "fill", "Answer = ____"),
        q("True or False: 2²×3² has (2+1)(2+1) = 9 factors.", "fill", "Answer = ____"),
        q("True or False: A prime number p has prime factorisation p¹.", "fill", "Answer = ____"),
        q("Write prime factorisation of 1000: ____", "fill", "Answer = ____"),
        q("True or False: 1000 = 2³×5³.", "fill", "Answer = ____"),
        q("Spot: 144 = 2³×3³. Correct? Fix. ____", "fill", "Answer = ____"),
        q("Spot: Number of factors of 2³×3 = 3×1 = 3. Correct? Fix. ____", "fill", "Answer = ____"),
    ]


# ─── 9CUM1: Mixed A+B+C ─────────────────────────────────────
def _l6_prime_factors_multiset(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def _l6_hcf(a, b):
    while b:
        a, b = b, a % b
    return a

def _l6_lcm(a, b):
    return a * b // _l6_hcf(a, b)

def _l6_is_prime(n):
    if n < 2: return False
    for k in range(2, int(n**0.5) + 1):
        if n % k == 0: return False
    return True


# ─── 9CUM1: Factor Trees (visual prime factorisation) ───────
def _L9CUM1_s(sheet):
    random.seed(900 + sheet)
    ranges = {1: (12, 40), 2: (20, 70), 3: (35, 100), 4: (50, 150)}
    lo, hi = ranges[sheet]
    items = [
        cb("Factor Trees — Prime Factorisation Visualised", [
            "A factor tree splits a number into factors, then splits those factors again, until every branch ends in a PRIME number.",
            "The prime numbers at the bottom (the leaves) are the number's prime factorisation.",
            "It doesn't matter which factor pair you start with -- you always end up with the same set of primes.",
        ], "60 = 2 x 2 x 3 x 5 (see the tree)"),
    ]
    composites = [n for n in range(lo, hi) if not _l6_is_prime(n) and n > 3]
    for _ in range(6):
        n = random.choice(composites)
        items.append(q(f"Complete the factor tree for {n}, then write its prime factorisation.", "diagram", "____",
                        "", "factor_tree", {"n": n}))
    for _ in range(6):
        n = random.choice(composites)
        items.append(q(f"Find the prime factorisation of {n}.", "fill", "Answer = ____"))
    for _ in range(4):
        n = random.choice(composites)
        pf = _l6_prime_factors_multiset(n)
        correct = " x ".join(str(p) for p in pf)
        wrong_pf = pf[:-1] + [pf[-1] + 1] if len(pf) > 1 else [pf[0], pf[0]]
        wrong = " x ".join(str(p) for p in wrong_pf)
        shown = correct if random.random() > 0.4 else wrong
        items.append(q(f"True or False: {n} = {shown}", "fill", "Answer = ____"))
    for _ in range(4):
        n = random.choice(composites)
        pf = _l6_prime_factors_multiset(n)
        if len(pf) > 1:
            bad = pf[:]; bad[0] = bad[0] + 1
            bad_str = " x ".join(str(p) for p in bad)
        else:
            bad_str = f"{n} (no factors shown)"
        items.append(q(f"Spot the mistake: a student wrote {n} = {bad_str}. What's wrong? Give the correct factorisation. ____", "fill", "Answer = ____"))
    return items

# ─── 9D: HCF ────────────────────────────────────────────────
def _L9D_1():
    return [
        cb("Highest Common Factor (HCF)", [
            "HCF = the LARGEST number that divides BOTH numbers exactly.",
            "Step 1: List ALL factors of each number.",
            "Step 2: Find all COMMON factors.",
            "Step 3: The LARGEST common factor = HCF.",
        ], "HCF(12,18): Factors of 12=1,2,3,4,6,12. Factors of 18=1,2,3,6,9,18. Common=1,2,3,6. HCF=6"),
        q("Factors of 8: ____. Factors of 12: ____. HCF(8,12) = ____", "fill", "HCF = ____"),
        q("Factors of 10: ____. Factors of 15: ____. HCF(10,15) = ____", "fill", "HCF = ____"),
        q("Factors of 12: ____. Factors of 20: ____. HCF(12,20) = ____", "fill", "HCF = ____"),
        q("Factors of 16: ____. Factors of 24: ____. HCF(16,24) = ____", "fill", "HCF = ____"),
        q("Factors of 18: ____. Factors of 27: ____. HCF(18,27) = ____", "fill", "HCF = ____"),
        q("HCF(6, 9) = ____", "fill", "HCF = ____"),
        q("HCF(8, 20) = ____", "fill", "HCF = ____"),
        q("HCF(15, 25) = ____", "fill", "HCF = ____"),
        q("HCF(14, 21) = ____", "fill", "HCF = ____"),
        q("HCF(24, 36) = ____", "fill", "HCF = ____"),
        q("HCF(20, 30) = ____", "fill", "HCF = ____"),
        q("HCF(9, 12) = ____", "fill", "HCF = ____"),
        q("HCF(7, 14) = ____", "fill", "HCF = ____"),
        q("HCF(5, 25) = ____", "fill", "HCF = ____"),
        q("HCF(18, 30) = ____", "fill", "HCF = ____"),
        q("True or False: HCF(12,18) = 6.", "fill", "Answer = ____"),
        q("True or False: HCF(8,12) = 4.", "fill", "Answer = ____"),
        q("Spot: HCF(16,24) = 8. Correct? ____", "fill", "Answer = ____"),
        q("Spot: HCF(15,25) = 5. Correct? ____", "fill", "Answer = ____"),
        q("True or False: HCF of any two numbers is at least 1.", "fill", "Answer = ____"),
    ]

def _L9D_2():
    return [
        cb("HCF by Prime Factorisation", [
            "Step 1: Write prime factorisation of EACH number.",
            "Step 2: Find common prime factors.",
            "Step 3: Take the LOWEST power of each common prime.",
            "Step 4: Multiply these together = HCF.",
        ], "HCF(12,18): 12=2²×3, 18=2×3². Common primes: 2(take 2¹), 3(take 3¹). HCF=2×3=6"),
        q("HCF(24,36): 24=2³×3, 36=2²×3². Common primes: ____. HCF = ____", "fill", "HCF = ____"),
        q("HCF(20,30): 20=2²×5, 30=2×3×5. Common primes: ____. HCF = ____", "fill", "HCF = ____"),
        q("HCF(48,72): 48=2⁴×3, 72=2³×3². Common primes: ____. HCF = ____", "fill", "HCF = ____"),
        q("HCF(45,60): 45=3²×5, 60=2²×3×5. Common primes: ____. HCF = ____", "fill", "HCF = ____"),
        q("HCF(42,70): 42=2×3×7, 70=2×5×7. Common primes: ____. HCF = ____", "fill", "HCF = ____"),
        q("HCF(36, 48) using prime factorisation: ____", "fill", "HCF = ____"),
        q("HCF(60, 90) using prime factorisation: ____", "fill", "HCF = ____"),
        q("HCF(84, 126) using prime factorisation: ____", "fill", "HCF = ____"),
        q("HCF(75, 100) using prime factorisation: ____", "fill", "HCF = ____"),
        q("HCF(56, 84) using prime factorisation: ____", "fill", "HCF = ____"),
        q("If HCF(a,b)=1, the numbers are called CO-PRIME. Are 8 and 9 co-prime? ____", "fill", "Answer = ____"),
        q("Are 6 and 35 co-prime? ____", "fill", "Answer = ____"),
        q("True or False: HCF(24,36) = 12.", "fill", "Answer = ____"),
        q("True or False: HCF(45,60) = 15.", "fill", "Answer = ____"),
        q("True or False: HCF(42,70) = 14.", "fill", "Answer = ____"),
        q("True or False: HCF(a,b) is never greater than the smaller of a and b.", "fill", "Answer = ____"),
        q("Spot: HCF(48,72) = 24. Correct? ____", "fill", "Answer = ____"),
        q("Spot: HCF(84,126) = 21. Correct? ____", "fill", "Answer = ____"),
        q("True or False: HCF(60,90) = 30.", "fill", "Answer = ____"),
        q("True or False: HCF(a,b) = HCF(b,a) — order does not matter.", "fill", "Answer = ____"),
    ]

def _L9D_3():
    return [
        tb("HCF — Tips", [
            "Listing method: list all factors, find common ones, take the largest.",
            "Prime factorisation method: common primes with LOWEST powers, multiply.",
            "HCF tells you the largest equal group size when sharing two quantities.",
            "HCF(a,a) = a. HCF(a,b) = a if a divides b.",
            "If HCF(a,b)=1, the numbers are co-prime.",
        ]),
        q("HCF(16, 40) = ____", "fill", "HCF = ____"),
        q("HCF(21, 35) = ____", "fill", "HCF = ____"),
        q("HCF(32, 48) = ____", "fill", "HCF = ____"),
        q("HCF(54, 72) = ____", "fill", "HCF = ____"),
        q("HCF(28, 42) = ____", "fill", "HCF = ____"),
        q("HCF(30, 45) = ____", "fill", "HCF = ____"),
        q("HCF(64, 96) = ____", "fill", "HCF = ____"),
        q("HCF(75, 100) = ____", "fill", "HCF = ____"),
        q("HCF(8, 9) = ____  (co-prime)", "fill", "HCF = ____"),
        q("HCF(11, 22) = ____  (22 = 2×11)", "fill", "HCF = ____"),
        q("Ravi has 24 sweets and 36 biscuits. Share equally. Largest group size = HCF(24,36) = ____", "word", "Group size = ____", "HCF of 24 and 36"),
        q("Two ropes: 48m and 72m. Cut equal pieces, no waste. Longest piece = HCF(48,72) = ____ m", "word", "Length = ____ m", "HCF of 48 and 72"),
        q("True or False: HCF(16,40) = 8.", "fill", "Answer = ____"),
        q("True or False: HCF(21,35) = 7.", "fill", "Answer = ____"),
        q("True or False: HCF(32,48) = 16.", "fill", "Answer = ____"),
        q("True or False: HCF(54,72) = 18.", "fill", "Answer = ____"),
        q("True or False: HCF(a,b) = HCF(b,a).", "fill", "Answer = ____"),
        q("True or False: HCF(75,100) = 25.", "fill", "Answer = ____"),
        q("Spot: HCF(54,72) = 18. Correct? ____", "fill", "Answer = ____"),
        q("True or False: HCF(64,96) = 32.", "fill", "Answer = ____"),
    ]

def _L9D_4():
    return [
        tb("HCF — Mastery Tips", [
            "HCF(a,b,c): find common prime factors of ALL three, take lowest powers.",
            "Word problems: largest equal groups, cut equal pieces, maximum tile size → HCF.",
            "HCF(a,b) × LCM(a,b) = a × b. Use this to find LCM when HCF is known.",
        ]),
        q("HCF(12, 18, 24) = ____", "fill", "HCF = ____"),
        q("HCF(30, 45, 60) = ____", "fill", "HCF = ____"),
        q("HCF(36, 60, 84) = ____", "fill", "HCF = ____"),
        q("HCF(48, 72, 96) = ____", "fill", "HCF = ____"),
        q("HCF(a,b)=12 and a×b=288. LCM(a,b) = 288÷12 = ____", "fill", "LCM = ____"),
        q("HCF(a,b)=8 and a×b=192. LCM(a,b) = ____", "fill", "LCM = ____"),
        q("36 boys, 54 girls, 72 teachers. Equal teams. Largest team = HCF(36,54,72) = ____", "word", "Team size = ____", "HCF of 36, 54, 72"),
        q("Cloth: 60m, 84m, 108m. Cut equal pieces, no waste. Longest piece = ____ m", "word", "Length = ____ m", "HCF of 60, 84, 108"),
        q("True or False: HCF(12,18,24) = 6.", "fill", "Answer = ____"),
        q("True or False: HCF(30,45,60) = 15.", "fill", "Answer = ____"),
        q("True or False: HCF(36,60,84) = 12.", "fill", "Answer = ____"),
        q("True or False: HCF(48,72,96) = 24.", "fill", "Answer = ____"),
        q("Verify: HCF(12,18)=6, LCM=36. Check: 6×36=____ and 12×18=____", "fill", "Answer = ____"),
        q("True or False: HCF(a,b) × LCM(a,b) = a × b always.", "fill", "Answer = ____"),
        q("Are 35 and 36 co-prime? ____", "fill", "Answer = ____"),
        q("Are 14 and 21 co-prime? ____", "fill", "Answer = ____"),
        q("True or False: Co-prime numbers always have HCF = 1.", "fill", "Answer = ____"),
        q("Spot: HCF(36,60,84) = 24. Correct? Fix. ____", "fill", "Answer = ____"),
        q("Spot: HCF(a,b)=8, a×b=192, so LCM=24. Correct? ____", "fill", "Answer = ____"),
        q("True or False: HCF of three numbers is never larger than the smallest of them.", "fill", "Answer = ____"),
    ]


# ─── 9E: LCM ────────────────────────────────────────────────
def _L9E_1():
    return [
        cb("Lowest Common Multiple (LCM)", [
            "LCM = the SMALLEST number that is a multiple of BOTH numbers.",
            "Step 1: List multiples of each number.",
            "Step 2: Find the FIRST number in BOTH lists.",
        ], "LCM(4,6): Multiples of 4: 4,8,12,16. Multiples of 6: 6,12,18. First common: 12. LCM=12"),
        q("Multiples of 3: ____. Multiples of 4: ____. LCM(3,4) = ____", "fill", "LCM = ____"),
        q("Multiples of 4: ____. Multiples of 5: ____. LCM(4,5) = ____", "fill", "LCM = ____"),
        q("Multiples of 2: ____. Multiples of 7: ____. LCM(2,7) = ____", "fill", "LCM = ____"),
        q("Multiples of 5: ____. Multiples of 6: ____. LCM(5,6) = ____", "fill", "LCM = ____"),
        q("Multiples of 3: ____. Multiples of 8: ____. LCM(3,8) = ____", "fill", "LCM = ____"),
        q("LCM(4, 6) = ____", "fill", "LCM = ____"),
        q("LCM(3, 5) = ____", "fill", "LCM = ____"),
        q("LCM(4, 10) = ____", "fill", "LCM = ____"),
        q("LCM(6, 9) = ____", "fill", "LCM = ____"),
        q("LCM(8, 12) = ____", "fill", "LCM = ____"),
        q("LCM(5, 10) = ____", "fill", "LCM = ____"),
        q("LCM(3, 9) = ____", "fill", "LCM = ____"),
        q("LCM(7, 14) = ____", "fill", "LCM = ____"),
        q("LCM(6, 8) = ____", "fill", "LCM = ____"),
        q("LCM(9, 12) = ____", "fill", "LCM = ____"),
        q("True or False: LCM(4,6) = 12.", "fill", "Answer = ____"),
        q("True or False: LCM(5,10) = 10.", "fill", "Answer = ____"),
        q("Spot: LCM(3,9) = 27. Correct? Fix. ____", "fill", "Answer = ____"),
        q("Spot: LCM(6,8) = 48. Correct? Fix. ____", "fill", "Answer = ____"),
        q("True or False: LCM of two numbers is always at least as large as both of them.", "fill", "Answer = ____"),
    ]

def _L9E_2():
    return [
        cb("LCM by Prime Factorisation", [
            "Step 1: Write prime factorisation of each number.",
            "Step 2: List ALL prime factors from both.",
            "Step 3: Take the HIGHEST power of each prime.",
            "Step 4: Multiply these together = LCM.",
        ], "LCM(12,18): 12=2²×3, 18=2×3². All primes: 2(take 2²), 3(take 3²). LCM=4×9=36"),
        q("LCM(12,18): 12=2²×3, 18=2×3². Highest powers: ____. LCM = ____", "fill", "LCM = ____"),
        q("LCM(20,30): 20=2²×5, 30=2×3×5. Highest powers: ____. LCM = ____", "fill", "LCM = ____"),
        q("LCM(24,36): 24=2³×3, 36=2²×3². Highest powers: ____. LCM = ____", "fill", "LCM = ____"),
        q("LCM(15,20): 15=3×5, 20=2²×5. Highest powers: ____. LCM = ____", "fill", "LCM = ____"),
        q("LCM(14,21): 14=2×7, 21=3×7. Highest powers: ____. LCM = ____", "fill", "LCM = ____"),
        q("LCM(8, 12) by prime factorisation: ____", "fill", "LCM = ____"),
        q("LCM(15, 25) by prime factorisation: ____", "fill", "LCM = ____"),
        q("LCM(16, 24) by prime factorisation: ____", "fill", "LCM = ____"),
        q("LCM(18, 27) by prime factorisation: ____", "fill", "LCM = ____"),
        q("LCM(30, 45) by prime factorisation: ____", "fill", "LCM = ____"),
        q("True or False: LCM(12,18) = 36.", "fill", "Answer = ____"),
        q("True or False: LCM(20,30) = 60.", "fill", "Answer = ____"),
        q("True or False: LCM(24,36) = 72.", "fill", "Answer = ____"),
        q("True or False: LCM(14,21) = 42.", "fill", "Answer = ____"),
        q("True or False: LCM(15,25) = 75.", "fill", "Answer = ____"),
        q("Spot: LCM(12,18) = 12. Correct? Fix. ____", "fill", "Answer = ____"),
        q("Spot: LCM(16,24) = 48. Correct? ____", "fill", "Answer = ____"),
        q("True or False: LCM(18,27) = 54.", "fill", "Answer = ____"),
        q("True or False: LCM(30,45) = 90.", "fill", "Answer = ____"),
        q("True or False: LCM(a,b) is always a multiple of both a and b.", "fill", "Answer = ____"),
    ]

def _L9E_3():
    return [
        tb("LCM — Tips", [
            "Listing method: write multiples of both, find first common one.",
            "Prime factorisation: ALL primes from both, take HIGHEST powers.",
            "LCM tells you when two events next happen at the SAME time.",
            "If one number is a multiple of the other, LCM = the larger number.",
            "LCM(a,b) = a×b ÷ HCF(a,b).",
        ]),
        q("LCM(10, 15) = ____", "fill", "LCM = ____"),
        q("LCM(12, 16) = ____", "fill", "LCM = ____"),
        q("LCM(9, 15) = ____", "fill", "LCM = ____"),
        q("LCM(8, 18) = ____", "fill", "LCM = ____"),
        q("LCM(6, 14) = ____", "fill", "LCM = ____"),
        q("LCM(20, 25) = ____", "fill", "LCM = ____"),
        q("LCM(12, 15) = ____", "fill", "LCM = ____"),
        q("LCM(7, 11) = ____  (both prime, so LCM = 7×11)", "fill", "LCM = ____"),
        q("LCM(15, 20) = ____", "fill", "LCM = ____"),
        q("LCM(24, 40) = ____", "fill", "LCM = ____"),
        q("Bus A: every 12 min. Bus B: every 15 min. Next together = LCM(12,15) = ____ min", "word", "Minutes = ____", "LCM of 12 and 15"),
        q("Bell 1 rings every 6 min. Bell 2 every 8 min. Both ring at 9am. Next both ring = ____ min later", "word", "Minutes = ____", "LCM of 6 and 8"),
        q("True or False: LCM(10,15) = 30.", "fill", "Answer = ____"),
        q("True or False: LCM(9,15) = 45. Fix if wrong. ____", "fill", "Answer = ____"),
        q("True or False: LCM(12,16) = 48.", "fill", "Answer = ____"),
        q("True or False: LCM(8,18) = 72.", "fill", "Answer = ____"),
        q("True or False: LCM(6,14) = 42.", "fill", "Answer = ____"),
        q("True or False: LCM(20,25) = 100.", "fill", "Answer = ____"),
        q("True or False: If both numbers are prime, LCM = their product.", "fill", "Answer = ____"),
        q("True or False: LCM(24,40) = 120.", "fill", "Answer = ____"),
    ]

def _L9E_4():
    return [
        tb("LCM — Mastery Tips", [
            "LCM(a,b,c): ALL primes from all three, take HIGHEST powers.",
            "Formula: LCM(a,b) = a×b ÷ HCF(a,b).",
            "Word problems: when do they meet again, smallest number divisible by both → LCM.",
            "LCM(a,b) × HCF(a,b) = a × b.",
        ]),
        q("LCM(4, 6, 9) = ____", "fill", "LCM = ____"),
        q("LCM(6, 8, 12) = ____", "fill", "LCM = ____"),
        q("LCM(5, 6, 10) = ____", "fill", "LCM = ____"),
        q("LCM(3, 4, 5) = ____", "fill", "LCM = ____"),
        q("LCM(a,b)=60, HCF(a,b)=4. Then a×b = LCM×HCF = ____", "fill", "a×b = ____"),
        q("LCM(a,b)=36, HCF(a,b)=6. Then a×b = ____", "fill", "a×b = ____"),
        q("Three bells: every 6, 8, 12 min. All ring now. Next all ring = LCM(6,8,12) = ____ min", "word", "Minutes = ____", "LCM of 6, 8, 12"),
        q("Smallest number divisible by 4, 6, and 9 = LCM(4,6,9) = ____", "fill", "Answer = ____"),
        q("Use formula: LCM(18,24) = 18×24÷HCF(18,24) = 432÷6 = ____", "fill", "LCM = ____"),
        q("Use formula: LCM(15,20) = 15×20÷HCF(15,20) = 300÷5 = ____", "fill", "LCM = ____"),
        q("True or False: LCM(4,6,9) = 36.", "fill", "Answer = ____"),
        q("True or False: LCM(6,8,12) = 24.", "fill", "Answer = ____"),
        q("True or False: LCM(5,6,10) = 30.", "fill", "Answer = ____"),
        q("True or False: LCM(3,4,5) = 60.", "fill", "Answer = ____"),
        q("Verify: LCM(4,6)=12, HCF(4,6)=2. Check: 12×2=____ and 4×6=____", "fill", "Answer = ____"),
        q("True or False: LCM(a,b,c) is divisible by each of a, b, and c.", "fill", "Answer = ____"),
        q("True or False: LCM(18,24) = 72.", "fill", "Answer = ____"),
        q("True or False: LCM(15,20) = 60.", "fill", "Answer = ____"),
        q("Spot: LCM(4,6,9) = 72. Correct? Fix. ____", "fill", "Answer = ____"),
        q("True or False: LCM(a,b) = a×b ÷ HCF(a,b).", "fill", "Answer = ____"),
    ]


# ─── 9F: Word problems ──────────────────────────────────────
def _L9F_1():
    return [
        cb("HCF and LCM Word Problems — Which to use?", [
            "HCF problems: dividing/sharing/cutting into EQUAL parts. Find MAXIMUM.",
            "  Keywords: largest, maximum, greatest, equal pieces with no waste.",
            "LCM problems: things happening together in CYCLES. Find NEXT TIME.",
            "  Keywords: smallest, when will they meet again, next time together.",
        ], "24 sweets, 36 biscuits shared equally → HCF(24,36)=12 (max group size)"),
        q("Ravi has 12 pens and 18 pencils. Equal bundles. Max bundle size = HCF(12,18) = ____", "word", "Bundle size = ____", "HCF of 12 and 18"),
        q("Two ropes: 24m and 36m. Cut equal pieces, no waste. Longest piece = HCF(24,36) = ____ m", "word", "Piece = ____ m", "HCF of 24 and 36"),
        q("48 boys and 60 girls. Equal teams, no mixing. Largest team = HCF(48,60) = ____", "word", "Team size = ____", "HCF of 48 and 60"),
        q("24 red and 40 blue marbles in equal bags. Max bag size = HCF(24,40) = ____", "word", "Bag size = ____", "HCF of 24 and 40"),
        q("Floor 36cm × 48cm tiled with square tiles, no cutting. Largest tile side = HCF(36,48) = ____ cm", "word", "Side = ____ cm", "HCF of 36 and 48"),
        q("Bus A every 10 min. Bus B every 15 min. Both leave at 9am. Next together = LCM(10,15) = ____ min later", "word", "Minutes = ____", "LCM of 10 and 15"),
        q("Ravi saves every 3 days. Meena every 4 days. Both save today. Next together = LCM(3,4) = ____ days", "word", "Days = ____", "LCM of 3 and 4"),
        q("Bell A every 6 min. Bell B every 8 min. Both ring at noon. Next both ring = LCM(6,8) = ____ min later", "word", "Minutes = ____", "LCM of 6 and 8"),
        q("Smallest number divisible by both 6 and 9 = LCM(6,9) = ____", "word", "Number = ____", "LCM of 6 and 9"),
        q("Smallest number exactly divisible by 4, 5, and 6 = LCM(4,5,6) = ____", "word", "Number = ____", "LCM of 4, 5, 6"),
        q("Is this HCF or LCM? Two ropes cut into equal pieces, no waste. ____", "fill", "Answer = ____"),
        q("Is this HCF or LCM? When will both bells ring together again? ____", "fill", "Answer = ____"),
        q("Is this HCF or LCM? Largest team from 24 boys and 36 girls. ____", "fill", "Answer = ____"),
        q("Is this HCF or LCM? Smallest number divisible by both 8 and 12. ____", "fill", "Answer = ____"),
        q("True or False: HCF(12,18)=6 means max bundle size = 6.", "fill", "Answer = ____"),
        q("True or False: LCM(10,15)=30 means buses next meet after 30 minutes.", "fill", "Answer = ____"),
        q("Spot: Longest equal piece from 24m and 36m = LCM(24,36)=72m. Correct? Fix. ____", "fill", "Answer = ____"),
        q("Spot: Next time bells ring together = HCF(6,8)=2 min. Correct? Fix. ____", "fill", "Answer = ____"),
        q("True or False: LCM(4,5,6) = 60.", "fill", "Answer = ____"),
        q("True or False: HCF(48,60) = 12.", "fill", "Answer = ____"),
    ]

def _L9F_2():
    return [
        cb("Identifying HCF vs LCM", [
            "HCF: you are SPLITTING something into equal groups → find LARGEST group.",
            "LCM: you need things to COINCIDE or fit → find SMALLEST common value.",
            "Read carefully. Underline key words before solving.",
        ], "Sharing equally → HCF. Meeting together → LCM. Largest piece → HCF. Smallest common → LCM"),
        q("36 students, 60 chairs divided equally. Max per room = HCF(36,60) = ____", "word", "Per room = ____", "HCF of 36 and 60"),
        q("Three strings: 45m, 60m, 75m. Equal pieces, no waste. Longest = HCF(45,60,75) = ____ m", "word", "Length = ____ m", "HCF of 45, 60, 75"),
        q("Rs 72 and Rs 108 shared equally. Max equal share = HCF(72,108) = Rs ____", "word", "Share = Rs ____", "HCF of 72 and 108"),
        q("Floor 72cm × 90cm. Largest square tiles, no cutting. Tile side = HCF(72,90) = ____ cm", "word", "Side = ____ cm", "HCF of 72 and 90"),
        q("Traffic light: red every 40 sec, green every 60 sec. Both green now. Next both green = LCM(40,60) = ____ sec", "word", "Seconds = ____", "LCM of 40 and 60"),
        q("Ravi runs every 4 days. Meena every 6 days. Both run today. Next run together = LCM(4,6) = ____ days", "word", "Days = ____", "LCM of 4 and 6"),
        q("Smallest number divisible by 4, 6, and 10 = LCM(4,6,10) = ____", "word", "Number = ____", "LCM of 4, 6, 10"),
        q("HCF(45,60,75) = ____", "fill", "HCF = ____"),
        q("HCF(72,108) = ____", "fill", "HCF = ____"),
        q("LCM(40,60) = ____", "fill", "LCM = ____"),
        q("LCM(4,6,10) = ____", "fill", "LCM = ____"),
        q("True or False: HCF(36,60) = 12.", "fill", "Answer = ____"),
        q("True or False: HCF(72,90) = 18.", "fill", "Answer = ____"),
        q("True or False: LCM(40,60) = 120.", "fill", "Answer = ____"),
        q("Spot: Strings 45,60,75: HCF = 20. Correct? Fix. ____", "fill", "Answer = ____"),
        q("True or False: HCF(72,108) = 36.", "fill", "Answer = ____"),
        q("True or False: LCM(4,6,10) = 60.", "fill", "Answer = ____"),
        q("True or False: HCF answer is always ≤ the smallest of the numbers.", "fill", "Answer = ____"),
        q("True or False: LCM answer is always ≥ the largest of the numbers.", "fill", "Answer = ____"),
        q("True or False: HCF(45,60,75) = 15.", "fill", "Answer = ____"),
    ]

def _L9F_3():
    return [
        tb("HCF and LCM Word Problems — Tips", [
            "HCF: dividing/sharing/cutting → LARGEST equal piece. Use HCF.",
            "LCM: meeting/coinciding/smallest that fits → NEXT TIME. Use LCM.",
            "Underline key words. Identify the numbers. Decide: HCF or LCM. Calculate.",
            "Check: HCF answer ≤ both numbers. LCM answer ≥ both numbers.",
        ]),
        q("Garlands: 48 red and 72 white flowers. Equal garlands. Max per garland = HCF(48,72) = ____", "word", "Flowers = ____", "HCF of 48 and 72"),
        q("Two clocks: one chimes every 12 min, another every 18 min. Next chime together = LCM(12,18) = ____ min", "word", "Minutes = ____", "LCM of 12 and 18"),
        q("Three friends: Ravi every 3 days, Meena every 5 days, Arjun every 6 days. All meet today. Next all meet = ____ days", "word", "Days = ____", "LCM of 3, 5, 6"),
        q("Square tiles for 120cm × 180cm floor. Largest tile, no cutting = HCF(120,180) = ____ cm", "word", "Side = ____ cm", "HCF of 120 and 180"),
        q("HCF(48,72) = ____", "fill", "HCF = ____"),
        q("LCM(12,18) = ____", "fill", "LCM = ____"),
        q("LCM(3,5,6) = ____", "fill", "LCM = ____"),
        q("HCF(120,180) = ____", "fill", "HCF = ____"),
        q("True or False: HCF(48,72)=24 means max garland size is 24.", "fill", "Answer = ____"),
        q("True or False: LCM(12,18)=36 means next chime together after 36 min.", "fill", "Answer = ____"),
        q("True or False: LCM(3,5,6)=30 means all three friends meet after 30 days.", "fill", "Answer = ____"),
        q("True or False: HCF(120,180)=60 means largest tile is 60cm × 60cm.", "fill", "Answer = ____"),
        q("Spot: Garlands HCF(48,72)=12. Correct? Fix. ____", "fill", "Answer = ____"),
        q("Spot: Three friends 3,5,6 meet after LCM=15 days. Correct? Fix. ____", "fill", "Answer = ____"),
        q("True or False: LCM(8,12) = 24.", "fill", "Answer = ____"),
        q("True or False: LCM answer is always at least as large as each number.", "fill", "Answer = ____"),
        q("True or False: HCF answer is always at most as large as each number.", "fill", "Answer = ____"),
        q("Write a word problem using HCF(24,36)=12 as its answer.", "fill", "Answer = ____"),
        q("Write a word problem using LCM(6,9)=18 as its answer.", "fill", "Answer = ____"),
        q("True or False: For finding the largest tile size, we use HCF of the two dimensions.", "fill", "Answer = ____"),
    ]

def _L9F_4():
    return [
        tb("HCF and LCM Word Problems — Mastery Tips", [
            "Multi-step: find HCF or LCM, then use the result in another calculation.",
            "HCF × LCM = a × b. Use to find one when you know the other.",
            "How many pieces = original length ÷ HCF.",
            "How many times meet = total time ÷ LCM.",
        ]),
        q("HCF(60,90)=30. Pieces from 60m rope: 60÷30=____. Pieces from 90m rope: 90÷30=____", "word", "Answer = ____", "60÷30 and 90÷30"),
        q("24 boys, 36 girls, HCF=12. Teams=____. Boys per team=____. Girls per team=____", "word", "Answer = ____", "24÷12 and 36÷12"),
        q("LCM(15,20)=60. In 3 hours (180 min), times they ring together: 180÷60 = ____", "word", "Times = ____", "180 ÷ 60"),
        q("LCM(a,b)=72 and HCF(a,b)=6. Find a×b. ____", "fill", "a×b = ____"),
        q("HCF(a,b)=8 and a×b=192. Find LCM(a,b). ____", "fill", "LCM = ____"),
        q("HCF(84,126)=42. LCM(84,126)=84×126÷42=____", "fill", "LCM = ____"),
        q("Three pipes: 36cm, 54cm, 90cm. Max equal length = HCF(36,54,90) = ____ cm. Total pieces = ____", "word", "Length=____ Pieces=____", "HCF and count"),
        q("True or False: LCM(15,20)=60, so in 3 hours they ring together 3 times.", "fill", "Answer = ____"),
        q("True or False: HCF(60,90)=30, so 60÷30=2 pieces from 60m rope.", "fill", "Answer = ____"),
        q("True or False: LCM(a,b) × HCF(a,b) = a × b always.", "fill", "Answer = ____"),
        q("True or False: HCF(a,b)=8, a×b=192 gives LCM=24.", "fill", "Answer = ____"),
        q("True or False: HCF(36,54,90) = 18.", "fill", "Answer = ____"),
        q("Spot: 24 boys, 36 girls, HCF=12: 12 teams, each with 2 boys and 3 girls. Correct? ____", "fill", "Answer = ____"),
        q("True or False: LCM(a,b) = a×b ÷ HCF(a,b).", "fill", "Answer = ____"),
        q("Find LCM(12,15) using formula: HCF=3. LCM=12×15÷3=____", "fill", "LCM = ____"),
        q("Find LCM(8,14) using formula: HCF=2. LCM=8×14÷2=____", "fill", "LCM = ____"),
        q("True or False: LCM(12,15) = 60.", "fill", "Answer = ____"),
        q("True or False: HCF(84,126) = 42.", "fill", "Answer = ____"),
        q("True or False: LCM(84,126) = 252.", "fill", "Answer = ____"),
        q("True or False: LCM(8,14) = 56.", "fill", "Answer = ____"),
    ]


# ─── 9CUM2: Mixed D+E+F ─────────────────────────────────────
# ─── 9CUM2: HCF & LCM via Venn Diagrams ──────────────────────
def _L9CUM2_s(sheet):
    random.seed(910 + sheet)
    ranges = {1: (20, 60), 2: (30, 90), 3: (45, 120), 4: (60, 200)}
    lo, hi = ranges[sheet]
    items = [
        cb("HCF & LCM via Venn Diagrams", [
            "Write each number's prime factors in a Venn diagram: shared primes go in the OVERLAP, unique primes go in their own circle.",
            "HCF = multiply everything in the OVERLAP.",
            "LCM = multiply EVERYTHING in the whole diagram (both circles combined).",
        ], "24=2x2x2x3, 36=2x2x3x3 -> overlap: 2,2,3 (HCF=12); all: 2,2,2,3,3 (LCM=72)"),
    ]

    def make_pair():
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        while a == b:
            b = random.randint(lo, hi)
        return a, b

    def venn_regions(a, b):
        from collections import Counter
        fa, fb = Counter(_l6_prime_factors_multiset(a)), Counter(_l6_prime_factors_multiset(b))
        common = fa & fb
        a_only = fa - fb
        b_only = fb - fa
        return sorted(a_only.elements()), sorted(common.elements()), sorted(b_only.elements())

    for _ in range(6):
        a, b = make_pair()
        a_only, common, b_only = venn_regions(a, b)
        items.append(q(f"Use the Venn diagram to find HCF({a},{b}) and LCM({a},{b}).", "diagram", "____", "",
                        "venn_two", {"a_only": a_only, "common": common, "b_only": b_only, "label_a": str(a), "label_b": str(b)}))
    for _ in range(5):
        a, b = make_pair()
        items.append(q(f"HCF({a}, {b}) = ____", "fill", "HCF = ____"))
    for _ in range(5):
        a, b = make_pair()
        items.append(q(f"LCM({a}, {b}) = ____", "fill", "LCM = ____"))
    for _ in range(2):
        a, b = make_pair()
        h = _l6_hcf(a, b)
        shown = h if random.random() > 0.4 else h + random.choice([2, -3])
        items.append(q(f"True or False: HCF({a},{b}) = {shown}.", "fill", "Answer = ____"))
    for _ in range(2):
        a, b = make_pair()
        l = _l6_lcm(a, b)
        shown = l if random.random() > 0.4 else l + random.choice([10, -15])
        items.append(q(f"True or False: LCM({a},{b}) = {shown}.", "fill", "Answer = ____"))
    return items

# ─── 9G: Applications ───────────────────────────────────────
def _L9G_1():
    return [
        cb("Applying HCF — Simplifying Fractions", [
            "To simplify a fraction: divide numerator AND denominator by HCF.",
            "Simplify 12/18: HCF(12,18)=6. 12÷6=2, 18÷6=3. Answer: 2/3.",
            "The simplified fraction has the same value.",
        ], "Simplify 8/12: HCF(8,12)=4. 8÷4=2, 12÷4=3. Answer: 2/3"),
        q("Simplify 6/9. HCF(6,9)=____. 6÷____=____, 9÷____=____. Answer: ____", "fill", "Answer = ____"),
        q("Simplify 8/12. HCF(8,12)=____. Answer: ____", "fill", "Answer = ____"),
        q("Simplify 15/20. HCF(15,20)=____. Answer: ____", "fill", "Answer = ____"),
        q("Simplify 18/24. HCF(18,24)=____. Answer: ____", "fill", "Answer = ____"),
        q("Simplify 24/36. HCF(24,36)=____. Answer: ____", "fill", "Answer = ____"),
        q("Simplify 30/45. HCF(30,45)=____. Answer: ____", "fill", "Answer = ____"),
        q("Simplify ratio 8:12. HCF(8,12)=4. Ratio: ____:____", "fill", "Answer = ____"),
        q("Simplify ratio 15:25. HCF(15,25)=5. Ratio: ____:____", "fill", "Answer = ____"),
        q("Simplify ratio 18:24. HCF(18,24)=6. Ratio: ____:____", "fill", "Answer = ____"),
        q("Simplify ratio 20:30. HCF=____. Ratio: ____:____", "fill", "Answer = ____"),
        q("True or False: Simplify 12/18 = 2/3 using HCF = 6.", "fill", "Answer = ____"),
        q("True or False: Simplify 15/20 = 3/4 using HCF = 5.", "fill", "Answer = ____"),
        q("True or False: Ratio 8:12 simplifies to 2:3.", "fill", "Answer = ____"),
        q("True or False: Ratio 15:25 simplifies to 3:5.", "fill", "Answer = ____"),
        q("Spot: Simplify 8/12 using HCF=3: 8/12=8/3. Correct? Fix. ____", "fill", "Answer = ____"),
        q("Spot: Ratio 18:24 using HCF=6: 3:4. Correct? ____", "fill", "Answer = ____"),
        q("True or False: HCF is used to simplify fractions and ratios.", "fill", "Answer = ____"),
        q("True or False: Simplifying a fraction changes its value.", "fill", "Answer = ____"),
        q("Simplify 36/48. HCF(36,48)=____. Answer: ____", "fill", "Answer = ____"),
        q("Simplify ratio 24:36. HCF=____. Ratio: ____:____", "fill", "Answer = ____"),
    ]

def _L9G_2():
    return [
        cb("Applying LCM — Adding Fractions", [
            "To add fractions with different denominators: find LCD = LCM of denominators.",
            "Convert both fractions to LCD, then add numerators.",
        ], "1/4 + 1/6: LCD=LCM(4,6)=12. 3/12 + 2/12 = 5/12"),
        q("Add 1/4 + 1/6. LCD=LCM(4,6)=____. Convert: ____+____ = ____", "fill", "Answer = ____"),
        q("Add 1/3 + 1/4. LCD=LCM(3,4)=____. Convert: ____+____ = ____", "fill", "Answer = ____"),
        q("Add 2/5 + 1/3. LCD=LCM(5,3)=____. Convert: ____+____ = ____", "fill", "Answer = ____"),
        q("Add 3/4 + 1/6. LCD=LCM(4,6)=____. Convert: ____+____ = ____", "fill", "Answer = ____"),
        q("Add 1/8 + 1/12. LCD=LCM(8,12)=____. Convert: ____+____ = ____", "fill", "Answer = ____"),
        q("Compare 3/4 and 5/6. LCD=LCM(4,6)=____. Convert: ____/12 and ____/12. Larger = ____", "fill", "Answer = ____"),
        q("Compare 2/3 and 3/4. LCD=____. Larger = ____", "fill", "Answer = ____"),
        q("Compare 5/8 and 7/12. LCD=LCM(8,12)=____. Larger = ____", "fill", "Answer = ____"),
        q("Container A: 3/4 litres. Container B: 5/6 litres. Which holds more? ____", "word", "Answer = ____", "compare 3/4 and 5/6"),
        q("True or False: LCD for adding 1/4 and 1/6 is LCM(4,6) = 12.", "fill", "Answer = ____"),
        q("True or False: 1/3 + 1/4 = 7/12 using LCD=12.", "fill", "Answer = ____"),
        q("True or False: 1/8 + 1/12 = 5/24 using LCD=24.", "fill", "Answer = ____"),
        q("True or False: 3/4 < 5/6 because 9/12 < 10/12.", "fill", "Answer = ____"),
        q("True or False: 5/8 > 7/12 because LCD=24: 15/24 > 14/24.", "fill", "Answer = ____"),
        q("Spot: LCD for 2/5+1/3 = LCM(5,3)=8. Correct? Fix. ____", "fill", "Answer = ____"),
        q("Spot: 3/4+1/6 = 9/12+2/12 = 11/12. Correct? ____", "fill", "Answer = ____"),
        q("True or False: LCM is used to find the common denominator for adding fractions.", "fill", "Answer = ____"),
        q("True or False: 2/3 < 3/4 because LCD=12: 8/12 < 9/12.", "fill", "Answer = ____"),
        q("Add 1/4 + 1/9. LCD=LCM(4,9)=____. Answer: ____", "fill", "Answer = ____"),
        q("True or False: 1/4+1/9 = 13/36.", "fill", "Answer = ____"),
    ]

def _L9G_3():
    return [
        tb("Applications of HCF and LCM — Tips", [
            "Simplify fraction: divide top and bottom by HCF.",
            "Simplify ratio: divide ALL parts by HCF of all parts.",
            "Add/subtract fractions: find LCM of denominators = LCD.",
            "Compare fractions: convert to same LCD, compare numerators.",
            "Always double-check by multiplying back.",
        ]),
        q("Simplify 45/60. HCF(45,60)=____. Answer: ____", "fill", "Answer = ____"),
        q("Simplify 42/70. HCF(42,70)=____. Answer: ____", "fill", "Answer = ____"),
        q("Simplify ratio 30:45. HCF=____. Ratio: ____:____", "fill", "Answer = ____"),
        q("Simplify ratio 20:30:40. HCF=10. Ratio: ____:____:____", "fill", "Answer = ____"),
        q("Add 3/8 + 1/6. LCD=LCM(8,6)=____. Answer: ____", "fill", "Answer = ____"),
        q("Add 1/4 + 1/9. LCD=LCM(4,9)=____. Answer: ____", "fill", "Answer = ____"),
        q("Compare 4/9 and 5/12. LCD=LCM(9,12)=____. Larger = ____", "fill", "Answer = ____"),
        q("Compare 7/10 and 5/8. LCD=LCM(10,8)=____. Larger = ____", "fill", "Answer = ____"),
        q("True or False: 45/60 simplifies to 3/4.", "fill", "Answer = ____"),
        q("True or False: 42/70 simplifies to 3/5.", "fill", "Answer = ____"),
        q("True or False: Ratio 30:45 = 2:3.", "fill", "Answer = ____"),
        q("True or False: Ratio 20:30:40 = 2:3:4.", "fill", "Answer = ____"),
        q("True or False: 3/8 + 1/6 = 13/24.", "fill", "Answer = ____"),
        q("True or False: 4/9 > 5/12 because LCD=36: 16/36 > 15/36.", "fill", "Answer = ____"),
        q("True or False: 7/10 > 5/8 because LCD=40: 28/40 > 25/40.", "fill", "Answer = ____"),
        q("Spot: Simplify 42/70 using HCF=7: 6/10. Simplify further? ____", "fill", "Answer = ____"),
        q("Spot: Ratio 24:36 using HCF=12: 2:4. Correct? Fix. ____", "fill", "Answer = ____"),
        q("True or False: LCD for adding fractions = LCM of the denominators.", "fill", "Answer = ____"),
        q("True or False: HCF is needed to simplify fractions.", "fill", "Answer = ____"),
        q("True or False: LCM is needed to add fractions with different denominators.", "fill", "Answer = ____"),
    ]

def _L9G_4():
    return [
        tb("Applications — Mastery Tips", [
            "To add fractions: find LCD (LCM of denominators), convert, then add.",
            "To compare fractions: convert to same LCD, compare numerators.",
            "Multi-step: simplify result after adding/subtracting.",
            "Always express answers in simplest form.",
        ]),
        q("Add 5/6 + 3/8. LCD=LCM(6,8)=____. Answer: ____. Simplify: ____", "fill", "Answer = ____"),
        q("Subtract 3/4 - 2/9. LCD=LCM(4,9)=____. Answer: ____", "fill", "Answer = ____"),
        q("Subtract 5/6 - 3/10. LCD=LCM(6,10)=____. Answer: ____. Simplify: ____", "fill", "Answer = ____"),
        q("Simplify ratio 48:72:96. HCF=____. Ratio: ____", "fill", "Answer = ____"),
        q("Simplify ratio 60:84:120. HCF=____. Ratio: ____", "fill", "Answer = ____"),
        q("Order ascending: 2/3, 3/4, 5/6, 7/12. LCD=____. Order: ____", "fill", "Answer = ____"),
        q("Sum of 3/4 + 5/6 + 7/8. LCD=____. Sum = ____", "fill", "Answer = ____"),
        q("True or False: 5/6+3/8 = 20/24+9/24 = 29/24 = 1 and 5/24.", "fill", "Answer = ____"),
        q("True or False: 3/4-2/9 = 27/36-8/36 = 19/36.", "fill", "Answer = ____"),
        q("True or False: 5/6-3/10 = 25/30-9/30 = 16/30 = 8/15.", "fill", "Answer = ____"),
        q("True or False: Ratio 48:72:96 = 2:3:4.", "fill", "Answer = ____"),
        q("True or False: Ascending order of 2/3,3/4,5/6,7/12 is: 7/12, 2/3, 3/4, 5/6.", "fill", "Answer = ____"),
        q("True or False: 3/4+5/6+7/8 = 18/24+20/24+21/24 = 59/24.", "fill", "Answer = ____"),
        q("True or False: 7/12 < 2/3 < 3/4 < 5/6.", "fill", "Answer = ____"),
        q("Spot: 5/6-3/10: LCD=30: 25/30-9/30=16/30=8/15. Correct? ____", "fill", "Answer = ____"),
        q("Spot: Ratio 60:84:120 using HCF=12: 5:7:10. Correct? ____", "fill", "Answer = ____"),
        q("True or False: HCF is needed to simplify, LCM to add fractions.", "fill", "Answer = ____"),
        q("True or False: 6/8 = 9/12 = 15/20 = 3/4.", "fill", "Answer = ____"),
        q("True or False: Ratio 48:72:96 simplifies to 2:3:4.", "fill", "Answer = ____"),
        q("True or False: LCD for 3/4+5/6+7/8 = LCM(4,6,8) = 24.", "fill", "Answer = ____"),
    ]


# ─── 9H: Mixed ──────────────────────────────────────────────
# ─── 9H: Euclidean Algorithm for HCF (big numbers) ───────────
def _L9H_s(sheet):
    random.seed(920 + sheet)
    ranges = {1: (50, 200), 2: (100, 400), 3: (200, 600), 4: (300, 999)}
    lo, hi = ranges[sheet]
    items = [
        cb("The Euclidean Algorithm — a FASTER way to find HCF", [
            "For big numbers, listing factors or prime-factorising takes too long. The Euclidean Algorithm is much faster.",
            "Divide the bigger number by the smaller. Note the remainder.",
            "Replace the bigger number with the smaller, and the smaller with the remainder. Repeat.",
            "Stop when the remainder is 0 -- the LAST divisor is the HCF.",
        ], "HCF(252,105): 252=105x2+42; 105=42x2+21; 42=21x2+0 -> HCF=21"),
    ]

    def make_pair():
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        if a < b: a, b = b, a
        while a == b:
            b = random.randint(lo, hi)
            if a < b: a, b = b, a
        return a, b

    for _ in range(6):
        a, b = make_pair()
        items.append(q(f"Step 1 of the Euclidean Algorithm for HCF({a},{b}): {a} = {b} x ____ + ____. Find the quotient and remainder.", "fill", "Answer = ____"))
    for _ in range(8):
        a, b = make_pair()
        items.append(q(f"Use the Euclidean Algorithm to find HCF({a}, {b}).", "fill", "HCF = ____"))
    for _ in range(3):
        a, b = make_pair()
        h = _l6_hcf(a, b)
        shown = h if random.random() > 0.4 else h + random.choice([3, -5])
        items.append(q(f"True or False: HCF({a},{b}) = {shown} (using the Euclidean Algorithm).", "fill", "Answer = ____"))
    for _ in range(3):
        a, b = make_pair()
        items.append(q(f"Compare methods: find HCF({a},{b}) using the Euclidean Algorithm. Would listing every factor of both numbers be faster or slower than this method here? ____", "fill", "Answer = ____"))
    return items

# ─── 9I: Puzzle ─────────────────────────────────────────────
def _L9I_s(sheet):
    s1 = [
        cb("Factor and Multiple Puzzles", [
            "Use clues to find the hidden number.",
            "I am a multiple of 3 AND a factor of 36 → try 3, 6, 9, 12, 18, 36.",
            "Check each clue one by one.",
        ], "I am between 10 and 20. I am a multiple of 3. I am a factor of 36. Answer: 12 or 18"),
        q("I am a multiple of 4 and a factor of 24. I am between 10 and 20. I am ____", "fill", "Answer = ____"),
        q("I am a multiple of 6. I am less than 30. I am a factor of 60. List all. ____", "fill", "Answer = ____"),
        q("I am a common factor of 24 and 36. I am greater than 5. I am ____", "fill", "Answer = ____"),
        q("I am a common multiple of 4 and 6. I am less than 30. I am ____", "fill", "Answer = ____"),
        q("My prime factorisation is 2²×3. I am ____", "fill", "Answer = ____"),
        q("My prime factorisation is 2×3×5. I am ____", "fill", "Answer = ____"),
        q("I am a 2-digit number. All my digits are the same. I am a multiple of 9. I am ____", "fill", "Answer = ____"),
        q("HCF(n, 12) = 4. n is between 10 and 20. n = ____", "fill", "n = ____"),
        q("LCM(n, 6) = 18. n = ____", "fill", "n = ____"),
        q("LCM(n, 4) = 12. n could be ____", "fill", "n = ____"),
        q("I have exactly 3 factors. I am less than 30. List all such numbers. ____", "fill", "Answer = ____"),
        q("I am a prime number between 20 and 30. I am ____", "fill", "Answer = ____"),
        q("Sum of my digits = 9. I am a 2-digit multiple of 9. List all. ____", "fill", "Answer = ____"),
        q("I am divisible by both 4 and 6 but not by 9. I am between 10 and 50. List all. ____", "fill", "Answer = ____"),
        q("True or False: A number with exactly 2 factors is prime.", "fill", "Answer = ____"),
        q("True or False: 12 is a multiple of 4 AND a factor of 36.", "fill", "Answer = ____"),
        q("True or False: LCM(n,6)=18 gives n=9 (since LCM(9,6)=18).", "fill", "Answer = ____"),
        q("True or False: Numbers with exactly 3 factors are squares of primes.", "fill", "Answer = ____"),
        q("True or False: HCF(n,12)=4 means n is a multiple of 4.", "fill", "Answer = ____"),
        q("True or False: A number between 1 and 30 with sum of digits = 9 and divisible by 9: 9, 18, 27.", "fill", "Answer = ____"),
    ]
    s2 = [
        cb("HCF and LCM Puzzles", [
            "If HCF(a,b)=h, then both a and b are multiples of h.",
            "If LCM(a,b)=l, then l is divisible by both a and b.",
            "HCF(a,b) × LCM(a,b) = a × b. Use this to find unknowns.",
        ], "HCF(a,b)=6, LCM=36. Find a×b: 6×36=216. If a=12, b=216÷12=18."),
        q("HCF(a,b)=4, LCM(a,b)=24. Find a×b. ____", "fill", "a×b = ____"),
        q("HCF(a,b)=6, LCM(a,b)=36. Find a×b. ____", "fill", "a×b = ____"),
        q("HCF(a,b)=5, LCM(a,b)=60. Find a×b. ____", "fill", "a×b = ____"),
        q("HCF(a,b)=4, LCM=24, a=8. Find b. b=96÷8=____", "fill", "b = ____"),
        q("HCF(a,b)=6, LCM=36, a=12. Find b. b=216÷12=____", "fill", "b = ____"),
        q("HCF(a,b)=3, LCM=45, a=9. Find b. ____", "fill", "b = ____"),
        q("Both a and b are multiples of 6. HCF(a,b)=6. LCM(a,b)=24. Find a and b. ____", "fill", "Answer = ____"),
        q("Two numbers with HCF=5 and LCM=30. Both less than 30. Find all pairs. ____", "fill", "Answer = ____"),
        q("Two numbers with HCF=4 and LCM=48. Find all pairs. ____", "fill", "Answer = ____"),
        q("Pattern: factors of n = 1, 2, 4, 8, n. What is n? ____", "fill", "n = ____"),
        q("Pattern: n has exactly 4 factors. n is between 10 and 20. List all such n. ____", "fill", "Answer = ____"),
        q("True or False: HCF(a,b)×LCM(a,b) = a×b.", "fill", "Answer = ____"),
        q("True or False: HCF(a,b)=4, LCM=24 gives a×b=96.", "fill", "Answer = ____"),
        q("True or False: If HCF(a,b)=6, both a and b are multiples of 6.", "fill", "Answer = ____"),
        q("True or False: HCF(6,24)=6, LCM(6,24)=24. Check: 6×24=144=6×24. ✓", "fill", "Answer = ____"),
        q("True or False: Numbers with exactly 4 factors between 10 and 20: 10,14,15.", "fill", "Answer = ____"),
        q("Spot: HCF=5, LCM=30: pairs could be (5,30) or (10,15). Check HCF(10,15)=5 ✓ and LCM(10,15)=30 ✓. Correct?", "fill", "Answer = ____"),
        q("True or False: Factors of 16 = 1,2,4,8,16 — all powers of 2.", "fill", "Answer = ____"),
        q("True or False: If n has exactly 4 factors, n = p×q (product of two distinct primes) OR n = p³.", "fill", "Answer = ____"),
        q("True or False: Two numbers with HCF=4 and LCM=48: one pair is (4,48).", "fill", "Answer = ____"),
    ]
    s3 = [
        tb("Factor, Multiple and HCF/LCM Puzzles — Tips", [
            "List and check: write possible values, test each clue.",
            "HCF × LCM = a × b: use to find the unknown.",
            "If HCF(a,b)=h, write a=h×m and b=h×n where HCF(m,n)=1.",
            "Numbers with exactly 3 factors are squares of primes: 4, 9, 25, 49...",
        ]),
        q("I am a multiple of 7 and a factor of 84. I am between 15 and 50. I am ____", "fill", "Answer = ____"),
        q("I am a 2-digit number. I am a multiple of 8. My digits sum to 8. I am ____", "fill", "Answer = ____"),
        q("HCF(a,b)=7, LCM(a,b)=84. Find a×b. ____", "fill", "a×b = ____"),
        q("HCF(a,b)=7, LCM=84, a=28. Find b. ____", "fill", "b = ____"),
        q("Two numbers: HCF=8, LCM=48. Find all possible pairs. ____", "fill", "Answer = ____"),
        q("I am a number between 50 and 100. I am divisible by both 6 and 9. List all. ____", "fill", "Answer = ____"),
        q("n is a prime number. LCM(n,15)=15. n = ____", "fill", "n = ____"),
        q("n is a prime number. LCM(n,12)=60. n = ____", "fill", "n = ____"),
        q("Find all n where HCF(n,18)=6 and n<40. ____", "fill", "Answer = ____"),
        q("I have exactly 5 factors. I am less than 30. I am ____", "fill", "Answer = ____"),
        q("True or False: A multiple of 7 and factor of 84 between 15 and 50: 21 and 42.", "fill", "Answer = ____"),
        q("True or False: 2-digit multiples of 8 with digits summing to 8: 80.", "fill", "Answer = ____"),
        q("True or False: HCF(a,b)=7, LCM=84 gives a×b=588.", "fill", "Answer = ____"),
        q("True or False: HCF=8, LCM=48: pairs are (8,48) and (16,24).", "fill", "Answer = ____"),
        q("True or False: Numbers between 50 and 100 divisible by both 6 and 9: 54, 72, 90.", "fill", "Answer = ____"),
        q("True or False: A number with exactly 5 factors is a 4th power of a prime: p⁴.", "fill", "Answer = ____"),
        q("Spot: n divisible by 6 and 9 between 50 and 100: must be multiple of LCM(6,9)=18: 54,72,90. Correct?", "fill", "Answer = ____"),
        q("True or False: LCM(n,15)=15 means n is a factor of 15.", "fill", "Answer = ____"),
        q("True or False: LCM(n,12)=60 and n is prime: n=5.", "fill", "Answer = ____"),
        q("True or False: Numbers with exactly 5 factors less than 30: 16.", "fill", "Answer = ____"),
    ]
    s4 = [
        tb("Factor, Multiple, HCF/LCM Puzzles — Mastery Tips", [
            "If n = p^k, it has (k+1) factors.",
            "If n = p^a × q^b, it has (a+1)(b+1) factors.",
            "HCF(a,b)=h: write a=h×p, b=h×q where HCF(p,q)=1. Then LCM=h×p×q.",
            "Find all pairs with given HCF and LCM: systematic factor pair search.",
        ]),
        q("Find all pairs (a,b) with HCF=6 and LCM=60. ____", "fill", "Answer = ____"),
        q("Find all pairs (a,b) with HCF=4 and LCM=48. ____", "fill", "Answer = ____"),
        q("Find a number n with exactly 6 factors. ____", "fill", "Answer = ____"),
        q("Find a number n with exactly 8 factors. ____", "fill", "Answer = ____"),
        q("HCF(a,b)=12, LCM(a,b)=144. Find a×b. ____. Find all pairs. ____", "fill", "Answer = ____"),
        q("n is divisible by 8, 9, and 10. Smallest such n = LCM(8,9,10) = ____", "fill", "n = ____"),
        q("Two consecutive multiples of 7 with HCF=7. What is their LCM? ____", "fill", "Answer = ____"),
        q("a and b are both multiples of 6. HCF(a,b)=6, LCM(a,b)=72. Find all pairs. ____", "fill", "Answer = ____"),
        q("True or False: All pairs (a,b) with HCF=6, LCM=60: (6,60), (12,30), (20,18). Check each.", "fill", "Answer = ____"),
        q("True or False: LCM(8,9,10) = 360.", "fill", "Answer = ____"),
        q("True or False: A number with exactly 6 factors: 12 (factors:1,2,3,4,6,12).", "fill", "Answer = ____"),
        q("True or False: HCF=12, LCM=144: a×b=12×144=1728.", "fill", "Answer = ____"),
        q("True or False: Two consecutive multiples of 7: e.g. 7 and 14. LCM(7,14)=14.", "fill", "Answer = ____"),
        q("True or False: a=6, b=72 have HCF=6 and LCM=72.", "fill", "Answer = ____"),
        q("True or False: Pairs with HCF=4, LCM=48: (4,48),(8,24),(16,12). Check: HCF(16,12)=4? LCM(16,12)=48?", "fill", "Answer = ____"),
        q("True or False: A number with exactly 8 factors: 24 (factors: 1,2,3,4,6,8,12,24).", "fill", "Answer = ____"),
        q("Spot: LCM(8,9,10): 8=2³, 9=3², 10=2×5. LCM=2³×3²×5=360. Correct?", "fill", "Answer = ____"),
        q("Spot: HCF=6, LCM=60: (6,60) ✓, (12,30) ✓, (20,18)? HCF(20,18)=2≠6. Correct pair removed?", "fill", "Answer = ____"),
        q("True or False: Any number of the form p×q (distinct primes) has exactly 4 factors.", "fill", "Answer = ____"),
        q("True or False: If HCF(a,b)=h, then h divides both a and b.", "fill", "Answer = ____"),
    ]
    return [s1, s2, s3, s4][sheet - 1]


# ─── 9CUM3: Mixed G+H+I ─────────────────────────────────────
# ─── 9CUM3: Prime Number Enrichment ──────────────────────────
def _L9CUM3_s(sheet):
    random.seed(930 + sheet)
    ranges = {1: (2, 50), 2: (2, 100), 3: (50, 150), 4: (100, 200)}
    lo, hi = ranges[sheet]
    items = [
        cb("Prime Number Enrichment", [
            "Sieve of Eratosthenes: cross out multiples of 2, then 3, then 5, then 7... whatever is LEFT is prime.",
            "Twin primes: two primes that differ by exactly 2 (e.g. 11 and 13, 17 and 19).",
            "A perfect number equals the sum of its own factors (not counting itself). 6 = 1+2+3. The next is 28.",
        ], "Twin primes near 40-45: 41 and 43. Perfect number check: 6->1+2+3=6 YES"),
    ]
    for _ in range(4):
        n = random.randint(max(lo, 2), hi)
        items.append(q(f"Using the Sieve of Eratosthenes idea, is {n} prime? (Check: is it divisible by any prime up to its square root?)", "fill", "Answer = ____ (Yes/No)"))
    for _ in range(4):
        start = random.randint(max(lo, 2), max(hi - 20, lo + 1))
        items.append(q(f"List all prime numbers between {start} and {start+20} using the Sieve method.", "fill", "Answer = ____"))
    for _ in range(4):
        n = random.randint(max(lo, 3), hi)
        items.append(q(f"Is {n} part of a twin prime pair? If so, what is its twin?", "fill", "Answer = ____"))
    items.append(q("Verify that 6 is a perfect number (sum of its factors, excluding itself, equals 6).", "fill", "Answer = ____"))
    items.append(q("Verify that 28 is a perfect number (sum of its factors, excluding itself, equals 28).", "fill", "Answer = ____"))
    items.append(q("True or False: 12 is a perfect number.", "fill", "Answer = ____"))
    items.append(q("True or False: 11 and 13 are twin primes.", "fill", "Answer = ____"))
    items.append(q("True or False: Every even number greater than 2 is composite.", "fill", "Answer = ____"))
    items.append(q("True or False: 2 and 3 are the only pair of consecutive prime numbers.", "fill", "Answer = ____"))
    items.append(q("Spot: A student says 1 is a prime number. Correct? Explain why or why not. ____", "fill", "Answer = ____"))
    items.append(q("Spot: A student lists 21 as prime. Correct? Fix it (21 = 3 x 7). ____", "fill", "Answer = ____"))
    return items

# ─── 9J: Mixed challenge ────────────────────────────────────
# ─── 9J: Mastery Challenge (bigger numbers, gamified) ────────
def _L9J_s(sheet):
    random.seed(940 + sheet)
    ranges = {1: (100, 400), 2: (200, 600), 3: (300, 800), 4: (500, 999)}
    lo, hi = ranges[sheet]
    items = [
        cb("Level 6 Mastery Challenge", [
            "Every skill: factors, multiples, prime factorisation, HCF (listing, prime factorisation, OR the Euclidean Algorithm), LCM, and applications.",
            "Numbers are bigger here -- choose your method wisely!",
            "Speed challenge: each question has a point value. Bronze 20+, Silver 30+, Gold 38+ (all correct).",
        ], "Bronze 20+, Silver 30+, Gold 38+ (all correct)"),
    ]

    def make_pair():
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        while a == b:
            b = random.randint(lo, hi)
        return a, b

    for _ in range(5):
        a, b = make_pair()
        items.append(q(f"HCF({a}, {b}) = ____  [2 points]", "fill", "HCF = ____"))
    for _ in range(5):
        a, b = make_pair()
        items.append(q(f"LCM({a}, {b}) = ____  [2 points]", "fill", "LCM = ____"))
    for _ in range(4):
        a, b, c = random.randint(lo//2, hi//2), random.randint(lo//2, hi//2), random.randint(lo//2, hi//2)
        items.append(q(f"HCF({a}, {b}, {c}) = ____  [3 points]", "fill", "HCF = ____"))
    for _ in range(3):
        n = random.randint(lo, hi)
        items.append(q(f"Find the prime factorisation of {n}.  [2 points]", "fill", "Answer = ____"))
    for _ in range(3):
        a, b = make_pair()
        h = _l6_hcf(a, b)
        shown = h if random.random() > 0.4 else h + random.choice([5, -7])
        items.append(q(f"True or False: HCF({a},{b}) = {shown}.  [1 point]", "fill", "Answer = ____ (True/False)"))
    items.append(tb("Your Score", ["My total score: _____.  My badge: Bronze / Silver / Gold (circle one)"]))
    return items

# ─── 9REV: Level 6 Revision ─────────────────────────────────
# ─── 9REV: Level 6 Revision (samples every topic, climbs in difficulty) ───
def _L9REV_s(sheet):
    random.seed(950 + sheet)
    ranges = {1: (10, 40), 2: (30, 100), 3: (80, 300), 4: (200, 700)}
    lo, hi = ranges[sheet]
    items = [
        tb("Level 6 Revision — Tips", [
            "Factors: divide exactly, come in pairs. Multiples: n x 1, n x 2, ...",
            "HCF: listing, prime factorisation, OR the Euclidean Algorithm (fastest for big numbers).",
            "LCM: smallest common multiple. HCF x LCM = a x b.",
            "Applications: HCF simplifies fractions/ratios. LCM finds common denominators / meeting times.",
            "Enrichment: Sieve of Eratosthenes for primes, twin primes, perfect numbers.",
        ]),
    ]

    def make_pair():
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        while a == b:
            b = random.randint(lo, hi)
        return a, b

    for _ in range(3):
        n = random.randint(lo, hi)
        items.append(q(f"List all factors of {n}.", "fill", "Answer = ____"))
    for _ in range(2):
        n = random.randint(max(lo, 2), hi)
        items.append(q(f"Find the prime factorisation of {n}.", "fill", "Answer = ____"))
    for _ in range(3):
        a, b = make_pair()
        items.append(q(f"HCF({a}, {b}) = ____", "fill", "HCF = ____"))
    for _ in range(3):
        a, b = make_pair()
        items.append(q(f"LCM({a}, {b}) = ____", "fill", "LCM = ____"))
    for _ in range(2):
        a, b = make_pair()
        items.append(q(f"Use the Euclidean Algorithm to find HCF({a}, {b}).", "fill", "HCF = ____"))
    for _ in range(2):
        n = random.randint(max(lo, 2), hi)
        items.append(q(f"Is {n} prime or composite?", "fill", "Answer = ____ (Prime/Composite)"))
    for _ in range(2):
        a, b = make_pair()
        h = _l6_hcf(a, b)
        shown = h if random.random() > 0.4 else h + random.choice([2, -3])
        items.append(q(f"True or False: HCF({a},{b}) = {shown}.", "fill", "Answer = ____"))
    for _ in range(2):
        a, b = make_pair()
        l = _l6_lcm(a, b)
        shown = l if random.random() > 0.4 else l + random.choice([6, -9])
        items.append(q(f"True or False: LCM({a},{b}) = {shown}.", "fill", "Answer = ____"))
    num = random.randint(max(lo, 4), hi)
    den = random.randint(max(lo, 4), hi)
    items.append(q(f"Simplify the fraction {min(num,den)}/{max(num,den)} using HCF.", "fill", "Answer = ____"))
    return items





_RAW_DISPATCH = {
    "6A":    {1:_L9A_1, 2:_L9A_2, 3:_L9A_3, 4:_L9A_4},
    "6B":    {1:_L9B_1, 2:_L9B_2, 3:_L9B_3, 4:_L9B_4},
    "6C":    {1:_L9C_1, 2:_L9C_2, 3:_L9C_3, 4:_L9C_4},
    "6D":    {1:_L9D_1, 2:_L9D_2, 3:_L9D_3, 4:_L9D_4},
    "6E":    {1:_L9E_1, 2:_L9E_2, 3:_L9E_3, 4:_L9E_4},
    "6F":    {1:_L9F_1, 2:_L9F_2, 3:_L9F_3, 4:_L9F_4},
    "6G":    {1:_L9G_1, 2:_L9G_2, 3:_L9G_3, 4:_L9G_4},
    "6H":    {1:lambda:_L9H_s(1), 2:lambda:_L9H_s(2), 3:lambda:_L9H_s(3), 4:lambda:_L9H_s(4)},
    "6I":    {1:lambda:_L9I_s(1), 2:lambda:_L9I_s(2), 3:lambda:_L9I_s(3), 4:lambda:_L9I_s(4)},
    "6J":    {1:lambda:_L9J_s(1), 2:lambda:_L9J_s(2), 3:lambda:_L9J_s(3), 4:lambda:_L9J_s(4)},
    "6CUM1": {1:lambda:_L9CUM1_s(1), 2:lambda:_L9CUM1_s(2), 3:lambda:_L9CUM1_s(3), 4:lambda:_L9CUM1_s(4)},
    "6CUM2": {1:lambda:_L9CUM2_s(1), 2:lambda:_L9CUM2_s(2), 3:lambda:_L9CUM2_s(3), 4:lambda:_L9CUM2_s(4)},
    "6CUM3": {1:lambda:_L9CUM3_s(1), 2:lambda:_L9CUM3_s(2), 3:lambda:_L9CUM3_s(3), 4:lambda:_L9CUM3_s(4)},
    "6REV":  {1:lambda:_L9REV_s(1), 2:lambda:_L9REV_s(2), 3:lambda:_L9REV_s(3), 4:lambda:_L9REV_s(4)},
}




def _l6_factors_of(n):
    return sorted(d for d in range(1, n + 1) if n % d == 0)


def _l6_infer_diagram(text):
    t = text
    m = _l6_re.search(r'Euclidean Algorithm[^0-9]*?HCF\((\d+),\s*(\d+)\)', t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return "euclidean_algorithm", {"a": max(a, b), "b": min(a, b)}
    m = _l6_re.search(r'HCF\((\d+),\s*(\d+)\)', t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return "ladder_division", {"a": max(a, b), "b": min(a, b), "mode": "hcf"}
    m = _l6_re.search(r'HCF of (\d+) and (\d+)', t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return "ladder_division", {"a": max(a, b), "b": min(a, b), "mode": "hcf"}
    m = _l6_re.search(r'LCM\((\d+),\s*(\d+)(?:,\s*\d+)?\)', t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return "ladder_division", {"a": max(a, b), "b": min(a, b), "mode": "lcm"}
    m = _l6_re.search(r'LCM of (\d+)[,\s]+(\d+)', t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return "ladder_division", {"a": max(a, b), "b": min(a, b), "mode": "lcm"}
    m = _l6_re.search(r'Simplify\s+(\d+)/(\d+)', t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return "ladder_division", {"a": max(a, b), "b": min(a, b), "mode": "hcf"}
    m = _l6_re.search(r'[Rr]atio\s+(\d+):(\d+)', t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return "ladder_division", {"a": max(a, b), "b": min(a, b), "mode": "hcf"}
    m = _l6_re.search(r'[Ii]s \d+ a common factor of (\d+) and (\d+)', t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        fa, fb = set(_l6_factors_of(a)), set(_l6_factors_of(b))
        return "venn_two", {"a_only": sorted(fa - fb), "common": sorted(fa & fb), "b_only": sorted(fb - fa), "label_a": str(a), "label_b": str(b)}
    m = _l6_re.search(r'[Cc]ommon factors of (\d+) and (\d+)', t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        fa, fb = set(_l6_factors_of(a)), set(_l6_factors_of(b))
        return "venn_two", {"a_only": sorted(fa - fb), "common": sorted(fa & fb), "b_only": sorted(fb - fa), "label_a": str(a), "label_b": str(b)}
    m = _l6_re.search(r'[Pp]rime factorisation of (\d+)', t)
    if m:
        return "factor_tree", {"n": int(m.group(1))}
    m = _l6_re.search(r'Sieve of Eratosthenes idea, is (\d+) prime', t)
    if m:
        n = int(m.group(1))
        return ("hundred_grid_highlight", {"highlight": [n]}) if n <= 100 else ("factor_rainbow", {"n": min(n, 60)})
    m = _l6_re.search(r'[Ll]ist all prime numbers between (\d+) and (\d+)', t)
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        if hi <= 100:
            return "hundred_grid_highlight", {"highlight": [k for k in range(lo, hi + 1) if _l6_is_prime(k)]}
        return "factor_rainbow", {"n": 24}
    m = _l6_re.search(r'[Ii]s (\d+) part of a twin prime pair', t)
    if m:
        n = int(m.group(1))
        cands = [x for x in (n - 2, n, n + 2) if 1 <= x <= 100]
        return ("hundred_grid_highlight", {"highlight": cands}) if cands else ("factor_rainbow", {"n": 24})
    m = _l6_re.search(r'[Vv]erify that (\d+) is a perfect number', t)
    if m:
        n = int(m.group(1))
        return ("factor_rainbow", {"n": n}) if n <= 60 else ("hundred_grid_highlight", {"highlight": _l6_factors_of(n)})
    m = _l6_re.search(r'^(?:True or False|Complete|Spot)[:\s]*[a-zA-Z]*\s*(\d+)\s*=', t)
    if m:
        return "factor_tree", {"n": int(m.group(1))}
    m = _l6_re.search(r'[Mm]ultiples of (\d+)', t)
    if m:
        return "multiples_number_line", {"n": int(m.group(1)), "count": 8}
    m = _l6_re.search(r'multiple of (\d+)', t)
    if m:
        return "multiples_number_line", {"n": int(m.group(1)), "count": 8}
    m = _l6_re.search(r'[Ii]s (\d+) a factor of (\d+)', t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if b % a == 0:
            return "factor_array", {"n": b, "rows": a, "cols": b // a}
        return ("factor_rainbow", {"n": b}) if b <= 60 else ("hundred_grid_highlight", {"highlight": _l6_factors_of(b)})
    m = _l6_re.search(r'factor pairs of (\d+)', t)
    if m:
        n = int(m.group(1))
        return ("factor_rainbow", {"n": n}) if n <= 60 else ("hundred_grid_highlight", {"highlight": _l6_factors_of(n)})
    m = _l6_re.search(r'factors does (\d+) have', t)
    if m:
        n = int(m.group(1))
        return ("factor_rainbow", {"n": n}) if n <= 60 else ("hundred_grid_highlight", {"highlight": _l6_factors_of(n)})
    m = _l6_re.search(r'factors? of (\d+)', t)
    if m:
        n = int(m.group(1))
        return ("factor_rainbow", {"n": n}) if n <= 60 else ("hundred_grid_highlight", {"highlight": _l6_factors_of(n)})
    return None


_L6_FAMILY_FALLBACK = {
    "6A": ("factor_rainbow", {"n": 12}),
    "6B": ("multiples_number_line", {"n": 6, "count": 8}),
    "6C": ("factor_tree", {"n": 60}),
    "6CUM1": ("factor_tree", {"n": 60}),
    "6D": ("ladder_division", {"a": 24, "b": 36, "mode": "hcf"}),
    "6E": ("ladder_division", {"a": 8, "b": 12, "mode": "lcm"}),
    "6F": ("ladder_division", {"a": 24, "b": 36, "mode": "hcf"}),
    "6CUM2": ("venn_two", {"a_only": [2], "common": [2, 3], "b_only": [3], "label_a": "24", "label_b": "36"}),
    "6G": ("ladder_division", {"a": 12, "b": 18, "mode": "hcf"}),
    "6H": ("euclidean_algorithm", {"a": 252, "b": 105}),
    "6I": ("factor_rainbow", {"n": 24}),
    "6J": ("ladder_division", {"a": 24, "b": 36, "mode": "hcf"}),
    "6REV": ("factor_rainbow", {"n": 24}),
}


def _l6_fallback(sublevel_code):
    for key in sorted(_L6_FAMILY_FALLBACK, key=len, reverse=True):
        if sublevel_code.startswith(key):
            return _L6_FAMILY_FALLBACK[key]
    return ("factor_rainbow", {"n": 12})


def _l6_visualize(items, sublevel_code):
    fb_type, fb_params = _l6_fallback(sublevel_code)
    out = []
    diagram_count = 0
    for item in items:
        new_item = dict(item)
        if item.get("type") in ("fill", "word"):
            inferred = _l6_infer_diagram(item["text"])
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


def _l6_wrap(fn, sublevel_code):
    return lambda: _l6_visualize(fn(), sublevel_code)




def _l6_fallback(sublevel_code):
    for key in sorted(_L6_FAMILY_FALLBACK, key=len, reverse=True):
        if sublevel_code.startswith(key):
            return _L6_FAMILY_FALLBACK[key]
    return ("factor_rainbow", {"n": 12})


def _l6_visualize(items, sublevel_code):
    fb_type, fb_params = _l6_fallback(sublevel_code)
    out = []
    diagram_count = 0
    for item in items:
        new_item = dict(item)
        if item.get("type") in ("fill", "word"):
            inferred = _l6_infer_diagram(item["text"])
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


def _l6_wrap(fn, sublevel_code):
    return lambda: _l6_visualize(fn(), sublevel_code)


LEVEL6_DISPATCH = {
    sub: {sheet: _l6_wrap(fn, sub) for sheet, fn in sheets.items()}
    for sub, sheets in _RAW_DISPATCH.items()
}
