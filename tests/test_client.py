from unittest.mock import Mock, patch

import pytest

from src.client import build_chat_payload, check_health

# komentarz
def test_build_chat_payload_valid():
    payload = build_chat_payload("Witaj", max_tokens=32)
    assert payload["model"] == "LLaMA_CPP"
    assert payload["max_tokens"] == 32
    assert payload["messages"][0]["content"] == "Witaj"


def test_build_chat_payload_empty():
    with pytest.raises(ValueError):
        build_chat_payload("   ")


@patch("src.client.requests.get")
def test_check_health_ok(mock_get):
    mock_get.return_value = Mock(status_code=200)
    assert check_health("http://192.168.100.162:8080") is True
