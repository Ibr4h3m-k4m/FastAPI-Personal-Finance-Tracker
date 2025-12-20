from pydantic import BaseModel, ConfigDict, EmailStr, field_validator , model_validator
from typing import Optional
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from datetime import timezone
from pydantic import Field

from app.models.transaction import TransactionType

# For Creating a new transaction
class TransactionCreate(BaseModel):
    amount: Decimal
    description: Optional[str] = Field(None, max_length=500)
    transaction_type: TransactionType
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        max_future = now + timedelta(days=30)
        if v > max_future:
            raise ValueError('Transaction date cannot be more than 30 days in the future')
        return v

# For updating a transaction
class TransactionUpdate(BaseModel):
    amount: Optional[Decimal] = None
    description: Optional[str] = Field(None, max_length=500)
    transaction_type: Optional[TransactionType] = None

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v

    @model_validator(mode='after')
    def check_at_least_one_field(self):
        # At least one must be provided
        if self.amount is None and self.description is None and self.transaction_type is None:
            raise ValueError('Must provide at least one field to update')
        return self

# For API responses
class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: Decimal
    description: Optional[str] = None
    transaction_type: TransactionType
    date: datetime 
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)  # Allows SQLAlchemy model conversion