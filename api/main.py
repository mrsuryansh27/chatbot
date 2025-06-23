from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import clients, leads, flights, chat, portal
from app.config import settings

app = FastAPI(title="Chatbot SaaS", version="1.0")

# CORS, etc.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount all routers under /v1 except portal
app.include_router(clients.router, prefix="/v1/clients")
app.include_router(leads.router, prefix="/v1/leads")
app.include_router(flights.router, prefix="/v1/flights")
app.include_router(chat.router, prefix="/v1/chat")

# mount the public-facing portal endpoint
app.include_router(portal.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
