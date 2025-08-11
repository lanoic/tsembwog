from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from .deps import get_db, get_current_user
from .models import APIKey

router = APIRouter(prefix="/keys", tags=["api-keys"])

def require_api_key(x_api_key: str | None = Header(default=None), db: Session = Depends(get_db)):
    if not x_api_key: raise HTTPException(status_code=401, detail="Missing API key")
    row = db.query(APIKey).filter(APIKey.key == x_api_key).first()
    if not row: raise HTTPException(status_code=401, detail="Invalid API key")
    return row

@router.post("/issue")
def issue(label: str = "default", user=Depends(get_current_user), db: Session = Depends(get_db)):
    key = str(uuid4())
    row = APIKey(key=key, label=label, owner_user_id=user.id)
    db.add(row); db.commit(); db.refresh(row)
    return {"api_key": row.key, "label": row.label}

@router.get("/mine")
def mine(user=Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(APIKey).filter(APIKey.owner_user_id == user.id).all()
    return [{"label": r.label, "key": r.key, "created_at": r.created_at.isoformat()} for r in rows]

# Example protected service endpoint
@router.get("/service/ping")
def svc_ping(_key=Depends(require_api_key)):
    return {"ok": True}
