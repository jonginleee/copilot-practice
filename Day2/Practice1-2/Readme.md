# Day2 Practice1-2. /create-skill로 Python 코드 리뷰 Skill 만들기

이 실습은 VS Code Copilot Chat의 `/create-skill` 명령으로 Python 코드 리뷰 기준을 재사용 가능한 Skill로 만드는 흐름을 연습합니다.

핵심 학습 포인트:
- `/create-skill`로 Workspace Skill 생성
- `SKILL.md`의 `name`과 `description` 이해
- 코드 리뷰 출력 형식 표준화
- Skill 호출 후 결과 확인
- `SKILL.md` 수정으로 Skill 개선

---

## 실습 폴더

아래 Start 폴더를 VS Code에서 열고 진행합니다.

- `Day2/Practice1-2/Start/python-skill-demo`

초기 파일 구조:

```text
python-skill-demo/
└─ src/
   └─ calculator.py
```

---

## Step 1. 실습용 Python 파일 확인

`src/calculator.py`에는 아래 함수 3개가 준비되어 있습니다.

```python
def calculate_discount(price, discount_rate):
    return price * (1 - discount_rate)


def normalize_name(name):
    return name.strip().title()


def divide(a, b):
    return a / b
```

---

## Step 2. /create-skill 실행

Copilot Chat에서 아래처럼 입력합니다.

```text
/create-skill
```

Skill 설명은 아래 예시를 사용합니다.

```text
Python 코드를 리뷰하는 Skill을 만들고 싶어.
코드가 하는 일을 요약하고, 버그 가능성, edge case, pytest 테스트 아이디어를 한국어로 정리해주는 Skill이야.
출력은 요약, 발견한 점, 테스트 아이디어, 확인이 필요한 부분, 추천 다음 단계 순서로 나오면 좋겠어.
```

위치 선택 질문이 나오면 실습에서는 **Workspace Skill**을 선택합니다.

---


## Step 3. 생성된 Skill 확인

생성 후 파일 구조가 아래와 유사한지 확인합니다.

```text
.github/
└─ skills/
   └─ python-code-review/
      └─ SKILL.md
```

`SKILL.md` frontmatter 확인 포인트:

```markdown
---
name: python-code-review
description: use when reviewing Python code, explaining Python functions, identifying possible bugs, or suggesting pytest tests and improvements for Python snippets or files.
---
```

---

## Step 4. Skill 사용해보기

Skill은 slash command가 아니라, Copilot이 `description`을 보고 자동으로 로드하거나 자연어로 명시해서 호출합니다.

Copilot Chat(Agent 모드)에서 아래처럼 실행합니다.

```text
python-code-review Skill을 사용해서 #file:src/calculator.py 를 리뷰해줘.
```

또는 Skill 이름 없이 요청해도 description이 일치하면 자동 로드됩니다.

```text
#file:src/calculator.py 를 리뷰해줘. 버그 가능성과 pytest 테스트 아이디어 중심으로.
```

기대 포인트:
- `divide(a, b)`는 `b=0`일 때 `ZeroDivisionError` 가능성
- `calculate_discount`는 음수 가격/음수 할인율/1 초과 할인율 정책 불명확
- `normalize_name`은 빈 문자열/공백 문자열/비영어 입력 처리 기준 확인 필요
- 함수별 pytest 테스트 아이디어 제안

---

## Step 6. Skill 개선하기

생성된 `SKILL.md`에 아래 기준을 추가한 뒤 다시 실행합니다.

```markdown
## 추가 기준

- 리뷰 결과가 너무 길어지면 가장 중요한 문제 3개를 먼저 제시합니다.
- 테스트 아이디어는 가능한 한 함수별로 나누어 작성합니다.
- 숫자 함수는 0, 음수, 경계값, 잘못된 타입을 확인합니다.
- 문자열 함수는 빈 문자열, 앞뒤 공백, 대소문자, 비영어 입력을 확인합니다.
```

재실행 예시:

```text
python-code-review Skill을 사용해서 #file:src/calculator.py 를 다시 리뷰해줘. 방금 추가한 기준까지 반영해줘.
```

---

## 실습 마무리 메시지

```text
이번 실습에서는 /create-skill 명령으로 Python 코드 리뷰 Skill을 만들었습니다.

Skill은 한 번 쓰고 버리는 프롬프트가 아니라,
반복해서 설명하던 리뷰 기준과 출력 형식을 저장해 두고
Copilot이 필요한 순간에 다시 불러 쓰게 하는 구조입니다.
```