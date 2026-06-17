WAKE_WORDS = ["hey nova", "nova"]

def has_wake_word(text: str) -> bool:
    text = text.lower()
    return any(w in text for w in WAKE_WORDS)

def remove_wake_word(text: str) -> str:
    text = text.lower()
    for w in WAKE_WORDS:
        text = text.replace(w, "")
    return text.strip()
