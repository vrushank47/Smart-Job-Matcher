import { useState } from "react";
import { analyzeResume } from "./services/api";
import "./App.css";
import GridBackground from "./components/GridBackground";

const MIN_LENGTH = 10;

export default function App() {
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const canSubmit =
    resumeText.trim().length >= MIN_LENGTH &&
    jobDescription.trim().length >= MIN_LENGTH &&
    !loading;

  async function handleAnalyze(e) {
    e.preventDefault();
    if (!canSubmit) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeResume(resumeText, jobDescription);
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong while analyzing.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
    <GridBackground />
    <div className="page">
      <header className="masthead">
        <h1>Smart Job Matcher</h1>
        <p className="subhead">
          Paste a resume and a job description to see how well they line up.
        </p>
      </header>

      <form className="input-grid" onSubmit={handleAnalyze}>
        <div className="field">
          <label htmlFor="resume">Resume</label>
          <textarea
            id="resume"
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="Paste the resume text here..."
            rows={12}
          />
        </div>

        <div className="field">
          <label htmlFor="jd">Job description</label>
          <textarea
            id="jd"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description here..."
            rows={12}
          />
        </div>

        <div className="action-row">
          <button type="submit" disabled={!canSubmit}>
            {loading ? "Analyzing..." : "Analyze match"}
          </button>
          {!loading && (resumeText || jobDescription) && !canSubmit && (
            <span className="hint">
              Both fields need at least {MIN_LENGTH} characters.
            </span>
          )}
        </div>
      </form>

      {loading && (
        <div className="status-panel loading" role="status">
          <span className="spinner" aria-hidden="true" />
          Comparing resume against job requirements...
        </div>
      )}

      {error && (
        <div className="status-panel error" role="alert">
          Couldn't complete the analysis: {error}
        </div>
      )}

      {result && !loading && (
        <section className="results">
          <div className="score-card">
            <div className="score-number">{Math.round(result.match_score)}</div>
            <div className="score-label">match score out of 100</div>
            <p className="recommendation">{result.recommendation}</p>
          </div>

          <div className="skills-grid">
            <div className="skill-panel matched">
              <h2>Matched skills ({result.matched_skills.length})</h2>
              {result.matched_skills.length > 0 ? (
                <ul>
                  {result.matched_skills.map((skill) => (
                    <li key={skill}>{skill}</li>
                  ))}
                </ul>
              ) : (
                <p className="empty">No overlapping skills found.</p>
              )}
            </div>

            <div className="skill-panel missing">
              <h2>Missing skills ({result.missing_skills.length})</h2>
              {result.missing_skills.length > 0 ? (
                <ul>
                  {result.missing_skills.map((skill) => (
                    <li key={skill}>{skill}</li>
                  ))}
                </ul>
              ) : (
                <p className="empty">Nothing missing — full skill coverage.</p>
              )}
            </div>
          </div>

          <details className="breakdown">
            <summary>Score breakdown</summary>
            <dl>
              <dt>Text similarity (TF-IDF)</dt>
              <dd>{result.similarity_score.toFixed(3)}</dd>
              <dt>Skill match</dt>
              <dd>{result.skill_match_percentage.toFixed(1)}%</dd>
            </dl>
          </details>
        </section>
      )}
    </div>
    </>
  );
}