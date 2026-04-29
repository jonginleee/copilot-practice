# FastAPI 주문 API 연동 가이드 (키오스크 개발자용)

이 문서는 이 프로젝트에서 **주문(Order) 기능만** 연동하려는 개발자를 위한 가이드입니다.
제품/아키텍처 전반 설명은 아래 문서를 참고하세요.

- [제품 목표 및 기능 범위](./PRODUCT.md)
- [시스템 아키텍처](./ARCHITECTURE.md)
- [개발 가이드라인](./CONTRIBUTING.md)

## 1) 개요

주문 생성 API는 장바구니에 담긴 항목을 기준으로 주문을 확정하고, 주문번호와 주문 요약을 반환합니다.

- Endpoint: `POST /orders`
- 인증: 필요 없음 (현재 구현 기준)
- 요청 바디: 없음
- 선행 조건: 장바구니에 최소 1개 항목 존재
- 성공 시 동작:
  - 주문/주문항목 DB 저장
  - 장바구니 비움
  - 주문 응답 반환

## 2) 요청 방법

### 2.1 주문 생성

- Method: `POST`
- Path: `/orders`
- Headers:
  - 필수 헤더 없음
  - `Content-Type`은 생략 가능 (바디가 없기 때문)
- Path/Query/Body 파라미터: 없음

예시:

```bash
curl -X POST "http://127.0.0.1:8000/orders"
```

### 2.2 주문 전 선행 호출 (장바구니 담기)

주문 API 자체는 바디를 받지 않으므로, 주문 내용은 장바구니 상태로 결정됩니다.
즉, 주문 전에는 최소 1회 이상 장바구니 API를 호출해야 합니다.

- Method: `POST`
- Path: `/cart/items`
- Body(JSON):
  - `menu_id` (int, 필수)
  - `quantity` (int, 필수, `>= 1`)

예시:

```bash
curl -X POST "http://127.0.0.1:8000/cart/items" \
  -H "Content-Type: application/json" \
  -d '{"menu_id": 1, "quantity": 2}'
```

## 3) 응답 형식

### 3.1 주문 생성 성공 (`200 OK`)

```json
{
  "order_number": 12,
  "timestamp": "2026-03-29 08:21:17",
  "total_price": 13800,
  "items": [
    {
      "menu_id": 1,
      "name": "Classic Burger",
      "category": "burger",
      "image_url": "/static/images/burger/classic.png",
      "price": 6900,
      "quantity": 2,
      "subtotal": 13800
    }
  ]
}
```

필드 설명:

- `order_number`: DB에 저장된 주문 ID
- `timestamp`: 주문 생성 시각 문자열 (`YYYY-MM-DD HH:MM:SS`)
- `total_price`: 주문 총액
- `items`: 주문 항목 목록
  - 각 항목은 메뉴/카테고리/이미지/단가/수량/소계 포함

## 4) 실전 curl 시나리오

### 4.1 정상 주문 플로우

```bash
# 1) 장바구니 비우기 (테스트 시작 전 권장)
curl -X DELETE "http://127.0.0.1:8000/cart"

# 2) 장바구니 담기
curl -X POST "http://127.0.0.1:8000/cart/items" \
  -H "Content-Type: application/json" \
  -d '{"menu_id": 1, "quantity": 2}'

# 3) 주문 생성
curl -X POST "http://127.0.0.1:8000/orders"

# 4) 장바구니가 비워졌는지 확인
curl -X GET "http://127.0.0.1:8000/cart"
```

## 5) 주의할 점

- 주문 API는 **요청 바디가 없는 설계**입니다.
- 주문 금액/항목은 요청 payload가 아니라 장바구니 데이터로 계산됩니다.
- 주문 성공 후 장바구니는 자동으로 초기화됩니다.
- 키오스크 화면에서 중복 탭(다중 클릭) 방지가 필요합니다.
  - 같은 장바구니 상태로 연속 `POST /orders` 호출 시 첫 호출 후 장바구니가 비워지므로, 다음 호출은 실패(`400`)할 수 있습니다.

## 6) 에러 및 디버깅

### 6.1 `400 Bad Request`

장바구니가 비어 있을 때 발생합니다.

예시 응답:

```json
{
  "detail": "장바구니가 비어 있어 주문할 수 없습니다."
}
```

점검 순서:

1. `GET /cart`로 `items`가 비어 있지 않은지 확인
2. 주문 직전에 다른 로직이 `DELETE /cart`를 호출하지 않았는지 확인
3. UI에서 주문 버튼 중복 호출이 없는지 확인

### 6.2 `405 Method Not Allowed`

잘못된 HTTP 메서드를 사용했을 때 발생합니다.

- 주문 생성은 `POST /orders`만 허용
- 예: `GET /orders` 호출 시 405

### 6.3 `422 Unprocessable Entity` (주문 API보다 선행 API에서 주로 발생)

`POST /orders`는 바디를 받지 않으므로 422 가능성이 낮습니다.
대신 주문 전 단계인 장바구니 API에서 자주 발생합니다.

대표 원인:

- `POST /cart/items`에서 `menu_id` 누락
- `quantity` 누락
- `quantity`가 1 미만 (`0`, `-1`)
- 타입 불일치 (예: 문자열)

잘못된 요청 예시:

```bash
curl -X POST "http://127.0.0.1:8000/cart/items" \
  -H "Content-Type: application/json" \
  -d '{"menu_id": 1, "quantity": 0}'
```

점검 포인트:

1. JSON 키 이름 오타 여부 (`menu_id`, `quantity`)
2. `quantity >= 1` 충족 여부
3. 숫자 타입으로 전달했는지 여부

## 7) 로컬 확인 빠른 체크

서버 실행/기본 URL은 [LOCAL_RUN.md](./LOCAL_RUN.md)를 따릅니다.

- FastAPI Base URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

Swagger에서 `/orders`와 `/cart/items`를 함께 테스트하면 연동 확인이 가장 빠릅니다.
