from sqlalchemy.orm import Session
from .. import models, schemas
from datetime import date, timedelta

# Subscription CRUD
def get_subscription(db: Session, subscription_id: int):
    return db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()

def get_subscriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subscription).offset(skip).limit(limit).all()

def create_subscription(db: Session, subscription: schemas.SubscriptionCreate):
    db_subscription = models.Subscription(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def update_subscription(db: Session, subscription_id: int, subscription_update: schemas.SubscriptionUpdate):
    db_subscription = get_subscription(db, subscription_id)
    if not db_subscription:
        return None
    
    update_data = subscription_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_subscription, field, value)
    
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def delete_subscription(db: Session, subscription_id: int):
    db_subscription = get_subscription(db, subscription_id)
    if db_subscription:
        db.delete(db_subscription)
        db.commit()
    return db_subscription

# Client Subscription CRUD
def create_client_subscription(db: Session, client_subscription: schemas.ClientSubscriptionCreate):
    db_client_subscription = models.ClientSubscription(**client_subscription.dict())
    db.add(db_client_subscription)
    db.commit()
    db.refresh(db_client_subscription)
    return db_client_subscription

def get_client_subscriptions(db: Session, client_id: int):
    return db.query(models.ClientSubscription).filter(models.ClientSubscription.client_id == client_id).all()

def get_active_client_subscription(db: Session, client_id: int):
    today = date.today()
    return db.query(models.ClientSubscription).filter(
        models.ClientSubscription.client_id == client_id,
        models.ClientSubscription.start_action_date <= today,
        models.ClientSubscription.end_action_date >= today,
        models.SubscriptionActivity.activity_flag == True
    ).join(models.SubscriptionActivity).first()