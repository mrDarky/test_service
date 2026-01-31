from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from typing import List
from app.database import get_db
from app.models import Message, User
from app.schemas import MessageCreate, MessageResponse
from app.auth import get_current_active_user

router = APIRouter(prefix="/api/messages", tags=["messages"])

@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    message: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Validate receiver if specified
    if message.receiver_id:
        result = await db.execute(select(User).where(User.id == message.receiver_id))
        receiver = result.scalar_one_or_none()
        if not receiver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receiver not found"
            )
    
    db_message = Message(
        sender_id=current_user.id,
        receiver_id=message.receiver_id,
        project_id=message.project_id,
        subject=message.subject,
        content=message.content
    )
    
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    
    return db_message

@router.get("/", response_model=List[MessageResponse])
async def list_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    unread_only: bool = False,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Message).where(
        or_(
            Message.receiver_id == current_user.id,
            Message.sender_id == current_user.id
        )
    )
    
    if unread_only:
        query = query.where(
            and_(
                Message.receiver_id == current_user.id,
                Message.is_read == False
            )
        )
    
    query = query.order_by(Message.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    messages = result.scalars().all()
    
    return messages

@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Check permissions
    if message.sender_id != current_user.id and message.receiver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Mark as read if receiver
    if message.receiver_id == current_user.id and not message.is_read:
        message.is_read = True
        await db.commit()
        await db.refresh(message)
    
    return message

@router.put("/{message_id}/read", status_code=status.HTTP_200_OK)
async def mark_message_read(
    message_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    if message.receiver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    message.is_read = True
    await db.commit()
    
    return {"message": "Message marked as read"}
