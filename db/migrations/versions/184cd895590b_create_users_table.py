"""Create users table

Revision ID: 184cd895590b
Revises: c3e10420c10c
Create Date: 2025-07-18 11:26:35.123209

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '184cd895590b'
down_revision: Union[str, Sequence[str], None] = 'c3e10420c10c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Use batch mode to support SQLite and other dialects
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column(
            'id',
            existing_type=sa.NUMERIC(),
            type_=sa.UUID(),
            existing_nullable=False
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column(
            'id',
            existing_type=sa.UUID(),
            type_=sa.NUMERIC(),
            existing_nullable=False
        )
