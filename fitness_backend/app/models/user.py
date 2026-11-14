from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, Text
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_employee = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    phone = Column(String(20))
    email = Column(String(100), unique=True, index=True, nullable=False)
    registration_date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User")
    # Просто указываем имя класса - SQLAlchemy найдет его в реестре
    subscriptions = relationship("ClientSubscription", back_populates="client")
    records = relationship("ClientRecord", back_populates="client")
    feedbacks = relationship("Feedback", back_populates="client")

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    position_id = Column(Integer, ForeignKey("positions.id"))
    phone = Column(String(20))
    email = Column(String(100), unique=True, index=True, nullable=False)
    date_of_employment = Column(Date)
    fitness_center_id = Column(Integer, ForeignKey("fitness_centers.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User")
    position = relationship("Position")
    fitness_center = relationship("FitnessCenter")
    vacations = relationship("Vacation", back_populates="employee")
    salary_statements = relationship("SalaryStatement", back_populates="employee")
    trainer_profile = relationship("Trainer", uselist=False, back_populates="employee")

class Position(Base):
    __tablename__ = "positions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    salary = Column(DECIMAL(10, 2))

class Trainer(Base):
    __tablename__ = "trainers"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    specialization_id = Column(Integer, ForeignKey("trainer_specializations.id"))
    work_experience = Column(Integer, default=0)
    
    # Отношения
    employee = relationship("Employee", back_populates="trainer_profile")
    specialization = relationship("TrainerSpecialization", back_populates="trainers")
    workouts = relationship("Workout", back_populates="trainer")
    feedbacks = relationship("Feedback", back_populates="trainer")

class TrainerSpecialization(Base):
    __tablename__ = "trainer_specializations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    description = Column(String)

    trainers = relationship("Trainer", back_populates="specialization")

class Vacation(Base):
    __tablename__ = "vacations"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    type_of_vacation_id = Column(Integer, ForeignKey("type_of_vacations.id"))
    
    employee = relationship("Employee", back_populates="vacations")
    type_of_vacation = relationship("TypeOfVacation")

class TypeOfVacation(Base):
    __tablename__ = "type_of_vacations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    duration = Column(Integer)
    past = Column(Boolean, default=False)

class SalaryStatement(Base):
    __tablename__ = "salary_statements"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    month_period = Column(String(100))
    year_period = Column(Integer)
    salary = Column(DECIMAL(10, 2))
    bonus = Column(DECIMAL(10, 2))
    penalty = Column(DECIMAL(10, 2))
    total_amount = Column(DECIMAL(10, 2))
    date_of_payment = Column(Date)
    
    employee = relationship("Employee", back_populates="salary_statements")