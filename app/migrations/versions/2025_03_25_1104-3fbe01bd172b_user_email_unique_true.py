"""user.email unique=true

Revision ID: 3fbe01bd172b
Revises: 69339ab2afb8
Create Date: 2025-03-25 11:04:45.026633

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "3fbe01bd172b"
down_revision: Union[str, None] = "69339ab2afb8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
