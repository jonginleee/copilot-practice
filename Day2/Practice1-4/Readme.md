# Day2 Practice1-4. Script를 실행하는 Python File Counter Skill 만들기

이 실습은 VS Code Copilot Chat의 `/create-skill` 명령으로 스크립트를 직접 실행하는 Skill을 만드는 흐름을 연습합니다.

이번 실습의 핵심은 딱 하나입니다.

```text
Skill 안의 scripts/count_python_files.py를 실행한다.
```

핵심 학습 포인트:
- `/create-skill`로 Workspace Skill 생성
- Skill 폴더 안에 `scripts/`를 두고 실행 파일 추가
- `SKILL.md`에서 어떤 요청에 어떤 스크립트를 실행할지 명시
- 스크립트 실행 결과를 바탕으로 최종 답변 정리

---

## 실습 폴더

아래 Start 폴더를 VS Code에서 열고 진행합니다.

- `Day2/Practice1-4/Start/python-skill-demo`

초기 파일 구조:

```text
python-skill-demo/
└─ src/
   ├─ calculator.py
   └─ formatter.py
```

---

## Step 1. /create-skill 실행

VS Code Copilot Chat에서 아래처럼 입력합니다.

```text
/create-skill
```

Skill 설명은 아래 예시를 사용합니다.

```text
Python 프로젝트의 파일 통계를 내는 Skill을 만들고 싶어.

이 Skill은 scripts/count_python_files.py를 실행해서
프로젝트 안의 Python 파일 개수, 전체 라인 수, 빈 줄 수, 주석 줄 수를 계산해줘.

Skill 이름은 python-file-counter로 해줘.
핵심은 설명이 아니라 스크립트를 실행하는 거야.
```

위치 선택 질문이 나오면 실습에서는 **Workspace Skill**을 선택합니다.

---

## Step 2. 생성된 Skill 구조 확인

생성 후 파일 구조가 아래와 유사한지 확인합니다.

```text
.github/
└─ skills/
   └─ python-file-counter/
      └─ SKILL.md
```

이 실습에서는 필요한 파일을 일일이 수동으로 만들지 않아도 됩니다.
Copilot에게 필요한 스크립트 파일을 만들어 달라고 요청하면 됩니다.

최종적으로는 아래 구조가 되면 됩니다.

```text
.github/
└─ skills/
   └─ python-file-counter/
      ├─ SKILL.md
      └─ scripts/
         └─ count_python_files.py
```

---

## Step 3. 스크립트 만들기

Copilot Chat에 아래처럼 요청합니다.

```text
.github/skills/python-file-counter/scripts/count_python_files.py 파일을 만들어줘.
프로젝트 안의 Python 파일 개수, 전체 라인 수, 빈 줄 수, 주석 줄 수를 JSON으로 출력하는 스크립트로 작성해줘.
```

만들어질 파일은 아래 경로입니다.

```text
.github/skills/python-file-counter/scripts/count_python_files.py
```

내용:

```python
#!/usr/bin/env python3

from pathlib import Path
import json
import sys


def count_file(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()

    total = len(lines)
    blank = sum(1 for line in lines if not line.strip())
    comments = sum(1 for line in lines if line.strip().startswith("#"))
    code = total - blank - comments

    return {
        "file": str(path),
        "total_lines": total,
        "code_lines": code,
        "blank_lines": blank,
        "comment_lines": comments,
    }


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    files = [
        path
        for path in root.rglob("*.py")
        if ".venv" not in path.parts
        and "__pycache__" not in path.parts
        and ".git" not in path.parts
    ]

    file_results = [count_file(path) for path in files]

    summary = {
        "python_file_count": len(file_results),
        "total_lines": sum(item["total_lines"] for item in file_results),
        "code_lines": sum(item["code_lines"] for item in file_results),
        "blank_lines": sum(item["blank_lines"] for item in file_results),
        "comment_lines": sum(item["comment_lines"] for item in file_results),
        "files": file_results,
    }

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

---

## Step 4. 테스트용 Python 파일 확인

Start 폴더에는 통계를 낼 대상 파일이 두 개 들어 있습니다.
실습용 파일은 이미 준비되어 있으므로 따로 추가할 필요가 없습니다.

```text
src/
├─ calculator.py
└─ formatter.py
```

`src/calculator.py`

```python
# calculator utilities

def add(a, b):
    return a + b


def divide(a, b):
    return a / b
```

`src/formatter.py`

```python
def normalize_name(name):
    return name.strip().title()
```

---

## Step 5. SKILL.md 정리

생성된 `SKILL.md`가 아래 방향이 되도록 Copilot에게 정리해 달라고 요청합니다.

````markdown
---
name: python-file-counter
description: use when the user asks to count Python files, summarize Python file statistics, inspect project size, or calculate total lines of Python code in a project.
---

# Python File Counter Skill

## 목표

Python 프로젝트의 파일 통계를 계산한다.

이 Skill의 핵심은 설명이 아니라 `scripts/count_python_files.py`를 실행하는 것이다.

## 실행 규칙

사용자가 Python 파일 통계, 라인 수, 코드 줄 수, 파일 개수를 요청하면 반드시 아래 스크립트를 실행한다.

```bash
python .github/skills/python-file-counter/scripts/count_python_files.py .
```

## 출력 규칙

스크립트가 출력한 JSON을 바탕으로 한국어로 짧게 요약한다.

반드시 포함할 항목:

- Python 파일 개수
- 전체 라인 수
- 코드 라인 수
- 빈 줄 수
- 주석 줄 수
- 라인 수가 가장 많은 파일 3개

## 주의사항

- 스크립트를 실행하지 않고 추측해서 답하지 않는다.
- `.venv`, `.git`, `__pycache__`는 제외한다.
- 결과는 간단한 표로 정리한다.
````

---

## Step 6. Skill 실행해보기

Copilot Chat에서 요청합니다.

```text
지금 프로젝트의 파일 개수를 구해줘.
```

좀 더 명확하게 말하고 싶다면 아래처럼 요청해도 됩니다.

```text
python-file-counter Skill을 사용해서 지금 프로젝트의 Python 파일 개수와 라인 통계를 구해줘.
반드시 scripts/count_python_files.py를 실행해줘.
```

핵심은 사용자가 복잡한 명령을 외우는 것이 아니라,
자연어로 "지금 프로젝트의 파일 개수를 구해줘."라고 요청해도 Skill이 스크립트를 실행하는 경험을 하는 것입니다.

---

## 기대 결과

Copilot이 스크립트를 실행하고, 이런 식으로 요약하면 성공입니다.

```text
Python 파일 통계

| 항목 | 값 |
|---|---:|
| Python 파일 개수 | 2 |
| 전체 라인 수 | 9 |
| 코드 라인 수 | 5 |
| 빈 줄 수 | 3 |
| 주석 줄 수 | 1 |

라인 수가 많은 파일

| 파일 | 전체 라인 수 |
|---|---:|
| src/calculator.py | 7 |
| src/formatter.py | 2 |
```