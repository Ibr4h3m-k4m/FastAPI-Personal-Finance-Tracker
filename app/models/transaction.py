import enum
from datetime import datetime, timezone, date
from decimal import Decimal
from sqlalchemy import ForeignKey, Enum as SQLAlchemyEnum, DECIMAL, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

# Inheriting from str ensures it works well with Pydantic/JSON
class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), index=True)
    
    description: Mapped[str | None] = mapped_column(String)
    
    # The Enum Column
    # We pass the Python Enum class to the SQLAlchemy Enum type
    transaction_type: Mapped[TransactionType] = mapped_column(
        SQLAlchemyEnum(TransactionType), 
        nullable=False
    )
    # Using a lambda for default ensures the time is calculated at insertion
    date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc).date())
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    # Relationship back to User (if you have a User model)
    user = relationship("User", back_populates="transactions")