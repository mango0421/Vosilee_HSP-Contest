import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import uuid
import os
from datetime import datetime
from keyword_matching import classify_keyword


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


def sanitize_filename(text: str) -> str:
    """파일명으로 사용할 수 없는 문자를 제거"""
    invalid = '\\/:*?"<>|'
    for c in invalid:
        text = text.replace(c, "")
    return text


def record_and_transcribe(seconds: int = 4, fs: int = 16000) -> str:
    """음성을 녹음하고 Whisper로 STT한 뒤 텍스트 반환"""

    # (1) 임시 파일명
    temp_filename = os.path.join(RECORDING_DIR, f"{uuid.uuid4()}.wav")

    print("Recording...")
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()

    write(temp_filename, fs, audio)
    print(f"Saved: {temp_filename}")

    # (2) Whisper STT
    result = model.transcribe(temp_filename)
    text = result["text"].strip()

    # (3) 파일명 구성 요소 (날짜 + 시간 + 첫 단어)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # 첫 단어만 추출 (없으면 unknown)
    first_word = text.split()[0] if text else "unknown"
    first_word = sanitize_filename(first_word)

    new_filename = os.path.join(RECORDING_DIR, f"{now}_{first_word}.wav")

    # (4) 파일명을 rename
    os.rename(temp_filename, new_filename)
    print(f"Renamed to: {new_filename}")

    # (5) 텍스트 로그 저장
    save_log(text)

    return text


if __name__ == "__main__":
    text = record_and_transcribe()
    print("STT 결과:", text)

    result = classify_keyword(text)
    print("분류 결과:", result)
