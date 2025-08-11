from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from .deps import get_db, get_current_user
from . import models, schemas
router = APIRouter(prefix="/rego", tags=["rego"])
@router.post("/issue", response_model=schemas.CertificateOut)
def issue(cert: schemas.CertificateIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user.is_admin and user.id != cert.owner_id: raise HTTPException(status_code=403)
    c=models.Certificate(uid=str(uuid4()), source=cert.source, amount_mwh=cert.amount_mwh, owner_id=cert.owner_id)
    db.add(c); db.commit(); db.refresh(c); return c
@router.get("/mine", response_model=list[schemas.CertificateOut])
def mine(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Certificate).filter(models.Certificate.owner_id==user.id).all()
@router.post("/transfer/{uid}")
def transfer(uid:str, new_owner_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    c=db.query(models.Certificate).filter(models.Certificate.uid==uid).first()
    if not c: raise HTTPException(404)
    if c.owner_id!=user.id and not user.is_admin: raise HTTPException(403)
    c.owner_id=new_owner_id; c.status="transferred"; db.commit(); return {"status":"ok"}
@router.post("/retire/{uid}")
def retire(uid:str, db:Session=Depends(get_db), user=Depends(get_current_user)):
    c=db.query(models.Certificate).filter(models.Certificate.uid==uid).first()
    if not c: raise HTTPException(404)
    if c.owner_id!=user.id and not user.is_admin: raise HTTPException(403)
    c.status="retired"; db.commit(); return {"status":"ok"}
