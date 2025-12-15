from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from app.config import settings
from typing import Optional, Dict, Any
from jose import jwt, JWTError

# Our secret key and algorithm (from .env)
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

# Configure the password hashing context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    Args:
        password: Plain text password string
    Returns:
        str: Hashed password (safe to store in database)
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password from database
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    Args:
        data: Dictionary to encode in token (usually {"sub": user_email})
        expires_delta: Optional custom expiration time
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    
    # Add expiration to the payload
    to_encode.update({"exp": expire})
    
    # Encode and return the JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify a JWT token.
    Args:
        token: JWT token string
    Returns:
        Dict with token payload if valid, None if invalid/expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None