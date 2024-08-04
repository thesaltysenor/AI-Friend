import os
from logging.config import fileConfig


from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.models.image import GeneratedImage

from app.core.config import settings
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", settings.get_database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from app.models import Base
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_url():
    if os.environ.get("RUNNING_IN_DOCKER") == "true":
        return settings.DATABASE_URL
    else:
        # Ensure this returns a valid SQLAlchemy connection string
        return f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@localhost:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"
    
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
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
    
    
# run this first  alembic revision --autogenerate -m "Add GeneratedImage model"