from fastapi import APIRouter, Depends

from app.auth import get_current_client
from app.schemas import ChatRequest, ChatResponse
from app.vector_store import VectorStore
from app.prompt import build_prompt
from app.services.gemini_client import generate_reply

router = APIRouter(prefix="/v1/chat", tags=["chat"])

vs = VectorStore()

@router.post("", response_model=ChatResponse)
async def chat_endpoint(
    req: ChatRequest,
    current_client = Depends(get_current_client)
):
    history = await vs.get_context(req.session_id)
    prompt = build_prompt(current_client.client_id, history, [], req.message)
    reply = await generate_reply({"messages": prompt})
    await vs.save_message(req.session_id, req.message, reply)
    return ChatResponse(response=reply)
