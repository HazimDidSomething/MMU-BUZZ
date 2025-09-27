"""add bookmarks and flairs

Revision ID: add_bookmarks_and_flairs
Revises: e0d5bbb6f345
Create Date: 2023-09-26 16:30:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_bookmarks_and_flairs'
down_revision = 'e0d5bbb6f345'
branch_labels = None
depends_on = None


def upgrade():
    # Create community_flairs table
    op.create_table(
        'community_flairs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('color', sa.String(length=20), server_default='#6c757d', nullable=True),
        sa.Column('community_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['community_id'], ['communities.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Prevent duplicate flair names within the same community
    op.create_unique_constraint('uq_flair_name_per_community', 'community_flairs', ['community_id', 'name'])
    # Helpful index for listing flairs by community
    op.create_index('ix_community_flairs_community_id', 'community_flairs', ['community_id'])

    # Create bookmarks table
    op.create_table(
        'bookmarks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['post_id'], ['Posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Ensure one bookmark per user per post
    op.create_unique_constraint('uq_bookmarks_user_post', 'bookmarks', ['user_id', 'post_id'])
    # Helpful indexes for filtering
    op.create_index('ix_bookmarks_user_id', 'bookmarks', ['user_id'])
    op.create_index('ix_bookmarks_post_id', 'bookmarks', ['post_id'])

    # Add flair_id column to Posts table
    op.add_column('Posts', sa.Column('flair_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_posts_flair_id', 'Posts', 'community_flairs', ['flair_id'], ['id'], ondelete='SET NULL')
    op.create_index('ix_posts_flair_id', 'Posts', ['flair_id'])


def downgrade():
    # Drop Posts -> community_flairs relation first
    op.drop_index('ix_posts_flair_id', table_name='Posts')
    op.drop_constraint('fk_posts_flair_id', 'Posts', type_='foreignkey')
    op.drop_column('Posts', 'flair_id')

    # Drop bookmarks and its indexes/constraints
    op.drop_index('ix_bookmarks_post_id', table_name='bookmarks')
    op.drop_index('ix_bookmarks_user_id', table_name='bookmarks')
    op.drop_constraint('uq_bookmarks_user_post', 'bookmarks', type_='unique')
    op.drop_table('bookmarks')

    # Drop community_flairs and its indexes/constraints
    op.drop_index('ix_community_flairs_community_id', table_name='community_flairs')
    op.drop_constraint('uq_flair_name_per_community', 'community_flairs', type_='unique')
    op.drop_table('community_flairs')
