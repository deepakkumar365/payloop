from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShopBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    is_direct_payer: bool = False

class ShopCreate(ShopBase):
    customer_id: Optional[int] = None

class ShopUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    customer_id: Optional[int] = None
    is_active: Optional[bool] = None

class Shop(ShopBase):
    id: int
    customer_id: Optional[int]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
