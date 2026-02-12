from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from repositories.chat_repo import ChatRepo
from schemas.chat_schemas import ChatCreate, ChatUpdate, ChatOut, ChatListItem, MessageCreate, MessageOut
from utils.jwt_handler import get_current_user
from typing import List

router = APIRouter()


@router.post("/chats", response_model=ChatOut)
def create_chat(
    chat_data: ChatCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new chat for the authenticated user."""
    repo = ChatRepo(db)
    chat = repo.create_chat(user_id=current_user["id"], title=chat_data.title)
    return chat


@router.get("/chats", response_model=List[ChatListItem])
def get_chats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all chats for the authenticated user (for sidebar)."""
    repo = ChatRepo(db)
    return repo.get_chats_by_user(user_id=current_user["id"])


@router.get("/chats/{chat_id}", response_model=ChatOut)
def get_chat(
    chat_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a single chat with all its messages."""
    repo = ChatRepo(db)
    chat = repo.get_chat_by_id(chat_id=chat_id, user_id=current_user["id"])
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.post("/chats/{chat_id}/messages", response_model=MessageOut)
def add_message(
    chat_id: int,
    message_data: MessageCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a message to a chat."""
    repo = ChatRepo(db)
    # Verify the chat belongs to the user
    chat = repo.get_chat_by_id(chat_id=chat_id, user_id=current_user["id"])
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    message = repo.add_message(chat_id=chat_id, role=message_data.role, content=message_data.content)
    return message


@router.put("/chats/{chat_id}", response_model=ChatOut)
def update_chat(
    chat_id: int,
    chat_data: ChatUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a chat's title."""
    repo = ChatRepo(db)
    chat = repo.update_chat_title(chat_id=chat_id, user_id=current_user["id"], title=chat_data.title)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.delete("/chats/{chat_id}")
def delete_chat(
    chat_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a chat and all its messages."""
    repo = ChatRepo(db)
    deleted = repo.delete_chat(chat_id=chat_id, user_id=current_user["id"])
    if not deleted:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Chat deleted successfully"}
