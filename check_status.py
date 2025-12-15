from openai import OpenAI
import time
import os # ⭐ 1. os 라이브러리 추가
from dotenv import load_dotenv # ⭐ 2. dotenv 라이브러리 추가

load_dotenv() # ⭐ 3. .env 파일을 읽어 환경 변수로 로드

# 🚨 API 키를 환경 변수에서 안전하게 읽어옵니다. (하드코딩된 키 제거)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 파인튜닝 Job ID (이미 완료되었으므로 확인용으로 사용)
job_id = "ftjob-mSBkcmEGHLLk4rf3CYqB7Yjv"

while True:
    try:
        job = client.fine_tuning.jobs.retrieve(job_id)
        status = job.status
        print(f"현재 상태: {status}")

        if status == "succeeded":
            print("\n학습 완료! 🎉")
            print(f"모델 ID: {job.fine_tuned_model}")
            break
        elif status == "failed":
            print("\n학습 실패... 에러 내용을 확인하세요.")
            print(job.error)
            break
        
        print("10초 뒤 다시 확인합니다...")
        time.sleep(10)
        
    except Exception as e:
        print(f"API 요청 중 오류 발생: {e}")
        break