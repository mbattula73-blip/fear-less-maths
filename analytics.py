"""
analytics.py — aggregation queries for the Analytics Dashboard tab.
Reads from db.py's SQLite store. Kept separate from db.py so the raw
storage layer stays simple and these queries can be tested independently.
"""
from collections import defaultdict
from datetime import date as _date
import db


def _session_accuracy(session: dict) -> float:
    wrong = [q for q in session["wrong_qs"].split(",") if q.strip()]
    total = session["total_questions"] or 1
    return (total - len(wrong)) / total


def get_current_levels() -> dict:
    """
    {student_id: level_num} based on each student's most recent session
    (by date, then by id as tiebreak) — regardless of any dashboard date filter,
    since "current level" is a standing fact, not a date-range fact.
    """
    with db.get_conn() as conn:
        rows = conn.execute(
            """
            SELECT s.student_id, s.level_num
            FROM sessions s
            WHERE s.id = (
                SELECT id FROM sessions s2
                WHERE s2.student_id = s.student_id
                ORDER BY s2.session_date DESC, s2.id DESC
                LIMIT 1
            )
            """
        ).fetchall()
        return {r["student_id"]: r["level_num"] for r in rows}


def school_summary(date_from: str = None, date_to: str = None) -> dict:
    all_students = db.get_students()
    total_students = len(all_students)
    current_levels = get_current_levels()

    avg_level = (sum(current_levels.values()) / len(current_levels)) if current_levels else 0.0

    today = _date.today().isoformat()
    today_sessions = db.get_sessions(date_from=today, date_to=today)
    students_today = len({s["student_id"] for s in today_sessions})
    completion_rate_today = (students_today / total_students * 100) if total_students else 0.0

    return {
        "total_students": total_students,
        "avg_level": round(avg_level, 1),
        "students_seen_today": students_today,
        "completion_rate_today": round(completion_rate_today, 1),
    }


def class_summary(date_from: str = None, date_to: str = None) -> list:
    """
    Returns a list of dicts, one per class:
    {class_name, student_count, level_distribution: {level: count}, avg_accuracy}
    level_distribution uses each student's CURRENT level (not filtered by date).
    avg_accuracy is computed only from sessions within the given date range.
    """
    students = db.get_students()
    current_levels = get_current_levels()
    by_class = defaultdict(list)
    for s in students:
        by_class[s["class_name"]].append(s)

    out = []
    for class_name, roster in sorted(by_class.items()):
        level_dist = defaultdict(int)
        for s in roster:
            lvl = current_levels.get(s["id"])
            if lvl is not None:
                level_dist[lvl] += 1

        sessions = db.get_sessions(class_name=class_name, date_from=date_from, date_to=date_to)
        accuracies = [_session_accuracy(sess) for sess in sessions]
        avg_acc = (sum(accuracies) / len(accuracies) * 100) if accuracies else None

        out.append({
            "class_name": class_name,
            "student_count": len(roster),
            "level_distribution": dict(sorted(level_dist.items())),
            "avg_accuracy": round(avg_acc, 1) if avg_acc is not None else None,
            "sessions_in_range": len(sessions),
        })
    return out


def grade_rollup(date_from: str = None, date_to: str = None) -> list:
    """
    Returns a list of dicts, one per grade (1-10 that have students):
    {grade, student_count, level_distribution: {level: count}, avg_accuracy}
    """
    students = db.get_students()
    current_levels = get_current_levels()
    by_grade = defaultdict(list)
    for s in students:
        by_grade[s["grade"]].append(s)

    out = []
    for grade, roster in sorted(by_grade.items()):
        level_dist = defaultdict(int)
        for s in roster:
            lvl = current_levels.get(s["id"])
            if lvl is not None:
                level_dist[lvl] += 1

        student_ids = {s["id"] for s in roster}
        all_sessions = db.get_sessions(date_from=date_from, date_to=date_to)
        grade_sessions = [s for s in all_sessions if s["student_id"] in student_ids]
        accuracies = [_session_accuracy(sess) for sess in grade_sessions]
        avg_acc = (sum(accuracies) / len(accuracies) * 100) if accuracies else None

        out.append({
            "grade": grade,
            "student_count": len(roster),
            "level_distribution": dict(sorted(level_dist.items())),
            "avg_accuracy": round(avg_acc, 1) if avg_acc is not None else None,
        })
    return out


def topic_failure_ranking(date_from: str = None, date_to: str = None, class_name: str = None) -> list:
    """
    Returns [{topic, student_count, occurrence_count}, ...] sorted by
    student_count desc (how many distinct students are currently struggling
    with this topic), within the given date range.
    """
    sessions = db.get_sessions(date_from=date_from, date_to=date_to, class_name=class_name)
    topic_students = defaultdict(set)
    topic_occurrences = defaultdict(int)

    for sess in sessions:
        topics = [t.strip() for t in sess["resolved_topics"].split(",") if t.strip()]
        for t in topics:
            if t == "(untagged)":
                continue
            topic_students[t].add(sess["student_id"])
            topic_occurrences[t] += 1

    rows = [
        {"topic": t, "student_count": len(topic_students[t]), "occurrence_count": topic_occurrences[t]}
        for t in topic_students
    ]
    rows.sort(key=lambda r: (-r["student_count"], -r["occurrence_count"]))
    return rows


# ─────────────────────────────────────────────────────────────────────────────
# PER-STUDENT DETAIL  (powers the Student Profile tab)
# ─────────────────────────────────────────────────────────────────────────────

def student_history(student_id: int) -> list:
    """
    Every session for one student, most recent first. Each session dict is
    annotated with accuracy (%), wrong_count, a human remedial_status
    ("Completed" / "Pending" / None if no remedial was needed), and
    wrong_details — {q_num: {"mistake_type", "student_answer"}} for whatever
    was captured at entry time (may be empty if staff skipped it).
    """
    sessions = db.get_sessions(student_id=student_id)
    out = []
    for sess in sessions:
        wrong = [q for q in sess["wrong_qs"].split(",") if q.strip()]
        remedial_status = None
        if sess["remedial_id"]:
            rs = db.get_remedial_status(sess["id"])
            remedial_status = "Completed" if (rs and rs["completed"]) else "Pending"
        out.append({
            **sess,
            "accuracy": round(_session_accuracy(sess) * 100, 1),
            "wrong_count": len(wrong),
            "remedial_status": remedial_status,
            "wrong_details": db.get_wrong_answer_details(sess["id"]),
        })
    return out


def student_topic_breakdown(student_id: int) -> list:
    """
    Returns [{topic, count}, ...] sorted by count desc — how many times this
    student has gotten each topic wrong, across all sessions.
    """
    sessions = db.get_sessions(student_id=student_id)
    topic_counts = defaultdict(int)
    for sess in sessions:
        topics = [t.strip() for t in sess["resolved_topics"].split(",") if t.strip()]
        for t in topics:
            if t == "(untagged)":
                continue
            topic_counts[t] += 1

    rows = [{"topic": t, "count": c} for t, c in topic_counts.items()]
    rows.sort(key=lambda r: -r["count"])
    return rows


def student_mistake_breakdown(student_id: int) -> list:
    """
    Returns [{mistake_type, count}, ...] sorted by count desc — across every
    wrong answer this student has had, what KIND of mistake it was (concept
    gap vs calculation slip vs carelessness, etc.). This is the "how is this
    child thinking" view, distinct from student_topic_breakdown's "WHAT
    they're getting wrong" view.
    """
    sessions = db.get_sessions(student_id=student_id)
    counts = defaultdict(int)
    for sess in sessions:
        details = db.get_wrong_answer_details(sess["id"])
        for d in details.values():
            mt = (d.get("mistake_type") or "").strip()
            if mt:
                counts[mt] += 1

    rows = [{"mistake_type": mt, "count": c} for mt, c in counts.items()]
    rows.sort(key=lambda r: -r["count"])
    return rows


def student_remedial_summary(student_id: int) -> dict:
    """
    Returns {assigned, completed, pending_count, pending_sessions} for one
    student — pending_sessions is the list of session dicts whose remedial
    worksheet hasn't been marked completed yet.
    """
    sessions = db.get_sessions(student_id=student_id)
    assigned = [s for s in sessions if s["remedial_id"]]
    pending = []
    completed = 0
    for sess in assigned:
        rs = db.get_remedial_status(sess["id"])
        if rs and rs["completed"]:
            completed += 1
        else:
            pending.append(sess)

    return {
        "assigned": len(assigned),
        "completed": completed,
        "pending_count": len(assigned) - completed,
        "pending_sessions": pending,
    }
