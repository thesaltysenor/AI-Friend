def post_process_response(response: str) -> str:
    phrases_to_remove = [
        "As an AI language model,",
        "As an AI assistant,",
        "I'm an AI, so",
        "I don't have personal experiences,",
        "I don't have feelings,"
    ]
    for phrase in phrases_to_remove:
        response = response.replace(phrase, "")
    return response.strip()