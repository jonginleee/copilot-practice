# Day2 Practice1-3. pytest 실패 로그를 원인 분류 + 재현 가이드로 정리하는 Skill 만들기

이 실습은 VS Code Copilot Chat의 `/create-skill` 명령으로 pytest 실패 로그와 traceback을 분석하는 Skill을 만드는 흐름을 연습합니다.

핵심 학습 포인트:
- `/create-skill`로 Workspace Skill 생성
- `SKILL.md`에 분석 순서와 출력 규칙 정의
- `references/`에 실패 원인 분류 기준 저장
- `assets/`에 최종 리포트 템플릿 저장
- Skill 결과를 보고 지침을 개선하는 반복 흐름 익히기

---

## 실습 폴더

아래 Start 폴더를 VS Code에서 열고 진행합니다.

- `Day2/Practice1-3/Start/python-skill-demo`

초기 파일 구조:

```text
python-skill-demo/
├─ src/
│  └─ pricing.py
├─ requirements.txt
└─ tests/
   └─ test_pricing.py
```

---

## Step 0. 의존성 설치

프로젝트 루트(`python-skill-demo`)에서 코파일럿에게 아래의 명령을 실행해 달라고 합니다.

```bash
python -m pip install -r requirements.txt
```

---

## Step 1. 예제 Python 파일 확인

`src/pricing.py`에는 아래 함수가 준비되어 있습니다.

```python
def apply_discount(price, discount_rate):
    return price * (1 - discount_rate)
```

`tests/test_pricing.py`에는 아래 테스트가 준비되어 있습니다.

```python
from src.pricing import apply_discount


def test_apply_discount_rounds_to_two_decimals():
    assert apply_discount(19.99, 0.15) == 16.99
```

이 테스트는 실제로 `16.9915`를 반환할 수 있어서 실패합니다.

---

## Step 2. 실패 재현

프로젝트 루트(`python-skill-demo`)에서 아래 명령을 실행합니다.

```text
pytest를 실행해줘.
```

기대되는 실패 포인트:
- `FAILED tests/test_pricing.py::test_apply_discount_rounds_to_two_decimals`
- `assert 16.9915 == 16.99`
- 반올림 정책이 코드에 없는데 테스트는 소수점 둘째 자리 결과를 기대함

---

## Step 3. /create-skill 실행

Copilot Chat에서 아래처럼 입력합니다.

```text
/create-skill
```

Skill 설명은 아래 예시를 사용합니다.

```text
pytest 실패 로그를 분석하는 Skill을 만들고 싶어.

이 Skill은 Python 테스트 실패 로그나 traceback을 입력받으면,
실패 원인을 분류하고, 재현 방법과 수정 방향을 한국어로 정리해줘.

references 폴더에는 실패 원인 분류 기준을 두고,
assets 폴더에는 최종 리포트 템플릿을 둘 거야.

Skill 이름은 pytest-failure-triage로 해줘.
```

위치 선택 질문이 나오면 실습에서는 **Workspace Skill**을 선택합니다.

---

## Step 4. 생성된 Skill 구조 확인

생성 후 파일 구조가 아래와 유사한지 확인합니다.

```text
.github/
└─ skills/
   └─ pytest-failure-triage/
      └─ SKILL.md
```

이제 아래 파일을 직접 추가합니다.

```text
.github/
└─ skills/
   └─ pytest-failure-triage/
      ├─ SKILL.md
      ├─ references/
      │  └─ failure-taxonomy.md
      └─ assets/
         └─ triage-report-template.md
```

---

## Step 5. references 추가

만약 자동으로 references를 추가하지 않았다면 `references/failure-taxonomy.md`에 아래 기준을 넣습니다.
파일이 생성되었다면 통과합니다.

```markdown
# pytest 실패 원인 분류 기준

pytest 실패를 분석할 때 아래 기준으로 원인을 분류한다.

## 1. Assertion mismatch

기대값과 실제값이 다르다.

예:
- `assert 16.9915 == 16.99`
- 반올림 정책이 정해지지 않음
- 계산 결과의 precision 문제가 있음

## 2. Exception raised

테스트 실행 중 예외가 발생했다.

예:
- ZeroDivisionError
- TypeError
- ValueError
- ImportError

## 3. Missing behavior definition

코드가 잘못되었다기보다, 기대 동작이 명확하지 않다.

예:
- 음수 가격을 허용할지 불명확함
- 할인율이 1보다 클 때 정책이 없음
- 반올림 기준이 문서화되어 있지 않음

## 4. Test setup issue

테스트 코드나 환경 설정 문제다.

예:
- import path 문제
- fixture 누락
- mock 설정 오류
- 테스트 데이터 준비 누락

## 5. Regression candidate

기존에는 통과했을 가능성이 높고, 최근 변경으로 깨졌을 수 있다.

예:
- 같은 기능의 다른 테스트는 통과함
- 최근 수정된 함수에서만 실패함
- 실패가 특정 입력에서만 발생함
```

---

## Step 6. assets 추가

만약 자동으로 references를 추가하지 않았다면 `assets/triage-report-template.md`에 아래 템플릿을 넣습니다.

```markdown
# Pytest 실패 분석 리포트

## 1. 요약
- 실패 유형:
- 영향 범위:
- 우선순위:

## 2. 실패 로그 핵심
```text
[중요한 실패 메시지나 assertion만 발췌]
```

## 3. 원인 추정
- 가장 가능성 높은 원인:
- 근거:
- 확신도: 높음 / 중간 / 낮음

## 4. 재현 방법

## 5. 수정 방향
- 권장 수정:
- 대안:
- 주의할 점:

## 6. 추가로 확인할 것

---

## Step 7. Skill 사용해보기

Copilot Chat에서 아래처럼 입력합니다.

```text
아래 pytest 실패 로그를 분석해줘.

FAILED tests/test_pricing.py::test_apply_discount_rounds_to_two_decimals

E       assert 16.9915 == 16.99
E        +  where 16.9915 = apply_discount(19.99, 0.15)
```

기대 결과 방향:
- 실패 유형: `Assertion mismatch` 또는 `Missing behavior definition`
- 핵심 원인: `apply_discount`가 반올림을 하지 않는데 테스트는 소수점 둘째 자리 결과를 기대함
- 수정 방향:
  1. 함수가 항상 소수점 둘째 자리로 반올림해야 한다면 `round(..., 2)` 적용
  2. 반올림이 함수 책임이 아니라면 테스트 기대값을 `16.9915`로 수정
  3. 가격 계산 정책을 먼저 명확히 정의

---

## Step 8. Skill 개선하기

마지막에 `SKILL.md`에 아래 규칙을 추가합니다.

```markdown
## 추가 규칙

- 금액 계산과 관련된 실패는 반올림, 부동소수점 오차, 통화 단위 정책을 반드시 확인한다.
- 기대값이 소수점 둘째 자리인데 실제값이 더 긴 소수라면, 반올림 정책이 누락되었을 가능성을 우선 검토한다.
- 수정 방향은 "코드 수정"과 "테스트 기대값 수정"을 나누어 제안한다.
```

다시 실행합니다.

```text
/pytest-failure-triage

방금 추가한 기준까지 반영해서 같은 실패 로그를 다시 분석해줘.
```

---

## 실습에서 배우는 것

1. `/create-skill`로 Skill을 만든다.
2. `SKILL.md`에는 작업 순서를 적는다.
3. `references/`에는 판단 기준을 둔다.
4. `assets/`에는 최종 출력 템플릿을 둔다.
5. 결과를 보고 Skill 지침을 개선한다.

---