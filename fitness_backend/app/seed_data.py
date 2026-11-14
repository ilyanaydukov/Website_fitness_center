# app/seed_data.py
import sys
from pathlib import Path
from datetime import date, time, datetime, timedelta
from sqlalchemy.orm import Session

# Добавляем путь к корневой директории проекта
sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models.user import *
from app.models.fitness import *
from app.models.schedule import *
from app.models.subscription import *
from app.auth.security import get_password_hash

def seed_data():
    """
    Заполняет базу данных тестовыми данными на русском языке
    """
    db = SessionLocal()
    
    try:
        print("Заполнение базы данных тестовыми данными...")
        
        # 1. Создаем сначала все основные справочники
        print("Создание основных справочников...")
        
        # Статусы подписок
        activity_active = SubscriptionActivity(
            status_name="Активна",
            activity_flag=True
        )
        activity_expired = SubscriptionActivity(
            status_name="Истекла",
            activity_flag=False
        )
        activity_suspended = SubscriptionActivity(
            status_name="Приостановлена",
            activity_flag=False
        )
        db.add_all([activity_active, activity_expired, activity_suspended])
        db.flush()  # Получаем ID
        
        print("   ✓ Статусы подписок созданы")
        
        # Уровни доступа подписок
        access_basic = SubscriptionAccessLevel(
            access_level_name="Базовый",
            access_description="Доступ к базовому оборудованию и групповым занятиям"
        )
        access_premium = SubscriptionAccessLevel(
            access_level_name="Премиум",
            access_description="Доступ ко всему оборудованию, групповым занятиям и консультациям персонального тренера"
        )
        access_vip = SubscriptionAccessLevel(
            access_level_name="VIP",
            access_description="Полный доступ включая спа и специальные услуги"
        )
        db.add_all([access_basic, access_premium, access_vip])
        db.flush()
        
        print("   ✓ Уровни доступа созданы")
        
        # Типы подписок
        subscription_basic = Subscription(
            subscription_type="Базовый (месяц)",
            price=1999.00,
            validity_period=30,
            subscription_access_level_id=access_basic.id
        )
        subscription_premium = Subscription(
            subscription_type="Премиум (месяц)",
            price=3999.00,
            validity_period=30,
            subscription_access_level_id=access_premium.id
        )
        subscription_vip = Subscription(
            subscription_type="VIP (месяц)",
            price=6999.00,
            validity_period=30,
            subscription_access_level_id=access_vip.id
        )
        subscription_3months = Subscription(
            subscription_type="Премиум (3 месяца)",
            price=9999.00,
            validity_period=90,
            subscription_access_level_id=access_premium.id
        )
        subscription_year = Subscription(
            subscription_type="VIP (год)",
            price=59999.00,
            validity_period=365,
            subscription_access_level_id=access_vip.id
        )
        db.add_all([subscription_basic, subscription_premium, subscription_vip, subscription_3months, subscription_year])
        db.flush()
        
        print("   ✓ Типы подписок созданы")
        
        # Типы отпусков
        vacation_annual = TypeOfVacation(
            name="Ежегодный отпуск",
            duration=14,
            past=False
        )
        vacation_sick = TypeOfVacation(
            name="Больничный",
            duration=7,
            past=False
        )
        vacation_maternity = TypeOfVacation(
            name="Декретный отпуск",
            duration=140,
            past=False
        )
        db.add_all([vacation_annual, vacation_sick, vacation_maternity])
        db.flush()
        
        print("   ✓ Типы отпусков созданы")
        
        # Должности
        position_manager = Position(
            name="Менеджер",
            salary=80000.00
        )
        position_trainer = Position(
            name="Фитнес-тренер",
            salary=50000.00
        )
        position_receptionist = Position(
            name="Администратор",
            salary=40000.00
        )
        position_cleaner = Position(
            name="Уборщик",
            salary=30000.00
        )
        position_director = Position(
            name="Директор",
            salary=120000.00
        )
        db.add_all([position_manager, position_trainer, position_receptionist, position_cleaner, position_director])
        db.flush()
        
        print("   ✓ Должности созданы")
        
        # Категории оборудования
        cardio_category = EquipmentCategory(name="Кардио-оборудование")
        strength_category = EquipmentCategory(name="Силовое оборудование")
        yoga_category = EquipmentCategory(name="Йога и пилатес")
        functional_category = EquipmentCategory(name="Функциональный тренинг")
        recovery_category = EquipmentCategory(name="Восстановление")
        db.add_all([cardio_category, strength_category, yoga_category, functional_category, recovery_category])
        db.flush()
        
        print("   ✓ Категории оборудования созданы")
        
        # Специализации тренеров
        spec_yoga = TrainerSpecialization(
            name="Инструктор йоги",
            description="Специализация по йоге и медитации"
        )
        spec_pilates = TrainerSpecialization(
            name="Инструктор пилатеса",
            description="Специализация по пилатесу и укреплению кора"
        )
        spec_bodybuilding = TrainerSpecialization(
            name="Тренер по бодибилдингу",
            description="Специализация по силовым тренировкам и бодибилдингу"
        )
        spec_cardio = TrainerSpecialization(
            name="Кардио-тренер",
            description="Специализация по кардио и выносливости"
        )
        spec_crossfit = TrainerSpecialization(
            name="Тренер CrossFit",
            description="Специализация по CrossFit и функциональному тренингу"
        )
        spec_rehab = TrainerSpecialization(
            name="Реабилитолог",
            description="Специализация по восстановлению после травм"
        )
        spec_dance = TrainerSpecialization(
            name="Тренер по танцам",
            description="Специализация по танцевальным направлениям"
        )
        db.add_all([spec_yoga, spec_pilates, spec_bodybuilding, spec_cardio, spec_crossfit, spec_rehab, spec_dance])
        db.flush()
        
        print("   ✓ Специализации тренеров созданы")
        
        # Фитнес-центры
        fitness_center1 = FitnessCenter(
            name="Фитнес Мир Центр",
            address="ул. Ленина, 123, Томск",
            working_hours="06:00-23:00 Пн-Пт, 08:00-22:00 Сб-Вс",
            phone="+7 (3822) 123-45-67",
            email="info@fitnessmir.tomsk.ru"
        )
        fitness_center2 = FitnessCenter(
            name="Спорт Лайф Премиум",
            address="пр. Спортивный, 456, Томск",
            working_hours="05:00-24:00 ежедневно",
            phone="+7 (3822) 765-43-21",
            email="contact@sportlife.tomsk.ru"
        )
        fitness_center3 = FitnessCenter(
            name="Активная Жизнь",
            address="ул. Советская, 78, Томск",
            working_hours="07:00-22:00 Пн-Пт, 09:00-20:00 Сб-Вс",
            phone="+7 (3822) 987-65-43",
            email="info@activlife.tomsk.ru"
        )
        db.add_all([fitness_center1, fitness_center2, fitness_center3])
        db.flush()
        
        print("   ✓ Фитнес-центры созданы")
        
        # Залы
        room1_center1 = Room(
            fitness_center_id=fitness_center1.id,
            name="Основной зал",
            description="Основная тренировочная зона с современным оборудованием",
            capacity=50,
            photo_url="/images/room1.jpg"
        )
        room2_center1 = Room(
            fitness_center_id=fitness_center1.id,
            name="Студия йоги",
            description="Уютная студия для йоги и медитации",
            capacity=25,
            photo_url="/images/room2.jpg"
        )
        room3_center1 = Room(
            fitness_center_id=fitness_center1.id,
            name="Зал для сайклинга",
            description="Специализированный зал для занятий сайклингом",
            capacity=30,
            photo_url="/images/room3.jpg"
        )
        room4_center1 = Room(
            fitness_center_id=fitness_center1.id,
            name="Зона функционального тренинга",
            description="Зона для функциональных тренировок",
            capacity=20,
            photo_url="/images/room4.jpg"
        )
        
        room1_center2 = Room(
            fitness_center_id=fitness_center2.id,
            name="Премиум зона",
            description="VIP тренировочная зона с премиум оборудованием",
            capacity=15,
            photo_url="/images/room5.jpg"
        )
        room2_center2 = Room(
            fitness_center_id=fitness_center2.id,
            name="Бассейн",
            description="25-метровый бассейн с дорожками",
            capacity=40,
            photo_url="/images/room6.jpg"
        )
        room3_center2 = Room(
            fitness_center_id=fitness_center2.id,
            name="Спа-зона",
            description="Зона отдыха с сауной и джакузи",
            capacity=10,
            photo_url="/images/room7.jpg"
        )
        
        room1_center3 = Room(
            fitness_center_id=fitness_center3.id,
            name="Танцевальный зал",
            description="Зал с зеркалами для танцевальных направлений",
            capacity=35,
            photo_url="/images/room8.jpg"
        )
        
        db.add_all([room1_center1, room2_center1, room3_center1, room4_center1,
                   room1_center2, room2_center2, room3_center2,
                   room1_center3])
        db.flush()
        
        print("   ✓ Залы созданы")
        
        # Оборудование
        equipment_data = [
            (room1_center1.id, "Беговая дорожка Pro 5000", cardio_category.id, date(2023, 1, 15), date(2024, 1, 10), "Отличное состояние, регулярное обслуживание"),
            (room1_center1.id, "Эллиптический тренажер Elite", cardio_category.id, date(2023, 3, 20), date(2024, 3, 15), "Хорошее состояние, небольшой износ"),
            (room1_center1.id, "Скамья для жима Pro", strength_category.id, date(2022, 11, 5), date(2024, 2, 1), "Хорошее состояние"),
            (room1_center1.id, "Гантельный набор (2-30 кг)", strength_category.id, date(2023, 5, 10), date(2024, 4, 20), "Полный комплект, отличное состояние"),
            (room2_center1.id, "Набор ковриков для йоги", yoga_category.id, date(2024, 1, 10), date(2024, 6, 1), "Новые, отличное состояние"),
            (room2_center1.id, "Блоки для йоги", yoga_category.id, date(2024, 2, 15), date(2024, 7, 1), "Новые"),
            (room3_center1.id, "Сайкл-тренажер Pro Cycle", cardio_category.id, date(2023, 6, 1), date(2024, 5, 15), "Отличное состояние"),
            (room4_center1.id, "TRX петли", functional_category.id, date(2023, 8, 20), date(2024, 6, 10), "Хорошее состояние"),
            (room4_center1.id, "Медицинские мячи", functional_category.id, date(2023, 9, 5), date(2024, 6, 20), "Полный набор"),
            
            (room1_center2.id, "Беговая дорожка Premium", cardio_category.id, date(2024, 1, 5), date(2024, 7, 1), "Новая, премиум класс"),
            (room1_center2.id, "Эллиптический тренажер Luxury", cardio_category.id, date(2024, 1, 10), date(2024, 7, 5), "Новая"),
            (room2_center2.id, "Дорожки для плавания", recovery_category.id, date(2023, 12, 1), date(2024, 6, 15), "Отличное состояние"),
            (room3_center2.id, "Инфракрасная сауна", recovery_category.id, date(2024, 2, 1), date(2024, 8, 1), "Новая"),
            
            (room1_center3.id, "Зеркальная стена", yoga_category.id, date(2023, 10, 1), date(2024, 5, 1), "Отличное состояние"),
            (room1_center3.id, "Звуковая система", yoga_category.id, date(2023, 10, 1), date(2024, 5, 1), "Хорошее состояние"),
        ]
        
        for room_id, name, category_id, purchase_date, last_service, condition in equipment_data:
            equipment = Equipment(
                room_id=room_id,
                name=name,
                equipment_category_id=category_id,
                purchase_date=purchase_date,
                date_of_last_service=last_service,
                description_of_condition=condition
            )
            db.add(equipment)
        
        db.flush()
        print("   ✓ Оборудование создано")
        
        # Категории услуг
        category_group = ServiceCategory(
            category_name="Групповые занятия",
            category_description="Различные групповые тренировки"
        )
        category_personal = ServiceCategory(
            category_name="Персональные тренировки",
            category_description="Индивидуальные тренировки с персональными тренерами"
        )
        category_special = ServiceCategory(
            category_name="Специальные программы",
            category_description="Специализированные фитнес-программы"
        )
        category_aqua = ServiceCategory(
            category_name="Водные программы",
            category_description="Занятия в бассейне"
        )
        db.add_all([category_group, category_personal, category_special, category_aqua])
        db.flush()
        
        print("   ✓ Категории услуг созданы")
        
        # Услуги
        service_yoga = Service(
            name="Йога",
            price=500.00,
            description="Групповое занятие йогой для всех уровней",
            duration=60
        )
        service_pilates = Service(
            name="Пилатес",
            price=600.00,
            description="Групповое занятие пилатесом с акцентом на укрепление кора",
            duration=60
        )
        service_spinning = Service(
            name="Сайклинг",
            price=700.00,
            description="Высокоинтенсивное занятие на велотренажерах",
            duration=45
        )
        service_zumba = Service(
            name="Зумба",
            price=550.00,
            description="Танцевальная фитнес-программа",
            duration=60
        )
        service_crossfit = Service(
            name="Кроссфит",
            price=800.00,
            description="Высокоинтенсивный функциональный тренинг",
            duration=60
        )
        service_personal = Service(
            name="Персональная тренировка",
            price=1500.00,
            description="Индивидуальная тренировка с сертифицированным тренером",
            duration=60
        )
        service_aqua = Service(
            name="Аквааэробика",
            price=650.00,
            description="Групповое занятие в бассейне",
            duration=45
        )
        service_stretching = Service(
            name="Стретчинг",
            price=450.00,
            description="Занятие на растяжку и гибкость",
            duration=50
        )
        service_boxing = Service(
            name="Бокс",
            price=750.00,
            description="Групповое занятие по боксу",
            duration=60
        )
        service_trx = Service(
            name="TRX",
            price=700.00,
            description="Функциональный тренинг с петлями TRX",
            duration=50
        )
        db.add_all([service_yoga, service_pilates, service_spinning, service_zumba,
                   service_crossfit, service_personal, service_aqua, service_stretching,
                   service_boxing, service_trx])
        db.flush()
        
        print("   ✓ Услуги созданы")
        
        # Связи услуг и категорий (создаем после того, как и услуги, и категории созданы)
        variety_relations = [
            (category_group.id, service_yoga.id),
            (category_group.id, service_pilates.id),
            (category_group.id, service_spinning.id),
            (category_group.id, service_zumba.id),
            (category_group.id, service_crossfit.id),
            (category_group.id, service_stretching.id),
            (category_group.id, service_boxing.id),
            (category_group.id, service_trx.id),
            (category_personal.id, service_personal.id),
            (category_special.id, service_crossfit.id),
            (category_special.id, service_boxing.id),
            (category_aqua.id, service_aqua.id),
        ]
        
        for category_id, service_id in variety_relations:
            variety = VarietyServiceCategory(
                service_category_id=category_id,
                service_id=service_id
            )
            db.add(variety)
        
        db.flush()
        print("   ✓ Связи услуг и категорий созданы")
        
        # 2. Создаем пользователей с правильным bcrypt хешированием
        print("\nСоздание пользователей...")
        
        # Создание администратора
        admin_user = User(
            email="admin@fitness.ru",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_employee=True,
            is_superuser=True
        )
        db.add(admin_user)
        db.flush()
        
        print("   ✓ Администратор создан")
        
        # Создание сотрудников
        employees_data = [
            ("anna.ivanova@fitness.ru", "anna123", "Анна", "Иванова", position_manager.id, "+7 (913) 123-45-67", "anna.ivanova@fitness.ru", date(2020, 3, 15), fitness_center1.id),
            ("alex.smirnov@fitness.ru", "alex123", "Алексей", "Смирнов", position_trainer.id, "+7 (913) 234-56-78", "alex.smirnov@fitness.ru", date(2021, 5, 10), fitness_center1.id),
            ("maria.petrova@fitness.ru", "maria123", "Мария", "Петрова", position_receptionist.id, "+7 (913) 345-67-89", "maria.petrova@fitness.ru", date(2022, 8, 20), fitness_center2.id),
            ("sergey.volkov@fitness.ru", "sergey123", "Сергей", "Волков", position_trainer.id, "+7 (913) 456-78-90", "sergey.volkov@fitness.ru", date(2021, 9, 1), fitness_center1.id),
            ("elena.sokolova@fitness.ru", "elena123", "Елена", "Соколова", position_cleaner.id, "+7 (913) 567-89-01", "elena.sokolova@fitness.ru", date(2023, 1, 15), fitness_center2.id),
            ("dmitry.ivanov@fitness.ru", "dmitry123", "Дмитрий", "Иванов", position_director.id, "+7 (913) 678-90-12", "dmitry.ivanov@fitness.ru", date(2019, 6, 1), fitness_center1.id),
        ]
        
        employee_objects = []
        for email, password, first_name, last_name, position_id, phone, emp_email, emp_date, center_id in employees_data:
            user = User(
                email=email,
                hashed_password=get_password_hash(password),
                is_active=True,
                is_employee=True,
                is_superuser=False
            )
            db.add(user)
            db.flush()
            
            employee = Employee(
                first_name=first_name,
                last_name=last_name,
                position_id=position_id,
                phone=phone,
                email=emp_email,
                date_of_employment=emp_date,
                fitness_center_id=center_id,
                user_id=user.id
            )
            db.add(employee)
            db.flush()
            employee_objects.append(employee)
        
        print("   ✓ Сотрудники созданы")
        
        # Создание клиентов
        clients_data = [
            ("ivan.petrov@email.com", "ivan123", "Иван", "Петров", date(1990, 5, 15), "+7 (913) 789-01-23", "ivan.petrov@email.com", date(2023, 1, 10)),
            ("olga.sidorova@email.com", "olga123", "Ольга", "Сидорова", date(1995, 8, 22), "+7 (913) 890-12-34", "olga.sidorova@email.com", date(2023, 3, 5)),
            ("sergey.kuznetsov@email.com", "sergey123", "Сергей", "Кузнецов", date(1988, 11, 30), "+7 (913) 901-23-45", "sergey.kuznetsov@email.com", date(2024, 2, 15)),
            ("ekaterina.volkova@email.com", "ekaterina123", "Екатерина", "Волкова", date(1992, 3, 8), "+7 (913) 012-34-56", "ekaterina.volkova@email.com", date(2024, 4, 20)),
            ("alexander.popov@email.com", "alexander123", "Александр", "Попов", date(1985, 7, 12), "+7 (913) 123-45-67", "alexander.popov@email.com", date(2024, 1, 5)),
            ("natalia.morozova@email.com", "natalia123", "Наталия", "Морозова", date(1993, 9, 25), "+7 (913) 234-56-78", "natalia.morozova@email.com", date(2023, 11, 15)),
            ("maxim.kovalev@email.com", "maxim123", "Максим", "Ковалев", date(1991, 2, 14), "+7 (913) 345-67-89", "maxim.kovalev@email.com", date(2024, 3, 1)),
            ("anna.smirnova@email.com", "anna123", "Анна", "Смирнова", date(1994, 6, 30), "+7 (913) 456-78-90", "anna.smirnova@email.com", date(2023, 12, 20)),
        ]
        
        client_objects = []
        for email, password, first_name, last_name, birth_date, phone, client_email, reg_date in clients_data:
            user = User(
                email=email,
                hashed_password=get_password_hash(password),
                is_active=True,
                is_employee=False,
                is_superuser=False
            )
            db.add(user)
            db.flush()
            
            client = Client(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=birth_date,
                phone=phone,
                email=client_email,
                registration_date=reg_date,
                user_id=user.id
            )
            db.add(client)
            db.flush()
            client_objects.append(client)
        
        print("   ✓ Клиенты созданы")
        
        # 3. Создаем тренеров
        print("\nСоздание тренеров...")

        # Для тренеров Алексея Смирнова и Сергея Волкова используем уже созданных сотрудников
        trainer1 = Trainer(
            employee_id=employee_objects[1].id,  # Алексей Смирнов (индекс 1 в employee_objects)
            specialization_id=spec_crossfit.id,
            work_experience=5
        )
        trainer2 = Trainer(
            employee_id=employee_objects[3].id,  # Сергей Волков (индекс 3 в employee_objects)
            specialization_id=spec_bodybuilding.id,
            work_experience=10
        )

        # Создаем дополнительных сотрудников для остальных тренеров
        print("   Создание дополнительных сотрудников для тренеров...")

        additional_trainers_data = [
            ("elena.vasilieva@fitness.ru", "elena123", "Елена", "Васильева", position_trainer.id, 
            "+7 (913) 789-01-23", "elena.vasilieva@fitness.ru", date(2019, 8, 15), fitness_center1.id, spec_yoga.id, 8),
            
            ("dmitry.orlov@fitness.ru", "dmitry123", "Дмитрий", "Орлов", position_trainer.id, 
            "+7 (913) 890-12-34", "dmitry.orlov@fitness.ru", date(2020, 4, 10), fitness_center2.id, spec_cardio.id, 7),
            
            ("anna.kuznetsova@fitness.ru", "anna123", "Анна", "Кузнецова", position_trainer.id, 
            "+7 (913) 901-23-45", "anna.kuznetsova@fitness.ru", date(2021, 6, 20), fitness_center1.id, spec_dance.id, 6),
            
            ("igor.pavlov@fitness.ru", "igor123", "Игорь", "Павлов", position_trainer.id, 
            "+7 (913) 012-34-56", "igor.pavlov@fitness.ru", date(2018, 3, 5), fitness_center3.id, spec_rehab.id, 12),
        ]

        additional_trainer_objects = []
        for email, password, first_name, last_name, position_id, phone, emp_email, emp_date, center_id, spec_id, experience in additional_trainers_data:
            # Создаем пользователя
            user = User(
                email=email,
                hashed_password=get_password_hash(password),
                is_active=True,
                is_employee=True,
                is_superuser=False
            )
            db.add(user)
            db.flush()
            
            # Создаем сотрудника
            employee = Employee(
                first_name=first_name,
                last_name=last_name,
                position_id=position_id,
                phone=phone,
                email=emp_email,
                date_of_employment=emp_date,
                fitness_center_id=center_id,
                user_id=user.id
            )
            db.add(employee)
            db.flush()
            
            # Создаем тренера
            trainer = Trainer(
                employee_id=employee.id,
                specialization_id=spec_id,
                work_experience=experience
            )
            db.add(trainer)
            db.flush()
            
            additional_trainer_objects.append(trainer)

        print("   ✓ Дополнительные тренеры созданы")

        # Собираем всех тренеров
        trainers = [trainer1, trainer2] + additional_trainer_objects
        db.flush()
        print(f"   ✓ Всего создано тренеров: {len(trainers)}")

        # 4. Создаем подписки клиентов
        print("\nСоздание подписок клиентов...")
        
        client_subs = [
            (client_objects[0].id, subscription_premium.id, date(2024, 1, 1), date(2024, 12, 31), activity_active.id),
            (client_objects[1].id, subscription_basic.id, date(2024, 3, 1), date(2024, 9, 1), activity_active.id),
            (client_objects[2].id, subscription_vip.id, date(2024, 2, 15), date(2025, 2, 15), activity_active.id),
            (client_objects[3].id, subscription_3months.id, date(2024, 5, 1), date(2024, 8, 1), activity_active.id),
            (client_objects[4].id, subscription_premium.id, date(2024, 1, 5), date(2024, 7, 5), activity_expired.id),
            (client_objects[5].id, subscription_year.id, date(2024, 1, 1), date(2025, 1, 1), activity_active.id),
            (client_objects[6].id, subscription_basic.id, date(2024, 4, 1), date(2024, 7, 1), activity_suspended.id),
            (client_objects[7].id, subscription_vip.id, date(2024, 3, 15), date(2024, 9, 15), activity_active.id),
        ]
        
        for client_id, sub_id, start_date, end_date, activity_id in client_subs:
            client_sub = ClientSubscription(
                client_id=client_id,
                subscription_id=sub_id,
                start_action_date=start_date,
                end_action_date=end_date,
                subscription_activity_id=activity_id
            )
            db.add(client_sub)
        
        db.flush()
        print("   ✓ Подписки клиентов созданы")
        
        # 5. Создаем тренировки
        print("\nСоздание тренировок...")
        today = date.today()
        
        # Используем индексы наших тренеров
        workouts_data = [
            # Сегодня
            (room1_center1.id, trainer1.id, service_crossfit.id, today, time(9, 0), time(10, 0), 15, 5),
            (room2_center1.id, additional_trainer_objects[0].id, service_yoga.id, today, time(10, 30), time(11, 30), 20, 8),  # Елена Васильева
            (room1_center1.id, trainer1.id, service_personal.id, today, time(14, 0), time(15, 0), 1, 1),
            (room3_center1.id, trainer1.id, service_spinning.id, today, time(18, 0), time(18, 45), 25, 12),
            (room2_center1.id, additional_trainer_objects[2].id, service_zumba.id, today, time(19, 0), time(20, 0), 25, 15),  # Анна Кузнецова
            
            # Завтра
            (room1_center1.id, trainer1.id, service_crossfit.id, today + timedelta(days=1), time(8, 0), time(9, 0), 15, 3),
            (room3_center1.id, trainer1.id, service_spinning.id, today + timedelta(days=1), time(10, 0), time(10, 45), 25, 4),
            (room4_center1.id, additional_trainer_objects[3].id, service_boxing.id, today + timedelta(days=1), time(12, 0), time(13, 0), 15, 7),  # Игорь Павлов
            (room1_center2.id, additional_trainer_objects[1].id, service_pilates.id, today + timedelta(days=1), time(14, 0), time(15, 0), 20, 10),  # Дмитрий Орлов
            (room2_center1.id, trainer2.id, service_trx.id, today + timedelta(days=1), time(16, 0), time(17, 0), 12, 8),
            (room2_center1.id, additional_trainer_objects[2].id, service_zumba.id, today + timedelta(days=1), time(18, 0), time(19, 0), 25, 12),  # Анна Кузнецова
            (room1_center3.id, additional_trainer_objects[2].id, service_zumba.id, today + timedelta(days=1), time(19, 30), time(20, 30), 35, 22),  # Анна Кузнецова
        ]
        
        workout_objects = []
        for room_id, trainer_id, service_id, workout_date, start_time, end_time, max_capacity, current_reg in workouts_data:
            workout = Workout(
                room_id=room_id,
                trainer_id=trainer_id,
                service_id=service_id,
                workout_date=workout_date,
                start_time=start_time,
                end_time=end_time,
                max_persons_capacity=max_capacity,
                current_number_of_recorded=current_reg
            )
            db.add(workout)
            db.flush()
            workout_objects.append(workout)
        
        print("   ✓ Тренировки созданы")
        
        # 6. Создаем записи на тренировки
        print("\nСоздание записей на тренировки...")
        
        records_data = [
            (workout_objects[0].id, client_objects[0].id, today, time(8, 30)),
            (workout_objects[0].id, client_objects[2].id, today, time(8, 45)),
            (workout_objects[1].id, client_objects[1].id, today, time(9, 0)),
            (workout_objects[3].id, client_objects[0].id, today, time(17, 30)),
            (workout_objects[4].id, client_objects[3].id, today, time(10, 0)),
        ]
        
        for workout_id, client_id, record_date, record_time in records_data:
            record = ClientRecord(
                workout_id=workout_id,
                client_id=client_id,
                record_date=record_date,
                record_time=record_time
            )
            db.add(record)
        
        db.flush()
        print("   ✓ Записи на тренировки созданы")
        
        # 7. Создаем отзывы
        print("\nСоздание отзывов...")
        
        feedbacks = [
            (trainer1.id, client_objects[0].id, 5, "Отличный тренер! Очень профессионален и мотивирует.", today - timedelta(days=10)),
            (additional_trainer_objects[0].id, client_objects[1].id, 4, "Хорошие занятия йогой, очень расслабляющая атмосфера.", today - timedelta(days=15)),  # Елена Васильева
            (trainer1.id, client_objects[2].id, 5, "Лучший тренер по кроссфиту в городе!", today - timedelta(days=5)),
        ]
        
        for trainer_id, client_id, mark, comment, feedback_date in feedbacks:
            feedback = Feedback(
                trainer_id=trainer_id,
                client_id=client_id,
                mark=mark,
                comment=comment,
                feedback_date=feedback_date
            )
            db.add(feedback)
        
        db.flush()
        print("   ✓ Отзывы созданы")
        
        # 8. Создаем отпуска и зарплаты
        print("\nСоздание отпусков и зарплатных ведомостей...")
        
        # Отпуска
        vacation1 = Vacation(
            employee_id=employee_objects[1].id,
            start_date=date(2024, 7, 1),
            end_date=date(2024, 7, 14),
            type_of_vacation_id=vacation_annual.id
        )
        db.add(vacation1)
        
        # Зарплатные ведомости
        salaries = [
            (employee_objects[0].id, "Июнь", 2024, 80000.00, 5000.00, 0.00, 85000.00, date(2024, 7, 5)),
            (employee_objects[1].id, "Июнь", 2024, 50000.00, 3000.00, 0.00, 53000.00, date(2024, 7, 5)),
        ]
        
        for employee_id, month, year, salary, bonus, penalty, total, payment_date in salaries:
            salary_stmt = SalaryStatement(
                employee_id=employee_id,
                month_period=month,
                year_period=year,
                salary=salary,
                bonus=bonus,
                penalty=penalty,
                total_amount=total,
                date_of_payment=payment_date
            )
            db.add(salary_stmt)
        
        # Финальный коммит
        db.commit()
        
        print("\n" + "="*60)
        print("✅ База данных успешно заполнена тестовыми данными!")
        print("="*60)
        
        print("\n=== Созданные тестовые данные ===")
        print(f"Фитнес-центров: 3")
        print(f"Залы: 8")
        print(f"Оборудование: 15")
        print(f"Услуг: 10")
        print(f"Пользователей: 15 (1 админ, 6 сотрудников, 8 клиентов)")
        print(f"Тренеров: 6")
        print(f"Подписок: 5 типов")
        print(f"Активных подписок клиентов: 8")
        print(f"Тренировок в расписании: 12")
        print(f"Записей на тренировки: 5")
        print(f"Отзывов: 3")
        
        print("\n=== Тестовые учетные данные ===")
        print("Администратор: admin@fitness.ru / admin123")
        print("Сотрудник (менеджер): anna.ivanova@fitness.ru / anna123")
        print("Сотрудник (тренер): alex.smirnov@fitness.ru / alex123")
        print("Клиент: ivan.petrov@email.com / ivan123")
        print("Клиент: olga.sidorova@email.com / olga123")
        print("Клиент: sergey.kuznetsov@email.com / sergey123")
        
        print("\n=== Для тестирования API ===")
        print("ID комнаты для отчета по оборудованию: 1-8")
        print("ID тренировки для отчета по записям: 1-12")
        print(f"Даты для отчета по расписанию: {today} - {today + timedelta(days=1)}")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка при заполнении базы данных: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()