"""사용자 관리 모듈 (불완전 구현)"""

import logging
import re
from typing import Optional


logger = logging.getLogger(__name__)


class ValidationError(Exception):
    pass


class DuplicateUserError(Exception):
    pass


class User:
    def __init__(self, username: str, email: str, age: int):
        self.username = username
        self.email = email
        self.age = age
    
    def validate(self) -> bool:
        if not re.fullmatch(r"[A-Za-z0-9]{3,20}", self.username):
            raise ValidationError("username은 3-20자의 영문자와 숫자만 허용됩니다.")

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", self.email):
            raise ValidationError("email 형식이 올바르지 않습니다.")

        if not 18 <= self.age <= 120:
            raise ValidationError("age는 18 이상 120 이하여야 합니다.")

        return True
    
    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "age": self.age
        }


class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self, user: User) -> bool:
        user.validate()

        if user.username in self.users:
            logger.warning("add_user failed: duplicate username=%s", user.username)
            raise DuplicateUserError(f"이미 존재하는 username입니다: {user.username}")

        self.users[user.username] = user
        logger.info("add_user succeeded: username=%s", user.username)
        return True
    
    def find_user(self, username: str) -> Optional[User]:
        return self.users.get(username)
    
    def get_all_users(self) -> list:
        return list(self.users.values())
    
    def remove_user(self, username: str) -> bool:
        if username not in self.users:
            logger.warning("remove_user failed: username=%s", username)
            return False

        del self.users[username]
        logger.info("remove_user succeeded: username=%s", username)
        return True
