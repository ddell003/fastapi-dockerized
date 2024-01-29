import uuid
from typing import List
from pydantic import BaseModel


class SpecialtyBaseSchema(BaseModel):
    """Represents a Degree object which will be returned to the UI"""

    name: str


class SpecialtySchema(SpecialtyBaseSchema):

    id: uuid.UUID

    class Config:
        orm_mode = True


class SpecialtyCreateSchema(SpecialtyBaseSchema):
    pass


class SpecialtyListSchema(BaseModel):
    data: List[SpecialtySchema]
    total_count: int


class SpecialtyPutRequestSchema(BaseModel):
    """
    Represents a Degree request object. This will be used for PUT operations when updating a user.
    The below represents the fields that can be updated
    """
    name: str
