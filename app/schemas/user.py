from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

# Base schema with common fields
class UserBase(BaseModel):
    email: EmailStr
    username: str

# For registration
class UserCreate(UserBase):
    password: str

# For login
class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str
    
    @field_validator('email', 'username')
    @classmethod
    def check_email_or_username(cls, v, info):
        # At least one must be provided
        if info.data.get('email') is None and info.data.get('username') is None:
            raise ValueError('Must provide either email or username')
        return v

# For updating profile
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None

# For API responses
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows SQLAlchemy model conversion