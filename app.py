"""
Fear Less Maths — Final Production App
LA Excellence Schools / IDPS Orchards
"""
import streamlit as st
from levels_data import LEVELS, SUBLEVELS, SHEET_OPTIONS, get_tier
from pdf_engine import build_pdf
import db
import analytics
import concept_tagger
from ws_helpers import numbered_questions, remedial_id_for, build_whatsapp_report

st.set_page_config(
    page_title="Fear Less Maths",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

*, html, body { font-family: 'IBM Plex Sans', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ═══ HEADER BAR ══════════════════════════════════════════ */
.app-header {
    background: #0D0D0D;
    padding: 16px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}
.app-brand {
    font-family: 'Playfair Display', serif !important;
    font-size: 22px; font-weight: 700;
    color: #FFFFFF !important;
    letter-spacing: -.02em;
}
.app-sub {
    font-size: 10px; color: #555 !important;
    text-transform: uppercase; letter-spacing: .1em;
}

/* ═══ SELECTOR STRIP ══════════════════════════════════════ */
.selector-strip {
    background: #FFFFFF;
    border-bottom: 1.5px solid #E5E2DC;
    padding: 16px 24px;
}

/* ═══ MAIN CONTENT ════════════════════════════════════════ */
.main-area {
    background: #F4F2EE;
    min-height: 100vh;
    padding: 0 0 40px;
}

/* Worksheet ID card */
.ws-hero {
    margin: 20px 24px 0;
    background: #0D0D0D;
    border-radius: 10px;
    padding: 20px 24px;
    display: flex; align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}
.ws-hero-id {
    font-family: 'Playfair Display',serif;
    font-size: 36px; color: #FFF;
    letter-spacing: -.03em; line-height: 1;
}
.ws-hero-meta { text-align: right; }
.ws-hero-topic { font-size: 13px; color: #888; margin-bottom: 4px; }
.ws-hero-tier { font-size: 11px; color: #444;
                text-transform: uppercase; letter-spacing: .08em; }

/* Tier track */
.tier-track {
    display: flex; margin: 14px 24px 0;
    background: #FFFFFF;
    border: 1.5px solid #E5E2DC;
    border-radius: 8px; overflow: hidden;
}
.tier-step {
    flex: 1; padding: 10px 6px; text-align: center;
    border-right: 1px solid #E5E2DC;
    font-size: 10px; color: #AAA;
    background: #FAFAFA;
}
.tier-step:last-child { border-right: none; }
.tier-step.on { background:#0D0D0D; color:#FFF; }
.tier-step .tn {
    font-size: 9px; display: block; margin-bottom: 2px;
    opacity: .5; text-transform: uppercase; letter-spacing: .06em;
}
.tier-step .tnm { font-weight: 600; font-size: 11px; }

/* Info row */
.info-row {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 10px; margin: 12px 24px 0;
}
@media (min-width: 600px) {
    .info-row { grid-template-columns: 1fr 1fr 1fr 1fr; }
}
.info-cell {
    background: #FFFFFF; border: 1.5px solid #E5E2DC;
    border-radius: 8px; padding: 12px 14px;
}
.info-cell .il { font-size: 10px; color: #AAA;
                 text-transform: uppercase; letter-spacing: .06em; margin-bottom: 4px; }
.info-cell .iv { font-size: 13px; font-weight: 600; color: #111; }

/* Buttons */
.stButton > button {
    font-family: 'IBM Plex Sans',sans-serif !important;
    background: #0D0D0D !important; color: #FFFFFF !important;
    border: none !important; border-radius: 8px !important;
    font-size: 15px !important; font-weight: 600 !important;
    padding: 14px 40px !important; width: 100% !important;
    letter-spacing: .01em !important;
    transition: transform .12s, background .12s !important;
}
.stButton > button:hover {
    background: #222 !important; transform: translateY(-1px) !important;
}

.stDownloadButton > button {
    font-family: 'IBM Plex Sans',sans-serif !important;
    background: #FFFFFF !important; color: #0D0D0D !important;
    border: 2px solid #0D0D0D !important;
    border-radius: 8px !important;
    font-size: 15px !important; font-weight: 600 !important;
    padding: 14px 0 !important; width: 100% !important;
    transition: all .12s !important;
}
.stDownloadButton > button:hover {
    background: #0D0D0D !important; color: #FFF !important;
}

/* Success */
.success-card {
    background: #FFF; border: 1.5px solid #0D0D0D;
    border-radius: 8px; padding: 14px 18px;
    display: flex; align-items: center; gap: 12px;
    font-weight: 600; font-size: 14px; color: #111;
    margin: 12px 0;
}
.success-card .ck {
    width: 28px; height: 28px; border-radius: 50%;
    background: #0D0D0D; color: #FFF;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; flex-shrink: 0;
}

/* Selectbox labels */
.stSelectbox label {
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: .06em !important;
    color: #555 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid #E5E2DC !important;
    gap: 0; padding: 0 24px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #AAA !important; font-size: 13px !important;
    font-weight: 500 !important;
    padding: 12px 16px !important;
    border: none !important; border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
    color: #0D0D0D !important; font-weight: 700 !important;
    border-bottom: 2px solid #0D0D0D !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }

/* Progress */
.stProgress > div > div { background: #0D0D0D !important; }

/* Tier guide strip */
.tier-guide {
    margin: 12px 24px 0;
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 6px;
}
@media (min-width: 600px) {
    .tier-guide { grid-template-columns: repeat(5, 1fr); }
}
.tg-item {
    display: flex; align-items: center; gap: 8px;
    padding: 8px 10px;
    background: #FFF; border: 1px solid #E5E2DC;
    border-radius: 6px; font-size: 11px; color: #888;
}
.tg-pip { width:7px;height:7px;border-radius:50%;flex-shrink:0; }

/* Footer */
.footer-bar {
    background: #0D0D0D; padding: 12px 24px;
    display: flex; align-items: center;
    justify-content: space-between; margin-top: 40px;
    flex-wrap: wrap; gap: 8px;
}
.footer-bar .fl { font-size: 11px; color: #555; }
.footer-bar .fr { font-size: 11px; color: #333; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="app-header">
    <div>
        <div class="app-brand">Fear Less Maths</div>
        <div class="app-sub">Worksheet Generator · LA Excellence Schools</div>
    </div>
    <div style="font-size:11px;color:#444">A4 · B&W · 20 Questions · Print Ready</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SELECTORS — always visible, top of page (works on mobile & desktop)
# ═══════════════════════════════════════════════════════════════════════════════
with st.container():
    st.markdown('<div style="background:#fff;padding:16px 24px 4px;border-bottom:1.5px solid #E5E2DC">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        lvl_opts = [f"Level {n}  ·  {d['name']}" for n, d in LEVELS.items()]
        lvl_sel  = st.selectbox("Level", lvl_opts, index=6, key="lvl")
        level_num = int(lvl_sel.split()[1])

    with col2:
        subs     = SUBLEVELS.get(level_num, [])
        sub_opts = [f"{c}  ·  {t}" for c, t in subs]
        sub_sel  = st.selectbox("Sublevel", sub_opts, key="sub")
        sublevel_code = sub_sel.split("  ·  ")[0].strip()
        topic         = sub_sel.split("  ·  ", 1)[1].strip() if "  ·  " in sub_sel else ""

    with col3:
        st.markdown(f"""
        <div style="padding-top:28px;font-size:12px;color:#888;line-height:1.6">
            Level {level_num}<br>
            <b style="color:#111">{sublevel_code}</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  Generate Single Worksheet  ", "  Batch — All 8 Sheets  ",
    "  🏷️ Concept Tags  ", "  ✏️ Daily Entry  ", "  📊 Dashboard  ",
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

# ─── TAB 4 — DAILY ENTRY ───────────────────────────────────────────────────────
with tab4:
    import pandas as pd
    from datetime import date as _date
    from ws_helpers import build_whatsapp_link

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


# ─── TAB 5 — DASHBOARD ─────────────────────────────────────────────────────────
with tab5:
    import pandas as pd
    from datetime import date as _date, timedelta as _timedelta

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)

    students_exist = bool(db.get_classes())
    if not students_exist:
        st.info("No data yet. Add your roster and log a few entries in the Daily Entry tab first.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        col_h, col_f = st.columns([2, 1])
        with col_h:
            st.markdown("##### Dashboard")
        with col_f:
            ad_preset = st.selectbox("Date range", ["Today", "Last 7 days", "Last 30 days", "All time"],
                                     index=1, key="ad_preset", label_visibility="collapsed")
        ad_from = ad_to = None
        if ad_preset == "Today":
            ad_from = ad_to = _date.today().isoformat()
        elif ad_preset == "Last 7 days":
            ad_from = (_date.today() - _timedelta(days=6)).isoformat(); ad_to = _date.today().isoformat()
        elif ad_preset == "Last 30 days":
            ad_from = (_date.today() - _timedelta(days=29)).isoformat(); ad_to = _date.today().isoformat()

        # ── Summary metric cards ───────────────────────────────────────────────
        summary = analytics.school_summary()
        cards = [
            ("Students", summary["total_students"]),
            ("Avg Level", summary["avg_level"]),
            ("Seen Today", summary["students_seen_today"]),
            ("Done Today", f'{summary["completion_rate_today"]}%'),
        ]
        card_html = '<div class="info-row" style="margin-left:0;margin-right:0">'
        for label, value in cards:
            card_html += (f'<div class="info-cell"><div class="il">{label}</div>'
                          f'<div class="iv" style="font-size:22px">{value}</div></div>')
        card_html += '</div>'
        st.markdown(card_html, unsafe_allow_html=True)

        st.markdown('<div style="height:28px"></div>', unsafe_allow_html=True)

        # ── Top struggling topics ──────────────────────────────────────────────
        st.markdown("###### Where students are struggling most")
        st.caption(f"Topics with the most students struggling · {ad_preset.lower()}")
        topic_rows = analytics.topic_failure_ranking(ad_from, ad_to)
        if topic_rows:
            top = topic_rows[:10]
            chart_df = pd.DataFrame(
                {"Students": [r["student_count"] for r in top]},
                index=[r["topic"] for r in top],
            )
            st.bar_chart(chart_df, horizontal=True, color="#0D0D0D", width='stretch')
        else:
            st.caption("No wrong-answer data in this range yet.")

        st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

        # ── Class comparison ───────────────────────────────────────────────────
        st.markdown("###### Class overview")
        class_rows = analytics.class_summary(ad_from, ad_to)
        if class_rows:
            comp_df = pd.DataFrame([{
                "Class": c["class_name"],
                "Students": c["student_count"],
                "Avg Accuracy": f'{c["avg_accuracy"]}%' if c["avg_accuracy"] is not None else "—",
                "Sessions": c["sessions_in_range"],
            } for c in class_rows])
            st.dataframe(comp_df, hide_index=True, width='stretch')

            for c in class_rows:
                if c["level_distribution"]:
                    st.caption(f"{c['class_name']} — level distribution")
                    lvl_df = pd.DataFrame({"Students": list(c["level_distribution"].values())},
                                          index=[f"L{k}" for k in c["level_distribution"].keys()])
                    st.bar_chart(lvl_df, color="#0D0D0D", width='stretch')

        st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

        # ── Grade overview ─────────────────────────────────────────────────────
        st.markdown("###### Grade overview")
        grade_rows = analytics.grade_rollup(ad_from, ad_to)
        if grade_rows:
            grade_df = pd.DataFrame([{
                "Grade": g["grade"],
                "Students": g["student_count"],
                "Avg Accuracy": f'{g["avg_accuracy"]}%' if g["avg_accuracy"] is not None else "—",
            } for g in grade_rows])
            st.dataframe(grade_df, hide_index=True, width='stretch')

        st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


st.markdown(f"""
<div class="footer-bar">
    <div class="fl">LA Excellence Schools / IDPS Orchards &nbsp;·&nbsp; Fear Less Maths</div>
    <div class="fr">Level {level_num} · {sublevel_code}</div>
</div>
""", unsafe_allow_html=True)
