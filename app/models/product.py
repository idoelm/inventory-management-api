from typing import Optional
from sqlmodel import SQLModel, Field

class ProductBase(SQLModel):
    name: str = Field(index=True)
    sku: str = Field(unique=True, index=True)
    price: float
    quantity: int = Field(default=0)
    description: Optional[str] = None
    warehouse_id: Optional[int] = Field(default=None, foreign_key="warehouse.id")
class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)