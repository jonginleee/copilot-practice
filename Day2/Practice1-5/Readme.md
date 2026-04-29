# Day2 Practice1-5. FastAPI endpoint 문서화 기준을 Custom Instructions로 고정하기

이 실습은 VS Code Copilot의 Custom Instructions를 사용해 FastAPI endpoint를 작성하거나 수정할 때 항상 같은 API 설계 기준을 따르게 만드는 흐름을 연습합니다.

이번 실습의 핵심은 아래 기준을 Copilot이 반복적으로 지키게 만드는 것입니다.

```text
- endpoint 함수에 명확한 docstring 작성
- response model 사용
- 에러 응답 형식 통일
- 한국어 설명 제공
- OpenAPI 문서에 잘 보이는 summary / description 작성
```

핵심 학습 포인트:
- `/create-instructions`로 프로젝트 전반 규칙 설정
- FastAPI endpoint에 `summary`, `description`, `response_model` 적용
- `HTTPException` 기반으로 에러 응답 표준화
- 경로별 세부 규칙을 `/create-instructions`로 추가
- 같은 요청을 다시 실행했을 때 결과가 어떻게 달라지는지 비교

---

## 실습 폴더

아래 Start 폴더를 VS Code에서 열고 진행합니다.

- `Day2/Practice1-5/Start/fastapi-instructions-demo`

초기 파일 구조:

```text
fastapi-instructions-demo/
├─ app.py
└─ .github/
   └─ copilot-instructions.md
```

이 실습에서는 instructions 파일을 손으로 직접 편집하기보다,
Copilot의 `/create-instructions` 프롬프트를 통해 지침을 추가하는 흐름에 집중합니다.

---

## Step 1. 예제 파일 확인

`app.py`에는 아래와 같은 단순한 FastAPI endpoint가 들어 있습니다.

```python
from fastapi import FastAPI

app = FastAPI(title="Operations API")


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    if order_id == 1:
        return {
            "id": 1,
            "status": "paid",
            "amount": 12000,
        }

    return {
        "error": "order not found",
    }
```

현재 코드는 다음 점이 아쉽습니다.

- `response_model`이 없음
- 404가 `HTTPException`이 아니라 단순 dict 반환임
- OpenAPI 문서용 `summary`, `description`이 없음
- 에러 응답 형식이 일관되지 않음

---

## Step 2. 먼저 지침 없이 요청해보기

Copilot Chat에서 아래처럼 입력합니다.

```text
이 FastAPI endpoint를 더 좋은 API 코드로 정리해줘.
```

확인할 점:

- `response_model`을 만드는가?
- 404 처리를 `HTTPException`으로 바꾸는가?
- OpenAPI 문서에 보일 `summary`, `description`을 추가하는가?
- 에러 응답 형식을 일관되게 정리하는가?

---

## Step 3. /create-instructions로 Custom Instructions 작성

이제 Copilot Chat에서 아래처럼 입력해 프로젝트 전반 지침을 추가합니다.

```text
/create-instructions

FastAPI 코드를 작성하거나 수정할 때 항상 아래 기준을 따르는 프로젝트 지침을 만들어줘.

- 사용자가 따로 요청하지 않아도 한국어로 설명한다.
- 코드를 제안할 때는 변경 이유를 짧게 설명한다.
- 불필요한 대규모 구조 변경은 피한다.
- endpoint에는 summary와 description을 작성한다.
- 응답 데이터는 가능하면 Pydantic model로 정의한다.
- 성공 응답과 에러 응답의 구조를 일관되게 유지한다.
- 찾을 수 없는 리소스는 단순 dict 반환 대신 HTTPException(status_code=404)를 사용한다.
- endpoint 함수에는 짧은 docstring을 작성한다.
- 외부 의존성은 사용자가 요청하지 않으면 추가하지 않는다.
- model 이름은 OrderResponse, ErrorResponse처럼 명확하게 작성한다.
- 금액 필드는 정수 원 단위라면 amount_krw처럼 단위를 드러낸다.
- 상태값은 가능한 한 의미가 분명한 문자열을 사용한다.

에러 응답 형식은 아래를 따른다.

{
    "detail": {
        "code": "ORDER_NOT_FOUND",
        "message": "주문을 찾을 수 없습니다."
    }
}
```

생성 후 `.github/copilot-instructions.md`에 아래와 같은 방향의 내용이 들어가면 됩니다.

````markdown
# FastAPI 프로젝트 작업 기준

이 저장소에서 Copilot은 FastAPI 코드를 작성하거나 수정할 때 아래 기준을 따른다.

## 답변 방식

- 사용자가 따로 요청하지 않아도 한국어로 설명한다.
- 코드를 제안할 때는 변경 이유를 짧게 설명한다.
- 불필요한 대규모 구조 변경은 피한다.

## FastAPI 코드 기준

- endpoint에는 `summary`와 `description`을 작성한다.
- 응답 데이터는 가능하면 Pydantic model로 정의한다.
- 성공 응답과 에러 응답의 구조를 일관되게 유지한다.
- 찾을 수 없는 리소스는 단순 dict 반환 대신 `HTTPException(status_code=404)`를 사용한다.
- endpoint 함수에는 짧은 docstring을 작성한다.
- 외부 의존성은 사용자가 요청하지 않으면 추가하지 않는다.

## 응답 모델 기준

- model 이름은 명확하게 작성한다.
- 예: `OrderResponse`, `ErrorResponse`, `OrderStatusResponse`
- 금액 필드는 정수 원 단위라면 `amount_krw`처럼 단위를 드러낸다.
- 상태값은 가능한 한 의미가 분명한 문자열을 사용한다.

## 에러 처리 기준

에러 응답은 아래 형식을 따른다.

```json
{
  "detail": {
    "code": "ORDER_NOT_FOUND",
    "message": "주문을 찾을 수 없습니다."
  }
}
```

## 검증 기준

변경 후에는 아래 항목을 확인한다.

- OpenAPI 문서에서 endpoint 설명이 이해하기 쉬운가?
- 성공 응답과 실패 응답의 구조가 일관적인가?
- 클라이언트가 에러 코드를 보고 처리할 수 있는가?
````

---

## Step 4. 같은 요청 다시 해보기

Copilot Chat에서 다시 요청합니다.

```text
이 FastAPI endpoint를 우리 프로젝트 기준에 맞게 정리해줘.
```

기대 결과 방향:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Operations API")


class OrderResponse(BaseModel):
    id: int
    status: str
    amount_krw: int


@app.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
    summary="주문 상세 조회",
    description="주문 ID를 기준으로 주문 상태와 결제 금액을 조회합니다.",
)
def get_order(order_id: int) -> OrderResponse:
    """주문 ID로 주문 상세 정보를 조회합니다."""
    if order_id == 1:
        return OrderResponse(
            id=1,
            status="paid",
            amount_krw=12000,
        )

    raise HTTPException(
        status_code=404,
        detail={
            "code": "ORDER_NOT_FOUND",
            "message": "주문을 찾을 수 없습니다.",
        },
    )
```

확인할 점:

- 한국어 설명을 하는가?
- `summary`, `description`을 추가하는가?
- Pydantic model을 쓰는가?
- `amount`를 `amount_krw`처럼 더 명확하게 바꾸는가?
- 404를 dict가 아니라 `HTTPException`으로 처리하는가?

---

## Step 5. path-specific instruction 추가

이번에는 API 파일에만 더 강한 규칙을 적용합니다.

이번에도 직접 파일을 편집하지 않고 `/create-instructions`를 사용합니다.

```text
/create-instructions

FastAPI endpoint 파일에만 적용되는 세부 기준을 추가하고 싶어.
대상은 app.py와 src/api/**/*.py 로 해줘.

- endpoint 이름은 동사보다 리소스 중심으로 작성한다.
- 응답 model은 endpoint 근처가 아니라 models 영역으로 분리할 수 있는지 먼저 검토한다.
- status code가 중요한 endpoint는 status_code를 명시한다.
- 리소스를 생성하는 endpoint는 201을 사용한다.
- 리소스를 찾지 못한 경우 404를 사용한다.
- 입력값 검증이 필요한 경우 Pydantic request model을 사용한다.
- 단순 예제 코드가 아니라 운영 코드처럼 읽히게 작성한다.
```

생성 결과는 `.github/instructions/fastapi-endpoints.instructions.md`에 저장되고, 내용은 아래 방향이면 됩니다.

```markdown
---
applyTo: "app.py,src/api/**/*.py"
---

# FastAPI endpoint 세부 기준

FastAPI endpoint를 수정할 때는 아래 기준을 우선 적용한다.

- endpoint 이름은 동사보다 리소스 중심으로 작성한다.
- 응답 model은 endpoint 근처가 아니라 models 영역으로 분리할 수 있는지 먼저 검토한다.
- status code가 중요한 endpoint는 `status_code`를 명시한다.
- 리소스를 생성하는 endpoint는 201을 사용한다.
- 리소스를 찾지 못한 경우 404를 사용한다.
- 입력값 검증이 필요한 경우 Pydantic request model을 사용한다.
- 단순 예제 코드가 아니라 운영 코드처럼 읽히게 작성한다.
```

---

## Step 6. 새 endpoint 추가 요청

Copilot Chat에서 아래처럼 요청합니다.

```text
주문 취소 endpoint를 하나 추가해줘.
우리 FastAPI endpoint 기준을 따라줘.
```

기대 결과 방향:

```python
class CancelOrderResponse(BaseModel):
    id: int
    status: str
    message: str


@app.post(
    "/orders/{order_id}/cancel",
    response_model=CancelOrderResponse,
    status_code=200,
    summary="주문 취소",
    description="주문 ID를 기준으로 결제 전 주문을 취소합니다.",
)
def cancel_order(order_id: int) -> CancelOrderResponse:
    """주문 ID로 주문을 취소합니다."""
    if order_id != 1:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "ORDER_NOT_FOUND",
                "message": "주문을 찾을 수 없습니다.",
            },
        )

    return CancelOrderResponse(
        id=order_id,
        status="cancelled",
        message="주문이 취소되었습니다.",
    )
```
