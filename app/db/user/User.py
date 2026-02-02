# app/models/user.py
from sqlalchemy import String, Boolean, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from dev.app.core import Base   # 定义的Base类

class User(Base):  # 这个 Python 类 = 数据库里的 users 表
    __tablename__ = "users"   # ← 数据库里的表名
    
    # 类型标注（type hint）
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True) # set user_id as primary key
    username: Mapped[str] = mapped_column(String(50), nullable=False) # default nullable=False
    email: Mapped[str] = mapped_column(String(255), nullable=True) # 这个Python属性对应数据库中的一列 （users.email 这一列）
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_verified: Mapped[bool] = mapped_column(String(355), nullable=False)
    account_status: Mapped[str] = mapped_column(String(20))
    
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("now()")
    )
    
# ORM 映射（Mapping to existing table）