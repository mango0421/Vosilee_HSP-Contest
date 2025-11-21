import json

FINANCE_KEYWORDS = {
    "이체": "transfer_page",
    "예금": "deposit_page",
    "적금": "saving_page",
    "송금": "remittance_page"
}

RISK_KEYWORDS = ["담보", "대출"]


def parse_text_to_json(text: str) -> dict:
    """STT 결과 텍스트를 JSON 형태로 변환"""
    return {"recognized_text": text}


def classify_keyword(text: str) -> dict:
    """키워드 분류 및 위험 금융어 예외 처리"""
    text = text.replace(" ", "")  # 공백 제거해 매칭 정확도 올림

    # 위험 금융어 먼저 체크
    for risk in RISK_KEYWORDS:
        if risk in text:
            return {
                "status": "danger",
                "keyword": risk,
                "message": "위험 금융어 감지됨. 다시 질문 필요"
            }

    # 정상 금융어 체크
    for keyword, page in FINANCE_KEYWORDS.items():
        if keyword in text:
            return {
                "status": "ok",
                "keyword": keyword,
                "page": page,
                "message": f"{keyword} 기능으로 이동"
            }

    # 아무 키워드도 없는 경우
    return {
        "status": "unknown",
        "keyword": None,
        "message": "관련 금융어가 없어 다시 입력 필요"
    }
