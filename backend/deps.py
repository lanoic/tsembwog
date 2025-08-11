from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from .database import SessionLocal
from .models import User
from .config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
def get_current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db))->User:
    try:
        payload=jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email=payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user=db.query(User).filter(User.email==email).first()
    if not user: raise HTTPException(status_code=401, detail="User not found")
    return user
