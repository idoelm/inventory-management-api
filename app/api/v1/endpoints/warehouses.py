from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import Session

from app.core.db import get_db
from app.schemas.warehouse import WarehouseCreate, WarehouseResponse
from app.crud import warehouse as crud_warehouse

router = APIRouter(prefix="/warehouses", tags=["Warehouses"])


@router.post("/", response_model=WarehouseResponse, status_code=201)
def create_warehouse(warehouse_in: WarehouseCreate, db: Session = Depends(get_db)):
    return crud_warehouse.create_warehouse(db=db, warehouse_in=warehouse_in)


@router.get("/{warehouse_id}", response_model=WarehouseResponse)
def read_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse = crud_warehouse.get_warehouse(db=db, warehouse_id=warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse