# 数据库连接分发器, 统一创建 / 关闭数据库 Session
# 负责：创建数据库连接 → 给你用 → 用完一定关掉
from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
