from pydantic import BaseModel, field_validator
from typing import Optional, Union
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Team Tracker",
                "description": "Manage tasks and issues for our CS project"
            }
        }

class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_by: int
    created_at: Union[str, datetime]

    @field_validator("created_at", mode="before")
    def serialize_created_at(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

    class Config:
        from_attributes = True 