from typing import Optional, List
from pydantic import BaseModel
from api.schemas.role import RoleSchema


class UserBaseSchema(BaseModel):
    """Represents a User object which will be returned to the UI"""

    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    active: bool
    # active_date: date
    #  address: Optional[str]


class UserSchema(UserBaseSchema):

    id: int
    roles: Optional[List[RoleSchema]] = []

    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
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
