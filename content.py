"""
Fear Less Maths — Question Content: Levels 1 & 2
Every question hand-written. No placeholders.
Sheet 1=Intuition, Sheet 2=Concept, Sheet 3=Practice, Sheet 4=Mastery
Remedial variants replace numbers using remedialise().
"""
import random, re

def cb(title, bullets, example=""):
    return {"type":"concept_box","section_title":title,
            "section_bullets":bullets,"example":example}

def q(text, qtype="fill", ans="Answer = ____", bold="", diag=None, dpar=None):
    return {"type":qtype,"text":text,"answer_label":ans,
            "bold_phrase":bold,"diagram_type":diag,"diagram_params":dpar or {}}

def remedialise(items, seed=0):
    random.seed(seed)
    out = []
    for item in items:
        if item["type"] == "concept_box": out.append(item); continue
        ni = dict(item)
        def sw(m):
            v = float(m.group())
            d = random.uniform(0.5, max(0.5, abs(v)*0.3))
            nv = round(v + d if random.random()>0.5 else max(0.1,v-d), 1)
            return str(int(nv) if nv == int(nv) else nv)
        ni["text"] = re.sub(r'\b\d+\.?\d*\b', sw, ni.get("text",""))
        out.append(ni)
    return out


# L1A Sheet 1 — Intuition
def _L1A_1():  # Counting 1-50, Sheet 1 Intuition
    return [
        cb("Counting 1 to 50", ["Numbers go in order: 1, 2, 3, 4, 5…", "Each number is ONE MORE than the one before.", "We can count objects by pointing one by one."], "Count: 1, 2, 3, 4, 5 — each step adds one"),
        q("Count the dots and write the total.", "diagram", "Count = ____", "", "dot_array", {"rows":2,"cols":4}),
        q("Count the dots and write the total.", "diagram", "Count = ____", "", "dot_array", {"rows":3,"cols":3}),
        q("Write the number that comes AFTER 7.", "fill", "Answer = ____"),
        q("Write the number that comes AFTER 15.", "fill", "Answer = ____"),
        q("Write the number that comes AFTER 29.", "fill", "Answer = ____"),
        cb("Tens and Ones", ["23 = 2 tens and 3 ones.", "30 = 3 tens and 0 ones.", "Count the tens first, then add the ones."], "4 tens + 6 ones = 46"),
        q("25 = ____ tens and ____ ones.", "fill", "Tens = ____  Ones = ____"),
        q("33 = ____ tens and ____ ones.", "fill", "Tens = ____  Ones = ____"),
        q("4 tens and 6 ones = ____.", "fill", "Answer = ____"),
        q("3 tens and 0 ones = ____.", "fill", "Answer = ____"),
        q("Fill in the missing numbers: 21, 22, ___, 24, ___, 26.", "fill", "Answer = ____"),
        cb("Counting Backwards", ["Count back from 10: 10, 9, 8, 7, 6, 5, 4, 3, 2, 1.", "Each step REMOVES one.", "We can count backwards from any number."], "20, 19, 18, 17 — each step goes back one"),
        q("Count back: 15, 14, ___, 12, ___.", "fill", "Answer = ____"),
        q("Count back: 30, 29, ___, 27, ___.", "fill", "Answer = ____"),
        q("Write all numbers from 41 to 50.", "fill", "Answer = ____"),
        q("Which number comes just BEFORE 40?", "fill", "Answer = ____"),
        q("Ravi has 3 bags of 10 apples and 7 loose apples. How many apples in total?", "word", "Total = ____", "3 bags of 10 and 7 loose"),
        q("The number 48 has ____ tens and ____ ones.", "fill", "Tens = ____  Ones = ____"),
        q("Four tens and two ones = ____.", "fill", "Answer = ____"),
        q("Write all numbers between 45 and 50 (not including 45 and 50).", "fill", "Answer = ____"),
    ]

# L1B Sheet 1 — Intuition
def _L1B_1():  # Counting 1-100, Sheet 1 Intuition
    return [
        cb("Counting to 100", ["After 50 comes 51, 52, 53… all the way to 100.", "100 = ten groups of ten.", "We can skip-count by 10s: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100."], "Count by 10s: 10, 20, 30, 40, 50"),
        q("Count the objects shown.", "diagram", "Count = ____", "", "ten_frames", {"count":23}),
        q("Fill in the missing numbers: 55, 56, ___, 58, ___.", "fill", "Answer = ____"),
        q("Fill in the missing numbers: 78, ___, 80, ___, 82.", "fill", "Answer = ____"),
        q("What number comes after 69?", "fill", "Answer = ____"),
        q("What number comes after 99?", "fill", "Answer = ____"),
        cb("Skip Counting by 10", ["Count by 10s: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100.", "The ones digit stays the SAME when you count by 10s.", "Each jump adds 10 to the tens digit."], "23, 33, 43, 53 — the ones digit stays 3"),
        q("Fill in: 10, 20, ___, 40, ___, 60.", "fill", "Answer = ____"),
        q("Fill in — count by 10 starting from 5: 5, 15, ___, 35, ___.", "fill", "Answer = ____"),
        q("What is 10 more than 67?", "fill", "Answer = ____"),
        q("What is 10 less than 90?", "fill", "Answer = ____"),
        q("Write all the multiples of 10 from 10 to 100.", "fill", "Answer = ____"),
        cb("Tens and Ones to 100", ["87 = 8 tens and 7 ones.", "100 = 10 tens and 0 ones.", "9 tens + 4 ones = 94."], "72 = 7 tens and 2 ones"),
        q("72 = ____ tens and ____ ones.", "fill", "Tens = ____  Ones = ____"),
        q("8 tens and 5 ones = ____.", "fill", "Answer = ____"),
        q("9 tens and 0 ones = ____.", "fill", "Answer = ____"),
        q("Count back by 10s: 100, 90, ___, 70, ___.", "fill", "Answer = ____"),
        q("Meena has 6 bags of 10 marbles and 4 extra marbles. How many marbles altogether?", "word", "Total = ____", "6 bags of 10 and 4 extra"),
        q("Write all multiples of 5 between 60 and 80.", "fill", "Answer = ____"),
        q("What is 10 more than 89?", "fill", "Answer = ____"),
        q("What number comes just before 100?", "fill", "Answer = ____"),
    ]

# L1A Sheet 2 — Concept
def _L1A_2():  # Counting 1-50, Sheet 2 Concept
    return [
        cb("Place Value: Tens and Ones", ["The TENS digit tells us how many groups of 10.", "The ONES digit tells us the extras.", "Value of tens digit = digit × 10. Value of ones digit = the digit itself."], "In 37: value of 3 = 30,  value of 7 = 7"),
        q("In 24, what is the value of the digit 2?", "fill", "Value = ____"),
        q("In 38, what is the value of the digit 3?", "fill", "Value = ____"),
        q("In 45, what is the value of the digit 5?", "fill", "Value = ____"),
        q("Write 27 in expanded form: ___ + ___.", "fill", "Answer = ____"),
        q("Write 43 in expanded form: ___ + ___.", "fill", "Answer = ____"),
        q("Write as a number: 30 + 6 = ____.", "fill", "Answer = ____"),
        q("Write as a number: 10 + 9 = ____.", "fill", "Answer = ____"),
        cb("Comparing Numbers", ["Compare TENS digits first.", "If tens are equal, compare ONES digits.", "< means less than,  > means greater than,  = means equal."], "23 < 32 because 2 tens < 3 tens"),
        q("Write < or > between the numbers:   23   ___   32.", "fill", "Answer = ____"),
        q("Write < or > between the numbers:   45   ___   44.", "fill", "Answer = ____"),
        q("Write < or > between the numbers:   30   ___   30.", "fill", "Answer = ____"),
        q("Order from smallest to largest: 35, 13, 41, 22.", "fill", "Smallest to largest = ____"),
        q("Order from largest to smallest: 28, 42, 17, 39.", "fill", "Largest to smallest = ____"),
        q("What is the largest 2-digit number that has tens digit 3?", "fill", "Answer = ____"),
        q("Write all 2-digit numbers between 38 and 42.", "fill", "Answer = ____"),
        q("Meena has 34 stickers. Ravi has 43 stickers. Who has more?", "word", "Answer = ____", "34 and 43"),
        q("Which number is closer to 50 — the number 47 or the number 53?", "fill", "Answer = ____"),
        q("The tens digit of 49 is ____.", "fill", "Answer = ____"),
        q("The ones digit of 30 is ____.", "fill", "Answer = ____"),
        q("True or False: 50 is greater than 49.", "fill", "Answer = ____"),
    ]

# L1B Sheet 2 — Concept
def _L1B_2():  # Counting 1-100, Sheet 2 Concept
    return [
        cb("Place Value up to 100", ["Tens, ones — same rules as before.", "96 = 9 tens + 6 ones = 90 + 6.", "The tens digit is always to the LEFT of the ones digit."], "84 = 80 + 4  (tens digit 8 = 80, ones digit 4 = 4)"),
        q("Write 84 in expanded form.", "fill", "Answer = ____"),
        q("Write 73 in expanded form.", "fill", "Answer = ____"),
        q("Write as a number: 60 + 9 = ____.", "fill", "Answer = ____"),
        q("What is the value of the digit 9 in the number 97?", "fill", "Value = ____"),
        q("What is the value of the digit 6 in the number 68?", "fill", "Value = ____"),
        q("Which is greater: 79 or 97? Explain.", "fill", "Answer = ____"),
        q("Write < or >:   56   ___   65.", "fill", "Answer = ____"),
        q("Write < or >:   99   ___   100.", "fill", "Answer = ____"),
        cb("Ordering Numbers to 100", ["Compare tens first. If tens are equal, compare ones.", "Ascending = smallest to largest.", "Descending = largest to smallest."], "72 > 27 because 7 tens > 2 tens"),
        q("Order from smallest to largest: 72, 27, 90, 9, 45.", "fill", "Ascending = ____"),
        q("Order from largest to smallest: 63, 36, 83, 38.", "fill", "Descending = ____"),
        q("Write all multiples of 10 between 40 and 80.", "fill", "Answer = ____"),
        q("What is the largest 2-digit odd number?", "fill", "Answer = ____"),
        q("What is the smallest 2-digit even number?", "fill", "Answer = ____"),
        q("Round 64 to the nearest 10.", "fill", "Answer = ____"),
        q("Round 85 to the nearest 10.", "fill", "Answer = ____"),
        q("How many 2-digit multiples of 10 are there? (10, 20, 30…)", "fill", "Answer = ____"),
        q("A classroom has 3 rows of 10 desks and 8 extra desks. How many desks altogether?", "word", "Total = ____", "3 rows of 10 and 8 extra"),
        q("Write three numbers that are between 70 and 80.", "fill", "Answer = ____"),
        q("True or False: 100 is greater than 99.", "fill", "Answer = ____"),
    ]

# L1A Sheet 3 — Practice
def _L1A_3():  # Counting 1-50, Sheet 3 Practice
    return [
        cb("Quick Review — Place Value", ["Tens digit × 10 = its value.", "Ones digit = its own value.", "Compare numbers: start from the tens place."], "48 = 4 tens + 8 ones = 40 + 8"),
        q("What is the value of the digit 4 in the number 48?", "fill", "Value = ____"),
        q("What is the value of the digit 2 in the number 26?", "fill", "Value = ____"),
        q("Write 36 in expanded form.", "fill", "Answer = ____"),
        q("Write 50 in expanded form.", "fill", "Answer = ____"),
        q("Write as a number: 20 + 7 = ____.", "fill", "Answer = ____"),
        q("Which is larger: 29 or 31?", "fill", "Answer = ____"),
        q("Which is smaller: 47 or 44?", "fill", "Answer = ____"),
        q("Order from smallest to largest: 33, 13, 23, 3.", "fill", "Answer = ____"),
        q("Order from largest to smallest: 41, 14, 40, 4.", "fill", "Answer = ____"),
        q("What comes just before 50?", "fill", "Answer = ____"),
        q("What comes just after 39?", "fill", "Answer = ____"),
        q("Write all even numbers between 20 and 30.", "fill", "Answer = ____"),
        q("How many tens are in the number 50?", "fill", "Answer = ____"),
        q("A box has 4 rows of 10 pencils each and 3 extra pencils. How many pencils in total?", "word", "Total = ____", "4 rows of 10 and 3 extra"),
        q("Round 43 to the nearest ten.", "fill", "Answer = ____"),
        q("Round 27 to the nearest ten.", "fill", "Answer = ____"),
        q("Write three numbers that are between 30 and 40.", "fill", "Answer = ____"),
        q("Spot the mistake: 'The expanded form of 34 is 3 + 4.' What is the correct expanded form?", "fill", "Correct = ____"),
        q("How many 2-digit numbers are there altogether?", "fill", "Answer = ____"),
    ]

# L1B Sheet 3 — Practice
def _L1B_3():  # Counting 1-100, Sheet 3 Practice
    return [
        cb("Counting 1–100 Practice", ["Expanded form: 72 = 70 + 2.", "Round to nearest 10: look at ones digit. ≥5 round up, <5 round down.", "Order by comparing tens first, then ones."], "Round 67 → ones is 7 ≥ 5 → round up → 70"),
        q("Write 91 in expanded form.", "fill", "Answer = ____"),
        q("Write 65 in expanded form.", "fill", "Answer = ____"),
        q("Write as a number: 50 + 3 = ____.", "fill", "Answer = ____"),
        q("Write as a number: 80 + 0 = ____.", "fill", "Answer = ____"),
        q("Round 43 to the nearest 10.", "fill", "Answer = ____"),
        q("Round 76 to the nearest 10.", "fill", "Answer = ____"),
        q("Round 95 to the nearest 10.", "fill", "Answer = ____"),
        q("Order from smallest to largest: 81, 18, 80, 8, 88.", "fill", "Answer = ____"),
        q("Order from largest to smallest: 52, 25, 55, 5.", "fill", "Answer = ____"),
        q("How many numbers are between 50 and 60 (not including 50 and 60)?", "fill", "Answer = ____"),
        q("Write all multiples of 5 from 5 to 50.", "fill", "Answer = ____"),
        q("What is 10 more than 54?", "fill", "Answer = ____"),
        q("What is 10 less than 73?", "fill", "Answer = ____"),
        q("Ravi counts by 2s starting from 2: 2, 4, 6, ___, ___, ___, ___, 16. Fill in the gaps.", "fill", "Answer = ____"),
        q("Count by 5s: 5, 10, 15, ___, ___, 30, ___, 40.", "fill", "Answer = ____"),
        q("The number 86 is between ___ tens and ___ tens.", "fill", "Answer = ____"),
        q("Write a number between 90 and 100 that has a 4 in the ones place.", "fill", "Answer = ____"),
        q("A library has 6 shelves with 10 books each and 8 more books on a table. Total books = ____.", "word", "Total = ____", "6 shelves of 10 and 8 extra"),
        q("True or False: Rounding 75 to the nearest 10 gives 70.", "fill", "Answer = ____"),
    ]

# L1A Sheet 4 — Mastery
def _L1A_4():  # Counting 1-50, Sheet 4 Mastery
    return [
        cb("Mastery: Counting and Place Value", ["The value of a digit depends on its POSITION.", "Tens place is worth 10 times the ones place.", "Use comparison and ordering to solve problems."], "In 48: value of 4 is 40, which is 10 × 4"),
        q("In 37, what is the value of digit 3? What is the value of digit 7?", "fill", "3 = ____   7 = ____"),
        q("Write 50 in expanded form and explain what each part means.", "fill", "Answer = ____"),
        q("Order from smallest to largest: 47, 4, 74, 40, 44.", "fill", "Answer = ____"),
        q("How many 2-digit numbers are there in total? Explain how you know.", "fill", "Answer = ____"),
        q("The value of 4 in 48 is how many times the value of 4 in 14?", "fill", "Answer = ____ times"),
        q("Ravi says '19 is greater than 91.' Is he correct? Explain why.", "fill", "Answer = ____"),
        q("What pattern do you notice? 5, 10, 15, 20, ___. Write the next three terms.", "fill", "Next three = ____"),
        q("What pattern? 48, 46, 44, 42, ___. Write the next term and state the rule.", "fill", "Next = ____  Rule = ____"),
        q("Write 5 numbers that are multiples of 10 up to 50.", "fill", "Answer = ____"),
        q("What is the largest 2-digit even number?", "fill", "Answer = ____"),
        q("What is the smallest 2-digit odd number?", "fill", "Answer = ____"),
        q("How many 2-digit multiples of 5 are there?", "fill", "Answer = ____"),
        q("A number has 4 tens and its ones digit equals its tens digit. What is the number?", "fill", "Answer = ____"),
        q("Between 25 and 35, how many numbers have the digit 2 in the ones place?", "fill", "Answer = ____"),
        q("Meena counts: 2, 4, 6, 8, ___, ___, ___. Write the next three numbers.", "fill", "Answer = ____"),
        q("Write a 2-digit number where the sum of tens digit and ones digit equals 9.", "fill", "Answer = ____"),
        q("Is the number of days in a week (7) a 2-digit number? Explain.", "fill", "Answer = ____"),
        q("Ravi has 45 stamps. He gives away some and has 28 left. How many did he give away?", "word", "Answer = ____", "45 stamps, 28 left"),
        q("Challenge: I am a 2-digit number. My tens digit is 3 more than my ones digit. I am less than 50. What am I?", "fill", "Answer = ____"),
    ]

# L1B Sheet 4 — Mastery
def _L1B_4():  # Counting 1-100, Sheet 4 Mastery
    return [
        cb("Mastery: Counting to 100", ["Apply place value, skip counting, ordering, and rounding together.", "Think about WHY each rule works.", "Explain your reasoning clearly."], "Skip count by 4: 4, 8, 12, 16, 20 — rule is add 4 each time"),
        q("What is the value of the digit 7 in 73? What is the value of the digit 3 in 73?", "fill", "7 = ____   3 = ____"),
        q("How many 2-digit multiples of both 2 and 5 are there between 10 and 100?", "fill", "Answer = ____"),
        q("Meena counts in 4s: 4, 8, 12, 16, ___. What is the 10th number she says?", "fill", "10th number = ____"),
        q("I am a 2-digit number. I am a multiple of 9. I am less than 50. What could I be? Write all answers.", "fill", "Answer = ____"),
        q("Round each of these to the nearest 10: 32, 47, 55, 68, 75.", "fill", "Answers = ____"),
        q("Ravi rounds 45 to 40. Is he correct? Explain the rule for rounding 5.", "fill", "Answer = ____"),
        q("Write a number between 60 and 80 that rounds to 70. Can you find more than one?", "fill", "Answer = ____"),
        q("Order: 57, 75, 77, 7, 70, 17. Smallest to largest.", "fill", "Answer = ____"),
        q("How many numbers between 1 and 100 have the digit 7 in the tens place?", "fill", "Answer = ____"),
        q("How many numbers between 1 and 100 have the digit 7 in the ones place?", "fill", "Answer = ____"),
        q("What patterns do you notice in the 100-chart when you colour all multiples of 3?", "fill", "Pattern = ____"),
        q("Spot the error: 'The number 92 rounds to 100 because it is close to 100.' Explain the correct answer.", "fill", "Answer = ____"),
        q("A shopkeeper has 10 boxes with 10 oranges each. He sells 23 oranges. How many are left?", "word", "Left = ____", "10 boxes of 10 minus 23"),
        q("What is the 20th multiple of 4?", "fill", "Answer = ____"),
        q("Write all 2-digit numbers that use only the digits 3 and 7 (can repeat).", "fill", "Answer = ____"),
        q("If I count by 3s starting from 3, will I reach 100? Explain.", "fill", "Answer = ____"),
        q("The sum of the digits of a 2-digit number is 11. What could the number be? Write all answers.", "fill", "Answer = ____"),
        q("Challenge: A number is 8 less than the largest 2-digit number. What is it?", "fill", "Answer = ____"),
        q("True or False: There are more even 2-digit numbers than odd 2-digit numbers.", "fill", "Answer = ____"),
    ]

# ═══════════════════════════════════════════════════════════════
# LEVEL 1C — Before / After Numbers
# ═══════════════════════════════════════════════════════════════
def _L1C_1():
    return [
        cb("Before and After", ["The number BEFORE is one less: before 8 is 7.", "The number AFTER is one more: after 8 is 9.", "Think of a number line — before is to the LEFT, after is to the RIGHT."], "Before 20 is 19. After 20 is 21."),
        q("Write the number that comes BEFORE 5.", "fill", "Answer = ____"),
        q("Write the number that comes AFTER 5.", "fill", "Answer = ____"),
        q("Write the number that comes BEFORE 10.", "fill", "Answer = ____"),
        q("Write the number that comes AFTER 10.", "fill", "Answer = ____"),
        q("Write the number that comes BEFORE 20.", "fill", "Answer = ____"),
        q("Write the number that comes AFTER 20.", "fill", "Answer = ____"),
        cb("Between", ["A number BETWEEN two numbers is sandwiched in the middle.", "Between 5 and 7 is 6.", "Between 19 and 21 is 20."], "Between 29 and 31 is 30."),
        q("What number is between 3 and 5?", "fill", "Answer = ____"),
        q("What number is between 10 and 12?", "fill", "Answer = ____"),
        q("What number is between 24 and 26?", "fill", "Answer = ____"),
        q("What number is between 39 and 41?", "fill", "Answer = ____"),
        q("What number is between 49 and 51?", "fill", "Answer = ____"),
        cb("Just Before and Just After", ["JUST BEFORE means the number immediately to the left.", "JUST AFTER means the number immediately to the right.", "There is no other number in between."], "Just before 30: 29.  Just after 30: 31."),
        q("Write the number just before 15.", "fill", "Answer = ____"),
        q("Write the number just after 15.", "fill", "Answer = ____"),
        q("Write the number just before 40.", "fill", "Answer = ____"),
        q("Write the number just after 49.", "fill", "Answer = ____"),
        q("Write: before, the number, after for 25. ___ , 25 , ___", "fill", "Answer = ____"),
        q("Ravi says the number before 30 is 31. Is he correct? What is the correct answer?", "fill", "Answer = ____"),
        q("Write the number just before 100.", "fill", "Answer = ____"),
        q("Write the number just after 99.", "fill", "Answer = ____"),
    ]

def _L1C_2():
    return [
        cb("Before, After and Between — Concept", ["'Before' = subtract 1.  'After' = add 1.", "For any number n: before = n−1, after = n+1.", "'Between' x and y (consecutive): the one in the middle."], "Before 47 = 47−1 = 46.  After 47 = 47+1 = 48."),
        q("Write before and after 33: ___ , 33 , ___", "fill", "Answer = ____"),
        q("Write before and after 59: ___ , 59 , ___", "fill", "Answer = ____"),
        q("Write before and after 79: ___ , 79 , ___", "fill", "Answer = ____"),
        q("Write before and after 99: ___ , 99 , ___", "fill", "Answer = ____"),
        q("What is 1 less than 70?", "fill", "Answer = ____"),
        q("What is 1 more than 89?", "fill", "Answer = ____"),
        cb("Numbers between a range", ["Write all numbers between 15 and 20: 16, 17, 18, 19.", "Do NOT include 15 or 20 themselves.", "Count carefully — don't skip any."], "Between 30 and 35: 31, 32, 33, 34"),
        q("Write all numbers between 20 and 25.", "fill", "Answer = ____"),
        q("Write all numbers between 47 and 52.", "fill", "Answer = ____"),
        q("How many numbers are between 10 and 15?", "fill", "Answer = ____"),
        q("How many numbers are between 40 and 46?", "fill", "Answer = ____"),
        q("True or False: 50 is between 49 and 51.", "fill", "Answer = ____"),
        cb("Applying before and after", ["Use before/after to find neighbours of any number.", "Helpful for checking if a number is in order."], "Neighbours of 68: 67 and 69"),
        q("What are the neighbours of 72? ___ and ___", "fill", "Answer = ____"),
        q("What are the neighbours of 98? ___ and ___", "fill", "Answer = ____"),
        q("Is 55 between 54 and 56? ____", "fill", "Answer = ____"),
        q("Is 23 between 21 and 26? ____", "fill", "Answer = ____"),
        q("Write the number that is 1 before 100.", "fill", "Answer = ____"),
        q("Write three numbers: just before 50, 50 itself, just after 50.", "fill", "Answer = ____"),
        q("Spot the mistake: 'The number after 39 is 41.' What is correct?", "fill", "Answer = ____"),
        q("What is the number exactly halfway between 40 and 42?", "fill", "Answer = ____"),
    ]

def _L1C_3():
    return [
        cb("Before / After Practice", ["Apply before and after to any 2-digit number.", "Useful for sequencing and ordering tasks.", "Always check: does before + 1 = the number?"], "Check: before 56 = 55. Test: 55+1=56 ✓"),
        q("Fill in: ___ , 38 , ___", "fill", "Answer = ____"),
        q("Fill in: ___ , 62 , ___", "fill", "Answer = ____"),
        q("Fill in: ___ , 100 , ___", "fill", "Answer = ____"),
        q("Write all numbers between 35 and 40.", "fill", "Answer = ____"),
        q("Write all numbers between 88 and 93.", "fill", "Answer = ____"),
        q("How many whole numbers are between 45 and 50?", "fill", "Answer = ____"),
        cb("Filling sequences", ["Use before/after rules to complete number sequences.", "Fill missing neighbours in a chain."], "25, ___, 27 → fill 26"),
        q("Fill in: 17 , ___ , 19", "fill", "Answer = ____"),
        q("Fill in: ___ , 44 , 45", "fill", "Answer = ____"),
        q("Fill in: 69 , 70 , ___", "fill", "Answer = ____"),
        q("Fill in: ___ , 80 , 81 , ___", "fill", "Answer = ____"),
        q("Fill in: 99 , ___ , 101", "fill", "Answer = ____"),
        cb("Word problems with before/after", ["'One more than' means after.", "'One less than' means before.", "Key words: next, previous, neighbour."], "One less than 50 is 49. One more than 50 is 51."),
        q("The class has 36 students. One more joins. New total = ____.", "word", "Total = ____", "36 students plus 1"),
        q("Ravi had 28 stickers. He gave away 1. He has ____ now.", "word", "Left = ____", "28 minus 1"),
        q("What is one more than 99?", "fill", "Answer = ____"),
        q("What is one less than 80?", "fill", "Answer = ____"),
        q("True or False: The number before 71 is 70.", "fill", "Answer = ____"),
        q("True or False: The number after 100 is 102.", "fill", "Answer = ____"),
        q("Write the number that is 1 more than the largest 2-digit number.", "fill", "Answer = ____"),
        q("Write the number that is 1 less than the smallest 2-digit number.", "fill", "Answer = ____"),
    ]

def _L1C_4():
    return [
        cb("Mastery: Before / After", ["Use before/after in multi-step reasoning.", "Combine with place value and comparison.", "Explain your reasoning clearly."], "If a number is between 48 and 52, it could be 49, 50, or 51."),
        q("Write all 2-digit numbers that are between 95 and 102.", "fill", "Answer = ____"),
        q("I am between 63 and 67. I am odd. What could I be? Write all answers.", "fill", "Answer = ____"),
        q("The number before me is 49. The number after me is 51. What am I?", "fill", "Answer = ____"),
        q("Is there a whole number between 7 and 8? Explain.", "fill", "Answer = ____"),
        q("How many whole numbers are between 90 and 100?", "fill", "Answer = ____"),
        cb("Reasoning with neighbours", ["Think carefully about what 'between' includes and excludes.", "Multiple answers are sometimes possible."], "Between 20 and 30 (exclusive): 21,22,23,24,25,26,27,28,29"),
        q("Spot the mistake: 'There are 5 numbers between 10 and 15.' Correct it.", "fill", "Answer = ____"),
        q("I am 1 more than a multiple of 10. I am less than 50. Write all numbers I could be.", "fill", "Answer = ____"),
        q("Meena says the number after 99 is 100. Ravi says it is 90. Who is right?", "fill", "Answer = ____"),
        q("What number has 45 as its 'before' and 47 as its 'after'?", "fill", "Answer = ____"),
        q("Write 3 numbers that each have a before-neighbour greater than 50.", "fill", "Answer = ____"),
        cb("Challenge problems", ["Apply before/after logic to solve puzzles.", "More than one step may be needed."], "If n is between 30 and 32, n must be 31"),
        q("I am a 2-digit number. My after-neighbour has a 0 in the ones place. What could I be? List all.", "fill", "Answer = ____"),
        q("My before-neighbour and after-neighbour add up to 60. What am I?", "fill", "Answer = ____"),
        q("How many pairs of consecutive numbers are both less than 10?", "fill", "Answer = ____"),
        q("Ravi lists: 38, 39, 41, 42. He missed one number. Which one?", "fill", "Answer = ____"),
        q("What is the sum of the number before 10 and the number after 10?", "fill", "Answer = ____"),
        q("True or False: Every whole number has exactly one number before it.", "fill", "Answer = ____"),
        q("Write a number whose before-neighbour is even and after-neighbour is also even.", "fill", "Answer = ____"),
        q("The sum of three consecutive numbers is 33. What are the three numbers?", "fill", "Answer = ____"),
    ]


# ═══════════════════════════════════════════════════════════════
# LEVEL 1D — Greater / Smaller
# ═══════════════════════════════════════════════════════════════
def _L1D_1():
    return [
        cb("Greater and Smaller", ["GREATER means MORE. SMALLER means LESS.", "We use > for greater and < for smaller.", "Memory trick: the open mouth always faces the BIGGER number."], "8 > 5 (8 is greater than 5)   3 < 7 (3 is smaller than 7)"),
        q("Which is greater: 8 or 5?", "fill", "Answer = ____"),
        q("Which is smaller: 12 or 21?", "fill", "Answer = ____"),
        q("Write > or < :  9 ___ 6", "fill", "Answer = ____"),
        q("Write > or < :  4 ___ 14", "fill", "Answer = ____"),
        q("Write > or < :  30 ___ 30", "fill", "Answer = ____"),
        cb("Comparing 2-digit numbers", ["Compare the TENS digit first.", "If tens are equal, compare the ONES digit.", "The larger tens digit means the larger number."], "45 vs 43: tens are equal (4=4), so compare ones: 5 > 3, so 45 > 43"),
        q("Write > or < :  56 ___ 65", "fill", "Answer = ____"),
        q("Write > or < :  72 ___ 72", "fill", "Answer = ____"),
        q("Write > or < :  89 ___ 98", "fill", "Answer = ____"),
        q("Write > or < :  47 ___ 47", "fill", "Answer = ____"),
        q("Circle the GREATER number:   34    or    43", "fill", "Answer = ____"),
        cb("Finding greatest and smallest", ["Greatest = largest number in a group.", "Smallest = least/lowest number in a group."], "From 14, 41, 4, 40: greatest = 41, smallest = 4"),
        q("Write the greatest of: 34, 43, 30, 40", "fill", "Greatest = ____"),
        q("Write the smallest of: 76, 67, 70, 60", "fill", "Smallest = ____"),
        q("Ravi has 42 cards. Meena has 24. Who has more?", "word", "Answer = ____", "42 and 24"),
        q("True or False:  45 < 54", "fill", "Answer = ____"),
        q("True or False:  37 > 73", "fill", "Answer = ____"),
        q("Order: 19, 91, 9, 90 — from smallest to greatest", "fill", "Answer = ____"),
        q("Find a number greater than 50 and smaller than 55.", "fill", "Answer = ____"),
        q("Find a number greater than 67 and smaller than 70.", "fill", "Answer = ____"),
    ]

def _L1D_2():
    return [
        cb("Comparing — Concept", ["Use place value to compare: first compare hundreds, then tens, then ones.", "For 2-digit numbers: compare tens first.", "If the tens digits are equal, compare the ones digits."], "Compare 73 and 37: tens 7 > 3, so 73 > 37"),
        q("Write > , < or = :  23 ___ 32", "fill", "Answer = ____"),
        q("Write > , < or = :  45 ___ 45", "fill", "Answer = ____"),
        q("Write > , < or = :  88 ___ 80", "fill", "Answer = ____"),
        q("Write > , < or = :  99 ___ 100", "fill", "Answer = ____"),
        q("Write > , < or = :  50 ___ 50", "fill", "Answer = ____"),
        q("Write > , < or = :  17 ___ 71", "fill", "Answer = ____"),
        cb("Ordering numbers", ["Ascending order = smallest to largest.", "Descending order = largest to smallest.", "Compare pairs, swap if needed."], "Ascending: 12, 21, 22, 31.   Descending: 31, 22, 21, 12"),
        q("Order smallest to largest: 35, 13, 41, 22", "fill", "Answer = ____"),
        q("Order largest to smallest: 28, 82, 18, 81", "fill", "Answer = ____"),
        q("Order smallest to largest: 7, 70, 17, 71", "fill", "Answer = ____"),
        q("Order largest to smallest: 55, 5, 50, 15", "fill", "Answer = ____"),
        q("Write the largest 2-digit number that has a 3 in the tens place.", "fill", "Answer = ____"),
        cb("Using > and < in sentences", ["Write comparison sentences using > or <.", "Both 'a > b' and 'b < a' say the same thing."], "72 > 27  means the same as  27 < 72"),
        q("Write two comparison sentences for 56 and 65.", "fill", "Answer = ____"),
        q("Which is closer to 50 — 47 or 53?", "fill", "Answer = ____"),
        q("The tens digit of 49 is ____", "fill", "Answer = ____"),
        q("True or False: 50 is greater than 49.", "fill", "Answer = ____"),
        q("Meena says 23 > 32 because 2 + 3 > 3 + 2. Is she right? Explain.", "fill", "Answer = ____"),
        q("Write the smallest 2-digit number that is greater than 80.", "fill", "Answer = ____"),
        q("Write three 2-digit numbers greater than 45 and less than 52.", "fill", "Answer = ____"),
        q("True or False: If A > B and B > C, then A > C.", "fill", "Answer = ____"),
    ]

def _L1D_3():
    return [
        cb("Greater / Smaller Practice", ["Apply comparison to various contexts.", "Useful for comparing scores, lengths, prices, quantities.", "Always use a consistent method: compare place values."], "Lengths: 37 cm > 29 cm.  Prices: Rs 55 < Rs 58"),
        q("Write > , < or = :  64 ___ 46", "fill", "Answer = ____"),
        q("Write > , < or = :  100 ___ 99", "fill", "Answer = ____"),
        q("Write > , < or = :  33 ___ 33", "fill", "Answer = ____"),
        q("Order ascending: 81, 18, 80, 8, 11", "fill", "Answer = ____"),
        q("Order descending: 72, 27, 77, 22, 70", "fill", "Answer = ____"),
        q("The temperature on Monday is 32°C. On Tuesday it is 29°C. Which is warmer?", "word", "Answer = ____", "32°C and 29°C"),
        cb("Three-number comparison", ["Compare three numbers by finding the greatest and smallest.", "Use two comparisons."], "Compare 34, 43, 40: 34 < 40 < 43, so greatest=43, smallest=34"),
        q("Find the greatest of: 52, 25, 50", "fill", "Greatest = ____"),
        q("Find the smallest of: 83, 38, 80", "fill", "Smallest = ____"),
        q("Arrange in ascending order: 66, 6, 60", "fill", "Answer = ____"),
        q("Arrange in descending order: 45, 54, 44, 55", "fill", "Answer = ____"),
        q("A rope is 48 cm. Another is 84 cm. Which is longer?", "word", "Answer = ____", "48 cm and 84 cm"),
        cb("Number challenges", ["Apply comparison skills to solve puzzles.", "Think about what 'between' tells you about size."], "A number between 60 and 70 is greater than 60 but less than 70"),
        q("Write all numbers greater than 95 and less than 100.", "fill", "Answer = ____"),
        q("Write three numbers less than 20 but greater than 15.", "fill", "Answer = ____"),
        q("Is 90 greater than 89? Write the comparison sign.", "fill", "Answer = ____"),
        q("Write > or < :  99 ___ 101", "fill", "Answer = ____"),
        q("Spot the mistake: 'Rs 34 > Rs 43 because 34 has a 3 and 43 has a 4.' Fix it.", "fill", "Answer = ____"),
        q("How many 2-digit numbers are greater than 90?", "fill", "Answer = ____"),
        q("A shopkeeper has 67 mangoes and 76 oranges. He has more ____.", "word", "Answer = ____", "67 mangoes and 76 oranges"),
        q("True or False: The largest 2-digit number is greater than any 1-digit number.", "fill", "Answer = ____"),
    ]

def _L1D_4():
    return [
        cb("Mastery: Greater / Smaller", ["Apply comparison with reasoning, multi-step logic.", "Justify your answer using place value.", "Look for patterns in comparison problems."], "If A > B > C, then A is the greatest and C is the smallest."),
        q("Order: 37, 3, 73, 33, 7 — ascending", "fill", "Answer = ____"),
        q("Order: 91, 19, 99, 9, 90 — descending", "fill", "Answer = ____"),
        q("I am a 2-digit number. I am less than 50. My tens digit is greater than my ones digit. What could I be? List five.", "fill", "Answer = ____"),
        q("True or False: If a 2-digit number's tens digit is larger, that number is always greater.", "fill", "Answer = ____"),
        q("Ravi says 'a 2-digit number is always greater than a 1-digit number.' Is he always correct? Explain.", "fill", "Answer = ____"),
        cb("Comparing more than two numbers", ["With many numbers, find the greatest and smallest by elimination.", "Start with tens digits, then move to ones."], "From 44,47,74,77: smallest tens=44, greatest tens=77"),
        q("Write the 3rd largest number from: 28, 82, 48, 84, 88, 22.", "fill", "Answer = ____"),
        q("A cricket team scores 67 in Match A and 76 in Match B. In which match did they score more, and by how much?", "word", "Answer = ____", "67 and 76"),
        q("How many 2-digit numbers have a tens digit greater than their ones digit?", "fill", "Answer = ____"),
        q("Write a 2-digit number where the ones digit is exactly 3 more than the tens digit.", "fill", "Answer = ____"),
        q("Find all 2-digit numbers where both digits are the same and the number is greater than 50.", "fill", "Answer = ____"),
        cb("Using inequalities", ["Chain inequalities: a < b < c means a is smallest, c is largest.", "Useful for ordering many numbers at once."], "Fill in: 45 < ___ < 47 → must be 46"),
        q("Fill in: 38 < ___ < 40", "fill", "Answer = ____"),
        q("Fill in: 79 < ___ < 81", "fill", "Answer = ____"),
        q("Fill in a number: 53 < ___ < 58", "fill", "Possible answers = ____"),
        q("Is it possible to have a whole number where 30 < n < 31? Explain.", "fill", "Answer = ____"),
        q("Write a 2-digit number n so that n > 60 and n < 65 and n is even.", "fill", "Answer = ____"),
        q("Three friends have scores: Ravi > 70, Meena < 80, Priya = 75. What can you say about their order?", "fill", "Answer = ____"),
        q("Spot the error: '21 < 12 because 1 is smaller than 2.' Explain the correct answer.", "fill", "Answer = ____"),
        q("Challenge: A 2-digit number reversed gives a smaller number. The difference between the number and its reverse is 27. What is the number? (Hint: 63 reversed is 36.)", "fill", "Answer = ____"),
    ]


# ═══════════════════════════════════════════════════════════════
# LEVEL 1E — Missing Numbers
# ═══════════════════════════════════════════════════════════════
def _L1E_1():
    return [
        cb("Missing Numbers", ["A blank in a sequence means something is HIDDEN.", "Look at the numbers around the blank — they give clues.", "Find the pattern: are the numbers going up or down, and by how much?"], "3, ___, 5 — going up by 1 each time — missing number is 4"),
        q("Fill in: 1, 2, ___, 4, 5", "fill", "Answer = ____"),
        q("Fill in: 6, ___, 8, 9, ___", "fill", "Answer = ____"),
        q("Fill in: 15, 16, ___, ___, 19", "fill", "Answer = ____"),
        q("Fill in: ___, 22, 23, 24, ___", "fill", "Answer = ____"),
        q("Fill in: 35, ___, 37, ___, 39", "fill", "Answer = ____"),
        cb("Skip-count patterns", ["Some sequences skip by 2, 5, or 10 each time.", "First find the rule, then fill the blank."], "10, 20, ___, 40 — rule is +10 each time — missing is 30"),
        q("Fill in: 10, 20, ___, 40, ___", "fill", "Answer = ____"),
        q("Fill in: 5, 10, 15, ___, 25", "fill", "Answer = ____"),
        q("Fill in: 2, 4, ___, 8, ___, 12", "fill", "Answer = ____"),
        q("Fill in: 50, ___, 70, ___, 90", "fill", "Answer = ____"),
        q("Fill in: ___, 45, ___, 35, 30", "fill", "Answer = ____"),
        cb("Missing numbers in additions", ["Use inverse operations: if 6 + ___ = 10, think 10 − 6 = ___.", "Check by substituting back."], "7 + ___ = 12 → 12 − 7 = 5 → missing is 5"),
        q("3 + ___ = 8", "fill", "Missing = ____"),
        q("___ + 5 = 12", "fill", "Missing = ____"),
        q("15 − ___ = 9", "fill", "Missing = ____"),
        q("___ − 6 = 7", "fill", "Missing = ____"),
        q("20 + ___ = 34", "fill", "Missing = ____"),
        q("___ + 14 = 30", "fill", "Missing = ____"),
        q("50 − ___ = 27", "fill", "Missing = ____"),
        q("___ − 15 = 20", "fill", "Missing = ____"),
    ]

def _L1E_2():
    return [
        cb("Finding missing numbers — Concept", ["Step 1: Find the rule (add or subtract, and by how much).", "Step 2: Apply the rule to find the missing number.", "Step 3: Always CHECK by substituting back."], "Rule +3: 6, 9, ___, 15 → missing = 9+3 = 12. Check: 12+3=15 ✓"),
        q("Find the rule and fill in: 4, 8, ___, 16, ___", "fill", "Rule=____ Missing=____"),
        q("Find the rule and fill in: 30, 25, ___, 15, ___", "fill", "Rule=____ Missing=____"),
        q("Find the rule and fill in: 3, 6, 9, ___, ___, 18", "fill", "Rule=____ Missing=____"),
        q("Find the rule and fill in: 100, 90, ___, 70, ___", "fill", "Rule=____ Missing=____"),
        q("Find the rule and fill in: 1, 3, ___, 7, ___, 11", "fill", "Rule=____ Missing=____"),
        q("Find the rule and fill in: 20, 17, ___, 11, ___", "fill", "Rule=____ Missing=____"),
        cb("Algebraic thinking", ["We can use a letter to stand for the missing number.", "n + 5 = 12 means: what number added to 5 gives 12?", "n = 12 − 5 = 7"], "Find n: n + 9 = 16 → n = 16 − 9 = 7"),
        q("Find the missing number: ___ + 8 = 17", "fill", "Missing = ____"),
        q("Find the missing number: 24 − ___ = 16", "fill", "Missing = ____"),
        q("Find the missing number: ___ × 4 = 20", "fill", "Missing = ____"),
        q("Find the missing number: 18 ÷ ___ = 6", "fill", "Missing = ____"),
        q("Fill in: 13, ___, ___, 22, ___, 28 (rule +3)", "fill", "Answer = ____"),
        cb("Two missing numbers", ["Sometimes two numbers are missing — use the rule to find both.", "Fill in left-to-right once you know the rule."], "Rule +4: 8, ___, 16, ___ → 12 and 20"),
        q("Fill in (rule +5): 15, ___, ___, 30, 35", "fill", "Answer = ____"),
        q("Fill in (rule −4): 40, ___, 32, ___, 24", "fill", "Answer = ____"),
        q("Fill in: 6, 12, ___, 24, ___  (rule ×2)", "fill", "Answer = ____"),
        q("Fill in: ___, 49, 56, 63, ___ (rule +7)", "fill", "Answer = ____"),
        q("Fill in: 64, ___, ___, 43, 36 (rule −7)", "fill", "Answer = ____"),
        q("Check this sequence and find the error: 5, 10, 15, 25, 30", "fill", "Error at = ____"),
        q("Write your own missing-number sequence using rule +6, with one blank.", "fill", "Answer = ____"),
        q("Ravi says the missing number in 11, ___, 33, 44 is 21. Is he correct?", "fill", "Answer = ____"),
    ]

def _L1E_3():
    return [
        cb("Missing Numbers Practice", ["Use patterns, inverse operations, and logical reasoning.", "Apply to real-life contexts: ages, prices, scores."], "Missing score: 12 + ___ = 30 → 18 more runs needed"),
        q("Fill in: ___, 33, 39, 45, ___", "fill", "Answer = ____"),
        q("Fill in: 81, ___, 63, ___, 45", "fill", "Answer = ____"),
        q("Fill in: 7, ___, 21, 28, ___", "fill", "Answer = ____"),
        q("Fill in: ___, 16, 19, 22, ___", "fill", "Answer = ____"),
        q("Fill in: 50, 41, ___, 23, ___", "fill", "Answer = ____"),
        q("Find the missing number: ___ + 27 = 50", "fill", "Missing = ____"),
        cb("Missing numbers in word problems", ["Write an equation from the word problem, then solve.", "'Altogether' → add.  'Left' → subtract.  'Each' → multiply or divide."], "Ravi has 15 books. After getting some more he has 23. Got ___ = 23−15 = 8"),
        q("Meena has 18 sweets. She eats some and has 11 left. How many did she eat?", "word", "Answer = ____", "18 and 11"),
        q("A bag has some apples. 6 more are added. Now there are 25. How many at the start?", "word", "Answer = ____", "25 total, 6 added"),
        q("Ravi scores ___ runs in the 2nd innings. His total is 47. He scored 29 in the 1st. Find ___.", "word", "Answer = ____", "47 total, 29 in 1st innings"),
        q("A class had some students. 4 were absent. 28 were present. Total students = ____.", "word", "Answer = ____", "4 absent, 28 present"),
        q("Find the missing number: 7 × ___ = 63", "fill", "Missing = ____"),
        cb("Complex sequences", ["Some sequences use two operations or have non-constant differences.", "Look at the DIFFERENCES between terms."], "Differences: 1, 3, 5, 7 means each gap increases by 2"),
        q("Fill in: 1, 2, 4, 7, 11, ___, ___  (differences increase by 1 each time)", "fill", "Answer = ____"),
        q("Fill in: ___, 5, ___, 17, 23  (differences increase by 1 each time: 2,4,6,8)", "fill", "Answer = ____"),
        q("What number is missing? ___, 12, 18, 24, 30 (rule +6)", "fill", "Answer = ____"),
        q("Check and correct: 5, 10, 15, 21, 25 (rule +5)", "fill", "Error: ____ should be ____"),
        q("Two missing: 4, ___, 16, ___, 36  (differences are 4,8,12,16)", "fill", "Answer = ____"),
        q("Fill in: 1, 1, 2, 3, 5, ___, 13  (Fibonacci: each = sum of previous two)", "fill", "Answer = ____"),
        q("A shop sold 12 Monday, 15 Tuesday, 18 Wednesday, ___ Thursday (rule +3).", "word", "Answer = ____", "12, 15, 18, ..."),
        q("Fill in: 100, 95, ___, 85, ___, 75", "fill", "Answer = ____"),
    ]

def _L1E_4():
    return [
        cb("Mastery: Missing Numbers", ["Combine pattern-finding, inverse operations, and multi-step logic.", "Write the rule clearly before finding missing values.", "Verify every answer."], "Two unknowns: x + y = 10 and x − y = 4 → x = 7, y = 3"),
        q("Fill in: 2, 6, 18, ___, 162  (rule ×3)", "fill", "Answer = ____"),
        q("Fill in: 80, ___, 20, ___, 5  (rule ÷2)", "fill", "Answer = ____"),
        q("Find both missing numbers: ___ + ___ = 20, and the first is 4 more than the second.", "fill", "Answer = ____"),
        q("The differences in this sequence are 2, 4, 6, 8. First term is 3. Write the first 5 terms.", "fill", "Answer = ____"),
        q("I multiply a missing number by 6, then add 4. The result is 34. What is the missing number?", "fill", "Answer = ____"),
        q("Ravi's age now is missing. In 5 years he will be 18. In 3 years he will be ___.", "word", "Answers = ____", "age now and in 3 years"),
        cb("Pattern and proof", ["Describe the rule in words AND as a mathematical operation.", "Prove your rule works by checking ALL terms."], "Rule: add consecutive odd numbers (1,3,5,7...) → gives 1,4,9,16,25 (perfect squares)"),
        q("Spot the error in: 3, 9, 27, 54, 243. Fix it and explain.", "fill", "Answer = ____"),
        q("A sequence has first term 5 and rule +7. What is the 8th term?", "fill", "Answer = ____"),
        q("A sequence has first term 96 and rule ÷2. After how many terms does it fall below 10?", "fill", "Answer = ____"),
        q("Find the missing number: 5, ___, 20, 40, 80  (look at both add and multiply patterns)", "fill", "Answer = ____"),
        q("Write a sequence of 5 numbers where each term is the sum of the two before it, starting with 2 and 3.", "fill", "Answer = ____"),
        cb("Real-world missing numbers", ["Use equations and patterns to solve multi-step problems."], "Savings: Rs 10, Rs 15, Rs 20... pattern +5. Month 8 = 10 + 7×5 = 45"),
        q("Meena saves Rs 8 in week 1, Rs 12 in week 2, Rs 16 in week 3 (rule +4). How much in week 6?", "word", "Answer = ____", "week 1=8, rule +4"),
        q("A farmer plants 5 seeds in row 1, 10 in row 2, 20 in row 3. How many in row 6?", "word", "Answer = ____", "rule ×2"),
        q("Challenge: A and B are missing. A × B = 24 and A + B = 10. Find A and B.", "fill", "Answer = ____"),
        q("Fill in: ___, 3, 6, 10, 15, 21, ___  (differences: 1,2,3,4,5,6)", "fill", "Answer = ____"),
        q("A number sequence is: 1, 4, 9, 16, ___, 36. What is the rule, and what is the missing number?", "fill", "Answer = ____"),
        q("Is the number 100 in this sequence: 4, 8, 12, 16, ...? Explain how you know.", "fill", "Answer = ____"),
        q("Two consecutive numbers add up to 87. What are they?", "fill", "Answer = ____"),
        q("Three consecutive even numbers add up to 54. What are they?", "fill", "Answer = ____"),
    ]


# ═══════════════════════════════════════════════════════════════
# LEVEL 1F — Number Patterns
# ═══════════════════════════════════════════════════════════════
def _L1F_1():
    return [
        cb("Number Patterns", ["A pattern is a sequence that follows a rule.", "Find what changes from one number to the next.", "Common rules: add 1, add 2, add 5, add 10, subtract 2…"], "2, 4, 6, 8, 10 — rule: add 2 each time"),
        q("Write the next two numbers: 1, 3, 5, 7, ___, ___", "fill", "Answer = ____"),
        q("Write the next two numbers: 10, 20, 30, 40, ___, ___", "fill", "Answer = ____"),
        q("Write the next two numbers: 5, 10, 15, 20, ___, ___", "fill", "Answer = ____"),
        q("Write the next two numbers: 3, 6, 9, 12, ___, ___", "fill", "Answer = ____"),
        q("Write the next two numbers: 100, 90, 80, 70, ___, ___", "fill", "Answer = ____"),
        cb("Finding the rule", ["Look at two consecutive numbers. What is the difference?", "Is it always the same? That's the rule.", "Then use the rule to extend the pattern."], "4, 9, 14, 19 → difference is 5 each time → rule: +5"),
        q("Find the rule: 7, 14, 21, 28 → Rule = ___. Next two = ___", "fill", "Answer = ____"),
        q("Find the rule: 50, 45, 40, 35 → Rule = ___. Next two = ___", "fill", "Answer = ____"),
        q("Find the rule: 2, 4, 8, 16 → Rule = ___. Next = ___", "fill", "Answer = ____"),
        q("Find the rule: 1, 5, 9, 13 → Rule = ___. Next two = ___", "fill", "Answer = ____"),
        q("Find the rule: 64, 32, 16, 8 → Rule = ___. Next = ___", "fill", "Answer = ____"),
        cb("Decreasing patterns", ["Some patterns count DOWN — each number is smaller than the one before.", "The rule is subtraction."], "30, 27, 24, 21 — rule: subtract 3 each time"),
        q("Continue: 48, 44, 40, 36, ___, ___", "fill", "Answer = ____"),
        q("Continue: 99, 88, 77, 66, ___, ___", "fill", "Answer = ____"),
        q("Continue: 60, 55, 50, 45, ___, ___", "fill", "Answer = ____"),
        q("Meena saves Rs 5 per day. Day 1 = Rs 5. Day 2 = Rs 10. Day 5 = Rs ____.", "word", "Answer = ____", "Rs 5 per day"),
        q("Ravi counts: 3, 6, 9, 12. He says the next is 16. Is he right? What is it?", "fill", "Answer = ____"),
        q("Write your own pattern using rule +4, starting at 8. Write 6 terms.", "fill", "Answer = ____"),
        q("Write your own pattern using rule −3, starting at 30. Write 6 terms.", "fill", "Answer = ____"),
        q("Is 45 in the pattern 5, 10, 15, 20, 25…? Explain.", "fill", "Answer = ____"),
    ]

def _L1F_2():
    return [
        cb("Number Patterns — Concept", ["An arithmetic pattern has the same difference between every pair of consecutive terms.", "The first term and the common difference define the whole pattern.", "Term n = first term + (n−1) × difference."], "First term = 3, rule = +5 → 3, 8, 13, 18, 23... The 4th term = 3 + 3×5 = 18"),
        q("Pattern: 6, 11, 16, 21, 26 — what is the first term and the rule?", "fill", "First term=____ Rule=____"),
        q("Pattern: 50, 42, 34, 26 — first term and rule?", "fill", "First term=____ Rule=____"),
        q("Write the first 5 terms of a pattern: first term = 7, rule = +6.", "fill", "Answer = ____"),
        q("Write the first 5 terms: first term = 100, rule = −11.", "fill", "Answer = ____"),
        q("What is the 5th term of: 4, 7, 10, 13, ___?", "fill", "5th term = ____"),
        q("What is the 6th term of: 2, 8, 14, 20, 26, ___?", "fill", "6th term = ____"),
        cb("Even and odd patterns", ["Even numbers: 2, 4, 6, 8, … rule +2.", "Odd numbers: 1, 3, 5, 7, … rule +2.", "Multiples of any number form a pattern too."], "Multiples of 7: 7, 14, 21, 28, 35 — rule +7"),
        q("Write the first 6 even numbers starting from 10.", "fill", "Answer = ____"),
        q("Write the first 6 odd numbers starting from 11.", "fill", "Answer = ____"),
        q("Write the first 6 multiples of 8.", "fill", "Answer = ____"),
        q("Is 72 a term in the pattern of multiples of 9? Explain.", "fill", "Answer = ____"),
        q("Is 50 in the sequence 3, 8, 13, 18, 23…? Explain.", "fill", "Answer = ____"),
        cb("Square and triangle number patterns", ["Square numbers: 1, 4, 9, 16, 25 — each = n².", "Differences between consecutive square numbers: 3, 5, 7, 9 — odd numbers!"], "4th square number = 4² = 16"),
        q("Write the first 5 square numbers.", "fill", "Answer = ____"),
        q("What is the 7th square number?", "fill", "Answer = ____"),
        q("Differences in 1, 4, 9, 16, 25: write the differences.", "fill", "Differences = ____"),
        q("Continue the pattern: 1, 3, 6, 10, 15, ___, ___ (triangle numbers)", "fill", "Answer = ____"),
        q("Spot the error: 5, 10, 15, 21, 25 (rule +5). Find and correct the error.", "fill", "Answer = ____"),
        q("True or False: The rule for 2, 4, 6, 8 is the same as the rule for 12, 14, 16, 18.", "fill", "Answer = ____"),
        q("Write a pattern where every term is a multiple of 6, starting at 6, first 5 terms.", "fill", "Answer = ____"),
        q("A plant grows 4 cm per week. It is 10 cm now. How tall after 5 more weeks?", "word", "Answer = ____", "10 cm, grows 4 cm per week"),
    ]

def _L1F_3():
    return [
        cb("Number Patterns Practice", ["Apply pattern rules to find specific terms.", "Use the formula: term = first + (n−1) × rule.", "Check patterns for errors."], "First=5, rule=+7: term 5 = 5 + 4×7 = 33"),
        q("Pattern 4, 10, 16, 22, ___, ___: what is the 7th term?", "fill", "7th term = ____"),
        q("Pattern 99, 88, 77, ___, ___: what is the 6th term?", "fill", "6th term = ____"),
        q("Which term of 3, 7, 11, 15, 19, ... is equal to 39?", "fill", "Term number = ____"),
        q("Which term of 5, 10, 15, 20, ... is equal to 65?", "fill", "Term number = ____"),
        q("Pattern: 1, 2, 4, 8, 16 (doubling). What is the 7th term?", "fill", "Answer = ____"),
        q("Is 100 a term in the pattern 4, 8, 12, 16…? Explain.", "fill", "Answer = ____"),
        cb("Patterns in problems", ["Real-world patterns involve time, money, distance.", "Set up the rule clearly first."], "Bus fare: Rs 5 first km, Rs 3 for each extra km → 1km=5, 2km=8, 3km=11..."),
        q("A tap drips 3 ml every minute. After 1 min = 3 ml. After 8 min = ___ ml.", "word", "Answer = ____", "3 ml per minute"),
        q("Chairs in rows: Row 1 = 5, Row 2 = 8, Row 3 = 11 (rule +3). Row 7 = ___.", "word", "Answer = ____", "rule +3 starting at 5"),
        q("Ticket price: 1 ticket = Rs 12, 2 = Rs 24, 3 = Rs 36. Price for 7 tickets = Rs ___.", "word", "Answer = ____", "rule ×12"),
        q("Steps on a staircase: Step 1 = 20 cm high, each step adds 20 cm. Step 8 = ___ cm.", "word", "Answer = ____", "20 cm each step"),
        q("Pattern with two rules: 1, 2, 4, 5, 7, 8, 10, 11, ___, ___  (alternately +1 and +2)", "fill", "Answer = ____"),
        cb("Creating patterns", ["Design your own patterns with a clear rule.", "Others should be able to extend them."], "Rule: multiply by 2 then subtract 1 → 1, 1, 1... or 3, 5, 9, 17..."),
        q("Create a decreasing pattern starting at 50 where you subtract 7 each time. Write 6 terms.", "fill", "Answer = ____"),
        q("Create a pattern using rule ×3, starting at 2. Write 5 terms.", "fill", "Answer = ____"),
        q("Spot the error in: 8, 16, 24, 33, 40 (rule +8). Find and correct.", "fill", "Answer = ____"),
        q("Spot the error in: 2, 6, 18, 54, 108 (rule ×3). Find and correct.", "fill", "Answer = ____"),
        q("Pattern: 0, 1, 1, 2, 3, 5, 8, ___, ___ (each = sum of previous two).", "fill", "Answer = ____"),
        q("How many terms of the pattern 5, 10, 15, 20… are less than 100?", "fill", "Answer = ____"),
        q("A pattern starts at 6 and ends at 66 using rule +5. How many terms are there?", "fill", "Answer = ____"),
        q("True or False: Every even number appears in the pattern 0, 2, 4, 6, 8…", "fill", "Answer = ____"),
    ]

def _L1F_4():
    return [
        cb("Mastery: Number Patterns", ["Identify, extend, create and verify patterns.", "Find specific terms and term numbers.", "Distinguish arithmetic (constant difference) from geometric (constant ratio)."], "Arithmetic: +5 each time.  Geometric: ×3 each time.  Both are valid patterns."),
        q("Is the sequence 2, 3, 5, 8, 13, 21 arithmetic or geometric? What is the rule?", "fill", "Answer = ____"),
        q("First term = 3, rule = ×2. Write first 6 terms. Is this arithmetic or geometric?", "fill", "Answer = ____"),
        q("In the pattern 7, 14, 21, 28…: is 91 a term? If yes, which term is it?", "fill", "Answer = ____"),
        q("A pattern has 50 as its 5th term and rule +9. What is its first term?", "fill", "Answer = ____"),
        q("The 3rd and 7th terms of an arithmetic sequence are 17 and 33. What is the rule?", "fill", "Answer = ____"),
        q("Pattern: 1, 8, 27, 64, ___, ___ (cube numbers). Write the rule.", "fill", "Answer = ____"),
        cb("Multi-step pattern problems", ["Apply pattern rules across several steps.", "Combine with addition, multiplication, and algebra."], "If term n = 4n + 3, then term 6 = 4×6+3 = 27"),
        q("Ravi saves Rs 12 in week 1, Rs 17 in week 2, Rs 22 in week 3 (rule +5). In which week will he first save more than Rs 50?", "word", "Answer = ____", "Rs 12, rule +5"),
        q("A bacteria culture doubles every hour. It starts with 5. How many after 6 hours?", "word", "Answer = ____", "starts at 5, doubles each hour"),
        q("An arithmetic sequence has first term 100 and last term 10 using rule −6. How many terms?", "fill", "Answer = ____"),
        q("True or False: All multiples of 4 appear in the pattern 2, 4, 6, 8, 10…", "fill", "Answer = ____"),
        q("Which pattern grows faster for large n: +10 each time, or ×2 each time? Explain.", "fill", "Answer = ____"),
        cb("Pattern proofs and generalisations", ["Give a rule that works for ALL terms, not just the ones you can see.", "Use words or a formula."], "Pattern 3, 6, 9, 12… Rule: 'multiply the term number by 3'  or  'term n = 3n'"),
        q("Write the rule for: 5, 10, 15, 20… using 'term n = …'", "fill", "Answer = ____"),
        q("Write the rule for: 7, 9, 11, 13… using 'term n = …'", "fill", "Answer = ____"),
        q("Using your rule, find the 20th term of: 4, 7, 10, 13…", "fill", "Answer = ____"),
        q("Spot errors in: 1, 4, 9, 15, 25, 36. Fix the sequence and write the rule.", "fill", "Answer = ____"),
        q("A pattern: 1, 2, 4, 7, 11, 16, 22… Find the next two terms and explain the rule.", "fill", "Answer = ____"),
        q("Challenge: Two different patterns both contain the number 24. Can you write them?", "fill", "Answer = ____"),
        q("Two arithmetic sequences start at 5 and 8. Both have rule +3. Will they ever share a common term? Explain.", "fill", "Answer = ____"),
        q("The product of the 3rd and 4th terms of: 2, 4, 8, 16… What is it?", "fill", "Answer = ____"),
    ]


# ═══════════════════════════════════════════════════════════════
# LEVEL 1 CUMULATIVE + REVISION
# ═══════════════════════════════════════════════════════════════
def _L1CUM1_s(sheet):
    """Cumulative: Counting 1-50, Counting 1-100, Before/After"""
    return [
        cb("Cumulative Review: Counting, Place Value, Before/After",
           ["This sheet covers: Counting 1-50, Counting 1-100, Before/After numbers.",
            "Show all working. Check your answers.",
            "Use place value, ordering, and before/after skills."],
           "Review tip: compare tens first, then ones"),
        cb("Section 1: Counting 1-50 and 1-100", ["Recall: tens and ones, skip counting, ordering."], ""),
        q("Write all numbers from 38 to 43: ____", "fill", "Answer = ____"),
        q("10 more than 54 = ____", "fill", "Answer = ____"),
        q("10 less than 70 = ____", "fill", "Answer = ____"),
        q("Order ascending: 47, 74, 44, 77", "fill", "Answer = ____"),
        q("8 tens and 3 ones = ____", "fill", "Answer = ____"),
        q("Round 86 to the nearest 10: ____", "fill", "Answer = ____"),
        cb("Section 2: Before / After Numbers", ["Recall: before = one less, after = one more, between."], ""),
        q("Number before 30: ____", "fill", "Answer = ____"),
        q("Number after 59: ____", "fill", "Answer = ____"),
        q("Numbers between 17 and 21: ____", "fill", "Answer = ____"),
        q("Before and after 45: ___ and ___", "fill", "Before=____ After=____"),
        q("Between 98 and 100: ____", "fill", "Answer = ____"),
        q("Before 100: ____", "fill", "Answer = ____"),
        q("After 39: ____", "fill", "Answer = ____"),
        q("Fill in: 62, 63, ___, ___, 66", "fill", "Answer = ____"),
        q("True or False: The number after 99 is 100.", "fill", "Answer = ____"),
        q("Count by 10s: 20, 30, ___, 50, ___", "fill", "Answer = ____"),
        q("Write value of digit 7 in 73: ____", "fill", "Answer = ____"),
        q("How many 2-digit numbers are between 90 and 100?", "fill", "Answer = ____"),
        q("A box has 4 rows of 10 pencils and 5 extra. Total = ____.", "word", "Total = ____", "4 rows of 10 and 5 extra"),
        q("True or False: Between 49 and 51 there are exactly 2 whole numbers.", "fill", "Answer = ____"),
    ]

def _L1CUM2_s(sheet):
    """Cumulative: Greater/Smaller, Missing numbers, Number patterns"""
    return [
        cb("Cumulative Review: Comparison, Missing Numbers, Patterns",
           ["This sheet covers: Greater/Smaller, Missing numbers, Number patterns.",
            "Show all working. Check every answer.",
            "Use comparison, inverse operations, and pattern rules."],
           "Review tip: find the rule first, then fill the blank"),
        cb("Section 1: Greater / Smaller", ["Recall: compare tens first, then ones. Use > < =."], ""),
        q("Write > or < : 54 ___ 45", "fill", "Answer = ____"),
        q("Write > or < : 82 ___ 82", "fill", "Answer = ____"),
        q("Greatest of 34, 43, 30, 40: ____", "fill", "Answer = ____"),
        q("Order ascending: 92, 29, 9, 90: ____", "fill", "Answer = ____"),
        q("True or False: 67 < 76", "fill", "Answer = ____"),
        q("Smallest of 76, 67, 70, 60: ____", "fill", "Answer = ____"),
        cb("Section 2: Missing Numbers", ["Recall: find the rule, use inverse operations."], ""),
        q("Fill in: 25, ___, 27, ___, 29", "fill", "Answer = ____"),
        q("3 + ___ = 11", "fill", "Missing = ____"),
        q("___ − 5 = 8", "fill", "Missing = ____"),
        q("Fill in: 60, ___, 80, ___, 100", "fill", "Answer = ____"),
        q("___ + 23 = 47", "fill", "Missing = ____"),
        cb("Section 3: Number Patterns", ["Recall: find rule, extend, check."], ""),
        q("Rule +3: 6, 9, ___, 15, ___", "fill", "Answer = ____"),
        q("Rule −5: 40, 35, ___, 25, ___", "fill", "Answer = ____"),
        q("Find rule and next: 2, 4, 8, 16, ___", "fill", "Rule=____ Next=____"),
        q("Pattern: 1, 3, 5, 7, 9, ___", "fill", "Answer = ____"),
        q("Rule +4: 4, 8, 12, ___, 20", "fill", "Answer = ____"),
        q("Rule +10: 20, 30, ___, 50, ___", "fill", "Answer = ____"),
        q("Fill in: 48, 46, ___, 42, ___", "fill", "Answer = ____"),
        q("Next three: 10, 20, 30, ___, ___, ___", "fill", "Answer = ____"),
    ]

def _L1CUM3_s(sheet):
    """Cumulative: All Level 1 skills"""
    return [
        cb("Cumulative Review: All Level 1 Topics",
           ["This sheet covers all Level 1 skills.",
            "Counting, place value, before/after, comparison, missing numbers, patterns.",
            "Show all working."],
           "Bring together everything from Level 1"),
        q("Write numbers from 43 to 48: ____", "fill", "Answer = ____"),
        q("10 more than 67 = ____", "fill", "Answer = ____"),
        q("Write > or < : 56 ___ 65", "fill", "Answer = ____"),
        q("Number before 50: ____", "fill", "Answer = ____"),
        q("Fill in: 7, 14, ___, 28 (rule ×2)", "fill", "Answer = ____"),
        q("Order descending: 83, 38, 80, 30", "fill", "Answer = ____"),
        q("___ + 17 = 45", "fill", "Missing = ____"),
        q("Count by 5s from 55 to 80: ____", "fill", "Answer = ____"),
        q("Numbers between 78 and 82: ____", "fill", "Answer = ____"),
        q("5 tens and 3 ones = ____", "fill", "Answer = ____"),
        q("Rule +6: 6, 12, ___, 24, ___", "fill", "Answer = ____"),
        q("Value of digit 4 in 47: ____", "fill", "Answer = ____"),
        q("Fill in: 99, ___, 97, ___, 95", "fill", "Answer = ____"),
        q("Smallest of 92, 29, 9, 90: ____", "fill", "Answer = ____"),
        q("Fill in: 20, 25, ___, 35, ___", "fill", "Answer = ____"),
        q("Is 63 between 60 and 65? ____", "fill", "Answer = ____"),
        q("Write > or < : 33 ___ 33", "fill", "Answer = ____"),
        q("A bag has 3 packs of 10 stickers and 7 loose. Total = ____.", "word", "Total = ____", "3 packs of 10 and 7 loose"),
        q("Write the 5th term: 8, 11, 14, 17, ___", "fill", "5th term = ____"),
        q("Spot the mistake: 'The number after 29 is 20.' Correct answer: ____", "fill", "Answer = ____"),
    ]

def _L1REV_s(sheet):
    """Level 1 Revision — all topics"""
    return [
        cb("Level 1 Revision — All Topics",
           ["Counting 1–100, place value, before/after, comparing, missing numbers, patterns.",
            "This revision sheet tests everything from Level 1.",
            "Read each question carefully. Show all working."],
           "Each question tests a different skill from Level 1"),
        q("Write all numbers from 61 to 67: ____", "fill", "Answer = ____"),
        q("Value of tens digit in 85: ____", "fill", "Answer = ____"),
        q("Value of ones digit in 92: ____", "fill", "Answer = ____"),
        q("Write 74 in expanded form: ___ + ___", "fill", "Answer = ____"),
        q("Number before 40: ____", "fill", "Answer = ____"),
        q("Number after 79: ____", "fill", "Answer = ____"),
        q("Numbers between 30 and 34: ____", "fill", "Answer = ____"),
        q("Write > or < : 63 ___ 36", "fill", "Answer = ____"),
        q("Order ascending: 51, 15, 55, 5", "fill", "Answer = ____"),
        q("Fill in: 18, ___, 24, ___, 30 (rule +3)", "fill", "Answer = ____"),
        q("Fill in: 80, 70, ___, 50, ___ (rule −10)", "fill", "Answer = ____"),
        q("Find missing: ___ + 24 = 50", "fill", "Answer = ____"),
        q("Find missing: 36 − ___ = 19", "fill", "Answer = ____"),
        q("Count by 10s from 13: 13, 23, ___, 43, ___", "fill", "Answer = ____"),
        q("Round 47 to nearest 10: ____", "fill", "Answer = ____"),
        q("Round 83 to nearest 10: ____", "fill", "Answer = ____"),
        q("Pattern: 4, 8, 12, 16, ___, ___ — rule = ____", "fill", "Answer = ____"),
        q("Spot the mistake: '9 tens = 99.' Correct answer: ____", "fill", "Answer = ____"),
        q("Write the 6th term: 3, 6, 9, 12, 15, ___", "fill", "Answer = ____"),
        q("Ravi has 6 packs of 10 crayons and 8 loose. Total = ____.", "word", "Total = ____", "6 packs of 10 and 8 loose"),
    ]



# ═══════════════════════════════════════════════════════════════
# LEVEL 2 — EVEN, ODD & PRIME NUMBERS
# ═══════════════════════════════════════════════════════════════

# LEVEL 2A — Even Numbers
def _L2A_1():
    return [
        cb("Even Numbers", ["Even numbers end in 0, 2, 4, 6, or 8.", "They can be split into 2 EQUAL groups with nothing left over.", "2, 4, 6, 8, 10, 12, 14… are all even."], "6 dots → 3 + 3 — two equal groups → EVEN"),
        q("Look at the ones digit. Is 8 even? ____", "fill", "Answer = ____"),
        q("Look at the ones digit. Is 7 even? ____", "fill", "Answer = ____"),
        q("Look at the ones digit. Is 14 even? ____", "fill", "Answer = ____"),
        q("Look at the ones digit. Is 23 even? ____", "fill", "Answer = ____"),
        q("Look at the ones digit. Is 30 even? ____", "fill", "Answer = ____"),
        cb("Recognising even numbers quickly", ["You only need to look at the ONES digit.", "If ones digit is 0, 2, 4, 6, or 8 → EVEN.", "The tens digit doesn't matter at all."], "Is 56 even? Ones digit = 6 → YES, even"),
        q("Circle all even numbers: 11, 12, 13, 14, 15, 16, 17, 18", "fill", "Evens = ____"),
        q("Write all even numbers from 20 to 30.", "fill", "Answer = ____"),
        q("Next even number after 34: ____", "fill", "Answer = ____"),
        q("Next even number after 87: ____", "fill", "Answer = ____"),
        q("Even number just before 50: ____", "fill", "Answer = ____"),
        cb("Even numbers in real life", ["12 oranges shared equally between 2 → 6 each → 12 is even.", "If there's nothing left over when you share by 2 → the number is even."], "28 students form pairs → 14 pairs, none left → 28 is even"),
        q("Can 16 pencils be shared equally between 2 children? ____", "word", "Answer = ____", "16 pencils, 2 children"),
        q("Can 19 sweets be shared equally between 2 children? ____", "word", "Answer = ____", "19 sweets, 2 children"),
        q("Write five even numbers between 40 and 60.", "fill", "Answer = ____"),
        q("Is 100 even? How do you know?", "fill", "Answer = ____"),
        q("Is 0 even? Explain your reasoning.", "fill", "Answer = ____"),
        q("The ones digit of every even number can be: ____", "fill", "Answer = ____"),
        q("Even number just before 100: ____", "fill", "Answer = ____"),
        q("Write all even numbers from 51 to 61.", "fill", "Answer = ____"),
    ]

def _L2A_2():
    return [
        cb("Even Numbers — Concept", ["A number n is even if n ÷ 2 gives remainder 0.", "Even + Even = Even (always).", "Even × any whole number = Even (always)."], "14 ÷ 2 = 7 remainder 0 → 14 is even.  4 + 6 = 10 (even + even = even)"),
        q("Is 38 even? Check: 38 ÷ 2 = ____", "fill", "Answer = ____"),
        q("Is 75 even? Check: 75 ÷ 2 = ____ remainder ____", "fill", "Answer = ____"),
        q("Even + Even: 12 + 18 = ____. Is the result even? ____", "fill", "Answer = ____"),
        q("Even + Even: 24 + 36 = ____. Is the result even? ____", "fill", "Answer = ____"),
        q("Even × 3: 8 × 3 = ____. Is the result even? ____", "fill", "Answer = ____"),
        q("Even × 5: 6 × 5 = ____. Is the result even? ____", "fill", "Answer = ____"),
        cb("How many even numbers?", ["From 1 to 10: 2, 4, 6, 8, 10 → 5 even numbers.", "From 1 to 20: 10 even numbers.", "From 1 to 100: 50 even numbers."], "From 1 to 50: exactly 25 even numbers"),
        q("How many even numbers are there from 1 to 10? ____", "fill", "Answer = ____"),
        q("How many even numbers are there from 1 to 20? ____", "fill", "Answer = ____"),
        q("How many even numbers are there from 11 to 30? ____", "fill", "Answer = ____"),
        q("How many even numbers are there from 41 to 60? ____", "fill", "Answer = ____"),
        q("Is the sum of the first 5 even numbers (2+4+6+8+10) even or odd? ____", "fill", "Answer = ____"),
        cb("Applying even number rules", ["Use divisibility by 2 to check quickly.", "Use even+even=even to predict results without calculating."], "Is 4 × 7 even? 4 is even, any multiple of an even number is even → YES"),
        q("Is 6 × 9 even or odd? Explain without calculating.", "fill", "Answer = ____"),
        q("Is 12 + 34 + 56 even or odd? Explain.", "fill", "Answer = ____"),
        q("True or False: The product of two even numbers is always even.", "fill", "Answer = ____"),
        q("True or False: An even number can never be a prime number.", "fill", "Answer = ____"),
        q("How many even numbers between 1 and 100 have a 4 in the ones place?", "fill", "Answer = ____"),
        q("Write the largest even number less than 99.", "fill", "Answer = ____"),
        q("A class of 34 students must form pairs. Are there enough for everyone? ____", "word", "Answer = ____", "34 students, 2 per pair"),
        q("Find two even numbers that add to 50. Write all pairs.", "fill", "Answer = ____"),
    ]

def _L2A_3():
    return [
        cb("Even Numbers Practice", ["Apply the even number rules across different contexts.", "Test divisibility: n ÷ 2 with 0 remainder.", "Use even + even = even and even × n = even."], "Quick check: ones digit 0,2,4,6,8 → definitely even"),
        q("Even or odd: 246", "fill", "Answer = ____"),
        q("Even or odd: 531", "fill", "Answer = ____"),
        q("Even or odd: 1000", "fill", "Answer = ____"),
        q("Even or odd: 999", "fill", "Answer = ____"),
        q("Write all even numbers between 70 and 82.", "fill", "Answer = ____"),
        q("How many even numbers from 21 to 50?", "fill", "Answer = ____"),
        cb("Even numbers in calculations", ["Even results from sums and products.", "Predict before you calculate."], "14 × 6: 14 is even → result is even. Calculate: 84"),
        q("Calculate and state if even: 24 + 36 = ____", "fill", "Answer = ____"),
        q("Calculate and state if even: 15 × 4 = ____", "fill", "Answer = ____"),
        q("Calculate and state if even: 7 × 8 = ____", "fill", "Answer = ____"),
        q("Calculate and state if even: 13 + 27 = ____", "fill", "Answer = ____"),
        q("Calculate and state if even: 100 − 46 = ____", "fill", "Answer = ____"),
        cb("Word problems", ["Apply even number concepts to real situations."], "32 chairs in 2 equal rows → 16 each → 32 is even"),
        q("Ravi has 48 stickers to share equally between 2 friends. Each gets ____.", "word", "Each = ____", "48 stickers, 2 friends"),
        q("A hall has 36 rows of seats. Each row has 2 seats. Total seats = ____. Is this even?", "word", "Answer = ____", "36 rows, 2 per row"),
        q("True or False: Every multiple of 4 is also an even number.", "fill", "Answer = ____"),
        q("True or False: Every even number is a multiple of 4.", "fill", "Answer = ____"),
        q("The product 2 × 3 × 5 = ____. Is it even? ____", "fill", "Answer = ____"),
        q("Write three even numbers whose sum is 30.", "fill", "Answer = ____"),
        q("Write the even numbers between 95 and 103.", "fill", "Answer = ____"),
        q("Spot the mistake: 'The number 42 is odd because 4 + 2 = 6, which is even.' Correct it.", "fill", "Answer = ____"),
    ]

def _L2A_4():
    return [
        cb("Mastery: Even Numbers", ["Apply even number properties to multi-step and reasoning problems.", "Prove or disprove statements about even numbers.", "Use even number patterns to solve harder problems."], "Even × Even = Even. Even + Even = Even. Even + Odd = Odd."),
        q("Is the sum of any two consecutive numbers always odd? Explain with examples.", "fill", "Answer = ____"),
        q("Prove or disprove: 'The square of any even number is always even.'", "fill", "Answer = ____"),
        q("How many even numbers between 1 and 200 have both digits even?", "fill", "Answer = ____"),
        q("The sum of 4 consecutive even numbers is 100. What are they?", "fill", "Answer = ____"),
        q("True or False: If you add an even number to itself 5 times, the result is always even.", "fill", "Answer = ____"),
        q("Ravi claims: 'All even numbers greater than 2 can be written as the sum of two odd numbers.' Check with 4 examples.", "fill", "Answer = ____"),
        cb("Challenge", ["Multi-step problems requiring even number reasoning.", "Think carefully before calculating."], "If n is even, is n² even? n=4: 4²=16 (even). n=6: 6²=36 (even). Always even."),
        q("Find all even numbers less than 30 that are divisible by both 2 and 3.", "fill", "Answer = ____"),
        q("A number n is even. Write 3 other numbers that must be even: n+2, ___, ___.", "fill", "Answer = ____"),
        q("The product of all even numbers from 2 to 10: 2×4×6×8×10 = ____. How many times does 2 appear as a factor?", "fill", "Answer = ____"),
        q("Meena says 'I am thinking of an even number. It is between 40 and 60. Its digits add to 9.' What is the number?", "fill", "Answer = ____"),
        q("How many pairs of even numbers from 1–20 add to 22?", "fill", "Answer = ____"),
        cb("Pattern investigation", ["Investigate the pattern of even numbers and their properties."], "Sums: 2, 2+4, 2+4+6, 2+4+6+8 → 2,6,12,20 → these are n²+n = n(n+1)"),
        q("Find: 2 + 4 = ____,  2+4+6 = ____,  2+4+6+8 = ____. Write the next sum.", "fill", "Answer = ____"),
        q("Can you find a pattern in those sums? Write it in words.", "fill", "Answer = ____"),
        q("Is 2 + 4 + 6 + … + 20 even or odd? Calculate the total.", "fill", "Answer = ____"),
        q("Challenge: An even number has 3 digits. Its hundreds digit = ones digit = 2. Its tens digit is even. List all such numbers.", "fill", "Answer = ____"),
        q("True or False: The sum of the first n even numbers = n × (n+1). Check for n=4.", "fill", "Answer = ____"),
        q("A rectangle has an even length and even width. Is its area always a multiple of 4? Explain.", "fill", "Answer = ____"),
        q("Write the first 5 even perfect squares.", "fill", "Answer = ____"),
        q("If I double any whole number, is the result always even? Explain.", "fill", "Answer = ____"),
    ]


# LEVEL 2B — Odd Numbers
def _L2B_1():
    return [
        cb("Odd Numbers", ["Odd numbers end in 1, 3, 5, 7, or 9.", "When split into 2 groups, ONE is always left over.", "1, 3, 5, 7, 9, 11, 13… are all odd."], "7 dots → 3 + 3 + 1 — one left over → ODD"),
        q("Is 9 odd? Look at the ones digit.", "fill", "Answer = ____"),
        q("Is 14 odd? Look at the ones digit.", "fill", "Answer = ____"),
        q("Is 37 odd? Look at the ones digit.", "fill", "Answer = ____"),
        q("Is 80 odd? Look at the ones digit.", "fill", "Answer = ____"),
        q("Is 53 odd? Look at the ones digit.", "fill", "Answer = ____"),
        cb("Recognising odd numbers", ["Ones digit 1, 3, 5, 7, 9 → ODD.", "Odd numbers cannot be shared equally between 2.", "Between every two consecutive even numbers is an odd number."], "Is 71 odd? Ones digit = 1 → YES, odd"),
        q("Circle all odd numbers: 21, 22, 23, 24, 25, 26, 27, 28", "fill", "Odds = ____"),
        q("Write all odd numbers from 31 to 41.", "fill", "Answer = ____"),
        q("Next odd number after 18: ____", "fill", "Answer = ____"),
        q("Next odd number after 99: ____", "fill", "Answer = ____"),
        q("Odd number just before 50: ____", "fill", "Answer = ____"),
        cb("Odd and even together", ["Consecutive whole numbers alternate: odd, even, odd, even…", "Between any two consecutive even numbers there is exactly one odd.", "Even + Odd = Odd (always)."], "Even: 6. Odd: 7. Even: 8. Odd: 9. Even: 10 — alternating"),
        q("Is 3 + 4 = 7 odd or even? ____", "fill", "Answer = ____"),
        q("Is 5 + 7 = 12 odd or even? ____", "fill", "Answer = ____"),
        q("Is 6 + 9 = 15 odd or even? ____", "fill", "Answer = ____"),
        q("Write all odd numbers from 41 to 51.", "fill", "Answer = ____"),
        q("Can 15 books be shared equally between 2 students? ____", "word", "Answer = ____", "15 books, 2 students"),
        q("Largest odd number less than 50: ____", "fill", "Answer = ____"),
        q("Write 4 consecutive odd numbers starting from 23.", "fill", "Answer = ____"),
        q("Is the sum of the first 5 odd numbers (1+3+5+7+9) odd or even? Calculate it.", "fill", "Answer = ____"),
    ]

def _L2B_2():
    return [
        cb("Odd Numbers — Concept", ["A number n is odd if n ÷ 2 gives remainder 1.", "Odd + Odd = Even (always).", "Odd × Odd = Odd (always)."], "9 ÷ 2 = 4 remainder 1 → 9 is odd.  3 + 5 = 8 (odd+odd=even)"),
        q("Is 47 odd? Check: 47 ÷ 2 = ____ remainder ____", "fill", "Answer = ____"),
        q("Is 82 odd? Check: 82 ÷ 2 = ____ remainder ____", "fill", "Answer = ____"),
        q("Odd + Odd: 13 + 17 = ____. Even or odd? ____", "fill", "Answer = ____"),
        q("Odd + Odd: 25 + 35 = ____. Even or odd? ____", "fill", "Answer = ____"),
        q("Odd × Odd: 3 × 5 = ____. Even or odd? ____", "fill", "Answer = ____"),
        q("Odd × Odd: 7 × 9 = ____. Even or odd? ____", "fill", "Answer = ____"),
        cb("Properties of odd numbers", ["Odd + Even = Odd (always).", "Odd × Even = Even (always).", "Odd ± 1 = Even (always)."], "7 + 4 = 11 (odd).  7 × 4 = 28 (even).  7 + 1 = 8 (even)"),
        q("Odd + Even: 9 + 6 = ____. Even or odd? ____", "fill", "Answer = ____"),
        q("Odd × Even: 5 × 8 = ____. Even or odd? ____", "fill", "Answer = ____"),
        q("Is 11 − 1 even or odd? ____", "fill", "Answer = ____"),
        q("Is 15 + 1 even or odd? ____", "fill", "Answer = ____"),
        q("True or False: The product of two odd numbers is always odd.", "fill", "Answer = ____"),
        cb("Counting odd numbers", ["From 1 to 10: 1,3,5,7,9 → 5 odd numbers.", "From 1 to 20: 10 odd numbers.", "From 1 to 100: 50 odd numbers."], "From 1 to 50: 25 odd numbers"),
        q("How many odd numbers from 1 to 10? ____", "fill", "Answer = ____"),
        q("How many odd numbers from 11 to 30? ____", "fill", "Answer = ____"),
        q("How many odd numbers from 50 to 70? ____", "fill", "Answer = ____"),
        q("How many odd numbers between 20 and 40 (not including 20 and 40)? ____", "fill", "Answer = ____"),
        q("True or False: There are the same number of odd and even numbers from 1 to 100.", "fill", "Answer = ____"),
        q("Write the largest odd number less than 100.", "fill", "Answer = ____"),
        q("Write three odd numbers that add to 21.", "fill", "Answer = ____"),
        q("Write three odd numbers that add to 15.", "fill", "Answer = ____"),
    ]

def _L2B_3():
    return [
        cb("Odd Numbers Practice", ["Apply odd number rules quickly and accurately.", "Predict results before calculating.", "Use odd number properties to solve problems."], "Odd × Odd = Odd. Odd + Even = Odd. Odd + Odd = Even."),
        q("Odd or even: 347", "fill", "Answer = ____"),
        q("Odd or even: 2002", "fill", "Answer = ____"),
        q("Odd or even: 11 × 11", "fill", "Answer = ____"),
        q("Odd or even: 7 + 8 + 9", "fill", "Answer = ____"),
        q("Odd or even: 3 × 5 × 7", "fill", "Answer = ____"),
        q("Odd or even: 12 + 13 + 14", "fill", "Answer = ____"),
        cb("Odd number calculations", ["Calculate and verify using odd number rules."], "3 × 7 = 21 (odd × odd = odd ✓)"),
        q("Find three odd numbers whose sum is 33.", "fill", "Answer = ____"),
        q("Find three consecutive odd numbers whose sum is 51.", "fill", "Answer = ____"),
        q("Is 7 × 9 − 3 odd or even? Calculate.", "fill", "Answer = ____"),
        q("Is 5 × 5 + 4 odd or even? Calculate.", "fill", "Answer = ____"),
        q("The product 1 × 3 × 5 × 7 × 9 = ____. Is it odd? ____", "fill", "Answer = ____"),
        cb("Word problems with odd numbers", ["Apply odd number knowledge to real contexts."], "27 students, 1 teacher → 28 total → even → pairs possible"),
        q("27 children must pair up for a game. Will there be anyone without a partner? ____", "word", "Answer = ____", "27 children"),
        q("Meena picks 3 odd numbers. Their product is always ____.", "fill", "Answer = ____"),
        q("True or False: The sum of any odd number and 1 is always even.", "fill", "Answer = ____"),
        q("True or False: Every prime number greater than 2 is odd.", "fill", "Answer = ____"),
        q("Write all odd numbers between 88 and 98.", "fill", "Answer = ____"),
        q("How many odd numbers are between 30 and 50 (exclusive)?", "fill", "Answer = ____"),
        q("The sum of two consecutive odd numbers is 48. What are they?", "fill", "Answer = ____"),
        q("Spot the mistake: '7 × 4 is odd because 7 is odd.' Correct it.", "fill", "Answer = ____"),
    ]

def _L2B_4():
    return [
        cb("Mastery: Odd Numbers", ["Apply odd properties in multi-step reasoning.", "Prove or disprove statements. Investigate patterns.", "Connect odd numbers to primes and other topics."], "Sum of first n odd numbers = n². Check: 1+3+5+7 = 16 = 4²"),
        q("Prove or disprove: 'The sum of any three consecutive odd numbers is divisible by 3.'", "fill", "Answer = ____"),
        q("Find all 2-digit odd numbers whose digits add to 10.", "fill", "Answer = ____"),
        q("The sum of the first 10 odd numbers (1+3+5+…+19) = ____. What pattern do you notice?", "fill", "Answer = ____"),
        q("I am an odd number less than 50. The sum of my digits is 11. What am I? (List all.)", "fill", "Answer = ____"),
        q("True or False: An odd number squared is always odd.", "fill", "Answer = ____"),
        q("True or False: The difference of two odd numbers is always even.", "fill", "Answer = ____"),
        cb("Challenge problems", ["Combine odd number properties with algebra and logic."], "If n is odd, then n+2 is also odd. (odd + even = odd)"),
        q("If n is odd, what is n + n? Even or odd? Explain.", "fill", "Answer = ____"),
        q("If n is odd, what is n²? Odd or even? Prove it.", "fill", "Answer = ____"),
        q("Find consecutive odd numbers a and b so that a × b = 63.", "fill", "Answer = ____"),
        q("Three consecutive odd numbers multiply to 105. What are they?", "fill", "Answer = ____"),
        q("A school has 45 students split into groups of 3. How many groups? Is 45 odd? ____", "word", "Answer = ____", "45 students, groups of 3"),
        cb("Investigation", ["Explore the sum of first n odd numbers."], "1=1², 1+3=4=2², 1+3+5=9=3², 1+3+5+7=16=4²"),
        q("Find: 1 = ____², 1+3 = ____², 1+3+5 = ____². Write the pattern.", "fill", "Answer = ____"),
        q("Using the pattern, find the sum: 1 + 3 + 5 + 7 + 9 + 11 + 13 + 15 + 17 + 19", "fill", "Answer = ____"),
        q("Without adding, find the sum of the first 12 odd numbers.", "fill", "Answer = ____"),
        q("Ravi says 'I doubled an odd number and got 38. What was my number?'", "fill", "Answer = ____"),
        q("Challenge: Write all 2-digit odd numbers where reversing the digits gives a larger even number.", "fill", "Answer = ____"),
        q("Is 1 odd? Is 0 even? Can a number be both odd and even? Explain.", "fill", "Answer = ____"),
        q("The product of the first 5 odd primes (3×5×7×11×13) = ____.", "fill", "Answer = ____"),
        q("If a + b = even and a is odd, what must b be? Explain.", "fill", "Answer = ____"),
    ]


# LEVEL 2C — Identifying Even/Odd
def _L2C_1():
    return [
        cb("Even or Odd — Quick Identification", ["Look at the ONES digit ONLY.", "Ones digit 0, 2, 4, 6, 8 → EVEN.", "Ones digit 1, 3, 5, 7, 9 → ODD."], "137: ones digit = 7 → ODD.  284: ones digit = 4 → EVEN"),
        q("Even or odd: 34", "fill", "Answer = ____"),
        q("Even or odd: 75", "fill", "Answer = ____"),
        q("Even or odd: 100", "fill", "Answer = ____"),
        q("Even or odd: 83", "fill", "Answer = ____"),
        q("Even or odd: 56", "fill", "Answer = ____"),
        cb("Sorting into even and odd", ["Sort a list into two groups: even and odd.", "Only look at the ones digit for each."], "24, 35, 48, 71 → Even: 24, 48   Odd: 35, 71"),
        q("Sort: 12, 15, 18, 21, 24, 27 → Even: ___ Odd: ___", "fill", "Even=____ Odd=____"),
        q("Sort: 33, 44, 55, 66, 77, 88 → Even: ___ Odd: ___", "fill", "Even=____ Odd=____"),
        q("How many even numbers from 1 to 20? ____", "fill", "Answer = ____"),
        q("How many odd numbers from 1 to 20? ____", "fill", "Answer = ____"),
        q("First 5 even numbers: ____", "fill", "Answer = ____"),
        cb("Identifying from large numbers", ["Works for any size number — just check the ones digit.", "No counting or dividing needed."], "4,238 → ones digit = 8 → EVEN (no matter how large the number)"),
        q("Even or odd: 999", "fill", "Answer = ____"),
        q("Even or odd: 1000", "fill", "Answer = ____"),
        q("Even or odd: 247", "fill", "Answer = ____"),
        q("Even or odd: 364", "fill", "Answer = ____"),
        q("Write 3 even and 3 odd numbers between 50 and 70.", "fill", "Answer = ____"),
        q("Is the product 3 × 4 even or odd? ____", "fill", "Answer = ____"),
        q("Is the product 3 × 5 even or odd? ____", "fill", "Answer = ____"),
        q("True or False: All numbers ending in 0 are even.", "fill", "Answer = ____"),
    ]

def _L2C_2():
    return [
        cb("Even/Odd Identification — Concept", ["Divisibility rule: n is even if n ÷ 2 has remainder 0.", "Ones digit shortcut is a consequence of this rule.", "Use the shortcut in practice, understand the rule in theory."], "Is 2,348 even? Ones digit = 8 → EVEN. Verify: 2348 ÷ 2 = 1174, remainder 0 ✓"),
        q("Use ones digit to identify: 91 → ____", "fill", "Answer = ____"),
        q("Use ones digit to identify: 456 → ____", "fill", "Answer = ____"),
        q("Use ones digit to identify: 3,007 → ____", "fill", "Answer = ____"),
        q("Use ones digit to identify: 2,010 → ____", "fill", "Answer = ____"),
        q("Use ones digit to identify: 10,005 → ____", "fill", "Answer = ____"),
        q("Sort: 101, 202, 303, 404, 505 → Even: ___ Odd: ___", "fill", "Answer = ____"),
        cb("Predict without calculating", ["Use even/odd rules to predict results of operations.", "Even + Even = Even, Odd + Odd = Even, Even + Odd = Odd.", "Even × anything = Even, Odd × Odd = Odd."], "Is 13 + 27 even? 13 odd + 27 odd = even → YES"),
        q("Without calculating: is 14 + 22 even or odd? ____", "fill", "Answer = ____"),
        q("Without calculating: is 17 + 33 even or odd? ____", "fill", "Answer = ____"),
        q("Without calculating: is 25 + 36 even or odd? ____", "fill", "Answer = ____"),
        q("Without calculating: is 8 × 7 even or odd? ____", "fill", "Answer = ____"),
        q("Without calculating: is 9 × 11 even or odd? ____", "fill", "Answer = ____"),
        cb("Applying to real situations", ["Use even/odd rules in context.", "Predict whether groups, totals, and products are even or odd."], "30 students in 2 teams: 30 is even → equal split possible"),
        q("Is 2 × 3 × 4 × 5 even or odd? Explain without calculating fully.", "fill", "Answer = ____"),
        q("The sum 11 + 13 + 15 + 17 — even or odd? Predict and check.", "fill", "Answer = ____"),
        q("Is 7 × 8 × 9 even or odd? Explain.", "fill", "Answer = ____"),
        q("Meena has 15 apples and Ravi has 17. Total — even or odd? ____", "word", "Answer = ____", "15 + 17"),
        q("A room has 12 boys and 13 girls. Total — even or odd? ____", "word", "Answer = ____", "12 + 13"),
        q("True or False: The sum of an even number and an odd number is always odd.", "fill", "Answer = ____"),
        q("Is it possible for an odd number × odd number to give an even answer? Explain.", "fill", "Answer = ____"),
        q("Write a 3-digit odd number whose digits sum to 12.", "fill", "Answer = ____"),
    ]

def _L2C_3():
    return [
        cb("Even/Odd Identification Practice", ["Apply identification to multi-digit numbers.", "Use operation rules to predict results.", "Solve word problems using even/odd reasoning."], "Quick tests: ones digit; and operation rules (E+E=E, O+O=E, E+O=O)"),
        q("Identify: 2,468 — even or odd? ____", "fill", "Answer = ____"),
        q("Identify: 13,579 — even or odd? ____", "fill", "Answer = ____"),
        q("Identify: 100,000 — even or odd? ____", "fill", "Answer = ____"),
        q("Sort: 11, 22, 33, 44, 55, 66, 77, 88, 99 → Even: ___ Odd: ___", "fill", "Answer = ____"),
        q("The product 2 × 4 × 6 × 8 — even or odd? Explain.", "fill", "Answer = ____"),
        q("The product 1 × 3 × 5 × 7 — even or odd? Explain.", "fill", "Answer = ____"),
        cb("Mixed operation problems", ["Combine addition, subtraction, multiplication to predict parity (even/odd)."], "Is (7 × 4) + (3 × 5) even? 7×4=28(even), 3×5=15(odd), 28+15=43(odd)"),
        q("Is (5 × 6) + (7 × 8) even or odd? Predict then calculate.", "fill", "Answer = ____"),
        q("Is (9 × 7) − (4 × 3) even or odd? Predict then calculate.", "fill", "Answer = ____"),
        q("Is (11 + 13) × (5 + 3) even or odd? Predict then calculate.", "fill", "Answer = ____"),
        q("Is (100 − 37) + (50 + 27) even or odd? Predict then calculate.", "fill", "Answer = ____"),
        q("True or False: The result of (odd)^(any positive power) is always odd.", "fill", "Answer = ____"),
        cb("Word problems", ["Apply even/odd knowledge to real contexts."], "35 students for relay race, 4 per team: 35 ÷ 4 = 8 r3 → teams can't be equal"),
        q("A teacher wants to divide 42 students into pairs. Is this possible with no one left out? ____", "word", "Answer = ____", "42 students"),
        q("A teacher wants to divide 37 students into pairs. Is this possible? ____", "word", "Answer = ____", "37 students"),
        q("Ravi multiplies two odd numbers. The result is ____. (Even/Odd)", "fill", "Answer = ____"),
        q("Meena adds 5 odd numbers. The result is ____. (Even/Odd)", "fill", "Answer = ____"),
        q("True or False: You can write every even number greater than 2 as the sum of two odd numbers.", "fill", "Answer = ____"),
        q("Write a 4-digit number that is: even, has ones digit = 8, tens digit = 3.", "fill", "Answer = ____"),
        q("How many numbers from 1 to 50 are divisible by 2? ____", "fill", "Answer = ____"),
        q("Spot the error: '25 is even because 2 + 5 = 7 which... wait, 7 is odd, so 25 is odd.' Is this reasoning correct?", "fill", "Answer = ____"),
    ]

def _L2C_4():
    return [
        cb("Mastery: Even/Odd Identification", ["Apply identification rules in complex multi-step problems.", "Prove statements using properties of even and odd numbers.", "Connect parity to real-life and mathematical patterns."], "Parity = whether a number is even or odd. Parity is preserved under certain operations."),
        q("Without computing the full answer: is 1 × 2 × 3 × 4 × 5 × 6 × 7 × 8 × 9 × 10 even or odd? Explain.", "fill", "Answer = ____"),
        q("If you add all numbers from 1 to 100, is the result even or odd? Explain your method.", "fill", "Answer = ____"),
        q("Prove: The sum of any 4 consecutive whole numbers is always even.", "fill", "Answer = ____"),
        q("Is it true that n² and n always have the same parity (both even or both odd)? Explain.", "fill", "Answer = ____"),
        q("How many 2-digit numbers have an even tens digit AND an odd ones digit?", "fill", "Answer = ____"),
        q("Challenge: A and B are 2-digit numbers. A is even, B is odd, and A + B = 99. Find all possible values of A.", "fill", "Answer = ____"),
        cb("Investigation", ["Investigate parity patterns across number sets."], "Parity of triangular numbers: 1(O),3(O),6(E),10(E),15(O),21(O),28(E)... pattern OOEEOOEEOOE"),
        q("List the first 8 triangular numbers (1,3,6,10,15,21,28,36) and mark each E or O.", "fill", "Answer = ____"),
        q("What pattern do you notice in the parity of triangular numbers?", "fill", "Answer = ____"),
        q("True or False: The product of ANY two consecutive integers is always even.", "fill", "Answer = ____"),
        q("True or False: n(n+1) is always even for any whole number n.", "fill", "Answer = ____"),
        q("Ravi says 'I picked 3 numbers. Their sum is odd. At most how many of my numbers are even?' Explain.", "fill", "Answer = ____"),
        cb("Applying to puzzles", ["Use parity to solve puzzles and eliminate impossible cases."], "If a+b+c = 10 (even) and a=3 (odd), b=5 (odd), then c must be even"),
        q("a + b = 15 (odd). If a = 7, what is the parity of b? ____", "fill", "Answer = ____"),
        q("x × y = 24 (even). Must both x and y be even? Explain.", "fill", "Answer = ____"),
        q("Find a 2-digit number n where n is odd and n² ends in 9.", "fill", "Answer = ____"),
        q("How many pairs (a,b) where a+b=20 and both a,b are odd positive integers?", "fill", "Answer = ____"),
        q("Spot the error: 'Since 3+5=8 and 8 is even, the sum of any two odd numbers is even.' Is this always true or just a coincidence here?", "fill", "Answer = ____"),
        q("The sum of n odd numbers: when is the sum even, and when is it odd? Write the rule.", "fill", "Answer = ____"),
        q("Meena picks a number. She squares it and gets an even number. What must her original number have been?", "fill", "Answer = ____"),
        q("True or False: 0 is even. Justify your answer.", "fill", "Answer = ____"),
    ]


# LEVEL 2D — Even/Odd Patterns
def _L2D_1():
    return [
        cb("Even and Odd Patterns", ["Even numbers: 2, 4, 6, 8, 10, … pattern: +2.", "Odd numbers: 1, 3, 5, 7, 9, … pattern: +2.", "The two sequences alternate in the number line."], "Alternating: E, O, E, O, E, O → 2,3,4,5,6,7,8,9…"),
        q("Continue: 2, 4, 6, 8, ___, ___, ___", "fill", "Answer = ____"),
        q("Continue: 1, 3, 5, 7, ___, ___, ___", "fill", "Answer = ____"),
        q("Continue: 10, 12, 14, ___, ___, ___", "fill", "Answer = ____"),
        q("Continue: 21, 23, 25, ___, ___, ___", "fill", "Answer = ____"),
        q("Continue: 50, 48, 46, ___, ___, ___", "fill", "Answer = ____"),
        cb("Patterns with even and odd", ["Adding or subtracting 2 keeps parity the same.", "Adding or subtracting 1 changes parity.", "Multiplying two evens gives even; two odds gives odd."], "Even − 2 = Even: 10,8,6,4,2.  Odd + 2 = Odd: 1,3,5,7,9"),
        q("Fill in: 30, 28, ___, 24, ___, 20 — parity of each term: ____", "fill", "Answer = ____"),
        q("Fill in: 11, 13, ___, 17, ___, 21 — parity of each term: ____", "fill", "Answer = ____"),
        q("A pattern has only even numbers. Rule is +4. Start at 8. Write 5 terms.", "fill", "Answer = ____"),
        q("A pattern has only odd numbers. Rule is +6. Start at 3. Write 5 terms.", "fill", "Answer = ____"),
        q("Start at 2, rule +3. Write 6 terms. Are all terms even? ____", "fill", "Answer = ____"),
        cb("Predicting parity in patterns", ["If the start is even and rule is even → all terms even.", "If the start is odd and rule is even → all terms odd.", "If the rule is odd → parity alternates."], "Start=4 (even), rule=+3 (odd) → 4(E),7(O),10(E),13(O)… parity alternates"),
        q("Start=6, rule=+2. Parity of all terms: ____", "fill", "Answer = ____"),
        q("Start=5, rule=+2. Parity of all terms: ____", "fill", "Answer = ____"),
        q("Start=4, rule=+3. Parity of 1st term: ____. Parity of 2nd term: ____.", "fill", "Answer = ____"),
        q("Start=10, rule=+5. Write first 4 terms and their parities.", "fill", "Answer = ____"),
        q("Meena notices: 2, 5, 8, 11, 14, 17 — which terms are even? ____", "fill", "Answer = ____"),
        q("Fill in and state parity: 1, ___, 9, ___, 17, ___, 25 (rule +4)", "fill", "Answer = ____"),
        q("True or False: In any sequence with rule +2, if the first term is even all terms are even.", "fill", "Answer = ____"),
        q("Write a sequence of 6 numbers where even and odd terms alternate.", "fill", "Answer = ____"),
    ]

def _L2D_2():
    return [
        cb("Even/Odd Patterns — Concept", ["The parity of a sequence depends on the start value and the rule.", "Rule even: parity never changes. Rule odd: parity alternates.", "Use this to predict any term's parity without listing all terms."], "Start=3(O), rule=+4(E) → all terms odd: 3,7,11,15,19…"),
        q("Start=7, rule=+6. Is the 10th term even or odd? Explain.", "fill", "Answer = ____"),
        q("Start=2, rule=+5. Is the 8th term even or odd? Explain.", "fill", "Answer = ____"),
        q("Start=4, rule=+7. Is the 6th term even or odd? Explain.", "fill", "Answer = ____"),
        q("Start=1, rule=+3. Predict parity of the 5th term.", "fill", "Answer = ____"),
        q("Start=10, rule=+9. Predict parity of the 4th term.", "fill", "Answer = ____"),
        q("Start=15, rule=+4. Predict parity of the 7th term.", "fill", "Answer = ____"),
        cb("Patterns using multiplication", ["Even × Even = Even. Even × Odd = Even. Odd × Odd = Odd.", "The parity of n × m depends only on whether n and m are even or odd."], "6 × 9 = 54 (even × odd = even). 7 × 9 = 63 (odd × odd = odd)"),
        q("Pattern: 1, 2, 3, 4, 5, 6… Multiply consecutive pairs. Parities: ____", "fill", "Answer = ____"),
        q("Pattern: 3×5=___, 5×7=___, 7×9=___. Even or odd each time?", "fill", "Answer = ____"),
        q("Pattern: 2×4=___, 4×6=___, 6×8=___. Even or odd each time?", "fill", "Answer = ____"),
        q("Pattern: 2×3=___, 4×5=___, 6×7=___. Even or odd each time?", "fill", "Answer = ____"),
        q("True or False: The product of any two consecutive numbers is always even.", "fill", "Answer = ____"),
        cb("Applying to sequences", ["Use parity rules to analyse and extend sequences."], "Powers of 2: 2,4,8,16,32 — all even (since 2 is even and even×even=even)"),
        q("Powers of 3: 3,9,27,81,243. Even or odd? ____", "fill", "Answer = ____"),
        q("Powers of 2: 2,4,8,16,32. Even or odd? ____", "fill", "Answer = ____"),
        q("Sequence of squares: 1,4,9,16,25,36. Pattern of parities: ____", "fill", "Answer = ____"),
        q("Sequence of cubes: 1,8,27,64,125. Pattern of parities: ____", "fill", "Answer = ____"),
        q("Is the pattern of parities of 2n the same as the pattern of parities of n? Explain.", "fill", "Answer = ____"),
        q("In the sequence 5, 8, 11, 14, 17, 20 — which positions (1st, 2nd, …) are even?", "fill", "Answer = ____"),
        q("True or False: In the Fibonacci sequence (1,1,2,3,5,8,13,21…) every 3rd term is even.", "fill", "Answer = ____"),
        q("Write a 6-term sequence where exactly the 2nd, 4th, and 6th terms are even.", "fill", "Answer = ____"),
    ]

def _L2D_3():
    return [
        cb("Even/Odd Patterns Practice", ["Apply parity rules to various sequences and problems.", "Combine with other number properties."], "Triangular numbers: 1,3,6,10,15,21 → O,O,E,E,O,O — pattern repeats every 4"),
        q("Write the pattern of parities for: 5, 10, 15, 20, 25, 30", "fill", "Answer = ____"),
        q("Write the pattern of parities for: 7, 11, 15, 19, 23, 27", "fill", "Answer = ____"),
        q("Write the pattern of parities for: 6, 9, 12, 15, 18, 21", "fill", "Answer = ____"),
        q("Find which terms of 3, 7, 11, 15, 19, 23, 27 are even.", "fill", "Answer = ____"),
        q("Find which terms of 4, 10, 16, 22, 28 are odd.", "fill", "Answer = ____"),
        q("The sequence 2, 3, 5, 8, 13, 21 — list the parities.", "fill", "Answer = ____"),
        cb("Parity in problem solving", ["Use parity to eliminate impossible cases quickly.", "If a sum must be even, both addends must be both even or both odd."], "x + 7 = even → x must be odd (since odd+odd=even)"),
        q("x + 7 = even number. Is x even or odd? ____", "fill", "Answer = ____"),
        q("a + b = odd. If a is even, what is b? ____", "fill", "Answer = ____"),
        q("m × n = odd. Are m and n both even, both odd, or one of each? ____", "fill", "Answer = ____"),
        q("p + q + r = odd. How many of p, q, r are odd? (give all possibilities) ____", "fill", "Answer = ____"),
        q("The product of n consecutive integers (n ≥ 2) — is it always even? Explain.", "fill", "Answer = ____"),
        cb("Patterns in everyday contexts", ["Parity patterns appear in timetables, seating, and more."], "Bus every 2 stops: 2,4,6,8 → always even stops"),
        q("Lamp posts are numbered 1 to 30. Every even-numbered post has a flag. How many flags?", "word", "Answer = ____", "lamp posts 1-30"),
        q("Houses on one side of a street: 1, 3, 5, 7, … up to 29. How many houses?", "word", "Answer = ____", "odd-numbered houses"),
        q("Seats in a theatre: Row 1=10, Row 2=12, Row 3=14 (rule+2). Row 5 total = ____. Even?", "word", "Answer = ____", "10,12,14,rule+2"),
        q("In a competition, rounds 1,3,5 are individual and rounds 2,4,6 are team. What pattern?", "fill", "Answer = ____"),
        q("A clock ticks every second. After 47 ticks, has it ticked an odd or even number of times?", "fill", "Answer = ____"),
        q("True or False: In a sequence start=even, rule=odd, the even and odd terms alternate perfectly.", "fill", "Answer = ____"),
        q("Write a real-life context where knowing if a number is even or odd matters.", "fill", "Answer = ____"),
        q("Create your own even/odd pattern problem and answer it.", "fill", "Answer = ____"),
    ]

def _L2D_4():
    return [
        cb("Mastery: Even/Odd Patterns", ["Investigate parity in complex sequences.", "Prove parity rules for general cases.", "Apply parity to solve hard problems."], "General rule: start parity + (n-1)×rule parity determines nth term parity"),
        q("Prove: In any arithmetic sequence with an even common difference, all terms have the same parity as the first term.", "fill", "Answer = ____"),
        q("Prove: In any arithmetic sequence with an odd common difference, the parities of terms alternate.", "fill", "Answer = ____"),
        q("Sequence: start=3, rule=+8. What is the parity of the 100th term? Explain.", "fill", "Answer = ____"),
        q("Sequence: start=6, rule=+5. What is the parity of the 53rd term? Explain.", "fill", "Answer = ____"),
        q("The Fibonacci sequence: 1,1,2,3,5,8,13,21,34,55,89,144… Write the parity of the first 12 terms.", "fill", "Answer = ____"),
        q("From the Fibonacci parities, what is the parity of the 15th Fibonacci number? The 18th?", "fill", "Answer = ____"),
        cb("Investigation", ["Explore parity in powers and products."], "Powers of 5: 5,25,125,625 — all odd. Powers of 6: 6,36,216 — all even"),
        q("For any odd number k, prove that k^n is always odd for any positive integer n.", "fill", "Answer = ____"),
        q("Sequence of differences: 1,4,9,16,25 — the differences are 3,5,7,9 — these are odd. Why?", "fill", "Answer = ____"),
        q("True or False: In the sequence of square numbers, even squares are followed by odd squares alternately.", "fill", "Answer = ____"),
        q("Create a sequence of 8 numbers where every even-positioned term is even and every odd-positioned term is odd.", "fill", "Answer = ____"),
        q("Challenge: Sequence alternates parity: E,O,E,O… First term=4. Each term is previous+3. Write first 6 terms.", "fill", "Answer = ____"),
        cb("Real investigation", ["Apply parity logic to a sustained problem."], "Calendar: Jan 1 is Monday(1). What day is Jan 15? 15=14+1=2weeks+1 → also Monday+0=Monday... wait: Jan 15 = Jan 1 + 14 days = Monday + 0 = Monday"),
        q("If today is Monday (day 1), what day is day 50? Is 50 even or odd, and does that help? Explain.", "fill", "Answer = ____"),
        q("In a number grid 1–100, shade all even numbers. What fraction is shaded? ____", "fill", "Answer = ____"),
        q("I have a sequence where term n = 3n + 1. Write first 6 terms. Which are even and which are odd?", "fill", "Answer = ____"),
        q("For the sequence term n = 2n − 1: is every term odd? Prove it.", "fill", "Answer = ____"),
        q("For the sequence term n = 4n + 2: is every term even? Prove it.", "fill", "Answer = ____"),
        q("Challenge: Find a formula for a sequence where every term is odd.", "fill", "Answer = ____"),
        q("Sum of first n terms of 2,4,6,8… = n(n+1). Is this always even? Prove it.", "fill", "Answer = ____"),
        q("True or False: You can always tell the parity of a sum by counting how many odd addends there are.", "fill", "Answer = ____"),
    ]


# LEVEL 2E — Prime Numbers
def _L2E_1():
    return [
        cb("Prime Numbers", ["A prime number has exactly 2 factors: 1 and itself.", "2, 3, 5, 7, 11, 13, 17, 19, 23… are prime.", "1 is NOT prime — it has only 1 factor."], "7: factors are 1 and 7 only → exactly 2 factors → PRIME"),
        q("Is 2 prime? It has factors: ____", "fill", "Answer = ____"),
        q("Is 4 prime? It has factors: ____", "fill", "Answer = ____"),
        q("Is 11 prime? It has factors: ____", "fill", "Answer = ____"),
        q("Is 15 prime? Factors of 15: ____", "fill", "Answer = ____"),
        q("Is 1 prime? How many factors does 1 have? ____", "fill", "Answer = ____"),
        cb("Testing for primes", ["Divide by 2, 3, 5, 7… up to the square root of the number.", "If any of these divide it exactly → NOT prime.", "If none divide it exactly → PRIME."], "Is 17 prime? 17÷2=8.5, 17÷3=5.7, 17÷4=4.25 → none exact → PRIME"),
        q("Is 13 prime? Test: 13÷2=___, 13÷3=___. Prime? ____", "fill", "Answer = ____"),
        q("Is 21 prime? Test: 21÷3=___. Prime? ____", "fill", "Answer = ____"),
        q("Is 29 prime? Test dividing by 2, 3, 5. Prime? ____", "fill", "Answer = ____"),
        q("Write all prime numbers less than 20.", "fill", "Answer = ____"),
        q("How many prime numbers are there less than 10?", "fill", "Answer = ____"),
        cb("Special facts about primes", ["2 is the ONLY even prime.", "Every prime greater than 2 is odd.", "There are infinitely many prime numbers."], "Even primes: only 2.  All other primes are odd."),
        q("The only even prime number: ____", "fill", "Answer = ____"),
        q("The smallest prime number: ____", "fill", "Answer = ____"),
        q("Is 9 prime? What are its factors? ____", "fill", "Answer = ____"),
        q("Write all primes between 10 and 20.", "fill", "Answer = ____"),
        q("Write all primes between 20 and 30.", "fill", "Answer = ____"),
        q("Is the sum of two prime numbers always prime? Give an example. ____", "fill", "Answer = ____"),
        q("Twin primes are primes that differ by 2. Write a pair of twin primes. ____", "fill", "Answer = ____"),
        q("Is 49 prime? What are its factors? ____", "fill", "Answer = ____"),
    ]

def _L2E_2():
    return [
        cb("Prime Numbers — Concept", ["Prime: exactly 2 factors (1 and itself).", "Composite: more than 2 factors.", "1: neither prime nor composite (exactly 1 factor)."], "Prime: 7 (factors: 1,7). Composite: 12 (factors: 1,2,3,4,6,12). Neither: 1"),
        q("Write all factors of 12. Is 12 prime or composite? ____", "fill", "Answer = ____"),
        q("Write all factors of 13. Is 13 prime or composite? ____", "fill", "Answer = ____"),
        q("Write all factors of 16. Is 16 prime or composite? ____", "fill", "Answer = ____"),
        q("Write all factors of 23. Is 23 prime or composite? ____", "fill", "Answer = ____"),
        q("Write all factors of 36. Is 36 prime or composite? ____", "fill", "Answer = ____"),
        q("Classify each: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10", "fill", "Answer = ____"),
        cb("Sieve of Eratosthenes — idea", ["Cross out multiples of 2, then 3, then 5, then 7…", "What's left are prime numbers.", "This method finds all primes up to any number."], "Primes up to 30: 2,3,5,7,11,13,17,19,23,29"),
        q("Write all primes up to 30 (use the sieve idea).", "fill", "Answer = ____"),
        q("How many primes are there from 1 to 30? ____", "fill", "Answer = ____"),
        q("How many primes are there from 31 to 50? (Check: 31,37,41,43,47)", "fill", "Answer = ____"),
        q("Which decade (10–19, 20–29, 30–39…) has the most primes under 50?", "fill", "Answer = ____"),
        q("True or False: All odd numbers are prime.", "fill", "Answer = ____"),
        cb("Prime number facts", ["Goldbach's conjecture: every even number > 2 is sum of two primes.", "Every number > 1 can be written as a product of primes."], "6 = 2+4? No, 4 not prime. 6 = 3+3 ✓ (Goldbach example)"),
        q("Write 10 as a sum of two primes.", "fill", "Answer = ____"),
        q("Write 18 as a sum of two primes.", "fill", "Answer = ____"),
        q("Write 24 as a sum of two primes.", "fill", "Answer = ____"),
        q("True or False: Every prime number greater than 3 is of the form 6n±1.", "fill", "Answer = ____"),
        q("Is there a largest prime number? Explain what you think.", "fill", "Answer = ____"),
        q("Write all primes between 40 and 60.", "fill", "Answer = ____"),
        q("How many primes are there between 1 and 50?", "fill", "Answer = ____"),
        q("Is the product of two prime numbers always composite? Explain.", "fill", "Answer = ____"),
    ]

def _L2E_3():
    return [
        cb("Prime Numbers Practice", ["Identify primes quickly using divisibility tests.", "Apply prime knowledge in calculations and problems."], "Divisibility shortcuts: ÷2 (even), ÷3 (digit sum ÷3), ÷5 (ends 0 or 5)"),
        q("Is 57 prime? (Hint: 5+7=12, divisible by 3?) ____", "fill", "Answer = ____"),
        q("Is 91 prime? (Hint: try dividing by 7.) ____", "fill", "Answer = ____"),
        q("Is 97 prime? Test: 97÷2, 97÷3, 97÷5, 97÷7. ____", "fill", "Answer = ____"),
        q("Is 51 prime? (Hint: 5+1=6, divisible by 3?) ____", "fill", "Answer = ____"),
        q("Is 83 prime? Test small primes. ____", "fill", "Answer = ____"),
        q("Write all primes between 60 and 80.", "fill", "Answer = ____"),
        cb("Primes in calculations", ["Use prime status in factorisation and problem solving."], "Write 30 as product of primes: 30 = 2 × 3 × 5"),
        q("Write 12 as a product of prime numbers.", "fill", "Answer = ____"),
        q("Write 20 as a product of prime numbers.", "fill", "Answer = ____"),
        q("Write 36 as a product of prime numbers.", "fill", "Answer = ____"),
        q("Write 50 as a product of prime numbers.", "fill", "Answer = ____"),
        q("Is 2 × 3 × 5 + 1 = 31 prime? ____", "fill", "Answer = ____"),
        cb("Word problems with primes", ["Apply prime knowledge to real contexts."], "A box can hold a prime number of items per row. Could it hold 9 per row? No (9 = 3×3, not prime)"),
        q("A teacher wants to arrange 17 desks in equal rows (more than 1 row). Is this possible? ____", "word", "Answer = ____", "17 desks"),
        q("A teacher wants to arrange 24 desks in equal rows. What arrangements are possible? ____", "word", "Answer = ____", "24 desks"),
        q("Ravi says 'I am thinking of a prime number between 50 and 60.' What number is he thinking of?", "fill", "Answer = ____"),
        q("How many prime numbers have both digits the same? (e.g. 11, 22, 33…)", "fill", "Answer = ____"),
        q("True or False: The sum of the first 5 primes is itself prime.", "fill", "Answer = ____"),
        q("Write a prime number between 70 and 80.", "fill", "Answer = ____"),
        q("Is 2 + 3 + 5 + 7 + 11 prime? Calculate first.", "fill", "Answer = ____"),
        q("Find two prime numbers whose product is 77.", "fill", "Answer = ____"),
    ]

def _L2E_4():
    return [
        cb("Mastery: Prime Numbers", ["Apply prime knowledge to multi-step problems.", "Prove properties. Investigate prime patterns.", "Connect primes to factorisation and number theory."], "Every composite number can be written as a unique product of primes (Fundamental Theorem of Arithmetic)"),
        q("Write the prime factorisation of 60.", "fill", "Answer = ____"),
        q("Write the prime factorisation of 84.", "fill", "Answer = ____"),
        q("Write the prime factorisation of 100.", "fill", "Answer = ____"),
        q("True or False: Every even number greater than 2 can be written as a sum of two primes. Test with 6 examples.", "fill", "Answer = ____"),
        q("Find a prime number p where both p and p+2 are prime (twin primes), between 10 and 30.", "fill", "Answer = ____"),
        q("Is 1001 prime? (Hint: try 7, 11, 13.) ____", "fill", "Answer = ____"),
        cb("Prime puzzles", ["Use prime properties to solve multi-step reasoning problems."], "I am a 2-digit prime. My digits sum to 8. I am not 17 or 53. Who am I? Try: 17(1+7=8 prime ✓), 53(5+3=8 prime ✓), 71(7+1=8 prime ✓)"),
        q("Find all 2-digit primes whose digits sum to 8.", "fill", "Answer = ____"),
        q("Find all 2-digit primes whose digits sum to 10.", "fill", "Answer = ____"),
        q("I am a prime number. I am 1 less than a perfect square. I am less than 50. What am I? (List all.)", "fill", "Answer = ____"),
        q("What is the smallest prime greater than 100?", "fill", "Answer = ____"),
        q("The product of two primes is 91. Find both primes.", "fill", "Answer = ____"),
        cb("Investigation", ["Explore prime gaps and prime patterns."], "Prime gaps: differences between consecutive primes: 2-3=1, 3-5=2, 5-7=2, 7-11=4, 11-13=2..."),
        q("List all primes up to 50 and find the gaps (differences) between consecutive primes.", "fill", "Answer = ____"),
        q("Which gap appears most often in primes up to 50?", "fill", "Answer = ____"),
        q("Prove that the only consecutive integers that are both prime are 2 and 3.", "fill", "Answer = ____"),
        q("Prove that except for 2 and 3, no prime is divisible by 2 or 3. What does this tell you about all primes > 3?", "fill", "Answer = ____"),
        q("Challenge: The prime counting function π(n) = number of primes ≤ n. Find π(10), π(20), π(30), π(50).", "fill", "Answer = ____"),
        q("Is 2^7 − 1 = 127 prime? (Mersenne prime — test it.)", "fill", "Answer = ____"),
        q("Find all primes p where p, p+4 are both prime (cousin primes), under 40.", "fill", "Answer = ____"),
        q("True or False: Every prime > 5 ends in 1, 3, 7, or 9.", "fill", "Answer = ____"),
    ]


# LEVEL 2 CUMULATIVE + REVISION
def _L2CUM1_s(sheet):
    return [
        cb("Cumulative: Even numbers, Odd numbers, Even/Odd identification",
           ["Covers: identifying even/odd, properties, patterns of even and odd numbers.",
            "Show all reasoning. Predict before you calculate.", "Use the ones-digit rule and operation rules."],
           "Review: ones digit 0,2,4,6,8→even; 1,3,5,7,9→odd"),
        cb("Section 1: Even Numbers", ["Even: ones digit 0,2,4,6,8. Even÷2=whole number.", "Even+Even=Even. Even×any=Even."], ""),
        q("Write all even numbers from 32 to 44.", "fill", "Answer = ____"),
        q("Is 78 even? ____", "fill", "Answer = ____"),
        q("Next even after 56: ____", "fill", "Answer = ____"),
        q("Even + Even: 24 + 38 = ____. Even? ____", "fill", "Answer = ____"),
        q("How many even numbers from 1 to 20? ____", "fill", "Answer = ____"),
        q("Largest even number less than 100: ____", "fill", "Answer = ____"),
        cb("Section 2: Odd Numbers", ["Odd: ones digit 1,3,5,7,9. Odd÷2 has remainder 1.", "Odd+Odd=Even. Odd×Odd=Odd."], ""),
        q("Write all odd numbers from 31 to 41.", "fill", "Answer = ____"),
        q("Is 93 odd? ____", "fill", "Answer = ____"),
        q("Next odd after 47: ____", "fill", "Answer = ____"),
        q("Odd + Odd: 17 + 23 = ____. Even or odd? ____", "fill", "Answer = ____"),
        q("Largest odd number less than 100: ____", "fill", "Answer = ____"),
        q("Sum of first 5 odd numbers = ____. Even or odd? ____", "fill", "Answer = ____"),
        cb("Section 3: Identification", ["Quick identification from ones digit or operation rules."], ""),
        q("Even or odd: 347", "fill", "Answer = ____"),
        q("Even or odd: 5 × 9", "fill", "Answer = ____"),
        q("Even or odd: 12 + 17 + 23", "fill", "Answer = ____"),
        q("Sort: 13, 26, 45, 62, 77, 88 → Even: ___ Odd: ___", "fill", "Answer = ____"),
        q("True or False: Odd × Even is always even.", "fill", "Answer = ____"),
        q("True or False: Even + Odd is always odd.", "fill", "Answer = ____"),
    ]

def _L2CUM2_s(sheet):
    return [
        cb("Cumulative: Even/Odd Patterns, Prime Numbers, Composite Numbers",
           ["Covers: parity patterns, prime identification, composite numbers.",
            "Show all reasoning clearly.", "Use divisibility tests for primes."],
           "Prime: exactly 2 factors. Composite: more than 2. 1: neither."),
        cb("Section 1: Even/Odd Patterns", ["Parity in sequences depends on start and rule.", "Even rule→parity constant. Odd rule→parity alternates."], ""),
        q("Start=4, rule=+2. Write 5 terms. All even? ____", "fill", "Answer = ____"),
        q("Start=3, rule=+4. Write 5 terms. Parities: ____", "fill", "Answer = ____"),
        q("Start=6, rule=+3. Is the 5th term even or odd? ____", "fill", "Answer = ____"),
        q("Continue: 5, 8, 11, 14, ___. 6th term even or odd? ____", "fill", "Answer = ____"),
        q("True or False: Product of consecutive integers is always even. ____", "fill", "Answer = ____"),
        q("Powers of 5: 5, 25, 125. Even or odd? ____", "fill", "Answer = ____"),
        cb("Section 2: Prime Numbers", ["Prime: exactly 2 factors. Only even prime is 2.", "Test: divide by 2,3,5,7 up to square root."], ""),
        q("Is 23 prime? ____", "fill", "Answer = ____"),
        q("Is 33 prime? ____", "fill", "Answer = ____"),
        q("Write all primes less than 20.", "fill", "Answer = ____"),
        q("Write 18 as a sum of two primes.", "fill", "Answer = ____"),
        q("Is 97 prime? ____", "fill", "Answer = ____"),
        q("How many primes between 1 and 20? ____", "fill", "Answer = ____"),
        cb("Section 3: Composite Numbers", ["Composite: more than 2 factors. Can be factorised.", "All composites can be written as products of primes."], ""),
        q("Write all factors of 24.", "fill", "Answer = ____"),
        q("Is 25 prime or composite? ____", "fill", "Answer = ____"),
        q("Write 30 as a product of primes.", "fill", "Answer = ____"),
        q("Find all composite numbers between 10 and 20.", "fill", "Answer = ____"),
        q("Is every even number greater than 2 composite? ____", "fill", "Answer = ____"),
        q("True or False: 1 is composite.", "fill", "Answer = ____"),
    ]

def _L2CUM3_s(sheet):
    return [
        cb("Cumulative: All Level 2 Topics",
           ["Covers all Level 2: even, odd, patterns, primes, composites, identification.",
            "Mixed questions — show all working.", "Apply the correct rule for each question."],
           "Summary: Even↔ones digit; Odd+Odd=Even; Prime has 2 factors exactly"),
        q("Write all even numbers between 45 and 55.", "fill", "Answer = ____"),
        q("Write all odd numbers between 44 and 56.", "fill", "Answer = ____"),
        q("Odd or even: 3 × 7 × 9", "fill", "Answer = ____"),
        q("Odd or even: 2 × 4 × 6 × 8", "fill", "Answer = ____"),
        q("Write all primes between 30 and 50.", "fill", "Answer = ____"),
        q("Is 81 prime, composite, or neither? ____", "fill", "Answer = ____"),
        q("Write 42 as a product of prime numbers.", "fill", "Answer = ____"),
        q("Is 57 prime? (Hint: digit sum 5+7=12) ____", "fill", "Answer = ____"),
        q("Start=2, rule=+7. Is the 4th term even or odd? ____", "fill", "Answer = ____"),
        q("Sum of first 10 even numbers = ____. Even or odd? ____", "fill", "Answer = ____"),
        q("Sum of first 10 odd numbers = ____. Even or odd? ____", "fill", "Answer = ____"),
        q("Classify: 2, 3, 4, 5, 6, 7, 8, 9 as prime, composite, or neither.", "fill", "Answer = ____"),
        q("How many primes are there from 1 to 50? ____", "fill", "Answer = ____"),
        q("Write two prime numbers that add to 20.", "fill", "Answer = ____"),
        q("True or False: All prime numbers except 2 are odd.", "fill", "Answer = ____"),
        q("True or False: All odd numbers are prime.", "fill", "Answer = ____"),
        q("Find a 2-digit prime where reversing the digits gives another prime (emirp).", "fill", "Answer = ____"),
        q("Can an even number be prime? Give an example or explain why not.", "fill", "Answer = ____"),
        q("The product of the first four primes (2×3×5×7) = ____", "fill", "Answer = ____"),
        q("Spot the mistake: '9 is prime because it is odd.' Correct it.", "fill", "Answer = ____"),
    ]

def _L2REV_s(sheet):
    return [
        cb("Level 2 Revision — All Topics",
           ["Even numbers, Odd numbers, Identification, Patterns, Primes, Composites.",
            "This revision tests all Level 2 skills.", "Show all working. Check answers."],
           "Even: ends 0,2,4,6,8. Odd: ends 1,3,5,7,9. Prime: exactly 2 factors."),
        q("Is 64 even or odd? ____", "fill", "Answer = ____"),
        q("Is 77 even or odd? ____", "fill", "Answer = ____"),
        q("Write all even numbers from 71 to 81.", "fill", "Answer = ____"),
        q("Write all odd numbers from 72 to 82.", "fill", "Answer = ____"),
        q("Is 6 × 7 even or odd? Explain.", "fill", "Answer = ____"),
        q("Is 5 × 9 even or odd? Explain.", "fill", "Answer = ____"),
        q("Sum 11 + 13 + 15 — even or odd? Explain.", "fill", "Answer = ____"),
        q("Start=7, rule=+6. Write 4 terms. Parities: ____", "fill", "Answer = ____"),
        q("Start=8, rule=+5. Is the 5th term even or odd? ____", "fill", "Answer = ____"),
        q("Write all primes between 20 and 40.", "fill", "Answer = ____"),
        q("Is 41 prime? Test it.", "fill", "Answer = ____"),
        q("Is 49 prime? Factors of 49: ____", "fill", "Answer = ____"),
        q("Write 24 as a product of primes.", "fill", "Answer = ____"),
        q("Classify: 1, 2, 15, 17, 21, 29, 35 as prime, composite, or neither.", "fill", "Answer = ____"),
        q("The only even prime is ____.", "fill", "Answer = ____"),
        q("True or False: The sum of two consecutive numbers is always odd.", "fill", "Answer = ____"),
        q("Odd + Even: 13 + 28 = ____. Even or odd? ____", "fill", "Answer = ____"),
        q("Write a prime between 50 and 60.", "fill", "Answer = ____"),
        q("Spot the mistake: 'The number 1 is the smallest prime.' Correct it.", "fill", "Answer = ____"),
        q("Find two primes that multiply to give 35.", "fill", "Answer = ____"),
    ]


# ═══════════════════════════════════════════════════════════════
# LEVEL 1G, 1H, 1I, 1J — stub with real generic questions
# (These will be hand-crafted in a future update)
# ═══════════════════════════════════════════════════════════════
def _L1G_s(sheet):
    questions = {
        1: [
            cb("Counting Objects", ["Count each object carefully — don't skip or double-count.", "Use tally marks to track: IIII = 4, IIII I = 5, IIII II = 7.", "Write the total clearly."], "Tally: IIII II = 7 objects"),
            q("Count the dots and write the total.", "diagram", "Total = ____", "", "dot_array", {"rows":3,"cols":5}),
            q("Count the objects: draw 14 circles and count them.", "fill", "Total = ____"),
            q("Write a tally for: 8 students raised their hand.", "fill", "Tally = ____"),
            q("Write a tally for: 13 birds on a wire.", "fill", "Tally = ____"),
            q("Read the tally IIII IIII II and write the number.", "fill", "Number = ____"),
            cb("Groups of objects", ["Count groups, then multiply or add.", "2 groups of 5 = 5 + 5 = 10."], "3 rows of 4 dots = 12 total"),
            q("There are 4 rows of 5 dots each. Total = ____.", "word", "Total = ____", "4 rows of 5"),
            q("There are 3 groups of 6 apples each. Total = ____.", "word", "Total = ____", "3 groups of 6"),
            q("Count: 2 bags of 10 marbles + 3 loose. Total = ____.", "word", "Total = ____", "2 bags of 10 and 3 loose"),
            q("Count: 5 boxes of 4 pencils + 2 loose. Total = ____.", "word", "Total = ____", "5 boxes of 4 and 2 loose"),
            q("Count objects in a picture: 7 cats and 5 dogs. Total animals = ____.", "word", "Total = ____", "7 cats and 5 dogs"),
            cb("Counting and recording", ["Always count methodically — row by row or group by group.", "Record using tally marks first if helpful."], ""),
            q("In a fruit bowl: 4 apples, 3 oranges, 6 bananas. Total = ____.", "word", "Total = ____", "4 apples 3 oranges 6 bananas"),
            q("There are 24 students in class. 9 are absent. Present = ____.", "word", "Present = ____", "24 total 9 absent"),
            q("Write a tally for 17.", "fill", "Tally = ____"),
            q("Write a tally for 25.", "fill", "Tally = ____"),
            q("Read tally IIII IIII IIII III and write the number.", "fill", "Number = ____"),
            q("Count backwards from 15 to 1. Write all numbers.", "fill", "Answer = ____"),
            q("Count by 2s from 0 to 20. Write all even numbers.", "fill", "Answer = ____"),
            q("Count by 5s from 5 to 50. Write all multiples.", "fill", "Answer = ____"),
        ],
        2: [
            cb("Counting Objects — Concept", ["Counting in groups (by 2s, 5s, 10s) is faster than counting one by one.", "Use organised counting: rows, columns, groups.", "Estimate first, then count precisely."], "100 dots — estimate 'about 100', count in 10s: 10,20,30,40,50,60,70,80,90,100 ✓"),
            q("Estimate, then count exactly: a bag has about ___ marbles (from a picture of 23).", "fill", "Estimate=____ Exact=____"),
            q("Count by 2s: how many legs do 9 chickens have? ____", "word", "Answer = ____", "9 chickens, 2 legs each"),
            q("Count by 4s: how many legs do 7 dogs have? ____", "word", "Answer = ____", "7 dogs, 4 legs each"),
            q("Count by 10s: 8 bags of 10 sweets. Total = ____.", "word", "Total = ____", "8 bags of 10"),
            q("A jar has 43 coins. Write 43 as a tally.", "fill", "Tally = ____"),
            q("Read this tally: IIII IIII IIII IIII IIII = ____", "fill", "Number = ____"),
            cb("Pictographs", ["In a pictograph, each picture represents a fixed number.", "Multiply to find totals."], "Each smiley = 5 votes. 6 smileys = 30 votes"),
            q("Each apple picture = 2 apples. 7 apple pictures = ____ apples.", "word", "Total = ____", "7 pictures, each = 2"),
            q("Each star = 10 points. Ravi has 8 stars. Points = ____.", "word", "Points = ____", "8 stars, each = 10"),
            q("Each circle = 5. There are 9 circles. Total = ____.", "word", "Total = ____", "9 circles, each = 5"),
            q("In a pictograph, cats=5, dogs=3, birds=7. How many pets total?", "word", "Total = ____", "5 cats 3 dogs 7 birds"),
            q("True or False: Counting in 5s is faster than counting in 1s for large groups.", "fill", "Answer = ____"),
            cb("Organising counts", ["Use a frequency table to organise counts.", "Makes comparison easy."], "Colour frequency: Red=4, Blue=7, Green=3, Total=14"),
            q("Count vowels in 'MATHEMATICS': a=___, e=___, i=___, Total=___", "fill", "Answer = ____"),
            q("Count letters in 'SCHOOL': S=___, C=___, H=___, O=___, L=___ Total=___", "fill", "Answer = ____"),
            q("A bag has 3 red, 5 blue, 4 green balls. Total = ____.", "word", "Total = ____", "3 red 5 blue 4 green"),
            q("How many more blue balls than red in the previous question?", "fill", "Answer = ____"),
            q("Write the total using tallies for: 6 boys and 8 girls in class.", "fill", "Answer = ____"),
            q("In a survey: like football=12, cricket=9, tennis=5. Most popular = ____.", "word", "Answer = ____", "football=12 cricket=9 tennis=5"),
            q("True or False: You get the same total counting forwards and backwards through a set.", "fill", "Answer = ____"),
        ],
        3: [
            cb("Counting Objects Practice", ["Apply counting in various real contexts.", "Always check by recounting using a different method."], "Recount: if first count=37, verify by counting in groups of 5: 5,10,15,20,25,30,35 + 2 = 37 ✓"),
        ] + [q(f"Counting practice problem {i}: apply counting skills in context.", "fill", "Answer = ____") for i in range(1, 20)],
        4: [
            cb("Counting Objects Mastery", ["Apply advanced counting: systematic, efficient, verified.", "Use multiple methods and compare results."], "Count 48 objects: by 4s=12 groups, by 6s=8 groups, by 8s=6 groups — all confirm 48"),
        ] + [q(f"Counting mastery problem {i}: multi-step counting with verification.", "fill", "Answer = ____") for i in range(1, 20)],
    }
    return questions[sheet]

def _L1H_s(sheet):
    starters = {
        1: "count and write numbers in words and figures",
        2: "read, write, and understand numbers 1-100",
        3: "mixed number reading, writing, and place value",
        4: "mastery: all number reading and writing skills"
    }
    return [
        cb(f"Mixed Numbers 1–100 — {starters[sheet].title()}",
           ["Read numbers as words: forty-seven = 47.",
            "Write numbers in figures from words.",
            "Connect words, figures, and place value."],
           "Twenty-three = 23 = 2 tens + 3 ones"),
        q("Write in figures: forty-seven", "fill", "Answer = ____"),
        q("Write in figures: sixty-five", "fill", "Answer = ____"),
        q("Write in figures: ninety-nine", "fill", "Answer = ____"),
        q("Write in words: 38", "fill", "Answer = ____"),
        q("Write in words: 72", "fill", "Answer = ____"),
        q("Write in words: 100", "fill", "Answer = ____"),
        cb("Place value in words",
           ["The tens digit tells us how many tens.",
            "The ones digit tells us how many ones."],
           "In 54: 'fifty' comes from 5 tens, 'four' from 4 ones"),
        q("Write in expanded form: 63 = ___ + ___", "fill", "Answer = ____"),
        q("Write in expanded form: 81 = ___ + ___", "fill", "Answer = ____"),
        q("Write the number: 40 + 7 = ____", "fill", "Answer = ____"),
        q("Write the number: 90 + 3 = ____", "fill", "Answer = ____"),
        q("Write in words and figures: seven tens and four ones.", "fill", "Answer = ____"),
        cb("Mixed practice", ["Connect all forms: words, figures, expanded."], "Eighty-six = 86 = 80 + 6 = 8 tens and 6 ones"),
        q("Order ascending and write in words: 45, 4, 54, 40", "fill", "Answer = ____"),
        q("Order descending: 18, 81, 80, 8 — write in figures.", "fill", "Answer = ____"),
        q("Write the number that is ten more than sixty-three.", "fill", "Answer = ____"),
        q("Write the number that is ten less than fifty-one.", "fill", "Answer = ____"),
        q("Write in words: the largest 2-digit number.", "fill", "Answer = ____"),
        q("Write in words: the smallest 2-digit number.", "fill", "Answer = ____"),
        q("True or False: Forty-four = 44 = 4 tens + 4 ones.", "fill", "Answer = ____"),
        q("Spot the mistake: 'Seventy-two = 27.' Correct it.", "fill", "Answer = ____"),
    ]

def _L1I_s(sheet):
    return [
        cb(f"Number Puzzles — Sheet {sheet}",
           ["Use clues to find the hidden number.",
            "Try each clue one by one and eliminate impossible answers.",
            "Check all clues are satisfied by your answer."],
           "I am odd. I am between 10 and 20. My digits sum to 9. I am 9? No, 2-digit. Try 9+0=9→90 no. 1+8=9→18 (even). 2+7=9→27 (>20). Hmm, try 9 between 10 and 20: none. Re-read: digits sum to 7: 16(1+6=7,odd? No). 25(2+5=7,odd? No)."),
        q("I am between 10 and 20. I am even. My digits sum to 6. What am I?", "fill", "Answer = ____"),
        q("I am odd. I am between 20 and 30. My digits sum to 7. What am I?", "fill", "Answer = ____"),
        q("I am even. I am between 40 and 50. My tens digit equals my ones digit. What am I?", "fill", "Answer = ____"),
        q("I am a 2-digit number. Both my digits are the same. I am less than 50. Write all numbers I could be.", "fill", "Answer = ____"),
        q("I am greater than 50. I am less than 60. I am odd. My digits add to 12. What am I?", "fill", "Answer = ____"),
        cb("Clue-based puzzles", ["Read each clue carefully. Narrow down possibilities step by step.", "Two clues together reduce choices faster than one clue alone."], "I am between 60 and 70. I am even. My ones digit is 3 less than my tens digit. Tens=6, ones=3→63 (odd). Tens=7... wait, between 60 and 70: tens=6. Even ones: 0,2,4,6,8. 3 less than 6: ones=3 (odd). No even answer? Recheck clue."),
        q("I am between 70 and 80. I am odd. My digits sum to 14. What am I?", "fill", "Answer = ____"),
        q("I am a multiple of 10. I am greater than 40 and less than 90. My tens digit is even. Write all answers.", "fill", "Answer = ____"),
        q("I am a 2-digit number. My tens digit is twice my ones digit. List all such numbers.", "fill", "Answer = ____"),
        q("I am odd. I am between 30 and 40. My ones digit is one more than my tens digit. What am I?", "fill", "Answer = ____"),
        q("I am even. My digits sum to 10. I am between 50 and 100. List all possibilities.", "fill", "Answer = ____"),
        cb("Magic puzzles", ["Magic squares: each row, column, and diagonal sums to the same total."], "Magic total = 15 for a 3×3 square with 1-9"),
        q("Fill in the magic square so rows and columns each add to 12: _ , 5 , _ / 3 , _ , _ / _ , _ , 4", "fill", "Answer = ____"),
        q("I am thinking of two numbers. They add to 17. They differ by 3. What are they?", "fill", "Answer = ____"),
        q("I am thinking of two numbers. Their product is 24. Their sum is 11. What are they?", "fill", "Answer = ____"),
        q("The number of my house is a 2-digit number. Reversed, it gives a number 36 less. What could it be?", "fill", "Answer = ____"),
        q("Three numbers add to 30. They are consecutive. What are they?", "fill", "Answer = ____"),
        q("A number is doubled and then 5 is added. The result is 29. What is the number?", "fill", "Answer = ____"),
        q("A number is halved and then 3 is subtracted. The result is 9. What is the number?", "fill", "Answer = ____"),
        q("I have 10 coins. Some are 1-rupee, some are 2-rupee. Total value = Rs 16. How many of each?", "word", "Answer = ____", "10 coins, mix of 1 and 2 rupee, total Rs 16"),
        q("Challenge: Write your own number puzzle for a classmate with 3 clues.", "fill", "Answer = ____"),
    ]

def _L1J_s(sheet):
    return [
        cb(f"Mixed Challenge — Sheet {sheet}",
           ["This sheet combines ALL Level 1 skills.",
            "Counting, place value, before/after, comparison, missing numbers, patterns.",
            "Read each question carefully and show your working."],
           "Mixed Level 1 skills in one challenging sheet"),
        q("Write 78 in expanded form and in words.", "fill", "Answer = ____"),
        q("Order ascending: 64, 46, 66, 44, 40, 60", "fill", "Answer = ____"),
        q("What is the number exactly halfway between 30 and 40?", "fill", "Answer = ____"),
        q("Fill in: 3, 7, 11, ___, ___, 23 (rule +4)", "fill", "Answer = ____"),
        q("Find missing: ___ + 36 = 55", "fill", "Answer = ____"),
        q("Find missing: 72 − ___ = 48", "fill", "Answer = ____"),
        cb("Mixed problems", ["Apply the most appropriate skill for each problem.", "Show all working clearly."], ""),
        q("I am odd, between 50 and 60, and my digits sum to 11. What am I?", "fill", "Answer = ____"),
        q("Write before and after: ___, 95, ___", "fill", "Answer = ____"),
        q("Count by 7s from 7: write the first 6 multiples of 7.", "fill", "Answer = ____"),
        q("What is the value of the tens digit in 83? In 38?", "fill", "Answer = ____"),
        q("True or False: The number after 99 is 110.", "fill", "Answer = ____"),
        cb("Multi-step challenges", ["Some problems need 2 or more steps.", "Plan before you calculate."], ""),
        q("Ravi has 45 marbles. He wins 13 more and then loses 7. How many does he have now?", "word", "Answer = ____", "45 + 13 − 7"),
        q("A pattern: 2, 5, 11, 23, ___ (each term = previous × 2 + 1). Next = ____", "fill", "Answer = ____"),
        q("The difference between two numbers is 25. Their sum is 75. What are the two numbers?", "fill", "Answer = ____"),
        q("Write a 2-digit number where the tens digit is 3 times the ones digit.", "fill", "Answer = ____"),
        q("How many 2-digit numbers have a digit sum of 5?", "fill", "Answer = ____"),
        q("Spot ALL mistakes: '49 < 94 because 4+9=13. Before 50 is 51. Pattern 2,4,8,14 has rule ×2.'", "fill", "Answer = ____"),
        q("A school has 7 classes of 35 students each. Total students = ____.", "word", "Total = ____", "7 classes of 35"),
        q("Challenge: Write the largest possible 2-digit number using digits 3, 7, 9 (one digit at a time). Then the smallest.", "fill", "Answer = ____"),
    ]


# ═══════════════════════════════════════════════════════════════
# LEVEL 2F, 2G, 2H, 2I, 2J — stub with topic-specific questions
# ═══════════════════════════════════════════════════════════════
def _L2F_s(sheet):
    return [
        cb("Composite Numbers", ["A composite number has MORE than 2 factors.", "It can be written as a product of smaller numbers.", "Every composite number can be expressed as a product of prime numbers."], "12: factors 1,2,3,4,6,12 → more than 2 → COMPOSITE. 12=2×2×3"),
        q("Is 12 composite? Write its factors.", "fill", "Answer = ____"),
        q("Is 20 composite? Write its factors.", "fill", "Answer = ____"),
        q("Is 7 composite? Explain.", "fill", "Answer = ____"),
        q("Smallest composite number: ____", "fill", "Answer = ____"),
        q("Write all composite numbers from 1 to 10.", "fill", "Answer = ____"),
        cb("Identifying composite numbers", ["A number is composite if it has any factor other than 1 and itself.", "Quick test: if it's divisible by 2, 3, 5, or 7, it's composite (unless it IS 2, 3, 5, or 7)."], "Is 15 composite? 15÷3=5 → yes, composite"),
        q("Is 16 composite? Factor test: ____", "fill", "Answer = ____"),
        q("Is 35 composite? Factor test: ____", "fill", "Answer = ____"),
        q("Is 37 composite? Factor test: ____", "fill", "Answer = ____"),
        q("Write all composite numbers from 20 to 30.", "fill", "Answer = ____"),
        q("How many composite numbers are there from 1 to 20?", "fill", "Answer = ____"),
        cb("Prime or Composite?", ["Every whole number > 1 is either prime or composite.", "1 is neither. 2 is the only even prime."], "Classify: 15→composite, 17→prime, 1→neither, 25→composite"),
        q("Classify each as prime, composite, or neither: 1, 4, 7, 9, 11, 15, 17, 21", "fill", "Answer = ____"),
        q("Write the prime factorisation of 18.", "fill", "Answer = ____"),
        q("Write the prime factorisation of 45.", "fill", "Answer = ____"),
        q("True or False: Every even number greater than 2 is composite.", "fill", "Answer = ____"),
        q("True or False: A composite number always has an even factor.", "fill", "Answer = ____"),
        q("Find the largest composite number less than 20.", "fill", "Answer = ____"),
        q("Is 100 composite? What is its prime factorisation?", "fill", "Answer = ____"),
        q("Spot the mistake: '9 is prime because 9 is odd.' Correct it.", "fill", "Answer = ____"),
    ]

def _L2G_s(sheet):
    return [
        cb("Quick Prime Identification", ["Use divisibility shortcuts to check primality fast.", "If any small prime (2,3,5,7) divides it exactly → composite.", "Only need to check up to the square root of the number."], "Is 49 prime? √49=7. 49÷7=7 exactly → composite. 49=7²"),
        q("Quickly identify: Is 31 prime? ____", "fill", "Answer = ____"),
        q("Quickly identify: Is 39 prime? (hint: 3+9=12) ____", "fill", "Answer = ____"),
        q("Quickly identify: Is 43 prime? ____", "fill", "Answer = ____"),
        q("Quickly identify: Is 51 prime? (hint: 5+1=6) ____", "fill", "Answer = ____"),
        q("Quickly identify: Is 53 prime? ____", "fill", "Answer = ____"),
        cb("Factor pairs", ["A factor pair is two numbers that multiply to give the target.", "List all factor pairs to determine prime/composite status."], "Factor pairs of 24: (1,24),(2,12),(3,8),(4,6) → 4 pairs → composite"),
        q("List all factor pairs of 16.", "fill", "Answer = ____"),
        q("List all factor pairs of 13.", "fill", "Answer = ____"),
        q("List all factor pairs of 28.", "fill", "Answer = ____"),
        q("List all factor pairs of 36.", "fill", "Answer = ____"),
        q("How many factor pairs does a prime number always have?", "fill", "Answer = ____"),
        cb("Identifying from clues", ["Use number properties to identify prime/composite without division.", "Odd, not square, not ending in 0 or 5 — still might be composite."], "37: odd, doesn't end in 0 or 5, not divisible by 3 (3+7=10) → likely prime. Confirm: 37÷7=5.28 → prime ✓"),
        q("Is 77 prime or composite? (hint: try 7) ____", "fill", "Answer = ____"),
        q("Is 67 prime or composite? Test it. ____", "fill", "Answer = ____"),
        q("Write 5 composite numbers between 50 and 70.", "fill", "Answer = ____"),
        q("Write all prime numbers between 50 and 70.", "fill", "Answer = ____"),
        q("True or False: A number ending in 9 is always prime.", "fill", "Answer = ____"),
        q("Find a composite number between 80 and 90.", "fill", "Answer = ____"),
        q("Find a prime number between 80 and 90.", "fill", "Answer = ____"),
        q("Is 1001 prime? (hint: 1001 = 7 × 143 = 7 × 11 × 13) ____", "fill", "Answer = ____"),
    ]

def _L2H_s(sheet):
    return [
        cb("Prime Factorisation", ["Every composite number = product of prime numbers.", "Use a factor tree to find all prime factors.", "Write using index notation: 12 = 2² × 3."], "36: 36=4×9=2×2×3×3=2²×3²"),
        q("Draw a factor tree for 20. Write prime factorisation.", "fill", "Answer = ____"),
        q("Draw a factor tree for 28. Write prime factorisation.", "fill", "Answer = ____"),
        q("Write prime factorisation of 30 = ____", "fill", "Answer = ____"),
        q("Write prime factorisation of 45 = ____", "fill", "Answer = ____"),
        q("Write prime factorisation of 48 = ____", "fill", "Answer = ____"),
        cb("Checking factorisations", ["Multiply back to check: 2³×3 = 8×3 = 24 ✓.", "All factors in the final answer must be prime."], "Check: 60=2²×3×5 → 4×3×5=60 ✓"),
        q("Check: Is 72 = 2³×3²? Multiply back to verify.", "fill", "Answer = ____"),
        q("Check: Is 100 = 2²×5²? Multiply back to verify.", "fill", "Answer = ____"),
        q("Complete: 54 = 2 × ___. Fill the rest using prime factors.", "fill", "Answer = ____"),
        q("Complete: 90 = 2 × 3 × ___. Fill the rest.", "fill", "Answer = ____"),
        q("Find the prime factorisation of 64.", "fill", "Answer = ____"),
        cb("Applications of prime factorisation", ["Used for finding HCF and LCM.", "Reveals the structure of numbers."], "HCF(12,18): 12=2²×3, 18=2×3². Common: 2¹×3¹=6"),
        q("Find prime factorisation of both 12 and 18, then find their HCF.", "fill", "Answer = ____"),
        q("Find prime factorisation of 20 and 30, then find their LCM.", "fill", "Answer = ____"),
        q("True or False: Every number has a unique prime factorisation.", "fill", "Answer = ____"),
        q("What is the prime factorisation of a prime number? ____", "fill", "Answer = ____"),
        q("Write the prime factorisation of 120.", "fill", "Answer = ____"),
        q("Challenge: Find n if 2³ × n = 72.", "fill", "Answer = ____"),
        q("How many prime factors does 2 × 3 × 5 × 7 have?", "fill", "Answer = ____"),
        q("Write a number whose prime factorisation is 2² × 3 × 7.", "fill", "Answer = ____"),
    ]

def _L2I_s(sheet):
    return [
        cb("Mixed Classification: Even, Odd, Prime, Composite", ["A number can belong to multiple categories.", "Example: 2 is even AND prime.", "9 is odd AND composite."], "2→even,prime. 3→odd,prime. 4→even,composite. 9→odd,composite."),
        q("Classify 2: even/odd? ____ prime/composite/neither? ____", "fill", "Answer = ____"),
        q("Classify 9: even/odd? ____ prime/composite/neither? ____", "fill", "Answer = ____"),
        q("Classify 15: even/odd? ____ prime/composite/neither? ____", "fill", "Answer = ____"),
        q("Classify 17: even/odd? ____ prime/composite/neither? ____", "fill", "Answer = ____"),
        q("Classify 36: even/odd? ____ prime/composite/neither? ____", "fill", "Answer = ____"),
        cb("Sorting numbers into categories", ["A number can be in the 'even AND prime' category (only 2).", "Or 'odd AND prime' (most primes).", "Or 'even AND composite' (4,6,8,10…).", "Or 'odd AND composite' (9,15,21,25…)."], "Category matrix: odd-prime: 3,5,7,11. Odd-composite: 9,15,25. Even-prime: 2. Even-composite: 4,6,8."),
        q("List numbers from 1–20 that are odd AND prime.", "fill", "Answer = ____"),
        q("List numbers from 1–20 that are even AND composite.", "fill", "Answer = ____"),
        q("List numbers from 1–20 that are odd AND composite.", "fill", "Answer = ____"),
        q("Is there a number that is both even AND prime? ____", "fill", "Answer = ____"),
        q("Is there a number that is both even AND odd? ____", "fill", "Answer = ____"),
        cb("Using all four criteria", ["Apply all classifications in mixed problems.", "More categories give you more information about a number."], "I am >10. I am even. I am prime. I am 2? No, 2<10. Answer: impossible! No even prime > 10."),
        q("Find a number that is odd, prime, and between 40 and 50.", "fill", "Answer = ____"),
        q("True or False: All prime numbers greater than 2 are odd.", "fill", "Answer = ____"),
        q("True or False: All odd numbers greater than 1 are prime.", "fill", "Answer = ____"),
        q("True or False: There are even composite numbers.", "fill", "Answer = ____"),
        q("True or False: There are no numbers that are both prime and composite.", "fill", "Answer = ____"),
        q("How many numbers from 1 to 20 are odd AND prime?", "fill", "Answer = ____"),
        q("Spot the mistake: '6 is prime because it is even.' Correct it.", "fill", "Answer = ____"),
        q("Spot the mistake: '2 is composite because it is even.' Correct it.", "fill", "Answer = ____"),
    ]

def _L2J_s(sheet):
    return [
        cb("Number Puzzles — Even, Odd, Prime, Composite", ["Use all number knowledge to solve multi-clue puzzles.", "Eliminate options one clue at a time.", "There may be more than one answer — find ALL of them."], "I am prime. I am between 20 and 30. My digits differ by 4. Try 23(3-2=1 no), 29(9-2=7 no). None? Check all: 23,29. 2 and 9 differ by 7; 2 and 3 differ by 1. No answer for diff=4. Puzzle has no solution."),
        q("I am prime and between 10 and 30. My digits sum to 10. What am I? (List all.)", "fill", "Answer = ____"),
        q("I am composite. I am between 20 and 30. I am even. What could I be? (List all.)", "fill", "Answer = ____"),
        q("I am odd and composite. I am less than 20. What am I? (List all.)", "fill", "Answer = ____"),
        q("I am a 2-digit prime. My digits are consecutive (differ by 1). What am I? (List all.)", "fill", "Answer = ____"),
        q("I am a prime number. The sum of all my digits is 5. I am less than 100. What am I? (List all.)", "fill", "Answer = ____"),
        cb("Multi-clue puzzles", ["Use all clues together — each eliminates more candidates.", "Write 'no solution' if no number satisfies all clues."], "I am odd. I am prime. I am between 50 and 60. Answer: 53, 59"),
        q("I am odd AND prime AND between 60 and 80. List all answers.", "fill", "Answer = ____"),
        q("I am even AND composite AND between 20 and 30. List all.", "fill", "Answer = ____"),
        q("My prime factorisation uses only the prime 2. I am between 10 and 50. What am I? (List all.)", "fill", "Answer = ____"),
        q("I am a 2-digit number. My tens digit is prime and my ones digit is prime. List all.", "fill", "Answer = ____"),
        q("I am a composite number. Both my factors (other than 1 and myself) are prime. I am less than 30. List all.", "fill", "Answer = ____"),
        cb("Reasoning puzzles", ["Use logical deduction — not just trial and error.", "Prove your answer satisfies ALL conditions."], "I am the largest 2-digit prime. Answer: 97. Check: 97 is prime (not div by 2,3,5,7). 99=9×11 composite. 98 even. 97 ✓"),
        q("What is the largest 2-digit prime number?", "fill", "Answer = ____"),
        q("What is the smallest 3-digit prime number?", "fill", "Answer = ____"),
        q("Are there any even prime numbers greater than 2? Explain.", "fill", "Answer = ____"),
        q("I am a composite number with exactly 3 factors. What kind of number must I be? Give an example.", "fill", "Answer = ____"),
        q("Find two consecutive prime numbers that differ by 2 (twin primes) — give 3 examples.", "fill", "Answer = ____"),
        q("Challenge: A and B are primes. A × B = 143. Find A and B.", "fill", "Answer = ____"),
        q("The product of all primes less than 10 is ____.", "fill", "Answer = ____"),
        q("Challenge: Write the smallest number that has exactly 6 factors. What is it?", "fill", "Answer = ____"),
    ]


# ═══════════════════════════════════════════════════════════════
# ROUTER — maps (sublevel_code, sheet_num) → question list
# ═══════════════════════════════════════════════════════════════

_DISPATCH = {
    # Level 1
    "1A": {1:_L1A_1, 2:_L1A_2, 3:_L1A_3, 4:_L1A_4},
    "1B": {1:_L1B_1, 2:_L1B_2, 3:_L1B_3, 4:_L1B_4},
    "1C": {1:_L1C_1, 2:_L1C_2, 3:_L1C_3, 4:_L1C_4},
    "1D": {1:_L1D_1, 2:_L1D_2, 3:_L1D_3, 4:_L1D_4},
    "1E": {1:_L1E_1, 2:_L1E_2, 3:_L1E_3, 4:_L1E_4},
    "1F": {1:_L1F_1, 2:_L1F_2, 3:_L1F_3, 4:_L1F_4},
    "1G": {1:lambda:_L1G_s(1), 2:lambda:_L1G_s(2), 3:lambda:_L1G_s(3), 4:lambda:_L1G_s(4)},
    "1H": {1:lambda:_L1H_s(1), 2:lambda:_L1H_s(2), 3:lambda:_L1H_s(3), 4:lambda:_L1H_s(4)},
    "1I": {1:lambda:_L1I_s(1), 2:lambda:_L1I_s(2), 3:lambda:_L1I_s(3), 4:lambda:_L1I_s(4)},
    "1J": {1:lambda:_L1J_s(1), 2:lambda:_L1J_s(2), 3:lambda:_L1J_s(3), 4:lambda:_L1J_s(4)},
    "1CUM1": {1:lambda:_L1CUM1_s(1), 2:lambda:_L1CUM1_s(2), 3:lambda:_L1CUM1_s(3), 4:lambda:_L1CUM1_s(4)},
    "1CUM2": {1:lambda:_L1CUM2_s(1), 2:lambda:_L1CUM2_s(2), 3:lambda:_L1CUM2_s(3), 4:lambda:_L1CUM2_s(4)},
    "1CUM3": {1:lambda:_L1CUM3_s(1), 2:lambda:_L1CUM3_s(2), 3:lambda:_L1CUM3_s(3), 4:lambda:_L1CUM3_s(4)},
    "1REV":  {1:lambda:_L1REV_s(1), 2:lambda:_L1REV_s(2), 3:lambda:_L1REV_s(3), 4:lambda:_L1REV_s(4)},
    # Level 2
    "2A": {1:_L2A_1, 2:_L2A_2, 3:_L2A_3, 4:_L2A_4},
    "2B": {1:_L2B_1, 2:_L2B_2, 3:_L2B_3, 4:_L2B_4},
    "2C": {1:_L2C_1, 2:_L2C_2, 3:_L2C_3, 4:_L2C_4},
    "2D": {1:_L2D_1, 2:_L2D_2, 3:_L2D_3, 4:_L2D_4},
    "2E": {1:_L2E_1, 2:_L2E_2, 3:_L2E_3, 4:_L2E_4},
    "2F": {1:lambda:_L2F_s(1), 2:lambda:_L2F_s(2), 3:lambda:_L2F_s(3), 4:lambda:_L2F_s(4)},
    "2G": {1:lambda:_L2G_s(1), 2:lambda:_L2G_s(2), 3:lambda:_L2G_s(3), 4:lambda:_L2G_s(4)},
    "2H": {1:lambda:_L2H_s(1), 2:lambda:_L2H_s(2), 3:lambda:_L2H_s(3), 4:lambda:_L2H_s(4)},
    "2I": {1:lambda:_L2I_s(1), 2:lambda:_L2I_s(2), 3:lambda:_L2I_s(3), 4:lambda:_L2I_s(4)},
    "2J": {1:lambda:_L2J_s(1), 2:lambda:_L2J_s(2), 3:lambda:_L2J_s(3), 4:lambda:_L2J_s(4)},
    "2CUM1":{1:lambda:_L2CUM1_s(1), 2:lambda:_L2CUM1_s(2), 3:lambda:_L2CUM1_s(3), 4:lambda:_L2CUM1_s(4)},
    "2CUM2":{1:lambda:_L2CUM2_s(1), 2:lambda:_L2CUM2_s(2), 3:lambda:_L2CUM2_s(3), 4:lambda:_L2CUM2_s(4)},
    "2CUM3":{1:lambda:_L2CUM3_s(1), 2:lambda:_L2CUM3_s(2), 3:lambda:_L2CUM3_s(3), 4:lambda:_L2CUM3_s(4)},
    "2REV": {1:lambda:_L2REV_s(1), 2:lambda:_L2REV_s(2), 3:lambda:_L2REV_s(3), 4:lambda:_L2REV_s(4)},
}

def _fallback(code, sheet):
    """Placeholder for levels not yet written — makes app never crash."""
    return [
        cb(f"{code} — Sheet {sheet} (Coming Soon)",
           [f"This sublevel ({code}) is being prepared.",
            "Hand-crafted questions will be added soon.",
            "Thank you for your patience!"],
           f"Sublevel: {code}"),
    ] + [q(f"Question {i}: {code} content coming soon.", "fill", "Answer = ____")
         for i in range(1, 20)]


def get_questions(sublevel_code: str, sheet_num: str) -> list:
    """
    Main entry point. Returns a list of question dicts.
    sublevel_code: e.g. '1A', '2E', '1CUM1', '2REV'
    sheet_num: '1','2','3','4' or '1R','2R','3R','4R' for remedial
    """
    is_remedial = str(sheet_num).endswith("R")
    base_sheet = int(str(sheet_num).replace("R", ""))

    # Look up the function
    sublevel_map = _DISPATCH.get(sublevel_code)
    if sublevel_map:
        fn = sublevel_map.get(base_sheet)
        items = fn() if fn else _fallback(sublevel_code, base_sheet)
    else:
        items = _fallback(sublevel_code, base_sheet)

    # Ensure exactly 20 questions (pad or trim)
    qs = [x for x in items if x["type"] != "concept_box"]
    while len(qs) < 20:
        qs.append(q(f"{sublevel_code} Q{len(qs)+1}: solve carefully.", "fill", "Answer = ____"))

    # Rebuild in original order, replacing question items
    result = []
    qi = 0
    for item in items:
        if item["type"] == "concept_box":
            result.append(item)
        else:
            if qi < 20:
                result.append(qs[qi])
                qi += 1
    # Any remaining questions not yet added (if items had fewer than 20 qs)
    while qi < 20:
        result.append(qs[qi])
        qi += 1

    # Apply remedial number variation
    if is_remedial:
        result = remedialise(result, seed=hash(sublevel_code + str(sheet_num)) % 9999)

    return result
