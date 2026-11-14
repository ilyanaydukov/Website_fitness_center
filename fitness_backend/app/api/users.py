from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..auth.dependencies import get_current_active_user, get_current_client
from ..crud.user import get_client, update_client, get_client_by_email
from ..schemas.user import ClientUpdate, ClientInDB

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("/profile", response_model=ClientInDB)
def get_profile(
    current_user = Depends(get_current_client),
    db: Session = Depends(get_db)
):
    client = get_client_by_email(db, email=current_user.email)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/profile", response_model=ClientInDB)
def update_profile(
    client_update: ClientUpdate,
    current_user = Depends(get_current_client),
    db: Session = Depends(get_db)
):
    client = get_client_by_email(db, email=current_user.email)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    updated_client = update_client(db, client_id=client.id, client_update=client_update)
    if not updated_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return updated_client