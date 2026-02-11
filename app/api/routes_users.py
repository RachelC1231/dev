from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.user_service import UserService
from app.api.schemas import CreateUserRequest, CreateUserResponse, GetUserRequest, GetUserResponse

router = APIRouter(prefix="/users", tags=["users"])
service = UserService()

@router.post("", response_model=CreateUserResponse)
def create_user(payload: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        user_dict = service.register(db, email=payload.email, username=payload.username)
        return {"user_id": str(user_dict["user"].user_id)}
    except ValueError as e:
        print(e)
        # 比如 email 已存在
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/get_user", response_model=GetUserResponse)
def get_user(payload: GetUserRequest, db: Session = Depends(get_db)):
    try:
        user_dict = service.get_user(db, email=payload.email)
        return user_dict
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=CreateUserResponse)
def user_login(payload: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        user = service.register(db, email=payload.email, username=payload.username)
        return {"user_id": str(user.user_id)}
    except ValueError as e:
        # 比如 email 已存在
        raise HTTPException(status_code=400, detail=str(e))
    
    
    