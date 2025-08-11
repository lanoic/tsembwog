from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from .deps import get_current_user
from .feature_flags import get_flags, set_flag

router = APIRouter(prefix="/admin", tags=["admin"])

class FlagIn(BaseModel):
    key: str
    value: bool

@router.get("/flags")
def read_flags(user=Depends(get_current_user)):
    if not user.is_admin: raise HTTPException(status_code=403, detail="Admin only")
    return get_flags()

@router.post("/flags")
def write_flag(req: FlagIn, user=Depends(get_current_user)):
    if not user.is_admin: raise HTTPException(status_code=403, detail="Admin only")
    set_flag(req.key, req.value)
    return get_flags()


from .ai.pipeline import train_and_save

@router.post("/train-now")
def train_now(user=Depends(get_current_user)):
    if not user.is_admin: raise HTTPException(status_code=403, detail="Admin only")
    path = train_and_save()
    return {"status":"ok","artifact":path}


from sqlalchemy.orm import Session
from .deps import get_db

@router.get("/users")
def list_users(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.is_admin: raise HTTPException(status_code=403, detail="Admin only")
    from .models import User
    rows = db.query(User).all()
    return [{"id":u.id,"email":u.email,"is_admin":u.is_admin,"role":u.role,"org_id":u.org_id} for u in rows]

@router.post("/users/{user_id}/role")
def set_role(user_id: int, role: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.is_admin: raise HTTPException(status_code=403, detail="Admin only")
    from .models import User
    row = db.query(User).get(user_id)
    if not row: raise HTTPException(404)
    row.role = role; db.commit()
    return {"status":"ok"}

@router.get("/orgs")
def list_orgs(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.is_admin: raise HTTPException(status_code=403, detail="Admin only")
    from .models import Organization
    rows = db.query(Organization).all()
    return [{"id":o.id,"name":o.name} for o in rows]

@router.post("/orgs/create")
def create_org(name: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.is_admin: raise HTTPException(status_code=403, detail="Admin only")
    from .models import Organization
    o = Organization(name=name); db.add(o); db.commit(); db.refresh(o)
    return {"id": o.id, "name": o.name}
