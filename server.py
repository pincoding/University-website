from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# 🚨 API 키를 환경 변수에서 안전하게 읽어옵니다. (코드에 키 노출 없음)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY")) 
FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-0125:personal::Cmop8cxB" 

# ✅ CORS 설정 수정: GitHub Pages 주소를 허용 목록에 추가 (CORS 해결)
origins = [
    # 📌 프론트엔드 배포 주소 (필수 추가!)
    "https://pincoding.github.io", 
    
    # 로컬 테스트용 (선택 사항)
    "http://localhost:3000", 
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 수정된 origins 리스트 사용
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