from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.models.subscription import Subscription, Bill, BillPayment
from app.models.customer import Customer
from app.schemas.subscription import (
    Subscription as SubscriptionSchema, SubscriptionCreate,
    Bill as BillSchema, BillCreate,
    BillPayment as BillPaymentSchema, BillPaymentCreate,
    SubscriptionWithBills, BillWithPayments
)

router = APIRouter()

@router.post("/", response_model=SubscriptionSchema, status_code=status.HTTP_201_CREATED)
def create_subscription(
    subscription_in: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    customer = db.query(Customer).filter(Customer.id == subscription_in.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if current_user.role == "AGENT" and customer.agent_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Agents can only create subscriptions for their customers"
        )
    
    db_subscription = Subscription(**subscription_in.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@router.get("/", response_model=List[SubscriptionSchema])
def list_subscriptions(
    skip: int = 0,
    limit: int = 100,
    customer_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Subscription)
    
    if current_user.role == "AGENT":
        query = query.join(Customer).filter(Customer.agent_id == current_user.id)
    
    if customer_id:
        query = query.filter(Subscription.customer_id == customer_id)
    
    subscriptions = query.offset(skip).limit(limit).all()
    return subscriptions

@router.get("/{subscription_id}", response_model=SubscriptionWithBills)
def read_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    if current_user.role == "AGENT":
        customer = db.query(Customer).filter(Customer.id == subscription.customer_id).first()
        if customer.agent_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return subscription

@router.post("/{subscription_id}/bills", response_model=BillSchema, status_code=status.HTTP_201_CREATED)
def create_bill(
    subscription_id: int,
    bill_in: BillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    if current_user.role not in ["ADMIN", "SUPERADMIN"]:
        raise HTTPException(
            status_code=403,
            detail="Only admins can create bills"
        )
    
    existing_bill = db.query(Bill).filter(Bill.bill_number == bill_in.bill_number).first()
    if existing_bill:
        raise HTTPException(
            status_code=400,
            detail="Bill number already exists"
        )
    
    db_bill = Bill(**bill_in.dict())
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill

@router.get("/{subscription_id}/bills", response_model=List[BillSchema])
def list_bills(
    subscription_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    if current_user.role == "AGENT":
        customer = db.query(Customer).filter(Customer.id == subscription.customer_id).first()
        if customer.agent_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    bills = db.query(Bill).filter(Bill.subscription_id == subscription_id).offset(skip).limit(limit).all()
    return bills

@router.post("/bills/{bill_id}/payments", response_model=BillPaymentSchema, status_code=status.HTTP_201_CREATED)
def record_bill_payment(
    bill_id: int,
    payment_in: BillPaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    customer = db.query(Customer).filter(Customer.id == bill.customer_id).first()
    if current_user.role == "AGENT" and customer.agent_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Agents can only record payments for their customers"
        )
    
    db_payment = BillPayment(
        **payment_in.dict(),
        recorded_by_id=current_user.id
    )
    
    bill.amount_paid = (bill.amount_paid or 0) + payment_in.amount_paid
    if bill.amount_paid >= bill.total_amount_to_collect:
        from app.models.subscription import BillStatus
        bill.status = BillStatus.FULLY_PAID
    else:
        from app.models.subscription import BillStatus
        bill.status = BillStatus.PARTIALLY_PAID
    
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/bills/{bill_id}", response_model=BillWithPayments)
def read_bill(
    bill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    if current_user.role == "AGENT":
        customer = db.query(Customer).filter(Customer.id == bill.customer_id).first()
        if customer.agent_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return bill

@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    if current_user.role not in ["ADMIN", "SUPERADMIN"]:
        raise HTTPException(
            status_code=403,
            detail="Only admins can delete subscriptions"
        )
    
    db.delete(subscription)
    db.commit()
    return None
