"""
db.py — Storage layer for Fear Less Maths Student Analytics Module.

CONNECTION MODES
-----------------
This module can run in two modes, chosen automatically:

1. Remote (Turso) — if TURSO_DATABASE_URL and TURSO_AUTH_TOKEN are set in
   Streamlit secrets, every connection goes to your Turso database instead
   of a local file. Turso is a real persistent database (free tier: 100
   databases, 5GB storage, 500M row reads/mo, 10M row writes/mo — see
   turso.tech/pricing) that survives Streamlit Cloud's container
   redeploys/restarts/sleep-wake cycles completely. This is what removes
   the "app reset wipes all student data" risk for good.

2. Local file (fallback) — if no Turso secrets are configured, this module
   behaves exactly as before: a local SQLite-compatible file
   (flm_data.db) next to this script. Streamlit Cloud's filesystem for
   THIS mode is still ephemeral across redeploys/restarts — see
   backup_bytes()/restore_from_bytes() below.

Both modes use the `libsql` package (libSQL — Turso's SQLite-compatible
engine), which speaks the same SQL dialect either way, so every other
function in this file is identical regardless of which mode is active.

A thin _DictConnection/_DictCursor wrapper makes libsql's plain-tuple rows
behave like sqlite3.Row (dict(row), row["col"]) — this is the ONLY reason
the wrapper exists, so nothing else in this codebase had to change.
"""
import libsql
import os
import json
from collections import defaultdict
from datetime import datetime, date
from contextlib import contextmanager

try:
    import streamlit as st
except ImportError:  # pragma: no cover — db.py is only ever run inside the app
    st = None

DB_PATH = os.path.join(os.path.dirname(__file__), "flm_data.db")

# Tables in FK-safe order: parents before children. Used by backup/restore
# and by the foreign-key-safe wipe order.
_TABLES_IN_ORDER = ["students", "worksheet_tags", "sessions", "remedial_status", "wrong_answer_details"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    class_name      TEXT NOT NULL,
    grade           INTEGER NOT NULL,
    parent_whatsapp TEXT,
    created_at      TEXT NOT NULL,
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

CREATE TABLE IF NOT EXISTS wrong_answer_details (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      INTEGER NOT NULL,
    q_num           INTEGER NOT NULL,
    mistake_type    TEXT,      -- e.g. 'Concept not understood', 'Calculation slip', ...
    student_answer  TEXT,      -- optional: what the student actually wrote, free text
    created_at      TEXT NOT NULL,
    UNIQUE(session_id, q_num),
    FOREIGN KEY(session_id) REFERENCES sessions(id)
);

CREATE INDEX IF NOT EXISTS idx_sessions_student ON sessions(student_id);
CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions(session_date);
CREATE INDEX IF NOT EXISTS idx_tags_worksheet ON worksheet_tags(worksheet_id);
CREATE INDEX IF NOT EXISTS idx_wad_session ON wrong_answer_details(session_id);
"""


def _turso_credentials():
    """Returns (url, token) if Turso secrets are configured, else (None, None)."""
    if st is None:
        return None, None
    try:
        url = st.secrets.get("TURSO_DATABASE_URL")
        token = st.secrets.get("TURSO_AUTH_TOKEN")
    except Exception:
        # No secrets.toml at all yet — perfectly normal before Turso is set up.
        return None, None
    if url and token:
        return url, token
    return None, None


def connection_status() -> dict:
    """
    Reports which backend is actually active right now, and (for Turso)
    whether a real query against it succeeds — so the app can show a clear
    yes/no instead of leaving it to guesswork after configuring secrets.
    Returns {"mode": "turso"|"local", "ok": bool, "detail": str}.
    """
    url, token = _turso_credentials()
    if not (url and token):
        return {
            "mode": "local", "ok": True,
            "detail": "No Turso secrets found — using the local file (resets on every redeploy/restart).",
        }
    try:
        with get_conn() as conn:
            conn.execute("SELECT 1")
        host = url.split("//", 1)[-1].split("?", 1)[0]
        return {
            "mode": "turso", "ok": True,
            "detail": f"Connected to Turso ({host}) — this persists across redeploys/restarts.",
        }
    except Exception as e:
        return {
            "mode": "turso", "ok": False,
            "detail": f"Turso secrets are set, but the connection failed: {e}",
        }


class _DictCursor:
    """Wraps a libsql cursor so fetchone()/fetchall() return dict-like rows
    (matching sqlite3.Row's dict(row) / row['col'] ergonomics), since the
    libsql DBAPI itself returns plain tuples."""

    def __init__(self, cursor):
        self._cursor = cursor

    def _row_to_dict(self, row):
        if row is None:
            return None
        cols = [d[0] for d in self._cursor.description]
        return dict(zip(cols, row))

    def fetchone(self):
        return self._row_to_dict(self._cursor.fetchone())

    def fetchall(self):
        return [self._row_to_dict(r) for r in self._cursor.fetchall()]

    @property
    def lastrowid(self):
        return self._cursor.lastrowid

    @property
    def rowcount(self):
        return self._cursor.rowcount


class _DictConnection:
    """Wraps a libsql connection so every execute()/executemany() call
    returns a _DictCursor — the rest of this file never needs to know
    whether it's talking to a local file or a remote Turso database."""

    def __init__(self, raw):
        self._raw = raw

    def execute(self, sql, params=None):
        cur = self._raw.execute(sql, params) if params is not None else self._raw.execute(sql)
        return _DictCursor(cur)

    def executemany(self, sql, seq_of_params):
        cur = self._raw.executemany(sql, seq_of_params)
        return _DictCursor(cur)

    def executescript(self, sql):
        return self._raw.executescript(sql)

    def commit(self):
        self._raw.commit()

    def close(self):
        self._raw.close()


@contextmanager
def get_conn():
    url, token = _turso_credentials()
    if url and token:
        raw = libsql.connect(database=url, auth_token=token)
    else:
        raw = libsql.connect(database=DB_PATH)
    conn = _DictConnection(raw)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()



def init_db():
    with get_conn() as conn:
        conn.executescript(SCHEMA)
        # Migration: add parent_whatsapp to older DBs that predate it
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(students)").fetchall()]
        if "parent_whatsapp" not in cols:
            conn.execute("ALTER TABLE students ADD COLUMN parent_whatsapp TEXT")


def import_roster(rows: list) -> dict:
    """
    Bulk import students. rows: list of dicts with keys name, class_name, grade, parent_whatsapp.
    Returns {'added': n, 'errors': [...]}.
    """
    added = 0
    errors = []
    for i, r in enumerate(rows, 1):
        name = str(r.get("name", "")).strip()
        cls = str(r.get("class_name", "")).strip()
        grade = r.get("grade")
        wa = r.get("parent_whatsapp", "")
        if not name or not cls:
            errors.append(f"Row {i}: missing name or class")
            continue
        try:
            grade = int(grade)
        except (TypeError, ValueError):
            errors.append(f"Row {i} ({name}): invalid grade '{grade}'")
            continue
        add_student(name, cls, grade, wa)
        added += 1
    return {"added": added, "errors": errors}


# ─────────────────────────────────────────────────────────────────────────────
# STUDENTS
# ─────────────────────────────────────────────────────────────────────────────

def _normalize_whatsapp(num: str) -> str:
    """Strip spaces/dashes/parens; ensure a country code. Defaults to +91 (India)
    if a bare 10-digit number is given. Returns digits-only with country code,
    suitable for wa.me links."""
    if not num:
        return ""
    cleaned = "".join(ch for ch in str(num) if ch.isdigit() or ch == "+")
    cleaned = cleaned.lstrip("+")
    if len(cleaned) == 10:           # bare Indian mobile
        cleaned = "91" + cleaned
    return cleaned


def add_student(name: str, class_name: str, grade: int, parent_whatsapp: str = None) -> int:
    wa = _normalize_whatsapp(parent_whatsapp) if parent_whatsapp else None
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT OR IGNORE INTO students (name, class_name, grade, parent_whatsapp, created_at) VALUES (?,?,?,?,?)",
            (name.strip(), class_name.strip(), grade, wa, datetime.now().isoformat()),
        )
        if cur.lastrowid:
            return cur.lastrowid
        # Already exists — update grade/parent if provided
        row = conn.execute(
            "SELECT id FROM students WHERE name=? AND class_name=?", (name.strip(), class_name.strip())
        ).fetchone()
        if wa:
            conn.execute("UPDATE students SET parent_whatsapp=?, grade=? WHERE id=?", (wa, grade, row["id"]))
        return row["id"]


def update_parent_whatsapp(student_id: int, parent_whatsapp: str):
    with get_conn() as conn:
        conn.execute("UPDATE students SET parent_whatsapp=? WHERE id=?",
                     (_normalize_whatsapp(parent_whatsapp), student_id))


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


def get_worksheet_tags_with_fallback(worksheet_id: str) -> dict:
    """
    Like get_worksheet_tags, but if a remedial worksheet (ends in 'R') has no tags
    of its own, falls back to its base sheet's tags — remedial sheets test the same
    topics per question number, only the numbers in the text change.
    e.g. '4A-1R' falls back to '4A-1' if '4A-1R' itself isn't tagged.
    """
    tags = get_worksheet_tags(worksheet_id)
    if tags:
        return tags
    if worksheet_id.endswith("R"):
        base_id = worksheet_id[:-1]
        return get_worksheet_tags(base_id)
    return tags


def list_tagged_worksheets():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT worksheet_id, COUNT(*) as n FROM worksheet_tags GROUP BY worksheet_id ORDER BY worksheet_id"
        ).fetchall()
        return [dict(r) for r in rows]


def get_worksheets_tagged_with(topic: str) -> list:
    """
    Returns [{"worksheet_id": ..., "count": ...}, ...] sorted by count desc —
    which worksheets have the most questions explicitly tagged with this
    exact topic/concept string. Used to find the best worksheet to recommend
    when a student keeps struggling with one concept.
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT worksheet_id, COUNT(*) as n FROM worksheet_tags WHERE topic=? "
            "GROUP BY worksheet_id ORDER BY n DESC",
            (topic,),
        ).fetchall()
        return [{"worksheet_id": r["worksheet_id"], "count": r["n"]} for r in rows]


def resolve_topics(worksheet_id: str, wrong_qs: list, fallback_topic: str = None) -> dict:
    """Returns {q_num: topic} for the given wrong question numbers.
    Resolution order per question:
      1. explicit per-question tag for this worksheet
      2. explicit per-question tag of the base sheet (if this is a remedial 'R' sheet)
      3. the worksheet's sublevel topic label (fallback_topic), so reports are
         always meaningful even when nothing has been tagged by hand
      4. '(untagged)' only if no fallback_topic was supplied
    """
    tags = get_worksheet_tags_with_fallback(worksheet_id)
    default = fallback_topic if fallback_topic else "(untagged)"
    return {int(q): tags.get(int(q), default) for q in wrong_qs}


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


def get_remedial_status_bulk(session_ids: list) -> dict:
    """
    Returns {session_id: {...}} for MANY sessions in ONE query, instead of
    calling get_remedial_status() once per session in a loop. Over a remote
    backend (Turso), each separate query is a network round-trip — looping
    per-session is what makes a page with many sessions feel slow.
    """
    if not session_ids:
        return {}
    placeholders = ", ".join("?" for _ in session_ids)
    with get_conn() as conn:
        rows = conn.execute(
            f"SELECT * FROM remedial_status WHERE session_id IN ({placeholders})",
            list(session_ids),
        ).fetchall()
        return {r["session_id"]: dict(r) for r in rows}


# ─────────────────────────────────────────────────────────────────────────────
# WRONG-ANSWER DETAIL  (per-question mistake type + what the student wrote)
# ─────────────────────────────────────────────────────────────────────────────

def save_wrong_answer_details(session_id: int, details: dict):
    """
    details: {q_num(int): {"mistake_type": str, "student_answer": str}, ...}
    Overwrites any existing detail rows for this session.
    """
    with get_conn() as conn:
        conn.execute("DELETE FROM wrong_answer_details WHERE session_id=?", (session_id,))
        rows = [
            (session_id, int(q), d.get("mistake_type") or None, d.get("student_answer") or None,
             datetime.now().isoformat())
            for q, d in details.items()
        ]
        if rows:
            conn.executemany(
                "INSERT INTO wrong_answer_details (session_id, q_num, mistake_type, student_answer, created_at) "
                "VALUES (?,?,?,?,?)",
                rows,
            )


def get_wrong_answer_details(session_id: int) -> dict:
    """Returns {q_num: {"mistake_type": str, "student_answer": str}, ...} for one session."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT q_num, mistake_type, student_answer FROM wrong_answer_details WHERE session_id=?",
            (session_id,),
        ).fetchall()
        return {r["q_num"]: {"mistake_type": r["mistake_type"], "student_answer": r["student_answer"]}
                for r in rows}


def get_wrong_answer_details_bulk(session_ids: list) -> dict:
    """
    Returns {session_id: {q_num: {...}}} for MANY sessions in ONE query,
    instead of calling get_wrong_answer_details() once per session in a
    loop. Same reasoning as get_remedial_status_bulk above.
    """
    if not session_ids:
        return {}
    placeholders = ", ".join("?" for _ in session_ids)
    with get_conn() as conn:
        rows = conn.execute(
            f"SELECT * FROM wrong_answer_details WHERE session_id IN ({placeholders})",
            list(session_ids),
        ).fetchall()
    out = defaultdict(dict)
    for r in rows:
        out[r["session_id"]][r["q_num"]] = {"mistake_type": r["mistake_type"], "student_answer": r["student_answer"]}
    return dict(out)


# ─────────────────────────────────────────────────────────────────────────────
# RESET  (for clearing demo/test data before loading the real roster)
# ─────────────────────────────────────────────────────────────────────────────

def wipe_student_data():
    """
    Deletes ALL students, sessions, remedial_status, and wrong_answer_details
    rows — e.g. to clear out demo/test data before loading the real roster.
    Does NOT touch worksheet_tags, since those are concept tags on the
    worksheet content itself, not tied to any student.
    """
    with get_conn() as conn:
        conn.execute("DELETE FROM wrong_answer_details")
        conn.execute("DELETE FROM remedial_status")
        conn.execute("DELETE FROM sessions")
        conn.execute("DELETE FROM students")


# ─────────────────────────────────────────────────────────────────────────────
# BACKUP / RESTORE
#
# Works as a portable JSON snapshot of every table's data, rather than raw
# file bytes — this is what lets it work identically whether the live
# backend is a local file OR a remote Turso database (there's no single
# "the file" to copy once the data lives on a server). It's also a genuine
# human-readable, backend-independent archive format, not just a backup.
# ─────────────────────────────────────────────────────────────────────────────

_BACKUP_FORMAT_VERSION = 2

def backup_bytes() -> bytes:
    """Returns a JSON snapshot of every table, as UTF-8 bytes, for download."""
    init_db()
    snapshot = {"format": "flm_backup", "version": _BACKUP_FORMAT_VERSION, "tables": {}}
    with get_conn() as conn:
        for table in _TABLES_IN_ORDER:
            rows = conn.execute(f"SELECT * FROM {table}").fetchall()
            snapshot["tables"][table] = [dict(r) for r in rows]
    return json.dumps(snapshot, indent=None).encode("utf-8")


def restore_from_bytes(data: bytes):
    """
    Restores every table from a backup produced by backup_bytes(). Wipes
    existing rows first, then reloads from the snapshot in FK-safe order.

    Also accepts the OLD raw-SQLite-file backup format (from before this
    module supported remote Turso databases) — but ONLY when currently
    running in local-file mode, since there's no way to replay a raw file
    onto a remote server. Raises ValueError for anything else unrecognized,
    or for an old-format file while running against Turso.
    """
    # Old format: raw SQLite file bytes (pre-Turso-support backups)
    if data.startswith(b"SQLite format 3\x00"):
        url, token = _turso_credentials()
        if url and token:
            raise ValueError(
                "This is an old-format backup file from before this app supported "
                "Turso — it can't be restored directly into a remote database. "
                "Restore it on a version of the app running in local-file mode "
                "first, then download a fresh backup from there to migrate it."
            )
        with open(DB_PATH, "wb") as f:
            f.write(data)
        return

    # New format: JSON snapshot
    try:
        snapshot = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise ValueError(
            "This doesn't look like a valid Fear Less Maths backup file. "
            "Restore cancelled — nothing was changed."
        ) from e

    if snapshot.get("format") != "flm_backup" or "tables" not in snapshot:
        raise ValueError(
            "This doesn't look like a valid Fear Less Maths backup file "
            "(missing expected structure). Restore cancelled — nothing was changed."
        )

    init_db()
    with get_conn() as conn:
        for table in reversed(_TABLES_IN_ORDER):
            conn.execute(f"DELETE FROM {table}")
        for table in _TABLES_IN_ORDER:
            for row in snapshot["tables"].get(table, []):
                cols = list(row.keys())
                placeholders = ", ".join("?" for _ in cols)
                conn.execute(
                    f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders})",
                    [row[c] for c in cols],
                )

# Ensure DB + schema exist as soon as this module is imported.
init_db()
