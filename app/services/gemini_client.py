import httpx
from app.config import settings

gemini_client = httpx.AsyncClient(timeout=30)

async def generate_reply(payload: dict) -> str:
    resp = await gemini_client.post(settings.GEMINI_MODEL_URL, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]
