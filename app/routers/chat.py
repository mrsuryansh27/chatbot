from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas import ChatRequest, ChatResponse
from app.vector_store import query_similar
from app.prompt import build_prompt
from app.services.gemini_client import generate_reply

router = APIRouter(prefix="/api/chat", tags=["chat"])
# In-memory session history; consider moving to Redis or DB in prod
session_history: dict[str, list[dict]] = {}

@router.post("", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    bg: BackgroundTasks  # unused for now, but available for background tasks (e.g. logging)
):
    # 1) Retrieve or initialize session history
    hist = session_history.setdefault(req.session_id, [])
    hist.append({"role": "user", "content": req.message})

    # 2) Fetch semantic context
    try:
        chunks = query_similar(req.site_id, req.message)
    except Exception:
        chunks = []

    # 3) Build the full prompt (system, history, context, current)
    prompt_msgs = build_prompt(req.site_id, hist, chunks, req.message)

    # 4) Assemble Gemini payload
    system = {"parts": [{"text": prompt_msgs[0]["content"]}]}
    contents = [
        {
            "role": "user" if m["role"] == "user" else "model",
            "parts": [{"text": m["content"]}]
        }
        for m in prompt_msgs[1:]
    ]
    payload = {
        "systemInstruction": system,
        "contents": contents,
        "generationConfig": {"temperature": 0.7}
    }

    # 5) Call Gemini and handle errors
    try:
        reply = await generate_reply(payload)
    except Exception as e:
        raise HTTPException(502, detail=f"Chat service error: {e}")

    # 6) Record assistant’s reply for next turn
    hist.append({"role": "assistant", "content": reply})

    return ChatResponse(session_id=req.session_id, reply=reply)
