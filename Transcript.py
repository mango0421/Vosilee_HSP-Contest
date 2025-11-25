import os

LOG_FILE = "transcript_log.txt"


def list_audio_files():
    """프로젝트 루트에 저장된 .wav 파일 목록 반환"""

RECORDING_DIR = "recordings"

def list_audio_files():
    if not os.path.exists(RECORDING_DIR):
        return []
    return sorted([
        f for f in os.listdir(RECORDING_DIR)
        if f.endswith(".wav")
    ])

    return sorted(files)


def read_transcript_log():
    """음성 인식된 텍스트 로그 읽기"""
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = f.readlines()
    return [log.strip() for log in logs]


def show_transcript():
    """녹음 파일들과 텍스트 로그를 터미널에 출력"""
    print("\n==============================")
    print(" 📄 녹음 파일 기록")
    print("==============================")

    audio_files = list_audio_files()
    if audio_files:
        for f in audio_files:
            print(" -", f)
    else:
        print(" (저장된 녹음 없음)")

    print("\n==============================")
    print(" 📝 인식된 텍스트 기록 (Transcript Log)")
    print("==============================")

    logs = read_transcript_log()
    if logs:
        for line in logs:
            print(" -", line)
    else:
        print(" (저장된 텍스트 로그 없음)")

    print("\n")


if __name__ == "__main__":
    show_transcript()
