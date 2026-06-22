"""
ui_common.py — shared page chrome for Fear Less Maths.

Holds the page config, global CSS, header bar, Level/Sublevel selector, and
footer — used by BOTH app.py (the teacher's full control panel) and
pages/1_Daily_Entry.py (the standalone staff entry screen).

Why this matters: app.py and pages/1_Daily_Entry.py are two pages of the
SAME Streamlit app/deployment, so they share one running process and one
filesystem — which means they share the exact same db.py / flm_data.db.
An entry staff log on the Daily Entry page shows up immediately in the
teacher's Student Profile tab. No second database, no sync needed.

Splitting the CSS/header/selector out here (instead of duplicating it in
both files) means any visual change only needs to be made once.
"""
import streamlit as st
from levels_data import LEVELS, SUBLEVELS

MAIN_CSS = """
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
"""

# Hides Streamlit's auto-generated multipage nav links in the sidebar, so a
# staff member opened directly on the Daily Entry page has no visible way to
# wander into the teacher's tabs (and vice versa). This is a UX separation,
# not an access-control boundary — both pages are still reachable by anyone
# who has/guesses the URL. Layer on a PIN gate if you need real auth later.
HIDE_NAV_CSS = '<style>[data-testid="stSidebarNav"] {display: none;}</style>'


def setup_page(page_title: str = "Fear Less Maths", hide_nav: bool = True):
    st.set_page_config(
        page_title=page_title,
        page_icon="📐",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(MAIN_CSS, unsafe_allow_html=True)
    if hide_nav:
        st.markdown(HIDE_NAV_CSS, unsafe_allow_html=True)


def render_header(subtitle: str = "Worksheet Generator · LA Excellence Schools",
                   badge: str = "A4 · B&W · 20 Questions · Print Ready"):
    st.markdown(f"""
    <div class="app-header">
        <div>
            <div class="app-brand">Fear Less Maths</div>
            <div class="app-sub">{subtitle}</div>
        </div>
        <div style="font-size:11px;color:#444">{badge}</div>
    </div>
    """, unsafe_allow_html=True)


def render_level_selector(key_prefix: str = ""):
    """
    Renders the Level / Sublevel selector strip. Returns (level_num, sublevel_code, topic).
    key_prefix lets each page keep its own independent selectbox state
    (e.g. "de_" on the Daily Entry page) since Streamlit widget keys must be
    unique within a single page run.
    """
    with st.container():
        st.markdown('<div style="background:#fff;padding:16px 24px 4px;'
                     'border-bottom:1.5px solid #E5E2DC">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            lvl_opts = [f"Level {n}  ·  {d['name']}" for n, d in LEVELS.items()]
            lvl_sel = st.selectbox("Level", lvl_opts, index=6, key=f"{key_prefix}lvl")
            level_num = int(lvl_sel.split()[1])

        with col2:
            subs = SUBLEVELS.get(level_num, [])
            sub_opts = [f"{c}  ·  {t}" for c, t in subs]
            sub_sel = st.selectbox("Sublevel", sub_opts, key=f"{key_prefix}sub")
            sublevel_code = sub_sel.split("  ·  ")[0].strip()
            topic = sub_sel.split("  ·  ", 1)[1].strip() if "  ·  " in sub_sel else ""

        with col3:
            st.markdown(f"""
            <div style="padding-top:28px;font-size:12px;color:#888;line-height:1.6">
                Level {level_num}<br>
                <b style="color:#111">{sublevel_code}</b>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
    return level_num, sublevel_code, topic


def render_footer(level_num: int, sublevel_code: str):
    st.markdown(f"""
    <div class="footer-bar">
        <div class="fl">LA Excellence Schools / IDPS Orchards &nbsp;·&nbsp; Fear Less Maths</div>
        <div class="fr">Level {level_num} · {sublevel_code}</div>
    </div>
    """, unsafe_allow_html=True)
