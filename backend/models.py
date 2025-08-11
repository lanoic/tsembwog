from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime, Float, ForeignKey, UniqueConstraint
from datetime import datetime, timedelta
from .database import Base
class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

class User(Base):

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[str] = mapped_column(String, default='member')
    org_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'), nullable=True)
class Certificate(Base):
    __tablename__ = "certificates"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[str] = mapped_column(String, unique=True, index=True)
    source: Mapped[str] = mapped_column(String)
    amount_mwh: Mapped[float] = mapped_column(Float)
    issue_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    valid_until: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow()+timedelta(days=365))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String, default="active")
class DSRDevice(Base):
    __tablename__ = "dsr_devices"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    site: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    max_kw: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
class DSREvent(Base):
    __tablename__ = "dsr_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    target_reduction_kw: Mapped[float] = mapped_column(Float)
    note: Mapped[str] = mapped_column(String, default="")
class DSREventRegistration(Base):
    __tablename__ = "dsr_event_registrations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("dsr_events.id"))
    device_id: Mapped[int] = mapped_column(ForeignKey("dsr_devices.id"))
    committed_kw: Mapped[float] = mapped_column(Float)
    UniqueConstraint('event_id','device_id',name='uix_event_device')
class BTMDevice(Base):
    __tablename__ = "btm_devices"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site: Mapped[str] = mapped_column(String)
    storage_capacity_kwh: Mapped[float] = mapped_column(Float)
    current_soc: Mapped[float] = mapped_column(Float, default=0.5)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String)
class BTMReading(Base):
    __tablename__ = "btm_readings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("btm_devices.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    load_kw: Mapped[float] = mapped_column(Float)
    solar_kw: Mapped[float] = mapped_column(Float)


class APIKey(Base):
    __tablename__ = "api_keys"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String, unique=True, index=True)
    label: Mapped[str] = mapped_column(String, default='default')
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
