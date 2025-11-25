from voice_test import record_and_transscribe
from keyword_matching import parse_text_to_json, classify_keyword
from Transcript import show_transcript
from send_money import send_money_flow   # 🔥 ① 송금 기능 import


def route_action(result: dict):
    status = result["status"]

    if status == "danger":
        print("\n⚠ 위험 금융어 탐지됨 → 보이스피싱 의심, 추가 본인 확인 필요\n")
        return

    if status == "ok":
        page = result["page"]
        
        # 🔥 ② 송금 / 이체 페이지로 가는 경우 send_money_flow 호출
        if page in ["remittance_page", "transfer_page"]:
            print("\n➡ 송금/이체 기능으로 이동합니다.\n")
            send_money_flow()
            return

        # 그 외 금융업무 페이지
        print(f"\n➡ 정상 금융 키워드 감지: {result['keyword']}")
        print(f"➡ {page} 기능으로 이동합니다.\n")
        return

    if status == "unknown":
        print("\n🤔 인식된 키워드가 없습니다. 다시 말해주세요.\n")
        return


def main():
    print("\n🎤 음성 인식 시작\n")
    text = record_and_transscribe()

    print(f"📌 STT 결과: {text}\n")

    # 🔥 ③ “기록” 명령 처리
    if "기록" in text.replace(" ", ""):
        print("\n📑 기록 조회 기능 실행\n")
        show_transcript()
        return

    parsed_json = parse_text_to_json(text)
    print("📌 JSON:", parsed_json, "\n")

    classify_result = classify_keyword(text)
    print("📌 키워드 분류 결과:", classify_result, "\n")

    # 🔥 ④ route_action() 으로 전체 흐름 분기 처리
    route_action(classify_result)


if __name__ == "__main__":
    main()
