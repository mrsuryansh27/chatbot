# app/database.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 1) load DATABASE_URL (dotenv should have run before)
DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    # fallback if somehow missing
    DATABASE_URL = "sqlite:///db.sqlite3"

# 2) async engine only
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "false").lower() == "true",
)

# 3) session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 4) Base for models
Base = declarative_base()

# 5) dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
