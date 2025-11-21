from voice_test import record_and_transcribe
from keyword_matching import parse_text_to_json, classify_keyword


def route_page(result: dict):
    """키워드 결과에 따라 페이지 이동 또는 재질문 처리"""
    if result["status"] == "danger":
        print("⚠ 위험 금융어 감지됨. 다시 말씀해주세요.")
        return None

    if result["status"] == "ok":
        print(f"→ {result['page']} 로 이동합니다.")
        return result["page"]

    print("관련 금융어를 찾지 못했어요. 다시 말해주세요.")
    return None


def main():
    print("음성 인식 시스템 시작")

    while True:
        input("Press Enter to record...")

        # 1) 음성 인식
        text = record_and_transcribe()
        print("Recognized:", text)

        # 2) JSON 파싱
        json_data = parse_text_to_json(text)
        print("JSON:", json_data)

        # 3) 키워드 분류
        result = classify_keyword(text)
        print("Result:", result)

        # 4) 페이지 이동 처리
        page = route_page(result)

        if page:
            print(f"*** [{page}] 페이지 로직 실행 ***")
            break


if __name__ == "__main__":
    main()
