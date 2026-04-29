# ARCHITECTURE.md — 햄버거 가게 키오스크 시스템

---

## 1. 아키텍처 개요

본 시스템은 백엔드 API와 키오스크 화면을 분리한 2계층 구조를 기반으로 합니다.

- **FastAPI**: 주문/메뉴/매출 관리 API 제공
- **Streamlit**: 키오스크 화면 및 관리자 화면 UI 제공
- **SQLite**: 로컬 단일 파일 DB로 주문/메뉴 데이터 저장
- **SQLAlchemy**: DB 스키마 및 데이터 접근 계층(ORM) 표준화

초기 목표는 매장 내 단일 단말(또는 소수 단말) 환경에서 빠르게 운영 가능한 구조를 제공하는 것입니다. 이후 트래픽 증가 시 SQLite를 PostgreSQL 등으로 전환할 수 있도록 ORM 중심 설계를 유지합니다.

---

## 2. 기술 스택 선정 이유

| 구성 요소 | 기술 | 선정 이유 |
|------|------|------|
| **백엔드 API** | FastAPI | 비동기 지원, 명확한 라우팅, 자동 API 문서(OpenAPI) 제공으로 개발/테스트 효율이 높음 |
| **프론트엔드(UI)** | Streamlit | 빠른 프로토타이핑 및 터치 기반 키오스크 화면 구현이 쉬움 |
| **데이터 저장소** | SQLite | 설치/운영 부담이 낮고 로컬 파일 기반이라 소규모 매장 환경에 적합 |
| **ORM** | SQLAlchemy | 도메인 모델 중심 개발 가능, DB 전환 시 영향 최소화 |

기술 조합의 핵심은 “빠른 개발 + 단순 운영 + 이후 확장 가능성 확보”입니다.

---

## 3. 모듈 구조

권장 디렉터리 구조는 다음과 같습니다.

```text
project/
  app/
    api/
      routes/
        menu.py
        cart.py
        order.py
        admin.py
      deps.py
    core/
      config.py
      logging.py
      security.py
    db/
      base.py
      session.py
      models.py
      repositories/
        menu_repository.py
        order_repository.py
    schemas/
      menu.py
      cart.py
      order.py
      common.py
    services/
      menu_service.py
      cart_service.py
      order_service.py
      sales_service.py
    main.py
  ui/
    kiosk_app.py
    admin_app.py
    pages/
      menu.py
      cart.py
      checkout.py
      order_done.py
      admin_menu.py
      admin_orders.py
      admin_sales.py
  docs/
    PRODUCT.md
    ARCHITECTURE.md
```

모듈 책임은 다음과 같이 분리합니다.

- **routes**: HTTP 엔드포인트 정의, 요청/응답 바인딩
- **schemas**: 요청/응답 DTO(Pydantic), 입력 검증
- **services**: 주문 금액 계산, 재고/품절 검증 등 비즈니스 로직
- **repositories**: SQLAlchemy를 통한 데이터 접근 캡슐화
- **db**: 모델/세션/DB 초기화 등 영속성 설정
- **ui**: 화면 흐름, 사용자 입력, API 호출 및 상태 표시

이 구조는 UI 변경(예: Streamlit → Web SPA) 시 비즈니스 로직 재사용이 가능하도록 설계되었습니다.

---

## 4. 데이터 흐름

### 4.1 고객 주문 흐름

1. Streamlit 키오스크 화면이 FastAPI의 메뉴 조회 API 호출
2. 고객이 메뉴 선택 및 수량 조정 후 장바구니 구성
3. 주문 버튼 클릭 시 Streamlit이 주문 생성 API 호출
4. FastAPI Service 계층에서 금액 계산, 품절/유효성 검증 수행
5. Repository 계층이 SQLAlchemy 세션을 통해 SQLite에 주문/주문항목 저장
6. 저장 완료 후 주문번호와 요약 금액을 응답
7. Streamlit이 주문 완료 화면 및 주문번호 표시

### 4.2 관리자 운영 흐름

1. 관리자 화면에서 메뉴 등록/수정/품절 처리 요청
2. FastAPI가 검증 후 DB 반영
3. 주문 현황/매출 조회 요청 시 집계 쿼리 또는 서비스 계산 결과 반환
4. Streamlit 관리자 페이지에서 테이블/요약 카드 형태로 시각화

### 4.3 트랜잭션/일관성

- 주문 생성은 단일 트랜잭션으로 처리하여 주문 헤더/상세 불일치 방지
- 실패 시 롤백하여 부분 저장 방지
- 입력 검증은 API 계층(스키마) + 서비스 계층(도메인 규칙) 2중으로 수행

---

## 5. 설계 원칙

### 5.1 계층 분리(Separation of Concerns)

- UI, API, 비즈니스 로직, 데이터 접근을 분리하여 변경 파급 최소화
- 라우터에는 비즈니스 로직을 두지 않고 서비스로 위임

### 5.2 단순성 우선(Simple First)

- 초기 릴리즈는 SQLite 단일 DB 파일로 운영 복잡도 최소화
- 복잡한 분산 구조 대신 매장 운영에 필요한 안정성과 유지보수성을 우선

### 5.3 확장 가능성(Scalability Path)

- SQLAlchemy 사용으로 DB 엔진 교체 비용 절감
- API 계약(스키마) 고정으로 UI/외부 채널 확장 가능
- 서비스 계층 중심 설계로 기능 추가 시 재사용성 확보

### 5.4 신뢰성/운영성(Reliability & Operability)

- 주문 생성, 상태 변경 등 핵심 이벤트에 대한 로깅 표준화
- 예외 응답 포맷 통일(오류 코드, 사용자 메시지 분리)
- 헬스체크 및 기본 모니터링 지표(요청 수, 실패율, 응답 시간) 확보

### 5.5 보안/권한(Security by Default)

- 관리자 API는 인증/권한 검증 후 접근 허용
- 민감정보 최소 저장 원칙 준수
- 입력값 검증 및 SQLAlchemy 파라미터 바인딩으로 인젝션 위험 완화

---

## 6. 배포 및 운영 관점(로컬 매장 기준)

- FastAPI 서버와 Streamlit 앱을 동일 로컬 네트워크 또는 단일 장비에서 실행
- SQLite 파일 백업 정책(일 단위) 적용
- 장애 대응: 앱 재기동 시 데이터 파일 기반으로 빠른 복구 가능

본 아키텍처는 소규모 매장 운영에 최적화된 실용적 구조이며, 기능 확장 및 인프라 고도화에 대비한 명확한 진화 경로를 제공합니다.

---

*최종 수정일: 2026-03-28*
