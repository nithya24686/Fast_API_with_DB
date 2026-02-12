from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatCreate(BaseModel):
    title: Optional[str] = "New Chat"


class ChatUpdate(BaseModel):
    title: str


class MessageCreate(BaseModel):
    role: str
    content: str


class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatOut(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: List[MessageOut] = []

    class Config:
        from_attributes = True


class ChatListItem(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True
