DEFAULT_MODEL = "LLaMA_CPP"
DEFAULT_TIMEOUT = 10.0


def get_endpoint_url(host: str, port: int = 8080) -> str:
    return f"http://{host.strip()}:{port}/v1/chat/completions"
