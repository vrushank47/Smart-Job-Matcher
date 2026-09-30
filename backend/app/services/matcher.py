"""Core AI matching service — TF-IDF cosine similarity + skill gap analysis.

Pipeline (called by /api/analyze)
----------------------------------
1. PREPROCESS
   Both texts go through nlp_utils.preprocess():
     raw text → lowercase → strip noise → tokenize → POS-tag
              → lemmatize → remove stop-words → clean string

2. VECTORIZE (TF-IDF)
   Build a shared TF-IDF vocabulary from [resume, job_description].
   Each document becomes a sparse vector where each dimension is a
   term and the value is its TF-IDF weight:
       TF-IDF(t, d) = TF(t, d) × IDF(t)

3. COSINE SIMILARITY
   Measures the angle between the two TF-IDF vectors (0.0 to 1.0):
       cosine_sim = (A · B) / (||A|| × ||B||)

4. SKILL GAP ANALYSIS (services/skill_analyzer.py)
   Exact skill detection using data/skills.json vocabulary.
   Computes matched_skills, missing_skills, and skill match_percentage.

5. BLENDED MATCH SCORE (0 – 100)
   Combines TF-IDF similarity with skill coverage:
       match_score = (0.5 × cosine_sim + 0.5 × (skill_match_percentage / 100)) × 100

6. SCORE BREAKDOWN
   Returned alongside the score explaining each component.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine

from app.services.nlp_utils import preprocess
from app.services.skill_analyzer import analyze_skills

# ---------------------------------------------------------------------------
# Step 2 + 3 — TF-IDF vectorisation and cosine similarity
# ---------------------------------------------------------------------------

def _compute_tfidf_similarity(resume_clean: str, jd_clean: str) -> float:
    """Fit a TF-IDF vectorizer on both documents and return cosine similarity.

    Both strings are pre-processed (lemmatized, stop-words removed) before
    they arrive here, so the vectorizer only needs to do tokenisation
    (split on whitespace) and the IDF weighting.

    Returns a float in [0.0, 1.0].
    """
    vectorizer = TfidfVectorizer(
        analyzer="word",
        token_pattern=r"\S+",
        sublinear_tf=True,
        max_df=1.0,
        min_df=1,
    )

    tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])
    similarity: float = sklearn_cosine(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return round(float(similarity), 4)


# ---------------------------------------------------------------------------
# Step 5 — Score + recommendation
# ---------------------------------------------------------------------------

def _blend_score(similarity: float, skill_coverage_ratio: float) -> float:
    """Combine TF-IDF similarity (0-1) and skill coverage ratio (0-1) into 0–100 score."""
    return round((0.5 * similarity + 0.5 * skill_coverage_ratio) * 100, 2)


def _recommend(score: float) -> str:
    if score >= 80:
        return (
            "Excellent match! Your resume aligns strongly with the job requirements. "
            "Focus on tailoring your cover letter to stand out."
        )
    if score >= 60:
        return (
            "Good match. You meet most requirements — consider emphasising your "
            "experience with the missing skills or showing transferable expertise."
        )
    if score >= 40:
        return (
            "Moderate match. Bridging the skill gaps (see missing_skills) would "
            "significantly improve your candidacy."
        )
    return (
        "Low match. The resume may need substantial tailoring — or additional "
        "qualifications — to be competitive for this role."
    )


# ---------------------------------------------------------------------------
# Public entry point (called by /api/analyze)
# ---------------------------------------------------------------------------

def analyze(resume_text: str, job_description: str) -> dict:
    """Run the full matching pipeline and return a structured result dict.

    Parameters
    ----------
    resume_text:     raw plain-text resume (any length)
    job_description: raw plain-text job description (any length)

    Returns
    -------
    dict with keys:
        match_score            – blended 0-100 score
        matched_skills         – skills in both documents
        missing_skills         – skills required by JD but absent from resume
        skill_match_percentage – percentage of required skills matched (0–100)
        resume_skills          – all skills detected in resume
        similarity_score       – raw TF-IDF cosine similarity (0–1)
        recommendation         – human-readable advice
        breakdown              – dict explaining each score component
    """
    # ------------------------------------------------------------------
    # Step 1 — Preprocess
    # ------------------------------------------------------------------
    resume_clean = preprocess(resume_text)
    jd_clean = preprocess(job_description)

    # ------------------------------------------------------------------
    # Step 2 + 3 — TF-IDF vectorisation → cosine similarity
    # ------------------------------------------------------------------
    similarity = _compute_tfidf_similarity(resume_clean, jd_clean)

    # ------------------------------------------------------------------
    # Step 4 — Skill analysis via services/skill_analyzer.py
    # ------------------------------------------------------------------
    skill_data = analyze_skills(resume_text, job_description)
    skill_coverage_ratio = round(skill_data["match_percentage"] / 100.0, 4)

    # ------------------------------------------------------------------
    # Step 5 — Blended score
    # ------------------------------------------------------------------
    match_score = _blend_score(similarity, skill_coverage_ratio)

    # ------------------------------------------------------------------
    # Step 6 — Build explainable breakdown
    # ------------------------------------------------------------------
    breakdown = {
        "tfidf_similarity": similarity,
        "tfidf_weight": 0.5,
        "skill_coverage": skill_coverage_ratio,
        "skill_match_percentage": skill_data["match_percentage"],
        "skill_weight": 0.5,
        "tfidf_contribution": round(similarity * 0.5 * 100, 2),
        "skill_contribution": round(skill_coverage_ratio * 0.5 * 100, 2),
    }

    return {
        "match_score": match_score,
        "matched_skills": skill_data["matched_skills"],
        "missing_skills": skill_data["missing_skills"],
        "skill_match_percentage": skill_data["match_percentage"],
        "resume_skills": skill_data["resume_skills"],
        "similarity_score": similarity,
        "recommendation": _recommend(match_score),
        "breakdown": breakdown,
    }
