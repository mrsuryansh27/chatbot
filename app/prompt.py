def build_prompt(site_id: str, chunks: list, user_message: str) -> list[dict]:
    system = {"role": "system", "content": f"You are a travel guide for {site_id}."}
    context = [
        {"role": "system", "content": f"{c['title']}: {c['text']}"}
        for c in chunks
    ] if chunks else []
    return [system, *context, {"role": "user", "content": user_message}]
