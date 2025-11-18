from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.loan import LoanRepaymentFrequency

class LoanBase(BaseModel):
    customer_id: int
    principal_amount: Decimal
    interest_rate: Optional[Decimal] = Decimal("0.00")
    total_repayable_amount: Decimal
    repayment_frequency: LoanRepaymentFrequency
    start_date: datetime
    end_date: Optional[datetime] = None
    notes: Optional[str] = None

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class LoanPaymentBase(BaseModel):
    loan_id: int
    customer_id: int
    amount_paid: Decimal
    pending_balance: Decimal
    payment_date: datetime
    payment_mode: Optional[str] = "CASH"
    notes: Optional[str] = None

class LoanPaymentCreate(LoanPaymentBase):
    pass

class LoanPayment(LoanPaymentBase):
    id: int
    recorded_by_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class LoanWithPayments(Loan):
    loan_payments: list[LoanPayment] = []
