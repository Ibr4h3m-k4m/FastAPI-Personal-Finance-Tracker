from fastapi import APIRouter , HTTPException , status , Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.utils.dependencies import get_current_active_user
from app.database import get_db
from app.models.user import User
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse , CategoryUpdate

router = APIRouter()


@router.get("/categories", response_model = list[CategoryResponse], status_code = status.HTTP_200_OK)
def get_current_user_categories(current_user : User = Depends(get_current_active_user),db:Session = Depends(get_db)):
    """This end point is to get all categories of the current user."""      
    categories = db.query(Category).filter(Category.user_id == current_user.id).all()
    return categories   


@router.post("/categories", response_model = CategoryResponse, status_code = status.HTTP_201_CREATED)
def create_new_category(category : CategoryCreate,db:Session = Depends(get_db),
                        current_user:User = Depends(get_current_active_user) ):
    """This end point is to create a new category for the current user."""
    try:
        new_category = Category(
            user_id = current_user.id,
            name = category.name,
            color = category.color,
            icon = category.icon
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists"
        )
    
@router.get("/categories/{category_id}", response_model = CategoryResponse, status_code = status.HTTP_200_OK)
def get_current_user_category(category_id:int, current_user : User = Depends(get_current_active_user),db:Session = Depends(get_db)):
    """This end point is to get a specific category of the current user."""      
    category = db.query(Category).filter(
        Category.user_id == current_user.id, 
        Category.id == category_id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found"
        )
    return category


@router.put("/categories/{category_id}", response_model = CategoryResponse, status_code = status.HTTP_200_OK)
def update_category(category : CategoryUpdate,category_id:int,db:Session = Depends(get_db),
                        current_user:User = Depends(get_current_active_user) ):
    """This end point is to update a category's information for the current user."""
    db_category = db.query(Category).filter(
        Category.user_id == current_user.id, 
        Category.id == category_id
    ).first()
    
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found"
        )
    
    try:
        # Get only the fields that were provided
        update_dict = category.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists"
        )


@router.delete("/categories/{category_id}", status_code = status.HTTP_200_OK)
def delete_category(category_id:int,current_user : User = Depends(get_current_active_user),
                                  db:Session = Depends(get_db)):
    """Delete a category and set all its transactions' category_id to NULL. (
    this function was declared in the SQLAlchemy ORM model)"""
    category = db.query(Category).filter(
        Category.user_id == current_user.id, 
        Category.id == category_id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found"
        )
    
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}



"""
When to use if/else vs try/except:
Use if/else for:
✅ Expected conditions - checking if something exists, ownership validation, business logic

"Does this category exist?"
"Does this belong to the user?"
"Is this field empty?"

Why? These are normal control flow, not errors. More readable and explicit.
Use try/except for:
✅ Unexpected errors - database constraints, network issues, actual exceptions

Database unique constraint violations
Database connection errors
Type conversion errors

Why? These are exceptional situations. Easier to let the database/library handle the check rather than pre-validate everything.
In your code:
Ownership checks (if/else): Predictable - you're checking if query returned None. Clear intent.
Duplicate names (try/except): Let the database enforce it via UniqueConstraint. Catches the IntegrityError. Cleaner than checking beforehand.
General rule: Don't use exceptions for control flow, use them for actual exceptional situations!
"""