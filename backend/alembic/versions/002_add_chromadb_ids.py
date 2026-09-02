"""add chromadb_ids to portfolio

Revision ID: 002_add_chromadb_ids
Revises: 001_create_tables
Create Date: 2026-09-02 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision: str = '002_add_chromadb_ids'
down_revision: Union[str, None] = '001_create_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('portfolio', sa.Column('chromadb_ids', JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column('portfolio', 'chromadb_ids')
