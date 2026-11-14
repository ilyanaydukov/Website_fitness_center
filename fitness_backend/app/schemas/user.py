# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    is_employee: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    is_employee: Optional[bool] = False

class ClientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    email: EmailStr

class ClientCreate(ClientBase):
    password: str

class ClientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class ClientInDB(ClientBase):
    id: int
    registration_date: date
    
    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    position_id: int
    phone: Optional[str] = None
    email: EmailStr
    fitness_center_id: int

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeInDB(EmployeeBase):
    id: int
    date_of_employment: date
    
    class Config:
        from_attributes = True

class PositionBase(BaseModel):
    name: str
    salary: Optional[float] = None

class PositionInDB(PositionBase):
    id: int
    
    class Config:
        from_attributes = True

# Добавьте эти схемы после существующих:

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position_id: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    fitness_center_id: Optional[int] = None

class PositionUpdate(BaseModel):
    name: Optional[str] = None
    salary: Optional[float] = None