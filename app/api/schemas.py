from pydantic import BaseModel, EmailStr

class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str

class CreateUserResponse(BaseModel):
    user_id: str
