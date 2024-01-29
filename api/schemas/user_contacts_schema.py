import uuid
from typing import Optional, List
from pydantic import BaseModel


class EmailBaseSchema(BaseModel):
    email: str
    primary: bool


class EmailSchema(EmailBaseSchema):
    id: uuid.UUID

    class Config:
        orm_mode = True


class EmailCreateSchema(EmailBaseSchema):
    pass


class EmailPutRequestSchema(EmailBaseSchema):
    pass


'''Fax'''


class FaxBaseSchema(BaseModel):
    fax_number: str
    primary: bool


class FaxSchema(FaxBaseSchema):
    id: uuid.UUID

    class Config:
        orm_mode = True


class FaxCreateSchema(FaxBaseSchema):
    pass


class FaxPutRequestSchema(FaxBaseSchema):
    pass


'''Phone'''


class PhoneBaseSchema(BaseModel):
    phone_number: str
    primary: bool


class PhoneSchema(PhoneBaseSchema):
    id: uuid.UUID

    class Config:
        orm_mode = True


class PhoneCreateSchema(PhoneBaseSchema):
    pass


class PhonePutRequestSchema(PhoneBaseSchema):
    pass
