"""add last columns to posts

Revision ID: c5691c263172
Revises: 0b9d262a5ed1
Create Date: 2024-08-16 15:00:45.020325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5691c263172'
down_revision: Union[str, None] = '0b9d262a5ed1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean, server_default="true", nullable=False))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
