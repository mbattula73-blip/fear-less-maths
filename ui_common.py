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

DESIGN SYSTEM (v2 — "chalkboard & paper")
------------------------------------------
This app is a daily-use tool for a math teacher and school staff, not a
marketing page — so the brief is legibility and speed, not spectacle. The
look is grounded in the worksheet's own world: ink-black headers like a
blackboard, warm paper-cream pages like the worksheets themselves, and ONE
accent color — a muted chalkboard green — used only for active/interactive
states (the thing you're doing right now), never for decoration. Elevation
is done with soft shadows rather than hard borders, which is most of what
separates a dated flat-bordered UI from a current one.

Every CSS class name below (.info-cell, .ws-hero, .tier-step, .app-header,
etc.) is referenced directly in app.py and pages/1_Daily_Entry.py's raw
HTML — renaming any of them would silently break those pages. Only the
property VALUES changed in this revision, not the class names.
"""
import streamlit as st
from levels_data import LEVELS, SUBLEVELS

MAIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --ink: #161616;
    --ink-2: #232323;
    --paper: #F6F3EC;
    --card: #FFFFFF;
    --hairline: #E4E0D2;
    --muted: #8C8676;
    --slate: #2E6B5E;       /* the one accent — chalkboard green */
    --slate-soft: #E8F0EC;
    --danger: #C0392B;
    --shadow-sm: 0 1px 2px rgba(22,22,22,.05), 0 1px 1px rgba(22,22,22,.04);
    --shadow-md: 0 6px 16px -8px rgba(22,22,22,.16), 0 2px 4px rgba(22,22,22,.05);
}

*, html, body { font-family: 'IBM Plex Sans', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
body { background: var(--paper) !important; }

/* Visible keyboard focus everywhere — accessibility floor, not optional */
a:focus-visible, button:focus-visible, [tabindex]:focus-visible {
    outline: 2px solid var(--slate) !important;
    outline-offset: 2px !important;
}

/* ═══ HEADER BAR ══════════════════════════════════════════ */
.app-header {
    background: linear-gradient(180deg, var(--ink) 0%, var(--ink-2) 100%);
    padding: 18px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    border-bottom: 2px solid var(--slate);
}
.app-brand {
    font-family: 'Playfair Display', serif !important;
    font-size: 23px; font-weight: 700;
    color: #FFFFFF !important;
    letter-spacing: -.02em;
}
.app-sub {
    font-size: 10px; color: #6B6B6B !important;
    text-transform: uppercase; letter-spacing: .12em;
    margin-top: 2px;
}

/* ═══ SELECTOR STRIP ══════════════════════════════════════ */
.selector-strip {
    background: var(--card);
    border-bottom: 1px solid var(--hairline);
    padding: 16px 24px;
}

/* ═══ MAIN CONTENT ════════════════════════════════════════ */
.main-area {
    background: var(--paper);
    min-height: 100vh;
    padding: 0 0 40px;
}

/* Worksheet ID card — the signature element: a thin chalk-green edge and a
   tinted glow, anchoring the one accent color to "the thing you're building" */
.ws-hero {
    margin: 20px 24px 0;
    background: var(--ink);
    border-radius: 14px;
    border-top: 3px solid var(--slate);
    padding: 20px 24px;
    display: flex; align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    box-shadow: 0 10px 28px -14px rgba(46,107,94,.45), var(--shadow-md);
}
.ws-hero-id {
    font-family: 'Playfair Display',serif;
    font-size: 36px; color: #FFF;
    letter-spacing: -.03em; line-height: 1;
}
.ws-hero-meta { text-align: right; }
.ws-hero-topic { font-size: 13px; color: #9A9A9A; margin-bottom: 4px; }
.ws-hero-tier { font-size: 11px; color: var(--slate);
                font-weight: 600;
                text-transform: uppercase; letter-spacing: .08em; }

/* Tier track */
.tier-track {
    display: flex; margin: 14px 24px 0;
    background: var(--card);
    border: 1px solid var(--hairline);
    border-radius: 10px; overflow: hidden;
    box-shadow: var(--shadow-sm);
}
.tier-step {
    flex: 1; padding: 10px 6px; text-align: center;
    border-right: 1px solid var(--hairline);
    font-size: 10px; color: #B5AFA0;
    background: #FBFAF6;
    transition: background .15s, color .15s;
}
.tier-step:last-child { border-right: none; }
.tier-step.on { background: var(--slate); color: #FFF; }
.tier-step .tn {
    font-size: 9px; display: block; margin-bottom: 2px;
    opacity: .65; text-transform: uppercase; letter-spacing: .06em;
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
    background: var(--card); border: 1px solid var(--hairline);
    border-radius: 10px; padding: 13px 15px;
    box-shadow: var(--shadow-sm);
    transition: box-shadow .15s;
}
.info-cell .il { font-size: 10px; color: var(--muted);
                 text-transform: uppercase; letter-spacing: .07em; margin-bottom: 4px; }
.info-cell .iv { font-size: 13px; font-weight: 600; color: var(--ink); }

/* Buttons */
.stButton > button {
    font-family: 'IBM Plex Sans',sans-serif !important;
    background: var(--ink) !important; color: #FFFFFF !important;
    border: none !important; border-radius: 10px !important;
    font-size: 15px !important; font-weight: 600 !important;
    padding: 14px 40px !important; width: 100% !important;
    letter-spacing: .01em !important;
    box-shadow: var(--shadow-sm) !important;
    transition: transform .12s, background .12s, box-shadow .12s !important;
}
.stButton > button:hover {
    background: var(--ink-2) !important; transform: translateY(-1px) !important;
    box-shadow: var(--shadow-md) !important;
}

.stDownloadButton > button {
    font-family: 'IBM Plex Sans',sans-serif !important;
    background: var(--card) !important; color: var(--ink) !important;
    border: 1.5px solid var(--ink) !important;
    border-radius: 10px !important;
    font-size: 15px !important; font-weight: 600 !important;
    padding: 14px 0 !important; width: 100% !important;
    transition: all .12s !important;
}
.stDownloadButton > button:hover {
    background: var(--ink) !important; color: #FFF !important;
}

/* Success */
.success-card {
    background: var(--slate-soft); border: 1px solid var(--slate);
    border-radius: 10px; padding: 14px 18px;
    display: flex; align-items: center; gap: 12px;
    font-weight: 600; font-size: 14px; color: var(--ink);
    margin: 12px 0;
}
.success-card .ck {
    width: 28px; height: 28px; border-radius: 50%;
    background: var(--slate); color: #FFF;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; flex-shrink: 0;
}

/* Selectbox labels */
.stSelectbox label, .stNumberInput label, .stTextInput label, .stDateInput label {
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: .06em !important;
    color: var(--muted) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--hairline) !important;
    gap: 0; padding: 0 24px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #AFA89A !important; font-size: 13px !important;
    font-weight: 500 !important;
    padding: 12px 16px !important;
    border: none !important; border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -1px !important;
    transition: color .12s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--ink) !important; }
.stTabs [aria-selected="true"] {
    color: var(--ink) !important; font-weight: 700 !important;
    border-bottom: 2px solid var(--slate) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }

/* Progress */
.stProgress > div > div { background: var(--slate) !important; }

/* Expanders — used by Manage Students / Demo Data panels */
.streamlit-expanderHeader, [data-testid="stExpander"] summary {
    border-radius: 10px !important;
    font-weight: 600 !important;
}

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
    background: var(--card); border: 1px solid var(--hairline);
    border-radius: 8px; font-size: 11px; color: var(--muted);
}
.tg-pip { width:7px;height:7px;border-radius:50%;flex-shrink:0; }

/* Footer */
.footer-bar {
    background: linear-gradient(0deg, var(--ink) 0%, var(--ink-2) 100%);
    padding: 12px 24px;
    display: flex; align-items: center;
    justify-content: space-between; margin-top: 40px;
    flex-wrap: wrap; gap: 8px;
}
.footer-bar .fl { font-size: 11px; color: #707070; }
.footer-bar .fr { font-size: 11px; color: #4D4D4D; }
</style>
"""

# Hides Streamlit's auto-generated multipage nav links in the sidebar.
# Used on the Daily Entry page so staff have no visible way to wander into
# the teacher's tabs. The main app (app.py) keeps nav visible so you (the
# teacher) can find/open the Daily Entry page and copy its URL to share.
# This is a UX separation, not an access-control boundary — both pages are
# still reachable by anyone who has/guesses the URL. Layer on a PIN gate if
# you need real auth later.
HIDE_NAV_CSS = '<style>[data-testid="stSidebarNav"] {display: none;}</style>'

# Streamlit serves files in /static/ at the URL path /app/static/... when
# server.enableStaticServing=true (see .streamlit/config.toml). manifest.json
# and the two icon PNGs live there — this is what a TWA/PWA-install check
# (and Bubblewrap, when building the Android wrapper) reads to know the
# app's name, icons, and colors.
#
# st.markdown()'s HTML doesn't execute <script> tags, so a plain <link> tag
# there never reaches the real <head> — only components.html() (which runs
# inside an iframe) executes scripts, and reaching the REAL page's head from
# inside that iframe needs window.parent.document rather than document.
# This is a known, slightly hacky pattern; wrapped in try/catch so a future
# Streamlit change that blocks parent-document access fails silently instead
# of breaking the page.
_PWA_MANIFEST_INJECT = """
<script>
try {
    var d = window.parent.document;
    if (!d.querySelector('link[rel="manifest"]')) {
        var link = d.createElement('link');
        link.rel = 'manifest';
        link.href = '/app/static/manifest.json';
        d.head.appendChild(link);
    }
    if (!d.querySelector('meta[name="theme-color"]')) {
        var meta = d.createElement('meta');
        meta.name = 'theme-color';
        meta.content = '#161616';
        d.head.appendChild(meta);
    }
} catch (e) { /* parent-document access blocked — fail silently */ }
</script>
"""


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
    st.iframe(_PWA_MANIFEST_INJECT, height=1)


def render_header(subtitle: str = "Worksheet Generator · LA Excellence Schools",
                   badge: str = "A4 · B&W · 20 Questions · Print Ready"):
    st.markdown(f"""
    <div class="app-header">
        <div>
            <div class="app-brand">Fear Less Maths</div>
            <div class="app-sub">{subtitle}</div>
        </div>
        <div style="font-size:11px;color:#6B6B6B">{badge}</div>
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
        st.markdown('<div style="background:var(--card);padding:16px 24px 4px;'
                     'border-bottom:1px solid var(--hairline)">', unsafe_allow_html=True)
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
            <div style="padding-top:28px;font-size:12px;color:var(--muted);line-height:1.6">
                Level {level_num}<br>
                <b style="color:var(--ink)">{sublevel_code}</b>
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
