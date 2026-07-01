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
        "Action", ["Add one student", "Bulk import a class", "View / edit roster"],
        horizontal=True, key="mgmt_mode", label_visibility="collapsed",
    )

    if mgmt_mode == "Add one student":
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
existing_classes = db.get_classes()

if not existing_classes:
    st.info("No students yet — add your first student above.")
else:
    st.markdown("##### Daily Entry")

    # ── Class + serial number student picker ──────────────────────────────────
    col_d1, col_d2, col_d3 = st.columns([1.2, 0.8, 1.5])
    with col_d1:
        de_class = st.selectbox("Class", existing_classes, key="de_class")

    roster = db.get_students(de_class)

    with col_d2:
        # Show roll number range as hint
        roll_input = st.number_input(
            f"Roll No (1–{len(roster)})",
            min_value=1, max_value=len(roster),
            value=1, step=1, key="de_roll",
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

    de_sheet_lbls = [lbl for _, lbl in SHEET_OPTIONS]
    de_num_sheets = st.radio(
        "Worksheets today", [1, 2], index=1, horizontal=True, key="de_num_sheets",
        format_func=lambda n: "1 worksheet" if n == 1 else "2 worksheets (default)",
    )

    # ── Pre-load question items + correct answers for this level/sublevel ─────
    try:
        from content import get_questions as _gq
        from answer_key import derive_answer_and_explanation as _dae
        _items_cache = {}
        def _get_items(code, sheet, lvl):
            key = (code, sheet, lvl)
            if key not in _items_cache:
                raw = _gq(code, sheet, lvl)
                _items_cache[key] = [
                    it for it in raw
                    if it.get("type") not in ("concept_box", "tips_box")
                ]
            return _items_cache[key]
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

        st.markdown(f"""
        <div style="font-size:13px;color:#888;margin:4px 0 10px">
            Worksheet: <b style="color:#111">{de_ws_id}</b>
            &nbsp;·&nbsp; {topic} &nbsp;·&nbsp; Level {level_num}
        </div>
        """, unsafe_allow_html=True)

        # Try to load correct answers for this sheet
        if _answers_available:
            try:
                ws_items    = _get_items(sublevel_code, de_sheet_num, level_num)
                ws_answers  = [_dae(it)[0] for it in ws_items]
            except Exception:
                ws_items   = []
                ws_answers = []
        else:
            ws_items   = []
            ws_answers = []

        # ── Wrong-answer grid ─────────────────────────────────────────────────
        st.markdown(
            '<div style="font-size:11px;font-weight:600;text-transform:uppercase;'
            'letter-spacing:.06em;color:#555;margin-bottom:6px">'
            'Mark wrong answers</div>',
            unsafe_allow_html=True,
        )
        de_wrong_qs = []
        cols_per_row = 5
        for row_start in range(1, total_q_int + 1, cols_per_row):
            row_cols = st.columns(cols_per_row)
            for i, col in enumerate(row_cols):
                qn = row_start + i
                if qn > total_q_int:
                    break
                with col:
                    if st.checkbox(f"Q{qn}", key=f"de_q_{sheet_idx}_{qn}"):
                        de_wrong_qs.append(qn)
        de_wrong_qs.sort()

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
                'What did the student write?  '
                '<span style="font-weight:400;text-transform:none;font-size:10px;color:#888">'
                '— App will auto-detect mistake type</span></div>',
                unsafe_allow_html=True,
            )

            for qn in de_wrong_qs:
                # Correct answer for this question (0-indexed)
                q_idx = qn - 1
                item     = ws_items[q_idx]   if q_idx < len(ws_items)   else None
                corr_ans = ws_answers[q_idx]  if q_idx < len(ws_answers) else None

                col_q, col_ans, col_type, col_conf = st.columns([0.5, 1.5, 1.5, 0.8])

                with col_q:
                    st.markdown(
                        f'<div style="padding-top:28px;font-size:13px;'
                        f'font-weight:700;color:#333">Q{qn}</div>',
                        unsafe_allow_html=True,
                    )

                with col_ans:
                    sans = st.text_input(
                        f"Student wrote (Q{qn})",
                        key=f"de_ans_{sheet_idx}_{qn}",
                        placeholder="what they wrote…",
                        label_visibility="visible" if qn == de_wrong_qs[0] else "collapsed",
                    )

                # Auto-classify if student answer is entered and we have question data
                auto_type, auto_conf, auto_reason = None, None, None
                if sans.strip() and item and corr_ans:
                    auto_type, auto_conf, auto_reason = mc.classify(
                        item, corr_ans, sans.strip()
                    )

                # Show auto-detected type (or dropdown override)
                with col_type:
                    if auto_type:
                        # Show auto-detected as default selection
                        default_idx = mc.MISTAKE_TYPES.index(auto_type) \
                            if auto_type in mc.MISTAKE_TYPES else 0
                    else:
                        default_idx = 0

                    override_key = f"de_mtype_{sheet_idx}_{qn}"
                    current_override = st.session_state.get(override_key)
                    if current_override and current_override != auto_type:
                        # Staff already manually overrode
                        sel_idx = mc.MISTAKE_TYPES.index(current_override) \
                            if current_override in mc.MISTAKE_TYPES else default_idx
                    else:
                        sel_idx = default_idx

                    mtype = st.selectbox(
                        f"Mistake type (Q{qn})",
                        mc.MISTAKE_TYPES,
                        index=sel_idx,
                        key=override_key,
                        label_visibility="visible" if qn == de_wrong_qs[0] else "collapsed",
                    )

                with col_conf:
                    if auto_type and auto_conf:
                        conf_color = {
                            "high": "#2E6B5E", "medium": "#CC7000", "low": "#B71C1C"
                        }.get(auto_conf, "#888")
                        conf_label = {"high": "✓ Sure", "medium": "~ Likely", "low": "? Check"}.get(auto_conf, "")
                        st.markdown(
                            f'<div style="padding-top:{"28px" if qn == de_wrong_qs[0] else "8px"};'
                            f'font-size:11px;font-weight:700;color:{conf_color}">'
                            f'{conf_label}</div>',
                            unsafe_allow_html=True,
                        )
                        if auto_reason:
                            st.caption(auto_reason[:80])
                    else:
                        st.markdown(
                            f'<div style="padding-top:{"28px" if qn == de_wrong_qs[0] else "8px"};'
                            f'font-size:11px;color:#aaa">Enter answer above</div>',
                            unsafe_allow_html=True,
                        )

                de_wrong_details[qn] = {
                    "mistake_type": mtype,
                    "student_answer": sans.strip(),
                }

        resolved   = db.resolve_topics(de_ws_id, de_wrong_qs, fallback_topic=topic) if de_wrong_qs else {}
        remedial_id = remedial_id_for(sublevel_code, de_sheet_num) if len(de_wrong_qs) > 3 else None

        sheet_entries.append({
            "worksheet_id": de_ws_id, "sheet_num": de_sheet_num,
            "total_questions": total_q_int, "wrong_qs": de_wrong_qs,
            "wrong_details": de_wrong_details, "resolved_topics": resolved,
            "remedial_id": remedial_id,
        })

    # ── Save + Send (single combined action) ─────────────────────────────────
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    whatsapp_msg = build_whatsapp_report_multi(de_name, sheet_entries)
    st.markdown(f"""
    <div class="info-cell" style="margin-bottom:12px">
        <div class="il">Parent report preview</div>
        <div style="font-size:13px;color:#222;line-height:1.5;margin-top:6px">{whatsapp_msg}</div>
    </div>
    """, unsafe_allow_html=True)

    wa_number = student.get("parent_whatsapp")

    def _save_entry():
        """Saves all sheet entries to DB. Called from both buttons below."""
        for entry in sheet_entries:
            new_session_id = db.add_session(
                session_date=de_date.isoformat(),
                student_id=student["id"],
                class_name=de_class,
                grade=student["grade"],
                level_num=level_num,
                worksheet_id=entry["worksheet_id"],
                wrong_qs=entry["wrong_qs"],
                resolved_topics=entry["resolved_topics"],
                total_questions=entry["total_questions"],
                remedial_id=entry["remedial_id"],
            )
            if entry["wrong_details"]:
                db.save_wrong_answer_details(new_session_id, entry["wrong_details"])
        # Clear grids and auto-advance roll number
        for sidx in range(1, 3):
            for qn in range(1, 51):
                st.session_state.pop(f"de_q_{sidx}_{qn}", None)
                st.session_state.pop(f"de_mtype_{sidx}_{qn}", None)
                st.session_state.pop(f"de_ans_{sidx}_{qn}", None)
        st.session_state["de_roll"] = min(int(roll_input) + 1, len(roster))

    ws_ids_saved = ", ".join(e["worksheet_id"] for e in sheet_entries)

    if wa_number:
        wa_link = build_whatsapp_link(wa_number, whatsapp_msg)
        if st.button("💾 📲  Save & Send to Parent", type="primary",
                     key="de_save_and_send", use_container_width=True):
            _save_entry()
            st.success(f"✅ Saved for {de_name} ({ws_ids_saved}). Opening WhatsApp…")
            st.markdown(
                f'<meta http-equiv="refresh" content="1;url={wa_link}">',
                unsafe_allow_html=True,
            )
            st.rerun()
    else:
        if st.button("💾  Save Entry", type="primary", key="de_save",
                     use_container_width=True):
            _save_entry()
            st.success(f"✅ Saved for {de_name} ({ws_ids_saved}). Next → Roll #{st.session_state['de_roll']}")
            st.rerun()
        st.caption("No parent number on file — add one in Manage Students to enable WhatsApp sending.")

    st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
ui_common.render_footer(level_num, sublevel_code)
