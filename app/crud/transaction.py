from typing import Optional
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.models.product import Product
from app.models.warehouse import Warehouse


def get_transaction(db: Session, transaction_id: int):
    return db.get(Transaction, transaction_id)


def get_transactions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    product_id: Optional[int] = None,
    warehouse_id: Optional[int] = None,
    transaction_type: Optional[str] = None,
):
    query = select(Transaction)

    if product_id is not None:
        query = query.where(Transaction.product_id == product_id)
    if warehouse_id is not None:
        query = query.where(Transaction.warehouse_id == warehouse_id)
    if transaction_type is not None:
        query = query.where(Transaction.transaction_type == transaction_type)

    query = query.offset(skip).limit(limit)
    return db.exec(query).all()


def create_transaction(db: Session, transaction_in: TransactionCreate):
    warehouse = db.get(Warehouse, transaction_in.warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="warehouse not found")

    product = db.get(Product, transaction_in.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    if transaction_in.transaction_type not in ("IN", "OUT"):
        raise HTTPException(
            status_code=400, detail="Invalid transaction_type. Expected 'IN' or 'OUT'"
        )

    if transaction_in.transaction_type == "IN":
        product.quantity += transaction_in.quantity
    elif transaction_in.transaction_type == "OUT":
        if product.quantity < transaction_in.quantity:
            raise HTTPException(
                status_code=400,
                detail="product quantity is smaller than transaction quantity",
            )
        product.quantity -= transaction_in.quantity

    db_transaction = Transaction(**transaction_in.model_dump())
    db.add(product)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction