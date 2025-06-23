def build_prompt(
    site_id: str,
    history: list[dict],
    chunks: list[dict],
    user_message: str,
) -> list[dict]:
    system = {"role": "system", "content": f"You are a travel guide for {site_id}."}

    history_msgs = [
        {"role": m["role"], "content": m["content"]} for m in history
    ] if history else []

    context_msgs = [
        {"role": "system", "content": f"{c['title']}: {c['text']}"}
        for c in chunks
    ] if chunks else []

    user_msg = {"role": "user", "content": user_message}
    return [system, *history_msgs, *context_msgs, user_msg]
