"""
components/uploader.py
-----------------------
Module 2 from the project spec: Read PDFs (UI-facing wrapper).

Turns uploaded PDF files into clean text, and shows the extracted
text in an expander so HR can double check the app read the PDF
correctly.
"""

import streamlit as st
from utils.pdf_reader import extract_text_from_pdf


def process_jd(jd_file):
    """
    Extract and display text from the uploaded Job Description PDF.
    Returns the extracted text (or empty string if nothing uploaded).
    """
    if jd_file is None:
        return ""

    jd_text = extract_text_from_pdf(jd_file)

    with st.expander("📄 Job Description Text (extracted)"):
        st.text_area(
            "Extracted JD text",
            value=jd_text,
            height=200,
            key="jd_text_display",
            label_visibility="collapsed",
        )

    return jd_text


def process_resumes(resume_files):
    """
    Extract text from every uploaded resume PDF.

    Returns a list of dicts: [{"name": filename, "text": resume_text}, ...]
    """
    resumes = []
    if not resume_files:
        return resumes

    for file in resume_files:
        text = extract_text_from_pdf(file)
        resumes.append({"name": file.name.rsplit(".", 1)[0], "text": text})

    with st.expander(f"📄 Resume Text (extracted) - {len(resumes)} file(s)"):
        for r in resumes:
            st.markdown(f"**{r['name']}**")
            st.text_area(
                f"Extracted text for {r['name']}",
                value=r["text"],
                height=150,
                key=f"resume_text_{r['name']}",
                label_visibility="collapsed",
            )

    return resumes
