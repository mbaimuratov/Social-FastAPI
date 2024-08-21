"""merge heads

Revision ID: 0b9d262a5ed1
Revises: a4c3a81774b8, dd7f4d2aeab3
Create Date: 2024-08-16 15:00:28.014116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b9d262a5ed1'
down_revision: Union[str, None] = ('dd7f4d2aeab3')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
