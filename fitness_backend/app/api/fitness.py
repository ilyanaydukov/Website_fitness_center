from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from ..database import get_db
from ..auth.dependencies import get_current_active_user, get_current_client
from ..crud.fitness import (
    get_fitness_centers, get_fitness_center, get_room,
    get_rooms, get_rooms_by_fitness_center,
    get_services, get_service,
    get_all_trainers, get_trainer,
    create_feedback, get_feedbacks_for_trainer
)
from ..crud.user import get_client_by_email
from ..schemas.fitness import (
    FitnessCenterInDB, RoomInDB, ServiceInDB,
    TrainerInDB, FeedbackCreate, FeedbackInDB
)

router = APIRouter(prefix="/api/v1/fitness", tags=["fitness"])

# Public endpoints
@router.get("/centers", response_model=List[FitnessCenterInDB])
def read_fitness_centers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_fitness_centers(db, skip=skip, limit=limit)

@router.get("/centers/{fitness_center_id}", response_model=FitnessCenterInDB)
def read_fitness_center(
    fitness_center_id: int,
    db: Session = Depends(get_db)
):
    fitness_center = get_fitness_center(db, fitness_center_id)
    if not fitness_center:
        raise HTTPException(status_code=404, detail="Fitness center not found")
    return fitness_center

@router.get("/rooms", response_model=List[RoomInDB])
def read_rooms(
    skip: int = 0,
    limit: int = 100,
    fitness_center_id: int = None,
    db: Session = Depends(get_db)
):
    if fitness_center_id:
        return get_rooms_by_fitness_center(db, fitness_center_id)
    return get_rooms(db, skip=skip, limit=limit)

@router.get("/rooms/{room_id}", response_model=RoomInDB)
def read_room(
    room_id: int,
    db: Session = Depends(get_db)
):
    room = get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.get("/services", response_model=List[ServiceInDB])
def read_services(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_services(db, skip=skip, limit=limit)

@router.get("/services/{service_id}", response_model=ServiceInDB)
def read_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    service = get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.get("/trainers", response_model=List[TrainerInDB])
def read_trainers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    trainers = get_all_trainers(db, skip=skip, limit=limit)
    return trainers

@router.get("/trainers/{trainer_id}", response_model=TrainerInDB)
def read_trainer(
    trainer_id: int,
    db: Session = Depends(get_db)
):
    trainer = get_trainer(db, trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return trainer

@router.get("/trainers/{trainer_id}/feedbacks", response_model=List[FeedbackInDB])
def read_trainer_feedbacks(
    trainer_id: int,
    db: Session = Depends(get_db)
):
    return get_feedbacks_for_trainer(db, trainer_id)

# Client endpoints
@router.post("/trainers/{trainer_id}/feedbacks", response_model=FeedbackInDB)
def create_trainer_feedback(
    trainer_id: int,
    feedback: FeedbackCreate,
    current_user = Depends(get_current_client),
    db: Session = Depends(get_db)
):
    # Verify trainer exists
    trainer = get_trainer(db, trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    
    # Get client
    client = get_client_by_email(db, email=current_user.email)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Check if mark is valid
    if feedback.mark < 1 or feedback.mark > 5:
        raise HTTPException(status_code=400, detail="Mark must be between 1 and 5")
    
    return create_feedback(db, feedback=feedback, client_id=client.id)