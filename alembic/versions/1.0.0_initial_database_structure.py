"""Initial database structure

Revision ID: 1.0.0
Revises:
Create Date: 2021-09-30 12:47:00.182978

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Enum

from api.models.enums import UserType, AccomplishmentType, UserContactType, EthicType, PatientSource
from api.models.uuid import UUID

# revision identifiers, used by Alembic.
revision = "1.0.0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "addresses",
        sa.Column("id", UUID(), primary_key=True, default=uuid.uuid4()),
        sa.Column("street_1", sa.String(250), nullable=False),
        sa.Column("street_2", sa.String(250), nullable=True),
        sa.Column("city", sa.String(250), nullable=False),
        sa.Column("state", sa.String(250), nullable=False),
        sa.Column("zip", sa.String(20), nullable=False),
        sa.Column("country_code", sa.String(12), nullable=True),
        sa.Column("deleted", sa.BOOLEAN, default=False),
    )

    op.create_table(
        "users",
        # sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("id", UUID(), primary_key=True, default=uuid.uuid4()),
        sa.Column("first_name", sa.types.String(250), nullable=False, index=True),
        sa.Column("last_name", sa.types.String(250), nullable=False, index=True),
        sa.Column("middle_name", sa.types.String(250), nullable=False, index=True),
        sa.Column("username", sa.types.String(250), nullable=False, index=True),
        sa.Column("password", sa.types.String(250), nullable=False),
        sa.Column("type", Enum(UserType), nullable=False),
        sa.Column("deleted", sa.BOOLEAN, default=False),
    )

    op.create_table(
        "investigators",
        sa.Column("id", UUID(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("address_id", UUID, sa.ForeignKey("addresses.id"),  nullable=True, index=True),
        sa.Column("deleted", sa.BOOLEAN, default=False),
    )
    op.create_table(
        "sponsors",
        sa.Column("id", UUID(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("title", sa.types.String(250), nullable=False),
        sa.Column("deleted", sa.BOOLEAN, default=False),
    )

    op.create_table(
        "degrees",
        sa.Column("id", UUID(), primary_key=True, default=uuid.uuid4()),
        sa.Column("name", sa.String(250), nullable=False, index=True),
        sa.Column("deleted", sa.BOOLEAN, default=False),
    )
    op.create_table(
        "specialties",
        sa.Column("id", UUID(), primary_key=True, default=uuid.uuid4()),
        sa.Column("name", sa.String(250), nullable=False, index=True),
        sa.Column("deleted", sa.BOOLEAN, default=False),
    )

    op.create_table(
        "user_accomplishments",
        sa.Column("id", UUID(), primary_key=True, default=uuid.uuid4()),
        sa.Column("user_id", UUID(), nullable=False, index=True),
        sa.Column("type", Enum(AccomplishmentType), nullable=False),
        sa.Column("deleted", sa.BOOLEAN, default=False),
    )

    op.create_table(
        "user_specialties",
        sa.Column("id", UUID(), sa.ForeignKey("user_accomplishments.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("specialty_id", UUID(), sa.ForeignKey("specialties.id", ondelete="CASCADE"), nullable=False),
    )
    op.create_table(
        "user_degrees",
        sa.Column("id", UUID(), sa.ForeignKey("user_accomplishments.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("degree_id", UUID(), sa.ForeignKey("degrees.id", ondelete="CASCADE"), nullable=False),
    )

    op.create_table(
        "roles",
        sa.Column("id", UUID(), primary_key=True, default=uuid.uuid4()),
        sa.Column("name", sa.String(250), nullable=False, index=True),
        sa.Column("active", sa.types.BOOLEAN, default=1),
        sa.Column("deleted", sa.BOOLEAN, default=False),
    )

    op.create_table(
        "networks",
        sa.Column("id", UUID(), primary_key=True, default=uuid.uuid4()),
        sa.Column("name", sa.String(250), nullable=False, index=True),
        sa.Column("deleted", sa.BOOLEAN, default=False),
    )

    op.create_table(
        "user_networks",
        sa.Column("user_id", UUID(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("network_id", UUID(), sa.ForeignKey("networks.id", ondelete="CASCADE"), nullable=False),
        sa.PrimaryKeyConstraint("user_id", "network_id"),
    )

    op.create_table(
        "user_contacts",
        sa.Column("id", UUID(), primary_key=True, default=uuid.uuid4()),
        sa.Column("user_id", UUID(), nullable=False, index=True),
        sa.Column("type", Enum(UserContactType), nullable=False),
        sa.Column("primary", sa.BOOLEAN, default=False),
        sa.Column("deleted", sa.BOOLEAN, default=False),
    )

    op.create_table(
        "user_emails",
        sa.Column("id", UUID(), sa.ForeignKey("user_contacts.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("email", sa.String(250), nullable=False),
    )
    op.create_table(
        "user_faxes",
        sa.Column("id", UUID(), sa.ForeignKey("user_contacts.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("fax_number", sa.String(250), nullable=False),
    )
    op.create_table(
        "user_phones",
        sa.Column("id", UUID(), sa.ForeignKey("user_contacts.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("phone_number", sa.String(250), nullable=False),
    )

    op.create_table(
        "user_roles",
        sa.Column("role_id",UUID(),sa.ForeignKey("roles.id", ondelete="CASCADE"),nullable=False,),
        sa.Column("user_id",UUID(),sa.ForeignKey("users.id", ondelete="CASCADE"),nullable=False,),
        sa.PrimaryKeyConstraint("role_id", "user_id"),
    )

    op.create_table(
        "facilities",
        sa.Column("id", UUID(), primary_key=True, default=uuid.uuid4()),
        sa.Column("name", sa.String(250), nullable=False),
        sa.Column("address_id", UUID, sa.ForeignKey("addresses.id", ondelete="CASCADE"), nullable=True, index=True),
        sa.Column("coordinator_id", UUID, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True),
        sa.Column("ethics_type", Enum(EthicType), nullable=False),
        sa.Column("can_use_central_irb", sa.BOOLEAN, nullable=True),
        sa.Column("in_patient_capabilities", sa.BOOLEAN, nullable=True),
        sa.Column("inpatient_beds", sa.INTEGER, nullable=True),
        sa.Column("icu_capabilities", sa.BOOLEAN, nullable=True),
        sa.Column("access_ventilators", sa.BOOLEAN, nullable=True),
        sa.Column("patient_source", Enum(PatientSource), nullable=True),
        sa.Column("referral_network", sa.BOOLEAN, nullable=True),
        sa.Column("patients_per_month", sa.INTEGER, nullable=True),
        sa.Column("deleted", sa.BOOLEAN, default=False),
    )

    op.create_table(
        "user_facilities",
        sa.Column("user_id", UUID(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("facility_id", UUID(), sa.ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("primary", sa.BOOLEAN, nullable=False, default=True),
        sa.PrimaryKeyConstraint("user_id", "facility_id"),
    )


def downgrade() -> None:
    op.drop_table("user_facilities")
    op.drop_table("facilities")
    op.drop_table("user_phones")
    op.drop_table("user_faxes")
    op.drop_table("user_emails")
    op.drop_table("user_contacts")
    op.drop_table("user_networks")
    op.drop_table("user_degrees")
    op.drop_table("user_specialties")
    op.drop_table("user_accomplishments")
    op.drop_table("specialties")
    op.drop_table("degrees")
    op.drop_table("sponsors")
    op.drop_table("investigators")
    op.drop_table("addresses")

    op.drop_table("user_roles")
    op.drop_table("roles")
    op.drop_table("users")
    op.drop_table("networks")

    sa.Enum(name='usertype').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='usercontacttype').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='accomplishmenttype').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='ethictype').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='patientsource').drop(op.get_bind(), checkfirst=False)
