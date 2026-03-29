from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schemas import RegisterRequest

router = APIRouter(prefix="/auth", tags=["auth"])

def error(code: str, message: str, status_code: int):
    return JSONResponse(
        status_code=status_code,
        content={"ok": False, "error": {"code": code, "message": message}},
    )

# TODO: POST /auth/register 구현
