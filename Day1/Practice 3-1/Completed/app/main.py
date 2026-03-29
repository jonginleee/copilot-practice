from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routes.auth import router as auth_router

app = FastAPI(title="Copilot Prompt Lab")


@app.exception_handler(RequestValidationError)
def handle_validation_error(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "ok": False,
            "error": {
                "code": "INVALID_REQUEST",
                "message": "Invalid request body",
            },
        },
    )

@app.get("/health")
def health():
    # one-shot 예시용: 응답 구조를 고정해두고 다른 엔드포인트도 따라오게 만들기
    return {"ok": True, "status": "up"}

app.include_router(auth_router)
