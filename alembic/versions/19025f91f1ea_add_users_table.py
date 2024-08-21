from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = '19025f91f1ea'
down_revision = '6ac47976d4c4'
branch_labels = None
depends_on = None

def upgrade():
    # Get the current connection
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Check if the 'users' table already exists
    if 'users' not in inspector.get_table_names():
        op.create_table(
            'users',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('username', sa.String, nullable=False),
            sa.Column('email', sa.String, nullable=False, unique=True),
            sa.Column('password', sa.String, nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False)
        )

def downgrade():
    op.drop_table('users')