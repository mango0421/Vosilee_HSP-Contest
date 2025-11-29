import json

# 1. 대표 금융 키워드 및 페이지 매핑 (6가지로 확장)
FINANCE_KEYWORDS = {
    "잔액 조회": "balance_page",
    "이체": "transfer_page",
    "송금": "remittance_page",
    "예금": "deposit_page",
    "적금": "saving_page",
    "상담": "consulting_page"
}

# 2. 발음 오류 / 오인식 / 유사 단어 보정 테이블 (대폭 보강)
# 주의: classify_keyword 함수에서 공백을 제거하므로, 여기 있는 단어들도 공백 없이 작성해야 정확도가 높습니다.
NORMALIZE_MAP = {
    "잔액 조회": [
        "잔액", "자낵", "잔애", "잔핵", "잔엑", "잔고", "통장정리",
        "얼마있어", "얼마남아", "남은돈", "나먼돈", "잔돈확인", "잔액조회"
    ],
    "이체": [
        "이체", "이췌", "잇체", "익채", "이채", "잇채", "리체", "계좌이체",
        "돈옴겨", "돈옮겨", "이치", "이채해"
    ],
    "송금": [
        "송금", "숑금", "송굼", "성금", "손금", "송그", 
        "보내줘", "보내기", "부쳐", "붙여", "붗여", "돈보내", "입금해"
    ],
    "예금": [
        "예금", "얘금", "예김", "얘김", "애금", "여금", "예그", 
        "거치", "목돈", "맞길래", "맡길래", "예치"
    ],
    "적금": [
        "적금", "적끔", "젇금", "조금", "저금", "저끔", 
        "붓는거", "부을래", "매달", "적립"
    ],
    "상담": [
        "상담", "상당", "산담", "쌍담", "샹담", 
        "문의", "질문", "고객센터", "도와줘", "연결", "직원", "어려워", "모르겠어"
    ]
}

# 3. 위험 단어 (금융사기 의심 등)
RISK_KEYWORDS = ["담보", "대출", "보증", "해지", "비밀번호", "검찰", "경찰"]


def normalize_keyword(text: str) -> str | None:
    """
    입력된 텍스트(공백 제거됨)에 변형된 키워드가 포함되어 있는지 확인하여
    대표 키워드를 반환합니다.
    """
    for canonical, variants in NORMALIZE_MAP.items():
        for v in variants:
            if v in text:
                return canonical
    return None


def classify_keyword(text: str) -> dict:
    # 1. 공백 제거 (매칭 정확도를 위해)
    clean_text = text.replace(" ", "")

    # 2. 위험 금융어 먼저 체크
    for risk in RISK_KEYWORDS:
        if risk in clean_text:
            return {
                "status": "danger",
                "keyword": risk,
                "message": "⚠️ 위험 금융어 감지됨. 상담원 연결 또는 주의 필요."
            }

    # 3. 정상 금융어: 발음 변형 → 정규 키워드 보정
    normalized = normalize_keyword(clean_text)

    if normalized:
        return {
            "status": "ok",
            "keyword": normalized,
            "page": FINANCE_KEYWORDS[normalized],
            "message": f"'{normalized}' 기능으로 이동합니다."
        }

    # 4. 아무 키워드도 없는 경우
    return {
        "status": "unknown",
        "keyword": None,
        "message": "죄송합니다. 원하시는 금융 업무를 다시 말씀해 주세요."
    }

# --- 테스트 실행 코드 ---
if __name__ == "__main__":
    test_sentences = [
        "내 통장에 얼마 있니",       # 잔액 조회 (얼마)
        "친구한테 돈좀 부쳐줘",      # 송금 (부쳐)
        "적끔 하나 들고 싶어",       # 적금 (적끔)
        "상당원 연결해줘",          # 상담 (상당)
        "계좌 이채 할래",           # 이체 (이채)
        "대출 상담 받고 싶어",       # 위험 (대출) -> 주의: '상담'보다 '대출'이 먼저 걸림
    ]

    for sent in test_sentences:
        print(f"입력: {sent}")
        print(f"결과: {classify_keyword(sent)}")
        print("-" * 30)