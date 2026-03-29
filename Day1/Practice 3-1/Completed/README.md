# Prompt Lab: FastAPI Register Endpoint

## Goal
POST /auth/register 를 구현한다.

## Response contract (must follow)
- Success (201):
  { "ok": true, "user": { "id": 1, "email": "user@example.com" } }

- Error (4xx):
  { "ok": false, "error": { "code": "ERROR_CODE", "message": "human readable message" } }

## Validation rules & Error codes
- **email**: 기본 이메일 형태 검사(간단한 정규식 수준 ok)
  - 실패 시: 400 INVALID_EMAIL
  
- **password**: 
  - 길이 >= 8
  - 숫자 1개 이상 포함
  - 특수문자 1개 이상 포함 (예: !@#$%^&* 등)
  - 위반 시: 400 WEAK_PASSWORD

- **email 중복**:
  - 이미 존재하는 email → 409 DUPLICATE_EMAIL

## Storage
- DB 없이 메모리(dict) 기반
- 중복 email 가입 시 409 반환
- 비밀번호는 bcrypt로 해싱해서 저장 (평문 저장 금지)

## 구현할 것
- app/security.py: validate_password, hash_password, verify_password
- app/storage.py: in-memory user store
- app/routes/auth.py: POST /auth/register