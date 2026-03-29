"""
[Context for Copilot]
- DB 없이 dict 기반 저장소
- create_user(email, password_hash) -> dict{id, email, password_hash}
- get_user_by_email(email) -> dict | None
- 중복 email이면 예외(또는 False)로 처리할 수 있게 설계
"""

_users: dict[int, dict] = {}
_next_id = 1


def create_user(email: str, password_hash: str) -> dict:
	"""Create a new user or raise ValueError if email already exists."""
	global _next_id
	
	if email in {u["email"] for u in _users.values()}:
		raise ValueError("Email already exists")
	
	user = {"id": _next_id, "email": email, "password_hash": password_hash}
	_users[_next_id] = user
	_next_id += 1
	
	return {"id": user["id"], "email": user["email"]}


def get_user_by_email(email: str) -> dict | None:
	"""Get user by email or return None."""
	for user in _users.values():
		if user["email"] == email:
			return user
	return None
