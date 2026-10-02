from app.services.nlp_utils import preprocess
from app.services.matcher import analyze

resume = "Python developer with experience in JavaScript, React, SQL, MongoDB and Git."
jd = "Looking for a developer experienced with C/C++, IPC, socket programming, multithreading, data structures and algorithms."

print("RESUME CLEAN:", repr(preprocess(resume)))
print("JD CLEAN:    ", repr(preprocess(jd)))

result = analyze(resume, jd)
print("similarity:", result["similarity_score"])
print("skill_match_percentage:", result["skill_match_percentage"])
print("match_score:", result["match_score"])
print("breakdown:", result["breakdown"])
