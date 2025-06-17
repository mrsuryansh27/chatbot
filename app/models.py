# app/models.py
from pydantic import BaseModel
from typing import List, Dict

class ChatRequest(BaseModel):
    session_id: str
    site_id: str
    message: str
    # New: full conversation so far, in LLM format
    history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    session_id: str
    reply: str
