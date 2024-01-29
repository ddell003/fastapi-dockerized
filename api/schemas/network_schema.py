import uuid
from typing import List
from pydantic import BaseModel


class NetworkBaseSchema(BaseModel):
    """Represents a Degree object which will be returned to the UI"""

    name: str


class NetworkSchema(NetworkBaseSchema):

    id: uuid.UUID

    class Config:
        orm_mode = True


class NetworkCreateSchema(NetworkBaseSchema):
    pass


class NetworkListSchema(BaseModel):
    data: List[NetworkSchema]
    total_count: int


class NetworkPutRequestSchema(BaseModel):
    """
    Represents a network request object. This will be used for PUT operations when updating a user.
    The below represents the fields that can be updated
    """
    name: str
