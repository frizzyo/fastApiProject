"""add user fname, sname, nname

Revision ID: 69339ab2afb8
Revises: d5b5128aa14b
Create Date: 2025-03-24 14:09:24.398036

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "69339ab2afb8"
down_revision: Union[str, None] = "d5b5128aa14b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users", sa.Column("first_name", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "users", sa.Column("second_name", sa.String(length=100), nullable=True)
    )
    op.add_column("users", sa.Column("nickname", sa.String(length=100), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "nickname")
    op.drop_column("users", "second_name")
    op.drop_column("users", "first_name")
