"""
components/theme.py
--------------------
Central place for all custom styling (CSS injection + small UI helpers).

DESIGN CONCEPT — "Candidate Case File"
---------------------------------------
Instead of a generic SaaS purple-gradient look, the whole app is styled like
an HR case-file / dossier: warm manila paper background with faint ruled
lines, a folder-tab header, typewriter display type, and recommendations
rendered as ink stamps (HIRE / INTERVIEW / REJECT) rather than flat pills.

Palette
  --paper       #F3ECD8   warm manila background
  --paper-deep  #E7DAB3   deeper paper tone (tracks, tab fill)
  --card        #FFFBF2   index-card white
  --ink         #232323   body ink
  --ink-soft    #5B564A   muted ink
  --navy        #1F3A5F   structural / headers
  --navy-deep   #16283F   hover / deep structural
  --rust        #A23E2E   folder tab accent
  --stamp-green #2F6F4E   "Hire" ink
  --stamp-amber #B9781F   "Interview" ink
  --stamp-red   #A23C2F   "Reject" ink
  --line        #D8CBA5   hairline / dashed rule

Type
  Display: 'Special Elite'   (typewriter — used sparingly, for the hero
                               title and stamp badges only)
  Body:    'IBM Plex Sans'   (everything readable)
  Data:    'IBM Plex Mono'   (ranks, scores, labels, eyebrow tags)

Signature element: recommendation "ink stamps" — rotated, double-bordered,
uppercase, monospace-adjacent badges that read like a real HR reviewer
stamped the page, plus a wax-seal style badge for the #1 ranked candidate.
"""

import streamlit as st

NAVY = "#1F3A5F"
NAVY_DEEP = "#16283F"
RUST = "#A23E2E"
STAMP_GREEN = "#2F6F4E"
STAMP_AMBER = "#B9781F"
STAMP_RED = "#A23C2F"

RECOMMENDATION_STYLES = {
    "Hire": {"bg": "#E3EFE7", "fg": STAMP_GREEN, "emoji": "✔"},
    "Interview": {"bg": "#F6ECD8", "fg": STAMP_AMBER, "emoji": "◐"},
    "Reject": {"bg": "#F2E1DC", "fg": STAMP_RED, "emoji": "✕"},
}


def inject_custom_css():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

            :root {
                --paper: #F3ECD8;
                --paper-deep: #E7DAB3;
                --card: #FFFBF2;
                --ink: #232323;
                --ink-soft: #5B564A;
                --navy: #1F3A5F;
                --navy-deep: #16283F;
                --rust: #A23E2E;
                --stamp-green: #2F6F4E;
                --stamp-amber: #B9781F;
                --stamp-red: #A23C2F;
                --line: #D8CBA5;
            }

            html, body, [class*="css"] {
                font-family: 'IBM Plex Sans', sans-serif;
                color: var(--ink);
            }

            /* Ruled-paper background: faint horizontal lines like an index card */
            .stApp {
                background-color: var(--paper);
                background-image: repeating-linear-gradient(
                    to bottom,
                    transparent 0px,
                    transparent 27px,
                    rgba(31, 58, 95, 0.06) 27px,
                    rgba(31, 58, 95, 0.06) 28px
                );
            }

            h1, h2, h3 {
                font-family: 'IBM Plex Sans', sans-serif;
                color: var(--navy);
            }

            /* ---------------- Hero / folder-tab header ---------------- */
            .hero-banner {
                position: relative;
                background: var(--navy);
                color: var(--paper);
                padding: 2.6rem 2.2rem 1.9rem 2.2rem;
                border-radius: 3px 20px 20px 3px;
                margin: 1.6rem 0 1.8rem 0;
                box-shadow: 6px 6px 0 rgba(162, 62, 46, 0.18);
                border-left: 6px solid var(--rust);
            }
            .hero-banner::before {
                content: "CASE FILE \\2022 RECRUITMENT DESK";
                position: absolute;
                top: -15px;
                left: 26px;
                background: var(--rust);
                color: var(--paper);
                font-family: 'IBM Plex Mono', monospace;
                font-size: 0.68rem;
                letter-spacing: 0.14em;
                padding: 5px 14px;
                border-radius: 3px 3px 0 0;
            }
            .hero-banner h1 {
                font-family: 'Special Elite', 'IBM Plex Mono', monospace;
                color: var(--paper) !important;
                margin: 0 0 0.5rem 0;
                font-size: 2rem;
                letter-spacing: 0.3px;
            }
            .hero-banner p {
                margin: 0;
                max-width: 680px;
                opacity: 0.88;
                font-size: 0.98rem;
                line-height: 1.55;
            }

            /* ---------------- Sidebar ---------------- */
            section[data-testid="stSidebar"] {
                background: var(--paper-deep);
                border-right: 2px solid var(--line);
            }
            section[data-testid="stSidebar"] h2 {
                font-family: 'Special Elite', monospace;
                color: var(--navy);
                letter-spacing: 0.5px;
            }
            section[data-testid="stSidebar"] h4 {
                font-family: 'IBM Plex Mono', monospace;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                font-size: 0.85rem;
                color: var(--navy-deep);
                border-bottom: 1px dashed var(--line);
                padding-bottom: 0.3rem;
            }

            /* ---------------- Buttons ---------------- */
            .stButton > button {
                font-family: 'IBM Plex Mono', monospace;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                font-weight: 600;
                border-radius: 4px;
                border: 2px solid var(--navy);
                transition: transform 0.12s ease, box-shadow 0.12s ease;
            }
            .stButton > button[kind="primary"] {
                background: var(--navy);
                color: var(--paper);
                box-shadow: 4px 4px 0 var(--rust);
            }
            .stButton > button[kind="primary"]:hover {
                transform: translate(-2px, -2px);
                box-shadow: 6px 6px 0 var(--rust);
                background: var(--navy-deep);
            }
            .stButton > button:not([kind="primary"]) {
                background: var(--card);
                color: var(--navy);
            }
            div[data-testid="stDownloadButton"] > button {
                font-family: 'IBM Plex Mono', monospace;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                border-radius: 4px;
                border: 2px solid var(--stamp-green);
                background: var(--card);
                color: var(--stamp-green);
                font-weight: 600;
            }
            div[data-testid="stDownloadButton"] > button:hover {
                background: var(--stamp-green);
                color: var(--card);
            }

            /* ---------------- Candidate "index card" ---------------- */
            .candidate-card {
                position: relative;
                background: var(--card);
                border: 1px solid var(--line);
                border-left: 6px solid var(--navy);
                border-radius: 2px 12px 12px 2px;
                padding: 1.4rem 1.7rem;
                margin-bottom: 1.1rem;
                box-shadow: 0 3px 12px rgba(31, 58, 95, 0.09);
            }
            .candidate-card::after {
                content: "";
                position: absolute;
                top: 0;
                right: 0;
                width: 22px;
                height: 22px;
                background: linear-gradient(135deg, transparent 50%, var(--paper-deep) 50%);
                border-bottom-left-radius: 4px;
            }

            /* ---------------- Section labels ---------------- */
            .section-title {
                font-family: 'IBM Plex Mono', monospace;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-size: 0.76rem;
                font-weight: 600;
                color: var(--navy);
                border-bottom: 1px dashed var(--line);
                padding-bottom: 0.35rem;
                margin-bottom: 0.6rem;
            }

            /* ---------------- Recommendation "ink stamp" ---------------- */
            .badge-pill {
                display: inline-block;
                font-family: 'Special Elite', monospace;
                text-transform: uppercase;
                letter-spacing: 0.09em;
                font-size: 0.86rem;
                padding: 0.4rem 1.05rem;
                border: 2px solid currentColor;
                border-radius: 4px;
                box-shadow: inset 0 0 0 2px rgba(255, 255, 255, 0.55);
                transform: rotate(-3deg);
            }

            /* ---------------- Ranking table ---------------- */
            .ranking-table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0 10px;
            }
            .ranking-table th {
                text-align: left;
                font-family: 'IBM Plex Mono', monospace;
                font-size: 0.72rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: var(--navy-deep);
                padding: 0 0.9rem 0.4rem 0.9rem;
                border-bottom: 2px solid var(--line);
            }
            .ranking-table td {
                background: var(--card);
                padding: 0.95rem 0.9rem;
                border-top: 1px solid var(--line);
                border-bottom: 1px solid var(--line);
            }
            .ranking-table tr td:first-child {
                border-left: 4px solid var(--navy);
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
            }
            .ranking-table tr.rank-top td:first-child {
                border-left: 4px solid var(--rust);
            }
            .ranking-table tr td:last-child {
                border-right: 1px solid var(--line);
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }

            /* Rank badge: plain navy circle, gold/rust wax-seal for #1 */
            .rank-badge {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                background: var(--navy);
                color: var(--paper);
                font-family: 'IBM Plex Mono', monospace;
                font-weight: 700;
                font-size: 0.85rem;
            }
            .rank-badge.rank-badge-top {
                background: var(--rust);
                box-shadow: 0 0 0 3px rgba(162, 62, 46, 0.2);
            }

            /* Score bar */
            .score-bar-wrap {
                background: var(--paper-deep);
                border-radius: 6px;
                height: 9px;
                width: 100%;
                overflow: hidden;
                border: 1px solid var(--line);
            }
            .score-bar-fill {
                height: 100%;
                border-radius: 6px;
                background: linear-gradient(90deg, var(--stamp-amber), var(--stamp-green));
            }

            /* Divider */
            hr {
                border-top: 1px dashed var(--line) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_html(html_str: str):
    """
    Renders an HTML string with st.markdown safely.

    Streamlit's markdown parser treats any line indented with 4+ spaces
    as a preformatted code block (standard Markdown behavior), even when
    unsafe_allow_html=True is set. Since our HTML is built from nicely
    indented Python triple-quoted strings, we strip the leading/trailing
    whitespace on every line first so it never gets mistaken for a code
    block and always renders as real HTML.
    """
    cleaned = "\n".join(line.strip() for line in html_str.strip().split("\n"))
    st.markdown(cleaned, unsafe_allow_html=True)


def render_hero_banner(title: str, subtitle: str):
    render_html(
        f"""
        <div class="hero-banner">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """
    )


def recommendation_badge(recommendation: str) -> str:
    style = RECOMMENDATION_STYLES.get(
        recommendation, {"bg": "#eee", "fg": "#555", "emoji": "•"}
    )
    return (
        f'<span class="badge-pill" style="background:{style["bg"]}; '
        f'color:{style["fg"]};">{style["emoji"]} {recommendation}</span>'
    )
