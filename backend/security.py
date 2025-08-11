from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from .config import settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM="HS256"
def hash_password(p): return pwd_context.hash(p)
def verify_password(p,h): return pwd_context.verify(p,h)
def create_access_token(sub:str, minutes:int|None=None):
    expire = datetime.utcnow()+timedelta(minutes=minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub":sub,"exp":expire}, settings.SECRET_KEY, algorithm=ALGORITHM)
