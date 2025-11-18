from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.models.loan import Loan, LoanPayment
from app.models.customer import Customer
from app.schemas.loan import Loan as LoanSchema, LoanCreate, LoanPayment as LoanPaymentSchema, LoanPaymentCreate, LoanWithPayments

router = APIRouter()

@router.post("/", response_model=LoanSchema, status_code=status.HTTP_201_CREATED)
def create_loan(
    loan_in: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    customer = db.query(Customer).filter(Customer.id == loan_in.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if current_user.role == "AGENT" and customer.agent_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Agents can only create loans for their customers"
        )
    
    db_loan = Loan(**loan_in.dict())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

@router.get("/", response_model=List[LoanSchema])
def list_loans(
    skip: int = 0,
    limit: int = 100,
    customer_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Loan)
    
    if current_user.role == "AGENT":
        query = query.join(Customer).filter(Customer.agent_id == current_user.id)
    
    if customer_id:
        query = query.filter(Loan.customer_id == customer_id)
    
    loans = query.offset(skip).limit(limit).all()
    return loans

@router.get("/{loan_id}", response_model=LoanWithPayments)
def read_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    if current_user.role == "AGENT":
        customer = db.query(Customer).filter(Customer.id == loan.customer_id).first()
        if customer.agent_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return loan

@router.post("/{loan_id}/payments", response_model=LoanPaymentSchema, status_code=status.HTTP_201_CREATED)
def record_loan_payment(
    loan_id: int,
    payment_in: LoanPaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    customer = db.query(Customer).filter(Customer.id == loan.customer_id).first()
    if current_user.role == "AGENT" and customer.agent_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Agents can only record payments for their customers"
        )
    
    db_payment = LoanPayment(
        **payment_in.dict(),
        recorded_by_id=current_user.id
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/{loan_id}/payments", response_model=List[LoanPaymentSchema])
def list_loan_payments(
    loan_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    if current_user.role == "AGENT":
        customer = db.query(Customer).filter(Customer.id == loan.customer_id).first()
        if customer.agent_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    payments = db.query(LoanPayment).filter(LoanPayment.loan_id == loan_id).offset(skip).limit(limit).all()
    return payments

@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    if current_user.role not in ["ADMIN", "SUPERADMIN"]:
        raise HTTPException(
            status_code=403,
            detail="Only admins can delete loans"
        )
    
    db.delete(loan)
    db.commit()
    return None
