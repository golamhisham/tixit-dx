from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from datetime import datetime, timezone
from app.database import Base
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    member = "member"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(Role), default=Role.member)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))