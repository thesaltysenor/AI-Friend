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

USERS_USER_ID = 'users.user_id'

def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    update_sessions_table(inspector)
    update_generated_images_table(inspector)
    update_ai_personalities_table(inspector)
    update_entity_table(inspector)
    update_feedback_table(inspector)
    update_intent_table(inspector)
    update_interaction_table(inspector)
    update_messages_table(inspector)
    update_sessions_table_indexes(inspector)
    update_user_preferences_table(inspector)
    update_users_table(inspector)

def update_sessions_table(inspector):
    fk_constraints = [fk['name'] for fk in inspector.get_foreign_keys('sessions')]
    if 'sessions_ibfk_1' in fk_constraints:
        op.drop_constraint('sessions_ibfk_1', 'sessions', type_='foreignkey')
    op.alter_column('sessions', 'user_id',
                    existing_type=mysql.INTEGER(),
                    type_=sa.String(length=36),
                    existing_nullable=True)
    op.create_foreign_key('sessions_ibfk_1', 'sessions', 'users', ['user_id'], ['user_id'])

def update_generated_images_table(inspector):
    existing_indexes = [index['name'] for index in inspector.get_indexes('generated_images')]
    drop_existing_indexes(existing_indexes, 'generated_images')
    create_new_indexes(existing_indexes, 'generated_images')

def drop_existing_indexes(existing_indexes, table_name):
    if 'prompt_id' in existing_indexes:
        op.drop_index('prompt_id', table_name=table_name)
    if 'prompt_id_2' in existing_indexes:
        op.drop_index('prompt_id_2', table_name=table_name)

def create_new_indexes(existing_indexes, table_name):
    new_indexes = [
        ('ix_generated_images_id', ['id'], False),
        ('ix_generated_images_prompt', ['prompt'], False),
        ('ix_generated_images_prompt_id', ['prompt_id'], True)
    ]
    for index_name, columns, unique in new_indexes:
        if index_name not in existing_indexes:
            op.create_index(index_name, table_name, columns, unique=unique)

def update_ai_personalities_table(inspector):
    if not any(idx['name'] == 'ix_ai_personalities_id' for idx in inspector.get_indexes('ai_personalities')):
        op.create_index('ix_ai_personalities_id', 'ai_personalities', ['id'], unique=False)

def update_entity_table(inspector):
    create_entity_indexes(inspector)
    op.alter_column('entity', 'entity_name',
                    existing_type=mysql.VARCHAR(length=255),
                    type_=sa.String(length=100),
                    existing_nullable=True)

def create_entity_indexes(inspector):
    entity_indexes = [
        ('ix_entity_entity_name', ['entity_name'], False),
        ('ix_entity_id', ['id'], False)
    ]
    for index_name, columns, unique in entity_indexes:
        if not any(idx['name'] == index_name for idx in inspector.get_indexes('entity')):
            op.create_index(index_name, 'entity', columns, unique=unique)

def update_feedback_table(inspector):
    if not any(idx['name'] == 'ix_feedback_id' for idx in inspector.get_indexes('feedback')):
        op.create_index('ix_feedback_id', 'feedback', ['id'], unique=False)
    op.alter_column('feedback', 'message_id',
                    existing_type=mysql.VARCHAR(length=36),
                    type_=sa.Integer(),
                    existing_nullable=True)

def update_intent_table(inspector):
    op.alter_column('intent', 'intent_name',
                    existing_type=mysql.VARCHAR(length=255),
                    type_=sa.String(length=100),
                    existing_nullable=True)
    create_intent_indexes(inspector)

def create_intent_indexes(inspector):
    intent_indexes = [
        ('ix_intent_id', ['id'], False),
        ('ix_intent_intent_name', ['intent_name'], False)
    ]
    for index_name, columns, unique in intent_indexes:
        if not any(idx['name'] == index_name for idx in inspector.get_indexes('intent')):
            op.create_index(index_name, 'intent', columns, unique=unique)

def update_interaction_table(inspector):
    if not any(idx['name'] == 'ix_interaction_id' for idx in inspector.get_indexes('interaction')):
        op.create_index('ix_interaction_id', 'interaction', ['id'], unique=False)

def update_messages_table(inspector):
    op.alter_column('messages', 'timestamp',
                    existing_type=mysql.FLOAT(),
                    type_=sa.DateTime(),
                    existing_nullable=True)
    create_messages_indexes(inspector)

def create_messages_indexes(inspector):
    messages_indexes = [
        ('ix_messages_id', ['id'], False),
        ('ix_messages_timestamp', ['timestamp'], False),
        ('ix_messages_user_id', ['user_id'], False)
    ]
    for index_name, columns, unique in messages_indexes:
        if not any(idx['name'] == index_name for idx in inspector.get_indexes('messages')):
            op.create_index(index_name, 'messages', columns, unique=unique)

def update_sessions_table_indexes(inspector):
    if not any(idx['name'] == 'ix_sessions_id' for idx in inspector.get_indexes('sessions')):
        op.create_index('ix_sessions_id', 'sessions', ['id'], unique=False)

def update_user_preferences_table(inspector):
    if not any(idx['name'] == 'ix_user_preferences_id' for idx in inspector.get_indexes('user_preferences')):
        op.create_index('ix_user_preferences_id', 'user_preferences', ['id'], unique=False)

def update_users_table(inspector):
    op.drop_index('email', table_name='users')
    op.drop_index('username', table_name='users')
    create_users_indexes(inspector)

def create_users_indexes(inspector):
    users_indexes = [
        ('ix_users_email', ['email'], True),
        ('ix_users_id', ['id'], False),
        ('ix_users_username', ['username'], True)
    ]
    for index_name, columns, unique in users_indexes:
        if not any(idx['name'] == index_name for idx in inspector.get_indexes('users')):
            op.create_index(index_name, 'users', columns, unique=unique)

def downgrade() -> None:
    # The downgrade function remains the same as in your original file
    # You may want to refactor it similarly to reduce complexity if needed
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