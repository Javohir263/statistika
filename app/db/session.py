from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


# Async engine bazaga ulanadi
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,        # DEBUG=True bo'lsa SQL'larni terminalda ko'rsatadi
    pool_pre_ping=True,         # uzilgan ulanishlarni tekshiradi
    pool_size=5,                # parallel ulanishlar soni
    max_overflow=10,
)

# Session factory yaratish uchun
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,     # commit'dan keyin ham obyektlar bilan ishlash mumkin
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: har so'rov uchun database session beradi."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
