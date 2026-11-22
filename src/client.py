import requests


def build_chat_payload(prompt: str, model: str = "LLaMA_CPP", max_tokens: int = 64) -> dict:
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    return {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }


def check_health(base_url: str, timeout: float = 5.0) -> bool:
    response = requests.get(f"{base_url}/v1/models", timeout=timeout)
    return response.status_code == 200
