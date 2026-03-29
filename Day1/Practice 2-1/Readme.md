# GitHub Copilot 여러 기능 알아보기

## 목차
1. [사전 준비](#사전-준비)
2. [실습 환경 설정](#실습-환경-설정)
3. [기능별 실습](#기능별-실습)
   - [실습 1: 인라인 제안](#실습-1-인라인-제안)
   - [실습 2: 명령 팔레트](#실습-2-명령-팔레트)
   - [실습 3: Copilot Chat](#실습-3-copilot-chat)
   - [실습 4: 인라인 채팅](#실습-4-인라인-채팅)
   - [실습 5: 슬래시 명령](#실습-5-슬래시-명령)
   - [실습 6: 여러 제안 비교](#실습-6-여러-제안-비교)
   - [실습 7: 코드 설명](#실습-7-코드-설명)
   - [실습 8: 컨텍스트 초기화](#실습-8-컨텍스트-초기화)

---

## 사전 준비

### 준비물
- VS Code 최신 버전
- GitHub Copilot + Copilot Chat 확장 설치
- GitHub 로그인 완료
- Chat view 단축키 확인: `Ctrl+Alt+I`
- Inline chat 단축키 확인: `Ctrl+I`

### 확인할 슬래시 명령
- `/explain`: 선택한 코드의 동작과 의도를 자연어로 설명
- `/fix`: 선택한 코드의 문제점을 분석하고 수정안 제안
- `/tests`: 현재 실습에서는 사용하지 않음
- `/new`: 새 프로젝트 또는 파일, 기본 구조 생성
- `/clear`: 현재 채팅 컨텍스트 초기화

---

## 실습 환경 설정

### 프로젝트 구조

```
2. GitHub Copilot 여러 기능 알아보기/
├── src/
    ├── bank_account.py    # 은행 계좌 관리 실습용
    └── invoice.py         # 송장 계산 실습용
```

### 가상환경 설정

CMD에서 다음 명령을 실행하세요:

```cmd
# 프로젝트 폴더로 이동
cd "Day1\2. GitHub Copilot 여러 기능 알아보기"

# 가상환경 생성
python -m venv .venv

# 가상환경 활성화
.venv\Scripts\activate.bat
```
---

## 기능별 실습

## 실습 1: 인라인 제안

### 학습 목표
- 인라인 제안(고스트 텍스트)을 이해하고 활용하기
- Tab, Esc, 부분 수락 단축키 익히기
- TODO 주석을 바탕으로 코드 완성하기

### 실습 단계

#### 1단계: bank_account.py 파일 열기
1. `src/bank_account.py` 파일을 엽니다.
2. 파일 구조를 확인합니다.

#### 2단계: TODO 주석 작성하기
1. `deposit()` 메서드에 다음 TODO 주석을 작성합니다.

   ```python
   def deposit(self, amount: int) -> None:
       # TODO: amount가 0 이하이면 ValueError
       # TODO: balance 증가
       # TODO: ledger에 Transaction(kind="deposit") 기록
       raise NotImplementedError
   ```

2. 주석만으로도 Copilot이 문맥을 파악하는지 확인합니다.

#### 3단계: deposit() 메서드 구현
1. `raise NotImplementedError` 줄을 삭제합니다.
2. TODO 주석 아래에서 구현을 시작합니다.
3. 고스트 텍스트가 나타나면 다음 키를 사용해봅니다.

#### 4단계: withdraw() 메서드 구현
1. `withdraw()` 메서드에 아래 TODO 주석을 작성합니다.

   ```python
   def withdraw(self, amount: int) -> None:
       # TODO: amount가 0 이하이면 ValueError
       # TODO: 잔액 부족이면 InsufficientFunds
       # TODO: balance 감소
       # TODO: ledger에 Transaction(kind="withdraw") 기록
       raise NotImplementedError
   ```

2. 같은 방식으로 구현합니다.
3. 예외 처리까지 포함되는지 확인합니다.

#### 5단계: statement() 메서드 구현
1. `statement()` 메서드에 TODO 주석을 작성합니다.

   ```python
   def statement(self) -> str:
       # TODO: ledger를 줄 단위 문자열로 변환
       raise NotImplementedError
   ```

2. Copilot 제안으로 구현을 완성합니다.

---

## 실습 2: 명령 팔레트

### 학습 목표
- Command Palette에서 Copilot 명령 실행하기
- Copilot 제안 일시 중지/복구하기
- 모델 변경 및 설정 관리하기

### 실습 단계

#### 1단계: Command Palette 열기
1. `F1` 또는 `Ctrl+Shift+P`를 누릅니다.
2. `copilot`을 입력해 사용 가능한 명령을 확인합니다.

#### 2단계: 인라인 제안 일시 중지
1. `Snooze Inline Suggestions`를 실행합니다.
2. 코드 에디터에서 타이핑해 제안이 멈췄는지 확인합니다.

#### 3단계: 인라인 제안 복구
1. `Cancel Snooze Inline Suggestions`를 실행합니다.
2. 제안이 다시 나타나는지 확인합니다.

#### 4단계: 모델 변경
1. `GitHub Copilot: Change Completions Model` 명령을 찾습니다.
2. 사용 가능한 모델 목록을 확인합니다.

#### 5단계: 설정 확인
1. 설정(`Ctrl+,`)을 엽니다.
2. `github.copilot.enable`을 검색합니다.
3. Copilot을 전체 언어에 대해 켜고 끌 수 있는지 확인합니다.
4. Python 같은 특정 언어만 따로 켜고 끌 수 있는 설정 위치도 확인합니다.
5. 즉, "Copilot을 어디서 제어하는지"를 찾는 단계라고 이해하면 됩니다.

---

## 실습 3: Copilot Chat

### 학습 목표
- Chat view를 활용한 코드 이해와 질의응답
- 후속 질문으로 응답 정교화하기
- 현재 지원되는 슬래시 명령 확인하기

### 실습 단계

#### 1단계: Chat view 열기
1. `Ctrl+Alt+I`를 누르거나 활동 표시줄에서 채팅 아이콘을 클릭합니다.
2. Chat view가 열리면 새 대화를 시작합니다.

#### 2단계: 코드 기반 질문
1. `src/bank_account.py` 파일을 엽니다.
2. Chat에 다음 질문을 입력합니다.

```text
BankAccount.deposit/withdraw의 예외 정책이 합리적인지 설명해줘.
```

#### 3단계: 후속 질문
응답을 읽고 다음 질문을 이어서 입력합니다.

```text
초보자가 이해하기 쉽게 핵심 규칙만 3줄로 다시 설명해줘.
```

#### 4단계: 슬래시 명령 목록 확인
1. Chat 입력창에 `/`를 입력합니다.
2. 아래의 명령이 있는 지 확인합니다.

- `/explain`
- `/fix`
- `/tests`
- `/new`
- `/clear`
---

## 실습 4: 인라인 채팅

### 학습 목표
- 인라인 채팅으로 코드 수정 요청하기
- diff 형식 제안을 검토하고 수락/거부하기
- 선택 영역 기반 수정 범위 이해하기

### 실습 단계

#### 1단계: statement() 메서드 선택
1. `src/bank_account.py`에서 `statement()` 메서드 전체를 선택합니다.

#### 2단계: 인라인 채팅 시작
1. `Ctrl+I`를 누릅니다.
2. 편집기 안에 채팅 입력창이 나타나는지 확인합니다.

#### 3단계: 수정 요청
다음처럼 요청합니다.

```text
이 함수가 "deposit +1000 balance=1000" 형식을 유지하도록 구현해줘.
ledger가 비어 있으면 빈 문자열을 반환해줘.
```

#### 4단계: diff 검토
1. 제안된 diff를 읽습니다.
2. `Keep` 또는 `Undo`를 선택합니다.

#### 5단계: 제약을 바꿔 재요청
1. 다시 `Ctrl+I`로 인라인 채팅을 엽니다.
2. 추가 제약을 포함해 재요청합니다.

```text
금액은 항상 +/- 부호를 포함하고, 각 줄의 공백 위치를 일정하게 맞춰줘.
```
---

## 실습 5: 슬래시 명령

### 학습 목표
- 자주 쓰는 작업을 슬래시 명령으로 단축하기
- 현재 지원되는 `/explain`, `/fix`, `/new`, `/clear` 흐름 익히기
- 환경별 명령 목록이 달라질 수 있음을 이해하기

### 실습 단계

#### 1단계: 슬래시 명령 목록 확인
1. Chat view 또는 인라인 채팅을 엽니다.
2. `/`를 입력합니다.
3. 현재 환경에서 보이는 명령 목록을 확인합니다.

#### 2단계: /fix로 버그 수정
1. `src/bank_account.py`의 `withdraw()` 메서드에 의도적으로 버그를 만듭니다.

   ```python
   def withdraw(self, amount: int) -> None:
       self._balance -= amount
       self.ledger.append(Transaction(kind="withdraw", amount=amount, balance_after=self._balance))
   ```

2. 버그가 있는 코드를 선택합니다.
3. `/fix`를 실행합니다.
4. 제안된 수정 사항이 잔액 부족 검사와 금액 검증을 포함하는지 확인합니다.

#### 3단계: /explain으로 현재 코드 설명 확인
1. 같은 코드 블록 또는 수정된 코드를 다시 선택합니다.
2. `/explain`을 실행합니다.
3. 수정된 코드가 현재 어떤 동작을 하는지 자연어 설명을 확인합니다.
4. 필요하면 자유 프롬프트로 `이 수정이 왜 필요한지도 설명해줘`라고 추가 질문합니다.

---

## 실습 6: 여러 제안 비교

### 학습 목표
- 같은 위치에서 여러 제안을 탐색하기
- 서로 다른 구현 스타일을 비교하기

### 실습 단계

#### 1단계: invoice.py 열기
1. `invoice.py`를 엽니다.
2. `calculate_total` 함수 본문 일부를 비웁니다.

#### 2단계: 대안 제안 탐색
1. Copilot 제안이 뜨면 hover를 확인합니다.
2. `Alt+[` 또는 `Alt+]`로 이전/다음 제안을 넘겨봅니다.

#### 3단계: 비교 포인트 정리
다음 관점으로 두 제안을 비교합니다.
- 조건문 구조가 단순한가
- 변수명이 읽기 쉬운가
- 반올림/할인 처리 순서가 명확한가

---

## 실습 7: 코드 설명

### 학습 목표
- `/explain`으로 구현 의도 파악하기
- 경계 조건이나 전제 조건을 후속 질문으로 보강하기
- 설명을 이해용 요약으로 바꾸기

### 실습 단계

#### 1단계: calculate_total 선택
1. `invoice.py`에서 `calculate_total` 함수를 선택합니다.

#### 2단계: /explain 실행
1. 코드를 드래그해서 선택합니다.
2. 마우스 오른쪽을 눌러 나오는 메뉴에서`explain`을 클릭합니다.
3. 설명에서 다음 항목을 확인합니다.

- 입력값의 의미
- 계산 순서
- 예외 또는 경계 조건 언급 여부

#### 3단계: 후속 질문
설명이 부족하면 추가로 질문합니다.

```text
이 함수를 처음 보는 개발자 관점에서, 주의할 경계 조건만 4개로 요약해줘.
```

#### 4단계: docstring 작성
응답을 바탕으로 함수 설명을 한 줄로 정리합니다.

```text
설명을 바탕으로 함수에 docstring을 추가해줘.
```
---

## 실습 8: 컨텍스트 초기화

### 학습 목표
- `/clear`로 대화 맥락을 초기화하기
- 작업 전환 시 컨텍스트 관리 필요성 이해하기

### 실습 단계

1. `/clear`를 실행합니다.
2. 이어서 아래 질문을 입력합니다.

```text
bank_account.py의 핵심 책임만 한 문장으로 설명해줘.
```

3. 이전 할인 정책 문맥이 제거되었는지 확인합니다.