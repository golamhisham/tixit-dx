from pydantic import BaseModel
from typing import Optional
from app.models.user import Role

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[Role] = None

class UserLogin(BaseModel):
    email: str
    password: str
    
class UserOut(BaseModel):
    username: str
    email: str
    role: Role
    created_at: str
    class Config:
        orm_mode = True
