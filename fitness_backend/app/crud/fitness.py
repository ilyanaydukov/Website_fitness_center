from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func 
from typing import List, Optional
from .. import models
from ..schemas import fitness as fitness_schemas
from ..auth.security import get_password_hash
from ..crud.user import get_user_by_email, create_user, create_employee, update_employee, delete_employee, get_employee, get_user_by_email
from datetime import date
from ..schemas import user as user_schemas

# Fitness Center CRUD
def get_fitness_center(db: Session, fitness_center_id: int):
    return db.query(models.FitnessCenter).filter(models.FitnessCenter.id == fitness_center_id).first()

def get_fitness_centers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FitnessCenter).offset(skip).limit(limit).all()

def create_fitness_center(db: Session, fitness_center: fitness_schemas.FitnessCenterCreate):
    db_fitness_center = models.FitnessCenter(**fitness_center.dict())
    db.add(db_fitness_center)
    db.commit()
    db.refresh(db_fitness_center)
    return db_fitness_center

def update_fitness_center(db: Session, fitness_center_id: int, fitness_center_update: fitness_schemas.FitnessCenterUpdate):
    db_fitness_center = get_fitness_center(db, fitness_center_id)
    if not db_fitness_center:
        return None
    
    update_data = fitness_center_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_fitness_center, field, value)
    
    db.commit()
    db.refresh(db_fitness_center)
    return db_fitness_center

def delete_fitness_center(db: Session, fitness_center_id: int):
    db_fitness_center = get_fitness_center(db, fitness_center_id)
    if db_fitness_center:
        db.delete(db_fitness_center)
        db.commit()
    return db_fitness_center

# Room CRUD
def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()

def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()

def get_rooms_by_fitness_center(db: Session, fitness_center_id: int):
    return db.query(models.Room).filter(models.Room.fitness_center_id == fitness_center_id).all()

def create_room(db: Session, room: fitness_schemas.RoomCreate):
    db_room = models.Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room(db: Session, room_id: int, room_update: fitness_schemas.RoomUpdate):
    db_room = get_room(db, room_id)
    if not db_room:
        return None
    
    update_data = room_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_room, field, value)
    
    db.commit()
    db.refresh(db_room)
    return db_room

def delete_room(db: Session, room_id: int):
    db_room = get_room(db, room_id)
    if db_room:
        db.delete(db_room)
        db.commit()
    return db_room

# Equipment CRUD
def get_equipment(db: Session, equipment_id: int):
    return db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()

def get_equipment_by_room(db: Session, room_id: int):
    return db.query(models.Equipment).filter(models.Equipment.room_id == room_id).all()

def get_all_equipment(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Equipment).offset(skip).limit(limit).all()

def create_equipment(db: Session, equipment: fitness_schemas.EquipmentCreate):
    db_equipment = models.Equipment(**equipment.dict())
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

def update_equipment(db: Session, equipment_id: int, equipment_update: fitness_schemas.EquipmentUpdate):
    db_equipment = get_equipment(db, equipment_id)
    if not db_equipment:
        return None
    
    update_data = equipment_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_equipment, field, value)
    
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

def delete_equipment(db: Session, equipment_id: int):
    db_equipment = get_equipment(db, equipment_id)
    if db_equipment:
        db.delete(db_equipment)
        db.commit()
    return db_equipment

# Service CRUD
def get_service(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def get_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Service).offset(skip).limit(limit).all()

def create_service(db: Session, service: fitness_schemas.ServiceCreate):
    db_service = models.Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def update_service(db: Session, service_id: int, service_update: fitness_schemas.ServiceUpdate):
    db_service = get_service(db, service_id)
    if not db_service:
        return None
    
    update_data = service_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_service, field, value)
    
    db.commit()
    db.refresh(db_service)
    return db_service

def delete_service(db: Session, service_id: int):
    db_service = get_service(db, service_id)
    if db_service:
        db.delete(db_service)
        db.commit()
    return db_service

# Feedback CRUD
def create_feedback(db: Session, feedback: fitness_schemas.FeedbackCreate, client_id: int):
    db_feedback = models.Feedback(
        **feedback.dict(),
        client_id=client_id,
        feedback_date=date.today()
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_feedbacks_for_trainer(db: Session, trainer_id: int):
    return db.query(models.Feedback).filter(models.Feedback.trainer_id == trainer_id).all()


# ==================== Тренер CRUD (с наследованием от Employee) ====================

def create_trainer(db: Session, trainer: fitness_schemas.TrainerCreate):
    """
    Создать тренера (сначала создается Employee, затем Trainer)
    """
    # 1. Проверяем, не существует ли уже сотрудник с таким email
    existing_user = get_user_by_email(db, email=trainer.email)
    if existing_user:
        raise ValueError(f"Пользователь с email {trainer.email} уже существует")
    
    # 2. Создаем сотрудника
    employee_data = user_schemas.EmployeeCreate(
        first_name=trainer.first_name,
        last_name=trainer.last_name,
        email=trainer.email,
        password=trainer.password,
        position_id=trainer.position_id,
        phone=trainer.phone,
        fitness_center_id=trainer.fitness_center_id
    )
    
    try:
        db_employee = create_employee(db, employee_data)
    except Exception as e:
        raise ValueError(f"Ошибка при создании сотрудника: {str(e)}")
    
    # 3. Создаем профиль тренера
    trainer_data = trainer.dict(exclude={'email', 'password', 'first_name', 'last_name', 
                                         'phone', 'position_id', 'fitness_center_id'})
    
    db_trainer = models.Trainer(
        **trainer_data,
        employee_id=db_employee.id
    )
    
    try:
        db.add(db_trainer)
        db.commit()
        db.refresh(db_trainer)
        
        # Получаем полные данные для ответа
        trainer_response = get_trainer_full_info(db, db_trainer.id)
        return trainer_response
        
    except Exception as e:
        db.rollback()
        # Если не удалось создать тренера, удаляем сотрудника
        delete_employee(db, db_employee.id)
        raise ValueError(f"Ошибка при создании профиля тренера: {str(e)}")

def get_trainer(db: Session, trainer_id: int):
    """
    Получить тренера по ID
    """
    return db.query(models.Trainer).filter(models.Trainer.id == trainer_id).first()


def get_trainer_by_employee_id(db: Session, employee_id: int):
    """
    Получить тренера по ID сотрудника
    """
    return db.query(models.Trainer).filter(models.Trainer.employee_id == employee_id).first()


def get_trainer_with_details(db: Session, trainer_id: int):
    """
    Получить тренера со всеми деталями (Employee + User + связи)
    """
    trainer = db.query(models.Trainer)\
        .options(
            joinedload(models.Trainer.employee)
            .joinedload(models.Employee.user),
            joinedload(models.Trainer.employee)
            .joinedload(models.Employee.position),
            joinedload(models.Trainer.employee)
            .joinedload(models.Employee.fitness_center),
            joinedload(models.Trainer.specialization),
            joinedload(models.Trainer.workouts),
            joinedload(models.Trainer.feedbacks)
        )\
        .filter(models.Trainer.id == trainer_id)\
        .first()
    
    if not trainer:
        return None
    
    return trainer


def get_trainer_full_info(db: Session, trainer_id: int):
    """
    Получить тренера в структурированном виде для API
    """
    trainer = get_trainer_with_details(db, trainer_id)
    if not trainer:
        return None
    
    # Формируем структурированные данные
    trainer_data = {
        "id": trainer.id,
        "employee_id": trainer.employee_id,
        "first_name": trainer.employee.first_name,
        "last_name": trainer.employee.last_name,
        "email": trainer.employee.user.email if trainer.employee.user else None,
        "phone": trainer.employee.phone,
        "position_id": trainer.employee.position_id,
        "position": {
            "id": trainer.employee.position.id,
            "name": trainer.employee.position.name,
            "salary": float(trainer.employee.position.salary) if trainer.employee.position.salary else None
        } if trainer.employee.position else None,
        "fitness_center_id": trainer.employee.fitness_center_id,
        "fitness_center": {
            "id": trainer.employee.fitness_center.id,
            "name": trainer.employee.fitness_center.name,
            "address": trainer.employee.fitness_center.address
        } if trainer.employee.fitness_center else None,
        "specialization_id": trainer.specialization_id,
        "specialization": {
            "id": trainer.specialization.id,
            "name": trainer.specialization.name,
            "description": trainer.specialization.description
        } if trainer.specialization else None,
        "work_experience": trainer.work_experience,
        "date_of_employment": trainer.employee.date_of_employment,
        "workouts": [
            {
                "id": workout.id,
                "workout_date": workout.workout_date,
                "start_time": workout.start_time,
                "end_time": workout.end_time,
                "service_id": workout.service_id,
                "room_id": workout.room_id
            } for workout in trainer.workouts
        ] if trainer.workouts else [],
        "feedbacks": [
            {
                "id": feedback.id,
                "mark": feedback.mark,
                "comment": feedback.comment,
                "feedback_date": feedback.feedback_date,
                "client_id": feedback.client_id
            } for feedback in trainer.feedbacks
        ] if trainer.feedbacks else [],
        "average_rating": sum(f.mark for f in trainer.feedbacks) / len(trainer.feedbacks) if trainer.feedbacks else 0,
        "total_workouts": len(trainer.workouts),
        "total_feedbacks": len(trainer.feedbacks)
    }
    
    return trainer_data


def get_all_trainers(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить всех тренеров (базовая информация)
    """
    return db.query(models.Trainer)\
        .offset(skip)\
        .limit(limit)\
        .all()


def get_all_trainers_with_details(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить всех тренеров с деталями сотрудника
    """
    results = db.query(
        models.Trainer,
        models.Employee,
        models.User.email,
        models.Position.name.label('position_name'),
        models.Position.salary.label('position_salary'),
        models.FitnessCenter.name.label('fitness_center_name'),
        models.FitnessCenter.address.label('fitness_center_address'),
        models.TrainerSpecialization.name.label('specialization_name')
    )\
        .join(models.Employee, models.Trainer.employee_id == models.Employee.id)\
        .join(models.User, models.Employee.user_id == models.User.id)\
        .outerjoin(models.Position, models.Employee.position_id == models.Position.id)\
        .outerjoin(models.FitnessCenter, models.Employee.fitness_center_id == models.FitnessCenter.id)\
        .outerjoin(models.TrainerSpecialization, models.Trainer.specialization_id == models.TrainerSpecialization.id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    trainers_list = []
    for trainer, employee, email, position_name, position_salary, fc_name, fc_address, spec_name in results:
        # Получаем статистику
        workouts_count = db.query(models.Workout)\
            .filter(models.Workout.trainer_id == trainer.id)\
            .count()
        
        feedbacks_count = db.query(models.Feedback)\
            .filter(models.Feedback.trainer_id == trainer.id)\
            .count()
        
        avg_rating_result = db.query(
            func.avg(models.Feedback.mark).label('average_rating')
        )\
            .filter(models.Feedback.trainer_id == trainer.id)\
            .first()
        
        avg_rating = float(avg_rating_result[0]) if avg_rating_result[0] else 0
        
        trainers_list.append({
            "id": trainer.id,
            "employee_id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "email": email,
            "phone": employee.phone,
            "position_id": employee.position_id,
            "position_name": position_name,
            "position_salary": float(position_salary) if position_salary else None,
            "fitness_center_id": employee.fitness_center_id,
            "fitness_center_name": fc_name,
            "fitness_center_address": fc_address,
            "specialization_id": trainer.specialization_id,
            "specialization_name": spec_name,
            "work_experience": trainer.work_experience,
            "date_of_employment": employee.date_of_employment,
            "workouts_count": workouts_count,
            "feedbacks_count": feedbacks_count,
            "average_rating": avg_rating
        })
    
    return trainers_list


def update_trainer(db: Session, trainer_id: int, trainer_update: fitness_schemas.TrainerUpdate):
    """
    Обновить тренера (обновляем и Employee и Trainer)
    """
    db_trainer = get_trainer(db, trainer_id)
    if not db_trainer:
        return None
    
    # Получаем связанного сотрудника
    db_employee = get_employee(db, db_trainer.employee_id)
    if not db_employee:
        return None
    
    update_data = trainer_update.dict(exclude_unset=True)
    
    # Разделяем поля для обновления
    employee_update_fields = {}
    trainer_update_fields = {}
    
    # Определяем, какие поля принадлежат Employee
    employee_fields = ['first_name', 'last_name', 'email', 'password', 
                       'phone', 'position_id', 'fitness_center_id']
    
    for field, value in update_data.items():
        if field in employee_fields:
            employee_update_fields[field] = value
        else:
            trainer_update_fields[field] = value
    
    # Обновляем сотрудника
    if employee_update_fields:
        from ..schemas.user import EmployeeUpdate
        employee_update_schema = EmployeeUpdate(**employee_update_fields)
        updated_employee = update_employee(db, db_employee.id, employee_update_schema)
        if not updated_employee:
            return None
    
    # Обновляем тренера
    if trainer_update_fields:
        for field, value in trainer_update_fields.items():
            setattr(db_trainer, field, value)
    
    try:
        db.commit()
        db.refresh(db_trainer)
        return db_trainer
    except Exception as e:
        db.rollback()
        raise ValueError(f"Ошибка при обновлении тренера: {str(e)}")


def delete_trainer(db: Session, trainer_id: int, delete_employee_also: bool = False):
    """
    Удалить тренера
    Если delete_employee_also=True, то удалит и связанного сотрудника
    Если False, то только профиль тренера (сотрудник останется)
    """
    db_trainer = get_trainer(db, trainer_id)
    if not db_trainer:
        return None
    
    employee_id = db_trainer.employee_id
    
    try:
        # Удаляем тренера
        db.delete(db_trainer)
        
        # Если нужно удалить и сотрудника
        if delete_employee_also:
            delete_employee(db, employee_id)
        
        db.commit()
        return db_trainer
    except Exception as e:
        db.rollback()
        raise ValueError(f"Ошибка при удалении тренера: {str(e)}")


def get_trainers_by_fitness_center(db: Session, fitness_center_id: int):
    """
    Получить тренеров по фитнес-центру
    """
    results = db.query(models.Trainer)\
        .join(models.Employee, models.Trainer.employee_id == models.Employee.id)\
        .filter(models.Employee.fitness_center_id == fitness_center_id)\
        .all()
    
    return results


def get_trainers_by_specialization(db: Session, specialization_id: int):
    """
    Получить тренеров по специализации
    """
    return db.query(models.Trainer)\
        .filter(models.Trainer.specialization_id == specialization_id)\
        .all()


def get_trainer_statistics(db: Session, trainer_id: int):
    """
    Получить статистику тренера
    """
    trainer = get_trainer(db, trainer_id)
    if not trainer:
        return None
    
    # Статистика по тренировкам
    workouts_stats = db.query(
        func.count(models.Workout.id).label('total_workouts'),
        func.min(models.Workout.workout_date).label('first_workout'),
        func.max(models.Workout.workout_date).label('last_workout'),
        func.avg(
            func.extract('epoch', models.Workout.end_time) - 
            func.extract('epoch', models.Workout.start_time)
        ).label('avg_duration_minutes')
    )\
        .filter(models.Workout.trainer_id == trainer_id)\
        .first()
    
    # Статистика по отзывам
    feedbacks_stats = db.query(
        func.count(models.Feedback.id).label('total_feedbacks'),
        func.avg(models.Feedback.mark).label('average_rating'),
        func.min(models.Feedback.feedback_date).label('first_feedback'),
        func.max(models.Feedback.feedback_date).label('last_feedback')
    )\
        .filter(models.Feedback.trainer_id == trainer_id)\
        .first()
    
    # Статистика по записям клиентов
    registrations_stats = db.query(
        func.count(models.ClientRecord.id).label('total_registrations'),
        func.avg(
            models.Workout.current_number_of_recorded / models.Workout.max_persons_capacity * 100
        ).label('avg_occupancy_percent')
    )\
        .join(models.Workout, models.ClientRecord.workout_id == models.Workout.id)\
        .filter(models.Workout.trainer_id == trainer_id)\
        .first()
    
    return {
        "trainer_id": trainer_id,
        "workouts": {
            "total": workouts_stats.total_workouts or 0,
            "first_workout": workouts_stats.first_workout,
            "last_workout": workouts_stats.last_workout,
            "avg_duration_minutes": round(float(workouts_stats.avg_duration_minutes or 0) / 60, 2)
        },
        "feedbacks": {
            "total": feedbacks_stats.total_feedbacks or 0,
            "average_rating": round(float(feedbacks_stats.average_rating or 0), 2),
            "first_feedback": feedbacks_stats.first_feedback,
            "last_feedback": feedbacks_stats.last_feedback
        },
        "registrations": {
            "total": registrations_stats.total_registrations or 0,
            "avg_occupancy_percent": round(float(registrations_stats.avg_occupancy_percent or 0), 2)
        }
    }


def search_trainers(db: Session, 
                    name: Optional[str] = None,
                    specialization_id: Optional[int] = None,
                    fitness_center_id: Optional[int] = None,
                    min_experience: Optional[int] = None,
                    min_rating: Optional[float] = None,
                    skip: int = 0, 
                    limit: int = 100):
    """
    Поиск тренеров по критериям
    """
    query = db.query(models.Trainer)\
        .join(models.Employee, models.Trainer.employee_id == models.Employee.id)\
        .outerjoin(models.Feedback, models.Feedback.trainer_id == models.Trainer.id)
    
    # Применяем фильтры
    if name:
        query = query.filter(
            models.Employee.first_name.ilike(f"%{name}%") | 
            models.Employee.last_name.ilike(f"%{name}%")
        )
    
    if specialization_id:
        query = query.filter(models.Trainer.specialization_id == specialization_id)
    
    if fitness_center_id:
        query = query.filter(models.Employee.fitness_center_id == fitness_center_id)
    
    if min_experience:
        query = query.filter(models.Trainer.work_experience >= min_experience)
    
    # Для фильтра по рейтингу нужна группировка
    if min_rating:
        query = query.group_by(models.Trainer.id, models.Employee.id)\
            .having(func.avg(models.Feedback.mark) >= min_rating)
    
    return query.offset(skip).limit(limit).all()

# Specialization CRUD
def get_specialization(db: Session, specialization_id: int):
    return db.query(models.TrainerSpecialization).filter(models.TrainerSpecialization.id == specialization_id).first()

def get_specializations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TrainerSpecialization).offset(skip).limit(limit).all()