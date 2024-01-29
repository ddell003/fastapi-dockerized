from typing import Optional
from pydantic import BaseModel


class RoleBaseSchema(BaseModel):
    """Represents a Sprint object which will be returned to the UI"""

    name: str
    active: bool


class RoleSchema(RoleBaseSchema):
    """Represents a Sprint object which will be returned to the UI"""

    id: str
    user_count: Optional[int] = None

    class Config:
        orm_mode = True


class RoleCreateSchema(RoleBaseSchema):
    pass


class RoleUpdateSchema(RoleBaseSchema):
    pass
