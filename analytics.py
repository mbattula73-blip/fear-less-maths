"""
analytics.py — aggregation queries for the Analytics Dashboard tab.
Reads from db.py's SQLite store. Kept separate from db.py so the raw
storage layer stays simple and these queries can be tested independently.
"""
from collections import defaultdict
from datetime import date as _date
import db
from levels_data import SUBLEVELS

try:
    import streamlit as st
except ImportError:
    st = None


def _cached(*args, **kwargs):
    """Same reasoning as db._cached — see that docstring. Duplicated here
    (rather than imported from db) to avoid db.py needing to import
    analytics.py back, which would create a circular import."""
    if st is None:
        def _noop(fn):
            return fn
        return _noop
    return st.cache_data(*args, **kwargs)


_CACHED_FUNCS = []


def _registered(fn):
    """Tracks every cached function in this module so clear_caches() can
    invalidate all of them in one call, without having to remember to list
    each one by hand as more get added."""
    _CACHED_FUNCS.append(fn)
    return fn


def clear_caches():
    """Called by db.py after every write, so the Alerts tab and Student
    Profile never show stale data just because a TTL hasn't expired yet."""
    for fn in _CACHED_FUNCS:
        if hasattr(fn, "clear"):
            fn.clear()


def _session_accuracy(session: dict) -> float:
    wrong = [q for q in session["wrong_qs"].split(",") if q.strip()]
    total = session["total_questions"] or 1
    return (total - len(wrong)) / total


@_registered
@_cached(ttl=3600, show_spinner=False)
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


@_registered
@_cached(ttl=3600, show_spinner=False)
def school_summary(date_from: str = None, date_to: str = None, class_name: str = None) -> dict:
    """
    Whole-school (or one class) summary for a date range — total roster,
    how many were actually active in that range, completion rate, average
    accuracy, and current average level. Powers both the old "today" quick
    glance and the Report tab's weekly/monthly view (pass a real range).
    """
    all_students = db.get_students(class_name) if class_name else db.get_students()
    total_students = len(all_students)
    current_levels = get_current_levels()

    relevant_levels = [current_levels[s["id"]] for s in all_students if s["id"] in current_levels]
    avg_level = (sum(relevant_levels) / len(relevant_levels)) if relevant_levels else 0.0

    sessions = db.get_sessions(date_from=date_from, date_to=date_to, class_name=class_name)
    active_ids = {s["student_id"] for s in sessions}
    completion_rate = (len(active_ids) / total_students * 100) if total_students else 0.0

    accuracies = [_session_accuracy(s) for s in sessions]
    avg_accuracy = (sum(accuracies) / len(accuracies) * 100) if accuracies else None

    return {
        "total_students": total_students,
        "avg_level": round(avg_level, 1),
        "active_students": len(active_ids),
        "inactive_students": total_students - len(active_ids),
        "completion_rate": round(completion_rate, 1),
        "total_sessions": len(sessions),
        "avg_accuracy": round(avg_accuracy, 1) if avg_accuracy is not None else None,
    }


@_registered
@_cached(ttl=3600, show_spinner=False)
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
            "active_students": len({s["student_id"] for s in sessions}),
        })
    return out


@_registered
@_cached(ttl=3600, show_spinner=False)
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

    all_sessions = db.get_sessions(date_from=date_from, date_to=date_to)  # fetched once, not per grade

    out = []
    for grade, roster in sorted(by_grade.items()):
        level_dist = defaultdict(int)
        for s in roster:
            lvl = current_levels.get(s["id"])
            if lvl is not None:
                level_dist[lvl] += 1

        student_ids = {s["id"] for s in roster}
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


@_registered
@_cached(ttl=3600, show_spinner=False)
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


@_registered
@_cached(ttl=3600, show_spinner=False)
def school_mistake_breakdown(date_from: str = None, date_to: str = None, class_name: str = None) -> list:
    """
    Schoolwide (or one class) mistake-type breakdown for a date range —
    the aggregate "how is the school thinking" view, for the Report tab.
    Distinct from student_mistake_breakdown, which is one student only.
    """
    sessions = db.get_sessions(date_from=date_from, date_to=date_to, class_name=class_name)
    details_map = db.get_wrong_answer_details_bulk([s["id"] for s in sessions])
    counts = defaultdict(int)
    for details in details_map.values():
        for d in details.values():
            mt = (d.get("mistake_type") or "").strip()
            if mt:
                counts[mt] += 1
    rows = [{"mistake_type": mt, "count": c} for mt, c in counts.items()]
    rows.sort(key=lambda r: -r["count"])
    return rows


@_registered
@_cached(ttl=3600, show_spinner=False)
def remedial_completion_summary(date_from: str = None, date_to: str = None, class_name: str = None) -> dict:
    """
    How many remedial worksheets were assigned (sessions with a remedial_id)
    within this date range, and how many have since been marked completed —
    schoolwide or for one class. For the Report tab.
    """
    sessions = db.get_sessions(date_from=date_from, date_to=date_to, class_name=class_name)
    assigned = [s for s in sessions if s["remedial_id"]]
    remedial_map = db.get_remedial_status_bulk([s["id"] for s in assigned])
    completed = sum(1 for s in assigned if remedial_map.get(s["id"], {}).get("completed"))
    return {
        "assigned": len(assigned),
        "completed": completed,
        "pending": len(assigned) - completed,
        "completion_rate": round(completed / len(assigned) * 100, 1) if assigned else None,
    }


# ─────────────────────────────────────────────────────────────────────────────
# PER-STUDENT DETAIL  (powers the Student Profile tab)
# ─────────────────────────────────────────────────────────────────────────────

def student_history(student_id: int, sessions: list = None) -> list:
    """
    Every session for one student, most recent first. Each session dict is
    annotated with accuracy (%), wrong_count, a human remedial_status
    ("Completed" / "Pending" / None if no remedial was needed), and
    wrong_details — {q_num: {"mistake_type", "student_answer"}} for whatever
    was captured at entry time (may be empty if staff skipped it).

    Pass `sessions` if the caller already fetched them (e.g. app.py fetching
    once and sharing across student_history/topic_breakdown/etc.) to avoid
    re-querying — each query is a real network round-trip against Turso.
    """
    sessions = sessions if sessions is not None else db.get_sessions(student_id=student_id)
    session_ids = [s["id"] for s in sessions]
    remedial_map = db.get_remedial_status_bulk(session_ids)
    details_map = db.get_wrong_answer_details_bulk(session_ids)

    out = []
    for sess in sessions:
        wrong = [q for q in sess["wrong_qs"].split(",") if q.strip()]
        remedial_status = None
        if sess["remedial_id"]:
            rs = remedial_map.get(sess["id"])
            remedial_status = "Completed" if (rs and rs["completed"]) else "Pending"
        out.append({
            **sess,
            "accuracy": round(_session_accuracy(sess) * 100, 1),
            "wrong_count": len(wrong),
            "remedial_status": remedial_status,
            "wrong_details": details_map.get(sess["id"], {}),
        })
    return out


def student_topic_breakdown(student_id: int, sessions: list = None) -> list:
    """
    Returns [{topic, count}, ...] sorted by count desc — how many times this
    student has gotten each topic wrong, across all sessions.
    """
    sessions = sessions if sessions is not None else db.get_sessions(student_id=student_id)
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


def student_mistake_breakdown(student_id: int, sessions: list = None) -> list:
    """
    Returns [{mistake_type, count}, ...] sorted by count desc — across every
    wrong answer this student has had, what KIND of mistake it was (concept
    gap vs calculation slip vs carelessness, etc.). This is the "how is this
    child thinking" view, distinct from student_topic_breakdown's "WHAT
    they're getting wrong" view.
    """
    sessions = sessions if sessions is not None else db.get_sessions(student_id=student_id)
    details_map = db.get_wrong_answer_details_bulk([s["id"] for s in sessions])
    counts = defaultdict(int)
    for details in details_map.values():
        for d in details.values():
            mt = (d.get("mistake_type") or "").strip()
            if mt:
                counts[mt] += 1

    rows = [{"mistake_type": mt, "count": c} for mt, c in counts.items()]
    rows.sort(key=lambda r: -r["count"])
    return rows


def student_remedial_summary(student_id: int, sessions: list = None) -> dict:
    """
    Returns {assigned, completed, pending_count, pending_sessions} for one
    student — pending_sessions is the list of session dicts whose remedial
    worksheet hasn't been marked completed yet.
    """
    sessions = sessions if sessions is not None else db.get_sessions(student_id=student_id)
    assigned = [s for s in sessions if s["remedial_id"]]
    remedial_map = db.get_remedial_status_bulk([s["id"] for s in assigned])

    pending = []
    completed = 0
    for sess in assigned:
        rs = remedial_map.get(sess["id"])
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


# ─────────────────────────────────────────────────────────────────────────────
# CONCEPT ALERTS  (a student stuck on the same concept across DIFFERENT
# worksheets/levels — flags it and suggests where to send them to fix it)
# ─────────────────────────────────────────────────────────────────────────────

# {sublevel_code: (level_num, topic_label)} — built once from levels_data.
_SUBLEVEL_INDEX = {
    code: (lvl, t)
    for lvl, subs in SUBLEVELS.items()
    for code, t in subs
}


def recommend_worksheet_for_concept(concept: str, sample_worksheet_ids: list = None):
    """
    Given a concept/topic string (as it appears in resolved_topics), finds
    the sublevel that teaches it and returns the worksheet best suited to
    re-teach it — the sublevel's Sheet 2 ("Try it — Concept" tier).

    IMPORTANT: several sublevels share generic topic labels across totally
    different levels (e.g. every level's cumulative-review sublevel is
    labelled "Mixed A+B+C") — so a bare string match against the topic
    label is ambiguous about WHICH level. `sample_worksheet_ids` should be
    the actual worksheet_ids from the student's own sessions where this
    concept occurred; we use the most common sublevel among those to anchor
    the recommendation to the level the student is actually struggling in.

    Falls back to 1) the most-tagged worksheet for this exact concept
    (handles concept_tagger's specific labels) or 2) the first sublevel
    whose own topic label matches, if no sample is given.

    Returns None if no match can be found.
    """
    sublevel_code = None

    if sample_worksheet_ids:
        codes = [wid.split("-")[0] for wid in sample_worksheet_ids if "-" in wid]
        if codes:
            sublevel_code = max(set(codes), key=codes.count)

    if not sublevel_code:
        tagged = db.get_worksheets_tagged_with(concept)
        if tagged:
            sublevel_code = tagged[0]["worksheet_id"].split("-")[0]

    if not sublevel_code:
        for code, (lvl, t) in _SUBLEVEL_INDEX.items():
            if t == concept:
                sublevel_code = code
                break

    if not sublevel_code or sublevel_code not in _SUBLEVEL_INDEX:
        return None

    level_num, sub_topic = _SUBLEVEL_INDEX[sublevel_code]
    return {
        "level_num": level_num,
        "sublevel_code": sublevel_code,
        "sublevel_topic": sub_topic,
        "recommended_worksheet_id": f"{sublevel_code}-2",
    }


def concept_mistake_types_for_student(student_id: int, concept: str) -> list:
    """
    Returns [{mistake_type, count}, ...] sorted desc, but ONLY for this
    student's wrong answers that were tagged with this specific concept —
    e.g. telling you whether their repeated "HCF" mistakes are mostly
    "Concept not understood" (needs re-teaching) vs "Calculation slip"
    (just needs more practice). Kept as a standalone utility (concept_alerts
    computes this itself, in one pass, for efficiency — see below).
    """
    sessions = db.get_sessions(student_id=student_id)
    counts = defaultdict(int)
    for sess in sessions:
        topics_in_session = [t.strip() for t in sess["resolved_topics"].split(",") if t.strip()]
        if concept not in topics_in_session:
            continue
        details = db.get_wrong_answer_details(sess["id"])
        for d in details.values():
            mt = (d.get("mistake_type") or "").strip()
            if mt:
                counts[mt] += 1

    rows = [{"mistake_type": mt, "count": c} for mt, c in counts.items()]
    rows.sort(key=lambda r: -r["count"])
    return rows


@_registered
@_cached(ttl=3600, show_spinner=False)
def concept_alerts(threshold: int = 2, class_name: str = None) -> list:
    """
    Scans every student (optionally limited to one class) and flags any
    student+concept pair where that concept caused a wrong answer in MORE
    THAN `threshold` separate worksheet sessions (default threshold=2, i.e.
    3 or more times) — even if those sessions span different worksheets and
    different levels, since the same concept (e.g. "Fractions") can recur
    across the curriculum.

    Fetches every session for the whole school (or class) in ONE query,
    instead of one query per student — looping per-student is what made
    this tab slow over a remote (Turso) backend with a real student count.

    Returns alerts sorted worst-first:
    [{student_id, student_name, class_name, grade, concept, times,
      mistake_breakdown: [...], recommendation: {...} or None}, ...]
    """
    students = db.get_students(class_name) if class_name else db.get_students()
    if not students:
        return []
    students_by_id = {s["id"]: s for s in students}

    all_sessions = db.get_sessions(class_name=class_name) if class_name else db.get_sessions()
    sessions_by_student = defaultdict(list)
    for sess in all_sessions:
        sessions_by_student[sess["student_id"]].append(sess)

    details_map = db.get_wrong_answer_details_bulk([s["id"] for s in all_sessions])

    alerts = []
    for student_id, sessions in sessions_by_student.items():
        s = students_by_id.get(student_id)
        if not s:
            continue  # session belongs to a student outside this filter

        concept_sessions = defaultdict(list)
        for sess in sessions:
            topics = [t.strip() for t in sess["resolved_topics"].split(",") if t.strip()]
            for t in topics:
                if t == "(untagged)":
                    continue
                concept_sessions[t].append(sess)

        for concept, sess_list in concept_sessions.items():
            if len(sess_list) <= threshold:
                continue

            mistake_counts = defaultdict(int)
            for sess in sess_list:
                for d in details_map.get(sess["id"], {}).values():
                    mt = (d.get("mistake_type") or "").strip()
                    if mt:
                        mistake_counts[mt] += 1
            mistake_rows = sorted(
                [{"mistake_type": mt, "count": c} for mt, c in mistake_counts.items()],
                key=lambda r: -r["count"],
            )

            worksheet_ids = [sess["worksheet_id"] for sess in sess_list]
            alerts.append({
                "student_id": s["id"],
                "student_name": s["name"],
                "class_name": s["class_name"],
                "grade": s["grade"],
                "concept": concept,
                "times": len(sess_list),
                "mistake_breakdown": mistake_rows,
                "recommendation": recommend_worksheet_for_concept(concept, worksheet_ids),
            })

    alerts.sort(key=lambda a: (-a["times"], a["class_name"], a["student_name"]))
    return alerts
