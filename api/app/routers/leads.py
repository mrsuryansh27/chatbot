from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_client
from app.database import get_db
from app.schemas import LeadCreate, LeadOut
from app.models import Lead

router = APIRouter(prefix="/v1/leads", tags=["leads"])

@router.post("", response_model=LeadOut)
async def create_lead(
    payload: LeadCreate,
    current_client = Depends(get_current_client),
    db: AsyncSession = Depends(get_db)
):
    lead = Lead(**payload.dict(), client_id=current_client.id)
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead
