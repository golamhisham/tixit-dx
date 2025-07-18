from pydantic import BaseModel, field_validator
from typing import Optional, Union
from datetime import datetime

class IssueCreate(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    assigned_to: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Fix login bug",
                "description": "Users cannot log in with Google OAuth.",
                "status": "open",
                "priority": "high",
                "assigned_to": 2
            }
        }

class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[int] = None

class IssueOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    assigned_to: Optional[int]
    created_by: int
    created_at: Union[str, datetime]
    updated_at: Optional[Union[str, datetime]] = None
    project_id: int

    @field_validator("created_at", mode="before")
    def serialize_created_at(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

    @field_validator("updated_at", mode="before")
    def serialize_updated_at(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

    class Config:
        from_attributes = True 