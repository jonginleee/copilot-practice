---
title: 장바구니 담기 백엔드 API 구현
date_created: 2026-03-28
---
# 구현 계획: 장바구니 담기 백엔드 API
고객이 메뉴를 수량 지정하여 장바구니에 추가·수정·삭제할 수 있는 백엔드 API를 구현한다. 품절 메뉴는 추가 불가 규칙을 서비스 계층에서 검증하고, 기존 routes → services → repositories 계층 구조를 따른다. 장바구니 데이터는 서버 메모리(세션 단위 딕셔너리)로 관리하며, 추후 DB 영속화로 전환 가능한 구조를 유지한다.

## 아키텍처 및 설계
- 엔드포인트 목록
  - `POST /cart/items`: 메뉴 추가 (menu_id, quantity)
  - `PUT /cart/items/{menu_id}`: 수량 수정
  - `DELETE /cart/items/{menu_id}`: 항목 삭제
  - `GET /cart`: 장바구니 전체 조회 (항목 목록, 합계 금액)
  - `DELETE /cart`: 장바구니 초기화
- 데이터 구조
  - `CartItem`: menu_id, name, price, quantity, subtotal
  - `Cart`: items(list[CartItem]), total_price
- 비즈니스 규칙 (CartService에서 처리)
  - 품절(is_sold_out=True) 메뉴 추가 시 400 오류 반환
  - 수량은 1 이상 정수만 허용
  - 존재하지 않는 menu_id 추가 시 404 오류 반환
  - 동일 menu_id 재추가 시 수량 누적 처리
- 저장소
  - 단일 전역 인메모리 딕셔너리(세션 구분 없이 서버 프로세스 전체 공유)
  - 추후: SQLAlchemy 세션 기반 Cart/CartItem 테이블로 전환 가능
- 합계 금액 계산
  - CartService가 추가/수정/삭제/조회 모든 변경 작업의 응답에 total_price를 계산해 반환
  - 라우터는 서비스 반환값을 그대로 응답에 바인딩하고 계산 로직을 포함하지 않음
- 의존 관계
  - CartService → CartRepository (장바구니 상태 읽기/쓰기)
  - CartService → MenuRepository (메뉴 유효성 및 품절 여부 확인)

## 작업 목록
- [x] `schemas/cart.py` 작성
  - 수용 기준: CartItemRequest, CartItem, Cart Pydantic 스키마가 정의됨
- [x] `repositories/cart_repository.py` 작성
  - 수용 기준: 인메모리 딕셔너리 기반 추가/수정/삭제/조회/초기화 메서드가 동작함
- [x] `services/cart_service.py` 작성
  - 수용 기준: 품절 검증, 수량 검증, menu_id 존재 검증이 서비스 계층에서 처리됨
- [x] `api/routes/cart.py` 작성 및 main.py에 라우터 등록
  - 수용 기준: 5개 엔드포인트가 OpenAPI 문서에 노출되고 예상 상태코드를 반환함
- [x] 단위 테스트 작성 (`tests/backend/test_cart.py`)
  - 수용 기준: 정상 추가/수정/삭제/조회, 품절 추가 거부, 잘못된 수량, 없는 menu_id 케이스를 포함함

## 미결 사항
- 현재 기준 미결 사항 없음
