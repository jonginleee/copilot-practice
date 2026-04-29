# Day2 Practice1-1. Python Test Helper Custom Agent 실습

이 실습은 VS Code Copilot Custom Agent를 사용해 Python 코드 품질 개선 작업을 반복 가능한 방식으로 표준화하는 데 목적이 있습니다.

핵심 학습 포인트:
- Python 코드 읽기
- pytest 테스트 작성
- 엣지 케이스 탐색
- 타입 힌트와 docstring 개선 제안
- 테스트 실행/검증 명령 안내

---

## 실습 폴더

아래 Start 폴더를 VS Code에서 열고 진행합니다.

- `Day2/Practice1-1/Start/python-agent-demo`

초기 파일 구조:

```text
python-agent-demo/
├─ src/
│  └─ calculator.py
└─ tests/
   └─ test_calculator.py
```

---

## Step 1. 예제 코드 확인

`src/calculator.py`에는 아래 함수 3개가 준비되어 있습니다.

```python
def divide(a, b):
	return a / b


def calculate_discount(price, discount_rate):
	return price * (1 - discount_rate)


def normalize_name(name):
	return name.strip().title()
```

`tests/test_calculator.py`는 빈 상태(초기 주석만 포함)입니다.

---

## Step 2. /create-agent로 Custom Agent 생성

Copilot Chat에서 아래처럼 `/create-agent`를 실행해 Python 테스트 전용 에이전트를 생성합니다.

```text
/create-agent

Python 테스트 작성 전용 Custom Agent를 만들어줘.
이름은 Python Test Helper로 하고, 역할은 아래를 따르도록 해줘.

1. 테스트 수정 전에 대상 Python 파일을 먼저 읽는다.
2. pytest 스타일 테스트를 우선한다.
3. 정상/엣지/오류 케이스를 모두 다룬다.
4. 코드나 사용자 요청에 없는 동작을 임의로 만들지 않는다.
5. 동작이 불명확하면 가정을 명시하거나 확인 질문을 한다.
6. 복잡한 파라미터화보다 읽기 쉬운 테스트를 우선한다.
7. 타입 힌트/docstring은 가독성 개선에 필요할 때만 제안한다.
8. 요청이 없으면 프로덕션 코드를 변경하지 않는다.
9. 테스트 실행 명령은 아래를 우선 안내한다.
	- python -m pytest
	- python -m pytest tests/test_calculator.py
10. 작업 마지막에 아래를 요약한다.
	- 추가한 테스트
	- 커버한 엣지 케이스
	- 추가 확인이 필요한 동작
11. 숫자 함수는 항상 0/음수/경계값/잘못된 타입을 검토한다.
12. 문자열 함수는 항상 빈 문자열/앞뒤 공백/대소문자 혼합/필요 시 비ASCII를 검토한다.

도구는 read, edit, search 중심으로 제한해줘.
생성 파일은 .github/agents 아래에 저장해줘.
```

생성 후 `.github/agents` 아래 생성된 에이전트 파일을 열어 규칙이 잘 들어갔는지 확인합니다.

확인 포인트:
- pytest 중심 테스트 작성
- 정상 / 엣지 / 오류 케이스 모두 고려
- 프로덕션 코드는 요청 없으면 변경 금지
- 실행 명령은 `python -m pytest`와 `python -m pytest tests/test_calculator.py` 우선 사용
- 숫자 함수와 문자열 함수의 필수 엣지 케이스 체크리스트 포함

이렇게 역할을 좁히면, Agent가 매번 비슷한 품질 기준으로 동작합니다.

---

## Step 3. 생성한 Agent로 테스트 작성

Copilot Chat에서 방금 생성한 Python Test Helper 에이전트를 선택한 뒤 아래 프롬프트를 입력합니다.

```text
Python Test Helper 에이전트를 사용해서 src/calculator.py에 대한 pytest 테스트를 추가해줘.
엣지 케이스 중심으로 작성하고 프로덕션 코드는 변경하지 마.
```

기대 결과:
- `tests/test_calculator.py`에 정상/예외/경계 테스트가 추가됨
- 최소 포함 권장 항목
  - divide: 정상 나눗셈, 0으로 나누기
  - calculate_discount: 일반 할인, 할인율 0
  - normalize_name: 공백 정리, title 처리, 빈 문자열

---

## Step 4. 같은 Agent로 검증 및 리뷰

아래 요청으로 테스트 품질을 점검합니다.

```text
Python Test Helper 에이전트를 사용해서 테스트를 리뷰해줘.
중요한 엣지 케이스가 빠졌는지 확인해줘.
```

또는 리팩터링 제안만 받습니다.

```text
Python Test Helper 에이전트를 사용해서 src/calculator.py에 대한 최소 리팩터링 제안을 해줘.
아직 파일은 수정하지 마.
```

검토 시 확인할 질문:
- 할인율이 1보다 큰 경우의 정책은?
- 음수 price/discount_rate 허용 여부는?
- normalize_name에서 비ASCII 문자열 처리 정책은?

---

## Step 5. /create-agent로 지침 업데이트 후 재실행

처음 생성한 에이전트를 개선하고 싶다면 `/create-agent`를 다시 사용해 지침을 업데이트합니다.

예시 요청:

```text
/create-agent

기존 Python Test Helper 에이전트 지침을 보강해줘.
숫자 함수와 문자열 함수의 엣지 케이스 확인 규칙을 더 강조하고,
마지막 요약에 "정책이 불명확한 항목" 섹션을 반드시 포함해줘.
```

업데이트 후 다시 아래처럼 요청해 테스트를 개선합니다.

```text
Python Test Helper 에이전트를 다시 사용해서,
업데이트된 지침에 맞게 테스트를 개선해줘.
```

학습 포인트:

Custom Agent는 일회성 프롬프트가 아니라, 반복 업무를 동일 기준으로 수행하도록 만든 전문 역할을 하는 에이전트 입니다.

---

## 테스트 실행 방법

프로젝트 루트(`python-agent-demo`)에서 실행:

```bash
python -m pytest
```

특정 파일만 실행:

```bash
python -m pytest tests/test_calculator.py
```