from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.example", extra="ignore")

    ENV: str = "dev"

    # Postgres 连接串（同步: postgresql+psycopg2://  异步: postgresql+asyncpg://）
    DATABASE_URL: str

    # 连接池参数（给生产用）
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_RECYCLE: int = 1800   # 秒：避免云上 idle 断链
    DB_POOL_PRE_PING: bool = True # 断链自动探测

    DB_ECHO: bool = False         # SQL 打印（开发可 True）
    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

settings = Settings()

