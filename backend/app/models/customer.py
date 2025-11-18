from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.database import Base

class CollectionCycle(str, enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"

class PaymentType(str, enum.Enum):
    LOAN = "LOAN"
    SUBSCRIPTION = "SUBSCRIPTION"
    USAGE_BASED = "USAGE_BASED"

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True)
    address = Column(String)
    payment_type = Column(Enum(PaymentType), nullable=True)
    collection_cycle = Column(Enum(CollectionCycle), nullable=False)
    collection_amount = Column(Numeric(10, 2), nullable=False)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    agent = relationship("User", back_populates="customers", lazy="joined")
    shops = relationship("Shop", back_populates="customer", lazy="dynamic")
    payments = relationship("Payment", back_populates="customer", lazy="dynamic")
    loans = relationship("Loan", back_populates="customer", lazy="dynamic")
    loan_payments = relationship("LoanPayment", back_populates="customer", lazy="dynamic")
    subscriptions = relationship("Subscription", back_populates="customer", lazy="dynamic")
    subscription_bills = relationship("Bill", back_populates="customer", lazy="dynamic")
    subscription_bill_payments = relationship("BillPayment", back_populates="customer", lazy="dynamic")
    usage_billings = relationship("UsageBasedBilling", back_populates="customer", lazy="dynamic")
    usage_records = relationship("UsageRecord", back_populates="customer", lazy="dynamic")
    usage_bills = relationship("UsageBill", back_populates="customer", lazy="dynamic")
    usage_bill_payments = relationship("UsageBillPayment", back_populates="customer", lazy="dynamic")
