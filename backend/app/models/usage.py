from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Enum, Boolean, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date
import enum
from app.db.database import Base

class UsageBillingStatus(str, enum.Enum):
    PENDING = "PENDING"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    FULLY_PAID = "FULLY_PAID"

class UsageBasedBilling(Base):
    __tablename__ = "usage_based_billings"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    service_name = Column(String, nullable=False)
    rate_per_unit = Column(Numeric(10, 2), nullable=False)
    rate_type = Column(String, default="PER_DAY")
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = Column(Text)
    
    customer = relationship("Customer", back_populates="usage_billings", lazy="joined")
    usage_records = relationship("UsageRecord", back_populates="usage_billing", lazy="dynamic")
    usage_bills = relationship("UsageBill", back_populates="usage_billing", lazy="dynamic")

class UsageRecord(Base):
    __tablename__ = "usage_records"
    
    id = Column(Integer, primary_key=True, index=True)
    usage_billing_id = Column(Integer, ForeignKey("usage_based_billings.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    usage_date = Column(Date, nullable=False)
    quantity_used = Column(Numeric(10, 2), nullable=False, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = Column(Text)
    
    usage_billing = relationship("UsageBasedBilling", back_populates="usage_records", lazy="joined")
    customer = relationship("Customer", back_populates="usage_records", lazy="joined")

class UsageBill(Base):
    __tablename__ = "usage_bills"
    
    id = Column(Integer, primary_key=True, index=True)
    usage_billing_id = Column(Integer, ForeignKey("usage_based_billings.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    bill_number = Column(String, unique=True, nullable=False)
    billing_period_start = Column(Date, nullable=False)
    billing_period_end = Column(Date, nullable=False)
    total_usage_days = Column(Integer, nullable=False, default=0)
    total_quantity_used = Column(Numeric(10, 2), nullable=False, default=0)
    rate_per_unit = Column(Numeric(10, 2), nullable=False)
    amount_due = Column(Numeric(12, 2), nullable=False)
    previous_pending_balance = Column(Numeric(12, 2), default=0)
    total_amount_to_collect = Column(Numeric(12, 2), nullable=False)
    amount_paid = Column(Numeric(12, 2), default=0)
    status = Column(Enum(UsageBillingStatus), default=UsageBillingStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = Column(Text)
    
    usage_billing = relationship("UsageBasedBilling", back_populates="usage_bills", lazy="joined")
    customer = relationship("Customer", back_populates="usage_bills", lazy="joined")
    usage_bill_payments = relationship("UsageBillPayment", back_populates="usage_bill", lazy="dynamic")

class UsageBillPayment(Base):
    __tablename__ = "usage_bill_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    usage_bill_id = Column(Integer, ForeignKey("usage_bills.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    amount_paid = Column(Numeric(12, 2), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    payment_mode = Column(String, default="CASH")
    recorded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    
    usage_bill = relationship("UsageBill", back_populates="usage_bill_payments", lazy="joined")
    customer = relationship("Customer", back_populates="usage_bill_payments", lazy="joined")
    recorded_by = relationship("User", back_populates="usage_bill_payments", lazy="joined")
