
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models, database
from uuid import uuid4

def seed_data():
    db: Session = database.SessionLocal()

    # Create mock users
    user1 = models.User(email="admin@tsembwog.com", hashed_password="fakehashedadmin", is_admin=True)
    user2 = models.User(email="user@tsembwog.com", hashed_password="fakehasheduser", is_admin=False)

    db.add_all([user1, user2])
    db.commit()

    # Create mock certificates
    certs = [
        models.Certificate(
            id=str(uuid4()),
            owner="user@tsembwog.com",
            source="SolarFarm-Alpha",
            amount_mwh=100.0,
            issue_date=datetime.utcnow(),
            valid_until=datetime.utcnow() + timedelta(days=365)
        ),
        models.Certificate(
            id=str(uuid4()),
            owner="admin@tsembwog.com",
            source="WindFarm-Beta",
            amount_mwh=200.0,
            issue_date=datetime.utcnow(),
            valid_until=datetime.utcnow() + timedelta(days=365)
        )
    ]
    db.add_all(certs)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_data()
