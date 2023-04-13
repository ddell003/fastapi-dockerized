"""Initial database structure

Revision ID: 1.0.0
Revises:
Create Date: 2021-09-30 12:47:00.182978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1.0.0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.types.String(250), nullable=False, index=True),
        sa.Column("last_name", sa.types.String(250), nullable=False, index=True),
        sa.Column("username", sa.types.String(250), nullable=False, index=True),
        sa.Column("email", sa.types.String(250), nullable=False),
        sa.Column("password", sa.types.String(250), nullable=False),
        sa.Column("active", sa.types.BOOLEAN, default=1),
    )

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(250), nullable=False, index=True),
        sa.Column("active", sa.types.BOOLEAN, default=1),
    )

    op.create_table(
        "user_roles",
        sa.Column(
            "role_id",
            sa.types.Integer,
            sa.ForeignKey("roles.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.types.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("role_id", "user_id"),
    )


def downgrade() -> None:
    op.drop_table("user_roles")
    op.drop_table("roles")
    op.drop_table("users")
