# api/main.py

import os, sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# make sure dotenv + imports work
from dotenv import load_dotenv
PROJECT_ROOT = os.path.dirname(__file__)
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# ensure your code is on the path
sys.path.insert(0, PROJECT_ROOT)

from app.database import engine, Base
from app.config import settings
from app.routers import clients, leads, flights, chat, portal

app = FastAPI()

# CORS etc.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(portal.router)
app.include_router(clients.router, prefix="/v1/clients")
app.include_router(leads.router, prefix="/v1/leads")
app.include_router(flights.router, prefix="/v1/flights")
app.include_router(chat.router, prefix="/v1/chat")

# Create tables on startup, using the async engine
@app.on_event("startup")
async def on_startup():
    # run synchronous metadata.create_all inside an async transaction
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
