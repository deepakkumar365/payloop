from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Enum, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.database import Base

class LoanRepaymentFrequency(str, enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"

class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    principal_amount = Column(Numeric(12, 2), nullable=False)
    interest_rate = Column(Numeric(5, 2), default=0)
    total_repayable_amount = Column(Numeric(12, 2), nullable=False)
    repayment_frequency = Column(Enum(LoanRepaymentFrequency), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = Column(Text)
    
    customer = relationship("Customer", back_populates="loans", lazy="joined")
    loan_payments = relationship("LoanPayment", back_populates="loan", lazy="dynamic")

class LoanPayment(Base):
    __tablename__ = "loan_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    amount_paid = Column(Numeric(12, 2), nullable=False)
    pending_balance = Column(Numeric(12, 2), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    payment_mode = Column(String, default="CASH")
    recorded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    
    loan = relationship("Loan", back_populates="loan_payments", lazy="joined")
    customer = relationship("Customer", back_populates="loan_payments", lazy="joined")
    recorded_by = relationship("User", back_populates="loan_payments", lazy="joined")
