import pytest

from app.security import hash_password, validate_password, verify_password


def test_validate_password_accepts_valid_password():
	valid_passwords = [
		"SecurePass123!",
		"Abcdefg1@",
		"MyPassword9#",
	]

	for password in valid_passwords:
		validate_password(password)


@pytest.mark.parametrize(
	"password, expected_fragments",
	[
		(
			"short!",
			[
				"길이는 최소 8자 이상이어야 합니다",
				"숫자를 최소 1개 이상 포함해야 합니다",
			],
		),
		("LongPassword!", ["숫자를 최소 1개 이상 포함해야 합니다"]),
		("Password123", ["특수문자를 최소 1개 이상 포함해야 합니다"]),
		(
			"weak",
			[
				"길이는 최소 8자 이상이어야 합니다",
				"숫자를 최소 1개 이상 포함해야 합니다",
				"특수문자를 최소 1개 이상 포함해야 합니다",
			],
		),
	],
)
def test_validate_password_rejects_invalid_passwords(password, expected_fragments):
	with pytest.raises(ValueError) as exc_info:
		validate_password(password)

	message = str(exc_info.value)
	assert message.startswith("비밀번호 규칙 위반:")
	for fragment in expected_fragments:
		assert fragment in message


def test_hash_password_returns_non_plain_string():
	plain = "SecurePass123!"
	hashed = hash_password(plain)

	assert isinstance(hashed, str)
	assert hashed
	assert hashed != plain
	assert "pbkdf2-sha256" in hashed


def test_verify_password_returns_true_for_correct_password():
	plain = "SecurePass123!"
	hashed = hash_password(plain)

	assert verify_password(plain, hashed) is True


def test_verify_password_returns_false_for_wrong_password():
	plain = "SecurePass123!"
	hashed = hash_password(plain)

	assert verify_password("WrongPass999!", hashed) is False


def test_hash_password_uses_salt_hashes_are_different_for_same_input():
	plain = "SecurePass123!"
	hashed1 = hash_password(plain)
	hashed2 = hash_password(plain)

	assert hashed1 != hashed2
	assert verify_password(plain, hashed1) is True
	assert verify_password(plain, hashed2) is True