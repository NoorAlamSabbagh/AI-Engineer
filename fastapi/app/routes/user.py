

from fastapi import APIRouter

from app.schemas.user import (
    UserResponse,
    UserCreate
)

from app.controllers.user import(
    add_user,
    get_users
)

router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "/",
    response_model=UserResponse
)
def create_user(request:UserCreate):
    return add_user(request)

@router.get(
    "/",
    response_model=list[UserResponse]
)
def fetch_users():
    return get_users()