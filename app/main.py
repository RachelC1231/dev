from fastapi import FastAPI
from app.api.routes_users import router as users_router
from app.core.config import settings

print("🔥 API 正在连接数据库:", settings.DATABASE_URL)

app = FastAPI(title="Collect API")
app.include_router(users_router)

@app.get("/health")
def health():
    return {"ok": True}
