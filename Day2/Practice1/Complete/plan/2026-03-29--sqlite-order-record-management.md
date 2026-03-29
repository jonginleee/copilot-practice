---
title: SQLite 기반 주문 기록 관리 및 결제 결과 연동
date_created: 2026-03-29
---
# 구현 계획: SQLite 기반 주문 기록 관리 및 결제 결과 연동
백엔드에 SQLite + SQLAlchemy를 적용해 주문을 영속 저장하고, 프론트 결제(모의 완료) 시 실제 DB에 생성된 주문 번호와 timestamp를 응답으로 받아 사용자에게 표시한다. 기존 데이터 흐름(메뉴 조회 -> 장바구니 -> 주문 생성)을 유지하며 라우터/서비스/리포지토리 계층 분리를 준수한다.

## 아키텍처 및 설계
- DB/ORM 구성
  - SQLite 파일 DB를 백엔드에 연결하고 SQLAlchemy 세션/베이스를 구성한다.
  - 앱 시작 시 주문 관련 테이블(Order, OrderItem)을 생성/초기화 가능한 구조를 둔다.
- 도메인 모델
  - Order: id(자동 증가 PK), total_price, created_at(timestamp)
  - OrderItem: id, order_id(FK), menu_id, name, category, image_url, price, quantity, subtotal
  - 주문 번호는 Order.id를 사용해 DB에서 순차 증가로 관리한다.
- API 계약
  - POST /orders: 현재 장바구니를 주문으로 확정하고 DB에 저장
  - 응답: order_number(정수), timestamp(UTC ISO-8601), total_price, items 요약
  - 빈 장바구니 주문 시 400 오류
- 서비스/저장소 책임
  - routes/order.py: 요청/응답 바인딩만 담당
  - order_service.py: 장바구니 검증, 총액 검증, 주문 생성 트랜잭션 처리, 장바구니 비우기 호출
  - order_repository.py: Order/OrderItem 저장 및 조회 캡슐화
- 프론트 연동
  - 결제 버튼 클릭 시 POST /orders 호출
  - 성공 시 응답의 order_number/timestamp/total_price를 주문 완료 영역에 표시
  - 실패 시 상태코드별 사용자 메시지 표시(400/404/422/500)
- 테스트 전략
  - 백엔드: 주문 생성 정상/예외(빈 장바구니) + 저장 검증 테스트
  - 프론트: API 클라이언트 단위 테스트(성공 응답 파싱, 오류 매핑)

## 작업 목록
- [x] 백엔드 DB 인프라 추가
  - 수용 기준: SQLite 연결 설정과 SQLAlchemy Base/Session 구성이 추가되고 앱 기동 시 사용 가능하다.
- [x] 주문 모델/스키마 구현
  - 수용 기준: Order, OrderItem 모델 및 요청/응답 Pydantic 스키마가 정의된다.
- [x] 주문 저장소/서비스 구현
  - 수용 기준: 장바구니 기준 주문 생성 시 단일 트랜잭션으로 Order/OrderItem이 저장되고 order_number가 DB 자동 증가 값으로 반환된다.
- [x] 주문 API 라우트 추가 및 앱 등록
  - 수용 기준: POST /orders가 노출되고 빈 장바구니/정상 케이스 상태코드가 요구사항과 일치한다.
- [x] 프론트 결제 흐름을 실제 주문 API로 연결
  - 수용 기준: 결제 버튼이 POST /orders를 호출하고 DB 생성 주문번호/시간/총액을 UI에 표시한다.
- [x] 테스트 작성 및 회귀 검증
  - 수용 기준: 주문 API 테스트와 프론트 API 클라이언트 테스트가 추가되고 기존 cart/health 테스트와 함께 통과한다.

## 미결 사항
- 현재 기준 미결 사항 없음
