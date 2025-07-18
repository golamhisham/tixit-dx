from fastapi import Depends, HTTPException, status
from app.models.user import User, Role
from app.routes.auth import get_current_user

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user 