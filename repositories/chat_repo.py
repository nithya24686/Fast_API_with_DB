from sqlalchemy.orm import Session
from models import Chat, Message


class ChatRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_chat(self, user_id: int, title: str = "New Chat") -> Chat:
        chat = Chat(user_id=user_id, title=title)
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def get_chats_by_user(self, user_id: int) -> list[Chat]:
        return (
            self.db.query(Chat)
            .filter(Chat.user_id == user_id)
            .order_by(Chat.created_at.desc())
            .all()
        )

    def get_chat_by_id(self, chat_id: int, user_id: int) -> Chat | None:
        return (
            self.db.query(Chat)
            .filter(Chat.id == chat_id, Chat.user_id == user_id)
            .first()
        )

    def add_message(self, chat_id: int, role: str, content: str) -> Message:
        message = Message(chat_id=chat_id, role=role, content=content)
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def update_chat_title(self, chat_id: int, user_id: int, title: str) -> Chat | None:
        chat = self.get_chat_by_id(chat_id, user_id)
        if chat:
            chat.title = title
            self.db.commit()
            self.db.refresh(chat)
        return chat

    def delete_chat(self, chat_id: int, user_id: int) -> bool:
        chat = self.get_chat_by_id(chat_id, user_id)
        if chat:
            self.db.delete(chat)
            self.db.commit()
            return True
        return False
