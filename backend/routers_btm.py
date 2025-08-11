from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .deps import get_db, get_current_user
from . import models, schemas
router = APIRouter(prefix="/btm", tags=["btm"])
@router.post("/device/register")
def register_device(d: schemas.BTMDeviceIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user.is_admin and user.id != d.owner_id: raise HTTPException(403)
    row=models.BTMDevice(**d.model_dump()); db.add(row); db.commit(); db.refresh(row); return {"id":row.id}
@router.post("/reading")
def reading(r: schemas.BTMReadingIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    dev=db.query(models.BTMDevice).get(r.device_id)
    if not dev or (dev.owner_id != user.id and not user.is_admin): raise HTTPException(403)
    row=models.BTMReading(**r.model_dump())
    net=r.solar_kw - r.load_kw
    dev.current_soc = min(1.0, max(0.0, dev.current_soc + net / max(dev.storage_capacity_kwh,1)))
    db.add(row); db.commit(); return {"status":"recorded","soc":dev.current_soc}
@router.get("/device/{device_id}")
def status(device_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    dev=db.query(models.BTMDevice).get(device_id)
    if not dev or (dev.owner_id != user.id and not user.is_admin): raise HTTPException(404)
    return {"id":dev.id,"soc":dev.current_soc,"capacity_kwh":dev.storage_capacity_kwh,"site":dev.site,"name":dev.name}
