from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Meeting, TranscriptSegment
from ..schemas import TranscriptIn, TranscriptOut
router = APIRouter(prefix="/api", tags=["transcripts"])

@router.post("/meetings/{mid}/transcript", response_model=TranscriptOut, status_code=201)
def create(mid:int, payload:TranscriptIn, db:Session=Depends(get_db)):
    if not db.query(Meeting).filter(Meeting.id==mid).first(): raise HTTPException(404,"Meeting not found")
    item=TranscriptSegment(meeting_id=mid,**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item

@router.put("/transcript/{sid}", response_model=TranscriptOut)
def update(sid:int,payload:TranscriptIn,db:Session=Depends(get_db)):
    item=db.query(TranscriptSegment).filter(TranscriptSegment.id==sid).first()
    if not item: raise HTTPException(404,"Transcript segment not found")
    for k,v in payload.model_dump().items(): setattr(item,k,v)
    db.commit(); db.refresh(item); return item

@router.delete("/transcript/{sid}",status_code=204)
def delete(sid:int,db:Session=Depends(get_db)):
    item=db.query(TranscriptSegment).filter(TranscriptSegment.id==sid).first()
    if not item: raise HTTPException(404,"Transcript segment not found")
    db.delete(item); db.commit()
