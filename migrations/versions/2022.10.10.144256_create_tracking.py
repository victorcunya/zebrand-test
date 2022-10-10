"""create tracking

Revision ID: 7763d7d1915c
Revises: eff1744c85e7
Create Date: 2022-10-10 14:42:56.733006

"""
from datetime import datetime

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '7763d7d1915c'
down_revision = 'eff1744c85e7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('tracking',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('entity', sa.String(length=50), nullable=False),
        sa.Column('data_id', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True, default=datetime.now),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('tracking')
