"""
utils/pdf_reader.py
--------------------
Module 2 from the project spec: Read PDFs.

Takes an uploaded PDF file (from Streamlit's file_uploader) and returns
clean extracted text, ready to feed into the LangChain pipeline.
"""

import re
import io
from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract raw text from a PDF file.

    uploaded_file: a Streamlit UploadedFile object (or any file-like object
                   with .read()).
    Returns: extracted text as a single string.
    """
    # Streamlit's UploadedFile supports .getvalue(); regular file objects
    # support .read(). Handle both so this function works everywhere.
    if hasattr(uploaded_file, "getvalue"):
        file_bytes = uploaded_file.getvalue()
    else:
        file_bytes = uploaded_file.read()

    reader = PdfReader(io.BytesIO(file_bytes))

    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"

    return clean_text(text)


def clean_text(text: str) -> str:
    """
    Module: Text Cleaning.
    Basic cleanup so the LLM gets tidy input:
    - collapse multiple blank lines/spaces
    - strip weird control characters
    """
    if not text:
        return ""

    # Remove non-printable / control characters
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)

    # Collapse 3+ newlines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Collapse repeated spaces
    text = re.sub(r"[ \t]{2,}", " ", text)

    return text.strip()
