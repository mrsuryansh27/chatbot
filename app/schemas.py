from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
import uuid

class LeadCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr

class LeadOut(LeadCreate):
    id: uuid.UUID
    created_at: datetime

class ChatRequest(BaseModel):
    site_id: str
    session_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    reply: str

class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    departure_date: str
    return_date: Optional[str] = None
    adults: int

class FlightOffer(BaseModel):
    id: str
    total_amount: float
    currency: str
    departure_airport: str
    arrival_airport: str
    departure_time: str
    arrival_time: str
