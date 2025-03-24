"""second_step

Revision ID: b04b79fde715
Revises: 3e1e03575127
Create Date: 2025-03-24 21:09:15.543738

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b04b79fde715'
down_revision: Union[str, None] = '3e1e03575127'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'alembic_table_1',
        sa.Column('id', sa.Integer),
        sa.Column('name', sa.String(50)),
        sa.Column('description', sa.String(50)),
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
