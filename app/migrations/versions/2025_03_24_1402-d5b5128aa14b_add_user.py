"""add user

Revision ID: d5b5128aa14b
Revises: a3364b263fdd
Create Date: 2025-03-24 14:02:07.586135

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d5b5128aa14b"
down_revision: Union[str, None] = "a3364b263fdd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
