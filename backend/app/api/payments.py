from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.models.payment import Payment
from app.models.customer import Customer
from app.schemas.payment import PaymentCreate, Payment as PaymentSchema

router = APIRouter()

@router.post("/", response_model=PaymentSchema, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment_in: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    customer = db.query(Customer).filter(Customer.id == payment_in.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if current_user.role == "agent" and customer.agent_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Agents can only collect payments for their customers"
        )
    
    db_payment = Payment(
        **payment_in.dict(),
        collected_by_id=current_user.id
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/", response_model=List[PaymentSchema])
def list_payments(
    skip: int = 0,
    limit: int = 100,
    customer_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Payment)
    
    if current_user.role == "agent":
        query = query.join(Customer).filter(Customer.agent_id == current_user.id)
    
    if customer_id:
        query = query.filter(Payment.customer_id == customer_id)
    
    payments = query.order_by(Payment.payment_date.desc()).offset(skip).limit(limit).all()
    return payments

@router.get("/{payment_id}", response_model=PaymentSchema)
def read_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    if current_user.role == "agent":
        customer = db.query(Customer).filter(Customer.id == payment.customer_id).first()
        if customer.agent_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return payment

@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    if current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(
            status_code=403,
            detail="Only admins can delete payments"
        )
    
    db.delete(payment)
    db.commit()
    return None
