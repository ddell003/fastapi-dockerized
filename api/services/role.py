from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.models import Role, User, user_role_table
from ..schemas.role import RoleCreateSchema


def create_role(db: Session, role: RoleCreateSchema):
    item = Role(**role.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_roles(connection: Session):
    return (
        connection.query(
            Role.id, Role.name, Role.active, func.count(User.id).label("user_count")
        )
        .join(Role.users)
        .order_by(Role.name.desc())
        .group_by(Role)
        .all()
    )


def connect_users(connection: Session, role_id: int, user_id: int):

    lookup = (
        connection.query(user_role_table)
        .filter(user_role_table.c.user_id == user_id)
        .filter(user_role_table.c.role_id == role_id)
        .all()
    )

    if len(lookup) > 0:
        return False

    statement = user_role_table.insert().values(role_id=role_id, user_id=user_id)
    connection.execute(statement)
    connection.commit()
