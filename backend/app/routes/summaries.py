from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Meeting, Summary
from ..schemas import SummaryIn, SummaryOut
router=APIRouter(prefix="/api",tags=["summaries"])
@router.put("/meetings/{mid}/summary",response_model=SummaryOut)
def update(mid:int,payload:SummaryIn,db:Session=Depends(get_db)):
    if not db.query(Meeting).filter(Meeting.id==mid).first(): raise HTTPException(404,"Meeting not found")
    item=db.query(Summary).filter(Summary.meeting_id==mid).first()
    if not item: item=Summary(meeting_id=mid); db.add(item)
    item.overview=payload.overview; item.key_topics="\n".join(payload.key_topics); item.outline="\n".join(payload.outline)
    db.commit(); db.refresh(item); return item
