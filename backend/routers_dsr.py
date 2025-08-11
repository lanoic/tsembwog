from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .deps import get_db, get_current_user
from . import models, schemas
router = APIRouter(prefix="/dsr", tags=["dsr"])
@router.post("/device/register")
def register_device(d: schemas.DSRDeviceIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user.is_admin and user.id != d.owner_id: raise HTTPException(status_code=403)
    row=models.DSRDevice(name=d.name, site=d.site, owner_id=d.owner_id, max_kw=d.max_kw, is_active=True)
    db.add(row); db.commit(); db.refresh(row); return {"id":row.id}
@router.post("/event/create")
def create_event(e: schemas.DSREventIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user.is_admin: raise HTTPException(403)
    row=models.DSREvent(**e.model_dump()); db.add(row); db.commit(); db.refresh(row); return {"id":row.id}
@router.get("/events")
def events(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.DSREvent).all()
