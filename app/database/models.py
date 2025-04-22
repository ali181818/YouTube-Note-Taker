from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from app.config import DATABASE_URL

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    chat_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    first_use_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=False)
    language = Column(String(10), default="en")
    
    messages = relationship("Message", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.name} ({self.chat_id})>"

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, ForeignKey("users.chat_id"), nullable=False)
    message = Column(Text, nullable=False)
    message_date = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="messages")
    
    def __repr__(self):
        return f"<Message {self.id} from user {self.chat_id}>"

# Create the engine and tables
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()