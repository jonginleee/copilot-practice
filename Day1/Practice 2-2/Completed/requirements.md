# UserManager 개선 요구사항

## 배경
기존 UserManager 클래스를 보안, 성능, 기능 측면에서 개선해야 함

## 요구사항

### 1. 검증 강화
- username: 3-20자, 알파벳과 숫자만 허용
- email: 유효한 이메일 형식 검증
- age: 18-120 범위 검증

### 2. remove_user 메서드 구현
- username으로 사용자 찾기
- 사용자 없으면 False 반환
- 사용자 있으면 제거 후 True 반환

### 3. 예외 처리 추가
- username이 이미 존재하면 DuplicateUserError
- 검증 실패하면 ValidationError

### 4. 성능 개선
- username으로 빠른 조회 가능하도록 dict 사용

### 5. 로깅 추가
- add_user 호출 시 로그 기록 (성공/실패 여부 포함)
- remove_user 호출 시 로그 기록 (성공/실패 여부 포함)