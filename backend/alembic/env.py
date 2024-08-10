from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.core.config import settings
import os
import sys

# Ensure the app directory is in the Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your models here to ensure Alembic recognizes them
from app.models import Base, User, Session, Feedback, Entity, GeneratedImage, Intent, Interaction, Message, UserPreference

# Set up target metadata for Alembic to use when generating migrations
target_metadata = Base.metadata

# Get the Alembic config object
config = context.config

# If a config file is specified, use it to configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL  # Ensure this URL handles Docker/non-Docker environments
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL  # Ensure the correct DB URL is used

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine if we are in 'offline' or 'online' mode and run the appropriate function
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
