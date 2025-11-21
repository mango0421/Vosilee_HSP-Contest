import wave
import os
from google import genai
from google.genai import types

# 1. API 키 설정 (환경 변수에 GOOGLE_API_KEY가 없다면 직접 입력)
# os.environ["GOOGLE_API_KEY"] = "여기에_API_키를_입력하세요"
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("API 키가 설정되지 않았습니다. 코드 내에 직접 입력하거나 환경 변수를 설정해주세요.")
    # client = genai.Client(api_key="YOUR_API_KEY") # 직접 입력 시 사용
    exit()

client = genai.Client(api_key=api_key)

print("1. 대본(Transcript) 생성 중...")
# 팟캐스트 대본 생성
transcript = client.models.generate_content(
    model="gemini-2.0-flash-exp", # 혹은 gemini-1.5-flash
    contents="""Generate a short transcript around 100 words that reads 
            like it was clipped from a podcast by excited herpetologists. 
            The hosts names are Dr. Anya and Liam."""
).text

print(f"대본 내용:\n{transcript}\n")

print("2. 음성(TTS) 생성 중...")
# 음성 생성 요청
response = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts", # 2025년 9월 기준 최신 모델
    contents=transcript,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[
                    types.SpeakerVoiceConfig(
                        speaker='Dr. Anya',
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='Kore',
                            )
                        )
                    ),
                    types.SpeakerVoiceConfig(
                        speaker='Liam',
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='Puck',
                            )
                        )
                    ),
                ]
            )
        )
    )
)

# 3. 오디오 저장 (PCM -> WAV)
# Gemini TTS는 헤더가 없는 PCM 데이터를 반환하므로, wave 라이브러리로 헤더를 씌워야 재생 가능합니다.
print("3. 파일 저장 중...")

# 응답에서 오디오 데이터 추출 (바이너리 데이터)
# candidates[0].content.parts[0].inline_data.data 에 위치함
audio_data = response.candidates[0].content.parts[0].inline_data.data

output_filename = "podcast_output.wav"

# WAV 파일 설정 (Gemini TTS 기본값: 24kHz, 16bit, Mono)
with wave.open(output_filename, "wb") as f:
    f.setnchannels(1)      # 모노 채널
    f.setsampwidth(2)      # 16비트 (2바이트)
    f.setframerate(24000)  # 샘플링 레이트 (24000Hz)
    f.writeframes(audio_data)

print(f"완료! '{output_filename}' 파일이 생성되었습니다.")