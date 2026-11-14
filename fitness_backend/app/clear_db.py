# clear_database.py
import sys
import os
import argparse
from sqlalchemy import text, inspect

# Добавляем путь к приложению
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base, SessionLocal
from app import models

def get_table_names():
    """Получает список всех таблиц в базе данных"""
    inspector = inspect(engine)
    return inspector.get_table_names()

def show_database_stats():
    """Показывает статистику базы данных"""
    db = SessionLocal()
    
    try:
        print("📊 Статистика базы данных:")
        print("-" * 50)
        
        table_names = get_table_names()
        
        for table in table_names:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"  {table}: {count} записей")
            except Exception as e:
                print(f"  {table}: ошибка при подсчете - {e}")
        
        print("-" * 50)
        
        # Общее количество записей
        total = 0
        for table in table_names:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                total += result.scalar()
            except:
                pass
        
        print(f"Всего записей во всех таблицах: {total}")
        
    except Exception as e:
        print(f"❌ Ошибка при получении статистики: {e}")
    finally:
        db.close()

def clear_all_data(confirm: bool = False):
    """Очищает все данные из всех таблиц"""
    if not confirm:
        print("⚠️  ВНИМАНИЕ: Эта операция удалит ВСЕ данные из базы данных!")
        print("Это действие нельзя отменить!")
        print("\n📊 Текущее состояние базы данных:")
        show_database_stats()
        
        response = input("\n❓ Вы уверены, что хотите удалить все данные? (yes/NO): ")
        if response.lower() != 'yes':
            print("❌ Операция отменена")
            return
    
    db = SessionLocal()
    
    try:
        print("🧹 Начинаю очистку базы данных...")
        
        # Получаем список всех таблиц
        table_names = get_table_names()
        
        # Отключаем внешние ключи (для PostgreSQL)
        try:
            db.execute(text("SET session_replication_role = 'replica'"))
        except:
            pass  # Игнорируем ошибку, если не поддерживается
        
        # Удаляем данные из всех таблиц в правильном порядке (с учетом зависимостей)
        tables_to_clear = [
            # Сначала дочерние таблицы
            'feedback_for_trainer',
            'client_record_on_workout',
            'client_subscription',
            'vacation',
            'salary_statement',
            'variety_service_category',
            'workout_schedule',
            'equipment',
            
            # Затем основные таблицы
            'trainer',
            'employee',
            'room',
            'service',
            'service_category',
            'subscription',
            'subscription_access_level',
            'subscription_activity',
            'trainer_specialization',
            'position',
            'type_of_vacation',
            'equipment_category',
            'fitness_center',
            
            # В конце клиентов
            'client'
        ]
        
        deleted_counts = {}
        
        for table in tables_to_clear:
            if table in table_names:
                try:
                    # Считаем количество записей
                    count_result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = count_result.scalar()
                    
                    if count > 0:
                        # Удаляем данные
                        db.execute(text(f"DELETE FROM {table}"))
                        deleted_counts[table] = count
                        print(f"  ✅ {table}: удалено {count} записей")
                    else:
                        print(f"  ℹ️  {table}: таблица пуста")
                except Exception as e:
                    print(f"  ⚠️  {table}: ошибка - {e}")
        
        # Включаем внешние ключи обратно
        try:
            db.execute(text("SET session_replication_role = 'origin'"))
        except:
            pass
        
        db.commit()
        
        print("\n✅ Очистка базы данных завершена!")
        
        # Показываем статистику удаления
        if deleted_counts:
            print("\n📊 Удаленные данные:")
            total_deleted = sum(deleted_counts.values())
            for table, count in deleted_counts.items():
                print(f"  {table}: {count} записей")
            print(f"Всего удалено: {total_deleted} записей")
        
        # Показываем текущее состояние
        print("\n📊 Текущее состояние базы данных:")
        show_database_stats()
        
    except Exception as e:
        print(f"❌ Ошибка при очистке базы данных: {e}")
        db.rollback()
    finally:
        db.close()

def drop_all_tables(confirm: bool = False):
    """Удаляет все таблицы из базы данных (полный сброс)"""
    if not confirm:
        print("⚠️  ВНИМАНИЕ: Эта операция УДАЛИТ ВСЕ ТАБЛИЦЫ из базы данных!")
        print("Все данные и структура будут потеряны!")
        print("Это действие нельзя отменить!")
        
        response = input("\n❓ Вы уверены, что хотите удалить все таблицы? (yes/NO): ")
        if response.lower() != 'yes':
            print("❌ Операция отменена")
            return
    
    try:
        print("🗑️  Начинаю удаление всех таблиц...")
        
        # Удаляем все таблицы
        Base.metadata.drop_all(bind=engine)
        
        print("✅ Все таблицы удалены!")
        print("\nℹ️  Чтобы создать таблицы заново, запустите сервер или скрипт init_data.py")
        
    except Exception as e:
        print(f"❌ Ошибка при удалении таблиц: {e}")

def recreate_tables():
    """Создает все таблицы заново"""
    try:
        print("🔄 Создание таблиц...")
        
        # Создаем все таблицы
        Base.metadata.create_all(bind=engine)
        
        print("✅ Таблицы созданы!")
        print("\n📋 Список созданных таблиц:")
        
        tables = get_table_names()
        for table in sorted(tables):
            print(f"  - {table}")
        
        print(f"\nВсего создано таблиц: {len(tables)}")
        
    except Exception as e:
        print(f"❌ Ошибка при создании таблиц: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Управление базой данных фитнес-центра')
    parser.add_argument('--clear', '-c', action='store_true', 
                       help='Очистить все данные из таблиц')
    parser.add_argument('--drop', '-d', action='store_true',
                       help='Удалить все таблицы из базы данных')
    parser.add_argument('--recreate', '-r', action='store_true',
                       help='Создать таблицы заново')
    parser.add_argument('--stats', '-s', action='store_true',
                       help='Показать статистику базы данных')
    parser.add_argument('--force', '-f', action='store_true',
                       help='Пропустить подтверждение (используйте с осторожностью!)')
    
    args = parser.parse_args()
    
    if args.stats:
        show_database_stats()
    elif args.clear:
        clear_all_data(confirm=args.force)
    elif args.drop:
        drop_all_tables(confirm=args.force)
    elif args.recreate:
        recreate_tables()
    else:
        print("ℹ️ Использование:")
        print("  python clear_database.py --stats           # Показать статистику БД")
        print("  python clear_database.py --clear           # Очистить все данные")
        print("  python clear_database.py --clear --force   # Очистить без подтверждения")
        print("  python clear_database.py --drop            # Удалить все таблицы")
        print("  python clear_database.py --recreate        # Создать таблицы заново")
        print("\n⚠️  ВНИМАНИЕ: Операции clear и drop НЕОБРАТИМЫ!")