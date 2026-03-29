"""사용자 관리 모듈."""

import logging
import re
from typing import Optional


logger = logging.getLogger(__name__)


class ValidationError(ValueError):
    """사용자 데이터 검증 실패 시 발생하는 예외."""


class DuplicateUserError(ValueError):
    """이미 존재하는 사용자명을 추가하려고 할 때 발생하는 예외."""


class User:
    def __init__(self, username: str, email: str, age: int):
        self.username = username
        self.email = email
        self.age = age

    def validate(self) -> bool:
        if not re.fullmatch(r"[A-Za-z0-9]{3,20}", self.username):
            raise ValidationError("username must be 3-20 alphanumeric characters")

        if not re.fullmatch(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", self.email):
            raise ValidationError("email must be a valid email address")

        if not isinstance(self.age, int) or not 18 <= self.age <= 120:
            raise ValidationError("age must be between 18 and 120")

        return True

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "age": self.age,
        }


class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user: User) -> bool:
        try:
            user.validate()

            if user.username in self.users:
                raise DuplicateUserError(f"username '{user.username}' already exists")

            self.users[user.username] = user
            logger.info("add_user succeeded for username=%s", user.username)
            return True
        except (ValidationError, DuplicateUserError):
            logger.warning("add_user failed for username=%s", user.username)
            raise

    def find_user(self, username: str) -> Optional[User]:
        return self.users.get(username)

    def get_all_users(self) -> list:
        return list(self.users.values())

    def remove_user(self, username: str) -> bool:
        if username not in self.users:
            logger.info("remove_user failed for username=%s", username)
            return False

        del self.users[username]
        logger.info("remove_user succeeded for username=%s", username)
        return True
