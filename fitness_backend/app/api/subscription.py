from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..auth.dependencies import get_current_active_user, get_current_client
from ..crud.subscription import (
    get_subscriptions, get_subscription,
    get_client_subscriptions, get_active_client_subscription
)
from ..crud.user import get_client_by_email
from ..schemas.subscription import SubscriptionInDB, ClientSubscriptionInDB

router = APIRouter(prefix="/api/v1/subscriptions", tags=["subscriptions"])

# Public endpoints
@router.get("/", response_model=List[SubscriptionInDB])
def read_subscriptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_subscriptions(db, skip=skip, limit=limit)

@router.get("/{subscription_id}", response_model=SubscriptionInDB)
def read_subscription(
    subscription_id: int,
    db: Session = Depends(get_db)
):
    subscription = get_subscription(db, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

# Client endpoints
@router.get("/my-subscriptions", response_model=List[ClientSubscriptionInDB])
def get_my_subscriptions(
    current_user = Depends(get_current_client),
    db: Session = Depends(get_db)
):
    client = get_client_by_email(db, email=current_user.email)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return get_client_subscriptions(db, client_id=client.id)

@router.get("/my-active-subscription", response_model=ClientSubscriptionInDB)
def get_my_active_subscription(
    current_user = Depends(get_current_client),
    db: Session = Depends(get_db)
):
    client = get_client_by_email(db, email=current_user.email)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    subscription = get_active_client_subscription(db, client_id=client.id)
    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription found")
    
    return subscription