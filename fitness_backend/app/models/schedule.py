from sqlalchemy import Column, Integer, Date, Time, ForeignKey, DECIMAL, Text
from sqlalchemy.orm import relationship
from ..database import Base

class Workout(Base):
    __tablename__ = "workout_schedule"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    workout_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    max_persons_capacity = Column(Integer)
    current_number_of_recorded = Column(Integer, default=0)
    
    room = relationship("Room", back_populates="workouts")
    trainer = relationship("Trainer", back_populates="workouts")
    service = relationship("Service", back_populates="workouts")
    records = relationship("ClientRecord", back_populates="workout")

class ClientRecord(Base):
    __tablename__ = "client_record_on_workout"
    
    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workout_schedule.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    record_date = Column(Date)
    record_time = Column(Time)
    
    workout = relationship("Workout", back_populates="records")
    client = relationship("Client", back_populates="records")