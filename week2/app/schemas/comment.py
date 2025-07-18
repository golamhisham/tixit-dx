from pydantic import BaseModel
from typing import Optional

class CommentCreate(BaseModel):
    content: str

    class Config:
        schema_extra = {
            "example": {
                "content": "I am also experiencing this issue on version 1.2.3."
            }
        }

class CommentOut(BaseModel):
    id: int
    content: str
    issue_id: int
    user_id: int
    timestamp: str

    class Config:
        orm_mode = True 