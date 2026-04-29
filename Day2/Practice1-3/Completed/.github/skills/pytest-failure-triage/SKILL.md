---
name: pytest-failure-triage
description: 'Analyze pytest failure logs, Python tracebacks, test failures, assertion errors, fixture errors, import errors, flaky tests, and setup failures. Use when triaging pytest 실패 로그, traceback, 테스트 실패 원인 분류, 재현 방법 정리, 수정 방향 제안이 필요할 때.'
argument-hint: 'pytest 실패 로그나 traceback을 붙여 넣어 주세요.'
---

# Pytest Failure Triage

## What This Skill Produces
- Python 테스트 실패 로그나 traceback을 읽고 실패 원인을 분류합니다.
- 로그 근거를 바탕으로 재현 방법을 정리합니다.
- 최소 수정 방향과 후속 검증 포인트를 한국어로 정리합니다.
- 최종 결과는 [리포트 템플릿](./assets/failure-report-template.md) 형식으로 작성합니다.

## When to Use
- pytest 실행 결과에서 실패 원인을 빨리 분류해야 할 때
- 긴 traceback에서 실제 원인과 파급 증상을 분리해야 할 때
- 실패 재현 명령, 재현 범위, 수정 우선순위를 정리해야 할 때
- 동일한 형식으로 테스트 실패 분석 리포트를 남겨야 할 때

## Inputs To Request
- 실패한 pytest 로그 전체 또는 핵심 traceback
- 가능하면 실패한 테스트 노드 ID 예: tests/test_pricing.py::test_bulk_discount
- 가능하면 실행 명령, Python 버전, 최근 변경 파일
- 관련 코드 일부가 있으면 함께 검토합니다

## Procedure
1. 실패 신호를 먼저 고정합니다.
핵심 예외 타입, 실패한 테스트 이름, 최초 실패 지점, 마지막 assertion 메시지를 추출합니다.

2. 1차 원인과 2차 증상을 분리합니다.
후속 예외가 연쇄적으로 보이면 가장 먼저 실패한 위치를 우선 원인 후보로 삼습니다.

3. 실패 원인을 분류합니다.
[분류 기준](./references/failure-categories.md)을 사용해 하나의 주 원인을 선택하고, 필요하면 보조 분류를 덧붙입니다.

4. 로그 근거를 명시합니다.
원인 분류가 왜 타당한지 traceback의 함수명, assertion 문구, fixture 이름, import 경로 같은 단서를 근거로 설명합니다.

5. 재현 방법을 최소 단위로 제안합니다.
가능하면 실패한 테스트 하나만 다시 실행하는 명령부터 제안하고, 환경 변수나 fixture 조건이 있으면 함께 적습니다.

6. 수정 방향을 루트 원인 기준으로 제안합니다.
테스트만 고칠지, 프로덕션 코드를 고칠지, fixture나 설정을 고칠지 구분합니다. 증상 완화보다 원인 제거를 우선합니다.

7. 검증 항목으로 마무리합니다.
수정 후 다시 돌릴 테스트 범위와 추가로 확인할 회귀 포인트를 적습니다.

## Decision Rules
- `ModuleNotFoundError`, `ImportError`, 환경 변수 누락, 버전 충돌이 먼저 보이면 환경/설정 계열을 우선 검토합니다.
- `fixture` 이름, setup, teardown, monkeypatch, mock 초기화에서 깨지면 테스트 인프라 계열을 우선 검토합니다.
- assertion 값 차이만 보이고 예외가 없다면 비즈니스 로직 또는 테스트 기대값 불일치를 우선 검토합니다.
- 시간, 순서, 랜덤성, 비동기 대기 누락이 섞이면 flaky 또는 상태 누수 가능성을 별도로 표시합니다.
- 외부 서비스, DB, 파일 경로, 네트워크 호출이 포함되면 I/O 의존성과 격리 실패를 함께 점검합니다.

## Output Rules
- 항상 한국어로 작성합니다.
- 추정과 확정은 구분합니다.
- 근거 없는 단정은 피하고, 로그에서 확인된 사실과 추정 사항을 분리합니다.
- 재현 명령은 가능한 한 바로 실행 가능한 형태로 씁니다.
- 출력 형식은 [리포트 템플릿](./assets/failure-report-template.md)을 따릅니다.

## Completion Checks
- 주 원인 분류가 하나 이상 제시되었는가
- 분류 근거가 로그의 구체적 단서와 연결되어 있는가
- 재현 방법이 최소 실행 단위로 정리되었는가
- 수정 방향이 테스트 코드와 제품 코드 중 어디를 다뤄야 하는지 구분하는가
- 수정 후 검증할 테스트 범위가 포함되어 있는가

## 추가 규칙

- 금액 계산과 관련된 실패는 반올림, 부동소수점 오차, 통화 단위 정책을 반드시 확인한다.
- 기대값이 소수점 둘째 자리인데 실제값이 더 긴 소수라면, 반올림 정책이 누락되었을 가능성을 우선 검토한다.
- 수정 방향은 "코드 수정"과 "테스트 기대값 수정"을 나누어 제안한다.

## Resources
- [실패 원인 분류 기준](./references/failure-categories.md)
- [최종 리포트 템플릿](./assets/failure-report-template.md)