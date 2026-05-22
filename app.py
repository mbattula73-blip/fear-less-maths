"""
Fear Less Maths — Final Production App
LA Excellence Schools / IDPS Orchards
"""
import streamlit as st
from levels_data import LEVELS, SUBLEVELS, SHEET_OPTIONS, get_tier
from pdf_engine import build_pdf

st.set_page_config(
    page_title="Fear Less Maths",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

*, html, body { font-family: 'IBM Plex Sans', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ═══ SIDEBAR ═══════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: #0D0D0D !important;
    border-right: 1px solid #1C1C1C;
    width: 300px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }
section[data-testid="stSidebar"] * { color: #D4D4D4 !important; }

.sb-header {
    padding: 32px 28px 24px;
    background: #0D0D0D;
    border-bottom: 1px solid #1C1C1C;
}
.sb-brand {
    font-family: 'Playfair Display', serif !important;
    font-size: 26px; font-weight: 700;
    color: #FFFFFF !important; line-height: 1.1;
    letter-spacing: -.02em; margin-bottom: 6px;
}
.sb-sub {
    font-size: 11px; color: #555 !important;
    text-transform: uppercase; letter-spacing: .1em;
}
.sb-stats {
    display: flex; gap: 0;
    border-top: 1px solid #1C1C1C;
    margin-top: 20px;
}
.sb-stat {
    flex: 1; padding: 12px 10px; text-align: center;
    border-right: 1px solid #1C1C1C;
}
.sb-stat:last-child { border-right: none; }
.sb-stat .n { font-family: 'Playfair Display',serif !important;
              font-size: 20px; color: #FFF !important; }
.sb-stat .l { font-size: 9px; color: #444 !important;
              text-transform: uppercase; letter-spacing: .06em; }

.sb-section {
    padding: 20px 28px 8px;
    font-size: 10px; font-weight: 600;
    letter-spacing: .1em; text-transform: uppercase;
    color: #3A3A3A !important;
}

/* sidebar select */
section[data-testid="stSidebar"] .stSelectbox label { display: none !important; }
section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
    background: #161616 !important;
    border: 1px solid #282828 !important;
    border-radius: 6px !important;
    color: #D4D4D4 !important;
    font-size: 13px !important;
}
section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div:hover {
    border-color: #444 !important;
}
section[data-testid="stSidebar"] .stSelectbox { padding: 0 28px 12px; }

.sb-tiers { padding: 0 28px 28px; }
.sb-tier {
    display: flex; align-items: center; gap: 10px;
    padding: 9px 12px; margin-bottom: 5px;
    border: 1px solid #1C1C1C; border-radius: 6px;
    background: #111; font-size: 12px;
    color: #888 !important;
}
.sb-tier .pip { width:8px;height:8px;border-radius:50%;flex-shrink:0; }

/* ═══ MAIN ══════════════════════════════════════════════ */
.main-area {
    background: #F4F2EE;
    min-height: 100vh;
    display: flex; flex-direction: column;
}

/* Top bar */
.topbar {
    background: #FFFFFF;
    border-bottom: 1.5px solid #E5E2DC;
    padding: 0 44px;
    height: 58px;
    display: flex; align-items: center;
    justify-content: space-between;
    position: sticky; top: 0; z-index: 100;
}
.topbar-left { display: flex; align-items: center; gap: 20px; }
.topbar-title {
    font-family: 'Playfair Display',serif;
    font-size: 18px; color: #111;
}
.topbar-crumb { font-size: 12px; color: #AAA; }
.topbar-right { font-size: 11px; color: #CCC; letter-spacing: .04em; }

/* Worksheet ID card */
.ws-hero {
    margin: 32px 44px 0;
    background: #0D0D0D;
    border-radius: 10px;
    padding: 28px 36px;
    display: flex; align-items: center;
    justify-content: space-between;
}
.ws-hero-id {
    font-family: 'Playfair Display',serif;
    font-size: 42px; color: #FFF;
    letter-spacing: -.03em; line-height: 1;
}
.ws-hero-meta { text-align: right; }
.ws-hero-topic { font-size: 14px; color: #888; margin-bottom: 4px; }
.ws-hero-tier { font-size: 11px; color: #444;
                text-transform: uppercase; letter-spacing: .08em; }

/* Tier track */
.tier-track {
    display: flex; margin: 20px 44px 0;
    background: #FFFFFF;
    border: 1.5px solid #E5E2DC;
    border-radius: 8px; overflow: hidden;
}
.tier-step {
    flex: 1; padding: 12px 10px; text-align: center;
    border-right: 1px solid #E5E2DC;
    font-size: 11px; color: #AAA;
    background: #FAFAFA;
}
.tier-step:last-child { border-right: none; }
.tier-step.on { background:#0D0D0D; color:#FFF; }
.tier-step .tn {
    font-size: 9px; display: block; margin-bottom: 3px;
    opacity: .5; text-transform: uppercase; letter-spacing: .06em;
}
.tier-step .tnm { font-weight: 600; }

/* Info row */
.info-row {
    display: grid; grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 12px; margin: 16px 44px 0;
}
.info-cell {
    background: #FFFFFF; border: 1.5px solid #E5E2DC;
    border-radius: 8px; padding: 16px 18px;
}
.info-cell .il { font-size: 10px; color: #AAA;
                 text-transform: uppercase; letter-spacing: .06em; margin-bottom: 5px; }
.info-cell .iv { font-size: 14px; font-weight: 600; color: #111; }

/* Action zone */
.action-zone { margin: 20px 44px 0; }

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
.stButton > button:active { transform: translateY(0) !important; }

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
    border-radius: 8px; padding: 16px 20px;
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

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid #E5E2DC !important;
    gap: 0; padding: 0 44px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #AAA !important; font-size: 13px !important;
    font-weight: 500 !important;
    padding: 14px 24px !important;
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

/* Batch grid */
.batch-dl-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-top: 12px; }
.batch-dl-cell {
    background: #FFF; border: 1.5px solid #E5E2DC;
    border-radius: 8px; padding: 14px 10px; text-align: center;
}
.batch-dl-cell .bc { font-family: 'Playfair Display',serif;
                    font-size: 17px; color: #111; }
.batch-dl-cell .bn { font-size: 10px; color: #AAA; margin: 2px 0 10px; }

/* Footer bar */
.footer-bar {
    background: #0D0D0D; padding: 14px 44px;
    display: flex; align-items: center;
    justify-content: space-between; margin-top: auto;
}
.footer-bar .fl { font-size: 11px; color: #555; }
.footer-bar .fr { font-size: 11px; color: #333; }

/* Divider */
hr { border: none; border-top: 1.5px solid #E5E2DC !important; margin: 0 44px !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-header">
        <div class="sb-brand">Fear Less<br>Maths</div>
        <div class="sb-sub">Worksheet Generator</div>
        <div class="sb-stats">
            <div class="sb-stat"><div class="n">20</div><div class="l">Levels</div></div>
            <div class="sb-stat"><div class="n">280</div><div class="l">Sublvls</div></div>
            <div class="sb-stat"><div class="n">2240</div><div class="l">Sheets</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Level
    st.markdown('<div class="sb-section">Level</div>', unsafe_allow_html=True)
    lvl_opts  = [f"Level {n}  ·  {d['name']}" for n, d in LEVELS.items()]
    lvl_sel   = st.selectbox("lvl", lvl_opts, index=6, key="lvl")
    level_num = int(lvl_sel.split()[1])

    # Sublevel
    st.markdown('<div class="sb-section">Sublevel</div>', unsafe_allow_html=True)
    subs      = SUBLEVELS.get(level_num, [])
    sub_opts  = [f"{c}  ·  {t}" for c, t in subs]
    sub_sel   = st.selectbox("sub", sub_opts, key="sub")
    sublevel_code = sub_sel.split("  ·  ")[0].strip()
    topic         = sub_sel.split("  ·  ", 1)[1].strip() if "  ·  " in sub_sel else ""

    # Tier guide
    st.markdown("""
    <div class="sb-section" style="margin-top:8px">Tier Progression</div>
    <div class="sb-tiers">
        <div class="sb-tier"><div class="pip" style="background:#888"></div>Sheet 1 — See it · Intuition</div>
        <div class="sb-tier"><div class="pip" style="background:#777"></div>Sheet 2 — Try it · Concept</div>
        <div class="sb-tier"><div class="pip" style="background:#555"></div>Sheet 3 — Do it · Practice</div>
        <div class="sb-tier"><div class="pip" style="background:#333"></div>Sheet 4 — Master it · Mastery</div>
        <div class="sb-tier"><div class="pip" style="background:#222;border:1px dashed #555"></div>Sheets R — Remedial</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

# Top bar
st.markdown(f"""
<div class="topbar">
    <div class="topbar-left">
        <div class="topbar-title">Worksheet Generator</div>
        <div class="topbar-crumb">
            Level {level_num} &nbsp;/&nbsp; {LEVELS[level_num]['name']}
            &nbsp;/&nbsp; {sublevel_code}: {topic}
        </div>
    </div>
    <div class="topbar-right">A4 · B&W · 20 Questions · Print Ready</div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["  Generate Single Worksheet  ", "  Batch — All 8 Sheets  "])

# ─── TAB 1 ────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div style="height:28px"></div>', unsafe_allow_html=True)

    # Sheet selector - clean row
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
            <div style="font-size:11px;color:#555;text-transform:uppercase;
                        letter-spacing:.08em;margin-bottom:8px">Worksheet</div>
            <div class="ws-hero-id">{ws_id}</div>
        </div>
        <div class="ws-hero-meta">
            <div class="ws-hero-topic">{topic}</div>
            <div class="ws-hero-tier">{tier}</div>
            <div style="font-size:10px;color:#333;margin-top:8px">
                LA Excellence Schools
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tier progression track
    steps  = [("1","See it","Intuition"),("2","Try it","Concept"),
              ("3","Do it","Practice"),("4","Master it","Mastery")]
    track  = '<div class="tier-track">'
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
            <div class="iv">20 Qs · 2 pages</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    # Generate button + download
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
    st.markdown('<div style="height:28px"></div>', unsafe_allow_html=True)

    # Batch hero
    st.markdown(f"""
    <div style="margin:0 44px">
        <div class="ws-hero">
            <div>
                <div style="font-size:11px;color:#555;text-transform:uppercase;
                            letter-spacing:.08em;margin-bottom:8px">Batch Generation</div>
                <div class="ws-hero-id">{sublevel_code}</div>
                <div style="font-size:14px;color:#888;margin-top:6px">{topic}</div>
            </div>
            <div class="ws-hero-meta">
                <div class="ws-hero-topic">8 worksheets</div>
                <div class="ws-hero-tier">Sheets 1 · 2 · 3 · 4 · 1R · 2R · 3R · 4R</div>
                <div style="font-size:10px;color:#333;margin-top:8px">
                    Level {level_num} — {LEVELS[level_num]['name']}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    col_b1, col_b2 = st.columns([2, 1])
    with col_b1:
        if st.button(f"⚡  Generate All 8 Sheets for {sublevel_code}", type="primary", key="batch"):
            sheets = ["1","2","3","4","1R","2R","3R","4R"]
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
            results = st.session_state["batch_results"]
            total_kb = sum(len(v) for v in results.values()) // 1024
            st.markdown(f"""
            <div class="success-card" style="margin:0 44px 0 0">
                <div class="ck">✓</div>
                <div>{len(results)} worksheets ready &nbsp;·&nbsp; {total_kb} KB total</div>
            </div>
            """, unsafe_allow_html=True)

            names = {"1":"See it","2":"Try it","3":"Do it","4":"Master",
                     "1R":"Redo 1","2R":"Redo 2","3R":"Redo 3","4R":"Redo 4"}

            # Row 1: sheets 1-4
            row1 = st.columns(4)
            # Row 2: sheets 1R-4R
            row2 = st.columns(4)
            all_rows = [row1, row2]
            items = list(results.items())
            for idx, (sn, data) in enumerate(items):
                row, col = idx // 4, idx % 4
                with all_rows[row][col]:
                    st.markdown(f"""
                    <div style="text-align:center;margin-bottom:6px">
                        <div style="font-family:'Playfair Display',serif;font-size:16px;
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

# Footer
st.markdown(f"""
<div class="footer-bar">
    <div class="fl">LA Excellence Schools / IDPS Orchards &nbsp;·&nbsp; Fear Less Maths</div>
    <div class="fr">Currently: Level {level_num} · {sublevel_code}</div>
</div>
""", unsafe_allow_html=True)
