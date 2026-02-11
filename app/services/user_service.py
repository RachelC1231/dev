# 业务逻辑核心
# 你只能在这里做：
# 1. 注册 / 登录 / 禁用用户
# 2. 多表操作
# 3. commit（这次操作我确认要了）/ rollback（刚才那一串操作全部作废）
# 4. 业务判断（if / else）
import secrets
from datetime import datetime
from pydantic import EmailStr
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.core import jwt
from app.core.config import settings
from app.api.schemas import GetUserResponse

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def register(self, db, email: str, username: str) -> dict:
        # 1) 防重复（可选）
        existing = self.repo.get_by_email(db, email)
        if existing:
            raise ValueError("email already exists")

        # 2) 生成 jwt_token_key（开发占位）
        # token_key = secrets.token_urlsafe(32)  # 随机字符串

        # user = User(
        #     email=email,
        #     username=username,
        #     jwt_token_key=token_key,
        #     # data_consent/account_status/user_role/country_code 等都让数据库默认值处理
        # )

        token_key = secrets.token_urlsafe(32)
        
        user = User(
            email=email,
            username=username,
            jwt_token_key=token_key,
        )
        
        self.repo.create(db, user)

        # 2) 提交事务（关键）
        db.commit()
        db.refresh(user)
    
        secret_key = settings.AUTH_SECRETE_KEY
        duration = 3600
        
        # 3) 再生成 token（用已落库的 user 字段 和 随机生成的 jwt_token_key）
        token_key = jwt.generate_jwt_token(user.user_id, 
        user.external_uid, 
        user.user_role, 
        user.username, 
        user.email, 
        secret_key, 
        duration)
        
        # 4) 返回给前端
        return {
            "user": user,
            "access_token": token_key,
            "token_type": "bearer",
        }
    # def login(self, db, email: str, username: str) -> dict:
    #     db.
    
    def get_user(self, db, email: EmailStr) -> GetUserResponse:
        user = self.repo.get_by_email(db, email)
        return GetUserResponse(
        user_id=user.user_id,
        email=user.email,
        username=user.username,
        external_uid=user.external_uid,
        jwt_token_key=user.jwt_token_key,
        country_code=user.country_code,
        user_role=user.user_role,
    )

