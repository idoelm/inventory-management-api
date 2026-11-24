from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional

from app.core.db import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.crud import transaction as crud_transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(
    transaction_in: TransactionCreate,
    db: Session = Depends(get_db),
):
    return crud_transaction.create_transaction(db=db, transaction_in=transaction_in)


@router.get("/", response_model=List[TransactionResponse])
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    product_id: Optional[int] = Query(default=None),
    warehouse_id: Optional[int] = Query(default=None),
    transaction_type: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    return crud_transaction.get_transactions(
        db=db,
        skip=skip,
        limit=limit,
        product_id=product_id,
        warehouse_id=warehouse_id,
        transaction_type=transaction_type,
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
def read_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    db_transaction = crud_transaction.get_transaction(db=db, transaction_id=transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction