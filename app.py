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

# Top bar with ☰ button
col_brand, col_menu_btn = st.columns([8, 1])
with col_brand:
    st.markdown("""
    <div style="padding:14px 0 10px 8px">
        <div style="font-size:20px;font-weight:700;color:#111;letter-spacing:-.4px">Fear Less Maths</div>
        <div style="font-size:11px;color:#777;margin-top:1px">LA Excellence Schools · IDPS Orchards</div>
    </div>
    """, unsafe_allow_html=True)
with col_menu_btn:
    st.markdown('<div style="padding-top:14px">', unsafe_allow_html=True)
    if st.button("☰", key="menu_toggle", help="Menu", use_container_width=True):
        st.session_state["menu_open"] = not st.session_state["menu_open"]
    st.markdown('</div>', unsafe_allow_html=True)

# ── Menu panel (shown when ☰ is open) ─────────────────────────────────────────
if st.session_state["menu_open"]:
    st.markdown('<div class="menu-panel"><div class="menu-panel-title">Go to</div></div>',
                unsafe_allow_html=True)
    col_m1, col_m2, col_m3, col_m4 = st.columns([1, 1, 1, 1])
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
        if st.button("🧪  Screening Test", key="goto_screen", use_container_width=True):
            st.session_state["view"] = "screening"
            st.session_state["menu_open"] = False
            st.rerun()
    with col_m4:
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
# VIEW: SCREENING TEST
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state["view"] == "screening":
    st.markdown('<div class="back-bar">', unsafe_allow_html=True)
    col_back, col_title = st.columns([1, 6])
    with col_back:
        if st.button("← Back", key="back_screen"):
            st.session_state["view"] = "dashboards"
            st.rerun()
    with col_title:
        st.markdown('<span style="font-weight:600;color:#111">Screening Test — Who Needs FLM?</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)
    st.markdown("##### Comprehensive FLM Readiness Screening")
    st.caption(
        "Generates a diagnostic worksheet built from real, already-verified FLM questions "
        "sampling every prerequisite level a student should have secured by the end of the "
        "previous class. Use the score to decide FLM placement — see the Screening Test "
        "Accountability Framework document for the scoring bands and decision rules."
    )

    import screening_test as _st

    class_options = sorted(_st.SCREENING_BLUEPRINTS.keys(), key=int)
    screen_class = st.selectbox("Class", class_options, key="screen_class",
                                format_func=lambda c: f"Class {c}")

    if st.button(f"🧪  Generate Screening Test — Class {screen_class}", type="primary", key="gen_screen"):
        with st.spinner(f"Assembling comprehensive screening test for Class {screen_class}…"):
            try:
                pdf_bytes, report = _st.build_screening_pdf_with_report(
                    screen_class, _st.SCREENING_BLUEPRINTS[screen_class]
                )
                st.session_state["screen_pdf"] = pdf_bytes.read()
                st.session_state["screen_report"] = report
                st.session_state["screen_class_done"] = screen_class
            except Exception as e:
                st.error(f"Error: {e}")
                st.exception(e)

    if st.session_state.get("screen_class_done") == screen_class and "screen_pdf" in st.session_state:
        report = st.session_state["screen_report"]
        size_kb = len(st.session_state["screen_pdf"]) // 1024
        st.markdown(f"""
        <div class="success-card">
            <div class="ck">✓</div>
            <div>Class {screen_class} screening test ready &nbsp;·&nbsp; {report['total_questions']} questions &nbsp;·&nbsp; {size_kb} KB</div>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            label=f"⬇  Download  SCREEN-{screen_class}.pdf",
            data=st.session_state["screen_pdf"],
            file_name=f"SCREEN-{screen_class}.pdf",
            mime="application/pdf",
            key="dl_screen",
        )

        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        st.caption(f"Sublevels sampled: {len(report['used'])}")
        if report["skipped"]:
            st.warning(
                f"⚠️ {len(report['skipped'])} sublevel(s) skipped — no content built yet for: "
                f"{', '.join(report['skipped'])}. These were left out honestly rather than "
                f"faked; the test score should be read with this gap in mind."
            )

    st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
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
    GEN_SECTIONS = ["📄 Single Worksheet", "📦 Batch — All 8 Sheets", "🗂️ Bulk Export", "📘 Bulk Export — Single PDF/Level", "🎯 Class Plan (5-Month)", "🏷️ Concept Tags"]
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

    # ─── Bulk Export ────────────────────────────────────────────────────────
    elif gen_section == "🗂️ Bulk Export":
        import bulk_export as be

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)
        st.markdown("##### Bulk Export")
        st.caption("Generates every worksheet (4 main + 4 remedial sheets, every sublevel) "
                   "for a whole level or a 5-level range, and packages them into one ZIP file.")

        bulk_mode = st.radio("Export scope", ["Whole Level", "5-Level Range"],
                             horizontal=True, key="bulk_mode")

        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

        if bulk_mode == "Whole Level":
            all_levels = sorted(LEVELS.keys())
            bulk_level = st.selectbox(
                "Level", all_levels, index=all_levels.index(level_num) if level_num in all_levels else 0,
                format_func=lambda l: f"Level {l} — {LEVELS[l]['name']}", key="bulk_level",
            )
            n_pdfs = be.count_pdfs_for_levels([bulk_level])
            est_sec = round(n_pdfs * 0.1)
            st.caption(f"This will generate **{n_pdfs} PDFs** (≈{est_sec}s) and zip them.")

            if st.button(f"🗂️  Export Level {bulk_level} (ZIP)", type="primary", key="bulk_export_level"):
                progress = st.progress(0, text="Starting…")
                def _cb(done, total):
                    progress.progress(done/total, text=f"Generating {done}/{total} worksheets…")
                zip_buf, failures = be.build_level_zip(bulk_level, progress_cb=_cb)
                progress.empty()
                st.session_state["bulk_zip"] = zip_buf.getvalue()
                st.session_state["bulk_zip_name"] = f"Level{bulk_level:02d}_AllWorksheets.zip"
                st.session_state["bulk_failures"] = failures
                st.success(f"Level {bulk_level} export ready — {n_pdfs - len(failures)}/{n_pdfs} worksheets included.")

        else:  # 5-Level Range
            range_label = st.selectbox("Range", list(be.FIVE_LEVEL_RANGES.keys()), key="bulk_range")
            range_levels = be.FIVE_LEVEL_RANGES[range_label]
            n_pdfs = be.count_pdfs_for_levels(range_levels)
            est_sec = round(n_pdfs * 0.1)
            st.caption(f"This will generate **{n_pdfs} PDFs** across {len(range_levels)} levels "
                      f"(≈{est_sec}s, may take over a minute) and zip them.")

            if st.button(f"🗂️  Export {range_label} (ZIP)", type="primary", key="bulk_export_range"):
                progress = st.progress(0, text="Starting…")
                def _cb(done, total):
                    progress.progress(done/total, text=f"Generating {done}/{total} worksheets…")
                zip_buf, failures = be.build_multi_level_zip(range_levels, progress_cb=_cb)
                progress.empty()
                st.session_state["bulk_zip"] = zip_buf.getvalue()
                st.session_state["bulk_zip_name"] = f"{range_label.replace(' ', '_')}_AllWorksheets.zip"
                st.session_state["bulk_failures"] = failures
                st.success(f"{range_label} export ready — {n_pdfs - len(failures)}/{n_pdfs} worksheets included.")

        if "bulk_zip" in st.session_state:
            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
            size_mb = len(st.session_state["bulk_zip"]) / (1024*1024)
            st.markdown(f"""
            <div class="success-card">
                <div class="ck">✓</div>
                <div>{st.session_state['bulk_zip_name']} &nbsp;·&nbsp; {size_mb:.1f} MB</div>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                label=f"⬇  Download  {st.session_state['bulk_zip_name']}",
                data=st.session_state["bulk_zip"],
                file_name=st.session_state["bulk_zip_name"],
                mime="application/zip",
                key="dl_bulk_zip",
            )
            if st.session_state.get("bulk_failures"):
                st.warning(f"⚠️ {len(st.session_state['bulk_failures'])} worksheet(s) failed to generate "
                          f"and were skipped — see MANIFEST.txt inside the zip for details.")

        st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ─── Class Plan (5-Month) ───────────────────────────────────────────────
    # ─── Bulk Export — Single PDF per Level (main sheets only, print-ready) ─
    elif gen_section == "📘 Bulk Export — Single PDF/Level":
        import bulk_export as be

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)
        st.markdown("##### Bulk Export — Single PDF per Level")
        st.caption("Merges the 4 main sheets (1, 2, 3, 4) for every sublevel in a level into "
                   "**one single PDF**, in sublevel order, ready to print in one go. "
                   "Remedial sheets (1R-4R) are excluded — those are printed separately.")

        sp_mode = st.radio("Export scope", ["Whole Level", "5-Level Range"],
                             horizontal=True, key="sp_mode")

        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

        if sp_mode == "Whole Level":
            all_levels = sorted(LEVELS.keys())
            sp_level = st.selectbox(
                "Level", all_levels, index=all_levels.index(level_num) if level_num in all_levels else 0,
                format_func=lambda l: f"Level {l} — {LEVELS[l]['name']}", key="sp_level",
            )
            n_pdfs = be.count_main_pdfs_for_levels([sp_level])
            est_sec = round(n_pdfs * 0.1)
            st.caption(f"This will merge **{n_pdfs} worksheets** (≈{est_sec}s) into one PDF.")

            if st.button(f"📘  Export Level {sp_level} (Single PDF)", type="primary", key="sp_export_level"):
                progress = st.progress(0, text="Starting…")
                def _cb(done, total):
                    progress.progress(done/total, text=f"Merging {done}/{total} worksheets…")
                pdf_buf, failures = be.build_level_single_pdf(sp_level, progress_cb=_cb)
                progress.empty()
                level_name = LEVELS.get(sp_level, {}).get("name", f"Level {sp_level}")
                st.session_state["sp_pdf"] = pdf_buf.getvalue()
                st.session_state["sp_pdf_name"] = f"Level{sp_level:02d} - {level_name}".replace("/", "-") + ".pdf"
                st.session_state["sp_failures"] = failures
                st.success(f"Level {sp_level} single-PDF ready — {n_pdfs - len(failures)}/{n_pdfs} worksheets included.")

        else:  # 5-Level Range
            sp_range_label = st.selectbox("Range", list(be.FIVE_LEVEL_RANGES.keys()), key="sp_range")
            sp_range_levels = be.FIVE_LEVEL_RANGES[sp_range_label]
            n_pdfs = be.count_main_pdfs_for_levels(sp_range_levels)
            est_sec = round(n_pdfs * 0.1)
            st.caption(f"This will merge **{n_pdfs} worksheets** across {len(sp_range_levels)} levels "
                      f"(≈{est_sec}s) into one PDF per level, zipped together.")

            if st.button(f"📘  Export {sp_range_label} (Single PDF/Level)", type="primary", key="sp_export_range"):
                progress = st.progress(0, text="Starting…")
                def _cb(done, total):
                    progress.progress(done/total, text=f"Merging {done}/{total} worksheets…")
                zip_buf, failures = be.build_multi_level_single_pdfs(sp_range_levels, progress_cb=_cb)
                progress.empty()
                st.session_state["sp_zip"] = zip_buf.getvalue()
                st.session_state["sp_zip_name"] = f"{sp_range_label.replace(' ', '_')}_SinglePDFs.zip"
                st.session_state["sp_failures"] = failures
                st.success(f"{sp_range_label} export ready — {n_pdfs - len(failures)}/{n_pdfs} worksheets included.")

        if "sp_pdf" in st.session_state:
            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
            size_mb = len(st.session_state["sp_pdf"]) / (1024*1024)
            st.markdown(f"""
            <div class="success-card">
                <div class="ck">✓</div>
                <div>{st.session_state['sp_pdf_name']} &nbsp;·&nbsp; {size_mb:.1f} MB</div>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                label=f"⬇  Download  {st.session_state['sp_pdf_name']}",
                data=st.session_state["sp_pdf"],
                file_name=st.session_state["sp_pdf_name"],
                mime="application/pdf",
                key="dl_sp_pdf",
            )

        if "sp_zip" in st.session_state:
            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
            size_mb = len(st.session_state["sp_zip"]) / (1024*1024)
            st.markdown(f"""
            <div class="success-card">
                <div class="ck">✓</div>
                <div>{st.session_state['sp_zip_name']} &nbsp;·&nbsp; {size_mb:.1f} MB</div>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                label=f"⬇  Download  {st.session_state['sp_zip_name']}",
                data=st.session_state["sp_zip"],
                file_name=st.session_state["sp_zip_name"],
                mime="application/zip",
                key="dl_sp_zip",
            )

        st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif gen_section == "🎯 Class Plan (5-Month)":
        import class_plan_export as cpe
        from class_plan_2026_27 import CLASS_PLAN_2026_27

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)
        st.markdown("##### Personalised 5-Month Class Plan")
        st.caption(
            "One tap per class downloads exactly the worksheets assigned to that class in the "
            "published 5-month plan (16 FLM days/month × 5 months) — the specific levels, "
            "sublevels, and sheet depth already worked out to fit the time budget. Not a whole "
            "level — only what that class actually needs."
        )

        CLASS_ORDER = ["Class 1","Class 2","Class 3","Class 4","Class 5",
                       "Class 6","Class 7","Class 8","Class 9","Class 10"]
        PRE_PRIMARY = ["Nursery","LKG","UKG"]

        def _class_button_grid(class_list, cols_per_row=5):
            for row_start in range(0, len(class_list), cols_per_row):
                row_classes = class_list[row_start:row_start+cols_per_row]
                cols = st.columns(cols_per_row)
                for i, cls in enumerate(row_classes):
                    with cols[i]:
                        n_ws = cpe.count_pdfs_for_class(cls)
                        if st.button(f"{cls}\n({n_ws} sheets)", key=f"class_plan_btn_{cls}",
                                     use_container_width=True):
                            st.session_state["class_plan_target"] = cls

        st.markdown("###### Classes 1 – 10")
        _class_button_grid(CLASS_ORDER)
        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        st.markdown("###### Pre-Primary")
        _class_button_grid(PRE_PRIMARY)

        target = st.session_state.get("class_plan_target")
        if target:
            st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
            n_ws = cpe.count_pdfs_for_class(target)
            est_sec = round(n_ws * 0.1)
            st.info(f"**{target}** — {n_ws} worksheets, ≈{est_sec}s to generate.")

            if st.button(f"🎯  Generate {target} Plan (ZIP)", type="primary", key="gen_class_plan"):
                progress = st.progress(0, text="Starting…")
                def _cb(done, total):
                    progress.progress(done/total, text=f"Generating {done}/{total} worksheets…")
                zip_buf, failures = cpe.build_class_plan_zip(target, progress_cb=_cb)
                progress.empty()
                st.session_state["class_plan_zip"] = zip_buf.getvalue()
                st.session_state["class_plan_zip_name"] = f"{target.replace(' ', '_')}_5Month_Plan.zip"
                st.session_state["class_plan_failures"] = failures
                st.success(f"{target} plan ready — {n_ws - len(failures)}/{n_ws} worksheets included.")

        if "class_plan_zip" in st.session_state:
            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
            size_mb = len(st.session_state["class_plan_zip"]) / (1024*1024)
            st.markdown(f"""
            <div class="success-card">
                <div class="ck">✓</div>
                <div>{st.session_state['class_plan_zip_name']} &nbsp;·&nbsp; {size_mb:.1f} MB</div>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                label=f"⬇  Download  {st.session_state['class_plan_zip_name']}",
                data=st.session_state["class_plan_zip"],
                file_name=st.session_state["class_plan_zip_name"],
                mime="application/zip",
                key="dl_class_plan_zip",
            )
            if st.session_state.get("class_plan_failures"):
                st.warning(f"⚠️ {len(st.session_state['class_plan_failures'])} worksheet(s) failed to generate "
                          f"and were skipped — see MANIFEST.txt inside the zip for details.")

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

    DASH_SECTIONS = ["🏫 Class Dashboard", "👤 Student Profile", "🚨 Alerts", "📊 Report"]
    st.markdown('<div class="section-switcher">', unsafe_allow_html=True)
    dash_section = st.radio("Dashboard", DASH_SECTIONS, horizontal=True,
                            key="dash_section", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── CLASS DASHBOARD ────────────────────────────────────────────────────
    if dash_section == "🏫 Class Dashboard":
        import pandas as pd
        from datetime import date as _cdate, timedelta as _ctimedelta

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)
        st.markdown("##### Class Dashboard")
        st.caption("Pick a class to see who's submitted today, class-level accuracy, and weak topics — the quick daily check-in view.")

        cd_classes = db.get_classes()
        if not cd_classes:
            st.info("No student data yet. Use Daily Entry to add sessions.")
        else:
            col_c1, col_c2 = st.columns([1, 1])
            with col_c1:
                cd_class = st.selectbox("Class", cd_classes, key="cd_class")
            with col_c2:
                cd_period = st.radio("Period", ["Today", "This Week", "This Month"],
                                     horizontal=True, key="cd_period")

            today = _cdate.today()
            if cd_period == "Today":
                cd_from = cd_to = today.isoformat()
            elif cd_period == "This Week":
                cd_from = (today - _ctimedelta(days=today.weekday())).isoformat()
                cd_to = today.isoformat()
            else:
                cd_from = today.replace(day=1).isoformat()
                cd_to = today.isoformat()

            summary = analytics.school_summary(cd_from, cd_to, cd_class)
            cards = [
                ("Total Students", summary["total_students"]),
                ("Submitted" if cd_period == "Today" else "Active", summary["active_students"]),
                ("Not Yet" if cd_period == "Today" else "Inactive", summary["inactive_students"]),
                ("Avg Accuracy", f'{summary["avg_accuracy"]}%' if summary["avg_accuracy"] is not None else "—"),
                ("Avg Current Level", summary["avg_level"]),
            ]
            card_html = '<div class="info-row" style="margin-left:0;margin-right:0">'
            for label, value in cards:
                card_html += (f'<div class="info-cell"><div class="il">{label}</div>'
                              f'<div class="iv" style="font-size:18px">{value}</div></div>')
            card_html += '</div>'
            st.markdown(card_html, unsafe_allow_html=True)

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            # ── Per-student roll call: who submitted, who didn't ──────────────
            roster = db.get_students(cd_class)
            sessions = db.get_sessions(class_name=cd_class, date_from=cd_from, date_to=cd_to)
            by_student = defaultdict(list)
            for sess in sessions:
                by_student[sess["student_id"]].append(sess)
            current_levels = analytics.get_current_levels()
            open_alerts = analytics.concept_alerts(threshold=2, class_name=cd_class)
            alert_counts = defaultdict(int)
            for a in open_alerts:
                alert_counts[a["student_id"]] += 1

            rows = []
            for i, s in enumerate(sorted(roster, key=lambda x: x["name"]), 1):
                s_sessions = by_student.get(s["id"], [])
                submitted = len(s_sessions) > 0
                accs = [analytics._session_accuracy(sess) for sess in s_sessions
                        if sess.get("status") not in ("absent",)]
                avg_acc = f"{round(sum(accs)/len(accs)*100)}%" if accs else "—"
                rows.append({
                    "#": i,
                    "Name": s["name"],
                    "Submitted" if cd_period == "Today" else "Active": "✅" if submitted else "—",
                    "Level": current_levels.get(s["id"], "—"),
                    "Accuracy": avg_acc,
                    "Alerts": alert_counts.get(s["id"], 0) or "—",
                })

            not_submitted = [r["Name"] for r in rows if r.get("Submitted" if cd_period == "Today" else "Active") == "—"]
            if cd_period == "Today" and not_submitted:
                st.warning(f"⏳ Not yet submitted today ({len(not_submitted)}): " + ", ".join(not_submitted))
            elif cd_period == "Today":
                st.success("✅ Everyone in this class has submitted today.")

            st.markdown("###### Roll call")
            st.dataframe(pd.DataFrame(rows), hide_index=True, width='stretch')

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            st.markdown("###### Topics needing attention in this class")
            topic_rows = analytics.topic_failure_ranking(cd_from, cd_to, cd_class)
            if topic_rows:
                top_t = topic_rows[:8]
                topic_df = pd.DataFrame({"Students affected": [t["student_count"] for t in top_t]},
                                        index=[t["topic"] for t in top_t])
                st.bar_chart(topic_df, horizontal=True, color="#0D0D0D", width='stretch')
            else:
                st.caption("No wrong-answer data in this period.")

        st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ─── STUDENT PROFILE ────────────────────────────────────────────────────
    elif dash_section == "👤 Student Profile":
        import pandas as pd
        from datetime import date as _date

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)

        existing_classes = db.get_classes()
        if not existing_classes:
            st.info("No student data yet. Use Daily Entry to add sessions, or generate demo data below.")
            with st.expander("Generate demo data"):
                st.caption("Generates 300 fake students (30 per class, Class 1–10) with a realistic "
                           "mix of sessions, wrong answers, and remedial assignments.")
                if st.button("👥  Generate 300 demo students", key="gen_demo"):
                    with st.spinner("Seeding demo data…"):
                        import seed_demo_data
                        seed_demo_data.seed()
                    st.success("Demo data ready. Refresh the page to see it.")
        else:
            col_p1, col_p2 = st.columns([1, 1])
            with col_p1:
                profile_class = st.selectbox("Class", existing_classes, key="profile_class")
            pool = db.get_students(profile_class)
            with col_p2:
                sp_labels = [f'{s["name"]}' for s in pool]
                sp_pick = st.selectbox("Student", sp_labels, key="sp_pick")
            student = pool[sp_labels.index(sp_pick)]

            current_levels   = analytics.get_current_levels()
            cur_level        = current_levels.get(student["id"])
            student_sessions = db.get_sessions(student_id=student["id"])
            history          = analytics.student_history(student["id"], sessions=student_sessions)
            topic_rows       = analytics.student_topic_breakdown(student["id"], sessions=student_sessions)
            mistake_rows     = analytics.student_mistake_breakdown(student["id"], sessions=student_sessions)
            remedial         = analytics.student_remedial_summary(student["id"], sessions=student_sessions)

            today_str      = _date.today().isoformat()
            today_sessions = [h for h in history if h["session_date"] == today_str]
            days_active    = len({h["session_date"] for h in history})
            last_active    = history[0]["session_date"] if history else "—"

            # Header
            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:20px;font-weight:700;margin-bottom:6px">{student["name"]}</div>',
                        unsafe_allow_html=True)
            header_cards = [
                ("Class", student["class_name"]), ("Grade", student["grade"]),
                ("Current Level", cur_level if cur_level is not None else "—"),
                ("Total Sessions", len(history)), ("Days Active", days_active),
                ("Last Active", last_active),
            ]
            card_html = '<div class="info-row" style="margin-left:0;margin-right:0">'
            for label, value in header_cards:
                card_html += (f'<div class="info-cell"><div class="il">{label}</div>'
                              f'<div class="iv" style="font-size:18px">{value}</div></div>')
            card_html += '</div>'
            st.markdown(card_html, unsafe_allow_html=True)
            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            # Today's update
            st.markdown("###### Today's update")
            if today_sessions:
                for h in today_sessions:
                    correct = h["total_questions"] - h["wrong_count"]
                    rem_txt = f' · Remedial: {h["remedial_status"]}' if h["remedial_status"] else ""
                    detail_lines = ""
                    if h["wrong_details"]:
                        parts = []
                        for qn in sorted(h["wrong_details"].keys()):
                            d = h["wrong_details"][qn]
                            mt = d.get("mistake_type") or "untagged"
                            ans = d.get("student_answer")
                            piece = f"Q{qn}: {mt}" + (f' ("{ans}")' if ans else "")
                            parts.append(piece)
                        detail_lines = (f'<div style="font-size:12px;color:#777;margin-top:6px">'
                                       f'{" &nbsp;·&nbsp; ".join(parts)}</div>')
                    st.markdown(
                        f'<div class="info-cell" style="margin-bottom:8px">'
                        f'<b>{h["worksheet_id"]}</b> — {correct}/{h["total_questions"]} correct '
                        f'({h["accuracy"]}%){rem_txt}{detail_lines}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No entry logged for today yet.")

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            # Growth charts
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
                st.caption("Not enough history yet — needs at least 2 sessions.")

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            # Topic weaknesses
            st.markdown("###### Topics needing attention")
            if topic_rows:
                topic_df = pd.DataFrame({"Times wrong": [t["count"] for t in topic_rows[:10]]},
                                        index=[t["topic"] for t in topic_rows[:10]])
                st.bar_chart(topic_df, horizontal=True, color="#0D0D0D", width='stretch')
            else:
                st.caption("No wrong-answer data yet — clean record so far!")

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            # Mistake types
            st.markdown("###### How they're thinking")
            st.caption("What kind of mistake this student makes — concept gaps need different follow-up than calculation slips.")
            if mistake_rows:
                mistake_df = pd.DataFrame({"Times": [m["count"] for m in mistake_rows]},
                                          index=[m["mistake_type"] for m in mistake_rows])
                st.bar_chart(mistake_df, horizontal=True, color="#0D0D0D", width='stretch')
            else:
                st.caption("No mistake-type data yet.")

            st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

            # Remedial tracking
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

            # Full history
            st.markdown("###### Full history")
            hist_df = pd.DataFrame([{
                "Date": h["session_date"],
                "Worksheet": h["worksheet_id"],
                "Score": f'{h["total_questions"] - h["wrong_count"]}/{h["total_questions"]}',
                "Accuracy": f'{h["accuracy"]}%',
                "Topics missed": h["resolved_topics"] or "—",
                "Mistake types": ", ".join(sorted({
                    d.get("mistake_type") for d in h["wrong_details"].values() if d.get("mistake_type")
                })) or "—",
                "Remedial": h["remedial_status"] or "—",
            } for h in history])
            st.dataframe(hist_df, hide_index=True, width='stretch')

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
