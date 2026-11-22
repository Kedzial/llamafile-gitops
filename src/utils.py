def format_prompt(system_msg: str, user_msg: str) -> str:
    return f"[SYSTEM]: {system_msg.strip()}\n[USER]: {user_msg.strip()}"
