import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import uuid
import os


model = whisper.load_model("base")


def record_and_transcribe(seconds: int = 4, fs: int = 16000) -> str:
    """음성을 녹음하고 STT 후 텍스트만 반환"""
    filename = f"{uuid.uuid4()}.wav"

    print("Recording...")
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)
    print(f"Saved: {filename}")

    result = model.transcribe(filename)
    text = result["text"]

    # 파일 유지하고 싶으면 삭제하지 말 것
    # os.remove(filename)

    return text
