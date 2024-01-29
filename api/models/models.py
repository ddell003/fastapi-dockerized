import uuid

from sqlalchemy.orm import relationship

from api.db import Base
from sqlalchemy import String, Integer, Column, ForeignKey, BOOLEAN, Table, Enum, and_

from api.models.enums import UserType, UserContactType
from api.models.uuid import UUID

BaseModel = Base

user_role_table = Table(
    "user_roles",
    BaseModel.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class User(BaseModel):
    __tablename__ = "users"
    id = Column(UUID(), primary_key=True, default=uuid.uuid4, )

    first_name = Column(String(250), nullable=False, index=False)
    last_name = Column(String(250), nullable=False, index=False)
    middle_name = Column(String(250), nullable=False, index=False)
    username = Column(String(250), nullable=False, index=True, unique=True)
    password = Column(String(250), nullable=False)
    type = Column(Enum(UserType), nullable=False)
    deleted = Column(BOOLEAN, default=False)

    roles = relationship("Role", secondary=user_role_table, back_populates="users")
    contacts = relationship("UserContact")
    emails = relationship("UserContact",primaryjoin="and_(User.id==UserContact.user_id, " "UserContact.type=='email')",lazy="joined")
    phone_numbers = relationship("UserContact",primaryjoin="and_(User.id==UserContact.user_id, " "UserContact.type=='phone')",lazy="joined")
    fax_numbers = relationship("UserContact",primaryjoin="and_(User.id==UserContact.user_id, " "UserContact.type=='fax')",lazy="joined")

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }


class Address(BaseModel):
    __tablename__ = "addresses"
    id = Column(UUID(), primary_key=True, default=uuid.uuid4, )

    street_1 = Column(String(250), nullable=False)
    street_2 = Column(String(250), nullable=True)
    city = Column(String(250), nullable=False)
    state = Column(String(250), nullable=False)
    zip = Column(String(20), nullable=False)
    country_code = Column(String(12), nullable=True)
    deleted = Column(BOOLEAN, default=False)


class Investigator(User):
    __tablename__ = "investigators"
    id = Column(UUID(), ForeignKey("users.id"), primary_key=True)
    address_id = Column(UUID(), ForeignKey("addresses.id"), nullable=True, index=True)

    __mapper_args__ = {
        'polymorphic_identity': UserType.investigator,
    }

    address = relationship("Address", lazy="joined", )


class Sponsor(User):
    __tablename__ = "sponsors"
    id = Column(UUID(), ForeignKey("users.id"), primary_key=True)
    title = Column(String(250), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': UserType.sponsor,
    }


class UserContact(BaseModel):
    __tablename__ = "user_contacts"
    id = Column(UUID(), primary_key=True, default=uuid.uuid4, )
    user_id = Column(UUID(), ForeignKey("users.id"), nullable=True, index=True)
    primary = Column(BOOLEAN, default=False)
    type = Column(Enum(UserContactType), nullable=False)
    deleted = Column(BOOLEAN, default=False)

    # roles = relationship("Role", secondary=user_role_table, back_populates="users")

    __mapper_args__ = {
        'polymorphic_identity': 'user_contact',
        'polymorphic_on': type
    }


class Email(UserContact):
    __tablename__ = "user_emails"
    id = Column(UUID(), ForeignKey("user_contacts.id"), primary_key=True)
    email = Column(String(250), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': UserContactType.email,
    }


class Fax(UserContact):
    __tablename__ = "user_faxes"
    id = Column(UUID(), ForeignKey("user_contacts.id"), primary_key=True)
    fax_number = Column(String(250), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': UserContactType.fax,
    }


class Phone(UserContact):
    __tablename__ = "user_phones"
    id = Column(UUID(), ForeignKey("user_contacts.id"), primary_key=True)
    phone_number = Column(String(250), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': UserContactType.phone,
    }


class Role(BaseModel):
    __tablename__ = "roles"
    id = Column(UUID(), primary_key=True, default=uuid.uuid4, )
    name = Column(String(250), nullable=False, index=True)
    active = Column(BOOLEAN, default=1)

    users = relationship("User", secondary=user_role_table, back_populates="roles")


class Degree(BaseModel):
    __tablename__ = "degrees"
    id = Column(UUID(), primary_key=True, default=uuid.uuid4, )
    name = Column(String(250), nullable=False, index=True)
    deleted = Column(BOOLEAN, default=False, index=True)


class Specialty(BaseModel):
    __tablename__ = "specialties"
    id = Column(UUID(), primary_key=True, default=uuid.uuid4, )
    name = Column(String(250), nullable=False, index=True)
    deleted = Column(BOOLEAN, default=False, index=True)


class Network(BaseModel):
    __tablename__ = "networks"
    id = Column(UUID(), primary_key=True, default=uuid.uuid4, )
    name = Column(String(250), nullable=False, index=True)
    deleted = Column(BOOLEAN, default=False, index=True)
