"""Skill analysis service: loads vocabulary from data/skills.json and analyzes skills."""

import json
import pathlib
import re
from typing import Any


# Resolve path to data/skills.json relative to repository root or fallback
_DEFAULT_DATA_PATH = pathlib.Path(__file__).resolve().parents[3] / "data" / "skills.json"


def load_skills_vocabulary(path: pathlib.Path = _DEFAULT_DATA_PATH) -> list[str]:
    """Load the skills vocabulary from data/skills.json."""
    if not path.exists():
        # Fallback to current working directory or relative path search
        fallback = pathlib.Path("data/skills.json")
        if fallback.exists():
            path = fallback.resolve()
        else:
            alt = pathlib.Path(__file__).resolve().parents[2] / "data" / "skills.json"
            if alt.exists():
                path = alt.resolve()

    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# Cache vocabulary at import time
SKILLS_VOCABULARY: list[str] = load_skills_vocabulary()


def extract_skills(text: str, vocabulary: list[str] = SKILLS_VOCABULARY) -> list[str]:
    """Extract skills from *text* that match items in *vocabulary*.

    Uses whole-word boundary matching to avoid false positive substring matches
    (e.g., 'SQL' shouldn't match inside 'NoSQL' or 'PostgreSQL').
    """
    if not text:
        return []

    found: list[str] = []
    text_lower = text.lower()

    for skill in vocabulary:
        # Regex boundary pattern accommodating special characters like C++, .NET, etc.
        escaped_skill = re.escape(skill.lower())
        pattern = re.compile(
            r"(?<![a-z0-9])" + escaped_skill + r"(?![a-z0-9])"
        )
        if pattern.search(text_lower):
            found.append(skill)

    return found


def analyze_skills(
    resume_text: str,
    job_description: str,
    vocabulary: list[str] = SKILLS_VOCABULARY,
) -> dict[str, Any]:
    """Analyze skills in resume against job description requirements.

    Detects:
    - matched skills: skills present in both job description and resume
    - missing skills: skills required by the job description but absent from resume
    - resume skills: all skills detected in resume
    - jd skills: all skills detected in job description
    - match percentage: percentage of required skills matched (0.0 to 100.0)

    Returns
    -------
    dict with:
        matched_skills: list[str]
        missing_skills: list[str]
        resume_skills: list[str]
        jd_skills: list[str]
        match_percentage: float (0.0 to 100.0)
    """
    resume_skills = extract_skills(resume_text, vocabulary)
    jd_skills = extract_skills(job_description, vocabulary)

    resume_skill_set = {s.lower() for s in resume_skills}

    # Preserve original vocabulary casing
    matched_skills = [s for s in jd_skills if s.lower() in resume_skill_set]
    missing_skills = [s for s in jd_skills if s.lower() not in resume_skill_set]

    # Calculate match percentage based on required skills in JD
    if jd_skills:
        match_percentage = round((len(matched_skills) / len(jd_skills)) * 100.0, 2)
    else:
        # If no specific skills are found in JD, neutral 100% or 0% depending on interpretation
        # 100.0 represents no unmet skill requirements
        match_percentage = 100.0 if resume_skills else 0.0

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "match_percentage": match_percentage,
    }
