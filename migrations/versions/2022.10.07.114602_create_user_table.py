"""create user table

Revision ID: eff1744c85e7
Revises: 6f202fd77b28
Create Date: 2022-10-07 11:46:02.813297

"""
from datetime import datetime

import sqlalchemy as sa
from alembic import op
from app.infrastructure.adapters.postgres.models import UserRole

# revision identifiers, used by Alembic.
revision = 'eff1744c85e7'
down_revision = '6f202fd77b28'
branch_labels = None
depends_on = None


def upgrade() -> None:
    user_table = op.create_table('user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=80), unique=True, nullable=False),
        sa.Column('password', sa.String(length=250), nullable=False),
        sa.Column('role', sa.Enum(UserRole), default=UserRole.USER_ROLE),
        sa.Column('state', sa.SmallInteger, default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True, default=datetime.now),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, default=datetime.now),
        sa.PrimaryKeyConstraint('id')
    )

    op.bulk_insert(user_table,
        [
            {
                'name': 'admin',
                'email': 'admin@admin.com',
                'password': '$2b$12$ynjZtzZe4UzG5gQkPmD0cuf3AZxitdRw5Ko1ZZow2/CYYIH9ZiF7a',
                'role': 'ADMIN_ROLE'
            },
             {
                'name': 'user',
                'email': 'user@admin.com',
                'password': '$2b$12$2L2x.FhECHcxuUEzg/XDJup1aGCVQCLROgSp.27.kt1aE0OreTVyi',
                'role': 'USER_ROLE'
            },
        ]
    )


def downgrade() -> None:
    op.drop_table('user')
    sa.Enum(UserRole).drop(op.get_bind())
