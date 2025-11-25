import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import uuid
import os

# Whisper 모델 로드
model = whisper.load_model("base")

# 텍스트 로그 파일
LOG_FILE = "transcript_log.txt"

# 녹음 저장 폴더
RECORDING_DIR = "recordings"

# 폴더 자동 생성
if not os.path.exists(RECORDING_DIR):
    os.makedirs(RECORDING_DIR)

def save_log(text: str):
    """인식된 텍스트를 transcript_log.txt에 저장"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def record_and_transcribe(seconds: int = 4, fs: int = 16000) -> str:
    """음성을 녹음하고 Whisper로 STT한 뒤 텍스트 반환"""
    
    # 녹음 파일 경로 설정
    filename = os.path.join(RECORDING_DIR, f"{uuid.uuid4()}.wav")

    print("Recording...")
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()

    write(filename, fs, audio)
    print(f"Saved: {filename}")

    result = model.transcribe(filename)
    text = result["text"]

    # 로그 저장
    save_log(text)

    return text


if __name__ == "__main__":
    text = record_and_transcribe()
    print("STT 결과:", text)
