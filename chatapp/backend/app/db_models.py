from sqlalchemy import Column, Integer, String, Sequence, Boolean, ForeignKey

from .db_settings import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(100))
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, Sequence("chat_id_seq"), primary_key=True)
    name = Column(String(100), unique=True, index=True)
    created_at = Column(Integer)
    created_by = Column(Integer, ForeignKey("users.id"))


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, Sequence("message_id_seq"), primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String(500))
    timestamp = Column(Integer)


class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, Sequence("membership_id_seq"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    chat_id = Column(Integer, ForeignKey("chats.id"))
    role = Column(String(50))
    joined_at = Column(Integer)


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, Sequence("user_settings_id_seq"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    theme = Column(String(50))
    notifications_enabled = Column(Boolean, default=True)
    language = Column(String(50))
