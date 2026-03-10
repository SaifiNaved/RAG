from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from database import Base

# Alembic Config
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def do_run_migrations(connection: Connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,  # useful for SQLite
        )

        async with context.begin_transaction():
            await context.run_migrations()

    import asyncio
    asyncio.run(do_run_migrations(connectable.connect()))

run_migrations_online()
