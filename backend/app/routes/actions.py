from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ActionItem, Meeting
from ..schemas import ActionItemIn, ActionItemOut
router = APIRouter(prefix="/api", tags=["actions"])

def get_action(db, aid):
    item = db.query(ActionItem).filter(ActionItem.id == aid).first()
    if not item: raise HTTPException(404, "Action item not found")
    return item

@router.post("/meetings/{mid}/actions", response_model=ActionItemOut, status_code=201)
def create(mid: int, payload: ActionItemIn, db: Session = Depends(get_db)):
    if not db.query(Meeting).filter(Meeting.id == mid).first(): raise HTTPException(404, "Meeting not found")
    item = ActionItem(meeting_id=mid, **payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item

@router.put("/actions/{aid}", response_model=ActionItemOut)
def update(aid: int, payload: ActionItemIn, db: Session = Depends(get_db)):
    item = get_action(db, aid)
    for k,v in payload.model_dump().items(): setattr(item,k,v)
    db.commit(); db.refresh(item); return item

@router.delete("/actions/{aid}", status_code=204)
def delete(aid: int, db: Session = Depends(get_db)):
    item = get_action(db, aid); db.delete(item); db.commit()
