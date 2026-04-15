# TalentMatch AI

TalentMatch AI is a SaaS MVP for resume ingestion, candidate search, hybrid matching, and feedback-driven learning.

## What It Includes

- FastAPI backend for upload, candidate CRUD, search, semantic search, matching, and feedback.
- React frontend for recruiter workflows.
- Adaptive weight learning stored in `learning_weights.json`.
- Optional database-backed candidate storage.
- Optional LangChain-style reasoning hooks.
- Persistent vector index snapshot in `data/vector_index.json`.

## Project Layout

- `backend/`: API, services, agents, learning, and storage logic.
- `frontend/`: Vite + React UI.
- `data/`: seed candidates and generated runtime data.
- `tests/`: backend tests.
- `project_memory.md`: running engineering memory for the project.

## Final Version: How To Use It

### 1. Backend setup

Install the lightweight backend runtime if you need it again:

```powershell
python -m pip install --target .deps fastapi==0.109.2 uvicorn==0.27.1 pydantic==2.6.1 pydantic-settings==2.1.0 python-multipart==0.0.9 httpx==0.26.0 pytest==8.0.0
```

Then run the API:

```powershell
$env:PYTHONPATH="C:\Users\Akshat\OneDrive\Documents\I.T\talentmatch-ai\.deps;C:\Users\Akshat\OneDrive\Documents\I.T\talentmatch-ai\backend"
python -m uvicorn app.main:app --reload
```

Open:

- API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

### 2. Frontend setup

From `frontend/`:

```powershell
npm install
npm run dev
```

Open:

- App: `http://127.0.0.1:5173`

### 3. Main recruiter flow

1. Start the backend.
2. Start the frontend.
3. Open the app in the browser.
4. Upload a `.txt` or `.pdf` resume.
5. Review the candidate list.
6. Edit the job description.
7. Run matching.
8. Review top candidates and explanations.
9. Send feedback to `/api/feedback` to improve weights over time.

### 4. Key API endpoints

- `GET /api/candidates`
- `GET /api/candidates/semantic?query=python+fastapi`
- `POST /api/candidates`
- `POST /api/resume/upload`
- `POST /api/match`
- `POST /api/feedback`
- `GET /api/learning/weights`

### 5. Optional upgraded mode

TalentMatch AI runs now in fallback-safe mode by default. You can enable stronger integrations through environment variables:

```powershell
$env:TALENTMATCH_USE_LANGCHAIN="true"
$env:TALENTMATCH_USE_DATABASE="true"
$env:TALENTMATCH_DATABASE_URL="sqlite:///C:/Users/Akshat/OneDrive/Documents/I.T/talentmatch-ai/data/talentmatch.db"
```

Notes:

- If LangChain packages are available, analyzer and matcher reasoning will use prompt templating paths.
- If `TALENTMATCH_USE_DATABASE=true` and `TALENTMATCH_DATABASE_URL` points to SQLite, candidate records are stored in a real local database table.
- If it points to PostgreSQL and SQLAlchemy drivers are installed, the same candidate repository can use Postgres.
- `data/vector_index.json` is refreshed from candidate data and used as a persistent semantic-search snapshot.

### 6. Run tests

```powershell
$env:PYTHONPATH="C:\Users\Akshat\OneDrive\Documents\I.T\talentmatch-ai\.deps;C:\Users\Akshat\OneDrive\Documents\I.T\talentmatch-ai\backend"
python -m pytest -q
```

## Current Implementation Notes

- Matching combines weighted feature scoring and semantic similarity.
- Learning updates weights from positive/negative feedback patterns.
- LangChain and FAISS are optional integrations with safe fallbacks.
- The repo is designed to stay runnable even on constrained environments.
