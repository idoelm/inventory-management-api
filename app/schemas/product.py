from typing import Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    sku: str
    price: float
    quantity: int = 0
    description: Optional[str] = None
    warehouse_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
    warehouse_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True