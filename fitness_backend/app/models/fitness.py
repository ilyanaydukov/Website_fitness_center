from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, DECIMAL, Text
from sqlalchemy.orm import relationship
from ..database import Base

class FitnessCenter(Base):
    __tablename__ = "fitness_centers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250))
    working_hours = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    
    rooms = relationship("Room", back_populates="fitness_center")
    employees = relationship("Employee", back_populates="fitness_center")

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    fitness_center_id = Column(Integer, ForeignKey("fitness_centers.id"))
    name = Column(String(250), nullable=False)
    description = Column(Text)
    capacity = Column(Integer)
    photo_url = Column(String(300))
    
    fitness_center = relationship("FitnessCenter", back_populates="rooms")
    equipment = relationship("Equipment", back_populates="room")
    workouts = relationship("Workout", back_populates="room")

class EquipmentCategory(Base):
    __tablename__ = "equipment_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)

class Equipment(Base):
    __tablename__ = "equipment"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    name = Column(String(250), nullable=False)
    equipment_category_id = Column(Integer, ForeignKey("equipment_categories.id"))
    purchase_date = Column(Date)
    date_of_last_service = Column(Date)
    description_of_condition = Column(Text)
    
    room = relationship("Room", back_populates="equipment")
    category = relationship("EquipmentCategory")

class ServiceCategory(Base):
    __tablename__ = "service_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(250), nullable=False)
    category_description = Column(Text)

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    price = Column(DECIMAL(10, 2))
    description = Column(Text)
    duration = Column(Integer)  # in minutes
    
    workouts = relationship("Workout", back_populates="service")

class VarietyServiceCategory(Base):
    __tablename__ = "variety_service_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    service_category_id = Column(Integer, ForeignKey("service_categories.id"))
    service_id = Column(Integer, ForeignKey("services.id"))

class Feedback(Base):
    __tablename__ = "feedback_for_trainer"
    
    id = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    mark = Column(Integer)
    comment = Column(Text)
    feedback_date = Column(Date)
    
    trainer = relationship("Trainer", back_populates="feedbacks")
    client = relationship("Client", back_populates="feedbacks")

