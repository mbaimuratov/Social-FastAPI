"""merge heads

Revision ID: f079bad93ab4
Revises: 19025f91f1ea, c5691c263172
Create Date: 2024-08-16 16:19:34.801271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f079bad93ab4'
down_revision: Union[str, None] = ('19025f91f1ea', 'c5691c263172')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
