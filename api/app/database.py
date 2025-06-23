from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine as create_sync_engine

from app.config import DATABASE_URL, settings

# Base metadata
Base = declarative_base()

# 1) Synchronous table creation at startup
sync_url = DATABASE_URL.replace("+asyncpg", "")
sync_engine = create_sync_engine(sync_url, echo=False)
Base.metadata.create_all(bind=sync_engine)

# 2) Async engine for FastAPI
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    poolclass=NullPool,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
