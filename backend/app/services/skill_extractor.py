"""Backward-compatibility wrapper for skill_extractor.

All core skill detection and analysis now lives in app.services.skill_analyzer.
"""

from app.services.skill_analyzer import (
    SKILLS_VOCABULARY as SKILLS_CATALOGUE,
    analyze_skills,
    extract_skills,
    load_skills_vocabulary as _load_skills,
)

__all__ = ["SKILLS_CATALOGUE", "extract_skills", "analyze_skills", "_load_skills"]
