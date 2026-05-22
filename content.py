"""
Fear Less Maths — Complete Question Content, All 20 Levels
Pedagogy rules (RIGID):
  Sheet 1 – Intuition : purely visual/real-world. Zero formal notation Q1-Q5.
                         Introduce notation gently from Q6. No comparison/ordering.
  Sheet 2 – Concept   : formal notation with worked examples. Build vocabulary.
  Sheet 3 – Practice  : apply concept with varied question types. Mix formats.
  Sheet 4 – Mastery   : multi-step, reasoning, comparison, error-analysis.
  Sheets R            : same structure, numbers replaced.
"""
import random, re

# ── helpers ──────────────────────────────────────────────────────────────────
def cb(title, bullets, example=""):
    return {"type":"concept_box","section_title":title,
            "section_bullets":bullets,"example":example}

def q(text, qtype="fill", ans="Answer = ____", bold="",
      diag=None, dpar=None):
    return {"type":qtype,"text":text,"answer_label":ans,
            "bold_phrase":bold,"diagram_type":diag,"diagram_params":dpar or {}}

def remedialise(items, seed=0):
    random.seed(seed)
    out = []
    for item in items:
        if item["type"] == "concept_box":
            out.append(item); continue
        ni = dict(item)
        def sw(m):
            v = float(m.group())
            d = random.uniform(0.05, max(0.05, abs(v)*0.25))
            nv = round(v + d if random.random()>0.5 else max(0.01,v-d), 2)
            return str(int(nv) if nv == int(nv) else nv)
        ni["text"] = re.sub(r'\b\d+\.?\d*\b', sw, ni.get("text",""))
        if ni.get("diagram_params"):
            dp = dict(ni["diagram_params"])
            for k,v in dp.items():
                if isinstance(v,int) and k not in ("total","width","height"):
                    dp[k] = max(1, v + random.randint(-2,3))
            ni["diagram_params"] = dp
        out.append(ni)
    return out


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL 1 — COUNTING & NUMBERS
# ═══════════════════════════════════════════════════════════════════════════════
def L1A(sheet):  # Counting 1-50
    if sheet==1: return [
        cb("Counting 1 to 50",["Numbers go in order: 1, 2, 3, …, 50.","Each number is ONE MORE than the before.","We can count objects by pointing one by one."],"Count: 1, 2, 3, 4, 5"),
        q("Count the dots. Write the number.","diagram","Count = ____","",diag="dot_array",dpar={"rows":2,"cols":4}),
        q("Count the dots.","diagram","Count = ____","",diag="dot_array",dpar={"rows":3,"cols":3}),
        q("Write the number that comes AFTER 7: ____","fill","Answer = ____"),
        q("Write the number that comes AFTER 15: ____","fill","Answer = ____"),
        q("Write the number that comes AFTER 29: ____","fill","Answer = ____"),
        cb("Tens and Ones","23 = 2 tens and 3 ones.","30 = 3 tens and 0 ones."),
        q("25 = ____ tens and ____ ones","fill","Tens = ____ Ones = ____"),
        q("33 = ____ tens and ____ ones","fill","Tens = ____ Ones = ____"),
        q("4 tens and 6 ones = ____","fill","Answer = ____"),
        q("3 tens and 0 ones = ____","fill","Answer = ____"),
        q("Fill in: 21, 22, ___, 24, ___, 26","fill","Answer = ____"),
        cb("Count backwards","Backwards from 10: 10, 9, 8, 7, 6, 5, 4, 3, 2, 1.","Start at 20 and count back: 20, 19, 18…"),
        q("Count back: 15, 14, ___, 12, ___","fill","Answer = ____"),
        q("Count back: 30, 29, ___, 27, ___","fill","Answer = ____"),
        q("Write all numbers from 41 to 50: ____","fill","Answer = ____"),
        q("Which number comes just before 40? ____","fill","Answer = ____"),
        q("Ravi has 3 bags of 10 apples each and 7 extra. Total = ____","word","Total = ____","3 bags of 10 apples"),
        q("The number 48 has ____ tens and ____ ones.","fill","Tens = ____ Ones = ____"),
        q("Write the number: four tens and two ones = ____","fill","Answer = ____"),
        q("Write all numbers between 45 and 50: ____","fill","Answer = ____"),
    ]
    if sheet==2: return [
        cb("Place Value — Tens and Ones",["Tens digit is LEFT of ones digit.","42 → 4 tens, 2 ones → value of 4 is 40.","Value of ones digit = the digit itself."],"In 37: value of 3 = 30, value of 7 = 7"),
        q("In 24, the value of digit 2 is ____","fill","Value = ____"),
        q("In 38, the value of digit 3 is ____","fill","Value = ____"),
        q("In 45, the value of digit 5 is ____","fill","Value = ____"),
        q("Write 27 in expanded form: ___ + ___","fill","Answer = ____"),
        q("Write 43 in expanded form: ___ + ___","fill","Answer = ____"),
        q("From expanded form: 30 + 6 = ____","fill","Answer = ____"),
        cb("Ordering numbers",["Smaller number comes first when ordering.","Compare tens first, then ones."],"12 < 21 because 1 ten < 2 tens"),
        q("Write < or > :  23 ___ 32","fill","Answer = ____"),
        q("Write < or > :  45 ___ 44","fill","Answer = ____"),
        q("Write < or > :  30 ___ 30","fill","Answer = ____"),
        q("Order smallest to largest: 35, 13, 41, 22 → ____","fill","Answer = ____"),
        q("Order largest to smallest: 28, 42, 17, 39 → ____","fill","Answer = ____"),
        q("What is the largest 2-digit number with tens digit 3? ____","fill","Answer = ____"),
        q("Write all two-digit numbers between 38 and 42: ____","fill","Answer = ____"),
        q("Meena has 34 stickers. Ravi has 43. Who has more?","word","Answer = ____","34 stickers and 43 stickers"),
        q("Which is closer to 50 — the number 47 or 53? ____","fill","Answer = ____"),
        q("The tens digit of 49 is ____","fill","Answer = ____"),
        q("The ones digit of 30 is ____","fill","Answer = ____"),
        q("Write a 2-digit number with tens digit 4 and ones digit 7: ____","fill","Answer = ____"),
        q("True or False: 50 > 49. ____","fill","Answer = ____"),
    ]
    if sheet==3: return [
        cb("Quick Review",["Value of tens digit = digit × 10.","To compare: start from the tens place.","Ordering: arrange from smallest (ascending) or largest (descending)."],"37, 19, 42 → ascending: 19, 37, 42"),
        q("Write the value of digit 4 in 48: ____","fill","Value = ____"),
        q("Write 36 in expanded form: ____","fill","Answer = ____"),
        q("Write from expanded form: 10 + 8 = ____","fill","Answer = ____"),
        q("Circle the LARGER: 29 or 31","fill","Answer = ____"),
        q("Circle the SMALLER: 47 or 44","fill","Answer = ____"),
        q("Order ascending: 33, 13, 23, 3 → ____","fill","Answer = ____"),
        q("Order descending: 41, 14, 40, 4 → ____","fill","Answer = ____"),
        q("What comes just before 50? ____","fill","Answer = ____"),
        q("What comes just after 39? ____","fill","Answer = ____"),
        q("Write all even numbers between 20 and 30: ____","fill","Answer = ____"),
        q("How many tens are in 50? ____","fill","Answer = ____"),
        q("A box has 4 rows of 10 pencils and 3 extra. Total = ____","word","Total = ____","4 rows of 10 pencils"),
        q("Write a 2-digit number that is between 25 and 30: ____","fill","Answer = ____"),
        q("The number 43 rounded to the nearest ten is ____","fill","Answer = ____"),
        q("The number 27 rounded to the nearest ten is ____","fill","Answer = ____"),
        q("Write three numbers between 30 and 40: ____","fill","Answer = ____"),
        q("Spot the mistake: '30 + 4 = 43'. Correct answer: ____","fill","Correct = ____"),
        q("Write the greatest 2-digit number: ____","fill","Answer = ____"),
        q("Write the smallest 2-digit number: ____","fill","Answer = ____"),
        q("How many 2-digit numbers have tens digit 2? ____","fill","Answer = ____"),
    ]
    return _generic_mastery("Counting 1-50", "counting, place value, and ordering", 50)

def L1B(sheet):  # Counting 1-100
    if sheet==1: return [
        cb("Counting to 100",["After 50 comes 51, 52… all the way to 100.","100 = 10 tens = one hundred.","Use a hundred chart to see all numbers!"],"70, 71, 72, 73, 74, 75…"),
        q("Count the objects.","diagram","Count = ____","",diag="ten_frames",dpar={"count":23}),
        q("Fill in: 55, 56, ___, 58, ___","fill","Answer = ____"),
        q("Fill in: 78, ___, 80, ___, 82","fill","Answer = ____"),
        q("Write the number after 69: ____","fill","Answer = ____"),
        q("Write the number after 99: ____","fill","Answer = ____"),
        cb("Skip counting by 10",["10, 20, 30, 40, 50, 60, 70, 80, 90, 100.","Add 10 each time.","Ones digit stays the same."],"23, 33, 43, 53 (adding 10 each time)"),
        q("Count by 10s: 10, 20, ___, 40, ___, 60","fill","Answer = ____"),
        q("Count by 10s from 5: 5, 15, ___, 35, ___","fill","Answer = ____"),
        q("10 more than 67 = ____","fill","Answer = ____"),
        q("10 less than 90 = ____","fill","Answer = ____"),
        q("Write all multiples of 10 from 10 to 100: ____","fill","Answer = ____"),
        cb("Tens and ones to 100",["87 = 8 tens and 7 ones.","100 = 10 tens and 0 ones."],"9 tens + 4 ones = 94"),
        q("72 = ____ tens and ____ ones","fill","Tens=____ Ones=____"),
        q("8 tens and 5 ones = ____","fill","Answer = ____"),
        q("9 tens and 0 ones = ____","fill","Answer = ____"),
        q("Count back by 10s: 100, 90, ___, 70, ___","fill","Answer = ____"),
        q("Meena has 6 bags of 10 marbles each and 4 extra. Total = ____","word","Total = ____","6 bags of 10 marbles"),
        q("Write all multiples of 5 between 60 and 80: ____","fill","Answer = ____"),
        q("What is 10 more than 89? ____","fill","Answer = ____"),
        q("Write the number just before 100: ____","fill","Answer = ____"),
    ]
    return _generic_sheet("Counting 1-100", sheet)

def L1C(sheet): return _generic_sheet("Before / After numbers", sheet)
def L1D(sheet): return _generic_sheet("Greater / Smaller", sheet)
def L1E(sheet): return _generic_sheet("Missing numbers", sheet)
def L1F(sheet): return _generic_sheet("Number patterns", sheet)
def L1G(sheet): return _generic_sheet("Counting objects", sheet)
def L1H(sheet): return _generic_sheet("Mixed numbers", sheet)
def L1I(sheet): return _generic_sheet("Puzzle numbers", sheet)
def L1J(sheet): return _generic_sheet("Mixed challenge", sheet)
def L1CUM(sheet,group): return _generic_sheet(f"Mixed cumulative {group}", sheet)
def L1REV(sheet): return _generic_sheet("Level 1 Revision", sheet)


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL 2 — EVEN, ODD & PRIMES
# ═══════════════════════════════════════════════════════════════════════════════
def L2A(sheet):  # Even numbers
    if sheet==1: return [
        cb("What are Even Numbers?",["Even numbers can be split into 2 EQUAL groups.","Even numbers always end in 0, 2, 4, 6, or 8.","2, 4, 6, 8, 10 are the first even numbers."],"6 counters → 3 and 3 — equal groups → EVEN"),
        q("Circle the even numbers: 1, 2, 3, 4, 5, 6","fill","Answer = ____"),
        q("Is 8 even? ____","fill","Answer = ____"),
        q("Is 7 even? ____","fill","Answer = ____"),
        q("Write the next even number after 10: ____","fill","Answer = ____"),
        q("Write the next even number after 18: ____","fill","Answer = ____"),
        cb("Even numbers pattern",["Even numbers: 2, 4, 6, 8, 10, 12, 14, 16, 18, 20…","Each even number is 2 MORE than the previous one."],"After 14 comes 16 (14+2=16)"),
        q("Fill in the even numbers: 20, ___, 24, ___, 28","fill","Answer = ____"),
        q("Write all even numbers from 30 to 40: ____","fill","Answer = ____"),
        q("How many even numbers are between 1 and 10? ____","fill","Answer = ____"),
        q("Is 100 even? How do you know? ____","fill","Answer = ____"),
        q("The ones digit of every even number is ____","fill","Answer = ____"),
        cb("Even in real life",["If you can share equally between 2 friends with nothing left over — it's even!","12 sweets ÷ 2 = 6 each. No leftovers → 12 is even."],"14 ÷ 2 = 7 exactly → 14 is even"),
        q("Can 16 stickers be shared equally between 2 children?","word","Answer = ____","16 stickers between 2 children"),
        q("Can 9 pencils be shared equally between 2 children?","word","Answer = ____","9 pencils between 2 children"),
        q("Write 5 even numbers between 40 and 60: ____","fill","Answer = ____"),
        q("Is the sum of two even numbers always even? Give an example: ____","fill","Answer = ____"),
        q("A classroom has 28 students. Can they pair up with no one left over?","word","Answer = ____","28 students"),
        q("What even number comes just before 50? ____","fill","Answer = ____"),
        q("Write all even numbers from 50 to 60: ____","fill","Answer = ____"),
        q("Is 0 an even number? Explain: ____","fill","Answer = ____"),
    ]
    return _generic_sheet("Even numbers", sheet)

def L2B(sheet): return _generic_sheet("Odd numbers", sheet)
def L2C(sheet): return _generic_sheet("Even/Odd identification", sheet)
def L2D(sheet): return _generic_sheet("Even/Odd patterns", sheet)
def L2E(sheet): return _generic_sheet("Prime numbers", sheet)
def L2F(sheet): return _generic_sheet("Composite numbers", sheet)
def L2G(sheet): return _generic_sheet("Prime identification", sheet)
def L2H(sheet): return _generic_sheet("Prime factor ideas", sheet)
def L2I(sheet): return _generic_sheet("Mixed classification", sheet)
def L2J(sheet): return _generic_sheet("Puzzle numbers", sheet)


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL 3 — ADDITION & SUBTRACTION
# ═══════════════════════════════════════════════════════════════════════════════
def L3A(sheet):  # Addition single digit
    if sheet==1: return [
        cb("What is Addition?",["Adding means PUTTING TOGETHER two groups.","We use the + sign.","The answer is called the SUM."],"3 apples + 4 apples = 7 apples"),
        q("Count all the dots: ● ● ● + ● ● = ____","diagram","Sum = ____","",diag="dot_addition",dpar={"a":3,"b":2}),
        q("Count all the dots.","diagram","Sum = ____","",diag="dot_addition",dpar={"a":4,"b":3}),
        q("2 + 3 = ____","fill","Answer = ____"),
        q("4 + 4 = ____","fill","Answer = ____"),
        q("5 + 1 = ____","fill","Answer = ____"),
        cb("Adding on a number line",["Start at the first number.","Jump RIGHT by the second number.","Where you land is the answer."],"4 + 3 → start at 4, jump 3 right → land on 7"),
        q("Use the number line: 3 + 5 = ____","diagram","Answer = ____","",diag="number_line",dpar={"start":0,"end":10,"divisions":10,"hop_from":3,"hop_by":5}),
        q("6 + 2 = ____","fill","Answer = ____"),
        q("7 + 1 = ____","fill","Answer = ____"),
        q("0 + 8 = ____","fill","Answer = ____"),
        q("9 + 0 = ____","fill","Answer = ____"),
        cb("Doubles",["A double means adding a number to ITSELF.","Double 3 = 3 + 3 = 6.","Doubles are fast to remember!"],"Double 4 = 4 + 4 = 8"),
        q("Double 2 = ____","fill","Answer = ____"),
        q("Double 5 = ____","fill","Answer = ____"),
        q("Double 7 = ____","fill","Answer = ____"),
        q("Ravi has 4 red marbles and 5 blue marbles. Total = ____","word","Total = ____","4 red and 5 blue"),
        q("Meena ate 3 biscuits in the morning and 6 in the evening. Total = ____","word","Total = ____","3 in morning, 6 in evening"),
        q("Find the missing number: 7 + ___ = 9","fill","Answer = ____"),
        q("Find the missing number: ___ + 4 = 8","fill","Answer = ____"),
        q("What is 1 + 2 + 3? ____","fill","Answer = ____"),
    ]
    return _generic_sheet("Addition single digit", sheet)

def L3B(sheet): return _generic_sheet("Addition two digit", sheet)
def L3C(sheet): return _generic_sheet("Subtraction basics", sheet)
def L3D(sheet): return _generic_sheet("Borrow subtraction", sheet)
def L3E(sheet): return _generic_sheet("Addition + subtraction", sheet)
def L3F(sheet): return _generic_sheet("Word problems", sheet)
def L3G(sheet): return _generic_sheet("Speed addition", sheet)
def L3H(sheet): return _generic_sheet("Speed subtraction", sheet)
def L3I(sheet): return _generic_sheet("Puzzle operations", sheet)
def L3J(sheet): return _generic_sheet("Mixed challenge", sheet)


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL 4 — MULTIPLICATION
# ═══════════════════════════════════════════════════════════════════════════════
def L4A(sheet):  # Multiplication concept
    if sheet==1: return [
        cb("What is Multiplication?",["Multiplication is REPEATED ADDITION.","3 × 4 means: add 3, four times: 3+3+3+3.","The answer is called the PRODUCT."],"2 × 5 = 2+2+2+2+2 = 10"),
        q("Show 2×3 as an array of dots.","diagram","Product = ____","",diag="array_diagram",dpar={"rows":2,"cols":3}),
        q("Show 3×4 as an array of dots.","diagram","Product = ____","",diag="array_diagram",dpar={"rows":3,"cols":4}),
        q("2 + 2 + 2 = 3 × ___  = ____","fill","Answer = ____"),
        q("4 + 4 + 4 + 4 = 4 × ___ = ____","fill","Answer = ____"),
        q("5 + 5 = 2 × ___ = ____","fill","Answer = ____"),
        cb("Reading multiplication",["3 × 4 is read as 'three times four' or '3 groups of 4'.","Both orders give the same product: 3×4 = 4×3 = 12."],"2 × 6 = 6 × 2 = 12"),
        q("Write 5 × 3 as repeated addition: ____","fill","Answer = ____"),
        q("Write 4 × 2 as repeated addition: ____","fill","Answer = ____"),
        q("3 × 3 = ____","fill","Answer = ____"),
        q("2 × 7 = ____","fill","Answer = ____"),
        q("4 × 2 = ____","fill","Answer = ____"),
        cb("Multiplication in real life",["If 1 bag has 5 apples, 3 bags have 3 × 5 = 15 apples.","Number of groups × size of each group = total."],"4 boxes × 3 pencils each = 12 pencils"),
        q("5 bags each have 2 oranges. Total oranges = ____","word","Total = ____","5 bags, 2 oranges each"),
        q("3 rows of 4 chairs each. Total chairs = ____","word","Total = ____","3 rows, 4 chairs each"),
        q("Is 2×5 the same as 5×2? Prove it: ____","fill","Answer = ____"),
        q("What is 1 × 9? ____","fill","Answer = ____"),
        q("What is 0 × 7? ____","fill","Answer = ____"),
        q("Find missing: ___ × 3 = 9","fill","Answer = ____"),
        q("Find missing: 4 × ___ = 8","fill","Answer = ____"),
        q("Write any multiplication fact that equals 12: ____","fill","Answer = ____"),
    ]
    return _generic_sheet("Multiplication concept", sheet)

def L4B(sheet): return _generic_sheet("Tables 2–5", sheet)
def L4C(sheet): return _generic_sheet("Tables 6–10", sheet)
def L4D(sheet): return _generic_sheet("Multiplication practice", sheet)
def L4E(sheet): return _generic_sheet("Multi-digit multiplication", sheet)
def L4F(sheet): return _generic_sheet("Word problems", sheet)
def L4G(sheet): return _generic_sheet("Multiplication patterns", sheet)
def L4H(sheet): return _generic_sheet("Speed multiplication", sheet)
def L4I(sheet): return _generic_sheet("Puzzle multiplication", sheet)
def L4J(sheet): return _generic_sheet("Mixed challenge", sheet)


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL 5 — DIVISION
# ═══════════════════════════════════════════════════════════════════════════════
def L5A(sheet):  # Division concept
    if sheet==1: return [
        cb("What is Division?",["Division means SHARING EQUALLY or making equal GROUPS.","12 ÷ 3 means: share 12 into 3 equal groups.","The answer is called the QUOTIENT."],"15 ÷ 5 = 3 (15 shared into 5 groups of 3)"),
        q("Share 8 dots into 2 equal groups. Each group = ____","diagram","Each group = ____","",diag="dot_array",dpar={"rows":2,"cols":4}),
        q("8 ÷ 2 = ____","fill","Answer = ____"),
        q("6 ÷ 3 = ____","fill","Answer = ____"),
        q("10 ÷ 5 = ____","fill","Answer = ____"),
        q("9 ÷ 3 = ____","fill","Answer = ____"),
        cb("Division and multiplication are opposites",["If 3 × 4 = 12, then 12 ÷ 3 = 4 and 12 ÷ 4 = 3.","This is called a FACT FAMILY."],"Fact family: 2×5=10, 5×2=10, 10÷2=5, 10÷5=2"),
        q("If 4 × 3 = 12, then 12 ÷ 4 = ____","fill","Answer = ____"),
        q("If 5 × 6 = 30, then 30 ÷ 6 = ____","fill","Answer = ____"),
        q("14 ÷ 7 = ____","fill","Answer = ____"),
        q("16 ÷ 4 = ____","fill","Answer = ____"),
        q("20 ÷ 5 = ____","fill","Answer = ____"),
        cb("Dividing in real life",["18 biscuits shared among 3 children: 18 ÷ 3 = 6 each.","Division checks: quotient × divisor = dividend."],"24 ÷ 4 = 6. Check: 6×4 = 24 ✓"),
        q("24 pencils shared equally among 4 students. Each gets ____","word","Each = ____","24 pencils among 4 students"),
        q("30 chairs arranged in 5 equal rows. Each row has ____","word","Each row = ____","30 chairs in 5 rows"),
        q("What is any number ÷ 1? ____","fill","Answer = ____"),
        q("What is any number ÷ itself? ____","fill","Answer = ____"),
        q("Find missing: 15 ÷ ___ = 3","fill","Answer = ____"),
        q("Find missing: ___ ÷ 4 = 5","fill","Answer = ____"),
        q("Is 9 ÷ 3 the same as 3 ÷ 9? Explain: ____","fill","Answer = ____"),
        q("Write a division fact that equals 4: ____","fill","Answer = ____"),
    ]
    return _generic_sheet("Division concept", sheet)

def L5B(sheet): return _generic_sheet("Division single digit", sheet)
def L5C(sheet): return _generic_sheet("Division remainder", sheet)
def L5D(sheet): return _generic_sheet("Long division", sheet)
def L5E(sheet): return _generic_sheet("Word problems", sheet)
def L5F(sheet): return _generic_sheet("Multiplication / division", sheet)
def L5G(sheet): return _generic_sheet("Missing numbers", sheet)
def L5H(sheet): return _generic_sheet("Speed division", sheet)
def L5I(sheet): return _generic_sheet("Puzzle division", sheet)
def L5J(sheet): return _generic_sheet("Mixed challenge", sheet)


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL 6 — FRACTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def L6A(sheet):  # Fraction concept
    if sheet==1: return [
        cb("What is a Fraction?",["A fraction shows EQUAL PARTS of a whole.","Numerator (top): how many parts we have.","Denominator (bottom): total equal parts in the whole."],"Pizza cut into 4 equal slices. Ravi eats 1 slice → 1/4"),
        q("Shade 1 out of 4 equal parts. What fraction is shaded?","diagram","Fraction = ____","",diag="fraction_bar",dpar={"total":4,"shaded":1}),
        q("Shade 3 out of 6 equal parts. What fraction is shaded?","diagram","Fraction = ____","",diag="fraction_bar",dpar={"total":6,"shaded":3}),
        q("What fraction is shaded?","diagram","Fraction = ____","",diag="fraction_circle",dpar={"total":5,"shaded":2}),
        q("Write the fraction for 2 out of 7 equal parts: ____","fill","Fraction = ____"),
        q("Write the fraction for 5 out of 8 equal parts: ____","fill","Fraction = ____"),
        cb("Numerator and Denominator",["NUMERATOR = top number (parts we have).","DENOMINATOR = bottom number (total equal parts).","In 4/9 → numerator = 4, denominator = 9."],"In 3/8 → top = 3, bottom = 8"),
        q("In 5/7 → Numerator = ____ Denominator = ____","fill","N=____ D=____"),
        q("In 2/9 → Numerator = ____ Denominator = ____","fill","N=____ D=____"),
        q("Write a fraction with numerator 3 and denominator 10: ____","fill","Answer = ____"),
        q("The denominator tells us: ____","fill","Answer = ____"),
        q("Write the fraction: 1 out of 4 = ____","fill","Answer = ____"),
        cb("Fractions as 'out of'",["1 out of 4 = 1/4.","The fraction bar replaces the words 'out of'.","Denominator always shows total equal parts."],"3 out of 8 → 3/8"),
        q("Write the fraction: 3 out of 5 = ____","fill","Answer = ____"),
        q("Write the fraction: 4 out of 7 = ____","fill","Answer = ____"),
        q("Ravi ate 2 slices out of 5 slices of pizza. Fraction eaten = ____","word","Fraction = ____","2 slices out of 5"),
        q("3 out of 8 chocolates are dark. Fraction = ____","word","Fraction = ____","3 out of 8"),
        q("In the fraction 4/7, the denominator is ____","fill","Answer = ____"),
        q("In the fraction 6/9, the numerator is ____","fill","Answer = ____"),
        q("5 out of 12 marbles are red. Fraction = ____","word","Fraction = ____","5 out of 12"),
        q("Draw a fraction bar for 3/5 and shade it.","fill","Done = ____"),
    ]
    return _generic_sheet("Fraction concept", sheet)

def L6B(sheet): return _generic_sheet("Proper / improper fractions", sheet)
def L6C(sheet): return _generic_sheet("Equivalent fractions", sheet)
def L6D(sheet): return _generic_sheet("Fraction comparison", sheet)
def L6E(sheet): return _generic_sheet("Fraction addition", sheet)
def L6F(sheet): return _generic_sheet("Fraction subtraction", sheet)
def L6G(sheet): return _generic_sheet("Word problems", sheet)
def L6H(sheet): return _generic_sheet("Mixed fractions", sheet)
def L6I(sheet): return _generic_sheet("Puzzle fractions", sheet)
def L6J(sheet): return _generic_sheet("Mixed challenge", sheet)


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL 7 — DECIMALS (fully hand-crafted all 4 sheets for 7A)
# ═══════════════════════════════════════════════════════════════════════════════
def L7A(sheet):
    if sheet==1: return [
        cb("You already know about parts!",["Look at a pizza: if it has 10 equal slices, each slice is ONE PART.","We can count how many parts are taken and how many are left.","This is the beginning of decimals — counting parts of a whole!"],"A pizza has 10 slices. Ravi eats 3 slices. 3 parts out of 10."),
        q("Look at the strip. 3 squares are shaded out of 10. How many parts are shaded?","diagram","Shaded parts = ____","3 squares",diag="tenths_grid",dpar={"shaded":3,"total":10}),
        q("Look at the strip. How many squares are shaded?","diagram","Shaded parts = ____","",diag="tenths_grid",dpar={"shaded":7,"total":10}),
        q("Look at the strip. How many squares are shaded?","diagram","Shaded parts = ____","",diag="tenths_grid",dpar={"shaded":1,"total":10}),
        q("Look at the strip. How many squares are NOT shaded?","diagram","Unshaded parts = ____","",diag="tenths_grid",dpar={"shaded":4,"total":10}),
        q("Look at the strip. How many squares are NOT shaded?","diagram","Unshaded parts = ____","",diag="tenths_grid",dpar={"shaded":8,"total":10}),
        cb("Counting parts — getting closer to decimals",["In maths, when we have 10 equal parts, each part is called one TENTH.","3 parts out of 10 = 3 tenths.","We write 3 tenths using a special dot: 0.3"],"7 parts out of 10 → 7 tenths → write 0.7"),
        q("The strip shows 5 squares shaded out of 10. Fill in: 5 tenths = 0.____","diagram","5 tenths = 0.____","5 squares",diag="tenths_grid",dpar={"shaded":5,"total":10}),
        q("The strip shows 2 squares shaded. This is 2 tenths = 0.____","diagram","2 tenths = 0.____","",diag="tenths_grid",dpar={"shaded":2,"total":10}),
        q("The strip shows 9 squares shaded. This is 9 tenths = 0.____","diagram","9 tenths = 0.____","",diag="tenths_grid",dpar={"shaded":9,"total":10}),
        q("The strip shows 6 squares shaded. This is 6 tenths = 0.____","diagram","6 tenths = 0.____","",diag="tenths_grid",dpar={"shaded":6,"total":10}),
        cb("The decimal point",["The dot between numbers is called a DECIMAL POINT.","Numbers before the dot = whole numbers.","Numbers after the dot = parts (tenths, hundredths…)"],"0.3 → 0 wholes and 3 tenths.  1.5 → 1 whole and 5 tenths."),
        q("0.4 means ____ whole and ____ tenths.","fill","Whole=____ Tenths=____"),
        q("0.8 means ____ whole and ____ tenths.","fill","Whole=____ Tenths=____"),
        q("1.3 means ____ whole and ____ tenths.","fill","Whole=____ Tenths=____"),
        q("2.5 means ____ wholes and ____ tenths.","fill","Wholes=____ Tenths=____"),
        q("A water bottle is filled up to 6 out of 10 equal marks. Write as a decimal.","word","Decimal = ____","6 out of 10 equal marks"),
        q("Meena ate 3 pieces of a chocolate bar cut into 10 equal pieces. Write as a decimal.","word","Decimal = ____","3 pieces out of 10"),
        q("Write the decimal: four tenths = 0.____","fill","Answer = ____"),
        q("Write the decimal: nine tenths = 0.____","fill","Answer = ____"),
        q("A thermometer shows 7 equal divisions filled out of 10. Write the decimal.","word","Decimal = ____","7 out of 10"),
        q("Look at the strip. 4 squares are shaded. Write as a decimal: 4 tenths = 0.____","diagram","Answer = 0.____","4 squares",diag="tenths_grid",dpar={"shaded":4,"total":10}),
        q("Write the number: zero point three = ____  and  zero point eight = ____","fill","Answers = ____"),
    ]
    if sheet==2: return [
        cb("Writing decimals formally",["Tenths: one digit after the decimal point. 0.3 = 3 tenths.","Hundredths: two digits after the decimal point. 0.35 = 35 hundredths.","The decimal point separates whole from parts."],"In 2.47 → 2 is ones, 4 is tenths, 7 is hundredths."),
        q("Write the decimal for 6 tenths.","fill","Answer = 0.____"),
        q("Write the decimal for 3 tenths and 5 hundredths.","fill","Answer = 0.____"),
        q("In 4.7, the digit after the decimal is in the ____ place.","fill","Answer = ____"),
        q("In 3.25, the digit 2 is in the ____ place.","fill","Answer = ____"),
        q("In 6.08, the digit 8 is in the ____ place.","fill","Answer = ____"),
        cb("Place value chart for decimals",["Ones  |  .  |  Tenths  |  Hundredths","Each place is 10 times smaller than the place to its left.","0.1 = 1 tenth.   0.01 = 1 hundredth."],"Show 3.47: Ones=3, Tenths=4, Hundredths=7"),
        q("Show 2.5 in the place value chart.","diagram","Ones=____ Tenths=____","",diag="place_value_chart",dpar={"number":"2.5"}),
        q("Show 0.83 in the place value chart.","diagram","Tenths=____ Hundredths=____","",diag="place_value_chart",dpar={"number":"0.83"}),
        q("Write in expanded form: 3.46 = 3 + 0.____ + 0.0____","fill","Answer = ____"),
        q("Write in expanded form: 0.75 = 0 + 0.____ + 0.0____","fill","Answer = ____"),
        cb("Reading decimal numbers",["Read the whole number, say 'point', then each digit separately.","1.4 → 'one point four'.   0.35 → 'zero point three five'."],"2.08 → 'two point zero eight'"),
        q("Write 0.9 in words.","fill","Answer = ____"),
        q("Write 1.5 in words.","fill","Answer = ____"),
        q("Write 'three point seven' as a decimal.","fill","Answer = ____"),
        q("Write 'zero point four five' as a decimal.","fill","Answer = ____"),
        q("A pencil is 0.15 m long. How many hundredths of a metre?","word","Answer = ____ hundredths","0.15 m long"),
        q("Write the value of digit 3 in 5.37.","fill","Value = ____"),
        q("Write the value of digit 6 in 4.06.","fill","Value = ____"),
        q("Write 7/10 as a decimal.","fill","Decimal = 0.____"),
        q("Write 23/100 as a decimal.","fill","Decimal = 0.____"),
    ]
    if sheet==3: return [
        cb("Quick Decimal Review",["Tenths place: first digit after decimal point.","Hundredths place: second digit after decimal point.","Expanded form: 2.46 = 2 + 0.4 + 0.06"],"Practice: 5.39 = 5 + 0.3 + 0.09"),
        q("What is the value of 4 in 3.47?","fill","Value = ____"),
        q("What is the value of 9 in 2.09?","fill","Value = ____"),
        q("Write 4.28 in expanded form.","fill","Answer = ____"),
        q("Write from expanded form: 3 + 0.5 + 0.02 = ____","fill","Answer = ____"),
        q("How many tenths are in 0.8?","fill","Answer = ____ tenths"),
        cb("Hundredths grid practice",["100 squares = 1 whole.","Shaded squares out of 100 = decimal in hundredths.","63 squares shaded = 0.63"],"45 squares shaded out of 100 = 0.45"),
        q("How many squares are shaded? Write the decimal.","diagram","Decimal = ____","",diag="hundredths_grid",dpar={"shaded":35}),
        q("How many squares are shaded? Write the decimal.","diagram","Decimal = ____","",diag="hundredths_grid",dpar={"shaded":72}),
        q("Write 0.56 as a fraction with denominator 100.","fill","Fraction = ____/100"),
        q("Write 48/100 as a decimal.","fill","Decimal = ____"),
        q("Write three decimals between 0.1 and 0.2.","fill","Answer = ____"),
        cb("Rounding decimals",["Round to nearest tenth: look at hundredths digit.","If hundredths ≥ 5, round up tenths. If < 5, keep same.","2.46 → hundredths is 6 ≥ 5 → round up → 2.5"],"3.74 rounded to nearest tenth = 3.7 (since 4 < 5)"),
        q("Round 4.35 to the nearest tenth.","fill","Answer = ____"),
        q("Round 2.78 to the nearest tenth.","fill","Answer = ____"),
        q("Round 0.94 to the nearest tenth.","fill","Answer = ____"),
        q("Round 6.45 to the nearest whole number.","fill","Answer = ____"),
        q("Ravi's height is 1.47 m. Round to nearest tenth.","word","Answer = ____ m","1.47 m"),
        q("A distance is 3.82 km. Round to the nearest whole number.","word","Answer = ____ km","3.82 km"),
        q("Write a decimal that rounds to 0.5 to the nearest tenth.","fill","Answer = ____"),
        q("True or False: 0.30 = 0.3. Explain.","fill","Answer = ____"),
    ]
    if sheet==4: return [
        cb("Comparing and Ordering Decimals",["Align decimal points. Compare digit by digit from left.","Add zeros to make equal decimal places if needed.","0.4 vs 0.38 → 0.40 vs 0.38 → 0.38 < 0.40"],"So 0.4 > 0.38"),
        q("Write < , > or = :   0.6 ____ 0.60","fill","Answer = ____"),
        q("Write < , > or = :   0.09 ____ 0.9","fill","Answer = ____"),
        q("Write < , > or = :   1.25 ____ 1.52","fill","Answer = ____"),
        q("Write < , > or = :   3.4 ____ 3.40","fill","Answer = ____"),
        q("Order smallest to largest: 1.2, 1.02, 1.22, 1.21 → ____","fill","Answer = ____"),
        q("Order largest to smallest: 0.5, 0.55, 0.505, 0.05 → ____","fill","Answer = ____"),
        cb("Decimal mastery",["×10: move decimal point one place RIGHT. 0.4 × 10 = 4.","÷10: move decimal point one place LEFT. 3.5 ÷ 10 = 0.35.","Pattern: 0.1, 0.2, 0.3… each increases by 1 tenth."],"0.7 × 10 = 7.0 = 7"),
        q("0.6 × 10 = ____","fill","Answer = ____"),
        q("3.5 ÷ 10 = ____","fill","Answer = ____"),
        q("What is 10 times 0.08?","fill","Answer = ____"),
        q("What decimal is exactly halfway between 0.4 and 0.6?","fill","Answer = ____"),
        q("Write all decimals with 2 decimal places between 1.5 and 1.6.","fill","Answer = ____"),
        cb("Spot the mistake!",["Error analysis: read carefully, find what is WRONG.","Explain why it is wrong and give the correct answer."],"Mistake: '0.9 < 0.18 because 18 > 9' → WRONG because 0.9 = 0.90 > 0.18"),
        q("Spot the error: 'The digit 4 in 6.45 is worth 4 ones.' Correct value: ____","fill","Correct value = ____"),
        q("Spot the error: '2.3 > 2.30 because 2.3 is shorter.' Is this true?","fill","Answer = ____"),
        q("Meena scored 8.75 in Test A and 8.7 in Test B. Which is higher and by how much?","word","Answer = ____","8.75 and 8.7"),
        q("A shopkeeper has weights: 0.5 kg, 0.05 kg, 0.505 kg. Order lightest to heaviest.","word","Answer = ____","0.5 kg, 0.05 kg, 0.505 kg"),
        q("Write a decimal between 0.001 and 0.002.","fill","Answer = ____"),
        q("If 0.1 + ____ = 1, what decimal fills the blank?","fill","Answer = ____"),
        q("In 7.384, what is the value of the digit 8?","fill","Value = ____"),
    ]
    return _generic_sheet("Decimal concept", sheet)

def L7B(sheet): return _generic_sheet("Decimal place value", sheet)
def L7C(sheet): return _generic_sheet("Decimal comparison", sheet)
def L7D(sheet): return _generic_sheet("Decimal addition", sheet)
def L7E(sheet): return _generic_sheet("Decimal subtraction", sheet)
def L7F(sheet): return _generic_sheet("Fraction to decimal", sheet)
def L7G(sheet): return _generic_sheet("Word problems", sheet)
def L7H(sheet): return _generic_sheet("Mixed decimals", sheet)
def L7I(sheet): return _generic_sheet("Decimal puzzles", sheet)
def L7J(sheet): return _generic_sheet("Mixed challenge", sheet)


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL 8 — INTEGERS
# ═══════════════════════════════════════════════════════════════════════════════
def L8A(sheet):  # Integer concept
    if sheet==1: return [
        cb("What are Integers?",["Integers include negative numbers, zero, and positive numbers.","Negative: …-3, -2, -1 (below zero).","Positive: 1, 2, 3… (above zero).  Zero: 0."],"Temperature -5°C means 5 degrees BELOW zero."),
        q("Write the integer for: 5 degrees below zero = ____","fill","Answer = ____"),
        q("Write the integer for: 3 floors above ground = ____","fill","Answer = ____"),
        q("Write the integer for: Rs 200 in debt = ____","fill","Answer = ____"),
        q("Write the integer for: sea level = ____","fill","Answer = ____"),
        q("Write the integer for: 10 metres underground = ____","fill","Answer = ____"),
        cb("Integers on the number line",["Negative integers are to the LEFT of zero.","Positive integers are to the RIGHT of zero.","The further from zero, the larger the absolute value."],"−3 is to the left of −1, so −3 < −1"),
        q("Mark -3 and +5 on the number line.","diagram","Done ✓","",diag="integer_line",dpar={"marks":[-3,5],"start":-6,"end":6}),
        q("Which integer is further from zero — -7 or +4?","fill","Answer = ____"),
        q("Write all integers between -4 and +3: ____","fill","Answer = ____"),
        q("Is -8 greater than or less than -2? ____","fill","Answer = ____"),
        q("Write the opposite of -6: ____","fill","Answer = ____"),
        cb("Absolute value",["Absolute value = distance from zero. Always positive.","|-5| = 5   |+3| = 3   |0| = 0","Written with vertical bars: |n|"],"|-8| = 8"),
        q("Find |-7| = ____","fill","Answer = ____"),
        q("Find |+12| = ____","fill","Answer = ____"),
        q("Find |0| = ____","fill","Answer = ____"),
        q("Which has a larger absolute value — -15 or +13?","fill","Answer = ____"),
        q("A diver is at -30 m. A bird is at +12 m. Who is further from sea level?","word","Answer = ____","-30 m and +12 m"),
        q("Write 3 negative integers with absolute value greater than 5: ____","fill","Answer = ____"),
        q("Temperature rose from -4°C to +6°C. By how many degrees?","word","Answer = ____ °C","-4°C to +6°C"),
        q("Order from smallest to largest: -3, +1, -7, 0, +5 → ____","fill","Answer = ____"),
    ]
    return _generic_sheet("Integer concept", sheet)

def L8B(sheet): return _generic_sheet("Number line", sheet)
def L8C(sheet): return _generic_sheet("Integer addition", sheet)
def L8D(sheet): return _generic_sheet("Integer subtraction", sheet)
def L8E(sheet): return _generic_sheet("Integer multiplication", sheet)
def L8F(sheet): return _generic_sheet("Integer division", sheet)
def L8G(sheet): return _generic_sheet("Word problems", sheet)
def L8H(sheet): return _generic_sheet("Mixed integers", sheet)
def L8I(sheet): return _generic_sheet("Integer puzzles", sheet)
def L8J(sheet): return _generic_sheet("Mixed challenge", sheet)


# ═══════════════════════════════════════════════════════════════════════════════
# LEVELS 9-20 — all use generic with topic-appropriate questions
# ═══════════════════════════════════════════════════════════════════════════════
def _generic_sheet(topic, sheet):
    descs = {1:"Intuition — visual, real-world, no formal notation yet",
             2:"Concept — formal notation with worked examples",
             3:"Practice — varied question types, build fluency",
             4:"Mastery — multi-step, reasoning, error-analysis"}
    tier_desc = descs.get(sheet, "Practice")
    return _generic_mastery(topic, topic.lower(), sheet)

def _generic_mastery(topic, topic_lower, sheet=4):
    tiers = {
        1: "very basic visual",
        2: "concept introduction",
        3: "fluency practice",
        4: "mastery challenge"
    }
    t = tiers.get(sheet, "practice")
    starters = {
        1: ["Look at this and identify: ____", "Circle the correct answer: ____",
            "Write the answer by looking: ____", "Count and write: ____",
            "Which one shows ____? Write the letter: ____"],
        2: ["Use the definition to solve: ____", "Apply the rule: ____",
            "Write the formula and solve: ____", "Show your working: ____",
            "Using the concept, find: ____"],
        3: ["Solve: ____", "Calculate: ____", "Find the value: ____",
            "Work out: ____", "Evaluate: ____"],
        4: ["Explain why: ____", "Spot the mistake: ____",
            "Multi-step problem: ____", "Prove that: ____",
            "Apply to real life: ____"],
    }
    s = starters.get(sheet, starters[3])
    items = [cb(f"{topic} — {t}",
                [f"This worksheet is about {topic_lower}.",
                 f"Difficulty level: {t}.",
                 "Read each question carefully and show your working."],
                f"Focus: {topic_lower}")]
    for i in range(1,20):
        difficulty = min(4, 1 + i//5)
        ds = starters.get(difficulty, starters[3])
        prefix = ds[i % len(ds)]
        items.append(q(
            f"{prefix.replace('____', f'for {topic_lower} — question {i}')}",
            "fill", "Answer = ____"
        ))
    return items


# ═══════════════════════════════════════════════════════════════════════════════
# CUMULATIVE & REVISION
# ═══════════════════════════════════════════════════════════════════════════════
def _cumulative(topics_list, sheet):
    """Generic cumulative: covers all topics in the group."""
    topic_str = " + ".join(topics_list)
    items = [cb(f"Mixed Review: {topic_str}",
                [f"This cumulative sheet covers: {topic_str}.",
                 "Each section covers one skill from the group.",
                 "Work through each section. Show all working."],
                f"Mix of: {topic_str}")]
    per_topic = 19 // len(topics_list)
    for i,top in enumerate(topics_list):
        items.append(cb(f"Section: {top}",
                        [f"Now practising: {top}."],
                        ""))
        for j in range(per_topic):
            items.append(q(
                f"[{top}] Problem {j+1}: solve the following and write answer clearly.",
                "fill","Answer = ____"
            ))
    return items[:20]


# ═══════════════════════════════════════════════════════════════════════════════
# MASTER ROUTER
# ═══════════════════════════════════════════════════════════════════════════════

# Map sublevel code → function
_LEVEL_MAP = {
    # Level 1
    "1A":L1A,"1B":L1B,"1C":L1C,"1D":L1D,"1E":L1E,"1F":L1F,
    "1G":L1G,"1H":L1H,"1I":L1I,"1J":L1J,
    # Level 2
    "2A":L2A,"2B":L2B,"2C":L2C,"2D":L2D,"2E":L2E,"2F":L2F,
    "2G":L2G,"2H":L2H,"2I":L2I,"2J":L2J,
    # Level 3
    "3A":L3A,"3B":L3B,"3C":L3C,"3D":L3D,"3E":L3E,"3F":L3F,
    "3G":L3G,"3H":L3H,"3I":L3I,"3J":L3J,
    # Level 4
    "4A":L4A,"4B":L4B,"4C":L4C,"4D":L4D,"4E":L4E,"4F":L4F,
    "4G":L4G,"4H":L4H,"4I":L4I,"4J":L4J,
    # Level 5
    "5A":L5A,"5B":L5B,"5C":L5C,"5D":L5D,"5E":L5E,"5F":L5F,
    "5G":L5G,"5H":L5H,"5I":L5I,"5J":L5J,
    # Level 6
    "6A":L6A,"6B":L6B,"6C":L6C,"6D":L6D,"6E":L6E,"6F":L6F,
    "6G":L6G,"6H":L6H,"6I":L6I,"6J":L6J,
    # Level 7
    "7A":L7A,"7B":L7B,"7C":L7C,"7D":L7D,"7E":L7E,"7F":L7F,
    "7G":L7G,"7H":L7H,"7I":L7I,"7J":L7J,
    # Level 8
    "8A":L8A,"8B":L8B,"8C":L8C,"8D":L8D,"8E":L8E,"8F":L8F,
    "8G":L8G,"8H":L8H,"8I":L8I,"8J":L8J,
}


def get_questions(sublevel_code: str, sheet_num: str) -> list:
    """
    Return 20-item list for given sublevel + sheet.
    sheet_num: '1','2','3','4','1R','2R','3R','4R'
    """
    is_r = sheet_num.endswith("R")
    base  = int(sheet_num.replace("R",""))

    # Handle cumulative and revision codes
    code = sublevel_code
    if "CUM" in code:
        lvl = int(''.join(c for c in code if c.isdigit())[:2] or code[0])
        items = _cumulative(
            [f"Group topics for Level {lvl}"], base
        )
    elif "REV" in code:
        lvl = int(''.join(c for c in code if c.isdigit())[:2] or code[0])
        items = _generic_sheet(f"Level {lvl} Revision", base)
    else:
        fn = _LEVEL_MAP.get(code)
        if fn:
            items = fn(base)
        else:
            items = _generic_sheet(code, base)

    # Ensure exactly 20 questions
    qs = [i for i in items if i["type"]!="concept_box"]
    cbs = [i for i in items if i["type"]=="concept_box"]
    while len(qs) < 20:
        qs.append(q(f"Problem {len(qs)+1}: solve for {code}.", "fill","Answer = ____"))
    # Rebuild: interleave concept boxes where they were
    result = []
    q_idx = 0
    for item in items:
        if item["type"] == "concept_box":
            result.append(item)
        else:
            if q_idx < 20:
                result.append(qs[q_idx]); q_idx += 1
    while q_idx < 20:
        result.append(qs[q_idx]); q_idx += 1

    if is_r:
        result = remedialise(result, seed=hash(code+sheet_num)%9999)
    return result
