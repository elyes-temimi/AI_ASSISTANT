import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os
from faster_whisper import WhisperModel
from voice.state import voice_state

WAKE_WORDS = ["nova", "hey nova"]

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

SAMPLE_RATE = 16000
DURATION = 1.5  # seconds


def passive_listen_for_wake_word(agent, start_vc_callback):
    print("👂 Passive wake-word listener running...")

    while True:
        # Do NOTHING if VC is active
        if voice_state.is_vc_active():
            break

        try:
            # Record audio
            audio = sd.rec(
                int(SAMPLE_RATE * DURATION),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype=np.float32
            )
            sd.wait()

            # Create temp file (Windows-safe)
            fd, path = tempfile.mkstemp(suffix=".wav")
            os.close(fd)  # IMPORTANT

            wav.write(path, SAMPLE_RATE, audio)

            segments, _ = model.transcribe(
                path,
                language="en",
                beam_size=1
            )

            os.remove(path)  # cleanup

            text = " ".join(seg.text.lower() for seg in segments).strip()
            if not text:
                continue

            if any(w in text for w in WAKE_WORDS):
                print("🔔 Wake word detected!")
                start_vc_callback(agent)
                voice_state.exit_vc()
                
        except Exception as e:
            print("Wake listener error:", e)
