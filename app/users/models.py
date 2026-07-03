from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), nullable=False)
    password = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tasks = relationship("TaskModel", back_populates="user")

    def __repr__(self):
        return f"user => username: {self.username}, email: {self.email}"


class TokenModel(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("UserModel", uselist=False)
