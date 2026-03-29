from fastapi import FastAPI
from app.routes.auth import router as auth_router

app = FastAPI(title="Copilot Prompt Lab")

@app.get("/health")
def health():
    # one-shot 예시용: 응답 구조를 고정해두고 다른 엔드포인트도 따라오게 만들기
    return {"ok": True, "status": "up"}

app.include_router(auth_router)
