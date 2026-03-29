# Copilot 실습: Todo 앱 만들기

## 실습 목표

GitHub Copilot을 활용하여 Python 로직 → 테스트 → API → UI까지 간단한 서비스 개발 흐름을 한 번에 경험

---

## 사용 기술

* Python: 핵심 비즈니스 로직 구현
* pytest: 핵심 로직 단위 테스트
* FastAPI: REST API 구성
* Streamlit: API 기반 UI 구현

---

## 구현 범위 (Minimal Spec)

기능 4개만 구현

* 할 일 추가
* 목록 조회
* 완료 토글
* 삭제

조건

* DB 없이 메모리 기반
* API 4개만 구성 

---

## 진행 순서

1. Python으로 TodoService 구현
2. pytest로 핵심 로직 테스트 작성
3. FastAPI로 로직을 API에 연결
4. Streamlit으로 API 호출 UI 구성

---

## 완료 기준

* pytest 통과
* FastAPI /docs에서 API 동작 확인
* Streamlit에서 CRUD 동작 확인

---