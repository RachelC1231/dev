# 数据库操作层
# “怎么查 / 怎么存”数据库， 只关心：怎么用 ORM 和数据库打交道
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.user import User

# 储存对数据库user表的一些操作functions
class UserRepository:

    def get_by_id(self, db: Session, user_id):
        return db.get(User, user_id)

    def get_by_email(self, db: Session, email: str):
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalar_one_or_none()

    def create(self, db: Session, user: User):
        db.add(user)
        db.flush()   # 拿到 user_id
        return user

    def update_last_login(self, db: Session, user: User):
        user.last_login = func.now()

