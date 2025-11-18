from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date
from app.db.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.models.usage import UsageBasedBilling, UsageRecord, UsageBill, UsageBillPayment
from app.models.customer import Customer
from app.schemas.usage import (
    UsageBasedBilling as UsageBasedBillingSchema, UsageBasedBillingCreate,
    UsageRecord as UsageRecordSchema, UsageRecordCreate,
    UsageBill as UsageBillSchema, UsageBillCreate,
    UsageBillPayment as UsageBillPaymentSchema, UsageBillPaymentCreate,
    UsageBasedBillingWithRecords, UsageBillWithPayments
)

router = APIRouter()

@router.post("/", response_model=UsageBasedBillingSchema, status_code=status.HTTP_201_CREATED)
def create_usage_billing(
    billing_in: UsageBasedBillingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    customer = db.query(Customer).filter(Customer.id == billing_in.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if current_user.role == "AGENT" and customer.agent_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Agents can only create usage billing for their customers"
        )
    
    db_billing = UsageBasedBilling(**billing_in.dict())
    db.add(db_billing)
    db.commit()
    db.refresh(db_billing)
    return db_billing

@router.get("/", response_model=List[UsageBasedBillingSchema])
def list_usage_billings(
    skip: int = 0,
    limit: int = 100,
    customer_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(UsageBasedBilling)
    
    if current_user.role == "AGENT":
        query = query.join(Customer).filter(Customer.agent_id == current_user.id)
    
    if customer_id:
        query = query.filter(UsageBasedBilling.customer_id == customer_id)
    
    billings = query.offset(skip).limit(limit).all()
    return billings

@router.get("/{billing_id}", response_model=UsageBasedBillingWithRecords)
def read_usage_billing(
    billing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    billing = db.query(UsageBasedBilling).filter(UsageBasedBilling.id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Usage billing not found")
    
    if current_user.role == "AGENT":
        customer = db.query(Customer).filter(Customer.id == billing.customer_id).first()
        if customer.agent_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return billing

@router.post("/{billing_id}/records", response_model=UsageRecordSchema, status_code=status.HTTP_201_CREATED)
def create_usage_record(
    billing_id: int,
    record_in: UsageRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    billing = db.query(UsageBasedBilling).filter(UsageBasedBilling.id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Usage billing not found")
    
    customer = db.query(Customer).filter(Customer.id == billing.customer_id).first()
    if current_user.role == "AGENT" and customer.agent_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Agents can only record usage for their customers"
        )
    
    db_record = UsageRecord(**record_in.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.get("/{billing_id}/records", response_model=List[UsageRecordSchema])
def list_usage_records(
    billing_id: int,
    skip: int = 0,
    limit: int = 100,
    usage_date: date = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    billing = db.query(UsageBasedBilling).filter(UsageBasedBilling.id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Usage billing not found")
    
    if current_user.role == "AGENT":
        customer = db.query(Customer).filter(Customer.id == billing.customer_id).first()
        if customer.agent_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    query = db.query(UsageRecord).filter(UsageRecord.usage_billing_id == billing_id)
    
    if usage_date:
        query = query.filter(UsageRecord.usage_date == usage_date)
    
    records = query.offset(skip).limit(limit).all()
    return records

@router.post("/{billing_id}/bills", response_model=UsageBillSchema, status_code=status.HTTP_201_CREATED)
def create_usage_bill(
    billing_id: int,
    bill_in: UsageBillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    billing = db.query(UsageBasedBilling).filter(UsageBasedBilling.id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Usage billing not found")
    
    if current_user.role not in ["ADMIN", "SUPERADMIN"]:
        raise HTTPException(
            status_code=403,
            detail="Only admins can create bills"
        )
    
    existing_bill = db.query(UsageBill).filter(UsageBill.bill_number == bill_in.bill_number).first()
    if existing_bill:
        raise HTTPException(
            status_code=400,
            detail="Bill number already exists"
        )
    
    db_bill = UsageBill(**bill_in.dict())
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill

@router.get("/{billing_id}/bills", response_model=List[UsageBillSchema])
def list_usage_bills(
    billing_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    billing = db.query(UsageBasedBilling).filter(UsageBasedBilling.id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Usage billing not found")
    
    if current_user.role == "AGENT":
        customer = db.query(Customer).filter(Customer.id == billing.customer_id).first()
        if customer.agent_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    bills = db.query(UsageBill).filter(UsageBill.usage_billing_id == billing_id).offset(skip).limit(limit).all()
    return bills

@router.post("/bills/{bill_id}/payments", response_model=UsageBillPaymentSchema, status_code=status.HTTP_201_CREATED)
def record_usage_bill_payment(
    bill_id: int,
    payment_in: UsageBillPaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    bill = db.query(UsageBill).filter(UsageBill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    customer = db.query(Customer).filter(Customer.id == bill.customer_id).first()
    if current_user.role == "AGENT" and customer.agent_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Agents can only record payments for their customers"
        )
    
    db_payment = UsageBillPayment(
        **payment_in.dict(),
        recorded_by_id=current_user.id
    )
    
    bill.amount_paid = (bill.amount_paid or 0) + payment_in.amount_paid
    if bill.amount_paid >= bill.total_amount_to_collect:
        from app.models.usage import UsageBillingStatus
        bill.status = UsageBillingStatus.FULLY_PAID
    else:
        from app.models.usage import UsageBillingStatus
        bill.status = UsageBillingStatus.PARTIALLY_PAID
    
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/bills/{bill_id}", response_model=UsageBillWithPayments)
def read_usage_bill(
    bill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    bill = db.query(UsageBill).filter(UsageBill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    if current_user.role == "AGENT":
        customer = db.query(Customer).filter(Customer.id == bill.customer_id).first()
        if customer.agent_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return bill

@router.delete("/{billing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usage_billing(
    billing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    billing = db.query(UsageBasedBilling).filter(UsageBasedBilling.id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Usage billing not found")
    
    if current_user.role not in ["ADMIN", "SUPERADMIN"]:
        raise HTTPException(
            status_code=403,
            detail="Only admins can delete usage billing"
        )
    
    db.delete(billing)
    db.commit()
    return None
