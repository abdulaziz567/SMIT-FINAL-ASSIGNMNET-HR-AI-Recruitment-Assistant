"""
components/sidebar.py
----------------------
Module 1 from the project spec: Build the UI (Sidebar part).

Renders the sidebar where HR uploads the Job Description and one or
more resumes. Pure UI - no AI logic here.
"""

import streamlit as st


def render_sidebar():
    """
    Renders the sidebar and returns the uploaded files.

    Returns:
        jd_file: single uploaded JD PDF (or None)
        resume_files: list of uploaded resume PDFs (can be empty)
    """
    with st.sidebar:
        st.markdown(
            "<h2 style='margin-bottom:0;'>📂 Uploads</h2>"
            "<p style='color:#8b88a8; margin-top:0.2rem; font-size:0.9rem;'>"
            "Step 1: add your files below</p>",
            unsafe_allow_html=True,
        )

        st.markdown("#### 1️⃣ Job Description")
        jd_file = st.file_uploader(
            "Upload Job Description (PDF)",
            type=["pdf"],
            key="jd_uploader",
            label_visibility="collapsed",
        )
        if jd_file:
            st.success(f"✔️ Loaded: {jd_file.name}", icon="✅")

        st.markdown("#### 2️⃣ Resume(s)")
        resume_files = st.file_uploader(
            "Upload Resume(s) - single or multiple",
            type=["pdf"],
            accept_multiple_files=True,
            key="resume_uploader",
            label_visibility="collapsed",
        )
        if resume_files:
            st.success(f"✔️ {len(resume_files)} resume(s) loaded", icon="✅")

        st.divider()
        st.caption(
            "💡 **Tip:** You can upload just one resume, or select multiple "
            "resumes at once to rank several candidates together."
        )

    return jd_file, resume_files
