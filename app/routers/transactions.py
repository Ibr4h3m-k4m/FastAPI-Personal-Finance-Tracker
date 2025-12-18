from fastapi import APIRouter , HTTPException , status , Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from app.utils.dependencies import get_current_active_user
from app.database import get_db
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import  TransactionResponse , TransactionCreate , TransactionUpdate

router = APIRouter()

@router.get("/transactions", response_model = list[TransactionResponse], status_code = status.HTTP_200_OK)
def get_current_user_transactions(skip:int=0,limit:int=100,current_user : User = Depends(get_current_active_user),db:Session = Depends(get_db)):
    """
    Get current_user from the dependency 
    filter transactions by user_id.
    and then return the transactions of the user.
    """
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).offset(skip).limit(limit).all()
    return transactions

@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction :TransactionCreate, db:Session = Depends(get_db),current_user : User = Depends(get_current_active_user)):
    """
    Check for the current_user from the dependency (no user no new transaction)
    check for the fields needed
    and then return the added transaction of the user.
    """
    new_transaction = Transaction(
       user_id = current_user.id,
       amount = transaction.amount,
       description = transaction.description,
       transaction_type = transaction.transaction_type,
       date = transaction.date
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    return new_transaction


@router.get("/transactions/{id}", response_model = TransactionResponse, status_code = status.HTTP_200_OK)
def get_current_user_transaction_by_id(id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    Get current_user from the dependency 
    filter transactions by user_id.
    and then return the transaction with the provided id of the current user.
    """
    try:
        transaction = db.query(Transaction).filter(Transaction.user_id == current_user.id, Transaction.id == id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Not found")
        return transaction
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
    

@router.put("/transactions/{id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
def update_current_user_transaction_by_id(
    id: int,
    transaction_update: TransactionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        transaction = db.query(Transaction).filter(
            Transaction.user_id == current_user.id,
            Transaction.id == id
        ).first()
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Get only the fields that were provided
        update_dict = transaction_update.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(transaction, key, value)
        db.commit()
        db.refresh(transaction)
        
        return transaction
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


    

@router.delete("/transactions/{id}", status_code = status.HTTP_200_OK)
def delete_transaction(id:int,current_user : User = Depends(get_current_active_user),
                                  db:Session = Depends(get_db)):
    """
    Get current_user from the dependency 
    filter transactions by user_id.
    and then delete the transactions of the user.
    """
    try:
        transaction_to_delete = db.query(Transaction).filter(Transaction.user_id == current_user.id, Transaction.id == id).first()
        if not transaction_to_delete:
            raise HTTPException(status_code=404, detail="Not found")
        db.delete(transaction_to_delete)
        db.commit()
        return {"message": "Transaction was deleted successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
    