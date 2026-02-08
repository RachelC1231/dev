# 业务逻辑核心
# 你只能在这里做：
# 1. 注册 / 登录 / 禁用用户
# 2. 多表操作
# 3. commit（这次操作我确认要了）/ rollback（刚才那一串操作全部作废）
# 4. 业务判断（if / else）
import secrets
from datetime import datetime

from app.models.user import User
from app.repositories.user_repo import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def register(self, db, email: str, username: str) -> User:
        # 1) 防重复（可选）
        existing = self.repo.get_by_email(db, email)
        if existing:
            raise ValueError("email already exists")

        # 2) 生成 jwt_token_key（开发占位）
        token_key = secrets.token_urlsafe(32)  # 随机字符串

        user = User(
            email=email,
            username=username,
            jwt_token_key=token_key,
            # data_consent/account_status/user_role/country_code 等都让数据库默认值处理
        )

        self.repo.create(db, user)

        # 3) 提交事务（关键）
        db.commit()
        db.refresh(user)
        return user
