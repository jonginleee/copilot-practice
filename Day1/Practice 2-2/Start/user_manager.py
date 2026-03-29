"""사용자 관리 모듈 (불완전 구현)"""

class User:
    def __init__(self, username: str, email: str, age: int):
        self.username = username
        self.email = email
        self.age = age
    
    def validate(self) -> bool:
        # 불완전한 검증 로직
        if len(self.username) < 1:
            return False
        return True
    
    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "age": self.age
        }


class UserManager:
    def __init__(self):
        self.users = []
    
    def add_user(self, user: User) -> bool:
        # 검증 없이 추가
        self.users.append(user)
        return True
    
    def find_user(self, username: str) -> User:
        # 선형 탐색만 사용
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def get_all_users(self) -> list:
        return self.users
    
    def remove_user(self, username: str) -> bool:
        # 구현 누락
        pass
