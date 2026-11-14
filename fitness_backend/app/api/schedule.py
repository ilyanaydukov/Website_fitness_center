from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from ..database import get_db
from ..auth.dependencies import get_current_active_user, get_current_client, get_current_employee
from ..crud.schedule import (
    get_workouts, get_workout, create_workout,
    update_workout, delete_workout,
    create_client_record, get_client_records, delete_client_record,
    get_workout_records
)
from ..crud.user import get_client_by_email
from ..schemas.schedule import (
    WorkoutInDB, WorkoutCreate, WorkoutUpdate,
    ClientRecordInDB, ClientRecordCreate
)

router = APIRouter(prefix="/api/v1/schedule", tags=["schedule"])

# Public endpoints
@router.get("/workouts", response_model=List[WorkoutInDB])
def read_workouts(
    skip: int = 0,
    limit: int = 100,
    date_from: date = None,
    date_to: date = None,
    db: Session = Depends(get_db)
):
    return get_workouts(db, skip=skip, limit=limit, date_from=date_from, date_to=date_to)

@router.get("/workouts/{workout_id}", response_model=WorkoutInDB)
def read_workout(
    workout_id: int,
    db: Session = Depends(get_db)
):
    workout = get_workout(db, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

# Client endpoints
@router.post("/workouts/{workout_id}/register", response_model=ClientRecordInDB)
def register_for_workout(
    workout_id: int,
    current_user = Depends(get_current_client),
    db: Session = Depends(get_db)
):
    # Get client
    client = get_client_by_email(db, email=current_user.email)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Check if workout exists
    workout = get_workout(db, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    # Create record
    record_data = ClientRecordCreate(
        workout_id=workout_id,
        record_date=date.today(),
        record_time=workout.start_time
    )
    
    try:
        record = create_client_record(db, record=record_data, client_id=client.id)
        return record
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my-registrations", response_model=List[ClientRecordInDB])
def get_my_registrations(
    current_user = Depends(get_current_client),
    db: Session = Depends(get_db)
):
    client = get_client_by_email(db, email=current_user.email)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return get_client_records(db, client_id=client.id)

@router.delete("/registrations/{record_id}")
def cancel_registration(
    record_id: int,
    current_user = Depends(get_current_client),
    db: Session = Depends(get_db)
):
    client = get_client_by_email(db, email=current_user.email)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    record = delete_client_record(db, record_id=record_id, client_id=client.id)
    if not record:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    return {"message": "Registration cancelled successfully"}

# Employee/Admin endpoints
@router.post("/workouts", response_model=WorkoutInDB)
def create_new_workout(
    workout: WorkoutCreate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    return create_workout(db, workout=workout)

@router.put("/workouts/{workout_id}", response_model=WorkoutInDB)
def update_existing_workout(
    workout_id: int,
    workout_update: WorkoutUpdate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    updated_workout = update_workout(db, workout_id=workout_id, workout_update=workout_update)
    if not updated_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return updated_workout

@router.delete("/workouts/{workout_id}")
def delete_existing_workout(
    workout_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    workout = delete_workout(db, workout_id=workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return {"message": "Workout deleted successfully"}

@router.get("/workouts/{workout_id}/registrations", response_model=List[ClientRecordInDB])
def get_workout_registrations(
    workout_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    return get_workout_records(db, workout_id=workout_id)