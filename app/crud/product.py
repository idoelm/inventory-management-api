from sqlmodel import Session, select
from app.models.product import Product
from app.schemas.product import ProductCreate

def get_product(db: Session, product_id: int):
    return db.get(Product, product_id)

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.exec(select(Product).offset(skip).limit(limit)).all()

def create_product(db: Session, product_in: ProductCreate):
    db_product = Product(**product_in.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product