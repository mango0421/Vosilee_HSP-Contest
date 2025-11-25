import os
from datetime import datetime

# 로그 파일들
TRANSCRIPT_LOG = "transcript_log.txt"
SEND_MONEY_LOG = "send_money_log.txt"

# 녹음 파일 폴더
RECORDING_DIR = "recordings"


# -----------------------------------------------------------
# 녹음 파일 목록 가져오기
# -----------------------------------------------------------
def list_audio_files():
    if not os.path.exists(RECORDING_DIR):
        return []
    return sorted([
        f for f in os.listdir(RECORDING_DIR)
        if f.endswith(".wav")
    ])


# -----------------------------------------------------------
# transcript_log.txt 읽기
# -----------------------------------------------------------
def read_transcript_log():
    if not os.path.exists(TRANSCRIPT_LOG):
        return []
    with open(TRANSCRIPT_LOG, "r", encoding="utf-8") as f:
        logs = f.readlines()
    return [line.strip() for line in logs]


# -----------------------------------------------------------
# send_money_log.txt 읽기
# -----------------------------------------------------------
def read_sendmoney_log():
    if not os.path.exists(SEND_MONEY_LOG):
        return []
    with open(SEND_MONEY_LOG, "r", encoding="utf-8") as f:
        logs = f.readlines()
    return [line.strip() for line in logs]


# -----------------------------------------------------------
# 파일명에서 날짜/시간/키워드 추출
# recordings/2025-11-25_14-20-10_송금.wav
# -----------------------------------------------------------
def parse_record_filename(filename: str):
    try:
        base = filename.replace(".wav", "")
        # 2025-11-25_14-20-10_송금
        date_str, time_str, keyword = base.split("_", 2)
        datetime_str = f"{date_str} {time_str.replace('-', ':')}"
        return datetime_str, keyword
    except:
        return None, None


# -----------------------------------------------------------
# 전체 기록 출력
# -----------------------------------------------------------
def show_transcript():
    print("\n==============================")
    print(" 🎧 녹음 파일 기록")
    print("==============================")

    audio_files = list_audio_files()
    if audio_files:
        for f in audio_files:
            dt, kw = parse_record_filename(f)
            if dt and kw:
                print(f" - {f}  |  날짜: {dt}  |  키워드: {kw}")
            else:
                print(f" - {f}")
    else:
        print(" (저장된 녹음 없음)")

    # -----------------------------
    print("\n==============================")
    print(" 📝 일반 음성 텍스트 로그")
    print("==============================")

    tlogs = read_transcript_log()
    if tlogs:
        for line in tlogs:
            print(" -", line)
    else:
        print(" (기록 없음)")

    # -----------------------------
    print("\n==============================")
    print(" 💸 송금 대화 로그 (send_money_log)")
    print("==============================")

    sm_logs = read_sendmoney_log()
    if sm_logs:
        for line in sm_logs:
            print(" -", line)
    else:
        print(" (송금 로그 없음)")

    print("\n")


if __name__ == "__main__":
    show_transcript()
