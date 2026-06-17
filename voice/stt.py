import sounddevice as sd
import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

def listen():
    print("▶ Press ENTER to start recording")
    input()
    print("⏺ Recording... Press ENTER to stop")

    audio_chunks = []

    def callback(indata, frames, time, status):
        audio_chunks.append(indata.copy())

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=callback
    )

    stream.start()
    input()
    stream.stop()
    stream.close()

    audio = np.concatenate(audio_chunks, axis=0)
    sf.write("voice_input.wav", audio, SAMPLE_RATE)

    segments, info = model.transcribe("voice_input.wav")

    text = " ".join(seg.text for seg in segments).strip()

    return {
        "text": text,
        "language": info.language
    }
