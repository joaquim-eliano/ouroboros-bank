"""
create users table

Revision ID: <revision>
Revises:
Create Date: YYYY-MM-DD HH:MM:SS
"""
from alembic import op
import sqlalchemy as sa
\# revision identifiers, used by Alembic.
revision = '<revision>'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('username', sa.String(), unique=True, nullable=False),
        sa.Column('email', sa.String(), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False)
    )


def downgrade():
    op.drop_table('users')