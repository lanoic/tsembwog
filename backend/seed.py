from uuid import uuid4

from .database import Base, engine, SessionLocal
from .models import User, Certificate, Organization, APIKey
from .security import hash_password


def run() -> None:
    """Create tables and seed minimal, idempotent demo data."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # --- Organization ---
        org = db.query(Organization).filter(Organization.name == "Tsembwog Ltd").first()
        if not org:
            org = Organization(name="Tsembwog Ltd")
            db.add(org)
            db.commit()
            db.refresh(org)

        # --- Admin user ---
        admin = db.query(User).filter(User.email == "admin@tsembwog.com").first()
        if not admin:
            admin = User(
                email="admin@tsembwog.com",
                hashed_password=hash_password("admin123"),
                is_admin=True,
                role="admin",
                org_id=org.id,
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)

        # --- Member user ---
        member = db.query(User).filter(User.email == "user@tsembwog.com").first()
        if not member:
            member = User(
                email="user@tsembwog.com",
                hashed_password=hash_password("user123"),
                is_admin=False,
                role="member",
                org_id=org.id,
            )
            db.add(member)
            db.commit()
            db.refresh(member)

        # --- Demo certificates (only if none exist yet) ---
        if db.query(Certificate).count() == 0:
            c1 = Certificate(
                uid=str(uuid4()), source="SolarFarm-Alpha", amount_mwh=250, owner_id=admin.id
            )
            c2 = Certificate(
                uid=str(uuid4()), source="WindPark-Beta", amount_mwh=120, owner_id=member.id
            )
            db.add_all([c1, c2])
            db.commit()

        # --- Demo API key (owned by admin) ---
        if not db.query(APIKey).first():
            db.add(APIKey(key="DEMO-KEY", label="demo", owner_user_id=admin.id))
            db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    run()
