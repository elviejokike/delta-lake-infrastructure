from logging.config import fileConfig

from sqlalchemy import create_engine
from alembic import context

from alembic.ddl.impl import DefaultImpl
class TrinoImpl(DefaultImpl):
    __dialect__ = 'trino'
    transactional_ddl = False

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

engine = create_engine(config.get_main_option("sqlalchemy.url"))

# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=None)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
