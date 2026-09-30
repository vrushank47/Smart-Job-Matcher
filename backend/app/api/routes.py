"""API router: exposes /api/analyze, /api/skills/analyze, and /api/skills endpoints."""

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    SkillAnalysisResult,
)
from app.services import matcher
from app.services.skill_analyzer import SKILLS_VOCABULARY, analyze_skills

router = APIRouter(prefix="/api", tags=["matching"])


@router.post("/analyze", response_model=AnalyzeResponse, summary="Analyze resume vs. job description")
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    """Accept a resume and a job description, then return a match analysis.

    - **match_score**: blended 0–100 score (TF-IDF similarity + skill coverage)
    - **matched_skills**: skills present in both documents
    - **missing_skills**: skills required by the JD but absent from the resume
    - **skill_match_percentage**: percentage of required skills matched (0–100)
    - **resume_skills**: all skills detected in the resume
    - **similarity_score**: raw TF-IDF cosine similarity (0–1)
    - **recommendation**: human-readable advice based on the score
    - **breakdown**: explainable score components and weights
    """
    try:
        result = matcher.analyze(
            resume_text=payload.resume_text,
            job_description=payload.job_description,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}") from exc

    return AnalyzeResponse(**result)


@router.post("/skills/analyze", response_model=SkillAnalysisResult, summary="Standalone skill analysis")
def analyze_skills_endpoint(payload: AnalyzeRequest) -> SkillAnalysisResult:
    """Detect matched and missing skills and return the skill match percentage."""
    try:
        result = analyze_skills(
            resume_text=payload.resume_text,
            job_description=payload.job_description,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Skill analysis failed: {exc}") from exc

    return SkillAnalysisResult(**result)


@router.get("/skills", summary="List available skills in the vocabulary")
def list_skills() -> dict:
    """Return the full skills vocabulary used for extraction."""
    return {"skills": SKILLS_VOCABULARY, "count": len(SKILLS_VOCABULARY)}
