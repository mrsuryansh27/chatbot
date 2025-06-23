# app/schemas.py
from pydantic import BaseModel, EmailStr, AnyUrl
from typing import Optional, List, Dict
from uuid import UUID

class Branding(BaseModel):
    welcomeMessage: str
    logoUrl: Optional[AnyUrl] = None
    colors: Optional[Dict[str, str]] = None

# Clients
class ClientCreate(BaseModel):
    name: str
    domain: str
    branding: Branding       # ← now expects a Branding object :contentReference[oaicite:1]{index=1}

class ClientOut(BaseModel):
    client_id: str
    api_key: str
    name: str
    domain: str
    branding: Branding       # ← outputs the structured branding

class ClientConfig(BaseModel):
    client_id: str
    branding: Branding

# Leads
class LeadCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr

class LeadOut(BaseModel):
    id: UUID
    name: str
    phone: str
    email: EmailStr

# Flights
class FlightSearch(BaseModel):
    origin: str
    destination: str
    depart_date: str
    return_date: Optional[str] = None
    adults: int

class FlightOffer(BaseModel):
    id: str
    price: float
    currency: str
    carrier: str
    depart_time: str
    arrive_time: str

# Chat
class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
