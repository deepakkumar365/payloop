from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Enum, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.database import Base

class BillingCycle(str, enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"

class BillStatus(str, enum.Enum):
    PENDING = "PENDING"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    FULLY_PAID = "FULLY_PAID"

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    subscription_amount = Column(Numeric(12, 2), nullable=False)
    billing_cycle = Column(Enum(BillingCycle), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = Column(Text)
    
    customer = relationship("Customer", back_populates="subscriptions", lazy="joined")
    bills = relationship("Bill", back_populates="subscription", lazy="dynamic")

class Bill(Base):
    __tablename__ = "bills"
    
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    bill_number = Column(String, unique=True, nullable=False)
    billing_period_start = Column(DateTime, nullable=False)
    billing_period_end = Column(DateTime, nullable=False)
    amount_due = Column(Numeric(12, 2), nullable=False)
    previous_pending_balance = Column(Numeric(12, 2), default=0)
    total_amount_to_collect = Column(Numeric(12, 2), nullable=False)
    amount_paid = Column(Numeric(12, 2), default=0)
    status = Column(Enum(BillStatus), default=BillStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = Column(Text)
    
    subscription = relationship("Subscription", back_populates="bills", lazy="joined")
    customer = relationship("Customer", back_populates="subscription_bills", lazy="joined")
    bill_payments = relationship("BillPayment", back_populates="bill", lazy="dynamic")

class BillPayment(Base):
    __tablename__ = "bill_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    amount_paid = Column(Numeric(12, 2), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    payment_mode = Column(String, default="CASH")
    recorded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    
    bill = relationship("Bill", back_populates="bill_payments", lazy="joined")
    customer = relationship("Customer", back_populates="subscription_bill_payments", lazy="joined")
    recorded_by = relationship("User", back_populates="bill_payments", lazy="joined")
