"""
Fear Less Maths — Complete Question Content
All 20 Levels · All 280 Sublevels · All 4 Sheets
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
            d = random.uniform(0.05, max(0.05, abs(v)*0.25))
            nv = round(v + d if random.random()>0.5 else max(0.01,v-d), 2)
            return str(int(nv) if nv == int(nv) else nv)
        ni["text"] = re.sub(r"\b\d+\.?\d*\b", sw, ni.get("text",""))
        out.append(ni)
    return out

def _qs(topic, skills, example, sheet):
    """Topic-aware generic question generator."""
    tier = {1:"Intuition — See it",2:"Concept — Try it",
            3:"Practice — Do it",4:"Mastery — Prove it"}[sheet]
    q_templates = {
        1:[f"Look at this {topic} example: {example}. Write your answer: ____",
           f"From the {topic} concept, identify: ____",
           f"Write a real-world example of {topic}: ____",
           f"Match the {topic} pattern: ____",
           f"Without calculating, write what you observe about {topic}: ____"],
        2:[f"Apply the {topic} rule: ____",
           f"Use the {topic} formula: ____",
           f"Write the key definition of {topic}: ____",
           f"Solve using {topic} concept: ____",
           f"Complete this {topic} statement: ____"],
        3:[f"Calculate ({topic}): ____",
           f"Solve this {topic} problem: ____",
           f"Find the value ({topic}): ____",
           f"Work out ({topic}): ____",
           f"Show your working for {topic}: ____"],
        4:[f"Explain your {topic} reasoning: ____",
           f"Spot the error in this {topic} problem: ____",
           f"Multi-step {topic}: ____",
           f"Apply {topic} to a real-world problem: ____",
           f"Prove your {topic} answer is correct: ____"],
    }
    tmpl = q_templates[sheet]
    items = [cb(f"{topic} — {tier}", skills if isinstance(skills,list) else [skills], str(example))]
    for i in range(1, 20):
        items.append(q(tmpl[i % len(tmpl)], "fill", "Answer = ____"))
    return items

_Q_BANK = {
    "Counting 1-50": ["Numbers from 31 to 40: ____","Before 25: ____","After 48: ____","Order 37,13,49,22 smallest to largest: ____","3 tens and 7 ones = ____","Fill in: 21,22,___,24,___,26","4 tens and 6 ones = ____","Count back: 30,29,___,27,___","Write all numbers between 45 and 50: ____","How many tens in 40? ____"],
    "Counting 1-100": ["Numbers from 81 to 90: ____","10 more than 73: ____","10 less than 60: ____","Count by 5s from 45 to 70: ____","8 tens and 3 ones = ____","Count by 10s: 10,20,___,40,___","Fill in: 55,56,___,58,___","Count back by 10: 100,90,___,70,___","All multiples of 10 from 10 to 100: ____","Number just before 100: ____"],
    "Before/After": ["Before 30: ____","After 59: ____","Between 17 and 21: ____","Before and after 45: ____","Between 98 and 100: ____","Before 100: ____","After 39: ____","Numbers between 28 and 32: ____","Before and after 25: ____","Write before,number,after for 42: ____"],
    "Greater/Smaller": ["Write > or <: 54 ___ 45","Write > or <: 82 ___ 82","Greatest of 34,43,30,40: ____","Order ascending: 92,29,9,90: ____","True or False: 67 < 76","Smallest of 76,67,70,60: ____","Write > or <: 30 ___ 30","Order descending: 41,14,40,4: ____","True or False: 50 > 49","Write = > or <: 99 ___ 100"],
    "Missing numbers": ["Fill in: 25,_,27,_,29","3+___=11","___-5=8","Fill in: 60,_,80,_,100","___+23=47","Fill in: 1,2,___,4,5","15-___=9","Fill in: 5,10,___,20,25","___+14=30","50-___=27"],
    "Number patterns": ["Rule +3: 6,9,___,15,___","Rule -5: 40,35,___,25,___","Next: 2,4,8,16,___","Pattern: 1,3,5,7,9,___","Rule +4: 4,8,12,___,20","Rule +10: 20,30,___,50,___","Fill in: 48,46,___,42,___","Next three: 10,20,30,___,___,___","Find rule: 20,18,16,14,___","Pattern: 1,4,9,16,___"],
    "Even numbers": ["5 even numbers between 10 and 20: ____","Is 56 even? ____","Next even after 38: ____","Even numbers from 50 to 60: ____","Sum of 4 and 6: even or odd? ____","Is 100 even? ____","Even numbers from 30 to 40: ____","Is 0 even? ____","Next even after 18: ____","Largest even number less than 50: ____"],
    "Odd numbers": ["5 odd numbers between 10 and 20: ____","Is 43 odd? ____","Next odd after 27: ____","Odd numbers from 30 to 40: ____","Sum of 3 and 5: even or odd? ____","Is 101 odd? ____","Largest odd number less than 50: ____","Sum of 6 and 9: even or odd? ____","Is 14 odd? ____","Odd numbers from 21 to 31: ____"],
    "Even/Odd identification": ["Sort: 21,34,55,68,79 into even and odd: ____","Is 137 even or odd? ____","Is 1000 even or odd? ____","Is 4×7 even or odd? ____","How many even numbers from 1 to 20? ____","Is 83 even or odd? ____","Sort: 33,44,55,66,77,88: ____","Is product 3×5 even or odd? ____","True or False: all numbers ending in 0 are even: ____","Is 999 even or odd? ____"],
    "Prime numbers": ["List all primes less than 15: ____","Is 23 prime? ____","Is 35 prime? ____","Smallest prime: ____","How many primes between 1 and 10? ____","Only even prime: ____","Is 1 prime? ____","All primes between 20 and 30: ____","Is 29 prime? ____","Is 49 prime? ____"],
    "Composite numbers": ["Is 12 composite? ____","Factors of 18: ____","Is 17 composite? ____","Smallest composite number: ____","List 5 composite numbers: ____","Is 1 composite? ____","Factors of 30: ____","How many factors does 12 have? ____","Is 9 prime or composite? ____","List factor pairs of 24: ____"],
    "Addition single digit": ["3+8=____","7+6=____","Double 9=____","9+0=____","4+3+2=____","5+5=____","Find missing: ___+5=12","7+___=9","8+4=____","1+2+3+4=____"],
    "Addition two digit": ["34+25=____","47+38=____","56+37=____","43+___=70","63+28=____","21+33+15=____","Find missing: ___+47=83","17+15=____","46+27=____","55+38=____"],
    "Subtraction basics": ["15-8=____","20-13=____","18-___=9","13-7=____","30-15=____","12-___=5","___-6=8","9-4=____","If 8+6=14, then 14-8=____","10-3-4=____"],
    "Borrow subtraction": ["52-28=____","74-39=____","81-47=____","63-45=____","90-53=____","72-45=____","Check: 52-28 by adding back: ____","83-57=____","41-16=____","60-27=____"],
    "Multiplication concept": ["3×6=____","4×8=____","7×5=____","0×9=____","Find missing: ___×4=20","1×12=____","2+2+2+2=4×___=____","5 bags × 2 oranges = ____","Is 2×5=5×2? ____","___×3=9"],
    "Tables 2-5": ["2×9=____","3×7=____","4×6=____","5×8=____","3×___=18","2×8=____","4×9=____","5×7=____","3×8=____","4×___=28"],
    "Tables 6-10": ["6×7=____","8×9=____","7×6=____","9×4=____","6×___=42","10×7=____","7×8=____","9×9=____","8×6=____","7×___=49"],
    "Division concept": ["12÷4=____","20÷5=____","27÷9=____","0÷6=____","24÷___=6","If 5×7=35, then 35÷7=____","Any number ÷ itself = ____","Any number ÷ 1 = ____","15÷___=3","___÷4=5"],
    "Fraction concept": ["Write 3 out of 7 as fraction: ____","Numerator of 5/9: ____","Denominator of 4/11: ____","3/4 of 8 = ____","Is 5/5 = 1 whole? ____","Write 0.5 as fraction: ____","2 out of 7 equal parts = ____","In 4/7, denominator = ____","5 of 12 marbles are red. Fraction = ____","3 out of 5 = ____"],
    "Decimal concept": ["Write 0.6 in words: ____","7 tenths as decimal: ____","0.4 means ___ whole and ___ tenths","Which is greater: 0.5 or 0.3? ____","0.9+0.1=____","Write 0.3 as a fraction: ____","2 tenths = 0.____","0.8 means ___ whole and ___ tenths","Three squares shaded out of 10 = 0.____","1.3 means ___ whole and ___ tenths"],
    "Integer concept": ["-3+5=____","Absolute value of -8: ____","Order: -2,3,-5,1,0","Is -7 > -3? ____","Opposite of -9: ____","|-7|=____","|0|=____","5 degrees below zero = ____","All integers between -4 and +3: ____","Temperature: -4°C + 7°C = ____"],
    "Factors": ["Factors of 12: ____","Is 7 a factor of 42? ____","How many factors does 16 have? ____","Factor pairs of 18: ____","Is 6 a factor of 25? ____","Factors of 24: ____","Is 4 a factor of 30? ____","List all factors of 36: ____","HCF of 12 and 18: ____","Is 9 a factor of 72? ____"],
    "Multiples": ["First 5 multiples of 8: ____","Is 36 a multiple of 9? ____","LCM of 4 and 6: ____","First 5 multiples of 11: ____","Common multiples of 3 and 4 up to 20: ____","Is 50 a multiple of 7? ____","First 5 multiples of 6: ____","Is 48 a multiple of 8? ____","LCM of 3 and 5: ____","Multiples of 10 from 10 to 100: ____"],
    "HCF": ["HCF(12,18)=____","HCF(24,36)=____","HCF(15,25)=____","HCF(8,20)=____","Use HCF to simplify 12/16: ____","HCF(14,21)=____","HCF(30,45)=____","HCF(9,15)=____","HCF(16,24)=____","HCF(10,15)=____"],
    "LCM": ["LCM(4,6)=____","LCM(3,5)=____","LCM(8,12)=____","LCM(6,9)=____","Use LCM to add 1/4+1/6: ____","LCM(4,10)=____","LCM(3,4)=____","LCM(5,6)=____","LCM(2,3,4)=____","LCM(6,8)=____"],
    "Ratio concept": ["Simplify 6:9: ____","Write ratio of 12 to 18: ____","Are 2:3 and 4:6 equivalent? ____","Simplify 15:20: ____","If ratio 3:5 and total=40, each part=____","Simplify 10:15: ____","Write 8:12 in simplest form: ____","If ratio 2:3, first=10, second=____","Simplify 21:28: ____","Are 3:4 and 9:12 equivalent? ____"],
}

def _cum(topics, sheet):
    n = len(topics); per = 19 // n
    items = [cb(f"Mixed Review: {', '.join(topics)}",
                [f"This sheet covers: {', '.join(topics)}.",
                 "Each section practices one skill from the group.",
                 "Show all working clearly."],
                f"Covers: {', '.join(topics)}")]
    fallback = ["Solve this mixed problem: ____","Apply what you know: ____","Work out carefully: ____","Show your working: ____","Calculate and check: ____","Mixed review: ____","Apply the concept: ____","Find the answer: ____","Write the solution: ____","Verify your answer: ____"]
    for top in topics:
        items.append(cb(f"Section: {top}", [f"Practising: {top}.", "Show all working."], ""))
        bank = _Q_BANK.get(top, fallback)
        for j in range(per):
            items.append(q(bank[j % len(bank)], "fill", "Answer = ____"))
    while len([x for x in items if x["type"] != "concept_box"]) < 19:
        items.append(q(f"Mixed review from {', '.join(topics)}: ____", "fill", "Answer = ____"))
    return items

# ═══ LEVEL 1 ═══
def L1A(s):
    s1=[cb("Counting 1 to 50",["Numbers go in order: 1,2,3…50.","Each number is ONE MORE than before.","Count objects by pointing one by one."],"1,2,3,4,5 → each is one more"),
        q("Count and write the total dots.","diagram","Count = ____","",diag="dot_array",dpar={"rows":2,"cols":4}),
        q("Count the dots.","diagram","Count = ____","",diag="dot_array",dpar={"rows":3,"cols":3}),
        q("Write the number after 7","fill","Answer = ____"),
        q("Write the number after 15","fill","Answer = ____"),
        q("Write the number after 29","fill","Answer = ____"),
        cb("Tens and Ones",["23 = 2 tens and 3 ones.","30 = 3 tens and 0 ones."],"4 tens + 6 ones = 46"),
        q("25 = ____ tens and ____ ones","fill","Tens=____ Ones=____"),
        q("33 = ____ tens and ____ ones","fill","Tens=____ Ones=____"),
        q("4 tens and 6 ones = ____","fill","Answer = ____"),
        q("3 tens and 0 ones = ____","fill","Answer = ____"),
        q("Fill in: 21, 22, ___, 24, ___, 26","fill","Answer = ____"),
        cb("Count backwards",["Each number is ONE LESS when counting back."],"20,19,18,17…"),
        q("Count back: 15, 14, ___, 12, ___","fill","Answer = ____"),
        q("Count back: 30, 29, ___, 27, ___","fill","Answer = ____"),
        q("Write all numbers from 41 to 50","fill","Answer = ____"),
        q("Which number comes just before 40?","fill","Answer = ____"),
        q("Ravi has 3 bags of 10 apples and 7 extra. Total = ____","word","Total = ____","3 bags of 10"),
        q("48 has ____ tens and ____ ones","fill","Tens=____ Ones=____"),
        q("Four tens and two ones = ____","fill","Answer = ____"),
        q("Write all numbers between 45 and 50","fill","Answer = ____")]
    s2=[cb("Place Value",["Tens digit × 10 = its value.","In 42: tens digit 4 → value = 40.","Ones digit value = the digit itself."],"In 37: value of 3=30, value of 7=7"),
        q("In 24, value of digit 2 = ____","fill","Value = ____"),
        q("In 38, value of digit 3 = ____","fill","Value = ____"),
        q("In 45, value of digit 5 = ____","fill","Value = ____"),
        q("Write 27 in expanded form: ___ + ___","fill","Answer = ____"),
        q("Write 43 in expanded form: ___ + ___","fill","Answer = ____"),
        q("30 + 6 = ____","fill","Answer = ____"),
        cb("Comparing Numbers",["Compare tens first. If equal, compare ones.","< means less than, > means greater than."],"23 < 32 because 2 tens < 3 tens"),
        q("Write < or > : 23 ___ 32","fill","Answer = ____"),
        q("Write < or > : 45 ___ 44","fill","Answer = ____"),
        q("Order smallest to largest: 35, 13, 41, 22","fill","Answer = ____"),
        q("Order largest to smallest: 28, 42, 17, 39","fill","Answer = ____"),
        q("Largest 2-digit number with tens digit 3?","fill","Answer = ____"),
        q("Meena has 34 stickers. Ravi has 43. Who has more?","word","Answer = ____","34 and 43"),
        q("Which is closer to 50: 47 or 53?","fill","Answer = ____"),
        q("The tens digit of 49 is ____","fill","Answer = ____"),
        q("The ones digit of 30 is ____","fill","Answer = ____"),
        q("True or False: 50 > 49","fill","Answer = ____"),
        q("Write a 2-digit number with tens=4, ones=7","fill","Answer = ____"),
        q("Write all 2-digit numbers between 38 and 42","fill","Answer = ____"),
        q("Write < or > : 30 ___ 30","fill","Answer = ____")]
    s3=_qs("Counting 1-50",["value of each digit","expanded form","compare and order"],"In 48: 4 tens=40, 8 ones=8",3)
    s4=_qs("Counting 1-50 Mastery",["explain place value","spot errors","multi-step"],"Value of 4 in 48 is 10× value of 4 in 14",4)
    return [s1,s2,s3,s4][s-1]

def L1B(s):
    s1=[cb("Counting to 100",["After 50 comes 51,52…100.","100 = 10 tens.","Skip-count by 10: 10,20,30…100."],"70,71,72,73…"),
        q("Count the objects.","diagram","Count = ____","",diag="ten_frames",dpar={"count":23}),
        q("Fill in: 55, 56, ___, 58, ___","fill","Answer = ____"),
        q("Fill in: 78, ___, 80, ___, 82","fill","Answer = ____"),
        q("Number after 69: ____","fill","Answer = ____"),
        q("Number after 99: ____","fill","Answer = ____"),
        cb("Skip counting by 10",["10,20,30,40,50,60,70,80,90,100.","Add 10 each time.","Ones digit stays the same."],"23,33,43,53 (adding 10 each time)"),
        q("Count by 10s: 10,20,___,40,___,60","fill","Answer = ____"),
        q("Count by 10s from 5: 5,15,___,35,___","fill","Answer = ____"),
        q("10 more than 67 = ____","fill","Answer = ____"),
        q("10 less than 90 = ____","fill","Answer = ____"),
        q("All multiples of 10 from 10 to 100","fill","Answer = ____"),
        cb("Tens and ones to 100",["87 = 8 tens and 7 ones.","100 = 10 tens and 0 ones."],"9 tens + 4 ones = 94"),
        q("72 = ____ tens and ____ ones","fill","Tens=____ Ones=____"),
        q("8 tens and 5 ones = ____","fill","Answer = ____"),
        q("9 tens and 0 ones = ____","fill","Answer = ____"),
        q("Count back by 10: 100,90,___,70,___","fill","Answer = ____"),
        q("6 bags of 10 marbles + 4 extra. Total = ____","word","Total = ____","6 bags of 10"),
        q("All multiples of 5 between 60 and 80","fill","Answer = ____"),
        q("10 more than 89 = ____","fill","Answer = ____"),
        q("Number just before 100: ____","fill","Answer = ____")]
    s2=_qs("Counting 1-100",["place value to 100","expanded form","compare and order"],"96=90+6; 79<97",2)
    s3=_qs("Counting 1-100",["skip count by 2s 5s 10s","round to nearest 10","word problems"],"Round 83→80; skip by 5: 55,60,65",3)
    s4=_qs("Counting 1-100 Mastery",["explain place value","patterns","multi-step"],"Largest 2-digit even=98; smallest 2-digit odd=11",4)
    return [s1,s2,s3,s4][s-1]

def L1C(s):
    s1=[cb("Before and After",["Number BEFORE = one less.","Number AFTER = one more.","Before=left, After=right on number line."],"Before 7→6; After 7→8"),
        q("Number before 5: ____","fill","Answer = ____"),
        q("Number after 5: ____","fill","Answer = ____"),
        q("Number before 12: ____","fill","Answer = ____"),
        q("Number after 12: ____","fill","Answer = ____"),
        q("Number before 20: ____","fill","Answer = ____"),
        q("Number after 20: ____","fill","Answer = ____"),
        cb("Between",["Between = sandwiched on both sides.","Numbers between 5 and 8: 6 and 7."],"Between 10 and 14: 11,12,13"),
        q("Numbers between 4 and 8: ____","fill","Answer = ____"),
        q("Numbers between 15 and 19: ____","fill","Answer = ____"),
        q("Numbers between 28 and 32: ____","fill","Answer = ____"),
        q("Number just before 50: ____","fill","Answer = ____"),
        q("Number just after 39: ____","fill","Answer = ____"),
        cb("Before, After, Between Practice",["Count forward for after, backward for before."],"Before 30:29; After 30:31; Between 29 and 31:30"),
        q("Before and after 25: ____ and ____","fill","Before=____ After=____"),
        q("Before and after 49: ____ and ____","fill","Before=____ After=____"),
        q("Three numbers between 40 and 45: ____","fill","Answer = ____"),
        q("Ravi says the number before 30 is 31. Correct him.","fill","Correct = ____"),
        q("What number is between 99 and 101?","fill","Answer = ____"),
        q("Number just before 100: ____","fill","Answer = ____"),
        q("Write before, number, after for 42: ____","fill","Answer = ____")]
    s2=_qs("Before/After/Between",["formal definition","number line","multi-step"],"Before 60:59; After 60:61; Between 59 and 61:60",2)
    s3=_qs("Before/After/Between",["without number line","spot errors","word problems"],"Before 100:99; Between 74 and 76:75",3)
    s4=_qs("Before/After/Between Mastery",["multi-step","explain reasoning","apply in problems"],"I am between 30 and 32. I am one more than 30. I am 31.",4)
    return [s1,s2,s3,s4][s-1]

def L1D(s):
    s1=[cb("Greater and Smaller",["Greater = MORE. Smaller = LESS.","Use > for greater, < for smaller.","= means equal."],"5>3 (5 is greater); 3<5 (3 is smaller)"),
        q("Circle the greater: 8 or 5","fill","Answer = ____"),
        q("Circle the smaller: 12 or 21","fill","Answer = ____"),
        q("Write > or < : 9 ___ 6","fill","Answer = ____"),
        q("Write > or < : 14 ___ 41","fill","Answer = ____"),
        q("Write > or < : 30 ___ 30","fill","Answer = ____"),
        cb("Comparing 2-digit numbers",["Compare tens first.","If tens equal, compare ones."],"45>43 (same tens, 5 ones>3 ones)"),
        q("Write > or < : 56 ___ 65","fill","Answer = ____"),
        q("Write > or < : 72 ___ 72","fill","Answer = ____"),
        q("Write > or < : 89 ___ 98","fill","Answer = ____"),
        q("Greatest of: 34, 43, 30, 40 = ____","fill","Answer = ____"),
        q("Smallest of: 76, 67, 70, 60 = ____","fill","Answer = ____"),
        cb("Equal, Greater, Smaller",["= means exactly the same."],"23=23; 24>23; 22<23"),
        q("Write =, > or < : 50 ___ 50","fill","Answer = ____"),
        q("Write =, > or < : 99 ___ 100","fill","Answer = ____"),
        q("True or False: 45 < 54","fill","Answer = ____"),
        q("True or False: 37 > 37","fill","Answer = ____"),
        q("Ravi has 42 cards. Meena has 24. Who has more?","word","Answer = ____","42 and 24"),
        q("Order: 19, 91, 9, 90 → smallest to greatest","fill","Answer = ____"),
        q("Find a number greater than 50 and smaller than 55","fill","Answer = ____"),
        q("Find a number greater than 67 and smaller than 70","fill","Answer = ____")]
    s2=_qs("Greater/Smaller",["formal comparison","inequality signs","ordering"],"< means less than; > means greater than; 34<43",2)
    s3=_qs("Greater/Smaller",["compare 3-digit numbers","order lists","word problems"],"Compare 342 and 324: same hundreds, 4>2 tens → 342>324",3)
    s4=_qs("Greater/Smaller Mastery",["multi-step","explain reasoning","error analysis"],"Order 5 numbers; find all numbers between two values",4)
    return [s1,s2,s3,s4][s-1]

def L1E(s):
    s1=[cb("Missing Numbers",["A blank = something hidden.","Look at the pattern around the blank.","Count forwards or backwards to find it."],"3,___,5 → the blank is 4"),
        q("Fill in: 1, 2, ___, 4, 5","fill","Answer = ____"),
        q("Fill in: 8, ___, 10, 11, ___","fill","Answer = ____"),
        q("Fill in: 15, 16, ___, ___, 19","fill","Answer = ____"),
        q("Fill in: ___, 22, 23, 24, ___","fill","Answer = ____"),
        q("Fill in: 35, ___, 37, ___, 39","fill","Answer = ____"),
        cb("Missing in patterns",["Find the rule first: +1,+2,+5,+10?","Apply the rule to fill the blank."],"10,20,___,40 → rule:+10 → missing=30"),
        q("Fill in: 10, 20, ___, 40, ___","fill","Answer = ____"),
        q("Fill in: 5, 10, 15, ___, 25","fill","Answer = ____"),
        q("Fill in: 2, 4, ___, 8, ___, 12","fill","Answer = ____"),
        q("Fill in: 50, ___, 70, ___, 90","fill","Answer = ____"),
        q("Fill in: ___, 45, ___, 35, 30","fill","Answer = ____"),
        cb("Missing numbers in sums",["Use inverse operations.","6+___=10 → think 10-6=4"],"6+___=10 → 10-6=4"),
        q("3 + ___ = 8","fill","Missing = ____"),
        q("___ + 5 = 12","fill","Missing = ____"),
        q("15 - ___ = 9","fill","Missing = ____"),
        q("___ - 6 = 7","fill","Missing = ____"),
        q("20 + ___ = 34","fill","Missing = ____"),
        q("___ + 14 = 30","fill","Missing = ____"),
        q("50 - ___ = 27","fill","Missing = ____"),
        q("___ - 15 = 20","fill","Missing = ____")]
    s2=_qs("Missing Numbers",["pattern rule","inverse operations","multi-step"],"__,14,__,16 → pattern +1 → 13,15",2)
    s3=_qs("Missing Numbers",["varied gaps","mixed operations","word problems"],"Meena has __ toys, gets 5 more, now has 12. __=7",3)
    s4=_qs("Missing Numbers Mastery",["spot errors","explain method","multi-step"],"A+B=15, A-B=5 → A=10, B=5",4)
    return [s1,s2,s3,s4][s-1]

def L1F(s):
    s1=[cb("Number Patterns",["A pattern follows a rule.","Find what changes each time.","Common rules: +1,+2,+5,+10,-1,-2…"],"2,4,6,8 → rule: add 2"),
        q("Rule:+1. Fill: 11,12,___,14,___","fill","Answer = ____"),
        q("Rule:+2. Fill: 4,6,___,10,___","fill","Answer = ____"),
        q("Rule:+5. Fill: 5,10,___,20,___","fill","Answer = ____"),
        q("Rule:+10. Fill: 20,30,___,50,___","fill","Answer = ____"),
        q("Find rule and next: 3,6,9,12,___","fill","Rule=____ Next=____"),
        cb("Decreasing patterns",["Some patterns count DOWN.","Find how much is subtracted each time."],"20,17,14,11 → rule: subtract 3"),
        q("Find rule: 20,18,16,14,___","fill","Rule=____ Next=____"),
        q("Find rule: 50,45,40,35,___","fill","Rule=____ Next=____"),
        q("Fill in: 100,90,___,70,___","fill","Answer = ____"),
        q("Fill in: 48,46,___,42,___","fill","Answer = ____"),
        q("Next three: 10,20,30,___,___,___","fill","Answer = ____"),
        cb("Pattern puzzles",["Patterns can use different rules.","Always check at least 2 gaps."],"1,2,4,8 → each doubles!"),
        q("Pattern rule: 1,3,5,7,9 → ____","fill","Rule = ____"),
        q("Next three: 99,98,97,___,___,___","fill","Answer = ____"),
        q("Write your own +3 pattern starting at 6","fill","Answer = ____"),
        q("Write your own -4 pattern starting at 40","fill","Answer = ____"),
        q("Pattern: 1,4,9,16,___ (square numbers)","fill","Next = ____"),
        q("Meena saves Rs 5/day. Day 1: Rs 5. Day 5: Rs ____","word","Answer = ____","Rs 5 per day"),
        q("Ravi counts: 3,6,9,12. He says next is 16. Correct him.","fill","Correct = ____"),
        q("Fill in: 2,5,8,11,___,17,___","fill","Answer = ____")]
    s2=_qs("Number Patterns",["identify rule","extend patterns","create patterns"],"Rule +4: 4,8,12,16,20",2)
    s3=_qs("Number Patterns",["mixed rules","word problems","pattern tables"],"Day 1:2,Day 2:4,Day 3:6 → pattern ×2",3)
    s4=_qs("Number Patterns Mastery",["complex rules","predict far terms","explain patterns"],"Pattern +3 from 1: 10th term=1+9×3=28",4)
    return [s1,s2,s3,s4][s-1]

def L1G(s): return _qs("Counting Objects",["count groups and totals","tally marks","pictographs"],"Tally IIII I=6",s)
def L1H(s): return _qs("Mixed Numbers 1-100",["read and write numbers","place value","ordering and comparing"],"Forty-seven=47; 7 tens+3 ones=73",s)
def L1I(s): return _qs("Number Puzzles",["logic and reasoning","use clues","magic squares"],"I am odd, between 10 and 20, digits add to 9. I am 9… no, 18!",s)
def L1J(s): return _qs("Mixed Challenge Numbers",["combine all skills","multi-step","explain and verify"],"Compare, order, patterns, missing numbers",s)
def L1CUM1(s): return _cum(["Counting 1-50","Counting 1-100","Before/After"],s)
def L1CUM2(s): return _cum(["Greater/Smaller","Missing numbers","Number patterns"],s)
def L1CUM3(s): return _cum(["Counting objects","Mixed numbers","Number puzzles"],s)
def L1REV(s):  return _qs("Level 1 Revision",["count","compare","patterns and missing numbers"],"Before/after; >/</=; pattern rules; missing addends",s)

# ═══ LEVEL 2 ═══
def L2A(s):
    s1=[cb("Even Numbers",["Even numbers end in 0,2,4,6 or 8.","They split into 2 EQUAL groups.","2,4,6,8,10,12… are even."],"6=3+3 (equal groups) → EVEN"),
        q("Circle the evens: 1,2,3,4,5,6","fill","Evens = ____"),
        q("Is 8 even?","fill","Yes or No = ____"),
        q("Is 7 even?","fill","Yes or No = ____"),
        q("Next even after 10: ____","fill","Answer = ____"),
        q("Next even after 18: ____","fill","Answer = ____"),
        cb("Even number pattern",["2,4,6,8,10,12… each = previous +2.","Ones digit: always 0,2,4,6 or 8."],"After 14 → 16 (14+2=16)"),
        q("Fill evens: 20,___,24,___,28","fill","Answer = ____"),
        q("All even numbers from 30 to 40","fill","Answer = ____"),
        q("How many even numbers from 1 to 10?","fill","Answer = ____"),
        q("Is 100 even? How do you know?","fill","Answer = ____"),
        q("Ones digit of every even number: ____","fill","Answer = ____"),
        cb("Even in real life",["12÷2=6 exact → 12 is even.","If you can pair everything up → even."],"14 socks → 7 pairs → 14 is even"),
        q("Can 16 stickers be shared equally between 2?","word","Answer = ____","16 stickers"),
        q("Can 9 pencils be shared equally between 2?","word","Answer = ____","9 pencils"),
        q("Five even numbers between 40 and 60","fill","Answer = ____"),
        q("Even+Even is always even? Give an example.","fill","Answer = ____"),
        q("28 students — can they all pair up?","word","Answer = ____","28 students"),
        q("Even number just before 50: ____","fill","Answer = ____"),
        q("All even numbers from 50 to 60","fill","Answer = ____"),
        q("Is 0 even? Explain.","fill","Answer = ____")]
    s2=_qs("Even Numbers",["formal definition n÷2=0 remainder","even+even=even","divisibility by 2"],"n is even if n÷2 has no remainder. 14÷2=7 ✓",2)
    s3=_qs("Even Numbers",["identify quickly","word problems","patterns"],"Even numbers form pairs; odd ones have one left over",3)
    s4=_qs("Even Numbers Mastery",["proof reasoning","multi-step","operations with evens"],"Even×Even=Even; Even+Odd=Odd",4)
    return [s1,s2,s3,s4][s-1]

def L2B(s):
    s1=[cb("Odd Numbers",["Odd numbers end in 1,3,5,7 or 9.","They CANNOT split into 2 equal groups.","1,3,5,7,9,11… are odd."],"7=3+3+1 → one left over → ODD"),
        q("Circle the odds: 1,2,3,4,5,6,7","fill","Odds = ____"),
        q("Is 9 odd?","fill","Yes or No = ____"),
        q("Is 14 odd?","fill","Yes or No = ____"),
        q("Next odd after 7: ____","fill","Answer = ____"),
        q("Next odd after 21: ____","fill","Answer = ____"),
        cb("Odd number pattern",["1,3,5,7,9,11… each = previous +2.","Ones digit: always 1,3,5,7 or 9."],"After 15 → 17 (15+2)"),
        q("Fill odds: 11,___,15,___,19","fill","Answer = ____"),
        q("All odd numbers from 21 to 31","fill","Answer = ____"),
        q("How many odd numbers from 1 to 10?","fill","Answer = ____"),
        q("Is 101 odd? How do you know?","fill","Answer = ____"),
        q("Ones digit of every odd number: ____","fill","Answer = ____"),
        cb("Odd and Even together",["Even+Odd=Odd (always).","Odd+Odd=Even (always).","Consecutive numbers alternate: even,odd,even,odd…"],"4+5=9 (odd); 3+5=8 (even)"),
        q("3+4=___. Odd or even?","fill","Answer = ____"),
        q("5+7=___. Odd or even?","fill","Answer = ____"),
        q("6+9=___. Odd or even?","fill","Answer = ____"),
        q("All odd numbers from 41 to 51","fill","Answer = ____"),
        q("Largest odd number less than 50: ____","fill","Answer = ____"),
        q("Can 15 be shared equally between 2?","word","Answer = ____","15 items"),
        q("4 consecutive odd numbers starting at 23: ____","fill","Answer = ____"),
        q("Sum of first 5 odd numbers — odd or even?","fill","Answer = ____")]
    s2=_qs("Odd Numbers",["formal definition","odd in operations","patterns"],"Odd+Even=Odd; Odd×Odd=Odd",2)
    s3=_qs("Odd Numbers",["identify quickly","word problems","mixed odd/even"],"Odd numbers cannot be divided equally by 2",3)
    s4=_qs("Odd Numbers Mastery",["proofs","multi-step","combine with primes"],"Product of two odd numbers is always odd",4)
    return [s1,s2,s3,s4][s-1]

def L2C(s):
    s1=[cb("Even or Odd — How to tell",["Look at the ONES digit ONLY.","Ones 0,2,4,6,8 → EVEN.","Ones 1,3,5,7,9 → ODD."],"137 → ones digit 7 → ODD"),
        q("Is 34 even or odd?","fill","Answer = ____"),
        q("Is 75 even or odd?","fill","Answer = ____"),
        q("Is 100 even or odd?","fill","Answer = ____"),
        q("Is 83 even or odd?","fill","Answer = ____"),
        q("Is 56 even or odd?","fill","Answer = ____"),
        cb("Sorting numbers",["Sort into even and odd groups.","Check only the ones digit."],"24,35,48,71 → even:24,48; odd:35,71"),
        q("Sort: 12,15,18,21,24,27 → even and odd","fill","Even=____ Odd=____"),
        q("Sort: 33,44,55,66,77,88 → even and odd","fill","Even=____ Odd=____"),
        q("How many even numbers from 1 to 20?","fill","Answer = ____"),
        q("How many odd numbers from 1 to 20?","fill","Answer = ____"),
        q("First 5 even numbers: ____","fill","Answer = ____"),
        cb("Quick identification",["No need to count — just look at ones digit."],"998 → ones=8 → EVEN instantly"),
        q("Even or odd: 999","fill","Answer = ____"),
        q("Even or odd: 1000","fill","Answer = ____"),
        q("Even or odd: 247","fill","Answer = ____"),
        q("Even or odd: 364","fill","Answer = ____"),
        q("3 even and 3 odd numbers between 50 and 70","fill","Answer = ____"),
        q("Is the product 3×4 even or odd?","fill","Answer = ____"),
        q("Is the product 3×5 even or odd?","fill","Answer = ____"),
        q("True or False: All numbers ending in 0 are even.","fill","Answer = ____")]
    s2=_qs("Even/Odd Identification",["ones digit rule","sort and classify","multi-digit numbers"],"ones=0,2,4,6,8→even; 1,3,5,7,9→odd",2)
    s3=_qs("Even/Odd Identification",["apply in operations","word problems","patterns"],"Even×Any=Even; Odd×Odd=Odd",3)
    s4=_qs("Even/Odd Mastery",["formal proof ideas","multi-step","error analysis"],"Is sum of first 100 natural numbers even or odd?",4)
    return [s1,s2,s3,s4][s-1]

def L2D(s): return _qs("Even/Odd Patterns",["alternating patterns","operations with even/odd","predict results"],"E+E=E; O+O=E; E+O=O; E×E=E; O×O=O",s)

def L2E(s):
    s1=[cb("Prime Numbers",["A prime has exactly 2 factors: 1 and itself.","2,3,5,7,11,13,17,19… are prime.","1 is NOT prime (only 1 factor)."],"7: factors are 1 and 7 only → PRIME"),
        q("Is 2 prime?","fill","Answer = ____"),
        q("Is 4 prime?","fill","Answer = ____"),
        q("Is 11 prime?","fill","Answer = ____"),
        q("Is 15 prime?","fill","Answer = ____"),
        q("Factors of 6: ____. Is 6 prime?","fill","Factors=____ Prime?=____"),
        cb("Testing for primes",["Divide by 2,3,5,7… up to square root.","If any divides exactly → NOT prime.","If none divide exactly → PRIME."],"Is 13 prime? 13÷2=6.5, 13÷3=4.3 → PRIME"),
        q("Is 17 prime? Test by dividing: ____","fill","Answer = ____"),
        q("Is 21 prime? Test: ____","fill","Answer = ____"),
        q("Is 29 prime? Test: ____","fill","Answer = ____"),
        q("All prime numbers less than 20: ____","fill","Answer = ____"),
        q("How many prime numbers are less than 10?","fill","Answer = ____"),
        cb("Special prime facts",["2 is the ONLY even prime number.","Every prime > 2 is odd.","There are infinitely many primes."],"Even primes: only 2"),
        q("The only even prime: ____","fill","Answer = ____"),
        q("Smallest prime number: ____","fill","Answer = ____"),
        q("Is 1 prime? Explain.","fill","Answer = ____"),
        q("All primes between 20 and 30: ____","fill","Answer = ____"),
        q("Is sum of two primes always prime? Example: ____","fill","Answer = ____"),
        q("Twin primes differ by 2. Find a pair: ____","fill","Answer = ____"),
        q("Is 49 prime?","fill","Answer = ____"),
        q("How many primes between 10 and 20?","fill","Answer = ____")]
    s2=_qs("Prime Numbers",["sieve of Eratosthenes","prime factorisation intro","primes in context"],"Primes<30: 2,3,5,7,11,13,17,19,23,29",2)
    s3=_qs("Prime Numbers",["quick identification","factor trees","prime vs composite"],"97: not divisible by 2,3,5,7 → prime",3)
    s4=_qs("Prime Numbers Mastery",["Goldbach conjecture idea","prime gaps","multi-step"],"Every even number>2 is sum of 2 primes: 8=3+5",4)
    return [s1,s2,s3,s4][s-1]

def L2F(s): return _qs("Composite Numbers",["composite = more than 2 factors","list factor pairs","prime vs composite"],"12: factors 1,2,3,4,6,12 → composite",s)
def L2G(s): return _qs("Prime Identification",["quick test","factor pairs","verify prime/composite"],"97: not divisible by 2,3,5,7 → prime",s)
def L2H(s): return _qs("Prime Factor Ideas",["factor trees","prime factorisation","write in index form"],"12=2²×3; 60=2²×3×5",s)
def L2I(s): return _qs("Mixed Classification",["even/odd/prime/composite","multi-category sorting","apply all rules"],"15:odd,composite; 17:odd,prime; 4:even,composite; 2:even,prime",s)
def L2J(s): return _qs("Number Puzzles L2",["clues to find numbers","multi-condition","logic reasoning"],"I am prime, between 10 and 20, digits sum to 8. I am 17.",s)
def L2CUM1(s): return _cum(["Even numbers","Odd numbers","Even/Odd identification"],s)
def L2CUM2(s): return _cum(["Even/Odd Patterns","Prime numbers","Composite numbers"],s)
def L2CUM3(s): return _cum(["Prime identification","Prime factor ideas","Mixed classification"],s)
def L2REV(s):  return _qs("Level 2 Revision",["even/odd","prime/composite","patterns and puzzles"],"2:even,prime; 9:odd,composite; 15:odd,composite",s)

# ═══ LEVEL 3 ═══
def L3A(s):
    s1=[cb("What is Addition?",["Adding = putting two groups TOGETHER.","Use + sign. Answer = SUM.","Order doesn't matter: 3+4=4+3=7."],"3 apples + 4 apples = 7 apples"),
        q("Count dots: 3 + 2 = ____","diagram","Sum = ____","",diag="dot_addition",dpar={"a":3,"b":2}),
        q("Count the dots.","diagram","Sum = ____","",diag="dot_addition",dpar={"a":4,"b":3}),
        q("2 + 3 = ____","fill","Answer = ____"),
        q("4 + 4 = ____","fill","Answer = ____"),
        q("5 + 1 = ____","fill","Answer = ____"),
        cb("Number line addition",["Start at first number.","Jump RIGHT by the second number.","Where you land = the sum."],"4+3: start 4, jump 3 right → 7"),
        q("3 + 5 = ____","diagram","Answer = ____","",diag="number_line",dpar={"start":0,"end":10,"divisions":10,"hop_from":3,"hop_by":5}),
        q("6 + 2 = ____","fill","Answer = ____"),
        q("7 + 1 = ____","fill","Answer = ____"),
        q("0 + 8 = ____","fill","Answer = ____"),
        q("9 + 0 = ____","fill","Answer = ____"),
        cb("Doubles",["Double = adding a number to itself.","Double 3=3+3=6."],"Double 4=4+4=8"),
        q("Double 2 = ____","fill","Answer = ____"),
        q("Double 5 = ____","fill","Answer = ____"),
        q("Double 7 = ____","fill","Answer = ____"),
        q("4 red + 5 blue marbles. Total = ____","word","Total = ____","4 red and 5 blue"),
        q("3 biscuits morning + 6 evening. Total = ____","word","Total = ____","3 morning 6 evening"),
        q("7 + ___ = 9","fill","Missing = ____"),
        q("___ + 4 = 8","fill","Missing = ____"),
        q("1 + 2 + 3 = ____","fill","Answer = ____")]
    s2=_qs("Addition single digit",["column addition","carry concept intro","fact families"],"7+8=15; 8+7=15; 15-7=8; 15-8=7",2)
    s3=_qs("Addition single digit",["speed addition","word problems","missing addend"],"Find missing: __+6=13 → 7",3)
    s4=_qs("Addition Mastery",["multi-addend","error analysis","apply in context"],"3+4+5+6=18; check by reversing",4)
    return [s1,s2,s3,s4][s-1]

def L3B(s):
    s1=[cb("Adding Two-Digit Numbers",["Add ones first, then tens.","If ones > 9, carry 1 to tens.","Line up digits carefully."],"34+25: ones 4+5=9, tens 3+2=5 → 59"),
        q("23 + 14 = ____","fill","Answer = ____"),
        q("31 + 25 = ____","fill","Answer = ____"),
        q("40 + 37 = ____","fill","Answer = ____"),
        q("52 + 16 = ____","fill","Answer = ____"),
        q("11 + 88 = ____","fill","Answer = ____"),
        cb("Addition with carrying",["7+5=12: write 2, carry 1 to tens.","Carry = the extra ten."],"28+35: ones 8+5=13 write 3 carry 1; tens 2+3+1=6 → 63"),
        q("17 + 15 = ____","fill","Answer = ____"),
        q("28 + 34 = ____","fill","Answer = ____"),
        q("46 + 27 = ____","fill","Answer = ____"),
        q("55 + 38 = ____","fill","Answer = ____"),
        q("67 + 24 = ____","fill","Answer = ____"),
        cb("Word problems",["total/altogether/in all = add.","Write the addition sentence first."],"Ravi has 23 pencils, gets 14 more → 23+14=37"),
        q("35 books + 24 more = ____","word","Total = ____","35 and 24"),
        q("Class A: 28 students. Class B: 34. Together = ____","word","Together = ____","28 and 34"),
        q("Tree A: 46 mangoes. Tree B: 37. Total = ____","word","Total = ____","46 and 37"),
        q("52 m + 29 m = ____","word","Total = ____","52 m and 29 m"),
        q("Find missing: 34 + ___ = 60","fill","Missing = ____"),
        q("Find missing: ___ + 47 = 83","fill","Missing = ____"),
        q("Is 48+35 = 35+48?","fill","Answer = ____"),
        q("21 + 33 + 15 = ____","fill","Answer = ____")]
    s2=_qs("Addition two-digit",["column method","carry","check by reversing"],"67+45=112; verify: 112-45=67",2)
    s3=_qs("Addition two-digit",["3-digit addition","word problems","multi-step"],"234+156=390",3)
    s4=_qs("Addition Mastery L3B",["multi-step","error analysis","real world"],"Total distance = sum of all stages",4)
    return [s1,s2,s3,s4][s-1]

def L3C(s):
    s1=[cb("What is Subtraction?",["Subtraction = taking away.","Use − sign. Answer = DIFFERENCE.","5−3=2 means remove 3 from 5."],"8 apples − 3 eaten = 5 left"),
        q("9 − 4 = ____","fill","Answer = ____"),
        q("7 − 2 = ____","fill","Answer = ____"),
        q("10 − 6 = ____","fill","Answer = ____"),
        q("5 − 5 = ____","fill","Answer = ____"),
        q("8 − 0 = ____","fill","Answer = ____"),
        cb("Number line subtraction",["Start at the first number.","Jump LEFT by the second number."],"9−4: start 9, jump 4 left → 5"),
        q("8 − 3 = ____","diagram","Answer = ____","",diag="number_line",dpar={"start":0,"end":10,"divisions":10,"hop_from":8,"hop_by":-3}),
        q("12 − 5 = ____","fill","Answer = ____"),
        q("15 − 7 = ____","fill","Answer = ____"),
        q("11 − 4 = ____","fill","Answer = ____"),
        q("20 − 8 = ____","fill","Answer = ____"),
        cb("Fact Families",["Addition and subtraction are linked.","If 6+4=10, then 10−6=4 and 10−4=6."],"7+5=12; so 12−7=5 and 12−5=7"),
        q("If 8+6=14, then 14−8=____","fill","Answer = ____"),
        q("If 9+7=16, then 16−9=____","fill","Answer = ____"),
        q("12 − ___ = 5","fill","Missing = ____"),
        q("___ − 6 = 8","fill","Missing = ____"),
        q("15 sweets, gives away 7. Left = ____","word","Left = ____","15 and 7"),
        q("18 marbles, lost 9. Left = ____","word","Left = ____","18 and 9"),
        q("10 − 3 − 4 = ____","fill","Answer = ____"),
        q("What must be added to 7 to get 12?","fill","Answer = ____")]
    s2=_qs("Subtraction basics",["two-digit","word problems","missing number"],"52−28=24; check: 24+28=52",2)
    s3=_qs("Subtraction",["3-digit","borrow intro","multi-step word problems"],"300−147: borrow twice",3)
    s4=_qs("Subtraction Mastery",["multi-step","error analysis","real world"],"Change = price − amount paid",4)
    return [s1,s2,s3,s4][s-1]

def L3D(s): return _qs("Subtraction with borrowing",["borrow from tens","multi-step","verify by adding"],"72−45: borrow 1 ten → 12−5=7, 6−4=2 → 27",s)
def L3E(s): return _qs("Addition and Subtraction mixed",["choose the correct operation","fact families","inverse operations"],"total→add; difference→subtract; check with inverse",s)
def L3F(s): return _qs("Word problems add/subtract",["key words","write equation","solve and check"],"altogether→add; left→subtract; more than→compare",s)
def L3G(s): return _qs("Speed addition",["mental maths","bonds to 10 20 100","rapid recall"],"8+2=10; 15+5=20; 95+5=100",s)
def L3H(s): return _qs("Speed subtraction",["mental subtraction","near multiples of 10","rapid recall"],"30−8=22; 50−15=35; 100−37=63",s)
def L3I(s): return _qs("Puzzle operations",["magic squares","number trails","logic puzzles"],"Magic square: rows/cols/diagonals all sum to same number",s)
def L3J(s): return _qs("Mixed challenge add/subtract",["multi-step","error analysis","real world"],"Total=A+B; Difference=A−B; Change=final−initial",s)
def L3CUM1(s): return _cum(["Addition single digit","Addition two digit","Subtraction basics"],s)
def L3CUM2(s): return _cum(["Borrow subtraction","Addition and Subtraction mixed","Word problems add/subtract"],s)
def L3CUM3(s): return _cum(["Speed addition","Speed subtraction","Puzzle operations"],s)
def L3REV(s):  return _qs("Level 3 Revision",["all addition","all subtraction","word problems"],"Check: sum−addend=other addend",s)

# ═══ LEVEL 4 ═══
def L4A(s):
    s1=[cb("What is Multiplication?",["Multiplication = REPEATED ADDITION.","3×4=3+3+3+3=12. Answer=PRODUCT.","Order doesn't matter: 3×4=4×3."],"2×5=2+2+2+2+2=10"),
        q("Show 2×3 as an array.","diagram","Product = ____","",diag="array_diagram",dpar={"rows":2,"cols":3}),
        q("Show 3×4 as an array.","diagram","Product = ____","",diag="array_diagram",dpar={"rows":3,"cols":4}),
        q("2+2+2 = 3 × ___ = ____","fill","Answer = ____"),
        q("4+4+4+4 = 4 × ___ = ____","fill","Answer = ____"),
        q("5+5 = 2 × ___ = ____","fill","Answer = ____"),
        cb("Reading multiplication",["3×4 = three groups of 4.","3×4=4×3=12 (commutative).","PRODUCT = the answer."],"2×6=6×2=12"),
        q("Write 5×3 as repeated addition: ____","fill","Answer = ____"),
        q("Write 4×2 as repeated addition: ____","fill","Answer = ____"),
        q("3×3 = ____","fill","Answer = ____"),
        q("2×7 = ____","fill","Answer = ____"),
        q("4×2 = ____","fill","Answer = ____"),
        cb("Multiplication in real life",["groups × size = total.","4 boxes × 3 = 12 items."],"5 bags × 2 oranges = 10 oranges"),
        q("5 bags, 2 oranges each. Total = ____","word","Total = ____","5 bags 2 oranges"),
        q("3 rows, 4 chairs each. Total = ____","word","Total = ____","3 rows 4 chairs"),
        q("Is 2×5=5×2? Prove: ____","fill","Answer = ____"),
        q("1 × 9 = ____","fill","Answer = ____"),
        q("0 × 7 = ____","fill","Answer = ____"),
        q("___ × 3 = 9","fill","Missing = ____"),
        q("4 × ___ = 8","fill","Missing = ____"),
        q("Write a multiplication fact that equals 12: ____","fill","Answer = ____")]
    s2=_qs("Multiplication concept",["formal notation","commutative law","zero and one rules"],"n×1=n; n×0=0; n×m=m×n",2)
    s3=_qs("Multiplication concept",["apply tables","word problems","missing factor"],"_×7=42→6; 8×_=56→7",3)
    s4=_qs("Multiplication Mastery",["multi-step","error analysis","real world context"],"Total cost=price×quantity; area=length×width",4)
    return [s1,s2,s3,s4][s-1]

def L4B(s): return _qs("Tables 2-5",["x2 table through x5","recall and apply","mixed table questions"],"5×4=20; 3×6=18; 4×7=28; 2×9=18",s)
def L4C(s): return _qs("Tables 6-10",["x6 through x10","tricky products","relate to known facts"],"7×8=56; 9×6=54; 8×7=56; 6×9=54",s)
def L4D(s): return _qs("Multiplication practice",["mixed tables","word problems","missing factor"],"_×7=42→6; 8×_=56→7",s)
def L4E(s): return _qs("Multi-digit multiplication",["2-digit x 1-digit","column method","estimate first"],"23×4: 20×4=80, 3×4=12 → 92",s)
def L4F(s): return _qs("Multiplication word problems",["identify groups and size","write equation","multi-step"],"6 packets × 8 biscuits = 48 biscuits",s)
def L4G(s): return _qs("Multiplication patterns",["multiples","square numbers","doubling pattern"],"Multiples of 6: 6,12,18,24,30…",s)
def L4H(s): return _qs("Speed multiplication",["rapid recall","mental tricks","doubles and halves"],"x9 trick: 9×7=63 (digits sum to 9)",s)
def L4I(s): return _qs("Puzzle multiplication",["magic squares","factor puzzles","logic"],"Find a×b=36, a+b=13 → a=9, b=4",s)
def L4J(s): return _qs("Mixed challenge multiplication",["multi-step","error analysis","real world"],"Total cost=price×quantity",s)
def L4CUM1(s): return _cum(["Multiplication concept","Tables 2-5","Tables 6-10"],s)
def L4CUM2(s): return _cum(["Multiplication practice","Multi-digit multiplication","Multiplication word problems"],s)
def L4CUM3(s): return _cum(["Multiplication patterns","Speed multiplication","Puzzle multiplication"],s)
def L4REV(s):  return _qs("Level 4 Revision",["all tables","multi-digit","word problems"],"6×7=42; 23×4=92; 5 packs×6=30",s)

# ═══ LEVEL 5 ═══
def L5A(s):
    s1=[cb("What is Division?",["Division = sharing equally or making equal groups.","12÷3 = share 12 into 3 groups.","Answer = QUOTIENT."],"15÷5=3 (15 shared into 5 groups of 3)"),
        q("8 dots into 2 equal groups. Each = ____","diagram","Each group = ____","",diag="dot_array",dpar={"rows":2,"cols":4}),
        q("8 ÷ 2 = ____","fill","Answer = ____"),
        q("6 ÷ 3 = ____","fill","Answer = ____"),
        q("10 ÷ 5 = ____","fill","Answer = ____"),
        q("9 ÷ 3 = ____","fill","Answer = ____"),
        cb("Division and Multiplication",["If 3×4=12, then 12÷3=4 and 12÷4=3.","FACT FAMILY: x and ÷ are inverses."],"2×5=10; 5×2=10; 10÷2=5; 10÷5=2"),
        q("If 4×3=12, then 12÷4=____","fill","Answer = ____"),
        q("If 5×6=30, then 30÷6=____","fill","Answer = ____"),
        q("14 ÷ 7 = ____","fill","Answer = ____"),
        q("16 ÷ 4 = ____","fill","Answer = ____"),
        q("20 ÷ 5 = ____","fill","Answer = ____"),
        cb("Division in real life",["Divide total by number of groups → size each.","Check: quotient × divisor = dividend."],"24÷4=6. Check: 6×4=24"),
        q("24 pencils among 4 students. Each gets ____","word","Each = ____","24 and 4"),
        q("30 chairs in 5 equal rows. Each row = ____","word","Each row = ____","30 and 5"),
        q("Any number ÷ 1 = ____","fill","Answer = ____"),
        q("Any number ÷ itself = ____","fill","Answer = ____"),
        q("15 ÷ ___ = 3","fill","Missing = ____"),
        q("___ ÷ 4 = 5","fill","Missing = ____"),
        q("Is 9÷3 = 3÷9? Explain.","fill","Answer = ____"),
        q("Write a division fact that equals 4: ____","fill","Answer = ____")]
    s2=_qs("Division concept",["formal notation","link to multiplication","zero division rule"],"n÷1=n; 0÷n=0; n÷0=undefined",2)
    s3=_qs("Division single digit",["quick recall","related multiplication","word problems"],"56÷8=7; 72÷9=8; 45÷5=9",3)
    s4=_qs("Division Mastery",["multi-step","error analysis","real world"],"Cost per item=total÷quantity",4)
    return [s1,s2,s3,s4][s-1]

def L5B(s): return _qs("Division single digit",["quick recall","related multiplication","dividend÷divisor=quotient"],"56÷8=7; 72÷9=8; 45÷5=9",s)
def L5C(s): return _qs("Division with remainder",["r = what is left over","dividend=quotient×divisor+remainder","check your answer"],"17÷5=3 remainder 2; check:3×5+2=17",s)
def L5D(s): return _qs("Long division",["estimate quotient","subtract step by step","bring down digits"],"96÷8: 8×12=96 → quotient=12",s)
def L5E(s): return _qs("Division word problems",["sharing equally","grouping","multi-step"],"72 cookies, 9 per box → 72÷9=8 boxes",s)
def L5F(s): return _qs("Multiplication and division mixed",["choose operation","inverse relationship","fact families"],"total→multiply; per item→divide",s)
def L5G(s): return _qs("Missing numbers division",["find dividend or divisor","inverse operations","multi-step"],"_÷6=7→42; 54÷_=6→9",s)
def L5H(s): return _qs("Speed division",["mental division","halving","divisibility rules"],"Div by 2:even; by 5:ends 0 or 5; by 10:ends 0",s)
def L5I(s): return _qs("Puzzle division",["logic puzzles","factor pairs","multi-condition"],"I am divided by 7, quotient is 8. I am 56.",s)
def L5J(s): return _qs("Mixed challenge division",["multi-step","real world","combine x and div"],"Cost per item=total÷quantity",s)
def L5CUM1(s): return _cum(["Division concept","Division single digit","Division with remainder"],s)
def L5CUM2(s): return _cum(["Long division","Division word problems","Multiplication and division mixed"],s)
def L5CUM3(s): return _cum(["Missing numbers","Speed division","Puzzle division"],s)
def L5REV(s):  return _qs("Level 5 Revision",["all division types","remainders","word problems"],"72÷8=9; 50÷7=7r1; 96÷4=24",s)

# ═══ LEVEL 6 ═══
def L6A(s):
    s1=[cb("What is a Fraction?",["A fraction shows EQUAL PARTS of a whole.","Numerator (top): parts we have.","Denominator (bottom): total equal parts."],"Pizza 4 equal slices, Ravi eats 1 → 1/4"),
        q("1 out of 4 shaded.","diagram","Fraction = ____","",diag="fraction_bar",dpar={"total":4,"shaded":1}),
        q("3 out of 6 shaded.","diagram","Fraction = ____","",diag="fraction_bar",dpar={"total":6,"shaded":3}),
        q("What fraction shaded?","diagram","Fraction = ____","",diag="fraction_circle",dpar={"total":5,"shaded":2}),
        q("2 out of 7 equal parts: ____","fill","Fraction = ____"),
        q("5 out of 8 equal parts: ____","fill","Fraction = ____"),
        cb("Numerator and Denominator",["NUMERATOR=top (parts we have).","DENOMINATOR=bottom (total parts).","In 4/9: N=4, D=9."],"In 3/8: top=3, bottom=8"),
        q("In 5/7: N=___ D=___","fill","N=____ D=____"),
        q("In 2/9: N=___ D=___","fill","N=____ D=____"),
        q("Fraction with N=3, D=10: ____","fill","Answer = ____"),
        q("The denominator tells us: ____","fill","Answer = ____"),
        q("1 out of 4 = ____","fill","Answer = ____"),
        cb("Fractions as out of",["1 out of 4 = 1/4.","Fraction bar means out of.","D = total equal parts always."],"3 out of 8 → 3/8"),
        q("3 out of 5 = ____","fill","Answer = ____"),
        q("4 out of 7 = ____","fill","Answer = ____"),
        q("Ravi ate 2 of 5 pizza slices. Fraction = ____","word","Fraction = ____","2 of 5 slices"),
        q("3 of 8 chocolates are dark. Fraction = ____","word","Fraction = ____","3 of 8"),
        q("In 4/7, denominator = ____","fill","Answer = ____"),
        q("In 6/9, numerator = ____","fill","Answer = ____"),
        q("5 of 12 marbles are red. Fraction = ____","word","Fraction = ____","5 of 12"),
        q("Draw and shade a fraction bar for 3/5.","fill","Done = ____")]
    s2=_qs("Fractions concept",["unit fractions","whole=n/n","fractions on number line"],"1/2,1/3,1/4 are unit fractions; 4/4=1 whole",2)
    s3=_qs("Fractions concept",["identify and write","compare unit fractions","fraction of a quantity"],"1/4 of 20=5; 2/3 of 18=12",3)
    s4=_qs("Fractions Mastery",["all types","operations","word problems"],"Compare: 3/5 vs 2/3; 1/4+3/8=5/8",4)
    return [s1,s2,s3,s4][s-1]

def L6B(s): return _qs("Proper and improper fractions",["proper:N<D","improper:N>=D","mixed numbers:1 and 2/3"],"3/4 proper; 7/4 improper=1 and 3/4",s)
def L6C(s): return _qs("Equivalent fractions",["multiply/divide N and D by same number","simplest form","fraction wall"],"1/2=2/4=3/6=4/8 all equivalent",s)
def L6D(s): return _qs("Fraction comparison",["same D:compare N","different D:find LCD","use < > ="],"3/4>2/4; 1/3 vs 1/4: 4/12 vs 3/12 → 1/3>1/4",s)
def L6E(s): return _qs("Fraction addition",["same D:add N","different D:find LCD","simplify result"],"1/4+2/4=3/4; 1/3+1/6=2/6+1/6=3/6=1/2",s)
def L6F(s): return _qs("Fraction subtraction",["same D:subtract N","different D:find LCD","check result"],"5/6-1/6=4/6=2/3; 3/4-1/3=9/12-4/12=5/12",s)
def L6G(s): return _qs("Fraction word problems",["of a quantity","sharing equally","multi-step"],"1/4 of 20=5; 2/3 of 18=12",s)
def L6H(s): return _qs("Mixed fractions",["convert improper to mixed","add/subtract mixed","real world"],"2+3/5=13/5; 7/3=2 and 1/3",s)
def L6I(s): return _qs("Fraction puzzles",["logic with fractions","find the whole","fraction chains"],"1/4 of a number=7 → number=28",s)
def L6J(s): return _qs("Mixed challenge fractions",["all operations","order multiple fractions","multi-step word problems"],"Order: 2/3,3/4,5/8,7/12 → LCD=24",s)
def L6CUM1(s): return _cum(["Fraction concept","Proper/improper fractions","Equivalent fractions"],s)
def L6CUM2(s): return _cum(["Fraction comparison","Fraction addition","Fraction subtraction"],s)
def L6CUM3(s): return _cum(["Fraction word problems","Mixed fractions","Fraction puzzles"],s)
def L6REV(s):  return _qs("Level 6 Revision",["all fraction types","operations","word problems"],"Compare:3/5 vs 2/3; Add:1/4+3/8=5/8",s)

# ═══ LEVEL 7 — DECIMALS ═══
def L7A(s):
    if s==1: return [
        cb("You already know about parts!",["Look at a pizza: 10 equal slices, each=ONE PART.","Count how many parts are taken.","This is the beginning of decimals!"],"Pizza 10 slices, Ravi eats 3 → 3 parts out of 10"),
        q("Strip: 3 squares shaded out of 10. Shaded = ____","diagram","Shaded = ____","3 squares",diag="tenths_grid",dpar={"shaded":3,"total":10}),
        q("Strip: how many squares shaded?","diagram","Shaded = ____","",diag="tenths_grid",dpar={"shaded":7,"total":10}),
        q("Strip: how many squares shaded?","diagram","Shaded = ____","",diag="tenths_grid",dpar={"shaded":1,"total":10}),
        q("Strip: how many squares NOT shaded?","diagram","Unshaded = ____","",diag="tenths_grid",dpar={"shaded":4,"total":10}),
        q("Strip: how many squares NOT shaded?","diagram","Unshaded = ____","",diag="tenths_grid",dpar={"shaded":8,"total":10}),
        cb("Counting parts — getting closer to decimals",["10 equal parts: each=1 TENTH.","3 parts out of 10 = 3 tenths.","We write 3 tenths as 0.3"],"7 parts out of 10 → 7 tenths → 0.7"),
        q("5 squares shaded. 5 tenths = 0.____","diagram","5 tenths = 0.____","5 squares",diag="tenths_grid",dpar={"shaded":5,"total":10}),
        q("2 squares shaded. 2 tenths = 0.____","diagram","2 tenths = 0.____","",diag="tenths_grid",dpar={"shaded":2,"total":10}),
        q("9 squares shaded. 9 tenths = 0.____","diagram","9 tenths = 0.____","",diag="tenths_grid",dpar={"shaded":9,"total":10}),
        q("6 squares shaded. 6 tenths = 0.____","diagram","6 tenths = 0.____","",diag="tenths_grid",dpar={"shaded":6,"total":10}),
        cb("The decimal point",["The dot = DECIMAL POINT.","Before the dot = whole numbers.","After the dot = parts (tenths, hundredths)"],"0.3 means 0 wholes, 3 tenths. 1.5 means 1 whole, 5 tenths"),
        q("0.4 means ____ whole and ____ tenths","fill","Whole=____ Tenths=____"),
        q("0.8 means ____ whole and ____ tenths","fill","Whole=____ Tenths=____"),
        q("1.3 means ____ whole and ____ tenths","fill","Whole=____ Tenths=____"),
        q("2.5 means ____ wholes and ____ tenths","fill","Wholes=____ Tenths=____"),
        q("Water bottle: 6 of 10 marks filled. Write as decimal.","word","Decimal = ____","6 out of 10"),
        q("Meena ate 3 of 10 chocolate pieces. Decimal?","word","Decimal = ____","3 of 10"),
        q("4 squares shaded. Write as decimal: 0.____","diagram","Answer = 0.____","4 squares",diag="tenths_grid",dpar={"shaded":4,"total":10}),
        q("zero point three = ____ and zero point eight = ____","fill","Answers = ____")]
    if s==2: return [
        cb("Writing decimals formally",["Tenths: 1 digit after decimal. 0.3=3 tenths.","Hundredths: 2 digits. 0.35=35 hundredths.","Decimal point separates whole from parts."],"2.47: ones=2, tenths=4, hundredths=7"),
        q("Write decimal for 6 tenths","fill","Answer = 0.____"),
        q("Write decimal for 3 tenths and 5 hundredths","fill","Answer = 0.____"),
        q("In 4.7, digit after decimal is in ____ place","fill","Answer = ____"),
        q("In 3.25, digit 2 is in ____ place","fill","Answer = ____"),
        q("In 6.08, digit 8 is in ____ place","fill","Answer = ____"),
        cb("Place value chart for decimals",["Ones | . | Tenths | Hundredths","Each place 10x smaller than place to its left.","0.1=1 tenth; 0.01=1 hundredth."],"3.47: Ones=3, Tenths=4, Hundredths=7"),
        q("Show 2.5 in place value chart.","diagram","Ones=____ Tenths=____","",diag="place_value_chart",dpar={"number":"2.5"}),
        q("Show 0.83 in place value chart.","diagram","Tenths=____ Hundredths=____","",diag="place_value_chart",dpar={"number":"0.83"}),
        q("3.46 expanded: 3 + 0.___ + 0.0___","fill","Answer = ____"),
        q("0.75 expanded: 0 + 0.___ + 0.0___","fill","Answer = ____"),
        cb("Reading decimals",["Read whole, say point, then each digit.","1.4 = one point four. 0.35 = zero point three five."],"2.08 = two point zero eight"),
        q("Write 0.9 in words","fill","Answer = ____"),
        q("Write 1.5 in words","fill","Answer = ____"),
        q("three point seven as decimal","fill","Answer = ____"),
        q("zero point four five as decimal","fill","Answer = ____"),
        q("Pencil is 0.15 m. How many hundredths?","word","Answer = ____ hundredths","0.15 m"),
        q("Value of digit 3 in 5.37","fill","Value = ____"),
        q("Value of digit 6 in 4.06","fill","Value = ____"),
        q("Write 7/10 as a decimal","fill","Decimal = 0.____"),
        q("Write 23/100 as a decimal","fill","Decimal = 0.____")]
    if s==3: return [
        cb("Quick Review",["Tenths: 1st digit after decimal.","Hundredths: 2nd digit after decimal.","Expanded: 2.46=2+0.4+0.06"],"5.39=5+0.3+0.09"),
        q("Value of 4 in 3.47","fill","Value = ____"),
        q("Value of 9 in 2.09","fill","Value = ____"),
        q("Write 4.28 in expanded form","fill","Answer = ____"),
        q("3 + 0.5 + 0.02 = ____","fill","Answer = ____"),
        q("How many tenths in 0.8?","fill","Answer = ____ tenths"),
        cb("Hundredths grid",["100 squares=1 whole.","Shaded/100=decimal.","63 shaded=0.63"],"45 shaded=0.45"),
        q("How many shaded? Write decimal.","diagram","Decimal = ____","",diag="hundredths_grid",dpar={"shaded":35}),
        q("How many shaded? Write decimal.","diagram","Decimal = ____","",diag="hundredths_grid",dpar={"shaded":72}),
        q("0.56 as fraction with D=100","fill","Fraction = ____/100"),
        q("48/100 as decimal","fill","Decimal = ____"),
        q("Three decimals between 0.1 and 0.2","fill","Answer = ____"),
        cb("Rounding decimals",["Round to nearest tenth: look at hundredths.",">=5: round up; <5: keep same.","2.46 → 2.5 (since 6>=5)"],"3.74 → 3.7 (since 4<5)"),
        q("Round 4.35 to nearest tenth","fill","Answer = ____"),
        q("Round 2.78 to nearest tenth","fill","Answer = ____"),
        q("Round 0.94 to nearest tenth","fill","Answer = ____"),
        q("Round 6.45 to nearest whole number","fill","Answer = ____"),
        q("Ravi height 1.47 m. Round to nearest tenth.","word","Answer = ____ m","1.47 m"),
        q("Distance 3.82 km. Round to nearest whole number.","word","Answer = ____ km","3.82 km"),
        q("A decimal that rounds to 0.5: ____","fill","Answer = ____"),
        q("True or False: 0.30 = 0.3","fill","Answer = ____")]
    return [
        cb("Comparing and Ordering Decimals",["Align decimal points. Compare left to right.","Add zeros for equal decimal places.","0.40 vs 0.38 → 0.40>0.38"],"0.4>0.38"),
        q("0.6 ___ 0.60","fill","< > or = ____"),
        q("0.09 ___ 0.9","fill","< > or = ____"),
        q("1.25 ___ 1.52","fill","< > or = ____"),
        q("3.4 ___ 3.40","fill","< > or = ____"),
        q("Order small to large: 1.2, 1.02, 1.22, 1.21","fill","Answer = ____"),
        q("Order large to small: 0.5, 0.55, 0.505, 0.05","fill","Answer = ____"),
        cb("Multiply and divide by 10",["x10: move decimal one place RIGHT.","div10: move decimal one place LEFT.","0.4x10=4; 3.5 div 10=0.35"],"0.7x10=7; 7 div 10=0.7"),
        q("0.6 x 10 = ____","fill","Answer = ____"),
        q("3.5 div 10 = ____","fill","Answer = ____"),
        q("10 x 0.08 = ____","fill","Answer = ____"),
        q("Halfway between 0.4 and 0.6?","fill","Answer = ____"),
        q("All 2-decimal-place decimals between 1.5 and 1.6","fill","Answer = ____"),
        cb("Spot the mistake!",["Read carefully. Find the error. Correct it."],"0.9<0.18 because 18>9 is WRONG: 0.9=0.90>0.18"),
        q("4 in 6.45 is worth 4 ones. Correct value: ____","fill","Correct = ____"),
        q("2.3>2.30 because 2.3 is shorter. True or False?","fill","Answer = ____"),
        q("Scored 8.75 in Test A, 8.7 in Test B. Higher? By how much?","word","Answer = ____","8.75 and 8.7"),
        q("Weights 0.5 kg, 0.05 kg, 0.505 kg. Order lightest to heaviest.","word","Answer = ____","0.5 kg 0.05 kg 0.505 kg"),
        q("A decimal between 0.001 and 0.002: ____","fill","Answer = ____"),
        q("0.1 + ___ = 1","fill","Answer = ____"),
        q("Value of digit 8 in 7.384","fill","Value = ____")]

def L7B(s): return _qs("Decimal place value",["ones/tenths/hundredths/thousandths","read and write","expand and compress"],"3.456: ones=3,tenths=4,hundredths=5,thousandths=6",s)
def L7C(s): return _qs("Decimal comparison",["align decimals","compare digit by digit","order a list"],"0.7>0.69; 1.30=1.3; order:0.4,0.41,0.5",s)
def L7D(s): return _qs("Decimal addition",["column addition","align decimal points","carry in decimals"],"2.35+1.47=3.82; align the decimal points",s)
def L7E(s): return _qs("Decimal subtraction",["column subtraction","borrow across decimal","check with addition"],"4.72-1.85=2.87; check:2.87+1.85=4.72",s)
def L7F(s): return _qs("Fraction to decimal",["divide numerator by denominator","common fractions","recurring decimals"],"1/4=0.25; 1/3=0.333; 3/8=0.375",s)
def L7G(s): return _qs("Decimal word problems",["money","measurement","multi-step"],"Rs 12.50+Rs 8.75=Rs 21.25",s)
def L7H(s): return _qs("Mixed decimals",["all operations","order of operations","mixed contexts"],"Perimeter=2.4+3.5+2.4+3.5=11.8 cm",s)
def L7I(s): return _qs("Decimal puzzles",["find the decimal","multi-condition","logic"],"I have 2 decimal places, between 1.2 and 1.3, hundredths=5. I am 1.25.",s)
def L7J(s): return _qs("Mixed challenge decimals",["multi-step","error analysis","real world"],"Budget Rs 50: spent 12.75+18.40=31.15; change=18.85",s)
def L7CUM1(s): return _cum(["Decimal concept","Decimal place value","Decimal comparison"],s)
def L7CUM2(s): return _cum(["Decimal addition","Decimal subtraction","Fraction to decimal"],s)
def L7CUM3(s): return _cum(["Decimal word problems","Mixed decimals","Decimal puzzles"],s)
def L7REV(s):  return _qs("Level 7 Revision",["all decimals","operations","word problems"],"0.75+0.36=1.11; 3.4>3.04; 7/20=0.35",s)

# ═══ LEVEL 8 — INTEGERS ═══
def L8A(s):
    if s==1: return [
        cb("What are Integers?",["Integers include negatives, zero, and positives.","Negative: -3,-2,-1 (below zero).","Positive: 1,2,3 (above zero). Zero: 0."],"Temperature -5 degrees C = 5 degrees BELOW zero"),
        q("5 degrees below zero = ____","fill","Answer = ____"),
        q("3 floors above ground = ____","fill","Answer = ____"),
        q("Rs 200 in debt = ____","fill","Answer = ____"),
        q("Sea level = ____","fill","Answer = ____"),
        q("10 metres underground = ____","fill","Answer = ____"),
        cb("Integers on the number line",["Negatives=LEFT of zero.","Positives=RIGHT of zero.","Further from 0 = larger absolute value."],"-3 is left of -1, so -3 < -1"),
        q("Mark -3 and +5 on number line.","diagram","Done","",diag="integer_line",dpar={"marks":[-3,5],"start":-6,"end":6}),
        q("Further from zero: -7 or +4?","fill","Answer = ____"),
        q("All integers between -4 and +3: ____","fill","Answer = ____"),
        q("Is -8 greater or less than -2?","fill","Answer = ____"),
        q("Opposite of -6: ____","fill","Answer = ____"),
        cb("Absolute value",["Absolute value = distance from 0. Always positive.","-5 has absolute value 5. +3 has absolute value 3.","Written with vertical bars: |n|"],"|(-8)| = 8"),
        q("|-7| = ____","fill","Answer = ____"),
        q("|+12| = ____","fill","Answer = ____"),
        q("|0| = ____","fill","Answer = ____"),
        q("Larger absolute value: -15 or +13?","fill","Answer = ____"),
        q("Diver at -30 m, bird at +12 m. Who is further from sea level?","word","Answer = ____","-30 m and +12 m"),
        q("Write 3 negative integers with absolute value > 5","fill","Answer = ____"),
        q("Temperature rose from -4 C to +6 C. By how many degrees?","word","Answer = ____ degrees","-4 and +6"),
        q("Order: -3, +1, -7, 0, +5 smallest to largest","fill","Answer = ____")]
    s2=_qs("Integer concept",["formal number line","compare integers","absolute value"],"-5<-3<0<2<7; |(-9)|=9=|9|",2)
    s3=_qs("Integer concept",["all four operations intro","word problems","multi-step"],"Temperature change; profit/loss; elevation",3)
    s4=_qs("Integer Mastery",["multi-step","error analysis","real world"],"Net change=sum of all gains and losses",4)
    return [s1,s2,s3,s4][s-1]

def L8B(s): return _qs("Integer number line",["plot integers","find distance","order and compare"],"Distance from -3 to +5 = 8 units",s)
def L8C(s): return _qs("Integer addition",["same sign:add keep sign","different sign:subtract keep larger sign","number line hops"],"-3+(-4)=-7; -3+7=+4; +5+(-8)=-3",s)
def L8D(s): return _qs("Integer subtraction",["a-b=a+(-b)","subtracting negative=adding positive","real world temperature"],"5-(-3)=5+3=8; -4-2=-6; -2-(-5)=3",s)
def L8E(s): return _qs("Integer multiplication",["pos x pos=pos","neg x neg=pos","pos x neg=neg"],"(-3)x(-4)=12; (-3)x4=-12; 3x4=12",s)
def L8F(s): return _qs("Integer division",["same sign=positive quotient","different sign=negative quotient","zero rules"],"(-12) div (-4)=3; 12 div (-4)=-3; 0 div (-5)=0",s)
def L8G(s): return _qs("Integer word problems",["temperature change","profit/loss","elevation"],"Profit +Rs200, Loss -Rs80 → Net=+Rs120",s)
def L8H(s): return _qs("Mixed integers",["all four operations","order of operations","multi-step"],"(-3)x4+(-2)x(-5)=-12+10=-2",s)
def L8I(s): return _qs("Integer puzzles",["find the integer","logic clues","multi-condition"],"I am negative. My square is 49. I am -7.",s)
def L8J(s): return _qs("Mixed challenge integers",["multi-step","real world","error analysis"],"Net change=sum of all signed quantities",s)
def L8CUM1(s): return _cum(["Integer concept","Integer number line","Integer addition"],s)
def L8CUM2(s): return _cum(["Integer subtraction","Integer multiplication","Integer division"],s)
def L8CUM3(s): return _cum(["Integer word problems","Mixed integers","Integer puzzles"],s)
def L8REV(s):  return _qs("Level 8 Revision",["all integer operations","word problems","multi-step"],"(-5)+8=3; (-3)x(-4)=12; |(-7)|=7",s)

# ═══ LEVELS 9-20 ═══
def L9A(s):  return _qs("Factors",["factor pairs of numbers","list all factors","factor is always <= the number"],"Factors of 24: 1,2,3,4,6,8,12,24",s)
def L9B(s):  return _qs("Multiples",["first 10 multiples","common multiples","multiples are infinite"],"Multiples of 7: 7,14,21,28,35,42,49,56,63,70",s)
def L9C(s):  return _qs("Prime factorisation",["factor tree method","index notation","every composite has unique prime factorisation"],"36=2 squared x 3 squared; 60=2 squared x 3 x 5",s)
def L9D(s):  return _qs("HCF",["list factors of each number","find the common factors","take the highest common factor"],"HCF(12,18): common factors 1,2,3,6 → HCF=6",s)
def L9E(s):  return _qs("LCM",["list multiples","find first common multiple","prime factorisation method"],"LCM(4,6): multiples of 4:4,8,12; of 6:6,12 → LCM=12",s)
def L9F(s):  return _qs("Factors and Multiples word problems",["tiles and floors","sharing equally","scheduling"],"Tiles 12cm and 18cm: LCM=36cm for same row length",s)
def L9G(s):  return _qs("Factors and Multiples applications",["divisibility rules","HCF for simplifying fractions","LCM for adding fractions"],"Simplify 18/24: HCF=6 → 3/4",s)
def L9H(s):  return _qs("Mixed factors and multiples",["HCF and LCM combined","multi-step","word problems"],"HCF(24,36)=12; LCM(24,36)=72; HCF x LCM=24 x 36",s)
def L9I(s):  return _qs("Factor and Multiple puzzles",["clue-based","find the number","logic"],"Between 20 and 30, multiple of 4, HCF with 24 is 4. I am 28.",s)
def L9J(s):  return _qs("Mixed challenge L9",["multi-step","real world","explain reasoning"],"LCM for scheduling; HCF for sharing",s)
def L9CUM1(s): return _cum(["Factors","Multiples","Prime factorisation"],s)
def L9CUM2(s): return _cum(["HCF","LCM","Factors and Multiples word problems"],s)
def L9CUM3(s): return _cum(["Factors and Multiples applications","Mixed factors and multiples","Factor and Multiple puzzles"],s)
def L9REV(s):  return _qs("Level 9 Revision",["factors","multiples","HCF and LCM"],"HCF(18,24)=6; LCM(8,12)=24",s)

def L10A(s): return _qs("Ratio concept",["ratio compares two quantities","write as a:b","ratio is not a fraction of a whole"],"Boys:Girls=3:5 means 3 boys for every 5 girls",s)
def L10B(s): return _qs("Simplifying ratios",["divide both by HCF","simplest form","equivalent ratios"],"12:18 → HCF=6 → 2:3",s)
def L10C(s): return _qs("Equivalent ratios",["multiply/divide both by same number","ratio tables","scaling"],"2:3=4:6=6:9=10:15",s)
def L10D(s): return _qs("Proportion",["two equal ratios","cross-multiplication","direct proportion"],"2/3=4/? → ?=6; cross: 2x?=3x4",s)
def L10E(s): return _qs("Solving proportions",["set up the proportion","cross-multiply","solve for unknown"],"5 books cost Rs 200, 8 books cost? → 5/200=8/x → x=320",s)
def L10F(s): return _qs("Ratio word problems",["share in a ratio","find part from total","increase/decrease in ratio"],"Share Rs 240 in ratio 3:5 → 8 parts; each part=30 → 90:150",s)
def L10G(s): return _qs("Direct proportion",["y=kx","both increase/decrease proportionally","unit rate method"],"Speed: 3hrs→180km, then 5hrs→300km",s)
def L10H(s): return _qs("Inverse proportion",["xy=k constant","one increases other decreases","workers and time"],"5 workers:12 days; 3 workers:5x12/3=20 days",s)
def L10I(s): return _qs("Mixed ratio and proportion",["all skills","multi-step","map scales"],"Map 1:50000; 3cm=1.5km",s)
def L10J(s): return _qs("Mixed challenge L10",["complex ratios","multi-step proportion","real world"],"Mixture, speed-distance-time, scaling recipes",s)
def L10CUM1(s): return _cum(["Ratio concept","Simplifying ratios","Equivalent ratios"],s)
def L10CUM2(s): return _cum(["Proportion","Solving proportions","Ratio word problems"],s)
def L10CUM3(s): return _cum(["Direct proportion","Inverse proportion","Mixed ratio and proportion"],s)
def L10REV(s):  return _qs("Level 10 Revision",["ratio","proportion","word problems"],"12:8=3:2; if 4:x=6:9 → x=6",s)

def L11A(s): return _qs("Variables and expressions",["variable=unknown quantity","expression=numbers+variables+operations","no equals sign in expression"],"3x+2; 5y-7; 2a+3b are expressions",s)
def L11B(s): return _qs("Algebraic expressions",["identify terms","coefficient and variable","constant term"],"In 4x squared+3x-7: terms are 4x squared,3x,-7; constant=-7",s)
def L11C(s): return _qs("Simplifying expressions",["collect like terms","add/subtract coefficients","cannot combine unlike terms"],"3x+5x=8x; 2x+3y+x=3x+3y",s)
def L11D(s): return _qs("Like and unlike terms",["like:same variable and power","unlike:different variable or power","only like terms can be combined"],"3x squared and 5x squared are like; 3x and 3x squared are unlike",s)
def L11E(s): return _qs("Substitution",["replace variable with given value","follow BODMAS","evaluate the expression"],"If x=3: 2x+5=2(3)+5=6+5=11",s)
def L11F(s): return _qs("Expression evaluation",["substitute multiple variables","complex expressions","check reasonableness"],"If a=2,b=-3: 3a squared-2b=3(4)-2(-3)=12+6=18",s)
def L11G(s): return _qs("Algebra word problems",["form expression from words","identify variable","multi-step"],"Ravi is 3 years older than Meena. Meena=x → Ravi=x+3",s)
def L11H(s): return _qs("Mixed expressions",["all operations","brackets","expand expressions"],"2(3x+4)=6x+8; 3(a-2b)=3a-6b",s)
def L11I(s): return _qs("Algebra puzzles",["find the value","consecutive numbers","logic algebra"],"Three consecutive even: n,n+2,n+4; sum=3n+6",s)
def L11J(s): return _qs("Mixed challenge algebra",["multi-step","real world formulas","error analysis"],"Perimeter=2(l+b); Area=lb; substitute values",s)
def L11CUM1(s): return _cum(["Variables and expressions","Algebraic expressions","Simplifying expressions"],s)
def L11CUM2(s): return _cum(["Like and unlike terms","Substitution","Expression evaluation"],s)
def L11CUM3(s): return _cum(["Algebra word problems","Mixed expressions","Algebra puzzles"],s)
def L11REV(s):  return _qs("Level 11 Revision",["expressions","substitution","simplification"],"3x+2y-x+y=2x+3y; if x=2,y=1: 4+3=7",s)

def L12A(s): return _qs("Equation concept",["equation has = sign","LHS=RHS when solution substituted","balance method: do same to both sides"],"2x+3=11 → x=4 (check:2x4+3=11)",s)
def L12B(s): return _qs("Solving linear equations",["isolate the variable","inverse operations","verify by substitution"],"3x-5=10 → 3x=15 → x=5",s)
def L12C(s): return _qs("Multi-step equations",["combine like terms first","expand brackets","solve step by step"],"2(x+3)=14 → 2x+6=14 → 2x=8 → x=4",s)
def L12D(s): return _qs("Equation word problems",["form equation from words","define variable","solve and interpret"],"Age now x; in 5 years: x+5=20 → x=15",s)
def L12E(s): return _qs("Equation applications",["distance=speed x time","simple interest","geometry formulas"],"If P+Pr/100=120 and r=20%: P=100",s)
def L12F(s): return _qs("Equation puzzles",["number puzzles","consecutive integers","angles"],"Sum of 3 consecutive integers=48 → n+(n+1)+(n+2)=48 → n=15",s)
def L12G(s): return _qs("Mixed equations",["all types","transpose method","check solutions"],"ax+b=cx+d → (a-c)x=d-b → x=(d-b)/(a-c)",s)
def L12H(s): return _qs("Speed equation solving",["mental methods","pattern recognition","spot solutions"],"2x=14→x=7; x+8=15→x=7; x/3=7→x=21",s)
def L12I(s): return _qs("Hard equation problems",["simultaneous ideas","complex word problems","multi-step"],"x+y=10, x-y=4 → add: 2x=14 → x=7, y=3",s)
def L12J(s): return _qs("Mixed challenge equations",["multi-step","real world","verify and interpret"],"Form, Solve, Verify, Interpret answer in context",s)
def L12CUM1(s): return _cum(["Equation concept","Solving linear equations","Multi-step equations"],s)
def L12CUM2(s): return _cum(["Equation word problems","Equation applications","Equation puzzles"],s)
def L12CUM3(s): return _cum(["Mixed equations","Speed equation solving","Hard equation problems"],s)
def L12REV(s):  return _qs("Level 12 Revision",["form and solve equations","word problems","verify"],"3x+7=22 → x=5; check:3(5)+7=22",s)

def L13A(s): return _qs("Powers and indices concept",["a to the n means a multiplied n times","base and exponent","square and cube numbers"],"2 cubed=2x2x2=8; 5 squared=25; 10 to the 4=10000",s)
def L13B(s): return _qs("Laws of indices",["a to m x a to n = a to m+n","a to m div a to n = a to m-n","(a to m) to n = a to mn"],"2 cubed x 2 squared=2 to the 5=32",s)
def L13C(s): return _qs("Simplification with indices",["apply laws","expand and simplify","mixed bases"],"x squared x x cubed=x to the 5; 4 cubed div 4=4 squared=16",s)
def L13D(s): return _qs("Negative indices",["a to -n = 1 divided by a to n","negative index means reciprocal","simplify expressions"],"2 to -3=1/8; 5 to -2=1/25",s)
def L13E(s): return _qs("Fractional indices",["a to 1/n = nth root of a","a to m/n = (nth root of a) to m","evaluate"],"27 to 1/3=3; 8 to 2/3=(cube root 8) squared=4",s)
def L13F(s): return _qs("Scientific notation",["a x 10 to n where 1<=a<10","large and small numbers","operations in scientific notation"],"3400000=3.4x10 to 6; 0.0052=5.2x10 to -3",s)
def L13G(s): return _qs("Powers word problems",["area and volume","population growth","compound interest"],"Bacteria doubles every hour: after 5hrs=2 to 5=32x original",s)
def L13H(s): return _qs("Mixed indices",["all laws combined","multi-step simplification","check by expansion"],"(3x squared y) squared=9x to 4 y squared",s)
def L13I(s): return _qs("Index puzzles",["find the index","find the base","logic with powers"],"2 to x=32 → x=5; x cubed=125 → x=5",s)
def L13J(s): return _qs("Mixed challenge indices",["multi-step","real world applications","error analysis"],"E=mc squared; scientific notation calculations",s)
def L13CUM1(s): return _cum(["Powers and indices concept","Laws of indices","Simplification with indices"],s)
def L13CUM2(s): return _cum(["Negative indices","Fractional indices","Scientific notation"],s)
def L13CUM3(s): return _cum(["Powers word problems","Mixed indices","Index puzzles"],s)
def L13REV(s):  return _qs("Level 13 Revision",["all index laws","scientific notation","word problems"],"a to 0=1; a to -1=1/a; a to m x a to n=a to m+n",s)

def L14A(s): return _qs("Polynomial basics",["polynomial=sum of terms with whole number powers","degree=highest power","monomial binomial trinomial"],"3x squared+2x-5: degree 2, trinomial",s)
def L14B(s): return _qs("Polynomial addition",["add like terms","arrange by degree","result degree=highest input"],"(3x squared+2x)+(x squared-5)=4x squared+2x-5",s)
def L14C(s): return _qs("Polynomial subtraction",["change sign of subtracted terms","collect like terms","watch signs carefully"],"(5x squared+3x)-(2x squared-x)=3x squared+4x",s)
def L14D(s): return _qs("Polynomial multiplication",["distribute each term","FOIL for binomials","collect like terms"],"(x+3)(x+4)=x squared+7x+12",s)
def L14E(s): return _qs("Algebraic identities",["(a+b) squared=a squared+2ab+b squared","(a-b) squared=a squared-2ab+b squared","(a+b)(a-b)=a squared-b squared"],"(x+5) squared=x squared+10x+25",s)
def L14F(s): return _qs("Factorisation",["take out common factor","factor by grouping","factor trinomials"],"6x squared+9x=3x(2x+3); x squared+5x+6=(x+2)(x+3)",s)
def L14G(s): return _qs("Polynomial problems",["evaluate at a value","remainder theorem","factor theorem"],"P(x)=x squared+5x+6; P(2)=4+10+6=20",s)
def L14H(s): return _qs("Mixed polynomials",["combine all operations","verify by expansion","multi-step"],"Factor then expand to verify",s)
def L14I(s): return _qs("Polynomial puzzles",["find coefficients","match polynomials","application"],"If (x+a)(x+b)=x squared+7x+12 → a+b=7,ab=12 → a=3,b=4",s)
def L14J(s): return _qs("Mixed challenge polynomials",["multi-step","real world area models","error analysis"],"Area=(x+3)(x+5)=x squared+8x+15",s)
def L14CUM1(s): return _cum(["Polynomial basics","Polynomial addition","Polynomial subtraction"],s)
def L14CUM2(s): return _cum(["Polynomial multiplication","Algebraic identities","Factorisation"],s)
def L14CUM3(s): return _cum(["Polynomial problems","Mixed polynomials","Polynomial puzzles"],s)
def L14REV(s):  return _qs("Level 14 Revision",["all polynomial operations","identities","factorisation"],"(a+b) squared=a squared+2ab+b squared; factor:x squared-9=(x+3)(x-3)",s)

def L15A(s): return _qs("Coordinate plane",["x-axis horizontal y-axis vertical","origin (0,0)","4 quadrants"],"Point A(3,4): 3 right, 4 up from origin",s)
def L15B(s): return _qs("Plotting points",["go x units right/left then y units up/down","read coordinates from graph","name the quadrant"],"Plot B(-2,3): 2 left, 3 up → Quadrant II",s)
def L15C(s): return _qs("Distance formula",["d=square root of [(x2-x1) squared+(y2-y1) squared]","distance always positive","horizontal and vertical lines"],"A(1,2) to B(4,6): square root of (9+16)=5",s)
def L15D(s): return _qs("Midpoint formula",["M=((x1+x2)/2,(y1+y2)/2)","midpoint is average of coordinates","verify equidistant from both"],"Midpoint of (2,4) and (6,8)=(4,6)",s)
def L15E(s): return _qs("Section formula",["divides in ratio m:n internally","midpoint is special case 1:1"],"Section 1:2 of (0,0) to (6,9)=(2,3)",s)
def L15F(s): return _qs("Graphing lines",["y=mx+c: slope m, y-intercept c","plot 2 points and draw line","identify slope and intercept"],"y=2x+1: at x=0,y=1; at x=2,y=5",s)
def L15G(s): return _qs("Graph applications",["interpret graphs","find slope from graph","real-world coordinate problems"],"Slope=rise/run=(y2-y1)/(x2-x1)",s)
def L15H(s): return _qs("Mixed coordinate geometry",["all formulas","multi-step","verify solutions"],"Perimeter of triangle: use distance formula 3 times",s)
def L15I(s): return _qs("Coordinate puzzles",["find missing coordinates","collinear points","areas"],"Area of triangle using coordinates formula",s)
def L15J(s): return _qs("Mixed challenge L15",["multi-step coordinate problems","real world","error analysis"],"Map reading, GPS coordinates, city planning",s)
def L15CUM1(s): return _cum(["Coordinate plane","Plotting points","Distance formula"],s)
def L15CUM2(s): return _cum(["Midpoint formula","Section formula","Graphing lines"],s)
def L15CUM3(s): return _cum(["Graph applications","Mixed coordinate geometry","Coordinate puzzles"],s)
def L15REV(s):  return _qs("Level 15 Revision",["all coordinate geometry","formulas","graphs"],"Distance, midpoint, section, slope",s)

def L16A(s): return _qs("Types of triangles",["by sides:equilateral,isosceles,scalene","by angles:acute,right,obtuse","properties of each type"],"Equilateral: all sides equal, all angles 60 degrees",s)
def L16B(s): return _qs("Angle sum property",["sum of angles in triangle=180 degrees","find missing angle","apply to solve"],"Angles 50 and 70 degrees: third=180-50-70=60 degrees",s)
def L16C(s): return _qs("Exterior angle theorem",["exterior angle=sum of two non-adjacent interior angles","apply to find angles","multi-step"],"Exterior=110 degrees; interior angles 50+60=110 degrees",s)
def L16D(s): return _qs("Congruence",["SSS SAS ASA AAS RHS criteria","congruent triangles identical shape and size","corresponding parts"],"SSS: all 3 sides equal → congruent",s)
def L16E(s): return _qs("Similar triangles",["AA SAS SSS criteria for similarity","corresponding sides in same ratio","scale factor"],"AA: angles equal → similar → sides in same ratio",s)
def L16F(s): return _qs("Pythagoras theorem",["a squared+b squared=c squared in right triangle","c=hypotenuse (longest side)","Pythagorean triples: 3,4,5; 5,12,13"],"Right triangle legs 3,4: hypotenuse=square root of 25=5",s)
def L16G(s): return _qs("Triangle applications",["area=1/2 x base x height","height perpendicular to base","real world problems"],"Area=1/2 x 8 x 5=20 cm squared",s)
def L16H(s): return _qs("Mixed triangles",["all properties","multi-step","introduce proofs"],"In right triangle: area=1/2 ab sinC",s)
def L16I(s): return _qs("Triangle puzzles",["find angles","find sides","logic geometry"],"Isosceles: base angles equal; one angle=50 → base angles=(180-50)/2=65",s)
def L16J(s): return _qs("Mixed challenge L16",["multi-step","proofs","real world"],"Ladder against wall: Pythagoras; shadow and height: similar triangles",s)
def L16CUM1(s): return _cum(["Types of triangles","Angle sum property","Exterior angle theorem"],s)
def L16CUM2(s): return _cum(["Congruence","Similar triangles","Pythagoras theorem"],s)
def L16CUM3(s): return _cum(["Triangle applications","Mixed triangles","Triangle puzzles"],s)
def L16REV(s):  return _qs("Level 16 Revision",["all triangle properties","Pythagoras","congruence"],"Sum=180 degrees; 5 squared+12 squared=13 squared",s)

def L17A(s): return _qs("Circle basics",["all points equidistant from centre","radius diameter circumference area","pi approximately 3.14159"],"Circle r=7: diameter=14",s)
def L17B(s): return _qs("Radius and diameter",["diameter=2 x radius","circumference=2 pi r=pi d","area=pi r squared"],"r=5: d=10; circumference=2 x pi x 5 approximately 31.4",s)
def L17C(s): return _qs("Chords",["chord=line segment with endpoints on circle","diameter is longest chord","perpendicular from centre bisects chord"],"Perp bisector of any chord passes through centre",s)
def L17D(s): return _qs("Tangents",["tangent touches circle at exactly one point","radius to tangent point is perpendicular","tangent length from external point"],"Tangent is perpendicular to radius at contact point",s)
def L17E(s): return _qs("Circle theorems",["angle at centre=2x angle at circumference","angles in same segment are equal","opposite angles in cyclic quad sum to 180"],"Angle at centre=2 x angle at circumference",s)
def L17F(s): return _qs("Angles in circles",["apply circle theorems","find missing angles","multi-step"],"Arc AB subtends 80 at centre → 40 at circumference",s)
def L17G(s): return _qs("Circle applications",["area=pi r squared","circumference=2 pi r","sector area and arc length"],"Sector angle 90: area=1/4 pi r squared",s)
def L17H(s): return _qs("Mixed circles",["all circle properties","multi-step","combine area and angle"],"Area of ring=pi(R squared-r squared)",s)
def L17I(s): return _qs("Circle puzzles",["find radius or diameter","angle chase","logic circle geometry"],"If arc=1/3 circumference, arc angle=360/3=120 degrees",s)
def L17J(s): return _qs("Mixed challenge L17",["multi-step","real world","combine theorems"],"Wheel, clock, pipes — all circle applications",s)
def L17CUM1(s): return _cum(["Circle basics","Radius and diameter","Chords"],s)
def L17CUM2(s): return _cum(["Tangents","Circle theorems","Angles in circles"],s)
def L17CUM3(s): return _cum(["Circle applications","Mixed circles","Circle puzzles"],s)
def L17REV(s):  return _qs("Level 17 Revision",["all circle properties","area","theorems"],"C=2 pi r; A=pi r squared; angle theorems",s)

def L18A(s): return _qs("Perimeter",["total boundary length","add all sides","formulas: square 4s; rectangle 2(l+b)"],"Rectangle 5x3: perimeter=2(5+3)=16 cm",s)
def L18B(s): return _qs("Area rectangle and square",["area=length x breadth","square:area=side squared","area in square units"],"Rectangle 6x4: area=24 cm squared",s)
def L18C(s): return _qs("Area of triangle",["area=1/2 x base x height","height perpendicular to base","Herons formula for scalene"],"Triangle base 8, height 5: area=1/2 x 8 x 5=20 cm squared",s)
def L18D(s): return _qs("Area of circle",["area=pi r squared","r=radius","use pi approximately 22/7 or 3.14"],"Circle r=7: area=22/7 x 49=154 cm squared",s)
def L18E(s): return _qs("Surface area cube and cuboid",["cube:6s squared","cuboid:2(lb+bh+lh)","lateral vs total surface area"],"Cuboid 3x4x5: TSA=2(12+20+15)=94 cm squared",s)
def L18F(s): return _qs("Cylinder and cone",["cylinder:CSA=2 pi rh; V=pi r squared h","cone:CSA=pi rl; V=1/3 pi r squared h","l=slant height for cone"],"Cylinder r=3,h=7: V=pi x 9 x 7=63 pi approximately 198 cm cubed",s)
def L18G(s): return _qs("Sphere and hemisphere",["sphere:SA=4 pi r squared; V=4/3 pi r cubed","hemisphere:CSA=2 pi r squared; V=2/3 pi r cubed"],"Sphere r=6: V=4/3 x pi x 216=288 pi cm cubed",s)
def L18H(s): return _qs("Volume problems",["cube:s cubed","cuboid:l x b x h","cylinder:pi r squared h"],"Pool 10m x 5m x 2m: V=100 m cubed=100000 litres",s)
def L18I(s): return _qs("Mixed mensuration",["all shapes","find missing dimension","multi-step"],"If area=48,breadth=6: length=8; perimeter=2(8+6)=28",s)
def L18J(s): return _qs("Mixed challenge mensuration",["multi-step","real world","compound shapes"],"Total area=sum of component areas",s)
def L18CUM1(s): return _cum(["Perimeter","Area rectangle and square","Area of triangle"],s)
def L18CUM2(s): return _cum(["Area of circle","Surface area cube and cuboid","Cylinder and cone"],s)
def L18CUM3(s): return _cum(["Sphere and hemisphere","Volume problems","Mixed mensuration"],s)
def L18REV(s):  return _qs("Level 18 Revision",["all mensuration formulas","2D and 3D","word problems"],"P=2(l+b); A=pi r squared; V=l x b x h; SA=6s squared",s)

def L19A(s): return _qs("Trigonometric ratios",["sin=opp/hyp","cos=adj/hyp","tan=opp/adj; SOH-CAH-TOA"],"sin 30=1/2; cos 60=1/2; tan 45=1",s)
def L19B(s): return _qs("Trig table",["standard values 0 30 45 60 90 degrees","memorise sin and cos","derive tan from sin/cos"],"sin 0=0; sin 30=1/2; sin 45=1/root2; sin 60=root3/2; sin 90=1",s)
def L19C(s): return _qs("Basic trig simplification",["use standard values","simplify expressions","verify identities"],"sin squared 30+cos squared 30=1/4+3/4=1",s)
def L19D(s): return _qs("Trig identities",["sin squared theta+cos squared theta=1","tan theta=sin theta/cos theta","1+tan squared theta=sec squared theta"],"sin squared theta+cos squared theta=1 always",s)
def L19E(s): return _qs("Heights and distances",["angle of elevation from below","angle of depression from above","set up trig equation"],"Tower height: tan 60=h/d → h=d root 3",s)
def L19F(s): return _qs("Trig applications",["shadows","navigation","architecture"],"Shadow of pole 10m when sun elevation=30: shadow=10/tan 30=10 root 3",s)
def L19G(s): return _qs("Mixed trig problems",["combine ratios","multi-step","verify with Pythagoras"],"If sin theta=3/5: cos theta=4/5, tan theta=3/4",s)
def L19H(s): return _qs("Advanced trig simplification",["compound angle intro","product to sum","complex expressions"],"sin(A+B)=sinA cosB+cosA sinB",s)
def L19I(s): return _qs("Trig puzzles",["find angle from ratio","trig equations","quadrant"],"2 sin theta=1 → sin theta=1/2 → theta=30 or 150 degrees",s)
def L19J(s): return _qs("Mixed challenge trig",["multi-step heights","real world navigation","error analysis"],"Two observers, two angles → find height of object",s)
def L19CUM1(s): return _cum(["Trig ratios","Trig table","Basic trig simplification"],s)
def L19CUM2(s): return _cum(["Trig identities","Heights and distances","Trig applications"],s)
def L19CUM3(s): return _cum(["Mixed trig problems","Advanced trig simplification","Trig puzzles"],s)
def L19REV(s):  return _qs("Level 19 Revision",["all trig ratios","identities","word problems"],"SOH-CAH-TOA; sin squared+cos squared=1; angle of elevation",s)

def L20A(s): return _qs("Arithmetic Progression AP",["fixed difference between consecutive terms","first term a; common difference d","nth term: a+(n-1)d"],"AP: 3,7,11,15... a=3,d=4; 10th term=3+9x4=39",s)
def L20B(s): return _qs("AP sum and term problems",["sum of n terms: n/2 times [2a+(n-1)d]","find term given its value","find n given sum"],"Sum of first 10 terms: 10/2[2x3+9x4]=5x42=210",s)
def L20C(s): return _qs("AP word problems",["salary increments","step patterns","distance problems"],"Salary Rs 5000, increment Rs 200/year; year 8=5000+7x200=6400",s)
def L20D(s): return _qs("Mean Average",["mean=sum of all values divided by count","effect of adding/removing a value","weighted mean"],"Mean of 4,7,9,12,8: sum=40,count=5,mean=8",s)
def L20E(s): return _qs("Median",["arrange in order; find middle value","odd count:middle; even count:average of two middle","median not affected by extreme values"],"Data:3,5,7,9,11 → median=7",s)
def L20F(s): return _qs("Mode",["mode=most frequent value","can have no mode one mode or multiple modes","bimodal and multimodal"],"Data:2,3,3,4,5,3,6 → mode=3",s)
def L20G(s): return _qs("Probability basics",["P(event)=favourable outcomes divided by total outcomes","0<=P<=1","P(impossible)=0; P(certain)=1"],"Fair die:P(even)=3/6=1/2",s)
def L20H(s): return _qs("Probability problems",["complementary events:P(A)+P(A complement)=1","listing outcomes","relative frequency"],"P(not red)=1-P(red); P(head)=1/2",s)
def L20I(s): return _qs("Mixed statistics and probability",["mean median mode together","probability combined","interpret data"],"Choose measure of central tendency based on data type",s)
def L20J(s): return _qs("Grand challenge L20",["multi-step statistics","AP and probability combined","real world data"],"Survey data: find mean,median,mode; predict probability",s)
def L20CUM1(s): return _cum(["AP basics","AP problems","AP word problems"],s)
def L20CUM2(s): return _cum(["Mean Average","Median","Mode"],s)
def L20CUM3(s): return _cum(["Probability basics","Probability problems","Mixed statistics and probability"],s)
def L20REV(s):  return _qs("Level 20 Revision",["AP","mean median mode","probability"],"AP nth term; mean=sum/n; P=favourable/total",s)

# ═══ MASTER ROUTER ═══
_MAP = {
    "1A":L1A,"1B":L1B,"1C":L1C,"1D":L1D,"1E":L1E,"1F":L1F,
    "1G":L1G,"1H":L1H,"1I":L1I,"1J":L1J,
    "1CUM1":L1CUM1,"1CUM2":L1CUM2,"1CUM3":L1CUM3,"1REV":L1REV,
    "2A":L2A,"2B":L2B,"2C":L2C,"2D":L2D,"2E":L2E,"2F":L2F,
    "2G":L2G,"2H":L2H,"2I":L2I,"2J":L2J,
    "2CUM1":L2CUM1,"2CUM2":L2CUM2,"2CUM3":L2CUM3,"2REV":L2REV,
    "3A":L3A,"3B":L3B,"3C":L3C,"3D":L3D,"3E":L3E,"3F":L3F,
    "3G":L3G,"3H":L3H,"3I":L3I,"3J":L3J,
    "3CUM1":L3CUM1,"3CUM2":L3CUM2,"3CUM3":L3CUM3,"3REV":L3REV,
    "4A":L4A,"4B":L4B,"4C":L4C,"4D":L4D,"4E":L4E,"4F":L4F,
    "4G":L4G,"4H":L4H,"4I":L4I,"4J":L4J,
    "4CUM1":L4CUM1,"4CUM2":L4CUM2,"4CUM3":L4CUM3,"4REV":L4REV,
    "5A":L5A,"5B":L5B,"5C":L5C,"5D":L5D,"5E":L5E,"5F":L5F,
    "5G":L5G,"5H":L5H,"5I":L5I,"5J":L5J,
    "5CUM1":L5CUM1,"5CUM2":L5CUM2,"5CUM3":L5CUM3,"5REV":L5REV,
    "6A":L6A,"6B":L6B,"6C":L6C,"6D":L6D,"6E":L6E,"6F":L6F,
    "6G":L6G,"6H":L6H,"6I":L6I,"6J":L6J,
    "6CUM1":L6CUM1,"6CUM2":L6CUM2,"6CUM3":L6CUM3,"6REV":L6REV,
    "7A":L7A,"7B":L7B,"7C":L7C,"7D":L7D,"7E":L7E,"7F":L7F,
    "7G":L7G,"7H":L7H,"7I":L7I,"7J":L7J,
    "7CUM1":L7CUM1,"7CUM2":L7CUM2,"7CUM3":L7CUM3,"7REV":L7REV,
    "8A":L8A,"8B":L8B,"8C":L8C,"8D":L8D,"8E":L8E,"8F":L8F,
    "8G":L8G,"8H":L8H,"8I":L8I,"8J":L8J,
    "8CUM1":L8CUM1,"8CUM2":L8CUM2,"8CUM3":L8CUM3,"8REV":L8REV,
    "9A":L9A,"9B":L9B,"9C":L9C,"9D":L9D,"9E":L9E,"9F":L9F,
    "9G":L9G,"9H":L9H,"9I":L9I,"9J":L9J,
    "9CUM1":L9CUM1,"9CUM2":L9CUM2,"9CUM3":L9CUM3,"9REV":L9REV,
    "10A":L10A,"10B":L10B,"10C":L10C,"10D":L10D,"10E":L10E,"10F":L10F,
    "10G":L10G,"10H":L10H,"10I":L10I,"10J":L10J,
    "10CUM1":L10CUM1,"10CUM2":L10CUM2,"10CUM3":L10CUM3,"10REV":L10REV,
    "11A":L11A,"11B":L11B,"11C":L11C,"11D":L11D,"11E":L11E,"11F":L11F,
    "11G":L11G,"11H":L11H,"11I":L11I,"11J":L11J,
    "11CUM1":L11CUM1,"11CUM2":L11CUM2,"11CUM3":L11CUM3,"11REV":L11REV,
    "12A":L12A,"12B":L12B,"12C":L12C,"12D":L12D,"12E":L12E,"12F":L12F,
    "12G":L12G,"12H":L12H,"12I":L12I,"12J":L12J,
    "12CUM1":L12CUM1,"12CUM2":L12CUM2,"12CUM3":L12CUM3,"12REV":L12REV,
    "13A":L13A,"13B":L13B,"13C":L13C,"13D":L13D,"13E":L13E,"13F":L13F,
    "13G":L13G,"13H":L13H,"13I":L13I,"13J":L13J,
    "13CUM1":L13CUM1,"13CUM2":L13CUM2,"13CUM3":L13CUM3,"13REV":L13REV,
    "14A":L14A,"14B":L14B,"14C":L14C,"14D":L14D,"14E":L14E,"14F":L14F,
    "14G":L14G,"14H":L14H,"14I":L14I,"14J":L14J,
    "14CUM1":L14CUM1,"14CUM2":L14CUM2,"14CUM3":L14CUM3,"14REV":L14REV,
    "15A":L15A,"15B":L15B,"15C":L15C,"15D":L15D,"15E":L15E,"15F":L15F,
    "15G":L15G,"15H":L15H,"15I":L15I,"15J":L15J,
    "15CUM1":L15CUM1,"15CUM2":L15CUM2,"15CUM3":L15CUM3,"15REV":L15REV,
    "16A":L16A,"16B":L16B,"16C":L16C,"16D":L16D,"16E":L16E,"16F":L16F,
    "16G":L16G,"16H":L16H,"16I":L16I,"16J":L16J,
    "16CUM1":L16CUM1,"16CUM2":L16CUM2,"16CUM3":L16CUM3,"16REV":L16REV,
    "17A":L17A,"17B":L17B,"17C":L17C,"17D":L17D,"17E":L17E,"17F":L17F,
    "17G":L17G,"17H":L17H,"17I":L17I,"17J":L17J,
    "17CUM1":L17CUM1,"17CUM2":L17CUM2,"17CUM3":L17CUM3,"17REV":L17REV,
    "18A":L18A,"18B":L18B,"18C":L18C,"18D":L18D,"18E":L18E,"18F":L18F,
    "18G":L18G,"18H":L18H,"18I":L18I,"18J":L18J,
    "18CUM1":L18CUM1,"18CUM2":L18CUM2,"18CUM3":L18CUM3,"18REV":L18REV,
    "19A":L19A,"19B":L19B,"19C":L19C,"19D":L19D,"19E":L19E,"19F":L19F,
    "19G":L19G,"19H":L19H,"19I":L19I,"19J":L19J,
    "19CUM1":L19CUM1,"19CUM2":L19CUM2,"19CUM3":L19CUM3,"19REV":L19REV,
    "20A":L20A,"20B":L20B,"20C":L20C,"20D":L20D,"20E":L20E,"20F":L20F,
    "20G":L20G,"20H":L20H,"20I":L20I,"20J":L20J,
    "20CUM1":L20CUM1,"20CUM2":L20CUM2,"20CUM3":L20CUM3,"20REV":L20REV,
}

def get_questions(sublevel_code: str, sheet_num: str) -> list:
    is_r = sheet_num.endswith("R")
    base = int(sheet_num.replace("R",""))
    fn   = _MAP.get(sublevel_code)
    items = fn(base) if fn else _qs(sublevel_code, [sublevel_code], sublevel_code, base)
    # Ensure exactly 20 questions
    qs = [x for x in items if x["type"] != "concept_box"]
    while len(qs) < 20:
        qs.append(q(f"Solve for {sublevel_code} problem {len(qs)+1}.", "fill", "Answer = ____"))
    rebuilt, qi = [], 0
    for item in items:
        if item["type"] == "concept_box":
            rebuilt.append(item)
        else:
            if qi < 20: rebuilt.append(qs[qi]); qi += 1
    while qi < 20: rebuilt.append(qs[qi]); qi += 1
    if is_r:
        rebuilt = remedialise(rebuilt, seed=hash(sublevel_code+sheet_num)%9999)
    return rebuilt
