from passlib.context import CryptContext


_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_password(password: str) -> None:
	errors: list[str] = []

	if len(password) < 8:
		errors.append("길이는 최소 8자 이상이어야 합니다")

	if not any(ch.isdigit() for ch in password):
		errors.append("숫자를 최소 1개 이상 포함해야 합니다")

	if not any(not ch.isalnum() for ch in password):
		errors.append("특수문자를 최소 1개 이상 포함해야 합니다")

	if errors:
		raise ValueError("비밀번호 규칙 위반: " + ", ".join(errors))


def hash_password(password: str) -> str:
	return _pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
	return _pwd_context.verify(plain, hashed)
