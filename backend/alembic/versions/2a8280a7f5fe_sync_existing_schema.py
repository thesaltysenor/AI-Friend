"""Sync existing schema

Revision ID: 2a8280a7f5fe
Revises: 421a2a9f7aa4
Create Date: 2024-08-08 22:19:29.881198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision: str = '2a8280a7f5fe'
down_revision: Union[str, None] = '421a2a9f7aa4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Modify users table
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('user_id', existing_type=mysql.VARCHAR(length=36), nullable=False)
        batch_op.alter_column('username', existing_type=mysql.VARCHAR(length=50), nullable=False)
        batch_op.alter_column('email', existing_type=mysql.VARCHAR(length=255), nullable=False)
        batch_op.alter_column('hashed_password', existing_type=mysql.VARCHAR(length=255), nullable=False)
        batch_op.alter_column('is_active', existing_type=mysql.TINYINT(display_width=1), nullable=False, server_default=sa.text('1'))

    # Modify or create ai_personalities table
    op.create_table('ai_personalities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('personality_traits', sa.Text(), nullable=True),
        sa.Column('available', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('character_type', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Modify or create generated_images table
    op.create_table('generated_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('prompt', sa.String(length=255), nullable=True),
        sa.Column('prompt_id', sa.String(length=255), nullable=False),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('ai_personality_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['ai_personality_id'], ['ai_personalities.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('prompt_id')
    )

def downgrade():
    # This downgrade function is simplified and may not be fully reversible
    op.drop_table('generated_images')
    op.drop_table('ai_personalities')
    
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('is_active', existing_type=mysql.TINYINT(display_width=1), nullable=True)
        batch_op.alter_column('hashed_password', existing_type=mysql.VARCHAR(length=255), nullable=True)
        batch_op.alter_column('email', existing_type=mysql.VARCHAR(length=255), nullable=True)
        batch_op.alter_column('username', existing_type=mysql.VARCHAR(length=50), nullable=True)
        batch_op.alter_column('user_id', existing_type=mysql.VARCHAR(length=36), nullable=True)