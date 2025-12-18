from fastapi import APIRouter , HTTPException , status , Depends
from sqlalchemy.orm import Session
from app.utils.dependencies import get_current_active_user
from app.database import get_db
from app.models.user import User
from app.schemas.user import  UserResponse , UserUpdate

users_router = APIRouter()

@users_router.get("/me", response_model = UserResponse, status_code = status.HTTP_200_OK)
def get_current_user_profile(current_user : User = Depends(get_current_active_user)):
    """
    Get current authenticated user's profile.
    Requires valid JWT token in Authorization header.
    """
    return current_user

@users_router.put("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current authenticated user's profile.
    Can update email and/or username.
    """
    
    # Check if new email is taken by another user
    if user_update.email is not None:
        existing = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        
        # Update the email
        current_user.email = user_update.email
    
    # Check if new username is taken by another user
    if user_update.username is not None:
        existing = db.query(User).filter(
            User.username == user_update.username,
            User.id != current_user.id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already in use"
            )
        
        # Update the username
        current_user.username = user_update.username
    
    # Commit all changes at once
    db.commit()
    db.refresh(current_user)
    
    return current_user


@users_router.delete("/me", status_code=status.HTTP_200_OK)
def delete_current_user_account(current_user: User = Depends(get_current_active_user), 
                                db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted successfully"}
    