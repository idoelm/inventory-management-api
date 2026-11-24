from sqlmodel import Session, select
from app.models.warehouse import Warehouse
from app.schemas.warehouse import WarehouseCreate

def get_warehouse(db: Session, warehouse_id: int):
    return db.get(Warehouse, warehouse_id)

def get_warehouses(db: Session, skip: int = 0, limit: int = 100):
    return db.exec(select(Warehouse).offset(skip).limit(limit)).all()

def create_warehouse(db: Session, warehouse_in: WarehouseCreate):
    db_warehouse = Warehouse(**warehouse_in.model_dump())
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse
