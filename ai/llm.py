"""
ai/llm.py
---------
Sets up the connection to Google Gemini using LangChain.

This file has ONE job: give the rest of the app a ready-to-use
LangChain chat model object called `llm`.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load variables from .env file (works when running locally)
load_dotenv()


def get_api_key() -> str:
    """
    Fetch the Gemini API key.

    Priority:
    1. Environment variable / .env file -> used when running locally
    2. Streamlit secrets (st.secrets) -> used when deployed on Streamlit Cloud

    Note: we check .env FIRST and only look at st.secrets if that fails.
    This avoids Streamlit printing its "No secrets found" info message
    to the console on every run when there's no secrets.toml file, which
    is the normal case for local development.
    """
    # 1. Try .env / environment variable first (normal case for local runs)
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key and api_key != "your_gemini_api_key_here":
        return api_key

    # 2. Fall back to Streamlit secrets (used on Streamlit Cloud deployments).
    # Only attempt this if a secrets file actually exists, so we don't
    # trigger Streamlit's harmless-but-noisy "No secrets found" message.
    secrets_paths = [
        os.path.join(os.path.expanduser("~"), ".streamlit", "secrets.toml"),
        os.path.join(os.getcwd(), ".streamlit", "secrets.toml"),
    ]
    if any(os.path.exists(p) for p in secrets_paths):
        try:
            api_key = st.secrets.get("GOOGLE_API_KEY", None)
        except Exception:
            api_key = None

    return api_key


def get_llm(temperature: float = 0.3):
    """
    Returns a configured Gemini chat model instance.

    temperature: lower = more consistent / factual answers.
                 We keep it low because this is an HR analysis tool,
                 not a creative writing tool.
    """
    api_key = get_api_key()

    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError(
            "GOOGLE_API_KEY is missing. Please add your Gemini API key to the "
            ".env file (see .env.example) or to Streamlit secrets."
        )

    # Model name can be overridden in .env as GEMINI_MODEL=gemini-3.1-flash etc.
    # "gemini-flash-latest" is Google's auto-updating alias that always points
    # to their current recommended Flash model, so it keeps working even as
    # Google retires/renames specific model versions over time.
    model_name = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=temperature,
        convert_system_message_to_human=True,
    )
    return llm
