# app/schemas/subscription.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

class SubscriptionAccessLevelBase(BaseModel):
    access_level_name: str
    access_description: Optional[str] = None

class SubscriptionAccessLevelInDB(SubscriptionAccessLevelBase):
    id: int
    
    class Config:
        from_attributes = True

class SubscriptionActivityBase(BaseModel):
    status_name: str
    activity_flag: bool = True

class SubscriptionActivityInDB(SubscriptionActivityBase):
    id: int
    
    class Config:
        from_attributes = True

class SubscriptionBase(BaseModel):
    subscription_type: str
    price: Optional[float] = None
    validity_period: int
    subscription_access_level_id: int

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    subscription_type: Optional[str] = None
    price: Optional[float] = None
    validity_period: Optional[int] = None
    subscription_access_level_id: Optional[int] = None

class SubscriptionInDB(SubscriptionBase):
    id: int
    
    class Config:
        from_attributes = True

class ClientSubscriptionBase(BaseModel):
    client_id: int
    subscription_id: int
    start_action_date: date
    end_action_date: date
    subscription_activity_id: int

class ClientSubscriptionCreate(ClientSubscriptionBase):
    pass

class ClientSubscriptionInDB(ClientSubscriptionBase):
    id: int
    
    class Config:
        from_attributes = True