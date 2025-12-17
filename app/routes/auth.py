from fastapi import APIRouter , HTTPException , status , Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate , UserResponse
from app.schemas.token import Token
from app.utils.security import verify_password , create_access_token , hash_password
from sqlalchemy import or_

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user :UserCreate, db:Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already Used")
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already Used")
    
    hashed_password = hash_password(user.password)
    # now we create the new user
    new_user = User(
        email = user.email,
        username = user.username,
        hashed_password = hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token , status_code=status.HTTP_200_OK)
def login(form_data : OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    existing_user = db.query(User).filter(or_(User.email == form_data.username, User.username == form_data.username )).first()
    
    if existing_user is None:
        raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email/username or password",headers={"WWW-Authenticate": "Bearer"})
        
    if not verify_password(form_data.password, str(existing_user.hashed_password)):
        raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email/username or password",headers={"WWW-Authenticate": "Bearer"})
    data = {"sub": str(existing_user.id)}
    token = create_access_token(data=data)
    
    return {"access_token": token, "token_type": "bearer"}



@router.post("/refresh", status_code=status.HTTP_200_OK , response_model=Token)
def refresh_token(current_user: User = Depends(get_db)):
    data = {"sub": str(current_user.id)}
    token = create_access_token(data=data)
    return {"access_token":token, "token_type" : "bearer"}
     