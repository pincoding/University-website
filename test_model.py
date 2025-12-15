from openai import OpenAI
import os
from dotenv import load_dotenv # ⭐ 1. dotenv 라이브러리 임포트

load_dotenv() # ⭐ 2. .env 파일을 읽어 환경 변수로 로드

# 🚨 1. API 키 설정 (이제 환경 변수에서 안전하게 읽어옵니다.)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY")) # 👈 하드코딩된 키 제거 및 환경 변수 적용

# 🚨 2. 최종 파인튜닝된 모델 ID 입력
FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-0125:personal::Cmop8cxB" 

# 테스트 메시지 설정
user_query = "교환학생 프로그램은 언제 지원하나요?" 

print(f"--- 스크립트 실행 시작: 테스트 모델 연결 ---")
print(f"--- 사용자 질문: {user_query} ---")
print(f"--- 사용 모델 ID: {FINE_TUNED_MODEL} ---")

try:
    completion = client.chat.completions.create(
        model=FINE_TUNED_MODEL,
        messages=[
            # ⭐ 중요: 시스템 역할은 파인튜닝 시 사용한 역할로 변경했습니다.
            {"role": "system", "content": "너는 한국교통대학교의 학사, 공지사항, 입시 정보를 전문적으로 안내하는 친절한 상담원이야."}, 
            {"role": "user", "content": user_query}
        ]
    )

    assistant_response = completion.choices[0].message.content
    print("\n==============================================")
    print(f"✅ 모델 답변: {assistant_response}")
    print("==============================================")

except Exception as e:
    print("\n==============================================")
    print(f"❌ 에러 발생: {e}")
    print("모델 ID 또는 API 키가 정확한지 확인해 주세요.")
    print("==============================================")