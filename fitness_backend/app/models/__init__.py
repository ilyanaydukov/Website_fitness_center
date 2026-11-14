# Объединяем все модели в одном месте

from .user import (
    User, Client, Employee, Position, 
    Trainer, TrainerSpecialization,
    Vacation, TypeOfVacation, SalaryStatement
)

from .fitness import (
    FitnessCenter, Room, EquipmentCategory, Equipment,
    ServiceCategory, Service, VarietyServiceCategory, Feedback
)

from .schedule import Workout, ClientRecord

from .subscription import (
    SubscriptionAccessLevel, SubscriptionActivity,
    Subscription, ClientSubscription
)

__all__ = [
    'User', 'Client', 'Employee', 'Position',
    'Trainer', 'TrainerSpecialization',
    'Vacation', 'TypeOfVacation', 'SalaryStatement',
    'FitnessCenter', 'Room', 'EquipmentCategory', 'Equipment',
    'ServiceCategory', 'Service', 'VarietyServiceCategory', 'Feedback',
    'Workout', 'ClientRecord',
    'SubscriptionAccessLevel', 'SubscriptionActivity',
    'Subscription', 'ClientSubscription'
]