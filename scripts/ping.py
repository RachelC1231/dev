from sqlalchemy import create_engine, text
from app.core.config import settings

def main():
    print("USING URL:", settings.DATABASE_URL)

    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    with engine.connect() as conn:
        print(conn.execute(text("select 1")).scalar())

if __name__ == "__main__":
    main()



