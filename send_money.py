from voice_test import record_and_transcribe
import requests
import os

LOG_FILE = "send_money_log.txt"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def save_log(text: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def ask_llm(prompt: str) -> str:
    """OpenRouter gpt-oss-20b 모델에게 질문하고 응답받는 함수"""
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "VoiceBanking-App"
    }

    data = {
        "model": "openai/gpt-oss-20b:free",   # 🔥 여기 모델명 중요
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    result = response.json()

    reply = result["choices"][0]["message"]["content"]
    save_log(f"LLM: {reply}")

    return reply


def send_money_flow():
    print("\n--- 송금 서비스 시작 ---\n")

    # 1) 금액 묻기
    question = "얼마를 송금하시겠습니까?"
    print(question)
    save_log("SYSTEM: " + question)

    amount = record_and_transcribe()
    save_log("USER: " + amount)

    # 2) 수신인 묻기
    question = "누구에게 송금할까요?"
    print(question)
    save_log("SYSTEM: " + question)

    receiver = record_and_transscribe()
    save_log("USER: " + receiver)

    # 3) LLM 자연스러운 확인 문장 생성
    prompt = f"사용자가 {receiver}에게 {amount} 송금하려고 합니다. 자연스럽게 확인 문장을 만들어줘."
    confirm_sentence = ask_llm(prompt)
    print("\n" + confirm_sentence)

    save_log("SYSTEM: 송금 완료")
    print("\n송금 요청이 완료되었습니다.\n")
