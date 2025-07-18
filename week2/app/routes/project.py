from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import project as project_models
from app.schemas import project as project_schemas
from app.routes.auth import get_current_user
from app.models.user import User, Role
from app.core.dependencies import require_admin

router = APIRouter()

@router.post("/projects", response_model=project_schemas.ProjectOut)
def create_project(
    project_data: project_schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new project for the authenticated user.
    """
    new_project = project_models.Project(
        name=project_data.name,
        description=project_data.description,
        created_by=current_user.id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/projects", response_model=list[project_schemas.ProjectOut])
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all projects created by the authenticated user, or all if admin.
    """
    if current_user.role == Role.admin:
        user_projects = db.query(project_models.Project).all()
    else:
        user_projects = db.query(project_models.Project).filter(project_models.Project.created_by == current_user.id).all()
    return user_projects

@router.get("/projects/{project_id}", response_model=project_schemas.ProjectOut)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a single project by ID (admins can access all, others only their own).
    """
    if current_user.role == Role.admin:
        project = db.query(project_models.Project).filter(project_models.Project.id == project_id).first()
    else:
        project = db.query(project_models.Project).filter(
            project_models.Project.id == project_id,
            project_models.Project.created_by == current_user.id
        ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/projects/{project_id}", response_model=project_schemas.ProjectOut)
def update_project(
    project_id: int,
    updated_data: project_schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a project (name or description) if the user owns it or is admin.
    """
    if current_user.role == Role.admin:
        project = db.query(project_models.Project).filter(project_models.Project.id == project_id).first()
    else:
        project = db.query(project_models.Project).filter(
            project_models.Project.id == project_id,
            project_models.Project.created_by == current_user.id
        ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.name = updated_data.name
    project.description = updated_data.description
    db.commit()
    db.refresh(project)
    return project

@router.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete a project (admin only).
    """
    project = db.query(project_models.Project).filter(
        project_models.Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"detail": "Project deleted successfully"} 