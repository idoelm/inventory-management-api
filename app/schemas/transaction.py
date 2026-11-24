from typing import Optional
from pydantic import BaseModel, Field 

class TransactionBase(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int = Field(..., gt=0)
    transaction_type: str
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    product_id: Optional[int] = None
    warehouse_id: Optional[int] = None
    quantity: Optional[int] = Field(default=None, gt=0)
    transaction_type: Optional[str] = None
    notes: Optional[str] = None

class TransactionResponse(TransactionBase):
    id: int

    class Config:
        from_attributes = True