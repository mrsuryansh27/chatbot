from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.api_key import APIKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.auth import get_master_key
from app.database import get_db
from app.schemas import ClientCreate, ClientOut
from app.models import Client

router = APIRouter(tags=["clients"])

@router.post("", response_model=ClientOut)
async def create_client(
    payload: ClientCreate,
    _: APIKey = Depends(get_master_key),
    db: AsyncSession = Depends(get_db)
):
    client = Client(**payload.dict())
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client

@router.get("/{client_id}", response_model=ClientOut)
async def get_client(client_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Client).where(Client.client_id == client_id))
    client = result.scalars().first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client
