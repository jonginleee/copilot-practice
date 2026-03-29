---
title: 브라우저 주문 기능 검증 계획
date_created: 2026-03-29
---
# 구현 계획: 브라우저 주문 기능 검증
브라우저(프론트 UI)에서 메뉴 선택부터 주문 생성까지 흐름이 실제로 동작하는지 확인한다. 제품 범위(오프라인 키오스크)와 기존 데이터 흐름(메뉴 조회 -> 장바구니 -> 주문 생성 -> 저장/응답)을 기준으로 정상/예외 시나리오를 검증한다.

## 아키텍처 및 설계
- 검증 대상 경로
  - 프론트 화면: [src/frontend/kiosk_app.py](src/frontend/kiosk_app.py)
  - 프론트 API 클라이언트: [src/frontend/api_client.py](src/frontend/api_client.py)
  - 백엔드 주문 라우트: [src/backend/app/api/routes/order.py](src/backend/app/api/routes/order.py)
  - 서비스/저장 계층: [src/backend/app/services/order_service.py](src/backend/app/services/order_service.py), [src/backend/app/repositories/order_repository.py](src/backend/app/repositories/order_repository.py)
- 검증 접근 방식
  - 사용자 관점 E2E 수동 검증: 브라우저에서 실제 클릭으로 주문 생성 확인
  - API 교차 검증: 주문 직후 `GET` 또는 저장소 상태로 주문 데이터 반영 여부 확인
  - 회귀 안전성 확인: 기존 cart/order 테스트 실행으로 핵심 흐름 회귀 확인
- 성공 기준
  - 메뉴 추가 -> 장바구니 반영 -> 주문하기 클릭 -> 주문 완료 정보(주문번호/총액/시각) 확인
  - 주문 후 장바구니 상태가 기대대로 초기화되거나 정책에 맞게 갱신됨
  - 백엔드 저장소(DB)에 주문 레코드와 항목이 일관되게 저장됨

## 작업 목록
- [x] 실행 환경 점검 및 앱 기동
  - 수용 기준: 백엔드(FastAPI)와 프론트(Streamlit)가 로컬에서 모두 기동되고 헬스체크가 정상이다
- [x] 정상 주문 시나리오 브라우저 검증
  - 수용 기준: 2개 이상 메뉴를 수량 지정해 담은 뒤 주문 완료 화면까지 문제 없이 진행된다
- [x] 예외 시나리오 검증
  - 수용 기준: 빈 장바구니 주문 시 사용자 오류 메시지가 노출되고 서버 4xx 응답이 UI에서 처리된다
- [x] 저장 결과 확인
  - 수용 기준: 주문 생성 직후 주문 데이터가 API/DB 기준으로 확인 가능하며 UI 표시값과 합계가 일치한다
- [x] 회귀 테스트 실행
  - 수용 기준: `tests/backend/test_order.py`, `tests/backend/test_cart.py`, `tests/frontend/test_api_client.py`가 통과한다
- [x] 검증 결과 기록
  - 수용 기준: 통과/실패 시나리오, 재현 절차, 발견 이슈를 계획 문서에 업데이트한다

## 검증 결과
- 실행 환경
  - `http://127.0.0.1:8000/health` 응답: `{"status":"ok"}`
  - `http://127.0.0.1:8501` 응답 코드: `200`
- 정상 주문 시나리오(브라우저)
  - 메뉴 2종(Classic Burger 1개, Cheese Burger 1개) 장바구니 담기 성공
  - 총액 `13,500원` 확인 후 주문하기 성공
  - 주문 완료 UI 확인: 주문번호 `2`, 결제금액 `13,500원`, 주문시각 표시
  - 주문 완료 후 장바구니 비움 상태 확인
- 예외 시나리오
  - 빈 장바구니 상태에서 `POST /orders` 호출 시 `400` 확인
  - 응답 본문: `{"detail":"장바구니가 비어 있어 주문할 수 없습니다."}`
- 저장 결과 교차 검증(DB)
  - 최신 주문 레코드: `id=2`, `total_price=13500`
  - 주문 항목: `(1, Classic Burger, qty=1, subtotal=6500)`, `(2, Cheese Burger, qty=1, subtotal=7000)`
  - 항목 합계와 주문 총액 일치 확인
- 회귀 테스트
  - `pytest -q tests/backend/test_order.py tests/backend/test_cart.py tests/frontend/test_api_client.py`
  - 결과: `21 passed, 2 warnings`

## 미결 사항
- 현재 검증 범위 내 차단 이슈 없음
- 참고: FastAPI `on_event("startup")` deprecation warning 2건이 테스트 중 관찰됨(기능 동작에는 영향 없음)
