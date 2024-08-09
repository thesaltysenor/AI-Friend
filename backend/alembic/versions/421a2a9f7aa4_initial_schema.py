"""Initial schema

Revision ID: 421a2a9f7aa4
Revises: 
Create Date: 2024-08-08 22:17:02.518092

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '421a2a9f7aa4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )

    # Create ai_personalities table
    op.create_table('ai_personalities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('personality_traits', sa.Text(), nullable=True),
        sa.Column('available', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('character_type', sa.String(50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create generated_images table
    op.create_table('generated_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('prompt', sa.String(255), nullable=True),
        sa.Column('prompt_id', sa.String(255), nullable=False),
        sa.Column('image_url', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('ai_personality_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['ai_personality_id'], ['ai_personalities.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('prompt_id')
    )

    # Add other table creations here...

def downgrade():
    op.drop_table('generated_images')
    op.drop_table('ai_personalities')
    op.drop_table('users')
    # Add other table drops here...