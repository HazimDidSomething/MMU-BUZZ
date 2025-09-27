"""Add anonymous mode features

Revision ID: add_anonymous_mode
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_anonymous_mode'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add anonymous fields to Posts table
    op.add_column('Posts', sa.Column('is_anonymous', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('Posts', sa.Column('anonymous_author_id', sa.Integer(), nullable=True))
    op.add_column('Posts', sa.Column('reveal_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('Posts', sa.Column('is_secret', sa.Boolean(), nullable=False, server_default='false'))
    
    # Add anonymous fields to PostComment table
    op.add_column('Posts_comment', sa.Column('is_anonymous', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('Posts_comment', sa.Column('anonymous_author_id', sa.Integer(), nullable=True))
    
    # Create Anonymous Polls table
    op.create_table('anonymous_polls',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('question', sa.String(500), nullable=False),
        sa.Column('options', sa.JSON(), nullable=False),
        sa.Column('is_multiple_choice', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['post_id'], ['Posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create Anonymous Poll Votes table
    op.create_table('anonymous_poll_votes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('poll_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),  # Nullable for truly anonymous votes
        sa.Column('selected_options', sa.JSON(), nullable=False),
        sa.Column('voted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('ip_hash', sa.String(64), nullable=True),  # For anonymous vote tracking
        sa.ForeignKeyConstraint(['poll_id'], ['anonymous_polls.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create Anonymous Reveals table for time-delayed reveals
    op.create_table('anonymous_reveals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('reveal_type', sa.String(50), nullable=False),  # 'time_delayed', 'moderator_approved', 'community_vote'
        sa.Column('scheduled_reveal_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('reveal_condition', sa.JSON(), nullable=True),  # Store conditions like vote threshold
        sa.Column('is_revealed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('revealed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['Posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop anonymous reveal table
    op.drop_table('anonymous_reveals')
    
    # Drop anonymous poll votes table
    op.drop_table('anonymous_poll_votes')
    
    # Drop anonymous polls table
    op.drop_table('anonymous_polls')
    
    # Remove anonymous fields from PostComment table
    op.drop_column('Posts_comment', 'anonymous_author_id')
    op.drop_column('Posts_comment', 'is_anonymous')
    
    # Remove anonymous fields from Posts table
    op.drop_column('Posts', 'is_secret')
    op.drop_column('Posts', 'reveal_date')
    op.drop_column('Posts', 'anonymous_author_id')
    op.drop_column('Posts', 'is_anonymous')
