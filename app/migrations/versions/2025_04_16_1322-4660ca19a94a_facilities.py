"""facilities

Revision ID: 4660ca19a94a
Revises: a361e60c145f
Create Date: 2025-04-16 13:22:07.074975

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4660ca19a94a"
down_revision: Union[str, None] = "a361e60c145f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rooms_facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=True),
        sa.Column("facilities_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["facilities_id"],
            ["facilities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("rooms_facilities")
    op.drop_table("facilities")
