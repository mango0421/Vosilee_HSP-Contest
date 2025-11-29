import numpy as np
from embeddings import get_embedding

# 1. 대표 금융 키워드 및 페이지 매핑
FINANCE_KEYWORDS = {
    "잔액 조회": "balance_page",
    "이체": "transfer_page",
    "송금": "remittance_page",
    "예금": "deposit_page",
    "적금": "saving_page",
    "상담": "consulting_page",
}

# 2. 발음 오류 / 오인식 / 유사 단어 보정 테이블
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
    ],
}

# 3. 위험 단어
RISK_KEYWORDS = ["담보", "대출", "보증", "해지", "비밀번호", "검찰", "경찰"]



# 4. 임베딩 기반 레퍼런스 DB
REFERENCE_DB: list[dict] = []
REF_MATRIX: np.ndarray | None = None


def _build_reference_db():
    global REFERENCE_DB, REF_MATRIX
    entries = []

    for canonical, variants in NORMALIZE_MAP.items():
        for phrase in variants:
            clean_phrase = phrase.replace(" ", "")
            emb = get_embedding(clean_phrase)
            entries.append({
                "keyword": canonical,
                "phrase": phrase,
                "embedding": emb,
            })

    REFERENCE_DB = entries
    REF_MATRIX = np.vstack([e["embedding"] for e in entries])


def _softmax(x: np.ndarray) -> np.ndarray:
    x = x - np.max(x)
    exps = np.exp(x)
    return exps / np.sum(exps)


# DB 초기 빌드
_build_reference_db()


def classify_keyword(text: str) -> dict:
    clean_text = text.replace(" ", "")

    # 0) 위험 키워드 먼저 체크
    for risk in RISK_KEYWORDS:
        if risk in clean_text:
            return {
                "status": "danger",
                "keyword": risk,
                "message": "⚠️ 위험 금융어 감지됨. 상담원 연결 또는 주의 필요.",
            }

    # 1) NORMALIZE_MAP 문자열 기반 즉시 매칭 (우선 처리)
    for canonical, variants in NORMALIZE_MAP.items():
        for v in variants:
            if v in clean_text:
                return {
                    "status": "ok",
                    "keyword": canonical,
                    "page": FINANCE_KEYWORDS[canonical],
                    "probability": 1.0,
                    "matched_phrase": v,
                    "message": f"'{canonical}' 기능으로 이동합니다. (정확 매칭)"
                }

    # 2) 문자열 매칭 실패 → 벡터 기반 비교
    q_emb = get_embedding(clean_text)
    scores = REF_MATRIX @ q_emb

    k = 5
    top_idx = np.argsort(-scores)[:k]
    top_scores = scores[top_idx]
    probs = _softmax(top_scores)

    best_idx = top_idx[0]
    best_prob = float(probs[0])
    best_entry = REFERENCE_DB[best_idx]

    # 3) 확률 기준 조정 
    THRESHOLD = 0.30
    if best_prob < THRESHOLD:
        return {
            "status": "retry",
            "keyword": None,
            "probability": best_prob,
            "message": "요청을 정확히 이해하기 어렵습니다. 다시 말씀해 주세요.",
        }

    # 4) 벡터 기반 정상 분류
    keyword = best_entry["keyword"]
    return {
        "status": "ok",
        "keyword": keyword,
        "page": FINANCE_KEYWORDS[keyword],
        "probability": best_prob,
        "matched_phrase": best_entry["phrase"],
        "message": f"'{keyword}' 기능으로 이동합니다.",
    }
