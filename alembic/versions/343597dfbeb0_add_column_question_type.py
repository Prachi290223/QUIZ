"""add column question_type

Revision ID: 343597dfbeb0
Revises: 
Create Date: 2025-08-22 14:22:49.554872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '343597dfbeb0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('questions',sa.Column('question_type',sa.String(30)))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('questions','question_type')
