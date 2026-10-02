from app.schemas.user import UserCreate
from app.services.user import (
    create_user,
    get_users_service
)
from fastapi import HTTPException

def add_user(request:UserCreate):
    return create_user(
        request.name,
        request.email
    ) 

def get_users():
    try:
        users=get_users_service()
        return users
    except Exception as error:
        print(f"Error while fwetching users : {error}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch"
        )