from typing import Optional, List
from pydantic import BaseModel

from api.models.enums import UserType
from api.schemas.role import RoleSchema


class UserBaseSchema(BaseModel):
    """Represents a User object which will be returned to the UI"""

    first_name: str
    last_name: str
    middle_name: str
    username: Optional[str]
    password: Optional[str]


class UserSchema(UserBaseSchema):

    id: str
    roles: Optional[List[RoleSchema]] = []

    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    type: Optional[UserType] = UserType.basic
    pass


class UserListSchema(BaseModel):
    data: List[UserSchema]
    total_count: int


class UserPutRequestSchema(BaseModel):
    """
    Represents a User request object. This will be used for PUT operations when updating a user.
    The below represents the fields that can be updated
    """

    first_name: str
    last_name: str
    email: str
    active: bool
