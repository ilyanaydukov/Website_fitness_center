from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, time

# User schemas for fitness module
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_employee: bool = False

# Fitness Center schemas
class FitnessCenterBase(BaseModel):
    name: str
    address: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    working_hours: Optional[str] = None

class FitnessCenterCreate(FitnessCenterBase):
    pass

class FitnessCenterUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    working_hours: Optional[str] = None

class FitnessCenterInDB(FitnessCenterBase):
    id: int
    
    class Config:
        from_attributes = True

# Room schemas
class RoomBase(BaseModel):
    name: str
    capacity: int
    fitness_center_id: int
    room_type: Optional[str] = None

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None
    fitness_center_id: Optional[int] = None
    room_type: Optional[str] = None

class RoomInDB(RoomBase):
    id: int
    fitness_center: Optional[FitnessCenterInDB] = None
    
    class Config:
        from_attributes = True

# Equipment schemas
class EquipmentBase(BaseModel):
    name: str
    equipment_type: str
    room_id: int
    purchase_date: Optional[date] = None
    last_maintenance_date: Optional[date] = None
    status: Optional[str] = "active"

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    equipment_type: Optional[str] = None
    room_id: Optional[int] = None
    purchase_date: Optional[date] = None
    last_maintenance_date: Optional[date] = None
    status: Optional[str] = None

class EquipmentInDB(EquipmentBase):
    id: int
    room: Optional[RoomInDB] = None
    
    class Config:
        from_attributes = True

# Equipment Category schemas
class EquipmentCategoryBase(BaseModel):
    category_name: str
    description: Optional[str] = None

class EquipmentCategoryCreate(EquipmentCategoryBase):
    pass

class EquipmentCategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    description: Optional[str] = None

class EquipmentCategoryInDB(EquipmentCategoryBase):
    id: int
    
    class Config:
        from_attributes = True

# Service Category schemas
class ServiceCategoryBase(BaseModel):
    category_name: str
    description: Optional[str] = None

class ServiceCategoryCreate(ServiceCategoryBase):
    pass

class ServiceCategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    description: Optional[str] = None

class ServiceCategoryInDB(ServiceCategoryBase):
    id: int
    
    class Config:
        from_attributes = True

# Service schemas
class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = 0.0
    duration: Optional[int] = 60  # in minutes

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[int] = None

class ServiceInDB(ServiceBase):
    id: int
    
    class Config:
        from_attributes = True

# Trainer schemas
class TrainerBase(BaseModel):
    first_name: str
    last_name: str
    specialization_id: Optional[int] = None
    work_experience: Optional[int] = 0

class TrainerCreate(BaseModel):
    # Основные поля из Employee
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    position_id: int  # ID позиции "Тренер"
    fitness_center_id: Optional[int] = None
    
    # Специфичные поля тренера
    specialization_id: Optional[int] = None
    work_experience: Optional[int] = 0

class TrainerUpdate(BaseModel):
    # Можно обновлять как поля сотрудника, так и специфичные поля тренера
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    position_id: Optional[int] = None
    fitness_center_id: Optional[int] = None
    specialization_id: Optional[int] = None
    work_experience: Optional[int] = None


# Feedback schemas
class FeedbackBase(BaseModel):
    trainer_id: int
    mark: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackInDB(FeedbackBase):
    id: int
    client_id: int
    feedback_date: date
    client: Optional[dict] = None
    
    class Config:
        from_attributes = True

# Specialization schemas
class SpecializationBase(BaseModel):
    name: str
    description: Optional[str] = None

class SpecializationCreate(SpecializationBase):
    pass

class SpecializationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class SpecializationInDB(SpecializationBase):
    id: int
    
    class Config:
        from_attributes = True

# Trainer Specialization schemas (добавляем недостающую схему)
class TrainerSpecializationBase(BaseModel):
    name: str
    description: Optional[str] = None

class TrainerSpecializationCreate(TrainerSpecializationBase):
    pass

class TrainerSpecializationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TrainerSpecializationInDB(TrainerSpecializationBase):
    id: int
    
    class Config:
        from_attributes = True

# Service Schedule schemas
class ServiceScheduleBase(BaseModel):
    service_id: int
    trainer_id: int
    room_id: int
    schedule_date: date
    start_time: time
    end_time: time
    max_capacity: int
    current_enrollment: int = 0

class ServiceScheduleCreate(ServiceScheduleBase):
    pass

class ServiceScheduleUpdate(BaseModel):
    service_id: Optional[int] = None
    trainer_id: Optional[int] = None
    room_id: Optional[int] = None
    schedule_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    max_capacity: Optional[int] = None
    current_enrollment: Optional[int] = None

class ServiceScheduleInDB(ServiceScheduleBase):
    id: int
    service: Optional[dict] = None
    trainer: Optional[dict] = None
    room: Optional[dict] = None
    
    class Config:
        from_attributes = True

# Maintenance schemas
class MaintenanceBase(BaseModel):
    equipment_id: int
    maintenance_date: date
    maintenance_type: str
    description: Optional[str] = None
    cost: Optional[float] = None
    technician: Optional[str] = None

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceUpdate(BaseModel):
    equipment_id: Optional[int] = None
    maintenance_date: Optional[date] = None
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    technician: Optional[str] = None

class MaintenanceInDB(MaintenanceBase):
    id: int
    equipment: Optional[dict] = None
    
    class Config:
        from_attributes = True

class TrainerInDB(BaseModel):
    id: int
    employee_id: int
    first_name: Optional[str] = None  # Получаем из Employee
    last_name: Optional[str] = None   # Получаем из Employee
    email: Optional[EmailStr] = None  # Получаем из User через Employee
    phone: Optional[str] = None       # Получаем из Employee
    position_id: Optional[int] = None # Получаем из Employee
    fitness_center_id: Optional[int] = None  # Получаем из Employee
    specialization_id: Optional[int] = None
    work_experience: Optional[int] = None
    date_of_employment: Optional[date] = None  # Получаем из Employee
    specialization: Optional[SpecializationInDB] = None
    
    class Config:
        from_attributes = True