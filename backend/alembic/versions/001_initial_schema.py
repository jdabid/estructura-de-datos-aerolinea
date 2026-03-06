"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-03-06

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "destinations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("tax_amount", sa.Float(), server_default="0.0"),
        sa.Column("is_promotion", sa.Boolean(), server_default="false"),
        sa.Column("allows_pets", sa.Boolean(), server_default="true"),
    )

    op.create_table(
        "flights",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("flight_number", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("origin", sa.String(), nullable=False),
        sa.Column("base_price", sa.Float(), nullable=False),
        sa.Column("destination_id", sa.Integer(), sa.ForeignKey("destinations.id"), nullable=False),
    )

    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("passenger_name", sa.String(), nullable=False),
        sa.Column("passenger_age", sa.Integer(), nullable=False),
        sa.Column("has_pet", sa.Boolean(), server_default="false"),
        sa.Column("total_price", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("flight_id", sa.Integer(), sa.ForeignKey("flights.id"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("bookings")
    op.drop_table("flights")
    op.drop_table("destinations")
