from datetime import datetime, timezone, date

from sqlalchemy import ForeignKey, DECIMAL, String , UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_user_category'),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    color : Mapped[str | None] = mapped_column()
    icon : Mapped[str | None] = mapped_column()
    
    # Using a lambda for default ensures the time is calculated at insertion
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    # Relationship back to User 
    user = relationship("User", back_populates="categories") 
    transactions = relationship("Transaction", back_populates="category", passive_deletes=True)  # This allows NULL on delete

