

def pluralize_ball(n: int) -> str:
    if 11 <= n % 100 <= 14:
        return "баллов"
    elif n % 10 == 1:
        return "балл"
    elif 2 <= n % 10 <= 4:
        return "балла"
    else:
        return "баллов"

def limit_text(text: str, max_length: int) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def split_text(text: str, max_length: int = 1000) -> list[str]:
    parts = []
    while len(text) > max_length:
        part = text[:max_length]
        parts.append(part)
        text = text[max_length:]
    parts.append(text)
    return parts
