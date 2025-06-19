from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from app.database import async_session

router = APIRouter(prefix="/api/clients", tags=["clients"])

class ClientIn(BaseModel):
    name: str
    domain: str
    branding: dict

@router.post("/", status_code=201)
async def create_client(data: ClientIn):
    cid = uuid.uuid4().hex[:8]
    async with async_session() as session:
        await session.execute(
            "INSERT INTO clients (client_id,name,domain,branding) VALUES (:cid,:n,:d,:b)",
            {"cid": cid, "n": data.name, "d": data.domain, "b": data.branding}
        )
        await session.commit()
    return {"client_id": cid}

@router.get("/{cid}")
async def get_client(cid: str):
    async with async_session() as session:
        row = await session.execute(
            "SELECT client_id,branding FROM clients WHERE client_id=:cid",
            {"cid": cid}
        )
        client = row.fetchone()
    if not client:
        raise HTTPException(404, "Not found")
    return {"client_id": client.client_id, "branding": client.branding}
