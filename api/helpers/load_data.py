import json

from sqlalchemy.orm import Session

from ..schemas.role import RoleCreateSchema
from ..schemas.user import UserCreateSchema
from ..services.role import create_role, connect_users
from ..services.user import create_user


def load_data_from_file(filepath: str, db: Session):
    with open(filepath, "r") as input_data:
        data = json.load(input_data)

        roles = {}

        for user in data["users"]:
            # see if user exists, and create it if it doesent
            user_id = None
            user_id = create_user(
                db,
                UserCreateSchema(
                    first_name=user["first_name"],
                    last_name=user["first_name"],
                    email=user["email"],
                    username=user["email"],
                    active=user["active"],
                    # password=bcrypt.hashpw(user["password"].encode('utf-8'), bcrypt.gensalt())
                    password=user["password"],
                ),
            ).id

            for role in user["roles"]:
                role_id = None
                if role["name"] in roles.values():
                    role_id = list(roles.keys())[
                        list(roles.values()).index(str(role["name"]))
                    ]
                else:
                    new_role = create_role(
                        db, RoleCreateSchema(name=role["name"], active=1)
                    )
                    roles[new_role.id] = new_role.name
                    role_id = new_role.id
                    new_role = True

                # connect users
                connect_users(db, user_id=user_id, role_id=role_id)
