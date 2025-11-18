from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.customer import CollectionCycle, PaymentType

class CustomerBase(BaseModel):
    name: str
    phone: str
    address: Optional[str] = None
    payment_type: Optional[PaymentType] = None
    collection_cycle: CollectionCycle
    collection_amount: Decimal

class CustomerCreate(CustomerBase):
    agent_id: int

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    payment_type: Optional[PaymentType] = None
    collection_cycle: Optional[CollectionCycle] = None
    collection_amount: Optional[Decimal] = None
    is_active: Optional[bool] = None

class Customer(CustomerBase):
    id: int
    agent_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
