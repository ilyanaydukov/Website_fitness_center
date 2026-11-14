# app/init_db.py
import sys
from pathlib import Path

# Добавляем путь к корневой директории проекта
sys.path.append(str(Path(__file__).parent.parent))

from app.database import Base, engine

def init_db():
    """
    Создает все таблицы в базе данных
    """
    print("Creating database tables...")
    
    # Импортируем все модели для их регистрации в метаданных Base
    from app.models.user import User, Client, Employee, Position, Trainer, TrainerSpecialization, Vacation, TypeOfVacation, SalaryStatement
    from app.models.fitness import FitnessCenter, Room, EquipmentCategory, Equipment, ServiceCategory, Service, VarietyServiceCategory, Feedback
    from app.models.schedule import Workout, ClientRecord
    from app.models.subscription import SubscriptionAccessLevel, SubscriptionActivity, Subscription, ClientSubscription
    
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()