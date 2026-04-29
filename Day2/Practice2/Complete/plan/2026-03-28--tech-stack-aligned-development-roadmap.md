---
title: src 기반 프론트/백엔드 스캐폴드 구축
date_created: 2026-03-28
---
# 구현 계획: src 폴더 기반 최소 실행 구조 구축
상세 기능 개발이나 대규모 체크리스트 대신, `src` 아래에 프론트/백엔드 구조를 만들고 FastAPI API와 Streamlit UI를 실제로 띄워 확인할 수 있는 최소 실행 기반만 만든다.

## 아키텍처 및 설계
- 목표 구조(예시)
  - `src/backend/app/main.py`: FastAPI 엔트리포인트
  - `src/backend/app/api/routes/menu.py`: 메뉴 조회 샘플 라우트
  - `src/backend/app/schemas/menu.py`: 응답 스키마
  - `src/frontend/kiosk_app.py`: Streamlit 엔트리포인트
  - `src/frontend/pages/menu.py`: 메뉴 조회 화면 샘플
  - `tests/backend/test_health.py`: API 기동/헬스체크 테스트
- 최소 연동 흐름
  - Streamlit 화면에서 백엔드 `GET /menus` 호출
  - 샘플 메뉴 목록 렌더링으로 API-UI 연결 확인
- 구현 범위
  - 더미 데이터 기반으로 동작 확인까지만 수행
  - 주문/장바구니/관리자 상세 기능은 본 계획 범위에서 제외
  - 샘플 데이터는 JSON 파일로 관리하고, 추후 필요 시 SQLite 시드로 전환

## 작업 목록
- [x] `src/backend`와 `src/frontend` 기본 디렉터리 생성
  - 수용 기준: 백엔드/프론트 엔트리 파일과 최소 라우트/페이지 파일이 생성됨
- [x] FastAPI 최소 앱 구성 및 샘플 메뉴 조회 API 추가
  - 수용 기준: 로컬 실행 시 `/docs`와 `/menus` 응답 확인이 가능함
- [x] Streamlit 최소 앱 구성 및 메뉴 조회 화면 추가
  - 수용 기준: 화면에서 API 호출 후 샘플 메뉴 목록이 표시됨
- [x] 로컬 실행 방법 문서화
  - 수용 기준: API/Streamlit 실행 명령과 접속 URL이 문서에 정리됨
- [x] 최소 검증 테스트 구성
  - 수용 기준: API 헬스체크 테스트 1개 이상과 Streamlit 수동 확인 절차가 준비됨

## 미결 사항
- 현재 기준 미결 사항 없음
