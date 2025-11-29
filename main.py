from voice_test import record_and_transcribe
from keyword_matching import classify_keyword      # ← 이거만 있으면 됨
from Transcript import show_transcript
from send_money import send_money_flow


def route_action(result: dict):
    status = result["status"]

    # 1) 위험 금융어 감지
    if status == "danger":
        print("\n⚠ 위험 금융어 탐지됨 → 보이스피싱 의심, 추가 본인 확인 필요\n")
        return

    # 2) 정상 분류
    if status == "ok":
        keyword = result["keyword"]
        page = result["page"]

        # 송금 / 이체는 바로 send_money_flow 실행
        if page in ["remittance_page", "transfer_page"]:
            print("\n➡ 송금/이체 기능으로 이동합니다.\n")
            send_money_flow()
            return

        # 나머지 금융 기능
        print(f"\n➡ 정상 금융 키워드 감지: {keyword}")
        print(f"➡ {page} 기능으로 이동합니다.\n")
        return

    # 3) 재질문
    if status == "retry":
        print("\n🤔 제가 정확히 듣지 못했어요. 다시 한번 말씀해주세요.\n")
        return


def main():
    print("\n🎤 음성 인식 시작\n")
    text = record_and_transcribe()

    print(f"📌 STT 결과: {text}\n")

    # ① "기록" 명령어: 로그 조회 기능
    if "기록" in text.replace(" ", ""):
        print("\n📑 기록 조회 기능 실행\n")
        show_transcript()
        return

    # ② 금융 키워드 분류
    classify_result = classify_keyword(text)
    print("📌 키워드 분류 결과:", classify_result, "\n")

    # ③ 최종 경로 라우팅
    route_action(classify_result)


if __name__ == "__main__":
    main()
