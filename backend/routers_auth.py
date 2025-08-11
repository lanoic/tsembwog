from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import schemas, models
from .deps import get_db
from .security import hash_password, verify_password, create_access_token
router = APIRouter(prefix="/auth", tags=["auth"])
@router.post("/register", response_model=schemas.UserOut)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email==payload.email).first():
        raise HTTPException(status_code=400, detail="Email exists")
    user=models.User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user); db.commit(); db.refresh(user); return user
@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect creds")
    return {"access_token": create_access_token(sub=user.email), "token_type":"bearer"}


from .deps import get_current_user

@router.get("/me", response_model=schemas.UserOut)
def me(user=Depends(get_current_user)):
    return user
