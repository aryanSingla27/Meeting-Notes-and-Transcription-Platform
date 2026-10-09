# Meeting Notes API

FastAPI + SQLAlchemy + SQLite backend for the Fireflies-style meeting workspace.

## Run

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000/docs for Swagger API documentation.
