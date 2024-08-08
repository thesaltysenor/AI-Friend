import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.models.image import GeneratedImage
from app.core.config import settings
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.models import Base
target_metadata = Base.metadata

def get_url():
    if os.environ.get("RUNNING_IN_DOCKER") == "true":
        return f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOSTNAME}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"
    else:
        # Use the exposed port when running from local machine
        return f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@localhost:3320/{settings.MYSQL_DB}"

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
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

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()