from typing import Optional
from pydantic import BaseModel

class WarehouseBase(BaseModel):
    name: str
    location: Optional[str] = None

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

class WarehouseResponse(WarehouseBase):
    id: int

    class Config:
        from_attributes = True