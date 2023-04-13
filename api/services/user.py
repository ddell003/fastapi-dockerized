from sqlalchemy.orm import Session

from ..dependencies.query_params import UserQueryParams
from ..models.models import User, Role
from ..schemas.user import UserCreateSchema


def create_user(db: Session, user_data: UserCreateSchema):
    # should bcrypt password here
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(connection: Session, user_id: int):
    return connection.query(User).filter(User.id == user_id).first()


def get_users(db: Session, params: UserQueryParams = None):

    # start of query builder
    query = db.query(User)

    apply_group = False

    # if no params we can end
    if not params:
        return query.all()

    # join example
    # query = query.join(Package, Package.id == PackageVersion.package_id)

    if params.q:
        # better way of doing this for users, you can provide a search on the concat of first, last name,
        # this is just to provide an example of how to search
        query = query.filter(User.first_name.like("%" + params.q + "%"))

    if params.roles or (params.sort and params.sort == "role"):
        query = query.join(User.roles)

    if params.roles:

        if len(params.roles) == 1:
            query = query.filter(Role.id == params.roles[0])
        elif type(params.roles) is list:
            query = query.filter(Role.id.in_(params.roles))

        apply_group = True

    if params.active is not None:
        query = query.filter(User.active == bool(params.active))

    # currently a limited search
    if params.sort in ["active", "email", "first_name", "last_name"]:
        # this lets us dynamically set what we want to sort by and the direction
        query = query.order_by(getattr(getattr(User, params.sort), params.direction)())
    elif params.sort == "role":
        query = query.order_by(getattr(getattr(Role, "name"), params.direction)())
        apply_group = True

    # if joins occur on pivot table, we need to apply a group by
    if apply_group:
        if params.sort == "role":
            query = query.group_by(User.id, Role.name)
        else:
            query = query.group_by(User.id)

    return query.all()
