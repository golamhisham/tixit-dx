from datetime import datetime
from app.models.notification import Notification

def log_notification(message: str):
    print(f"[NOTIFY] {datetime.utcnow().isoformat()} - {message}")

def create_notification(db, user_id: int, message: str):
    notification = Notification(user_id=user_id, message=message)
    db.add(notification)
    db.commit() 