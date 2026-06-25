"""
pages/1_Daily_Entry.py — Standalone staff workspace for Fear Less Maths.

This is a separate PAGE of the same Streamlit app as app.py (Streamlit's
multipage convention: anything in pages/ gets its own URL, e.g.
yourapp.streamlit.app/Daily_Entry, while app.py stays at the root URL).

Because it's part of the same deployment, it runs in the same process and
shares the exact same filesystem — so it reads/writes the SAME db.py /
flm_data.db as the teacher's main app. Anything entered here shows up
immediately in the teacher's Student Profile tab, and feeds the WhatsApp
parent reports below. No second database, no sync step.

This is the ONE tool associate staff need day to day:
  1. Manage Students — add a new student, bulk-import a class list, or
     look up/update a parent's WhatsApp number, any time (not just once).
  2. Daily Entry — pick a student + worksheet, mark wrong answers on a
     simple tap grid, save it (feeds the dashboard), and send the parent
     WhatsApp report.

Deliberately NOT included here: the Demo/Test Data panel (stays on the
teacher's app, since it can wipe all student data).
"""
import streamlit as st
import pandas as pd
from datetime import date as _date

import db
import ui_common
from levels_data import SHEET_OPTIONS
from ws_helpers import remedial_id_for, build_whatsapp_report, build_whatsapp_link, MISTAKE_TYPES

ui_common.setup_page("Daily Entry — Fear Less Maths")
ui_common.render_header(
    subtitle="Daily Entry · Staff",
    badge="Manage students & log today's worksheet results",
)
level_num, sublevel_code, topic = ui_common.render_level_selector(key_prefix="de_page_")

st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# 1. MANAGE STUDENTS — always available, not just a one-time setup
# ═══════════════════════════════════════════════════════════════════════════
with st.expander("👥 Manage Students — add new students, bulk import, or update a WhatsApp number",
                  expanded=(not db.get_classes())):
    mgmt_mode = st.radio(
        "Action", ["Add one student", "Bulk import a class", "View / edit roster"],
        horizontal=True, key="mgmt_mode", label_visibility="collapsed",
    )

    if mgmt_mode == "Add one student":
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            new_name = st.text_input("Student name", key="new_student_name")
            new_class = st.text_input("Class", key="new_student_class", placeholder="e.g. Class 7")
        with col_a2:
            new_grade = st.number_input("Grade", min_value=1, max_value=12, value=1, key="new_student_grade")
            new_wa = st.text_input("Parent WhatsApp number", key="new_student_wa",
                                   placeholder="e.g. 7036525875 (optional, can add later)")
        if st.button("➕  Add Student", type="primary", key="add_one_student"):
            if not new_name.strip() or not new_class.strip():
                st.error("Name and Class are required.")
            else:
                db.add_student(new_name.strip(), new_class.strip(), int(new_grade), new_wa.strip() or None)
                st.success(f"Added {new_name.strip()} to {new_class.strip()}.")
                for k in ("new_student_name", "new_student_class", "new_student_wa"):
                    st.session_state.pop(k, None)
                st.rerun()

    elif mgmt_mode == "Bulk import a class":
        st.caption("Upload a roster file, or paste directly. Format per line:  Name, Class, Grade, Parent WhatsApp number")
        roster_file = st.file_uploader("Upload a .txt roster file", type=["txt"], key="roster_file_upload")
        roster_text = st.text_area(
            "Or paste here instead",
            placeholder="Ravi Kumar, Class 7, 7, 7036525875\nMeena, Class 7, 7, 9812345678\nArjun, Class 5, 5, 9876543210",
            height=150, key="roster_text_bulk", label_visibility="collapsed",
        )
        if roster_file is not None:
            source_text = roster_file.getvalue().decode("utf-8")
            st.caption(f"📄 Using uploaded file: {roster_file.name} "
                      f"({len(source_text.strip().splitlines())} lines)")
        else:
            source_text = roster_text

        if st.button("📋  Import Roster", type="primary", key="import_roster_bulk"):
            rows, errs = [], []
            for i, line in enumerate(source_text.strip().splitlines(), 1):
                if not line.strip():
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) < 3:
                    errs.append(f"Line {i}: need at least Name, Class, Grade")
                    continue
                rows.append({
                    "name": parts[0], "class_name": parts[1], "grade": parts[2],
                    "parent_whatsapp": parts[3] if len(parts) > 3 else "",
                })
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
            st.caption("No students yet — use \"Add one student\" or \"Bulk import a class\" above.")
        else:
            vc = st.selectbox("Class", view_classes, key="mgmt_view_class")
            roster_view = db.get_students(vc)
            st.caption(f"{len(roster_view)} students in {vc}")
            view_df = pd.DataFrame([{
                "Name": s["name"],
                "Grade": s["grade"],
                "Parent WhatsApp": s.get("parent_whatsapp") or "— not on file —",
            } for s in roster_view])
            st.dataframe(view_df, hide_index=True, width='stretch')

            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
            st.caption("Update a parent's WhatsApp number:")
            col_e1, col_e2 = st.columns([1, 1])
            with col_e1:
                edit_pick = st.selectbox("Student", [s["name"] for s in roster_view],
                                         key="mgmt_edit_pick", label_visibility="collapsed")
            edit_student = next(s for s in roster_view if s["name"] == edit_pick)
            with col_e2:
                new_wa_val = st.text_input(
                    "WhatsApp number", value=edit_student.get("parent_whatsapp") or "",
                    key=f"mgmt_wa_input_{edit_student['id']}", placeholder="e.g. 7036525875",
                    label_visibility="collapsed",
                )
            if st.button("💾  Save WhatsApp Number", key="mgmt_wa_save"):
                db.update_parent_whatsapp(edit_student["id"], new_wa_val)
                st.success(f"Updated {edit_pick}'s WhatsApp number.")
                st.rerun()

st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# 2. DAILY ENTRY
# ═══════════════════════════════════════════════════════════════════════════
existing_classes = db.get_classes()

if not existing_classes:
    st.info("No students yet — add your first student above (\"Manage Students\") to begin daily entry.")
else:
    st.markdown("##### Daily Entry")
    st.caption("Pick a student and the worksheet they did, then tap any questions they got wrong. "
               "Topics, remedial worksheet and the parent report fill in automatically.")

    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        de_class = st.selectbox("Class", existing_classes, key="de_class")
    roster = db.get_students(de_class)
    with col_d2:
        de_name = st.selectbox("Student", [s["name"] for s in roster], key="de_name")
    student = next(s for s in roster if s["name"] == de_name)

    # missing-number nudge
    if not student.get("parent_whatsapp"):
        wa_in = st.text_input(f"Parent WhatsApp number for {de_name} (not on file)",
                              key="de_add_wa", placeholder="e.g. 7036525875")
        if wa_in.strip():
            db.update_parent_whatsapp(student["id"], wa_in)
            st.rerun()

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    col_w1, col_w2, col_w3 = st.columns([1, 1, 1])
    with col_w1:
        de_date = st.date_input("Date", value=_date.today(), key="de_date")
    with col_w2:
        de_sheet_lbls = [lbl for _, lbl in SHEET_OPTIONS]
        de_sheet_sel = st.selectbox("Sheet", de_sheet_lbls, key="de_sheet")
        de_sheet_num = SHEET_OPTIONS[de_sheet_lbls.index(de_sheet_sel)][0]
    with col_w3:
        de_total_q = st.number_input("Total Qs", min_value=1, max_value=50, value=20, key="de_total_q")

    de_ws_id = f"{sublevel_code}-{de_sheet_num}"
    st.markdown(f"""
    <div style="font-size:13px;color:#888;margin:4px 0 10px">
        Worksheet: <b style="color:#111">{de_ws_id}</b> &nbsp;·&nbsp; {topic} &nbsp;·&nbsp; Level {level_num}
    </div>
    """, unsafe_allow_html=True)

    # ── Wrong-answer grid — tap a question number if the student got it wrong ──
    st.markdown(
        '<div style="font-size:11px;font-weight:600;text-transform:uppercase;'
        'letter-spacing:.06em;color:#555;margin-bottom:6px">'
        'Mark wrong answers (leave unchecked = correct)</div>',
        unsafe_allow_html=True,
    )
    de_wrong_qs = []
    total_q_int = int(de_total_q)
    cols_per_row = 5
    for row_start in range(1, total_q_int + 1, cols_per_row):
        row_cols = st.columns(cols_per_row)
        for i, col in enumerate(row_cols):
            qn = row_start + i
            if qn > total_q_int:
                break
            with col:
                if st.checkbox(f"Q{qn}", key=f"de_q_{qn}"):
                    de_wrong_qs.append(qn)
    de_wrong_qs.sort()
    if de_wrong_qs:
        st.caption(f"Marked wrong: {', '.join(str(q) for q in de_wrong_qs)}")
    else:
        st.caption("All correct so far.")

    # ── For each wrong answer: WHAT kind of mistake, and what did they write? ──
    # This is what lets the Student Profile show how a child is thinking
    # (concept gap vs calculation slip vs carelessness), not just what topic
    # they got wrong.
    de_wrong_details = {}
    if de_wrong_qs:
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:11px;font-weight:600;text-transform:uppercase;'
            'letter-spacing:.06em;color:#555;margin-bottom:6px">'
            'For each wrong answer — what kind of mistake was it?</div>',
            unsafe_allow_html=True,
        )
        for qn in de_wrong_qs:
            col_m1, col_m2 = st.columns([1, 1.4])
            with col_m1:
                mtype = st.selectbox(
                    f"Q{qn} mistake type", MISTAKE_TYPES, key=f"de_mtype_{qn}",
                    label_visibility="collapsed" if qn != de_wrong_qs[0] else "visible",
                )
            with col_m2:
                sans = st.text_input(
                    f"Q{qn} — what did they write? (optional)", key=f"de_ans_{qn}",
                    placeholder=f"Q{qn}: what they actually wrote (optional)",
                    label_visibility="collapsed" if qn != de_wrong_qs[0] else "visible",
                )
            de_wrong_details[qn] = {"mistake_type": mtype, "student_answer": sans}

    resolved = db.resolve_topics(de_ws_id, de_wrong_qs, fallback_topic=topic) if de_wrong_qs else {}
    remedial_id = remedial_id_for(sublevel_code, de_sheet_num) if len(de_wrong_qs) > 3 else None
    whatsapp_msg = build_whatsapp_report(
        de_name, de_ws_id, total_q_int, de_wrong_qs, resolved, remedial_id
    )

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-cell" style="margin-bottom:12px">
        <div class="il">Parent report preview</div>
        <div style="font-size:13px;color:#222;line-height:1.5;margin-top:6px">{whatsapp_msg}</div>
    </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2 = st.columns([1, 1])
    with col_s1:
        if st.button("💾  Save Entry", type="primary", key="de_save"):
            new_session_id = db.add_session(
                session_date=de_date.isoformat(), student_id=student["id"],
                class_name=de_class, grade=student["grade"], level_num=level_num,
                worksheet_id=de_ws_id, wrong_qs=de_wrong_qs, resolved_topics=resolved,
                total_questions=total_q_int, remedial_id=remedial_id,
            )
            if de_wrong_details:
                db.save_wrong_answer_details(new_session_id, de_wrong_details)
            st.session_state["de_saved"] = de_name
            # Clear the wrong-answer grid + mistake details so the next student starts fresh.
            for qn in range(1, 51):
                st.session_state.pop(f"de_q_{qn}", None)
                st.session_state.pop(f"de_mtype_{qn}", None)
                st.session_state.pop(f"de_ans_{qn}", None)
            st.success(f"Saved entry for {de_name}.")
            st.rerun()

    with col_s2:
        wa_number = student.get("parent_whatsapp")
        if wa_number:
            wa_link = build_whatsapp_link(wa_number, whatsapp_msg)
            st.markdown(f"""
            <a href="{wa_link}" target="_blank" style="text-decoration:none">
              <div style="background:#25D366;color:#fff;text-align:center;
                          padding:14px 0;border-radius:8px;font-weight:600;font-size:15px">
                📲 Send to Parent
              </div>
            </a>
            """, unsafe_allow_html=True)
        else:
            st.caption("No parent number on file — add one above (in Manage Students) to enable sending.")

    st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
ui_common.render_footer(level_num, sublevel_code)
