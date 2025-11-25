import json

# 대표 금융 키워드 → 업무 페이지
FINANCE_KEYWORDS = {
    "이체": "transfer_page",
    "예금": "deposit_page",
    "적금": "saving_page",
    "송금": "remittance_page"
}

# 발음 오류 / 오인식 보정 테이블
NORMALIZE_MAP = {
    "이체": ["이체", "이췌", "잇체", "익채", "이채", "잇채"],
    "예금": ["예금", "예금", "예겜","얘김", "얘금","예김"],
    "적금": ["적금", "적끔", "젇금","조금"],
    "송금": ["송금", "숑금", "송굼"]
}

# 위험 단어
RISK_KEYWORDS = ["담보", "대출","보증",]


def normalize_keyword(text: str) -> str | None:
    """
    발음 변형이 섞인 금융어를 대표 키워드로 정규화하는 함수
    예: '이췌' → '이체'
    """
    for canonical, variants in NORMALIZE_MAP.items():
        for v in variants:
            if v in text:
                return canonical
    return None


def parse_text_to_json(text: str) -> dict:
    return {"recognized_text": text}


def classify_keyword(text: str) -> dict:
    text = text.replace(" ", "")

    # 위험 금융어 먼저 체크
    for risk in RISK_KEYWORDS:
        if risk in text:
            return {
                "status": "danger",
                "keyword": risk,
                "message": "위험 금융어 감지됨. 다시 질문 필요"
            }

    # 정상 금융어: 발음 변형 → 정규 키워드 보정
    normalized = normalize_keyword(text)

    if normalized:
        return {
            "status": "ok",
            "keyword": normalized,
            "page": FINANCE_KEYWORDS[normalized],
            "message": f"{normalized} 기능으로 이동"
        }

    # 아무 키워드도 없는 경우
    return {
        "status": "unknown",
        "keyword": None,
        "message": "관련 금융어가 없어 다시 입력 필요"
    }
