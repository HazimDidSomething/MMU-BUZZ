"""add karma fields to user

Revision ID: add_karma_fields_to_user
Revises: add_bookmarks_and_flairs
Create Date: 2025-09-26 00:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_karma_fields_to_user'
down_revision = 'add_bookmarks_and_flairs'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('karma', sa.Integer(), server_default='0', nullable=False))
    op.add_column('user', sa.Column('last_login_date', sa.Date(), nullable=True))
    op.add_column('user', sa.Column('login_streak', sa.Integer(), server_default='0', nullable=False))


def downgrade():
    op.drop_column('user', 'login_streak')
    op.drop_column('user', 'last_login_date')
    op.drop_column('user', 'karma')
