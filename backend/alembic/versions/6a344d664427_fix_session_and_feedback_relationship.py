"""fix_session_and_feedback_relationship

Revision ID: 6a344d664427
Revises: 07a8754a59e2
Create Date: 2024-08-11 14:07:55.506877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '6a344d664427'
down_revision: Union[str, None] = '07a8754a59e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def table_exists(conn, table_name):
    return inspect(conn).has_table(table_name)

def constraint_exists(conn, table_name, constraint_name):
    for fk in inspect(conn).get_foreign_keys(table_name):
        if fk['name'] == constraint_name:
            return True
    return False
def get_fk_constraint_name(conn, table_name, column_name):
    insp = inspect(conn)
    for fk in insp.get_foreign_keys(table_name):
        if column_name in fk['constrained_columns']:
            return fk['name']
    return None
def index_exists(conn, table_name, index_name):
    return any(idx['name'] == index_name for idx in inspect(conn).get_indexes(table_name))

def upgrade() -> None:
    conn = op.get_bind()
    
    # Handle generated_images table
    fk_name = get_fk_constraint_name(conn, 'generated_images', 'user_id')
    if fk_name:
        op.drop_constraint(fk_name, 'generated_images', type_='foreignkey')
    
    op.alter_column('generated_images', 'user_id',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=36),
               existing_nullable=True)
    
    op.create_foreign_key(
        fk_name, 'generated_images', 'users',
        ['user_id'], ['user_id'],
        ondelete='CASCADE'
    )
    
    # Handle 'sessions' to 'session' renaming
    if table_exists(conn, 'sessions') and not table_exists(conn, 'session'):
        op.rename_table('sessions', 'session')
    elif table_exists(conn, 'sessions') and table_exists(conn, 'session'):
        # Both tables exist, merge data
        op.execute('INSERT IGNORE INTO session SELECT * FROM sessions')
        op.drop_table('sessions')
    elif not table_exists(conn, 'session'):
        # Create 'session' table if it doesn't exist
        op.create_table('session',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.String(length=36), nullable=True),
            sa.Column('start_time', sa.DateTime(), nullable=True),
            sa.Column('end_time', sa.DateTime(), nullable=True),
            sa.Column('status', sa.String(length=50), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

    # Update 'session' table structure
    with op.batch_alter_table('session') as batch_op:
        batch_op.alter_column('user_id', existing_type=sa.Integer(), type_=sa.String(length=36))

    # Handle foreign key constraints
    if constraint_exists(conn, 'feedback', 'feedback_ibfk_2'):
        op.drop_constraint('feedback_ibfk_2', 'feedback', type_='foreignkey')
    op.create_foreign_key('feedback_ibfk_2', 'feedback', 'session', ['session_id'], ['id'])

    if constraint_exists(conn, 'session', 'sessions_ibfk_1'):
        op.drop_constraint('sessions_ibfk_1', 'session', type_='foreignkey')
    if not constraint_exists(conn, 'session', 'session_ibfk_1'):
        op.create_foreign_key('session_ibfk_1', 'session', 'users', ['user_id'], ['user_id'])

    # Create indexes if they don't exist
    if not index_exists(conn, 'session', 'ix_session_id'):
        op.create_index(op.f('ix_session_id'), 'session', ['id'], unique=False)
    if not index_exists(conn, 'ai_personalities', 'ix_ai_personalities_id'):
        op.create_index(op.f('ix_ai_personalities_id'), 'ai_personalities', ['id'], unique=False)
    if not index_exists(conn, 'entity', 'ix_entity_entity_name'):
        op.create_index(op.f('ix_entity_entity_name'), 'entity', ['entity_name'], unique=False)
    if not index_exists(conn, 'entity', 'ix_entity_id'):
        op.create_index(op.f('ix_entity_id'), 'entity', ['id'], unique=False)
    if not index_exists(conn, 'feedback', 'ix_feedback_id'):
        op.create_index(op.f('ix_feedback_id'), 'feedback', ['id'], unique=False)
    if not index_exists(conn, 'generated_images', 'ix_generated_images_id'):
        op.create_index(op.f('ix_generated_images_id'), 'generated_images', ['id'], unique=False)
    if not index_exists(conn, 'generated_images', 'ix_generated_images_prompt'):
        op.create_index(op.f('ix_generated_images_prompt'), 'generated_images', ['prompt'], unique=False)
    if not index_exists(conn, 'generated_images', 'ix_generated_images_prompt_id'):
        op.create_index(op.f('ix_generated_images_prompt_id'), 'generated_images', ['prompt_id'], unique=True)
    if not index_exists(conn, 'intent', 'ix_intent_id'):
        op.create_index(op.f('ix_intent_id'), 'intent', ['id'], unique=False)
    if not index_exists(conn, 'intent', 'ix_intent_intent_name'):
        op.create_index(op.f('ix_intent_intent_name'), 'intent', ['intent_name'], unique=False)
    if not index_exists(conn, 'interaction', 'ix_interaction_id'):
        op.create_index(op.f('ix_interaction_id'), 'interaction', ['id'], unique=False)
    if not index_exists(conn, 'messages', 'ix_messages_id'):
        op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)
    if not index_exists(conn, 'messages', 'ix_messages_timestamp'):
        op.create_index(op.f('ix_messages_timestamp'), 'messages', ['timestamp'], unique=False)
    if not index_exists(conn, 'messages', 'ix_messages_user_id'):
        op.create_index(op.f('ix_messages_user_id'), 'messages', ['user_id'], unique=False)
    if not index_exists(conn, 'user_preferences', 'ix_user_preferences_id'):
        op.create_index(op.f('ix_user_preferences_id'), 'user_preferences', ['id'], unique=False)
    if not index_exists(conn, 'users', 'ix_users_email'):
        op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    if not index_exists(conn, 'users', 'ix_users_id'):
        op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    if not index_exists(conn, 'users', 'ix_users_username'):
        op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Alter columns
    op.alter_column('entity', 'entity_name',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=True)
    op.alter_column('feedback', 'message_id',
               existing_type=mysql.VARCHAR(length=36),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('generated_images', 'user_id',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=36),
               existing_nullable=True)
    op.alter_column('intent', 'intent_name',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=True)
    op.alter_column('messages', 'timestamp',
               existing_type=mysql.FLOAT(),
               type_=sa.DateTime(),
               existing_nullable=True)

    # Drop and create foreign keys
    if constraint_exists(conn, 'generated_images', 'generated_images_ibfk_1'):
        op.drop_constraint('generated_images_ibfk_1', 'generated_images', type_='foreignkey')
    op.create_foreign_key(None, 'generated_images', 'users', ['user_id'], ['user_id'])

    # Drop indexes
    if index_exists(conn, 'generated_images', 'prompt_id'):
        op.drop_index('prompt_id', table_name='generated_images')
    if index_exists(conn, 'generated_images', 'prompt_id_2'):
        op.drop_index('prompt_id_2', table_name='generated_images')
    if index_exists(conn, 'users', 'email'):
        op.drop_index('email', table_name='users')
    if index_exists(conn, 'users', 'username'):
        op.drop_index('username', table_name='users')

def downgrade() -> None:
    conn = op.get_bind()
    
     # Handle generated_images table
    fk_name = get_fk_constraint_name(conn, 'generated_images', 'user_id')
    if fk_name:
        op.drop_constraint(fk_name, 'generated_images', type_='foreignkey')
    
    op.alter_column('generated_images', 'user_id',
               existing_type=sa.String(length=36),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    
    op.create_foreign_key(
        fk_name, 'generated_images', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )

    # Revert foreign key constraints
    if constraint_exists(conn, 'feedback', 'feedback_ibfk_2'):
        op.drop_constraint('feedback_ibfk_2', 'feedback', type_='foreignkey')
    if constraint_exists(conn, 'session', 'session_ibfk_1'):
        op.drop_constraint('session_ibfk_1', 'session', type_='foreignkey')

    # Rename 'session' back to 'sessions'
    if table_exists(conn, 'session'):
        op.rename_table('session', 'sessions')

    # Revert 'sessions' table structure
    with op.batch_alter_table('sessions') as batch_op:
        batch_op.alter_column('user_id', existing_type=sa.String(length=36), type_=sa.Integer())

    # Recreate original foreign key constraints
    op.create_foreign_key('sessions_ibfk_1', 'sessions', 'users', ['user_id'], ['id'])
    op.create_foreign_key('feedback_ibfk_2', 'feedback', 'sessions', ['session_id'], ['id'])

    # Drop indexes if they exist
    if index_exists(conn, 'sessions', 'ix_session_id'):
        op.drop_index(op.f('ix_session_id'), table_name='sessions')
    if index_exists(conn, 'users', 'ix_users_username'):
        op.drop_index(op.f('ix_users_username'), table_name='users')
    if index_exists(conn, 'users', 'ix_users_id'):
        op.drop_index(op.f('ix_users_id'), table_name='users')
    if index_exists(conn, 'users', 'ix_users_email'):
        op.drop_index(op.f('ix_users_email'), table_name='users')
    if index_exists(conn, 'user_preferences', 'ix_user_preferences_id'):
        op.drop_index(op.f('ix_user_preferences_id'), table_name='user_preferences')
    if index_exists(conn, 'messages', 'ix_messages_user_id'):
        op.drop_index(op.f('ix_messages_user_id'), table_name='messages')
    if index_exists(conn, 'messages', 'ix_messages_timestamp'):
        op.drop_index(op.f('ix_messages_timestamp'), table_name='messages')
    if index_exists(conn, 'messages', 'ix_messages_id'):
        op.drop_index(op.f('ix_messages_id'), table_name='messages')
    if index_exists(conn, 'interaction', 'ix_interaction_id'):
        op.drop_index(op.f('ix_interaction_id'), table_name='interaction')
    if index_exists(conn, 'intent', 'ix_intent_intent_name'):
        op.drop_index(op.f('ix_intent_intent_name'), table_name='intent')
    if index_exists(conn, 'intent', 'ix_intent_id'):
        op.drop_index(op.f('ix_intent_id'), table_name='intent')
    if index_exists(conn, 'generated_images', 'ix_generated_images_prompt_id'):
        op.drop_index(op.f('ix_generated_images_prompt_id'), table_name='generated_images')
    if index_exists(conn, 'generated_images', 'ix_generated_images_prompt'):
        op.drop_index(op.f('ix_generated_images_prompt'), table_name='generated_images')
    if index_exists(conn, 'generated_images', 'ix_generated_images_id'):
        op.drop_index(op.f('ix_generated_images_id'), table_name='generated_images')
    if index_exists(conn, 'feedback', 'ix_feedback_id'):
        op.drop_index(op.f('ix_feedback_id'), table_name='feedback')
    if index_exists(conn, 'entity', 'ix_entity_id'):
        op.drop_index(op.f('ix_entity_id'), table_name='entity')
    if index_exists(conn, 'entity', 'ix_entity_entity_name'):
        op.drop_index(op.f('ix_entity_entity_name'), table_name='entity')
    if index_exists(conn, 'ai_personalities', 'ix_ai_personalities_id'):
        op.drop_index(op.f('ix_ai_personalities_id'), table_name='ai_personalities')

    # Create original indexes
    if not index_exists(conn, 'users', 'username'):
        op.create_index('username', 'users', ['username'], unique=True)
    if not index_exists(conn, 'users', 'email'):
        op.create_index('email', 'users', ['email'], unique=True)
    if not index_exists(conn, 'generated_images', 'prompt_id'):
        op.create_index('prompt_id', 'generated_images', ['prompt_id'], unique=True)
    if not index_exists(conn, 'generated_images', 'prompt_id_2'):
        op.create_index('prompt_id_2', 'generated_images', ['prompt_id'], unique=False)

    # Revert column changes
    op.alter_column('messages', 'timestamp',
               existing_type=sa.DateTime(),
               type_=mysql.FLOAT(),
               existing_nullable=True)
    op.alter_column('intent', 'intent_name',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)
    op.alter_column('generated_images', 'user_id',
               existing_type=sa.String(length=36),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    op.alter_column('feedback', 'message_id',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(length=36),
               existing_nullable=True)
    op.alter_column('entity', 'entity_name',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)

    # Revert foreign key changes
    if constraint_exists(conn, 'generated_images', None):
        op.drop_constraint(None, 'generated_images', type_='foreignkey')
    op.create_foreign_key('generated_images_ibfk_1', 'generated_images', 'users', ['user_id'], ['id'])