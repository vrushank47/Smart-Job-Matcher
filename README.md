# Smart Job Matcher

Smart Job Matcher is an AI & NLP powered job and resume matching platform.

## Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: React, Vite
- **AI/ML**: scikit-learn
- **NLP**: NLTK
- **Database**: None (in-memory / file-based for now)

## Project Structure

```text
Smart_resume_matcher/
├── backend/
│   ├── app/
│   │   ├── api/          # API route handlers
│   │   ├── models/       # Data schemas and models
│   │   ├── services/     # NLP, ML, and business logic
│   │   ├── __init__.py
│   │   └── main.py       # FastAPI application entrypoint
│   └── requirements.txt  # Python backend dependencies
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # View / Page components
│   │   ├── services/     # API integration services
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx      # React entrypoint
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── data/
│   └── skills.json       # Skills dataset
├── requirements.txt      # Root pointer to backend requirements
└── .gitignore
```

## Getting Started

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Swagger docs are at `http://localhost:8000/docs`.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.
