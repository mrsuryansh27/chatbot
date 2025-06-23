# app/models.py
import uuid
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id         = Column(Integer, primary_key=True, index=True)
    client_id  = Column(String, unique=True, index=True, default=lambda: uuid.uuid4().hex[:8])
    api_key    = Column(String, unique=True, default=lambda: uuid.uuid4().hex)
    name       = Column(String, nullable=False)
    domain     = Column(String, nullable=False)
    branding   = Column(JSONB, nullable=False)  # ← switched from Text to JSONB :contentReference[oaicite:0]{index=0}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    leads      = relationship("Lead", back_populates="client")

class Lead(Base):
    __tablename__ = "leads"

    id         = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name       = Column(String, nullable=False)
    phone      = Column(String, nullable=False)
    email      = Column(String, nullable=False, index=True)
    client_id  = Column(Integer, ForeignKey("clients.id"))
    client     = relationship("Client", back_populates="leads")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
