from pydantic import BaseModel

class RegisterRequest(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

class ErrorDetail(BaseModel):
    code: str
    message: str

class ErrorResponse(BaseModel):
    ok: bool = False
    error: ErrorDetail

class RegisterResponse(BaseModel):
    ok: bool = True
    user: UserOut
