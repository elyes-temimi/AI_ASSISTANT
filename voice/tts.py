from piper.voice import PiperVoice
import sounddevice as sd
import numpy as np
from voice.voice_selector import select_voice_for_text

VOICE_BY_LANG = {
    "en": "en_US",
    "fr": "fr_FR",
    "ru": "ru_RU",
    "ar": "ar"
}

voices = {}

def get_voice(lang):
    if lang not in voices:
        voices[lang] = PiperVoice.load(
            f"voices/{VOICE_BY_LANG.get(lang, 'en_US')}.onnx"
        )
    return voices[lang]


def speak(text):
    voice_data = select_voice_for_text(text)
    lang=voice_data["tts_lang"]
    voice = get_voice(lang)
    audio = voice.synthesize(text)
    
    audio_buffers = []

    for chunk in voice.synthesize(text):
        if hasattr(chunk, "audio_float_array"):
            audio_buffers.append(chunk.audio_float_array)

    if not audio_buffers:
        print("❌ No audio generated")
        return

    audio = np.concatenate(audio_buffers).astype(np.float32)

    sd.play(audio, samplerate=voice.config.sample_rate)
    sd.wait()
