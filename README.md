# Smart Job Matcher

> **Know where your resume stands before you apply.**

Applying to jobs usually means the same repetitive comparison: read a job description, read your resume, and try to guess whether you're actually a good fit.

I built **Smart Job Matcher** to make that comparison fast and legible. Paste your resume, paste a job description, and the app breaks the match down into a score, the skills you share, the skills you're missing, and the reasoning behind all of it.

---

## What it does

The matcher looks at a resume and a job description from two angles:

### 1. Text similarity

**TF-IDF + cosine similarity** measures how closely the two texts overlap at the word level.

### 2. Skill matching

The technical skills mentioned in the job description are checked against the skills detected in the resume.

The two signals are combined into a single weighted match score. Instead of just saying:

```text
You are a 54% match
```

the app tells you *why*:

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

That breakdown is what makes the score worth trusting instead of just taking at face value.

---

## Why I built it

Most resume screening tools hand you a number with no context. I wanted something that could actually answer:

- What skills does this job require?
- Which of them do I already have?
- What am I missing?
- How much does the resume text itself overlap with the job description?

It also gave me a concrete way to apply basic NLP techniques in a real application, rather than as isolated exercises in a notebook.

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

The backend exposes this pipeline through a FastAPI API; the React frontend handles the interaction and renders the results.

---

## Tech stack

### Frontend
- React
- Vite
- JavaScript
- CSS

### Backend
- Python
- FastAPI

### NLP / machine learning
- Scikit-learn
- NLTK
- TF-IDF
- Cosine similarity

### Other
- Git
- GitHub
- REST API

---

## Project structure

```text
Smart_resume_matcher/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── matcher.py
│   │   │   ├── nlp_utils.py
│   │   │   ├── skill_analyzer.py
│   │   │   └── skill_extractor.py
│   │   ├── __init__.py
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
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

FastAPI's interactive docs:

```text
http://127.0.0.1:8000/docs
```

### Frontend

In a separate terminal:

```bash
cd frontend

npm install
npm run dev
```

Then open the local URL Vite prints to the terminal.

---

## A small technical detail

The project currently relies on **TF-IDF**, which measures lexical overlap — matching words, not meaning.

It works well when the resume and job description use similar terminology, but it won't recognize that two differently worded phrases mean the same thing. For example:

```text
"building backend APIs"
```

and

```text
"developing server-side REST services"
```

read as closely related to a person, but TF-IDF has no guarantee of scoring them that way. That's a real limitation of the current implementation, and one of the things I'd like to improve next.

---

## What's next

- Resume PDF upload and extraction
- Semantic similarity using sentence embeddings
- Better skill and entity extraction
- Experience-level matching
- More detailed resume improvement suggestions
- Job recommendations based on a candidate's profile

The current version keeps the matching pipeline simple on purpose — simple enough to fully understand and explain.

---

## Built by

**Vrushank Saravade**
Information Technology Engineering Student

[GitHub](https://github.com/vrushank47) · [LinkedIn](https://www.linkedin.com/in/vrushank-saravade/) · [X](https://x.com/Vrushank736)

---

⭐ If you find the project interesting, feel free to explore the code or try the matching pipeline yourself.
