# user表结构镜像, 数据结构说明书（表长什么样）
# ORM 帮你做了三件事：把 表 ↔ 类， 把 行 ↔ 对象， 把 SQL ↔ Python API
# Model 是“表结构层”
# dev/app/models/user.py
# users 表 ORM 映射（Python 3.9 兼容版）

import uuid
from datetime import datetime, date
from typing import Optional, Dict, Any

from sqlalchemy import (
    String,
    Boolean,
    TIMESTAMP,
    Date,
    Integer,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.Base import Base  # 你的 Base

class User(Base):
    __tablename__ = "users"

    # =======================
    # 主键 & 唯一标识
    # =======================
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        # 你 DB 里 default 是 gen_random_uuid()，用 server_default 更贴近数据库
        server_default=text("gen_random_uuid()"),
    )

    external_uid: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        # DBeaver 里显示 nextval('users_external_uid_seq'::regclass)
        server_default=text("nextval('users_external_uid_seq'::regclass)"),
    )

    # =======================
    # 登录 / 账号信息
    # =======================
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)

    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    password_salt: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    password_reset_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    password_reset_expiry: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )

    # =======================
    # JWT
    # =======================
    jwt_token_key: Mapped[str] = mapped_column(Text, nullable=False)

    # 你表里叫 jwt_token_key_created_a（看你截图的列名）
    jwt_token_key_created_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=True),
    nullable=False,
    server_default=text("CURRENT_TIMESTAMP"),
    )


    jwt_token_key_expiry: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )

    # =======================
    # 基本信息
    # =======================
    first_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # DB 是 date
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # DB 是 bool default false
    phone_verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )

    # =======================
    # 地址
    # =======================
    street_address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    province: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postcode: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # DB default 'CA'::bpchar（你截图里是 bpchar(2)）
    country_code: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
        server_default=text("'CA'::bpchar"),
    )

    # =======================
    # 其他用户信息
    # =======================
    emergency_contact: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    medical_conditions: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    data_consent: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )

    consent_timestamp: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )

    encrypted_health_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # DB default 'active'::character varying
    account_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'active'::character varying"),
    )

    avatar_path: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    referrer_username: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # DB default 'n'::character varying（你截图里 user_role default 是 'n'）
    user_role: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
        server_default=text("'n'::character varying"),
    )

    # DB default 0
    scores_balance: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("0"),
    )

    agent_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # =======================
    # 审计字段
    # =======================
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    last_login: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )
