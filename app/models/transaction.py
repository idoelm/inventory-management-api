from typing import Optional
from sqlmodel import SQLModel, Field

class TransactionBase(SQLModel):
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
    warehouse_id: Optional[int] = Field(default=None, foreign_key="warehouse.id")
    quantity: int
    transaction_type: str
    notes: Optional[str] = None

class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)