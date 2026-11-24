from typing import Optional
from sqlmodel import SQLModel, Field

class WarehouseBase(SQLModel):
    name: str = Field(index=True)
    location: Optional[str] = None

class Warehouse(WarehouseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)