from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    """
    Response schema for login endpoint.
    Returns JWT access token and token type.
    """
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """
    Schema for decoded JWT token payload.
    Used for validating token data in dependencies.
    """
    user_id: Optional[int] = None 