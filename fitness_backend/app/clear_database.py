# app/clear_database.py
import sys
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import text

# Добавляем путь к корневой директории проекта
sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal, engine
from app.models.user import *
from app.models.fitness import *
from app.models.schedule import *
from app.models.subscription import *

def clear_database():
    """
    Полностью очищает базу данных, удаляя все данные из таблиц
    """
    db = SessionLocal()
    
    try:
        print("Очистка базы данных...")
        
        # Для PostgreSQL отключаем проверку внешних ключей
        db.execute(text("SET session_replication_role = 'replica'"))
        
        # Очистка таблиц в правильном порядке (сначала дочерние, затем родительские)
        tables_to_clear = [
            ClientRecord,
            ClientSubscription,
            Feedback,
            Workout,
            Vacation,
            SalaryStatement,
            VarietyServiceCategory,
            Equipment,
            Client,
            Trainer,
            Employee,
            User,
            Position,
            TypeOfVacation,
            TrainerSpecialization,
            Service,
            ServiceCategory,
            Room,
            FitnessCenter,
            EquipmentCategory,
            Subscription,
            SubscriptionAccessLevel,
            SubscriptionActivity
        ]
        
        for table in tables_to_clear:
            print(f"Очистка {table.__tablename__}...")
            try:
                db.query(table).delete()
                db.commit()
            except Exception as e:
                print(f"  Предупреждение: {e}")
                db.rollback()
                # Пробуем альтернативный подход
                try:
                    # Удаляем записи по одной
                    records = db.query(table).all()
                    for record in records:
                        db.delete(record)
                    db.commit()
                    print(f"  Удалено {len(records)} записей")
                except Exception as e2:
                    print(f"  Ошибка при удалении: {e2}")
                    db.rollback()
        
        # Включаем проверку внешних ключей обратно
        db.execute(text("SET session_replication_role = 'origin'"))
        
        print("\n✅ База данных успешно очищена!")
        
        # Проверяем, что все таблицы пустые
        print("\nПроверка очистки:")
        for table in tables_to_clear:
            count = db.query(table).count()
            if count == 0:
                print(f"  {table.__tablename__}: очищена")
            else:
                print(f"  {table.__tablename__}: {count} записей осталось")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка очистки базы данных: {e}")
        raise
    finally:
        db.close()

def clear_database_alternative():
    """
    Альтернативный метод очистки без отключения внешних ключей
    """
    db = SessionLocal()
    
    try:
        print("Очистка базы данных (альтернативный метод)...")
        
        # Очистка таблиц в правильном порядке - ВАЖНО для PostgreSQL
        # Сначала очищаем таблицы, которые имеют внешние ключи
        
        print("1. Очистка записей на тренировки...")
        db.query(ClientRecord).delete()
        db.commit()
        
        print("2. Очистка отзывов...")
        db.query(Feedback).delete()
        db.commit()
        
        print("3. Очистка подписок клиентов...")
        db.query(ClientSubscription).delete()
        db.commit()
        
        print("4. Очистка тренировок...")
        db.query(Workout).delete()
        db.commit()
        
        print("5. Очистка отпусков...")
        db.query(Vacation).delete()
        db.commit()
        
        print("6. Очистка зарплатных ведомостей...")
        db.query(SalaryStatement).delete()
        db.commit()
        
        print("7. Очистка связей услуг...")
        db.query(VarietyServiceCategory).delete()
        db.commit()
        
        print("8. Очистка оборудования...")
        db.query(Equipment).delete()
        db.commit()
        
        print("9. Очистка тренеров...")
        db.query(Trainer).delete()
        db.commit()
        
        print("10. Очистка сотрудников...")
        db.query(Employee).delete()
        db.commit()
        
        print("11. Очистка клиентов...")
        db.query(Client).delete()
        db.commit()
        
        print("12. Очистка пользователей...")
        db.query(User).delete()
        db.commit()
        
        # Очистка справочников
        print("13. Очистка должностей...")
        db.query(Position).delete()
        db.commit()
        
        print("14. Очистка типов отпусков...")
        db.query(TypeOfVacation).delete()
        db.commit()
        
        print("15. Очистка специализаций тренеров...")
        db.query(TrainerSpecialization).delete()
        db.commit()
        
        print("16. Очистка услуг...")
        db.query(Service).delete()
        db.commit()
        
        print("17. Очистка категорий услуг...")
        db.query(ServiceCategory).delete()
        db.commit()
        
        print("18. Очистка залов...")
        db.query(Room).delete()
        db.commit()
        
        print("19. Очистка фитнес-центров...")
        db.query(FitnessCenter).delete()
        db.commit()
        
        print("20. Очистка категорий оборудования...")
        db.query(EquipmentCategory).delete()
        db.commit()
        
        print("21. Очистка подписок...")
        db.query(Subscription).delete()
        db.commit()
        
        print("22. Очистка уровней доступа...")
        db.query(SubscriptionAccessLevel).delete()
        db.commit()
        
        print("23. Очистка статусов активности...")
        db.query(SubscriptionActivity).delete()
        db.commit()
        
        print("\n✅ База данных успешно очищена!")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка очистки: {e}")
        print("Попробуйте метод с отключением внешних ключей...")
        raise
    finally:
        db.close()

def recreate_tables():
    """
    Удаляет и заново создает все таблицы
    """
    print("Пересоздание таблиц...")
    
    try:
        # Удаляем все таблицы
        print("Удаление таблиц...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Все таблицы удалены.")
        
        # Создаем все таблицы заново
        print("Создание таблиц...")
        Base.metadata.create_all(bind=engine)
        print("✅ Все таблицы созданы заново.")
        
    except Exception as e:
        print(f"❌ Ошибка пересоздания таблиц: {e}")
        raise

def clear_with_truncate():
    """
    Использует TRUNCATE для быстрой очистки таблиц PostgreSQL
    """
    db = SessionLocal()
    
    try:
        print("Очистка с помощью TRUNCATE...")
        
        # Получаем все таблицы в правильном порядке
        tables = [
            "client_record",
            "feedback", 
            "client_subscription",
            "workout",
            "vacation",
            "salary_statement",
            "variety_service_category",
            "equipment",
            "trainer",
            "employee",
            "client",
            "user_table",  # Обратите внимание на имя таблицы!
            "position",
            "type_of_vacation",
            "trainer_specialization",
            "service",
            "service_category",
            "room",
            "fitness_center",
            "equipment_category",
            "subscription",
            "subscription_access_level",
            "subscription_activity"
        ]
        
        # Выполняем TRUNCATE для каждой таблицы с CASCADE
        for table in tables:
            print(f"TRUNCATE {table}...")
            try:
                db.execute(text(f'TRUNCATE TABLE "{table}" CASCADE'))
                db.commit()
            except Exception as e:
                print(f"  Ошибка TRUNCATE {table}: {e}")
                db.rollback()
        
        # Сбрасываем последовательности
        print("Сброс последовательностей...")
        sequences = [
            "client_record_id_seq",
            "feedback_id_seq",
            "client_subscription_id_seq",
            "workout_id_seq",
            "vacation_id_seq",
            "salary_statement_id_seq",
            "variety_service_category_id_seq",
            "equipment_id_seq",
            "trainer_id_seq",
            "employee_id_seq",
            "client_id_seq",
            "user_table_id_seq",
            "position_id_seq",
            "type_of_vacation_id_seq",
            "trainer_specialization_id_seq",
            "service_id_seq",
            "service_category_id_seq",
            "room_id_seq",
            "fitness_center_id_seq",
            "equipment_category_id_seq",
            "subscription_id_seq",
            "subscription_access_level_id_seq",
            "subscription_activity_id_seq"
        ]
        
        for seq in sequences:
            try:
                db.execute(text(f"ALTER SEQUENCE {seq} RESTART WITH 1"))
                db.commit()
            except:
                pass  # Игнорируем ошибки для несуществующих последовательностей
        
        print("\n✅ База данных очищена с помощью TRUNCATE!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("="*50)
    print("Утилита очистки базы данных PostgreSQL")
    print("="*50)
    print("\nВыберите метод очистки:")
    print("1. Очистка данных (сохранить таблицы)")
    print("2. Очистка данных (альтернативный метод)")
    print("3. Очистка с помощью TRUNCATE (быстрый)")
    print("4. Пересоздать все таблицы")
    print("5. Полный сброс (удалить и создать таблицы)")
    
    choice = input("\nВведите номер (1-5): ").strip()
    
    if choice == "1":
        confirm = input("Очистить все данные? (y/n): ")
        if confirm.lower() == 'y':
            clear_database()
    elif choice == "2":
        confirm = input("Очистить все данные (альтернативный метод)? (y/n): ")
        if confirm.lower() == 'y':
            clear_database_alternative()
    elif choice == "3":
        confirm = input("Использовать TRUNCATE для быстрой очистки? (y/n): ")
        if confirm.lower() == 'y':
            clear_with_truncate()
    elif choice == "4":
        confirm = input("Удалить и создать таблицы заново? (y/n): ")
        if confirm.lower() == 'y':
            recreate_tables()
    elif choice == "5":
        confirm = input("Полный сброс базы данных? (y/n): ")
        if confirm.lower() == 'y':
            recreate_tables()
            print("\nТеперь заполните базу данными командой: python app/seed_data.py")
    else:
        print("❌ Неверный выбор")