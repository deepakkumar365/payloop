from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.database import Base

class UserRole(str, enum.Enum):
    SUPERADMIN = "SUPERADMIN"
    ADMIN = "ADMIN"
    AGENT = "AGENT"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    customers = relationship("Customer", back_populates="agent", lazy="dynamic")
    payments = relationship("Payment", back_populates="collected_by", lazy="dynamic")
    created_by = relationship("User", remote_side=[id], lazy="select")
    loan_payments = relationship("LoanPayment", back_populates="recorded_by", lazy="dynamic")
    bill_payments = relationship("BillPayment", back_populates="recorded_by", lazy="dynamic")
    usage_bill_payments = relationship("UsageBillPayment", back_populates="recorded_by", lazy="dynamic")
