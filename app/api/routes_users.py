from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.user_service import UserService
from app.api.schemas import CreateUserRequest, CreateUserResponse

router = APIRouter(prefix="/users", tags=["users"])
service = UserService()

@router.post("", response_model=CreateUserResponse)
def create_user(payload: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        user = service.register(db, email=payload.email, username=payload.username)
        return {"user_id": str(user.user_id)}
    except ValueError as e:
        # 比如 email 已存在
        raise HTTPException(status_code=400, detail=str(e))
