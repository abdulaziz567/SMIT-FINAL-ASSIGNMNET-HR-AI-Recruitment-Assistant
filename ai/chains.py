"""
ai/chains.py
------------
Module 3-9 from the project spec: LangChain Pipeline.

Each "Chain N" from the spec is a small function built with LangChain's
LCEL syntax:  prompt | llm | output_parser

analyze_resume() runs all 5 chains in sequence for ONE resume and returns
a single structured dict matching the JSON schema from Module 9:

{
  "summary": "...",
  "matching_skills": [...],
  "missing_skills": [...],
  "extra_skills": [...],
  "score": 88,
  "interview_questions": {"technical": [...], "hr": [...]},
  "recommendation": "...",
  "justification": "..."
}
"""

from langchain_core.output_parsers import StrOutputParser

from ai.llm import get_llm
from utils.prompts import (
    SUMMARY_PROMPT,
    SKILL_MATCH_PROMPT,
    SCORE_PROMPT,
    RECOMMENDATION_PROMPT,
    INTERVIEW_QUESTIONS_PROMPT,
)
from utils.parser import safe_json_parse


def analyze_resume(resume_text: str, jd_text: str, candidate_name: str = "Candidate") -> dict:
    """
    Runs the full 5-chain LangChain pipeline on a single resume.

    resume_text: cleaned text extracted from the candidate's resume PDF
    jd_text: cleaned text extracted from the job description PDF
    candidate_name: display name for this candidate (defaults to filename)

    Returns a dict following the Module 9 JSON schema, with an extra
    "candidate" field added for convenience in the ranking table.
    """
    llm = get_llm()
    str_parser = StrOutputParser()

    # -----------------------------------------------------------
    # Chain 1: Resume Summary
    # -----------------------------------------------------------
    summary_chain = SUMMARY_PROMPT | llm | str_parser
    summary = summary_chain.invoke({"resume_text": resume_text}).strip()

    # -----------------------------------------------------------
    # Chain 2: Skill Matching (Matching / Missing / Extra)
    # -----------------------------------------------------------
    skill_chain = SKILL_MATCH_PROMPT | llm | str_parser
    skill_raw = skill_chain.invoke({"resume_text": resume_text, "jd_text": jd_text})
    skills = safe_json_parse(
        skill_raw,
        fallback={"matching_skills": [], "missing_skills": [], "extra_skills": []},
    )
    matching_skills = skills.get("matching_skills", [])
    missing_skills = skills.get("missing_skills", [])
    extra_skills = skills.get("extra_skills", [])

    # -----------------------------------------------------------
    # Chain 3: Match Score (0-100%)
    # -----------------------------------------------------------
    score_chain = SCORE_PROMPT | llm | str_parser
    score_raw = score_chain.invoke(
        {
            "resume_text": resume_text,
            "jd_text": jd_text,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
        }
    )
    score_data = safe_json_parse(score_raw, fallback={"score": 0})
    try:
        score = int(score_data.get("score", 0))
    except (ValueError, TypeError):
        score = 0
    score = max(0, min(100, score))  # clamp to 0-100

    # -----------------------------------------------------------
    # Chain 4: HR Recommendation
    # -----------------------------------------------------------
    recommendation_chain = RECOMMENDATION_PROMPT | llm | str_parser
    rec_raw = recommendation_chain.invoke(
        {
            "jd_text": jd_text,
            "resume_summary": summary,
            "score": score,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
        }
    )
    rec_data = safe_json_parse(
        rec_raw, fallback={"recommendation": "Interview", "justification": "N/A"}
    )
    recommendation = rec_data.get("recommendation", "Interview")
    justification = rec_data.get("justification", "")

    # -----------------------------------------------------------
    # Chain 5: Interview Questions (only meaningful for Hire/Interview,
    # but we generate them for every candidate so HR has the option)
    # -----------------------------------------------------------
    interview_chain = INTERVIEW_QUESTIONS_PROMPT | llm | str_parser
    questions_raw = interview_chain.invoke(
        {"jd_text": jd_text, "resume_summary": summary}
    )
    questions_data = safe_json_parse(
        questions_raw, fallback={"technical_questions": [], "hr_questions": []}
    )

    # -----------------------------------------------------------
    # Module 9: Structured Output (JSON)
    # -----------------------------------------------------------
    result = {
        "candidate": candidate_name,
        "summary": summary,
        "score": score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
        "interview_questions": {
            "technical": questions_data.get("technical_questions", []),
            "hr": questions_data.get("hr_questions", []),
        },
        "recommendation": recommendation,
        "justification": justification,
    }
    return result
