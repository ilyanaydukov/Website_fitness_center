# app/schemas/__init__.py
from .user import (
    UserBase, UserCreate, UserUpdate, UserInDB,
    Token, TokenData,
    ClientBase, ClientCreate, ClientUpdate, ClientInDB,
    EmployeeBase, EmployeeCreate, EmployeeInDB,
    PositionBase, PositionInDB
)

from .fitness import (
    FitnessCenterBase, FitnessCenterCreate, FitnessCenterInDB,
    RoomBase, RoomCreate, RoomInDB,
    EquipmentCategoryBase, EquipmentCategoryInDB,
    EquipmentBase, EquipmentCreate, EquipmentInDB,
    ServiceCategoryBase, ServiceCategoryInDB,
    ServiceBase, ServiceCreate, ServiceInDB,
    FeedbackBase, FeedbackCreate, FeedbackInDB,
    TrainerBase, TrainerCreate, TrainerInDB,
    TrainerSpecializationBase, TrainerSpecializationInDB
)

from .schedule import (
    WorkoutBase, WorkoutCreate, WorkoutUpdate, WorkoutInDB,
    ClientRecordBase, ClientRecordCreate, ClientRecordInDB
)

from .subscription import (
    SubscriptionAccessLevelBase, SubscriptionAccessLevelInDB,
    SubscriptionActivityBase, SubscriptionActivityInDB,
    SubscriptionBase, SubscriptionCreate, SubscriptionUpdate, SubscriptionInDB,
    ClientSubscriptionBase, ClientSubscriptionCreate, ClientSubscriptionInDB
)

__all__ = [
    # User schemas
    'UserBase', 'UserCreate', 'UserUpdate', 'UserInDB',
    'Token', 'TokenData',
    'ClientBase', 'ClientCreate', 'ClientUpdate', 'ClientInDB',
    'EmployeeBase', 'EmployeeCreate', 'EmployeeInDB',
    'PositionBase', 'PositionInDB',
    
    # Fitness schemas
    'FitnessCenterBase', 'FitnessCenterCreate', 'FitnessCenterInDB',
    'RoomBase', 'RoomCreate', 'RoomInDB',
    'EquipmentCategoryBase', 'EquipmentCategoryInDB',
    'EquipmentBase', 'EquipmentCreate', 'EquipmentInDB',
    'ServiceCategoryBase', 'ServiceCategoryInDB',
    'ServiceBase', 'ServiceCreate', 'ServiceInDB',
    'FeedbackBase', 'FeedbackCreate', 'FeedbackInDB',
    'TrainerBase', 'TrainerCreate', 'TrainerInDB',
    'TrainerSpecializationBase', 'TrainerSpecializationInDB',
    
    # Schedule schemas
    'WorkoutBase', 'WorkoutCreate', 'WorkoutUpdate', 'WorkoutInDB',
    'ClientRecordBase', 'ClientRecordCreate', 'ClientRecordInDB',
    
    # Subscription schemas
    'SubscriptionAccessLevelBase', 'SubscriptionAccessLevelInDB',
    'SubscriptionActivityBase', 'SubscriptionActivityInDB',
    'SubscriptionBase', 'SubscriptionCreate', 'SubscriptionUpdate', 'SubscriptionInDB',
    'ClientSubscriptionBase', 'ClientSubscriptionCreate', 'ClientSubscriptionInDB'
]