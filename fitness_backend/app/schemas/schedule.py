# app/schemas/schedule.py
from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class WorkoutBase(BaseModel):
    room_id: int
    trainer_id: Optional[int] = None  # Сделайте опциональным временно
    service_id: int
    workout_date: date
    start_time: time
    end_time: time
    max_persons_capacity: int
    current_number_of_recorded: int = 0

class WorkoutCreate(WorkoutBase):
    pass

class WorkoutUpdate(BaseModel):
    room_id: Optional[int] = None
    trainer_id: Optional[int] = None
    service_id: Optional[int] = None
    workout_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    max_persons_capacity: Optional[int] = None

class WorkoutInDB(WorkoutBase):
    id: int
    
    class Config:
        from_attributes = True

class ClientRecordBase(BaseModel):
    workout_id: int
    record_date: date
    record_time: time

class ClientRecordCreate(ClientRecordBase):
    pass

class ClientRecordInDB(ClientRecordBase):
    id: int
    client_id: int
    
    class Config:
        from_attributes = True