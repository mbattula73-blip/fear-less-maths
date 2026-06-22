"""
seed_demo_data.py — One-click demo/test data generator for Fear Less Maths.

Creates a fake roster (30 students x 10 classes = 300 students by default)
plus a realistic worksheet session history for each — worksheet attempts,
wrong answers, remedial assignments/completions, spanning the last several
weeks — purely so the Student Profile tab has real data to explore before
the actual class roster and parent WhatsApp numbers are added.

Usage (from inside the running app, where db.py's connection is live):
    from seed_demo_data import generate_demo_data
    result = generate_demo_data()

Re-running after data already exists will just add MORE sessions for the
same 300 students (db.add_student de-dupes by name+class, so you won't get
duplicate students). If you want a clean slate, call db.wipe_student_data()
first.
"""
import random
from datetime import date, timedelta

import db
from levels_data import SUBLEVELS
from ws_helpers import remedial_id_for, MISTAKE_TYPES

FIRST_NAMES = [
    "Aarav", "Vihaan", "Aditya", "Sai", "Reyansh", "Krishna", "Ishaan", "Arjun", "Rohan", "Karthik",
    "Aarush", "Dhruv", "Pranav", "Siddharth", "Vivaan", "Yash", "Harsha", "Tarun", "Naveen", "Sandeep",
    "Ananya", "Diya", "Saanvi", "Aadhya", "Kavya", "Meera", "Sneha", "Priya", "Lakshmi", "Pooja",
    "Sahasra", "Bhavya", "Nikitha", "Tejaswini", "Deepika", "Anjali", "Rakshita", "Swathi", "Harika", "Madhuri",
    "Rahul", "Manoj", "Ganesh", "Suresh", "Ramesh", "Vamsi", "Charan", "Kiran", "Lokesh", "Mahesh",
    "Sowmya", "Divya", "Spandana", "Vasavi", "Keerthana", "Mounika", "Sireesha", "Padma", "Jyothi", "Aparna",
]
LAST_NAMES = [
    "Reddy", "Naidu", "Rao", "Sharma", "Varma", "Chowdary", "Babu", "Kumar", "Prasad", "Krishna",
    "Gupta", "Patel", "Yadav", "Goud", "Sastry", "Murthy", "Setty", "Raju", "Devi", "Kumari",
]

NUM_CLASSES = 10   # Class 1 .. Class 10 (one section each, matching IDPS)
PER_CLASS = 30     # 30 students per class -> 300 total
DAYS_BACK = 45     # simulate roughly the last 6-7 weeks of activity
TOTAL_Q = 20


def _fake_name(used: set) -> str:
    while True:
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        if name not in used:
            used.add(name)
            return name


def _level_for_grade(grade: int) -> int:
    """Roughly 2 worksheet-levels per school grade, capped 1-20, with a little spread."""
    base = grade * 2 - 1
    return min(20, max(1, base + random.choice([-1, 0, 0, 1])))


def generate_demo_data(num_classes: int = NUM_CLASSES, per_class: int = PER_CLASS,
                        days_back: int = DAYS_BACK) -> dict:
    """
    Creates fake students (Class 1..num_classes, per_class each) and a
    realistic worksheet session history for every one of them. Returns
    {"students_created": n, "sessions_created": n}.
    """
    students_created = 0
    sessions_created = 0

    for grade in range(1, num_classes + 1):
        class_name = f"Class {grade}"
        used_names = set()
        roster = []
        for _ in range(per_class):
            name = _fake_name(used_names)
            sid = db.add_student(name, class_name, grade, parent_whatsapp=None)
            roster.append(sid)
            students_created += 1

        for student_id in roster:
            level_num = _level_for_grade(grade)
            sublevels = SUBLEVELS.get(level_num, SUBLEVELS[1])
            sub_idx = 0
            cursor_date = date.today() - timedelta(days=days_back)
            # This student's underlying skill (0-1). Drifts upward slightly
            # over time so accuracy trend charts show real improvement.
            accuracy_skill = random.uniform(0.55, 0.9)

            while cursor_date <= date.today():
                if sub_idx >= len(sublevels):
                    if level_num < 20:
                        level_num += 1
                        sublevels = SUBLEVELS.get(level_num, sublevels)
                        sub_idx = 0
                    else:
                        break

                sublevel_code, topic = sublevels[sub_idx]
                sheets_today = random.sample(["1", "2", "3", "4"], k=random.choice([1, 1, 2]))

                for sheet_num in sheets_today:
                    accuracy_skill = min(0.97, accuracy_skill + random.uniform(0, 0.01))
                    error_rate = max(0.0, min(0.65, (1 - accuracy_skill) + random.uniform(-0.1, 0.15)))
                    n_wrong = round(error_rate * TOTAL_Q)
                    wrong_qs = sorted(random.sample(range(1, TOTAL_Q + 1), n_wrong)) if n_wrong else []

                    ws_id = f"{sublevel_code}-{sheet_num}"
                    resolved = db.resolve_topics(ws_id, wrong_qs, fallback_topic=topic) if wrong_qs else {}
                    remedial_id = remedial_id_for(sublevel_code, sheet_num) if wrong_qs else None

                    new_session_id = db.add_session(
                        session_date=cursor_date.isoformat(),
                        student_id=student_id,
                        class_name=class_name,
                        grade=grade,
                        level_num=level_num,
                        worksheet_id=ws_id,
                        wrong_qs=wrong_qs,
                        resolved_topics=resolved,
                        total_questions=TOTAL_Q,
                        remedial_id=remedial_id,
                    )
                    sessions_created += 1

                    if wrong_qs:
                        # Weighted toward the two most pedagogically common
                        # mistake types, with the rest as plausible noise.
                        weights = [30, 28, 12, 10, 12, 6, 2]
                        details = {}
                        for qn in wrong_qs:
                            mtype = random.choices(MISTAKE_TYPES, weights=weights, k=1)[0]
                            # Most real entries skip the free-text answer (staff are busy) —
                            # only fill it in occasionally, like a real classroom would.
                            ans = "" if random.random() < 0.75 else random.choice(
                                ["miscounted", "sign error", "wrong table used", "left it blank", "swapped digits"]
                            )
                            details[qn] = {"mistake_type": mtype, "student_answer": ans}
                        db.save_wrong_answer_details(new_session_id, details)

                    if remedial_id and random.random() < 0.6:
                        # Mark this just-inserted session's remedial as completed
                        # (simulating the teacher following up a few days later).
                        db.mark_remedial_completed(new_session_id, True)

                sub_idx += 1
                cursor_date += timedelta(days=random.choice([2, 3, 3, 4, 5]))

    return {"students_created": students_created, "sessions_created": sessions_created}
