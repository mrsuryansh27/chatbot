from fastapi import Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import Client
from app.config import settings

master_header = APIKeyHeader(name="X-MASTER-KEY")
user_header   = APIKeyHeader(name="X-API-KEY")

async def get_master_key(key: str = Security(master_header)) -> None:
    if key != settings.MASTER_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid master API key")

async def get_current_client(
    api_key: str = Security(user_header),
    db: AsyncSession = Depends(get_db)
) -> Client:
    result = await db.execute(select(Client).where(Client.api_key == api_key))
    client = result.scalars().first()
    if not client:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return client
