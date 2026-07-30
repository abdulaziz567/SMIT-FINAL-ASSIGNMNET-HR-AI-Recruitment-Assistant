"""
utils/prompts.py
-----------------
All the prompt templates used by the LangChain pipeline live here.
Keeping them in one file makes it easy to tweak wording without
touching the chain logic in ai/chains.py.
"""

from langchain_core.prompts import ChatPromptTemplate


# ---------------------------------------------------------------
# Chain 1: Resume Summary
# ---------------------------------------------------------------
SUMMARY_PROMPT = ChatPromptTemplate.from_template(
    """You are an expert HR analyst. Read the resume text below and extract
a short, clean candidate summary.

Resume:
{resume_text}

Return ONLY the summary as short bullet points covering:
- Education
- Total years of experience
- Key technical skills
- Notable projects / achievements

Do not add any extra commentary. Keep it concise (max 8 bullet points).
"""
)


# ---------------------------------------------------------------
# Chain 2: Skill Matching (Matching / Missing / Extra)
# ---------------------------------------------------------------
SKILL_MATCH_PROMPT = ChatPromptTemplate.from_template(
    """You are comparing a candidate's resume against a job description.

Job Description:
{jd_text}

Resume:
{resume_text}

Identify the skills required by the job description and classify the
candidate's skills into exactly three categories:

1. Matching Skills - skills required by the JD AND present in the resume
2. Missing Skills - skills required by the JD but NOT present in the resume
3. Extra Skills - skills the candidate has that are not required by the JD but are relevant

Return the result strictly as compact JSON with this exact shape and nothing else:
{{
  "matching_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "extra_skills": ["skill1", "skill2"]
}}
"""
)


# ---------------------------------------------------------------
# Chain 3: Match Score (0-100%)
# ---------------------------------------------------------------
SCORE_PROMPT = ChatPromptTemplate.from_template(
    """You are scoring how well a candidate fits a job.

Job Description:
{jd_text}

Resume:
{resume_text}

Matching Skills: {matching_skills}
Missing Skills: {missing_skills}

Based on skills overlap, relevant experience, and education fit, give a single
overall match score as a whole number percentage between 0 and 100.

Return strictly as compact JSON with this exact shape and nothing else:
{{
  "score": 88
}}
"""
)


# ---------------------------------------------------------------
# Chain 4: HR Recommendation
# ---------------------------------------------------------------
RECOMMENDATION_PROMPT = ChatPromptTemplate.from_template(
    """You are a senior HR manager making a hiring call.

Job Description:
{jd_text}

Resume Summary:
{resume_summary}

Match Score: {score}%
Matching Skills: {matching_skills}
Missing Skills: {missing_skills}

Decide on ONE of these recommendations: "Hire", "Interview", or "Reject".
Use "Hire" for a strong match (score >= 85 and few missing critical skills),
"Interview" for a moderate match worth a conversation (score 60-84),
and "Reject" for a weak match (score < 60).

Then give a short justification (1-3 sentences).

Return strictly as compact JSON with this exact shape and nothing else:
{{
  "recommendation": "Hire",
  "justification": "Excellent ML knowledge, strong Python skills, relevant projects."
}}
"""
)


# ---------------------------------------------------------------
# Chain 5: Interview Questions
# ---------------------------------------------------------------
INTERVIEW_QUESTIONS_PROMPT = ChatPromptTemplate.from_template(
    """You are preparing an interview panel for this candidate.

Job Description:
{jd_text}

Resume Summary:
{resume_summary}

Generate interview questions tailored to this specific resume and job description:
- 4 technical questions that probe the candidate's listed skills and projects
- 3 HR / behavioral questions

Return strictly as compact JSON with this exact shape and nothing else:
{{
  "technical_questions": ["question1", "question2", "question3", "question4"],
  "hr_questions": ["question1", "question2", "question3"]
}}
"""
)
