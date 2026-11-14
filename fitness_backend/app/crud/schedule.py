from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from datetime import date, datetime

# Workout CRUD
def get_workout(db: Session, workout_id: int):
    return db.query(models.Workout).filter(models.Workout.id == workout_id).first()

def get_workouts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None
):
    query = db.query(models.Workout)
    
    if date_from:
        query = query.filter(models.Workout.workout_date >= date_from)
    if date_to:
        query = query.filter(models.Workout.workout_date <= date_to)
    
    return query.offset(skip).limit(limit).all()

def get_workouts_by_trainer(db: Session, trainer_id: int):
    return db.query(models.Workout).filter(models.Workout.trainer_id == trainer_id).all()

def get_workouts_by_room(db: Session, room_id: int):
    return db.query(models.Workout).filter(models.Workout.room_id == room_id).all()

def create_workout(db: Session, workout: schemas.WorkoutCreate):
    db_workout = models.Workout(**workout.dict())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

def update_workout(db: Session, workout_id: int, workout_update: schemas.WorkoutUpdate):
    db_workout = get_workout(db, workout_id)
    if not db_workout:
        return None
    
    update_data = workout_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_workout, field, value)
    
    db.commit()
    db.refresh(db_workout)
    return db_workout

def delete_workout(db: Session, workout_id: int):
    db_workout = get_workout(db, workout_id)
    if db_workout:
        db.delete(db_workout)
        db.commit()
    return db_workout

# Client Record CRUD
def create_client_record(db: Session, record: schemas.ClientRecordCreate, client_id: int):
    # Check if workout exists and has capacity
    workout = get_workout(db, record.workout_id)
    if not workout:
        raise ValueError("Workout not found")
    
    if workout.current_number_of_recorded >= workout.max_persons_capacity:
        raise ValueError("Workout is full")
    
    # Check if client is already registered
    existing_record = db.query(models.ClientRecord).filter(
        models.ClientRecord.workout_id == record.workout_id,
        models.ClientRecord.client_id == client_id
    ).first()
    
    if existing_record:
        raise ValueError("Client already registered for this workout")
    
    db_record = models.ClientRecord(
        **record.dict(),
        client_id=client_id
    )
    
    # Update workout count
    workout.current_number_of_recorded += 1
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_client_records(db: Session, client_id: int):
    return db.query(models.ClientRecord).filter(models.ClientRecord.client_id == client_id).all()

def get_workout_records(db: Session, workout_id: int):
    return db.query(models.ClientRecord).filter(models.ClientRecord.workout_id == workout_id).all()

def delete_client_record(db: Session, record_id: int, client_id: int):
    db_record = db.query(models.ClientRecord).filter(
        models.ClientRecord.id == record_id,
        models.ClientRecord.client_id == client_id
    ).first()
    
    if db_record:
        # Decrease workout count
        workout = get_workout(db, db_record.workout_id)
        if workout and workout.current_number_of_recorded > 0:
            workout.current_number_of_recorded -= 1
        
        db.delete(db_record)
        db.commit()
    
    return db_record