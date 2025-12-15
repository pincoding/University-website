from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv # ⭐ 1. dotenv 라이브러리 임포트

load_dotenv() # ⭐ 2. .env 파일을 읽어 환경 변수로 로드

app = FastAPI()

# 🚨 API 키를 환경 변수에서 안전하게 읽어옵니다. (코드에 키 노출 없음)
# 3. 하드코딩된 키를 os.environ.get()으로 대체
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY")) 
FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-0125:personal::Cmop8cxB" 

# CORS 설정 (리액트 기본 포트 3000 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    """리액트로부터 메시지를 받아 OpenAI API에 전달하고 응답을 반환합니다."""
    try:
        response = client.chat.completions.create(
            model=FINE_TUNED_MODEL,
            messages=[
                # 시스템 역할은 그대로 유지
                {"role": "system", "content": "너는 한국교통대학교의 학사, 공지사항, 입시 정보를 전문적으로 안내하는 친절한 상담원이야."},
                {"role": "user", "content": req.message}
            ]
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        print(f"OpenAI API 에러: {e}")
        return {"error": "API 요청 중 오류가 발생했습니다."}, 500