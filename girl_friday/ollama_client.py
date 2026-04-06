"""Ollama chat client."""
import ollama


def chat_with_ollama(
    user_input: str,
    model: str = "neural-chat",
    system_prompt: str | None = None,
) -> str:
    """
    Send a message to Ollama and return the response.

    Args:
        user_input: The user's message
        model: Ollama model name
        system_prompt: Optional system prompt to set context

    Returns:
        The model's response text
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_input})

    response = ollama.chat(model=model, messages=messages)
    return response["message"]["content"]
