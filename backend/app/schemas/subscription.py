from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.subscription import BillingCycle, BillStatus

class SubscriptionBase(BaseModel):
    customer_id: int
    subscription_amount: Decimal
    billing_cycle: BillingCycle
    start_date: datetime
    end_date: Optional[datetime] = None
    notes: Optional[str] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class BillBase(BaseModel):
    subscription_id: int
    customer_id: int
    bill_number: str
    billing_period_start: datetime
    billing_period_end: datetime
    amount_due: Decimal
    previous_pending_balance: Optional[Decimal] = Decimal("0.00")
    total_amount_to_collect: Decimal
    notes: Optional[str] = None

class BillCreate(BillBase):
    pass

class Bill(BillBase):
    id: int
    amount_paid: Decimal
    status: BillStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class BillPaymentBase(BaseModel):
    bill_id: int
    customer_id: int
    amount_paid: Decimal
    payment_date: datetime
    payment_mode: Optional[str] = "CASH"
    notes: Optional[str] = None

class BillPaymentCreate(BillPaymentBase):
    pass

class BillPayment(BillPaymentBase):
    id: int
    recorded_by_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class BillWithPayments(Bill):
    bill_payments: list[BillPayment] = []

class SubscriptionWithBills(Subscription):
    bills: list[Bill] = []
