async def query_similar(site_id: str, text: str, top_k: int = 5) -> list[dict]:
    # TODO: replace with real embedding + Pinecone queries
    return []

class VectorStore:
    async def get_context(self, session_id: str) -> list[dict]:
        return await query_similar(None, session_id)

    async def save_message(self, session_id: str, user_msg: str, bot_msg: str):
        # TODO: store embeddings + raw text
        pass
