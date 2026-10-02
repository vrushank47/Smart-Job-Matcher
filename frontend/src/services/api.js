const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Calls POST /api/analyze on the Smart Job Matcher backend.
 * @param {string} resumeText
 * @param {string} jobDescription
 * @returns {Promise<object>} AnalyzeResponse shape from the backend schema
 */
export async function analyzeResume(resumeText, jobDescription) {
  const res = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobDescription,
    }),
  });

  if (!res.ok) {
    let detail = `Request failed with status ${res.status}`;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch {
      // response wasn't JSON — keep default message
    }
    throw new Error(detail);
  }

  return res.json();
}