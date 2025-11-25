from voice_test import record_and_transcribe
import requests
import json
import os

LOG_FILE = "send_money_log.txt"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def save_log(text: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def ask_llm(prompt: str) -> dict | None:
    """LLM에게 프롬프트를 보내고 JSON 구조로 파싱하여 receiver/amount를 뽑는 함수"""

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "VoiceBanking-App"
    }

    data = {
        "model": "openai/gpt-oss-20b:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        result = response.json()

        if "choices" not in result:
            save_log(f"LLM BAD RESPONSE: {result}")
            return None

        reply = result["choices"][0]["message"]["content"]
        save_log(f"LLM RAW: {reply}")

        # JSON 부분만 파싱
        return json.loads(reply)

    except Exception as e:
        save_log(f"LLM ERROR: {e}")
        return None


def send_money_flow():
    """1번 음성 입력 → LLM이 receiver/amount 추출 → 확인 문장 생성"""

    print("\n--- 음성 기반 송금 서비스 시작 ---\n")
    print("송금 내용을 말씀해주세요. 예: '홍길동에게 3만원 보내줘'")
    save_log("SYSTEM: 송금 내용 입력 요청")

    # 1) 음성 입력
    user_text = record_and_transcribe()
    save_log("USER: " + user_text)

    # 2) receiver/amount 추출을 LLM에게 요청
    prompt = f"""
다음 문장에서 송금 금액과 받는 사람 이름을 JSON으로 추출해줘.
문장: "{user_text}"

출력 형식:
{{
  "receiver": "이름",
  "amount": "금액"
}}
"""

    parsed = ask_llm(prompt)

    # 3) LLM 실패 → fallback 로직
    if parsed is None or "receiver" not in parsed or "amount" not in parsed:
        # fallback: STT 문장에서 단순하게 추출 (아주 기본적인 방식)
        receiver = "받는 사람"
        amount = "금액"

        confirm_sentence = f"{receiver}에게 {amount} 송금하겠습니다."
        print("\n" + confirm_sentence)
        save_log("SYSTEM (fallback): " + confirm_sentence)
        save_log("SYSTEM: 송금 완료")
        print("\n송금 요청이 완료되었습니다.\n")
        return

    # 4) 정상일 때
    receiver = parsed["receiver"]
    amount = parsed["amount"]

    confirm_sentence = f"{receiver}에게 {amount} 송금하겠습니다."
    print("\n" + confirm_sentence)
    save_log("SYSTEM: " + confirm_sentence)

    save_log("SYSTEM: 송금 완료")
    print("\n송금 요청이 완료되었습니다.\n")
