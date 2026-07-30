"""
app.py
------
Main entry point for the AI Recruitment Assistant Dashboard.

Run with:  streamlit run app.py

This file wires together every module from the project spec:
  Module 1  -> components/sidebar.py   (UI)
  Module 2  -> components/uploader.py  (PDF reading)
  Module 3-9-> ai/chains.py            (LangChain pipeline)
  Module 10 -> components/ranking.py   (Ranking table)
  Module 11 -> components/ranking.py   (CSV export)
"""

import streamlit as st

from components.sidebar import render_sidebar
from components.uploader import process_jd, process_resumes
from components.ranking import render_ranking_table
from components.theme import (
    inject_custom_css,
    render_hero_banner,
    recommendation_badge,
    render_html,
)
from ai.chains import analyze_resume


# -----------------------------------------------------------------
# Page config
# -----------------------------------------------------------------
st.set_page_config(
    page_title="AI Recruitment Assistant",
    page_icon="🧑‍💼",
    layout="wide",
)

inject_custom_css()

render_hero_banner(
    "🧑‍💼 AI Recruitment Assistant Dashboard",
    "Upload a job description and one or more resumes. The AI (Gemini via "
    "LangChain) will summarize each resume, score it against the job "
    "description, and give you a ranked hiring recommendation.",
)

# Session state holds analysis results so they survive Streamlit reruns
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = []


# -----------------------------------------------------------------
# Module 1: Sidebar - Uploads
# -----------------------------------------------------------------
jd_file, resume_files = render_sidebar()


# -----------------------------------------------------------------
# Module 2: Read PDFs (only runs after files are uploaded)
# -----------------------------------------------------------------
jd_text = process_jd(jd_file) if jd_file else ""
resumes = process_resumes(resume_files) if resume_files else []


# -----------------------------------------------------------------
# Main page: Analyze button
# -----------------------------------------------------------------
st.write("")

col1, col2 = st.columns([1, 3])
with col1:
    analyze_clicked = st.button(
        "🔍 Analyze Resume(s)",
        type="primary",
        use_container_width=True,
        disabled=not (jd_file and resumes),
    )
with col2:
    if jd_file and resumes:
        render_html(
            f"<div style='padding-top:0.6rem; font-family: \"IBM Plex Mono\", monospace; "
            f"font-size:0.85rem; color:#5B564A;'>"
            f"Ready to analyze <b style='color:#1F3A5F;'>{len(resumes)}</b> resume(s) "
            f"against the uploaded job description.</div>"
        )

if not jd_file:
    st.info("👈 Upload a Job Description PDF in the sidebar to get started.")
elif not resumes:
    st.info("👈 Upload at least one Resume PDF in the sidebar to get started.")

# -----------------------------------------------------------------
# Module 3-9: Run the LangChain pipeline for every resume
# -----------------------------------------------------------------
if analyze_clicked:
    st.session_state.analysis_results = []  # reset previous run
    progress = st.progress(0, text="Starting analysis...")

    for i, resume in enumerate(resumes):
        progress.progress(
            int((i / len(resumes)) * 100),
            text=f"Analyzing {resume['name']} ({i + 1}/{len(resumes)})...",
        )
        try:
            result = analyze_resume(
                resume_text=resume["text"],
                jd_text=jd_text,
                candidate_name=resume["name"],
            )
            st.session_state.analysis_results.append(result)
        except Exception as e:
            st.error(f"❌ Failed to analyze {resume['name']}: {e}")

    progress.progress(100, text="Done!")
    progress.empty()


# -----------------------------------------------------------------
# Display individual results per candidate
# -----------------------------------------------------------------
results = st.session_state.analysis_results

if results:
    render_html(
        "<p class='section-title' style='font-size:1.1rem;'>📋 Individual Candidate Analysis</p>"
    )

    tabs = st.tabs([f"👤 {r['candidate']}" for r in results])
    for tab, r in zip(tabs, results):
        with tab:
            render_html("<div class='candidate-card'>")

            score_col, rec_col = st.columns(2)
            with score_col:
                render_html(
                    f"""
                    <div class='section-title'>Match Score</div>
                    <div style='font-family: "Special Elite", monospace; font-size:2rem; color:#1F3A5F;'>{r['score']}%</div>
                    <div class='score-bar-wrap'><div class='score-bar-fill' style='width:{r['score']}%;'></div></div>
                    """
                )
            with rec_col:
                render_html(
                    f"""
                    <div class='section-title'>Recommendation</div>
                    <div style='margin-top:0.4rem;'>{recommendation_badge(r['recommendation'])}</div>
                    """
                )

            render_html("<br>")
            render_html("<div class='section-title'>Resume Summary</div>")
            st.markdown(r["summary"])

            render_html("<br>")
            skill_col1, skill_col2, skill_col3 = st.columns(3)
            with skill_col1:
                render_html("<div class='section-title'>✅ Matching Skills</div>")
                st.write(", ".join(r["matching_skills"]) or "None found")
            with skill_col2:
                render_html("<div class='section-title'>❌ Missing Skills</div>")
                st.write(", ".join(r["missing_skills"]) or "None")
            with skill_col3:
                render_html("<div class='section-title'>➕ Extra Skills</div>")
                st.write(", ".join(r["extra_skills"]) or "None")

            render_html("<br>")
            render_html("<div class='section-title'>HR Justification</div>")
            st.write(r["justification"])

            render_html("</div>")

            with st.expander("🎤 Interview Questions"):
                st.markdown("**Technical Questions**")
                for q in r["interview_questions"]["technical"]:
                    st.markdown(f"- {q}")
                st.markdown("**HR / Behavioral Questions**")
                for q in r["interview_questions"]["hr"]:
                    st.markdown(f"- {q}")

    # -----------------------------------------------------------
    # Module 10 & 11: Ranking table + CSV export
    # -----------------------------------------------------------
    st.divider()
    render_ranking_table(results)
