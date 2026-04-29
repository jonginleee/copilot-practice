---
name: python-file-counter
description: 'Count Python files and source statistics for a Python project. Use when you need the number of Python files, total lines, blank lines, or comment lines by running .github/skills/python-file-counter/scripts/count_python_files.py.'
---

# Python File Counter

이 Skill은 프로젝트 안의 Python 파일 통계를 계산할 때 사용합니다.

핵심 동작은 설명이 아니라 [count script](./scripts/count_python_files.py)를 실행하는 것입니다.

## When to Use

- Python 파일 개수를 빠르게 확인해야 할 때
- 전체 라인 수, 빈 줄 수, 주석 줄 수를 계산해야 할 때
- 프로젝트 규모를 간단히 파악해야 할 때

## Procedure

1. 현재 작업 디렉터리를 프로젝트 루트로 둡니다.
2. 다음 명령으로 스크립트를 실행합니다.

```powershell
python .github/skills/python-file-counter/scripts/count_python_files.py
```

3. 스크립트 출력에서 다음 네 값을 그대로 보고합니다.
   - Python files
   - Total lines
   - Blank lines
   - Comment lines
4. 사용자가 원하면 결과를 간단히 해석하되, 먼저 숫자를 정확히 전달합니다.

## Completion Check

- .github/skills/python-file-counter/scripts/count_python_files.py가 실제로 실행되었다.
- Python 파일 개수, 전체 라인 수, 빈 줄 수, 주석 줄 수가 모두 출력되었다.
- 결과 보고 시 추정값 대신 스크립트 출력값을 사용했다.