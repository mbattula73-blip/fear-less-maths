"""
Fear Less Maths — Final Production App
LA Excellence Schools / IDPS Orchards

This is the TEACHER's full control panel: worksheet generation, concept
tagging, and the Student Profile dashboard. Daily Entry lives on its own
page now (pages/1_Daily_Entry.py) for associate staff — see ui_common.py
for why both pages safely share the same live database.
"""
import streamlit as st
from levels_data import LEVELS, SUBLEVELS, SHEET_OPTIONS, get_tier
from pdf_engine import build_pdf
import db
import analytics
import concept_tagger
from ws_helpers import numbered_questions, remedial_id_for, build_whatsapp_report
import ui_common

ui_common.setup_page("Fear Less Maths", hide_nav=False)
ui_common.render_header()
level_num, sublevel_code, topic = ui_common.render_level_selector()

# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "  Generate Single Worksheet  ", "  Batch — All 8 Sheets  ",
    "  🏷️ Concept Tags  ", "  👤 Student Profile  ",
])

# ─── TAB 1 ────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    # Sheet selector
    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        sheet_lbls = [lbl for _, lbl in SHEET_OPTIONS]
        sheet_sel  = st.selectbox("Sheet", sheet_lbls, label_visibility="visible")
        sheet_num  = SHEET_OPTIONS[sheet_lbls.index(sheet_sel)][0]

    tier  = get_tier(sheet_num)
    ws_id = f"{sublevel_code}-{sheet_num}"
    is_r  = sheet_num.endswith("R")
    base  = int(sheet_num.replace("R",""))

    # Worksheet hero card
    st.markdown(f"""
    <div class="ws-hero">
        <div>
            <div style="font-size:10px;color:#555;text-transform:uppercase;
                        letter-spacing:.08em;margin-bottom:6px">Worksheet</div>
            <div class="ws-hero-id">{ws_id}</div>
        </div>
        <div class="ws-hero-meta">
            <div class="ws-hero-topic">{topic}</div>
            <div class="ws-hero-tier">{tier}</div>
            <div style="font-size:10px;color:#333;margin-top:6px">LA Excellence Schools</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tier track
    steps = [("1","See it","Intuition"),("2","Try it","Concept"),
             ("3","Do it","Practice"),("4","Master it","Mastery")]
    track = '<div class="tier-track">'
    for num, name, sub_name in steps:
        active = "on" if str(base) == num else ""
        suffix = "R" if is_r and str(base)==num else ""
        track += (f'<div class="tier-step {active}">'
                  f'<span class="tn">Sheet {num}{suffix}</span>'
                  f'<span class="tnm">{name}</span>'
                  f'</div>')
    track += '</div>'
    st.markdown(track, unsafe_allow_html=True)

    # Info row
    st.markdown(f"""
    <div class="info-row">
        <div class="info-cell">
            <div class="il">Level</div>
            <div class="iv">Level {level_num}</div>
        </div>
        <div class="info-cell">
            <div class="il">Domain</div>
            <div class="iv">{LEVELS[level_num]['name']}</div>
        </div>
        <div class="info-cell">
            <div class="il">Topic</div>
            <div class="iv">{topic}</div>
        </div>
        <div class="info-cell">
            <div class="il">Format</div>
            <div class="iv">20 Qs · A4</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tier guide
    st.markdown("""
    <div class="tier-guide">
        <div class="tg-item"><div class="tg-pip" style="background:#888"></div>Sheet 1 — Intuition</div>
        <div class="tg-item"><div class="tg-pip" style="background:#777"></div>Sheet 2 — Concept</div>
        <div class="tg-item"><div class="tg-pip" style="background:#555"></div>Sheet 3 — Practice</div>
        <div class="tg-item"><div class="tg-pip" style="background:#333"></div>Sheet 4 — Mastery</div>
        <div class="tg-item"><div class="tg-pip" style="background:#222;border:1px dashed #555"></div>R — Remedial</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    # Generate + download
    col_btn, col_pad = st.columns([2, 1])
    with col_btn:
        if st.button(f"⚡  Generate  {ws_id}.pdf", type="primary", key="gen"):
            with st.spinner(f"Generating {ws_id}…"):
                try:
                    pdf_bytes = build_pdf(level_num, sublevel_code, sheet_num).read()
                    st.session_state["pdf_ready"]  = pdf_bytes
                    st.session_state["pdf_ws_id"]  = ws_id
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.exception(e)

        if st.session_state.get("pdf_ws_id") == ws_id and "pdf_ready" in st.session_state:
            size_kb = len(st.session_state["pdf_ready"]) // 1024
            st.markdown(f"""
            <div class="success-card">
                <div class="ck">✓</div>
                <div>{ws_id}.pdf is ready &nbsp;·&nbsp; {size_kb} KB</div>
            </div>
            """, unsafe_allow_html=True)

            st.download_button(
                label=f"⬇  Download  {ws_id}.pdf",
                data=st.session_state["pdf_ready"],
                file_name=f"{ws_id}.pdf",
                mime="application/pdf",
                key="dl_s",
            )

    st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)


# ─── TAB 2 ────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin:0 24px">
        <div class="ws-hero">
            <div>
                <div style="font-size:10px;color:#555;text-transform:uppercase;
                            letter-spacing:.08em;margin-bottom:6px">Batch Generation</div>
                <div class="ws-hero-id">{sublevel_code}</div>
                <div style="font-size:13px;color:#888;margin-top:4px">{topic}</div>
            </div>
            <div class="ws-hero-meta">
                <div class="ws-hero-topic">8 worksheets</div>
                <div class="ws-hero-tier">Sheets 1 · 2 · 3 · 4 · 1R · 2R · 3R · 4R</div>
                <div style="font-size:10px;color:#333;margin-top:6px">
                    Level {level_num} — {LEVELS[level_num]['name']}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

    col_b1, col_b2 = st.columns([2, 1])
    with col_b1:
        if st.button(f"⚡  Generate All 8 Sheets for {sublevel_code}", type="primary", key="batch"):
            sheets  = ["1","2","3","4","1R","2R","3R","4R"]
            results = {}
            prog    = st.progress(0, text="Starting…")
            for i, sn in enumerate(sheets):
                prog.progress((i+1)/8, text=f"Building {sublevel_code}-{sn}…")
                try:
                    results[sn] = build_pdf(level_num, sublevel_code, sn).read()
                except Exception as e:
                    st.warning(f"⚠ {sublevel_code}-{sn}: {e}")
            prog.empty()

            if results:
                st.session_state["batch_results"] = results
                st.session_state["batch_sub"]     = sublevel_code

        if st.session_state.get("batch_sub") == sublevel_code and "batch_results" in st.session_state:
            results  = st.session_state["batch_results"]
            total_kb = sum(len(v) for v in results.values()) // 1024
            st.markdown(f"""
            <div class="success-card">
                <div class="ck">✓</div>
                <div>{len(results)} worksheets ready &nbsp;·&nbsp; {total_kb} KB total</div>
            </div>
            """, unsafe_allow_html=True)

            names = {"1":"See it","2":"Try it","3":"Do it","4":"Master",
                     "1R":"Redo 1","2R":"Redo 2","3R":"Redo 3","4R":"Redo 4"}

            row1 = st.columns(4)
            row2 = st.columns(4)
            all_rows = [row1, row2]
            for idx, (sn, data) in enumerate(list(results.items())):
                row, col = idx // 4, idx % 4
                with all_rows[row][col]:
                    st.markdown(f"""
                    <div style="text-align:center;margin-bottom:6px">
                        <div style="font-family:'Playfair Display',serif;font-size:15px;
                                    font-weight:700;color:#111">{sublevel_code}-{sn}</div>
                        <div style="font-size:10px;color:#AAA">{names.get(sn,'')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.download_button(
                        label="⬇ Download",
                        data=data,
                        file_name=f"{sublevel_code}-{sn}.pdf",
                        mime="application/pdf",
                        key=f"b_{sn}",
                    )

    st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)

# ─── TAB 3 — CONCEPT TAGS ───────────────────────────────────────────────────────
with tab3:
    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)

    st.markdown("##### Concept Tags")
    st.caption(
        "Each question can be tagged with the specific concept it tests (e.g. 'HCF' vs "
        "'LCM' within the same mixed worksheet). This makes wrong-answer reports and the "
        "Dashboard's 'struggling topics' chart genuinely specific instead of just repeating "
        "the worksheet name. Tags below are auto-suggested from the question text — edit any "
        "that need it, then save. Sheets 2–4 and remedial sheets reuse sheet 1's tags "
        "automatically, so tagging sheet 1 is usually enough."
    )

    col_t1, col_t2 = st.columns([1, 3])
    with col_t1:
        # Only non-remedial sheets (1-4) — remedials inherit tags automatically.
        ct_base_sheets = [(sn, lbl) for sn, lbl in SHEET_OPTIONS if not str(sn).endswith("R")]
        ct_sheet_lbls = [lbl for _, lbl in ct_base_sheets]
        ct_sheet_sel = st.selectbox("Sheet", ct_sheet_lbls, key="ct_sheet")
        ct_sheet_num = ct_base_sheets[ct_sheet_lbls.index(ct_sheet_sel)][0]

    ct_ws_id = f"{sublevel_code}-{ct_sheet_num}"
    with col_t2:
        st.markdown(f"""
        <div style="padding-top:28px;font-size:13px;color:#888">
            Worksheet: <b style="color:#111">{ct_ws_id}</b> &nbsp;·&nbsp; {topic} &nbsp;·&nbsp; Level {level_num}
        </div>
        """, unsafe_allow_html=True)

    ct_nq = numbered_questions(sublevel_code, ct_sheet_num)
    ct_existing = db.get_worksheet_tags(ct_ws_id)

    if not ct_nq:
        st.warning("No questions found for this worksheet.")
    else:
        if st.button("🔄  Re-suggest tags from question text", key="ct_resuggest"):
            st.session_state["ct_suggested"] = concept_tagger.auto_tag_worksheet(ct_nq, topic)
            st.session_state["ct_suggested_for"] = ct_ws_id

        # Use existing DB tags if present; otherwise auto-suggest fresh ones.
        if st.session_state.get("ct_suggested_for") == ct_ws_id:
            ct_tags = st.session_state["ct_suggested"]
        elif ct_existing:
            ct_tags = {qn: ct_existing.get(qn, topic) for qn, _ in ct_nq}
        else:
            ct_tags = concept_tagger.auto_tag_worksheet(ct_nq, topic)

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

        edited = {}
        for qn, preview in ct_nq:
            c1, c2 = st.columns([3, 1.3])
            with c1:
                st.markdown(
                    f'<div style="font-size:13px;color:#333;padding-top:9px">'
                    f'<b>Q{qn}.</b> {preview}</div>',
                    unsafe_allow_html=True,
                )
            with c2:
                edited[qn] = st.text_input(
                    f"Tag Q{qn}", value=ct_tags.get(qn, topic),
                    key=f"ct_tag_{ct_ws_id}_{qn}", label_visibility="collapsed",
                )

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        col_save, col_status = st.columns([1, 2])
        with col_save:
            if st.button("💾  Save Tags", type="primary", key="ct_save"):
                db.set_worksheet_tags(ct_ws_id, edited)
                st.session_state.pop("ct_suggested_for", None)
                st.success(f"Saved {len(edited)} tags for {ct_ws_id}.")
        with col_status:
            n_specific = sum(1 for v in edited.values() if v != topic)
            st.caption(f"{n_specific} of {len(edited)} questions have a specific tag "
                      f"(others default to '{topic}').")

    st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── TAB 4 — STUDENT PROFILE ───────────────────────────────────────────────────
with tab4:
    import pandas as pd
    from datetime import date as _date

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)

    with st.expander("🧪 Demo / Test Data — temporary, for testing only"):
        st.caption(
            "Generates 300 fake students (30 per class, Class 1–10) with a realistic "
            "worksheet history, so you can try out this tab before adding your real "
            "roster and parent WhatsApp numbers. (Kept here, not on the staff Daily "
            "Entry page, since it can wipe data.)"
        )
        col_demo1, col_demo2 = st.columns(2)
        with col_demo1:
            if st.button("👥  Generate 300 demo students", key="gen_demo"):
                with st.spinner("Creating 300 students and their worksheet history… this can take a minute."):
                    from seed_demo_data import generate_demo_data
                    demo_result = generate_demo_data()
                st.success(
                    f"Created {demo_result['students_created']} students and "
                    f"{demo_result['sessions_created']} worksheet sessions."
                )
                st.rerun()
        with col_demo2:
            confirm_wipe = st.checkbox("I understand this deletes ALL students & history", key="confirm_wipe")
            if st.button("⚠️  Wipe all data", key="wipe_data", disabled=not confirm_wipe):
                db.wipe_student_data()
                st.success("All student data wiped. Add your real roster on the Daily Entry page, or regenerate demo data.")
                st.rerun()

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

    all_students = db.get_students()
    if not all_students:
        st.info("No data yet. Add your roster and log a few entries on the Daily Entry page first.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("##### Student Profile")
        st.caption("Search by name and/or pick a class to find a student — then see their full history and growth.")

        col_sr, col_cl, col_st = st.columns([1.4, 1, 1.6])
        with col_sr:
            sp_search = st.text_input("Search by name", key="sp_search", placeholder="Type a name…",
                                       label_visibility="collapsed")
        with col_cl:
            sp_classes = ["All Classes"] + db.get_classes()
            sp_class = st.selectbox("Class", sp_classes, key="sp_class", label_visibility="collapsed")

        pool = all_students if sp_class == "All Classes" else [s for s in all_students if s["class_name"] == sp_class]
        if sp_search.strip():
            q = sp_search.strip().lower()
            pool = [s for s in pool if q in s["name"].lower()]
        pool = sorted(pool, key=lambda s: (s["class_name"], s["name"]))

        if not pool:
            with col_st:
                st.selectbox("Student", ["No matches"], key="sp_pick_empty",
                             disabled=True, label_visibility="collapsed")
            st.warning("No students match that name/class. Try a different search.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            with col_st:
                sp_labels = [f'{s["name"]} — {s["class_name"]} (Grade {s["grade"]})' for s in pool]
                sp_pick = st.selectbox("Student", sp_labels, key="sp_pick", label_visibility="collapsed")
            student = pool[sp_labels.index(sp_pick)]

            current_levels = analytics.get_current_levels()
            cur_level   = current_levels.get(student["id"])
            history     = analytics.student_history(student["id"])
            topic_rows  = analytics.student_topic_breakdown(student["id"])
            remedial    = analytics.student_remedial_summary(student["id"])

            today_str      = _date.today().isoformat()
            today_sessions = [h for h in history if h["session_date"] == today_str]
            days_active    = len({h["session_date"] for h in history})
            last_active    = history[0]["session_date"] if history else "—"

            # ── Header ──────────────────────────────────────────────────────────
            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
            st.markdown(
                f'<div style="font-size:20px;font-weight:700;margin-bottom:6px">{student["name"]}</div>',
                unsafe_allow_html=True,
            )
            header_cards = [
                ("Class", student["class_name"]),
                ("Grade", student["grade"]),
                ("Current Level", cur_level if cur_level is not None else "—"),
                ("Total Sessions", len(history)),
                ("Days Active", days_active),
                ("Last Active", last_active),
            ]
            card_html = '<div class="info-row" style="margin-left:0;margin-right:0">'
            for label, value in header_cards:
                card_html += (f'<div class="info-cell"><div class="il">{label}</div>'
                              f'<div class="iv" style="font-size:18px">{value}</div></div>')
            card_html += '</div>'
            st.markdown(card_html, unsafe_allow_html=True)

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            # ── Today's update ─────────────────────────────────────────────────
            st.markdown("###### Today's update")
            if today_sessions:
                for h in today_sessions:
                    correct = h["total_questions"] - h["wrong_count"]
                    rem_txt = f' · Remedial: {h["remedial_status"]}' if h["remedial_status"] else ""
                    st.markdown(
                        f'<div class="info-cell" style="margin-bottom:8px">'
                        f'<b>{h["worksheet_id"]}</b> — {correct}/{h["total_questions"]} correct '
                        f'({h["accuracy"]}%){rem_txt}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No entry logged for today yet.")

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            # ── Growth charts ──────────────────────────────────────────────────
            st.markdown("###### Growth over time")
            if len(history) >= 2:
                chrono = sorted(history, key=lambda h: (h["session_date"], h["id"]))
                growth_df = pd.DataFrame({
                    "Level": [h["level_num"] for h in chrono],
                    "Accuracy %": [h["accuracy"] for h in chrono],
                }, index=[h["session_date"] for h in chrono])

                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    st.caption("Level progression")
                    st.line_chart(growth_df[["Level"]], color="#0D0D0D", width='stretch')
                with col_g2:
                    st.caption("Accuracy trend")
                    st.line_chart(growth_df[["Accuracy %"]], color="#0D0D0D", width='stretch')
            else:
                st.caption("Not enough history yet for growth charts — needs at least 2 sessions.")

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            # ── Topic weaknesses ───────────────────────────────────────────────
            st.markdown("###### Topics needing attention")
            if topic_rows:
                top_t = topic_rows[:10]
                topic_df = pd.DataFrame({"Times wrong": [t["count"] for t in top_t]},
                                        index=[t["topic"] for t in top_t])
                st.bar_chart(topic_df, horizontal=True, color="#0D0D0D", width='stretch')
            else:
                st.caption("No wrong-answer data yet — clean record so far!")

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            # ── Remedial tracking ──────────────────────────────────────────────
            st.markdown("###### Remedial tracking")
            rem_cards = [
                ("Assigned", remedial["assigned"]),
                ("Completed", remedial["completed"]),
                ("Pending", remedial["pending_count"]),
            ]
            rcard_html = '<div class="info-row" style="margin-left:0;margin-right:0">'
            for label, value in rem_cards:
                rcard_html += (f'<div class="info-cell"><div class="il">{label}</div>'
                              f'<div class="iv" style="font-size:18px">{value}</div></div>')
            rcard_html += '</div>'
            st.markdown(rcard_html, unsafe_allow_html=True)
            if remedial["pending_sessions"]:
                pending_ids = ", ".join(s["remedial_id"] for s in remedial["pending_sessions"])
                st.caption(f"Pending: {pending_ids}")

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            # ── Full history ───────────────────────────────────────────────────
            st.markdown("###### Full history")
            hist_df = pd.DataFrame([{
                "Date": h["session_date"],
                "Worksheet": h["worksheet_id"],
                "Score": f'{h["total_questions"] - h["wrong_count"]}/{h["total_questions"]}',
                "Accuracy": f'{h["accuracy"]}%',
                "Topics missed": h["resolved_topics"] or "—",
                "Remedial": h["remedial_status"] or "—",
            } for h in history])
            st.dataframe(hist_df, hide_index=True, width='stretch')

            st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


ui_common.render_footer(level_num, sublevel_code)
