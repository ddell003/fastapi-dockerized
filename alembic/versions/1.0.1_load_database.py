"""Load database

Revision ID: 1.0.1
Revises: 1.0.0
Create Date: 2021-09-30 13:06:24.921122

"""
import os

from alembic import context
from sqlalchemy.orm import Session

from api.config import config
from api.helpers.load_data import load_data_from_file

# revision identifiers, used by Alembic.
from api.models.models import user_role_table, User, Role

revision = "1.0.1"
down_revision = "1.0.0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # use the alembic connection to make sure migrations work as expected
    # without this, we end up with multiple db connections across multiple migrations
    # and this causes some issues with transactions

    db = Session(bind=context.get_bind())


    for file in sorted(os.listdir(config.init_data_path)):
        filepath = os.path.join(config.init_data_path, file)
        if filepath == "/opt/data/__pycache__":
            continue
        load_data_from_file(filepath, db)


def downgrade() -> None:
    # Delete all the data from all the tables
    db = Session(bind=context.get_bind())
    db.query(user_role_table).delete()
    db.query(User).delete()
    db.query(Role).delete()
    db.commit()
