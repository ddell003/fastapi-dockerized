from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.dependencies.query_params import UserQueryParams
from api.schemas.user import (
    UserListSchema,
    UserSchema,
    UserPutRequestSchema,
    UserCreateSchema,
)
from api.services import user as user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=UserListSchema)
def get_users(
    args: UserQueryParams = Depends(), db: Session = Depends(get_db)
) -> UserListSchema:
    users = user_service.get_users(db, args)
    return UserListSchema(data=users, total_count=len(users))


@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserSchema:
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int, user_data: UserPutRequestSchema, db: Session = Depends(get_db)
) -> UserSchema:

    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.first_name = user_data.first_name
    user.last_name = user_data.last_name
    user.email = user_data.email

    db.commit()
    """
    Updates a user
    """
    return user


@router.post("", response_model=UserSchema)
def create_user(
    user_data: UserCreateSchema, db: Session = Depends(get_db)
) -> UserSchema:
    user = user_service.create_user(db, user_data)
    return user
