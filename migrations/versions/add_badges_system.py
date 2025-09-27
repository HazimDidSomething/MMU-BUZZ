"""add badges system

Revision ID: add_badges_system
Revises: add_karma_fields_to_user
Create Date: 2025-09-26 00:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_badges_system'
down_revision = 'add_karma_fields_to_user'
branch_labels = None
depends_on = None


def upgrade():
    # Create badges table
    op.create_table('badges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=200), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('color', sa.String(length=20), server_default='#6c757d', nullable=True),
        sa.Column('karma_threshold', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create user_badges junction table
    op.create_table('user_badges',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('badge_id', sa.Integer(), nullable=False),
        sa.Column('earned_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['badge_id'], ['badges.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'badge_id')
    )
    
    # Insert default badges
    op.execute("""
        INSERT INTO badges (name, description, icon, color, karma_threshold) VALUES
        ('Rising Star', 'First 100 karma milestone', 'bi-star-fill', '#ffc107', 100),
        ('Elite', 'Reached 500 karma', 'bi-sword', '#6f42c1', 500),
        ('Novice', 'Achieved 1000 karma', 'bi-gem', '#20c997', 1000),
        ('Legend', 'Master of 1500 karma', 'bi-trophy', '#dc3545', 1500),
        ('Elder', 'Ultimate 2500+ karma', 'bi-crown', '#6f42c1', 2500),
        ('Community Builder', 'Created your first community', 'bi-building', '#28a745', NULL),
        ('Streak Master', '7 day login streak', 'bi-lightning', '#fd7e14', NULL),
        ('Post Master', 'Created 10 posts', 'bi-pencil-square', '#17a2b8', NULL)
    """)


def downgrade():
    op.drop_table('user_badges')
    op.drop_table('badges')
