import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import storage


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_storage():
	"""각 테스트마다 storage를 초기화합니다."""
	storage._users.clear()
	storage._next_id = 1
	yield


def test_hello_world():
	assert 1 + 1 == 2


class TestRegister:
	"""POST /auth/register 엔드포인트 테스트"""
	
	def test_register_success(self):
		"""성공: 유효한 email과 password로 201 응답"""
		payload = {
			"email": "user@example.com",
			"password": "SecurePass123!"
		}
		response = client.post("/auth/register", json=payload)
		
		assert response.status_code == 201
		data = response.json()
		assert data["ok"] is True
		assert data["user"]["email"] == "user@example.com"
		assert "id" in data["user"]
	
	def test_register_invalid_email(self):
		"""실패: 이메일 형식 오류 -> 400 INVALID_EMAIL"""
		payload = {
			"email": "invalid-email",
			"password": "SecurePass123!"
		}
		response = client.post("/auth/register", json=payload)
		
		assert response.status_code == 400
		data = response.json()
		assert data["ok"] is False
		assert data["error"]["code"] == "INVALID_EMAIL"

	def test_register_invalid_email_too_long(self):
		"""실패: 매우 긴 이메일(200자) -> 400 INVALID_EMAIL"""
		local = "a" * 188
		payload = {
			"email": f"{local}@t.com",
			"password": "SecurePass123!"
		}
		response = client.post("/auth/register", json=payload)

		assert response.status_code == 400
		data = response.json()
		assert data["ok"] is False
		assert data["error"]["code"] == "INVALID_EMAIL"
	
	def test_register_weak_password(self):
		"""실패: 비밀번호 약함 -> 400 WEAK_PASSWORD"""
		payload = {
			"email": "user@example.com",
			"password": "weak"  # 너무 짧고 규칙 미충족
		}
		response = client.post("/auth/register", json=payload)
		
		assert response.status_code == 400
		data = response.json()
		assert data["ok"] is False
		assert data["error"]["code"] == "WEAK_PASSWORD"

	def test_register_password_only_spaces(self):
		"""실패: 공백만 있는 비밀번호 -> 400 WEAK_PASSWORD"""
		payload = {
			"email": "space@example.com",
			"password": "        "
		}
		response = client.post("/auth/register", json=payload)

		assert response.status_code == 400
		data = response.json()
		assert data["ok"] is False
		assert data["error"]["code"] == "WEAK_PASSWORD"

	def test_register_password_without_special_char(self):
		"""실패: 특수문자 없는 비밀번호 -> 400 WEAK_PASSWORD"""
		payload = {
			"email": "nospecial@example.com",
			"password": "Password123"
		}
		response = client.post("/auth/register", json=payload)

		assert response.status_code == 400
		data = response.json()
		assert data["ok"] is False
		assert data["error"]["code"] == "WEAK_PASSWORD"

	def test_register_success_min_length_password(self):
		"""성공: 정확히 8자 유효 비밀번호 -> 201"""
		payload = {
			"email": "minlen@example.com",
			"password": "Ab1!defg"
		}
		response = client.post("/auth/register", json=payload)

		assert response.status_code == 201
		data = response.json()
		assert data["ok"] is True
		assert data["user"]["email"] == "minlen@example.com"
		assert "id" in data["user"]
	
	def test_register_duplicate_email(self):
		"""실패: 중복 이메일 -> 409 DUPLICATE_EMAIL"""
		payload = {
			"email": "user@example.com",
			"password": "SecurePass123!"
		}
		# 첫 번째 등록
		response1 = client.post("/auth/register", json=payload)
		assert response1.status_code == 201
		
		# 두 번째 등록 (같은 이메일)
		response2 = client.post("/auth/register", json=payload)
		assert response2.status_code == 409
		data = response2.json()
		assert data["ok"] is False
		assert data["error"]["code"] == "DUPLICATE_EMAIL"