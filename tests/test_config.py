from src.config import DEFAULT_MODEL, get_endpoint_url


def test_get_endpoint_url():
    url = get_endpoint_url("192.168.100.162")
    assert DEFAULT_MODEL == "LLaMA_CPP"
    assert url == "http://192.168.100.162:8080/v1/chat/completions"
