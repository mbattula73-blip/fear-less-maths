"""
db.py — Storage layer for Fear Less Maths Student Analytics Module.

Uses a local SQLite file. Streamlit Cloud's filesystem is ephemeral across
redeploys/restarts, so this module also exposes backup_bytes()/restore_from_bytes()
so the teacher can download a snapshot and re-upload it after a redeploy.
"""
import sqlite3
import os
from datetime import datetime, date
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), "flm_data.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    class_name  TEXT NOT NULL,
    grade       INTEGER NOT NULL,
    created_at  TEXT NOT NULL,
    UNIQUE(name, class_name)
);

CREATE TABLE IF NOT EXISTS worksheet_tags (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    worksheet_id  TEXT NOT NULL,     -- e.g. '7G-1'
    q_num         INTEGER NOT NULL,
    topic         TEXT NOT NULL,
    UNIQUE(worksheet_id, q_num)
);

CREATE TABLE IF NOT EXISTS sessions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_date    TEXT NOT NULL,        -- ISO date 'YYYY-MM-DD'
    student_id      INTEGER NOT NULL,
    class_name      TEXT NOT NULL,
    grade           INTEGER NOT NULL,
    level_num       INTEGER NOT NULL,
    worksheet_id    TEXT NOT NULL,         -- e.g. '7G-1'
    wrong_qs        TEXT NOT NULL,         -- comma-separated q numbers, e.g. '11,12'
    resolved_topics TEXT NOT NULL,         -- comma-separated topics, '|' if multiple per q joined elsewhere
    total_questions INTEGER NOT NULL DEFAULT 20,
    remedial_id     TEXT,                  -- e.g. '7G-1R', NULL if no wrong answers
    created_at      TEXT NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS remedial_status (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  INTEGER NOT NULL,
    completed   INTEGER NOT NULL DEFAULT 0,   -- 0/1
    completed_at TEXT,
    FOREIGN KEY(session_id) REFERENCES sessions(id)
);

CREATE INDEX IF NOT EXISTS idx_sessions_student ON sessions(student_id);
CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions(session_date);
CREATE INDEX IF NOT EXISTS idx_tags_worksheet ON worksheet_tags(worksheet_id);
"""


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.executescript(SCHEMA)


# ─────────────────────────────────────────────────────────────────────────────
# STUDENTS
# ─────────────────────────────────────────────────────────────────────────────

def add_student(name: str, class_name: str, grade: int) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT OR IGNORE INTO students (name, class_name, grade, created_at) VALUES (?,?,?,?)",
            (name.strip(), class_name.strip(), grade, datetime.now().isoformat()),
        )
        if cur.lastrowid:
            return cur.lastrowid
        row = conn.execute(
            "SELECT id FROM students WHERE name=? AND class_name=?", (name.strip(), class_name.strip())
        ).fetchone()
        return row["id"]


def get_students(class_name: str = None):
    with get_conn() as conn:
        if class_name:
            rows = conn.execute(
                "SELECT * FROM students WHERE class_name=? ORDER BY name", (class_name,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM students ORDER BY class_name, name").fetchall()
        return [dict(r) for r in rows]


def get_classes():
    with get_conn() as conn:
        rows = conn.execute("SELECT DISTINCT class_name FROM students ORDER BY class_name").fetchall()
        return [r["class_name"] for r in rows]


# ─────────────────────────────────────────────────────────────────────────────
# WORKSHEET TAGS
# ─────────────────────────────────────────────────────────────────────────────

def set_worksheet_tags(worksheet_id: str, tag_map: dict):
    """tag_map: {q_num(int): topic(str)}. Overwrites existing tags for this worksheet."""
    with get_conn() as conn:
        conn.execute("DELETE FROM worksheet_tags WHERE worksheet_id=?", (worksheet_id,))
        conn.executemany(
            "INSERT INTO worksheet_tags (worksheet_id, q_num, topic) VALUES (?,?,?)",
            [(worksheet_id, int(q), str(t).strip()) for q, t in tag_map.items() if str(t).strip()],
        )


def get_worksheet_tags(worksheet_id: str) -> dict:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT q_num, topic FROM worksheet_tags WHERE worksheet_id=? ORDER BY q_num", (worksheet_id,)
        ).fetchall()
        return {r["q_num"]: r["topic"] for r in rows}


def list_tagged_worksheets():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT worksheet_id, COUNT(*) as n FROM worksheet_tags GROUP BY worksheet_id ORDER BY worksheet_id"
        ).fetchall()
        return [dict(r) for r in rows]


def resolve_topics(worksheet_id: str, wrong_qs: list) -> dict:
    """Returns {q_num: topic_or_'(untagged)'} for the given wrong question numbers."""
    tags = get_worksheet_tags(worksheet_id)
    return {q: tags.get(int(q), "(untagged)") for q in wrong_qs}


# ─────────────────────────────────────────────────────────────────────────────
# SESSIONS
# ─────────────────────────────────────────────────────────────────────────────

def add_session(session_date: str, student_id: int, class_name: str, grade: int,
                 level_num: int, worksheet_id: str, wrong_qs: list, resolved_topics: dict,
                 total_questions: int = 20, remedial_id: str = None) -> int:
    wrong_str = ",".join(str(q) for q in wrong_qs)
    topics_str = ",".join(sorted(set(resolved_topics.values()))) if resolved_topics else ""
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO sessions
               (session_date, student_id, class_name, grade, level_num, worksheet_id,
                wrong_qs, resolved_topics, total_questions, remedial_id, created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (session_date, student_id, class_name, grade, level_num, worksheet_id,
             wrong_str, topics_str, total_questions, remedial_id, datetime.now().isoformat()),
        )
        session_id = cur.lastrowid
        if remedial_id:
            conn.execute("INSERT INTO remedial_status (session_id, completed) VALUES (?,0)", (session_id,))
        return session_id


def get_sessions(student_id: int = None, date_from: str = None, date_to: str = None,
                  class_name: str = None):
    q = "SELECT * FROM sessions WHERE 1=1"
    params = []
    if student_id is not None:
        q += " AND student_id=?"; params.append(student_id)
    if class_name:
        q += " AND class_name=?"; params.append(class_name)
    if date_from:
        q += " AND session_date>=?"; params.append(date_from)
    if date_to:
        q += " AND session_date<=?"; params.append(date_to)
    q += " ORDER BY session_date DESC, id DESC"
    with get_conn() as conn:
        rows = conn.execute(q, params).fetchall()
        return [dict(r) for r in rows]


def mark_remedial_completed(session_id: int, completed: bool = True):
    with get_conn() as conn:
        conn.execute(
            "UPDATE remedial_status SET completed=?, completed_at=? WHERE session_id=?",
            (1 if completed else 0, datetime.now().isoformat() if completed else None, session_id),
        )


def get_remedial_status(session_id: int):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM remedial_status WHERE session_id=?", (session_id,)).fetchone()
        return dict(row) if row else None


# ─────────────────────────────────────────────────────────────────────────────
# BACKUP / RESTORE  (handles Streamlit Cloud's ephemeral filesystem)
# ─────────────────────────────────────────────────────────────────────────────

def backup_bytes() -> bytes:
    """Return the raw SQLite file bytes for download."""
    init_db()
    with open(DB_PATH, "rb") as f:
        return f.read()


def restore_from_bytes(data: bytes):
    """Overwrite the local DB file with an uploaded backup."""
    with open(DB_PATH, "wb") as f:
        f.write(data)


# Ensure DB + schema exist as soon as this module is imported.
init_db()
