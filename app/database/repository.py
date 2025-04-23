from datetime import datetime
from sqlalchemy.orm import Session
from app.database.models import User, Message, get_db

class UserRepository:
    @staticmethod
    def get_user(db: Session, chat_id: int):
        """Get user by chat ID"""
        return db.query(User).filter(User.chat_id == chat_id).first()
    
    @staticmethod
    def create_user(db: Session, chat_id: int, name: str, language: str = "en", is_active: bool = False):
        """Create a new user"""
        user = User(
            chat_id=chat_id,
            name=name,
            first_use_date=datetime.utcnow(),
            is_active=is_active,
            language=language
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update_user_active_status(db: Session, chat_id: int, is_active: bool):
        """Update user active status"""
        user = UserRepository.get_user(db, chat_id)
        if user:
            user.is_active = is_active
            db.commit()
            db.refresh(user)
            return user
        return None
    
    @staticmethod
    def update_user_language(db: Session, chat_id: int, language: str):
        """Update user language preference"""
        user = UserRepository.get_user(db, chat_id)
        if user:
            user.language = language
            db.commit()
            db.refresh(user)
            return user
        return None

class MessageRepository:
    @staticmethod
    def create_message(db: Session, message_id: int, chat_id: int, message: str):
        """Create a new message record"""
        message_obj = Message(
            message_id=message_id,
            chat_id=chat_id,
            message=message,
            message_date=datetime.utcnow()
        )
        db.add(message_obj)
        db.commit()
        db.refresh(message_obj)
        return message_obj
    
    @staticmethod
    def get_user_messages(db: Session, chat_id: int, limit: int = 10):
        """Get recent messages for a user"""
        return db.query(Message).filter(
            Message.chat_id == chat_id
        ).order_by(Message.message_date.desc()).limit(limit).all()