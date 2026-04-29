---
title: 키오스크 UI 이미지 표시
date_created: 2026-03-29
---

# 구현 계획: 키오스크 UI 이미지 표시

`resources/` 디렉터리에 있는 메뉴 이미지와 로고를 키오스크 화면에 표시한다.
로고는 기존 텍스트 타이틀을 대체하고, 메뉴 이미지는 프론트에 파일명을 하드매핑하지 않고 백엔드 데이터에서 받은 URL을 그대로 사용한다.

---

## 아키텍처 및 설계

### 이미지 제공 방식 (메뉴 이미지)

FastAPI에 정적 파일 마운트를 추가해 `resources/` 디렉터리를 `/static/images` 경로로 노출한다.

```
GET http://127.0.0.1:8000/static/images/burger_menu_classic_burger.png
```

`sample_menus.json`의 `image_url` 값을 위 경로로 교체하면 프론트는 `menu['image_url']` 값을 그대로 `st.image()`에 전달하기만 하면 되어 **파일명 하드매핑이 없다.**

```
[sample_menus.json] image_url
        ↓ (API / JSON 파일 로드 경유)
[kiosk_app.py] menu['image_url'] → st.image(url)   ← 하드매핑 없음
```

### 로고 표시 방식

`st.title("Hamburger Kiosk")` 를 제거하고 `resources/logo.png`를 `st.image()`로 교체한다.
로고 파일 경로는 런타임에 `__file__` 기준 상대 경로로 산출하며, 존재하지 않을 경우 텍스트 타이틀로 fallback한다.

```python
LOGO_PATH = Path(__file__).resolve().parents[2] / "resources" / "burger_logo.png"
if LOGO_PATH.exists():
    st.image(str(LOGO_PATH), width=240)
else:
    st.title("Hamburger Kiosk")
```

---

## 작업 목록

### 백엔드
- [x] **Task 1 – 정적 파일 마운트 추가**
  - `src/backend/app/main.py`에 `StaticFiles` 마운트 추가
  - 마운트 경로: `/static/images` → `resources/` 디렉터리
  - `resources/` 절대 경로는 `__file__` 기준으로 계산 (`Path(__file__).resolve().parents[4] / "resources"`)

- [x] **Task 2 – `sample_menus.json` image_url 교체**
  - 기존 placeholder URL → `http://127.0.0.1:8000/static/images/{파일명}.png`
  - 파일명 매핑 (JSON 수정):
    | 메뉴 | 기존 image_url | 변경 후 |
    |------|---------------|---------|
    | Classic Burger | `https://example.com/images/classic-burger.jpg` | `http://127.0.0.1:8000/static/images/burger_menu_classic_burger.png` |
    | Cheese Burger  | `https://example.com/images/cheese-burger.jpg`  | `http://127.0.0.1:8000/static/images/burger_menu_cheese_burger.png`  |
    | French Fries   | `https://example.com/images/french-fries.jpg`   | `http://127.0.0.1:8000/static/images/burger_menu_french_fries.png`   |
    | Cola           | `https://example.com/images/cola.jpg`           | `http://127.0.0.1:8000/static/images/burger_menu_coke.png`           |

### 프론트엔드
- [x] **Task 3 – 로고로 타이틀 교체**
  - `kiosk_app.py`의 `st.title("Hamburger Kiosk")`를 `st.image(LOGO_PATH)` 로 대체
  - `LOGO_PATH`는 `resources/burger_logo.png`를 가리키는 `Path` 계산식; 파일 없을 경우 fallback

- [x] **Task 4 – 메뉴 카드에 이미지 표시**
  - `render_menu_grid()` 내부 메뉴 카드 HTML 블록 위에 `st.image(menu['image_url'])` 추가
  - 이미지 로드 실패(URL 오류 등) 시 예외를 잡아 이미지 없이 카드만 렌더링하는 fallback 처리

---

## 수용 기준

1. FastAPI 기동 후 `http://127.0.0.1:8000/static/images/burger_menu_classic_burger.png` 요청이 200 OK를 반환한다.
2. Streamlit 메뉴 화면에서 각 메뉴 카드에 이미지가 표시된다.
3. 프론트 코드(`kiosk_app.py`, `api_client.py`)에 파일명 매핑 딕셔너리나 조건 분기가 없다.
4. 로고 파일이 존재하면 타이틀 대신 로고 이미지가 표시된다.
5. 로고 파일이 없어도 앱이 정상 실행된다(fallback으로 텍스트 타이틀 표시).

---