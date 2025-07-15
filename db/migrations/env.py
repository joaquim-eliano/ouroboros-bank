import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool, create_engine       # <-- importe create_engine
# retire o engine_from_config
# from sqlalchemy import engine_from_config

sys.path.append(os.path.abspath(os.getcwd()))

from config.settings import DATABASE_URL        # <-- importe a URL
from models.user import Base


# Configuração do Alembic
config = context.config

# Habilita logs definidos no alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define os metadados que o Alembic usará para detectar alterações no modelo
target_metadata = Base.metadata

def run_migrations_offline():
    """Executa as migrations no modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Executa as migrations no modo online, usando diretamente o DATABASE_URL."""
    # cria o engine direto do settings
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

# Decide qual modo usar
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
