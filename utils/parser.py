"""
utils/parser.py
----------------
LLMs sometimes wrap JSON in markdown code fences or add stray text
around it. This helper makes JSON parsing robust so the app doesn't
crash if Gemini's formatting is slightly off.
"""

import json
import re


def safe_json_parse(raw_text: str, fallback: dict) -> dict:
    """
    Try hard to turn the LLM's raw text output into a Python dict.

    1. Strip markdown code fences (```json ... ```)
    2. Try direct json.loads
    3. Try to find the first {...} block with a regex and parse that
    4. If everything fails, return the provided fallback dict
    """
    if not raw_text:
        return fallback

    text = raw_text.strip()

    # Remove ```json ... ``` or ``` ... ``` fences
    text = re.sub(r"^```(?:json)?", "", text.strip())
    text = re.sub(r"```$", "", text.strip())
    text = text.strip()

    # Attempt 1: direct parse
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        pass

    # Attempt 2: extract the first {...} block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    # Attempt 3: give up, return fallback so the app keeps running
    return fallback
