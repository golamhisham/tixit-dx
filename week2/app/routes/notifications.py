from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.database import get_db
from app.routes.auth import get_current_user
from typing import Optional

router = APIRouter()

@router.get("/notifications")
def get_notifications(
    read: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    if read is not None:
        query = query.filter(Notification.read == read)
    notifications = query.order_by(Notification.timestamp.desc()).all()
    return [
        {
            "id": n.id,
            "message": n.message,
            "timestamp": n.timestamp.isoformat(),
            "read": n.read
        } for n in notifications
    ] 