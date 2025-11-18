from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    collected_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="payments", lazy="joined")
    shop = relationship("Shop", back_populates="payments", lazy="joined")
    collected_by = relationship("User", back_populates="payments", lazy="joined")
