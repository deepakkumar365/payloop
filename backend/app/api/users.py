from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.core.deps import get_current_admin, get_current_active_user, get_current_superadmin
from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, User as UserSchema, UserUpdate, ChangePasswordRequest

router = APIRouter()

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    if user_in.role == UserRole.ADMIN and current_user.role != UserRole.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superadmins can create admin users"
        )
    
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        role=user_in.role,
        created_by_id=current_user.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserSchema)
def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/admins/list", response_model=List[UserSchema])
def list_admins(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superadmin)
):
    admins = db.query(User).filter(User.role == UserRole.ADMIN).offset(skip).limit(limit).all()
    return admins

@router.get("/admins/{admin_id}", response_model=UserSchema)
def get_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superadmin)
):
    admin = db.query(User).filter(User.id == admin_id, User.role == UserRole.ADMIN).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

@router.get("/", response_model=List[UserSchema])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role in ["admin", "superadmin"]:
        users = db.query(User).offset(skip).limit(limit).all()
    else:
        users = db.query(User).filter(User.id == current_user.id).all()
    return users

@router.get("/{user_id}", response_model=UserSchema)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if current_user.role not in ["admin", "superadmin"] and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return user

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return None

@router.put("/admins/{admin_id}", response_model=UserSchema)
def update_admin(
    admin_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superadmin)
):
    admin = db.query(User).filter(User.id == admin_id, User.role == UserRole.ADMIN).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    if user_in.email and admin.email != user_in.email:
        existing_user = db.query(User).filter(User.email == user_in.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already in use")
    
    update_data = user_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(admin, field, value)
    
    db.commit()
    db.refresh(admin)
    return admin

@router.put("/admins/{admin_id}/password")
def change_admin_password(
    admin_id: int,
    password_change: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superadmin)
):
    admin = db.query(User).filter(User.id == admin_id, User.role == UserRole.ADMIN).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    admin.hashed_password = get_password_hash(password_change.new_password)
    db.commit()
    db.refresh(admin)
    return {"message": "Password changed successfully"}

@router.delete("/admins/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superadmin)
):
    if admin_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own admin account"
        )
    
    admin = db.query(User).filter(User.id == admin_id, User.role == UserRole.ADMIN).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    db.delete(admin)
    db.commit()
    return None
