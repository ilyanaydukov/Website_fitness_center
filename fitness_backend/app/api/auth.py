from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Any

from ..database import get_db
from ..crud.user import get_user_by_email, create_client, create_employee
from ..auth.security import verify_password, create_access_token
from ..auth.dependencies import get_current_user
from ..schemas.user import (
    UserCreate, Token, ClientCreate, EmployeeCreate,
    ClientInDB, EmployeeInDB
)
from ..core.config import settings

router = APIRouter(prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])

@router.post("/register/client", response_model=ClientInDB)
def register_client(
    client: ClientCreate,
    db: Session = Depends(get_db)
):
    # Check if user exists
    db_client = get_user_by_email(db, email=client.email)
    if db_client:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    return create_client(db=db, client=client)

@router.post("/register/employee", response_model=EmployeeInDB)
def register_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    # In production, this should be protected or done by admin only
    db_employee = get_user_by_email(db, email=employee.email)
    if db_employee:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    return create_employee(db=db, employee=employee)

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "is_employee": user.is_employee},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(current_user = Depends(get_current_user)):
    return current_user