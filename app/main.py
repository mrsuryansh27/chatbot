import os
import logging

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import httpx

from app.models import ChatRequest, ChatResponse
from app.vector_store import query_similar
from app.prompt import build_prompt  # signature: build_prompt(site_id, chunks, user_message)

# 1) Load .env and logging
load_dotenv()
logging.basicConfig(level=logging.INFO)

# 2) Google Gemini settings
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
    f"?key={GEMINI_KEY}"
)

# 3) FastAPI + CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["OPTIONS", "POST"],
    allow_headers=["*"],
)

# 4) Explicit OPTIONS for preflight
@app.options("/api/chat")
async def preflight_chat():
    return Response(status_code=200)

# 5) Chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    # a) Fetch context (synchronous list)
    try:
        chunks = query_similar(req.site_id, req.message)
    except Exception:
        logging.warning("Context retrieval failed; continuing without it", exc_info=True)
        chunks = []

    # b) Build your prompt messages list
    #    build_prompt(site_id, chunks, user_message) → List[{"role","content"}]
    prompt_messages = build_prompt(req.site_id, chunks, req.message)

    # c) Extract systemInstruction (first entry)
    system_instruction = {
        "parts": [{"text": prompt_messages[0]["content"]}]
    }

    # d) Convert the rest into contents[], adding required role fields
    contents = []
    for msg in prompt_messages[1:]:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    body = {
        "systemInstruction": system_instruction,
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7
        }
    }

    # e) Call Gemini
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(GEMINI_URL, json=body)
            resp.raise_for_status()
            data = resp.json()
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
        except httpx.HTTPStatusError as e:
            logging.error("Gemini HTTP error %s: %s", e.response.status_code, e.response.text)
            raise HTTPException(502, detail=f"Chat service error: {e.response.text}")
        except Exception:
            logging.exception("Unexpected error calling Gemini")
            raise HTTPException(500, detail="Internal server error.")

    return ChatResponse(session_id=req.session_id, reply=reply)
