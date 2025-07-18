from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.models import project as project_models, issue as issue_models
from app.schemas import issue as schemas
from app.database import get_db
from app.routes.auth import get_current_user
from datetime import datetime
from typing import Optional
from sqlalchemy import or_
from app.services.notifications import log_notification, create_notification

router = APIRouter()

@router.get("/projects/{project_id}/issues", response_model=list[schemas.IssueOut])
def get_filtered_issues(
    project_id: int,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to: Optional[int] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check if the project exists and is owned by the current user
    project = db.query(project_models.Project).filter_by(id=project_id, created_by=current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    query = db.query(issue_models.Issue).filter_by(project_id=project_id)
    if status:
        query = query.filter(issue_models.Issue.status == status)
    if priority:
        query = query.filter(issue_models.Issue.priority == priority)
    if assigned_to:
        query = query.filter(issue_models.Issue.assigned_to == assigned_to)
    if q:
        query = query.filter(
            or_(
                issue_models.Issue.title.ilike(f"%{q}%"),
                issue_models.Issue.description.ilike(f"%{q}%")
            )
        )
    issues = query.all()
    return issues

@router.post("/projects/{project_id}/issues", response_model=schemas.IssueOut)
def create_issue(
    project_id: int,
    issue: schemas.IssueCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    background_tasks: BackgroundTasks = None
):
    # Ensure the user owns the project
    project = db.query(project_models.Project).filter_by(id=project_id, created_by=current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not authorized")

    new_issue = issue_models.Issue(
        title=issue.title,
        description=issue.description,
        status=issue.status,
        priority=issue.priority,
        assigned_to=issue.assigned_to,
        project_id=project_id,
        created_by=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    if background_tasks:
        if issue.assigned_to is not None:
            background_tasks.add_task(create_notification, db, issue.assigned_to, f"Issue {new_issue.id} assigned to you")
    return new_issue 

@router.get("/issues/{id}", response_model=schemas.IssueOut)
def get_issue_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    issue = db.query(issue_models.Issue).filter_by(id=id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Check if user is project owner or assigned to the issue
    project = db.query(project_models.Project).filter_by(id=issue.project_id).first()
    if not (issue.created_by == current_user.id or issue.assigned_to == current_user.id or (project and project.created_by == current_user.id)):
        raise HTTPException(status_code=403, detail="Not authorized to view this issue")

    return issue 

@router.put("/issues/{id}", response_model=schemas.IssueOut)
def update_issue(
    id: int,
    issue_update: schemas.IssueUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    background_tasks: BackgroundTasks = None
):
    issue = db.query(issue_models.Issue).filter_by(id=id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Check if the current user owns the project
    project = db.query(project_models.Project).filter_by(id=issue.project_id).first()
    if not project or project.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this issue")

    # Track status change
    old_status = issue.status
    # Update only provided fields
    for field, value in issue_update.dict(exclude_unset=True).items():
        setattr(issue, field, value)
    issue.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(issue)
    if background_tasks and issue.status != old_status:
        if issue.assigned_to is not None:
            background_tasks.add_task(create_notification, db, issue.assigned_to, f"Issue {issue.id} status changed to {issue.status.upper()}")
    return issue 

@router.delete("/issues/{id}", status_code=204)
def delete_issue(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    issue = db.query(issue_models.Issue).filter_by(id=id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Check if the current user owns the project
    project = db.query(project_models.Project).filter_by(id=issue.project_id).first()
    if not project or project.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this issue")

    db.delete(issue)
    db.commit()
    # 204 No Content: no return value needed 