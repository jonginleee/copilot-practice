"""
[Context for Copilot]
- DB 없이 dict 기반 저장소
- create_user(email, password_hash) -> dict{id, email, password_hash}
- get_user_by_email(email) -> dict | None
- 중복 email이면 예외(또는 False)로 처리할 수 있게 설계
"""
# TODO: Copilot로 구현
