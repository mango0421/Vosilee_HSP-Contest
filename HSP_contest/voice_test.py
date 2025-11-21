import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import uuid

model = whisper.load_model("base")

while True:
    input("Press Enter to record...")

    fs = 16000
    seconds = 4
    filename = f"{uuid.uuid4()}.wav"

    print("Recording...")
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)
    print("Saved:", filename)

    result = model.transcribe(filename)
    print("You said:", result["text"])
