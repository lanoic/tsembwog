from pydantic import BaseModel, EmailStr
from datetime import datetime
class Token(BaseModel): access_token: str; token_type: str = "bearer"
class UserCreate(BaseModel): email: EmailStr; password: str
class UserOut(BaseModel): id:int; email:EmailStr; is_admin:bool
class CertificateIn(BaseModel): source:str; amount_mwh:float; owner_id:int
class CertificateOut(BaseModel):
    uid:str; source:str; amount_mwh:float; issue_date:datetime; valid_until:datetime; owner_id:int; status:str
    class Config: from_attributes=True
class DSRDeviceIn(BaseModel): name:str; site:str; owner_id:int; max_kw:float
class DSREventIn(BaseModel): start_time:datetime; end_time:datetime; target_reduction_kw:float; note:str=""
class DSREventRegistrationIn(BaseModel): event_id:int; device_id:int; committed_kw:float
class BTMDeviceIn(BaseModel): site:str; storage_capacity_kwh:float; current_soc:float=0.5; owner_id:int; name:str
class BTMReadingIn(BaseModel): device_id:int; load_kw:float; solar_kw:float
