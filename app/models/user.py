from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base
from datetime import datetime , timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    # Relationship back to Transactions and cascade delete in case the user deleted its profile 
    transactions = relationship("Transaction", back_populates="user",cascade="all, delete-orphan")
    # Relationship back to Categories and cascade delete in case the user deleted its profile 
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
