import uuid
from typing import Optional, List
from pydantic import BaseModel


class AddressBaseSchema(BaseModel):
    """Represents a Degree object which will be returned to the UI"""

    street_1: str
    street_2: Optional[str] = ""
    city: str
    state: str
    zip: str
    country_code: Optional[str]


class AddressSchema(AddressBaseSchema):

    id: uuid.UUID

    class Config:
        orm_mode = True


class AddressCreateSchema(AddressBaseSchema):
    pass


class AddressListSchema(BaseModel):
    data: List[AddressSchema]
    total_count: int


class AddressPutRequestSchema(BaseModel):
    """
    Represents a Degree request object. This will be used for PUT operations when updating a user.
    The below represents the fields that can be updated
    """
    name: str
