from src.utils import format_prompt


def test_format_prompt():
    result = format_prompt("  Be helpful  ", "  Hello  ")
    assert result == "[SYSTEM]: Be helpful\n[USER]: Hello"
