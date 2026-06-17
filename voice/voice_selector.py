from utils.language_detector import detect_language
from voice.voice_config import LANGUAGE_VOICES, DEFAULT_VOICE

def select_voice_for_text(text: str):
    lang = detect_language(text)

    voice_cfg = LANGUAGE_VOICES.get(lang, DEFAULT_VOICE)

    return {
        "language": lang,
        "voice": voice_cfg["voice"],
        "tts_lang": voice_cfg["tts_lang"]
    }

