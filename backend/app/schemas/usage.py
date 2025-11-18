from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from app.models.usage import UsageBillingStatus

class UsageBasedBillingBase(BaseModel):
    customer_id: int
    service_name: str
    rate_per_unit: Decimal
    rate_type: Optional[str] = "PER_DAY"
    start_date: datetime
    end_date: Optional[datetime] = None
    notes: Optional[str] = None

class UsageBasedBillingCreate(UsageBasedBillingBase):
    pass

class UsageBasedBilling(UsageBasedBillingBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UsageRecordBase(BaseModel):
    usage_billing_id: int
    customer_id: int
    usage_date: date
    quantity_used: Optional[Decimal] = Decimal("1.00")
    notes: Optional[str] = None

class UsageRecordCreate(UsageRecordBase):
    pass

class UsageRecord(UsageRecordBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UsageBillBase(BaseModel):
    usage_billing_id: int
    customer_id: int
    bill_number: str
    billing_period_start: date
    billing_period_end: date
    total_usage_days: int
    total_quantity_used: Decimal
    rate_per_unit: Decimal
    amount_due: Decimal
    previous_pending_balance: Optional[Decimal] = Decimal("0.00")
    total_amount_to_collect: Decimal
    notes: Optional[str] = None

class UsageBillCreate(UsageBillBase):
    pass

class UsageBill(UsageBillBase):
    id: int
    amount_paid: Decimal
    status: UsageBillingStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UsageBillPaymentBase(BaseModel):
    usage_bill_id: int
    customer_id: int
    amount_paid: Decimal
    payment_date: datetime
    payment_mode: Optional[str] = "CASH"
    notes: Optional[str] = None

class UsageBillPaymentCreate(UsageBillPaymentBase):
    pass

class UsageBillPayment(UsageBillPaymentBase):
    id: int
    recorded_by_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UsageBillWithPayments(UsageBill):
    usage_bill_payments: list[UsageBillPayment] = []

class UsageBasedBillingWithRecords(UsageBasedBilling):
    usage_records: list[UsageRecord] = []
    usage_bills: list[UsageBill] = []
