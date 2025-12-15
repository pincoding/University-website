import os
from openai import OpenAI
from dotenv import load_dotenv # ⭐ 1. dotenv 라이브러리 추가

load_dotenv() # ⭐ 2. .env 파일을 읽어 환경 변수로 로드

# 🚨 API 키 설정 (이제 환경 변수에서 안전하게 읽어옵니다.)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 1. 파일 업로드
file_response = client.files.create(
  file=open("training_data.jsonl", "rb"),
  purpose="fine-tune"
)
file_id = file_response.id
print(f"파일 업로드 완료. ID: {file_id}")

# 2. 파인튜닝 작업 생성 (모델은 gpt-3.5-turbo 등 선택)
job_response = client.fine_tuning.jobs.create(
  training_file=file_id,
  model="gpt-3.5-turbo",
  hyperparameters={
     "n_epochs": 3
  }
)

print(f"작업 시작됨. Job ID: {job_response.id}")
print("OpenAI 대시보드나 이메일에서 완료 알림을 기다리세요.")