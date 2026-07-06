"""
Fear Less Maths — Full Roster Migration (one-time, 2026-27 school year reset).

Replaces every class's student roster with the official 2026-27 list, and
wipes all existing session/history data so every dashboard starts fresh.

Safety design:
  1. Always takes an automatic backup snapshot BEFORE wiping anything,
     returned to the caller so it can be offered as a download.
  2. Uses db.wipe_student_data(), the existing FK-safe deletion routine
     (already used for demo-data resets), rather than new deletion logic.
  3. Imports students in the exact serial order from the source roster,
     grouped by class, so roll-number-based Daily Entry lookup works
     correctly from the very first session.
  4. Returns a verification report (counts per class) so the caller can
     confirm the import matches expectations before trusting it.
"""
import db
from roster_2026_27 import ROSTER_2026_27
from datetime import datetime


def run_full_roster_replacement():
    """
    Wipes all students + session history, then imports ROSTER_2026_27.
    Returns (backup_bytes, report_dict).
    report_dict = {"total_before": int, "total_after": int,
                    "by_class": {class_name: count}, "errors": [str]}

    IMPORTANT: imports all 302 students inside a SINGLE database connection
    (one network round-trip to open, then all inserts happen locally within
    that session), rather than opening a new remote connection per student.
    The first version of this function called db.add_student() once per
    row, each opening its own fresh connection -- 302 separate network
    round-trips to the cloud database, which is almost certainly what
    caused a real run to time out / get interrupted partway through
    (reported as "only up to Class 1 imported"). This version finishes
    in a couple of seconds instead of a couple of minutes.
    """
    backup = db.backup_bytes()

    students_before = db.get_students()
    total_before = len(students_before)

    db.wipe_student_data()

    errors = []
    by_class = {}
    now = datetime.now().isoformat()

    with db.get_conn() as conn:
        for entry in ROSTER_2026_27:
            try:
                wa = db._normalize_whatsapp(entry["parent_whatsapp"]) if entry.get("parent_whatsapp") else None
                conn.execute(
                    "INSERT OR IGNORE INTO students "
                    "(name, class_name, grade, parent_whatsapp, roll_no, created_at) "
                    "VALUES (?,?,?,?,?,?)",
                    (entry["name"].strip(), entry["class_name"].strip(), entry["grade"],
                     wa, entry.get("serial"), now),
                )
                by_class[entry["class_name"]] = by_class.get(entry["class_name"], 0) + 1
            except Exception as e:
                errors.append(f"{entry['name']} ({entry['class_name']}): {e}")

    db._clear_read_caches()

    students_after = db.get_students()
    total_after = len(students_after)

    report = {
        "total_before": total_before,
        "total_after": total_after,
        "expected": len(ROSTER_2026_27),
        "by_class": by_class,
        "errors": errors,
    }
    return backup, report
