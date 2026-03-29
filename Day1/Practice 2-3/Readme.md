# GitHub Copilot /plan 기능 - 실습

## 목차
1. [사전 준비](#사전-준비)
2. [실습 환경 설정](#실습-환경-설정)
3. [기능별 실습](#기능별-실습)
   - [실습 1: requirements.md를 바탕으로 /plan 실행](#실습-1-requirementsmd를-바탕으로-plan-실행)

---

## 사전 준비

### 준비물
- VS Code 최신 버전
- GitHub Copilot + Copilot Chat 확장 설치
- GitHub 로그인 완료
- Chat view 단축키 확인: `Ctrl+Alt+I`
- Chat 모드를 **Agent**로 설정

### 이번 실습에서 집중할 기능
- `requirements.md`를 컨텍스트로 제공하여 Copilot이 요구사항을 이해하게 하기
- `/plan`으로 구현 계획을 먼저 생성하고 검토하기
- 계획을 확인한 뒤 수정을 요청하거나 그대로 실행하기

---

## 실습 환경 설정

### 사용할 파일

실습에는 `Day1\Practice 2-3\Start\` 폴더의 다음 파일을 사용합니다.

- `user_manager.py`: 불완전한 사용자 관리 클래스
- `data_handler.py`: 데이터 처리 함수 모음
- `REQUIREMENTS.md`: 실습 중 직접 만들어 첨부할 요구사항 문서

### 준비 작업
1. `user_manager.py`와 `data_handler.py`를 미리 열어 둡니다.
2. Chat view를 열고 모드를 **Agent**로 설정합니다.
3. `/plan` 명령어를 입력창에 입력했을 때 자동 완성이 뜨는지 확인합니다.

---

## 기능별 실습

## 실습 1: requirements.md를 바탕으로 /plan 실행

### 학습 목표
- 요구사항 문서를 컨텍스트로 제공하는 방법 익히기
- `/plan`으로 구현 계획 생성하기
- 계획을 검토하고 수정 요청하거나 그대로 실행하기

### 실습 단계

#### 1단계: /plan 실행
1. `Ctrl+Alt+I`로 Chat view를 엽니다.
2. 모드를 **Agent**로 설정합니다.
3. 입력창에서 `REQUIREMENTS.md`와 `user_manager.py`를 컨텍스트에 추가합니다.
4. 아래 프롬프트를 입력합니다.

```text
/plan #REQUIREMENTS.md의 요구사항을 바탕으로 user_manager.py를 개선하려고 해. 어떤 순서로 작업할지 계획을 세워줘.
```

#### 2단계: 계획 검토
계획이 출력되면 아래 항목을 확인합니다.
1. 요구사항의 4가지 항목(검증 강화, `remove_user`, 예외 처리, 성능 개선)이 모두 포함되어 있는지 확인합니다.
2. 구현 순서가 자연스러운지 확인합니다.
3. 누락되거나 순서가 어색한 부분이 있으면 후속 요청으로 보완합니다.

```text
예외 처리를 어느 단계에서 구현할지 명시해줘.
```

#### 3단계: 계획 실행
계획이 만족스러우면 `Start implementation` 버튼을 눌러 실행을 요청합니다.

생성된 코드가 요구사항 항목을 충족하는지 확인합니다.