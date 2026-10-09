from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import Meeting, Participant, TranscriptSegment, Summary, ActionItem
from ..schemas import MeetingCreate, MeetingOut, MeetingUpdate

router = APIRouter(prefix="/api/meetings", tags=["meetings"])

def load(db, mid):
    meeting = db.query(Meeting).options(joinedload(Meeting.participants), joinedload(Meeting.transcript), joinedload(Meeting.summary), joinedload(Meeting.action_items)).filter(Meeting.id == mid).first()
    if not meeting: raise HTTPException(404, "Meeting not found")
    return meeting

@router.get("", response_model=list[MeetingOut])
def list_meetings(search: str = "", participant: str = "", sort: str = Query("recent", pattern="^(recent|oldest)$"), db: Session = Depends(get_db)):
    q = db.query(Meeting).options(joinedload(Meeting.participants), joinedload(Meeting.transcript), joinedload(Meeting.summary), joinedload(Meeting.action_items))
    if search:
        term = f"%{search}%"
        q = q.outerjoin(Meeting.participants).filter(or_(Meeting.title.ilike(term), Participant.name.ilike(term))).distinct()
    if participant:
        q = q.join(Meeting.participants).filter(Participant.name.ilike(f"%{participant}%")).distinct()
    q = q.order_by(Meeting.date.desc() if sort == "recent" else Meeting.date.asc())
    return q.all()

@router.post("", response_model=MeetingOut, status_code=201)
def create_meeting(payload: MeetingCreate, db: Session = Depends(get_db)):
    meeting = Meeting(title=payload.title, date=payload.date or datetime.utcnow(), duration=payload.duration)
    db.add(meeting); db.flush()
    for p in payload.participants: db.add(Participant(meeting_id=meeting.id, name=p.name, email=p.email))
    for s in payload.transcript: db.add(TranscriptSegment(meeting_id=meeting.id, **s.model_dump()))
    if payload.summary:
        db.add(Summary(meeting_id=meeting.id, overview=payload.summary.overview, key_topics="\n".join(payload.summary.key_topics), outline="\n".join(payload.summary.outline)))
    for a in payload.action_items: db.add(ActionItem(meeting_id=meeting.id, **a.model_dump()))
    db.commit(); return load(db, meeting.id)

@router.get("/{mid}", response_model=MeetingOut)
def get_meeting(mid: int, db: Session = Depends(get_db)): return load(db, mid)

@router.put("/{mid}", response_model=MeetingOut)
def update_meeting(mid: int, payload: MeetingUpdate, db: Session = Depends(get_db)):
    meeting = load(db, mid)
    data = payload.model_dump(exclude_unset=True)
    participants = data.pop("participants", None)
    for key, value in data.items(): setattr(meeting, key, value)
    if participants is not None:
        db.query(Participant).filter(Participant.meeting_id == mid).delete()
        for p in participants: db.add(Participant(meeting_id=mid, **p))
    db.commit(); return load(db, mid)

@router.delete("/{mid}", status_code=204)
def delete_meeting(mid: int, db: Session = Depends(get_db)):
    meeting = load(db, mid); db.delete(meeting); db.commit()
