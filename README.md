
````markdown
# Smart Job Matcher

> **Know where your resume stands before you apply.**

Applying to jobs usually means doing the same thing over and over again — reading a job description, comparing it with your resume, and trying to figure out whether you're actually a good fit.

I built **Smart Job Matcher** to make that comparison quick and understandable.

Paste your resume, paste a job description, and the application breaks down the match into a score, relevant skills, missing skills, and the reasoning behind the score.

---

## What it does

The matcher looks at a resume and a job description from two different angles:

### 1. Text Similarity

It uses **TF-IDF + Cosine Similarity** to measure how closely the two pieces of text overlap.

### 2. Skill Matching

It checks the technical skills mentioned in the job description against the skills detected in the resume.

These are combined into a final match score.

Instead of just saying:

```text
You are a 54% match
````

the application also tells you **why**.

For example:

```text
Match Score        54%

TF-IDF Similarity  24.9%
Skill Match        83.3%

Matched Skills
✓ Python
✓ FastAPI
✓ MongoDB
✓ Git

Missing Skills
✗ Docker
✗ Kubernetes
```

That makes the score much easier to interpret.

---

## Why I built it

Most resume screening tools give you a number without much context.

I wanted to build something where I could actually see:

* What skills does this job require?
* Which of them do I already have?
* What am I missing?
* How much does the actual resume text overlap with the job description?

The project also gave me a practical way to understand how basic NLP techniques can be used in a real application instead of just implementing them as isolated ML exercises.

---

## How it works

```text
              Resume
                 │
                 ▼
         Text Preprocessing
                 │
        ┌────────┴────────┐
        ▼                 ▼
   TF-IDF +             Skill
   Cosine Similarity    Analysis
        │                 │
        └────────┬────────┘
                 ▼
          Weighted Score
                 │
                 ▼
      Match + Skill Gaps
                 │
                 ▼
           Recommendation
```

The backend exposes this through a FastAPI API, while the React frontend handles the interaction and presents the results.

---

## Tech Stack

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* Python
* FastAPI

### NLP / Machine Learning

* Scikit-learn
* NLTK
* TF-IDF
* Cosine Similarity

### Other

* Git
* GitHub
* REST API

---

## Project Structure

```text
Smart_resume_matcher/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   │   ├── matcher.py
│   │   │   ├── skill_analyzer.py
│   │   │   └── text_processor.py
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── ...
│   └── package.json
│
├── data/
│   └── skills.json
│
├── README.md
└── .gitignore
```

---

## Running it locally

### Backend

```bash
cd backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

Open another terminal:

```bash
cd frontend

npm install
npm run dev
```

Then open the local URL shown by Vite.

---

## A small technical detail

The project currently uses **TF-IDF**, which is based on lexical similarity.

That means it works well when the resume and job description use similar terminology, but it doesn't fully understand that different phrases can have the same meaning.

For example:

```text
"building backend APIs"
```

and

```text
"developing server-side REST services"
```

may be related to a human, but TF-IDF won't necessarily recognize them as strongly related.

That's one of the limitations of the current implementation — and also one of the areas I'd like to improve.

---

## What's next

Some things I'd like to explore:

* Resume PDF upload and extraction
* Semantic similarity using sentence embeddings
* Better skill/entity extraction
* Experience-level matching
* More detailed resume improvement suggestions
* Job recommendations based on the candidate's profile

The current version intentionally keeps the matching pipeline simple enough to understand and explain.

---

## Built by

**Vrushank Saravade**

Information Technology Engineering Student

[GitHub](https://github.com/vrushank47) · [LinkedIn](https://www.linkedin.com/in/vrushank-saravade/) · [X](https://x.com/Vrushank736)

---

⭐ If you find the project interesting, feel free to explore the code or try the matching pipeline yourself.

```

**One thing:** change the project structure name from `Smart_resume_matcher/` to `smart-job-matcher/` **only if you actually rename the GitHub repository/project folder**. Otherwise leave it as your real folder name.
```
