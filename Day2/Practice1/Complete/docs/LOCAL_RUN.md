# 로컬 실행 가이드

## 1. 의존성 설치

```bash
pip install -r requirements.txt
```

## 2. FastAPI 실행

```bash
uvicorn app.main:app --app-dir src/backend --reload --port 8000
```

- API 문서: http://localhost:8000/docs
- 헬스 체크: http://localhost:8000/health
- 메뉴 조회: http://localhost:8000/menus

## 3. Streamlit 실행

```bash
streamlit run src/frontend/kiosk_app.py --server.port 8501
```

- 앱: http://localhost:8501
- Menu 페이지에서 API Base URL(`http://localhost:8000`)로 조회 확인

## 4. 테스트 실행

```bash
pytest -q
```
