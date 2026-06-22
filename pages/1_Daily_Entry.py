"""
pages/1_Daily_Entry.py — Standalone Daily Entry screen for associate staff.

This is a separate PAGE of the same Streamlit app as app.py (Streamlit's
multipage convention: anything in pages/ gets its own URL, e.g.
yourapp.streamlit.app/Daily_Entry, while app.py stays at the root URL).

Because it's part of the same deployment, it runs in the same process and
shares the exact same filesystem — so it reads/writes the SAME db.py /
flm_data.db as the teacher's main app. An entry staff log here shows up
immediately in the teacher's Student Profile tab. No second database, no
sync step, nothing to keep in sync manually.

This page deliberately does NOT include the Demo/Test Data panel (that
stays on the teacher's app, since it can wipe all student data) — staff
only ever see the roster-import / daily-entry flow below.
"""
import streamlit as st
import pandas as pd
from datetime import date as _date

import db
import ui_common
from levels_data import SHEET_OPTIONS
from ws_helpers import remedial_id_for, build_whatsapp_report, build_whatsapp_link

ui_common.setup_page("Daily Entry — Fear Less Maths")
ui_common.render_header(
    subtitle="Daily Entry · Staff",
    badge="Log today's worksheet results",
)
level_num, sublevel_code, topic = ui_common.render_level_selector(key_prefix="de_page_")

st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)

existing_classes = db.get_classes()

# ── First-run: roster setup ────────────────────────────────────────────────
if not existing_classes:
    st.markdown("##### Set up your class roster (one time)")
    st.caption("Paste your students once. Format per line:  Name, Class, Grade, Parent WhatsApp number")
    roster_text = st.text_area(
        "Roster",
        placeholder="Ravi Kumar, Class A, 7, 7036525875\nMeena, Class A, 7, 9812345678\nArjun, Class B, 5, 9876543210",
        height=160, key="roster_text", label_visibility="collapsed",
    )
    if st.button("📋  Import Roster", type="primary", key="import_roster"):
        rows = []
        errs = []
        for i, line in enumerate(roster_text.strip().splitlines(), 1):
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
            st.success(f"Imported {res['added']} students. Reloading…")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # ── Daily entry flow ───────────────────────────────────────────────────
    st.markdown("##### Daily Entry")
    st.caption("Pick a student, the worksheet they did, and type the wrong question numbers. "
               "Topics, remedial and the parent report fill in automatically.")

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

    de_wrong_str = st.text_input(
        "Wrong question numbers (comma-separated · leave blank if all correct)",
        key="de_wrong_qs", placeholder="e.g. 17, 18",
    )

    de_wrong_qs, de_err = [], None
    if de_wrong_str.strip():
        for part in de_wrong_str.split(","):
            part = part.strip()
            if not part:
                continue
            if not part.isdigit():
                de_err = f"'{part}' is not a valid question number"; break
            qn = int(part)
            if qn < 1 or qn > de_total_q:
                de_err = f"Q{qn} is out of range (1–{de_total_q})"; break
            de_wrong_qs.append(qn)
    if de_err:
        st.error(de_err)

    if not de_err:
        resolved = db.resolve_topics(de_ws_id, de_wrong_qs, fallback_topic=topic) if de_wrong_qs else {}
        remedial_id = remedial_id_for(sublevel_code, de_sheet_num) if de_wrong_qs else None
        whatsapp_msg = build_whatsapp_report(
            de_name, de_ws_id, int(de_total_q), de_wrong_qs, resolved, remedial_id
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
                db.add_session(
                    session_date=de_date.isoformat(), student_id=student["id"],
                    class_name=de_class, grade=student["grade"], level_num=level_num,
                    worksheet_id=de_ws_id, wrong_qs=de_wrong_qs, resolved_topics=resolved,
                    total_questions=int(de_total_q), remedial_id=remedial_id,
                )
                st.session_state["de_saved"] = de_name
                st.success(f"Saved entry for {de_name}.")

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
                st.caption("No parent number on file — add one above to enable sending.")

    st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

ui_common.render_footer(level_num, sublevel_code)
