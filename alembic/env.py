"""Alembic migration environment.

Modellarni avtomatik aniqlash uchun:
- Base.metadata import qilinadi
- Barcha modellar import qilinadi (Base ularni topishi uchun)
- DATABASE_URL_SYNC settings'dan olinadi
"""
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Loyiha root'ini Python path'ga qo'shamiz
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings  # noqa: E402
from app.db.base import Base  # noqa: E402
from app.models import *  # noqa: F401, F403, E402

# Alembic Config
config = context.config

# DATABASE_URL_SYNC ni settings'dan olib qo'yamiz (sync URL — psycopg2)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL_SYNC)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Modellar metadata'si
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Offline rejim — SQL skript yaratadi, bazaga ulanmasdan."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Online rejim — bazaga ulanib, migratsiyalarni qo'llaydi."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()