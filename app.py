"""
Fear Less Maths — Main App (Dashboards default, Worksheet Generator behind ☰ menu)
LA Excellence Schools / IDPS Orchards

Default view: Dashboards (Student Profile · Alerts · Report)
☰ menu (top-right of header): opens Worksheet Generator or shows Daily Entry URL
Daily Entry lives on its own page (pages/1_Daily_Entry.py) for associate staff.
"""
import streamlit as st
from collections import defaultdict
from levels_data import LEVELS, SUBLEVELS, SHEET_OPTIONS, get_tier
from pdf_engine import build_pdf, build_answer_key_pdf
import db
import analytics
import concept_tagger
from ws_helpers import numbered_questions, remedial_id_for, build_whatsapp_report, build_school_whatsapp_report
import ui_common

ui_common.setup_page("Fear Less Maths", hide_nav=True)

# ── Session-state defaults ─────────────────────────────────────────────────────
if "view" not in st.session_state:
    st.session_state["view"] = "dashboards"   # "dashboards" | "generator" | "daily_entry_url"
if "menu_open" not in st.session_state:
    st.session_state["menu_open"] = False

# ── Custom header with ☰ menu ──────────────────────────────────────────────────
st.markdown("""
<style>
.flm-topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 24px 12px; background: var(--card);
    border-bottom: 1.5px solid var(--hairline); position: relative;
}
.flm-brand { font-size: 20px; font-weight: 700; color: var(--ink); letter-spacing: -.4px; }
.flm-sub   { font-size: 11px; color: var(--muted); margin-top: 1px; }
.menu-panel {
    background: #fff; border: 1.5px solid #E5E2DC; border-radius: 10px;
    padding: 10px 0; min-width: 220px; box-shadow: 0 6px 24px rgba(0,0,0,.10);
    margin-bottom: 2px;
}
.menu-panel-title {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: .08em; color: #999; padding: 6px 18px 4px;
}
.dash-tabs { display: flex; gap: 6px; padding: 10px 24px 0; background: var(--card); border-bottom: 1px solid var(--hairline); }
.dash-tab {
    font-size: 13px; font-weight: 600; color: #888; padding: 8px 16px;
    border-radius: 8px 8px 0 0; cursor: pointer; border: none; background: none;
    border-bottom: 3px solid transparent;
}
.dash-tab.active { color: var(--ink); border-bottom: 3px solid var(--ink); }
.back-bar {
    display: flex; align-items: center; gap: 10px; padding: 10px 24px;
    background: #F9F8F5; border-bottom: 1px solid var(--hairline);
    font-size: 13px; color: #555;
}
</style>
""", unsafe_allow_html=True)

# Top bar
col_brand, col_menu_btn = st.columns([8, 1])
with col_brand:
    st.markdown("""
    <div style="padding:14px 0 10px 24px">
        <div class="flm-brand">Fear Less Maths</div>
        <div class="flm-sub">LA Excellence Schools · IDPS Orchards</div>
    </div>
    """, unsafe_allow_html=True)

with col_menu_btn:
    st.markdown('<div style="padding-top:10px">', unsafe_allow_html=True)
    if st.button("☰", key="menu_toggle", help="Menu", use_container_width=True):
        st.session_state["menu_open"] = not st.session_state["menu_open"]
    st.markdown('</div>', unsafe_allow_html=True)

# ── Menu panel (shown when ☰ is open) ─────────────────────────────────────────
if st.session_state["menu_open"]:
    st.markdown('<div class="menu-panel"><div class="menu-panel-title">Go to</div></div>',
                unsafe_allow_html=True)
    col_m1, col_m2, col_m3 = st.columns([1, 1, 1])
    with col_m1:
        if st.button("📄  Worksheet Generator", key="goto_gen", use_container_width=True):
            st.session_state["view"] = "generator"
            st.session_state["menu_open"] = False
            st.rerun()
    with col_m2:
        if st.button("📝  Daily Entry URL", key="goto_de", use_container_width=True):
            st.session_state["view"] = "daily_entry_url"
            st.session_state["menu_open"] = False
            st.rerun()
    with col_m3:
        if st.button("🏠  Dashboards", key="goto_dash", use_container_width=True):
            st.session_state["view"] = "dashboards"
            st.session_state["menu_open"] = False
            st.rerun()
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# VIEW: DAILY ENTRY URL
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state["view"] == "daily_entry_url":
    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)
    st.markdown("##### Daily Entry — Staff Link")
    st.caption("Share this link with your associate staff. It opens **only** the Daily Entry screen — no access to worksheets, dashboards, or student data.")
    st.page_link("pages/1_Daily_Entry.py", label="Open Daily Entry page", icon="🔗")
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    st.info("Copy the URL from your browser after opening the link above, then share it with staff via WhatsApp.")
    if st.button("← Back to Dashboards", key="back_de"):
        st.session_state["view"] = "dashboards"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# VIEW: WORKSHEET GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state["view"] == "generator":

    # Back bar
    st.markdown('<div class="back-bar">', unsafe_allow_html=True)
    col_back, col_title = st.columns([1, 6])
    with col_back:
        if st.button("← Back", key="back_gen"):
            st.session_state["view"] = "dashboards"
            st.rerun()
    with col_title:
        st.markdown('<span style="font-weight:600;color:#111">Worksheet Generator</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Level selector
    level_num, sublevel_code, topic = ui_common.render_level_selector()

    # Generator sub-tabs
    GEN_SECTIONS = ["📄 Single Worksheet", "📦 Batch — All 8 Sheets", "🏷️ Concept Tags"]
    st.markdown('<div class="section-switcher">', unsafe_allow_html=True)
    gen_section = st.radio("Generator Section", GEN_SECTIONS, horizontal=True,
                           key="gen_section", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── Single Worksheet ───────────────────────────────────────────────────
    if gen_section == "📄 Single Worksheet":
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns([2, 1, 1])
        with col_a:
            sheet_lbls = [lbl for _, lbl in SHEET_OPTIONS]
            sheet_sel  = st.selectbox("Sheet", sheet_lbls, label_visibility="visible")
            sheet_num  = SHEET_OPTIONS[sheet_lbls.index(sheet_sel)][0]

        tier  = get_tier(sheet_num)
        ws_id = f"{sublevel_code}-{sheet_num}"
        is_r  = sheet_num.endswith("R")
        base  = int(sheet_num.replace("R",""))

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

        st.markdown(f"""
        <div class="info-row">
            <div class="info-cell"><div class="il">Level</div><div class="iv">Level {level_num}</div></div>
            <div class="info-cell"><div class="il">Domain</div><div class="iv">{LEVELS[level_num]['name']}</div></div>
            <div class="info-cell"><div class="il">Topic</div><div class="iv">{topic}</div></div>
            <div class="info-cell"><div class="il">Format</div><div class="iv">20 Qs · A4</div></div>
        </div>
        """, unsafe_allow_html=True)

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

        col_btn, col_pad = st.columns([2, 1])
        with col_btn:
            if st.button(f"⚡  Generate  {ws_id}.pdf", type="primary", key="gen"):
                with st.spinner(f"Generating {ws_id}…"):
                    try:
                        pdf_bytes = build_pdf(level_num, sublevel_code, sheet_num).read()
                        st.session_state["pdf_ready"] = pdf_bytes
                        st.session_state["pdf_ws_id"] = ws_id
                    except Exception as e:
                        st.error(f"Error: {e}"); st.exception(e)

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
                    mime="application/pdf", key="dl_s",
                )

            is_key_eligible = (not is_r) and (5 <= level_num <= 19)
            if is_key_eligible:
                st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
                if st.button(f"🔑  Key  —  {ws_id}", key="gen_key"):
                    with st.spinner(f"Generating answer key for {ws_id}…"):
                        try:
                            key_bytes = build_answer_key_pdf(level_num, sublevel_code, sheet_num).read()
                            st.session_state["key_ready"] = key_bytes
                            st.session_state["key_ws_id"] = ws_id
                        except Exception as e:
                            st.error(f"Error: {e}"); st.exception(e)

                if st.session_state.get("key_ws_id") == ws_id and "key_ready" in st.session_state:
                    size_kb = len(st.session_state["key_ready"]) // 1024
                    st.markdown(f"""
                    <div class="success-card">
                        <div class="ck">✓</div>
                        <div>{ws_id} answer key ready &nbsp;·&nbsp; {size_kb} KB</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.download_button(
                        label=f"⬇  Download  {ws_id}-KEY.pdf",
                        data=st.session_state["key_ready"],
                        file_name=f"{ws_id}-KEY.pdf",
                        mime="application/pdf", key="dl_key",
                    )

        st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)

    # ─── Batch ──────────────────────────────────────────────────────────────
    elif gen_section == "📦 Batch — All 8 Sheets":
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)
        st.markdown("##### Batch — All 8 Sheets")
        st.caption(f"Generates all four main sheets **+** all four remedial sheets for **{sublevel_code}** in one go. Each sheet is a separate PDF.")

        if st.button(f"⚡  Generate All 8 Sheets for {sublevel_code}", type="primary", key="batch"):
            progress = st.progress(0, text="Starting…")
            results = {}
            sheets = ["1","2","3","4","1R","2R","3R","4R"]
            for i, sn in enumerate(sheets):
                progress.progress((i+1)/len(sheets), text=f"Generating {sublevel_code}-{sn}…")
                try:
                    results[sn] = build_pdf(level_num, sublevel_code, sn).read()
                except Exception as e:
                    results[sn] = None
                    st.warning(f"{sublevel_code}-{sn}: {e}")
            progress.empty()
            st.session_state["batch_results"] = results
            st.session_state["batch_code"]    = sublevel_code
            st.success(f"All 8 sheets ready for {sublevel_code}.")

        if st.session_state.get("batch_code") == sublevel_code and "batch_results" in st.session_state:
            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
            for sn, data in st.session_state["batch_results"].items():
                if data:
                    fname = f"{sublevel_code}-{sn}.pdf"
                    st.download_button(f"⬇ {fname}", data=data, file_name=fname,
                                       mime="application/pdf", key=f"dl_b_{sn}")
        st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ─── Concept Tags ───────────────────────────────────────────────────────
    elif gen_section == "🏷️ Concept Tags":
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)
        st.markdown("##### Concept Tags")
        st.caption("Shows which concept each question in the selected worksheet is tagged to. Used by the Alerts system to detect when a student keeps getting the same concept wrong.")

        sheet_lbls = [lbl for _, lbl in SHEET_OPTIONS]
        tag_sheet_sel = st.selectbox("Sheet", sheet_lbls, key="tag_sheet")
        tag_sheet_num = SHEET_OPTIONS[sheet_lbls.index(tag_sheet_sel)][0]
        tag_ws_id = f"{sublevel_code}-{tag_sheet_num}"

        if st.button(f"🏷️  Show Tags for {tag_ws_id}", key="show_tags"):
            try:
                from content import get_questions
                items = get_questions(sublevel_code, tag_sheet_num, level_num)
                tags = concept_tagger.tag_questions(items, sublevel_code, topic)
                st.session_state["tag_results"] = tags
                st.session_state["tag_ws_id"]   = tag_ws_id
            except Exception as e:
                st.error(f"Error: {e}")

        if st.session_state.get("tag_ws_id") == tag_ws_id and "tag_results" in st.session_state:
            for qn, (q_text, concept) in enumerate(st.session_state["tag_results"], 1):
                st.markdown(f"""
                <div style="display:flex;gap:12px;padding:7px 0;border-bottom:1px solid #f0ede8">
                    <span style="font-size:12px;font-weight:700;color:#555;min-width:28px">Q{qn}</span>
                    <span style="font-size:12px;color:#222;flex:1">{q_text[:80]}</span>
                    <span style="font-size:11px;color:#0D6EFD;background:#EEF4FF;padding:2px 8px;border-radius:12px;white-space:nowrap">{concept}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# VIEW: DASHBOARDS (default)
# ══════════════════════════════════════════════════════════════════════════════
else:  # "dashboards"

    DASH_SECTIONS = ["👤 Student Profile", "🚨 Alerts", "📊 Report"]
    st.markdown('<div class="section-switcher">', unsafe_allow_html=True)
    dash_section = st.radio("Dashboard", DASH_SECTIONS, horizontal=True,
                            key="dash_section", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── STUDENT PROFILE ────────────────────────────────────────────────────
    if dash_section == "👤 Student Profile":
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)

        existing_classes = db.get_classes()
        if not existing_classes:
            st.info("No student data yet. Use Daily Entry to add sessions, or generate demo data below.")
            with st.expander("Generate demo data"):
                st.caption("Generates 300 fake students (30 per class, Class 1–10) with a realistic "
                           "mix of sessions, wrong answers, and remedial assignments — lets you preview "
                           "all the dashboards before real data arrives.")
                if st.button("👥  Generate 300 demo students", key="gen_demo"):
                    with st.spinner("Seeding demo data…"):
                        import seed_demo_data
                        seed_demo_data.seed()
                    st.success("Demo data ready. Refresh the page to see it.")
        else:
            col_p1, col_p2 = st.columns([1, 1])
            with col_p1:
                profile_class = st.selectbox("Class", existing_classes, key="profile_class")
            students = db.get_students(profile_class)
            with col_p2:
                profile_student = st.selectbox("Student", [s["name"] for s in students], key="profile_student")
            student = next(s for s in students if s["name"] == profile_student)

            sessions = db.get_student_sessions(student["id"])
            alerts   = db.get_student_alerts(student["id"], threshold=2)

            # ── Header card
            grade_badge = f"Grade {student.get('grade','?')}"
            st.markdown(f"""
            <div class="ws-hero" style="margin-top:14px">
                <div>
                    <div style="font-size:10px;color:#555;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px">Student</div>
                    <div class="ws-hero-id" style="font-size:22px">{student['name']}</div>
                    <div style="font-size:12px;color:#888;margin-top:3px">{profile_class} &nbsp;·&nbsp; {grade_badge}</div>
                </div>
                <div class="ws-hero-meta">
                    <div class="ws-hero-topic">{len(sessions)} sessions</div>
                    <div class="ws-hero-tier">{"⚠️ "+str(len(alerts))+" alerts" if alerts else "✅ No open alerts"}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Stats row
            if sessions:
                total_q  = sum(s["total_questions"] or 0 for s in sessions)
                total_w  = sum(len(s.get("wrong_qs") or []) for s in sessions)
                accuracy = round(100*(total_q-total_w)/total_q) if total_q else 0
                current_level = sessions[-1]["level_num"] if sessions else "—"
                st.markdown(f"""
                <div class="info-row" style="margin-left:0;margin-right:0">
                    <div class="info-cell"><div class="il">Sessions</div><div class="iv">{len(sessions)}</div></div>
                    <div class="info-cell"><div class="il">Questions</div><div class="iv">{total_q}</div></div>
                    <div class="info-cell"><div class="il">Accuracy</div><div class="iv">{accuracy}%</div></div>
                    <div class="info-cell"><div class="il">Current Level</div><div class="iv">{current_level}</div></div>
                </div>
                """, unsafe_allow_html=True)

                # ── Recent sessions
                st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
                st.markdown("###### Recent Sessions")
                for s in reversed(sessions[-8:]):
                    wq = s.get("wrong_qs") or []
                    n_wrong = len(wq); n_q = s["total_questions"] or 0
                    acc = round(100*(n_q-n_wrong)/n_q) if n_q else 0
                    acc_color = "#2E6B5E" if acc>=80 else ("#CC7000" if acc>=60 else "#B71C1C")
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;
                                padding:8px 0;border-bottom:1px solid #f0ede8">
                        <div>
                            <span style="font-size:13px;font-weight:600;color:#111">{s['worksheet_id']}</span>
                            <span style="font-size:11px;color:#888;margin-left:10px">{s['session_date']}</span>
                        </div>
                        <div style="font-size:13px;font-weight:700;color:{acc_color}">{acc}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                # ── Alerts for this student
                if alerts:
                    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
                    st.markdown("###### Open Alerts")
                    for a in alerts:
                        st.markdown(f"""
                        <div class="info-cell" style="margin-bottom:8px">
                            <div class="il">⚠️ Concept stuck</div>
                            <div style="font-size:13px;color:#222;margin-top:4px">
                                <b>{a['topic']}</b> — wrong {a['wrong_count']} times across {a['worksheet_count']} worksheets
                                <span style="font-size:11px;color:#888"> (Level {a['level_num']} · {a['sublevel_topic']})</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.caption("No sessions recorded yet for this student.")

        st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ─── ALERTS ─────────────────────────────────────────────────────────────
    elif dash_section == "🚨 Alerts":
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)
        st.markdown("##### Concept Alerts")
        st.caption("Students who have got the same concept wrong across 3 or more different worksheets. These are the students who need targeted remedial help — not just more practice.")

        alert_classes = ["All Classes"] + db.get_classes()
        col_a1, col_a2 = st.columns([1, 1])
        with col_a1:
            alert_class_sel = st.selectbox("Class", alert_classes, key="alert_class")
        with col_a2:
            alert_threshold = st.number_input("Minimum wrong-answer count", min_value=2, max_value=10,
                                              value=3, key="alert_threshold")
        alert_class = None if alert_class_sel == "All Classes" else alert_class_sel
        alerts = analytics.concept_alerts(threshold=alert_threshold, class_name=alert_class)

        if not alerts:
            st.success("No concept alerts at this threshold. 🎉")
        else:
            st.markdown(f"""
            <div class="info-cell" style="display:inline-block;padding:10px 20px;margin-bottom:16px">
                <div class="il">Open Alerts</div>
                <div class="iv" style="font-size:22px">{len(alerts)} <span style="font-size:13px;color:#888">student-concept pairs</span></div>
            </div>
            """, unsafe_allow_html=True)

            by_student = defaultdict(list)
            for a in alerts:
                by_student[a["student_name"]].append(a)

            for student_name, recs in sorted(by_student.items()):
                cls = recs[0].get("class_name","")
                mistake_types = list({d for r in recs for d in (r.get("mistake_types") or [])})
                mistake_html = ("Mistake types seen: " + ", ".join(mistake_types)) if mistake_types else ""
                recs_html = " &nbsp;·&nbsp; ".join(
                    f"<b>{r['topic']}</b> ×{r['wrong_count']}" for r in recs
                )
                st.markdown(f"""
                <div class="info-cell" style="margin-bottom:10px">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div>
                            <div style="font-size:14px;font-weight:700;color:#111">{student_name}</div>
                            <div style="font-size:11px;color:#888;margin-top:1px">{cls} &nbsp;·&nbsp; Level {recs[0]['level_num']} &nbsp;·&nbsp; {recs[0]['sublevel_topic']} — Concept sheet</div>
                        </div>
                        <div style="font-size:12px;color:#B71C1C;font-weight:700">⚠️ {len(recs)} concept(s)</div>
                    </div>
                    <div style="font-size:12px;color:#555;margin-top:6px">{mistake_html}</div>
                    <div style="font-size:13px;color:#222;margin-top:6px">{recs_html}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ─── REPORT ─────────────────────────────────────────────────────────────
    elif dash_section == "📊 Report":
        import pandas as pd
        from datetime import date as _rdate, timedelta as _rtimedelta

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)
        st.markdown("##### School Report")
        st.caption("A weekly/monthly snapshot of FLM usage and outcomes — built for sharing with school management.")

        col_r1, col_r2 = st.columns([1.3, 1])
        with col_r1:
            report_period = st.radio("Period", ["This Week", "This Month", "Custom"],
                                     horizontal=True, key="report_period")
        with col_r2:
            report_class_sel = st.selectbox("Class", ["All Classes"] + db.get_classes(), key="report_class")
        report_class = None if report_class_sel == "All Classes" else report_class_sel

        today = _rdate.today()
        if report_period == "This Week":
            r_from = today - _rtimedelta(days=today.weekday())
            r_to   = today
            period_label = f"Week of {r_from.strftime('%d %b')} – {r_to.strftime('%d %b %Y')}"
        elif report_period == "This Month":
            r_from = today.replace(day=1); r_to = today
            period_label = today.strftime("%B %Y")
        else:
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                r_from = st.date_input("From", value=today-_rtimedelta(days=7), key="report_from")
            with col_d2:
                r_to = st.date_input("To", value=today, key="report_to")
            period_label = f"{r_from.strftime('%d %b %Y')} – {r_to.strftime('%d %b %Y')}"

        date_from, date_to = r_from.isoformat(), r_to.isoformat()

        st.markdown(f"""
        <div style="font-size:13px;color:#888;margin:10px 0 4px">
            <b style="color:#111">{period_label}</b> &nbsp;·&nbsp; {report_class_sel}
        </div>
        """, unsafe_allow_html=True)

        summary = analytics.school_summary(date_from, date_to, report_class)

        if summary["total_students"] == 0:
            st.info("No students in this class yet.")
        else:
            cards = [
                ("Total Students", summary["total_students"]),
                ("Active This Period", summary["active_students"]),
                ("Completion Rate", f'{summary["completion_rate"]}%'),
                ("Total Sessions", summary["total_sessions"]),
                ("Avg Accuracy", f'{summary["avg_accuracy"]}%' if summary["avg_accuracy"] is not None else "—"),
                ("Avg Current Level", summary["avg_level"]),
            ]
            card_html = '<div class="info-row" style="margin-left:0;margin-right:0">'
            for label, value in cards:
                card_html += (f'<div class="info-cell"><div class="il">{label}</div>'
                              f'<div class="iv" style="font-size:18px">{value}</div></div>')
            card_html += '</div>'
            st.markdown(card_html, unsafe_allow_html=True)

            if summary["inactive_students"] > 0:
                st.caption(f"⚠️ {summary['inactive_students']} student(s) had no activity in this period.")

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            if report_class is None:
                st.markdown("###### Class-wise breakdown")
                cls_rows = analytics.class_summary(date_from, date_to)
                cls_df = pd.DataFrame([{
                    "Class": c["class_name"], "Students": c["student_count"],
                    "Active": c["active_students"], "Sessions": c["sessions_in_range"],
                    "Avg Accuracy": f'{c["avg_accuracy"]}%' if c["avg_accuracy"] is not None else "—",
                } for c in cls_rows])
                st.dataframe(cls_df, hide_index=True, width='stretch')
                st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)
            else:
                cls_rows = []

            st.markdown("###### Topics needing attention")
            topic_rows = analytics.topic_failure_ranking(date_from, date_to, report_class)
            if topic_rows:
                top_t = topic_rows[:10]
                topic_df = pd.DataFrame({"Students affected": [t["student_count"] for t in top_t]},
                                        index=[t["topic"] for t in top_t])
                st.bar_chart(topic_df, horizontal=True, color="#0D0D0D", width='stretch')
            else:
                st.caption("No wrong-answer data in this period.")

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            st.markdown("###### How students are thinking (mistake types)")
            mistake_rows = analytics.school_mistake_breakdown(date_from, date_to, report_class)
            if mistake_rows:
                mistake_df = pd.DataFrame({"Times": [m["count"] for m in mistake_rows]},
                                          index=[m["mistake_type"] for m in mistake_rows])
                st.bar_chart(mistake_df, horizontal=True, color="#2E6B5E", width='stretch')
            else:
                st.caption("No mistake-type data tagged in this period yet.")

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            st.markdown("###### Remedial follow-up")
            rem = analytics.remedial_completion_summary(date_from, date_to, report_class)
            rem_cards = [
                ("Assigned", rem["assigned"]), ("Completed", rem["completed"]),
                ("Pending", rem["pending"]),
                ("Completion Rate", f'{rem["completion_rate"]}%' if rem["completion_rate"] is not None else "—"),
            ]
            rcard_html = '<div class="info-row" style="margin-left:0;margin-right:0">'
            for label, value in rem_cards:
                rcard_html += (f'<div class="info-cell"><div class="il">{label}</div>'
                              f'<div class="iv" style="font-size:18px">{value}</div></div>')
            rcard_html += '</div>'
            st.markdown(rcard_html, unsafe_allow_html=True)

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            st.markdown("###### Currently flagged for follow-up")
            open_alerts = analytics.concept_alerts(threshold=2, class_name=report_class)
            flagged_students = len({a["student_id"] for a in open_alerts})
            st.markdown(f"""
            <div class="info-cell" style="display:inline-block;padding:13px 24px">
                <div class="il">Open Alerts</div>
                <div class="iv" style="font-size:22px">{len(open_alerts)} <span style="font-size:13px;color:#888">across {flagged_students} student(s)</span></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div style="height:32px"></div>', unsafe_allow_html=True)

            st.markdown("###### Send to chairman / management")
            st.caption("Tap the copy icon in the corner of the box below, then paste straight into WhatsApp.")
            wa_report_text = build_school_whatsapp_report(
                period_label=period_label, class_label=report_class_sel, summary=summary,
                class_rows=cls_rows, topic_rows=topic_rows, mistake_rows=mistake_rows,
                remedial=rem, num_alerts=len(open_alerts), num_flagged_students=flagged_students,
            )
            st.code(wa_report_text, language=None)

        st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-bar">
    <div class="fl">LA Excellence Schools / IDPS Orchards &nbsp;·&nbsp; Fear Less Maths</div>
    <div class="fr">FLM v2</div>
</div>
""", unsafe_allow_html=True)
