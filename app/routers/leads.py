from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import LeadCreate, LeadOut
from app.models import Lead
from app.database import get_db

router = APIRouter(prefix="/api/leads", tags=["leads"])

@router.post("", response_model=LeadOut)
async def create_lead(lead: LeadCreate, db: AsyncSession = Depends(get_db)):
    new = Lead(**lead.dict())
    db.add(new)
    await db.commit()
    await db.refresh(new)
    return new
