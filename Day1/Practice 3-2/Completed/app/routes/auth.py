import re
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schemas import RegisterRequest
from app import security, storage

router = APIRouter(prefix="/auth", tags=["auth"])
MAX_EMAIL_LENGTH = 100

def error(code: str, message: str, status_code: int):
    return JSONResponse(
        status_code=status_code,
        content={"ok": False, "error": {"code": code, "message": message}},
    )

@router.post("/register", status_code=201)
def register(req: RegisterRequest):
	# Email validation (basic regex + length)
	email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
	if len(req.email) > MAX_EMAIL_LENGTH or not re.match(email_pattern, req.email):
		return error("INVALID_EMAIL", "Invalid email format", 400)
	
	# Check for duplicate email
	if storage.get_user_by_email(req.email):
		return error("DUPLICATE_EMAIL", "Email already registered", 409)
	
	# Password validation
	try:
		security.validate_password(req.password)
	except ValueError as e:
		return error("WEAK_PASSWORD", str(e), 400)
	
	# Hash and store
	hashed = security.hash_password(req.password)
	user = storage.create_user(req.email, hashed)
	
	return {"ok": True, "user": user}
