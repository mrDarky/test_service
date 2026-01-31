from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Dict, Any
from app.database import get_db
from app.models import User, Project, Task, Message, IPLog, Settings, UserRole, TaskStatus, ProjectStatus
from app.schemas import UserResponse
from app.auth import get_current_admin_user

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/dashboard", response_model=Dict[str, Any])
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    # Count users
    result = await db.execute(select(func.count(User.id)))
    total_users = result.scalar()
    
    result = await db.execute(select(func.count(User.id)).where(User.role == UserRole.CREATOR))
    total_creators = result.scalar()
    
    result = await db.execute(select(func.count(User.id)).where(User.role == UserRole.TESTER))
    total_testers = result.scalar()
    
    # Count projects
    result = await db.execute(select(func.count(Project.id)))
    total_projects = result.scalar()
    
    result = await db.execute(select(func.count(Project.id)).where(Project.status == ProjectStatus.ACTIVE))
    active_projects = result.scalar()
    
    # Count tasks
    result = await db.execute(select(func.count(Task.id)))
    total_tasks = result.scalar()
    
    result = await db.execute(select(func.count(Task.id)).where(Task.status == TaskStatus.OPEN))
    open_tasks = result.scalar()
    
    result = await db.execute(select(func.count(Task.id)).where(Task.status == TaskStatus.COMPLETED))
    completed_tasks = result.scalar()
    
    # Count messages
    result = await db.execute(select(func.count(Message.id)))
    total_messages = result.scalar()
    
    return {
        "users": {
            "total": total_users,
            "creators": total_creators,
            "testers": total_testers
        },
        "projects": {
            "total": total_projects,
            "active": active_projects
        },
        "tasks": {
            "total": total_tasks,
            "open": open_tasks,
            "completed": completed_tasks
        },
        "messages": {
            "total": total_messages
        }
    }

@router.get("/users", response_model=List[UserResponse])
async def list_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    role: UserRole = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    query = select(User)
    
    if role:
        query = query.where(User.role == role)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    
    return users

@router.put("/users/{user_id}/activate")
async def activate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = True
    await db.commit()
    
    return {"message": "User activated successfully"}

@router.put("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate yourself"
        )
    
    user.is_active = False
    await db.commit()
    
    return {"message": "User deactivated successfully"}

@router.get("/ip-logs")
async def get_ip_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    result = await db.execute(
        select(IPLog).order_by(IPLog.timestamp.desc()).offset(skip).limit(limit)
    )
    logs = result.scalars().all()
    
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "ip_address": log.ip_address,
            "action": log.action,
            "timestamp": log.timestamp,
            "user_agent": log.user_agent
        }
        for log in logs
    ]

@router.get("/settings")
async def get_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    result = await db.execute(select(Settings))
    settings = result.scalars().all()
    
    return [
        {
            "id": setting.id,
            "key": setting.key,
            "value": setting.value,
            "description": setting.description,
            "updated_at": setting.updated_at
        }
        for setting in settings
    ]

@router.post("/settings")
async def create_setting(
    key: str,
    value: str,
    description: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    # Check if key already exists
    result = await db.execute(select(Settings).where(Settings.key == key))
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Setting with this key already exists"
        )
    
    setting = Settings(key=key, value=value, description=description)
    db.add(setting)
    await db.commit()
    await db.refresh(setting)
    
    return {
        "id": setting.id,
        "key": setting.key,
        "value": setting.value,
        "description": setting.description
    }

@router.put("/settings/{setting_id}")
async def update_setting(
    setting_id: int,
    value: str,
    description: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    result = await db.execute(select(Settings).where(Settings.id == setting_id))
    setting = result.scalar_one_or_none()
    
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Setting not found"
        )
    
    setting.value = value
    if description is not None:
        setting.description = description
    
    await db.commit()
    await db.refresh(setting)
    
    return {
        "id": setting.id,
        "key": setting.key,
        "value": setting.value,
        "description": setting.description
    }
