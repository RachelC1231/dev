from pydantic import BaseModel, EmailStr

class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str

class CreateUserResponse(BaseModel):
    user_id: str
    
class GetUserRequest(BaseModel):
    email: EmailStr

class GetUserResponse(BaseModel):
    user_id: str
    email: EmailStr
    username: str
    external_uid: int
    jwt_token_key: str
    country_code: str
    user_role: str
