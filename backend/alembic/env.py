"""Alembic migration environment configuration.

This module contains the configuration for running database migrations
using Alembic with async SQLAlchemy support. It handles both online
(connected to database) and offline (SQL generation) migration modes.
"""

from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import asyncio
from app.core.config import get_settings

from app.database.models import Base

settings = get_settings()

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Set the target metadata from your models
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    """Execute migrations synchronously using the given connection.

    Args:
        connection: A synchronous database connection object
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    """Run migrations in 'online' mode using async engine.

    Creates an async engine and runs migrations through
    a synchronous adapter layer.
    """
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url")
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def run_migrations_online():
    """Run the migrations in online mode using asyncio event loop."""
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
