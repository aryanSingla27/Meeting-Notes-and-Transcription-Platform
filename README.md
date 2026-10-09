# Fireflies-inspired Meeting Notes & Transcription Platform

A full-stack meeting workspace for the SDE assignment. The implementation uses original UI code and seeded sample data while following familiar meeting-assistant interaction patterns.

## Stack
- Frontend: Next.js 15, React 19, TypeScript, CSS, lucide-react
- Backend: Python with FastAPI / Django
- Database: SQLite
- Audio: bundled placeholder WAV; no real speech-to-text is performed

## Features
- Meetings library seeded with six meetings
- Search by meeting title and participant; recency sorting and date range filter
- Dedicated meeting detail view with transcript timestamps, speaker labels, search highlighting, player seeking, playback speed and active segment highlighting
- Create meeting by form or pasted/uploaded TXT, VTT, or JSON transcript
- Edit meeting metadata and delete meetings
- Summary, key topics, outline and action items
- Add, complete/uncomplete and delete action items
- TXT export from the meeting detail view
- Dedicated Channels/Integrations and Analytics pages
- Profile dropdown, notification dropdown, settings page, persistent light/dark theme
- SQLite persistence and FastAPI Swagger docs

## Folder structure
```text
frontend/  Next.js app and reusable components
backend/   FastAPI app, SQLAlchemy models, routes and seed data
```

## Requirements
- Node.js 20.9+ (Node 22 LTS recommended)
- Python 3.11 or 3.12
- Git (optional, for GitHub submission)

## Run on Windows

### 1. Start the backend
Open a terminal in the project root:

```powershell
cd backend
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

If PowerShell blocks environment activation, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then activate again. Keep the backend terminal open.

Backend health: http://localhost:8000/api/health  
API docs: http://localhost:8000/docs

If the Python launcher is not available, use `python -m venv .venv` instead of `py -3.12`.

### 2. Start the frontend
Open a second terminal in the project root:

```powershell
cd frontend
npm install
```

Create `.env.local` from `.env.example` if needed. The default API URL is `http://localhost:8000/api`.

```powershell
npm run dev
```

Open http://localhost:3000.

Keep both terminals open while using the application. Stop each server with Ctrl+C.

## Database
SQLite is created as `backend/meetings.db` when the backend starts. The app seeds six meetings only when the database is empty. Meeting data, transcript segments, summaries, participants and action items are related by foreign keys and SQLAlchemy relationships. To reset demo data, stop the backend, delete `backend/meetings.db`, then restart it.

### Schema
- `meetings`: title, date, duration, created/updated timestamps
- `participants`: meeting foreign key, name, email
- `transcript_segments`: meeting foreign key, speaker, start/end seconds, text
- `summaries`: one-to-one meeting foreign key, overview, key topics, outline
- `action_items`: meeting foreign key, title, description, assignee, completion state

## API overview
- `GET /api/meetings?search=&participant=&sort=recent|oldest`
- `POST /api/meetings`
- `GET /api/meetings/{id}`
- `PUT /api/meetings/{id}`
- `DELETE /api/meetings/{id}`
- `POST /api/meetings/{id}/transcript`
- `PUT /api/transcript/{segment_id}`
- `DELETE /api/transcript/{segment_id}`
- `GET/PUT /api/meetings/{id}/summary` (summary read is included in meeting detail)
- `POST /api/meetings/{id}/actions`
- `PUT /api/actions/{action_id}`
- `DELETE /api/actions/{action_id}`
- `GET /api/health`

## Assignment assumptions and limitations
- Default-user authentication is intentionally mocked as requested.
- Channels/integrations are clear placeholders; they do not connect to external services.
- Summary content is seeded or placeholder text. Real LLM summarization and audio transcription are out of scope.
- Audio is a placeholder sample and does not contain the actual meeting recording. Timestamp synchronization is implemented against transcript segment times.
- Local development is the primary verified configuration. Before public deployment, configure a persistent disk/database for the backend and set `NEXT_PUBLIC_API_URL` to the deployed API origin. SQLite on ephemeral hosting may lose data on redeploy.

## Pre-submission smoke test
1. Open dashboard and confirm six seeded meetings appear.
2. Search by a meeting title and participant; test recent/oldest and date filter.
3. Open a meeting; click transcript lines and move the player seek bar.
4. Search within transcript and confirm matching text is highlighted.
5. Add an action item, toggle completion, refresh, and verify it persists.
6. Create a meeting with a pasted transcript, edit its title, then delete it.
7. Visit Channels, Analytics and Settings using the sidebar.
8. Toggle theme in Settings and in the profile menu; refresh and verify the theme remains selected.
9. Check `/docs` and `/api/health` while the backend is running.
