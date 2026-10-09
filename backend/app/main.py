from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine, SessionLocal
from .seed import seed
from .routes import meetings, actions, transcripts, summaries

Base.metadata.create_all(bind=engine)
with SessionLocal() as db: seed(db)

app = FastAPI(title="Meeting Notes API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], allow_origin_regex=r"https://.*\.vercel\.app", allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(meetings.router); app.include_router(actions.router); app.include_router(transcripts.router); app.include_router(summaries.router)

@app.get("/api/health")
def health(): return {"status":"ok"}
