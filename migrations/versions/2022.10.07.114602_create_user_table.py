"""create user table

Revision ID: eff1744c85e7
Revises: 6f202fd77b28
Create Date: 2022-10-07 11:46:02.813297

"""
import sqlalchemy as sa
from alembic import op
from app.infrastructure.adapters.postgres.models import UserRole

# revision identifiers, used by Alembic.
revision = 'eff1744c85e7'
down_revision = '6f202fd77b28'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=80), nullable=False),
        sa.Column('password', sa.String(length=250), nullable=False),
        sa.Column('role', sa.Enum(UserRole), default=UserRole.user_role),
        sa.Column('state', sa.SmallInteger, default='1'),
        sa.PrimaryKeyConstraint('id')
    )



def downgrade() -> None:
    op.drop_table('user')
