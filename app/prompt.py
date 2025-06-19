def build_prompt(
    site_id: str,
    history: list[dict],
    chunks: list[dict],
    user_message: str,
) -> list[dict]:
    """
    Build a prompt sequence for the LLM including:
    1. System instruction defining travel guide role.
    2. All past conversation messages (history).
    3. Retrieved context chunks.
    4. The current user message.
    """
    # 1) System instruction
    system = {"role": "system", "content": f"You are a travel guide for {site_id}."}

    # 2) Conversation history
    history_msgs = [
        {"role": m["role"], "content": m["content"]}
        for m in history
    ] if history else []

    # 3) Contextual chunks from semantic search
    context_msgs = [
        {"role": "system", "content": f"{c['title']}: {c['text']}"}
        for c in chunks
    ] if chunks else []

    # 4) Current user message
    user_msg = {"role": "user", "content": user_message}

    # Combine into a single prompt message list
    return [system, *history_msgs, *context_msgs, user_msg]
