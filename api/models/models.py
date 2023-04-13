from sqlalchemy.orm import relationship

from api.db import Base
from sqlalchemy import String, Integer, Column, ForeignKey, BOOLEAN, Table

BaseModel = Base


user_role_table = Table(
    "user_roles",
    BaseModel.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

    first_name = Column(String(250), nullable=False, index=True)
    last_name = Column(String(250), nullable=False, index=True)
    username = Column(String(250), nullable=False, index=True, unique=True)
    email = Column(String(250), nullable=False, index=True)
    password = Column(String(250), nullable=False)
    active = Column(BOOLEAN, default=1)

    roles = relationship("Role", secondary=user_role_table, back_populates="users")


class Role(BaseModel):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, index=True)
    active = Column(BOOLEAN, default=1)

    users = relationship("User", secondary=user_role_table, back_populates="roles")
