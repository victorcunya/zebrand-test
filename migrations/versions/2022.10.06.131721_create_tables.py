'''create tables

Revision ID: 6f202fd77b28
Revises: 
Create Date: 2022-10-06 13:17:21.304754

'''
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '6f202fd77b28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('product',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('sku', sa.String(length=30), unique=True, nullable=False),
        sa.Column('brand', sa.String(length=20), nullable=False),
        sa.Column('price', sa.Float(7,2), default='0,0'),
        sa.Column('state', sa.SmallInteger, default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('product')
