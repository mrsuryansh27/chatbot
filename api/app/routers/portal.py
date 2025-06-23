from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from app.database import get_db
from app.models import Client as ClientModel
from app.schemas import ClientOut

router = APIRouter(prefix="/api", tags=["portal"])


class TenantCreate(BaseModel):
    name: str
    domain: str
    branding: dict  # this will match the JSONB column in your model


@router.post(
    "/create-tenant",
    response_model=ClientOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_tenant(
    payload: TenantCreate,
    db: AsyncSession = Depends(get_db),
):
    # Generate your own client_id/api_key logic if not in the model defaults:
    client = ClientModel(
        client_id=uuid4().hex[:8],
        api_key=uuid4().hex,
        name=payload.name,
        domain=payload.domain,
        branding=payload.branding,
    )
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client
