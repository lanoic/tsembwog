from .database import Base, engine, SessionLocal
from .models import User, Certificate, Organization, APIKey
from .security import hash_password
from uuid import uuid4
def run():
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    # orgs
    org = db.query(Organization).filter(Organization.name=='Tsembwog Ltd').first()
    if not org:
        org = Organization(name='Tsembwog Ltd'); db.add(org); db.commit(); db.refresh(org)
    if not db.query(User).filter(User.email=="admin@tsembwog.com").first():
        admin=User(email="admin@tsembwog.com", hashed_password=hash_password("admin123"), is_admin=True, role='admin', org_id=org.id)
        user=User(email="user@tsembwog.com", hashed_password=hash_password("user123"), is_admin=False, role='member', org_id=org.id)
        db.add_all([admin,user]); db.commit()
        c1=Certificate(uid=str(uuid4()), source="SolarFarm-Alpha", amount_mwh=250, owner_id=admin.id)
        c2=Certificate(uid=str(uuid4()), source="WindPark-Beta", amount_mwh=120, owner_id=user.id)
        db.add_all([c1,c2]); db.commit()
    db.close()
if __name__=="__main__": run()

    # demo api key
    if not db.query(APIKey).first():
        db.add(APIKey(key='DEMO-KEY', label='demo', owner_user_id=admin.id)); db.commit()
