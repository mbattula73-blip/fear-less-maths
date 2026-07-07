"""
pages/1_Daily_Entry.py — Staff daily worksheet entry for Fear Less Maths.

Two main improvements over the previous version:
  1. SERIAL NUMBER ENTRY — type roll number → student name appears instantly,
     no scrolling through a 30-name dropdown.
  2. INTELLIGENT MISTAKE CLASSIFICATION — staff just types what the student
     wrote; the app auto-detects the mistake type (calculation slip / concept
     not understood / wrong method / etc.) with a reason. Staff can override
     if the auto-detect is wrong with one tap.
"""
import streamlit as st
import pandas as pd
from datetime import date as _date

import db
import ui_common
from levels_data import SHEET_OPTIONS
from ws_helpers import (
    remedial_id_for, build_whatsapp_report_multi,
    build_whatsapp_link,
)
import mistake_classifier as mc

ui_common.setup_page("Daily Entry — Fear Less Maths")

ui_common.render_header(
    subtitle="Daily Entry · Staff",
    badge="Manage students & log today's worksheet results",
)
level_num, sublevel_code, topic = ui_common.render_level_selector(key_prefix="de_page_")

st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 1. MANAGE STUDENTS
# ════════════════════════════════════════════════════════════════════════════
with st.expander("👥 Manage Students — add new students, bulk import, or update a WhatsApp number",
                  expanded=(not db.get_classes())):
    mgmt_mode = st.radio(
        "Action", ["Add one student", "Bulk import a class", "View / edit roster",
                   "⚠️ Full Roster Reset (2026-27)"],
        horizontal=True, key="mgmt_mode", label_visibility="collapsed",
    )

    if mgmt_mode == "⚠️ Full Roster Reset (2026-27)":
        st.error(
            "**This is a one-time, irreversible reset.** It will:\n\n"
            "1. Delete every current student, session, and score history — ALL classes.\n"
            "2. Import the official 2026-27 roster (302 students, Nursery through Class 10) "
            "fresh, in serial order.\n\n"
            "Every dashboard (Student Profile, Alerts, Report) will start completely empty "
            "afterward. A backup of the current data is downloaded automatically before "
            "anything is deleted, in case you need to recover it."
        )
        current_count = len(db.get_students())
        st.caption(f"Students currently in the database: {current_count}")

        confirm_text = st.text_input(
            "Type RESET to confirm you understand this cannot be undone",
            key="roster_reset_confirm",
        )
        if confirm_text.strip().upper() == "RESET":
            if st.button("🗑️  Wipe & Import 2026-27 Roster", type="primary", key="do_roster_reset"):
                with st.spinner("Backing up current data, then wiping and importing…"):
                    import roster_migration
                    backup_bytes, report = roster_migration.run_full_roster_replacement()
                st.session_state["roster_reset_backup"] = backup_bytes
                st.session_state["roster_reset_report"] = report
                st.rerun()
        else:
            st.caption("Type RESET (all caps) above to unlock the button.")

        if "roster_reset_report" in st.session_state:
            report = st.session_state["roster_reset_report"]
            st.success(
                f"✅ Done. {report['total_before']} old student record(s) removed. "
                f"{report['total_after']} of {report['expected']} new students imported."
            )
            if report["errors"]:
                st.warning(f"{len(report['errors'])} row(s) had issues:\n\n" +
                          "\n".join(report["errors"][:10]))
            st.markdown("**By class:**")
            for cn, cnt in sorted(report["by_class"].items(), key=lambda x: x[0]):
                st.caption(f"{cn}: {cnt} students")
            st.download_button(
                "⬇ Download pre-reset backup (safety copy)",
                data=st.session_state["roster_reset_backup"],
                file_name="flm_backup_before_2026_27_reset.json",
                mime="application/json",
                key="dl_reset_backup",
            )

    elif mgmt_mode == "Add one student":
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            new_name  = st.text_input("Student name", key="new_student_name")
            new_class = st.text_input("Class", key="new_student_class",
                                      placeholder="e.g. Class 7")
        with col_a2:
            new_grade = st.number_input("Grade", min_value=1, max_value=12,
                                        value=1, key="new_student_grade")
            new_wa    = st.text_input("Parent WhatsApp number", key="new_student_wa",
                                      placeholder="e.g. 7036525875 (optional)")
        if st.button("➕  Add Student", type="primary", key="add_one_student"):
            if not new_name.strip() or not new_class.strip():
                st.error("Name and Class are required.")
            else:
                db.add_student(new_name.strip(), new_class.strip(),
                               int(new_grade), new_wa.strip() or None)
                st.success(f"Added {new_name.strip()} to {new_class.strip()}.")
                for k in ("new_student_name", "new_student_class", "new_student_wa"):
                    st.session_state.pop(k, None)
                st.rerun()

    elif mgmt_mode == "Bulk import a class":
        st.caption("Format per line:  Name, Class, Grade, Parent WhatsApp number")
        roster_file = st.file_uploader("Upload a .txt roster file",
                                       type=["txt"], key="roster_file_upload")
        roster_text = st.text_area(
            "Or paste here",
            placeholder="Ravi Kumar, Class 7, 7, 7036525875\nMeena, Class 7, 7",
            height=150, key="roster_text_bulk", label_visibility="collapsed",
        )
        source_text = roster_file.getvalue().decode("utf-8") if roster_file else roster_text
        if roster_file:
            st.caption(f"📄 {roster_file.name} ({len(source_text.strip().splitlines())} lines)")

        if st.button("📋  Import Roster", type="primary", key="import_roster_bulk"):
            rows, errs = [], []
            for i, line in enumerate(source_text.strip().splitlines(), 1):
                if not line.strip(): continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) < 3:
                    errs.append(f"Line {i}: need at least Name, Class, Grade")
                    continue
                rows.append({"name": parts[0], "class_name": parts[1],
                             "grade": parts[2],
                             "parent_whatsapp": parts[3] if len(parts) > 3 else ""})
            if errs:
                st.error("\n".join(errs))
            if rows:
                res = db.import_roster(rows)
                if res["errors"]:
                    st.warning("Some rows skipped:\n\n" + "\n".join(res["errors"]))
                st.success(f"Imported {res['added']} students.")
                st.session_state.pop("roster_text_bulk", None)
                st.rerun()

    else:  # View / edit roster
        view_classes = db.get_classes()
        if not view_classes:
            st.caption("No students yet.")
        else:
            vc = st.selectbox("Class", view_classes, key="mgmt_view_class")
            roster_view = db.get_students(vc)
            st.caption(f"{len(roster_view)} students in {vc}")
            view_df = pd.DataFrame([{
                "#": i+1,
                "Name": s["name"],
                "Grade": s["grade"],
                "Parent WhatsApp": s.get("parent_whatsapp") or "— not on file —",
            } for i, s in enumerate(roster_view)])
            st.dataframe(view_df, hide_index=True, width='stretch')

            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
            st.caption("Update a parent's WhatsApp number:")
            col_e1, col_e2 = st.columns([1, 1])
            with col_e1:
                edit_pick = st.selectbox("Student",
                    [f"{i+1}. {s['name']}" for i, s in enumerate(roster_view)],
                    key="mgmt_edit_pick", label_visibility="collapsed")
                edit_idx = int(edit_pick.split(".")[0]) - 1
            edit_student = roster_view[edit_idx]
            with col_e2:
                new_wa_val = st.text_input(
                    "WhatsApp number",
                    value=edit_student.get("parent_whatsapp") or "",
                    key=f"mgmt_wa_input_{edit_student['id']}",
                    placeholder="e.g. 7036525875",
                    label_visibility="collapsed",
                )
            if st.button("💾  Save WhatsApp Number", key="mgmt_wa_save"):
                db.update_parent_whatsapp(edit_student["id"], new_wa_val)
                st.success(f"Updated {edit_student['name']}'s WhatsApp number.")
                st.rerun()

st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 2. DAILY ENTRY — SERIAL NUMBER + INTELLIGENT MISTAKE DETECTION
# ════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════
# WHOLE-CLASS GRID — mark an entire class in one table instead of
# navigating student-by-student. Trade-off: this mode only records WHICH
# question numbers were wrong, not the per-student "what did they write"
# mistake-typing detail -- that level of detail is still available in
# One Student at a Time mode.
# ════════════════════════════════════════════════════════════════════════════
def _render_class_grid(de_class, roster, level_num, sublevel_code, topic):
    st.caption(
        "Type wrong question numbers per student (e.g. '3, 7, 15'), tick Absent "
        "for anyone away today, then Save Whole Class once at the bottom."
    )

    cg_date = st.date_input("Date", value=_date.today(), key="cg_date")

    de_sheet_lbls = [lbl for _, lbl in SHEET_OPTIONS]
    cg_num_sheets = st.radio(
        "Worksheets today", [1, 2], index=1, horizontal=True, key="cg_num_sheets",
        format_func=lambda n: "1 worksheet" if n == 1 else "2 worksheets (default)",
    )

    sheet_nums = []
    sheet_cols = st.columns(cg_num_sheets)
    for i, col in enumerate(sheet_cols, 1):
        with col:
            sel = st.selectbox(
                f"Worksheet {i} sheet", de_sheet_lbls,
                index=min(i - 1, len(de_sheet_lbls) - 1), key=f"cg_sheet_{i}",
            )
            sheet_nums.append(SHEET_OPTIONS[de_sheet_lbls.index(sel)][0])

    total_q = int(st.number_input(
        "Total Qs per sheet", min_value=1, max_value=50, value=20, key="cg_total_q",
    ))

    if not roster:
        st.info("No students in this class yet.")
        return

    # A fresh grid_key per class/date/sheet-count combo -- switching any of
    # those starts a clean grid instead of showing stale edits from before.
    grid_key = f"cg_grid_{de_class}_{cg_date.isoformat()}_{cg_num_sheets}"

    base_rows = []
    for i, s in enumerate(roster, 1):
        row = {"Roll": i, "Name": s["name"], "Absent": False}
        for sn in range(1, cg_num_sheets + 1):
            row[f"S{sn} Wrong"] = ""
        base_rows.append(row)
    base_df = pd.DataFrame(base_rows)

    column_config = {
        "Roll": st.column_config.NumberColumn(disabled=True, width="small"),
        "Name": st.column_config.TextColumn(disabled=True, width="medium"),
        "Absent": st.column_config.CheckboxColumn(width="small"),
    }
    for sn in range(1, cg_num_sheets + 1):
        column_config[f"S{sn} Wrong"] = st.column_config.TextColumn(
            f"Sheet {sn} — wrong Qs",
            help="e.g. 3, 7, 15 — leave blank if all correct",
        )

    edited = st.data_editor(
        base_df, key=grid_key, hide_index=True, width="stretch",
        column_config=column_config, num_rows="fixed",
    )

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

    if st.button("💾  Save Whole Class", type="primary", key="cg_save", use_container_width=True):
        student_by_roll = {i: s for i, s in enumerate(roster, 1)}
        rows_to_save = []
        for _, r in edited.iterrows():
            roll = int(r["Roll"])
            student = student_by_roll[roll]

            if bool(r["Absent"]):
                rows_to_save.append({
                    "student_id": student["id"], "grade": student["grade"], "status": "absent",
                })
                continue

            sheet_entries = []
            for idx, sn in enumerate(sheet_nums, 1):
                wrong_text = str(r.get(f"S{idx} Wrong", "") or "").strip()
                wrong_qs = sorted({
                    int(p.strip()) for p in wrong_text.split(",")
                    if p.strip().isdigit() and 1 <= int(p.strip()) <= total_q
                })
                ws_id = f"{sublevel_code}-{sn}"
                resolved = db.resolve_topics(ws_id, wrong_qs, fallback_topic=topic) if wrong_qs else {}
                remedial_id = remedial_id_for(sublevel_code, sn) if len(wrong_qs) > 3 else None
                sheet_entries.append({
                    "worksheet_id": ws_id, "wrong_qs": wrong_qs,
                    "resolved_topics": resolved, "total_questions": total_q,
                    "remedial_id": remedial_id,
                })

            rows_to_save.append({
                "student_id": student["id"], "grade": student["grade"],
                "status": None, "sheet_entries": sheet_entries,
            })

        db.save_class_entries(
            session_date=cg_date.isoformat(), class_name=de_class,
            level_num=level_num, rows=rows_to_save,
        )
        st.session_state["_flash_toast"] = f"✅ Saved {len(rows_to_save)} students in {de_class}."
        st.session_state.pop(grid_key, None)  # reset the grid for the next entry
        st.rerun()


@st.fragment
def _daily_entry_fragment(level_num, sublevel_code, topic):
    """Everything below reruns on its own (Save, checkboxes, roll number, etc.)
    instead of the whole page, via st.fragment -- this is what makes Save feel
    instant instead of re-loading the header/Manage Students/level selector too.
    """
    # Show the save confirmation as a floating toast. Lives inside the fragment
    # so it still fires after a fragment-scoped rerun (a check placed outside
    # the fragment would never run again once Save only reruns this block).
    if "_flash_toast" in st.session_state:
        st.toast(st.session_state.pop("_flash_toast"), icon="✅")

    existing_classes = db.get_classes()

    if not existing_classes:
        st.info("No students yet — add your first student above.")
    else:
        st.markdown("##### Daily Entry")

        entry_mode = st.radio(
            "Entry mode", ["One Student at a Time", "Whole Class Grid"],
            horizontal=True, key="de_entry_mode",
        )

        de_class = st.selectbox("Class", existing_classes, key="de_class")
        roster = db.get_students(de_class)

        if entry_mode == "Whole Class Grid":
            _render_class_grid(de_class, roster, level_num, sublevel_code, topic)
            return

        # ── Serial number student picker ────────────────────────────────────────
        col_d2, col_d3 = st.columns([0.8, 1.5])

        # Apply any pending roll-number advance queued by a previous Save click.
        # This MUST happen before the de_roll widget below is instantiated --
        # Streamlit forbids writing to a widget's session_state key after that
        # widget has already been drawn in the same script run, which is
        # exactly what caused the StreamlitAPIException when this was done
        # directly inside the Save button's own click handler further down.
        if "_pending_roll_advance" in st.session_state:
            st.session_state["de_roll"] = st.session_state.pop("_pending_roll_advance")

        with col_d2:
            # Show roll number range as hint. No `value=` here -- the widget's
            # value is fully owned by session_state (defaulted via
            # st.session_state.setdefault below), since passing both a
            # `value=` and a session_state entry for the same key triggers a
            # (harmless but noisy) Streamlit warning.
            st.session_state.setdefault("de_roll", 1)
            roll_input = st.number_input(
                f"Roll No (1–{len(roster)})",
                min_value=1, max_value=len(roster), step=1, key="de_roll",
            )

        # Resolve student from roll number (1-based index into alphabetical roster)
        roll_idx  = int(roll_input) - 1
        student   = roster[roll_idx]
        de_name   = student["name"]

        with col_d3:
            st.markdown(f"""
            <div style="padding-top:28px">
                <span style="font-size:18px;font-weight:700;color:#111">{de_name}</span>
                <span style="font-size:12px;color:#888;margin-left:8px">Roll #{int(roll_input)}</span>
            </div>
            """, unsafe_allow_html=True)

        # Roster quick-reference so staff can see names ↔ numbers at a glance
        with st.expander("📋 View class roster (roll numbers)", expanded=False):
            half = (len(roster) + 1) // 2
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                for i, s in enumerate(roster[:half], 1):
                    st.markdown(f"**{i}.** {s['name']}", unsafe_allow_html=False)
            with col_r2:
                for i, s in enumerate(roster[half:], half + 1):
                    st.markdown(f"**{i}.** {s['name']}", unsafe_allow_html=False)

        if not student.get("parent_whatsapp"):
            wa_in = st.text_input(
                f"Parent WhatsApp for {de_name} (not on file)",
                key="de_add_wa", placeholder="e.g. 7036525875",
            )
            if wa_in.strip():
                db.update_parent_whatsapp(student["id"], wa_in)
                st.rerun()

        de_date = st.date_input("Date", value=_date.today(), key="de_date")

        de_status = st.radio(
            "Student status today", ["Present", "Absent"], horizontal=True, key="de_status",
        )

        if de_status == "Absent":
            st.info(f"**{de_name}** will be marked absent for {de_date.strftime('%d %b %Y')} — no worksheet score is recorded.")
            if st.button("📌  Mark Absent & Save", type="primary", key="de_mark_absent", use_container_width=True):
                db.add_session(
                    session_date=de_date.isoformat(), student_id=student["id"],
                    class_name=de_class, grade=student["grade"], level_num=level_num,
                    worksheet_id=f"{sublevel_code}-ABSENT", wrong_qs=[], resolved_topics={},
                    total_questions=0, remedial_id=None, status="absent",
                )
                next_roll = min(int(roll_input) + 1, len(roster))
                st.session_state["_pending_roll_advance"] = next_roll
                st.session_state["_flash_toast"] = f"✅ Marked {de_name} absent. Next → Roll #{next_roll}"
                st.rerun()
            return

        de_sheet_lbls = [lbl for _, lbl in SHEET_OPTIONS]
        de_num_sheets = st.radio(
            "Worksheets today", [1, 2], index=1, horizontal=True, key="de_num_sheets",
            format_func=lambda n: "1 worksheet" if n == 1 else "2 worksheets (default)",
        )

        # ── Pre-load question items + correct answers for this level/sublevel ─────
        # Cached with st.cache_data so this only runs ONCE per (code, sheet, level)
        # combo and is reused across every rerun -- previously this recomputed
        # from scratch (question generation + answer derivation for every
        # question) on EVERY interaction, including just changing the roll
        # number, which is what caused the noticeable latency.
        try:
            from content import get_questions as _gq
            from answer_key import derive_answer_and_explanation as _dae

            @st.cache_data(ttl=3600, show_spinner=False)
            def _get_items_and_answers(code, sheet, lvl):
                raw = _gq(code, sheet, lvl)
                items = [it for it in raw if it.get("type") not in ("concept_box", "tips_box")]
                answers = [_dae(it)[0] for it in items]
                return items, answers
            _answers_available = True
        except Exception:
            _answers_available = False

        # ══════════════════════════════════════════════════════════════════════════
        # Per-worksheet entry
        # ══════════════════════════════════════════════════════════════════════════
        sheet_entries = []
        for sheet_idx in range(1, de_num_sheets + 1):
            st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
            st.markdown(f"###### Worksheet {sheet_idx}")

            col_w1, col_w2 = st.columns([1, 1])
            with col_w1:
                sel_default = min(sheet_idx - 1, len(de_sheet_lbls) - 1)
                de_sheet_sel = st.selectbox(
                    "Sheet", de_sheet_lbls, index=sel_default,
                    key=f"de_sheet_{sheet_idx}",
                )
                de_sheet_num = SHEET_OPTIONS[de_sheet_lbls.index(de_sheet_sel)][0]
            with col_w2:
                de_total_q = st.number_input(
                    "Total Qs", min_value=1, max_value=50, value=20,
                    key=f"de_total_q_{sheet_idx}",
                )

            de_ws_id = f"{sublevel_code}-{de_sheet_num}"
            total_q_int = int(de_total_q)

            de_not_attempted = st.checkbox(
                "Not attempted (student didn't do this worksheet today)",
                key=f"de_not_attempted_{student['id']}_{sheet_idx}",
            )
            if de_not_attempted:
                st.caption(f"{de_ws_id} will be logged as not attempted — no score recorded.")
                sheet_entries.append({
                    "worksheet_id": de_ws_id, "sheet_num": de_sheet_num,
                    "total_questions": 0, "wrong_qs": [],
                    "wrong_details": {}, "resolved_topics": {},
                    "remedial_id": None, "status": "not_attempted",
                })
                continue

            st.markdown(f"""
            <div style="font-size:13px;color:#888;margin:4px 0 10px">
                Worksheet: <b style="color:#111">{de_ws_id}</b>
                &nbsp;·&nbsp; {topic} &nbsp;·&nbsp; Level {level_num}
            </div>
            """, unsafe_allow_html=True)

            # Try to load correct answers for this sheet
            if _answers_available:
                try:
                    ws_items, ws_answers = _get_items_and_answers(sublevel_code, de_sheet_num, level_num)
                except Exception:
                    ws_items   = []
                    ws_answers = []
            else:
                ws_items   = []
                ws_answers = []

            # ── Wrong-answer entry: fast typed entry (default) + tap-grid fallback ──
            st.markdown(
                '<div style="font-size:11px;font-weight:600;text-transform:uppercase;'
                'letter-spacing:.06em;color:#555;margin-bottom:6px">'
                'Mark wrong answers</div>',
                unsafe_allow_html=True,
            )

            quick_key = f"de_quick_{student['id']}_{sheet_idx}"
            quick_last_key = f"de_quick_last_{student['id']}_{sheet_idx}"
            quick_val = st.text_input(
                "Type the wrong question numbers, comma-separated",
                key=quick_key,
                placeholder="e.g. 3, 7, 15 — leave blank if all correct",
            )

            # Sync typed numbers into the checkbox states below, but ONLY when
            # the typed text actually changed since last time -- otherwise a
            # manual tap in the grid (with the text box left untouched) would
            # get silently overwritten back to the old typed value on every
            # rerun, which is the bug this guard avoids.
            if st.session_state.get(quick_last_key) != quick_val:
                typed_wrong = set()
                for piece in quick_val.split(","):
                    piece = piece.strip()
                    if piece.isdigit():
                        qn = int(piece)
                        if 1 <= qn <= total_q_int:
                            typed_wrong.add(qn)
                for qn in range(1, total_q_int + 1):
                    st.session_state[f"de_q_{student['id']}_{sheet_idx}_{qn}"] = qn in typed_wrong
                st.session_state[quick_last_key] = quick_val

            de_wrong_qs = []
            already_tapped = any(
                st.session_state.get(f"de_q_{student['id']}_{sheet_idx}_{qn}")
                for qn in range(1, total_q_int + 1)
            )
            with st.expander("Prefer tapping boxes instead?", expanded=already_tapped and not quick_val.strip()):
                cols_per_row = 5
                for row_start in range(1, total_q_int + 1, cols_per_row):
                    row_cols = st.columns(cols_per_row)
                    for i, col in enumerate(row_cols):
                        qn = row_start + i
                        if qn > total_q_int:
                            break
                        with col:
                            if st.checkbox(f"Q{qn}", key=f"de_q_{student['id']}_{sheet_idx}_{qn}"):
                                de_wrong_qs.append(qn)
            # Ticks made in the tap-grid above already populated de_wrong_qs;
            # for numbers that came from typed entry (grid collapsed, so the
            # checkbox loop above still ran and appended them too since the
            # expander body still executes even when collapsed). Dedup + sort.
            de_wrong_qs = sorted(set(de_wrong_qs))

            if de_wrong_qs:
                st.caption(f"Marked wrong: {', '.join(str(q) for q in de_wrong_qs)}")
            else:
                st.caption("All correct so far.")

            # ── Intelligent wrong-answer entry ────────────────────────────────────
            de_wrong_details = {}
            if de_wrong_qs:
                st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
                st.markdown(
                    '<div style="font-size:11px;font-weight:600;text-transform:uppercase;'
                    'letter-spacing:.06em;color:#555;margin-bottom:4px">'
                    'What did the student write?</div>',
                    unsafe_allow_html=True,
                )

                cols = st.columns(len(de_wrong_qs) if len(de_wrong_qs) <= 4 else 4)
                for i, qn in enumerate(de_wrong_qs):
                    with cols[i % 4]:
                        sans = st.text_input(
                            f"Q{qn}",
                            key=f"de_ans_{student['id']}_{sheet_idx}_{qn}",
                            placeholder="wrote…",
                        )

                    # Auto-classify silently
                    q_idx    = qn - 1
                    item     = ws_items[q_idx]  if q_idx < len(ws_items)  else None
                    corr_ans = ws_answers[q_idx] if q_idx < len(ws_answers) else None
                    if sans.strip() and item and corr_ans:
                        auto_type, _, _ = mc.classify(item, corr_ans, sans.strip())
                    else:
                        auto_type = None

                    de_wrong_details[qn] = {
                        "mistake_type": auto_type,
                        "student_answer": sans.strip(),
                    }

            resolved   = db.resolve_topics(de_ws_id, de_wrong_qs, fallback_topic=topic) if de_wrong_qs else {}
            remedial_id = remedial_id_for(sublevel_code, de_sheet_num) if len(de_wrong_qs) > 3 else None

            sheet_entries.append({
                "worksheet_id": de_ws_id, "sheet_num": de_sheet_num,
                "total_questions": total_q_int, "wrong_qs": de_wrong_qs,
                "wrong_details": de_wrong_details, "resolved_topics": resolved,
                "remedial_id": remedial_id, "status": None,
            })

        # ── Save (WhatsApp send temporarily disabled — set WHATSAPP_ENABLED=True
        #    below to restore the "Save & Send to Parent" button) ────────────────
        WHATSAPP_ENABLED = False

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        whatsapp_msg = build_whatsapp_report_multi(de_name, sheet_entries)
        if WHATSAPP_ENABLED:
            st.markdown(f"""
            <div class="info-cell" style="margin-bottom:12px">
                <div class="il">Parent report preview</div>
                <div style="font-size:13px;color:#222;line-height:1.5;margin-top:6px">{whatsapp_msg}</div>
            </div>
            """, unsafe_allow_html=True)

        wa_number = student.get("parent_whatsapp")

        def _save_entry():
            """Saves all sheet entries to DB in a single batched call."""
            db.save_daily_entries(
                session_date=de_date.isoformat(),
                student_id=student["id"],
                class_name=de_class,
                grade=student["grade"],
                level_num=level_num,
                entries=sheet_entries,
            )
            # Clear this student's grids (now student-scoped, so this never
            # affects any other student's state) and auto-advance roll number
            for sidx in range(1, 3):
                for qn in range(1, 51):
                    st.session_state.pop(f"de_q_{student['id']}_{sidx}_{qn}", None)
                    st.session_state.pop(f"de_mtype_{sidx}_{qn}", None)
                    st.session_state.pop(f"de_ans_{student['id']}_{sidx}_{qn}", None)
            next_roll = min(int(roll_input) + 1, len(roster))
            st.session_state["_pending_roll_advance"] = next_roll
            return next_roll

        ws_ids_saved = ", ".join(e["worksheet_id"] for e in sheet_entries)

        if WHATSAPP_ENABLED and wa_number:
            wa_link = build_whatsapp_link(wa_number, whatsapp_msg)
            if st.button("💾 📲  Save & Send to Parent", type="primary",
                         key="de_save_and_send", use_container_width=True):
                _save_entry()
                st.session_state["_flash_toast"] = f"✅ Saved for {de_name} ({ws_ids_saved}). Opening WhatsApp…"
                st.markdown(
                    f'<meta http-equiv="refresh" content="1;url={wa_link}">',
                    unsafe_allow_html=True,
                )
                st.rerun()
        else:
            if st.button("💾  Save Entry", type="primary", key="de_save",
                         use_container_width=True):
                next_roll = _save_entry()
                # Fire the toast NOW, before the rerun, so the confirmation
                # pops the instant the save finishes rather than only after
                # the fragment finishes redrawing. The save above is fully
                # synchronous and already committed by this point -- this is
                # honest feedback, not an optimistic guess.
                st.toast(
                    f"✅ Saved for {de_name} ({ws_ids_saved}). Next → Roll #{next_roll}",
                    icon="✅",
                )
                st.rerun()

        st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)



_daily_entry_fragment(level_num, sublevel_code, topic)

st.markdown('</div>', unsafe_allow_html=True)
ui_common.render_footer(level_num, sublevel_code)
