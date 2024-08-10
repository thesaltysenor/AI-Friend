"""Sync schema changes

Revision ID: 07a8754a59e2
Revises: 2eba091a54ca
Create Date: 2024-08-09 19:56:11.577987

"""
from typing import Sequence, Union
from sqlalchemy import inspect
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '07a8754a59e2'
down_revision: Union[str, None] = '2eba091a54ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    # Ensure the user_id column in sessions matches the user_id type in users
    # Drop the existing foreign key constraint first
    fk_constraints = [fk['name'] for fk in inspector.get_foreign_keys('sessions')]
    if 'sessions_ibfk_1' in fk_constraints:
        op.drop_constraint('sessions_ibfk_1', 'sessions', type_='foreignkey')

    # Modify the user_id column in the sessions table to match the user_id column in the users table
    op.alter_column('sessions', 'user_id',
                    existing_type=mysql.INTEGER(),
                    type_=sa.String(length=36),  # Make sure this matches the type and length in the users table
                    existing_nullable=True)

    # Recreate the foreign key constraint with the correct column types
    op.create_foreign_key('sessions_ibfk_1', 'sessions', 'users', ['user_id'], ['user_id'])

    # Continue with other schema changes...
    existing_indexes = [index['name'] for index in inspector.get_indexes('generated_images')]

    # Only drop the 'prompt_id' index if it exists
    if 'prompt_id' in existing_indexes:
        op.drop_index('prompt_id', table_name='generated_images')

    if 'prompt_id_2' in existing_indexes:
        op.drop_index('prompt_id_2', table_name='generated_images')

    # Create indexes if they don't exist
    if 'ix_generated_images_id' not in existing_indexes:
        op.create_index('ix_generated_images_id', 'generated_images', ['id'], unique=False)

    if 'ix_generated_images_prompt' not in existing_indexes:
        op.create_index('ix_generated_images_prompt', 'generated_images', ['prompt'], unique=False)

    if 'ix_generated_images_prompt_id' not in existing_indexes:
        op.create_index('ix_generated_images_prompt_id', 'generated_images', ['prompt_id'], unique=True)

    if 'ix_generated_images_prompt_id' not in existing_indexes:
        op.create_index('ix_generated_images_prompt_id', 'generated_images', ['prompt_id'], unique=True)
    if not any(idx['name'] == 'ix_ai_personalities_id' for idx in inspector.get_indexes('ai_personalities')):
        op.create_index('ix_ai_personalities_id', 'ai_personalities', ['id'], unique=False)

    if not any(idx['name'] == 'ix_entity_entity_name' for idx in inspector.get_indexes('entity')):
        op.create_index('ix_entity_entity_name', 'entity', ['entity_name'], unique=False)

    if not any(idx['name'] == 'ix_entity_id' for idx in inspector.get_indexes('entity')):
        op.create_index('ix_entity_id', 'entity', ['id'], unique=False)

    op.alter_column('entity', 'entity_name',
                    existing_type=mysql.VARCHAR(length=255),
                    type_=sa.String(length=100),
                    existing_nullable=True)

    if not any(idx['name'] == 'ix_feedback_id' for idx in inspector.get_indexes('feedback')):
        op.create_index('ix_feedback_id', 'feedback', ['id'], unique=False)

    op.alter_column('feedback', 'message_id',
                    existing_type=mysql.VARCHAR(length=36),
                    type_=sa.Integer(),
                    existing_nullable=True)

    op.alter_column('intent', 'intent_name',
                    existing_type=mysql.VARCHAR(length=255),
                    type_=sa.String(length=100),
                    existing_nullable=True)

    if not any(idx['name'] == 'ix_intent_id' for idx in inspector.get_indexes('intent')):
        op.create_index('ix_intent_id', 'intent', ['id'], unique=False)

    if not any(idx['name'] == 'ix_intent_intent_name' for idx in inspector.get_indexes('intent')):
        op.create_index('ix_intent_intent_name', 'intent', ['intent_name'], unique=False)

    if not any(idx['name'] == 'ix_interaction_id' for idx in inspector.get_indexes('interaction')):
        op.create_index('ix_interaction_id', 'interaction', ['id'], unique=False)

    op.alter_column('messages', 'timestamp',
                    existing_type=mysql.FLOAT(),
                    type_=sa.DateTime(),
                    existing_nullable=True)

    if not any(idx['name'] == 'ix_messages_id' for idx in inspector.get_indexes('messages')):
        op.create_index('ix_messages_id', 'messages', ['id'], unique=False)

    if not any(idx['name'] == 'ix_messages_timestamp' for idx in inspector.get_indexes('messages')):
        op.create_index('ix_messages_timestamp', 'messages', ['timestamp'], unique=False)

    if not any(idx['name'] == 'ix_messages_user_id' for idx in inspector.get_indexes('messages')):
        op.create_index('ix_messages_user_id', 'messages', ['user_id'], unique=False)

    if not any(idx['name'] == 'ix_sessions_id' for idx in inspector.get_indexes('sessions')):
        op.create_index('ix_sessions_id', 'sessions', ['id'], unique=False)

    if not any(idx['name'] == 'ix_user_preferences_id' for idx in inspector.get_indexes('user_preferences')):
        op.create_index('ix_user_preferences_id', 'user_preferences', ['id'], unique=False)

    op.drop_index('email', table_name='users')
    op.drop_index('username', table_name='users')

    if not any(idx['name'] == 'ix_users_email' for idx in inspector.get_indexes('users')):
        op.create_index('ix_users_email', 'users', ['email'], unique=True)

    if not any(idx['name'] == 'ix_users_id' for idx in inspector.get_indexes('users')):
        op.create_index('ix_users_id', 'users', ['id'], unique=False)

    if not any(idx['name'] == 'ix_users_username' for idx in inspector.get_indexes('users')):
        op.create_index('ix_users_username', 'users', ['username'], unique=True)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    # Reverse the sessions table's user_id column change
    op.alter_column('sessions', 'user_id',
                    existing_type=sa.String(length=36),
                    type_=mysql.INTEGER(),  # revert to original type if necessary
                    existing_nullable=True)

    # Drop and recreate the original foreign key
    op.drop_constraint('sessions_ibfk_1', 'sessions', type_='foreignkey')
    op.create_foreign_key('sessions_ibfk_1', 'sessions', 'users', ['user_id'], ['user_id'])

    # Recreate indexes if they were dropped
    existing_indexes = [index['name'] for index in inspector.get_indexes('generated_images')]

    if 'prompt_id' not in existing_indexes:
        op.create_index('prompt_id', 'generated_images', ['prompt_id'], unique=True)

    if 'prompt_id_2' not in existing_indexes:
        op.create_index('prompt_id_2', 'generated_images', ['prompt_id'], unique=False)
        
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_index('username', 'users', ['username'], unique=True)
    op.create_index('email', 'users', ['email'], unique=True)
    op.drop_index(op.f('ix_user_preferences_id'), table_name='user_preferences')
    op.drop_constraint(None, 'sessions', type_='foreignkey')
    op.create_foreign_key('sessions_ibfk_1', 'sessions', 'users', ['user_id'], ['id'])

    op.drop_index(op.f('ix_sessions_id'), table_name='sessions')
    op.alter_column('sessions', 'user_id',
                    existing_type=sa.String(length=36),  
                    type_=mysql.INTEGER(),
                    existing_nullable=True)

    op.drop_index(op.f('ix_messages_user_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_timestamp'), table_name='messages')
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.alter_column('messages', 'timestamp',
                    existing_type=sa.DateTime(),
                    type_=mysql.FLOAT(),
                    existing_nullable=True)
    op.drop_index(op.f('ix_interaction_id'), table_name='interaction')
    op.drop_index(op.f('ix_intent_intent_name'), table_name='intent')
    op.drop_index(op.f('ix_intent_id'), table_name='intent')
    op.alter_column('intent', 'intent_name',
                    existing_type=sa.String(length=100),
                    type_=mysql.VARCHAR(length=255),
                    existing_nullable=True)
    op.drop_constraint(None, 'generated_images', type_='foreignkey')
    op.create_foreign_key('generated_images_ibfk_1', 'generated_images', 'users', ['user_id'], ['id'])
    op.drop_index(op.f('ix_generated_images_prompt_id'), table_name='generated_images')
    op.drop_index(op.f('ix_generated_images_prompt'), table_name='generated_images')
    op.drop_index(op.f('ix_generated_images_id'), table_name='generated_images')
    op.create_index('prompt_id_2', 'generated_images', ['prompt_id'], unique=False)
    op.create_index('prompt_id', 'generated_images', ['prompt_id'], unique=True)
    op.alter_column('generated_images', 'user_id',
                    existing_type=sa.String(length=36),
                    type_=mysql.INTEGER(),
                    existing_nullable=True)
    op.drop_constraint(None, 'feedback', type_='foreignkey')
    op.drop_index(op.f('ix_feedback_id'), table_name='feedback')
    op.alter_column('feedback', 'message_id',
                    existing_type=sa.Integer(),
                    type_=mysql.VARCHAR(length=36),
                    existing_nullable=True)
    op.drop_index(op.f('ix_entity_id'), table_name='entity')
    op.drop_index(op.f('ix_entity_entity_name'), table_name='entity')
    op.alter_column('entity', 'entity_name',
                    existing_type=sa.String(length=100),
                    type_=mysql.VARCHAR(length=255),
                    existing_nullable=True)
    op.drop_index(op.f('ix_ai_personalities_id'), table_name='ai_personalities')
