---
name: fastapi-developer-guide
description: "FastAPI API 사용 가이드를 작성할 때 사용하는 스킬. 엔드포인트 사용법, 요청/응답 형식, 인증, 검증, curl 예시 중심으로 안내한다. Use when: FastAPI endpoint guide, request response format, API integration guide, validation troubleshooting, 422 error explanation"
---

# FastAPI Developer Guide

이 스킬은 FastAPI API를 다른 개발자에게 설명할 때 사용합니다.
설명은 "무엇을 하는가"보다 "어떻게 호출하는가"에 집중합니다.

## 답변에 꼭 포함할 내용
- 엔드포인트 목적과 사용 시점
- 요청 방법: method, path, header, path/query/body 파라미터
- 응답 형식: 성공 응답 구조와 주요 필드 의미
- 인증/권한 필요 여부
- 자주 나는 에러(특히 422)와 점검 포인트

## 작성 원칙
- 필수값/선택값을 명확히 구분
- 요청/응답 예시는 curl만 제공
- OpenAPI와 코드가 다르면 코드 기준으로 설명
- 연동 개발자가 바로 복붙해 테스트할 수 있게 작성

## 권장 구성
1. 개요
2. 요청 방법
3. 응답 설명
4. curl 예시
5. 주의할 점
6. 에러 및 디버깅

## 공통 오류 가이드
- 422: 필드명 오타, 필수값 누락, 타입 불일치 확인
- 인증 실패: Authorization 헤더, 토큰 형식, 권한 범위 확인
- 응답 불일치: response_model과 실제 반환값 비교
- 의존성 실패: Depends(...) 내부 검증/조회 로직 확인

## 이 저장소 적용 규칙

- API 사용 가이드 문서를 새로 작성하거나 갱신할 때는 반드시 `guide/` 폴더에 저장한다.
- `docs/` 폴더에는 제품/아키텍처/개발 규칙 문서를 유지하고, 실제 연동용 사용 가이드는 `guide/`에서 관리한다.

## API 문서화 체크리스트 (범용)

1. 엔드포인트 목적과 사용 시점 명시
2. 요청 방법(Method/Path/Header/Path/Query/Body) 명시
3. 성공 응답 구조와 주요 필드 의미 설명
4. 인증/권한 필요 여부 명시
5. 복붙 가능한 curl 예시 제공
6. 자주 발생하는 에러(400/401/403/404/405/422 등)와 점검 절차 제공
