import uuid
from typing import List, Optional
from pydantic import BaseModel

from api.schemas.address_schema import AddressCreateSchema, AddressSchema
from api.schemas.user import UserBaseSchema
from api.schemas.user_contacts_schema import EmailCreateSchema, FaxCreateSchema, PhoneCreateSchema, EmailSchema, \
    FaxSchema, PhoneSchema


class InvestigatorBaseSchema(UserBaseSchema):
    """Represents a Degree object which will be returned to the UI"""

    pass


class InvestigatorSchema(InvestigatorBaseSchema):

    id: uuid.UUID
    address: Optional[AddressSchema]
    emails: Optional[List[EmailSchema]] = []
    fax_numbers: Optional[List[FaxSchema]] = []
    phone_numbers: Optional[List[PhoneSchema]] = []

    class Config:
        orm_mode = True


class UserAccomplishmentsCreateSchema(BaseModel):
    id: Optional[uuid.UUID]
    name: Optional[str]
    type: str


class InvestigatorCreateSchema(InvestigatorBaseSchema):
    address: Optional[AddressCreateSchema]
    emails: Optional[List[EmailCreateSchema]] = []
    fax_numbers: Optional[List[FaxCreateSchema]] = []
    phone_numbers: Optional[List[PhoneCreateSchema]] = []
    user_accomplishments: Optional[List[UserAccomplishmentsCreateSchema]]
    pass


class InvestigatorListSchema(BaseModel):
    data: List[InvestigatorSchema]
    total_count: int


class InvestigatorPutRequestSchema(BaseModel):
    """
    Represents a network request object. This will be used for PUT operations when updating a user.
    The below represents the fields that can be updated
    """
    name: str
