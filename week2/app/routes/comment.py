from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.models.issue import Issue
from app.schemas.comment import CommentCreate, CommentOut
from app.database import get_db
from app.routes.auth import get_current_user
from app.services.notifications import log_notification, create_notification
from datetime import datetime

router = APIRouter()

@router.post("/issues/{id}/comments", response_model=CommentOut)
def create_comment(
    id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    background_tasks: BackgroundTasks = None
):
    # Ensure the issue exists
    issue = db.query(Issue).filter_by(id=id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    new_comment = Comment(
        content=comment.content,
        issue_id=id,
        user_id=current_user.id,
        timestamp=datetime.utcnow()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    if background_tasks:
        # Notify the issue owner (created_by)
        issue = db.query(Issue).filter_by(id=id).first()
        if issue:
            background_tasks.add_task(create_notification, db, issue.created_by, f"New comment added on Issue {id}")
    return new_comment

@router.get("/issues/{id}/comments", response_model=list[CommentOut])
def get_comments(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Ensure the issue exists
    issue = db.query(Issue).filter_by(id=id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    comments = db.query(Comment).filter_by(issue_id=id).order_by(Comment.timestamp).all()
    return comments 