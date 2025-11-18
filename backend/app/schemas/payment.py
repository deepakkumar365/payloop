from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class PaymentBase(BaseModel):
    customer_id: int
    shop_id: Optional[int] = None
    amount: Decimal
    notes: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    collected_by_id: int
    payment_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
