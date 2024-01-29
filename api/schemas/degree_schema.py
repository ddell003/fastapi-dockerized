import uuid
from typing import Optional, List
from pydantic import BaseModel
from api.schemas.role import RoleSchema


class DegreeBaseSchema(BaseModel):
    """Represents a Degree object which will be returned to the UI"""

    name: str


class DegreeSchema(DegreeBaseSchema):

    id: uuid.UUID

    class Config:
        orm_mode = True


class DegreeCreateSchema(DegreeBaseSchema):
    pass


class DegreeListSchema(BaseModel):
    data: List[DegreeSchema]
    total_count: int


class DegreePutRequestSchema(BaseModel):
    """
    Represents a Degree request object. This will be used for PUT operations when updating a user.
    The below represents the fields that can be updated
    """
    name: str
