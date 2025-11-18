import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.db.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def create_admin():
    db = SessionLocal()
    try:
        existing_superadmin = db.query(User).filter(User.username == "superadmin").first()
        if existing_superadmin:
            print("Superadmin user already exists!")
            return
        
        superadmin = User(
            email="superadmin@payloop.com",
            username="superadmin",
            hashed_password=get_password_hash("superadmin123"),
            full_name="System Superadmin",
            role=UserRole.SUPERADMIN,
            is_active=True
        )
        db.add(superadmin)
        db.commit()
        print("✅ Superadmin user created successfully!")
        print("Username: superadmin")
        print("Password: superadmin123")
    except Exception as e:
        print(f"❌ Error creating superadmin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
