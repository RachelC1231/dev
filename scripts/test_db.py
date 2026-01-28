from sqlalchemy import text
from app.db.session import engine

# 测试文件
def main():
    print("Connecting to database...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("DB result:", result.scalar())

if __name__ == "__main__":
    main()