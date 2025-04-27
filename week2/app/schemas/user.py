from pydantic import BaseModel

class UserCreate(BaseModel):
    usernmae : str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str
    
class UserOut(BaseModel):
    # fields for showing user info safely
    username: str
    email: str
    role: str
    created_at: str
    class Config:
        orm_mode = True
