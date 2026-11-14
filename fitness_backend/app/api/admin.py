from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date
import io
from sqlalchemy import func

from app.models.user import Trainer
from ..models import Workout

from ..database import get_db
from ..auth.dependencies import get_current_employee
from ..crud.fitness import (
    create_fitness_center, update_fitness_center, delete_fitness_center,
    create_room, update_room, delete_room,
    create_equipment, update_equipment, delete_equipment, get_equipment_by_room,
    create_service, update_service, delete_service,
    create_trainer, update_trainer, delete_trainer, get_specializations,
    get_all_trainers_with_details, get_trainer_with_details
)
from ..crud.schedule import get_workouts, get_workout, create_workout, update_workout, delete_workout
from ..crud.user import (
    create_position, get_positions, get_position as get_position_by_id,
    update_position, delete_position,
    get_employees, get_employee, update_employee, delete_employee,
    create_employee
)
from ..crud.subscription import (
    create_subscription, update_subscription, delete_subscription,
    get_subscriptions as get_all_subscriptions
)
from ..utils.pdf_generator import (
    generate_equipment_pdf, generate_schedule_pdf, generate_registrations_pdf
)
from ..schemas.fitness import (
    FitnessCenterCreate, FitnessCenterUpdate, FitnessCenterInDB,
    RoomCreate, RoomUpdate, RoomInDB,
    EquipmentCreate, EquipmentUpdate, EquipmentInDB,
    ServiceCreate, ServiceUpdate, ServiceInDB,
    TrainerCreate, TrainerUpdate, TrainerInDB,
    SpecializationInDB
)
from ..schemas.subscription import SubscriptionCreate, SubscriptionUpdate, SubscriptionInDB
from ..schemas.user import PositionBase, PositionInDB, EmployeeInDB, EmployeeUpdate, EmployeeCreate
from ..schemas.schedule import WorkoutInDB, WorkoutCreate, WorkoutUpdate

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

# ============ Расписание тренировок ============
@router.get("/workouts", response_model=List[WorkoutInDB])
def get_workouts_admin(
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить все тренировки для админки"""
    return get_workouts(db, skip=skip, limit=limit, date_from=date_from, date_to=date_to)

@router.post("/workouts", response_model=WorkoutInDB)
def create_workout_admin(
    workout: WorkoutCreate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Создать тренировку (админ)"""
    return create_workout(db, workout=workout)

@router.put("/workouts/{workout_id}", response_model=WorkoutInDB)
def update_workout_admin(
    workout_id: int,
    workout_update: WorkoutUpdate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Обновить тренировку (админ)"""
    updated_workout = update_workout(db, workout_id=workout_id, workout_update=workout_update)
    if not updated_workout:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    return updated_workout

@router.delete("/workouts/{workout_id}")
def delete_workout_admin(
    workout_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Удалить тренировку (админ)"""
    workout = delete_workout(db, workout_id=workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    return {"message": "Тренировка удалена успешно"}

# ============ Тренеры ============
@router.get("/trainers", response_model=List[TrainerInDB])
def get_trainers_admin(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить всех тренеров для админки"""
    return get_all_trainers_with_details(db, skip=skip, limit=limit)

@router.get("/trainers/{trainer_id}", response_model=TrainerInDB)
def get_trainer_admin(
    trainer_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить тренера по ID"""
    trainer = get_trainer_with_details(db, trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Тренер не найден")
    return trainer

@router.post("/trainers", response_model=TrainerInDB)
def create_trainer_admin(
    trainer: TrainerCreate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Создать тренера (создает сотрудника и тренерский профиль)"""
    try:
        # Проверяем, существует ли уже сотрудник с таким email
        from ..crud.user import get_employee_by_email
        existing_employee = get_employee_by_email(db, email=trainer.email)
        if existing_employee:
            raise HTTPException(
                status_code=400,
                detail="Сотрудник с таким email уже существует"
            )
        
        return create_trainer(db, trainer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания тренера: {str(e)}")

@router.put("/trainers/{trainer_id}", response_model=TrainerInDB)
def update_trainer_admin(
    trainer_id: int,
    trainer_update: TrainerUpdate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Обновить тренера (обновляет данные сотрудника и тренерский профиль)"""
    updated_trainer = update_trainer(db, trainer_id=trainer_id, trainer_update=trainer_update)
    if not updated_trainer:
        raise HTTPException(status_code=404, detail="Тренер не найден")
    return updated_trainer

@router.delete("/trainers/{trainer_id}")
def delete_trainer_admin(
    trainer_id: int,
    delete_employee: bool = False,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """
    Удалить тренера
    
    Parameters:
    - delete_employee: если True, удаляет полностью сотрудника, если False - только тренерский профиль
    """
    from ..crud.fitness import get_trainer
    
    trainer = get_trainer(db, trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Тренер не найден")
    
    if delete_employee:
        # Удаляем полностью сотрудника
        employee = delete_employee(db, trainer.employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Сотрудник не найден")
        return {"message": "Тренер и сотрудник удалены успешно"}
    else:
        # Удаляем только тренерский профиль
        trainer_deleted = delete_trainer(db, trainer_id)
        if not trainer_deleted:
            raise HTTPException(status_code=404, detail="Тренер не найден")
        return {"message": "Тренерский профиль удален успешно, сотрудник сохранен"}

@router.get("/trainers/{trainer_id}/workouts", response_model=List[WorkoutInDB])
def get_trainer_workouts_admin(
    trainer_id: int,
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить тренировки тренера"""
    from ..crud.schedule import get_workouts_by_trainer
    
    workouts = get_workouts_by_trainer(db, trainer_id)
    
    # Фильтрация по датам
    if date_from:
        workouts = [w for w in workouts if w.workout_date >= date_from]
    if date_to:
        workouts = [w for w in workouts if w.workout_date <= date_to]
    
    # Пагинация
    return workouts[skip:skip + limit]

# ============ Сотрудники ============
@router.get("/employees", response_model=List[EmployeeInDB])
def get_employees_admin(
    skip: int = 0,
    limit: int = 100,
    is_trainer: Optional[bool] = None,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить всех сотрудников, с фильтрацией по тренерам"""
    from sqlalchemy.orm import aliased
    from ..models import Employee, Trainer
    
    query = db.query(Employee)
    
    # Фильтрация: только тренеры или только не тренеры
    if is_trainer is True:
        query = query.join(Trainer, Employee.id == Trainer.employee_id)
    elif is_trainer is False:
        query = query.outerjoin(Trainer, Employee.id == Trainer.employee_id)\
                     .filter(Trainer.id == None)
    
    employees = query.offset(skip).limit(limit).all()
    return employees

@router.get("/employees/{employee_id}", response_model=EmployeeInDB)
def get_employee_admin(
    employee_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить сотрудника по ID"""
    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return employee

@router.post("/employees", response_model=EmployeeInDB)
def create_employee_admin(
    employee: EmployeeCreate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Создать сотрудника (не тренера)"""
    try:
        # Проверяем, существует ли уже сотрудник с таким email
        from ..crud.user import get_employee_by_email
        existing_employee = get_employee_by_email(db, email=employee.email)
        if existing_employee:
            raise HTTPException(
                status_code=400,
                detail="Сотрудник с таким email уже существует"
            )
        
        return create_employee(db, employee)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания сотрудника: {str(e)}")

@router.put("/employees/{employee_id}", response_model=EmployeeInDB)
def update_employee_admin(
    employee_id: int,
    employee_update: EmployeeUpdate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Обновить данные сотрудника"""
    updated_employee = update_employee(db, employee_id=employee_id, employee_update=employee_update)
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return updated_employee

@router.delete("/employees/{employee_id}")
def delete_employee_admin(
    employee_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Удалить сотрудника"""
    employee = delete_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return {"message": "Сотрудник удален успешно"}

@router.post("/employees/{employee_id}/promote-to-trainer", response_model=TrainerInDB)
def promote_employee_to_trainer(
    employee_id: int,
    specialization_id: Optional[int] = None,
    work_experience: int = 0,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Превратить существующего сотрудника в тренера"""
    from ..crud.fitness import create_trainer_from_employee
    from ..models import Employee
    
    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    
    # Проверяем, не является ли уже тренером
    if employee.trainer_profile:
        raise HTTPException(
            status_code=400,
            detail="Сотрудник уже является тренером"
        )
    
    # Создаем тренерский профиль
    trainer_data = {
        "employee_id": employee_id,
        "specialization_id": specialization_id,
        "work_experience": work_experience
    }
    
    trainer = create_trainer_from_employee(db, trainer_data)
    return trainer

# ============ Специализации ============
@router.get("/specializations", response_model=List[SpecializationInDB])
def get_specializations_admin(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить все специализации"""
    return get_specializations(db, skip=skip, limit=limit)

# ============ Фитнес-центры ============
@router.post("/fitness-centers", response_model=FitnessCenterInDB)
def create_fitness_center_admin(
    fitness_center: FitnessCenterCreate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Создать фитнес-центр"""
    return create_fitness_center(db, fitness_center)

@router.put("/fitness-centers/{fitness_center_id}", response_model=FitnessCenterInDB)
def update_fitness_center_admin(
    fitness_center_id: int,
    fitness_center_update: FitnessCenterUpdate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Обновить фитнес-центр"""
    updated_fitness_center = update_fitness_center(db, fitness_center_id=fitness_center_id, 
                                                   fitness_center_update=fitness_center_update)
    if not updated_fitness_center:
        raise HTTPException(status_code=404, detail="Фитнес-центр не найден")
    return updated_fitness_center

@router.delete("/fitness-centers/{fitness_center_id}")
def delete_fitness_center_admin(
    fitness_center_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Удалить фитнес-центр"""
    fitness_center = delete_fitness_center(db, fitness_center_id=fitness_center_id)
    if not fitness_center:
        raise HTTPException(status_code=404, detail="Фитнес-центр не найден")
    return {"message": "Фитнес-центр удален успешно"}

# ============ Помещения ============
@router.post("/rooms", response_model=RoomInDB)
def create_room_admin(
    room: RoomCreate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Создать помещение"""
    return create_room(db, room)

@router.put("/rooms/{room_id}", response_model=RoomInDB)
def update_room_admin(
    room_id: int,
    room_update: RoomUpdate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Обновить помещение"""
    updated_room = update_room(db, room_id=room_id, room_update=room_update)
    if not updated_room:
        raise HTTPException(status_code=404, detail="Помещение не найден")
    return updated_room

@router.delete("/rooms/{room_id}")
def delete_room_admin(
    room_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Удалить помещение"""
    room = delete_room(db, room_id=room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Помещение не найден")
    return {"message": "Помещение удалено успешно"}

# ============ Оборудование ============
@router.post("/equipment", response_model=EquipmentInDB)
def create_equipment_admin(
    equipment: EquipmentCreate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Создать оборудование"""
    return create_equipment(db, equipment)

@router.put("/equipment/{equipment_id}", response_model=EquipmentInDB)
def update_equipment_admin(
    equipment_id: int,
    equipment_update: EquipmentUpdate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Обновить оборудование"""
    updated_equipment = update_equipment(db, equipment_id=equipment_id, equipment_update=equipment_update)
    if not updated_equipment:
        raise HTTPException(status_code=404, detail="Оборудование не найдено")
    return updated_equipment

@router.delete("/equipment/{equipment_id}")
def delete_equipment_admin(
    equipment_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Удалить оборудование"""
    equipment = delete_equipment(db, equipment_id=equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Оборудование не найдено")
    return {"message": "Оборудование удалено успешно"}

# ============ Услуги ============
@router.get("/services", response_model=List[ServiceInDB])
def get_services_admin(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить все услуги (админ)"""
    from ..crud.fitness import get_services
    return get_services(db, skip=skip, limit=limit)

@router.get("/services/{service_id}", response_model=ServiceInDB)
def get_service_admin(
    service_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить услугу по ID (админ)"""
    from ..crud.fitness import get_service
    service = get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    return service

@router.post("/services", response_model=ServiceInDB)
def create_service_admin(
    service: ServiceCreate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Создать услугу"""
    return create_service(db, service)

@router.put("/services/{service_id}", response_model=ServiceInDB)
def update_service_admin(
    service_id: int,
    service_update: ServiceUpdate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Обновить услугу"""
    updated_service = update_service(db, service_id=service_id, service_update=service_update)
    if not updated_service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    return updated_service

@router.delete("/services/{service_id}")
def delete_service_admin(
    service_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Удалить услугу"""
    service = delete_service(db, service_id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    return {"message": "Услуга удалена успешно"}

# ============ Абонементы ============
@router.get("/subscriptions", response_model=List[SubscriptionInDB])
def get_subscriptions_admin(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить все абонементы"""
    return get_all_subscriptions(db, skip=skip, limit=limit)

@router.post("/subscriptions", response_model=SubscriptionInDB)
def create_subscription_admin(
    subscription: SubscriptionCreate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Создать абонемент"""
    return create_subscription(db, subscription)

@router.put("/subscriptions/{subscription_id}", response_model=SubscriptionInDB)
def update_subscription_admin(
    subscription_id: int,
    subscription_update: SubscriptionUpdate,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Обновить абонемент"""
    updated_subscription = update_subscription(db, subscription_id=subscription_id, 
                                               subscription_update=subscription_update)
    if not updated_subscription:
        raise HTTPException(status_code=404, detail="Абонемент не найден")
    return updated_subscription

@router.delete("/subscriptions/{subscription_id}")
def delete_subscription_admin(
    subscription_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Удалить абонемент"""
    subscription = delete_subscription(db, subscription_id=subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Абонемент не найден")
    return {"message": "Абонемент удален успешно"}

# ============ Должности ============
@router.post("/positions", response_model=PositionInDB)
def create_position_admin(
    position: PositionBase,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Создать должность"""
    return create_position(db, position)

@router.get("/positions", response_model=List[PositionInDB])
def get_positions_admin(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить все должности"""
    return get_positions(db, skip=skip, limit=limit)

@router.get("/positions/{position_id}", response_model=PositionInDB)
def get_position_admin(
    position_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить должность по ID"""
    position = get_position_by_id(db, position_id)
    if not position:
        raise HTTPException(status_code=404, detail="Должность не найдена")
    return position

@router.put("/positions/{position_id}", response_model=PositionInDB)
def update_position_admin(
    position_id: int,
    position_update: PositionBase,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Обновить должность"""
    updated_position = update_position(db, position_id=position_id, position_update=position_update)
    if not updated_position:
        raise HTTPException(status_code=404, detail="Должность не найдена")
    return updated_position

@router.delete("/positions/{position_id}")
def delete_position_admin(
    position_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Удалить должность"""
    position = delete_position(db, position_id=position_id)
    if not position:
        raise HTTPException(status_code=404, detail="Должность не найдена")
    return {"message": "Должность удалена успешно"}

# ============ Генерация PDF отчетов ============
@router.get("/pdf/equipment/{room_id}")
def generate_equipment_pdf_report(
    room_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """
    Генерация PDF отчета по оборудованию в комнате
    """
    try:
        equipment_list = get_equipment_by_room(db, room_id)
        pdf_buffer = generate_equipment_pdf(equipment_list)
        
        headers = {
            'Content-Disposition': f'attachment; filename="equipment_room_{room_id}_{date.today()}.pdf"'
        }
        
        pdf_buffer.seek(0)
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers=headers
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации PDF: {str(e)}")

@router.get("/pdf/schedule/{date_from}/{date_to}")
def generate_schedule_pdf_report(
    date_from: date,
    date_to: date,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """
    Генерация PDF отчета по расписанию тренировок за период
    """
    try:
        
        workouts = db.query(Workout)\
            .options(
                joinedload(Workout.trainer).joinedload(Trainer.employee),
                joinedload(Workout.room),
                joinedload(Workout.service)
            )\
            .filter(
                Workout.workout_date >= date_from,
                Workout.workout_date <= date_to
            )\
            .all()
        
        pdf_buffer = generate_schedule_pdf(workouts, date_from, date_to)
        
        if pdf_buffer is None:
            raise HTTPException(status_code=500, detail="PDF generation failed")
        
        headers = {
            'Content-Disposition': f'attachment; filename="schedule_{date_from}_{date_to}.pdf"'
        }
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers=headers
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации PDF: {str(e)}")

@router.get("/pdf/registrations/{workout_id}")
def generate_registrations_pdf_report(
    workout_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """
    Генерация PDF отчета по регистрациям на тренировку
    """
    try:
        from ..crud.schedule import get_workout_records
        registrations = get_workout_records(db, workout_id)
        pdf_buffer = generate_registrations_pdf(registrations, workout_id)
        
        headers = {
            'Content-Disposition': f'attachment; filename="registrations_workout_{workout_id}_{date.today()}.pdf"'
        }
        
        pdf_buffer.seek(0)
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers=headers
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации PDF: {str(e)}")

# ============ Статистика ============
@router.get("/stats")
def get_admin_stats(
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить статистику для админ-панели"""
    try:
        from sqlalchemy import func
        from ..models import Client, Employee, Trainer, Workout, Subscription, ClientSubscription
        
        # Количество клиентов
        clients_count = db.query(func.count(Client.id)).scalar() or 0
        
        # Количество сотрудников (всех, включая тренеров)
        employees_count = db.query(func.count(Employee.id)).scalar() or 0
        
        # Количество тренеров
        trainers_count = db.query(func.count(Trainer.id)).scalar() or 0
        
        # Количество обычных сотрудников (не тренеров)
        regular_employees_count = employees_count - trainers_count
        
        # Количество активных тренировок
        workouts_count = db.query(func.count(Workout.id)).filter(
            Workout.workout_date >= date.today()
        ).scalar() or 0
        
        # Количество активных абонементов
        active_subscriptions = db.query(func.count(ClientSubscription.id)).filter(
            ClientSubscription.start_action_date <= date.today(),
            ClientSubscription.end_action_date >= date.today()
        ).scalar() or 0
        
        return {
            "clients": clients_count,
            "employees": {
                "total": employees_count,
                "trainers": trainers_count,
                "regular": regular_employees_count
            },
            "workouts": {
                "total": db.query(func.count(Workout.id)).scalar() or 0,
                "active": workouts_count
            },
            "subscriptions": {
                "active": active_subscriptions,
                "total": db.query(func.count(Subscription.id)).scalar() or 0
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")

# ============ Просмотр записей на тренировку ============
@router.get("/workouts/{workout_id}/registrations")
def get_workout_registrations_admin(
    workout_id: int,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить записи на тренировку"""
    from ..crud.schedule import get_workout_records
    records = get_workout_records(db, workout_id)
    
    # Формируем ответ с дополнительной информацией
    result = []
    for record in records:
        client_info = {
            "id": record.client_id,
            "name": f"{record.client.first_name} {record.client.last_name}" if record.client else "Неизвестно",
            "email": record.client.email if record.client else None,
            "phone": record.client.phone if record.client else None
        }
        result.append({
            "id": record.id,
            "record_date": record.record_date,
            "record_time": record.record_time,
            "client": client_info
        })
    
    return result

# ============ Управление отзывами ============
@router.get("/trainers/{trainer_id}/feedbacks")
def get_trainer_feedbacks_admin(
    trainer_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Получить отзывы о тренере"""
    from ..crud.fitness import get_feedbacks_for_trainer
    
    feedbacks = get_feedbacks_for_trainer(db, trainer_id)
    return feedbacks[skip:skip + limit]

# ============ Экспорт данных ============
@router.get("/export/trainers")
def export_trainers_data(
    format: str = "csv",
    current_user = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Экспорт данных о тренерах"""
    try:
        trainers = get_all_trainers_with_details(db, skip=0, limit=1000)
        
        if format.lower() == "csv":
            import csv
            
            # Создаем CSV в памяти
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Заголовки
            writer.writerow([
                "ID", "Employee ID", "First Name", "Last Name", "Email", 
                "Phone", "Position", "Fitness Center", "Specialization",
                "Work Experience", "Date of Employment"
            ])
            
            # Данные
            for trainer in trainers:
                writer.writerow([
                    trainer.get("id"),
                    trainer.get("employee_id"),
                    trainer.get("first_name"),
                    trainer.get("last_name"),
                    trainer.get("email"),
                    trainer.get("phone"),
                    trainer.get("position_name"),
                    trainer.get("fitness_center_name"),
                    trainer.get("specialization", {}).get("name") if trainer.get("specialization") else "",
                    trainer.get("work_experience"),
                    trainer.get("date_of_employment")
                ])
            
            output.seek(0)
            return StreamingResponse(
                iter([output.getvalue()]),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=trainers_export.csv"}
            )
        
        elif format.lower() == "json":
            import json
            return trainers
        
        else:
            raise HTTPException(status_code=400, detail="Unsupported format. Use 'csv' or 'json'")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка экспорта: {str(e)}")