# app/crud/user.py
from sqlalchemy.orm import Session
from typing import Optional
from app import models
from ..models.user import User, Client, Employee, Position, TrainerSpecialization, Vacation, TypeOfVacation, SalaryStatement
from ..schemas import user as user_schemas
from ..auth.security import get_password_hash, verify_password
from datetime import date

# User CRUD
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: user_schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        is_employee=user.is_employee
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Client CRUD
def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()

def get_client_by_email(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email == email).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()

def create_client(db: Session, client: user_schemas.ClientCreate):
    # First create user
    user_data = user_schemas.UserCreate(
        email=client.email,
        password=client.password,
        is_employee=False
    )
    db_user = create_user(db, user_data)
    
    # Then create client
    db_client = models.Client(
        first_name=client.first_name,
        last_name=client.last_name,
        date_of_birth=client.date_of_birth,
        phone=client.phone,
        email=client.email,
        registration_date=date.today(),
        user_id=db_user.id
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, client_id: int, client_update: user_schemas.ClientUpdate):
    db_client = get_client(db, client_id)
    if not db_client:
        return None
    
    update_data = client_update.dict(exclude_unset=True)
    
    if "password" in update_data:
        # Update password in User model
        db_user = get_user_by_email(db, db_client.email)
        if db_user:
            db_user.hashed_password = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_client, field, value)
    
    db.commit()
    db.refresh(db_client)
    return db_client

# Employee CRUD
def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def get_employee_by_email(db: Session, email: str):
    return db.query(models.Employee).filter(models.Employee.email == email).first()

def create_employee(db: Session, employee: user_schemas.EmployeeCreate):
    # First create user
    user_data = user_schemas.UserCreate(
        email=employee.email,
        password=employee.password,
        is_employee=True
    )
    db_user = create_user(db, user_data)
    
    # Then create employee
    db_employee = models.Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        position_id=employee.position_id,
        phone=employee.phone,
        email=employee.email,
        date_of_employment=date.today(),
        fitness_center_id=employee.fitness_center_id,
        user_id=db_user.id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Position CRUD
def create_position(db: Session, position: user_schemas.PositionBase):
    db_position = models.Position(**position.dict())
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

def get_positions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Position).offset(skip).limit(limit).all()

# После существующих функций добавьте:

# Employee CRUD - дополнительные функции
def get_employees(db: Session, skip: int = 0, limit: int = 100):
    """Получить всех сотрудников"""
    return db.query(models.Employee).offset(skip).limit(limit).all()

def get_employee_by_user_id(db: Session, user_id: int):
    """Получить сотрудника по ID пользователя"""
    return db.query(models.Employee).filter(models.Employee.user_id == user_id).first()

def update_employee(db: Session, employee_id: int, employee_update: user_schemas.EmployeeUpdate):
    """Обновить данные сотрудника"""
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return None
    
    update_data = employee_update.dict(exclude_unset=True)
    
    # Обновить пароль если указан
    if "password" in update_data:
        db_user = get_user_by_email(db, db_employee.email)
        if db_user:
            db_user.hashed_password = get_password_hash(update_data.pop("password"))
    
    # Обновить email если указан
    if "email" in update_data:
        db_user = get_user_by_email(db, db_employee.email)
        if db_user:
            db_user.email = update_data["email"]
        db_employee.email = update_data["email"]
    
    for field, value in update_data.items():
        setattr(db_employee, field, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Position CRUD - дополнительные функции
def get_position(db: Session, position_id: int):
    """Получить должность по ID"""
    return db.query(models.Position).filter(models.Position.id == position_id).first()

def update_position(db: Session, position_id: int, position_update: user_schemas.PositionBase):
    """Обновить должность"""
    db_position = get_position(db, position_id)
    if not db_position:
        return None
    
    update_data = position_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_position, field, value)
    
    db.commit()
    db.refresh(db_position)
    return db_position

def delete_position(db: Session, position_id: int):
    """Удалить должность"""
    db_position = get_position(db, position_id)
    if db_position:
        db.delete(db_position)
        db.commit()
    return db_position

def delete_employee(db: Session, employee_id: int):
    """Удалить сотрудника"""
    db_employee = get_employee(db, employee_id)
    if db_employee:
        # Также удалить связанного пользователя
        db_user = get_user_by_email(db, db_employee.email)
        if db_user:
            db.delete(db_user)
        db.delete(db_employee)
        db.commit()
    return db_employee