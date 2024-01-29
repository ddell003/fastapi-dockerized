import json
import os

from alembic import context
from sqlalchemy.orm import Session

from api.config import config
from api.db import SessionLocal
from ..schemas.investigator_schema import InvestigatorCreateSchema
from ..schemas.role import RoleCreateSchema
from ..services.role import create_role, connect_users
from ..services.users import investigator_service


def load_data_from_file(filepath: str, db: Session):
    with open(filepath, "r") as input_data:
        data = json.load(input_data)

        roles = {}

        for user in data["users"]:

            user["middle_name"] = ""
            user_id = investigator_service.create(
                db,
                InvestigatorCreateSchema(
                    **user
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


def run_seeder():
    db = SessionLocal()

    for file in sorted(os.listdir(config.init_data_path)):
        filepath = os.path.join(config.init_data_path, file)
        if filepath == "/opt/data/__pycache__":
            continue
        load_data_from_file(filepath, db)


if __name__ == "__main__":
    print("running loader")
    run_seeder()
