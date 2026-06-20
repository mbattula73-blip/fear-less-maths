"""
Fear Less Maths — Final Production App
LA Excellence Schools / IDPS Orchards
"""
import streamlit as st
from levels_data import LEVELS, SUBLEVELS, SHEET_OPTIONS, get_tier
from pdf_engine import build_pdf
import db
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
tab1, tab2, tab3, tab4 = st.tabs([
    "  Generate Single Worksheet  ", "  Batch — All 8 Sheets  ",
    "  📑 Topic Tag Map  ", "  ✏️ Daily Entry  ",
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

# ─── TAB 3 — TOPIC TAG MAP (Admin) ─────────────────────────────────────────────
with tab3:
    import pandas as pd

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)
    st.markdown("##### Topic Tag Map")
    st.caption(
        "Map each question number on a worksheet to the topic/skill it tests. "
        "Once tagged, every wrong-question entry in Daily Entry will auto-resolve to its topic."
    )

    col_t1, col_t2 = st.columns([1, 2])
    with col_t1:
        tag_sheet_lbls = [lbl for _, lbl in SHEET_OPTIONS]
        tag_sheet_sel = st.selectbox("Sheet to tag", tag_sheet_lbls, key="tag_sheet")
        tag_sheet_num = SHEET_OPTIONS[tag_sheet_lbls.index(tag_sheet_sel)][0]
    tag_ws_id = f"{sublevel_code}-{tag_sheet_num}"

    with col_t2:
        st.markdown(f"""
        <div style="padding-top:28px;font-size:13px;color:#888">
            Tagging worksheet <b style="color:#111">{tag_ws_id}</b>
            &nbsp;·&nbsp; {topic}
        </div>
        """, unsafe_allow_html=True)

    try:
        q_list = numbered_questions(sublevel_code, tag_sheet_num)
    except Exception as e:
        q_list = []
        st.error(f"Could not load questions for {tag_ws_id}: {e}")

    if q_list:
        existing_tags = db.get_worksheet_tags(tag_ws_id)
        df = pd.DataFrame(
            [{"Q#": n, "Question preview": preview, "Topic": existing_tags.get(n, "")}
             for n, preview in q_list]
        )

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        edited_df = st.data_editor(
            df,
            column_config={
                "Q#": st.column_config.NumberColumn("Q#", disabled=True, width="small"),
                "Question preview": st.column_config.TextColumn("Question preview", disabled=True, width="large"),
                "Topic": st.column_config.TextColumn("Topic", width="medium"),
            },
            hide_index=True,
            width='stretch',
            key=f"editor_{tag_ws_id}",
        )

        col_s1, col_s2 = st.columns([1, 1])
        with col_s1:
            if st.button("💾  Save Topic Tags", type="primary", key="save_tags"):
                tag_map = {
                    int(row["Q#"]): row["Topic"]
                    for _, row in edited_df.iterrows()
                    if str(row["Topic"]).strip()
                }
                db.set_worksheet_tags(tag_ws_id, tag_map)
                st.success(f"Saved {len(tag_map)} topic tags for {tag_ws_id}.")

        with col_s2:
            tagged_count = sum(1 for _, r in edited_df.iterrows() if str(r["Topic"]).strip())
            st.caption(f"{tagged_count} / {len(edited_df)} questions tagged in this editor (unsaved changes included).")

        st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)
        st.markdown("###### Bulk paste (CSV)")
        st.caption('Paste rows as "Q#,Topic" — one per line. This will overwrite tags for the Q# numbers you include; existing tags for other Q#s on this worksheet are kept unless re-saved via the table above.')
        bulk_text = st.text_area(
            "CSV paste box",
            placeholder="11,fraction subtraction unlike denominators\n12,LCM word problems",
            height=120,
            key=f"bulk_{tag_ws_id}",
            label_visibility="collapsed",
        )
        if st.button("📋  Apply Bulk Paste", key="apply_bulk"):
            if not bulk_text.strip():
                st.warning("Paste some rows first.")
            else:
                parsed = {}
                errors = []
                for i, line in enumerate(bulk_text.strip().splitlines(), 1):
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",", 1)
                    if len(parts) != 2:
                        errors.append(f"Line {i}: expected 'Q#,Topic' — got '{line}'")
                        continue
                    qnum_str, topic_str = parts[0].strip(), parts[1].strip()
                    if not qnum_str.isdigit():
                        errors.append(f"Line {i}: '{qnum_str}' is not a valid question number")
                        continue
                    if not topic_str:
                        errors.append(f"Line {i}: empty topic for Q{qnum_str}")
                        continue
                    parsed[int(qnum_str)] = topic_str

                if errors:
                    st.error("Some rows could not be parsed:\n\n" + "\n".join(errors))
                if parsed:
                    merged = db.get_worksheet_tags(tag_ws_id)
                    merged.update(parsed)
                    db.set_worksheet_tags(tag_ws_id, merged)
                    st.success(f"Applied {len(parsed)} tags from bulk paste to {tag_ws_id}. Refresh the table above to see them.")
                    st.rerun()
    else:
        st.info("No questions found for this worksheet.")

    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)
    st.markdown("###### Worksheets tagged so far")
    tagged_list = db.list_tagged_worksheets()
    if tagged_list:
        st.dataframe(pd.DataFrame(tagged_list).rename(columns={"worksheet_id": "Worksheet", "n": "Tagged Qs"}),
                     hide_index=True, width='stretch')
    else:
        st.caption("No worksheets tagged yet.")

    st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── TAB 4 — DAILY ENTRY ───────────────────────────────────────────────────────
with tab4:
    from datetime import date as _date

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    st.markdown('<div style="margin:0 24px">', unsafe_allow_html=True)
    st.markdown("##### Daily Entry")
    st.caption("Log a student's worksheet attempt. Wrong questions auto-resolve to topics, "
               "the matching remedial worksheet is auto-linked, and a parent report is generated.")

    # ── Student picker / add-new ──────────────────────────────────────────────
    st.markdown("###### Student")
    existing_classes = db.get_classes()
    default_mode_idx = 1 if not existing_classes else 0
    pick_mode = st.radio("Student source", ["Pick existing", "Add new"], horizontal=True,
                          index=default_mode_idx, key="de_student_mode", label_visibility="collapsed")

    de_student_id = None
    de_student_name = None
    de_class = None
    de_grade = None

    if pick_mode == "Pick existing":
        if not existing_classes:
            st.info("No students added yet — switch to 'Add new' to add your first student.")
        else:
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                de_class_pick = st.selectbox("Class", existing_classes, key="de_class_pick")
            students_in_class = db.get_students(de_class_pick)
            with col_p2:
                if students_in_class:
                    names = [s["name"] for s in students_in_class]
                    de_name_pick = st.selectbox("Student", names, key="de_name_pick")
                    picked = next(s for s in students_in_class if s["name"] == de_name_pick)
                    de_student_id, de_student_name, de_class, de_grade = (
                        picked["id"], picked["name"], picked["class_name"], picked["grade"]
                    )
                else:
                    st.info("No students in this class yet — switch to 'Add new'.")
    else:
        col_n1, col_n2, col_n3 = st.columns(3)
        with col_n1:
            new_name = st.text_input("Student name", key="de_new_name")
        with col_n2:
            new_class = st.text_input("Class", key="de_new_class", placeholder="e.g. Class A")
        with col_n3:
            new_grade = st.number_input("Grade", min_value=1, max_value=10, value=1, key="de_new_grade")
        if new_name.strip() and new_class.strip():
            de_student_name, de_class, de_grade = new_name.strip(), new_class.strip(), int(new_grade)

    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

    # ── Worksheet + wrong questions ───────────────────────────────────────────
    st.markdown("###### Worksheet attempted")
    col_w1, col_w2, col_w3 = st.columns([1, 1, 1])
    with col_w1:
        de_date = st.date_input("Date", value=_date.today(), key="de_date")
    with col_w2:
        de_sheet_lbls = [lbl for _, lbl in SHEET_OPTIONS]
        de_sheet_sel = st.selectbox("Sheet", de_sheet_lbls, key="de_sheet")
        de_sheet_num = SHEET_OPTIONS[de_sheet_lbls.index(de_sheet_sel)][0]
    with col_w3:
        de_total_q = st.number_input("Total questions", min_value=1, max_value=50, value=20, key="de_total_q")

    de_ws_id = f"{sublevel_code}-{de_sheet_num}"
    st.markdown(f"""
    <div style="font-size:13px;color:#888;margin:4px 0 12px">
        Worksheet: <b style="color:#111">{de_ws_id}</b> &nbsp;·&nbsp; {topic} &nbsp;·&nbsp; Level {level_num}
    </div>
    """, unsafe_allow_html=True)

    de_wrong_str = st.text_input(
        "Wrong question numbers (comma-separated, leave blank if all correct)",
        key="de_wrong_qs", placeholder="e.g. 17, 18",
    )

    de_wrong_qs = []
    de_parse_error = None
    if de_wrong_str.strip():
        for part in de_wrong_str.split(","):
            part = part.strip()
            if not part:
                continue
            if not part.isdigit():
                de_parse_error = f"'{part}' is not a valid question number"
                break
            qn = int(part)
            if qn < 1 or qn > de_total_q:
                de_parse_error = f"Q{qn} is out of range (1–{de_total_q})"
                break
            de_wrong_qs.append(qn)

    if de_parse_error:
        st.error(de_parse_error)

    # ── Live preview: resolved topics + remedial + WhatsApp report ───────────
    if not de_parse_error and de_student_name and de_class:
        resolved = db.resolve_topics(de_ws_id, de_wrong_qs) if de_wrong_qs else {}
        remedial_id = remedial_id_for(sublevel_code, de_sheet_num) if de_wrong_qs else None

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        st.markdown("###### Preview")

        if de_wrong_qs:
            for qn, t in resolved.items():
                tag_color = "#888" if t == "(untagged)" else "#111"
                st.markdown(f"<div style='font-size:13px;margin-bottom:2px'>Q{qn} → "
                            f"<span style='color:{tag_color}'>{t}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:13px;margin-top:8px;color:#555'>"
                        f"Remedial worksheet: <b>{remedial_id}</b></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size:13px;color:#555'>No wrong questions — full marks.</div>",
                        unsafe_allow_html=True)

        whatsapp_msg = build_whatsapp_report(
            de_student_name, de_ws_id, int(de_total_q), de_wrong_qs, resolved, remedial_id
        )
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        st.markdown("###### Parent WhatsApp report")
        whatsapp_key = f"de_whatsapp_preview_{de_ws_id}_{de_wrong_str}_{de_student_name}"
        st.text_area("WhatsApp message", whatsapp_msg, height=100, key=whatsapp_key)

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        if st.button("💾  Save Entry", type="primary", key="de_save"):
            sid = de_student_id or db.add_student(de_student_name, de_class, de_grade)
            session_id = db.add_session(
                session_date=de_date.isoformat(),
                student_id=sid,
                class_name=de_class,
                grade=int(de_grade),
                level_num=level_num,
                worksheet_id=de_ws_id,
                wrong_qs=de_wrong_qs,
                resolved_topics=resolved,
                total_questions=int(de_total_q),
                remedial_id=remedial_id,
            )
            st.success(f"Saved entry for {de_student_name} — {de_ws_id} "
                       f"({len(de_wrong_qs)} wrong). Session #{session_id}.")
    elif not de_student_name or not de_class:
        st.info("Pick or add a student above to continue.")

    st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


st.markdown(f"""
<div class="footer-bar">
    <div class="fl">LA Excellence Schools / IDPS Orchards &nbsp;·&nbsp; Fear Less Maths</div>
    <div class="fr">Level {level_num} · {sublevel_code}</div>
</div>
""", unsafe_allow_html=True)
