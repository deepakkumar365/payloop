from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.models.shop import Shop
from app.models.customer import Customer
from app.schemas.shop import ShopCreate, Shop as ShopSchema, ShopUpdate

router = APIRouter()

@router.post("/", response_model=ShopSchema, status_code=status.HTTP_201_CREATED)
def create_shop(
    shop_in: ShopCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if shop_in.customer_id:
        customer = db.query(Customer).filter(Customer.id == shop_in.customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        if current_user.role == "agent" and customer.agent_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_shop = Shop(**shop_in.dict())
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop

@router.get("/", response_model=List[ShopSchema])
def list_shops(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role in ["admin", "superadmin"]:
        shops = db.query(Shop).offset(skip).limit(limit).all()
    else:
        shops = db.query(Shop).join(Customer).filter(
            Customer.agent_id == current_user.id
        ).offset(skip).limit(limit).all()
    return shops

@router.get("/{shop_id}", response_model=ShopSchema)
def read_shop(
    shop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    if current_user.role == "agent" and shop.customer:
        if shop.customer.agent_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return shop

@router.put("/{shop_id}", response_model=ShopSchema)
def update_shop(
    shop_id: int,
    shop_in: ShopUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    if current_user.role == "agent" and shop.customer:
        if shop.customer.agent_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = shop_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(shop, field, value)
    
    db.commit()
    db.refresh(shop)
    return shop

@router.delete("/{shop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shop(
    shop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    if current_user.role == "agent" and shop.customer:
        if shop.customer.agent_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(shop)
    db.commit()
    return None
