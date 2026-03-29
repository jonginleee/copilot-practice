# 3-1. GitHub Copilot 프롬프트 엔지니어링 실습

---

## 사전 준비

### 1. 환경 셋업

GitHub Copilot에 아래와 같이 프롬프트를 입력합니다.

```cmd
파이썬 가상환경 셋업하고

pip install fastapi uvicorn[standard] passlib[bcrypt] httpx

설치해줘.
```

---

## 핵심 개념: 4S 빠르게 확인

프롬프트 엔지니어링은 AI에게 원하는 작업을 정확하고 효율적으로 전달하는 기술입니다.

같은 의도라도 프롬프트 품질에 따라 결과가 크게 달라집니다.

- 나쁜 예: `API 만들어줘`
- 좋은 예: `FastAPI로 회원가입 API 하나만 만들어줘. 입력은 email, password이고 중복 이메일은 409를 반환해줘.`

Copilot에서 특히 중요한 기준은 4S입니다.

- Single: 한 번에 하나의 작업만 요청
- Specific: 입력/출력/조건/예외를 구체적으로 명시
- Short: 길게 쓰기보다 핵심만 짧게 전달
- Surround: README, 테스트, 열린 파일 같은 맥락 함께 제공

---

## Step 1: Bad → Good 프롬프트

1. 나쁜 프롬프트 (의도적으로 시도):  
`app/security.py` 파일을 열고 Chat에 입력:

```
비밀번호 처리 로직 만들어줘.
```

2. 작성한 코드를 확인합니다. 자세한 규칙들이 설정되어 있지 않습니다.

3. 기존 작성 내용을 Undo 하고 `/clear`를 입력해 채팅창을 초기화 합니다.

4. 아래 프롬프트를 다시 입력합니다.

좋은 프롬프트:

```
`app/security.py`에 `validate_password(password: str) -> None` 하나만 구현해줘.

규칙:
- 길이 >= 8
- 숫자 >= 1
- 특수문자 >= 1 (!@#$%^&* 등)
- 위반 시 ValueError 발생, 메시지는 사람이 이해 가능하게

다른 함수는 건드리지 말고 이것만.
```

---

## Step 2: 맥락 제공 (Surround)

1. `README.md` 파일을 추가합니다.

2. README 파일에 아래의 내용을 추가합니다.

```
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
```

3. 아래의 프롬프트를 입력합니다.

```
#README.md 요구사항을 따르게 `app/security.py`에 다음 함수를 추가해줘:

- hash_password(password: str) -> str: bcrypt로 해시 반환
- verify_password(plain: str, hashed: str) -> bool: 일치 여부 확인

조건:
- passlib[bcrypt] 사용 (이미 설치됨)
- 평문 저장/로깅 절대 금지
- 외부 라이브러리 추가 금지

```

---

## Step 3: 예시 활용 (One-shot)

아래의 프롬프트를 순차적으로 입력합니다.

```
`app/main.py`의 `/health`처럼 응답은 JSON dict로 반환하되,
#README.md 의 Response contract를 반드시 지켜줘.
```

```
`app/routes/auth.py`에 `POST /auth/register` 구현:

입력: RegisterRequest (email, password)

처리:
1. 이메일 형식 검증 실패 -> 400 INVALID_EMAIL
2. 비밀번호 약함 -> 400 WEAK_PASSWORD
3. 이미 존재하는 이메일 -> 409 DUPLICATE_EMAIL
4. 성공 -> 201 + {"ok": true, "user": {"id": X, "email": "..."}}

변경 파일: app/routes/auth.py (필요 시 app/storage.py도)
```

---

## Step 4: 프로젝트 전체 맥락

```
현재 구현에서 실행에 문제될 만한 부분을 찾아 수정 제안해줘.

특히 확인:
- import 경로 오류
- 라우터 include 누락
- 응답 형식이 테스트 기대값과 맞는지
```