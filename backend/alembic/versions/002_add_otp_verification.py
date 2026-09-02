"""replace verification_token with OTP fields

Revision ID: 002_add_otp_verification
Revises: 001_create_tables
Create Date: 2026-09-02 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = '002_add_otp_verification'
down_revision: Union[str, None] = '002_add_email_verification'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('otp', sa.String(6), nullable=True))
    op.add_column('users', sa.Column('otp_expires_at', sa.DateTime(), nullable=True))
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_column('verification_token')


def downgrade() -> None:
    op.add_column('users', sa.Column('verification_token', sa.String(255), nullable=True))
    op.drop_column('users', 'otp_expires_at')
    op.drop_column('users', 'otp')
