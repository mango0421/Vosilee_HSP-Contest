from voice_test import record_and_transcribe
from keyword_matching import parse_text_to_json, classify_keyword
from Transcript import show_transcript


def route_action(result: dict):
    status = result["status"]

    if status == "danger":
        print("\n⚠ 위험 금융어 탐지됨 → 보이스피싱 의심, 추가 본인 확인 필요\n")
        return

    if status == "ok":
        page = result["page"]
        print(f"\n➡ 정상 금융 키워드 감지: {result['keyword']}")
        print(f"➡ {page} 기능으로 이동합니다.\n")
        return

    if status == "unknown":
        print("\n🤔 인식된 키워드가 없습니다. 다시 말해주세요.\n")
        return


def main():
    print("\n🎤 음성 인식 시작\n")
    text = record_and_transcribe()

    print(f"📌 STT 결과: {text}\n")

    # 사용자가 “기록”이라고 말한 경우
    if "기록" in text.replace(" ", ""):
        print("\n📑 기록 조회 기능 실행\n")
        show_transcript()
        return

    parsed_json = parse_text_to_json(text)
    print("📌 JSON:", parsed_json, "\n")

    classify_result = classify_keyword(text)
    print("📌 키워드 분류 결과:", classify_result, "\n")

    route_action(classify_result)


if __name__ == "__main__":
    main()
