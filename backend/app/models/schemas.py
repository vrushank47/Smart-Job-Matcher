"""Pydantic request/response models for the Smart Job Matcher API."""

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Input payload for the /api/analyze endpoint."""

    resume_text: str = Field(
        ...,
        min_length=10,
        description="Plain-text content of the candidate's resume.",
    )
    job_description: str = Field(
        ...,
        min_length=10,
        description="Plain-text content of the job description to match against.",
    )


class SkillAnalysisResult(BaseModel):
    """Result of skill extraction and gap analysis."""

    matched_skills: list[str] = Field(
        ...,
        description="Skills found in both the resume and the job description.",
    )
    missing_skills: list[str] = Field(
        ...,
        description="Skills required by the job description but absent from the resume.",
    )
    resume_skills: list[str] = Field(
        ...,
        description="All skills detected in the resume.",
    )
    jd_skills: list[str] = Field(
        default_factory=list,
        description="All skills detected in the job description.",
    )
    match_percentage: float = Field(
        ...,
        description="Percentage of required skills found in the resume (0–100).",
    )


class AnalyzeResponse(BaseModel):
    """Output payload returned by the /api/analyze endpoint."""

    match_score: float = Field(
        ...,
        description="Overall match score between resume and job description (0–100).",
    )
    matched_skills: list[str] = Field(
        ...,
        description="Skills found in both the resume and the job description.",
    )
    missing_skills: list[str] = Field(
        ...,
        description="Skills required by the job description but absent from the resume.",
    )
    skill_match_percentage: float = Field(
        ...,
        description="Percentage of job description required skills matched in resume (0–100).",
    )
    resume_skills: list[str] = Field(
        ...,
        description="All skills detected in the resume.",
    )
    similarity_score: float = Field(
        ...,
        description="Raw TF-IDF cosine similarity between resume and job description (0–1).",
    )
    recommendation: str = Field(
        ...,
        description="Short human-readable recommendation based on the match score.",
    )
    breakdown: dict = Field(
        ...,
        description=(
            "Score component breakdown: tfidf_similarity, skill_coverage, "
            "their respective weights, and each component's contribution to match_score."
        ),
    )
